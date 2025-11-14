# Complete Integration Setup Script for Windows
# This sets up all dependencies and starts the complete integrated system

@echo off
echo.
echo 🌊 Divisor Wave Complete Integration Setup
echo ================================================
echo.

echo 📋 Setting up integrated mathematical discovery system...
echo    • Python Backend (divisor-wave-python)
echo    • Neural Networks (divisor-wave-neural-networks) 
echo    • AI Agents (divisor-wave-agent)
echo    • Next.js Frontend with AI integration
echo.

REM Check if we're in the right directory
if not exist "package.json" (
    echo ❌ Error: Please run this script from the divisor-wave-nextjs directory
    pause
    exit /b 1
)

echo 1️⃣ Installing Next.js dependencies...
call npm install
if errorlevel 1 (
    echo ❌ Failed to install Next.js dependencies
    pause
    exit /b 1
)
echo ✅ Next.js dependencies installed

echo.
echo 2️⃣ Installing Python dependencies for Neural Networks...
if exist "..\divisor-wave-neural-networks\requirements.txt" (
    pip install -r ..\divisor-wave-neural-networks\requirements.txt
    echo ✅ Neural network dependencies installed
) else (
    echo ⚠️  Neural network requirements.txt not found
)

echo.
echo 3️⃣ Installing Python dependencies for API servers...
pip install fastapi uvicorn pydantic
echo ✅ API server dependencies installed

echo.
echo 4️⃣ Starting integrated backend services...
start "Python Backend" python start-integrated-backend.py

echo.
echo 5️⃣ Waiting for services to initialize...
timeout /t 10 /nobreak

echo.
echo 6️⃣ Starting Next.js frontend with AI integration...
echo.
echo 🎯 Complete System Ready!
echo ================================================
echo    • Python Backend:     http://localhost:8000
echo    • Neural Networks:    http://localhost:8001
echo    • AI Agents:          http://localhost:8002
echo    • Next.js Frontend:   http://localhost:3000
echo.
echo 🚀 Features Available:
echo    • ✨ AI LaTeX Builder (neural network powered)
echo    • 🧠 Neural Dashboard (full AI toolkit)  
echo    • 💬 AI Mathematical Chat
echo    • 📊 Real-time Mathematical Visualization
echo    • 🔍 Pattern Discovery and Analysis
echo.

call npm run dev