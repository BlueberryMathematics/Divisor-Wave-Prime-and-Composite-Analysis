# Complete PowerShell Startup Script for Divisor Wave System
# Starts all 4 APIs: Python Backend, Neural Networks, AI Agents, and Next.js Frontend
# Run this from the main project directory

param(
    [switch]$SkipNeuralNetworks,  # Skip neural network API if dependencies not installed
    [switch]$SkipAgents,          # Skip AI agent API if dependencies not installed
    [switch]$Help                 # Show help
)

if ($Help) {
    Write-Host "🌊 Divisor Wave Complete System Launcher" -ForegroundColor Cyan
    Write-Host "========================================"
    Write-Host ""
    Write-Host "Usage:"
    Write-Host "  .\start-system.ps1               # Start all 4 APIs"
    Write-Host "  .\start-system.ps1 -SkipNeuralNetworks    # Skip neural network API"
    Write-Host "  .\start-system.ps1 -SkipAgents            # Skip AI agent API"
    Write-Host ""
    Write-Host "APIs Started:"
    Write-Host "  • Python Mathematical Backend:  http://localhost:8000"
    Write-Host "  • Neural Network API:           http://localhost:8001"
    Write-Host "  • AI Agent API:                 http://localhost:8002"
    Write-Host "  • Next.js Frontend:             http://localhost:3000"
    exit 0
}

Write-Host "🌊 Starting Complete Divisor Wave System" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# Get current directory and paths
$ProjectDir = Get-Location
$PythonDir = Join-Path $ProjectDir "divisor-wave-python"
$NextJsDir = Join-Path $ProjectDir "divisor-wave-nextjs"
$AgentDir = Join-Path $ProjectDir "divisor-wave-agent"
$NeuralDir = Join-Path $ProjectDir "divisor-wave-neural-networks"

Write-Host "📂 Project Directory: $ProjectDir" -ForegroundColor Gray

# Track all started processes for cleanup
$RunningProcesses = @()

# Check directories
$RequiredDirs = @($PythonDir, $NextJsDir)
$OptionalDirs = @($AgentDir, $NeuralDir)

foreach ($dir in $RequiredDirs) {
    if (-not (Test-Path $dir)) {
        Write-Host "❌ Required directory not found: $dir" -ForegroundColor Red
        exit 1
    }
}

# Function to start a server process
function Start-ServerProcess {
    param(
        [string]$Name,
        [string]$WorkingDir,
        [string]$Executable,
        [array]$Arguments,
        [int]$Port,
        [bool]$Required = $true
    )
    
    try {
        Write-Host "🚀 Starting $Name on port $Port..." -ForegroundColor Green
        
        $Process = Start-Process -FilePath $Executable -ArgumentList $Arguments -WorkingDirectory $WorkingDir -PassThru -WindowStyle Hidden
        
        if ($Process) {
            $script:RunningProcesses += @{
                Name = $Name
                Process = $Process
                Port = $Port
                Required = $Required
            }
            Write-Host "✅ $Name started successfully on http://localhost:$Port" -ForegroundColor Green
            return $Process
        } else {
            Write-Host "❌ Failed to start $Name" -ForegroundColor Red
            return $null
        }
    } catch {
        Write-Host "❌ Error starting $Name`: $_" -ForegroundColor Red
        if ($Required) {
            throw
        }
        return $null
    }
}

# Function to check if port is available
function Test-PortAvailable {
    param([int]$Port)
    try {
        $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Any, $Port)
        $listener.Start()
        $listener.Stop()
        return $true
    } catch {
        return $false
    }
}

# Check if ports are available
$Ports = @(8000, 8001, 8002, 3000)
foreach ($port in $Ports) {
    if (-not (Test-PortAvailable -Port $port)) {
        Write-Host "⚠️  Port $port is already in use" -ForegroundColor Yellow
    }
}

