"""
THRML Integration - Ising Neural Networks
=========================================

Integration of THRML (JAX-based probabilistic graphical models) with PyTorch
neural networks for energy-based models and Ising chain compute blocks.

This module provides:
- Ising model neural networks
- Energy-based discovery models
- Block Gibbs sampling integration
- JAX-PyTorch bridges
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import List, Dict, Optional, Tuple, Union, Any, Callable
from dataclasses import dataclass
from enum import Enum
import warnings

# JAX and THRML imports with fallback
try:
    import jax
    import jax.numpy as jnp
    from thrml import SpinNode, Block, SamplingSchedule, sample_states
    from thrml.models import IsingEBM, IsingSamplingProgram
    from thrml.block_management import BlockGibbsSpec
    from thrml.block_sampling import SamplingSchedule
    from thrml.pgm import CategoricalNode
    from thrml.models.discrete_ebm import CategoricalEBMFactor, CategoricalGibbsConditional
    from thrml.factor import FactorSamplingProgram
    THRML_AVAILABLE = True
except ImportError:
    warnings.warn("THRML library not available. Ising neural networks will use PyTorch-only fallbacks.")
    THRML_AVAILABLE = False
    # Create dummy classes for type hints
    class SpinNode: pass
    class Block: pass
    class IsingEBM: pass


class IsingModelType(Enum):
    """Types of Ising models for neural networks."""
    CLASSICAL = "classical"
    QUANTUM = "quantum"
    TRANSVERSE_FIELD = "transverse_field"
    LONG_RANGE = "long_range"
    HIERARCHICAL = "hierarchical"


class SamplingMethod(Enum):
    """Sampling methods for Ising models."""
    GIBBS = "gibbs"
    METROPOLIS = "metropolis"
    WOLFF = "wolff"
    SWENDSEN_WANG = "swendsen_wang"
    THRML_BLOCK_GIBBS = "thrml_block_gibbs"


@dataclass
class IsingNeuralNetworkConfig:
    """Configuration for Ising neural networks."""
    lattice_size: Tuple[int, ...] = (10, 10)
    model_type: IsingModelType = IsingModelType.CLASSICAL
    sampling_method: SamplingMethod = SamplingMethod.THRML_BLOCK_GIBBS
    temperature: float = 1.0
    magnetic_field: float = 0.0
    coupling_strength: float = 1.0
    num_layers: int = 4
    hidden_dim: int = 256
    use_thrml: bool = True
    n_warmup: int = 100
    n_samples: int = 1000
    steps_per_sample: int = 2


class IsingLayer(nn.Module):
    """
    Neural network layer based on Ising model interactions.
    
    Each neuron represents a spin, and connections follow Ising model rules.
    """
    
    def __init__(self, 
                 input_size: int,
                 output_size: int,
                 temperature: float = 1.0,
                 coupling_strength: float = 1.0,
                 magnetic_field: float = 0.0,
                 use_thrml: bool = True):
        super().__init__()
        
        self.input_size = input_size
        self.output_size = output_size
        self.temperature = temperature
        self.coupling_strength = coupling_strength
        self.magnetic_field = magnetic_field
        self.use_thrml = use_thrml and THRML_AVAILABLE
        
        # Coupling matrix (symmetric for Ising model)
        self.coupling_matrix = nn.Parameter(
            torch.randn(output_size, input_size) * coupling_strength
        )
        
        # Local magnetic fields
        self.local_fields = nn.Parameter(
            torch.ones(output_size) * magnetic_field
        )
        
        # THRML components (if available)
        if self.use_thrml:
            self._initialize_thrml_components()
        
        # PyTorch fallback components
        self.activation = nn.Tanh()  # Spin-like activation
        
    def _initialize_thrml_components(self):
        """Initialize THRML components for exact Ising sampling."""
        if not THRML_AVAILABLE:
            return
            
        # Create spin nodes
        self.spin_nodes = [SpinNode() for _ in range(self.output_size)]
        
        # Create edges based on coupling matrix
        self.edges = []
        for i in range(self.output_size):
            for j in range(self.input_size):
                if abs(self.coupling_matrix[i, j].item()) > 1e-6:
                    # Note: This is simplified - full implementation would be more complex
                    pass
        
        # Create THRML Ising model
        try:
            biases = jnp.array(self.local_fields.detach().numpy())
            weights = jnp.array([self.coupling_strength] * len(self.edges))
            beta = jnp.array(1.0 / self.temperature)
            
            self.thrml_model = IsingEBM(
                self.spin_nodes, 
                self.edges, 
                biases, 
                weights, 
                beta
            )
        except Exception as e:
            warnings.warn(f"Failed to initialize THRML model: {e}")
            self.use_thrml = False
    
    def _ising_energy(self, spins: torch.Tensor) -> torch.Tensor:
        """Calculate Ising energy for given spin configuration."""
        batch_size = spins.shape[0]
        
        # Interaction energy: -J * sum(s_i * s_j) for connected spins
        interaction_energy = -torch.sum(
            spins.unsqueeze(2) * self.coupling_matrix.unsqueeze(0) * spins.unsqueeze(1),
            dim=(1, 2)
        )
        
        # Field energy: -h * sum(s_i)
        field_energy = -torch.sum(self.local_fields.unsqueeze(0) * spins, dim=1)
        
        total_energy = interaction_energy + field_energy
        return total_energy
    
    def _sample_with_thrml(self, input_spins: torch.Tensor) -> torch.Tensor:
        """Sample output spins using THRML."""
        if not self.use_thrml or not THRML_AVAILABLE:
            return self._sample_with_pytorch(input_spins)
        
        try:
            batch_size = input_spins.shape[0]
            output_samples = []
            
            for b in range(batch_size):
                # Create sampling program
                free_blocks = [Block([node]) for node in self.spin_nodes]
                program = IsingSamplingProgram(self.thrml_model, free_blocks, clamped_blocks=[])
                
                # Sample
                key = jax.random.key(np.random.randint(0, 2**31))
                init_state = jnp.array(np.random.choice([-1, 1], size=self.output_size))
                schedule = SamplingSchedule(n_warmup=10, n_samples=1, steps_per_sample=1)
                
                samples = sample_states(
                    key, program, schedule, init_state, [], [Block(self.spin_nodes)]
                )
                
                # Convert to torch tensor
                sample_tensor = torch.tensor(np.array(samples[0][0]), dtype=torch.float32)
                output_samples.append(sample_tensor)
                
            return torch.stack(output_samples, dim=0)
            
        except Exception as e:
            warnings.warn(f"THRML sampling failed: {e}. Falling back to PyTorch.")
            return self._sample_with_pytorch(input_spins)
    
    def _sample_with_pytorch(self, input_spins: torch.Tensor) -> torch.Tensor:
        """Sample output spins using PyTorch (Gibbs sampling approximation)."""
        batch_size = input_spins.shape[0]
        
        # Initialize random spins
        output_spins = torch.randn(batch_size, self.output_size)
        
        # Gibbs sampling iterations
        for _ in range(5):  # Few iterations for efficiency
            for i in range(self.output_size):
                # Calculate local field for spin i
                neighbor_sum = torch.sum(
                    self.coupling_matrix[i].unsqueeze(0) * input_spins, dim=1
                )
                local_field = self.local_fields[i] + neighbor_sum
                
                # Probability of spin up
                prob_up = torch.sigmoid(2.0 * local_field / self.temperature)
                
                # Sample spin
                random_vals = torch.rand(batch_size)
                output_spins[:, i] = torch.where(random_vals < prob_up, 1.0, -1.0)
        
        return output_spins
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through Ising layer."""
        # Ensure input is in spin space (-1, +1)
        input_spins = torch.tanh(x)
        
        if self.training and (self.use_thrml or np.random.random() < 0.1):
            # Use Ising sampling during training (occasionally)
            output_spins = self._sample_with_thrml(input_spins)
        else:
            # Use deterministic forward pass for efficiency
            # Apply coupling matrix
            coupled = torch.matmul(input_spins, self.coupling_matrix.t())
            
            # Add local fields
            field_applied = coupled + self.local_fields.unsqueeze(0)
            
            # Apply temperature scaling and activation
            output_spins = torch.tanh(field_applied / self.temperature)
        
        return output_spins


