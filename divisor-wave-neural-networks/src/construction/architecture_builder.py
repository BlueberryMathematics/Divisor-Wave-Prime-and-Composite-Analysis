"""
Architecture Builder - Custom Neural Network Construction System
===============================================================

Comprehensive system for building custom neural network architectures
based on mathematical principles, sequences, and geometric structures.

This module provides:
- Interactive architecture builder
- Mathematical layer library
- Custom activation functions
- Architecture optimization
- Automated training pipelines
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import List, Dict, Optional, Tuple, Union, Any, Callable, Type
from dataclasses import dataclass, field
from enum import Enum
import math
import json

from ..utils.mathematical_sequences import MathematicalSequences, SequenceType
from ..architectures.tetrahedral_networks import TetrahedralLayer, TetrahedralConnectionType
from ..embeddings.crystal_embeddings import CrystalEmbedding


class LayerType(Enum):
    """Types of layers available in the architecture builder."""
    LINEAR = "linear"
    CONVOLUTIONAL = "convolutional"
    RECURRENT = "recurrent"
    ATTENTION = "attention"
    TETRAHEDRAL = "tetrahedral"
    CRYSTAL_EMBEDDING = "crystal_embedding"
    MATHEMATICAL_FUNCTION = "mathematical_function"
    SEQUENCE_BASED = "sequence_based"
    FRACTAL = "fractal"
    PRIME_BASED = "prime_based"
    GEOMETRIC = "geometric"
    CUSTOM = "custom"


class ActivationType(Enum):
    """Mathematical activation functions."""
    RELU = "relu"
    TANH = "tanh"
    SIGMOID = "sigmoid"
    GELU = "gelu"
    SWISH = "swish"
    # Mathematical activations
    SINE = "sine"
    COSINE = "cosine"
    EXPONENTIAL = "exponential"
    LOGARITHMIC = "logarithmic"
    TETRAHEDRAL = "tetrahedral"
    FIBONACCI = "fibonacci"
    PRIME_MODULO = "prime_modulo"
    ZETA_FUNCTION = "zeta_function"


class ConnectionPattern(Enum):
    """Connection patterns between layers."""
    FULLY_CONNECTED = "fully_connected"
    SPARSE = "sparse"
    RESIDUAL = "residual"
    DENSE = "dense"
    TETRAHEDRAL = "tetrahedral"
    PRIME_BASED = "prime_based"
    FIBONACCI = "fibonacci"
    CRYSTAL_LATTICE = "crystal_lattice"
    FRACTAL = "fractal"


@dataclass
class LayerSpec:
    """Specification for a single layer."""
    layer_type: LayerType
    input_size: int
    output_size: int
    activation: ActivationType = ActivationType.RELU
    connection_pattern: ConnectionPattern = ConnectionPattern.FULLY_CONNECTED
    sequence_type: Optional[SequenceType] = None
    mathematical_params: Dict[str, Any] = field(default_factory=dict)
    custom_properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ArchitectureSpec:
    """Complete specification for a neural network architecture."""
    name: str
    description: str
    input_dim: int
    output_dim: int
    layers: List[LayerSpec] = field(default_factory=list)
    global_properties: Dict[str, Any] = field(default_factory=dict)
    mathematical_foundation: Optional[str] = None
    sequence_basis: Optional[SequenceType] = None


class MathematicalActivation(nn.Module):
    """Custom activation functions based on mathematical functions."""
    
    def __init__(self, activation_type: ActivationType, **kwargs):
        super().__init__()
        self.activation_type = activation_type
        self.params = kwargs
        
        # Initialize parameters for mathematical activations
        if activation_type == ActivationType.TETRAHEDRAL:
            self.tetrahedral_index = kwargs.get('tetrahedral_index', 1)
        elif activation_type == ActivationType.PRIME_MODULO:
            self.prime_base = kwargs.get('prime_base', 7)
        elif activation_type == ActivationType.ZETA_FUNCTION:
            self.s_value = nn.Parameter(torch.tensor(kwargs.get('s_value', 2.0)))
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Apply mathematical activation function."""
        if self.activation_type == ActivationType.SINE:
            return torch.sin(x)
        elif self.activation_type == ActivationType.COSINE:
            return torch.cos(x)
        elif self.activation_type == ActivationType.EXPONENTIAL:
            return torch.exp(torch.clamp(x, max=10))  # Prevent overflow
        elif self.activation_type == ActivationType.LOGARITHMIC:
            return torch.log(torch.abs(x) + 1e-8)
        elif self.activation_type == ActivationType.TETRAHEDRAL:
            # Tetrahedral activation: x^3 - 3x (similar to tetrahedral polynomial)
            return x**3 - 3*x
        elif self.activation_type == ActivationType.FIBONACCI:
            # Fibonacci-inspired activation
            phi = (1 + math.sqrt(5)) / 2  # Golden ratio
            return (torch.pow(phi, x) - torch.pow(-phi, -x)) / math.sqrt(5)
        elif self.activation_type == ActivationType.PRIME_MODULO:
            # Prime-based modular activation
            return torch.fmod(x * self.prime_base, self.prime_base) / self.prime_base
        elif self.activation_type == ActivationType.ZETA_FUNCTION:
            # Simplified Riemann zeta function approximation
            return torch.pow(torch.abs(x) + 1, -self.s_value)
        else:
            # Standard activations
            if self.activation_type == ActivationType.RELU:
                return F.relu(x)
            elif self.activation_type == ActivationType.TANH:
                return torch.tanh(x)
            elif self.activation_type == ActivationType.SIGMOID:
                return torch.sigmoid(x)
            elif self.activation_type == ActivationType.GELU:
                return F.gelu(x)
            elif self.activation_type == ActivationType.SWISH:
                return x * torch.sigmoid(x)
            else:
                return F.relu(x)  # Default


