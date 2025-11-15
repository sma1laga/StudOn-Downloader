# StudOn Downloader

StudOn Downloader is a polished desktop utility that collects every downloadable file from a StudOn page and saves it to a folder
on your computer. The application ships with a Tkinter-based interface and includes build scripts for producing a standalone
`StudOnDownloader.exe` as well as an installer (`StudOnDownloaderSetup.exe`) for distribution.

## Features

- Intuitive GUI that guides you through URL, folder, and cookie configuration.
- Automatic detection of `.pdf`, `sendfile`, and generic `download` links on StudOn pages.
- Detailed logging view for monitoring progress and troubleshooting.
- Packaged as a real Windows application via PyInstaller, optionally wrapped with an Inno Setup installer.

## Project layout

```
├─ installer/                 # Inno Setup script used to build StudOnDownloaderSetup.exe
├─ src/studon_downloader/     # Python package with GUI and download logic
├─ StudOnDownloader.spec      # PyInstaller configuration (builds StudOnDownloader.exe)
├─ download_studon_pdfs.py    # Legacy launcher that forwards to the packaged GUI
└─ pyproject.toml             # Project metadata + dependencies
```

## Running from source

1. Install Python 3.10+ and ensure `python`/`pip` is available on your PATH.
2. Create a virtual environment (recommended) and install the dependencies:

   ```bash
   python -m venv .venv
   .venv\\Scripts\\activate   # PowerShell on Windows
   python -m pip install -U pip
   python -m pip install -e .
   ```

3. Start the GUI via either command:

   ```bash
   python -m studon_downloader
   # or
   studon-downloader
   ```

4. Enter the StudOn URL, choose a download folder, and provide a valid session cookie value. Use the help text in the application
   to find the cookie name/value inside your browser's developer tools.

## Building a standalone `StudOnDownloader.exe`

1. Install PyInstaller (already listed under the `ui` optional dependency):

   ```bash
   python -m pip install -e .[ui]
   ```

2. Run PyInstaller with the provided spec file:

   ```bash
   pyinstaller StudOnDownloader.spec
   ```

   The compiled executable and supporting files will be placed under `dist/StudOnDownloader/StudOnDownloader.exe`.

## Creating `StudOnDownloaderSetup.exe`

1. Build the standalone app as described above. Ensure `dist/StudOnDownloader` contains `StudOnDownloader.exe`.
2. Install [Inno Setup](https://jrsoftware.org/isinfo.php) on Windows.
3. Open `installer/StudOnDownloader.iss` in the Inno Setup IDE (or run `iscc installer/StudOnDownloader.iss`).
4. The resulting installer (`dist/StudOnDownloaderSetup.exe`) can be distributed to end users. It creates Start Menu entries and an
   optional desktop shortcut, then launches the application after installation.

## Tips & troubleshooting

- If no files download, make sure the StudOn page lists links ending in `.pdf`, `sendfile`, or `download`. Switch StudOn to "show
  all objects on one page" for best results.
- Authentication problems usually mean the session cookie expired. Refresh StudOn in your browser, copy the cookie again, and retry.
- The GUI writes detailed status updates to the log panel; include the log output when reporting issues.

## License

This project is provided as-is without warranty. Use it only with StudOn content you are allowed to access.
