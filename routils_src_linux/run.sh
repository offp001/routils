#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [[ -x "$ROOT/dist/routils" ]]; then
    exec "$ROOT/dist/routils" "$@"
fi

if [[ ! -f "$ROOT/venv/bin/activate" ]]; then
    printf '%s\n' 'Error: The virtual environment was not found. Run ./install.sh first.' >&2
    exit 1
fi

source "$ROOT/venv/bin/activate"
exec python main.pyw "$@"
