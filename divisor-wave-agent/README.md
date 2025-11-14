# Divisor Wave AI Agent System

## Overview
AI-powered mathematical discovery system for Leo J. Borcherding's divisor wave research. This system uses LlamaIndex AI agents to analyze mathematical patterns and generate new functions.

## Components

### Core Agents
- **FormulaAnalyst**: Analyzes mathematical formulas and patterns
- **AnalysisSpecialist**: Conducts deep mathematical analysis  
- **DiscoveryAgent**: Generates new mathematical functions

### Mathematical Integration
- Connects to `divisor-wave-python` for mathematical functions
- Uses 38+ functions from the enhanced function library
- Supports all normalization modes (X/Y/Z/XYZ/N)

### Capabilities
1. **Pattern Recognition**: Identify patterns in function families
2. **Function Generation**: Create new infinite product formulations
3. **Hypothesis Testing**: Validate mathematical theories
4. **Prime Analysis**: Explore prime/composite number patterns
5. **Research Direction**: Suggest new mathematical territories

## Usage

### Prerequisites
```bash
cd divisor-wave-agent
pip install -r requirements.txt
```

### Basic Usage
```python
from src.agents.mathematical_research_agent import MathematicalResearchAgent
from llama_index.llms.openai import OpenAI

# Initialize with your LLM
llm = OpenAI(model="gpt-4")
research_agent = MathematicalResearchAgent(llm)

# Conduct research
result = await research_agent.research_session(
    "Generate new functions based on Riesz product patterns"
)
```

### Discovery Workflow
```python
from src.workflows.ai_mathematical_discovery import AIDiscoveryWorkflow

workflow = AIDiscoveryWorkflow()
await workflow.run_discovery_session()
```

## Integration with Math System

The AI agents automatically connect to the mathematical functions in `divisor-wave-python`:
- `src/core/special_functions_library.py` (38 functions)
- `src/core/function_registry.py` (unified registry)
- `src/core/latex_function_builder.py` (LaTeX generation)
- `src/core/plotting_methods.py` (visualization)

## Research Context

Based on **"Divisor Wave Product Analysis of Prime and Composite Numbers"** by Leo J. Borcherding:
- Infinite products reveal prime/composite patterns
- Divisor waves: a_k(x) = |α(x/k)sin(πx/k)|
- Connection to Riemann Hypothesis through zeta functions
- Multiple function families explore different transformations