# 🚀 Divisor Wave System - Quick Start Guide

## ✅ Issues Fixed

1. **✅ Complete Launcher System**: Now starts all 4 APIs instead of just 2
2. **✅ React Hydration Error**: Fixed browser extension compatibility issues
3. **✅ Next.js Warning**: Updated deprecated turbo config
4. **✅ Process Management**: Proper cleanup when stopping

## 🎯 How to Start the Complete System

### **IMPORTANT: Use the Main Launcher**

Make sure you're in the **main project directory** and run:

```powershell
# Main directory launcher (CORRECT) ✅
M:\_tools\Divisor-Wave-Product-Prime-and-Composite-Analysis> .\start-system.ps1

# NOT this one (old launcher) ❌
M:\_tools\Divisor-Wave-Product-Prime-and-Composite-Analysis\divisor-wave-python> .\src\scripts\start-system.ps1
```

### **Complete System Startup**

```powershell
# Start all 4 APIs (recommended)
.\start-system.ps1

# Start with selective options
.\start-system.ps1 -SkipNeuralNetworks    # Skip neural network API
.\start-system.ps1 -SkipAgents           # Skip AI agent API
.\start-system.ps1 -Help                 # Show help
```

## 📊 Expected Output

When using the **correct launcher**, you should see:

```
🌊 Starting Complete Divisor Wave System
================================================
📂 Project Directory: M:\_tools\Divisor-Wave-Product-Prime-and-Composite-Analysis

1️⃣ Starting Python Mathematical Backend...
🚀 Starting Python Mathematical Backend on port 8000...
✅ Python Mathematical Backend started successfully on http://localhost:8000

2️⃣ Starting Neural Network API...
🚀 Starting Neural Network API on port 8001...
✅ Neural Network API started successfully on http://localhost:8001

3️⃣ Starting AI Agent API...
🚀 Starting AI Agent API on port 8002...
✅ AI Agent API started successfully on http://localhost:8002

📊 System Status Summary:
==========================
   • Python Mathematical Backend: ✅ Running on port 8000
   • Neural Network API: ✅ Running on port 8001
   • AI Agent API: ✅ Running on port 8002

🌐 Available Endpoints:
   • Python Backend:     http://localhost:8000
   • API Documentation:  http://localhost:8000/docs
   • Neural Networks:    http://localhost:8001
   • AI Agents:          http://localhost:8002
   • Next.js Frontend:   http://localhost:3000

4️⃣ Starting Next.js Frontend...
🎯 Complete Divisor Wave System Ready!
```

## 🔧 Troubleshooting

### 1. **Backend Connection Issues**

If you see "❌ Disconnected" in the frontend:

```powershell
# Test backend directly
curl http://localhost:8000/health

# Or check in browser
http://localhost:8000/docs
```

### 2. **Old Launcher Being Used**

If you see the old simple output like:
```
🌊 Starting Divisor Wave System
================================================
🐍 Starting Python Backend API...
⚛️ Starting Next.js Frontend...
```

**Solution**: Make sure you're running from the main directory:
```powershell
cd M:\_tools\Divisor-Wave-Product-Prime-and-Composite-Analysis
.\start-system.ps1
```

### 3. **React Hydration Errors**

The hydration errors have been fixed by adding `suppressHydrationWarning={true}` to handle browser extensions like DarkReader.

### 4. **Port Conflicts**

If ports are already in use:
```powershell
# Stop existing processes
Get-Process | Where-Object {$_.ProcessName -like "*node*" -or $_.ProcessName -like "*python*"} | Stop-Process -Force

# Then restart
.\start-system.ps1
```

## 🌐 System Endpoints

Once running, you'll have access to:

| Service | Port | URL | Purpose |
|---------|------|-----|---------|
| **Python Backend** | 8000 | http://localhost:8000 | Core math functions |
| **API Docs** | 8000 | http://localhost:8000/docs | API documentation |
| **Neural Networks** | 8001 | http://localhost:8001 | AI neural networks |
| **AI Agents** | 8002 | http://localhost:8002 | LlamaIndex research agents |
| **Frontend** | 3000 | http://localhost:3000 | Web interface |

## 🧠 AI Agent Features

The system includes **LlamaIndex-powered AI agents** for mathematical discovery:

### 🤖 Agent Status in Frontend
- **"AI Agents: ✅ Connected"** - API server running
- **"LlamaIndex Agents: Connected & Ready"** - Full AI enabled
- **"Demo Mode"** - Limited responses (LLM setup required)

### 🚀 To Enable Full AI Capabilities
See **[LLAMAINDEX_SETUP.md](./LLAMAINDEX_SETUP.md)** for complete setup instructions:

1. **Install LlamaIndex**: `cd divisor-wave-agent && pip install -r requirements.txt`
2. **Configure LLM**: Set `OPENAI_API_KEY` or other LLM provider
3. **Restart System**: `.\start-system.ps1`

### 🧠 Available AI Agents
- **🔬 Formula Analyst**: Pattern analysis and relationship discovery
- **✅ Analysis Specialist**: Mathematical validation and testing  
- **🎯 Discovery Agent**: New function generation and research

## 🎯 System Architecture

```
┌─────────────────────────────────────────────┐
│            COMPLETE SYSTEM                  │
├─────────────────────────────────────────────┤
│                                             │
│  ┌─────────────┐  ┌─────────────────┐      │
│  │ Python      │  │ Neural Network  │      │
│  │ Backend     │  │ API             │      │
│  │ Port: 8000  │  │ Port: 8001      │      │
│  │ (Core Math) │  │ (AI Discovery)  │      │
│  └─────────────┘  └─────────────────┘      │
│                                             │
│  ┌─────────────┐  ┌─────────────────┐      │
│  │ AI Agent    │  │ Next.js         │      │
│  │ API         │  │ Frontend        │      │
│  │ Port: 8002  │  │ Port: 3000      │      │
│  │ (Research)  │  │ (Interface)     │      │
│  └─────────────┘  └─────────────────┘      │
│                                             │
└─────────────────────────────────────────────┘
```

## ⚡ Performance Notes

- **Backend Connection**: Should connect within 3-5 seconds
- **Neural APIs**: May take longer to start due to model loading
- **Frontend**: Ready in ~3-15 seconds
- **Hot Reload**: All services support live code changes

---

**🎉 You now have a complete, AI-enhanced mathematical analysis platform with all 4 APIs running!**