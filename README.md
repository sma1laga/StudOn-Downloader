# StudOn Downloader

StudOn Downloader is a small Windows GUI utility that collects every downloadable file from a StudOn page and saves the files to a folder on your computer. It accepts any StudOn page that displays PDFs or other files ("sendfile", "download", etc.) and downloads them immediately once you provide the session cookie that proves you are logged in.

## Requirements

- Windows 10/11 with Python 3.10 or newer installed and added to your PATH
- Internet connection to reach StudOn
- A valid StudOn session (you must be logged in via your browser so you can copy the session cookie)

Install the Python dependencies once:

```bash
python -m pip install requests beautifulsoup4
```

## Downloading the tool

1. Download or clone this repository.
   - **Zip:** Press the green "Code" button on GitHub, choose "Download ZIP", and extract it to any folder.
   - **Git:** `git clone https://github.com/<your-account>/StudOn-Downloader.git`
2. Open the folder in Explorer.

## Running the downloader

1. Double-click `download_studon_pdfs.py` or run `python download_studon_pdfs.py` from PowerShell/CMD.
2. Enter the StudOn URL that lists the files you want. Enable “show all objects on one page” inside StudOn if possible so every file is visible.
3. Choose a target folder where the files should be saved.
4. Provide the cookie name and value for your StudOn session:
   - Sign in to StudOn in your browser.
   - Press `F12` to open the developer tools.
   - Chrome/Edge: Application → Storage → Cookies → your StudOn URL.
   - Firefox: Storage → Cookies.
   - Copy the session cookie (usually `PHPSESSID`, `ILIAS_LOGIN`, or similar) and paste its name and value into the two fields.
5. Press **Start download**. Every detected file (PDFs or other download links) will be downloaded into the target folder. The log box shows progress and any errors.

## Tips

- If nothing is downloaded, verify that the page shows links ending in `.pdf`, `sendfile`, or `download`. Switch StudOn to show all objects or open the folder containing the files directly.
- If you receive authentication errors, make sure the cookie is still valid (reload StudOn in your browser and copy the cookie again).
- Each run overwrites files with the same name. Create a dedicated folder per lecture/collection if needed.