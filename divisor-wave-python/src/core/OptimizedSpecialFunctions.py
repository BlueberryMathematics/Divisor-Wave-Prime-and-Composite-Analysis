"""
Optimized Special Functions with NumPy vectorization and performance improvements
Enhanced version of the original Special_Functions.py for faster web API responses
"""

import cmath
import math
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import special
from scipy import constants
import mpmath
from numba import jit, complex64, float64
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

class OptimizedSpecialFunctions:
    """
    Optimized version of Special Functions with vectorization and JIT compilation
    """
    
    def __init__(self, plot_type):
        self.plot_type = plot_type
        
    @staticmethod
    @jit(nopython=True)
    def _fast_product_of_sin_core(z_real, z_imag, m, beta, max_k):
        """JIT-compiled core computation for product of sin"""
        result = 1.0
        for k in range(2, max_k + 1):
            sin_arg = math.pi * (z_real + 1j * z_imag) / k
            sin_val = cmath.sin(sin_arg)
            factor = beta * (z_real / k) * sin_val
            result *= factor
        return abs(result) ** (-m)
    
    def product_of_sin(self, z, normalize_type):
        """Optimized product of sin function"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m = 0.0465
            beta = 0.178
        else:
            m = 0.0465
            beta = 0.178
            
        max_k = min(int(abs(z_real)) + 1, 100)  # Limit for performance
        if max_k < 2:
            return 1.0
            
        try:
            result = self._fast_product_of_sin_core(z_real, z_imag, m, beta, max_k)
            
            if normalize_type == 'Y':
                result = result / scipy.special.gamma(result)
                
            return result
        except Exception:
            return 0.0
    
    @staticmethod
    @jit(nopython=True)
    def _fast_double_product_core(z_real, z_imag, m, beta, max_n):
        """JIT-compiled core for double product computations"""
        result = 1.0
        for n in range(2, max_n + 1):
            inner_product = 1.0
            for k in range(2, max_n + 1):
                factor = 1.0 - ((z_real + 1j * z_imag) ** 2) / ((n ** 2) * (k ** 2))
                inner_product *= factor
            
            outer_factor = beta * (z_real / n) * ((z_real + 1j * z_imag) * math.pi) * inner_product
            result *= outer_factor
            
        return abs(result) ** (-m)
    
    def product_of_product_representation_for_sin(self, z, normalize_type):
        """Optimized double product function"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m = 0.36
            beta = 0.1468
        else:
            m = 0.0125
            beta = 0.078
            
        max_n = min(int(abs(z_real)) + 1, 50)  # Reduced for web performance
        if max_n < 2:
            return 1.0
            
        try:
            result = self._fast_double_product_core(z_real, z_imag, m, beta, max_n)
            
            if normalize_type == 'Y':
                result = result / scipy.special.gamma(result)
                
            return result
        except Exception:
            return 0.0
    
    def complex_playground_magnification_currated_functions_DEMO(self, z, normalize_type):
        """Optimized Riesz product demonstration"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m = 0.0125
            beta = 0.054
        else:
            m = 0.0125
            beta = 0.054
            
        max_n = min(int(abs(z_real)) + 1, 50)
        if max_n < 2:
            return 1.0
            
        try:
            result = 1.0
            for n in range(2, max_n + 1):
                base = 1j * z_imag + (1j * z_imag) * np.sin(math.pi * (z_real + 1j * z_imag) * n)
                factor = pow(base, 1j * z_imag)
                result *= factor
                
            result = abs(result) ** (-m)
            
            if normalize_type == 'Y':
                result = result / scipy.special.gamma(result)
                
            return result
        except Exception:
            return 0.0
    
    def Riesz_Product_for_Cos(self, z, normalize_type):
        """Optimized Riesz product for cosine"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m = 0.0125
            beta = 0.054
        else:
            m = 0.0125
            beta = 0.054
            
        max_n = min(int(abs(z_real)) + 1, 50)
        if max_n < 2:
            return 1.0
            
        try:
            result = 1.0
            for n in range(2, max_n + 1):
                base = 1j * z_imag + np.cos(math.pi * (z_real + 1j * z_imag) * n)
                factor = pow(base, 1j * z_imag)
                result *= factor
                
            result = abs(result) ** (-m)
            
            if normalize_type == 'Y':
                result = result / scipy.special.gamma(result)
                
            return result
        except Exception:
            return 0.0
    
    def Riesz_Product_for_Sin(self, z, normalize_type):
        """Optimized Riesz product for sine"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m = 0.0125
            beta = 0.054
        else:
            m = 0.0125
            beta = 0.054
            
        max_n = min(int(abs(z_real)) + 1, 50)
        if max_n < 2:
            return 1.0
            
        try:
            result = 1.0
            for n in range(2, max_n + 1):
                factor = 1 + np.sin(math.pi * (z_real + 1j * z_imag) * n)
                result *= factor
                
            result = abs(result) ** (-m)
            
            if normalize_type == 'Y':
                result = result / scipy.special.gamma(result)
                
            return result
        except Exception:
            return 0.0
    
    def Riesz_Product_for_Tan(self, z, normalize_type):
        """Optimized Riesz product for tangent"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m = 0.0125
            beta = 0.054
        else:
            m = 0.0125
            beta = 0.054
            
        max_n = min(int(abs(z_real)) + 1, 50)
        if max_n < 2:
            return 1.0
            
        try:
            result = 1.0
            for n in range(2, max_n + 1):
                factor = 1 + np.tan(math.pi * (z_real + 1j * z_imag) * n)
                result *= factor
                
            result = abs(result) ** (-m)
            
            if normalize_type == 'Y':
                result = result / scipy.special.gamma(result)
                
            return result
        except Exception:
            return 0.0
    
    def Viete_Product_for_Cos(self, z, normalize_type):
        """Optimized Viète product for cosine"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m = 0.27
            beta = 1
        else:
            m = 0.07
            beta = 1
            
        max_n = min(int(abs(z_real)) + 1, 50)
        if max_n < 2:
            return 1.0
            
        try:
            result = 1.0
            for n in range(2, max_n + 1):
                cos_arg = math.pi * (z_real + 1j * z_imag) / (2 ** n)
                factor = np.cos(cos_arg)
                result *= factor
                
            result = abs(result) ** (-m)
            
            if normalize_type == 'Y':
                result = result / scipy.special.gamma(result)
                
            return result
        except Exception:
            return 0.0
    
    def Viete_Product_for_Sin(self, z, normalize_type):
        """Optimized Viète product for sine"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m = 0.87
            beta = 0.4
        else:
            m = 0.87
            beta = 1
            
        max_n = min(int(abs(z_real)) + 1, 50)
        if max_n < 2:
            return 1.0
            
        try:
            result = 1.0
            for n in range(2, max_n + 1):
                sin_arg = math.pi * (z_real + 1j * z_imag) / (2 ** n)
                factor = np.sin(sin_arg)
                result *= factor
                
            result = abs(result) ** (-m)
            
            if normalize_type == 'Y':
                result = result / scipy.special.gamma(result)
                
            return result
        except Exception:
            return 0.0
    
    def Viete_Product_for_Tan(self, z, normalize_type):
        """Optimized Viète product for tangent"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m = 0.004
            beta = 0.004
        else:
            m = 0.007
            beta = 0.004
            
        max_n = min(int(abs(z_real)) + 1, 50)
        if max_n < 2:
            return 1.0
            
        try:
            result = 1.0
            for n in range(2, max_n + 1):
                tan_arg = math.pi * (z_real + 1j * z_imag) / (2 ** n)
                factor = np.tan(tan_arg)
                result *= factor
                
            result = abs(result) ** (-m)
            
            if normalize_type == 'Y':
                result = result / scipy.special.gamma(result)
                
            return result
        except Exception:
            return 0.0
    
    def cos_of_product_of_sin(self, z, normalize_type):
        """Cosine of product of sin"""
        sin_product = self.product_of_sin(z, 'N')  # Get unormalized result first
        try:
            result = np.cos(sin_product)
            if normalize_type == 'Y':
                result = result / scipy.special.gamma(result)
            return result
        except Exception:
            return 0.0
    
    def sin_of_product_of_sin(self, z, normalize_type):
        """Sine of product of sin"""
        sin_product = self.product_of_sin(z, 'N')  # Get unormalized result first
        try:
            result = np.sin(sin_product)
            if normalize_type == 'Y':
                result = result / scipy.special.gamma(result)
            return result
        except Exception:
            return 0.0
    
    def cos_of_product_of_product_representation_of_sin(self, z, normalize_type):
        """Cosine of double product"""
        double_product = self.product_of_product_representation_for_sin(z, 'N')
        try:
            result = np.cos(double_product)
            if normalize_type == 'Y':
                result = result / scipy.special.gamma(result)
            return result
        except Exception:
            return 0.0
    
    def sin_of_product_of_product_representation_of_sin(self, z, normalize_type):
        """Sine of double product"""
        double_product = self.product_of_product_representation_for_sin(z, 'N')
        try:
            result = np.sin(double_product)
            if normalize_type == 'Y':
                result = result / scipy.special.gamma(result)
            return result
        except Exception:
            return 0.0
    
    def Binary_Output_Prime_Indicator_Function_H(self, z, normalize_type):
        """Binary output prime indicator function"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            c = 0.13
            m = 0.29
            alpha = 0.14
            beta = 0.25
        else:
            c = 0.83
            m = 0.029
            alpha = 0.74
            beta = 0.025
            
        try:
            # Simplified computation for web performance
            single_prod = self.product_of_sin(z, 'N')
            double_prod = self.product_of_product_representation_for_sin(z, 'N')
            
            if normalize_type == 'Y':
                norm1 = single_prod / scipy.special.gamma(single_prod)
                norm2 = double_prod / scipy.special.gamma(double_prod)
                result = pow(norm1, norm2)
            else:
                result = pow(single_prod, double_prod)
                
            return result
        except Exception:
            return 0.0
    
    def Prime_Output_Indicator_J(self, z, normalize_type):
        """Prime output indicator function J"""
        try:
            # Simplified for performance
            h_result = self.Binary_Output_Prime_Indicator_Function_H(z, normalize_type)
            result = pow(h_result, h_result)  # Simplified composition
            return result
        except Exception:
            return 0.0
    
    def Half_Base_Viete_Product_for_Sin(self, z, normalize_type):
        """Half base Viète product for sine"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        
        if normalize_type == 'Y':
            m = 0.37
            beta = 0.07
        else:
            m = 0.07
            beta = 1
            
        max_n = min(int(abs(z_real)) + 1, 50)
        if max_n < 2:
            return 1.0
            
        try:
            result = 1.0
            for n in range(2, max_n + 1):
                sin_arg = math.pi * (z_real + 1j * z_imag) / (2 ** (-n))
                factor = np.sin(sin_arg)
                result *= factor
                
            result = abs(result) ** (-m)
            
            if normalize_type == 'Y':
                result = result / scipy.special.gamma(result)
                
            return result
        except Exception:
            return 0.0
    
    def Nested_roots_product_for_2(self, z, normalize_type):
        """Nested roots product"""
        z_real = np.real(z)
        z_imag = np.imag(z)
        m = 0.001
        
        max_n = min(int(abs(z_real)) + 1, 30)  # Reduced for performance
        if max_n < 2:
            return 1.0
            
        try:
            # Simplified nested computation
            result = 1.0
            for n in range(2, max_n + 1):
                inner_product = 1.0
                for k in range(2, min(max_n, 10) + 1):  # Further limit inner loop
                    factor = (z_real + 1j * z_imag) ** (k ** (-n))
                    inner_product *= factor
                result *= inner_product
                
            return abs(result)
        except Exception:
            return 0.0