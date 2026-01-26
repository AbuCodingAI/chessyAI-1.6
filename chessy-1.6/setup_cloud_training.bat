@echo off
REM Chessy 1.6 Cloud Training Setup Script (Windows)

echo ================================
echo Chessy 1.6 Cloud Training Setup
echo ================================
echo.

REM Check if build directory exists
if not exist "bin" (
    echo Checking for build.bat...
    if exist "build.bat" (
        echo Building project...
        call build.bat
    ) else (
        echo ERROR: build.bat not found
        exit /b 1
    )
)

REM Check if binary exists
if not exist "bin\chessy-1.6.exe" (
    echo ERROR: Binary not found. Please build first.
    exit /b 1
)

echo OK: Binary found: bin\chessy-1.6.exe

REM Create directories
if not exist "checkpoints" mkdir checkpoints
if not exist "models" mkdir models
if not exist "logs" mkdir logs

echo OK: Directories created

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.
    exit /b 1
)

echo OK: Python found

REM Check Stockfish
if exist "stockfish\stockfish-windows-x86-64-avx2.exe" (
    echo OK: Stockfish found
) else (
    echo WARNING: Stockfish not found. Training will use fallback evaluation.
    echo Download from: https://stockfishchess.org/download/
)

echo.
echo ================================
echo Setup Complete!
echo ================================
echo.
echo To start training:
echo   python train_cloud.py
echo.
echo To monitor training:
echo   type training.log
echo.
echo To deploy to Render:
echo   1. Push to GitHub
echo   2. Go to render.com
echo   3. Create new Background Worker
echo   4. Select this repository
echo   5. Set start command: python train_cloud.py
echo.
pause
