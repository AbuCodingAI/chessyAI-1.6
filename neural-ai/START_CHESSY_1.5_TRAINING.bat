@echo off
echo ========================================
echo CHESSY 1.5 - COMPLETE TRAINING PIPELINE
echo ========================================
echo.
echo This will:
echo 1. Generate training data (Stockfish vs Stockfish with blunders)
echo 2. Train neural network from data
echo 3. Self-play testing (40 games)
echo 4. Stockfish testing (60 games)
echo 5. Calculate final ELO rating
echo.
echo Estimated time: 4-6 hours
echo.
pause

cd neural-ai

echo.
echo ========================================
echo STEP 1: Generate Training Data
echo ========================================
python GENERATE_TRAINING_DATA_STOCKFISH.py
if errorlevel 1 (
    echo ERROR: Data generation failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo STEP 2: Train Neural Network
echo ========================================
python TRAIN_CHESSY_1.5_FROM_STOCKFISH.py
if errorlevel 1 (
    echo ERROR: Training failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo STEP 3: Self-Play and Stockfish Testing
echo ========================================
python TRAIN_CHESSY_1.5_SELF_PLAY.py
if errorlevel 1 (
    echo ERROR: Testing failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo TRAINING COMPLETE!
echo ========================================
echo.
echo View results:
echo   python view_chessy_1.5_results.py
echo.
pause
