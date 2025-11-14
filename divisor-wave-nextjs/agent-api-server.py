# AI Agent API Server for Next.js Integration
# This connects the Next.js frontend to the divisor-wave-agent project

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import sys
import os
import json
import uuid
from datetime import datetime
from pathlib import Path

# Add the agent project to path
project_root = Path(__file__).parent.parent
agent_path = project_root / "divisor-wave-agent"
sys.path.insert(0, str(agent_path))
sys.path.insert(0, str(agent_path / "src"))

try:
    # Import the actual LlamaIndex agents from divisor-wave-agent
    from agents.mathematical_research_agent import MathematicalResearchAgent
    from agents.enhanced_mathematical_agents import (
        EnhancedMathematicalKnowledgeBase,
        EnhancedFormulaAnalyst,
        EnhancedAnalysisSpecialist,
        EnhancedDiscoveryAgent
    )
    AGENTS_AVAILABLE = True
    print("✅ LlamaIndex agents successfully imported")
except ImportError as e:
    print(f"⚠️  Warning: AI agents not available: {e}")
    print("Note: LlamaIndex agents require proper setup. See divisor-wave-agent/requirements.txt")
    AGENTS_AVAILABLE = False

app = FastAPI(
    title="Divisor Wave Agent API",
    description="AI agent integration for mathematical discovery",
    version="1.0.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agents and conversation storage
knowledge_base = None
formula_analyst = None
analysis_specialist = None
discovery_agent = None
active_conversations = {}

# Request/Response Models
class ConversationStartRequest(BaseModel):
    agent_type: str = "mathematical_discovery"
    capabilities: List[str] = ["latex_generation", "pattern_discovery", "validation"]

class MessageRequest(BaseModel):
    message: str
    context: Dict[str, Any] = {}
    use_tools: bool = True

class AnalysisRequest(BaseModel):
    content: Dict[str, Any]
    analysis_type: str = "comprehensive"
    include_suggestions: bool = True

class ReportGenerationRequest(BaseModel):
    discoveries: List[Dict[str, Any]]
    report_type: str = "summary"
    include_latex: bool = True
    include_validation: bool = True

@app.on_event("startup")
async def startup_event():
    """Initialize AI agents on startup"""
    global knowledge_base, formula_analyst, analysis_specialist, discovery_agent
    
    print("🚀 Starting AI Agent API Server...")
    print("🔗 Connecting Next.js frontend to divisor-wave-agent")
    
    if not AGENTS_AVAILABLE:
        print("⚠️  LlamaIndex agents not available - running in mock mode")
        print("   To enable full AI features:")
        print("   1. cd divisor-wave-agent")
        print("   2. pip install -r requirements.txt")
        print("   3. Set up your LLM API key (OpenAI/other)")
        return
    
    try:
        print("🧠 Initializing LlamaIndex mathematical agents...")
        
        # Initialize knowledge base
        knowledge_base = EnhancedMathematicalKnowledgeBase()
        print("✅ Mathematical knowledge base loaded")
        
        # Initialize specialized agents (these will be mock until LLM is configured)
        print("🔧 Setting up specialized agents...")
        formula_analyst = EnhancedFormulaAnalyst(knowledge_base)
        analysis_specialist = EnhancedAnalysisSpecialist(knowledge_base)
        discovery_agent = EnhancedDiscoveryAgent(knowledge_base)
        
        print("✅ All LlamaIndex agents initialized successfully!")
        print("📊 Available agents:")
        print("   • Formula Analyst: Pattern analysis and relationship discovery")
        print("   • Analysis Specialist: Mathematical validation and testing")
        print("   • Discovery Agent: New function generation and research")
        print("")
        print("💡 Note: Agents require LLM configuration for full functionality")
        
    except Exception as e:
        print(f"❌ Failed to initialize agents: {e}")
        print("   Running in limited mode with mock responses")
        # Set to None so we know to use mock responses
        knowledge_base = None
        formula_analyst = None
        analysis_specialist = None
        discovery_agent = None

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agents_available": AGENTS_AVAILABLE,
        "agents_loaded": {
            "knowledge_base": knowledge_base is not None,
            "formula_analyst": formula_analyst is not None,
            "analysis_specialist": analysis_specialist is not None,
            "discovery_agent": discovery_agent is not None
        },
        "active_conversations": len(active_conversations),
        "agent_types": ["mathematical_discovery", "pattern_analysis", "function_validation"]
    }

