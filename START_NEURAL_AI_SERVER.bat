@echo off
echo Starting Chessy Neural AI Server...
echo.
echo This will start the Python backend for your trained neural AI models
echo The server will run on http://localhost:5000
echo.

cd neural-ai
python chess_ai_server.py

pause
