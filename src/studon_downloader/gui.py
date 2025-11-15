"""Tkinter user interface for the StudOn Downloader."""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from .core import download_pdfs


class StudOnDownloaderApp:
    """Encapsulates the Tkinter GUI widgets and event handlers."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("StudOn PDF Downloader")
        self.root.resizable(False, False)
        self.root.configure(bg="#e0e0e0")

        self.url_var = tk.StringVar()
        self.folder_var = tk.StringVar()
        self.cookie_name_var = tk.StringVar(value="PHPSESSID")
        self.cookie_value_var = tk.StringVar()

        self._build_layout()

    # ------------------------------------------------------------------
    # Tkinter wiring
    # ------------------------------------------------------------------
    def _build_layout(self) -> None:
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(1, weight=1)

        ttk.Label(main_frame, text="StudOn URL:").grid(
            row=0, column=0, sticky="w", pady=3
        )
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=60)
        url_entry.grid(row=0, column=1, columnspan=2, sticky="ew", pady=3)

        ttk.Label(main_frame, text="Target folder:").grid(
            row=1, column=0, sticky="w", pady=3
        )
        folder_entry = ttk.Entry(main_frame, textvariable=self.folder_var, width=60)
        folder_entry.grid(row=1, column=1, sticky="ew", pady=3)

        browse_button = ttk.Button(
            main_frame, text="Browse…", command=self._choose_target_folder
        )
        browse_button.grid(row=1, column=2, sticky="w", padx=(5, 0), pady=3)

        ttk.Label(main_frame, text="Cookie name:").grid(
            row=2, column=0, sticky="w", pady=3
        )
        ttk.Entry(
            main_frame, textvariable=self.cookie_name_var, width=30
        ).grid(row=2, column=1, sticky="w", pady=3)

        ttk.Label(main_frame, text="Cookie value:").grid(
            row=3, column=0, sticky="w", pady=3
        )
        ttk.Entry(
            main_frame, textvariable=self.cookie_value_var, width=60, show="*"
        ).grid(row=3, column=1, columnspan=2, sticky="ew", pady=3)

        cookie_help = (
            "How to find cookie name & value:\n"
            "- Log in to StudOn in your browser.\n"
            "- Press F12 → open Developer Tools.\n"
            "- Chrome/Edge: tab 'Application' → 'Cookies' → your StudOn URL.\n"
            "- Firefox: tab 'Storage' → 'Cookies'.\n"
            "- Look for a session cookie (e.g. 'PHPSESSID', 'ILIAS_LOGIN', etc.).\n"
            "- Copy its name into 'Cookie name' and its value into 'Cookie value'."
        )
        ttk.Label(main_frame, text=cookie_help, justify="left").grid(
            row=4, column=0, columnspan=3, sticky="w", pady=(5, 10)
        )

        self.start_button = ttk.Button(
            main_frame, text="Start download", command=self._on_start
        )
        self.start_button.grid(row=5, column=0, columnspan=3, pady=(0, 5))

        ttk.Label(main_frame, text="Log:").grid(row=6, column=0, sticky="nw", pady=(5, 0))

        log_frame = ttk.Frame(main_frame)
        log_frame.grid(row=6, column=1, columnspan=2, sticky="nsew", pady=(5, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.log_text = tk.Text(
            log_frame, width=70, height=15, state="disabled", wrap="word", bg="#f5f5f5"
        )
        log_scroll = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scroll.set)
        self.log_text.grid(row=0, column=0, sticky="nsew")
        log_scroll.grid(row=0, column=1, sticky="ns")

        url_entry.focus()

    # ------------------------------------------------------------------
    # UI helpers
    # ------------------------------------------------------------------
    def _append_log(self, message: str) -> None:
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message)
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _choose_target_folder(self) -> None:
        folder = filedialog.askdirectory(title="Choose target folder")
        if folder:
            self.folder_var.set(folder)

    def _validate_inputs(self) -> bool:
        if not self.url_var.get().strip():
            messagebox.showwarning("Missing input", "Please enter a StudOn URL.")
            return False
        if not self.folder_var.get().strip():
            messagebox.showwarning("Missing input", "Please choose a target folder.")
            return False
        if not self.cookie_name_var.get().strip() or not self.cookie_value_var.get().strip():
            messagebox.showwarning(
                "Missing input", "Please enter cookie name and value."
            )
            return False
        return True

    # ------------------------------------------------------------------
    # Event handling
    # ------------------------------------------------------------------
    def _on_start(self) -> None:
        if not self._validate_inputs():
            return

        self.start_button.config(state="disabled")
        self._append_log("Starting download…\n\n")

        try:
            download_pdfs(
                base_url=self.url_var.get().strip(),
                output_dir=self.folder_var.get().strip(),
                cookie_name=self.cookie_name_var.get().strip(),
                cookie_value=self.cookie_value_var.get().strip(),
                log_func=self._append_log,
            )
        except Exception as exc:  # pragma: no cover - UI only
            self._append_log(f"\nUnexpected error in download: {exc}\n")
            messagebox.showerror(
                "Unexpected error", f"An unexpected error occurred:\n{exc}"
            )
        finally:
            self.start_button.config(state="normal")

    # ------------------------------------------------------------------
    def run(self) -> None:
        self.root.mainloop()


def create_gui() -> StudOnDownloaderApp:
    """Return a configured :class:`StudOnDownloaderApp`."""

    app = StudOnDownloaderApp()
    return app


__all__ = ["StudOnDownloaderApp", "create_gui"]
