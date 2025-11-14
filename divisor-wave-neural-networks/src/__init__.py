"""
Divisor Wave Neural Networks
============================

A comprehensive PyTorch-based neural networks library for mathematical discovery,
sequence prediction, and custom architectures inspired by Leo J. Borcherding's
research on divisor waves, infinite products, and tetrahedral sequences.

This library provides:
- Mathematical discovery networks using deep learning and reinforcement learning
- Function prediction models for complex mathematical sequences
- Sequence-architected networks based on mathematical progressions
- Custom embedding models using geometric and tetrahedral structures
- THRML integration for energy-based models and Ising chain networks
- Comprehensive model construction system for custom architectures

Usage:
    from divisor_wave_neural_networks import (
        TetrahedralNetwork,
        CrystalEmbedding,
        FormulaDiscoveryAgent,
        IsingNeuralNetwork,
    )
"""

__version__ = "0.1.0"
__author__ = "Leo J. Borcherding"
__email__ = "leo@example.com"

# Core imports for easy access
from .discovery import (
    DeepDiscoveryNetwork,
    ReinforcementDiscoveryAgent,
    PoleZeroDetector,
)

from .prediction import (
    SequencePredictionModel,
    FunctionApproximator,
)

from .architectures import (
    TetrahedralNetwork,
    GeometricNetwork,
    OEISArchitecture,
)

from .embeddings import (
    CrystalEmbedding,
    TetrahedralEmbedding,
    SequenceEmbedding,
)

from .thrml_integration import (
    IsingNeuralNetwork,
    EnergyBasedDiscovery,
    PGMDiscoveryModel,
)

from .construction import (
    ArchitectureBuilder,
    MathematicalLayer,
    TrainingPipeline,
)

from .utils import (
    MathematicalSequences,
    DataLoaders,
    Visualization,
)

from .integration import (
    DivisorWaveBridge,
    AgentIntegration,
    WebInterface,
)

# Version information
VERSION_INFO = {
    "major": 0,
    "minor": 1,
    "patch": 0,
    "release": "alpha",
}

# Package metadata
PACKAGE_INFO = {
    "name": "divisor-wave-neural-networks",
    "description": "Mathematical Discovery Neural Networks Library",
    "author": "Leo J. Borcherding",
    "license": "Apache 2.0",
    "keywords": [
        "neural networks",
        "mathematical discovery", 
        "infinite products",
        "tetrahedral sequences",
        "prime numbers",
        "divisor waves",
        "deep learning",
        "reinforcement learning",
        "THRML",
        "energy-based models",
    ],
}

# Export all main classes and functions
__all__ = [
    # Discovery models
    "DeepDiscoveryNetwork",
    "ReinforcementDiscoveryAgent", 
    "PoleZeroDetector",
    
    # Prediction models
    "SequencePredictionModel",
    "FunctionApproximator",
    
    # Architectures
    "TetrahedralNetwork",
    "GeometricNetwork", 
    "OEISArchitecture",
    
    # Embeddings
    "CrystalEmbedding",
    "TetrahedralEmbedding",
    "SequenceEmbedding",
    
    # THRML integration
    "IsingNeuralNetwork",
    "EnergyBasedDiscovery",
    "PGMDiscoveryModel",
    
    # Construction tools
    "ArchitectureBuilder",
    "MathematicalLayer",
    "TrainingPipeline",
    
    # Utilities
    "MathematicalSequences",
    "DataLoaders",
    "Visualization",
    
    # Integration
    "DivisorWaveBridge",
    "AgentIntegration", 
    "WebInterface",
    
    # Package info
    "__version__",
    "VERSION_INFO",
    "PACKAGE_INFO",
]

def get_version_string():
    """Get formatted version string."""
    return f"{VERSION_INFO['major']}.{VERSION_INFO['minor']}.{VERSION_INFO['patch']}-{VERSION_INFO['release']}"

def print_package_info():
    """Print package information."""
    print(f"{PACKAGE_INFO['name']} v{__version__}")
    print(f"Description: {PACKAGE_INFO['description']}")
    print(f"Author: {PACKAGE_INFO['author']}")
    print(f"License: {PACKAGE_INFO['license']}")
    print(f"Keywords: {', '.join(PACKAGE_INFO['keywords'])}")