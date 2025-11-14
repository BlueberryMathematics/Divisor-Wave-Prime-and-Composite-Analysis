"""
Neural Network Tools for LlamaIndex Agents
==========================================

Tool wrappers that allow LlamaIndex agents to use divisor-wave neural networks
as specialized mathematical reasoning and discovery tools.
"""

from typing import Dict, Any, List, Optional, Union
import torch
import numpy as np
from llama_index.core.tools import FunctionTool
from llama_index.core.tools.types import ToolMetadata
import json
import random

# Import neural network components
from ..architectures.tetrahedral_networks import TetrahedralNetwork
from ..embeddings.crystal_embeddings import CrystalEmbedding, create_icosahedral_embedding
from ..discovery.deep_discovery import DeepMathematicalDiscovery
from ..thrml_integration.ising_networks import IsingNeuralNetwork
from ..construction.architecture_builder import ArchitectureBuilder


class NeuralNetworkToolWrapper:
    """Base class for wrapping neural networks as LlamaIndex tools."""
    
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    def load_model(self):
        """Load the neural network model."""
        if self.model_path and self.model is None:
            checkpoint = torch.load(self.model_path, map_location=self.device)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.model.eval()
    
    def to_tool_result(self, result: Any) -> str:
        """Convert neural network output to text for agent."""
        if isinstance(result, torch.Tensor):
            return f"Neural network result: {result.cpu().numpy().tolist()}"
        elif isinstance(result, dict):
            return f"Analysis results: {json.dumps(result, indent=2)}"
        else:
            return str(result)


