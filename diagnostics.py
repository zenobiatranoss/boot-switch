import os
import shutil
from command import run

def collect():
    result = {}

    result["efi_mode"] = os.path.isdir("/sys/firmware/efi")
    result["efibootmgr"] = shutil.which("efibootmgr") or ""
    result["pkexec"] = shutil.which("pkexec") or ""
    result["mokutil"] = shutil.which("mokutil") or ""

    if result["mokutil"]:
        code, out, err = run(["mokutil", "--sb-state"])
        result["secure_boot"] = out or err
    else:
        result["secure_boot"] = "unknown"

    code, out, err = run(["lsblk", "-f"])
    result["storage"] = out or err

    return result
