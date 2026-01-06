@echo off
echo ========================================
echo   Installing Missing Dependencies
echo ========================================
echo.

REM Activate virtual environment
call finalenv\Scripts\activate.bat

REM Install email-validator
echo Installing email-validator...
pip install email-validator

echo.
echo ========================================
echo   ✅ Dependencies installed!
echo ========================================
echo.
echo Now run: python backend\start.py
echo.

pause
