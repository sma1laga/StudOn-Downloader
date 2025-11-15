; Inno Setup script for packaging StudOn Downloader into StudOnDownloaderSetup.exe

#define MyAppName "StudOn Downloader"
#define MyAppVersion "1.0.0"
#define MyAppExeName "StudOnDownloader.exe"
#define MyOutputDir "dist"
#define MySourceDir "dist/StudOnDownloader"

[Setup]
AppId={{D09C2246-0E6B-4D96-AE15-7B6A9975D998}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir={#MyOutputDir}
OutputBaseFilename=StudOnDownloaderSetup
Compression=lzma
SolidCompression=yes
SetupIconFile={#MySourceDir}/StudOnDownloader.exe

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
Source: "{#MySourceDir}/*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
