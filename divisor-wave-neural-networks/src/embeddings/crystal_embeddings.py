"""
Crystal Embedding Models
========================

Hyperdimensional crystal embedding models using mathematical lattices for
structured semantic representations. Based on Leo J. Borcherding's unified
hyperdimensional crystal embedding model.

This module implements:
- Crystal sequence generation
- Icosahedral projections
- Sierpinski circlet transformers
- Geometric similarity measures
- Multi-modal crystal embeddings
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import List, Dict, Optional, Tuple, Union, Any
from dataclasses import dataclass
from enum import Enum
import math

from ..utils.mathematical_sequences import MathematicalSequences, SequenceType


class CrystalLatticeType(Enum):
    """Types of crystal lattices for embeddings."""
    CUBIC = "cubic"
    TETRAHEDRAL = "tetrahedral"
    OCTAHEDRAL = "octahedral"
    ICOSAHEDRAL = "icosahedral"
    DODECAHEDRAL = "dodecahedral"
    HEXAGONAL = "hexagonal"
    RHOMBOHEDRAL = "rhombohedral"


class CrystalSymmetryGroup(Enum):
    """Crystal symmetry groups."""
    POINT_GROUP = "point_group"
    SPACE_GROUP = "space_group"
    CRYSTALLOGRAPHIC = "crystallographic"


@dataclass
class CrystalEmbeddingConfig:
    """Configuration for crystal embedding models."""
    embedding_dim: int = 512
    lattice_type: CrystalLatticeType = CrystalLatticeType.ICOSAHEDRAL
    num_layers: int = 6
    num_heads: int = 8
    hidden_dim: int = 2048
    dropout_rate: float = 0.1
    symmetry_group: CrystalSymmetryGroup = CrystalSymmetryGroup.CRYSTALLOGRAPHIC
    use_geometric_similarity: bool = True
    temperature: float = 1.0
    max_sequence_length: int = 1024


class CrystalSequence(nn.Module):
    """
    Crystal sequence generator based on mathematical lattice structures.
    
    Generates sequences that follow crystal lattice patterns for use in
    embedding spaces and neural network architectures.
    """
    
    def __init__(self, 
                 lattice_type: CrystalLatticeType,
                 sequence_length: int = 512,
                 embedding_dim: int = 64):
        super().__init__()
        
        self.lattice_type = lattice_type
        self.sequence_length = sequence_length
        self.embedding_dim = embedding_dim
        
        # Initialize lattice parameters
        self.lattice_params = self._initialize_lattice_parameters()
        
        # Create crystal basis vectors
        self.basis_vectors = self._create_crystal_basis()
        
        # Sequence generation network
        self.sequence_net = nn.Sequential(
            nn.Linear(embedding_dim, embedding_dim * 2),
            nn.GELU(),
            nn.Linear(embedding_dim * 2, embedding_dim),
            nn.LayerNorm(embedding_dim)
        )
    
    def _initialize_lattice_parameters(self) -> Dict[str, torch.Tensor]:
        """Initialize parameters for the crystal lattice."""
        params = {}
        
        if self.lattice_type == CrystalLatticeType.CUBIC:
            # Cubic lattice: a = b = c, α = β = γ = 90°
            params['lattice_constants'] = torch.tensor([1.0, 1.0, 1.0])
            params['angles'] = torch.tensor([90.0, 90.0, 90.0]) * math.pi / 180
            
        elif self.lattice_type == CrystalLatticeType.TETRAHEDRAL:
            # Tetrahedral lattice parameters
            params['lattice_constants'] = torch.tensor([1.0, 1.0, 1.0])
            params['angles'] = torch.tensor([109.47, 109.47, 109.47]) * math.pi / 180
            
        elif self.lattice_type == CrystalLatticeType.ICOSAHEDRAL:
            # Icosahedral lattice (quasicrystal structure)
            phi = (1 + math.sqrt(5)) / 2  # Golden ratio
            params['lattice_constants'] = torch.tensor([1.0, phi, phi**2])
            params['angles'] = torch.tensor([72.0, 108.0, 144.0]) * math.pi / 180
            
        elif self.lattice_type == CrystalLatticeType.HEXAGONAL:
            # Hexagonal lattice: a = b ≠ c, α = β = 90°, γ = 120°
            params['lattice_constants'] = torch.tensor([1.0, 1.0, 1.633])  # c/a ≈ 1.633
            params['angles'] = torch.tensor([90.0, 90.0, 120.0]) * math.pi / 180
            
        else:
            # Default to cubic
            params['lattice_constants'] = torch.tensor([1.0, 1.0, 1.0])
            params['angles'] = torch.tensor([90.0, 90.0, 90.0]) * math.pi / 180
        
        # Convert to parameters
        for key, value in params.items():
            params[key] = nn.Parameter(value, requires_grad=False)
        
        return params
    
    def _create_crystal_basis(self) -> torch.Tensor:
        """Create basis vectors for the crystal lattice."""
        a, b, c = self.lattice_params['lattice_constants']
        alpha, beta, gamma = self.lattice_params['angles']
        
        # Create basis vectors based on lattice parameters
        # a-vector along x-axis
        a_vec = torch.tensor([a, 0.0, 0.0])
        
        # b-vector in xy-plane
        b_vec = torch.tensor([
            b * torch.cos(gamma),
            b * torch.sin(gamma),
            0.0
        ])
        
        # c-vector computed to satisfy angle constraints
        cx = c * torch.cos(beta)
        cy = c * (torch.cos(alpha) - torch.cos(beta) * torch.cos(gamma)) / torch.sin(gamma)
        cz = c * torch.sqrt(1 - torch.cos(beta)**2 - 
                           ((torch.cos(alpha) - torch.cos(beta) * torch.cos(gamma)) / torch.sin(gamma))**2)
        c_vec = torch.tensor([cx, cy, cz])
        
        # Stack basis vectors
        basis = torch.stack([a_vec, b_vec, c_vec], dim=0)
        
        return nn.Parameter(basis, requires_grad=False)
    
    def generate_crystal_sequence(self, batch_size: int) -> torch.Tensor:
        """Generate a sequence based on crystal lattice structure."""
        # Generate lattice points
        lattice_points = self._generate_lattice_points(batch_size)
        
        # Project to embedding space
        embeddings = self._project_to_embedding_space(lattice_points)
        
        # Apply sequence transformation
        sequence = self.sequence_net(embeddings)
        
        return sequence
    
    def _generate_lattice_points(self, batch_size: int) -> torch.Tensor:
        """Generate points in the crystal lattice."""
        # Generate lattice indices
        max_index = int(np.ceil(self.sequence_length**(1/3)))
        
        points = []
        for i in range(max_index):
            for j in range(max_index):
                for k in range(max_index):
                    if len(points) >= self.sequence_length:
                        break
                    
                    # Lattice point in fractional coordinates
                    frac_coords = torch.tensor([i/max_index, j/max_index, k/max_index])
                    
                    # Convert to Cartesian coordinates using basis vectors
                    cart_coords = torch.matmul(frac_coords, self.basis_vectors)
                    points.append(cart_coords)
                    
                if len(points) >= self.sequence_length:
                    break
            if len(points) >= self.sequence_length:
                break
        
        # Pad if necessary
        while len(points) < self.sequence_length:
            points.append(torch.zeros(3))
        
        # Stack and repeat for batch
        lattice_points = torch.stack(points[:self.sequence_length], dim=0)
        lattice_points = lattice_points.unsqueeze(0).repeat(batch_size, 1, 1)
        
        return lattice_points
    
    def _project_to_embedding_space(self, lattice_points: torch.Tensor) -> torch.Tensor:
        """Project 3D lattice points to higher-dimensional embedding space."""
        batch_size, seq_len, _ = lattice_points.shape
        
        # Use Fourier features for embedding
        frequencies = torch.randn(3, self.embedding_dim // 6)
        
        # Apply Fourier transform
        fourier_features = []
        for i in range(3):  # x, y, z coordinates
            coords = lattice_points[:, :, i].unsqueeze(-1)  # (batch, seq, 1)
            freqs = frequencies[i].unsqueeze(0).unsqueeze(0)  # (1, 1, embedding_dim//6)
            
            # Compute sin and cos features
            sin_features = torch.sin(2 * math.pi * coords * freqs)
            cos_features = torch.cos(2 * math.pi * coords * freqs)
            
            fourier_features.extend([sin_features, cos_features])
        
        # Concatenate all Fourier features
        embeddings = torch.cat(fourier_features, dim=-1)
        
        # Ensure correct embedding dimension
        if embeddings.shape[-1] != self.embedding_dim:
            # Project to correct dimension
            projection = nn.Linear(embeddings.shape[-1], self.embedding_dim)
            embeddings = projection(embeddings)
        
        return embeddings
    
    def forward(self, batch_size: int) -> torch.Tensor:
        """Forward pass to generate crystal sequences."""
        return self.generate_crystal_sequence(batch_size)


class IcosahedronProjection(nn.Module):
    """
    Icosahedral projection for crystal embeddings.
    
    Projects data onto the surface of an icosahedron, creating structured
    geometric representations with 20-fold symmetry.
    """
    
    def __init__(self, input_dim: int, output_dim: int = 512):
        super().__init__()
        
        self.input_dim = input_dim
        self.output_dim = output_dim
        
        # Create icosahedral vertices
        self.icosahedron_vertices = self._create_icosahedron_vertices()
        
        # Projection networks
        self.vertex_projections = nn.ModuleList([
            nn.Linear(input_dim, output_dim // 20) for _ in range(20)
        ])
        
        # Symmetry-aware combination
        self.combination_net = nn.Sequential(
            nn.Linear(output_dim, output_dim),
            nn.GELU(),
            nn.Linear(output_dim, output_dim),
            nn.LayerNorm(output_dim)
        )
    
    def _create_icosahedron_vertices(self) -> torch.Tensor:
        """Create the 12 vertices of a regular icosahedron."""
        phi = (1 + math.sqrt(5)) / 2  # Golden ratio
        
        vertices = torch.tensor([
            # Rectangle in xy-plane
            [1, phi, 0], [-1, phi, 0], [1, -phi, 0], [-1, -phi, 0],
            # Rectangle in xz-plane  
            [phi, 0, 1], [phi, 0, -1], [-phi, 0, 1], [-phi, 0, -1],
            # Rectangle in yz-plane
            [0, 1, phi], [0, -1, phi], [0, 1, -phi], [0, -1, -phi]
        ], dtype=torch.float32)
        
        # Normalize vertices to unit sphere
        vertices = F.normalize(vertices, dim=1)
        
        return nn.Parameter(vertices, requires_grad=False)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Project input onto icosahedral structure."""
        batch_size = x.shape[0]
        
        # Project to each of the 20 triangular faces (12 vertices -> 20 faces)
        face_projections = []
        
        for i in range(20):  # 20 faces of icosahedron
            projection = self.vertex_projections[i](x)
            face_projections.append(projection)
        
        # Combine projections
        combined = torch.cat(face_projections, dim=-1)
        
        # Apply symmetry-aware combination
        output = self.combination_net(combined)
        
        return output


