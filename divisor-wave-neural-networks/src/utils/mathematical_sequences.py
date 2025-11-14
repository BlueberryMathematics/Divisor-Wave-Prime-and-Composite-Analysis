"""
Mathematical Sequences Generator
===============================

Comprehensive collection of mathematical sequences used throughout the neural networks,
including tetrahedral numbers, geometric series, prime-related sequences, and OEIS sequences.

Based on Leo J. Borcherding's research on tetrahedral families and divisor waves.
"""

import numpy as np
import torch
from typing import List, Dict, Tuple, Optional, Union, Callable
from sympy import primefactorization, prime, isprime, nextprime
import math
from dataclasses import dataclass
from enum import Enum


class SequenceType(Enum):
    """Types of mathematical sequences available."""
    TETRAHEDRAL = "tetrahedral"
    TRIANGULAR = "triangular"
    SQUARE = "square"
    PENTAGONAL = "pentagonal"
    GEOMETRIC = "geometric"
    FIBONACCI = "fibonacci"
    PRIME = "prime"
    COMPOSITE = "composite"
    DIVISOR_WAVE = "divisor_wave"
    OEIS_A287324 = "A287324"  # The sequence from user's example
    RIEMANN_ZEROS = "riemann_zeros"
    CUSTOM = "custom"


@dataclass
class SequenceProperties:
    """Properties and metadata for a mathematical sequence."""
    name: str
    sequence_type: SequenceType
    description: str
    formula: str
    oeis_id: Optional[str] = None
    generating_function: Optional[str] = None
    recurrence_relation: Optional[str] = None
    asymptotic_behavior: Optional[str] = None
    mathematical_significance: Optional[str] = None


