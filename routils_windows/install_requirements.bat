@echo off
setlocal
cd /d "%~dp0"

set "VENV=%~dp0.venv"
set "PYTHON=%VENV%\Scripts\python.exe"

py -3.12 -m venv "%VENV%"
if errorlevel 1 (
    echo failed to create the python 3.12 virtual environment.
    pause
    exit /b 1
)

"%PYTHON%" -m pip install --upgrade pip
if errorlevel 1 (
    echo pip upgrade failed.
    pause
    exit /b 1
)

"%PYTHON%" -m pip install -r "%~dp0requirements.txt"
if errorlevel 1 (
    echo requirements installation failed.
    pause
    exit /b 1
)

echo requirements installed in routils_windows\.venv
pause
