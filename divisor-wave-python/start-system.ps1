# Ultra-Fast Legacy System Startup Script
# Comprehensive PowerShell automation for complete system management

param(
    [switch]$Backend,           # Start only backend API
    [switch]$Frontend,          # Start only frontend
    [switch]$Both,              # Start both services (default)
    [switch]$Test,              # Run system tests
    [switch]$Install,           # Install dependencies only
    [switch]$Clean,             # Clean build artifacts
    [switch]$Help               # Show help
)

# Configuration
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$PYTHON_DIR = $SCRIPT_DIR
$NEXTJS_DIR = Join-Path $SCRIPT_DIR "divisor-wave-nextjs"
$API_DIR = Join-Path $SCRIPT_DIR "src\api"
$VENV_DIR = Join-Path $SCRIPT_DIR "venv"

# Colors for output
function Write-ColorText {
    param(
        [string]$Text,
        [string]$Color = "White"
    )
    Write-Host $Text -ForegroundColor $Color
}

function Write-Success { Write-ColorText $args[0] "Green" }
function Write-Warning { Write-ColorText $args[0] "Yellow" }
function Write-Error { Write-ColorText $args[0] "Red" }
function Write-Info { Write-ColorText $args[0] "Cyan" }

function Show-Help {
    Write-Host "=" * 70 -ForegroundColor Blue
    Write-ColorText "🚀 ULTRA-FAST LEGACY SYSTEM STARTUP SCRIPT" "Blue"
    Write-Host "=" * 70 -ForegroundColor Blue
    Write-Host ""
    Write-Host "USAGE:" -ForegroundColor Yellow
    Write-Host "  .\start-system.ps1 [options]" -ForegroundColor White
    Write-Host ""
    Write-Host "OPTIONS:" -ForegroundColor Yellow
    Write-Host "  -Backend       Start only Python FastAPI backend" -ForegroundColor White
    Write-Host "  -Frontend      Start only Next.js frontend" -ForegroundColor White
    Write-Host "  -Both          Start both services (default)" -ForegroundColor White
    Write-Host "  -Test          Run comprehensive system tests" -ForegroundColor White
    Write-Host "  -Install       Install all dependencies only" -ForegroundColor White
    Write-Host "  -Clean         Clean build artifacts and cache" -ForegroundColor White
    Write-Host "  -Help          Show this help message" -ForegroundColor White
    Write-Host ""
    Write-Host "EXAMPLES:" -ForegroundColor Yellow
    Write-Host "  .\start-system.ps1                  # Start both services" -ForegroundColor Gray
    Write-Host "  .\start-system.ps1 -Backend         # Backend only" -ForegroundColor Gray
    Write-Host "  .\start-system.ps1 -Frontend        # Frontend only" -ForegroundColor Gray
    Write-Host "  .\start-system.ps1 -Test            # Run tests" -ForegroundColor Gray
    Write-Host "  .\start-system.ps1 -Install         # Install deps" -ForegroundColor Gray
    Write-Host ""
    Write-Host "INTERACTIVE COMMANDS (while running):" -ForegroundColor Yellow
    Write-Host "  /help          Show available commands" -ForegroundColor Gray
    Write-Host "  /status        Show system status" -ForegroundColor Gray
    Write-Host "  /restart-backend   Restart Python API" -ForegroundColor Gray
    Write-Host "  /restart-frontend  Restart Next.js dev server" -ForegroundColor Gray
    Write-Host "  /functions     List available functions" -ForegroundColor Gray
    Write-Host "  /test          Run quick API test" -ForegroundColor Gray
    Write-Host "  /stop          Stop all services" -ForegroundColor Gray
    Write-Host ""
    Write-Host "=" * 70 -ForegroundColor Blue
}

function Test-PowerShellVersion {
    if ($PSVersionTable.PSVersion.Major -lt 5) {
        Write-Error "❌ PowerShell 5.0 or higher required"
        Write-Warning "Current version: $($PSVersionTable.PSVersion)"
        return $false
    }
    Write-Success "✅ PowerShell version: $($PSVersionTable.PSVersion)"
    return $true
}

