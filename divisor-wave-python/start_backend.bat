@echo off
REM Startup script for Divisor Wave Complex Analysis Backend (Windows)

echo 🚀 Starting Divisor Wave Complex Analysis Backend...

REM Check if we're in the right directory
if not exist "requirements.txt" (
    echo ❌ Error: requirements.txt not found. Please run this script from the divisor-wave-python directory.
    pause
    exit /b 1
)

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH.
    pause
    exit /b 1
)

REM Display Python version
echo 📋 Python version:
python --version

REM Install requirements
echo 📦 Installing Python dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

REM Check if OptimizedSpecialFunctions is available
if exist "src\core\OptimizedSpecialFunctions.py" (
    echo ⚡ Using OptimizedSpecialFunctions for better performance
) else (
    echo ⚠️  Using original Special_Functions.py
)

REM Start the FastAPI server
echo.
echo 🌐 Starting FastAPI server on http://localhost:8000
echo 📖 API documentation will be available at http://localhost:8000/docs
echo 🔄 Server will auto-reload on code changes
echo.
echo Press Ctrl+C to stop the server
echo.

cd src\api
python main.py

pause