from backup import create
from detector import find_linux, find_windows
from uefi import raw, parse, order, set_order, delete

def preview():
    output = raw()
    entries = parse(output)
    current_order = order(output)

    windows = find_windows(entries)
    linux = find_linux(entries)

    desired = [x for x in current_order if x not in {e["id"] for e in linux}]

    for entry in windows:
        if entry["id"] in desired:
            desired.remove(entry["id"])
        desired.insert(0, entry["id"])

    return {
        "windows": windows,
        "linux": linux,
        "current": current_order,
        "desired": desired
    }

def hide_linux():
    state = preview()

    if len(state["windows"]) != 1:
        raise RuntimeError("Exactly one Windows boot entry is required")

    if not state["linux"]:
        raise RuntimeError("No Linux boot entry was found")

    backup = create()

    set_order(state["desired"])

    deleted = []

    for entry in state["linux"]:
        delete(entry["id"])
        deleted.append(entry["id"])

    verify = parse(raw())

    remaining_linux = find_linux(verify)
    windows = find_windows(verify)

    if remaining_linux:
        raise RuntimeError("Linux boot entry still exists after operation")

    if not windows:
        raise RuntimeError("Windows boot entry disappeared")

    final_order = order()

    if final_order[0] != windows[0]["id"]:
        raise RuntimeError("Windows is not first in BootOrder")

    return {
        "backup": backup,
        "deleted": deleted,
        "windows": windows[0]["id"],
        "order": final_order
    }

def set_windows_primary():
    state = preview()

    if len(state["windows"]) != 1:
        raise RuntimeError("Exactly one Windows boot entry is required")

    windows = state["windows"][0]["id"]
    new_order = [windows] + [x for x in state["current"] if x != windows]

    set_order(new_order)

    return new_order
