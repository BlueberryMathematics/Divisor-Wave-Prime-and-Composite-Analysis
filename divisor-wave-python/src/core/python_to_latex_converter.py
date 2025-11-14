"""
Python to LaTeX Converter System
Extracts mathematical formulas from Python function implementations and converts them to LaTeX notation
Specifically designed for divisor wave functions and infinite products

This converter:
- Analyzes Python code to identify mathematical operations
- Converts numpy/scipy operations to LaTeX equivalents  
- Handles infinite products, sums, and complex mathematical expressions
- Provides LaTeX formulas for display in frontend and on plots
"""

import ast
import re
import json
import inspect
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

class PythonToLatexConverter:
    """
    Converts Python mathematical functions to LaTeX notation
    Specialized for infinite products and divisor wave functions
    """
    
    def __init__(self):
        # Mathematical operation mappings
        self.math_mappings = {
            'np.sin': r'\sin',
            'math.sin': r'\sin',
            'np.cos': r'\cos', 
            'math.cos': r'\cos',
            'np.tan': r'\tan',
            'math.tan': r'\tan',
            'np.pi': r'\pi',
            'math.pi': r'\pi',
            'np.prod': r'\prod',
            'np.sum': r'\sum',
            'abs': r'\left|',
            'scipy.special.gamma': r'\Gamma',
            'np.exp': r'e^',
            'math.exp': r'e^',
            'cmath.exp': r'e^',
            'np.log': r'\log',
            'math.log': r'\log',
            'np.sqrt': r'\sqrt',
            'math.sqrt': r'\sqrt',
            '**': r'^',
            '*': r'\cdot',
        }
        
        # Pattern for identifying infinite products/sums
        self.product_patterns = [
            r'np\.prod\(\s*\[(.*?)\s+for\s+(\w+)\s+in\s+range\((\d+),\s*int\(([^)]+)\)\s*\+\s*1\)\]\)',
            r'np\.prod\(\s*\[(.*?)\s+for\s+(\w+)\s+in\s+range\((\d+),\s*([^)]+)\)\]\)',
        ]
        
        # Function name to LaTeX formula mappings for known functions
        self.known_formulas = self._initialize_known_formulas()
    
    def _initialize_known_formulas(self) -> Dict[str, str]:
        """Initialize LaTeX formulas for all known divisor wave functions"""
        return {
            'product_of_sin': r'f(z) = \left|\prod_{k=2}^{z} \beta \cdot \frac{z}{k} \cdot \sin\left(\frac{\pi z}{k}\right)\right|^{-m}',
            
            'product_of_product_representation_for_sin': r'g(z) = \left|\prod_{n=2}^{z} \beta \cdot \frac{z}{n} \cdot \left(\pi z \cdot \prod_{k=2}^{z} \left(1 - \frac{z^2}{n^2 k^2}\right)\right)\right|^{-m}',
            
            'cos_of_product_of_sin': r'h(z) = \cos\left(f(z)\right)',
            
            'sin_of_product_of_sin': r'h(z) = \sin\left(f(z)\right)',
            
            'cos_of_product_of_product_representation_of_sin': r'h(z) = \cos\left(g(z)\right)',
            
            'sin_of_product_of_product_representation_of_sin': r'h(z) = \sin\left(g(z)\right)',
            
            'Riesz_Product_for_Cos': r'R_{\cos}(z) = \left|\prod_{n=2}^{z} \left(1 + \cos(\pi z n)\right)\right|^{-m}',
            
            'Riesz_Product_for_Sin': r'R_{\sin}(z) = \left|\prod_{n=2}^{z} \left(1 + \sin(\pi z n)\right)\right|^{-m}',
            
            'Riesz_Product_for_Tan': r'R_{\tan}(z) = \left|\prod_{n=2}^{z} \left(1 + \tan(\pi z n)\right)\right|^{-m}',
            
            'Viete_Product_for_Cos': r'V_{\cos}(z) = \left|\prod_{n=2}^{z} \cos\left(\frac{\pi z}{2^n}\right)\right|^{-m}',
            
            'Viete_Product_for_Sin': r'V_{\sin}(z) = \left|\prod_{n=2}^{z} \sin\left(\frac{\pi z}{2^n}\right)\right|^{-m}',
            
            'Viete_Product_for_Tan': r'V_{\tan}(z) = \left|\prod_{n=2}^{z} \tan\left(\frac{\pi z}{2^n}\right)\right|^{-m}',
            
            'Half_Base_Viete_Product_for_Sin': r'V_{1/2}(z) = \left|\prod_{n=2}^{z} \sin\left(\frac{\pi z}{2^{-n}}\right)\right|^{-m}',
            
            'complex_playground_magnification_currated_functions_DEMO': r'D(z) = \left|\prod_{n=2}^{z} \left(iz_{\text{imag}} + iz_{\text{imag}} \sin(\pi z n)\right)^{iz_{\text{imag}}}\right|^{-m}',
            
            'Binary_Output_Prime_Indicator_Function_H': r'H(z) = f(z)^{g(z)}',
            
            'Prime_Output_Indicator_J': r'J(z) = f(z)^{f(z)^{g(z)}}',
        }
    
    def extract_formula_from_function(self, func) -> Optional[str]:
        """
        Extract LaTeX formula from a Python function by analyzing its source code
        """
        try:
            # First check if we have a known formula
            func_name = func.__name__
            if func_name in self.known_formulas:
                return self.known_formulas[func_name]
            
            # Get source code
            source = inspect.getsource(func)
            
            # Try to parse the mathematical expression
            latex_formula = self._parse_source_to_latex(source, func_name)
            
            return latex_formula
            
        except Exception as e:
            print(f"Could not extract formula from {func.__name__}: {e}")
            return None
    
    def _parse_source_to_latex(self, source: str, func_name: str) -> str:
        """
        Parse Python source code to extract mathematical formula
        """
        # Look for the main result calculation
        result_pattern = r'result\s*=\s*(.+?)(?=\n|\s*#|$)'
        matches = re.findall(result_pattern, source, re.MULTILINE | re.DOTALL)
        
        if not matches:
            return f"{func_name}(z) = \\text{{Complex mathematical function}}"
        
        # Get the most complex result assignment (usually the main formula)
        main_expr = max(matches, key=len).strip()
        
        # Convert to LaTeX
        latex_expr = self._convert_expression_to_latex(main_expr)
        
        return f"{func_name}(z) = {latex_expr}"
    
    def _convert_expression_to_latex(self, expr: str) -> str:
        """
        Convert a Python mathematical expression to LaTeX
        """
        # Handle infinite products
        for pattern in self.product_patterns:
            match = re.search(pattern, expr)
            if match:
                return self._convert_product_to_latex(match)
        
        # Handle basic mathematical operations
        latex_expr = expr
        
        # Replace mathematical functions
        for py_func, latex_func in self.math_mappings.items():
            latex_expr = latex_expr.replace(py_func, latex_func)
        
        # Handle abs() with proper LaTeX delimiters
        latex_expr = re.sub(r'abs\((.*?)\)', r'\\left|\\1\\right|', latex_expr)
        
        # Handle exponentiation
        latex_expr = re.sub(r'\*\*\s*\((.*?)\)', r'^{\\1}', latex_expr)
        latex_expr = re.sub(r'\*\*\s*(-?\w+)', r'^{\\1}', latex_expr)
        
        # Handle fractions
        latex_expr = re.sub(r'(\w+)\s*/\s*(\w+)', r'\\frac{\\1}{\\2}', latex_expr)
        
        return latex_expr
    
    def _convert_product_to_latex(self, match) -> str:
        """
        Convert an infinite product to LaTeX notation
        """
        expr, var, start, end = match.groups()
        
        # Clean up the expression
        expr = expr.strip()
        
        # Convert the inner expression
        latex_inner = self._convert_expression_to_latex(expr)
        
        return f"\\prod_{{{var}={start}}}^{{{end}}} {latex_inner}"
    
    def get_function_formula(self, func_name: str, func_obj=None) -> str:
        """
        Get LaTeX formula for a given function name or object
        """
        # Lambda function mapping to JSON names
        lambda_mapping = {
            '1': 'product_of_sin',
            '2': 'product_of_product_representation_for_sin',
            '3': 'product_of_product_representation_for_sin',
            '5': 'Riesz_Product_for_Cos',
            '6': 'Riesz_Product_for_Sin',
            '7': 'Riesz_Product_for_Tan',
            '8': 'Viete_Product_for_Cos',
            '9': 'Viete_Product_for_Sin',
            '10': 'Viete_Product_for_Tan',
            '11': 'cos_of_product_of_sin',
            '12': 'sin_of_product_of_sin',
            '13': 'cos_of_product_of_product_representation_of_sin',
            '14': 'sin_of_product_of_product_representation_of_sin',
            '15': 'Binary_Output_Prime_Indicator_Function_H',
            '16': 'Prime_Output_Indicator_J',
            '17': 'BOPIF_Q_Alternation_Series',
            '18': 'Dirichlet_Eta_Derived_From_BOPIF'
        }
        
        # Map lambda function numbers to actual function names
        mapped_name = lambda_mapping.get(func_name, func_name)
        
        # First try to load from divisor_wave_formulas.json
        try:
            json_path = Path(__file__).parent / "divisor_wave_formulas.json"
            if json_path.exists():
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if mapped_name in data.get("formulas", {}):
                        return data["formulas"][mapped_name]["latex"]
        except Exception as e:
            print(f"Error loading from divisor_wave_formulas.json: {e}")
        
        # Try custom_functions.json
        try:
            custom_json_path = Path(__file__).parent / "custom_functions.json"
            if custom_json_path.exists():
                with open(custom_json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if mapped_name in data.get("functions", {}):
                        return data["functions"][mapped_name]["latex_formula"]
        except Exception as e:
            print(f"Error loading from custom_functions.json: {e}")
        
        # Check known formulas in memory
        if mapped_name in self.known_formulas:
            return self.known_formulas[mapped_name]
        
        # Try to extract from function object
        if func_obj:
            extracted = self.extract_formula_from_function(func_obj)
            if extracted:
                return extracted
        
        # Return a generic formula
        return f"{func_name}(z) = \\text{{Mathematical function of complex variable z}}"
    
    def add_custom_formula(self, func_name: str, latex_formula: str):
        """
        Add a custom LaTeX formula for a function
        """
        self.known_formulas[func_name] = latex_formula
    
    def export_all_formulas(self) -> Dict[str, str]:
        """
        Export all known LaTeX formulas
        """
        return self.known_formulas.copy()
    
    def save_formulas_to_json(self, filepath: str):
        """
        Save all formulas to a JSON file
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.known_formulas, f, indent=2, ensure_ascii=False)
    
    def load_formulas_from_json(self, filepath: str):
        """
        Load formulas from a JSON file
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                loaded_formulas = json.load(f)
                self.known_formulas.update(loaded_formulas)
        except FileNotFoundError:
            print(f"Formula file {filepath} not found")
    
    def create_latex_for_coefficients(self, m: float, beta: float, normalize_type: str) -> str:
        """
        Create LaTeX representation of coefficients
        """
        coeff_latex = f"m = {m}, \\beta = {beta}"
        
        if normalize_type == 'Y':
            coeff_latex += ", \\text{with } \\Gamma \\text{ normalization}"
        
        return coeff_latex


# Example usage and testing
if __name__ == "__main__":
    converter = PythonToLatexConverter()
    
    # Test with known function names
    test_functions = [
        'product_of_sin',
        'product_of_product_representation_for_sin',
        'Riesz_Product_for_Cos',
        'Viete_Product_for_Sin'
    ]
    
    print("LaTeX Formulas for Divisor Wave Functions:")
    print("=" * 60)
    
    for func_name in test_functions:
        formula = converter.get_function_formula(func_name)
        print(f"\n{func_name}:")
        print(f"  {formula}")
    
    # Save all formulas
    converter.save_formulas_to_json("divisor_wave_formulas.json")
    print(f"\nSaved {len(converter.known_formulas)} formulas to divisor_wave_formulas.json")