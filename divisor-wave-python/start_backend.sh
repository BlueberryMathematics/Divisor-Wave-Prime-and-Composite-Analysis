#!/bin/bash

# Startup script for Divisor Wave Complex Analysis Backend

echo "🚀 Starting Divisor Wave Complex Analysis Backend..."

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found. Please run this script from the divisor-wave-python directory."
    exit 1
fi

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Error: Python is not installed or not in PATH."
    exit 1
fi

# Check Python version
python_version=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "📋 Python version: $python_version"

# Install requirements
echo "📦 Installing Python dependencies..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Check if OptimizedSpecialFunctions is available, if not use original
if [ -f "src/core/OptimizedSpecialFunctions.py" ]; then
    echo "⚡ Using OptimizedSpecialFunctions for better performance"
else
    echo "⚠️  Using original Special_Functions.py"
fi

# Start the FastAPI server
echo "🌐 Starting FastAPI server on http://localhost:8000"
echo "📖 API documentation will be available at http://localhost:8000/docs"
echo "🔄 Server will auto-reload on code changes"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd src/api && python main.py