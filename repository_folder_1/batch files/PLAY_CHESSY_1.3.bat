@echo off
echo.
echo ========================================
echo    CHESSY 1.3 - Time Control Specialist
echo    ELO: ~2200-2400 (Time-Aware)
echo ========================================
echo.
echo Starting Chessy 1.3 Server...
echo.

cd neural-ai
start cmd /k python chess_ai_server.py

timeout /t 3 /nobreak >nul

echo.
echo Server starting in new window...
echo.
echo Opening Chessy 1.3 in your browser in 5 seconds...
timeout /t 5 /nobreak >nul

start Chessy1-3.html

echo.
echo ========================================
echo    Chessy 1.3 is ready!
echo ========================================
echo.
echo Server running in separate window
echo Browser should open automatically
echo.
echo Press any key to close this window...
pause >nul
