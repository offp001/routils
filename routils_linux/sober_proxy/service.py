import json
import os
import re
import shutil
import socket
import ssl
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

from sober_support import sober_data_root, sober_flatpak_running

SOBER_APP_ID = "org.vinegarhq.Sober"
PROXY_HOST = "127.0.0.1"
PROXY_PORT = 58443
IGNORE_HOSTS = r".*"
INTERCEPT_DELAY_SECONDS = 20.0


class ProxyPortInUseError(RuntimeError):
    def __init__(self, port, pid=None, process_name=None, can_terminate=False):
        self.port = int(port)
        self.pid = int(pid) if pid else None
        self.process_name = str(process_name or "Unknown process")
        self.can_terminate = bool(can_terminate)
        if self.pid:
            message = f"127.0.0.1:{self.port} is already in use by {self.process_name} (PID {self.pid})."
        else:
            message = f"127.0.0.1:{self.port} is already in use, but RoUtils could not identify its owner."
        super().__init__(message)


class SoberProxyService:
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir).expanduser().resolve()
        self.root = self.data_dir / "sober_proxy"
        self.confdir = self.root / "mitmproxy"
        self.ca_key_path = self.confdir / "mitmproxy-ca.pem"
        self.ca_cert_path = self.confdir / "mitmproxy-ca-cert.pem"
        self.log_path = self.root / "proxy.log"
        self.pid_path = self.root / "proxy.pid"
        self.backup_path = self.root / "overlay-backup.json"
        self.overlay_path = sober_data_root() / "asset_overlay" / "ssl" / "cacert.pem"

    def _load_overlay_backup(self):
        try:
            return json.loads(self.backup_path.read_text(encoding="utf-8"))
        except (OSError, ValueError, TypeError):
            return None

    def _write_bytes_atomic(self, path, payload):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(path.name + ".tmp")
        temporary.write_bytes(payload)
        os.replace(temporary, path)

    def _make_ca(self):
        self.confdir.mkdir(parents=True, exist_ok=True)
        if self.ca_key_path.is_file() and self.ca_cert_path.is_file():
            try:
                key = serialization.load_pem_private_key(self.ca_key_path.read_bytes(), password=None)
                cert = x509.load_pem_x509_certificate(self.ca_cert_path.read_bytes())
                if key.public_key().public_numbers() == cert.public_key().public_numbers():
                    return self.ca_cert_path.read_bytes()
            except Exception:
                pass
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        subject = x509.Name([
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "RoUtils"),
            x509.NameAttribute(NameOID.COMMON_NAME, "RoUtils Sober Proxy CA"),
        ])
        now = datetime.now(timezone.utc)
        not_before = (now - timedelta(minutes=5)).replace(tzinfo=None)
        not_after = (now + timedelta(days=3650)).replace(tzinfo=None)
        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(subject)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(not_before)
            .not_valid_after(not_after)
            .add_extension(x509.BasicConstraints(ca=True, path_length=1), critical=True)
            .add_extension(x509.KeyUsage(digital_signature=False, content_commitment=False, key_encipherment=False, data_encipherment=False, key_agreement=False, key_cert_sign=True, crl_sign=True, encipher_only=False, decipher_only=False), critical=True)
            .add_extension(x509.SubjectKeyIdentifier.from_public_key(key.public_key()), critical=False)
            .sign(key, hashes.SHA256())
        )
        key_pem = key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.TraditionalOpenSSL, serialization.NoEncryption())
        cert_pem = cert.public_bytes(serialization.Encoding.PEM)
        self._write_bytes_atomic(self.ca_key_path, key_pem + cert_pem)
        self._write_bytes_atomic(self.ca_cert_path, cert_pem)
        return cert_pem

    def _system_ca_bundle(self):
        candidates = []
        default = ssl.get_default_verify_paths().cafile
        if default:
            candidates.append(Path(default))
        candidates.extend((Path("/etc/ssl/certs/ca-certificates.crt"), Path("/etc/pki/tls/certs/ca-bundle.crt"), Path("/etc/ssl/cert.pem")))
        for path in candidates:
            try:
                content = path.read_bytes()
                if b"-----BEGIN CERTIFICATE-----" in content:
                    return content
            except OSError:
                continue
        raise FileNotFoundError("A system CA certificate bundle could not be found.")

    def _patch_overlay(self, ca_pem):
        self.root.mkdir(parents=True, exist_ok=True)
        self.overlay_path.parent.mkdir(parents=True, exist_ok=True)
        backup = self._load_overlay_backup()
        if backup is None:
            existed = self.overlay_path.is_file()
            original_copy = self.root / "overlay-cacert.original.pem"
            if existed:
                shutil.copy2(self.overlay_path, original_copy)
                base = original_copy.read_bytes()
            else:
                base = self._system_ca_bundle()
            backup = {"overlay_path": str(self.overlay_path), "existed": existed, "backup_file": str(original_copy) if existed else ""}
            self._write_bytes_atomic(self.backup_path, json.dumps(backup, ensure_ascii=False, indent=2).encode("utf-8"))
        elif backup.get("existed"):
            backup_file = Path(str(backup.get("backup_file", "")))
            base = backup_file.read_bytes() if backup_file.is_file() else self.overlay_path.read_bytes()
        else:
            base = self._system_ca_bundle()
        normalized_ca = ca_pem.strip()
        if normalized_ca not in base:
            if base and not base.endswith(b"\n"):
                base += b"\n"
            base += normalized_ca + b"\n"
        self._write_bytes_atomic(self.overlay_path, base)

    def _restore_overlay(self):
        backup = self._load_overlay_backup()
        if backup is None:
            return
        target = Path(str(backup.get("overlay_path") or self.overlay_path))
        if backup.get("existed"):
            backup_file = Path(str(backup.get("backup_file") or ""))
            if not backup_file.is_file():
                return
            self._write_bytes_atomic(target, backup_file.read_bytes())
        else:
            try:
                target.unlink()
            except FileNotFoundError:
                pass
            try:
                target.parent.rmdir()
            except OSError:
                pass
        try:
            self.backup_path.unlink()
        except OSError:
            pass
        backup_file = Path(str(backup.get("backup_file") or ""))
        if backup_file.is_file():
            try:
                backup_file.unlink()
            except OSError:
                pass

    def _verified_proxy_pid(self):
        try:
            pid = int(self.pid_path.read_text(encoding="ascii").strip())
        except (OSError, ValueError):
            return 0
        try:
            command = (Path("/proc") / str(pid) / "cmdline").read_bytes().replace(b"\0", b" ").decode("utf-8", "replace")
        except OSError:
            return 0
        if str(Path(__file__).with_name("mitm_addon.py").resolve()) not in command:
            return 0
        return pid

    def is_running(self):
        pid = self._verified_proxy_pid()
        if not pid:
            return False
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False

    def _port_owner(self, port=PROXY_PORT):
        filter_expression = f"sport = :{int(port)}"
        commands = []
        sudo = shutil.which("sudo")
        ss = shutil.which("ss")
        pkexec = shutil.which("pkexec")
        if sudo and ss:
            commands.append(([sudo, "-n", ss, "-lptn", filter_expression], 3))
        if ss:
            commands.append(([ss, "-lptn", filter_expression], 3))
        if pkexec and ss and hasattr(os, "getuid") and os.getuid() != 0:
            commands.append(([pkexec, ss, "-lptn", filter_expression], 15))
        for command, timeout in commands:
            try:
                result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout, check=False)
            except (OSError, subprocess.SubprocessError):
                continue
            if result.returncode != 0:
                continue
            for line in result.stdout.splitlines():
                if "LISTEN" not in line:
                    continue
                match = re.search(r'users:\(\("([^"\\]+)",pid=(\d+)', line)
                if not match:
                    continue
                name = match.group(1)
                pid = int(match.group(2))
                try:
                    owner_uid = os.stat(f"/proc/{pid}").st_uid
                    can_terminate = hasattr(os, "getuid") and owner_uid == os.getuid() and pid > 1 and pid != os.getpid()
                except OSError:
                    can_terminate = False
                return {"pid": pid, "name": name or "Unknown process", "can_terminate": can_terminate}
        try:
            import psutil
        except ImportError:
            return None
        try:
            connections = psutil.net_connections(kind="tcp")
        except (OSError, psutil.Error):
            return None
        for connection in connections:
            address = getattr(connection, "laddr", None)
            if not address or getattr(address, "port", None) != int(port):
                continue
            if connection.status != psutil.CONN_LISTEN:
                continue
            pid = getattr(connection, "pid", None)
            if not pid:
                return {"pid": None, "name": "Unknown process", "can_terminate": False}
            try:
                process = psutil.Process(pid)
                name = process.name()
                can_terminate = bool(hasattr(os, "getuid") and process.uids().real == os.getuid() and pid > 1 and pid != os.getpid())
                return {"pid": int(pid), "name": name, "can_terminate": can_terminate}
            except (psutil.Error, OSError, ValueError):
                return {"pid": int(pid), "name": "Unknown process", "can_terminate": False}
        return None

    def terminate_port_owner(self, pid, port=PROXY_PORT):
        try:
            import psutil
        except ImportError as error:
            raise RuntimeError("Process inspection requires psutil.") from error
        try:
            target_pid = int(pid)
            if target_pid <= 1 or target_pid == os.getpid():
                raise RuntimeError("RoUtils will not terminate a protected or current process.")
            owner = self._port_owner(port)
            if not owner or owner.get("pid") != target_pid:
                raise RuntimeError("The selected process no longer owns the requested listening port.")
            process = psutil.Process(target_pid)
            try:
                owner_uid = os.stat(f"/proc/{target_pid}").st_uid
            except OSError:
                owner_uid = None
            if hasattr(os, "getuid") and owner_uid == os.getuid():
                process.terminate()
                try:
                    process.wait(timeout=4)
                except psutil.TimeoutExpired as error:
                    raise RuntimeError("The process did not exit after a termination request.") from error
                return
            pkexec = shutil.which("pkexec")
            kill = shutil.which("kill") or "/usr/bin/kill"
            if not pkexec:
                raise RuntimeError("The process belongs to another user. Install or enable polkit (pkexec) to request permission to close it.")
            result = subprocess.run([pkexec, kill, "-TERM", str(target_pid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=15, check=False)
            if result.returncode != 0:
                detail = result.stderr.strip() or result.stdout.strip() or "The privileged termination request was not approved."
                raise RuntimeError(detail)
            try:
                process.wait(timeout=4)
            except psutil.TimeoutExpired as error:
                raise RuntimeError("The process did not exit after a termination request.") from error
        except psutil.NoSuchProcess:
            return
        except psutil.AccessDenied as error:
            raise RuntimeError("Permission was denied while inspecting or terminating the port owner.") from error

    def _wait_for_listener(self, process, timeout=10):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if process.poll() is not None:
                return False
            try:
                with socket.create_connection((PROXY_HOST, PROXY_PORT), timeout=0.25):
                    return True
            except OSError:
                time.sleep(0.1)
        return False

    def start_and_launch(self):
        if not sys.platform.startswith("linux"):
            raise RuntimeError("The FFlag proxy is available only on Linux.")
        if sober_flatpak_running():
            raise RuntimeError("Sober is already running. Close Sober completely, then try again so it inherits the proxy environment.")
        flatpak = shutil.which("flatpak")
        executable_dir = Path(sys.executable).resolve().parent
        project_candidates = [executable_dir.parent, executable_dir, Path.cwd()]
        project_root = next((candidate for candidate in project_candidates if (candidate / "sober_proxy" / "mitm_addon.py").is_file()), Path(__file__).resolve().parent.parent)
        mitmdump_candidates = [project_root / "venv" / "bin" / "mitmdump", executable_dir / "mitmdump"]
        local_mitmdump = next((candidate for candidate in mitmdump_candidates if candidate.is_file() and os.access(candidate, os.X_OK)), None)
        mitmdump = str(local_mitmdump) if local_mitmdump else shutil.which("mitmdump")
        if not flatpak:
            raise FileNotFoundError("The flatpak command was not found.")
        if not mitmdump:
            raise FileNotFoundError("mitmdump was not found. Install the mitmproxy dependency from requirements.txt.")
        info = subprocess.run([flatpak, "info", SOBER_APP_ID], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, timeout=10)
        if info.returncode != 0:
            raise FileNotFoundError("The Sober Flatpak (org.vinegarhq.Sober) installation was not found.")
        self.root.mkdir(parents=True, exist_ok=True)
        proxy_pid = self._verified_proxy_pid()
        if not self.is_running():
            proxy_pid = 0
            probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                probe.bind((PROXY_HOST, PROXY_PORT))
            except OSError as error:
                owner = self._port_owner(PROXY_PORT) or {}
                raise ProxyPortInUseError(
                    PROXY_PORT,
                    owner.get("pid"),
                    owner.get("name", "Unknown process"),
                    owner.get("can_terminate", False),
                ) from error
            finally:
                probe.close()
            ca_pem = self._make_ca()
            self._patch_overlay(ca_pem)
            log_stream = open(self.log_path, "ab", buffering=0)
            addon_path = project_root / "sober_proxy" / "mitm_addon.py"
            if not addon_path.is_file():
                addon_path = Path(__file__).with_name("mitm_addon.py").resolve()
            command = [
                mitmdump,
                "--quiet",
                "--listen-host", PROXY_HOST,
                "--listen-port", str(PROXY_PORT),
                "--set", f"confdir={self.confdir}",
                "--set", f"ignore_hosts={IGNORE_HOSTS}",
                "--set", "connection_strategy=lazy",
                "--set", "http2_ping_keepalive=30",
                "--set", "tcp_timeout=600",
                "-s", str(addon_path),
            ]
            environment = os.environ.copy()
            project_root = str(project_root)
            previous_pythonpath = environment.get("PYTHONPATH", "")
            environment["PYTHONPATH"] = project_root + (os.pathsep + previous_pythonpath if previous_pythonpath else "")
            environment["ROUTILS_FFLAGS_PATH"] = str(self.data_dir / "routils_fflags.json")
            environment["ROUTILS_SOBER_INTERCEPT_DELAY"] = str(INTERCEPT_DELAY_SECONDS)
            process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=log_stream, stderr=log_stream, env=environment, start_new_session=True)
            log_stream.close()
            if not self._wait_for_listener(process):
                try:
                    process.terminate()
                    process.wait(timeout=2)
                except Exception:
                    try:
                        process.kill()
                    except Exception:
                        pass
                log_stream.close()
                self._restore_overlay()
                raise RuntimeError(f"Proxy failed to start. Log: {self.log_path}")
            proxy_pid = process.pid
            self._write_bytes_atomic(self.pid_path, str(proxy_pid).encode("ascii"))
        else:
            try:
                with socket.create_connection((PROXY_HOST, PROXY_PORT), timeout=1):
                    pass
            except OSError as error:
                raise RuntimeError("A proxy PID file exists, but the proxy port is not listening.") from error
        proxy_url = f"http://{PROXY_HOST}:{PROXY_PORT}"
        with open(self.log_path, "ab", buffering=0) as launch_log:
            launch = subprocess.Popen([
                flatpak,
                "run",
                f"--env=HTTP_PROXY={proxy_url}",
                f"--env=HTTPS_PROXY={proxy_url}",
                f"--env=http_proxy={proxy_url}",
                f"--env=https_proxy={proxy_url}",
                f"--env=ALL_PROXY={proxy_url}",
                f"--env=all_proxy={proxy_url}",
                "--env=NO_PROXY=127.0.0.1,localhost,::1",
                "--env=no_proxy=127.0.0.1,localhost,::1",
                SOBER_APP_ID,
            ], stdin=subprocess.DEVNULL, stdout=launch_log, stderr=launch_log, start_new_session=True)
        time.sleep(0.75)
        if launch.poll() is not None and not sober_flatpak_running():
            try:
                self.stop()
            except Exception:
                pass
            raise RuntimeError(f"Sober failed to start. Log: {self.log_path}")
        return {"proxy_pid": proxy_pid, "launch_pid": launch.pid, "port": PROXY_PORT, "overlay_path": str(self.overlay_path), "log_path": str(self.log_path)}

    def stop(self):
        if sober_flatpak_running():
            raise RuntimeError("Close Sober completely before stopping the proxy; stopping it during a game session may disconnect the client.")
        pid = self._verified_proxy_pid()
        if not pid:
            try:
                with socket.create_connection((PROXY_HOST, PROXY_PORT), timeout=0.25):
                    raise RuntimeError("The proxy port is in use, but RoUtils could not verify its process. The CA overlay was left unchanged.")
            except OSError:
                pass
        if pid:
            try:
                os.kill(pid, 15)
            except OSError:
                pass
            deadline = time.monotonic() + 5
            while time.monotonic() < deadline:
                try:
                    os.kill(pid, 0)
                    time.sleep(0.1)
                except OSError:
                    break
            try:
                os.kill(pid, 0)
                os.kill(pid, 9)
            except OSError:
                pass
        try:
            self.pid_path.unlink()
        except OSError:
            pass
        self._restore_overlay()
        return not bool(pid)
