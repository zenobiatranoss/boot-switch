#!/bin/sh
set -e

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

if [ "$(id -u)" -eq 0 ]; then
    exec python3 "$SCRIPT_DIR/main.py"
fi

if command -v pkexec >/dev/null 2>&1; then
    exec pkexec env DISPLAY="${DISPLAY:-}" \
        XAUTHORITY="${XAUTHORITY:-}" \
        WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-}" \
        XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-}" \
        python3 "$SCRIPT_DIR/main.py"
fi

echo "ERROR: pkexec is required."
exit 1
