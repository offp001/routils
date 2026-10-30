@echo off
setlocal

set "ROOT=%~dp0.."
set "VENV=%~dp0.venv"
set "PYTHON=%VENV%\Scripts\python.exe"

py -3.12 -m venv "%VENV%"
if errorlevel 1 (
    echo Failed to create the Python 3.12 virtual environment.
    pause
    exit /b 1
)

"%PYTHON%" -m pip install --upgrade pip
if errorlevel 1 (
    echo Pip upgrade failed.
    pause
    exit /b 1
)

"%PYTHON%" -m pip install -r "%ROOT%\requirements.txt" -r "%ROOT%\requirements-build.txt"
if errorlevel 1 (
    echo Requirements installation failed.
    pause
    exit /b 1
)

echo Requirements installed in routils_windows\.venv
pause
