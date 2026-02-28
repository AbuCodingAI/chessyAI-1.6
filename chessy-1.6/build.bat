@echo off
REM Chessy 1.6 Build Script for Windows

echo.
echo ========================================
echo Chessy 1.6 - C++ Neural Chess Engine
echo ========================================
echo.

REM Check if build directory exists
if not exist build (
    echo Creating build directory...
    mkdir build
)

cd build

REM Configure with CMake
echo Configuring CMake...
cmake .. -G "Visual Studio 17 2022" -DCMAKE_BUILD_TYPE=Release

if errorlevel 1 (
    echo.
    echo ERROR: CMake configuration failed!
    echo.
    pause
    exit /b 1
)

REM Build
echo.
echo Building Chessy 1.6...
cmake --build . --config Release

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    echo.
    pause
    exit /b 1
)

cd ..

echo.
echo ========================================
echo Build successful!
echo ========================================
echo.
echo Executable: bin\chessy-1.6.exe
echo.
echo Next steps:
echo   1. Download Stockfish from https://stockfishchess.org/download/
echo   2. Extract to: stockfish\
echo   3. Run: bin\chessy-1.6.exe --play
echo.
pause
