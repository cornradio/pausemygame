[Setup]
AppName=pausemygame
AppVersion=1.0.0
DefaultDirName={pf}\pausemygame_v2.0
OutputBaseFilename=pausemygame
Compression=lzma
SolidCompression=yes

[Files]
Source: "pausemygame_v2.0\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\pausemygame"; Filename: "{app}\pausemygame.exe"
