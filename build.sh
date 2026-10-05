#!/usr/bin/env bash
# Builds a standalone Linux executable with PyInstaller.
cd "$(dirname "$0")"
python3 -m pip install --quiet pyinstaller
pyinstaller --onefile --windowed --add-data "stages:stages" --name FrankenApp app.py
echo "Executable at dist/FrankenApp"