class SierpinskiCircletTransformer(nn.Module):
    """
    Transformer network based on Sierpinski triangle and circle packing patterns.
    
    Uses fractal geometry to create attention patterns that follow
    mathematical structures found in crystal lattices.
    """
    
    def __init__(self, 
                 embedding_dim: int,
                 num_heads: int = 8,
                 num_layers: int = 6,
                 hidden_dim: int = 2048,
                 max_sequence_length: int = 1024):
        super().__init__()
        
        self.embedding_dim = embedding_dim
        self.num_heads = num_heads
        self.num_layers = num_layers
        
        # Create Sierpinski-based position encodings
        self.position_encoding = self._create_sierpinski_position_encoding(
            max_sequence_length, embedding_dim
        )
        
        # Transformer layers with fractal attention
        self.transformer_layers = nn.ModuleList([
            SierpinskiTransformerLayer(
                embedding_dim, num_heads, hidden_dim
            ) for _ in range(num_layers)
        ])
        
        # Layer normalization
        self.layer_norm = nn.LayerNorm(embedding_dim)
    
    def _create_sierpinski_position_encoding(self, 
                                           max_length: int, 
                                           embedding_dim: int) -> torch.Tensor:
        """Create position encodings based on Sierpinski triangle patterns."""
        position = torch.arange(max_length).unsqueeze(1).float()
        
        # Create frequency patterns based on Sierpinski triangle
        div_term = torch.exp(torch.arange(0, embedding_dim, 2).float() * 
                           -(math.log(10000.0) / embedding_dim))
        
        pos_encoding = torch.zeros(max_length, embedding_dim)
        
        # Apply Sierpinski-inspired modulation
        for i in range(max_length):
            # Sierpinski triangle coordinate
            sierpinski_level = int(math.log2(i + 1)) if i > 0 else 0
            sierpinski_coord = (i >> sierpinski_level) / (2 ** sierpinski_level)
            
            # Modulate position encoding with Sierpinski coordinate
            pos_encoding[i, 0::2] = torch.sin(position[i] * div_term) * sierpinski_coord
            pos_encoding[i, 1::2] = torch.cos(position[i] * div_term) * sierpinski_coord
        
        return nn.Parameter(pos_encoding, requires_grad=False)
    
    def forward(self, x: torch.Tensor, mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        """Forward pass through Sierpinski circlet transformer."""
        seq_length = x.shape[1]
        
        # Add position encoding
        x = x + self.position_encoding[:seq_length]
        
        # Apply transformer layers
        for layer in self.transformer_layers:
            x = layer(x, mask)
        
        # Final layer normalization
        x = self.layer_norm(x)
        
        return x


class SierpinskiTransformerLayer(nn.Module):
    """Single transformer layer with Sierpinski-based attention."""
    
    def __init__(self, embedding_dim: int, num_heads: int, hidden_dim: int):
        super().__init__()
        
        self.attention = SierpinskiAttention(embedding_dim, num_heads)
        self.feed_forward = nn.Sequential(
            nn.Linear(embedding_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, embedding_dim)
        )
        
        self.norm1 = nn.LayerNorm(embedding_dim)
        self.norm2 = nn.LayerNorm(embedding_dim)
        self.dropout = nn.Dropout(0.1)
    
    def forward(self, x: torch.Tensor, mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        # Self-attention with residual connection
        attended = self.attention(x, mask)
        x = self.norm1(x + self.dropout(attended))
        
        # Feed-forward with residual connection
        fed_forward = self.feed_forward(x)
        x = self.norm2(x + self.dropout(fed_forward))
        
        return x


class SierpinskiAttention(nn.Module):
    """Attention mechanism based on Sierpinski triangle patterns."""
    
    def __init__(self, embedding_dim: int, num_heads: int):
        super().__init__()
        
        self.embedding_dim = embedding_dim
        self.num_heads = num_heads
        self.head_dim = embedding_dim // num_heads
        
        assert embedding_dim % num_heads == 0
        
        # Query, Key, Value projections
        self.query = nn.Linear(embedding_dim, embedding_dim)
        self.key = nn.Linear(embedding_dim, embedding_dim)
        self.value = nn.Linear(embedding_dim, embedding_dim)
        
        # Output projection
        self.output = nn.Linear(embedding_dim, embedding_dim)
        
        # Sierpinski attention mask
        self.register_buffer('attention_mask', self._create_sierpinski_mask())
    
    def _create_sierpinski_mask(self) -> torch.Tensor:
        """Create attention mask based on Sierpinski triangle pattern."""
        # This is a simplified version - full implementation would be more complex
        max_length = 1024
        mask = torch.ones(max_length, max_length)
        
        for i in range(max_length):
            for j in range(max_length):
                # Apply Sierpinski triangle rule
                if (i & j) != 0:  # Sierpinski triangle condition
                    mask[i, j] = 0.0
        
        return mask
    
    def forward(self, x: torch.Tensor, mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        batch_size, seq_length, _ = x.shape
        
        # Apply projections and reshape for multi-head attention
        Q = self.query(x).view(batch_size, seq_length, self.num_heads, self.head_dim).transpose(1, 2)
        K = self.key(x).view(batch_size, seq_length, self.num_heads, self.head_dim).transpose(1, 2)
        V = self.value(x).view(batch_size, seq_length, self.num_heads, self.head_dim).transpose(1, 2)
        
        # Compute attention scores
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.head_dim)
        
        # Apply Sierpinski mask
        sierpinski_mask = self.attention_mask[:seq_length, :seq_length]
        scores = scores * sierpinski_mask.unsqueeze(0).unsqueeze(0)
        
        # Apply additional mask if provided
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        
        # Apply softmax
        attention_weights = F.softmax(scores, dim=-1)
        
        # Apply attention to values
        attended = torch.matmul(attention_weights, V)
        
        # Reshape and apply output projection
        attended = attended.transpose(1, 2).contiguous().view(batch_size, seq_length, self.embedding_dim)
        output = self.output(attended)
        
        return output


class CrystalEmbedding(nn.Module):
    """
    Main crystal embedding model that combines all components.
    
    Creates structured semantic representations using mathematical lattices,
    icosahedral projections, and Sierpinski-based transformers.
    """
    
    def __init__(self, config: CrystalEmbeddingConfig):
        super().__init__()
        
        self.config = config
        
        # Crystal sequence generator
        self.crystal_sequence = CrystalSequence(
            lattice_type=config.lattice_type,
            sequence_length=config.max_sequence_length,
            embedding_dim=config.embedding_dim
        )
        
        # Icosahedral projection
        self.icosahedral_projection = IcosahedronProjection(
            input_dim=config.embedding_dim,
            output_dim=config.embedding_dim
        )
        
        # Sierpinski circlet transformer
        self.sierpinski_transformer = SierpinskiCircletTransformer(
            embedding_dim=config.embedding_dim,
            num_heads=config.num_heads,
            num_layers=config.num_layers,
            hidden_dim=config.hidden_dim,
            max_sequence_length=config.max_sequence_length
        )
        
        # Final projection layer
        self.final_projection = nn.Linear(config.embedding_dim, config.embedding_dim)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through crystal embedding model."""
        batch_size = x.shape[0]
        
        # Generate crystal sequence
        crystal_seq = self.crystal_sequence(batch_size)
        
        # Combine input with crystal sequence
        combined = x + crystal_seq[:, :x.shape[1]]
        
        # Apply icosahedral projection
        projected = self.icosahedral_projection(combined)
        
        # Apply Sierpinski transformer
        transformed = self.sierpinski_transformer(projected)
        
        # Final projection
        embeddings = self.final_projection(transformed)
        
        return embeddings
    
    def embed(self, x: torch.Tensor) -> torch.Tensor:
        """Create embeddings for input data."""
        return self.forward(x)
    
    def get_crystal_structure_info(self) -> Dict[str, Any]:
        """Get information about the crystal structure used."""
        return {
            "lattice_type": self.config.lattice_type.value,
            "embedding_dim": self.config.embedding_dim,
            "lattice_constants": self.crystal_sequence.lattice_params['lattice_constants'].tolist(),
            "lattice_angles": self.crystal_sequence.lattice_params['angles'].tolist(),
            "basis_vectors": self.crystal_sequence.basis_vectors.tolist(),
        }


# Factory functions for different crystal embedding configurations

def create_icosahedral_embedding(embedding_dim: int = 512) -> CrystalEmbedding:
    """Create icosahedral crystal embedding model."""
    config = CrystalEmbeddingConfig(
        embedding_dim=embedding_dim,
        lattice_type=CrystalLatticeType.ICOSAHEDRAL,
        num_heads=20,  # Match icosahedral faces
        num_layers=12   # Match icosahedral vertices
    )
    return CrystalEmbedding(config)


def create_tetrahedral_embedding(embedding_dim: int = 512) -> CrystalEmbedding:
    """Create tetrahedral crystal embedding model."""
    config = CrystalEmbeddingConfig(
        embedding_dim=embedding_dim,
        lattice_type=CrystalLatticeType.TETRAHEDRAL,
        num_heads=4,   # Match tetrahedral faces
        num_layers=4   # Match tetrahedral vertices
    )
    return CrystalEmbedding(config)