import unittest
from unittest.mock import patch

from detector import (
    is_windows_loader,
    is_linux_loader,
    is_windows_entry,
    is_linux_entry
)
from uefi import parse, order
from operations import preview

SAMPLE = r"""BootCurrent: 0003
Timeout: 0 seconds
BootOrder: 0003,0004,0005
Boot0003* MX Linux HD(1,GPT,AAAA)/File(\EFI\MX\SHIMX64.EFI)
Boot0004* Windows Boot Manager HD(2,GPT,BBBB)/File(\EFI\Microsoft\Boot\bootmgfw.efi)
Boot0005* UEFI OS HD(1,GPT,AAAA)/File(\EFI\BOOT\BOOTX64.EFI)
"""

NO_WINDOWS = r"""BootCurrent: 0003
Timeout: 0 seconds
BootOrder: 0003,0005
Boot0003* MX Linux HD(1,GPT,AAAA)/File(\EFI\MX\SHIMX64.EFI)
Boot0005* UEFI OS HD(1,GPT,AAAA)/File(\EFI\BOOT\BOOTX64.EFI)
"""

TWO_WINDOWS = r"""BootCurrent: 0003
Timeout: 0 seconds
BootOrder: 0003,0004,0006
Boot0003* MX Linux HD(1,GPT,AAAA)/File(\EFI\MX\SHIMX64.EFI)
Boot0004* Windows Boot Manager HD(2,GPT,BBBB)/File(\EFI\Microsoft\Boot\bootmgfw.efi)
Boot0006* Windows Boot Manager HD(3,GPT,CCCC)/File(\EFI\Microsoft\Boot\bootmgfw.efi)
"""

class Tests(unittest.TestCase):

    def test_windows_loader(self):
        self.assertTrue(
            is_windows_loader(
                r"\EFI\Microsoft\Boot\bootmgfw.efi"
            )
        )

    def test_linux_loader(self):
        self.assertTrue(
            is_linux_loader(
                r"\EFI\MX\SHIMX64.EFI"
            )
        )

    def test_parse_realistic_uefi(self):
        entries = parse(SAMPLE)
        self.assertEqual(len(entries), 3)
        self.assertIn("Boot0003", entries)
        self.assertIn("Boot0004", entries)
        self.assertIn("Boot0005", entries)

    def test_boot_order(self):
        self.assertEqual(
            order(SAMPLE),
            ["Boot0003", "Boot0004", "Boot0005"]
        )

    def test_windows_detection(self):
        entries = parse(SAMPLE)
        self.assertTrue(
            is_windows_entry(entries["Boot0004"])
        )

    def test_linux_detection(self):
        entries = parse(SAMPLE)
        self.assertTrue(
            is_linux_entry(entries["Boot0003"])
        )

    def test_windows_and_linux_detection(self):
        entries = parse(SAMPLE)

        windows = [
            x for x in entries.values()
            if is_windows_entry(x)
        ]

        linux = [
            x for x in entries.values()
            if is_linux_entry(x)
        ]

        self.assertEqual(len(windows), 1)
        self.assertEqual(len(linux), 1)
        self.assertEqual(windows[0]["id"], "Boot0004")
        self.assertEqual(linux[0]["id"], "Boot0003")

    def test_windows_first_simulation(self):
        entries = parse(SAMPLE)
        current = order(SAMPLE)

        windows = [
            x for x in entries.values()
            if is_windows_entry(x)
        ]

        windows_id = windows[0]["id"]
        desired = [
            x for x in current
            if x != windows_id
        ]

        desired.insert(0, windows_id)

        self.assertEqual(
            desired,
            ["Boot0004", "Boot0003", "Boot0005"]
        )

    def test_hide_linux_simulation(self):
        entries = parse(SAMPLE)
        current = order(SAMPLE)

        linux = [
            x for x in entries.values()
            if is_linux_entry(x)
        ]

        windows = [
            x for x in entries.values()
            if is_windows_entry(x)
        ]

        linux_ids = {x["id"] for x in linux}
        windows_id = windows[0]["id"]

        desired = [
            x for x in current
            if x not in linux_ids
        ]

        desired.remove(windows_id)
        desired.insert(0, windows_id)

        self.assertEqual(
            desired,
            ["Boot0004", "Boot0005"]
        )

    def test_no_windows(self):
        entries = parse(NO_WINDOWS)

        windows = [
            x for x in entries.values()
            if is_windows_entry(x)
        ]

        self.assertEqual(len(windows), 0)

    def test_multiple_windows(self):
        entries = parse(TWO_WINDOWS)

        windows = [
            x for x in entries.values()
            if is_windows_entry(x)
        ]

        self.assertEqual(len(windows), 2)

    def test_linux_is_not_windows(self):
        entries = parse(SAMPLE)

        self.assertFalse(
            is_windows_entry(entries["Boot0003"])
        )

    def test_windows_is_not_linux(self):
        entries = parse(SAMPLE)

        self.assertFalse(
            is_linux_entry(entries["Boot0004"])
        )

    def test_no_real_uefi_commands(self):
        with patch("operations.raw") as mocked:
            mocked.return_value = SAMPLE

            state = preview()

            mocked.assert_called_once()
            self.assertEqual(
                state["windows"][0]["id"],
                "Boot0004"
            )

if __name__ == "__main__":
    unittest.main(verbosity=2)
