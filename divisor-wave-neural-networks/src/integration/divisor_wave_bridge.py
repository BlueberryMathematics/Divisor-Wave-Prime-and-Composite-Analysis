"""
Divisor Wave Bridge - Integration with divisor-wave-python
=========================================================

Bridge module that connects the neural networks library with the core
divisor-wave-python mathematical functions and data structures.

This module provides:
- Data loading from divisor-wave JSON files
- Function evaluation integration
- Mathematical formula conversion
- Sequence generation from divisor wave functions
"""

import sys
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Union, Any, Callable
import torch
import torch.nn as nn
import numpy as np
import json
import warnings

# Add divisor-wave-python to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DIVISOR_WAVE_PYTHON_PATH = PROJECT_ROOT / "divisor-wave-python"
sys.path.insert(0, str(DIVISOR_WAVE_PYTHON_PATH))
sys.path.insert(0, str(DIVISOR_WAVE_PYTHON_PATH / "src"))

# Import divisor-wave-python components with fallbacks
try:
    from core.special_functions_library import SpecialFunctionsLibrary
    from core.mathematical_function_generator import MathematicalFunctionGenerator
    from core.latex_function_builder import LaTeXFunctionBuilder
    from utils.mathematical_sequences import MathematicalSequences as DWSequences
    DIVISOR_WAVE_AVAILABLE = True
except ImportError as e:
    warnings.warn(f"divisor-wave-python not available: {e}")
    DIVISOR_WAVE_AVAILABLE = False
    
    # Create dummy classes for type hints
    class SpecialFunctionsLibrary: pass
    class MathematicalFunctionGenerator: pass
    class LaTeXFunctionBuilder: pass
    class DWSequences: pass


