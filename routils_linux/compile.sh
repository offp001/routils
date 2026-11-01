#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

PYTHON="$ROOT/venv/bin/python"
if [[ ! -x "$PYTHON" ]]; then
    printf '%s\n' 'error: The project virtual environment is missing. run ./install.sh first.' >&2
    exit 1
fi

if [[ ! -f "$ROOT/main.pyw" || ! -f "$ROOT/routils_rpc.png" || ! -f "$ROOT/routils.ico" ]]; then
    printf '%s\n' 'error: One or more required project files are missing.' >&2
    exit 1
fi

"$PYTHON" "$ROOT/luau_interpreter/download_cli.py" "$ROOT/bin/luau"
"$PYTHON" -m compileall -q main.pyw sober_support.py ai cache client console emote_manager fflag history home plugins release_notes server_viewer settings subplace themes viewer sober_proxy autoupdate luau_interpreter
rm -rf "$ROOT/build" "$ROOT/dist" "$ROOT/routils.spec"
"$PYTHON" -m PyInstaller --clean --noconfirm --onefile --windowed --name routils --paths "$ROOT" --add-data "$ROOT/routils.ico:." --add-data "$ROOT/routils_rpc.png:." --add-data "$ROOT/src/presets:src/presets" --add-binary "$ROOT/bin/luau:bin" --collect-all sv_ttk --collect-all ttkbootstrap --hidden-import pynput.keyboard._xorg --hidden-import pynput.mouse._xorg main.pyw

if [[ ! -x "$ROOT/dist/routils" ]]; then
    printf '%s\n' 'error: The compiled executable was not created.' >&2
    exit 1
fi

chmod +x "$ROOT/dist/routils"
printf '%s\n' 'build completed. start the compiled executable with ./dist/routils.'
