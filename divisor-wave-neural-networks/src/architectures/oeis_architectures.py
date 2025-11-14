"""
OEIS-Based Architectures
=======================

Neural network architectures based on OEIS sequences, particularly
the A287324 sequence from Leo J. Borcherding's research.
"""

import torch
import torch.nn as nn
from typing import List
from dataclasses import dataclass

@dataclass
class OEISConfig:
    """Configuration for OEIS-based networks."""
    input_dim: int = 64
    output_dim: int = 32
    sequence_id: str = "A287324"
    max_layers: int = 8


class A287324Network(nn.Module):
    """Network based on OEIS A287324 sequence."""
    
    def __init__(self, config: OEISConfig):
        super().__init__()
        
        # A287324 sequence: 0, 1, 9, 40, 120, 280, 552, 968, 1560, 2360, ...
        a287324_values = [0, 1, 9, 40, 120, 280, 552, 968, 1560, 2360, 
                         3400, 4712, 6328, 8280, 10600, 13320]
        
        # Use sequence values to determine layer sizes
        layer_sizes = [config.input_dim]
        for i in range(min(config.max_layers, len(a287324_values) - 1)):
            size = max(1, a287324_values[i + 1] // 10)  # Scale down
            layer_sizes.append(size)
        layer_sizes.append(config.output_dim)
        
        # Create layers
        layers = []
        for i in range(len(layer_sizes) - 1):
            layers.append(nn.Linear(layer_sizes[i], layer_sizes[i + 1]))
            if i < len(layer_sizes) - 2:  # No activation on last layer
                layers.append(nn.ReLU())
        
        self.network = nn.Sequential(*layers)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)


class OEISArchitecture(nn.Module):
    """General OEIS sequence-based architecture."""
    
    def __init__(self, config: OEISConfig):
        super().__init__()
        
        if config.sequence_id == "A287324":
            self.network = A287324Network(config)
        else:
            # Default to standard network
            self.network = nn.Sequential(
                nn.Linear(config.input_dim, 128),
                nn.ReLU(),
                nn.Linear(128, config.output_dim)
            )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)