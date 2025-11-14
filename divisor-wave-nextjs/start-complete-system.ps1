# PowerShell Complete Integration Setup Script
# Cross-platform setup for the complete integrated system

Write-Host ""
Write-Host "🌊 Divisor Wave Complete Integration Setup" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "📋 Setting up integrated mathematical discovery system..." -ForegroundColor Yellow
Write-Host "   • Python Backend (divisor-wave-python)" -ForegroundColor Gray
Write-Host "   • Neural Networks (divisor-wave-neural-networks)" -ForegroundColor Gray
Write-Host "   • AI Agents (divisor-wave-agent)" -ForegroundColor Gray
Write-Host "   • Next.js Frontend with AI integration" -ForegroundColor Gray
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "package.json")) {
    Write-Host "❌ Error: Please run this script from the divisor-wave-nextjs directory" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "1️⃣ Installing Next.js dependencies..." -ForegroundColor Green
try {
    npm install
    Write-Host "✅ Next.js dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install Next.js dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "2️⃣ Installing Python dependencies for Neural Networks..." -ForegroundColor Green
if (Test-Path "..\divisor-wave-neural-networks\requirements.txt") {
    try {
        pip install -r ..\divisor-wave-neural-networks\requirements.txt
        Write-Host "✅ Neural network dependencies installed" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  Some neural network dependencies may have failed to install" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  Neural network requirements.txt not found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "3️⃣ Installing Python dependencies for API servers..." -ForegroundColor Green
try {
    pip install fastapi uvicorn pydantic
    Write-Host "✅ API server dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install API server dependencies" -ForegroundColor Red
}

Write-Host ""
Write-Host "4️⃣ Starting integrated backend services..." -ForegroundColor Green
try {
    # Start backend services in background
    Start-Process python -ArgumentList "start-integrated-backend.py" -WindowStyle Hidden
    Write-Host "✅ Backend services starting..." -ForegroundColor Green
} catch {
    Write-Host "⚠️  Backend services may not have started properly" -ForegroundColor Yellow
    Write-Host "   You can start them manually with: python start-integrated-backend.py" -ForegroundColor Gray
}

Write-Host ""
Write-Host "5️⃣ Waiting for services to initialize..." -ForegroundColor Green
Start-Sleep -Seconds 8

Write-Host ""
Write-Host "6️⃣ Ready to start Next.js frontend..." -ForegroundColor Green
Write-Host ""
Write-Host "🎯 Complete System Setup Complete!" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   • Python Backend:     http://localhost:8000" -ForegroundColor Gray
Write-Host "   • Neural Networks:    http://localhost:8001" -ForegroundColor Gray  
Write-Host "   • AI Agents:          http://localhost:8002" -ForegroundColor Gray
Write-Host "   • Next.js Frontend:   http://localhost:3000" -ForegroundColor Gray
Write-Host ""
Write-Host "🚀 Features Available:" -ForegroundColor Yellow
Write-Host "   • ✨ AI LaTeX Builder (neural network powered)" -ForegroundColor Gray
Write-Host "   • 🧠 Neural Dashboard (full AI toolkit)" -ForegroundColor Gray
Write-Host "   • 💬 AI Mathematical Chat" -ForegroundColor Gray
Write-Host "   • 📊 Real-time Mathematical Visualization" -ForegroundColor Gray
Write-Host "   • 🔍 Pattern Discovery and Analysis" -ForegroundColor Gray
Write-Host ""

Write-Host "🎬 Starting Next.js development server..." -ForegroundColor Green
Write-Host "   Open http://localhost:3000 to access the AI-integrated interface" -ForegroundColor Cyan
Write-Host ""

# Start Next.js development server
npm run dev