# 🧠 LlamaIndex AI Agents Setup Guide

## Overview

The Divisor Wave system includes **LlamaIndex-powered AI agents** for advanced mathematical discovery. These agents can analyze patterns, generate new functions, and provide mathematical insights.

## 📊 Current System Status

The frontend shows:
- **"AI Agents: ✅ Connected"** - The API server is running
- **"Demo Mode"** or **"LlamaIndex Agents: Connected & Ready"** in the chat

## 🛠️ Setup Instructions

### Step 1: Install LlamaIndex Dependencies

```bash
cd divisor-wave-agent
pip install -r requirements.txt
```

The requirements.txt includes:
```
llama-index
llama-index-embeddings-openai
llama-index-llms-openai
llama-index-readers-file
llama-index-agent-openai
openai
qdrant-client
numpy
pandas
matplotlib
sympy
```

### Step 2: Configure Your LLM

#### Option A: OpenAI (Recommended)
```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-openai-api-key-here"

# Or create .env file in divisor-wave-agent/
echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
```

#### Option B: Other LLM Providers
LlamaIndex supports many providers. Update the agent configuration in:
- `divisor-wave-agent/src/agents/mathematical_research_agent.py`
- `divisor-wave-agent/src/agents/enhanced_mathematical_agents.py`

### Step 3: Test Agent Integration

```bash
# Test the basic agent setup
cd divisor-wave-agent
python demo_ai_system.py

# Test enhanced agents
python -c "
from src.agents.enhanced_mathematical_agents import EnhancedMathematicalKnowledgeBase
kb = EnhancedMathematicalKnowledgeBase()
print('✅ Knowledge base initialized')
"
```

### Step 4: Restart the System

```powershell
# Stop the current system (Ctrl+C in the terminal)
# Then restart with the complete launcher
.\start-system.ps1
```

## 🤖 Available AI Agents

When properly configured, you'll have access to:

### 1. **Formula Analyst** 🔬
- **Purpose**: Pattern analysis and relationship discovery
- **Capabilities**: 
  - Analyzes mathematical formulas from the database
  - Identifies patterns in infinite products
  - Discovers relationships between function families

### 2. **Analysis Specialist** ✅
- **Purpose**: Mathematical validation and testing
- **Capabilities**:
  - Validates mathematical properties
  - Tests function convergence
  - Verifies computational results

### 3. **Discovery Agent** 🎯
- **Purpose**: New function generation and research
- **Capabilities**:
  - Generates new infinite product formulations
  - Creates hybrid function combinations
  - Develops novel mathematical transformations

## 🔧 Troubleshooting

### Issue: "Demo Mode" Message
**Cause**: LlamaIndex agents not properly initialized
**Solution**: 
1. Check API key configuration
2. Verify dependencies are installed
3. Check console logs in the agent-api-server terminal

### Issue: Agent API Not Connected
**Cause**: Port 8002 not running or blocked
**Solution**:
```bash
# Check if port is in use
netstat -ano | findstr :8002

# Restart the complete system
.\start-system.ps1
```

### Issue: LlamaIndex Import Errors
**Cause**: Dependencies not installed
**Solution**:
```bash
cd divisor-wave-agent
pip install --upgrade llama-index
pip install -r requirements.txt
```

## 🚀 Agent Chat Features

When properly configured, the AI chat provides:

- **Intelligent Responses**: Context-aware mathematical assistance
- **Function Analysis**: Deep analysis of the 38 mathematical functions
- **Pattern Discovery**: AI-powered pattern recognition
- **LaTeX Generation**: Automated mathematical expression creation
- **Research Guidance**: Suggestions for mathematical exploration

## 📊 Demo vs Full Mode

| Feature | Demo Mode | Full LlamaIndex Mode |
|---------|-----------|---------------------|
| **Basic Chat** | ✅ Simple responses | ✅ Intelligent conversation |
| **Function Analysis** | ❌ Limited info | ✅ Deep pattern analysis |
| **New Function Generation** | ❌ Not available | ✅ AI-powered creation |
| **Research Insights** | ❌ Basic suggestions | ✅ Advanced mathematical insights |
| **Context Awareness** | ❌ No memory | ✅ Conversation memory |

## 🎯 Usage Examples

Once configured, try these prompts in the AI chat:

```
🔬 Pattern Analysis:
"Analyze the patterns in the Riesz product functions"
"What relationships exist between infinite products and primes?"

🎯 Function Discovery:
"Generate a new infinite product similar to the divisor wave functions"
"Create a variant of the double product function"

✅ Validation:
"Verify the convergence properties of function #23"
"Test the mathematical properties of the enhanced Viète product"
```

## 🔄 Monitoring Agent Status

Check the agent status in multiple places:

1. **Frontend Dashboard**: Shows connection and LlamaIndex status
2. **Server Console**: Detailed startup logs and error messages
3. **Health Endpoint**: `http://localhost:8002/health`
4. **Capabilities Endpoint**: `http://localhost:8002/capabilities`

## 💡 Advanced Configuration

### Custom LLM Configuration
Edit `divisor-wave-agent/src/agents/enhanced_mathematical_agents.py`:

```python
# Example: Use local LLM instead of OpenAI
from llama_index.llms.ollama import Ollama
llm = Ollama(model="llama2", request_timeout=60.0)
```

### Memory Configuration
The agents can be configured with persistent memory:

```python
# In enhanced_mathematical_agents.py
from llama_index.core.memory import ChatMemoryBuffer
memory = ChatMemoryBuffer.from_defaults(token_limit=3000)
```

---

**🎉 With proper LlamaIndex setup, you'll have a complete AI-powered mathematical discovery platform!**