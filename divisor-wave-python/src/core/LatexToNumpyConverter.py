"""
LaTeX to NumPy Converter System
Converts mathematical LaTeX formulas to executable NumPy product representations
Uses Special_Functions.py as the canonical reference for infinite products
"""

import re
import json
import sympy as sp
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
import ast

class LatexToNumpyConverter:
    """
    Advanced LaTeX to NumPy converter for infinite products and mathematical formulas
    """
    
    def __init__(self, special_functions_path: str = None):
        """Initialize with patterns from Special_Functions.py"""
        self.patterns = {}
        self.function_templates = {}
        self.json_db_path = "custom_formulas_database.json"
        
        # Initialize pattern recognition from Special_Functions.py
        self._initialize_patterns()
        self._load_existing_database()
    
    def _initialize_patterns(self):
        """Extract patterns from Special_Functions.py to create conversion templates"""
        
        # Core infinite product patterns recognized
        self.patterns = {
            # Product of Sin pattern: ∏_{k=2}^x sin(πz/k)
            'product_of_sin': {
                'latex_pattern': r'\\prod_\{([^}]+)=([^}]+)\}\^[{]?([^}]*)[}]?.*?\\sin\\left\(\\frac\{\\pi ([^}]+)\}\{([^}]+)\}\\right\)',
                'template': 'np.prod([{beta} * ({z_real} / k) * np.sin(math.pi * ({z_real} + 1j * {z_imag}) / k) for k in range({start}, int({z_real}) + 1)])',
                'parameters': ['beta', 'z_real', 'z_imag', 'start']
            },
            
            # Double product pattern: ∏_{k=2}^x ∏_{n=2}^x (1 - z²/(k²n²))
            'double_product': {
                'latex_pattern': r'\\prod_\{([^}]+)=([^}]+)\}\^[{]?([^}]*)[}]?.*?\\prod_\{([^}]+)=([^}]+)\}\^[{]?([^}]*)[}]?.*?\(1-\\frac\{([^}]+)\}\{([^}]+)\}\)',
                'template': '''np.prod([{beta} * ({z_real} / n) * (({z_real} + 1j * {z_imag}) * math.pi) * np.prod([1 - (({z_real} + 1j * {z_imag}) ** 2) / ((n ** 2) * (k ** 2)) for k in range({start}, int({z_real}) + 1)]) for n in range({start}, int({z_real}) + 1)])''',
                'parameters': ['beta', 'z_real', 'z_imag', 'start']
            },
            
            # Viète product pattern: ∏_{n=2}^x cos(πz/2^n)
            'viete_product': {
                'latex_pattern': r'\\prod_\{([^}]+)=([^}]+)\}\^[{]?([^}]*)[}]?.*?\\cos\\left\(\\frac\{\\pi ([^}]+)\}\{2\^\{([^}]+)\}\}\\right\)',
                'template': 'np.prod([np.cos(math.pi * ({z_real} + 1j * {z_imag}) / (2 ** n)) for n in range({start}, int({z_real}) + 1)])',
                'parameters': ['z_real', 'z_imag', 'start']
            },
            
            # Riesz product pattern: ∏_{n=2}^x (1 + cos(πzn))
            'riesz_product': {
                'latex_pattern': r'\\prod_\{([^}]+)=([^}]+)\}\^[{]?([^}]*)[}]?.*?\(1 \+ \\cos\(\\pi ([^}]+) ([^}]+)\)\)',
                'template': 'np.prod([1 + np.cos(math.pi * ({z_real} + 1j * {z_imag}) * n) for n in range({start}, int({z_real}) + 1)])',
                'parameters': ['z_real', 'z_imag', 'start']
            },
            
            # Nested roots pattern: ∏_{n=2}^x ∜[n]{...}
            'nested_roots': {
                'latex_pattern': r'\\prod_\{([^}]+)=([^}]+)\}\^[{]?([^}]*)[}]?.*?\\sqrt\[([^]]+)\]\{',
                'template': '''np.prod([inner_product for n in range({start}, max_n + 1)] where inner_product involves nested computation)''',
                'parameters': ['z_real', 'z_imag', 'start', 'max_n']
            }
        }
    
    def parse_latex_formula(self, latex_formula: str) -> Dict:
        """
        Parse LaTeX formula and identify the mathematical pattern
        
        Args:
            latex_formula: LaTeX string representing the mathematical formula
            
        Returns:
            Dictionary with pattern info, parameters, and conversion metadata
        """
        latex_clean = latex_formula.strip().replace(' ', '')
        
        for pattern_name, pattern_info in self.patterns.items():
            pattern = pattern_info['latex_pattern']
            match = re.search(pattern, latex_clean)
            
            if match:
                return {
                    'pattern_type': pattern_name,
                    'matched_groups': match.groups(),
                    'template': pattern_info['template'],
                    'parameters': pattern_info['parameters'],
                    'original_latex': latex_formula,
                    'success': True
                }
        
        # If no pattern matches, try to use SymPy for general parsing
        return self._fallback_sympy_parsing(latex_formula)
    
    def _fallback_sympy_parsing(self, latex_formula: str) -> Dict:
        """Use SymPy to parse general LaTeX expressions"""
        try:
            # Convert LaTeX to SymPy expression
            from sympy.parsing.latex import parse_latex
            expr = parse_latex(latex_formula)
            
            # Try to identify if it's a product
            if hasattr(expr, 'is_Product') or 'Product' in str(type(expr)):
                return {
                    'pattern_type': 'general_product',
                    'sympy_expression': expr,
                    'original_latex': latex_formula,
                    'success': True,
                    'requires_manual_conversion': True
                }
            else:
                return {
                    'pattern_type': 'general_expression',
                    'sympy_expression': expr,
                    'original_latex': latex_formula,
                    'success': True,
                    'requires_manual_conversion': True
                }
                
        except Exception as e:
            return {
                'pattern_type': 'unknown',
                'original_latex': latex_formula,
                'success': False,
                'error': str(e)
            }
    
    def generate_numpy_code(self, parsed_formula: Dict, 
                          custom_parameters: Dict = None) -> str:
        """
        Generate executable NumPy code from parsed LaTeX formula
        
        Args:
            parsed_formula: Result from parse_latex_formula
            custom_parameters: Override default parameters
            
        Returns:
            Executable NumPy code string
        """
        if not parsed_formula['success']:
            raise ValueError(f"Cannot generate code for failed parse: {parsed_formula.get('error', 'Unknown error')}")
        
        pattern_type = parsed_formula['pattern_type']
        
        if pattern_type in self.patterns:
            template = parsed_formula['template']
            
            # Default parameters
            default_params = {
                'z_real': 'np.real(z)',
                'z_imag': 'np.imag(z)',
                'beta': '1.0',
                'start': '2',
                'max_n': 'min(int(abs(z_real)) + 1, 50)'
            }
            
            # Override with custom parameters
            if custom_parameters:
                default_params.update(custom_parameters)
            
            # Format the template
            try:
                numpy_code = template.format(**default_params)
                return numpy_code
            except KeyError as e:
                raise ValueError(f"Missing parameter for template: {e}")
        
        elif pattern_type == 'general_product':
            # Generate code for general SymPy products
            return self._generate_from_sympy(parsed_formula['sympy_expression'])
        
        else:
            raise ValueError(f"Cannot generate NumPy code for pattern type: {pattern_type}")
    
    def _generate_from_sympy(self, sympy_expr) -> str:
        """Generate NumPy code from SymPy expression"""
        # This is a simplified version - would need extensive development
        return f"# Generated from SymPy: {sympy_expr}\n# Manual conversion required"
    
    def create_executable_function(self, latex_formula: str, 
                                 function_name: str,
                                 description: str = "",
                                 custom_parameters: Dict = None) -> Dict:
        """
        Create a complete executable function from LaTeX formula
        
        Args:
            latex_formula: LaTeX representation of the mathematical formula
            function_name: Name for the generated function
            description: Human-readable description
            custom_parameters: Custom parameter values
            
        Returns:
            Dictionary with function code, metadata, and execution info
        """
        # Parse the LaTeX
        parsed = self.parse_latex_formula(latex_formula)
        
        if not parsed['success']:
            raise ValueError(f"Failed to parse LaTeX formula: {parsed.get('error')}")
        
        # Generate NumPy code
        numpy_code = self.generate_numpy_code(parsed, custom_parameters)
        
        # Create complete function
        function_template = f'''
def {function_name}(z, normalize_type='Y'):
    """
    Generated function: {description}
    LaTeX: {latex_formula}
    Pattern: {parsed['pattern_type']}
    """
    import numpy as np
    import math
    
    z_real = np.real(z)
    z_imag = np.imag(z)
    
    try:
        # Generated computation
        result = abs({numpy_code}) ** (-0.1)  # Default magnification
        
        if normalize_type == 'Y':
            import scipy.special
            result = result / scipy.special.gamma(result)
        
        return result
    except Exception:
        return 0.0
'''
        
        function_data = {
            'name': function_name,
            'description': description,
            'latex_formula': latex_formula,
            'pattern_type': parsed['pattern_type'],
            'numpy_code': numpy_code,
            'complete_function': function_template,
            'parameters': custom_parameters or {},
            'created_timestamp': str(np.datetime64('now')),
            'executable': True
        }
        
        return function_data
    
    def save_to_database(self, function_data: Dict) -> bool:
        """Save generated function to JSON database"""
        try:
            # Load existing database
            database = self._load_existing_database()
            
            # Add new function
            database['custom_functions'][function_data['name']] = function_data
            database['metadata']['total_functions'] = len(database['custom_functions'])
            database['metadata']['last_updated'] = str(np.datetime64('now'))
            
            # Save to file
            with open(self.json_db_path, 'w') as f:
                json.dump(database, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error saving to database: {e}")
            return False
    
    def _load_existing_database(self) -> Dict:
        """Load existing database or create new one"""
        try:
            if Path(self.json_db_path).exists():
                with open(self.json_db_path, 'r') as f:
                    return json.load(f)
            else:
                # Create new database structure
                return {
                    'metadata': {
                        'version': '1.0',
                        'total_functions': 0,
                        'created': str(np.datetime64('now')),
                        'last_updated': str(np.datetime64('now'))
                    },
                    'custom_functions': {},
                    'pattern_templates': self.patterns
                }
        except Exception:
            # Return empty database on error
            return {
                'metadata': {'version': '1.0', 'total_functions': 0},
                'custom_functions': {},
                'pattern_templates': {}
            }
    
    def load_function_from_database(self, function_name: str) -> Optional[Dict]:
        """Load a specific function from the database"""
        database = self._load_existing_database()
        return database['custom_functions'].get(function_name)
    
    def list_all_functions(self) -> List[str]:
        """List all available functions in the database"""
        database = self._load_existing_database()
        return list(database['custom_functions'].keys())
    
    def export_database(self, export_path: str) -> bool:
        """Export database to specified path for sharing"""
        try:
            database = self._load_existing_database()
            with open(export_path, 'w') as f:
                json.dump(database, f, indent=2)
            return True
        except Exception:
            return False
    
    def import_database(self, import_path: str, merge: bool = True) -> bool:
        """Import database from file"""
        try:
            with open(import_path, 'r') as f:
                imported_db = json.load(f)
            
            if merge:
                # Merge with existing database
                existing_db = self._load_existing_database()
                existing_db['custom_functions'].update(imported_db['custom_functions'])
                database = existing_db
            else:
                # Replace existing database
                database = imported_db
            
            with open(self.json_db_path, 'w') as f:
                json.dump(database, f, indent=2)
            
            return True
        except Exception:
            return False

# Example usage and testing
if __name__ == "__main__":
    converter = LatexToNumpyConverter()
    
    # Test LaTeX formulas
    test_formulas = [
        r"\prod_{k=2}^x \sin\left(\frac{\pi z}{k}\right)",
        r"\prod_{k=2}^x \prod_{n=2}^x \left(1-\frac{z^2}{k^2 n^2}\right)",
        r"\prod_{n=2}^x \cos\left(\frac{\pi z}{2^n}\right)"
    ]
    
    for i, formula in enumerate(test_formulas):
        print(f"\n--- Test {i+1} ---")
        print(f"LaTeX: {formula}")
        
        try:
            parsed = converter.parse_latex_formula(formula)
            print(f"Pattern: {parsed['pattern_type']}")
            
            if parsed['success']:
                numpy_code = converter.generate_numpy_code(parsed)
                print(f"NumPy: {numpy_code}")
                
                # Create complete function
                func_data = converter.create_executable_function(
                    formula, 
                    f"custom_function_{i+1}",
                    f"Test function {i+1}"
                )
                
                print(f"Function created: {func_data['name']}")
                
                # Save to database
                saved = converter.save_to_database(func_data)
                print(f"Saved to database: {saved}")
            
        except Exception as e:
            print(f"Error: {e}")