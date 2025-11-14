"""
Mathematical Discovery Networks Package
======================================

Discovery module for the divisor wave neural networks library.
"""

from .deep_discovery import (
    DeepDiscoveryNetwork,
    DeepDiscoveryConfig,
    InfiniteProductGenerator,
    PoleZeroDetector,
    MathematicalFormulaEncoder,
    DiscoveryTaskType,
    FormulaRepresentation,
    create_infinite_product_discoverer,
    create_pole_zero_detector,
    create_general_discovery_network,
)

from .reinforcement_discovery import (
    ReinforcementDiscoveryAgent,
    DiscoveryEnvironment,
    FormulaDiscoveryReward,
)

__all__ = [
    # Deep discovery
    "DeepDiscoveryNetwork",
    "DeepDiscoveryConfig", 
    "InfiniteProductGenerator",
    "PoleZeroDetector",
    "MathematicalFormulaEncoder",
    "DiscoveryTaskType",
    "FormulaRepresentation",
    
    # Reinforcement discovery
    "ReinforcementDiscoveryAgent",
    "DiscoveryEnvironment",
    "FormulaDiscoveryReward",
    
    # Factory functions
    "create_infinite_product_discoverer",
    "create_pole_zero_detector", 
    "create_general_discovery_network",
]