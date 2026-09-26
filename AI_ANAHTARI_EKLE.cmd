@echo off
cd /d "%~dp0"
if not exist "venv\Scripts\python.exe" (
  echo Once README dosyasindaki Python kurulumunu tamamlayin.
  pause
  exit /b 1
)
"venv\Scripts\python.exe" configure_ai.py
pause
