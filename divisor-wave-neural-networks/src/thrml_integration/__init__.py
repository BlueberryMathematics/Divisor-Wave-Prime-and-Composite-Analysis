"""
THRML Integration Package
=========================

THRML integration module for the divisor wave neural networks library.
"""

from .ising_networks import (
    IsingNeuralNetwork,
    IsingNeuralNetworkConfig,
    IsingLayer,
    IsingModelType,
    SamplingMethod,
    EnergyBasedDiscovery,
    PGMDiscoveryModel,
    create_mathematical_ising_network,
    create_formula_discovery_model,
    create_mathematical_pgm,
)

from .energy_models import (
    EnergyBasedModel,
    EnergyFunction,
    SamplingStrategy,
)

from .pgm_discovery import (
    ProbabilisticGraphicalModel,
    DiscoveryPGM,
    MathematicalRelationshipModel,
)

__all__ = [
    # Ising networks
    "IsingNeuralNetwork",
    "IsingNeuralNetworkConfig",
    "IsingLayer",
    "IsingModelType",
    "SamplingMethod",
    "EnergyBasedDiscovery",  
    "PGMDiscoveryModel",
    
    # Energy models
    "EnergyBasedModel",
    "EnergyFunction",
    "SamplingStrategy",
    
    # PGM discovery
    "ProbabilisticGraphicalModel",
    "DiscoveryPGM",
    "MathematicalRelationshipModel",
    
    # Factory functions
    "create_mathematical_ising_network",
    "create_formula_discovery_model",
    "create_mathematical_pgm",
]