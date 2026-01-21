@echo off
echo.
echo ========================================
echo    CHESSY - Neural AI Chess
echo ========================================
echo.
echo Starting Chessy Neural AI Server...
echo.

cd neural-ai
start cmd /k python chess_ai_server.py

timeout /t 3 /nobreak >nul

echo.
echo Server starting in new window...
echo.
echo Opening Chessy in your browser in 5 seconds...
timeout /t 5 /nobreak >nul

start Chessy1-2.html

echo.
echo ========================================
echo    Chessy is ready!
echo ========================================
echo.
echo Server running in separate window
echo Browser should open automatically
echo.
echo Press any key to close this window...
pause >nul
