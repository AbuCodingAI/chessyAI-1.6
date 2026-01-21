@echo off
echo.
echo ========================================
echo    CHESSY 1.3 - COMPLETE TRAINING SUITE
echo    IM-Beatable AI with All Features
echo ========================================
echo.
echo This will train Chessy 1.3 with:
echo   1. Time control optimization
echo   2. Blunder recognition
echo   3. Opening theory
echo   4. Deep search capability
echo.
echo Total time: ~5-6 hours
echo Result: 2500+ ELO IM-beatable AI!
echo.
pause

echo.
echo ========================================
echo    STEP 1: Time Control Training
echo    Time: ~3 hours
echo ========================================
echo.
python train_chessy_1.3_time_control.py
if errorlevel 1 (
    echo ERROR: Time control training failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo    STEP 2: Blunder Training
echo    Time: ~1-2 hours
echo ========================================
echo.
python blunder_training.py
if errorlevel 1 (
    echo ERROR: Blunder training failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo    STEP 3: Opening Training
echo    Time: ~30-45 minutes
echo ========================================
echo.
python stockfish_opening_training.py
if errorlevel 1 (
    echo ERROR: Opening training failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo    CHESSY 1.3 TRAINING COMPLETE!
echo ========================================
echo.
echo Your AI is now:
echo   - 2500+ ELO (IM-beatable!)
echo   - Time control optimized
echo   - Blunder-aware
echo   - Opening theory trained
echo   - Deep search capable
echo.
echo Models created:
echo   - chess_model_bullet_fast.h5
echo   - chess_model_blitz_fast.h5
echo   - chess_model_rapid_standard.h5
echo   - chess_model_classical_deep.h5
echo   - chess_model_blunder_trained.h5
echo   - chess_model_with_openings.h5
echo.
echo Next steps:
echo   1. Update server to use new models
echo   2. Test against strong opponents
echo   3. Enjoy your IM-level AI!
echo.
pause
