@echo off
cd /d "%~dp0"
python --version >nul 2>&1
if errorlevel 1 goto python_missing
if not exist "venv\Scripts\python.exe" python -m venv venv
if errorlevel 1 goto failed
"venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto failed
"venv\Scripts\python.exe" ilk_kurulum.py
if errorlevel 1 goto failed
echo Kurulum tamamlandi. BASLAT.cmd dosyasini acabilirsiniz.
pause
exit /b 0
:python_missing
echo Python 3.10 veya ustunu kurup Add Python to PATH secenegini isaretleyin.
pause
exit /b 1
:failed
echo Kurulum tamamlanamadi. Yukaridaki hata mesajini kontrol edin.
pause
exit /b 1
