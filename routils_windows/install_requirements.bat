@echo off
cd /d "%~dp0"
py -3.12 -m pip install --upgrade pip
py -3.12 -m pip install -r requirements.txt
if errorlevel 1 (
  echo Requirements installation failed. Make sure Python 3.12 is installed
  pause
  exit /b 1
)
echo Requirements installed
pause
