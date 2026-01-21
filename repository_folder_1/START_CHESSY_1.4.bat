@echo off
title Chessy 1.4 - GM Level Chess AI
color 0A
echo.
echo ========================================
echo   Chessy 1.4 - GM Level Chess AI
echo   ~2700+ ELO with Smart Quiescence
echo ========================================
echo.
echo [1/3] Checking Node.js installation...
node --version 2>nul
if errorlevel 1 (
    color 0C
    echo.
    echo ERROR: Node.js is not installed!
    echo.
    echo Please install Node.js from:
    echo https://nodejs.org/
    echo.
    pause
    exit /b 1
)
echo       Node.js found!
echo.
echo [2/3] Installing dependencies...
call npm install
if errorlevel 1 (
    echo       Warning: Some packages may have failed to install
    echo       Continuing anyway...
) else (
    echo       Dependencies installed!
)
echo.
echo [3/3] Starting server...
echo       Server will run on http://localhost:3000
echo.
timeout /t 2 /nobreak >nul
start "" "http://localhost:3000"
echo.
echo ========================================
echo   Server is running!
echo   Close this window to stop the server
echo ========================================
echo.
echo Available AIs:
echo   - Noob to Super GM (100-2700 ELO)
echo   - Chessy 1.4 (2700+ ELO with Neural Network)
echo   - Chocker (Ultimate Disrespect AI)
echo   - Random Guy, Trash Talker, Mystery
echo.
node server.js
pause
