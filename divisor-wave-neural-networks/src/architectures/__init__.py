"""
Neural Network Architectures Package
====================================

Architecture module for the divisor wave neural networks library.
"""

from .tetrahedral_networks import (
    TetrahedralNetwork,
    TetrahedralConfig,
    TetrahedralLayer,
    TetrahedralAttention,
    TetrahedralConnectionType,
    create_small_tetrahedral_network,
    create_large_tetrahedral_network,
    create_sequence_prediction_tetrahedral_network,
)

from .geometric_networks import (
    GeometricNetwork,
    GeometricConfig,
    GeometricLayer,
)

from .oeis_architectures import (
    OEISArchitecture,
    OEISConfig,
    A287324Network,
)

from .mathematical_gans import (
    MathematicalGAN,
    MathematicalGANConfig,
    MathematicalGANType,
    create_sequence_gan,
    create_riemann_gan,
    create_prime_gan,
)

__all__ = [
    # Tetrahedral networks
    "TetrahedralNetwork",
    "TetrahedralConfig",
    "TetrahedralLayer", 
    "TetrahedralAttention",
    "TetrahedralConnectionType",
    
    # Geometric networks
    "GeometricNetwork",
    "GeometricConfig",
    "GeometricLayer",
    
    # OEIS architectures
    "OEISArchitecture",
    "OEISConfig",
    "A287324Network",
    
    # Mathematical GANs
    "MathematicalGAN",
    "MathematicalGANConfig",
    "MathematicalGANType",
    "create_sequence_gan",
    "create_riemann_gan",
    "create_prime_gan",
    
    # Factory functions
    "create_small_tetrahedral_network",
    "create_large_tetrahedral_network", 
    "create_sequence_prediction_tetrahedral_network",
]