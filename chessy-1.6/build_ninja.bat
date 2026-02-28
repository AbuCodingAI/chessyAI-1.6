@echo off
REM Chessy 1.6 Build Script for Windows with Ninja

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

REM Configure with CMake using Ninja
echo Configuring CMake with Ninja...
cmake .. -G "Ninja" -DCMAKE_BUILD_TYPE=Release

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
ninja

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
pause
