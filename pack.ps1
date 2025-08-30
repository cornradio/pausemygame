Remove-Item -Path .\dist\* -Recurse -Force
# xcopy  afont.ttf dist\ /y
# xcopy game_name.txt  dist\ /y
xcopy  pssuspend.exe dist\ /y
xcopy  NTop.exe dist\ /y
xcopy  game_name.txt dist\ /y

pyinstaller  --exclude=pyinstaller --exclude=pandas --noconsole  --exclude=numpy --exclude=libcrypto  --onefile --icon=icon.ico  main3.py
# //compress \dist\lightspeed to lightspeed.zip using pwsh
Compress-Archive -Path .\dist\ -DestinationPath .\pausemygame_vx.x.zip -Force