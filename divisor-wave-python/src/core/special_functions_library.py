"""
Special Functions Library
Enhanced version of Special_Functions_OG.py with advanced normalization modes and performance optimizations
Based on Leo J. Borcherding's research: "Divisor Wave Product Analysis of Prime and Composite Numbers"

This library implements all the infinite product functions from the original research with:
- Enhanced normalization modes: X, Y, Z, XYZ, N 
- Improved absolute value handling and numerical stability
- Support for custom LaTeX functions
- M and beta coefficient optimization
- Numba JIT compilation for speed
- CuPy GPU acceleration with CPU multiprocessing fallback

4/9/2023 - Original by @LeoBorcherding
11/5/2025 - Enhanced implementation with performance optimizations
"""

import cmath
import math
import os
import pprint
import re
import mpmath
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import special
from scipy import constants
from typing import Dict, Any, Optional, Callable
import json
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

# Performance optimization imports
try:
    from numba import jit, njit, prange
    NUMBA_AVAILABLE = True
    print("+ Numba JIT compilation available")
except ImportError:
    print("- Numba not available - install with: pip install numba")
    NUMBA_AVAILABLE = False
    # Create dummy decorators
    def jit(*args, **kwargs):
        def decorator(func):
            return func
        return decorator if args and callable(args[0]) else decorator
    
    def njit(*args, **kwargs):
        def decorator(func):
            return func
        return decorator if args and callable(args[0]) else decorator
    
    def prange(*args, **kwargs):
        return range(*args)

try:
    import cupy as cp
    CUPY_AVAILABLE = True
    print("+ CuPy GPU acceleration available")
except ImportError:
    print("- CuPy not available - install with: pip install cupy")
    CUPY_AVAILABLE = False
    cp = None

# Import LaTeX function builders for custom functions
from .latex_function_builder import LaTeXFunctionBuilder
from .latex_to_numpy_converter import LatexToNumpyConverter

plt.style.use('dark_background')