function Test-PythonInstallation {
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "✅ Python found: $pythonVersion"
            return $true
        }
    } catch {}
    
    Write-Error "❌ Python not found in PATH"
    Write-Warning "Please install Python 3.8+ and add to PATH"
    return $false
}

function Test-NodeInstallation {
    try {
        $nodeVersion = node --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "✅ Node.js found: $nodeVersion"
            
            $npmVersion = npm --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Success "✅ npm found: v$npmVersion"
                return $true
            }
        }
    } catch {}
    
    Write-Error "❌ Node.js/npm not found in PATH"
    Write-Warning "Please install Node.js 18+ and add to PATH"
    return $false
}

function Test-VirtualEnvironment {
    if (Test-Path $VENV_DIR) {
        Write-Success "✅ Virtual environment exists"
        return $true
    }
    
    Write-Warning "⚠️  Virtual environment not found, creating..."
    try {
        Set-Location $PYTHON_DIR
        python -m venv venv
        if ($LASTEXITCODE -eq 0) {
            Write-Success "✅ Virtual environment created"
            return $true
        } else {
            Write-Error "❌ Failed to create virtual environment"
            return $false
        }
    } catch {
        Write-Error "❌ Error creating virtual environment: $_"
        return $false
    }
}

function Activate-VirtualEnvironment {
    $activateScript = Join-Path $VENV_DIR "Scripts\Activate.ps1"
    
    if (Test-Path $activateScript) {
        try {
            & $activateScript
            Write-Success "✅ Virtual environment activated"
            return $true
        } catch {
            Write-Error "❌ Failed to activate virtual environment: $_"
        }
    } else {
        Write-Error "❌ Activation script not found: $activateScript"
    }
    return $false
}

function Install-PythonDependencies {
    Write-Info "📦 Installing Python dependencies..."
    
    $packages = @(
        "fastapi", 
        "uvicorn[standard]", 
        "numpy", 
        "matplotlib", 
        "scipy", 
        "numba", 
        "sympy", 
        "pydantic",
        "requests",
        "psutil"
    )
    
    try {
        foreach ($package in $packages) {
            Write-Host "Installing $package..." -ForegroundColor Gray
            python -m pip install $package --upgrade
            if ($LASTEXITCODE -ne 0) {
                Write-Warning "⚠️  Warning: Failed to install $package"
            }
        }
        Write-Success "✅ Python dependencies installed"
        return $true
    } catch {
        Write-Error "❌ Error installing Python dependencies: $_"
        return $false
    }
}

function Install-NodeDependencies {
    if (-not (Test-Path $NEXTJS_DIR)) {
        Write-Warning "⚠️  Next.js directory not found: $NEXTJS_DIR"
        return $false
    }
    
    Write-Info "📦 Installing Node.js dependencies..."
    
    try {
        Set-Location $NEXTJS_DIR
        npm install
        if ($LASTEXITCODE -eq 0) {
            Write-Success "✅ Node.js dependencies installed"
            return $true
        } else {
            Write-Error "❌ npm install failed"
            return $false
        }
    } catch {
        Write-Error "❌ Error installing Node.js dependencies: $_"
        return $false
    } finally {
        Set-Location $SCRIPT_DIR
    }
}

function Test-APIHealth {
    Write-Info "🔍 Testing API health..."
    
    $maxAttempts = 30
    $attempt = 0
    
    while ($attempt -lt $maxAttempts) {
        try {
            $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 2 -ErrorAction Stop
            if ($response.status -eq "healthy") {
                Write-Success "✅ API is healthy!"
                Write-Info "   Version: $($response.version)"
                Write-Info "   Functions: $($response.features.builtin_functions) built-in, $($response.features.custom_functions) custom"
                return $true
            }
        } catch {
            # API not ready yet
        }
        
        $attempt++
        Start-Sleep -Seconds 1
        Write-Host "." -NoNewline -ForegroundColor Gray
    }
    
    Write-Warning "⚠️  API health check timeout"
    return $false
}

