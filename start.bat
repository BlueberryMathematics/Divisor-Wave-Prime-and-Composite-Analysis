@echo off
REM Divisor Wave Complex Analysis - Quick Start Script
echo.
echo 🌊 Starting Divisor Wave Complex Analysis...
echo ================================================

REM Start Python Backend
echo 🐍 Starting Python Backend...
start "Backend Server" cmd /k "cd /d "%~dp0divisor-wave-python" && python src/api/main.py"

REM Wait a moment
timeout /t 3 /nobreak >nul

REM Start Next.js Frontend  
echo ⚛️ Starting Next.js Frontend...
start "Frontend Server" cmd /k "cd /d "%~dp0divisor-wave-nextjs" && npm run dev"

REM Wait for servers to start
echo ⏳ Waiting for servers to start...
timeout /t 5 /nobreak >nul

echo.
echo 🎉 Divisor Wave Complex Analysis is starting!
echo 📊 Frontend:  http://localhost:3000
echo 🔧 Backend:   http://localhost:8000  
echo 📖 API Docs: http://localhost:8000/docs
echo.
echo 🔬 Ready to explore infinite products and prime relationships!
echo 💡 Close the terminal windows to stop the servers
echo.

REM Ask to open browser
set /p openBrowser="Open application in browser? (y/N): "
if /i "%openBrowser%"=="y" start http://localhost:3000

pause