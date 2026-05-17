@echo off
REM Build TuneScope executable for Windows
REM Requires: pip install pyinstaller

echo Installing dependencies...
pip install -r requirements.txt

echo Building executable...
pyinstaller --clean tunescope.spec

echo Done! Executable at dist\TuneScope.exe
