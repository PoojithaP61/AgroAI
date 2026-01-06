@echo off
echo ========================================
echo   AgroAI Backend Startup Script
echo ========================================
echo.

REM Navigate to project directory
cd /d "C:\Users\pooji\OneDrive\Desktop\AgroAI_FinalYear_Project"
echo Current directory: %CD%
echo.

REM Activate virtual environment
echo Activating virtual environment...
call finalenv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Could not activate virtual environment!
    echo Please make sure finalenv exists.
    pause
    exit /b 1
)
echo Virtual environment activated!
echo.

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo Dependencies not found. Installing...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies!
        pause
        exit /b 1
    )
) else (
    echo Dependencies OK!
)

REM Ensure email-validator is installed (required for Pydantic EmailStr)
echo Checking email-validator...
python -c "import email_validator" 2>nul
if errorlevel 1 (
    echo Installing email-validator...
    pip install email-validator
)
echo.

REM Start the server
echo ========================================
echo   Starting AgroAI Backend Server...
echo ========================================
echo.
echo Server will be available at: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press CTRL+C to stop the server
echo.

python backend\start.py

pause
