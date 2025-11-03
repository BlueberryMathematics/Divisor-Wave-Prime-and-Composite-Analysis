"""
EnhancedSuperFastPlotter.py
Complete mathematical visualization system with LaTeX formulas and all functions
Integrates with Next.js for real-time plotting with formula display
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for web - MUST be before pyplot import
import matplotlib.pyplot as plt
from matplotlib import cm, ticker
import time
import base64
import io
import warnings
import json
import os
from typing import Dict, List, Optional, Tuple

# Import optimized functions
try:
    from OptimizedSpecialFunctions import OptimizedSpecialFunctions
    print("✅ Using OptimizedSpecialFunctions for blazing speed")
except ImportError:
    print("❌ OptimizedSpecialFunctions not found")
    exit(1)

warnings.filterwarnings('ignore')
plt.style.use('dark_background')

class EnhancedSuperFastPlotter:
    """
    Complete mathematical visualization system with LaTeX formulas, 
    real-time plotting, and formula storage capabilities
    """
    
    def __init__(self):
        self.special_functions = OptimizedSpecialFunctions("2D")
        
        # Complete function mapping with LaTeX formulas
        self.function_data = {
            'product_of_sin': {
                'function': self.special_functions.product_of_sin,
                'display_name': 'Product of Sine (a(z))',
                'latex': r'a(z) = \left|\prod_{k=2}^x \alpha\frac{x}{k}\sin\left(\frac{\pi z}{k}\right)\right|',
                'description': 'Infinite product of sine functions representing divisor waves. Creates prime/composite number patterns.',
                'category': 'Core Divisor Wave Functions',
                'default_range': (-8, 8),
                'optimal_resolution': 200
            },
            'product_of_product_representation_for_sin': {
                'function': self.special_functions.product_of_product_representation_for_sin,
                'display_name': 'Double Product Representation (b(z))',
                'latex': r'b(z) = \left|\prod_{k=2}^x \prod_{n=2}^x \left(\pi z \left(1-\frac{z^2}{k^2 n^2}\right)\right)\right|',
                'description': 'Double infinite product using the product representation of sine. Enhanced complexity analysis.',
                'category': 'Core Divisor Wave Functions',
                'default_range': (-5, 5),
                'optimal_resolution': 150
            },
            'Riesz_Product_for_Cos': {
                'function': self.special_functions.Riesz_Product_for_Cos,
                'display_name': 'Riesz Product for Cosine',
                'latex': r'R_{\cos}(z) = \left|\prod_{n=2}^x \left(1 + \cos(\pi z n)\right)\right|^{-m}',
                'description': 'Riesz product using cosine functions. Shows trigonometric number theory patterns.',
                'category': 'Riesz Products',
                'default_range': (-6, 6),
                'optimal_resolution': 180
            },
            'Riesz_Product_for_Sin': {
                'function': self.special_functions.Riesz_Product_for_Sin,
                'display_name': 'Riesz Product for Sine',
                'latex': r'R_{\sin}(z) = \left|\prod_{n=2}^x \left(1 + \sin(\pi z n)\right)\right|^{-m}',
                'description': 'Riesz product using sine functions with number-theoretic significance.',
                'category': 'Riesz Products',
                'default_range': (-6, 6),
                'optimal_resolution': 180
            },
            'Riesz_Product_for_Tan': {
                'function': self.special_functions.Riesz_Product_for_Tan,
                'display_name': 'Riesz Product for Tangent',
                'latex': r'R_{\tan}(z) = \left|\prod_{n=2}^x \left(1 + \tan(\pi z n)\right)\right|^{-m}',
                'description': 'Riesz product using tangent functions with complex analytical properties.',
                'category': 'Riesz Products',
                'default_range': (-4, 4),
                'optimal_resolution': 160
            },
            'Viete_Product_for_Cos': {
                'function': self.special_functions.Viete_Product_for_Cos,
                'display_name': 'Viète Product for Cosine',
                'latex': r'V_{\cos}(z) = \left|\prod_{n=2}^x \cos\left(\frac{\pi z}{2^n}\right)\right|^{-m}',
                'description': 'Viète-style infinite product using cosine with geometric progression in denominators.',
                'category': 'Viète Products',
                'default_range': (-8, 8),
                'optimal_resolution': 200
            },
            'Viete_Product_for_Sin': {
                'function': self.special_functions.Viete_Product_for_Sin,
                'display_name': 'Viète Product for Sine',
                'latex': r'V_{\sin}(z) = \left|\prod_{n=2}^x \sin\left(\frac{\pi z}{2^n}\right)\right|^{-m}',
                'description': 'Viète-style infinite product using sine functions.',
                'category': 'Viète Products',
                'default_range': (-8, 8),
                'optimal_resolution': 200
            },
            'cos_of_product_of_sin': {
                'function': self.special_functions.cos_of_product_of_sin,
                'display_name': 'Cosine of Product of Sine',
                'latex': r'\cos\left(a(z)\right) = \cos\left(\left|\prod_{k=2}^x \alpha\frac{x}{k}\sin\left(\frac{\pi z}{k}\right)\right|\right)',
                'description': 'Cosine applied to the product of sine function, creating wave interference patterns.',
                'category': 'Composite Functions',
                'default_range': (-6, 6),
                'optimal_resolution': 180
            },
            'sin_of_product_of_sin': {
                'function': self.special_functions.sin_of_product_of_sin,
                'display_name': 'Sine of Product of Sine',
                'latex': r'\sin\left(a(z)\right) = \sin\left(\left|\prod_{k=2}^x \alpha\frac{x}{k}\sin\left(\frac{\pi z}{k}\right)\right|\right)',
                'description': 'Sine applied to the product of sine function.',
                'category': 'Composite Functions',
                'default_range': (-6, 6),
                'optimal_resolution': 180
            },
            'Binary_Output_Prime_Indicator_Function_H': {
                'function': self.special_functions.Binary_Output_Prime_Indicator_Function_H,
                'display_name': 'Binary Prime Indicator H(z)',
                'latex': r'H(z) = \begin{cases} 1 & \text{if } z \text{ is prime} \\\\ 0 & \text{if } z \text{ is composite} \end{cases}',
                'description': 'Binary function that outputs 1 for prime numbers and 0 for composite numbers.',
                'category': 'Prime Analysis Functions',
                'default_range': (0, 50),
                'optimal_resolution': 250
            },
            'Prime_Output_Indicator_J': {
                'function': self.special_functions.Prime_Output_Indicator_J,
                'display_name': 'Prime Output Indicator J(z)',
                'latex': r'J(z) = \begin{cases} p & \text{if } z = p \text{ (prime)} \\\\ 0 & \text{if } z \text{ is composite} \end{cases}',
                'description': 'Function that outputs the prime number itself for primes, 0 for composites.',
                'category': 'Prime Analysis Functions',
                'default_range': (0, 50),
                'optimal_resolution': 250
            },
            'Half_Base_Viete_Product_for_Sin': {
                'function': self.special_functions.Half_Base_Viete_Product_for_Sin,
                'display_name': 'Half-Base Viète Product',
                'latex': r'HV_{\sin}(z) = \left|\prod_{n=2}^x \sin\left(\frac{\pi z}{(1/2)^n}\right)\right|^{-m}',
                'description': 'Modified Viète product using half as the geometric base.',
                'category': 'Viète Products',
                'default_range': (-4, 4),
                'optimal_resolution': 160
            },
            'Nested_roots_product_for_2': {
                'function': self.special_functions.Nested_roots_product_for_2,
                'display_name': 'Nested Roots Product',
                'latex': r'NR(z) = \left|\prod_{n=2}^x \sqrt[n]{\sqrt[n-1]{\cdots\sqrt{2}}}\right|^{-m}',
                'description': 'Product involving nested radicals, creating fractal-like patterns.',
                'category': 'Advanced Functions',
                'default_range': (-3, 3),
                'optimal_resolution': 120
            },
            # Additional functions from legacy Special_Functions.py
            'complex_playground_magnification_currated_functions_DEMO': {
                'function': self.special_functions.complex_playground_magnification_currated_functions_DEMO,
                'display_name': 'Complex Playground Demo',
                'latex': r'CP(z) = \left|\prod_{n=2}^x \left(iz + iz\sin(\pi z n)\right)^{iz}\right|^{-m}',
                'description': 'Demonstration function for complex analysis with curated magnification patterns.',
                'category': 'Demo Functions',
                'default_range': (-4, 4),
                'optimal_resolution': 150
            },
            'cos_of_product_of_product_representation_of_sin': {
                'function': self.special_functions.cos_of_product_of_product_representation_of_sin,
                'display_name': 'Cosine of Double Product',
                'latex': r'\cos(b(z)) = \cos\left(\left|\prod_{k=2}^x \prod_{n=2}^x \left(\pi z \left(1-\frac{z^2}{k^2 n^2}\right)\right)\right|\right)',
                'description': 'Cosine applied to the double product representation, creating oscillatory patterns.',
                'category': 'Trigonometric Compositions',
                'default_range': (-4, 4),
                'optimal_resolution': 180
            },
            'sin_of_product_of_product_representation_of_sin': {
                'function': self.special_functions.sin_of_product_of_product_representation_of_sin,
                'display_name': 'Sine of Double Product',
                'latex': r'\sin(b(z)) = \sin\left(\left|\prod_{k=2}^x \prod_{n=2}^x \left(\pi z \left(1-\frac{z^2}{k^2 n^2}\right)\right)\right|\right)',
                'description': 'Sine applied to the double product representation, showing wave interference.',
                'category': 'Trigonometric Compositions',
                'default_range': (-4, 4),
                'optimal_resolution': 180
            },
            'Viete_Product_for_Tan': {
                'function': self.special_functions.Viete_Product_for_Tan,
                'display_name': 'Viète Product for Tangent',
                'latex': r'V_{\tan}(z) = \left|\prod_{n=2}^x \tan\left(\frac{\pi z}{2^n}\right)\right|^{-m}',
                'description': 'Viète-style infinite product using tangent functions.',
                'category': 'Viète Products',
                'default_range': (-3, 3),
                'optimal_resolution': 140
            }
        }
        
        # Load custom formulas from JSON storage
        self.load_custom_formulas()
        
        print(f"📋 Available functions: {len(self.function_data)}")
        for name, data in self.function_data.items():
            print(f"   • {data['display_name']}")
    
    def load_custom_formulas(self):
        """Load custom formulas from JSON storage"""
        custom_path = "custom_formulas.json"
        if os.path.exists(custom_path):
            try:
                with open(custom_path, 'r') as f:
                    custom_formulas = json.load(f)
                    for name, formula_data in custom_formulas.items():
                        # Add custom formulas to function_data
                        # Note: This would need the LaTeX to NumPy converter to be implemented
                        print(f"📄 Loaded custom formula: {name}")
            except Exception as e:
                print(f"⚠️ Error loading custom formulas: {e}")
    
    def save_custom_formula(self, name: str, latex_formula: str, description: str = ""):
        """Save a custom formula to JSON storage"""
        custom_path = "custom_formulas.json"
        
        # Load existing formulas
        custom_formulas = {}
        if os.path.exists(custom_path):
            try:
                with open(custom_path, 'r') as f:
                    custom_formulas = json.load(f)
            except:
                pass
        
        # Add new formula
        custom_formulas[name] = {
            'latex': latex_formula,
            'description': description,
            'category': 'Custom Functions',
            'created_date': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Save back to file
        with open(custom_path, 'w') as f:
            json.dump(custom_formulas, f, indent=2)
        
        print(f"💾 Saved custom formula: {name}")
    
    def generate_plot_base64(self, function_name: str, resolution: int = 200, 
                           x_range: Tuple[float, float] = (-8, 8), 
                           y_range: Tuple[float, float] = (-8, 8),
                           colormap: str = 'plasma', normalize_type: str = 'Y') -> Dict:
        """
        Generate plot and return as base64 string for web display
        """
        if function_name not in self.function_data:
            raise ValueError(f"Function '{function_name}' not available")
        
        func_data = self.function_data[function_name]
        func = func_data['function']
        
        start_time = time.time()
        
        # Create coordinate grids
        x = np.linspace(x_range[0], x_range[1], resolution)
        y = np.linspace(y_range[0], y_range[1], resolution)
        X, Y = np.meshgrid(x, y)
        
        # Compute function values
        Z = np.zeros_like(X, dtype=np.float64)
        x_flat = X.flatten()
        y_flat = Y.flatten()
        
        batch_size = 5000  # Smaller batches for web performance
        for i in range(0, len(x_flat), batch_size):
            end_idx = min(i + batch_size, len(x_flat))
            z_batch = x_flat[i:end_idx] + 1j * y_flat[i:end_idx]
            
            for j, z in enumerate(z_batch):
                try:
                    Z.flat[i + j] = func(z, normalize_type)
                except:
                    Z.flat[i + j] = 0.0
        
        # Create matplotlib plot
        fig, ax = plt.subplots(figsize=(12, 8), dpi=100)
        
        # Handle infinite/nan values
        Z_clean = np.where(np.isfinite(Z), Z, 0)
        
        # Apply colormap
        colormap_options = {
            'prism': cm.prism,
            'jet': cm.jet, 
            'plasma': cm.plasma,
            'viridis': cm.viridis,
            'magma': cm.magma,
            'rainbow': cm.rainbow
        }
        
        cmap = colormap_options.get(colormap, cm.plasma)
        
        # Normalize and create image
        if np.max(Z_clean) > 0:
            colors = cmap(Z_clean / np.max(Z_clean))
        else:
            colors = cmap(Z_clean)
        
        im = ax.imshow(colors, 
                      extent=[x_range[0], x_range[1], y_range[0], y_range[1]], 
                      origin='lower', 
                      aspect='auto')
        
        # Styling
        ax.set_title(func_data['display_name'], fontsize=16, color='white', pad=20)
        ax.set_xlabel('Real Axis', fontsize=12)
        ax.set_ylabel('Imaginary Axis', fontsize=12)
        
        # Format axes
        ax.xaxis.set_major_locator(ticker.MaxNLocator(8))
        ax.yaxis.set_major_locator(ticker.MaxNLocator(8))
        
        plt.tight_layout()
        
        # Convert to base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight',
                   facecolor='#1a1a1a', edgecolor='none')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        plt.close(fig)  # Free memory
        
        computation_time = time.time() - start_time
        
        return {
            'image_base64': img_base64,
            'latex_formula': func_data['latex'],
            'display_name': func_data['display_name'],
            'description': func_data['description'],
            'category': func_data['category'],
            'computation_time': computation_time,
            'resolution': resolution,
            'x_range': x_range,
            'y_range': y_range,
            'colormap': colormap,
            'normalize_type': normalize_type,
            'statistics': {
                'z_min': float(np.min(Z_clean)),
                'z_max': float(np.max(Z_clean)),
                'z_mean': float(np.mean(Z_clean)),
                'total_points': resolution * resolution
            }
        }
    
    def get_function_list(self) -> Dict:
        """Get list of all available functions with metadata"""
        functions = {}
        for name, data in self.function_data.items():
            functions[name] = {
                'display_name': data['display_name'],
                'latex': data['latex'],
                'description': data['description'],
                'category': data['category'],
                'default_range': data['default_range'],
                'optimal_resolution': data['optimal_resolution']
            }
        return functions
    
    def generate_plot_3d_base64(self, function_name: str, resolution: int = 150, 
                               x_range: Tuple[float, float] = (-5, 5), 
                               y_range: Tuple[float, float] = (-5, 5),
                               colormap: str = 'plasma', normalize_type: str = 'Y',
                               elevation: int = 30, azimuth: int = -60) -> Dict:
        """
        Generate 3D surface plot like the original Complex_Plotting.py
        Compatible with legacy create_plot_3D functionality
        """
        start_time = time.time()
        
        if function_name not in self.function_data:
            raise ValueError(f"Function '{function_name}' not found")
            
        func_data = self.function_data[function_name]
        func = func_data['function']
        
        # Create coordinate grid (reduced resolution for 3D performance)
        x = np.linspace(x_range[0], x_range[1], resolution)
        y = np.linspace(y_range[0], y_range[1], resolution)
        X, Y = np.meshgrid(x, y)
        Z_complex = X + 1j * Y
        
        # Compute function values with error handling
        Z = np.zeros_like(X, dtype=float)
        for i in range(resolution):
            for j in range(resolution):
                try:
                    z_val = Z_complex[i, j]
                    result = func(z_val, normalize_type)
                    Z[i, j] = float(np.real(result)) if np.isfinite(result) else 0.0
                except Exception:
                    Z[i, j] = 0.0
        
        # Create 3D surface plot
        fig = plt.figure(figsize=(10, 8), facecolor='#1a1a1a')
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('#1a1a1a')
        
        # Create surface plot
        surface = ax.plot_surface(X, Y, Z, cmap=colormap, alpha=0.9,
                                linewidth=0, antialiased=True, shade=True)
        
        # Set viewing angle (like original Complex_Plotting.py)
        ax.view_init(elev=elevation, azim=azimuth)
        
        # Styling to match the original dark theme
        ax.set_xlabel('Real(z)', color='white', fontsize=12)
        ax.set_ylabel('Imag(z)', color='white', fontsize=12)
        ax.set_zlabel('|f(z)|', color='white', fontsize=12)
        ax.set_title(f'3D: {func_data["display_name"]}', color='white', fontsize=14, pad=20)
        
        # Dark theme styling
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.grid(True, alpha=0.3)
        ax.tick_params(colors='white', labelsize=10)
        
        # Add colorbar
        colorbar = plt.colorbar(surface, ax=ax, shrink=0.6, aspect=20)
        colorbar.ax.yaxis.set_tick_params(color='white', labelsize=10)
        colorbar.ax.yaxis.label.set_color('white')
        
        plt.tight_layout()
        
        # Convert to base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight',
                   facecolor='#1a1a1a', edgecolor='none')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        plt.close(fig)  # Free memory
        
        computation_time = time.time() - start_time
        
        return {
            'image_base64': img_base64,
            'latex_formula': func_data['latex'],
            'display_name': func_data['display_name'],
            'description': func_data['description'],
            'category': func_data['category'],
            'computation_time': computation_time,
            'resolution': resolution,
            'x_range': x_range,
            'y_range': y_range,
            'elevation': elevation,
            'azimuth': azimuth,
            'colormap': colormap,
            'normalize_type': normalize_type,
            'plot_type': '3D',
            'statistics': {
                'z_min': float(np.min(Z)),
                'z_max': float(np.max(Z)),
                'z_mean': float(np.mean(Z)),
                'total_points': resolution * resolution
            }
        }
    
    def latex_to_numpy_converter(self, latex_formula: str) -> str:
        """
        Convert LaTeX infinite product formulas to NumPy for-loop format
        This is a simplified version - would need more sophisticated parsing for full implementation
        """
        # Basic pattern matching for infinite products
        numpy_code = ""
        
        if r'\prod_{' in latex_formula:
            # Extract the product bounds and expression
            # This is a simplified example - full implementation would need proper LaTeX parsing
            numpy_code = '''
def custom_function(z, normalize_type='Y'):
    z_real = np.real(z)
    z_imag = np.imag(z)
    
    result = 1.0
    max_n = min(int(abs(z_real)) + 1, 50)
    
    for n in range(2, max_n + 1):
        # Insert parsed expression here
        term = 1.0  # This would be the parsed term
        result *= term
    
    return abs(result) ** (-0.1)  # Apply standard normalization
'''
        
        return numpy_code

# Global instance for API usage
plotter_instance = None

def get_plotter():
    """Get global plotter instance"""
    global plotter_instance
    if plotter_instance is None:
        plotter_instance = EnhancedSuperFastPlotter()
    return plotter_instance

if __name__ == "__main__":
    # Test the enhanced plotter
    plotter = EnhancedSuperFastPlotter()
    
    # Test generating a plot
    result = plotter.generate_plot_base64('product_of_sin', resolution=150)
    print(f"✅ Generated plot in {result['computation_time']:.2f}s")
    print(f"📐 LaTeX: {result['latex_formula']}")
    print(f"📊 Statistics: min={result['statistics']['z_min']:.4f}, max={result['statistics']['z_max']:.4f}")