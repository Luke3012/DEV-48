@echo off
setlocal
cd /d "%~dp0"
title DEV//48 - Bootcamp tecnico
set "PYTHONUTF8=1"

if not exist ".venv\Scripts\python.exe" (
    echo [DEV//48] Prima configurazione: creo l'ambiente Python...
    where py >nul 2>nul
    if not errorlevel 1 (
        py -3.14 -m venv .venv 2>nul || py -3 -m venv .venv
    ) else (
        where python >nul 2>nul
        if errorlevel 1 goto :no_python
        python -m venv .venv
    )
    if errorlevel 1 goto :error
    ".venv\Scripts\python.exe" -m pip install --upgrade pip
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 goto :error
)

".venv\Scripts\python.exe" -c "import textual" >nul 2>nul
if errorlevel 1 (
    echo [DEV//48] Completo le dipendenze mancanti...
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 goto :error
)

".venv\Scripts\python.exe" -m dev48
if errorlevel 1 (
    echo.
    echo DEV//48 si e chiuso con un errore. Premi un tasto per vedere il messaggio.
    pause >nul
)
exit /b

:no_python
echo.
echo Python non trovato. Installa Python 3.11 o successivo e abilita "Add Python to PATH".
pause
exit /b 1

:error
echo.
echo Configurazione non riuscita. Esegui "Diagnostica DEV48.bat" per i dettagli.
pause
exit /b 1
