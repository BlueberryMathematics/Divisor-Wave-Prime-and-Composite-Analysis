# AI Agent Package
from .agents.mathematical_research_agent import MathematicalResearchAgent, MathematicalKnowledgeBase
from .workflows.ai_mathematical_discovery import AIDiscoveryWorkflow

__all__ = [
    'MathematicalResearchAgent',
    'MathematicalKnowledgeBase', 
    'AIDiscoveryWorkflow'
]

__version__ = "1.0.0"
__author__ = "Based on Leo J. Borcherding's research"
__description__ = "AI agents for mathematical discovery in divisor wave analysis"