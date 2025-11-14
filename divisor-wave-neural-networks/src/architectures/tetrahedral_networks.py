"""
Tetrahedral Neural Networks
===========================

Neural network architectures based on tetrahedral number sequences.
Inspired by Leo J. Borcherding's research on the unified tetrahedral family.

These networks use tetrahedral numbers to determine:
- Layer sizes
- Connection patterns
- Activation distributions
- Learning rate schedules
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import List, Dict, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum

from ..utils.mathematical_sequences import MathematicalSequences, SequenceType


class TetrahedralConnectionType(Enum):
    """Types of connections in tetrahedral networks."""
    STANDARD = "standard"  # Regular fully connected
    TETRAHEDRAL = "tetrahedral"  # Connections follow tetrahedral pattern
    PYRAMID = "pyramid"  # Pyramid-like connections
    SPARSE_TETRAHEDRAL = "sparse_tetrahedral"  # Sparse tetrahedral connections


@dataclass
class TetrahedralConfig:
    """Configuration for tetrahedral networks."""
    input_dim: int
    output_dim: int
    max_layers: int = 10
    connection_type: TetrahedralConnectionType = TetrahedralConnectionType.TETRAHEDRAL
    activation: str = "relu"
    dropout_rate: float = 0.1
    use_batch_norm: bool = True
    tetrahedral_scaling: float = 1.0
    min_layer_size: int = 8
    max_layer_size: int = 2048


class TetrahedralLayer(nn.Module):
    """
    A layer with tetrahedral-inspired connections and activations.
    """
    
    def __init__(self, 
                 input_size: int, 
                 output_size: int,
                 tetrahedral_index: int,
                 connection_type: TetrahedralConnectionType = TetrahedralConnectionType.TETRAHEDRAL,
                 activation: str = "relu",
                 dropout_rate: float = 0.1,
                 use_batch_norm: bool = True):
        super().__init__()
        
        self.input_size = input_size
        self.output_size = output_size
        self.tetrahedral_index = tetrahedral_index
        self.connection_type = connection_type
        
        # Create the main linear transformation
        if connection_type == TetrahedralConnectionType.TETRAHEDRAL:
            self.linear = self._create_tetrahedral_linear(input_size, output_size)
        elif connection_type == TetrahedralConnectionType.SPARSE_TETRAHEDRAL:
            self.linear = self._create_sparse_tetrahedral_linear(input_size, output_size)
        else:
            self.linear = nn.Linear(input_size, output_size)
        
        # Batch normalization
        self.batch_norm = nn.BatchNorm1d(output_size) if use_batch_norm else None
        
        # Activation function
        self.activation = self._get_activation(activation)
        
        # Dropout
        self.dropout = nn.Dropout(dropout_rate) if dropout_rate > 0 else None
        
        # Tetrahedral-specific components
        self.tetrahedral_bias = nn.Parameter(torch.zeros(output_size))
        self._initialize_tetrahedral_weights()
    
    def _create_tetrahedral_linear(self, input_size: int, output_size: int) -> nn.Module:
        """Create a linear layer with tetrahedral connection pattern."""
        # Create a custom linear layer with tetrahedral mask
        linear = nn.Linear(input_size, output_size)
        
        # Create tetrahedral connection mask
        mask = self._create_tetrahedral_mask(input_size, output_size)
        
        # Apply mask to weights
        with torch.no_grad():
            linear.weight.data *= mask
        
        # Register mask as buffer to maintain it during forward passes
        linear.register_buffer('tetrahedral_mask', mask)
        
        return linear
    
    def _create_sparse_tetrahedral_linear(self, input_size: int, output_size: int) -> nn.Module:
        """Create a sparse linear layer with tetrahedral pattern."""
        # Use a more sparse connection pattern based on tetrahedral numbers
        linear = nn.Linear(input_size, output_size)
        
        # Create sparse tetrahedral mask
        mask = self._create_sparse_tetrahedral_mask(input_size, output_size)
        
        with torch.no_grad():
            linear.weight.data *= mask
        
        linear.register_buffer('tetrahedral_mask', mask)
        return linear
    
    def _create_tetrahedral_mask(self, input_size: int, output_size: int) -> torch.Tensor:
        """Create a connection mask based on tetrahedral numbers."""
        mask = torch.ones(output_size, input_size)
        
        # Use tetrahedral number to determine connection pattern
        tet_num = self.tetrahedral_index * (self.tetrahedral_index + 1) * (self.tetrahedral_index + 2) // 6
        
        # Create pattern based on tetrahedral structure
        for i in range(output_size):
            for j in range(input_size):
                # Connection exists based on tetrahedral relationship
                connection_value = (i + j + tet_num) % (tet_num + 1)
                if connection_value > tet_num // 2:
                    mask[i, j] = 0.0
        
        return mask
    
    def _create_sparse_tetrahedral_mask(self, input_size: int, output_size: int) -> torch.Tensor:
        """Create a sparse connection mask with tetrahedral pattern."""
        mask = torch.zeros(output_size, input_size)
        
        # Calculate tetrahedral number for this layer
        tet_num = self.tetrahedral_index * (self.tetrahedral_index + 1) * (self.tetrahedral_index + 2) // 6
        
        # Create sparse connections based on tetrahedral geometry
        connections_per_output = max(1, min(input_size, tet_num % input_size + 1))
        
        for i in range(output_size):
            # Select connections based on tetrahedral pattern
            start_idx = (i * tet_num) % input_size
            for k in range(connections_per_output):
                j = (start_idx + k) % input_size
                mask[i, j] = 1.0
        
        return mask
    
    def _get_activation(self, activation: str) -> nn.Module:
        """Get activation function by name."""
        activations = {
            "relu": nn.ReLU(),
            "tanh": nn.Tanh(),
            "sigmoid": nn.Sigmoid(),
            "leaky_relu": nn.LeakyReLU(),
            "gelu": nn.GELU(),
            "swish": nn.SiLU(),
        }
        return activations.get(activation, nn.ReLU())
    
    def _initialize_tetrahedral_weights(self):
        """Initialize weights using tetrahedral-inspired patterns."""
        with torch.no_grad():
            # Initialize based on tetrahedral structure
            tet_num = self.tetrahedral_index * (self.tetrahedral_index + 1) * (self.tetrahedral_index + 2) // 6
            
            # Scale initialization based on tetrahedral number
            scale = np.sqrt(2.0 / (self.input_size + tet_num))
            
            # Apply scaled initialization
            nn.init.normal_(self.linear.weight, mean=0.0, std=scale)
            
            # Initialize tetrahedral bias
            nn.init.constant_(self.tetrahedral_bias, 1.0 / (tet_num + 1))
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through tetrahedral layer."""
        # Apply linear transformation
        out = self.linear(x)
        
        # Add tetrahedral bias
        out = out + self.tetrahedral_bias
        
        # Apply batch normalization
        if self.batch_norm is not None:
            out = self.batch_norm(out)
        
        # Apply activation
        out = self.activation(out)
        
        # Apply dropout
        if self.dropout is not None:
            out = self.dropout(out)
        
        return out


