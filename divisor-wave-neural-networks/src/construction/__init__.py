"""
Model Construction Package
==========================

Construction module for the divisor wave neural networks library.
"""

from .architecture_builder import (
    ArchitectureBuilder,
    ArchitectureSpec,
    LayerSpec,
    MathematicalLayer,
    MathematicalActivation,
    LayerType,
    ActivationType,
    ConnectionPattern,
    create_tetrahedral_discovery_network,
    create_prime_pattern_network,
    create_fibonacci_sequence_network,
)

from .mathematical_layers import (
    PrimeLayer,
    FibonacciLayer,
    GeometricLayer,
    FractalLayer,
    SequenceLayer,
)

from .training_pipelines import (
    TrainingPipeline,
    MathematicalTrainer,
    DiscoveryTrainer,
    SequenceTrainer,
)

__all__ = [
    # Architecture builder
    "ArchitectureBuilder",
    "ArchitectureSpec", 
    "LayerSpec",
    "MathematicalLayer",
    "MathematicalActivation",
    "LayerType",
    "ActivationType",
    "ConnectionPattern",
    
    # Mathematical layers
    "PrimeLayer",
    "FibonacciLayer",
    "GeometricLayer",
    "FractalLayer",
    "SequenceLayer",
    
    # Training pipelines
    "TrainingPipeline",
    "MathematicalTrainer",
    "DiscoveryTrainer", 
    "SequenceTrainer",
    
    # Factory functions
    "create_tetrahedral_discovery_network",
    "create_prime_pattern_network",
    "create_fibonacci_sequence_network",
]