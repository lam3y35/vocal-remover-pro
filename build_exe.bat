@echo off
setlocal

cd /d "%~dp0"
echo [1/3] Installing PyInstaller...
python -m pip install --upgrade pyinstaller
if errorlevel 1 goto :err

echo [2/3] Building executable package...
python build.py
if errorlevel 1 goto :err

echo [3/3] Done.
echo Output folder: dist\VocalRemoverPro
echo Zip this whole folder and share it.
exit /b 0

:err
echo Build failed. Check the errors above.
exit /b 1
