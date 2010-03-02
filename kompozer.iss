; Script template for Inno Setup
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
AppId={{20aa4150-b5f4-11de-8a39-0800200c9a66}
AppName=KompoZer
AppVerName=KompoZer @VERSION@
AppPublisher=KompoZer
AppPublisherURL=http://www.kompozer.net/
AppSupportURL=http://www.kompozer.net/community.php
AppUpdatesURL=http://www.kompozer.net/download.php
DefaultDirName={pf}\KompoZer
DefaultGroupName=KompoZer
AllowNoIcons=yes
LicenseFile=license.txt
;SetupIconFile=kompozer.ico
OutputDir=build\@VERSION@\win32\exe
OutputBaseFilename=kompozer-@VERSION@.@LOCALE@.win32
Compression=lzma
SolidCompression=yes

[Languages]
Name: "@MSGNAME@"; MessagesFile: "compiler:@MSGFILE@"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "build\bin\win32\@LOCALE@\KompoZer\kompozer.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "build\bin\win32\@LOCALE@\KompoZer\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\KompoZer"; Filename: "{app}\kompozer.exe"
Name: "{group}\{cm:ProgramOnTheWeb,KompoZer}"; Filename: "http://www.kompozer.net/"
Name: "{group}\{cm:UninstallProgram,KompoZer}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\KompoZer"; Filename: "{app}\kompozer.exe"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\KompoZer"; Filename: "{app}\kompozer.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\kompozer.exe"; Description: "{cm:LaunchProgram,KompoZer}"; Flags: nowait postinstall skipifsilent

