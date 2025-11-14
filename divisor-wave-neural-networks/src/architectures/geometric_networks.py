"""
Geometric Neural Networks
========================

Neural networks based on geometric sequences and patterns.
"""

import torch
import torch.nn as nn
from typing import Optional
from dataclasses import dataclass

@dataclass
class GeometricConfig:
    """Configuration for geometric networks."""
    input_dim: int = 64
    output_dim: int = 32
    geometric_ratio: float = 2.0
    num_layers: int = 5


class GeometricLayer(nn.Module):
    """Layer with geometric progression sizing."""
    
    def __init__(self, input_size: int, output_size: int, ratio: float = 2.0):
        super().__init__()
        self.linear = nn.Linear(input_size, output_size)
        self.ratio = ratio
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return torch.relu(self.linear(x))


class GeometricNetwork(nn.Module):
    """Network with geometric progression architecture."""
    
    def __init__(self, config: GeometricConfig):
        super().__init__()
        self.config = config
        
        # Create layers with geometric sizing
        layers = []
        current_size = config.input_dim
        
        for i in range(config.num_layers):
            next_size = max(1, int(current_size / config.geometric_ratio))
            layers.append(GeometricLayer(current_size, next_size, config.geometric_ratio))
            current_size = next_size
        
        # Output layer
        layers.append(nn.Linear(current_size, config.output_dim))
        
        self.layers = nn.ModuleList(layers)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        for layer in self.layers[:-1]:
            x = layer(x)
        return self.layers[-1](x)  # No activation on output