class MathematicalLayer(nn.Module):
    """
    Custom layer that incorporates mathematical structures and sequences.
    """
    
    def __init__(self, layer_spec: LayerSpec):
        super().__init__()
        
        self.spec = layer_spec
        self.seq_generator = MathematicalSequences()
        
        # Create the main transformation
        self.transformation = self._create_transformation()
        
        # Create activation function
        self.activation = MathematicalActivation(
            layer_spec.activation,
            **layer_spec.mathematical_params
        )
        
        # Additional mathematical components
        if layer_spec.sequence_type:
            self._initialize_sequence_components()
        
        # Connection pattern modifications
        if layer_spec.connection_pattern != ConnectionPattern.FULLY_CONNECTED:
            self._apply_connection_pattern()
    
    def _create_transformation(self) -> nn.Module:
        """Create the main transformation based on layer type."""
        if self.spec.layer_type == LayerType.LINEAR:
            return nn.Linear(self.spec.input_size, self.spec.output_size)
        
        elif self.spec.layer_type == LayerType.TETRAHEDRAL:
            return TetrahedralLayer(
                input_size=self.spec.input_size,
                output_size=self.spec.output_size,
                tetrahedral_index=self.spec.mathematical_params.get('tetrahedral_index', 1),
                connection_type=TetrahedralConnectionType.TETRAHEDRAL
            )
        
        elif self.spec.layer_type == LayerType.SEQUENCE_BASED:
            # Create layer with sizes based on mathematical sequence
            if self.spec.sequence_type:
                return self._create_sequence_based_layer()
            else:
                return nn.Linear(self.spec.input_size, self.spec.output_size)
        
        elif self.spec.layer_type == LayerType.PRIME_BASED:
            return self._create_prime_based_layer()
        
        elif self.spec.layer_type == LayerType.FRACTAL:
            return self._create_fractal_layer()
        
        else:
            # Default to linear
            return nn.Linear(self.spec.input_size, self.spec.output_size)
    
    def _create_sequence_based_layer(self) -> nn.Module:
        """Create a layer based on mathematical sequence properties."""
        sequence = self.seq_generator.get_sequence_by_type(
            self.spec.sequence_type, 
            max(self.spec.input_size, self.spec.output_size)
        )
        
        # Use sequence values to create structured connections
        class SequenceLinear(nn.Module):
            def __init__(self, input_size, output_size, sequence_values):
                super().__init__()
                self.linear = nn.Linear(input_size, output_size)
                self.sequence_mask = self._create_sequence_mask(
                    input_size, output_size, sequence_values
                )
                
            def _create_sequence_mask(self, input_size, output_size, seq_vals):
                mask = torch.zeros(output_size, input_size)
                seq_normalized = seq_vals / torch.max(seq_vals)
                
                for i in range(output_size):
                    for j in range(input_size):
                        # Connection strength based on sequence values
                        idx = (i + j) % len(seq_normalized)
                        mask[i, j] = seq_normalized[idx]
                
                return nn.Parameter(mask, requires_grad=False)
            
            def forward(self, x):
                # Apply sequence-based masking
                masked_weight = self.linear.weight * self.sequence_mask
                return F.linear(x, masked_weight, self.linear.bias)
        
        return SequenceLinear(self.spec.input_size, self.spec.output_size, sequence)
    
    def _create_prime_based_layer(self) -> nn.Module:
        """Create a layer with connections based on prime number patterns."""
        class PrimeLinear(nn.Module):
            def __init__(self, input_size, output_size):
                super().__init__()
                self.linear = nn.Linear(input_size, output_size)
                self.prime_mask = self._create_prime_mask(input_size, output_size)
                
            def _create_prime_mask(self, input_size, output_size):
                mask = torch.zeros(output_size, input_size)
                
                # Simple prime-based connection pattern
                primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
                
                for i in range(output_size):
                    for j in range(input_size):
                        # Connection exists if (i+j) is related to a prime
                        for p in primes:
                            if (i + j + 1) % p == 0:
                                mask[i, j] = 1.0
                                break
                
                return nn.Parameter(mask, requires_grad=False)
            
            def forward(self, x):
                masked_weight = self.linear.weight * self.prime_mask
                return F.linear(x, masked_weight, self.linear.bias)
        
        return PrimeLinear(self.spec.input_size, self.spec.output_size)
    
    def _create_fractal_layer(self) -> nn.Module:
        """Create a layer with fractal connection patterns."""
        class FractalLinear(nn.Module):
            def __init__(self, input_size, output_size):
                super().__init__()
                self.linear = nn.Linear(input_size, output_size)
                self.fractal_mask = self._create_fractal_mask(input_size, output_size)
                
            def _create_fractal_mask(self, input_size, output_size):
                mask = torch.zeros(output_size, input_size)
                
                # Sierpinski triangle-inspired pattern
                for i in range(output_size):
                    for j in range(input_size):
                        # Sierpinski triangle condition
                        if (i & j) == 0:  # Bitwise AND
                            mask[i, j] = 1.0
                
                return nn.Parameter(mask, requires_grad=False)
            
            def forward(self, x):
                masked_weight = self.linear.weight * self.fractal_mask
                return F.linear(x, masked_weight, self.linear.bias)
        
        return FractalLinear(self.spec.input_size, self.spec.output_size)
    
    def _initialize_sequence_components(self):
        """Initialize components based on the sequence type."""
        sequence = self.seq_generator.get_sequence_by_type(
            self.spec.sequence_type, self.spec.output_size
        )
        
        # Sequence-based bias initialization
        self.sequence_bias = nn.Parameter(sequence[:self.spec.output_size] / 100.0)
    
    def _apply_connection_pattern(self):
        """Apply special connection patterns to the layer."""
        if hasattr(self.transformation, 'weight'):
            weight = self.transformation.weight
            
            if self.spec.connection_pattern == ConnectionPattern.SPARSE:
                # Create sparse connections (keep only top 50% of weights)
                with torch.no_grad():
                    threshold = torch.quantile(torch.abs(weight), 0.5)
                    mask = torch.abs(weight) >= threshold
                    weight.data *= mask.float()
            
            elif self.spec.connection_pattern == ConnectionPattern.CRYSTAL_LATTICE:
                # Apply crystal lattice-like connectivity
                with torch.no_grad():
                    # Simple cubic lattice pattern
                    for i in range(weight.shape[0]):
                        for j in range(weight.shape[1]):
                            if (i + j) % 3 != 0:  # Keep every 3rd connection
                                weight[i, j] = 0.0
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through mathematical layer."""
        # Apply main transformation
        out = self.transformation(x)
        
        # Add sequence bias if available
        if hasattr(self, 'sequence_bias'):
            out = out + self.sequence_bias
        
        # Apply activation
        out = self.activation(out)
        
        return out


class ArchitectureBuilder:
    """
    Interactive builder for creating custom neural network architectures
    based on mathematical principles and sequences.
    """
    
    def __init__(self):
        self.architectures = {}
        self.layer_templates = self._create_layer_templates()
        self.seq_generator = MathematicalSequences()
    
    def _create_layer_templates(self) -> Dict[str, LayerSpec]:
        """Create predefined layer templates."""
        templates = {
            "tetrahedral": LayerSpec(
                layer_type=LayerType.TETRAHEDRAL,
                input_size=64,
                output_size=32,
                activation=ActivationType.TETRAHEDRAL,
                mathematical_params={"tetrahedral_index": 1}
            ),
            
            "fibonacci": LayerSpec(
                layer_type=LayerType.SEQUENCE_BASED,
                input_size=64,
                output_size=32,
                activation=ActivationType.FIBONACCI,
                sequence_type=SequenceType.FIBONACCI
            ),
            
            "prime": LayerSpec(
                layer_type=LayerType.PRIME_BASED,
                input_size=64,
                output_size=32,
                activation=ActivationType.PRIME_MODULO,
                connection_pattern=ConnectionPattern.PRIME_BASED,
                mathematical_params={"prime_base": 7}
            ),
            
            "fractal": LayerSpec(
                layer_type=LayerType.FRACTAL,
                input_size=64,
                output_size=32,
                activation=ActivationType.SINE,
                connection_pattern=ConnectionPattern.FRACTAL
            ),
            
            "crystal": LayerSpec(
                layer_type=LayerType.CRYSTAL_EMBEDDING,
                input_size=64,
                output_size=64,
                activation=ActivationType.GELU
            )
        }
        return templates
    
    def create_architecture(self, name: str, description: str = "") -> ArchitectureSpec:
        """Create a new architecture specification."""
        arch = ArchitectureSpec(
            name=name,
            description=description,
            input_dim=0,
            output_dim=0
        )
        self.architectures[name] = arch
        return arch
    
    def add_layer(self, 
                  architecture_name: str,
                  layer_spec: Union[LayerSpec, str]) -> None:
        """Add a layer to an architecture."""
        if architecture_name not in self.architectures:
            raise ValueError(f"Architecture '{architecture_name}' not found")
        
        arch = self.architectures[architecture_name]
        
        if isinstance(layer_spec, str):
            # Use template
            if layer_spec not in self.layer_templates:
                raise ValueError(f"Layer template '{layer_spec}' not found")
            layer_spec = self.layer_templates[layer_spec]
        
        arch.layers.append(layer_spec)
    
    def auto_generate_architecture(self, 
                                 input_dim: int,
                                 output_dim: int,
                                 sequence_type: SequenceType,
                                 num_layers: int = 5) -> ArchitectureSpec:
        """Automatically generate architecture based on mathematical sequence."""
        # Generate layer sizes based on sequence
        layer_sizes = self.seq_generator.generate_architecture_sequence(
            sequence_type, num_layers, scale_factor=0.1
        )
        
        # Ensure proper input/output dimensions
        layer_sizes = [input_dim] + layer_sizes + [output_dim]
        
        # Create architecture
        arch_name = f"auto_{sequence_type.value}_{num_layers}layers"
        arch = self.create_architecture(
            arch_name,
            f"Auto-generated architecture based on {sequence_type.value} sequence"
        )
        
        arch.input_dim = input_dim
        arch.output_dim = output_dim
        arch.sequence_basis = sequence_type
        
        # Add layers
        for i in range(len(layer_sizes) - 1):
            layer_spec = LayerSpec(
                layer_type=LayerType.SEQUENCE_BASED,
                input_size=layer_sizes[i],
                output_size=layer_sizes[i + 1],
                sequence_type=sequence_type,
                activation=ActivationType.GELU if i < len(layer_sizes) - 2 else ActivationType.LINEAR
            )
            arch.layers.append(layer_spec)
        
        return arch
    
    def build_network(self, architecture_spec: ArchitectureSpec) -> nn.Module:
        """Build actual PyTorch network from architecture specification."""
        layers = []
        
        for layer_spec in architecture_spec.layers:
            layer = MathematicalLayer(layer_spec)
            layers.append(layer)
        
        class CustomArchitecture(nn.Module):
            def __init__(self, layers, arch_spec):
                super().__init__()
                self.layers = nn.ModuleList(layers)
                self.arch_spec = arch_spec
            
            def forward(self, x):
                for layer in self.layers:
                    x = layer(x)
                return x
            
            def get_architecture_info(self):
                return {
                    "name": self.arch_spec.name,
                    "description": self.arch_spec.description,
                    "num_layers": len(self.layers),
                    "total_parameters": sum(p.numel() for p in self.parameters()),
                    "sequence_basis": self.arch_spec.sequence_basis.value if self.arch_spec.sequence_basis else None
                }
        
        return CustomArchitecture(layers, architecture_spec)
    
    def optimize_architecture(self, 
                            architecture_spec: ArchitectureSpec,
                            target_performance: float = 0.95,
                            max_iterations: int = 10) -> ArchitectureSpec:
        """Optimize architecture for better performance."""
        # This is a simplified optimization - full implementation would be more sophisticated
        best_arch = architecture_spec
        
        for iteration in range(max_iterations):
            # Try different modifications
            modified_arch = self._mutate_architecture(best_arch)
            
            # Evaluate architecture (simplified)
            score = self._evaluate_architecture(modified_arch)
            
            if score > target_performance:
                best_arch = modified_arch
                break
        
        return best_arch
    
    def _mutate_architecture(self, arch: ArchitectureSpec) -> ArchitectureSpec:
        """Create a mutated version of the architecture."""
        # Create a copy
        new_arch = ArchitectureSpec(
            name=f"{arch.name}_mutated",
            description=f"Mutated version of {arch.name}",
            input_dim=arch.input_dim,
            output_dim=arch.output_dim,
            layers=arch.layers.copy()
        )
        
        # Random mutations
        if len(new_arch.layers) > 1:
            # Randomly modify a layer
            layer_idx = np.random.randint(0, len(new_arch.layers))
            layer = new_arch.layers[layer_idx]
            
            # Change activation function
            activations = list(ActivationType)
            layer.activation = np.random.choice(activations)
        
        return new_arch
    
    def _evaluate_architecture(self, arch: ArchitectureSpec) -> float:
        """Evaluate architecture performance (simplified)."""
        # This would involve actual training and testing
        # For now, return a random score based on architecture properties
        score = 0.5
        
        # Bonus for mathematical foundations
        if arch.sequence_basis:
            score += 0.2
        
        # Bonus for reasonable number of layers
        if 3 <= len(arch.layers) <= 10:
            score += 0.1
        
        # Add some randomness
        score += np.random.normal(0, 0.1)
        
        return max(0, min(1, score))
    
    def save_architecture(self, architecture_name: str, filepath: str) -> None:
        """Save architecture specification to file."""
        if architecture_name not in self.architectures:
            raise ValueError(f"Architecture '{architecture_name}' not found")
        
        arch = self.architectures[architecture_name]
        
        # Convert to serializable format
        arch_dict = {
            "name": arch.name,
            "description": arch.description,
            "input_dim": arch.input_dim,
            "output_dim": arch.output_dim,
            "sequence_basis": arch.sequence_basis.value if arch.sequence_basis else None,
            "layers": []
        }
        
        for layer in arch.layers:
            layer_dict = {
                "layer_type": layer.layer_type.value,
                "input_size": layer.input_size,
                "output_size": layer.output_size,
                "activation": layer.activation.value,
                "connection_pattern": layer.connection_pattern.value,
                "sequence_type": layer.sequence_type.value if layer.sequence_type else None,
                "mathematical_params": layer.mathematical_params,
                "custom_properties": layer.custom_properties
            }
            arch_dict["layers"].append(layer_dict)
        
        with open(filepath, 'w') as f:
            json.dump(arch_dict, f, indent=2)
    
    def load_architecture(self, filepath: str) -> ArchitectureSpec:
        """Load architecture specification from file."""
        with open(filepath, 'r') as f:
            arch_dict = json.load(f)
        
        arch = ArchitectureSpec(
            name=arch_dict["name"],
            description=arch_dict["description"],
            input_dim=arch_dict["input_dim"],
            output_dim=arch_dict["output_dim"]
        )
        
        if arch_dict["sequence_basis"]:
            arch.sequence_basis = SequenceType(arch_dict["sequence_basis"])
        
        for layer_dict in arch_dict["layers"]:
            layer = LayerSpec(
                layer_type=LayerType(layer_dict["layer_type"]),
                input_size=layer_dict["input_size"],
                output_size=layer_dict["output_size"],
                activation=ActivationType(layer_dict["activation"]),
                connection_pattern=ConnectionPattern(layer_dict["connection_pattern"]),
                mathematical_params=layer_dict["mathematical_params"],
                custom_properties=layer_dict["custom_properties"]
            )
            
            if layer_dict["sequence_type"]:
                layer.sequence_type = SequenceType(layer_dict["sequence_type"])
            
            arch.layers.append(layer)
        
        self.architectures[arch.name] = arch
        return arch


# Factory functions for common architectures

def create_tetrahedral_discovery_network(input_dim: int, output_dim: int) -> nn.Module:
    """Create a network optimized for tetrahedral sequence discovery."""
    builder = ArchitectureBuilder()
    arch = builder.auto_generate_architecture(
        input_dim, output_dim, SequenceType.TETRAHEDRAL, num_layers=6
    )
    return builder.build_network(arch)


def create_prime_pattern_network(input_dim: int, output_dim: int) -> nn.Module:
    """Create a network optimized for prime number pattern recognition."""
    builder = ArchitectureBuilder()
    arch = builder.auto_generate_architecture(
        input_dim, output_dim, SequenceType.PRIME, num_layers=5
    )
    return builder.build_network(arch)


def create_fibonacci_sequence_network(input_dim: int, output_dim: int) -> nn.Module:
    """Create a network based on Fibonacci sequence architecture."""
    builder = ArchitectureBuilder()
    arch = builder.auto_generate_architecture(
        input_dim, output_dim, SequenceType.FIBONACCI, num_layers=7
    )
    return builder.build_network(arch)