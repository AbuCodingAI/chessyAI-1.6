@echo off
echo ========================================
echo CHESSY 1.5 - FULL TRAINING PIPELINE
echo ========================================
echo.
echo This will run the complete training pipeline:
echo.
echo 1. Generate Training Data
echo    - Stockfish vs Stockfish (100 games)
echo    - Collect ~5000 positions
echo    - Clean evaluations (depth 25)
echo.
echo 2. Train Neural Network
echo    - Train from Stockfish positions
echo    - 50 epochs with early stopping
echo.
echo 3. Self-Play Testing
echo    - 40 games (Chessy vs Chessy)
echo    - Learn from self-play
echo.
echo 4. Stockfish Testing
echo    - 60 games vs Stockfish (depth 10)
echo    - Calculate ELO rating
echo.
echo Estimated time: 4-6 hours
echo.
pause

cd neural-ai
python FULL_CHESSY_1.5_PIPELINE.py

echo.
echo ========================================
echo Training Complete!
echo ========================================
echo.
echo View results:
echo   cd neural-ai
echo   python view_chessy_1.5_results.py
echo.
pause