class TetrahedralAnalysisTool(NeuralNetworkToolWrapper):
    """Tool for analyzing tetrahedral number patterns."""
    
    def __init__(self, model_path: Optional[str] = None):
        super().__init__(model_path)
        self.model = TetrahedralNetwork(input_dim=50, hidden_dim=256, output_dim=10)
        if model_path:
            self.load_model()
    
    def analyze_sequence(self, sequence: List[float], context: str = "") -> str:
        """
        Analyze a mathematical sequence for tetrahedral patterns.
        
        Args:
            sequence: List of numbers to analyze
            context: Additional context about the sequence
            
        Returns:
            Analysis of tetrahedral patterns found
        """
        # Convert to tensor
        tensor_seq = torch.tensor(sequence, dtype=torch.float32).unsqueeze(0)
        
        with torch.no_grad():
            if self.model:
                self.model.eval()
                result = self.model(tensor_seq)
                analysis = {
                    "tetrahedral_coefficients": result.cpu().numpy().tolist(),
                    "dominant_patterns": self._identify_patterns(result),
                    "sequence_length": len(sequence),
                    "context": context
                }
            else:
                # Fallback analysis without trained model
                analysis = self._basic_tetrahedral_analysis(sequence)
        
        return self.to_tool_result(analysis)
    
    def _identify_patterns(self, result: torch.Tensor) -> List[str]:
        """Identify dominant patterns in the tetrahedral analysis."""
        patterns = []
        coeffs = result.squeeze().cpu().numpy()
        
        # Find dominant coefficients
        dominant_indices = np.argsort(np.abs(coeffs))[-3:][::-1]
        
        for idx in dominant_indices:
            if abs(coeffs[idx]) > 0.1:  # Threshold for significance
                patterns.append(f"Tetrahedral component {idx}: {coeffs[idx]:.4f}")
        
        return patterns
    
    def _basic_tetrahedral_analysis(self, sequence: List[float]) -> Dict[str, Any]:
        """Basic tetrahedral analysis without neural network."""
        # Check if sequence follows tetrahedral number pattern
        tetrahedral_nums = [n * (n + 1) * (n + 2) // 6 for n in range(1, len(sequence) + 1)]
        
        # Compute correlation
        if len(sequence) > 1:
            correlation = np.corrcoef(sequence, tetrahedral_nums[:len(sequence)])[0, 1]
        else:
            correlation = 0.0
        
        return {
            "tetrahedral_correlation": correlation,
            "likely_tetrahedral": correlation > 0.8,
            "analysis_type": "basic"
        }


class CrystalSymmetryTool(NeuralNetworkToolWrapper):
    """Tool for analyzing mathematical objects using crystal symmetry."""
    
    def __init__(self, embedding_dim: int = 512):
        super().__init__()
        self.model = create_icosahedral_embedding(embedding_dim)
    
    def analyze_symmetry(self, data: List[float], object_type: str = "sequence") -> str:
        """
        Analyze the symmetry properties of a mathematical object.
        
        Args:
            data: Mathematical object as list of numbers
            object_type: Type of object (sequence, matrix, function_values, etc.)
            
        Returns:
            Symmetry analysis results
        """
        # Convert to tensor and prepare for embedding
        tensor_data = torch.tensor(data, dtype=torch.float32).unsqueeze(0)
        
        # Pad or truncate to model's expected input size
        if tensor_data.shape[1] < self.model.config.embedding_dim:
            padding = torch.zeros(1, self.model.config.embedding_dim - tensor_data.shape[1])
            tensor_data = torch.cat([tensor_data, padding], dim=1)
        else:
            tensor_data = tensor_data[:, :self.model.config.embedding_dim]
        
        tensor_data = tensor_data.unsqueeze(1)  # Add sequence dimension
        
        with torch.no_grad():
            embeddings = self.model(tensor_data)
            crystal_info = self.model.get_crystal_structure_info()
            
            analysis = {
                "embedding_shape": list(embeddings.shape),
                "crystal_lattice": crystal_info["lattice_type"],
                "symmetry_detected": self._detect_symmetries(embeddings),
                "object_type": object_type,
                "lattice_properties": crystal_info
            }
        
        return self.to_tool_result(analysis)
    
    def _detect_symmetries(self, embeddings: torch.Tensor) -> List[str]:
        """Detect symmetries in the crystal embeddings."""
        symmetries = []
        
        # Analyze embedding patterns
        emb = embeddings.squeeze().cpu().numpy()
        
        # Check for rotational symmetry patterns
        if self._has_rotational_symmetry(emb):
            symmetries.append("rotational_symmetry")
        
        # Check for reflection symmetry
        if self._has_reflection_symmetry(emb):
            symmetries.append("reflection_symmetry")
        
        # Check for icosahedral patterns
        if self._has_icosahedral_patterns(emb):
            symmetries.append("icosahedral_structure")
        
        return symmetries
    
    def _has_rotational_symmetry(self, embedding: np.ndarray) -> bool:
        """Check for rotational symmetry patterns."""
        # Simplified check - full implementation would be more sophisticated
        return np.std(embedding) < np.mean(np.abs(embedding)) * 0.5
    
    def _has_reflection_symmetry(self, embedding: np.ndarray) -> bool:
        """Check for reflection symmetry."""
        mid = len(embedding) // 2
        first_half = embedding[:mid]
        second_half = embedding[mid:mid+len(first_half)][::-1]
        
        if len(first_half) == len(second_half):
            correlation = np.corrcoef(first_half, second_half)[0, 1]
            return not np.isnan(correlation) and correlation > 0.7
        return False
    
    def _has_icosahedral_patterns(self, embedding: np.ndarray) -> bool:
        """Check for icosahedral patterns (20-fold structure)."""
        if len(embedding) < 20:
            return False
        
        # Check if embedding can be divided into 20 similar parts
        chunk_size = len(embedding) // 20
        chunks = [embedding[i*chunk_size:(i+1)*chunk_size] for i in range(20)]
        
        # Compute similarity between chunks
        similarities = []
        for i in range(len(chunks)-1):
            if len(chunks[i]) == len(chunks[i+1]):
                corr = np.corrcoef(chunks[i], chunks[i+1])[0, 1]
                if not np.isnan(corr):
                    similarities.append(corr)
        
        return len(similarities) > 0 and np.mean(similarities) > 0.6


class MathematicalDiscoveryTool(NeuralNetworkToolWrapper):
    """Tool for discovering new mathematical patterns and relationships."""
    
    def __init__(self):
        super().__init__()
        self.model = DeepMathematicalDiscovery(
            input_dim=64,
            hidden_dim=256,
            output_dim=32
        )
    
    def discover_patterns(self, 
                         data: List[float], 
                         search_type: str = "infinite_products",
                         max_iterations: int = 100) -> str:
        """
        Discover mathematical patterns in the given data.
        
        Args:
            data: Mathematical data to analyze
            search_type: Type of patterns to search for
            max_iterations: Maximum iterations for discovery
            
        Returns:
            Discovered patterns and relationships
        """
        tensor_data = torch.tensor(data, dtype=torch.float32).unsqueeze(0)
        
        with torch.no_grad():
            if search_type == "infinite_products":
                discoveries = self.model.discover_infinite_products(tensor_data, max_iterations)
            elif search_type == "pole_zero":
                discoveries = self.model.detect_poles_and_zeros(tensor_data)
            else:
                discoveries = self.model.general_pattern_discovery(tensor_data)
            
            analysis = {
                "search_type": search_type,
                "discoveries": discoveries,
                "data_length": len(data),
                "iterations_used": max_iterations
            }
        
        return self.to_tool_result(analysis)


class LaTeXExpressionGANTool(NeuralNetworkToolWrapper):
    """Tool for generating new LaTeX mathematical expressions using GANs."""
    
    def __init__(self, projects_root: str = "../../../"):
        super().__init__()
        try:
            from ..architectures.latex_expression_gan import create_latex_gan_from_projects
            self.model, self.training_data = create_latex_gan_from_projects(projects_root)
            self.gan_ready = True
        except Exception as e:
            print(f"LaTeX GAN initialization failed: {e}")
            self.gan_ready = False
    
    def generate_latex_expressions(self, 
                                 num_expressions: int = 5,
                                 expression_type: str = "general",
                                 temperature: float = 1.0,
                                 seed_expression: str = "") -> str:
        """
        Generate new LaTeX mathematical expressions using GANs trained on divisor-wave JSON data.
        
        Args:
            num_expressions: Number of LaTeX expressions to generate
            expression_type: Type of expressions (general, sum, product, integral)
            temperature: Creativity level (higher = more creative, lower = more conservative)
            seed_expression: Optional seed LaTeX to start generation from
            
        Returns:
            Generated LaTeX mathematical expressions with analysis
        """
        if not self.gan_ready:
            return "LaTeX GAN not available. Using template-based generation."
        
        try:
            # Generate expressions
            if seed_expression:
                expressions = []
                for _ in range(num_expressions):
                    expr = self.model.generator.generate_latex(
                        temperature=temperature,
                        seed_text=seed_expression
                    )
                    expressions.append(expr)
            else:
                expressions = self.model.generate_new_latex_expressions(
                    num_expressions=num_expressions,
                    temperature=temperature
                )
            
            # Filter by expression type if specified
            if expression_type != "general":
                expressions = self._filter_by_type(expressions, expression_type)
            
            analysis = {
                "generated_expressions": expressions,
                "expression_type": expression_type,
                "temperature": temperature,
                "seed_used": seed_expression if seed_expression else "none",
                "training_data_size": len(self.training_data),
                "latex_analysis": self._analyze_latex_expressions(expressions),
                "mathematical_validity": self._validate_latex_expressions(expressions)
            }
            
        except Exception as e:
            analysis = {
                "error": f"Generation failed: {e}",
                "fallback_expressions": self._generate_fallback_expressions(num_expressions, expression_type)
            }
        
        return self.to_tool_result(analysis)
    
    def _filter_by_type(self, expressions: List[str], expr_type: str) -> List[str]:
        """Filter expressions by mathematical type."""
        filtered = []
        
        for expr in expressions:
            if expr_type == "sum" and ("\\sum" in expr or "+" in expr):
                filtered.append(expr)
            elif expr_type == "product" and ("\\prod" in expr or "\\cdot" in expr):
                filtered.append(expr)
            elif expr_type == "integral" and "\\int" in expr:
                filtered.append(expr)
            elif expr_type == "general":
                filtered.append(expr)
        
        return filtered[:5]  # Limit to 5 expressions
    
    def _analyze_latex_expressions(self, expressions: List[str]) -> Dict[str, Any]:
        """Analyze the mathematical content of generated expressions."""
        analysis = {
            "total_expressions": len(expressions),
            "average_length": np.mean([len(expr) for expr in expressions]) if expressions else 0,
            "contains_sum": sum(1 for expr in expressions if "\\sum" in expr),
            "contains_product": sum(1 for expr in expressions if "\\prod" in expr),
            "contains_integral": sum(1 for expr in expressions if "\\int" in expr),
            "contains_fraction": sum(1 for expr in expressions if "\\frac" in expr),
            "contains_infinity": sum(1 for expr in expressions if "\\infty" in expr),
            "complexity_score": self._calculate_complexity_score(expressions)
        }
        
        return analysis
    
    def _calculate_complexity_score(self, expressions: List[str]) -> float:
        """Calculate complexity score for LaTeX expressions."""
        if not expressions:
            return 0.0
        
        total_score = 0
        for expr in expressions:
            score = 0
            score += expr.count('\\') * 2  # LaTeX commands
            score += expr.count('{') * 1   # Braced expressions
            score += expr.count('^') * 1   # Superscripts
            score += expr.count('_') * 1   # Subscripts
            score += len(expr) * 0.1       # Base length
            total_score += score
        
        return total_score / len(expressions)
    
    def _validate_latex_expressions(self, expressions: List[str]) -> Dict[str, Any]:
        """Validate LaTeX expressions for basic correctness."""
        validation = {
            "all_non_empty": all(expr.strip() for expr in expressions),
            "balanced_braces": all(expr.count('{') == expr.count('}') for expr in expressions),
            "has_latex_commands": all('\\' in expr for expr in expressions),
            "reasonable_length": all(10 <= len(expr) <= 500 for expr in expressions),
        }
        
        validation["overall_valid"] = all(validation.values())
        return validation
    
    def _generate_fallback_expressions(self, num_expressions: int, expr_type: str) -> List[str]:
        """Generate fallback expressions if GAN fails."""
        templates = {
            "sum": [
                r"\sum_{n=1}^{\infty} \frac{1}{n^2}",
                r"\sum_{k=0}^{n} \binom{n}{k} x^k",
                r"\sum_{i=1}^{n} i = \frac{n(n+1)}{2}"
            ],
            "product": [
                r"\prod_{p \text{ prime}} \left(1 - \frac{1}{p}\right)",
                r"\prod_{n=1}^{\infty} \left(1 + x^n\right)",
                r"\prod_{k=1}^{n} k = n!"
            ],
            "integral": [
                r"\int_{0}^{1} x^n dx = \frac{1}{n+1}",
                r"\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}",
                r"\int_{0}^{\pi} \sin(x) dx = 2"
            ],
            "general": [
                r"e^{i\pi} + 1 = 0",
                r"\zeta(2) = \frac{\pi^2}{6}",
                r"\lim_{n \to \infty} \left(1 + \frac{1}{n}\right)^n = e"
            ]
        }
        
        template_list = templates.get(expr_type, templates["general"])
        return random.sample(template_list, min(num_expressions, len(template_list)))


class MathematicalGANTool(NeuralNetworkToolWrapper):
    """Tool for generating mathematical sequences and patterns using GANs."""
    
    def __init__(self, gan_type: str = "sequence"):
        super().__init__()
        # Import here to avoid circular imports
        from ..architectures.mathematical_gans import (
            create_sequence_gan, create_riemann_gan, create_prime_gan
        )
        
        if gan_type == "sequence":
            self.model = create_sequence_gan()
        elif gan_type == "riemann":
            self.model = create_riemann_gan()
        elif gan_type == "prime":
            self.model = create_prime_gan()
        else:
            self.model = create_sequence_gan()
        
        self.gan_type = gan_type
    
    def generate_mathematical_sequences(self, 
                                      num_sequences: int = 5,
                                      sequence_type: str = "general",
                                      seed: Optional[int] = None) -> str:
        """
        Generate new mathematical sequences using GANs.
        
        Args:
            num_sequences: Number of sequences to generate
            sequence_type: Type of sequences (general, riemann, prime)
            seed: Random seed for reproducible generation
            
        Returns:
            Generated mathematical sequences and analysis
        """
        with torch.no_grad():
            generated_sequences = self.model.generate_mathematical_sequences(
                num_sequences=num_sequences, 
                seed=seed
            )
            
            # Analyze generated sequences
            analysis = {
                "generated_sequences": generated_sequences.cpu().numpy().tolist(),
                "gan_type": self.gan_type,
                "sequence_type": sequence_type,
                "num_generated": num_sequences,
                "sequence_properties": self._analyze_generated_sequences(generated_sequences),
                "mathematical_validity": self._check_mathematical_validity(generated_sequences)
            }
        
        return self.to_tool_result(analysis)
    
    def _analyze_generated_sequences(self, sequences: torch.Tensor) -> Dict[str, Any]:
        """Analyze properties of generated sequences."""
        sequences_np = sequences.cpu().numpy()
        
        properties = {
            "mean_values": np.mean(sequences_np, axis=1).tolist(),
            "growth_rates": [],
            "monotonic_sequences": 0,
            "convergent_sequences": 0
        }
        
        for seq in sequences_np:
            # Growth rate analysis
            if len(seq) > 1:
                growth_rate = np.mean(seq[1:] - seq[:-1])
                properties["growth_rates"].append(growth_rate)
                
                # Check monotonicity
                if np.all(seq[1:] >= seq[:-1]):
                    properties["monotonic_sequences"] += 1
                
                # Check convergence (simplified)
                if abs(growth_rate) < 0.01:
                    properties["convergent_sequences"] += 1
        
        return properties
    
    def _check_mathematical_validity(self, sequences: torch.Tensor) -> Dict[str, Any]:
        """Check mathematical validity of generated sequences."""
        validity = {
            "all_finite": torch.all(torch.isfinite(sequences)).item(),
            "no_nans": not torch.any(torch.isnan(sequences)).item(),
            "reasonable_range": torch.all(torch.abs(sequences) < 1e6).item(),
            "non_trivial": not torch.all(sequences == 0).item()
        }
        
        validity["overall_valid"] = all(validity.values())
        return validity


class IsingModelTool(NeuralNetworkToolWrapper):
    """Tool for modeling mathematical problems as Ising systems."""
    
    def __init__(self, lattice_size: int = 16):
        super().__init__()
        self.model = IsingNeuralNetwork(lattice_size=lattice_size, hidden_dim=128)
    
    def model_as_ising_system(self, 
                             problem_data: List[float], 
                             temperature: float = 2.269) -> str:
        """
        Model a mathematical problem as an Ising system.
        
        Args:
            problem_data: Mathematical problem data
            temperature: System temperature
            
        Returns:
            Ising system analysis
        """
        # Convert problem to Ising system representation
        lattice_input = self._prepare_ising_input(problem_data)
        
        with torch.no_grad():
            ising_output = self.model(lattice_input, temperature)
            energy = self.model.compute_energy(lattice_input)
            
            analysis = {
                "ising_state": ising_output.cpu().numpy().tolist(),
                "system_energy": energy.item(),
                "temperature": temperature,
                "critical_behavior": self._analyze_criticality(energy, temperature),
                "phase": self._determine_phase(temperature)
            }
        
        return self.to_tool_result(analysis)
    
    def _prepare_ising_input(self, data: List[float]) -> torch.Tensor:
        """Convert problem data to Ising lattice representation."""
        lattice_size = int(np.sqrt(len(data))) if len(data) > 0 else 4
        
        # Reshape data to lattice
        if len(data) >= lattice_size * lattice_size:
            lattice = np.array(data[:lattice_size*lattice_size]).reshape(lattice_size, lattice_size)
        else:
            lattice = np.zeros((lattice_size, lattice_size))
            lattice.flat[:len(data)] = data
        
        # Normalize to [-1, 1] for spins
        lattice = 2 * (lattice - lattice.min()) / (lattice.max() - lattice.min() + 1e-8) - 1
        
        return torch.tensor(lattice, dtype=torch.float32).unsqueeze(0)
    
    def _analyze_criticality(self, energy: torch.Tensor, temperature: float) -> str:
        """Analyze if system is near critical point."""
        critical_temp = 2.269  # 2D Ising critical temperature
        
        if abs(temperature - critical_temp) < 0.1:
            return "near_critical"
        elif temperature > critical_temp:
            return "paramagnetic_phase"
        else:
            return "ferromagnetic_phase"
    
    def _determine_phase(self, temperature: float) -> str:
        """Determine the phase of the Ising system."""
        critical_temp = 2.269
        
        if temperature < critical_temp:
            return "ordered"
        else:
            return "disordered"


def create_neural_network_tools() -> List[FunctionTool]:
    """Create all neural network tools for LlamaIndex agents."""
    
    # Initialize tool wrappers
    tetrahedral_tool = TetrahedralAnalysisTool()
    crystal_tool = CrystalSymmetryTool()
    discovery_tool = MathematicalDiscoveryTool()
    latex_gan_tool = LaTeXExpressionGANTool()
    gan_tool = MathematicalGANTool()
    ising_tool = IsingModelTool()
    
    # Create LlamaIndex FunctionTools
    tools = [
        FunctionTool.from_defaults(
            fn=tetrahedral_tool.analyze_sequence,
            name="analyze_tetrahedral_patterns",
            description="Analyze mathematical sequences for tetrahedral number patterns and relationships."
        ),
        
        FunctionTool.from_defaults(
            fn=crystal_tool.analyze_symmetry,
            name="analyze_crystal_symmetry",
            description="Analyze mathematical objects using crystal lattice symmetries and geometric embeddings."
        ),
        
        FunctionTool.from_defaults(
            fn=discovery_tool.discover_patterns,
            name="discover_mathematical_patterns",
            description="Discover new mathematical patterns, infinite products, and relationships in data."
        ),
        
        FunctionTool.from_defaults(
            fn=latex_gan_tool.generate_latex_expressions,
            name="generate_latex_expressions",
            description="Generate new LaTeX mathematical expressions using GANs trained on divisor-wave project data."
        ),
        
        FunctionTool.from_defaults(
            fn=gan_tool.generate_mathematical_sequences,
            name="generate_mathematical_sequences",
            description="Generate new mathematical sequences and patterns using Generative Adversarial Networks."
        ),
        
        FunctionTool.from_defaults(
            fn=ising_tool.model_as_ising_system,
            name="model_ising_system",
            description="Model mathematical problems as Ising spin systems using statistical physics."
        ),
    ]
    
    return tools


# Example usage for LlamaIndex agent integration
def create_mathematical_agent_with_neural_tools():
    """Create a LlamaIndex agent with neural network tools."""
    from llama_index.core.agent import ReActAgent
    from llama_index.llms.openai import OpenAI
    
    # Get neural network tools
    neural_tools = create_neural_network_tools()
    
    # Create agent with tools
    llm = OpenAI(model="gpt-4")
    agent = ReActAgent.from_tools(
        neural_tools,
        llm=llm,
        verbose=True,
        system_message="""You are a mathematical research assistant with access to specialized neural networks.
        
        You can:
        - Analyze sequences for tetrahedral patterns
        - Detect crystal symmetries in mathematical objects  
        - Discover new mathematical relationships
        - Model problems as Ising systems
        
        Use these tools to help users with advanced mathematical analysis and discovery.
        Always explain your reasoning and the mathematical significance of the results."""
    )
    
    return agent