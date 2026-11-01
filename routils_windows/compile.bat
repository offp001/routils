@echo off
setlocal
cd /d "%~dp0"

set "PYTHON=%~dp0.venv\Scripts\python.exe"

if not exist "%PYTHON%" (
    echo Python environment not found. Run install_requirements.bat first.
    pause
    exit /b 1
)

if not exist "main.pyw" (
    echo main.pyw not found.
    pause
    exit /b 1
)

if not exist "routils.ico" (
    echo routils.ico not found.
    pause
    exit /b 1
)

if not exist "routils_rpc.png" (
    echo routils_rpc.png not found.
    pause
    exit /b 1
)

"%PYTHON%" -m compileall -q main.pyw autoupdate external fflag home luau_interpreter tools
if errorlevel 1 (
    echo Syntax check failed.
    pause
    exit /b 1
)

if not exist "bin" mkdir "bin"
"%PYTHON%" tools\download_luau.py --platform windows --output bin\luau.exe
if errorlevel 1 (
    echo Luau CLI download failed.
    pause
    exit /b 1
)

"%PYTHON%" -m PyInstaller --noconfirm --clean --onefile --windowed --icon=routils.ico --paths . --add-binary "bin\luau.exe;bin" --add-data "routils.ico;." --add-data "routils_rpc.png;." --add-data "src\presets;src\presets" --name=RoUtils main.pyw
if errorlevel 1 (
    echo.
    echo Compiling failed
    pause
    exit /b 1
)

if not exist "dist\RoUtils.exe" (
    echo Build output was not created.
    pause
    exit /b 1
)

echo.
echo Build complete: dist\RoUtils.exe
pause
