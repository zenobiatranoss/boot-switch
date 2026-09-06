import re
from command import run

def available():
    return run(["test", "-d", "/sys/firmware/efi"])[0] == 0

def raw():
    code, out, err = run(["efibootmgr", "-v"])
    if code != 0:
        raise RuntimeError(err or "efibootmgr failed")
    return out

def parse(raw_output=None):
    raw_output = raw_output if raw_output is not None else raw()
    entries = {}

    for line in raw_output.splitlines():
        match = re.match(r"^(Boot[0-9A-Fa-f]{4})(\*?)\s+(.+)$", line)
        if not match:
            continue

        number = match.group(1)
        active = bool(match.group(2))
        details = match.group(3).strip()

        path = ""
        path_match = re.search(r"/File\((.*?)\)", details, re.I)
        if path_match:
            path = path_match.group(1)

        entries[number] = {
            "id": number,
            "active": active,
            "details": details,
            "path": path
        }

    return entries

def order(raw_output=None):
    raw_output = raw_output if raw_output is not None else raw()
    match = re.search(r"BootOrder:\s*([0-9A-Fa-f,]+)", raw_output)
    if not match:
        return []
    return ["Boot" + x.upper() for x in match.group(1).split(",")]

def current(raw_output=None):
    raw_output = raw_output if raw_output is not None else raw()
    match = re.search(r"BootCurrent:\s*([0-9A-Fa-f]{4})", raw_output)
    return "Boot" + match.group(1).upper() if match else None

def next_boot(raw_output=None):
    raw_output = raw_output if raw_output is not None else raw()
    match = re.search(r"BootNext:\s*([0-9A-Fa-f]{4})", raw_output)
    return "Boot" + match.group(1).upper() if match else None

def set_order(entries):
    values = []
    for entry in entries:
        if not re.fullmatch(r"Boot[0-9A-Fa-f]{4}", entry):
            raise ValueError("Invalid boot entry")
        values.append(entry[4:].upper())

    if not values:
        raise ValueError("Boot order cannot be empty")

    code, out, err = run(["efibootmgr", "-o", ",".join(values)])
    if code != 0:
        raise RuntimeError(err or out or "Failed to set BootOrder")

def delete(entry):
    if not re.fullmatch(r"Boot[0-9A-Fa-f]{4}", entry):
        raise ValueError("Invalid boot entry")

    code, out, err = run(["efibootmgr", "-b", entry[4:], "-B"])
    if code != 0:
        raise RuntimeError(err or out or f"Failed to delete {entry}")

def create(disk, partition, label, loader):
    code, out, err = run([
        "efibootmgr",
        "-c",
        "-d", disk,
        "-p", str(partition),
        "-L", label,
        "-l", loader
    ])

    if code != 0:
        raise RuntimeError(err or out or "Failed to create boot entry")

    return parse(raw())