function Test-FrontendHealth {
    Write-Info "🔍 Testing frontend health..."
    
    $maxAttempts = 60  # Frontend takes longer to start
    $attempt = 0
    
    while ($attempt -lt $maxAttempts) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 2 -ErrorAction Stop
            if ($response.StatusCode -eq 200) {
                Write-Success "✅ Frontend is healthy!"
                return $true
            }
        } catch {
            # Frontend not ready yet
        }
        
        $attempt++
        Start-Sleep -Seconds 2
        Write-Host "." -NoNewline -ForegroundColor Gray
    }
    
    Write-Warning "⚠️  Frontend health check timeout"
    return $false
}

function Start-Backend {
    Write-Info "🚀 Starting Python FastAPI backend..."
    
    if (-not (Test-Path $API_DIR)) {
        Write-Error "❌ API directory not found: $API_DIR"
        return $false
    }
    
    try {
        Set-Location $API_DIR
        
        # Start the API in the background
        $job = Start-Job -ScriptBlock {
            param($apiDir, $venvDir)
            
            Set-Location $apiDir
            
            # Activate virtual environment
            $activateScript = Join-Path $venvDir "Scripts\Activate.ps1"
            & $activateScript
            
            # Start the API
            python ultra_fast_legacy_api.py
        } -ArgumentList $API_DIR, $VENV_DIR
        
        Write-Success "✅ Backend started (Job ID: $($job.Id))"
        
        # Test API health
        Test-APIHealth
        
        return $true
        
    } catch {
        Write-Error "❌ Error starting backend: $_"
        return $false
    } finally {
        Set-Location $SCRIPT_DIR
    }
}

function Start-Frontend {
    Write-Info "🚀 Starting Next.js frontend..."
    
    if (-not (Test-Path $NEXTJS_DIR)) {
        Write-Error "❌ Next.js directory not found: $NEXTJS_DIR"
        return $false
    }
    
    try {
        Set-Location $NEXTJS_DIR
        
        # Start Next.js dev server in background
        $job = Start-Job -ScriptBlock {
            param($nextjsDir)
            Set-Location $nextjsDir
            npm run dev
        } -ArgumentList $NEXTJS_DIR
        
        Write-Success "✅ Frontend started (Job ID: $($job.Id))"
        
        # Test frontend health
        Test-FrontendHealth
        
        return $true
        
    } catch {
        Write-Error "❌ Error starting frontend: $_"
        return $false
    } finally {
        Set-Location $SCRIPT_DIR
    }
}

function Start-Both {
    Write-Info "🚀 Starting both backend and frontend..."
    
    # Start backend first
    if (Start-Backend) {
        # Wait a moment for backend to stabilize
        Start-Sleep -Seconds 3
        
        # Start frontend
        if (Start-Frontend) {
            Write-Success "🎉 Both services started successfully!"
            Show-AccessInfo
            Show-InteractiveHelp
            return $true
        } else {
            Write-Warning "⚠️  Backend started but frontend failed"
            return $false
        }
    } else {
        Write-Error "❌ Failed to start backend"
        return $false
    }
}

function Show-AccessInfo {
    Write-Host ""
    Write-Host "=" * 60 -ForegroundColor Green
    Write-ColorText "🎉 SYSTEM READY!" "Green"
    Write-Host "=" * 60 -ForegroundColor Green
    Write-Host ""
    Write-ColorText "📡 Backend API:  http://localhost:8000" "Cyan"
    Write-ColorText "🌐 Frontend UI:  http://localhost:3000" "Cyan"
    Write-ColorText "📊 API Status:   http://localhost:8000/system/status" "Cyan"
    Write-ColorText "❤️  Health Check: http://localhost:8000/health" "Cyan"
    Write-Host ""
    Write-Host "=" * 60 -ForegroundColor Green
}

function Show-InteractiveHelp {
    Write-Host ""
    Write-ColorText "🎮 INTERACTIVE COMMANDS AVAILABLE:" "Yellow"
    Write-Host "Type '/' followed by command while backend is running" -ForegroundColor Gray
    Write-Host "  /help /status /functions /test /restart-backend /stop" -ForegroundColor Gray
    Write-Host ""
}

