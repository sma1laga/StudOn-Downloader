"""Core downloading logic for StudOn Downloader."""

from __future__ import annotations

import os
import re
from typing import Callable, List

import requests
from bs4 import BeautifulSoup
from tkinter import messagebox
from urllib.parse import urljoin

LogFunc = Callable[[str], None]


def sanitize_filename(name: str) -> str:
    """Return a filesystem-safe version of *name*."""

    name = name.split("/")[-1].split("\\")[-1]
    name = name.split("?")[0].split("#")[0]
    return re.sub(r"[^\w\-.]", "_", name)


def _collect_candidate_links(base_url: str, html: str) -> List[str]:
    """Extract potential download links from StudOn HTML."""

    soup = BeautifulSoup(html, "html.parser")
    pdf_links: List[str] = []

    for anchor in soup.find_all("a", href=True):
        href = anchor["href"].strip()
        href_lower = href.lower()

        if ".pdf" in href_lower or "sendfile" in href_lower or "download" in href_lower:
            pdf_links.append(urljoin(base_url, href))

    # Remove duplicates while preserving order
    return list(dict.fromkeys(pdf_links))


def download_pdfs(
    base_url: str,
    output_dir: str,
    cookie_name: str,
    cookie_value: str,
    log_func: LogFunc,
) -> None:
    """Download all detected StudOn PDF/download links to *output_dir*."""

    session = requests.Session()
    session.headers.update({"Cookie": f"{cookie_name}={cookie_value}"})

    log_func("Fetching StudOn page…\n")

    try:
        resp = session.get(base_url)
        resp.raise_for_status()
    except requests.RequestException as exc:  # pragma: no cover - UI only
        log_func(f"Error loading page: {exc}\n")
        messagebox.showerror("Error", f"Could not load the page:\n{exc}")
        return

    links = _collect_candidate_links(base_url, resp.text)
    if not links:
        log_func("No matching links found (.pdf / sendfile / download).\n")
        messagebox.showinfo(
            "No downloads",
            "No PDF/download links were found on this page.\n"
            "Try enabling 'show all objects on one page' in StudOn.",
        )
        return

    log_func(f"Found links: {len(links)}\n\n")
    os.makedirs(output_dir, exist_ok=True)

    for url in links:
        try:
            filename = sanitize_filename(url) or "download.pdf"
            file_path = os.path.join(output_dir, filename)

            log_func(f"Downloading: {filename} …\n")
            response = session.get(url, stream=True)
            response.raise_for_status()

            cd_header = response.headers.get("Content-Disposition", "")
            match = re.search(r'filename="?([^";]+)"?', cd_header)
            if match:
                filename_from_header = sanitize_filename(match.group(1))
                if filename_from_header:
                    file_path = os.path.join(output_dir, filename_from_header)

            with open(file_path, "wb") as handle:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        handle.write(chunk)

        except Exception as exc:  # pragma: no cover - UI only
            log_func(f"  -> Error downloading {url}: {exc}\n")

    log_func("\nDone! All files should now be in the target folder.\n")
    messagebox.showinfo("Done", f"Downloads finished.\nFolder: {output_dir}")


__all__ = ["download_pdfs", "sanitize_filename"]
