@echo off
cd /d "%~dp0"
py -3.12 -m PyInstaller --noconfirm --clean --onefile --windowed --icon=routils.ico --add-data "routils.ico;." --add-data "routils_rpc.png;." --name=RoUtils main.pyw
if errorlevel 1 (
    echo.
    echo Compiling failed
    pause
    exit /b 1
)
echo.
echo Build complete: dist\RoUtils.exe
pause