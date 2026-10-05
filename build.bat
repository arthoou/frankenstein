@echo off
REM Builds a standalone Windows executable with PyInstaller.
cd /d %~dp0
python -m pip install --quiet pyinstaller
pyinstaller --onefile --windowed --add-data "stages;stages" --name FrankenApp app.py
echo Executable at dist\FrankenApp.exe
