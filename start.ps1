# Divisor Wave Complex Analysis - Startup Script
# This script starts both the Python FastAPI backend and Next.js frontend

Write-Host "Starting Divisor Wave Complex Analysis..." -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Gray

# Get the script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = $ScriptDir

# Define paths
$PythonDir = Join-Path $ProjectRoot "divisor-wave-python"
$NextJsDir = Join-Path $ProjectRoot "divisor-wave-nextjs"

# Check if directories exist
if (-not (Test-Path $PythonDir)) {
    Write-Host "Error: Python directory not found at $PythonDir" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $NextJsDir)) {
    Write-Host "Error: Next.js directory not found at $NextJsDir" -ForegroundColor Red
    exit 1
}

# Function to start backend
function Start-Backend {
    Write-Host "Starting Python FastAPI Backend..." -ForegroundColor Yellow
    
    # Change to Python directory
    Set-Location $PythonDir
    
    # Check if requirements are installed
    Write-Host "Checking Python dependencies..." -ForegroundColor Gray
    try {
        python -c "import fastapi, uvicorn, numpy, scipy, matplotlib, numba" 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
            pip install -r requirements.txt --quiet
        }
    }
    catch {
        Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
        pip install -r requirements.txt --quiet
    }
    
    # Start the backend server
    Write-Host "Launching FastAPI server at http://localhost:8000" -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PythonDir'; python src/api/main.py" -WindowStyle Normal
    
    # Wait a moment for server to start
    Start-Sleep -Seconds 3
}

# Function to start frontend
function Start-Frontend {
    Write-Host "Starting Next.js Frontend..." -ForegroundColor Blue
    
    # Change to Next.js directory
    Set-Location $NextJsDir
    
    # Check if node_modules exists
    if (-not (Test-Path "node_modules")) {
        Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
        npm install --legacy-peer-deps
    }
    
    # Start the frontend server
    Write-Host "Launching Next.js server at http://localhost:3000" -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$NextJsDir'; npm run dev" -WindowStyle Normal
    
    # Wait a moment for server to start
    Start-Sleep -Seconds 3
}

# Function to check if servers are running
function Test-Servers {
    Write-Host "Checking server status..." -ForegroundColor Gray
    
    # Test backend
    try {
        $backend = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5 -UseBasicParsing
        if ($backend.StatusCode -eq 200) {
            Write-Host "Backend: Running at http://localhost:8000" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "Backend: Starting up..." -ForegroundColor Yellow
    }
    
    # Test frontend
    try {
        $frontend = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 5 -UseBasicParsing
        if ($frontend.StatusCode -eq 200) {
            Write-Host "Frontend: Running at http://localhost:3000" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "Frontend: Starting up..." -ForegroundColor Yellow
    }
}

# Main execution
try {
    # Start backend first
    Start-Backend
    
    # Start frontend
    Start-Frontend
    
    # Check status
    Write-Host ""
    Write-Host "Waiting for servers to fully start..." -ForegroundColor Gray
    Start-Sleep -Seconds 5
    
    Test-Servers
    
    Write-Host ""
    Write-Host "Divisor Wave Complex Analysis is starting up!" -ForegroundColor Cyan
    Write-Host "Frontend:  http://localhost:3000" -ForegroundColor White
    Write-Host "Backend:   http://localhost:8000" -ForegroundColor White
    Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor White
    Write-Host ""
    Write-Host "Ready to explore infinite products and prime number relationships!" -ForegroundColor Magenta
    Write-Host "Tip: Use Ctrl+C in each terminal window to stop the servers" -ForegroundColor Gray
    
    # Ask if user wants to open browser
    $openBrowser = Read-Host "Would you like to open the application in your browser? (y/N)"
    if ($openBrowser -eq "y" -or $openBrowser -eq "Y") {
        Start-Process "http://localhost:3000"
    }
    
}
catch {
    Write-Host "Error starting servers: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
finally {
    # Return to original directory
    Set-Location $ProjectRoot
}

Write-Host ""
Write-Host "Startup script completed!" -ForegroundColor Green