class TetrahedralNetwork(nn.Module):
    """
    A neural network with architecture based on tetrahedral number sequences.
    
    The network structure follows tetrahedral numbers for layer sizes,
    creating a unique architectural pattern inspired by 3D geometric shapes.
    """
    
    def __init__(self, config: TetrahedralConfig):
        super().__init__()
        
        self.config = config
        self.seq_generator = MathematicalSequences()
        
        # Generate tetrahedral sequence for layer sizes
        self.layer_sizes = self._generate_layer_architecture()
        
        # Create the network layers
        self.layers = self._create_layers()
        
        # Output layer
        self.output_layer = nn.Linear(self.layer_sizes[-1], config.output_dim)
        
        # Additional tetrahedral-specific components
        self.tetrahedral_attention = TetrahedralAttention(self.layer_sizes[-1])
        
        # Initialize the network
        self._initialize_network()
    
    def _generate_layer_architecture(self) -> List[int]:
        """Generate layer sizes based on tetrahedral numbers."""
        # Get tetrahedral numbers
        tet_numbers = self.seq_generator.tetrahedral_numbers(self.config.max_layers)
        
        # Scale to appropriate sizes
        scaled_sizes = (tet_numbers * self.config.tetrahedral_scaling).int()
        
        # Clamp to reasonable bounds
        layer_sizes = torch.clamp(
            scaled_sizes, 
            min=self.config.min_layer_size, 
            max=self.config.max_layer_size
        ).tolist()
        
        # Ensure input dimension compatibility
        layer_sizes = [self.config.input_dim] + layer_sizes
        
        return layer_sizes
    
    def _create_layers(self) -> nn.ModuleList:
        """Create the tetrahedral layers."""
        layers = nn.ModuleList()
        
        for i in range(len(self.layer_sizes) - 1):
            layer = TetrahedralLayer(
                input_size=self.layer_sizes[i],
                output_size=self.layer_sizes[i + 1],
                tetrahedral_index=i + 1,
                connection_type=self.config.connection_type,
                activation=self.config.activation,
                dropout_rate=self.config.dropout_rate,
                use_batch_norm=self.config.use_batch_norm
            )
            layers.append(layer)
        
        return layers
    
    def _initialize_network(self):
        """Initialize network weights using tetrahedral patterns."""
        for i, layer in enumerate(self.layers):
            # Each layer uses its tetrahedral index for initialization
            layer._initialize_tetrahedral_weights()
        
        # Initialize output layer
        nn.init.xavier_uniform_(self.output_layer.weight)
        nn.init.zeros_(self.output_layer.bias)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through the tetrahedral network."""
        # Pass through tetrahedral layers
        for layer in self.layers:
            x = layer(x)
        
        # Apply tetrahedral attention
        x = self.tetrahedral_attention(x)
        
        # Final output layer
        output = self.output_layer(x)
        
        return output
    
    def get_layer_info(self) -> Dict[str, List]:
        """Get information about the network layers."""
        return {
            "layer_sizes": self.layer_sizes,
            "tetrahedral_numbers": self.seq_generator.tetrahedral_numbers(len(self.layer_sizes)).tolist(),
            "total_parameters": sum(p.numel() for p in self.parameters()),
            "trainable_parameters": sum(p.numel() for p in self.parameters() if p.requires_grad),
        }
    
    def visualize_architecture(self) -> Dict[str, any]:
        """Get data for visualizing the network architecture."""
        return {
            "layer_sizes": self.layer_sizes,
            "connection_type": self.config.connection_type.value,
            "tetrahedral_indices": list(range(1, len(self.layer_sizes))),
            "total_layers": len(self.layers),
        }


class TetrahedralAttention(nn.Module):
    """
    Attention mechanism based on tetrahedral geometry.
    """
    
    def __init__(self, hidden_size: int, num_heads: int = 8):
        super().__init__()
        
        self.hidden_size = hidden_size
        self.num_heads = num_heads
        self.head_size = hidden_size // num_heads
        
        # Ensure head_size is divisible
        assert hidden_size % num_heads == 0
        
        # Query, Key, Value projections with tetrahedral pattern
        self.query = nn.Linear(hidden_size, hidden_size)
        self.key = nn.Linear(hidden_size, hidden_size)
        self.value = nn.Linear(hidden_size, hidden_size)
        
        # Output projection
        self.output = nn.Linear(hidden_size, hidden_size)
        
        # Tetrahedral position encoding
        self.tetrahedral_encoding = self._create_tetrahedral_encoding()
    
    def _create_tetrahedral_encoding(self) -> torch.Tensor:
        """Create position encoding based on tetrahedral structure."""
        # Create 3D tetrahedral coordinates for each position
        encoding = torch.zeros(self.hidden_size, 3)
        
        for i in range(self.hidden_size):
            # Map to tetrahedral coordinates
            tet_idx = i % 4  # 4 vertices of tetrahedron
            
            if tet_idx == 0:
                encoding[i] = torch.tensor([1.0, 1.0, 1.0])
            elif tet_idx == 1:
                encoding[i] = torch.tensor([1.0, -1.0, -1.0])
            elif tet_idx == 2:
                encoding[i] = torch.tensor([-1.0, 1.0, -1.0])
            else:
                encoding[i] = torch.tensor([-1.0, -1.0, 1.0])
        
        return nn.Parameter(encoding, requires_grad=False)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through tetrahedral attention."""
        batch_size, seq_len, hidden_size = x.shape
        
        # Apply projections
        Q = self.query(x)
        K = self.key(x)
        V = self.value(x)
        
        # Reshape for multi-head attention
        Q = Q.view(batch_size, seq_len, self.num_heads, self.head_size).transpose(1, 2)
        K = K.view(batch_size, seq_len, self.num_heads, self.head_size).transpose(1, 2)
        V = V.view(batch_size, seq_len, self.num_heads, self.head_size).transpose(1, 2)
        
        # Compute attention scores
        scores = torch.matmul(Q, K.transpose(-2, -1)) / np.sqrt(self.head_size)
        
        # Apply attention weights
        attention_weights = F.softmax(scores, dim=-1)
        
        # Apply attention to values
        attended = torch.matmul(attention_weights, V)
        
        # Reshape and apply output projection
        attended = attended.transpose(1, 2).contiguous().view(batch_size, seq_len, hidden_size)
        output = self.output(attended)
        
        return output


