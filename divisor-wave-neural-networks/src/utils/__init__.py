"""
Utilities Package
================

Utility modules for the divisor wave neural networks library.
"""

from .mathematical_sequences import (
    MathematicalSequences,
    SequenceType,
    SequenceProperties,
    analyze_sequence_growth,
    find_sequence_patterns,
)

from .data_loaders import (
    MathematicalDataLoader,
    SequenceDataset,
    FormulaDataset,
    PrimeDataset,
)

from .visualization import (
    SequenceVisualizer,
    NetworkArchitectureVisualizer,
    TrainingVisualizer,
)

from .loss_functions import (
    SequenceLoss,
    RiemannLoss,
    PrimeLoss,
    DivisorWaveLoss,
    CrystalLoss,
    ContrastiveLoss,
    get_loss_function
)

from .optimization import (
    MathematicalAdam,
    PrimeScheduler,
    FibonacciScheduler,
    TetrahedralScheduler,
    RiemannScheduler,
    AdaptiveMathOptimizer,
    get_optimizer,
    get_scheduler
)

__all__ = [
    # Mathematical sequences
    "MathematicalSequences",
    "SequenceType", 
    "SequenceProperties",
    "analyze_sequence_growth",
    "find_sequence_patterns",
    
    # Data loaders
    "MathematicalDataLoader",
    "SequenceDataset",
    "FormulaDataset", 
    "PrimeDataset",
    
    # Visualization
    "SequenceVisualizer",
    "NetworkArchitectureVisualizer",
    "TrainingVisualizer",
    
    # Loss functions
    "SequenceLoss",
    "RiemannLoss",
    "PrimeLoss",
    "DivisorWaveLoss",
    "CrystalLoss",
    "ContrastiveLoss",
    "get_loss_function",
    
    # Optimization
    "MathematicalAdam",
    "PrimeScheduler",
    "FibonacciScheduler",
    "TetrahedralScheduler",
    "RiemannScheduler",
    "AdaptiveMathOptimizer",
    "get_optimizer",
    "get_scheduler",
]