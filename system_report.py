from diagnostics import collect
from operations import preview

def build_report():
    diagnostics = collect()

    if not diagnostics["efi_mode"]:
        return {
            "safe": False,
            "reason": "System is not running in UEFI mode",
            "diagnostics": diagnostics
        }

    try:
        state = preview()
    except Exception as e:
        return {
            "safe": False,
            "reason": str(e),
            "diagnostics": diagnostics
        }

    if len(state["windows"]) != 1:
        return {
            "safe": False,
            "reason": "Exactly one Windows Boot Manager entry is required",
            "state": state,
            "diagnostics": diagnostics
        }

    if not state["linux"]:
        return {
            "safe": False,
            "reason": "No Linux boot entry was found",
            "state": state,
            "diagnostics": diagnostics
        }

    return {
        "safe": True,
        "reason": "System passed the UEFI safety checks",
        "state": state,
        "diagnostics": diagnostics
    }

def build_report_text():
    report = build_report()

    lines = [
        "Boot Switch",
        "",
        f"Safe: {report['safe']}",
        f"Reason: {report['reason']}"
    ]

    state = report.get("state")

    if state:
        lines.append("")
        lines.append("Windows:")
        for item in state["windows"]:
            lines.append(f"  {item['id']} {item['details']}")

        lines.append("")
        lines.append("Linux:")
        for item in state["linux"]:
            lines.append(f"  {item['id']} {item['details']}")

        lines.append("")
        lines.append("Current BootOrder:")
        lines.append("  " + " ".join(state["current"]))

        lines.append("")
        lines.append("After hide:")
        lines.append("  " + " ".join(state["desired"]))

    return "\n".join(lines)
