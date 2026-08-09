@echo off
setlocal
cd /d "%~dp0"
title DEV//48 - Diagnostica
set "PYTHONUTF8=1"

if not exist ".venv\Scripts\python.exe" (
    echo DEV//48 non e ancora configurato: avvia prima "Avvia DEV48.bat".
    echo.
    where py 2>nul
    where python 2>nul
    where node 2>nul
    where npm 2>nul
    pause
    exit /b 1
)

".venv\Scripts\python.exe" tools\doctor.py
echo.
echo Premi un tasto per chiudere.
pause >nul
