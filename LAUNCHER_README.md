# Divisor Wave System - Complete Launcher Guide

## Overview

The Divisor Wave system consists of **4 separate APIs** that work together to provide a complete mathematical analysis platform:

### 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DIVISOR WAVE SYSTEM                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │ Python Backend  │  │ Neural Network  │                  │
│  │ Port: 8000      │  │ API Port: 8001  │                  │
│  │ (Required)      │  │ (Optional)      │                  │
│  └─────────────────┘  └─────────────────┘                  │
│                                                             │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │ AI Agent API    │  │ Next.js         │                  │
│  │ Port: 8002      │  │ Frontend        │                  │
│  │ (Optional)      │  │ Port: 3000      │                  │
│  └─────────────────┘  └─────────────────┘                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 📋 API Components

### 1. Python Mathematical Backend (Port 8000) - **REQUIRED**
- **Location**: `divisor-wave-python/src/api/main.py`
- **Purpose**: Core mathematical functions and plotting
- **Dependencies**: `divisor-wave-python/venv/`
- **Features**:
  - 38 mathematical functions
  - LaTeX formula database
  - GPU/JIT accelerated computations
  - Function registry system

### 2. Neural Network API (Port 8001) - **OPTIONAL**
- **Location**: `divisor-wave-nextjs/neural-api-server.py`
- **Purpose**: AI-powered mathematical discovery using neural networks
- **Dependencies**: `divisor-wave-neural-networks/` components
- **Features**:
  - Tetrahedral networks
  - Crystal embeddings
  - Pattern discovery
  - Mathematical sequence prediction

### 3. AI Agent API (Port 8002) - **OPTIONAL**
- **Location**: `divisor-wave-nextjs/agent-api-server.py`
- **Purpose**: LLM-powered research agents for mathematical analysis
- **Dependencies**: `divisor-wave-agent/` components
- **Features**:
  - Mathematical research agents
  - Discovery workflows
  - Pattern recognition
  - Automated theorem exploration

### 4. Next.js Frontend (Port 3000) - **REQUIRED**
- **Location**: `divisor-wave-nextjs/`
- **Purpose**: Interactive web interface
- **Dependencies**: Node.js modules
- **Features**:
  - Interactive function explorer
  - Real-time plotting
  - LaTeX rendering
  - AI integration dashboard

## 🚀 Quick Start

### Option 1: PowerShell Launcher (Recommended)
```powershell
# Start all 4 APIs
.\start-system.ps1

# Start with options
.\start-system.ps1 -SkipNeuralNetworks    # Skip neural API
.\start-system.ps1 -SkipAgents            # Skip agent API
.\start-system.ps1 -Help                  # Show help
```

### Option 2: Python Launcher
```bash
# Start all 4 APIs
python start-system.py

# Start with options
python start-system.py --skip-neural     # Skip neural API
python start-system.py --skip-agents     # Skip agent API
python start-system.py --help           # Show help
```

### Option 3: Manual Startup
```bash
# Terminal 1 - Python Backend (Required)
cd divisor-wave-python
venv\Scripts\Activate.ps1
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Neural Network API (Optional)
cd divisor-wave-nextjs
python neural-api-server.py

# Terminal 3 - AI Agent API (Optional)
cd divisor-wave-nextjs  
python agent-api-server.py

# Terminal 4 - Next.js Frontend (Required)
cd divisor-wave-nextjs
npm run dev
```

## 📊 System Status After Launch

When all APIs are running, you should see:

```
📊 System Status Summary:
==========================
   ✅ Python Mathematical Backend: Running on port 8000
   ✅ Neural Network API: Running on port 8001
   ✅ AI Agent API: Running on port 8002
   ✅ Next.js Frontend: Running on port 3000

🌐 Available Endpoints:
   • Python Backend:     http://localhost:8000
   • API Documentation:  http://localhost:8000/docs
   • Neural Networks:    http://localhost:8001
   • AI Agents:          http://localhost:8002
   • Next.js Frontend:   http://localhost:3000
```

## 🔧 Prerequisites

### Required Dependencies
```bash
# Python Backend
cd divisor-wave-python
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Next.js Frontend
cd divisor-wave-nextjs
npm install
```

### Optional Dependencies
```bash
# Neural Networks (for port 8001)
cd divisor-wave-neural-networks
pip install -r requirements.txt

# AI Agents (for port 8002)
cd divisor-wave-agent
pip install -r requirements.txt
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Port Already in Use
```
⚠️  Port 8000 is already in use
```
**Solution**: Check for existing processes on that port or kill them:
```bash
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

#### 2. Virtual Environment Not Found
```
❌ Virtual environment not found!
```
**Solution**: Create and activate the virtual environment:
```bash
cd divisor-wave-python
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### 3. Node Dependencies Missing
```
❌ Node.js dependencies not installed
```
**Solution**: Install Node.js dependencies:
```bash
cd divisor-wave-nextjs
npm install
```

#### 4. Optional APIs Failed to Start
```
⚠️  neural-api-server.py not found
```
**Solution**: This is normal if optional components aren't set up. The system will work with just the required components.

### Selective API Starting

If you want to skip optional APIs (neural networks or agents) due to missing dependencies:

```powershell
# Skip both optional APIs
.\start-system.ps1 -SkipNeuralNetworks -SkipAgents

# Skip just neural networks
.\start-system.ps1 -SkipNeuralNetworks

# Skip just agents
.\start-system.ps1 -SkipAgents
```

## 📚 API Documentation

Once the system is running:

- **Python Backend Docs**: http://localhost:8000/docs
- **Neural API Docs**: http://localhost:8001/docs  
- **Agent API Docs**: http://localhost:8002/docs
- **Frontend Interface**: http://localhost:3000

## 🔄 Development Workflow

For development, the launcher provides:

- **Auto-reload**: Python APIs restart on code changes
- **Hot reload**: Next.js frontend updates automatically
- **Process management**: Graceful shutdown with Ctrl+C
- **Error handling**: Detailed error messages for troubleshooting

## 💡 Integration Notes

The system is designed for modularity:

- **Core functionality** requires only Python Backend + Next.js Frontend
- **Enhanced features** are available when Neural Network and Agent APIs are running
- **Graceful degradation** when optional components are missing
- **Independent scaling** of each component

This architecture allows you to run a basic system with just 2 APIs or the complete AI-enhanced system with all 4 APIs.