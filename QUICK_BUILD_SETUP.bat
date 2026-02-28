@echo off
REM Quick setup for building Chessy 1.6 locally

echo.
echo Installing minimal C++ build tools...
echo.

REM Install Visual Studio Build Tools (minimal)
echo Installing Visual Studio Build Tools...
winget install Microsoft.VisualStudio.2022.BuildTools --override "--wait --quiet --norestart --add Microsoft.VisualStudio.Workload.NativeDesktop" -e --silent --accept-source-agreements --accept-package-agreements

REM Install CMake
echo Installing CMake...
winget install Kitware.CMake -e --silent --accept-source-agreements --accept-package-agreements

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Close and reopen Command Prompt, then run:
echo   cd chessy-1.6
echo   build.bat
echo.
pause
