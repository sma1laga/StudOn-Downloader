import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import tkinter as tk
from tkinter import ttk, filedialog, messagebox


def sanitize_filename(name: str) -> str:
    """Replace problematic characters in a filename."""
    name = name.split("/")[-1].split("\\")[-1]
    name = name.split("?")[0].split("#")[0]
    return re.sub(r"[^\w\-.]", "_", name)


def download_pdfs(base_url, output_dir, cookie_name, cookie_value, log_func):
    """
    Download all PDF / download links from base_url into output_dir.
    log_func(msg: str) is used to write status messages into the UI.
    """
    try:
        session = requests.Session()
        # Set cookie via header (no need to care about domain)
        session.headers.update({"Cookie": f"{cookie_name}={cookie_value}"})

        log_func("Fetching StudOn page…\n")
        try:
            resp = session.get(base_url)
            resp.raise_for_status()
        except requests.RequestException as e:
            log_func(f"Error loading page: {e}\n")
            messagebox.showerror("Error", f"Could not load the page:\n{e}")
            return

        soup = BeautifulSoup(resp.text, "html.parser")

        pdf_links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            href_lower = href.lower()

            # Heuristic: PDFs and typical download links
            if ".pdf" in href_lower or "sendfile" in href_lower or "download" in href_lower:
                full_url = urljoin(base_url, href)
                pdf_links.append(full_url)

        # Remove duplicates while keeping order
        pdf_links = list(dict.fromkeys(pdf_links))

        if not pdf_links:
            log_func("No matching links found (.pdf / sendfile / download).\n")
            messagebox.showinfo(
                "No downloads",
                "No PDF/download links were found on this page.\n"
                "Try enabling 'show all objects on one page' in StudOn."
            )
            return

        log_func(f"Found links: {len(pdf_links)}\n\n")
        os.makedirs(output_dir, exist_ok=True)

        for url in pdf_links:
            try:
                filename = sanitize_filename(url)
                if not filename:
                    filename = "download.pdf"

                # Initial target path from URL
                file_path = os.path.join(output_dir, filename)

                log_func(f"Downloading: {filename} …\n")
                r = session.get(url, stream=True)
                r.raise_for_status()

                # If server sends Content-Disposition with a filename, prefer that
                cd = r.headers.get("Content-Disposition", "")
                match = re.search(r'filename="?([^";]+)"?', cd)
                if match:
                    filename_header = sanitize_filename(match.group(1))
                    file_path = os.path.join(output_dir, filename_header)

                with open(file_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

            except Exception as e:
                # Catch per-file errors so one broken link does not crash everything
                log_func(f"  -> Error downloading {url}: {e}\n")

        log_func("\nDone! All files should now be in the target folder.\n")
        messagebox.showinfo("Done", f"Downloads finished.\nFolder: {output_dir}")

    except Exception as e:
        # Very last-resort catch so the program does not crash
        log_func(f"\nUnexpected error: {e}\n")
        messagebox.showerror("Unexpected error", f"An unexpected error occurred:\n{e}")


def create_gui():
    root = tk.Tk()
    root.title("StudOn PDF Downloader")
    root.resizable(False, False)

    # Background & style
    bg_color = "#e0e0e0"
    root.configure(bg=bg_color)

    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid(row=0, column=0, sticky="nsew")

    # Column configuration
    main_frame.columnconfigure(1, weight=1)

    # --- Widgets ---
    # StudOn URL
    ttk.Label(main_frame, text="StudOn URL:").grid(row=0, column=0, sticky="w", pady=3)
    url_var = tk.StringVar()
    url_entry = ttk.Entry(main_frame, textvariable=url_var, width=60)
    url_entry.grid(row=0, column=1, columnspan=2, sticky="ew", pady=3)

    # Target folder
    ttk.Label(main_frame, text="Target folder:").grid(row=1, column=0, sticky="w", pady=3)
    folder_var = tk.StringVar()
    folder_entry = ttk.Entry(main_frame, textvariable=folder_var, width=60)
    folder_entry.grid(row=1, column=1, sticky="ew", pady=3)

    def browse_folder():
        folder = filedialog.askdirectory(title="Choose target folder")
        if folder:
            folder_var.set(folder)

    browse_button = ttk.Button(main_frame, text="Browse…", command=browse_folder)
    browse_button.grid(row=1, column=2, sticky="w", padx=(5, 0), pady=3)

    # Cookie name
    ttk.Label(main_frame, text="Cookie name:").grid(row=2, column=0, sticky="w", pady=3)
    cookie_name_var = tk.StringVar(value="PHPSESSID")
    cookie_name_entry = ttk.Entry(main_frame, textvariable=cookie_name_var, width=30)
    cookie_name_entry.grid(row=2, column=1, sticky="w", pady=3)

    # Cookie value (password field)
    ttk.Label(main_frame, text="Cookie value:").grid(row=3, column=0, sticky="w", pady=3)
    cookie_value_var = tk.StringVar()
    cookie_value_entry = ttk.Entry(main_frame, textvariable=cookie_value_var, width=60, show="*")
    cookie_value_entry.grid(row=3, column=1, columnspan=2, sticky="ew", pady=3)

    # Help text for cookie
    cookie_help = (
        "How to find cookie name & value:\n"
        "- Log in to StudOn in your browser.\n"
        "- Press F12 → open Developer Tools.\n"
        "- Chrome/Edge: tab 'Application' → 'Cookies' → your StudOn URL.\n"
        "- Firefox: tab 'Storage' → 'Cookies'.\n"
        "- Look for a session cookie (e.g. 'PHPSESSID', 'ILIAS_LOGIN', etc.).\n"
        "- Copy its name into 'Cookie name' and its value into 'Cookie value'."
    )
    help_label = ttk.Label(main_frame, text=cookie_help, justify="left")
    help_label.grid(row=4, column=0, columnspan=3, sticky="w", pady=(5, 10))

    # Start button
    start_button = ttk.Button(main_frame, text="Start download")

    # Log field
    log_label = ttk.Label(main_frame, text="Log:")
    log_label.grid(row=6, column=0, sticky="nw", pady=(5, 0))

    log_frame = ttk.Frame(main_frame)
    log_frame.grid(row=6, column=1, columnspan=2, sticky="nsew", pady=(5, 0))

    log_text = tk.Text(log_frame, width=70, height=15, state="disabled",
                       wrap="word", bg="#f5f5f5")
    log_scroll = ttk.Scrollbar(log_frame, orient="vertical", command=log_text.yview)
    log_text.configure(yscrollcommand=log_scroll.set)

    log_text.grid(row=0, column=0, sticky="nsew")
    log_scroll.grid(row=0, column=1, sticky="ns")
    log_frame.columnconfigure(0, weight=1)
    log_frame.rowconfigure(0, weight=1)

    def append_log(msg: str):
        log_text.configure(state="normal")
        log_text.insert("end", msg)
        log_text.see("end")
        log_text.configure(state="disabled")

    def on_start():
        base_url = url_var.get().strip()
        output_dir = folder_var.get().strip()
        cookie_name = cookie_name_var.get().strip()
        cookie_value = cookie_value_var.get().strip()

        if not base_url:
            messagebox.showwarning("Missing input", "Please enter a StudOn URL.")
            return
        if not output_dir:
            messagebox.showwarning("Missing input", "Please choose a target folder.")
            return
        if not cookie_name or not cookie_value:
            messagebox.showwarning("Missing input", "Please enter cookie name and value.")
            return

        # Disable button during download
        start_button.config(state="disabled")
        append_log("Starting download…\n\n")

        try:
            download_pdfs(base_url, output_dir, cookie_name, cookie_value, append_log)
        except Exception as e:
            # Catch any unexpected errors from download_pdfs
            append_log(f"\nUnexpected error in download: {e}\n")
            messagebox.showerror("Unexpected error", f"An unexpected error occurred:\n{e}")
        finally:
            start_button.config(state="normal")

    start_button.config(command=on_start)
    start_button.grid(row=5, column=0, columnspan=3, pady=(0, 5))

    # Focus on URL field
    url_entry.focus()

    root.mainloop()


if __name__ == "__main__":
    create_gui()
