@echo off
echo.
echo ========================================
echo    CHESSY 1.0 - Initial Version
echo    ELO: ~1200
echo ========================================
echo.
echo Starting Chessy 1.0 Server...
echo.

cd backups\chessy-1.0
start cmd /k python chess_ai_server.py

timeout /t 3 /nobreak >nul

echo.
echo Server starting in new window...
echo.
echo Opening Chessy 1.0 in your browser in 5 seconds...
timeout /t 5 /nobreak >nul

start Chessy1-0.html

echo.
echo ========================================
echo    Chessy 1.0 is ready!
echo ========================================
echo.
echo Server running in separate window
echo Browser should open automatically
echo.
echo Press any key to close this window...
pause >nul
