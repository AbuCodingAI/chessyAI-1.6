@echo off
REM Download and install all C++ tools needed for Chessy 1.6

echo.
echo ========================================
echo Chessy 1.6 - C++ Tools Setup
echo ========================================
echo.

REM Check if winget is available
where winget >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: winget not found. Please install Windows Package Manager first.
    echo Download from: https://www.microsoft.com/en-us/p/app-installer/9nblggh4nns1
    pause
    exit /b 1
)

echo Installing C++ build tools...
echo.

REM Install Visual Studio Build Tools
echo [1/4] Installing Visual Studio Build Tools...
winget install Microsoft.VisualStudio.2022.BuildTools -e --silent --accept-source-agreements --accept-package-agreements
if %errorlevel% neq 0 (
    echo WARNING: Visual Studio Build Tools installation may have failed
)

REM Install CMake
echo [2/4] Installing CMake...
winget install Kitware.CMake -e --silent --accept-source-agreements --accept-package-agreements
if %errorlevel% neq 0 (
    echo WARNING: CMake installation may have failed
)

REM Install Git
echo [3/4] Installing Git...
winget install Git.Git -e --silent --accept-source-agreements --accept-package-agreements
if %errorlevel% neq 0 (
    echo WARNING: Git installation may have failed
)

REM Install vcpkg
echo [4/4] Installing vcpkg...
if not exist "C:\vcpkg" (
    cd C:\
    git clone https://github.com/Microsoft/vcpkg.git
    cd vcpkg
    .\bootstrap-vcpkg.bat
) else (
    echo vcpkg already installed
)

echo.
echo ========================================
echo Installation complete!
echo ========================================
echo.
echo Next steps:
echo 1. Close and reopen Command Prompt
echo 2. Run: cd chessy-1.6
echo 3. Run: build.bat
echo.
pause