# Factory functions for common tetrahedral network configurations

def create_small_tetrahedral_network(input_dim: int, output_dim: int) -> TetrahedralNetwork:
    """Create a small tetrahedral network for testing."""
    config = TetrahedralConfig(
        input_dim=input_dim,
        output_dim=output_dim,
        max_layers=5,
        tetrahedral_scaling=0.5,
        min_layer_size=4,
        max_layer_size=128
    )
    return TetrahedralNetwork(config)


def create_large_tetrahedral_network(input_dim: int, output_dim: int) -> TetrahedralNetwork:
    """Create a large tetrahedral network for complex tasks."""
    config = TetrahedralConfig(
        input_dim=input_dim,
        output_dim=output_dim,
        max_layers=12,
        tetrahedral_scaling=2.0,
        min_layer_size=32,
        max_layer_size=2048,
        connection_type=TetrahedralConnectionType.SPARSE_TETRAHEDRAL
    )
    return TetrahedralNetwork(config)


def create_sequence_prediction_tetrahedral_network(sequence_length: int) -> TetrahedralNetwork:
    """Create a tetrahedral network optimized for sequence prediction."""
    config = TetrahedralConfig(
        input_dim=sequence_length,
        output_dim=1,  # Predict next value
        max_layers=8,
        tetrahedral_scaling=1.0,
        activation="gelu",
        dropout_rate=0.2,
        use_batch_norm=True
    )
    return TetrahedralNetwork(config)