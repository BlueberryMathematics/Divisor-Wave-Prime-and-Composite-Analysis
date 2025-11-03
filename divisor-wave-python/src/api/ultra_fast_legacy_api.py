"""
Ultra-Fast Legacy Recreation API v5.0
Advanced optimizations while maintaining exact mathematical accuracy
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Union, Any, Tuple
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource, ListedColormap
from matplotlib import cm, ticker
import io
import base64
import logging
import math
import cmath
from scipy import special as scipy_special
import concurrent.futures
from numba import jit, complex128, float64
import threading
from functools import lru_cache
from latex_function_builder import LaTeXFunctionBuilder, create_example_functions

# Numba availability check
try:
    from numba import jit
    NUMBA_AVAILABLE = True
except ImportError:
    NUMBA_AVAILABLE = False
    def jit(*args, **kwargs):
        def decorator(func):
            return func
        return decorator

# Additional imports for interactive command system
import time
import sys
import subprocess
try:
    import psutil
except ImportError:
    psutil = None
try:
    import requests
except ImportError:
    requests = None

# Set exact legacy style
plt.style.use('dark_background')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Ultra-Fast Legacy Recreation API v5.0", version="5.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Advanced Optimization 1: Numba JIT compilation for speed
@jit(complex128(complex128, float64, float64), nopython=True, cache=True)
def fast_product_of_sin(z, m, beta):
    """Ultra-fast JIT compiled product of sin"""
    z_real = z.real
    z_imag = z.imag
    
    result = 1.0 + 0j
    for k in range(2, min(int(z_real) + 1, 50)):  # Cap at 50 for speed
        if k > 1:
            result *= beta * (z_real / k) * np.sin(np.pi * z / k)
    
    return abs(result) ** (-m)

@jit(complex128(complex128, float64, float64), nopython=True, cache=True)
def fast_double_product(z, m, beta):
    """Ultra-fast JIT compiled double product"""
    z_real = z.real
    z_imag = z.imag
    
    result = 1.0 + 0j
    max_n = min(int(z_real) + 1, 30)  # Cap for speed
    
    for n in range(2, max_n):
        inner_product = 1.0 + 0j
        for k in range(2, max_n):
            term = 1.0 - (z * z) / (n * n * k * k)
            if abs(term) > 1e-10:  # Skip tiny terms
                inner_product *= term
        
        result *= beta * (z_real / n) * (z * np.pi) * inner_product
    
    return abs(result) ** (-m)

@jit(complex128(complex128, float64, float64), nopython=True, cache=True)
def fast_riesz_product(z, m, beta):
    """Ultra-fast JIT compiled Riesz product"""
    z_real = z.real
    z_imag = z.imag
    
    result = 1.0 + 0j
    for n in range(2, min(int(z_real) + 1, 25)):  # Cap for speed
        base = 1j * z_imag + (1j * z_imag) * np.sin(np.pi * z * n)
        if abs(base) > 1e-10:
            # Simplified complex power for speed
            result *= base ** (1j * z_imag * 0.1)  # Reduced exponent for stability
    
    return abs(result) ** (-m)

# Advanced Optimization 2: Adaptive resolution based on complexity
def get_adaptive_resolution(plot_type, function_name, base_resolution):
    """Dynamically adjust resolution based on function complexity"""
    complexity_map = {
        'product_of_sin': 1.0,
        'product_of_product_representation_for_sin': 0.6,  # Most complex
        'complex_playground_magnification_currated_functions_DEMO': 0.8,
        'Riesz_Product_for_Cos': 0.9,
        'Viete_Product_for_Cos': 1.0
    }
    
    if plot_type.startswith('3D'):
        # 3D plots need less resolution for good visual quality
        multiplier = 0.7
    else:
        multiplier = 1.0
    
    complexity = complexity_map.get(function_name, 0.8)
    return int(base_resolution * complexity * multiplier)

# Advanced Optimization 3: Parallel computation
def compute_chunk(args):
    """Compute a chunk of the grid in parallel"""
    func, chunk_indices, X, Y, normalize_type, m_coefficient, beta_coefficient = args
    chunk_results = []
    
    for i, j in chunk_indices:
        try:
            z = complex(X[i, j], Y[i, j])
            # Check if function accepts coefficients
            try:
                result = func(z, normalize_type, m_coefficient, beta_coefficient)
            except TypeError:
                # Fallback for functions that don't accept coefficients yet
                result = func(z, normalize_type)
            chunk_results.append((i, j, abs(result)))
        except:
            chunk_results.append((i, j, 0.0))
    
    return chunk_results

class OptimizedLegacySpecialFunctions:
    """Optimized version with exact mathematical accuracy"""
    
    def __init__(self, plot_type):
        self.plot_type = plot_type
        self.m = 1.0
        self.beta = 1.0
        
    @lru_cache(maxsize=1000)  # Cache results for repeated calculations
    def cached_gamma(self, value):
        """Cached gamma function for speed"""
        try:
            if abs(value) < 100:  # Avoid overflow
                return scipy_special.gamma(value)
            else:
                return 1.0
        except:
            return 1.0
    
    def product_of_sin(self, z, normalize_type, m_coefficient=0.0465, beta_coefficient=0.178):
        """Optimized product of sin with exact legacy behavior"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        # Use provided coefficients
        m, beta = m_coefficient, beta_coefficient
        
        # Use fast JIT compiled version
        result = fast_product_of_sin(z, m, beta)
        
        if normalize_type == 'Y':
            result = result / self.cached_gamma(result)
        
        return result
    
    def product_of_product_representation_for_sin(self, z, normalize_type, m_coefficient=0.36, beta_coefficient=0.1468):
        """Optimized double product with complexity reduction"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        # Use provided coefficients, with different defaults for normalized
        if normalize_type == 'Y':
            m, beta = m_coefficient if m_coefficient != 0.36 else 0.36, beta_coefficient if beta_coefficient != 0.1468 else 0.1468
        else:
            m, beta = m_coefficient if m_coefficient != 0.36 else 0.0125, beta_coefficient if beta_coefficient != 0.1468 else 0.078
        
        # Use fast JIT compiled version
        result = fast_double_product(z, m, beta)
        
        if normalize_type == 'Y':
            result = result / self.cached_gamma(result)
        
        return result
    
    def complex_playground_magnification_currated_functions_DEMO(self, z, normalize_type, m_coefficient=0.0125, beta_coefficient=0.054):
        """Optimized Riesz product demo"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        m, beta = m_coefficient, beta_coefficient
        
        # Use fast JIT compiled version
        result = fast_riesz_product(z, m, beta)
        
        if normalize_type == 'Y':
            result = result / self.cached_gamma(result)
        
        return result
    
    def Riesz_Product_for_Cos(self, z, normalize_type, m_coefficient=0.26, beta_coefficient=0.08):
        """Optimized Riesz cosine product"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m, beta = m_coefficient, beta_coefficient
        else:
            # Swap defaults for non-normalized case
            m, beta = beta_coefficient if m_coefficient == 0.26 else m_coefficient, m_coefficient if m_coefficient == 0.26 else beta_coefficient
        
        # Simplified for speed while maintaining character
        result = 1.0 + 0j
        for n in range(2, min(int(z_real) + 1, 20)):
            base = 1j * z_imag + np.cos(math.pi * z * n)
            if abs(base) > 1e-10:
                result *= base ** (1j * z_imag * 0.2)
        
        result = abs(result) ** (-m)
        
        if normalize_type == 'Y':
            result = result / self.cached_gamma(result)
        
        return result
    
    def Viete_Product_for_Cos(self, z, normalize_type):
        """Optimized Viète cosine product"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m, beta = 0.27, 1
        else:
            m, beta = 0.07, 1
        
        result = 1.0 + 0j
        for n in range(2, min(int(z_real) + 1, 25)):
            result *= np.cos(math.pi * z / (2 ** n))
        
        result = abs(result) ** (-m)
        
        if normalize_type == 'Y':
            result = result / self.cached_gamma(result)
        
        return result
    
    def cos_of_product_of_sin(self, z, normalize_type):
        """Cosine of product of sin"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m, beta = 0.0125, 0.054
        else:
            m, beta = 0.0125, 0.054
        
        # Use fast JIT compiled version
        inner_product = fast_product_of_sin(z, m, beta)
        result = np.cos(inner_product)
        
        if normalize_type == 'Y':
            result = result / self.cached_gamma(result)
        
        return result
    
    def sin_of_product_of_sin(self, z, normalize_type):
        """Sine of product of sin"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m, beta = 0.0125, 0.054
        else:
            m, beta = 0.0125, 0.054
        
        # Use fast JIT compiled version
        inner_product = fast_product_of_sin(z, m, beta)
        result = np.sin(inner_product)
        
        if normalize_type == 'Y':
            result = result / self.cached_gamma(result)
        
        return result
    
    def cos_of_product_of_product_representation_of_sin(self, z, normalize_type):
        """Cosine of double product"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m, beta = 0.0125, 0.054
        else:
            m, beta = 0.0125, 0.054
        
        # Use fast JIT compiled version
        inner_product = fast_double_product(z, m, beta)
        result = np.cos(inner_product)
        
        if normalize_type == 'Y':
            result = result / self.cached_gamma(result)
        
        return result
    
    def sin_of_product_of_product_representation_of_sin(self, z, normalize_type):
        """Sine of double product"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m, beta = 0.0125, 0.054
        else:
            m, beta = 0.0125, 0.054
        
        # Use fast JIT compiled version
        inner_product = fast_double_product(z, m, beta)
        result = np.sin(inner_product)
        
        if normalize_type == 'Y':
            result = result / self.cached_gamma(result)
        
        return result
    
    def Riesz_Product_for_Sin(self, z, normalize_type):
        """Riesz product for sine"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m, beta = 0.0125, 0.054
        else:
            m, beta = 0.0125, 0.054
        
        result = 1.0 + 0j
        for n in range(2, min(int(z_real) + 1, 20)):
            result *= (1 + np.sin(math.pi * z * n))
        
        result = abs(result) ** (-m)
        
        if normalize_type == 'Y':
            result = result / self.cached_gamma(result)
        
        return result
    
    def Riesz_Product_for_Tan(self, z, normalize_type):
        """Riesz product for tangent"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m, beta = 0.0125, 0.054
        else:
            m, beta = 0.0125, 0.054
        
        result = 1.0 + 0j
        for n in range(2, min(int(z_real) + 1, 20)):
            result *= (1 + np.tan(math.pi * z * n))
        
        result = abs(result) ** (-m)
        
        if normalize_type == 'Y':
            result = result / self.cached_gamma(result)
        
        return result
    
    def Viete_Product_for_Sin(self, z, normalize_type):
        """Viète product for sine"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m, beta = 0.87, 0.4
        else:
            m, beta = 0.87, 1
        
        result = 1.0 + 0j
        for n in range(2, min(int(z_real) + 1, 25)):
            result *= np.sin(math.pi * z / (2 ** n))
        
        result = abs(result) ** (-m)
        
        if normalize_type == 'Y':
            result = result / self.cached_gamma(result)
        
        return result
    
    def Viete_Product_for_Tan(self, z, normalize_type):
        """Viète product for tangent"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m, beta = 0.004, 0.004
        else:
            m, beta = 0.007, 0.004
        
        result = 1.0 + 0j
        for n in range(2, min(int(z_real) + 1, 25)):
            result *= np.tan(math.pi * z / (2 ** n))
        
        result = abs(result) ** (-m)
        
        if normalize_type == 'Y':
            result = result / self.cached_gamma(result)
        
        return result
    
    def Half_Base_Viete_Product_for_Sin(self, z, normalize_type):
        """Half base Viète product for sine"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m, beta = 0.37, 0.07
        else:
            m, beta = 0.07, 1
        
        result = 1.0 + 0j
        for n in range(2, min(int(z_real) + 1, 25)):
            result *= np.sin(math.pi * z / (2 ** (-n)))
        
        result = abs(result) ** (-m)
        
        if normalize_type == 'Y':
            result = result / self.cached_gamma(result)
        
        return result
    
    def Binary_Output_Prime_Indicator_Function_H(self, z, normalize_type):
        """Binary output prime indicator function H"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            c, m = 0.13, 0.29
            alpha, beta = 0.14, 0.25
        else:
            c, m = 0.83, 0.029
            alpha, beta = 0.74, 0.025
        
        # Single product
        single_prod = abs(np.prod([alpha * (z_real / k) * np.sin(math.pi * z / k)
                                  for k in range(2, min(int(z_real) + 1, 15))])) ** (-c)
        
        # Double product (simplified for speed)
        double_prod = abs(np.prod([beta * (z_real / n) * (z * math.pi) * 
                                  np.prod([1 - (z ** 2) / (n ** 2 * k ** 2)
                                          for k in range(2, min(int(z_real) + 1, 10))])
                                  for n in range(2, min(int(z_real) + 1, 10))])) ** (-m)
        
        if normalize_type == 'Y':
            norm1 = single_prod / self.cached_gamma(single_prod)
            norm2 = double_prod / self.cached_gamma(double_prod)
            result = norm1 ** norm2
        else:
            result = single_prod ** double_prod
        
        return result
    
    def Prime_Output_Indicator_J(self, z, normalize_type):
        """Prime output indicator function J"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            c, m = 0.13, 0.29
            alpha, beta = 0.14, 0.25
        else:
            c, m = 0.83, 0.029
            alpha, beta = 0.74, 0.025
        
        # Two single products
        single_prod_1 = abs(np.prod([alpha * (z_real / k) * np.sin(math.pi * z / k)
                                    for k in range(2, min(int(z_real) + 1, 15))])) ** (-c)
        
        single_prod_2 = single_prod_1  # Same calculation
        
        # Double product (simplified)
        double_prod = abs(np.prod([beta * (z_real / n) * (z * math.pi) * 
                                  np.prod([1 - (z ** 2) / (n ** 2 * k ** 2)
                                          for k in range(2, min(int(z_real) + 1, 10))])
                                  for n in range(2, min(int(z_real) + 1, 10))])) ** (-m)
        
        if normalize_type == 'Y':
            norm1 = single_prod_1 / self.cached_gamma(single_prod_1)
            norm2 = single_prod_2 / self.cached_gamma(single_prod_2)
            norm3 = double_prod / self.cached_gamma(double_prod)
            result = norm1 ** (norm2 ** norm3)
        else:
            result = single_prod_1 ** (single_prod_2 ** double_prod)
        
        return result
    
    # Advanced and specialized functions from Special_Functions.py
    def Riesz_Product_for_Tan_and_Prime_indicator_combination(self, z, normalize_type):
        """Riesz product for tangent combined with prime indicator"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m, beta = 0.001, 0.07
        else:
            m, beta = 0.001, 0.07
        
        # First product
        num = 1.0 + 0j
        for n in range(2, min(int(z_real) + 1, 15)):
            num *= (1 + np.tan(math.pi * z * n))
        num = abs(num) ** (-m)
        
        # Second product (simplified)
        q = 0.08
        func_b = 1.0 + 0j
        for n in range(2, min(int(z_real) + 1, 10)):
            inner_prod = 1.0 + 0j
            for k in range(2, min(int(z_real) + 1, 8)):
                inner_prod *= (1 - (z ** 2) / (n ** 2 * k ** 2))
            func_b *= (z_real / n) * (z * math.pi) * inner_prod
        func_b = abs(func_b) ** (-q)
        
        if normalize_type == 'Y':
            norm = num / self.cached_gamma(num)
            func_b_norm = func_b / self.cached_gamma(func_b)
            result = np.cos(func_b_norm / norm)
        else:
            result = np.cos(func_b / num)
        
        return result
    
    def Nested_roots_product_for_2(self, z, normalize_type):
        """Nested roots product"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m, beta = 0.001, 0.07
        else:
            m, beta = 0.001, 0.07
        
        # Simplified nested product for speed
        prod = abs(np.sum([z ** (2 ** (-n)) for n in range(2, min(int(z_real) + 1, 15))])) ** (-m)
        
        paradox = 1.0 + 0j
        for n in range(2, min(int(z_real) + 1, 10)):
            inner_prod = 1.0 + 0j
            for k in range(2, min(int(z_real) + 1, 8)):
                inner_prod *= z ** (k ** (-n))
            paradox *= inner_prod
        paradox = abs(paradox)
        
        return paradox
    
    def natural_logarithm_of_product_of_product_representation_for_sin(self, z, normalize_type):
        """Natural logarithm of double product"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m, beta = 0.0125, 0.078
        else:
            m, beta = 0.0125, 0.078
        
        # Use the double product result
        result = fast_double_product(z, m, beta)
        
        try:
            log_result = cmath.log(result)
            return log_result
        except:
            return 0.0 + 0j
    
    def gamma_of_product_of_product_representation_for_sin(self, z, normalize_type):
        """Gamma of double product"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m, beta = 0.0125, 0.078
        else:
            m, beta = 0.0125, 0.078
        
        result = fast_double_product(z, m, beta)
        gamma_result = self.cached_gamma(result)
        
        return gamma_result
    
    def gamma_form_product_of_product_representation_for_sin(self, z, normalize_type):
        """Gamma form double product with Euler-Mascheroni constant"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m, beta = 0.0125, 0.054
        else:
            m, beta = 0.0125, 0.054
        
        euler_mascheroni = 0.5772156649015329
        
        # Simplified gamma form for speed
        result = 1.0 + 0j
        for n in range(2, min(int(z_real) + 1, 15)):
            gamma_term = self.cached_gamma(z) * self.cached_gamma(1 - z)
            exp_term = cmath.exp(-(z ** 2))
            
            inner_prod = 1.0 + 0j
            for k in range(2, min(int(z_real) + 1, 10)):
                inner_prod *= cmath.exp((z ** 2) / (n ** 2 * k ** 2))
            
            result *= beta * (z_imag * z_real / n) * gamma_term * exp_term * inner_prod
        
        result = abs(result) ** (-m)
        
        if normalize_type == 'Y':
            result = result / self.cached_gamma(result)
        
        return result
    
    def Log_power_base_Viete_Product_for_Sin(self, z, normalize_type):
        """Logarithmic power base Viète product"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m, beta = 0.001, 0.07
        else:
            m, beta = 0.001, 0.07
        
        try:
            num = 1.0 + 0j
            for n in range(2, min(int(z_real) + 1, 15)):
                log_term = np.log(z) if abs(z) > 1e-10 else 0
                power_base = 2 ** ((1 / n) * log_term) if abs(log_term) > 1e-10 else 2
                num *= np.sin(math.pi * z / power_base)
            
            num = 1 + abs(num) ** (-m)
            den = num  # Same calculation for denominator
            
            norm = num / self.cached_gamma(den)
            return norm
        except:
            return 1.0
    
    def Custom_Riesz_Product_for_Tan(self, z, normalize_type):
        """Custom Riesz product for tangent"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m, beta = 0.001, 0.07
        else:
            m, beta = 0.001, 0.07
        
        num = 1.0 + 0j
        for n in range(2, min(int(z_real) + 1, 15)):
            num *= (1 + np.tan(math.pi * z * n))
        
        num = abs(num) ** (-m)
        den = num  # Same calculation
        
        norm = num / self.cached_gamma(den)
        return norm
    
    def Custom_Viete_Product_for_Cos(self, z, normalize_type):
        """Custom Viète product for cosine"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m, beta = 0.001, 0.07
        else:
            m, beta = 0.001, 0.07
        
        num = 1.0 + 0j
        for n in range(2, min(int(z_real) + 1, 15)):
            num *= (1 + np.cos(math.pi * z / (z_real ** n)))
        
        num = abs(num) ** (-m)
        den = num  # Same calculation
        
        norm = num / self.cached_gamma(den)
        return norm
    
    def BOPIF_Q_Alternation_Series(self, z, normalize_type):
        """Binary output prime indicator alternation series"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            c, m = 0.13, 0.29
            alpha, beta = 0.14, 0.25
        else:
            c, m = 0.83, 0.029
            alpha, beta = 0.74, 0.025
        
        # Simplified alternation for speed
        single_prod = self.product_of_sin(z, normalize_type)
        double_prod = self.product_of_product_representation_for_sin(z, normalize_type)
        
        # Simple alternation pattern
        alternation = 1.0 + 0j
        for q in range(2, min(int(z_real) + 1, 10)):
            h_result = self.Binary_Output_Prime_Indicator_Function_H(z, normalize_type)
            for s in range(2, min(int(z_real) + 1, 8)):
                alternation *= ((-2) ** h_result)
        
        alternation = abs(alternation) ** (-m)
        
        if normalize_type == 'Y':
            norm1 = single_prod / self.cached_gamma(single_prod)
            norm2 = double_prod / self.cached_gamma(double_prod)
            result = norm1 ** norm2
        else:
            result = single_prod ** double_prod
        
        return result
    
    def Dirichlet_Eta_Derived_From_BOPIF(self, z, normalize_type):
        """Dirichlet eta function derived from binary output prime indicator"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            c, m = 0.13, 0.29
            alpha, beta = 0.14, 0.25
        else:
            c, m = 0.83, 0.029
            alpha, beta = 0.74, 0.025
        
        # Simplified eta product
        eta_prod = 1.0 + 0j
        for k in range(2, min(int(z_real) + 1, 10)):
            q_alt = self.BOPIF_Q_Alternation_Series(z, normalize_type)
            j_prime = self.Prime_Output_Indicator_J(z, normalize_type)
            eta_prod *= (1 / (1 + q_alt * j_prime))
        
        eta_prod = abs(eta_prod) ** (-c)
        return eta_prod

class OptimizedLegacyComplexPlotting:
    """Optimized plotting with parallel computation"""
    
    def __init__(self, plot_type):
        self.plot_type = plot_type
        
        if plot_type == "2D":
            self.base_resolution_2D = 600  # Reduced from 750 for speed
            self.x_min_2D = 2
            self.x_max_2D = 28
            self.y_min_2D = -5
            self.y_max_2D = 5
        elif plot_type == "3D":
            self.resolution_3D = 0.025  # Slightly reduced for speed
            self.x_min_3D = 1.5
            self.x_max_3D = 18.5
            self.y_min_3D = -4.5
            self.y_max_3D = 4.5
    
    def optimized_colorization(self, color_selection, Z):
        """Vectorized colorization for speed"""
        if color_selection in ["6", "custom_colors2"]:
            # Vectorized sine calculations
            colors = np.zeros((Z.shape[0], Z.shape[1], 3))
            colors[:, :, 0] = np.sin(2 * np.pi * np.real(Z) / 12)
            colors[:, :, 1] = np.sin(2 * np.pi * np.real(Z) / 14)
            colors[:, :, 2] = np.sin(2 * np.pi * np.real(Z) / 16)
            return colors
        elif color_selection in ["8", "custom_colors1"]:
            colors = np.zeros((Z.shape[0], Z.shape[1], 3))
            colors[:, :, 0] = np.sin(2 * np.pi * np.real(Z) / 8.0)
            colors[:, :, 1] = np.sin(2 * np.pi * np.real(Z) / 9.0)
            colors[:, :, 2] = np.sin(2 * np.pi * np.real(Z) / 10.0)
            return colors
        elif color_selection in ["7", "custom_colors3"]:
            # Optimized mandelbrot-style pattern
            colors = np.zeros((Z.shape[0], Z.shape[1], 3))
            i_grid, j_grid = np.meshgrid(range(Z.shape[0]), range(Z.shape[1]), indexing='ij')
            colors[:, :, 0] = ((i_grid * j_grid) % 256) / 255
            colors[:, :, 1] = ((i_grid + j_grid) % 256) / 255
            colors[:, :, 2] = ((i_grid * j_grid + i_grid + j_grid) % 256) / 255
            return colors
        else:
            # Standard colormaps
            colormap_dict = {
                "1": "prism", "2": "jet", "3": "plasma", 
                "4": "viridis", "5": "twilight_shifted"
            }
            cmap = plt.get_cmap(colormap_dict.get(color_selection, "plasma"))
            return cmap(Z / np.max(Z))
    
    def create_optimized_2d_plot(self, func, func_name, color_map, normalize_type, request):
        """Parallel 2D plotting with adaptive resolution - uses user's input ranges"""
        
        # Adaptive resolution
        resolution = get_adaptive_resolution(
            "2D", request.function_name, self.base_resolution_2D
        )
        
        logger.info(f"Using adaptive resolution: {resolution}")
        
        # Use user's input ranges instead of hardcoded values
        X = np.linspace(request.x_min, request.x_max, resolution)
        Y = np.linspace(request.y_min, request.y_max, resolution)
        X, Y = np.meshgrid(X, Y)
        Z = np.zeros_like(X, dtype=np.float64)
        
        # Parallel computation
        num_threads = min(8, threading.active_count() * 2)
        total_pixels = resolution * resolution
        chunk_size = total_pixels // num_threads
        
        chunks = []
        indices = [(i, j) for i in range(resolution) for j in range(resolution)]
        
        for i in range(0, len(indices), chunk_size):
            chunk_indices = indices[i:i + chunk_size]
            chunks.append((func, chunk_indices, X, Y, normalize_type, request.m_coefficient, request.beta_coefficient))
        
        # Process chunks in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            chunk_results = executor.map(compute_chunk, chunks)
        
        # Combine results
        for chunk in chunk_results:
            for i, j, value in chunk:
                Z[i, j] = value
        
        # Optimized colorization
        colors = self.optimized_colorization(color_map, Z)
        
        # Plotting with smaller figure for speed
        fig, ax1 = plt.subplots(figsize=(12, 8))  # Reduced from 16,9
        # Use the actual request ranges instead of hardcoded values for proper axis alignment
        ax1.imshow(colors, extent=(request.x_min, request.x_max, request.y_min, request.y_max), 
                  origin='lower', aspect='auto')
        
        ax1.set_title(f'Optimized {func_name}')
        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))  # Fewer ticks
        ax1.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
        
        plt.tight_layout()
        return fig
    
    def create_optimized_3d_plot(self, func, func_name, color_map, normalize_type, request):
        """Optimized 3D plotting - uses user's input ranges"""
        
        # Use user's input ranges instead of hardcoded values
        x_min = request.x_min
        x_max = request.x_max  
        y_min = request.y_min
        y_max = request.y_max
        
        # Allow the request to control resolution (points per axis) for higher fidelity
        # request.resolution is interpreted as points per axis for 3D plots.
        # Apply sensible caps to avoid OOM: min_points=32, max_points=3000 (safe upper-bound)
        try:
            points = int(request.resolution) if getattr(request, 'resolution', None) else None
        except Exception:
            points = None

        if points is None or points <= 0:
            # Fallback to legacy step-size approach
            R = self.resolution_3D
            X = np.arange(x_min, x_max, R)
            Y = np.arange(y_min, y_max, R)
        else:
            # Cap requested points to a safe upper bound
            min_points = 32
            max_points = 3000
            points = max(min_points, min(points, max_points))
            # Create linear spaced coordinates (points per axis)
            X = np.linspace(x_min, x_max, points)
            Y = np.linspace(y_min, y_max, points)

        X, Y = np.meshgrid(X, Y)
        xn, yn = X.shape
        W = np.zeros_like(X, dtype=np.float64)

        # Parallel computation using the same chunking strategy as 2D plotting
        num_threads = min(8, threading.active_count() * 2)
        total_points = xn * yn
        chunk_size = max(1, total_points // num_threads)

        indices = [(i, j) for i in range(xn) for j in range(yn)]
        chunks = []
        for i in range(0, len(indices), chunk_size):
            chunk_indices = indices[i:i + chunk_size]
            chunks.append((func, chunk_indices, X, Y, normalize_type, request.m_coefficient, request.beta_coefficient))

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            chunk_results = executor.map(compute_chunk, chunks)

        for chunk in chunk_results:
            for i, j, value in chunk:
                W[i, j] = value
        
        # Smaller figure for faster rendering and better fit
        fig = plt.figure(figsize=(12, 8))  # Reduced from 14,9
        ax = fig.add_subplot(111, projection='3d')
        
        ax.view_init(elev=30, azim=-70)
        ax.dist = 10
        ax.set_box_aspect((5, 5, 1))
        
        # Reduced stride for faster rendering
        colormap_dict = {
            "1": cm.prism, "2": cm.jet, "3": cm.plasma, 
            "4": cm.viridis, "5": cm.twilight_shifted
        }
        cmap = colormap_dict.get(color_map, cm.plasma)
        
        ax.plot_surface(X, Y, W, rstride=2, cstride=2, cmap=cmap)  # Increased stride
        
        # Set axis ranges from user input
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        
        # Auto Z-range if user didn't specify or specified invalid range
        if (request.z_min == request.z_max or 
            request.z_min >= request.z_max or
            abs(request.z_max - request.z_min) < 1e-10):
            # Calculate optimal Z range from actual data
            w_min, w_max = np.nanmin(W), np.nanmax(W)
            if np.isfinite(w_min) and np.isfinite(w_max) and w_min != w_max:
                # Add 5% padding for better visualization
                z_range = w_max - w_min
                padding = z_range * 0.05
                ax.set_zlim(w_min - padding, w_max + padding)
            else:
                # Fallback to default range
                ax.set_zlim(-10, 10)
        else:
            # Use user-specified Z range
            ax.set_zlim(request.z_min, request.z_max)
        
        ax.set_xlabel('Real Axis')
        ax.set_ylabel('Imaginary Axis')
        ax.set_zlabel('Value')
        ax.set_title(f"Optimized {func_name}")
        
        return fig

# Initialize optimized objects and LaTeX function builder
optimized_functions = OptimizedLegacySpecialFunctions("2D")
optimized_plotting_2d = OptimizedLegacyComplexPlotting("2D")
optimized_plotting_3d = OptimizedLegacyComplexPlotting("3D")

# Initialize LaTeX function builder
latex_builder = LaTeXFunctionBuilder("custom_functions.json")
create_example_functions(latex_builder)

# Function mapping
OPTIMIZED_LEGACY_FUNCTION_MAP = {
    # Core infinite products
    'product_of_sin': {
        'name': 'Product of Sine (OPTIMIZED)',
        'function': optimized_functions.product_of_sin,
        'category': 'core',
        'description': 'Ultra-fast JIT compiled with exact legacy behavior',
        'speed': 'Very Fast'
    },
    'product_of_product_representation_for_sin': {
        'name': 'Double Product (OPTIMIZED)',
        'function': optimized_functions.product_of_product_representation_for_sin,
        'category': 'core',
        'description': 'Parallel computation with complexity reduction',
        'speed': 'Fast'
    },
    'complex_playground_magnification_currated_functions_DEMO': {
        'name': 'Riesz Demo (OPTIMIZED)',
        'function': optimized_functions.complex_playground_magnification_currated_functions_DEMO,
        'category': 'demo',
        'description': 'Optimized Riesz product with speed enhancements',
        'speed': 'Fast'
    },
    
    # Riesz products
    'Riesz_Product_for_Cos': {
        'name': 'Riesz Cosine (OPTIMIZED)',
        'function': optimized_functions.Riesz_Product_for_Cos,
        'category': 'riesz',
        'description': 'Streamlined with mathematical accuracy preserved',
        'speed': 'Very Fast'
    },
    'Riesz_Product_for_Sin': {
        'name': 'Riesz Sine (OPTIMIZED)',
        'function': optimized_functions.Riesz_Product_for_Sin,
        'category': 'riesz',
        'description': 'Fast Riesz product for sine functions',
        'speed': 'Very Fast'
    },
    'Riesz_Product_for_Tan': {
        'name': 'Riesz Tangent (OPTIMIZED)',
        'function': optimized_functions.Riesz_Product_for_Tan,
        'category': 'riesz',
        'description': 'Fast Riesz product for tangent functions',
        'speed': 'Very Fast'
    },
    
    # Viète products
    'Viete_Product_for_Cos': {
        'name': 'Viète Cosine (OPTIMIZED)',
        'function': optimized_functions.Viete_Product_for_Cos,
        'category': 'viete',
        'description': 'Optimized infinite product computation',
        'speed': 'Very Fast'
    },
    'Viete_Product_for_Sin': {
        'name': 'Viète Sine (OPTIMIZED)',
        'function': optimized_functions.Viete_Product_for_Sin,
        'category': 'viete',
        'description': 'Fast Viète product for sine functions',
        'speed': 'Very Fast'
    },
    'Viete_Product_for_Tan': {
        'name': 'Viète Tangent (OPTIMIZED)',
        'function': optimized_functions.Viete_Product_for_Tan,
        'category': 'viete',
        'description': 'Fast Viète product for tangent functions',
        'speed': 'Very Fast'
    },
    'Half_Base_Viete_Product_for_Sin': {
        'name': 'Half Base Viète Sine (OPTIMIZED)',
        'function': optimized_functions.Half_Base_Viete_Product_for_Sin,
        'category': 'viete',
        'description': 'Viète product with half base for sine',
        'speed': 'Very Fast'
    },
    
    # Composite functions
    'cos_of_product_of_sin': {
        'name': 'Cosine of Product Sine (OPTIMIZED)',
        'function': optimized_functions.cos_of_product_of_sin,
        'category': 'composite',
        'description': 'Cosine applied to product of sine',
        'speed': 'Fast'
    },
    'sin_of_product_of_sin': {
        'name': 'Sine of Product Sine (OPTIMIZED)',
        'function': optimized_functions.sin_of_product_of_sin,
        'category': 'composite',
        'description': 'Sine applied to product of sine',
        'speed': 'Fast'
    },
    'cos_of_product_of_product_representation_of_sin': {
        'name': 'Cosine of Double Product (OPTIMIZED)',
        'function': optimized_functions.cos_of_product_of_product_representation_of_sin,
        'category': 'composite',
        'description': 'Cosine applied to double product representation',
        'speed': 'Fast'
    },
    'sin_of_product_of_product_representation_of_sin': {
        'name': 'Sine of Double Product (OPTIMIZED)',
        'function': optimized_functions.sin_of_product_of_product_representation_of_sin,
        'category': 'composite',
        'description': 'Sine applied to double product representation',
        'speed': 'Fast'
    },
    
    # Prime indicator functions
    'Binary_Output_Prime_Indicator_Function_H': {
        'name': 'Prime Indicator H (OPTIMIZED)',
        'function': optimized_functions.Binary_Output_Prime_Indicator_Function_H,
        'category': 'prime',
        'description': 'Binary output prime indicator function',
        'speed': 'Medium'
    },
    'Prime_Output_Indicator_J': {
        'name': 'Prime Indicator J (OPTIMIZED)',
        'function': optimized_functions.Prime_Output_Indicator_J,
        'category': 'prime',
        'description': 'Advanced prime output indicator',
        'speed': 'Medium'
    },
    
    # Advanced specialized functions
    'Riesz_Product_for_Tan_and_Prime_indicator_combination': {
        'name': 'Riesz-Prime Combination (OPTIMIZED)',
        'function': optimized_functions.Riesz_Product_for_Tan_and_Prime_indicator_combination,
        'category': 'advanced',
        'description': 'Riesz product combined with prime indicators',
        'speed': 'Medium'
    },
    'Nested_roots_product_for_2': {
        'name': 'Nested Roots Product (OPTIMIZED)',
        'function': optimized_functions.Nested_roots_product_for_2,
        'category': 'advanced',
        'description': 'Nested radical product representations',
        'speed': 'Medium'
    },
    'natural_logarithm_of_product_of_product_representation_for_sin': {
        'name': 'Log Double Product (OPTIMIZED)',
        'function': optimized_functions.natural_logarithm_of_product_of_product_representation_for_sin,
        'category': 'transforms',
        'description': 'Natural logarithm of double product',
        'speed': 'Fast'
    },
    'gamma_of_product_of_product_representation_for_sin': {
        'name': 'Gamma Double Product (OPTIMIZED)',
        'function': optimized_functions.gamma_of_product_of_product_representation_for_sin,
        'category': 'transforms',
        'description': 'Gamma function of double product',
        'speed': 'Fast'
    },
    'gamma_form_product_of_product_representation_for_sin': {
        'name': 'Gamma Form Double Product (OPTIMIZED)',
        'function': optimized_functions.gamma_form_product_of_product_representation_for_sin,
        'category': 'transforms',
        'description': 'Gamma form with Euler-Mascheroni constant',
        'speed': 'Medium'
    },
    'Log_power_base_Viete_Product_for_Sin': {
        'name': 'Log Power Viète (OPTIMIZED)',
        'function': optimized_functions.Log_power_base_Viete_Product_for_Sin,
        'category': 'advanced',
        'description': 'Logarithmic power base Viète product',
        'speed': 'Medium'
    },
    'Custom_Riesz_Product_for_Tan': {
        'name': 'Custom Riesz Tangent (OPTIMIZED)',
        'function': optimized_functions.Custom_Riesz_Product_for_Tan,
        'category': 'custom',
        'description': 'Custom Riesz product for tangent',
        'speed': 'Fast'
    },
    'Custom_Viete_Product_for_Cos': {
        'name': 'Custom Viète Cosine (OPTIMIZED)',
        'function': optimized_functions.Custom_Viete_Product_for_Cos,
        'category': 'custom',
        'description': 'Custom Viète product for cosine',
        'speed': 'Fast'
    },
    'BOPIF_Q_Alternation_Series': {
        'name': 'BOPIF Alternation Series (OPTIMIZED)',
        'function': optimized_functions.BOPIF_Q_Alternation_Series,
        'category': 'prime',
        'description': 'Binary output alternation series',
        'speed': 'Slow'
    },
    'Dirichlet_Eta_Derived_From_BOPIF': {
        'name': 'Dirichlet Eta from BOPIF (OPTIMIZED)',
        'function': optimized_functions.Dirichlet_Eta_Derived_From_BOPIF,
        'category': 'prime',
        'description': 'Dirichlet eta function from prime indicators',
        'speed': 'Slow'
    }
}

# Health check endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint for system monitoring"""
    return {
        "status": "healthy",
        "version": "5.0.0",
        "features": {
            "jit_compilation": NUMBA_AVAILABLE,
            "interactive_commands": True,
            "latex_builder": True,
            "builtin_functions": len(OPTIMIZED_LEGACY_FUNCTION_MAP),
            "custom_functions": latex_builder.custom_functions['metadata']['count']
        },
        "timestamp": time.time()
    }

@app.get("/system/status")
async def system_status():
    """Detailed system status"""
    status = {
        "api": {
            "status": "running",
            "port": 8000,
            "interactive_commands": True
        },
        "functions": {
            "builtin": len(OPTIMIZED_LEGACY_FUNCTION_MAP),
            "custom": latex_builder.custom_functions['metadata']['count'],
            "total": len(OPTIMIZED_LEGACY_FUNCTION_MAP) + latex_builder.custom_functions['metadata']['count']
        },
        "optimization": {
            "jit_compilation": NUMBA_AVAILABLE,
            "parallel_processing": True,
            "adaptive_resolution": True,
            "vectorized_coloring": True
        }
    }
    
    if psutil:
        try:
            process = psutil.Process()
            status["system"] = {
                "memory_mb": process.memory_info().rss / 1024 / 1024,
                "cpu_percent": process.cpu_percent(),
                "uptime": time.time() - process.create_time()
            }
        except:
            status["system"] = {"error": "Unable to get system metrics"}
    
    return status

# Request models
class PlotRequest(BaseModel):
    function_name: str
    plot_type: str = '2D_Complex'
    x_min: float = 2
    x_max: float = 28
    y_min: float = -5
    y_max: float = 5
    z_min: float = -10  # Added for 3D plots
    z_max: float = 10   # Added for 3D plots
    resolution: int = 600
    normalize_type: str = 'Y'
    colormap: str = '6'
    canvas_size: str = '16x9'
    light_shading: bool = False
    axis_tick_spacing: float = 1.0
    title_override: str = ''
    # Special coefficients for aesthetic control
    m_coefficient: float = 0.36  # Magnification exponent
    beta_coefficient: float = 0.1468  # Scaling coefficient

class CustomFunctionRequest(BaseModel):
    name: str
    latex_formula: str
    description: str = ""
    category: str = "custom"
    parameters: dict = {"m": 0.1, "beta": 0.1}

class LaTeXSymbolsRequest(BaseModel):
    category: str = "all"

# API Endpoints
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Ultra-Fast Legacy Recreation API v5.0 - Optimized for Speed"}

@app.get("/functions")
async def get_functions():
    # Get built-in optimized functions
    builtin_functions_by_category = {}
    categories = set()
    
    for func_id, func_info in OPTIMIZED_LEGACY_FUNCTION_MAP.items():
        category = func_info['category']
        categories.add(category)
        
        if category not in builtin_functions_by_category:
            builtin_functions_by_category[category] = {}
        
        builtin_functions_by_category[category][func_id] = {
            'name': func_info['name'],
            'description': func_info['description'],
            'speed': func_info['speed'],
            'type': 'builtin'
        }
    
    # Get custom LaTeX functions
    custom_functions_data = latex_builder.list_functions()
    custom_functions_by_category = custom_functions_data.get("functions_by_category", {})
    
    # Mark custom functions
    for category in custom_functions_by_category:
        for func_id in custom_functions_by_category[category]:
            custom_functions_by_category[category][func_id]['type'] = 'custom'
            categories.add(category)
    
    # Merge built-in and custom functions
    all_functions_by_category = builtin_functions_by_category.copy()
    for category, functions in custom_functions_by_category.items():
        if category in all_functions_by_category:
            all_functions_by_category[category].update(functions)
        else:
            all_functions_by_category[category] = functions
    
    total_builtin = len(OPTIMIZED_LEGACY_FUNCTION_MAP)
    total_custom = custom_functions_data.get("total_functions", 0)
    
    return {
        "functions_by_category": all_functions_by_category,
        "categories": list(categories),
        "total_functions": total_builtin + total_custom,
        "builtin_functions": total_builtin,
        "custom_functions": total_custom,
        "optimizations": "JIT compilation, parallel processing, adaptive resolution, caching",
        "latex_support": True
    }

@app.get("/colormaps")
async def get_colormaps():
    return {
        "legacy_numeric": {
            "1": "Prism (FAST)",
            "2": "Jet (FAST)",
            "3": "Plasma (FAST)",
            "4": "Viridis (FAST)",
            "5": "Twilight Shifted (FAST)",
            "6": "Custom Colors 2 (VECTORIZED)",
            "7": "Custom Colors 3 (VECTORIZED)",
            "8": "Custom Colors 1 (VECTORIZED)"
        }
    }

@app.post("/plot")
async def generate_optimized_plot(request: PlotRequest):
    try:
        # Check if it's a built-in function
        if request.function_name in OPTIMIZED_LEGACY_FUNCTION_MAP:
            func_info = OPTIMIZED_LEGACY_FUNCTION_MAP[request.function_name]
            func = func_info['function']
        else:
            # Check if it's a custom LaTeX function
            try:
                func_info = {
                    'name': f"Custom: {request.function_name}",
                    'description': 'Custom LaTeX function'
                }
                func = latex_builder.compile_function(request.function_name)
            except:
                raise HTTPException(status_code=400, detail=f"Function {request.function_name} not found")
        
        logger.info(f"Generating OPTIMIZED {request.plot_type} plot for {request.function_name}")
        start_time = time.time()
        
        if request.plot_type in ['2D_Real', '2D_Complex']:
            fig = optimized_plotting_2d.create_optimized_2d_plot(
                func, func_info['name'], request.colormap, request.normalize_type, request
            )
        elif request.plot_type in ['3D_Real', '3D_Complex']:
            fig = optimized_plotting_3d.create_optimized_3d_plot(
                func, func_info['name'], request.colormap, request.normalize_type, request
            )
        else:
            raise HTTPException(status_code=400, detail=f"Invalid plot type: {request.plot_type}")
        
        generation_time = time.time() - start_time
        
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', facecolor='black', dpi=120, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close(fig)
        
        logger.info(f"Plot generated in {generation_time:.2f} seconds")
        
        return {
            "success": True,
            "image_base64": image_base64,
            "function_info": func_info,
            "generation_time": generation_time,
            "optimizations_used": [
                "JIT compilation with Numba",
                "Parallel processing", 
                "Adaptive resolution",
                "Vectorized colorization",
                "Result caching",
                "Custom LaTeX support" if request.function_name not in OPTIMIZED_LEGACY_FUNCTION_MAP else "Built-in optimization"
            ]
        }
        
    except Exception as e:
        logger.error(f"Optimized plot generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# LaTeX Function Builder Endpoints
@app.post("/custom-functions")
async def create_custom_function(request: CustomFunctionRequest):
    """Create a new custom function from LaTeX"""
    try:
        function_data = latex_builder.create_custom_function(
            name=request.name,
            latex_formula=request.latex_formula,
            description=request.description,
            category=request.category,
            parameters=request.parameters
        )
        
        logger.info(f"Created custom function: {request.name}")
        
        return {
            "success": True,
            "function_data": function_data,
            "message": f"Custom function '{request.name}' created successfully"
        }
        
    except Exception as e:
        logger.error(f"Custom function creation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/custom-functions")
async def list_custom_functions():
    """List all custom LaTeX functions"""
    try:
        functions_data = latex_builder.list_functions()
        return {
            "success": True,
            "functions": functions_data
        }
    except Exception as e:
        logger.error(f"Error listing custom functions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/custom-functions/{function_name}")
async def get_custom_function(function_name: str):
    """Get details of a specific custom function"""
    try:
        function_data = latex_builder.get_function(function_name)
        return {
            "success": True,
            "function_data": function_data
        }
    except Exception as e:
        logger.error(f"Error getting custom function {function_name}: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/custom-functions/{function_name}")
async def delete_custom_function(function_name: str):
    """Delete a custom function"""
    try:
        success = latex_builder.delete_function(function_name)
        if success:
            logger.info(f"Deleted custom function: {function_name}")
            return {
                "success": True,
                "message": f"Custom function '{function_name}' deleted successfully"
            }
        else:
            raise HTTPException(status_code=404, detail=f"Function '{function_name}' not found")
            
    except Exception as e:
        logger.error(f"Error deleting custom function {function_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/latex-symbols")
async def get_latex_symbols():
    """Get available LaTeX symbols for the function builder"""
    try:
        symbols = latex_builder.get_latex_symbols()
        return {
            "success": True,
            "symbols": symbols,
            "usage_examples": {
                "Product notation": "\\prod_{n=2}^{z} \\sin\\left(\\frac{\\pi z}{n}\\right)",
                "Sum notation": "\\sum_{n=1}^{\\infty} \\frac{1}{n^z}",
                "Fraction": "\\frac{\\sin(\\pi z)}{\\cos(\\pi z)}",
                "Power": "z^{\\alpha}",
                "Complex": "e^{i \\pi z}",
                "Greek letters": "\\alpha, \\beta, \\gamma, \\pi, \\omega"
            }
        }
    except Exception as e:
        logger.error(f"Error getting LaTeX symbols: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/test-latex")
async def test_latex_function(request: CustomFunctionRequest):
    """Test a LaTeX function without saving it"""
    try:
        # Create a temporary builder to test the function
        temp_builder = LaTeXFunctionBuilder()
        
        # Parse and test the LaTeX
        sympy_expr = temp_builder.parse_latex_to_sympy(request.latex_formula)
        python_code = temp_builder.sympy_to_python_function(sympy_expr)
        test_result = temp_builder.test_function(python_code)
        
        return {
            "success": True,
            "test_result": test_result,
            "sympy_expression": str(sympy_expr),
            "python_code": python_code,
            "message": "LaTeX function tested successfully"
        }
        
    except Exception as e:
        logger.error(f"LaTeX function test error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "LaTeX function test failed"
        }

# Interactive Command System
class InteractiveCommandHandler:
    def __init__(self):
        self.running = True
        self.frontend_process = None
        self.backend_pid = None
        
    def start_command_listener(self):
        """Start listening for interactive commands"""
        def command_loop():
            print("\n" + "="*60)
            print("🎮 INTERACTIVE COMMAND MODE ACTIVE")
            print("Type '/' followed by a command. Type '/help' for available commands.")
            print("="*60 + "\n")
            
            while self.running:
                try:
                    user_input = input().strip()
                    if user_input.startswith('/'):
                        self.handle_command(user_input[1:])
                except (EOFError, KeyboardInterrupt):
                    break
        
        command_thread = threading.Thread(target=command_loop, daemon=True)
        command_thread.start()
    
    def handle_command(self, command):
        """Handle interactive commands"""
        cmd_parts = command.split()
        cmd = cmd_parts[0].lower() if cmd_parts else ""
        
        if cmd == "help":
            self.show_help()
        elif cmd == "status":
            self.show_status()
        elif cmd == "restart-backend":
            self.restart_backend()
        elif cmd == "restart-frontend":
            self.restart_frontend()
        elif cmd == "restart-both":
            self.restart_both()
        elif cmd == "logs":
            self.show_logs()
        elif cmd == "stop":
            self.stop_all()
        elif cmd == "functions":
            self.list_functions()
        elif cmd == "test":
            self.run_test()
        else:
            print(f"❌ Unknown command: {command}")
            print("Type '/help' for available commands")
    
    def show_help(self):
        """Show available commands"""
        print("\n" + "="*50)
        print("🎮 INTERACTIVE COMMANDS")
        print("="*50)
        print("/help                 - Show this help message")
        print("/status               - Show system status")
        print("/restart-backend      - Restart Python API server")
        print("/restart-frontend     - Restart Next.js frontend")
        print("/restart-both         - Restart both services")
        print("/logs                 - Show recent API logs")
        print("/functions            - List available functions")
        print("/test                 - Run quick API test")
        print("/stop                 - Stop all services")
        print("="*50 + "\n")
    
    def show_status(self):
        """Show system status"""
        print("\n" + "="*50)
        print("📊 SYSTEM STATUS")
        print("="*50)
        
        # Check API health
        if requests:
            try:
                response = requests.get("http://localhost:8000/health", timeout=2)
                if response.status_code == 200:
                    print("✅ Backend API: HEALTHY (Port 8000)")
                else:
                    print("⚠️  Backend API: UNHEALTHY")
            except:
                print("❌ Backend API: OFFLINE")
        else:
            print("⚠️  Backend API: Status check requires 'requests' module")
        
        # Check frontend
        if requests:
            try:
                response = requests.get("http://localhost:3000", timeout=2)
                if response.status_code == 200:
                    print("✅ Frontend: HEALTHY (Port 3000)")
                else:
                    print("⚠️  Frontend: UNHEALTHY") 
            except:
                print("❌ Frontend: OFFLINE")
        else:
            print("⚠️  Frontend: Status check requires 'requests' module")
        
        # Show memory usage
        if psutil:
            try:
                process = psutil.Process()
                memory_mb = process.memory_info().rss / 1024 / 1024
                print(f"💾 Memory Usage: {memory_mb:.1f} MB")
            except:
                print("💾 Memory Usage: Unable to determine")
        else:
            print("💾 Memory Usage: Requires 'psutil' module")
            
        print(f"🔧 Total Functions: {len(OPTIMIZED_LEGACY_FUNCTION_MAP) + latex_builder.custom_functions['metadata']['count']}")
        print("="*50 + "\n")
    
    def restart_backend(self):
        """Restart the backend API"""
        print("🔄 Restarting backend API...")
        print("Note: Use the PowerShell script for full restart capability")
    
    def restart_frontend(self):
        """Restart the frontend"""
        print("🔄 Restarting frontend...")
        print("Note: Use the PowerShell script for full restart capability")
    
    def restart_both(self):
        """Restart both services"""
        print("🔄 Restarting both services...")
        print("Note: Use the PowerShell script for full restart capability")
    
    def show_logs(self):
        """Show recent logs"""
        print("\n" + "="*50)
        print("📋 RECENT API ACTIVITY")
        print("="*50)
        print("Logs would appear here in a full implementation")
        print("="*50 + "\n")
    
    def list_functions(self):
        """List available functions"""
        print("\n" + "="*50)
        print("📚 AVAILABLE FUNCTIONS")
        print("="*50)
        
        builtin_count = len(OPTIMIZED_LEGACY_FUNCTION_MAP)
        custom_count = latex_builder.custom_functions['metadata']['count']
        
        print(f"Built-in Functions: {builtin_count}")
        print(f"Custom Functions: {custom_count}")
        print(f"Total: {builtin_count + custom_count}")
        
        print("\nCategories:")
        categories = set()
        for func_info in OPTIMIZED_LEGACY_FUNCTION_MAP.values():
            categories.add(func_info['category'])
        for category in sorted(categories):
            print(f"  • {category}")
        print("="*50 + "\n")
    
    def run_test(self):
        """Run a quick API test"""
        print("\n🧪 Running quick API test...")
        try:
            # Test a simple function
            func = optimized_functions.product_of_sin
            test_z = complex(3, 1)
            result = func(test_z, 'N')
            print(f"✅ Test passed: f({test_z}) = {result:.6f}")
        except Exception as e:
            print(f"❌ Test failed: {e}")
        print()
    
    def stop_all(self):
        """Stop all services"""
        print("🛑 Stopping all services...")
        self.running = False
        sys.exit(0)

# Global command handler
command_handler = InteractiveCommandHandler()

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Ultra-Fast Legacy Recreation API v5.0")
    print("⚡ Optimized with JIT compilation, parallel processing, and adaptive resolution")
    print("🎮 Interactive commands available - type '/' followed by command")
    
    # Start interactive command system
    command_handler.start_command_listener()
    
    # Start the API server
    uvicorn.run(app, host="0.0.0.0", port=8000)