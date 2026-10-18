@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  py -3 -m venv .venv
  if errorlevel 1 goto fail
)
.venv\Scripts\python.exe -c "import serial" >nul 2>&1
if errorlevel 1 (
  .venv\Scripts\python.exe -m pip install -r requirements.txt
  if errorlevel 1 goto fail
)
.venv\Scripts\python.exe -m desktop.app %*
if errorlevel 1 goto fail
exit /b 0
:fail
echo Installatie/start mislukt. Zie DESKTOP.md; Python met Tkinter is vereist.
pause
exit /b 1
