# Contributing to RoUtils

Thank you for your interest in contributing to **RoUtils**! Contributions, bug reports, suggestions, and improvements are welcome.

<p align="center">
  <a href="https://github.com/offp001/routils"><img src="https://img.shields.io/badge/GitHub-RoUtils-black?logo=github" alt="GitHub"></a>
  <a href="https://offp001.github.io/routilsw/"><img src="https://img.shields.io/badge/Website-Visit-blue?logo=googlechrome" alt="Website"></a>
  <a href="https://discord.com/invite/849VtrYhm2"><img src="https://img.shields.io/badge/Discord-Community-5865F2?logo=discord&logoColor=white" alt="Discord"></a>
</p>

<p align="center">
  If you like RoUtils, please consider giving the repository a star.
</p>

<p align="center">
  <a href="https://github.com/offp001/routils">GitHub Repository</a> ·
  <a href="https://github.com/offp001/routils/issues">Issues</a> ·
  <a href="https://discord.com/invite/849VtrYhm2">Discord Support</a>
</p>

---

## Table of Contents

- [Requirements](#requirements)
- [Compilation on Windows](#compilation-on-windows)
  - [Easy Method](#easy-method)
  - [Normal Method](#normal-method)
- [Compilation on Linux](#compilation-on-linux)
  - [Requirements](#linux-requirements)
  - [Install Requirements](#install-requirements)
  - [Easy Method](#linux-easy-method)
  - [Normal Method](#linux-normal-method)
- [Reporting Issues](#reporting-issues)
- [Community and Website](#community-and-website)

---

## Requirements

- **Python 3.12 or newer** for the Windows build instructions.
- Git, if you plan to clone the repository.
- A compatible Python environment and the dependencies listed in `requirements.txt`.

When installing Python on Windows, enable **Add Python to PATH** so that Python and pip can be accessed from the terminal.

---

# Compilation on Windows

## Easy Method

The included scripts automate the installation and compilation process.

1. Run `install_requirements.bat` to install the required dependencies.
2. Once installation finishes, run `compile.bat`.
3. Wait for the compilation process to complete.
4. Open the generated `dist` folder.
5. Run `RoUtils.exe`.

## Normal Method

If you prefer to compile RoUtils manually, follow these steps.

### 1. Open a terminal

Open CMD or PowerShell in the project directory.

### 2. Install dependencies

Verify that Python 3.12 or newer and pip are available, then run:

```bash
pip install -r requirements.txt
```

### 3. Compile RoUtils

Run the following command:

```bash
py -3.12 -m PyInstaller --noconfirm --clean --onefile --windowed --icon=routils.ico --add-data "routils.ico;." --name=RoUtils main.pyw
```

### 4. Run the compiled application

After compilation finishes, navigate to the output directory:

```powershell
cd dist
```

Run RoUtils from the terminal:

```powershell
.\RoUtils.exe
```

Alternatively, open the `dist` folder in File Explorer and double-click `RoUtils.exe`.

---

# Compilation on Linux

## Linux Requirements

- Python 3.10 or newer
- Tkinter
- Python virtual environment support
- Required packages listed in the installation instructions below

## Install Requirements

### Debian and Ubuntu

```bash
sudo apt update
sudo apt install python3 python3-venv python3-tk python3-pip
```

### Fedora

```bash
sudo dnf install python3 python3-tkinter python3-pip
```

### Arch Linux

```bash
sudo pacman -S python tk python-pip
```

## Linux Easy Method

Extract the complete project directory and open a terminal inside it.

Make the scripts executable and run the installation and compilation scripts:

```bash
chmod +x install.sh run.sh compile.sh
./install.sh
./compile.sh
```

After compilation completes, run the generated executable:

```bash
chmod +x dist/routils
./dist/routils
```

## Linux Normal Method

### 1. Create a virtual environment

```bash
python3 -m venv venv
```

### 2. Activate the environment

```bash
source venv/bin/activate
```

### 3. Upgrade pip

```bash
python -m pip install --upgrade pip
```

### 4. Install dependencies

```bash
python -m pip install numpy DracoPy Pillow lz4 zstandard sv-ttk ttkbootstrap pypresence psutil pynput cryptography 'mitmproxy>=11,<13' pyinstaller
```

### 5. Check Python syntax

```bash
python -m compileall -q main.pyw sober_support.py ai cache client console emote_manager fflag history home plugins release_notes server_viewer settings subplace themes viewer sober_proxy
```

### 6. Build the executable

```bash
python -m PyInstaller --clean --noconfirm --onefile --windowed --name routils --paths "$PWD" --add-data "$PWD/routils.ico:." --add-data "$PWD/routils_rpc.png:." --collect-all sv_ttk --collect-all ttkbootstrap --hidden-import pynput.keyboard._xorg --hidden-import pynput.mouse._xorg main.pyw
```

### 7. Grant execution permission

```bash
chmod +x dist/routils
```

### 8. Run RoUtils

```bash
./dist/routils
```

---

## Reporting Issues

If you encounter a bug, have a suggestion, or want to request a feature, use the GitHub issue tracker.

- [Report a Bug](https://github.com/offp001/routils/issues/new)
- [Request a Feature](https://github.com/offp001/routils/issues/new)
- [View Existing Issues](https://github.com/offp001/routils/issues)

When reporting a bug, include relevant error messages, steps to reproduce the issue, and details about your operating system and Python version when applicable.

---

<p align="center">
  <sub>RoUtils by offp001</sub>
</p>
