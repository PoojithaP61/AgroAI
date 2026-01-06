@echo off
echo ========================================
echo   AgroAI Frontend Startup Script
echo ========================================
echo.

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

REM Navigate to frontend directory
cd /d "%SCRIPT_DIR%frontend"
if not exist "package.json" (
    echo ERROR: Frontend directory not found!
    echo Please make sure you're running this from the project root.
    echo Current directory: %CD%
    echo Script directory: %SCRIPT_DIR%
    pause
    exit /b 1
)

echo Current directory: %CD%
echo.

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies!
        pause
        exit /b 1
    )
    echo Dependencies installed!
    echo.
)

REM Start development server
echo ========================================
echo   Starting Frontend Development Server...
echo ========================================
echo.
echo Frontend will be available at: http://localhost:3000
echo Make sure backend is running on: http://localhost:8000
echo.
echo Press CTRL+C to stop the server
echo.

call npm run dev

pause
