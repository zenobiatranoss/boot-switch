import hashlib
import json
import os
import time
from uefi import raw, parse, order, current, next_boot

BACKUP_DIR = os.path.expanduser("~/.local/share/boot-switch/backups")

def create():
    os.makedirs(BACKUP_DIR, exist_ok=True)

    data = {
        "timestamp": int(time.time()),
        "raw": raw(),
        "entries": parse(),
        "order": order(),
        "current": current(),
        "next": next_boot()
    }

    encoded = json.dumps(data, indent=2, sort_keys=True)
    data["checksum"] = hashlib.sha256(encoded.encode()).hexdigest()

    filename = os.path.join(
        BACKUP_DIR,
        f"uefi-{int(time.time())}.json"
    )

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    return filename

def latest():
    if not os.path.isdir(BACKUP_DIR):
        return None

    files = [
        os.path.join(BACKUP_DIR, x)
        for x in os.listdir(BACKUP_DIR)
        if x.endswith(".json")
    ]

    return max(files, key=os.path.getmtime) if files else None

def load(path=None):
    path = path or latest()
    if not path:
        raise FileNotFoundError("No UEFI backup found")

    with open(path) as f:
        return json.load(f)