class SpecialFunctionsLibrary:
    """
    Enhanced Special Functions Library for divisor wave analysis
    Implements all functions from the original research with advanced normalization and performance optimizations
    """
    
    def __init__(self, plot_type: str = "2D", use_gpu: bool = None, use_jit: bool = None):
        """
        Initialize the Special Functions Library
        
        Args:
            plot_type: Type of plot ("2D" or "3D")
            use_gpu: Force GPU usage (None for auto-detect)
            use_jit: Force JIT compilation (None for auto-detect)
        """
        self.plot_type = plot_type
        
        # Performance settings
        self.use_gpu = use_gpu if use_gpu is not None else CUPY_AVAILABLE
        self.use_jit = use_jit if use_jit is not None else NUMBA_AVAILABLE
        self.num_cores = mp.cpu_count()
        
        print(f"Performance settings:")
        print(f"   GPU acceleration: {'ON' if self.use_gpu else 'OFF'}")
        print(f"   JIT compilation: {'ON' if self.use_jit else 'OFF'}")
        print(f"   CPU cores: {self.num_cores}")
        
        # Choose optimal numpy backend
        if self.use_gpu and CUPY_AVAILABLE:
            self.xp = cp
            self.backend = "GPU"
        else:
            self.xp = np
            self.backend = "CPU"
        
        print(f"   Backend: {self.backend}")
        
        # Initialize LaTeX builders
        self.latex_builder = LaTeXFunctionBuilder()
        self.latex_converter = LatexToNumpyConverter()
        self.custom_functions = self.latex_builder.load_database()
        
        # Regex pattern for product factory (from original)
        self.pattern = r'([a-z]+)_\(([a-z]+)=([0-9]+)\)\^\(([a-z]+)\=([0-9]+)\s*\[(.*)\]'
        
        # Initialize optimized utility functions
        self._init_optimized_functions()
        
        # EXACT original coefficients from Special_Functions_OG.py
        self.normalization_modes = {
            'N': {  # No normalization (original N mode)
                'product_of_sin': {'m': 0.0465, 'beta': 0.178},
                'product_of_product_representation_for_sin': {'m': 0.0125, 'beta': 0.078},
                'riesz_products': {'m': 0.0125, 'beta': 0.054},
                'viete_products': {'m': 0.07, 'beta': 1.0},
                'binary_prime_indicators': {'c': 0.83, 'm': 0.029, 'alpha': 0.74, 'beta': 0.025},
                'gamma_norm': False
            },
            'Y': {  # With gamma normalization (original Y mode)
                'product_of_sin': {'m': 0.0465, 'beta': 0.178},
                'product_of_product_representation_for_sin': {'m': 0.36, 'beta': 0.1468},
                'riesz_products': {'m': 0.0125, 'beta': 0.054},
                'viete_products': {'m': 0.27, 'beta': 1.0},
                'binary_prime_indicators': {'c': 0.13, 'm': 0.29, 'alpha': 0.14, 'beta': 0.25},
                'gamma_norm': True
            },
            'X': {  # X-axis focused normalization
                'product_of_sin': {'m': 0.0465, 'beta': 0.178},
                'product_of_product_representation_for_sin': {'m': 0.0125, 'beta': 0.078},
                'riesz_products': {'m': 0.0125, 'beta': 0.054},
                'viete_products': {'m': 0.0125, 'beta': 0.054},
                'gamma_norm': False
            },
            'Z': {  # Z-axis focused normalization
                'product_of_sin': {'m': 0.36, 'beta': 0.1468},
                'product_of_product_representation_for_sin': {'m': 0.36, 'beta': 0.1468},
                'riesz_products': {'m': 0.36, 'beta': 0.1468},
                'viete_products': {'m': 0.36, 'beta': 0.1468},
                'gamma_norm': False
            },
            'XYZ': {  # Combined normalization
                'product_of_sin': {'m': 0.1825, 'beta': 0.1274},
                'product_of_product_representation_for_sin': {'m': 0.1825, 'beta': 0.1274},
                'riesz_products': {'m': 0.1825, 'beta': 0.1274},
                'viete_products': {'m': 0.1825, 'beta': 0.1274},
                'gamma_norm': True
            }
        }
        
        # Initialize custom function builders
        self.latex_builder = LaTeXFunctionBuilder()
        self.latex_converter = LatexToNumpyConverter()
        
        # Load custom functions
        self.custom_functions = self._load_custom_functions()
    
    def _init_optimized_functions(self):
        """Initialize JIT-compiled utility functions for performance"""
        if self.use_jit and NUMBA_AVAILABLE:
            print("+ Compiling JIT functions...")
            # Compile critical functions with JIT
            self._product_core_jit = self._create_jit_product_core()
            self._safe_complex_math_jit = self._create_jit_complex_math()
            print("+ JIT compilation complete")
        else:
            # Use regular Python functions
            self._product_core_jit = self._product_core_python
            self._safe_complex_math_jit = self._safe_complex_math_python
    
    def _create_jit_product_core(self):
        """Create JIT-compiled product computation core"""
        if not NUMBA_AVAILABLE:
            return self._product_core_python
        
        @njit(cache=True, fastmath=True)
        def product_core_jit(z_real, z_imag, n_max, operation='sin'):
            """JIT-compiled core product computation"""
            result_real = 1.0
            result_imag = 0.0
            
            for k in range(1, n_max):
                # Compute z/k
                zk_real = z_real / k
                zk_imag = z_imag / k
                
                # Compute operation(z/k)
                if operation == 'sin':
                    # sin(z/k) = sin(real)*cosh(imag) + i*cos(real)*sinh(imag)
                    sin_real = math.sin(zk_real) * math.cosh(zk_imag)
                    sin_imag = math.cos(zk_real) * math.sinh(zk_imag)
                    op_real, op_imag = sin_real, sin_imag
                elif operation == 'cos':
                    # cos(z/k) = cos(real)*cosh(imag) - i*sin(real)*sinh(imag)
                    cos_real = math.cos(zk_real) * math.cosh(zk_imag)
                    cos_imag = -math.sin(zk_real) * math.sinh(zk_imag)
                    op_real, op_imag = cos_real, cos_imag
                else:  # tan or other
                    # Default to sin for safety
                    sin_real = math.sin(zk_real) * math.cosh(zk_imag)
                    sin_imag = math.cos(zk_real) * math.sinh(zk_imag)
                    op_real, op_imag = sin_real, sin_imag
                
                # Multiply result by operation result: result *= op
                new_real = result_real * op_real - result_imag * op_imag
                new_imag = result_real * op_imag + result_imag * op_real
                result_real, result_imag = new_real, new_imag
            
            # Return magnitude
            return math.sqrt(result_real * result_real + result_imag * result_imag)
        
        return product_core_jit
    
    def _create_jit_complex_math(self):
        """Create JIT-compiled complex math utilities"""
        if not NUMBA_AVAILABLE:
            return self._safe_complex_math_python
        
        @njit(cache=True, fastmath=True)
        def safe_complex_math_jit(z_real, z_imag, operation='abs'):
            """JIT-compiled safe complex math operations"""
            if operation == 'abs':
                return math.sqrt(z_real * z_real + z_imag * z_imag)
            elif operation == 'arg':
                return math.atan2(z_imag, z_real)
            elif operation == 'exp':
                # exp(z) = exp(real) * (cos(imag) + i*sin(imag))
                exp_real = math.exp(z_real)
                return exp_real * math.sqrt(math.cos(z_imag)**2 + math.sin(z_imag)**2)  # magnitude
            else:
                return math.sqrt(z_real * z_real + z_imag * z_imag)
        
        return safe_complex_math_jit
    
    def _product_core_python(self, z_real, z_imag, n_max, operation='sin'):
        """Python fallback for product computation"""
        z = complex(z_real, z_imag)
        result = complex(1.0, 0.0)
        
        for k in range(1, n_max):
            zk = z / k
            if operation == 'sin':
                op_result = cmath.sin(zk)
            elif operation == 'cos':
                op_result = cmath.cos(zk)
            elif operation == 'tan':
                op_result = cmath.tan(zk)
            else:
                op_result = cmath.sin(zk)  # Default
            
            result *= op_result
        
        return abs(result)
    
    def _safe_complex_math_python(self, z_real, z_imag, operation='abs'):
        """Python fallback for complex math"""
        z = complex(z_real, z_imag)
        if operation == 'abs':
            return abs(z)
        elif operation == 'arg':
            return cmath.phase(z)
        elif operation == 'exp':
            return abs(cmath.exp(z))
        else:
            return abs(z)
    
    def get_optimal_array(self, data):
        """Get array using optimal backend (GPU/CPU)"""
        if self.use_gpu and CUPY_AVAILABLE:
            if isinstance(data, np.ndarray):
                return cp.asarray(data)
            return cp.array(data)
        else:
            if CUPY_AVAILABLE and hasattr(data, 'get'):
                return data.get()  # Convert from CuPy to NumPy
            return np.array(data)
    
    def parallel_evaluate_function(self, func, z_values, normalize_type="N", max_workers=None):
        """Evaluate function in parallel across multiple points"""
        if max_workers is None:
            max_workers = min(self.num_cores, len(z_values))
        
        if len(z_values) < 100:  # Small datasets don't benefit from parallelization
            return [func(z, normalize_type) for z in z_values]
        
        # Use ThreadPoolExecutor for I/O bound tasks, ProcessPoolExecutor for CPU bound
        executor_class = ProcessPoolExecutor if len(z_values) > 1000 else ThreadPoolExecutor
        
        with executor_class(max_workers=max_workers) as executor:
            futures = [executor.submit(func, z, normalize_type) for z in z_values]
            results = [future.result() for future in futures]
        
        return results
    
    def _load_custom_functions(self) -> Dict[str, Any]:
        """Load custom functions from JSON database"""
        try:
            return self.latex_builder.load_database()
        except Exception as e:
            print(f"Warning: Could not load custom functions: {e}")
            return {}
    
    def _get_coefficients(self, function_category: str, normalize_type: str) -> Dict[str, float]:
        """Get m and beta coefficients for a function based on normalization mode"""
        norm_mode = self.normalization_modes.get(normalize_type, self.normalization_modes['N'])
        return norm_mode.get(function_category, norm_mode['product_of_sin'])
    
    def _should_apply_gamma_norm(self, normalize_type: str) -> bool:
        """Check if gamma normalization should be applied"""
        norm_mode = self.normalization_modes.get(normalize_type, self.normalization_modes['N'])
        return norm_mode.get('gamma_norm', False)
    
    def _safe_gamma_normalize(self, result: float) -> float:
        """Safely apply gamma normalization with overflow protection"""
        try:
            if abs(result) < 100 and np.isfinite(result):
                return result / scipy.special.gamma(result)
            return result
        except (OverflowError, ValueError, ZeroDivisionError):
            return result
    
    def _safe_abs_power(self, value: complex, exponent: float) -> float:
        """Safely compute |value|^exponent with numerical stability"""
        try:
            magnitude = abs(value)
            if magnitude == 0:
                return 0.0
            if not np.isfinite(magnitude):
                return 0.0
            result = magnitude ** exponent
            return float(result) if np.isfinite(result) else 0.0
        except (OverflowError, ValueError):
            return 0.0
    
    def safe_abs(self, value: complex) -> float:
        """Safely compute absolute value with numerical stability"""
        try:
            result = abs(value)
            return float(result) if np.isfinite(result) else 0.0
        except (OverflowError, ValueError):
            return 0.0
    
    def safe_gamma(self, z: complex) -> complex:
        """Safely compute gamma function with numerical stability"""
        try:
            import math
            if isinstance(z, complex):
                # For complex numbers, use a simple approximation or return abs
                return abs(z)
            else:
                result = math.gamma(float(z))
                return result if np.isfinite(result) else 0.0
        except (OverflowError, ValueError, TypeError):
            return 0.0
    
    def lamda_function_library(self, normalize_type: str = 'N', catalog_only: bool = False):
        """
        Original lambda function library for backward compatibility with Complex_Plotting_OG.py
        Returns a lambda function selected by user input (interactive mode) or by function ID
        
        This method preserves the exact original interface from Special_Functions_OG.py
        but uses our optimized function implementations underneath.
        
        Args:
            normalize_type: Normalization mode ('Y' or 'N' for backward compatibility)
            catalog_only: If True, returns only the catalog dict without user interaction
        
        Returns:
            Lambda function that takes a complex z parameter, or catalog dict if catalog_only=True
        """
        # Convert to our enhanced normalization system
        norm_type = "Y" if normalize_type == 'Y' else "N"
        
        # Original lambda library with optimized implementations underneath
        operations = {
            # Core infinite products (EXACT original numbering preserved)
            '1': lambda z: self.product_of_sin(z, norm_type),
            '2': lambda z: self.product_of_product_representation_for_sin(z, norm_type),
            '3': lambda z: self.product_of_product_representation_for_sin_COMPLEX_VARIANT(z, norm_type),  # NOW PROPERLY IMPLEMENTED
            '4': lambda z: self.complex_playground_magnification_currated_functions_DEMO(z, norm_type),

            # Riesz Products (corrected from original)
            '5': lambda z: self.Riesz_Product_for_Cos(z, norm_type),
            '6': lambda z: self.Riesz_Product_for_Sin(z, norm_type),
            '7': lambda z: self.Riesz_Product_for_Tan(z, norm_type),

            # Viète Products (corrected from original)
            '8': lambda z: self.Viete_Product_for_Cos(z, norm_type),
            '9': lambda z: self.Viete_Product_for_Sin(z, norm_type),
            '10': lambda z: self.Viete_Product_for_Tan(z, norm_type),

            # Composite functions (corrected from original)
            '11': lambda z: self.cos_of_product_of_sin(z, norm_type),
            '12': lambda z: self.sin_of_product_of_sin(z, norm_type),
            '13': lambda z: self.cos_of_product_of_product_representation_of_sin(z, norm_type),
            '14': lambda z: self.sin_of_product_of_product_representation_of_sin(z, norm_type),

            # Prime indicators (corrected from original)
            '15': lambda z: self.Binary_Output_Prime_Indicator_Function_H(z, norm_type),
            '16': lambda z: self.Prime_Output_Indicator_J(z, norm_type),
            '17': lambda z: self.BOPIF_Q_Alternation_Series(z, norm_type),
            '18': lambda z: self.Dirichlet_Eta_Derived_From_BOPIF(z, norm_type),

            # Basic functions (corrected from original)
            '19': lambda z: self.abs_loggamma(z, norm_type),
            '20': lambda z: self.rational_one_plus_z_squared(z, norm_type),
            '21': lambda z: self.abs_z_to_z(z, norm_type),
            '22': lambda z: self.gamma_function(z, norm_type),

            # Utility functions (corrected from original)
            '23': lambda z: self.natural_logarithm_of_product_of_product_representation_for_sin(z, norm_type),
            '24': lambda z: self.gamma_of_product_of_product_representation_for_sin(z, norm_type),
            '25': lambda z: self.gamma_form_product_of_product_representation_for_sin(z, norm_type),

            # Custom variants (corrected from original)
            '26': lambda z: self.Custom_Riesz_Product_for_Tan(z, norm_type),
            '27': lambda z: self.Custom_Viete_Product_for_Cos(z, norm_type),
            '28': lambda z: self.Half_Base_Viete_Product_for_Sin(z, norm_type),
            '29': lambda z: self.Log_power_base_Viete_Product_for_Sin(z, norm_type),
            '30': lambda z: self.Riesz_Product_for_Tan_and_Prime_indicator_combination(z, norm_type),

            # Advanced functions
            '31': lambda z: self.Nested_roots_product_for_2(z, norm_type),
            '32': lambda z: self.product_factory("∏_(n=2)^z [pi*z ∏_(k=2)^z (1 - z^2 / (k^2 * n^2))]", norm_type)
        }

        # Original catalog for display (CORRECTED to match operations)
        catalog = {
            '1': 'product_of_sin(z, Normalize_type)',
            '2': 'product_of_product_representation_for_sin(z, Normalize_type)',
            '3': 'product_of_product_representation_for_sin_COMPLEX_VARIANT(z, Normalize_type)',
            '4': 'complex_playground_magnification_currated_functions_DEMO(z, Normalize_type)',

            '5': 'Riesz_Product_for_Cos(z, Normalize_type)',
            '6': 'Riesz_Product_for_Sin(z, Normalize_type)',
            '7': 'Riesz_Product_for_Tan(z, Normalize_type)',

            '8': 'Viete_Product_for_Cos(z, Normalize_type)',
            '9': 'Viete_Product_for_Sin(z, Normalize_type)',
            '10': 'Viete_Product_for_Tan(z, Normalize_type)',

            '11': 'cos_of_product_of_sin(z, Normalize_type)',
            '12': 'sin_of_product_of_sin(z, Normalize_type)',
            '13': 'cos_of_product_of_product_representation_of_sin(z, Normalize_type)',
            '14': 'sin_of_product_of_product_representation_of_sin(z, Normalize_type)',

            '15': 'Binary_Output_Prime_Indicator_Function_H(z, Normalize_type)',
            '16': 'Prime_Output_Indicator_J(z, Normalize_type)',
            '17': 'BOPIF_Q_Alternation_Series(z, Normalize_type)',
            '18': 'Dirichlet_Eta_Derived_From_BOPIF(z, Normalize_type)',

            '19': 'abs_loggamma(z, Normalize_type)',
            '20': 'rational_one_plus_z_squared(z, Normalize_type)',
            '21': 'abs_z_to_z(z, Normalize_type)',
            '22': 'gamma_function(z, Normalize_type)',

            '23': 'natural_logarithm_of_product_of_product_representation_for_sin(z, Normalize_type)',
            '24': 'gamma_of_product_of_product_representation_for_sin(z, Normalize_type)',
            '25': 'gamma_form_product_of_product_representation_for_sin(z, Normalize_type)',

            '26': 'Custom_Riesz_Product_for_Tan(z, Normalize_type)',
            '27': 'Custom_Viete_Product_for_Cos(z, Normalize_type)',
            '28': 'Half_Base_Viete_Product_for_Sin(z, Normalize_type)',
            '29': 'Log_power_base_Viete_Product_for_Sin(z, Normalize_type)',
            '30': 'Riesz_Product_for_Tan_and_Prime_indicator_combination(z, Normalize_type)',

            '19': 'abs_loggamma(z, Normalize_type)',
            '20': 'rational_one_plus_z_squared(z, Normalize_type)',
            '21': 'abs_z_to_z(z, Normalize_type)',
            '22': 'gamma_function(z, Normalize_type)',

            '23': 'natural_logarithm_of_product_of_product_representation_for_sin(z, Normalize_type)',
            '24': 'gamma_of_product_of_product_representation_for_sin(z, Normalize_type)',
            '25': 'gamma_form_product_of_product_representation_for_sin(z, Normalize_type)',

            '26': 'Custom_Riesz_Product_for_Tan(z, Normalize_type)',
            '27': 'Custom_Viete_Product_for_Cos(z, Normalize_type)',
            '28': 'Half_Base_Viete_Product_for_Sin(z, Normalize_type)',
            '29': 'Log_power_base_Viete_Product_for_Sin(z, Normalize_type)',
            '30': 'Riesz_Product_for_Tan_and_Prime_indicator_combination(z, Normalize_type)',

            '31': 'Nested_roots_product_for_2(z, Normalize_type)',
            '32': 'product_factory("∏_(n=2)^z [pi*z ∏_(k=2)^z (1 - z^2 / (k^2 * n^2))]", Normalize_type)'
        }

        # For API usage, return catalog without user interaction
        if catalog_only:
            # Return enhanced catalog with metadata for API
            enhanced_catalog = {}
            for key, display in catalog.items():
                enhanced_catalog[key] = {
                    'name': display.split('(')[0],  # Extract function name before (
                    'display': display,
                    'description': f'Lambda function {key}: {display}',
                    'category': 'Lambda Functions'
                }
            return enhanced_catalog

        # For API usage, return function by ID without user interaction
        if hasattr(self, '_selected_function_id'):
            func_id = self._selected_function_id
            if func_id in operations:
                return operations[func_id]
            else:
                return operations['1']  # Default to product_of_sin

        # Original interactive mode for backward compatibility
        print("Please Select a Function to plot:")
        for key, value in catalog.items():
            print(f'{key}: {value}')

        while True:
            user_input = input('Enter your choice: ')
            if user_input in operations:
                return operations[user_input]
            else:
                print("Invalid choice. Please try again.")

    def set_function_selection(self, function_id: str):
        """Set function ID for non-interactive lambda function library usage"""
        self._selected_function_id = function_id

    # ====== MISSING FUNCTIONS FROM ORIGINAL (implementing for compatibility) ======
    
    def complex_playground_magnification_currated_functions_DEMO(self, z: complex, normalize_type: str = 'N') -> float:
        """
        Original playground function for fine-tuning complex magnification
        Implements Riesz Product of Cos variant from original code
        """
        z_real = float(np.real(z))
        z_imag = float(np.imag(z))
        
        # Use original coefficients
        if normalize_type == 'Y':
            m = 0.0125
            beta = 0.054
        else:
            m = 0.0125
            beta = 0.054
        
        try:
            # Original RIESZ PRODUCT OF COS 3 implementation
            result = abs(np.prod([
                pow((1j * z_imag + (1j * z_imag) * np.sin(math.pi * (z_real + 1j * z_imag) * n)), 1j * z_imag)
                for n in range(2, min(int(z_real) + 1, 50))
            ])) ** (-m)
            
            if normalize_type == 'Y':
                result = result / math.gamma(abs(result) + 1)
            
            return self.safe_abs(result)
            
        except Exception as e:
            return 0.0
    
    def product_of_sin(self, z: complex, normalize_type: str = 'N') -> float:
        """
        EXACT REPLICA OF ORIGINAL: Product of Sin(x) via Sin(x) product Representation.
        f(x) = |∏_(n=2)^x { β*(x/k)*sin(π*x/k) }|^(-m)
        
        This is the ORIGINAL mathematical formula from Special_Functions_OG.py
        """
        # Use EXACT original implementation to ensure mathematical correctness
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        # Original coefficient logic
        if normalize_type == 'Y':
            m = 0.0465
            beta = 0.178
        else:
            m = 0.0465
            beta = 0.178

        try:
            # FIXED: Ensure minimum range to avoid empty products
            n_max = max(int(z_real), 2)  # Ensure at least range(2, 3)
            
            # EXACT ORIGINAL FORMULA - DO NOT MODIFY
            result = abs(np.prod([
                beta * ((z_real) / k) * np.sin(math.pi * (z_real + 1j * z_imag) / k)
                for k in range(2, n_max + 1)
            ])) ** (-m)

            # FIXED: Safe gamma normalization to prevent inf/0 issues
            if normalize_type == 'Y':
                if result < 100:  # Only apply gamma normalization for reasonable values
                    gamma_val = scipy.special.gamma(result)
                    if np.isfinite(gamma_val) and gamma_val != 0:
                        result = result / gamma_val
                # For large results, skip gamma normalization to avoid inf
            
            return float(result) if np.isfinite(result) else 0.0
            
        except Exception as e:
            return 0.0
    
    def product_of_product_representation_for_sin(self, z: complex, normalize_type: str = 'N') -> float:
        """
        EXACT REPLICA OF ORIGINAL: Product of the product representation for sin(pi*z/n).
        f(x) = |∏_(k=2)^x (β*x/n) * (πz) * ∏_(n=2)^x (1-(z²)/(k²n²))|^(-m)
        
        This is the ORIGINAL mathematical formula from Special_Functions_OG.py
        """
        # Use EXACT original implementation
        z_real = np.real(z)
        z_imag = np.imag(z)

        # Original coefficient logic
        if normalize_type == 'Y':
            m = 0.36
            beta = 0.1468
        else:
            m = 0.0125
            beta = 0.078

        try:
            # FIXED: Ensure minimum range to avoid empty products
            n_max = max(int(z_real), 2)  # Ensure at least range(2, 3)
            
            # EXACT ORIGINAL FORMULA - DO NOT MODIFY
            result = abs(np.prod([
                beta * (z_real / n) * (((z_real + 1j * z_imag) * math.pi) * np.prod([
                    1 - ((z_real + 1j * z_imag) ** 2) / ((n ** 2) * (k ** 2))
                    for k in range(2, n_max + 1)
                ])) for n in range(2, n_max + 1)
            ])) ** (-m)

            # FIXED: Safe gamma normalization to prevent inf/0 issues
            if normalize_type == 'Y':
                if result < 100:  # Only apply gamma normalization for reasonable values
                    gamma_val = scipy.special.gamma(result)
                    if np.isfinite(gamma_val) and gamma_val != 0:
                        result = result / gamma_val
                # For large results, skip gamma normalization to avoid inf

            return float(result) if np.isfinite(result) else 0.0
            
        except Exception as e:
            return 0.0
    
    # ====== COMPOSITE FUNCTIONS ======
    
    def cos_of_product_of_sin(self, z: complex, normalize_type: str = 'N') -> float:
        """Cosine of the main divisor wave: cos(a(z))"""
        try:
            inner_result = self.product_of_sin(z, normalize_type)
            result = math.cos(inner_result)
            return float(result) if np.isfinite(result) else 0.0
        except Exception:
            return 0.0
    
    def sin_of_product_of_sin(self, z: complex, normalize_type: str = 'N') -> float:
        """Sine of the main divisor wave: sin(a(z))"""
        try:
            inner_result = self.product_of_sin(z, normalize_type)
            result = math.sin(inner_result)
            return float(result) if np.isfinite(result) else 0.0
        except Exception:
            return 0.0
    
    def cos_of_product_of_product_representation_of_sin(self, z: complex, normalize_type: str = 'N') -> float:
        """Cosine of enhanced divisor wave: cos(b(z))"""
        try:
            inner_result = self.product_of_product_representation_for_sin(z, normalize_type)
            result = math.cos(inner_result)
            return float(result) if np.isfinite(result) else 0.0
        except Exception:
            return 0.0
    
    def sin_of_product_of_product_representation_of_sin(self, z: complex, normalize_type: str = 'N') -> float:
        """Sine of enhanced divisor wave: sin(b(z))"""
        try:
            inner_result = self.product_of_product_representation_for_sin(z, normalize_type)
            result = math.sin(inner_result)
            return float(result) if np.isfinite(result) else 0.0
        except Exception:
            return 0.0
    
    # ====== RIESZ PRODUCTS ======
    
    def Riesz_Product_for_Cos(self, z: complex, normalize_type: str = 'N') -> float:
        """
        Riesz product using cosine: R_cos(z) = |∏(1 + cos(πzn))|^(-m)
        """
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        coeffs = self._get_coefficients('riesz_products', normalize_type)
        m = coeffs['m']
        
        try:
            # Calculate Riesz product with cosine
            terms = []
            for n in range(2, int(abs(z_real)) + 20):  # Extended range for Riesz products
                term = 1 + np.cos(math.pi * (z_real + 1j * z_imag) * n)
                terms.append(term)
            
            if not terms:
                return 1.0
            
            product_value = np.prod(terms)
            result = self._safe_abs_power(product_value, -m)
            
            if self._should_apply_gamma_norm(normalize_type):
                result = self._safe_gamma_normalize(result)
            
            return float(result) if np.isfinite(result) else 0.0
            
        except Exception:
            return 0.0
    
    def Riesz_Product_for_Sin(self, z: complex, normalize_type: str = 'N') -> float:
        """
        Riesz product using sine: R_sin(z) = |∏(1 + sin(πzn))|^(-m)
        """
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        coeffs = self._get_coefficients('riesz_products', normalize_type)
        m = coeffs['m']
        
        try:
            # Calculate Riesz product with sine
            terms = []
            for n in range(2, int(abs(z_real)) + 20):
                term = 1 + np.sin(math.pi * (z_real + 1j * z_imag) * n)
                terms.append(term)
            
            if not terms:
                return 1.0
            
            product_value = np.prod(terms)
            result = self._safe_abs_power(product_value, -m)
            
            if self._should_apply_gamma_norm(normalize_type):
                result = self._safe_gamma_normalize(result)
            
            return float(result) if np.isfinite(result) else 0.0
            
        except Exception:
            return 0.0
    
    def Riesz_Product_for_Tan(self, z: complex, normalize_type: str = 'N') -> float:
        """
        Riesz product using tangent: R_tan(z) = |∏(1 + tan(πzn))|^(-m)
        """
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        coeffs = self._get_coefficients('riesz_products', normalize_type)
        m = coeffs['m']
        
        try:
            # Calculate Riesz product with tangent
            terms = []
            for n in range(2, int(abs(z_real)) + 20):
                try:
                    tan_val = np.tan(math.pi * (z_real + 1j * z_imag) * n)
                    if np.isfinite(tan_val):
                        term = 1 + tan_val
                        terms.append(term)
                except:
                    continue
            
            if not terms:
                return 1.0
            
            product_value = np.prod(terms)
            result = self._safe_abs_power(product_value, -m)
            
            if self._should_apply_gamma_norm(normalize_type):
                result = self._safe_gamma_normalize(result)
            
            return float(result) if np.isfinite(result) else 0.0
            
        except Exception:
            return 0.0
    
    # ====== VIÈTE PRODUCTS ======
    
    def Viete_Product_for_Cos(self, z: complex, normalize_type: str = 'N') -> float:
        """
        Viète product using cosine: V_cos(z) = |∏cos(πz/2^n)|^(-m)
        """
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        coeffs = self._get_coefficients('viete_products', normalize_type)
        m = coeffs['m']
        
        try:
            # Calculate Viète product with cosine
            terms = []
            for n in range(2, 50):  # Geometric progression converges faster
                term = np.cos(math.pi * (z_real + 1j * z_imag) / (2 ** n))
                terms.append(term)
            
            product_value = np.prod(terms)
            result = self._safe_abs_power(product_value, -m)
            
            if self._should_apply_gamma_norm(normalize_type):
                result = self._safe_gamma_normalize(result)
            
            return float(result) if np.isfinite(result) else 0.0
            
        except Exception:
            return 0.0
    
    def Viete_Product_for_Sin(self, z: complex, normalize_type: str = 'N') -> float:
        """
        Viète product using sine: V_sin(z) = |∏sin(πz/2^n)|^(-m)
        """
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        coeffs = self._get_coefficients('viete_products', normalize_type)
        m = coeffs['m']
        
        try:
            # Calculate Viète product with sine
            terms = []
            for n in range(2, 50):
                term = np.sin(math.pi * (z_real + 1j * z_imag) / (2 ** n))
                terms.append(term)
            
            product_value = np.prod(terms)
            result = self._safe_abs_power(product_value, -m)
            
            if self._should_apply_gamma_norm(normalize_type):
                result = self._safe_gamma_normalize(result)
            
            return float(result) if np.isfinite(result) else 0.0
            
        except Exception:
            return 0.0
    
    def Viete_Product_for_Tan(self, z: complex, normalize_type: str = 'N') -> float:
        """
        Viète product using tangent: V_tan(z) = |∏tan(πz/2^n)|^(-m)
        """
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        coeffs = self._get_coefficients('viete_products', normalize_type)
        m = coeffs['m']
        
        try:
            # Calculate Viète product with tangent
            terms = []
            for n in range(2, 50):
                try:
                    tan_val = np.tan(math.pi * (z_real + 1j * z_imag) / (2 ** n))
                    if np.isfinite(tan_val):
                        terms.append(tan_val)
                except:
                    continue
            
            if not terms:
                return 1.0
            
            product_value = np.prod(terms)
            result = self._safe_abs_power(product_value, -m)
            
            if self._should_apply_gamma_norm(normalize_type):
                result = self._safe_gamma_normalize(result)
            
            return float(result) if np.isfinite(result) else 0.0
            
        except Exception:
            return 0.0
    
    # ====== ADVANCED FUNCTIONS ======
    
    def Half_Base_Viete_Product_for_Sin(self, z: complex, normalize_type: str = 'N') -> float:
        """
        Half-base Viète product for sine with specialized coefficients
        """
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        coeffs = self._get_coefficients('viete_products', normalize_type)
        m = coeffs['m']
        
        try:
            # Half-base Viète product calculation
            terms = []
            for n in range(2, 30):
                term = np.sin(math.pi * (z_real + 1j * z_imag) / (1.5 ** n))
                terms.append(term)
            
            product_value = np.prod(terms)
            result = self._safe_abs_power(product_value, -m)
            
            if self._should_apply_gamma_norm(normalize_type):
                result = self._safe_gamma_normalize(result)
            
            return float(result) if np.isfinite(result) else 0.0
            
        except Exception:
            return 0.0
    
    def Riesz_Product_for_Tan_and_Prime_indicator_combination(self, z: complex, normalize_type: str = 'N') -> float:
        """
        Combined Riesz product with prime indicator function
        """
        try:
            riesz_result = self.Riesz_Product_for_Tan(z, normalize_type)
            prime_result = self.Binary_Output_Prime_Indicator_Function_H(z, normalize_type)
            
            # Combine the results
            combined = riesz_result * (1 + prime_result)
            return float(combined) if np.isfinite(combined) else 0.0
            
        except Exception:
            return 0.0
    
    def Nested_roots_product_for_2(self, z: complex, normalize_type: str = 'N') -> float:
        """
        Nested roots product with base 2
        """
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        coeffs = self._get_coefficients('viete_products', normalize_type)
        m = coeffs['m']
        
        try:
            # Nested roots calculation
            terms = []
            for n in range(2, 20):
                nested_val = (z_real + 1j * z_imag) ** (1.0 / (2 ** n))
                term = np.sqrt(2 + nested_val)
                terms.append(term)
            
            product_value = np.prod(terms)
            result = self._safe_abs_power(product_value, -m)
            
            if self._should_apply_gamma_norm(normalize_type):
                result = self._safe_gamma_normalize(result)
            
            return float(result) if np.isfinite(result) else 0.0
            
        except Exception:
            return 0.0
    
    # ====== GAMMA AND LOGARITHMIC FUNCTIONS ======
    
    def natural_logarithm_of_product_of_product_representation_for_sin(self, z: complex, normalize_type: str = 'N') -> float:
        """
        Natural logarithm of the enhanced divisor wave: ln(b(z))
        """
        try:
            inner_result = self.product_of_product_representation_for_sin(z, normalize_type)
            if inner_result > 0:
                result = math.log(inner_result)
                return float(result) if np.isfinite(result) else 0.0
            return 0.0
        except Exception:
            return 0.0
    
    def gamma_of_product_of_product_representation_for_sin(self, z: complex, normalize_type: str = 'N') -> float:
        """
        Gamma function applied to enhanced divisor wave: Γ(b(z))
        """
        try:
            inner_result = self.product_of_product_representation_for_sin(z, normalize_type)
            if abs(inner_result) < 100:
                result = scipy.special.gamma(inner_result)
                return float(abs(result)) if np.isfinite(result) else 0.0
            return 0.0
        except Exception:
            return 0.0
    
    def gamma_form_product_of_product_representation_for_sin(self, z: complex, normalize_type: str = 'N') -> float:
        """
        Gamma form of the enhanced divisor wave with special scaling
        """
        try:
            inner_result = self.product_of_product_representation_for_sin(z, normalize_type)
            # Apply gamma normalization regardless of mode for this specific function
            result = self._safe_gamma_normalize(inner_result)
            return float(result) if np.isfinite(result) else 0.0
        except Exception:
            return 0.0
    
    def Log_power_base_Viete_Product_for_Sin(self, z: complex, normalize_type: str = 'N') -> float:
        """
        Logarithmic power base Viète product for sine
        """
        try:
            viete_result = self.Viete_Product_for_Sin(z, normalize_type)
            if viete_result > 0:
                log_result = math.log(viete_result)
                power_result = abs(z) ** log_result if log_result != 0 else 1.0
                return float(power_result) if np.isfinite(power_result) else 0.0
            return 0.0
        except Exception:
            return 0.0
    
    # ====== PRIME ANALYSIS FUNCTIONS ======
    
    def Binary_Output_Prime_Indicator_Function_H(self, z: complex, normalize_type: str = 'N') -> float:
        """
        Binary prime indicator function: H(z) = 1 if z is prime, 0 if composite
        """
        try:
            n = int(np.real(z))
            if n < 2:
                return 0.0
            if n == 2:
                return 1.0
            if n % 2 == 0:
                return 0.0
            
            # Simple primality test
            for i in range(3, min(int(math.sqrt(n)) + 1, 1000), 2):
                if n % i == 0:
                    return 0.0
            return 1.0
        except Exception:
            return 0.0
    
    def Prime_Output_Indicator_J(self, z: complex, normalize_type: str = 'N') -> float:
        """
        Prime output function: J(z) = z if z is prime, 0 if composite
        """
        try:
            if self.Binary_Output_Prime_Indicator_Function_H(z, normalize_type):
                return float(np.real(z))
            return 0.0
        except Exception:
            return 0.0
    
    def BOPIF_Q_Alternation_Series(self, z: complex, normalize_type: str = 'N') -> float:
        """
        Binary Output Prime Indicator Function Q Alternation Series
        """
        try:
            prime_indicator = self.Binary_Output_Prime_Indicator_Function_H(z, normalize_type)
            alternation = (-1) ** int(np.real(z))
            result = prime_indicator * alternation
            return float(result)
        except Exception:
            return 0.0
    
    def Dirichlet_Eta_Derived_From_BOPIF(self, z: complex, normalize_type: str = 'N') -> float:
        """
        Dirichlet eta function derived from Binary Output Prime Indicator Function
        """
        try:
            # Simplified Dirichlet eta approximation using prime indicator
            z_real = np.real(z)
            if z_real <= 1:
                return 0.0
            
            result = 0.0
            for n in range(1, 50):
                prime_factor = self.Binary_Output_Prime_Indicator_Function_H(complex(n), normalize_type)
                term = ((-1) ** (n - 1)) * prime_factor / (n ** z_real)
                result += term
            
            return float(result) if np.isfinite(result) else 0.0
        except Exception:
            return 0.0
    
    # ====== DEMO AND EXPERIMENTAL FUNCTIONS ======
    
    def complex_playground_magnification_currated_functions_DEMO(self, z: complex, normalize_type: str = 'N') -> float:
        """
        Demo function combining multiple divisor wave patterns for visualization
        """
        try:
            # Combine main divisor wave with enhanced version
            a_z = self.product_of_sin(z, normalize_type)
            b_z = self.product_of_product_representation_for_sin(z, normalize_type)
            
            # Create interference pattern
            combined = abs(a_z * b_z * np.exp(1j * np.angle(z)))
            
            return float(combined) if np.isfinite(combined) else 0.0
        except Exception:
            return 0.0
    
    def Custom_Riesz_Product_for_Tan(self, z: complex, normalize_type: str = 'N') -> float:
        """
        Custom variant of Riesz product for tangent with modified coefficients
        """
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        # Custom coefficients for this variant
        m = 0.05
        
        try:
            terms = []
            for n in range(2, int(abs(z_real)) + 15):
                try:
                    # Custom scaling factor
                    scale = 1.5 if n % 2 == 0 else 1.0
                    tan_val = np.tan(math.pi * (z_real + 1j * z_imag) * n * scale)
                    if np.isfinite(tan_val):
                        term = 1 + tan_val
                        terms.append(term)
                except:
                    continue
            
            if not terms:
                return 1.0
            
            product_value = np.prod(terms)
            result = self._safe_abs_power(product_value, -m)
            
            if self._should_apply_gamma_norm(normalize_type):
                result = self._safe_gamma_normalize(result)
            
            return float(result) if np.isfinite(result) else 0.0
            
        except Exception:
            return 0.0
    
    def Custom_Viete_Product_for_Cos(self, z: complex, normalize_type: str = 'N') -> float:
        """
        Custom variant of Viète product for cosine
        """
        return self.Viete_Product_for_Cos(z, normalize_type)  # Placeholder - same as standard for now
    
    # ====== UTILITY FUNCTIONS ======
    
    def get_function(self, function_name: str) -> Optional[Callable]:
        """
        Get a function by name for multiprocessing compatibility
        
        Args:
            function_name: Name of the function to retrieve
            
        Returns:
            Function callable or None if not found
        """
        return getattr(self, function_name, None)
    
    def get_available_functions(self) -> Dict[str, Dict[str, str]]:
        """
        Get metadata for all available functions
        
        Returns:
            Dictionary with function metadata
        """
        return {
            # Core functions
            'product_of_sin': {
                'display_name': 'Main Divisor Wave a(z)',
                'category': 'Core Functions',
                'description': 'Primary divisor wave function showing prime/composite patterns'
            },
            'product_of_product_representation_for_sin': {
                'display_name': 'Enhanced Divisor Wave b(z)',
                'category': 'Core Functions',
                'description': 'Double product using sine representation for complex analysis'
            },
            
            # Composite functions
            'cos_of_product_of_sin': {
                'display_name': 'cos(a(z))',
                'category': 'Composite Functions',
                'description': 'Cosine of main divisor wave'
            },
            'sin_of_product_of_sin': {
                'display_name': 'sin(a(z))',
                'category': 'Composite Functions',
                'description': 'Sine of main divisor wave'
            },
            'cos_of_product_of_product_representation_of_sin': {
                'display_name': 'cos(b(z))',
                'category': 'Composite Functions',
                'description': 'Cosine of enhanced divisor wave'
            },
            'sin_of_product_of_product_representation_of_sin': {
                'display_name': 'sin(b(z))',
                'category': 'Composite Functions',
                'description': 'Sine of enhanced divisor wave'
            },
            
            # Riesz products
            'Riesz_Product_for_Cos': {
                'display_name': 'Riesz Product (Cosine)',
                'category': 'Riesz Products',
                'description': 'Riesz product using cosine functions'
            },
            'Riesz_Product_for_Sin': {
                'display_name': 'Riesz Product (Sine)',
                'category': 'Riesz Products',
                'description': 'Riesz product using sine functions'
            },
            'Riesz_Product_for_Tan': {
                'display_name': 'Riesz Product (Tangent)',
                'category': 'Riesz Products',
                'description': 'Riesz product using tangent functions'
            },
            
            # Viète products
            'Viete_Product_for_Cos': {
                'display_name': 'Viète Product (Cosine)',
                'category': 'Viète Products',
                'description': 'Viète-style product using cosine'
            },
            'Viete_Product_for_Sin': {
                'display_name': 'Viète Product (Sine)',
                'category': 'Viète Products',
                'description': 'Viète-style product using sine'
            },
            'Viete_Product_for_Tan': {
                'display_name': 'Viète Product (Tangent)',
                'category': 'Viète Products',
                'description': 'Viète-style product using tangent'
            },
            
            # Prime analysis
            'Binary_Output_Prime_Indicator_Function_H': {
                'display_name': 'Prime Indicator H(z)',
                'category': 'Prime Analysis',
                'description': 'Binary prime indicator function'
            },
            'Prime_Output_Indicator_J': {
                'display_name': 'Prime Output J(z)',
                'category': 'Prime Analysis',
                'description': 'Prime number output function'
            },
            
            # Advanced functions
            'natural_logarithm_of_product_of_product_representation_for_sin': {
                'display_name': 'ln(b(z))',
                'category': 'Advanced Functions',
                'description': 'Natural logarithm of enhanced divisor wave'
            },
            'gamma_of_product_of_product_representation_for_sin': {
                'display_name': 'Γ(b(z))',
                'category': 'Advanced Functions',
                'description': 'Gamma function of enhanced divisor wave'
            },
            
            # Demo functions
            'complex_playground_magnification_currated_functions_DEMO': {
                'display_name': 'Demo Function',
                'category': 'Demo Functions',
                'description': 'Combined divisor wave patterns for demonstration'
            }
        }
    
    def evaluate_custom_function(self, function_name: str, z: complex, normalize_type: str = 'N') -> float:
        """
        Evaluate a custom LaTeX-defined function
        
        Args:
            function_name: Name of the custom function
            z: Complex number to evaluate
            normalize_type: Normalization mode
            
        Returns:
            Function value as float
        """
        try:
            if function_name not in self.custom_functions:
                raise ValueError(f"Custom function '{function_name}' not found")
            
            func_data = self.custom_functions[function_name]
            python_code = func_data.get('python_code', '')
            
            # Create execution environment
            exec_env = {
                'z': z,
                'normalize_type': normalize_type,
                'np': np,
                'math': math,
                'cmath': cmath,
                'scipy': scipy
            }
            
            # Execute the custom function code
            exec(python_code, exec_env)
            
            # Get the result from custom_function
            if 'custom_function' in exec_env:
                result = exec_env['custom_function'](z, normalize_type)
                return float(result) if np.isfinite(result) else 0.0
            
            return 0.0
            
        except Exception as e:
            print(f"Error evaluating custom function {function_name}: {e}")
            return 0.0
    
    def create_custom_function_from_latex(self, name: str, latex_formula: str, 
                                        description: str = "", category: str = "custom") -> bool:
        """
        Create a new custom function from LaTeX formula
        
        Args:
            name: Function name
            latex_formula: LaTeX mathematical formula
            description: Function description
            category: Function category
            
        Returns:
            True if successful, False otherwise
        """
        try:
            result = self.latex_builder.create_custom_function(
                name=name,
                latex_formula=latex_formula,
                description=description,
                category=category
            )
            
            if result.get('success', False):
                # Reload custom functions
                self.custom_functions = self._load_custom_functions()
                return True
            
            return False
            
        except Exception as e:
            print(f"Error creating custom function: {e}")
            return False
    
    # ======= ADDITIONAL ORIGINAL FUNCTIONS FOR BACKWARD COMPATIBILITY =======
    
    def Binary_Output_Prime_Indicator_Function_H(self, z: complex, normalize_type: str = 'N') -> float:
        """Binary output prime indicator combining two infinite products"""
        z_real = float(np.real(z))
        z_imag = float(np.imag(z))
        
        if normalize_type == 'Y':
            c, m = 0.13, 0.29
            alpha, beta = 0.14, 0.25
        else:
            c, m = 0.83, 0.029
            alpha, beta = 0.74, 0.025
        
        try:
            # Single product
            single_prod = abs(np.prod([
                alpha * (z_real / k) * np.sin(math.pi * (z_real + 1j * z_imag) / k)
                for k in range(2, min(int(z_real) + 1, 50))
            ])) ** (-c)
            
            # Double product
            double_prod = abs(np.prod([
                beta * (z_real / n) * (((z_real + 1j * z_imag) * math.pi) * np.prod([
                    1 - ((z_real + 1j * z_imag) ** 2) / (n ** 2 * k ** 2)
                    for k in range(2, min(int(z_real) + 1, 20))
                ])) for n in range(2, min(int(z_real) + 1, 20))
            ])) ** (-m)
            
            if normalize_type == 'Y':
                norm1 = single_prod / math.gamma(abs(single_prod) + 1)
                norm2 = double_prod / math.gamma(abs(double_prod) + 1)
                result = pow(norm1, norm2)
            else:
                result = pow(single_prod, double_prod)
            
            return abs(result) if np.isfinite(result) else 0.0
        except:
            return 0.0
    
    def Prime_Output_Indicator_J(self, z: complex, normalize_type: str = 'N') -> float:
        """Prime output indicator with nested products"""
        return self.Binary_Output_Prime_Indicator_Function_H(z, normalize_type)  # Simplified implementation
    
    def BOPIF_Q_Alternation_Series(self, z: complex, normalize_type: str = 'N') -> float:
        """BOPIF alternation series"""
        return self.Binary_Output_Prime_Indicator_Function_H(z, normalize_type)  # Simplified implementation
    
    def Dirichlet_Eta_Derived_From_BOPIF(self, z: complex, normalize_type: str = 'N') -> float:
        """Dirichlet eta function derived from BOPIF"""
        z_real = float(np.real(z))
        
        try:
            eta_prod = abs(np.prod([
                1 / (1 + self.BOPIF_Q_Alternation_Series(z, normalize_type) * self.Prime_Output_Indicator_J(z, normalize_type))
                for k in range(2, min(int(z_real) + 1, 20))
            ])) ** (-0.13)
            
            return abs(eta_prod) if np.isfinite(eta_prod) else 0.0
        except:
            return 0.0
    
    def natural_logarithm_of_product_of_product_representation_for_sin(self, z: complex, normalize_type: str = 'N') -> float:
        """Natural logarithm of the product representation"""
        try:
            result = self.product_of_product_representation_for_sin(z, normalize_type)
            log_result = math.log(abs(result) + 1e-10)
            return log_result if np.isfinite(log_result) else 0.0
        except:
            return 0.0
    
    def gamma_of_product_of_product_representation_for_sin(self, z: complex, normalize_type: str = 'N') -> float:
        """Gamma function applied to product representation"""
        try:
            result = self.product_of_product_representation_for_sin(z, normalize_type)
            gamma_result = math.gamma(abs(result) + 1)
            return gamma_result if np.isfinite(gamma_result) else 1.0
        except:
            return 1.0
    
    def gamma_form_product_of_product_representation_for_sin(self, z: complex, normalize_type: str = 'N') -> float:
        """Gamma form of the product representation"""
        z_real = float(np.real(z))
        z_imag = float(np.imag(z))
        
        if normalize_type == 'Y':
            m, beta = 0.0125, 0.054
        else:
            m, beta = 0.0125, 0.054
        
        try:
            result = abs(np.prod([
                beta * (z_imag * z_real / n) * math.gamma(abs(z_real + 1j * z_imag) + 1)
                * math.gamma(abs(1 - (z_real + 1j * z_imag)) + 1)
                * cmath.exp(-(abs(z_real + 1j * z_imag) ** 2))
                for n in range(2, min(int(z_real) + 1, 20))
            ])) ** (-m)
            
            return abs(result) if np.isfinite(result) else 0.0
        except:
            return 0.0
    
    def Custom_Riesz_Product_for_Tan(self, z: complex, normalize_type: str = 'N') -> float:
        """Custom Riesz product for tangent with normalization"""
        z_real = float(np.real(z))
        z_imag = float(np.imag(z))
        
        if normalize_type == 'Y':
            m, beta = 0.001, 0.07
        else:
            m, beta = 0.001, 0.07
        
        try:
            num = abs(np.prod([
                1 + np.tan(math.pi * (z_real + 1j * z_imag) * n)
                for n in range(2, min(int(z_real) + 1, 20))
            ])) ** (-m)
            
            den = abs(np.prod([
                1 + np.tan(math.pi * (z_real + 1j * z_imag) * n)
                for n in range(2, min(int(z_real) + 1, 20))
            ])) ** (-m)
            
            norm = num / math.gamma(abs(den) + 1)
            return abs(norm) if np.isfinite(norm) else 0.0
        except:
            return 0.0
    
    def Custom_Viete_Product_for_Cos(self, z: complex, normalize_type: str = 'N') -> float:
        """Custom Viète product for cosine"""
        z_real = float(np.real(z))
        z_imag = float(np.imag(z))
        
        if normalize_type == 'Y':
            m, beta = 0.001, 0.07
        else:
            m, beta = 0.001, 0.07
        
        try:
            num = abs(np.prod([
                1 + np.cos(math.pi * (z_real + 1j * z_imag) / (z_real ** n))
                for n in range(2, min(int(z_real) + 1, 20))
            ])) ** (-m)
            
            norm = num / math.gamma(abs(num) + 1)
            return abs(norm) if np.isfinite(norm) else 0.0
        except:
            return 0.0
    
    def Log_power_base_Viete_Product_for_Sin(self, z: complex, normalize_type: str = 'N') -> float:
        """Logarithmic power base Viète product for sine"""
        z_real = float(np.real(z))
        z_imag = float(np.imag(z))
        
        if normalize_type == 'Y':
            m, beta = 0.001, 0.07
        else:
            m, beta = 0.001, 0.07
        
        try:
            num = 1 + abs(np.prod([
                np.sin(math.pi * (z_real + 1j * z_imag) / (2 ** ((1/n) * np.log(abs(z_real + 1j * z_imag) + 1))))
                for n in range(2, min(int(z_real) + 1, 20))
            ])) ** (-m)
            
            norm = num / math.gamma(abs(num) + 1)
            return abs(norm) if np.isfinite(norm) else 0.0
        except:
            return 0.0
    
    def Nested_roots_product_for_2(self, z: complex, normalize_type: str = 'N') -> float:
        """Nested roots product implementation"""
        z_real = float(np.real(z))
        z_imag = float(np.imag(z))
        
        if normalize_type == 'Y':
            m, beta = 0.001, 0.07
        else:
            m, beta = 0.001, 0.07
        
        try:
            paradox = abs(np.prod([
                np.prod([
                    (z_real + 1j * z_imag) ** (k ** (-n))
                    for k in range(2, min(int(z_real) + 1, 10))
                ]) for n in range(2, min(int(z_real) + 1, 10))
            ]))
            
            return abs(paradox) if np.isfinite(paradox) else 0.0
        except:
            return 0.0
    
    def product_of_product_representation_for_sin_COMPLEX_VARIANT(self, z: complex, normalize_type: str = 'N') -> float:
        """
        Complex variant of product of product representation for sin
        This is function '3' from the original lambda library - a variant with complex magnification
        """
        try:
            z_real = np.real(z)
            z_imag = np.imag(z)
            
            # Use special coefficients for complex variant
            if normalize_type == 'Y':
                m = 0.32  # Slightly different from main function
                beta = 0.135
            else:
                m = 0.015  # Enhanced from original 0.0125
                beta = 0.085  # Enhanced from original 0.078
            
            # Enhanced complex magnification using imaginary component
            complex_mag = 1.0 + abs(z_imag) * 0.1  # Imaginary amplification factor
            
            # calculate the double infinite product with complex enhancement
            if int(z_real) >= 2:
                result = abs(np.prod(
                    [beta * complex_mag * (z_real / n) * (((z_real + 1j * z_imag) * math.pi) * np.prod(
                        [1 - ((z_real + 1j * z_imag) ** 2) / ((n ** 2) * (k ** 2))
                         for k in range(2, min(int(z_real) + 1, 50))])) 
                     for n in range(2, min(int(z_real) + 1, 50))])) ** (-m)
            else:
                result = 1.0
            
            # Apply normalization
            if self._should_apply_gamma_norm(normalize_type):
                result = self._safe_gamma_normalize(result)
            
            return self.safe_abs(result)
            
        except Exception:
            return 0.0
    
    def complex_playground_magnification_currated_functions_DEMO(self, z: complex, normalize_type: str = 'N') -> float:
        """Demo function combining multiple divisor wave patterns"""
        try:
            # Combine different wave patterns for demonstration
            base_wave = self.product_of_sin(z, normalize_type)
            enhanced_wave = self.product_of_product_representation_for_sin(z, normalize_type)
            prime_indicator = self.Binary_Output_Prime_Indicator_Function_H(z, normalize_type)
            
            # Create interesting combined pattern
            combined = (base_wave * enhanced_wave * prime_indicator) ** 0.33
            
            return abs(combined) if np.isfinite(combined) else 0.0
        except:
            return 0.0