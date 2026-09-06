import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

from config import APP_NAME
from security import check_password
from system_report import build_report, build_report_text
from operations import hide_linux, set_windows_primary


class App:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("940x800")
        self.root.resizable(False, False)
        self.root.configure(bg="#c8c8c8")

        self.code = tk.StringVar()

        self.setup_style()
        self.build_ui()
        self.scan()

    def setup_style(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "TButton",
            font=("TkDefaultFont", 10),
            padding=(20, 11),
            background="#e8e8e8",
            foreground="#111111",
            borderwidth=1
        )

        style.map(
            "TButton",
            background=[
                ("active", "#d9e8f7"),
                ("pressed", "#c8dcef")
            ]
        )

        style.configure(
            "Primary.TButton",
            background="#d8eafa",
            foreground="#102a43"
        )

        style.map(
            "Primary.TButton",
            background=[
                ("active", "#bddaf2"),
                ("pressed", "#a9cdea")
            ]
        )

        style.configure(
            "Danger.TButton",
            background="#f7e2e2",
            foreground="#7a1515"
        )

        style.map(
            "Danger.TButton",
            background=[
                ("active", "#efcccc"),
                ("pressed", "#e6b5b5")
            ]
        )

        style.configure(
            "TEntry",
            fieldbackground="#ffffff",
            foreground="#111111",
            borderwidth=1,
            padding=7
        )

    def build_ui(self):
        outer = tk.Frame(
            self.root,
            bg="#c8c8c8"
        )
        outer.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=14
        )

        header = tk.Frame(
            outer,
            bg="#b8b8b8",
            highlightbackground="#b6b6b6",
            highlightthickness=1
        )
        header.pack(fill="x")

        tk.Label(
            header,
            text="BOOT SWITCH",
            font=("TkDefaultFont", 18, "bold"),
            fg="#181818",
            bg="#b8b8b8"
        ).pack(
            side="left",
            padx=14,
            pady=10
        )

        tk.Label(
            header,
            text="UEFI Windows / Linux Boot Manager",
            font=("TkDefaultFont", 10),
            fg="#444444",
            bg="#b8b8b8"
        ).pack(
            side="left",
            padx=(4, 0),
            pady=12
        )

        info = tk.Frame(
            outer,
            bg="#c3c3c3",
            highlightbackground="#aac5dc",
            highlightthickness=1
        )
        info.pack(
            fill="x",
            pady=(10, 10)
        )

        tk.Label(
            info,
            text="WARNING",
            font=("TkDefaultFont", 10, "bold"),
            fg="#303030",
            bg="#c3c3c3"
        ).pack(
            anchor="w",
            padx=14,
            pady=(9, 2)
        )

        tk.Label(
            info,
            text=(
                "This tool changes UEFI boot entries. "
                "Make sure Windows Boot Manager is available before continuing."
            ),
            justify="left",
            anchor="w",
            wraplength=920,
            font=("TkDefaultFont", 9),
            fg="#383838",
            bg="#c3c3c3"
        ).pack(
            fill="x",
            padx=14,
            pady=(0, 9)
        )

        report_card = tk.Frame(
            outer,
            bg="#d8d8d8",
            highlightbackground="#b8b8b8",
            highlightthickness=1
        )
        report_card.pack(
            fill="both",
            expand=True
        )

        report_header = tk.Frame(
            report_card,
            bg="#b8b8b8"
        )
        report_header.pack(fill="x")

        tk.Label(
            report_header,
            text="BOOT ENTRIES AND CONFIGURATION",
            font=("TkDefaultFont", 9, "bold"),
            fg="#202020",
            bg="#b8b8b8"
        ).pack(
            anchor="w",
            padx=12,
            pady=8
        )

        self.report = scrolledtext.ScrolledText(
            report_card,
            wrap="word",
            bg="#d8d8d8",
            fg="#181818",
            insertbackground="#111111",
            selectbackground="#b8d8f0",
            selectforeground="#111111",
            relief="flat",
            borderwidth=0,
            font=("DejaVu Sans Mono", 10),
            padx=14,
            pady=12
        )
        self.report.pack(
            fill="both",
            expand=True,
            padx=1,
            pady=(0, 1)
        )

        bottom = tk.Frame(
            outer,
            bg="#c8c8c8"
        )
        bottom.pack(
            fill="x",
            pady=(12, 0)
        )

        code_box = tk.LabelFrame(
            bottom,
            text=" Confirmation ",
            bg="#c8c8c8",
            fg="#222222",
            padx=10,
            pady=8
        )
        code_box.pack(side="left")

        tk.Label(
            code_box,
            text="Code:",
            bg="#c8c8c8",
            fg="#202020"
        ).pack(side="left")

        ttk.Entry(
            code_box,
            textvariable=self.code,
            show="*",
            width=20
        ).pack(
            side="left",
            padx=(8, 8)
        )

        ttk.Button(
            code_box,
            text="Verify",
            command=self.scan
        ).pack(side="left", ipadx=12, ipady=4)

        actions = tk.Frame(
            bottom,
            bg="#c8c8c8"
        )
        actions.pack(side="right", padx=(0, 4), pady=8, ipadx=35)

        style = ttk.Style()
        style.configure(
            "LargeDanger.TButton",
            font=("TkDefaultFont", 11, "bold"),
            padding=(34, 14),
            background="#d6bcbc",
            foreground="#6d1515"
        )
        style.map(
            "LargeDanger.TButton",
            background=[
                ("active", "#cbaaaa"),
                ("pressed", "#bf9999")
            ]
        )

        ttk.Button(
            actions,
            text="Hide Linux + Windows",
            style="LargeDanger.TButton",
            command=self.hide
        ).pack(
            side="left",
            padx=(0, 10)
        )

        ttk.Button(
            actions,
            text="Windows Only",
            style="Primary.TButton",
            command=self.windows_only
        ).pack(side="left")

        tk.Label(
            outer,
            text="The Code 1999",
            font=("TkDefaultFont", 8),
            fg="#4a4a4a",
            bg="#c8c8c8"
        ).pack(
            anchor="w",
            pady=(8, 0)
        )

    def set_report(self, text):
        self.report.delete("1.0", "end")
        self.report.insert("1.0", text)

    def scan(self):
        self.root.update_idletasks()

        try:
            build_report()
            self.set_report(build_report_text())

        except Exception as e:
            self.set_report(str(e))

    def windows_only(self):
        if not check_password(self.code.get()):
            messagebox.showerror(
                APP_NAME,
                "Invalid confirmation code."
            )
            return

        if not messagebox.askyesno(
            APP_NAME,
            "Set Windows as the first UEFI boot entry?"
        ):
            return

        try:
            order = set_windows_primary()

            messagebox.showinfo(
                APP_NAME,
                "Windows is now first in BootOrder.\n\n"
                + " → ".join(order)
            )

            self.scan()

        except Exception as e:
            messagebox.showerror(APP_NAME, str(e))

    def hide(self):
        if not check_password(self.code.get()):
            messagebox.showerror(
                APP_NAME,
                "Invalid confirmation code."
            )
            return

        report = build_report()

        if not report["safe"]:
            messagebox.showerror(
                APP_NAME,
                report["reason"]
            )
            return

        if not messagebox.askyesno(
            APP_NAME,
            "This will:\n\n"
            "1. Back up the UEFI configuration\n"
            "2. Put Windows first\n"
            "3. Remove detected Linux UEFI entries\n\n"
            "Linux files and partitions will NOT be deleted.\n\n"
            "Continue?"
        ):
            return

        try:
            result = hide_linux()

            messagebox.showinfo(
                APP_NAME,
                "Operation completed.\n\n"
                f"Backup:\n{result['backup']}\n\n"
                f"Deleted entries:\n"
                f"{', '.join(result['deleted'])}\n\n"
                f"Windows: {result['windows']}"
            )

            self.scan()

        except Exception as e:
            messagebox.showerror(
                APP_NAME,
                f"Operation failed:\n\n{e}"
            )


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