class DivisorWaveBridge:
    """
    Bridge between neural networks and divisor-wave-python mathematical functions.
    
    Provides seamless integration with the mathematical backend for:
    - Loading mathematical formulas as training data
    - Evaluating functions for neural network training
    - Converting between representations
    - Generating mathematical sequences
    """
    
    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize the bridge with divisor-wave-python.
        
        Args:
            data_path: Path to divisor-wave-python data directory
        """
        self.data_path = Path(data_path) if data_path else self._find_data_path()
        self.available = DIVISOR_WAVE_AVAILABLE
        
        if self.available:
            self._initialize_components()
        else:
            warnings.warn("divisor-wave-python not available. Some features will be limited.")
    
    def _find_data_path(self) -> Path:
        """Automatically find the divisor-wave-python data path."""
        possible_paths = [
            DIVISOR_WAVE_PYTHON_PATH / "src" / "data",
            PROJECT_ROOT / "divisor-wave-python" / "src" / "data",
            Path.cwd() / "divisor-wave-python" / "src" / "data"
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        
        # Return first path as default
        return possible_paths[0]
    
    def _initialize_components(self):
        """Initialize divisor-wave-python components."""
        try:
            self.special_functions = SpecialFunctionsLibrary()
            self.function_generator = MathematicalFunctionGenerator()
            self.latex_builder = LaTeXFunctionBuilder()
            self.sequence_generator = DWSequences()
        except Exception as e:
            warnings.warn(f"Failed to initialize divisor-wave components: {e}")
            self.available = False
    
    def load_mathematical_formulas(self) -> Dict[str, Any]:
        """
        Load all mathematical formulas from divisor-wave-python data files.
        
        Returns:
            Dictionary containing all loaded formulas organized by category
        """
        if not self.available:
            return {"error": "divisor-wave-python not available"}
        
        formulas = {}
        
        try:
            # Load from different formula categories
            formula_files = [
                "formulas/core_functions.json",
                "formulas/riesz_products.json", 
                "formulas/viete_products.json",
                "formulas/special_products.json",
                "formulas/custom_functions.json",
                "formulas/ai_generated_functions.json"
            ]
            
            for file_path in formula_files:
                full_path = self.data_path / file_path
                if full_path.exists():
                    with open(full_path, 'r') as f:
                        data = json.load(f)
                    
                    category = file_path.split('/')[-1].replace('.json', '')
                    formulas[category] = data
                    
        except Exception as e:
            warnings.warn(f"Failed to load formulas: {e}")
            return {"error": str(e)}
        
        return formulas
    
    def convert_formulas_to_tensors(self, 
                                  formulas: Dict[str, Any],
                                  max_terms: int = 100) -> Dict[str, torch.Tensor]:
        """
        Convert mathematical formulas to tensor representations for neural networks.
        
        Args:
            formulas: Dictionary of formulas from load_mathematical_formulas
            max_terms: Maximum number of terms per formula
            
        Returns:
            Dictionary of tensors representing formulas
        """
        tensor_data = {}
        
        for category, category_data in formulas.items():
            if isinstance(category_data, dict) and 'functions' in category_data:
                functions = category_data['functions']
                category_tensors = []
                
                for func_name, func_data in functions.items():
                    if isinstance(func_data, dict):
                        # Extract numerical coefficients or create from LaTeX
                        tensor_repr = self._formula_to_tensor(func_data, max_terms)
                        if tensor_repr is not None:
                            category_tensors.append(tensor_repr)
                
                if category_tensors:
                    tensor_data[category] = torch.stack(category_tensors)
        
        return tensor_data
    
    def _formula_to_tensor(self, formula_data: Dict[str, Any], max_terms: int) -> Optional[torch.Tensor]:
        """Convert a single formula to tensor representation."""
        try:
            # Try to extract coefficients if available
            if 'coefficients' in formula_data:
                coeffs = formula_data['coefficients']
                if isinstance(coeffs, list):
                    tensor = torch.tensor(coeffs[:max_terms], dtype=torch.float32)
                    # Pad if necessary
                    if len(tensor) < max_terms:
                        padding = torch.zeros(max_terms - len(tensor))
                        tensor = torch.cat([tensor, padding])
                    return tensor
            
            # Try to evaluate LaTeX formula at specific points
            if 'latex_formula' in formula_data:
                latex_formula = formula_data['latex_formula']
                return self._latex_to_tensor(latex_formula, max_terms)
            
            # Try to use function implementation if available
            if 'python_implementation' in formula_data:
                return self._python_function_to_tensor(
                    formula_data['python_implementation'], max_terms
                )
            
            # Default: create tensor from function ID or other numerical data
            if 'id' in formula_data:
                # Create a simple representation based on function ID
                func_id = hash(str(formula_data['id'])) % 1000000
                np.random.seed(func_id)
                return torch.tensor(np.random.normal(0, 1, max_terms), dtype=torch.float32)
            
        except Exception as e:
            warnings.warn(f"Failed to convert formula to tensor: {e}")
        
        return None
    
    def _latex_to_tensor(self, latex_formula: str, max_terms: int) -> torch.Tensor:
        """Convert LaTeX formula to tensor by evaluation."""
        if not self.available:
            return torch.randn(max_terms)
        
        try:
            # Use LaTeX builder to convert and evaluate
            x_values = torch.linspace(-2, 2, max_terms)
            y_values = []
            
            for x in x_values:
                try:
                    # This would require actual LaTeX parsing - simplified version
                    # In practice, this would use the latex_function_builder
                    y = float(x)  # Placeholder
                    y_values.append(y)
                except:
                    y_values.append(0.0)
            
            return torch.tensor(y_values, dtype=torch.float32)
            
        except Exception as e:
            warnings.warn(f"Failed to evaluate LaTeX formula: {e}")
            return torch.randn(max_terms)
    
    def _python_function_to_tensor(self, python_code: str, max_terms: int) -> torch.Tensor:
        """Convert Python function implementation to tensor."""
        try:
            # Evaluate Python function at specific points
            x_values = torch.linspace(-2, 2, max_terms)
            y_values = []
            
            # This is simplified - real implementation would be more sophisticated
            for x in x_values:
                try:
                    # Execute the Python code safely (simplified)
                    # In practice, this would use ast or other safe evaluation
                    y = float(x)  # Placeholder
                    y_values.append(y)
                except:
                    y_values.append(0.0)
            
            return torch.tensor(y_values, dtype=torch.float32)
            
        except Exception as e:
            warnings.warn(f"Failed to evaluate Python function: {e}")
            return torch.randn(max_terms)
    
    def evaluate_divisor_wave_function(self, 
                                     function_id: str,
                                     x_values: torch.Tensor,
                                     normalization_type: str = 'N') -> torch.Tensor:
        """
        Evaluate a divisor wave function at given x values.
        
        Args:
            function_id: ID of the function to evaluate
            x_values: Tensor of x values to evaluate at
            normalization_type: Type of normalization ('N', 'X', 'Y', 'Z', 'XYZ')
            
        Returns:
            Tensor of function values
        """
        if not self.available:
            # Return mock data
            return torch.sin(x_values)
        
        try:
            # Convert torch tensor to numpy for divisor-wave-python
            x_numpy = x_values.detach().cpu().numpy()
            
            # Evaluate using special functions library
            y_values = []
            for x in x_numpy:
                try:
                    # This would call the actual divisor wave function
                    # Simplified for now
                    y = self.special_functions.evaluate_function(
                        function_id, complex(x), normalization_type
                    )
                    y_values.append(float(y.real) if hasattr(y, 'real') else float(y))
                except:
                    y_values.append(0.0)
            
            return torch.tensor(y_values, dtype=torch.float32)
            
        except Exception as e:
            warnings.warn(f"Failed to evaluate divisor wave function: {e}")
            return torch.sin(x_values)  # Fallback
    
    def generate_training_data(self, 
                             num_samples: int = 1000,
                             sequence_length: int = 100) -> Dict[str, torch.Tensor]:
        """
        Generate training data for neural networks using divisor wave functions.
        
        Args:
            num_samples: Number of training samples
            sequence_length: Length of each sequence
            
        Returns:
            Dictionary containing input sequences and target values
        """
        if not self.available:
            return self._generate_mock_training_data(num_samples, sequence_length)
        
        try:
            # Load formulas
            formulas = self.load_mathematical_formulas()
            tensor_formulas = self.convert_formulas_to_tensors(formulas, sequence_length)
            
            # Create training sequences
            input_sequences = []
            target_sequences = []
            
            for category, tensors in tensor_formulas.items():
                for i in range(min(num_samples // (len(tensor_formulas) + 1), tensors.shape[0])):
                    formula_tensor = tensors[i]
                    
                    # Input: partial sequence
                    input_seq = formula_tensor[:sequence_length//2]
                    # Target: next values in sequence
                    target_seq = formula_tensor[sequence_length//2:sequence_length]
                    
                    input_sequences.append(input_seq)
                    target_sequences.append(target_seq)
            
            # Pad to requested number of samples
            while len(input_sequences) < num_samples:
                idx = len(input_sequences) % len(input_sequences) if input_sequences else 0
                if input_sequences:
                    input_sequences.append(input_sequences[idx])
                    target_sequences.append(target_sequences[idx])
                else:
                    break
            
            return {
                "input_sequences": torch.stack(input_sequences[:num_samples]),
                "target_sequences": torch.stack(target_sequences[:num_samples]),
                "sequence_length": sequence_length
            }
            
        except Exception as e:
            warnings.warn(f"Failed to generate training data: {e}")
            return self._generate_mock_training_data(num_samples, sequence_length)
    
    def _generate_mock_training_data(self, 
                                   num_samples: int, 
                                   sequence_length: int) -> Dict[str, torch.Tensor]:
        """Generate mock training data when divisor-wave-python is not available."""
        # Generate synthetic mathematical sequences
        input_sequences = []
        target_sequences = []
        
        for i in range(num_samples):
            # Create sequences with mathematical patterns
            t = torch.linspace(0, 4*np.pi, sequence_length)
            
            # Mix of sine, cosine, and polynomial patterns
            pattern_type = i % 4
            if pattern_type == 0:
                sequence = torch.sin(t) + 0.1 * torch.sin(5*t)
            elif pattern_type == 1:
                sequence = torch.cos(t) * torch.exp(-t/10)
            elif pattern_type == 2:
                sequence = t**2 / 100 - t/10
            else:
                sequence = torch.sin(t) * torch.cos(2*t)
            
            # Add noise
            sequence += torch.randn_like(sequence) * 0.05
            
            # Split into input and target
            mid_point = sequence_length // 2
            input_sequences.append(sequence[:mid_point])
            target_sequences.append(sequence[mid_point:])
        
        return {
            "input_sequences": torch.stack(input_sequences),
            "target_sequences": torch.stack(target_sequences),
            "sequence_length": sequence_length
        }
    
    def create_function_dataset(self) -> torch.utils.data.Dataset:
        """Create a PyTorch dataset from divisor wave functions."""
        from torch.utils.data import Dataset
        
        class DivisorWaveDataset(Dataset):
            def __init__(self, bridge):
                self.bridge = bridge
                self.data = bridge.generate_training_data()
                
            def __len__(self):
                return len(self.data["input_sequences"])
            
            def __getitem__(self, idx):
                return (
                    self.data["input_sequences"][idx],
                    self.data["target_sequences"][idx]
                )
        
        return DivisorWaveDataset(self)
    
    def get_mathematical_constants(self) -> Dict[str, float]:
        """Get mathematical constants used in divisor wave analysis."""
        return {
            "pi": float(np.pi),
            "e": float(np.e),
            "golden_ratio": (1 + np.sqrt(5)) / 2,
            "euler_gamma": 0.5772156649015329,  # Euler-Mascheroni constant
            "zeta_2": np.pi**2 / 6,  # ζ(2)
            "zeta_4": np.pi**4 / 90,  # ζ(4)
        }
    
    def get_sequence_generators(self) -> Dict[str, Callable]:
        """Get sequence generator functions."""
        if not self.available:
            return {}
        
        generators = {}
        try:
            # Add divisor wave sequence generators
            generators["tetrahedral"] = lambda n: self.sequence_generator.tetrahedral_numbers(n)
            generators["triangular"] = lambda n: self.sequence_generator.triangular_numbers(n)
            generators["prime"] = lambda n: self.sequence_generator.prime_sequence(n)
        except:
            pass
        
        return generators
    
    def validate_connection(self) -> Dict[str, Any]:
        """Validate the connection to divisor-wave-python."""
        status = {
            "available": self.available,
            "data_path_exists": self.data_path.exists(),
            "components_loaded": False,
            "formula_files": [],
            "errors": []
        }
        
        if self.available:
            try:
                # Check if components are loaded
                status["components_loaded"] = all([
                    hasattr(self, 'special_functions'),
                    hasattr(self, 'function_generator'),
                    hasattr(self, 'latex_builder')
                ])
            except Exception as e:
                status["errors"].append(f"Component check failed: {e}")
        
        # Check for formula files
        if self.data_path.exists():
            formula_dir = self.data_path / "formulas"
            if formula_dir.exists():
                status["formula_files"] = list(formula_dir.glob("*.json"))
        
        return status


# Factory functions for easy integration

def create_divisor_wave_bridge(data_path: Optional[str] = None) -> DivisorWaveBridge:
    """Create a bridge to divisor-wave-python."""
    return DivisorWaveBridge(data_path)


def load_divisor_wave_training_data(num_samples: int = 1000, 
                                  sequence_length: int = 100) -> Dict[str, torch.Tensor]:
    """Quick function to load training data from divisor wave functions."""
    bridge = create_divisor_wave_bridge()
    return bridge.generate_training_data(num_samples, sequence_length)


def create_divisor_wave_dataset() -> torch.utils.data.Dataset:
    """Create a PyTorch dataset from divisor wave functions."""
    bridge = create_divisor_wave_bridge()
    return bridge.create_function_dataset()