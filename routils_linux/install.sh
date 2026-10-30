#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

PYTHON="$(command -v python3 || command -v python || true)"
if [[ -z "$PYTHON" ]]; then
    printf '%s\n' 'Error: Python 3 is required. Install Python and its venv support first.' >&2
    exit 1
fi

if ! "$PYTHON" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)'; then
    printf '%s\n' 'Error: Python 3.10 or newer is required.' >&2
    exit 1
fi

"$PYTHON" -m venv venv
source "$ROOT/venv/bin/activate"
python -m pip install --upgrade pip
python -m pip install numpy DracoPy Pillow lz4 zstandard sv-ttk ttkbootstrap pypresence psutil pynput cryptography 'mitmproxy>=11,<13' pyinstaller
printf '%s\n' 'Installation complete. Run ./run.sh to start RoUtils.'