class MathematicalSequences:
    """
    Generator for various mathematical sequences used in neural network architectures.
    
    This class provides methods to generate sequences that form the basis for:
    - Network layer sizes
    - Embedding dimensions
    - Training schedules
    - Mathematical discovery patterns
    """
    
    def __init__(self, device: str = "cpu"):
        self.device = device
        self._sequence_cache = {}
        self._initialize_sequence_properties()
    
    def _initialize_sequence_properties(self):
        """Initialize metadata for all supported sequences."""
        self.sequence_properties = {
            SequenceType.TETRAHEDRAL: SequenceProperties(
                name="Tetrahedral Numbers",
                sequence_type=SequenceType.TETRAHEDRAL,
                description="Tetrahedral numbers: T_n = n(n+1)(n+2)/6",
                formula="T_n = n(n+1)(n+2)/6",
                oeis_id="A000292",
                generating_function="x/(1-x)^4",
                mathematical_significance="3D analog of triangular numbers, fundamental to Borcherding's research"
            ),
            
            SequenceType.TRIANGULAR: SequenceProperties(
                name="Triangular Numbers", 
                sequence_type=SequenceType.TRIANGULAR,
                description="Triangular numbers: T_n = n(n+1)/2",
                formula="T_n = n(n+1)/2",
                oeis_id="A000217",
                generating_function="x/(1-x)^3"
            ),
            
            SequenceType.OEIS_A287324: SequenceProperties(
                name="A287324 Sequence",
                sequence_type=SequenceType.OEIS_A287324,
                description="Leo Borcherding's tetrahedral family sequence: f(9,n)",
                formula="a(n) = A008412(n-1) + A008412(n-2) for n>1",
                oeis_id="A287324",
                mathematical_significance="Part of unified tetrahedral family defined by Pascal's triangle"
            ),
            
            # Add more sequence properties...
        }
    
    def tetrahedral_numbers(self, n: int, start: int = 1) -> torch.Tensor:
        """
        Generate tetrahedral numbers: T_n = n(n+1)(n+2)/6
        
        Args:
            n: Number of terms to generate
            start: Starting index (default 1)
        
        Returns:
            Tensor of tetrahedral numbers
        """
        indices = torch.arange(start, start + n, device=self.device)
        return indices * (indices + 1) * (indices + 2) // 6
    
    def triangular_numbers(self, n: int, start: int = 1) -> torch.Tensor:
        """Generate triangular numbers: T_n = n(n+1)/2"""
        indices = torch.arange(start, start + n, device=self.device)
        return indices * (indices + 1) // 2
    
    def geometric_series(self, n: int, ratio: float = 2.0, start: float = 1.0) -> torch.Tensor:
        """Generate geometric series: a * r^n"""
        indices = torch.arange(n, device=self.device)
        return start * (ratio ** indices)
    
    def fibonacci_sequence(self, n: int) -> torch.Tensor:
        """Generate Fibonacci sequence."""
        if n <= 0:
            return torch.tensor([], device=self.device)
        elif n == 1:
            return torch.tensor([1], device=self.device)
        elif n == 2:
            return torch.tensor([1, 1], device=self.device)
        
        fib = torch.zeros(n, device=self.device)
        fib[0] = 1
        fib[1] = 1
        
        for i in range(2, n):
            fib[i] = fib[i-1] + fib[i-2]
        
        return fib
    
    def prime_sequence(self, n: int) -> torch.Tensor:
        """Generate first n prime numbers."""
        primes = []
        num = 2
        while len(primes) < n:
            if isprime(num):
                primes.append(num)
            num += 1
        return torch.tensor(primes, device=self.device)
    
    def a287324_sequence(self, n: int) -> torch.Tensor:
        """
        Generate OEIS A287324 sequence - Leo Borcherding's tetrahedral family.
        
        The sequence starts: 0, 1, 9, 40, 120, 280, 552, 968, 1560, 2360, ...
        Formula: a(n) = A008412(n-1) + A008412(n-2) for n>1, a(0)=0, a(1)=1
        """
        if n <= 0:
            return torch.tensor([], device=self.device)
        
        # Pre-computed first few terms for accuracy
        initial_terms = [0, 1, 9, 40, 120, 280, 552, 968, 1560, 2360, 
                        3400, 4712, 6328, 8280, 10600, 13320, 16472, 20088,
                        24200, 28840, 34040, 39832, 46248, 53320, 61080,
                        69560, 78792, 88808, 99640, 111320, 123880, 137352,
                        151768, 167160, 183560, 201000, 219512, 239128,
                        259880, 281800]
        
        if n <= len(initial_terms):
            return torch.tensor(initial_terms[:n], device=self.device)
        
        # For larger n, use the recurrence relation
        # This is a simplified version - the actual formula is more complex
        sequence = torch.zeros(n, device=self.device)
        sequence[:len(initial_terms)] = torch.tensor(initial_terms, device=self.device)
        
        # Use the general formula for larger terms
        for i in range(len(initial_terms), n):
            # Approximate formula based on the tetrahedral family pattern
            sequence[i] = 8 * (2*i - 3) * (i**2 - 3*i + 5) // 3
        
        return sequence
    
    def divisor_wave_coefficients(self, n: int, prime_base: int = 2) -> torch.Tensor:
        """
        Generate coefficients for divisor wave functions.
        
        Args:
            n: Number of coefficients
            prime_base: Base prime for the divisor wave
        
        Returns:
            Tensor of divisor wave coefficients
        """
        coefficients = torch.zeros(n, device=self.device)
        
        for k in range(1, n + 1):
            # Simplified divisor wave coefficient calculation
            # Based on the divisor function and prime factorization
            divisor_sum = sum(d for d in range(1, k + 1) if k % d == 0)
            coefficients[k-1] = divisor_sum / k  # Normalized
        
        return coefficients
    
    def custom_sequence(self, n: int, formula: Callable[[int], float]) -> torch.Tensor:
        """
        Generate a custom sequence based on a user-provided formula.
        
        Args:
            n: Number of terms
            formula: Function that takes an index and returns a value
        
        Returns:
            Tensor of sequence values
        """
        values = [formula(i) for i in range(1, n + 1)]
        return torch.tensor(values, device=self.device)
    
    def polynomial_sequence(self, n: int, coefficients: List[float]) -> torch.Tensor:
        """
        Generate a sequence based on a polynomial.
        
        Args:
            n: Number of terms
            coefficients: Polynomial coefficients [a_0, a_1, a_2, ...] for a_0 + a_1*x + a_2*x^2 + ...
        
        Returns:
            Tensor of polynomial sequence values
        """
        indices = torch.arange(1, n + 1, device=self.device)
        result = torch.zeros(n, device=self.device)
        
        for i, coeff in enumerate(coefficients):
            result += coeff * (indices ** i)
        
        return result
    
    def get_sequence_by_type(self, sequence_type: SequenceType, n: int, **kwargs) -> torch.Tensor:
        """Get a sequence by its type with optional parameters."""
        if sequence_type == SequenceType.TETRAHEDRAL:
            return self.tetrahedral_numbers(n, **kwargs)
        elif sequence_type == SequenceType.TRIANGULAR:
            return self.triangular_numbers(n, **kwargs)
        elif sequence_type == SequenceType.GEOMETRIC:
            return self.geometric_series(n, **kwargs)
        elif sequence_type == SequenceType.FIBONACCI:
            return self.fibonacci_sequence(n)
        elif sequence_type == SequenceType.PRIME:
            return self.prime_sequence(n)
        elif sequence_type == SequenceType.OEIS_A287324:
            return self.a287324_sequence(n)
        elif sequence_type == SequenceType.DIVISOR_WAVE:
            return self.divisor_wave_coefficients(n, **kwargs)
        else:
            raise ValueError(f"Unsupported sequence type: {sequence_type}")
    
    def get_sequence_properties(self, sequence_type: SequenceType) -> SequenceProperties:
        """Get properties and metadata for a sequence type."""
        return self.sequence_properties.get(sequence_type)
    
    def generate_architecture_sequence(self, sequence_type: SequenceType, 
                                     max_layers: int, scale_factor: float = 1.0) -> List[int]:
        """
        Generate a sequence suitable for neural network layer sizes.
        
        Args:
            sequence_type: Type of sequence to use
            max_layers: Maximum number of layers
            scale_factor: Scaling factor for the sequence values
        
        Returns:
            List of layer sizes
        """
        raw_sequence = self.get_sequence_by_type(sequence_type, max_layers)
        
        # Scale and convert to appropriate layer sizes
        scaled_sequence = (raw_sequence * scale_factor).int()
        
        # Ensure minimum layer size of 1 and reasonable maximum
        layer_sizes = torch.clamp(scaled_sequence, min=1, max=4096).tolist()
        
        return layer_sizes
    
    def create_training_schedule(self, sequence_type: SequenceType, 
                               total_epochs: int) -> Dict[str, List[float]]:
        """
        Create a training schedule based on a mathematical sequence.
        
        Args:
            sequence_type: Sequence type for scheduling
            total_epochs: Total number of training epochs
        
        Returns:
            Dictionary with learning rate and other hyperparameter schedules
        """
        base_sequence = self.get_sequence_by_type(sequence_type, total_epochs)
        
        # Normalize for learning rate schedule (decreasing)
        lr_schedule = (1.0 / (base_sequence + 1)).tolist()
        
        # Create momentum schedule (increasing)
        momentum_schedule = (1.0 - 1.0 / (base_sequence + 1)).tolist()
        
        return {
            "learning_rate": lr_schedule,
            "momentum": momentum_schedule,
            "sequence_values": base_sequence.tolist()
        }


# Additional utility functions for sequence analysis
def analyze_sequence_growth(sequence: torch.Tensor) -> Dict[str, float]:
    """Analyze the growth properties of a sequence."""
    if len(sequence) < 2:
        return {"growth_rate": 0.0, "variance": 0.0}
    
    differences = sequence[1:] - sequence[:-1]
    growth_rate = torch.mean(differences).item()
    variance = torch.var(differences).item()
    
    return {
        "growth_rate": growth_rate,
        "variance": variance,
        "mean": torch.mean(sequence).item(),
        "std": torch.std(sequence).item(),
        "min": torch.min(sequence).item(),
        "max": torch.max(sequence).item()
    }


def find_sequence_patterns(sequence: torch.Tensor, pattern_length: int = 3) -> List[Tuple[int, List[int]]]:
    """Find repeating patterns in a sequence."""
    patterns = []
    sequence_list = sequence.tolist()
    
    for i in range(len(sequence_list) - pattern_length + 1):
        pattern = sequence_list[i:i + pattern_length]
        
        # Look for repetitions of this pattern
        for j in range(i + pattern_length, len(sequence_list) - pattern_length + 1):
            if sequence_list[j:j + pattern_length] == pattern:
                patterns.append((i, pattern))
                break
    
    return patterns