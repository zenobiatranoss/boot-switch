def normalize_path(value):
    return value.replace("\\", "/").lower().lstrip("/")

def is_windows_loader(path):
    return normalize_path(path) == "efi/microsoft/boot/bootmgfw.efi"

def is_linux_loader(path):
    path = normalize_path(path)
    return path in {
        "efi/ubuntu/shimx64.efi",
        "efi/ubuntu/grubx64.efi",
        "efi/debian/shimx64.efi",
        "efi/debian/grubx64.efi",
        "efi/mx/grubx64.efi",
        "efi/mx/shimx64.efi",
        "efi/fedora/shimx64.efi",
        "efi/fedora/grubx64.efi",
        "efi/arch/grubx64.efi",
        "efi/linux/grubx64.efi"
    }

def is_windows_entry(entry):
    text = (entry.get("details", "") + " " + entry.get("path", "")).lower()
    return "windows boot manager" in text or is_windows_loader(entry.get("path", ""))

def is_linux_entry(entry):
    text = (entry.get("details", "") + " " + entry.get("path", "")).lower()
    return (
        "ubuntu" in text
        or "debian" in text
        or "fedora" in text
        or "arch" in text
        or "linux" in text
        or is_linux_loader(entry.get("path", ""))
    )

def find_windows(entries):
    return [x for x in entries.values() if is_windows_entry(x)]

def find_linux(entries):
    return [x for x in entries.values() if is_linux_entry(x)]
