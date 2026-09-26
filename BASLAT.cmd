@echo off
cd /d "%~dp0"
if not exist "venv\Scripts\python.exe" (
  echo Once README dosyasindaki kurulumu tamamlayin.
  pause
  exit /b 1
)
echo Stay Focused baslatiliyor.
echo Tarayicida http://127.0.0.1:5000 adresini acin.
echo Bu pencere acik kalmali. Durdurmak icin Ctrl+C kullanin.
"venv\Scripts\python.exe" run.py
pause
