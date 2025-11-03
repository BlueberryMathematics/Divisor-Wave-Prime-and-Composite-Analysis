#!/usr/bin/env pwsh

Write-Host "Building LaTeX document..." -ForegroundColor Green

# Change to docs directory
$DocsPath = Join-Path $PSScriptRoot ".." "docs"
Push-Location $DocsPath

$DocumentName = "Divisor_Waves_and_their_Connection_to_the_Riemann_Hypothesis"

try {
    Write-Host "Step 1: First pdflatex run..." -ForegroundColor Yellow
    & pdflatex -synctex=1 -interaction=nonstopmode "$DocumentName.tex"
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error in first pdflatex run!" -ForegroundColor Red
        exit 1
    }

    Write-Host "Step 2: Running biber for bibliography..." -ForegroundColor Yellow
    & biber $DocumentName
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Warning: Biber failed, continuing..." -ForegroundColor Red
    }

    Write-Host "Step 3: Second pdflatex run..." -ForegroundColor Yellow
    & pdflatex -synctex=1 -interaction=nonstopmode "$DocumentName.tex"
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error in second pdflatex run!" -ForegroundColor Red
        exit 1
    }

    Write-Host "Step 4: Third pdflatex run..." -ForegroundColor Yellow  
    & pdflatex -synctex=1 -interaction=nonstopmode "$DocumentName.tex"
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error in third pdflatex run!" -ForegroundColor Red
        exit 1
    }

    Write-Host "Build complete!" -ForegroundColor Green
    Write-Host "PDF available at: docs\$DocumentName.pdf" -ForegroundColor Cyan
    
    # Clean up auxiliary files (optional)
    $AuxFiles = @("*.aux", "*.bbl", "*.bcf", "*.blg", "*.log", "*.out", "*.run.xml", "*.synctex.gz")
    foreach ($pattern in $AuxFiles) {
        Get-ChildItem $pattern -ErrorAction SilentlyContinue | Remove-Item -Force
    }
    Write-Host "Cleaned up auxiliary files." -ForegroundColor Gray
    
} catch {
    Write-Host "Build failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
} finally {
    Pop-Location
}

Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')