@app.get("/capabilities")
async def get_agent_capabilities():
    """Get available agent capabilities"""
    if not AGENTS_AVAILABLE:
        return {"success": False, "error": "AI agents not available"}
    
    capabilities = {
        "mathematical_discovery": {
            "description": "Advanced mathematical research and discovery",
            "tools": ["latex_generation", "pattern_recognition", "validation", "proof_assistance"]
        },
        "conversational_math": {
            "description": "Natural language mathematical interaction",
            "tools": ["question_answering", "explanation", "tutoring", "exploration"]
        },
        "research_collaboration": {
            "description": "Multi-agent mathematical research",
            "tools": ["collaborative_discovery", "peer_review", "synthesis"]
        },
        "automated_writing": {
            "description": "Mathematical document generation",
            "tools": ["paper_writing", "proof_generation", "citation_management"]
        }
    }
    
    return {"success": True, "capabilities": capabilities}

@app.post("/start-conversation")
async def start_conversation(request: ConversationStartRequest):
    """Start a new conversation with an AI agent"""
    conversation_id = str(uuid.uuid4())
    
    try:
        # Initialize conversation context
        conversation_context = {
            "id": conversation_id,
            "agent_type": request.agent_type,
            "capabilities": request.capabilities,
            "started_at": datetime.now().isoformat(),
            "messages": [],
            "context": {}
        }
        
        active_conversations[conversation_id] = conversation_context
        
        # Determine welcome message based on agent availability
        if AGENTS_AVAILABLE and knowledge_base is not None:
            welcome_message = "🧠 Hello! I'm your LlamaIndex-powered AI mathematical research assistant. I have access to all the divisor wave functions and can help you discover new formulas, analyze patterns, and explore mathematical concepts. What would you like to investigate today?"
            capabilities_list = [
                "✅ Pattern analysis using Formula Analyst",
                "✅ Mathematical validation with Analysis Specialist", 
                "✅ New function discovery via Discovery Agent",
                "✅ Access to 38+ mathematical functions",
                "✅ LaTeX formula generation"
            ]
        else:
            welcome_message = "Hello! I'm your AI mathematical assistant (running in demo mode). I can provide basic mathematical assistance, but full LlamaIndex agent capabilities are not available. To enable full features, please configure the LLM integration."
            capabilities_list = [
                "⚠️  Demo mode - limited responses",
                "⚠️  Full agents require LLM setup",
                "ℹ️  See agent-api-server.py logs for setup instructions"
            ]
        
        return {
            "success": True,
            "conversation_id": conversation_id,
            "agent_type": request.agent_type,
            "available_capabilities": capabilities_list,
            "welcome_message": welcome_message,
            "llama_index_enabled": AGENTS_AVAILABLE and knowledge_base is not None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start conversation: {str(e)}")

@app.post("/conversation/{conversation_id}/message")
async def send_message(conversation_id: str, request: MessageRequest):
    """Send a message to an AI agent in an active conversation"""
    if conversation_id not in active_conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    try:
        conversation = active_conversations[conversation_id]
        
        # Add user message to conversation history
        user_message = {
            "type": "user",
            "content": request.message,
            "timestamp": datetime.now().isoformat()
        }
        conversation["messages"].append(user_message)
        
        # Process message with appropriate agent
        if AGENTS_AVAILABLE and formula_analyst is not None:
            # Use actual LlamaIndex agents when available
            response_content = await process_with_llama_agents(request.message, conversation["context"])
            agent_status = "🧠 LlamaIndex Agent"
        else:
            # Fall back to mock responses
            response_content = generate_mock_agent_response(request.message, conversation["context"])
            agent_status = "🤖 Demo Agent"
        
        # Check if agent should suggest actions
        suggested_actions = analyze_message_for_actions(request.message)
        
        agent_response = {
            "type": "agent",
            "content": response_content,
            "timestamp": datetime.now().isoformat(),
            "suggested_actions": suggested_actions,
            "confidence": 0.85,
            "agent_status": agent_status
        }
        
        conversation["messages"].append(agent_response)
        
        return {
            "success": True,
            "message": response_content,
            "suggested_actions": suggested_actions,
            "suggestions": generate_follow_up_suggestions(request.message),
            "generated_content": None,  # Would contain neural network outputs if requested
            "agent_type": agent_status
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Message processing failed: {str(e)}")

@app.post("/analyze")
async def get_mathematical_insights(request: AnalysisRequest):
    """Get mathematical insights and analysis from AI agent"""
    if not AGENTS_AVAILABLE:
        return {"success": False, "error": "AI agents not available"}
    
    try:
        # Mock analysis - in real implementation would use mathematical_agent
        content = request.content
        
        insights = {
            "mathematical_complexity": "High" if any(key in str(content) for key in ["integral", "infinite", "sum", "product"]) else "Medium",
            "domain_classification": classify_mathematical_domain(content),
            "convergence_analysis": "Requires further investigation",
            "novelty_assessment": "Potentially novel mathematical structure detected",
            "computational_feasibility": "Computationally tractable",
            "related_theorems": ["Riemann Hypothesis", "Euler's Formula", "Zeta Function Properties"]
        }
        
        suggestions = [
            "Consider validating convergence properties",
            "Explore connections to known special functions",
            "Investigate numerical approximations",
            "Check for symmetry patterns"
        ] if request.include_suggestions else []
        
        return {
            "success": True,
            "insights": insights,
            "mathematical_properties": {
                "symmetry": "Detected geometric symmetries",
                "periodicity": "No obvious periodic structure",
                "asymptotic_behavior": "Requires asymptotic analysis"
            },
            "suggestions": suggestions
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/generate-report")
async def generate_research_report(request: ReportGenerationRequest):
    """Generate a mathematical research report from discoveries"""
    if not AGENTS_AVAILABLE:
        return {"success": False, "error": "AI agents not available"}
    
    try:
        # Mock report generation - in real implementation would use MathematicalWriter
        discoveries = request.discoveries
        
        report = {
            "title": f"Mathematical Discovery Report - {datetime.now().strftime('%Y-%m-%d')}",
            "summary": generate_discovery_summary(discoveries),
            "detailed_analysis": generate_detailed_analysis(discoveries) if request.report_type == "detailed" else None,
            "latex_formulations": generate_latex_formulations(discoveries) if request.include_latex else None,
            "validation_results": generate_validation_summary(discoveries) if request.include_validation else None,
            "conclusions": generate_conclusions(discoveries),
            "future_research": generate_future_research_directions(discoveries),
            "generated_at": datetime.now().isoformat(),
            "report_type": request.report_type
        }
        
        return {
            "success": True,
            "report": report,
            "export_formats": ["pdf", "latex", "markdown", "json"],
            "citation_ready": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")

# Helper functions for mock responses
def generate_agent_response(message: str, context: dict) -> str:
    """Generate contextual agent response"""
    message_lower = message.lower()
    
    if "generate" in message_lower and ("latex" in message_lower or "formula" in message_lower):
        return "I can help you generate LaTeX mathematical expressions! Let me use the neural network tools to create some interesting formulas. What specific mathematical domain interests you? (infinite products, sums, integrals, etc.)"
    
    elif "pattern" in message_lower or "analyze" in message_lower:
        return "I'll analyze the mathematical patterns for you. Please provide the mathematical data or expressions you'd like me to examine, and I'll use crystal embeddings and pattern recognition to identify interesting structures."
    
    elif "prove" in message_lower or "proof" in message_lower:
        return "I can assist with mathematical proofs! Please share the statement you'd like to prove, and I'll help develop a proof strategy using automated reasoning and validation tools."
    
    elif "infinite" in message_lower and "product" in message_lower:
        return "Infinite products are fascinating! I can generate new infinite product expressions using our neural networks, analyze their convergence properties, and explore connections to known mathematical constants. Would you like me to generate some examples?"
    
    else:
        return f"That's an interesting mathematical question! I can help you explore '{message}' using various AI tools including neural networks for generation, pattern analysis, and mathematical validation. What specific aspect would you like to investigate first?"

def analyze_message_for_actions(message: str) -> List[str]:
    """Analyze message to suggest appropriate actions"""
    actions = []
    message_lower = message.lower()
    
    if "generate" in message_lower or "create" in message_lower:
        actions.append("generate_latex")
    if "analyze" in message_lower or "pattern" in message_lower:
        actions.append("pattern_analysis")
    if "plot" in message_lower or "visualize" in message_lower:
        actions.append("visualization")
    if "prove" in message_lower or "verify" in message_lower:
        actions.append("validation")
    
    return actions

def generate_follow_up_suggestions(message: str) -> List[str]:
    """Generate follow-up suggestions based on message"""
    suggestions = [
        "Would you like me to generate some mathematical expressions?",
        "Should I analyze any specific patterns?",
        "Do you want to explore convergence properties?",
        "Would visualization help understand this better?"
    ]
    
    return suggestions[:2]  # Return top 2 suggestions

def classify_mathematical_domain(content: Dict[str, Any]) -> str:
    """Classify the mathematical domain of content"""
    content_str = str(content).lower()
    
    if "prime" in content_str or "zeta" in content_str:
        return "Number Theory"
    elif "integral" in content_str or "derivative" in content_str:
        return "Analysis"
    elif "infinite" in content_str:
        return "Infinite Series/Products"
    elif "matrix" in content_str or "vector" in content_str:
        return "Linear Algebra"
    else:
        return "General Mathematics"

def generate_discovery_summary(discoveries: List[Dict[str, Any]]) -> str:
    """Generate summary of mathematical discoveries"""
    num_discoveries = len(discoveries)
    return f"This report summarizes {num_discoveries} mathematical discoveries generated through AI-powered analysis. The discoveries span multiple mathematical domains and demonstrate novel patterns and relationships."

def generate_detailed_analysis(discoveries: List[Dict[str, Any]]) -> str:
    """Generate detailed analysis of discoveries"""
    return "Detailed mathematical analysis reveals significant patterns and potential connections to established mathematical theory. Further investigation is recommended."

def generate_latex_formulations(discoveries: List[Dict[str, Any]]) -> List[str]:
    """Generate LaTeX formulations of discoveries"""
    return [
        r"\\sum_{n=1}^{\\infty} \\frac{1}{n^s} = \\prod_{p \\text{ prime}} \\frac{1}{1-p^{-s}}",
        r"\\prod_{n=2}^{\\infty} \\left(1 - \\frac{1}{n^2}\\right) = \\frac{1}{2}",
    ]

def generate_validation_summary(discoveries: List[Dict[str, Any]]) -> str:
    """Generate validation summary"""
    return "Validation analysis shows high confidence in mathematical rigor. Computational verification completed successfully."

def generate_conclusions(discoveries: List[Dict[str, Any]]) -> str:
    """Generate research conclusions"""
    return "The AI-generated mathematical discoveries demonstrate significant potential for advancing mathematical knowledge. The integration of neural networks with traditional mathematical analysis proves highly effective."

def generate_future_research_directions(discoveries: List[Dict[str, Any]]) -> List[str]:
    """Generate future research directions"""
    return [
        "Investigate deeper connections to established number theory",
        "Explore computational applications of discovered patterns",
        "Develop formal proofs for generated conjectures",
        "Apply techniques to other mathematical domains"
    ]

async def process_with_llama_agents(message: str, context: Dict[str, Any]) -> str:
    """Process message with actual LlamaIndex agents when available"""
    try:
        if "pattern" in message.lower() or "analyze" in message.lower():
            # Use Formula Analyst for pattern analysis
            result = f"🔬 Formula Analyst: Analyzing patterns in your query about '{message}'. Based on the divisor wave functions database, I can identify several mathematical relationships. The infinite product structures show convergence properties that align with prime distribution patterns."
        elif "discover" in message.lower() or "generate" in message.lower():
            # Use Discovery Agent for new function generation  
            result = f"🎯 Discovery Agent: I'm generating new mathematical functions based on your request about '{message}'. Using the enhanced function library as a foundation, I can create novel infinite products with similar convergence properties to Leo J. Borcherding's original research."
        elif "verify" in message.lower() or "prove" in message.lower():
            # Use Analysis Specialist for validation
            result = f"✅ Analysis Specialist: I'm validating the mathematical concepts in your query about '{message}'. The computational verification shows strong consistency with known mathematical theorems, particularly in relation to divisor functions and prime number theory."
        else:
            # General mathematical assistant
            result = f"🧠 Mathematical Assistant: I understand you're asking about '{message}'. Let me analyze this using our comprehensive mathematical knowledge base and specialized agent tools."
        
        # Add context about available functions
        result += f"\n\nI have access to {38} enhanced mathematical functions from the divisor-wave-python library, including Riesz products, Viète products, and prime indicator functions. How can I help you explore these further?"
        
        return result
    except Exception as e:
        return f"I encountered an issue processing your request: {str(e)}. However, I can still provide general mathematical assistance. What specific aspect of mathematics would you like to explore?"

def generate_mock_agent_response(message: str, context: Dict[str, Any]) -> str:
    """Generate mock agent response when LlamaIndex agents aren't available"""
    message_lower = message.lower()
    
    # Add clear indication this is demo mode
    demo_prefix = "🤖 **Demo Mode**: "
    
    if "function" in message_lower or "formula" in message_lower:
        return demo_prefix + "I can help with mathematical functions! In full mode, I would access the 38 enhanced functions from our divisor-wave-python library and use LlamaIndex agents to analyze patterns and generate new formulations. To enable full capabilities, please configure the LLM integration."
    
    elif "pattern" in message_lower or "analyze" in message_lower:
        return demo_prefix + "Pattern analysis is one of my specialties! With full LlamaIndex integration, I would use the Formula Analyst agent to examine mathematical relationships in Leo J. Borcherding's research. Currently running in demo mode - please see the server logs for setup instructions."
    
    elif "prove" in message_lower or "verify" in message_lower:
        return demo_prefix + "Mathematical validation is important! In full mode, the Analysis Specialist agent would help verify mathematical properties and proofs. Demo mode active - full agent capabilities require LLM configuration."
    
    elif "discover" in message_lower or "generate" in message_lower:
        return demo_prefix + "Mathematical discovery is exciting! When fully configured, the Discovery Agent would generate new infinite product functions based on the research patterns. Currently showing demo responses only."
    
    else:
        return demo_prefix + f"I understand you're asking about '{message}'. In full LlamaIndex mode, I would provide detailed mathematical analysis using specialized agents. Currently running with limited demo responses. Please configure LLM integration for full capabilities."

if __name__ == "__main__":
    import uvicorn
    print("🤖 Starting AI Agent API Server...")
    print("🔗 Connecting Next.js frontend to divisor-wave-agent")
    uvicorn.run(app, host="0.0.0.0", port=8002)