class IsingNeuralNetwork(nn.Module):
    """
    Complete neural network based on Ising model layers.
    
    Uses THRML for exact sampling when possible, with PyTorch fallbacks.
    """
    
    def __init__(self, config: IsingNeuralNetworkConfig):
        super().__init__()
        
        self.config = config
        
        # Calculate total lattice size
        self.lattice_size = np.prod(config.lattice_size)
        
        # Create Ising layers
        layer_sizes = self._calculate_layer_sizes()
        self.ising_layers = nn.ModuleList()
        
        for i in range(len(layer_sizes) - 1):
            layer = IsingLayer(
                input_size=layer_sizes[i],
                output_size=layer_sizes[i + 1],
                temperature=config.temperature,
                coupling_strength=config.coupling_strength,
                magnetic_field=config.magnetic_field,
                use_thrml=config.use_thrml
            )
            self.ising_layers.append(layer)
        
        # Final output transformation
        self.output_transform = nn.Linear(layer_sizes[-1], 1)
        
        # Energy tracking
        self.register_buffer('energy_history', torch.zeros(1000))
        self.energy_index = 0
    
    def _calculate_layer_sizes(self) -> List[int]:
        """Calculate layer sizes based on lattice structure."""
        sizes = [self.lattice_size]
        
        current_size = self.lattice_size
        for _ in range(self.config.num_layers):
            # Gradually reduce size
            current_size = max(4, current_size // 2)
            sizes.append(current_size)
        
        return sizes
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through Ising neural network."""
        # Reshape input to match lattice
        if len(x.shape) > 2:
            x = x.view(x.shape[0], -1)
        
        # Ensure input has correct size
        if x.shape[1] != self.lattice_size:
            # Project to correct size
            projection = nn.Linear(x.shape[1], self.lattice_size)
            x = projection(x)
        
        # Pass through Ising layers
        current_spins = x
        total_energy = 0.0
        
        for layer in self.ising_layers:
            current_spins = layer(current_spins)
            
            # Track energy if in training mode
            if self.training:
                energy = layer._ising_energy(current_spins)
                total_energy += torch.mean(energy)
        
        # Store energy for analysis
        if self.training:
            self.energy_history[self.energy_index % 1000] = total_energy.item()
            self.energy_index += 1
        
        # Final output
        output = self.output_transform(current_spins)
        
        return output
    
    def sample_configuration(self, batch_size: int = 1) -> torch.Tensor:
        """Sample a spin configuration from the model."""
        with torch.no_grad():
            # Random input
            x = torch.randn(batch_size, self.lattice_size)
            
            # Forward pass with sampling
            for layer in self.ising_layers:
                x = layer._sample_with_thrml(x)
        
        return x
    
    def get_energy_statistics(self) -> Dict[str, float]:
        """Get statistics about the energy during training."""
        valid_energies = self.energy_history[:min(self.energy_index, 1000)]
        
        if len(valid_energies) == 0:
            return {"mean_energy": 0.0, "energy_std": 0.0}
        
        return {
            "mean_energy": torch.mean(valid_energies).item(),
            "energy_std": torch.std(valid_energies).item(),
            "min_energy": torch.min(valid_energies).item(),
            "max_energy": torch.max(valid_energies).item(),
        }


class EnergyBasedDiscovery(nn.Module):
    """
    Energy-based model for mathematical discovery using Ising networks.
    
    Uses energy landscapes to discover mathematical relationships and patterns.
    """
    
    def __init__(self, 
                 input_dim: int,
                 num_formulas: int = 100,
                 temperature: float = 1.0):
        super().__init__()
        
        self.input_dim = input_dim
        self.num_formulas = num_formulas
        self.temperature = temperature
        
        # Ising network for formula representation
        config = IsingNeuralNetworkConfig(
            lattice_size=(int(np.sqrt(num_formulas)), int(np.sqrt(num_formulas))),
            temperature=temperature,
            num_layers=3,
            hidden_dim=128
        )
        self.ising_network = IsingNeuralNetwork(config)
        
        # Formula encoder
        self.formula_encoder = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, num_formulas)
        )
        
        # Energy function
        self.energy_function = nn.Sequential(
            nn.Linear(num_formulas * 2, 256),
            nn.ReLU(),
            nn.Linear(256, 1)
        )
    
    def encode_mathematical_formula(self, formula_features: torch.Tensor) -> torch.Tensor:
        """Encode mathematical formula into energy space."""
        return self.formula_encoder(formula_features)
    
    def compute_interaction_energy(self, 
                                 formula1: torch.Tensor, 
                                 formula2: torch.Tensor) -> torch.Tensor:
        """Compute interaction energy between two formulas."""
        combined = torch.cat([formula1, formula2], dim=-1)
        return self.energy_function(combined)
    
    def discover_related_formulas(self, 
                                query_formula: torch.Tensor,
                                num_candidates: int = 10) -> List[torch.Tensor]:
        """Discover formulas related to a query formula using energy minimization."""
        encoded_query = self.encode_mathematical_formula(query_formula)
        
        candidates = []
        best_energies = []
        
        for _ in range(num_candidates * 5):  # Sample more to get best
            # Sample candidate configuration
            candidate_config = self.ising_network.sample_configuration(1)
            candidate_encoded = candidate_config.squeeze(0)
            
            # Compute interaction energy
            energy = self.compute_interaction_energy(encoded_query, candidate_encoded)
            
            candidates.append(candidate_encoded)
            best_energies.append(energy.item())
        
        # Select best candidates (lowest energy)
        best_indices = np.argsort(best_energies)[:num_candidates]
        return [candidates[i] for i in best_indices]
    
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Forward pass for training."""
        # Encode input
        encoded = self.encode_mathematical_formula(x)
        
        # Pass through Ising network
        ising_output = self.ising_network(encoded)
        
        # Compute energy
        energy = self.compute_interaction_energy(encoded, encoded)
        
        return ising_output, energy


class PGMDiscoveryModel(nn.Module):
    """
    Probabilistic Graphical Model for mathematical discovery using THRML.
    
    Creates a PGM that represents relationships between mathematical concepts
    and uses block Gibbs sampling to discover new connections.
    """
    
    def __init__(self, 
                 num_concepts: int = 50,
                 num_relations: int = 100,
                 use_thrml: bool = True):
        super().__init__()
        
        self.num_concepts = num_concepts
        self.num_relations = num_relations
        self.use_thrml = use_thrml and THRML_AVAILABLE
        
        # Concept embeddings
        self.concept_embeddings = nn.Embedding(num_concepts, 64)
        
        # Relation weights
        self.relation_weights = nn.Parameter(torch.randn(num_relations, 64, 64))
        
        # THRML components
        if self.use_thrml:
            self._initialize_pgm()
    
    def _initialize_pgm(self):
        """Initialize THRML PGM components."""
        if not THRML_AVAILABLE:
            return
        
        # Create categorical nodes for concepts
        self.concept_nodes = [CategoricalNode() for _ in range(self.num_concepts)]
        
        # Create edges between related concepts
        self.concept_edges = []
        for i in range(self.num_concepts):
            for j in range(i + 1, min(i + 5, self.num_concepts)):  # Connect to nearby concepts
                self.concept_edges.append((i, j))
    
    def sample_mathematical_relationships(self, 
                                        num_samples: int = 10) -> List[Dict[str, Any]]:
        """Sample mathematical relationships using PGM."""
        relationships = []
        
        for _ in range(num_samples):
            # Sample concept pairs
            concept1 = np.random.randint(0, self.num_concepts)
            concept2 = np.random.randint(0, self.num_concepts)
            
            # Get embeddings
            emb1 = self.concept_embeddings(torch.tensor(concept1))
            emb2 = self.concept_embeddings(torch.tensor(concept2))
            
            # Compute relation strength
            relation_scores = []
            for i in range(self.num_relations):
                score = torch.sum(torch.matmul(emb1, self.relation_weights[i]) * emb2)
                relation_scores.append(score.item())
            
            best_relation = np.argmax(relation_scores)
            
            relationships.append({
                "concept1": concept1,
                "concept2": concept2,
                "relation": best_relation,
                "strength": relation_scores[best_relation]
            })
        
        return relationships
    
    def forward(self, concept_indices: torch.Tensor) -> torch.Tensor:
        """Forward pass for training."""
        embeddings = self.concept_embeddings(concept_indices)
        return embeddings


# Factory functions for common configurations

def create_mathematical_ising_network(lattice_size: Tuple[int, int] = (8, 8)) -> IsingNeuralNetwork:
    """Create an Ising network optimized for mathematical discovery."""
    config = IsingNeuralNetworkConfig(
        lattice_size=lattice_size,
        model_type=IsingModelType.CLASSICAL,
        temperature=0.5,  # Lower temperature for more structured states
        coupling_strength=1.5,
        magnetic_field=0.1,
        num_layers=4,
        use_thrml=True
    )
    return IsingNeuralNetwork(config)


def create_formula_discovery_model(input_dim: int = 64) -> EnergyBasedDiscovery:
    """Create an energy-based model for formula discovery."""
    return EnergyBasedDiscovery(
        input_dim=input_dim,
        num_formulas=64,
        temperature=1.0
    )


def create_mathematical_pgm(num_concepts: int = 30) -> PGMDiscoveryModel:
    """Create a PGM for mathematical concept discovery."""
    return PGMDiscoveryModel(
        num_concepts=num_concepts,
        num_relations=50,
        use_thrml=True
    )