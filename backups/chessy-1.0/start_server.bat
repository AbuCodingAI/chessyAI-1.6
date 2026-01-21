@echo off
title Chessy 1.0 - Neural Network AI Server
color 0A
echo.
echo ========================================
echo   Chessy 1.0 - Neural Network AI
echo ========================================
echo.
echo [1/4] Checking Python installation...
python --version 2>nul
if errorlevel 1 (
    color 0C
    echo.
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python 3.8+ from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)
echo       Python found!
echo.
echo [2/4] Installing required packages...
pip install -q flask flask-cors tensorflow numpy python-chess
if errorlevel 1 (
    echo       Warning: Some packages may have failed to install
    echo       Continuing anyway...
) else (
    echo       Packages installed!
)
echo.
echo [3/4] Starting AI server...
echo       Server will run on http://localhost:5000
echo.
echo [4/4] Opening browser...
timeout /t 2 /nobreak >nul
start "" "Chessy1-0.html"
echo.
echo ========================================
echo   Server is running!
echo   Close this window to stop the server
echo ========================================
echo.
python chess_ai_server.py
pause
