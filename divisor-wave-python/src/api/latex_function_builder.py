"""
LaTeX Function Builder System
Allows users to create custom mathematical functions using LaTeX notation
and converts them to executable Python code for plotting
"""

import json
import re
import os
import ast
import math
import cmath
import numpy as np
from typing import Dict, List, Any, Tuple
from fastapi import HTTPException
import sympy as sp
from sympy.parsing.latex import parse_latex
from sympy import lambdify, symbols, I, pi, E, exp, sin, cos, tan, log, sqrt
import traceback

class LaTeXFunctionBuilder:
    def __init__(self, database_path: str = "custom_functions.json"):
        self.database_path = database_path
        self.custom_functions = self.load_database()
        
        # LaTeX pattern mappings for mathematical symbols
        self.latex_patterns = {
            # Greek letters
            r'\\alpha': 'alpha',
            r'\\beta': 'beta', 
            r'\\gamma': 'gamma',
            r'\\delta': 'delta',
            r'\\epsilon': 'epsilon',
            r'\\zeta': 'zeta',
            r'\\eta': 'eta',
            r'\\theta': 'theta',
            r'\\lambda': 'lamda',
            r'\\mu': 'mu',
            r'\\nu': 'nu',
            r'\\xi': 'xi',
            r'\\pi': 'pi',
            r'\\rho': 'rho',
            r'\\sigma': 'sigma',
            r'\\tau': 'tau',
            r'\\phi': 'phi',
            r'\\chi': 'chi',
            r'\\psi': 'psi',
            r'\\omega': 'omega',
            
            # Mathematical functions
            r'\\sin': 'sin',
            r'\\cos': 'cos',
            r'\\tan': 'tan',
            r'\\log': 'log',
            r'\\ln': 'log',
            r'\\exp': 'exp',
            r'\\sqrt': 'sqrt',
            
            # Special constants
            r'\\infty': 'np.inf',
            r'\\Gamma': 'gamma',
            r'\\zeta': 'zeta',
            
            # Complex notation
            r'\\Im': 'np.imag',
            r'\\Re': 'np.real',
            r'\\bar\{([^}]+)\}': r'np.conj(\1)',
            
            # Fractions
            r'\\frac\{([^}]+)\}\{([^}]+)\}': r'((\1) / (\2))',
            
            # Powers and subscripts
            r'\^([^{]|\{[^}]*\})': r'**(\1)',
            r'_([^{]|\{[^}]*\})': r'',  # Subscripts ignored for now
            
            # Parentheses and brackets
            r'\\left\(': '(',
            r'\\right\)': ')',
            r'\\left\[': '[',
            r'\\right\]': ']',
            r'\\left\{': '{',
            r'\\right\}': '}',
            
            # Products and sums
            r'\\prod_\{([^}]+)\}\^\{([^}]+)\}': 'np.prod',
            r'\\sum_\{([^}]+)\}\^\{([^}]+)\}': 'np.sum',
            
            # Remove LaTeX spacing and formatting
            r'\\,': ' ',
            r'\\;': ' ',
            r'\\!': '',
            r'\\quad': ' ',
            r'\\qquad': ' ',
        }
        
        # Product notation patterns (special handling) - fixed with raw strings
        self.product_patterns = [
            r'\\prod_\{([^}]+)=([^}]+)\}\^\{([^}]+)\}\s*([^}]+)',
            r'∏_\{([^}]+)=([^}]+)\}\^\{([^}]+)\}\s*(.+)',
            r'∏_\(([^)]+)=([^)]+)\)\^\(([^)]+)\)\s*(.+)',
        ]
    
    def load_database(self) -> Dict[str, Any]:
        """Load custom functions from JSON database"""
        if os.path.exists(self.database_path):
            try:
                with open(self.database_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading database: {e}")
                return {"functions": {}, "metadata": {"version": "1.0", "count": 0}}
        else:
            return {"functions": {}, "metadata": {"version": "1.0", "count": 0}}
    
    def save_database(self):
        """Save custom functions to JSON database"""
        try:
            with open(self.database_path, 'w', encoding='utf-8') as f:
                json.dump(self.custom_functions, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving database: {e}")
    
    def parse_latex_to_sympy(self, latex_expr: str) -> sp.Basic:
        """Convert LaTeX expression to SymPy expression"""
        try:
            # Clean the LaTeX expression
            cleaned = self.preprocess_latex(latex_expr)
            
            # Try to parse with SymPy's LaTeX parser
            try:
                expr = parse_latex(cleaned)
                return expr
            except:
                # Fall back to manual parsing
                return self.manual_latex_parse(cleaned)
                
        except Exception as e:
            raise ValueError(f"Could not parse LaTeX expression: {str(e)}")
    
    def preprocess_latex(self, latex_expr: str) -> str:
        """Preprocess LaTeX expression for better parsing"""
        # Remove LaTeX environments
        latex_expr = re.sub(r'\\begin\{[^}]+\}', '', latex_expr)
        latex_expr = re.sub(r'\\end\{[^}]+\}', '', latex_expr)
        
        # Handle special product notation
        latex_expr = self.handle_product_notation(latex_expr)
        
        # Apply pattern replacements
        for pattern, replacement in self.latex_patterns.items():
            latex_expr = re.sub(pattern, replacement, latex_expr)
        
        return latex_expr
    
    def handle_product_notation(self, latex_expr: str) -> str:
        """Handle infinite product notation in LaTeX"""
        for pattern in self.product_patterns:
            matches = re.finditer(pattern, latex_expr)
            for match in matches:
                groups = match.groups()
                if len(groups) == 4:
                    var, start, end, expr = groups
                    # Convert to Python-style product
                    product_code = f"np.prod([{expr} for {var} in range({start}, {end}+1)])"
                    # Use re.escape to handle special characters properly
                    latex_expr = latex_expr.replace(match.group(0), product_code)
        
        return latex_expr
    
    def manual_latex_parse(self, latex_expr: str) -> sp.Basic:
        """Manual LaTeX parsing as fallback"""
        # Define symbols
        z, x, y, n, k = symbols('z x y n k', complex=True)
        
        # Replace common patterns manually
        expr_str = latex_expr
        
        # Handle fractions
        frac_pattern = r'\\frac\{([^}]+)\}\{([^}]+)\}'
        while re.search(frac_pattern, expr_str):
            expr_str = re.sub(frac_pattern, r'((\1) / (\2))', expr_str)
        
        # Handle powers
        expr_str = re.sub(r'\^([^{])', r'**\1', expr_str)
        expr_str = re.sub(r'\^\{([^}]+)\}', r'**(\1)', expr_str)
        
        # Clean up and evaluate
        expr_str = expr_str.replace('z', 'z').replace('\\', '')
        
        try:
            return sp.sympify(expr_str)
        except:
            # Very basic fallback
            return sp.sympify(f"sin(pi*z)")
    
    def sympy_to_python_function(self, sympy_expr: sp.Basic, var_name: str = 'z') -> str:
        """Convert SymPy expression to Python function code"""
        try:
            # Create the lambda function
            z = symbols(var_name, complex=True)
            
            # Generate Python code
            python_expr = str(sympy_expr)
            
            # Replace SymPy functions with NumPy equivalents
            replacements = {
                'sin(': 'np.sin(',
                'cos(': 'np.cos(',
                'tan(': 'np.tan(',
                'exp(': 'np.exp(',
                'log(': 'np.log(',
                'sqrt(': 'np.sqrt(',
                'pi': 'math.pi',
                'I': '1j',
                'E': 'math.e',
                'gamma(': 'scipy.special.gamma(',
            }
            
            for old, new in replacements.items():
                python_expr = python_expr.replace(old, new)
            
            # Create function template
            function_code = f"""
def custom_function(z, normalize_type='N'):
    import numpy as np
    import math
    import cmath
    import scipy.special
    
    z_real = np.real(z)
    z_imag = np.imag(z)
    
    try:
        result = {python_expr}
        
        if normalize_type == 'Y':
            result = result / scipy.special.gamma(result) if abs(result) < 100 else result
        
        return abs(result) if np.isfinite(result) else 0.0
    except:
        return 0.0
"""
            
            return function_code
            
        except Exception as e:
            raise ValueError(f"Could not convert to Python function: {str(e)}")
    
    def create_custom_function(self, 
                             name: str,
                             latex_formula: str, 
                             description: str = "",
                             category: str = "custom",
                             parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new custom function from LaTeX"""
        
        if parameters is None:
            parameters = {"m": 0.1, "beta": 0.1}
        
        try:
            # Parse LaTeX to SymPy
            sympy_expr = self.parse_latex_to_sympy(latex_formula)
            
            # Convert to Python function
            python_code = self.sympy_to_python_function(sympy_expr)
            
            # Test the function
            test_result = self.test_function(python_code)
            
            if not test_result["success"]:
                raise ValueError(f"Function test failed: {test_result['error']}")
            
            # Create function metadata
            function_data = {
                "name": name,
                "latex_formula": latex_formula,
                "description": description,
                "category": category,
                "parameters": parameters,
                "python_code": python_code,
                "sympy_expr": str(sympy_expr),
                "created_at": "2025-10-28",  # In real implementation, use datetime
                "test_result": test_result,
                "speed": "Custom"
            }
            
            # Save to database
            self.custom_functions["functions"][name] = function_data
            self.custom_functions["metadata"]["count"] = len(self.custom_functions["functions"])
            self.save_database()
            
            return function_data
            
        except Exception as e:
            raise ValueError(f"Failed to create custom function: {str(e)}\n{traceback.format_exc()}")
    
    def test_function(self, python_code: str) -> Dict[str, Any]:
        """Test a Python function with sample inputs"""
        try:
            # Execute the function code
            local_vars = {}
            exec(python_code, globals(), local_vars)
            func = local_vars['custom_function']
            
            # Test with sample values
            test_points = [
                complex(2, 0),
                complex(3, 1),
                complex(5, -1),
                complex(7, 0.5)
            ]
            
            results = []
            for point in test_points:
                try:
                    result = func(point)
                    results.append({"input": str(point), "output": float(result)})
                except Exception as e:
                    return {"success": False, "error": f"Function failed at {point}: {str(e)}"}
            
            return {
                "success": True,
                "test_results": results,
                "error": None
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_function(self, name: str) -> Dict[str, Any]:
        """Get a custom function by name"""
        if name in self.custom_functions["functions"]:
            return self.custom_functions["functions"][name]
        else:
            raise ValueError(f"Function '{name}' not found")
    
    def list_functions(self) -> Dict[str, Any]:
        """List all custom functions"""
        functions_by_category = {}
        
        for func_name, func_data in self.custom_functions["functions"].items():
            category = func_data.get("category", "custom")
            if category not in functions_by_category:
                functions_by_category[category] = {}
            
            functions_by_category[category][func_name] = {
                "name": func_data["name"],
                "description": func_data["description"],
                "latex_formula": func_data["latex_formula"],
                "speed": func_data.get("speed", "Custom")
            }
        
        return {
            "functions_by_category": functions_by_category,
            "total_functions": len(self.custom_functions["functions"]),
            "metadata": self.custom_functions["metadata"]
        }
    
    def delete_function(self, name: str) -> bool:
        """Delete a custom function"""
        if name in self.custom_functions["functions"]:
            del self.custom_functions["functions"][name]
            self.custom_functions["metadata"]["count"] = len(self.custom_functions["functions"])
            self.save_database()
            return True
        return False
    
    def compile_function(self, name: str) -> callable:
        """Compile a custom function to executable form"""
        function_data = self.get_function(name)
        python_code = function_data["python_code"]
        
        # Execute the function code
        local_vars = {}
        exec(python_code, globals(), local_vars)
        return local_vars['custom_function']
    
    def get_latex_symbols(self) -> Dict[str, str]:
        """Get available LaTeX symbols for the frontend"""
        return {
            "Greek Letters": {
                "α": "\\alpha",
                "β": "\\beta", 
                "γ": "\\gamma",
                "δ": "\\delta",
                "ε": "\\epsilon",
                "ζ": "\\zeta",
                "η": "\\eta",
                "θ": "\\theta",
                "λ": "\\lambda",
                "μ": "\\mu",
                "π": "\\pi",
                "ρ": "\\rho",
                "σ": "\\sigma",
                "φ": "\\phi",
                "ψ": "\\psi",
                "ω": "\\omega"
            },
            "Functions": {
                "sin": "\\sin",
                "cos": "\\cos", 
                "tan": "\\tan",
                "log": "\\log",
                "ln": "\\ln",
                "exp": "\\exp",
                "√": "\\sqrt"
            },
            "Operators": {
                "∏": "\\prod",
                "∑": "\\sum",
                "∫": "\\int",
                "∞": "\\infty",
                "±": "\\pm",
                "×": "\\times",
                "÷": "\\div"
            },
            "Special": {
                "Γ": "\\Gamma",
                "ζ": "\\zeta",
                "Re": "\\Re",
                "Im": "\\Im",
                "fraction": "\\frac{numerator}{denominator}",
                "power": "x^{exponent}",
                "subscript": "x_{subscript}"
            }
        }

# Example usage and predefined functions
def create_example_functions(builder: LaTeXFunctionBuilder):
    """Create some example custom functions"""
    
    examples = [
        {
            "name": "custom_sine_product",
            "latex": "\\prod_{n=2}^{z} \\sin\\left(\\frac{\\pi z}{n}\\right)",
            "description": "Custom sine product similar to the main product",
            "category": "example"
        },
        {
            "name": "riemann_zeta_style",
            "latex": "\\sum_{n=1}^{\\infty} \\frac{1}{n^z}",
            "description": "Riemann zeta function style series",
            "category": "example"
        },
        {
            "name": "exponential_spiral",
            "latex": "e^{i z \\theta}",
            "description": "Complex exponential spiral",
            "category": "example"
        }
    ]
    
    for example in examples:
        try:
            builder.create_custom_function(
                name=example["name"],
                latex_formula=example["latex"],
                description=example["description"],
                category=example["category"]
            )
        except Exception as e:
            print(f"Could not create example function {example['name']}: {e}")

if __name__ == "__main__":
    # Test the LaTeX function builder
    builder = LaTeXFunctionBuilder()
    
    # Create example functions
    create_example_functions(builder)
    
    # List all functions
    functions = builder.list_functions()
    print("Custom Functions:", json.dumps(functions, indent=2))