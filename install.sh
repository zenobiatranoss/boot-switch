#!/bin/sh
set -e

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
mkdir -p "$HOME/.local/share/applications"

sed "s|__BOOT_SWITCH_PATH__|$SCRIPT_DIR|g" \
    "$SCRIPT_DIR/BootSwitch.desktop" \
    > "$HOME/.local/share/applications/BootSwitch.desktop"

chmod +x "$SCRIPT_DIR/run.sh"

echo "Boot Switch installed."