try {
    # 1. Start Python Mathematical Backend (Required)
    Write-Host "`n1️⃣ Starting Python Mathematical Backend..." -ForegroundColor Blue
    Set-Location $PythonDir
    
    $VenvPython = Join-Path $PythonDir "venv\Scripts\python.exe"
    if (-not (Test-Path $VenvPython)) {
        Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
        Write-Host "💡 Please run these commands first:" -ForegroundColor Yellow
        Write-Host "   cd divisor-wave-python" -ForegroundColor Gray
        Write-Host "   python -m venv venv" -ForegroundColor Gray
        Write-Host "   venv\Scripts\Activate.ps1" -ForegroundColor Gray
        Write-Host "   pip install -r requirements.txt" -ForegroundColor Gray
        exit 1
    }
    
    $PythonProcess = Start-ServerProcess -Name "Python Mathematical Backend" -WorkingDir $PythonDir -Executable $VenvPython -Arguments @("-m", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload") -Port 8000 -Required $true
    Start-Sleep -Seconds 3
    
    # 2. Start Neural Network API (Optional)
    Write-Host "`n2️⃣ Starting Neural Network API..." -ForegroundColor Blue
    if (-not $SkipNeuralNetworks -and (Test-Path $NeuralDir)) {
        Set-Location $NextJsDir
        if (Test-Path "neural-api-server.py") {
            $NeuralProcess = Start-ServerProcess -Name "Neural Network API" -WorkingDir $NextJsDir -Executable "python" -Arguments @("neural-api-server.py") -Port 8001 -Required $false
            Start-Sleep -Seconds 2
        } else {
            Write-Host "⚠️  neural-api-server.py not found in $NextJsDir" -ForegroundColor Yellow
        }
    } else {
        Write-Host "⏩ Neural Network API skipped" -ForegroundColor Gray
    }
    
    # 3. Start AI Agent API (Optional)
    Write-Host "`n3️⃣ Starting AI Agent API..." -ForegroundColor Blue
    if (-not $SkipAgents -and (Test-Path $AgentDir)) {
        Set-Location $NextJsDir
        if (Test-Path "agent-api-server.py") {
            $AgentProcess = Start-ServerProcess -Name "AI Agent API" -WorkingDir $NextJsDir -Executable "python" -Arguments @("agent-api-server.py") -Port 8002 -Required $false
            Start-Sleep -Seconds 2
        } else {
            Write-Host "⚠️  agent-api-server.py not found in $NextJsDir" -ForegroundColor Yellow
        }
    } else {
        Write-Host "⏩ AI Agent API skipped" -ForegroundColor Gray
    }
    
    # 4. Show status summary
    Write-Host "`n📊 System Status Summary:" -ForegroundColor Cyan
    Write-Host "=========================="
    foreach ($proc in $RunningProcesses) {
        $status = if ($proc.Process.HasExited) { "❌ Stopped" } else { "✅ Running" }
        Write-Host "   • $($proc.Name): $status on port $($proc.Port)" -ForegroundColor $(if ($proc.Process.HasExited) { "Red" } else { "Green" })
    }
    
    Write-Host "`n🌐 Available Endpoints:" -ForegroundColor Cyan
    Write-Host "   • Python Backend:     http://localhost:8000"
    Write-Host "   • API Documentation:  http://localhost:8000/docs"
    Write-Host "   • Neural Networks:    http://localhost:8001"
    Write-Host "   • AI Agents:          http://localhost:8002"
    Write-Host "   • Next.js Frontend:   http://localhost:3000"
    
    # 5. Start Next.js Frontend (Blocking)
    Write-Host "`n4️⃣ Starting Next.js Frontend..." -ForegroundColor Blue
    Set-Location $NextJsDir
    
    # Check if node_modules exists
    if (-not (Test-Path "node_modules")) {
        Write-Host "📦 Installing Node.js dependencies..." -ForegroundColor Yellow
        npm install
    }
    
    Write-Host "`n🎯 Complete Divisor Wave System Ready!" -ForegroundColor Green
    Write-Host "========================================"
    Write-Host "⚛️  Starting Next.js Frontend..." -ForegroundColor Green
    Write-Host "🚀 Frontend will be available at http://localhost:3000" -ForegroundColor Cyan
    Write-Host "`n⚠️  Keep this terminal open to maintain all services" -ForegroundColor Yellow
    Write-Host "   Press Ctrl+C to stop all servers" -ForegroundColor Yellow
    Write-Host "========================================"
    
    # Start Next.js development server (blocking)
    npm run dev
    
} catch {
    Write-Host "`n❌ Error during startup: $_" -ForegroundColor Red
} finally {
    # Cleanup all processes
    Write-Host "`n🛑 Shutting down all services..." -ForegroundColor Yellow
    foreach ($proc in $RunningProcesses) {
        if ($proc.Process -and -not $proc.Process.HasExited) {
            Write-Host "   Stopping $($proc.Name)..." -ForegroundColor Gray
            try {
                $proc.Process.Kill()
            } catch {
                Write-Host "   Failed to stop $($proc.Name)" -ForegroundColor Red
            }
        }
    }
    Write-Host "✅ All services stopped" -ForegroundColor Green
}