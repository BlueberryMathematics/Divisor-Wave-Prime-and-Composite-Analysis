"""
Integration Package
===================

Integration module for connecting with other divisor wave projects.
"""

from .divisor_wave_bridge import (
    DivisorWaveBridge,
    create_divisor_wave_bridge,
    load_divisor_wave_training_data,
    create_divisor_wave_dataset,
)

from .agent_integration import (
    AgentIntegration,
    NeuralNetworkAgent,
    DiscoveryAgent,
)

from .web_interface import (
    WebInterface,
    NetworkVisualizer,
    TrainingDashboard,
)

__all__ = [
    # Divisor wave bridge
    "DivisorWaveBridge",
    "create_divisor_wave_bridge",
    "load_divisor_wave_training_data", 
    "create_divisor_wave_dataset",
    
    # Agent integration
    "AgentIntegration",
    "NeuralNetworkAgent",
    "DiscoveryAgent",
    
    # Web interface
    "WebInterface",
    "NetworkVisualizer",
    "TrainingDashboard",
]