function Run-SystemTests {
    Write-Info "🧪 Running comprehensive system tests..."
    
    try {
        Set-Location $PYTHON_DIR
        
        if (Test-Path "test_complete_system.py") {
            python test_complete_system.py
            if ($LASTEXITCODE -eq 0) {
                Write-Success "✅ All tests passed!"
                return $true
            } else {
                Write-Warning "⚠️  Some tests failed"
                return $false
            }
        } else {
            Write-Warning "⚠️  Test script not found"
            return $false
        }
    } catch {
        Write-Error "❌ Error running tests: $_"
        return $false
    }
}

function Clean-BuildArtifacts {
    Write-Info "🧹 Cleaning build artifacts..."
    
    # Python cache
    Get-ChildItem -Path $PYTHON_DIR -Recurse -Name "__pycache__" | ForEach-Object {
        Remove-Item -Path $_ -Recurse -Force
        Write-Host "Removed: $_" -ForegroundColor Gray
    }
    
    # Node modules (optional - commented out as it takes time to reinstall)
    # if (Test-Path (Join-Path $NEXTJS_DIR "node_modules")) {
    #     Remove-Item -Path (Join-Path $NEXTJS_DIR "node_modules") -Recurse -Force
    #     Write-Host "Removed: node_modules" -ForegroundColor Gray
    # }
    
    # Next.js build cache
    if (Test-Path (Join-Path $NEXTJS_DIR ".next")) {
        Remove-Item -Path (Join-Path $NEXTJS_DIR ".next") -Recurse -Force
        Write-Host "Removed: .next build cache" -ForegroundColor Gray
    }
    
    Write-Success "✅ Build artifacts cleaned"
}

# Main execution logic
function Main {
    Write-Host ""
    Write-Host "=" * 70 -ForegroundColor Blue
    Write-ColorText "🚀 ULTRA-FAST LEGACY SYSTEM STARTUP" "Blue"
    Write-Host "=" * 70 -ForegroundColor Blue
    Write-Host ""
    
    # Show help if requested
    if ($Help) {
        Show-Help
        return
    }
    
    # Clean if requested
    if ($Clean) {
        Clean-BuildArtifacts
        return
    }
    
    # System checks
    if (-not (Test-PowerShellVersion)) { return }
    if (-not (Test-PythonInstallation)) { return }
    if (-not (Test-VirtualEnvironment)) { return }
    if (-not (Activate-VirtualEnvironment)) { return }
    
    # Install dependencies if requested or needed
    if ($Install -or -not (Test-Path (Join-Path $VENV_DIR "Lib\site-packages\fastapi"))) {
        if (-not (Install-PythonDependencies)) { return }
    }
    
    if (($Frontend -or $Both -or -not $Backend) -and (Test-Path $NEXTJS_DIR)) {
        if (-not (Test-NodeInstallation)) { return }
        if ($Install -or -not (Test-Path (Join-Path $NEXTJS_DIR "node_modules"))) {
            if (-not (Install-NodeDependencies)) { return }
        }
    }
    
    # Run tests if requested
    if ($Test) {
        Run-SystemTests
        return
    }
    
    # Start services
    if ($Backend) {
        Start-Backend
    } elseif ($Frontend) {
        Start-Frontend
    } else {
        # Default: start both
        Start-Both
    }
    
    # Keep script running to show status
    if ($Backend -or $Frontend -or $Both -or (-not ($Install -or $Clean -or $Test))) {
        Write-Info "Press Ctrl+C to stop services and exit"
        try {
            while ($true) {
                Start-Sleep -Seconds 10
                # Could add periodic health checks here
            }
        } catch {
            Write-Info "Shutting down..."
        }
    }
}

# Error handling
try {
    Main
} catch {
    Write-Error "❌ Unexpected error: $_"
    Write-Warning "Please check the error message and try again"
} finally {
    # Cleanup jobs if they exist
    Get-Job | Stop-Job -PassThru | Remove-Job
    Set-Location $SCRIPT_DIR
}