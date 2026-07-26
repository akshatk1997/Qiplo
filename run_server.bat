@echo off
title Qiplo Local Server Watchdog
cd /d "%~dp0"

:LOOP
echo [%date% %time%] Launching Qiplo Flask Server on http://127.0.0.1:5000 ...
.venv\Scripts\python.exe app.py
echo [WARNING] Server stopped at %time%. Restarting in 2 seconds...
timeout /t 2 /nobreak >nul
goto LOOP
