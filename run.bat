@echo off
title CareerPath AI Launcher
cd /d "%~dp0"

echo ===================================================
echo           CareerPath AI - Fullstack App
echo ===================================================
echo.
echo [1/3] Starting Backend API Server (Port 8000)...
start "CareerPath Backend" cmd /k "cd /d ""%~dp0backend"" && py -3.10 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

echo [2/3] Waiting for backend initialization...
timeout /t 3 /nobreak >nul

echo [3/3] Starting Frontend Dev Server (Port 5173)...
start http://localhost:5173
cd /d "%~dp0frontend"
npm run dev
