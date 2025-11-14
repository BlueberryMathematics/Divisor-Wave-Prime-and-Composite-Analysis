"""
Mathematical Function Generator - Systematic Function Creation System
Creates new mathematical functions by systematically combining existing components
Focus on infinite series generation using established mathematical rules
"""

import random
import math
import json
import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Callable
from pathlib import Path
import itertools
from dataclasses import dataclass
from enum import Enum

# Import existing system components
from .special_functions_library import SpecialFunctionsLibrary
from .latex_function_builder import LaTeXFunctionBuilder
from .latex_to_numpy_converter import LatexToNumpyConverter

class SeriesType(Enum):
    """Types of infinite series we can generate"""
    INFINITE_SUM = "infinite_sum"
    INFINITE_PRODUCT = "infinite_product"
    NESTED_SERIES = "nested_series"
    HYBRID_SERIES = "hybrid_series"

class OperatorType(Enum):
    """Mathematical operators available for function generation"""
    SIN = "sin"
    COS = "cos"
    TAN = "tan"
    EXP = "exp"
    LOG = "log"
    SINH = "sinh"
    COSH = "cosh"
    TANH = "tanh"
    GAMMA = "gamma"
    ZETA = "zeta"

class IndexType(Enum):
    """Types of summation/product indices"""
    LINEAR = "linear"          # n, k, j
    QUADRATIC = "quadratic"    # n², k², j²
    CUBIC = "cubic"           # n³, k³, j³
    EXPONENTIAL = "exponential" # 2^n, 3^n
    FACTORIAL = "factorial"    # n!
    PRIME = "prime"           # prime numbers
    FIBONACCI = "fibonacci"   # Fibonacci sequence

@dataclass
class FunctionComponent:
    """Represents a mathematical function component"""
    operator: OperatorType
    argument: str  # The argument to the operator (e.g., "pi*z/n")
    coefficient: str = "1"  # Coefficient multiplying the component
    power: str = "1"  # Power to which the component is raised

@dataclass
class SeriesStructure:
    """Represents the structure of an infinite series"""
    series_type: SeriesType
    index_variable: str
    start_value: str
    end_value: str
    index_type: IndexType
    components: List[FunctionComponent]

@dataclass
class GeneratedFunction:
    """Represents a complete generated mathematical function"""
    name: str
    latex_formula: str
    python_code: str
    series_structure: SeriesStructure
    description: str
    category: str
    complexity_score: float
    mathematical_properties: Dict[str, Any]


class MathematicalFunctionGenerator:
    """
    Advanced mathematical function generator using systematic combination
    of existing components from the divisor wave analysis system.
    """
    
    def __init__(self):
        """Initialize the function generator with existing system components"""
        
        # Load existing system components
        self.special_functions = SpecialFunctionsLibrary()
        self.latex_builder = LaTeXFunctionBuilder()
        self.latex_converter = LatexToNumpyConverter()
        
        # Load existing functions from all sources
        self.existing_functions = self._load_all_existing_functions()
        
        # Mathematical building blocks extracted from existing system
        self.initialize_building_blocks()
        
        # Rules for infinite series construction
        self.initialize_series_rules()
        
        # AI evaluation interface
        self.ai_evaluator = None  # Will be set when needed
        
        # Statistics tracking
        self.generation_stats = {
            'total_generated': 0,
            'accepted_by_ai': 0,
            'rejected_by_ai': 0,
            'series_types_generated': {},
            'operator_usage': {},
            'complexity_distribution': []
        }
    
    def _load_all_existing_functions(self) -> Dict[str, Any]:
        """Load all existing functions from JSONs and special functions library"""
        
        functions = {}
        
        # Load from custom_functions.json
        try:
            with open('src/data/formulas/custom_functions.json', 'r') as f:
                custom_data = json.load(f)
                if 'functions' in custom_data:
                    functions.update(custom_data['functions'])
        except FileNotFoundError:
            print("custom_functions.json not found, using empty set")
        
        # Get functions from special functions library
        available_functions = self.special_functions.get_available_functions()
        functions.update(available_functions)
        
        # Extract lambda library functions
        lambda_catalog = self.special_functions.lamda_function_library(catalog_only=True)
        functions.update(lambda_catalog)
        
        print(f"Loaded {len(functions)} existing functions for reference")
        return functions
    
    def initialize_building_blocks(self):
        """Initialize mathematical building blocks from existing system"""
        
        # Basic operators from the system
        self.operators = {
            OperatorType.SIN: {
                'latex': r'\\sin\\left({arg}\\right)',
                'python': 'np.sin({arg})',
                'domain': 'complex',
                'range': '[-1, 1] for real args'
            },
            OperatorType.COS: {
                'latex': r'\\cos\\left({arg}\\right)',
                'python': 'np.cos({arg})',
                'domain': 'complex',
                'range': '[-1, 1] for real args'
            },
            OperatorType.TAN: {
                'latex': r'\\tan\\left({arg}\\right)',
                'python': 'np.tan({arg})',
                'domain': 'complex with restrictions',
                'range': 'real'
            },
            OperatorType.EXP: {
                'latex': r'e^{{{arg}}}',
                'python': 'np.exp({arg})',
                'domain': 'complex',
                'range': 'complex non-zero'
            },
            OperatorType.LOG: {
                'latex': r'\\log\\left({arg}\\right)',
                'python': 'np.log({arg})',
                'domain': 'complex non-zero',
                'range': 'complex'
            },
            OperatorType.SINH: {
                'latex': r'\\sinh\\left({arg}\\right)',
                'python': 'np.sinh({arg})',
                'domain': 'complex',
                'range': 'complex'
            },
            OperatorType.COSH: {
                'latex': r'\\cosh\\left({arg}\\right)',
                'python': 'np.cosh({arg})',
                'domain': 'complex',
                'range': 'complex, >= 1 for real args'
            },
            OperatorType.TANH: {
                'latex': r'\\tanh\\left({arg}\\right)',
                'python': 'np.tanh({arg})',
                'domain': 'complex',
                'range': '(-1, 1) for real args'
            },
            OperatorType.GAMMA: {
                'latex': r'\\Gamma\\left({arg}\\right)',
                'python': 'scipy.special.gamma({arg})',
                'domain': 'complex, not negative integers',
                'range': 'complex'
            },
            OperatorType.ZETA: {
                'latex': r'\\zeta\\left({arg}\\right)',
                'python': 'scipy.special.zeta({arg}, 1)',
                'domain': 'complex, s != 1',
                'range': 'complex'
            }
        }
        
        # Index types with their mathematical patterns
        self.index_patterns = {
            IndexType.LINEAR: {
                'latex': '{var}',
                'python': '{var}',
                'growth_rate': 'linear'
            },
            IndexType.QUADRATIC: {
                'latex': '{var}^2',
                'python': '{var}**2',
                'growth_rate': 'quadratic'
            },
            IndexType.CUBIC: {
                'latex': '{var}^3',
                'python': '{var}**3',
                'growth_rate': 'cubic'
            },
            IndexType.EXPONENTIAL: {
                'latex': '2^{{{var}}}',
                'python': '2**{var}',
                'growth_rate': 'exponential'
            },
            IndexType.FACTORIAL: {
                'latex': '{var}!',
                'python': 'math.factorial({var})',
                'growth_rate': 'factorial'
            },
            IndexType.PRIME: {
                'latex': 'p_{var}',  # p_n denotes nth prime
                'python': 'self.nth_prime({var})',
                'growth_rate': 'approximately n*log(n)'
            },
            IndexType.FIBONACCI: {
                'latex': 'F_{var}',  # F_n denotes nth Fibonacci number
                'python': 'self.fibonacci({var})',
                'growth_rate': 'approximately φ^n'
            }
        }
        
        # Common argument patterns from existing functions
        self.argument_patterns = [
            r'\\frac{{\\pi z}}{{{index}}}',  # π*z/n (most common in divisor waves)
            r'\\pi z {index}',               # π*z*n (Riesz products)
            r'\\frac{{z}}{{{index}}}',       # z/n (simple rational)
            r'\\frac{{\\pi z}}{{{index}^2}}', # π*z/n² (quadratic decay)
            r'\\frac{{\\pi z}}{{{index}^3}}', # π*z/n³ (cubic decay)
            r'\\frac{{z^2}}{{{index}}}',     # z²/n (quadratic numerator)
            r'\\frac{{z}}{{{index}^2}}',     # z/n² (quadratic denominator)
            r'\\frac{{\\log(z)}}{{{index}}}', # log(z)/n (logarithmic)
            r'z^{{1/{index}}}',              # z^(1/n) (fractional powers)
            r'\\frac{{1}}{{{index}^z}}',     # 1/n^z (generalized zeta-like)
        ]
        
        # Coefficient patterns from existing system
        self.coefficient_patterns = [
            '1',          # No coefficient
            'z',          # Variable coefficient
            '\\pi',       # Pi coefficient
            'z^2',        # Quadratic coefficient
            '\\frac{1}{z}', # Inverse coefficient
            '\\frac{z}{\\pi}', # Normalized coefficient
            '\\log(z)',   # Logarithmic coefficient
            'e^z',        # Exponential coefficient
            '\\frac{1}{\\log(z)}', # Inverse logarithmic
            '\\sqrt{z}',  # Square root coefficient
        ]
    
    def initialize_series_rules(self):
        """Initialize rules for constructing valid infinite series"""
        
        # Convergence rules based on mathematical analysis
        self.convergence_rules = {
            SeriesType.INFINITE_SUM: {
                'required_decay': 'p-series with p > 1 or exponential decay',
                'safe_patterns': [
                    (OperatorType.SIN, IndexType.QUADRATIC),
                    (OperatorType.COS, IndexType.QUADRATIC),
                    (OperatorType.EXP, IndexType.LINEAR),
                    (OperatorType.LOG, IndexType.CUBIC),
                ],
                'dangerous_patterns': [
                    (OperatorType.TAN, IndexType.LINEAR),  # Can have poles
                    (OperatorType.LOG, IndexType.LINEAR),  # Diverges
                ]
            },
            SeriesType.INFINITE_PRODUCT: {
                'required_decay': 'Product must converge to non-zero value',
                'safe_patterns': [
                    (OperatorType.SIN, IndexType.LINEAR),   # Like our main product
                    (OperatorType.COS, IndexType.EXPONENTIAL), # Viète-like
                    (OperatorType.SINH, IndexType.QUADRATIC),
                ],
                'dangerous_patterns': [
                    (OperatorType.EXP, IndexType.LINEAR),  # Diverges rapidly
                ]
            }
        }
        
        # Complexity scoring rules
        self.complexity_rules = {
            'base_complexity': 1.0,
            'operator_complexity': {
                OperatorType.SIN: 1.0, OperatorType.COS: 1.0, OperatorType.TAN: 1.2,
                OperatorType.EXP: 1.3, OperatorType.LOG: 1.4, OperatorType.SINH: 1.1,
                OperatorType.COSH: 1.1, OperatorType.TANH: 1.2, OperatorType.GAMMA: 2.0,
                OperatorType.ZETA: 2.5
            },
            'index_complexity': {
                IndexType.LINEAR: 1.0, IndexType.QUADRATIC: 1.2, IndexType.CUBIC: 1.4,
                IndexType.EXPONENTIAL: 1.8, IndexType.FACTORIAL: 2.5, IndexType.PRIME: 2.0,
                IndexType.FIBONACCI: 1.6
            },
            'series_complexity': {
                SeriesType.INFINITE_SUM: 1.0, SeriesType.INFINITE_PRODUCT: 1.3,
                SeriesType.NESTED_SERIES: 2.0, SeriesType.HYBRID_SERIES: 2.5
            }
        }
    
    def generate_random_function(self, target_complexity: float = None) -> GeneratedFunction:
        """
        Generate a single random mathematical function using systematic combination
        
        Args:
            target_complexity: Desired complexity level (1.0 = simple, 3.0+ = very complex)
            
        Returns:
            GeneratedFunction object with complete function definition
        """
        
        if target_complexity is None:
            target_complexity = random.uniform(1.0, 2.5)  # Default range
        
        # Step 1: Choose series type based on complexity
        series_type = self._choose_series_type(target_complexity)
        
        # Step 2: Generate series structure
        series_structure = self._generate_series_structure(series_type, target_complexity)
        
        # Step 3: Generate components
        components = self._generate_components(series_structure, target_complexity)
        series_structure.components = components
        
        # Step 4: Build LaTeX formula
        latex_formula = self._build_latex_formula(series_structure)
        
        # Step 5: Generate Python implementation
        python_code = self._generate_python_code(series_structure)
        
        # Step 6: Calculate actual complexity
        actual_complexity = self._calculate_complexity(series_structure)
        
        # Step 7: Generate metadata
        name = self._generate_function_name(series_structure)
        description = self._generate_description(series_structure)
        category = self._determine_category(series_structure)
        properties = self._analyze_mathematical_properties(series_structure)
        
        # Create function object
        generated_function = GeneratedFunction(
            name=name,
            latex_formula=latex_formula,
            python_code=python_code,
            series_structure=series_structure,
            description=description,
            category=category,
            complexity_score=actual_complexity,
            mathematical_properties=properties
        )
        
        # Update statistics
        self._update_statistics(generated_function)
        
        return generated_function
    
    def _choose_series_type(self, target_complexity: float) -> SeriesType:
        """Choose series type based on target complexity"""
        
        if target_complexity < 1.5:
            # Simple series - prefer sums and products
            return random.choice([SeriesType.INFINITE_SUM, SeriesType.INFINITE_PRODUCT])
        elif target_complexity < 2.5:
            # Medium complexity - allow all types
            return random.choice(list(SeriesType))
        else:
            # High complexity - prefer nested and hybrid
            return random.choice([SeriesType.NESTED_SERIES, SeriesType.HYBRID_SERIES])
    
    def _generate_series_structure(self, series_type: SeriesType, target_complexity: float) -> SeriesStructure:
        """Generate the basic structure of the series"""
        
        # Choose index variable
        index_var = random.choice(['n', 'k', 'j', 'm'])
        
        # Choose starting value (usually 1 or 2, sometimes 0)
        start_val = random.choice(['1', '2', '0']) if target_complexity < 2.0 else random.choice(['0', '1', '2', '3'])
        
        # Choose ending condition
        if series_type in [SeriesType.INFINITE_SUM, SeriesType.INFINITE_PRODUCT]:
            end_val = '\\infty'
        else:
            end_val = random.choice(['z', '\\lfloor z \\rfloor', '\\infty'])
        
        # Choose index type based on complexity
        if target_complexity < 1.5:
            index_type = random.choice([IndexType.LINEAR, IndexType.QUADRATIC])
        elif target_complexity < 2.5:
            index_type = random.choice([IndexType.LINEAR, IndexType.QUADRATIC, IndexType.CUBIC, IndexType.EXPONENTIAL])
        else:
            index_type = random.choice(list(IndexType))
        
        return SeriesStructure(
            series_type=series_type,
            index_variable=index_var,
            start_value=start_val,
            end_value=end_val,
            index_type=index_type,
            components=[]  # Will be filled later
        )
    
    def _generate_components(self, series_structure: SeriesStructure, target_complexity: float) -> List[FunctionComponent]:
        """Generate mathematical components for the series"""
        
        components = []
        
        # Determine number of components based on complexity
        if target_complexity < 1.5:
            num_components = 1
        elif target_complexity < 2.5:
            num_components = random.choice([1, 2])
        else:
            num_components = random.choice([1, 2, 3])
        
        for i in range(num_components):
            # Choose operator
            if series_structure.series_type == SeriesType.INFINITE_PRODUCT:
                # Products work well with sin, cos, and their variants
                if target_complexity < 2.0:
                    operator = random.choice([OperatorType.SIN, OperatorType.COS, OperatorType.SINH, OperatorType.COSH])
                else:
                    operator = random.choice([OperatorType.SIN, OperatorType.COS, OperatorType.TAN, 
                                            OperatorType.SINH, OperatorType.COSH, OperatorType.TANH])
            else:  # INFINITE_SUM or others
                # Sums are more flexible
                operator = random.choice(list(OperatorType))
            
            # Generate argument
            argument = self._generate_argument(series_structure, target_complexity)
            
            # Generate coefficient
            coefficient = self._generate_coefficient(target_complexity)
            
            # Generate power (usually 1, sometimes other values for complexity)
            if target_complexity < 2.0:
                power = '1'
            else:
                power = random.choice(['1', '1', '1', '2', '-1', '1/2'])  # Bias toward 1
            
            component = FunctionComponent(
                operator=operator,
                argument=argument,
                coefficient=coefficient,
                power=power
            )
            
            components.append(component)
        
        return components
    
    def _generate_argument(self, series_structure: SeriesStructure, target_complexity: float) -> str:
        """Generate argument for function components"""
        
        # Choose argument pattern
        if target_complexity < 1.5:
            # Simple patterns like π*z/n
            patterns = [
                r'\\frac{{\\pi z}}{{{index}}}',
                r'\\frac{{z}}{{{index}}}',
                r'\\pi z {index}'
            ]
        else:
            # Use full pattern library
            patterns = self.argument_patterns
        
        pattern = random.choice(patterns)
        
        # Replace {index} with actual index expression
        index_expr = self.index_patterns[series_structure.index_type]['latex'].format(
            var=series_structure.index_variable
        )
        
        argument = pattern.format(index=index_expr)
        
        return argument
    
    def _generate_coefficient(self, target_complexity: float) -> str:
        """Generate coefficient for function components"""
        
        if target_complexity < 1.5:
            # Simple coefficients
            return random.choice(['1', 'z', '\\pi', '\\frac{1}{\\pi}'])
        elif target_complexity < 2.5:
            # Medium complexity coefficients
            return random.choice(self.coefficient_patterns[:7])
        else:
            # All coefficient patterns
            return random.choice(self.coefficient_patterns)
    
    def _build_latex_formula(self, series_structure: SeriesStructure) -> str:
        """Build complete LaTeX formula from series structure"""
        
        # Start with series symbol
        if series_structure.series_type == SeriesType.INFINITE_SUM:
            series_symbol = '\\sum'
        elif series_structure.series_type == SeriesType.INFINITE_PRODUCT:
            series_symbol = '\\prod'
        elif series_structure.series_type == SeriesType.NESTED_SERIES:
            series_symbol = '\\sum'  # Nested will be handled in components
        else:  # HYBRID_SERIES
            series_symbol = random.choice(['\\sum', '\\prod'])
        
        # Build index expression
        index_expr = f"_{{{series_structure.index_variable}={series_structure.start_value}}}^{{{series_structure.end_value}}}"
        
        # Build component expressions
        component_exprs = []
        for component in series_structure.components:
            # Get operator LaTeX
            op_latex = self.operators[component.operator]['latex'].format(arg=component.argument)
            
            # Add coefficient and power
            if component.coefficient != '1':
                if component.power != '1':
                    expr = f"{component.coefficient} \\left({op_latex}\\right)^{{{component.power}}}"
                else:
                    expr = f"{component.coefficient} {op_latex}"
            else:
                if component.power != '1':
                    expr = f"\\left({op_latex}\\right)^{{{component.power}}}"
                else:
                    expr = op_latex
            
            component_exprs.append(expr)
        
        # Combine components
        if len(component_exprs) == 1:
            components_str = component_exprs[0]
        elif series_structure.series_type == SeriesType.INFINITE_PRODUCT:
            # For products, multiply components
            components_str = ' \\cdot '.join(component_exprs)
        else:
            # For sums, add components or create more complex combinations
            if len(component_exprs) == 2:
                components_str = f"{component_exprs[0]} + {component_exprs[1]}"
            else:
                components_str = ' + '.join(component_exprs)
        
        # Combine everything
        latex_formula = f"{series_symbol}{index_expr} \\left( {components_str} \\right)"
        
        return latex_formula
    
    def _generate_python_code(self, series_structure: SeriesStructure) -> str:
        """Generate Python implementation code"""
        
        # Build Python code template
        template = '''
def custom_function(z, normalize_type='N'):
    import numpy as np
    import math
    import cmath
    import scipy.special
    
    z_real = np.real(z)
    z_imag = np.imag(z)
    
    try:
        # Determine computation range
        if isinstance(z, complex):
            max_n = min(max(int(abs(z_real)), 10), 100)  # Reasonable bounds
        else:
            max_n = min(max(int(abs(z)), 10), 100)
        
        # Generate series terms
        terms = []
        for {index_var} in range({start_val}, max_n + 1):
            {component_code}
            terms.append(term_value)
        
        # Combine terms
        if not terms:
            result = 1.0 if "{series_op}" == "prod" else 0.0
        else:
            result = {combination_code}
        
        # Apply normalization if requested
        if normalize_type == 'Y':
            if abs(result) < 100:
                result = result / scipy.special.gamma(abs(result) + 1e-10)
        
        return abs(result) if np.isfinite(result) else 0.0
        
    except Exception as e:
        return 0.0
'''
        
        # Generate component code
        component_codes = []
        for component in series_structure.components:
            # Convert LaTeX argument to Python
            arg_python = self._latex_arg_to_python(component.argument, series_structure.index_variable)
            
            # Get operator Python code
            op_python = self.operators[component.operator]['python'].format(arg=arg_python)
            
            # Add coefficient and power
            coeff_python = self._latex_coeff_to_python(component.coefficient)
            
            if component.power != '1':
                power_python = self._latex_expr_to_python(component.power)
                if coeff_python != '1':
                    component_code = f"({coeff_python}) * (({op_python}) ** ({power_python}))"
                else:
                    component_code = f"(({op_python}) ** ({power_python}))"
            else:
                if coeff_python != '1':
                    component_code = f"({coeff_python}) * ({op_python})"
                else:
                    component_code = op_python
            
            component_codes.append(component_code)
        
        # Combine component codes
        if len(component_codes) == 1:
            full_component_code = f"term_value = {component_codes[0]}"
        elif series_structure.series_type == SeriesType.INFINITE_PRODUCT:
            full_component_code = f"term_value = {' * '.join(component_codes)}"
        else:
            full_component_code = f"term_value = {' + '.join(component_codes)}"
        
        # Determine series operation
        if series_structure.series_type == SeriesType.INFINITE_PRODUCT:
            series_op = "prod"
            combination_code = "np.prod(terms)"
        else:
            series_op = "sum"
            combination_code = "np.sum(terms)"
        
        # Fill template
        python_code = template.format(
            index_var=series_structure.index_variable,
            start_val=series_structure.start_value if series_structure.start_value.isdigit() else '1',
            component_code=full_component_code,
            series_op=series_op,
            combination_code=combination_code
        )
        
        return python_code
    
    def _latex_arg_to_python(self, latex_arg: str, index_var: str) -> str:
        """Convert LaTeX argument to Python code"""
        
        # Simple replacements
        replacements = {
            '\\pi': 'math.pi',
            ' z ': f' (z_real + 1j * z_imag) ',
            f' {index_var} ': f' {index_var} ',
            '\\frac{': '(',
            '}{': ') / (',
            '}': ')',
            '{': '',
            '^2': '**2',
            '^3': '**3',
            '^{2}': '**2',
            '^{3}': '**3',
            '\\log': 'np.log',
            '\\sqrt': 'np.sqrt'
        }
        
        result = latex_arg
        for latex_pattern, python_replacement in replacements.items():
            result = result.replace(latex_pattern, python_replacement)
        
        # Handle special cases
        result = result.replace('z', '(z_real + 1j * z_imag)')
        
        return result
    
    def _latex_coeff_to_python(self, latex_coeff: str) -> str:
        """Convert LaTeX coefficient to Python code"""
        
        if latex_coeff == '1':
            return '1'
        
        replacements = {
            '\\pi': 'math.pi',
            'z': '(z_real + 1j * z_imag)',
            '\\frac{': '(',
            '}{': ') / (',
            '}': ')',
            '{': '',
            '^2': '**2',
            '\\log': 'np.log',
            '\\sqrt': 'np.sqrt',
            'e^': 'np.exp('
        }
        
        result = latex_coeff
        for latex_pattern, python_replacement in replacements.items():
            result = result.replace(latex_pattern, python_replacement)
        
        return result
    
    def _latex_expr_to_python(self, latex_expr: str) -> str:
        """Convert general LaTeX expression to Python"""
        return self._latex_coeff_to_python(latex_expr)  # Same logic
    
    def _calculate_complexity(self, series_structure: SeriesStructure) -> float:
        """Calculate complexity score for the generated function"""
        
        complexity = self.complexity_rules['base_complexity']
        
        # Series type complexity
        complexity *= self.complexity_rules['series_complexity'][series_structure.series_type]
        
        # Index type complexity
        complexity *= self.complexity_rules['index_complexity'][series_structure.index_type]
        
        # Component complexity
        for component in series_structure.components:
            complexity *= self.complexity_rules['operator_complexity'][component.operator]
            
            # Power complexity
            if component.power not in ['1', '']:
                complexity *= 1.2
            
            # Coefficient complexity
            if component.coefficient not in ['1', '']:
                complexity *= 1.1
        
        return round(complexity, 2)
    
    def _generate_function_name(self, series_structure: SeriesStructure) -> str:
        """Generate descriptive name for the function"""
        
        series_name = {
            SeriesType.INFINITE_SUM: "sum",
            SeriesType.INFINITE_PRODUCT: "product",
            SeriesType.NESTED_SERIES: "nested",
            SeriesType.HYBRID_SERIES: "hybrid"
        }[series_structure.series_type]
        
        if series_structure.components:
            op_name = series_structure.components[0].operator.value
            index_name = series_structure.index_type.value
            
            name = f"generated_{series_name}_{op_name}_{index_name}"
        else:
            name = f"generated_{series_name}"
        
        # Add random suffix to ensure uniqueness
        suffix = random.randint(1000, 9999)
        return f"{name}_{suffix}"
    
    def _generate_description(self, series_structure: SeriesStructure) -> str:
        """Generate human-readable description"""
        
        series_desc = {
            SeriesType.INFINITE_SUM: "infinite sum",
            SeriesType.INFINITE_PRODUCT: "infinite product", 
            SeriesType.NESTED_SERIES: "nested series",
            SeriesType.HYBRID_SERIES: "hybrid series"
        }[series_structure.series_type]
        
        if series_structure.components:
            operators = [comp.operator.value for comp in series_structure.components]
            op_desc = ", ".join(operators)
            
            index_desc = series_structure.index_type.value.replace('_', ' ')
            
            description = f"Generated {series_desc} using {op_desc} with {index_desc} indexing"
        else:
            description = f"Generated {series_desc}"
        
        return description
    
    def _determine_category(self, series_structure: SeriesStructure) -> str:
        """Determine function category based on structure"""
        
        if series_structure.series_type == SeriesType.INFINITE_PRODUCT:
            return "infinite_products"
        elif series_structure.series_type == SeriesType.INFINITE_SUM:
            return "infinite_series"
        else:
            return "advanced_series"
    
    def _analyze_mathematical_properties(self, series_structure: SeriesStructure) -> Dict[str, Any]:
        """Analyze mathematical properties of the generated function"""
        
        properties = {
            'series_type': series_structure.series_type.value,
            'index_type': series_structure.index_type.value,
            'operators_used': [comp.operator.value for comp in series_structure.components],
            'estimated_convergence': self._estimate_convergence(series_structure),
            'domain': self._estimate_domain(series_structure),
            'symmetries': self._check_symmetries(series_structure),
            'computational_complexity': self._estimate_computational_complexity(series_structure)
        }
        
        return properties
    
    def _estimate_convergence(self, series_structure: SeriesStructure) -> str:
        """Estimate convergence properties"""
        
        if series_structure.index_type in [IndexType.QUADRATIC, IndexType.CUBIC]:
            return "likely_convergent"
        elif series_structure.index_type == IndexType.EXPONENTIAL:
            return "fast_convergent"
        elif series_structure.index_type == IndexType.FACTORIAL:
            return "very_fast_convergent"
        else:
            return "convergence_depends_on_z"
    
    def _estimate_domain(self, series_structure: SeriesStructure) -> str:
        """Estimate function domain"""
        
        has_log = any(comp.operator == OperatorType.LOG for comp in series_structure.components)
        has_tan = any(comp.operator == OperatorType.TAN for comp in series_structure.components)
        has_gamma = any(comp.operator == OperatorType.GAMMA for comp in series_structure.components)
        
        if has_log:
            return "complex_plane_excluding_branch_cuts"
        elif has_tan:
            return "complex_plane_excluding_poles"
        elif has_gamma:
            return "complex_plane_excluding_negative_integers"
        else:
            return "entire_complex_plane"
    
    def _check_symmetries(self, series_structure: SeriesStructure) -> List[str]:
        """Check for potential symmetries"""
        
        symmetries = []
        
        # Check for even/odd symmetries based on operators
        sin_ops = [comp for comp in series_structure.components if comp.operator == OperatorType.SIN]
        cos_ops = [comp for comp in series_structure.components if comp.operator == OperatorType.COS]
        
        if sin_ops and not cos_ops:
            symmetries.append("potentially_odd")
        elif cos_ops and not sin_ops:
            symmetries.append("potentially_even")
        
        # Check for real symmetry
        if all('z^2' not in comp.argument and 'z²' not in comp.argument for comp in series_structure.components):
            symmetries.append("potentially_real_symmetric")
        
        return symmetries
    
    def _estimate_computational_complexity(self, series_structure: SeriesStructure) -> str:
        """Estimate computational complexity"""
        
        if series_structure.index_type in [IndexType.LINEAR, IndexType.QUADRATIC]:
            return "O(n)"
        elif series_structure.index_type in [IndexType.CUBIC, IndexType.EXPONENTIAL]:
            return "O(n*log(n))"
        else:
            return "O(n^2)"
    
    def _update_statistics(self, generated_function: GeneratedFunction):
        """Update generation statistics"""
        
        self.generation_stats['total_generated'] += 1
        
        series_type = generated_function.series_structure.series_type.value
        self.generation_stats['series_types_generated'][series_type] = \
            self.generation_stats['series_types_generated'].get(series_type, 0) + 1
        
        for component in generated_function.series_structure.components:
            op = component.operator.value
            self.generation_stats['operator_usage'][op] = \
                self.generation_stats['operator_usage'].get(op, 0) + 1
        
        self.generation_stats['complexity_distribution'].append(generated_function.complexity_score)
    
    # Helper functions for special index types
    
    def nth_prime(self, n: int) -> int:
        """Get the nth prime number (simple implementation)"""
        if n == 1:
            return 2
        
        primes = [2]
        candidate = 3
        
        while len(primes) < n:
            is_prime = True
            for p in primes:
                if p * p > candidate:
                    break
                if candidate % p == 0:
                    is_prime = False
                    break
            
            if is_prime:
                primes.append(candidate)
            
            candidate += 2
        
        return primes[n - 1]
    
    def fibonacci(self, n: int) -> int:
        """Get the nth Fibonacci number"""
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        
        return b
    
    # Batch generation methods
    
    def generate_function_batch(self, batch_size: int = 10, 
                              complexity_range: Tuple[float, float] = (1.0, 2.5)) -> List[GeneratedFunction]:
        """Generate a batch of random functions"""
        
        functions = []
        
        for _ in range(batch_size):
            target_complexity = random.uniform(complexity_range[0], complexity_range[1])
            function = self.generate_random_function(target_complexity)
            functions.append(function)
        
        return functions
    
    def generate_diverse_batch(self, total_functions: int = 50) -> List[GeneratedFunction]:
        """Generate a diverse batch covering all series types and complexity levels"""
        
        functions = []
        
        # Ensure coverage of all series types
        series_types = list(SeriesType)
        functions_per_type = total_functions // len(series_types)
        
        for series_type in series_types:
            for i in range(functions_per_type):
                # Vary complexity across the range
                complexity = 1.0 + (i / functions_per_type) * 2.0
                
                # Generate function with preferred series type
                function = self.generate_random_function(complexity)
                
                # If it doesn't match desired type, regenerate a few times
                attempts = 0
                while function.series_structure.series_type != series_type and attempts < 3:
                    function = self.generate_random_function(complexity)
                    attempts += 1
                
                functions.append(function)
        
        # Fill remaining slots with random functions
        remaining = total_functions - len(functions)
        for _ in range(remaining):
            function = self.generate_random_function()
            functions.append(function)
        
        return functions
    
    # AI evaluation interface
    
    def set_ai_evaluator(self, evaluator_function: Callable[[GeneratedFunction], bool]):
        """Set AI evaluation function that returns True if function is interesting"""
        self.ai_evaluator = evaluator_function
    
    def generate_with_ai_filtering(self, target_count: int = 10, 
                                 max_attempts: int = 100) -> List[GeneratedFunction]:
        """Generate functions and use AI to filter for interesting ones"""
        
        if self.ai_evaluator is None:
            raise ValueError("AI evaluator not set. Call set_ai_evaluator() first.")
        
        interesting_functions = []
        attempts = 0
        
        while len(interesting_functions) < target_count and attempts < max_attempts:
            function = self.generate_random_function()
            attempts += 1
            
            # Ask AI if this function is interesting
            if self.ai_evaluator(function):
                interesting_functions.append(function)
                self.generation_stats['accepted_by_ai'] += 1
                print(f"✅ AI accepted: {function.name} (complexity: {function.complexity_score})")
            else:
                self.generation_stats['rejected_by_ai'] += 1
                if attempts % 10 == 0:  # Progress update
                    print(f"🔄 Generated {attempts} functions, AI accepted {len(interesting_functions)}")
        
        print(f"🎯 AI filtering complete: {len(interesting_functions)} interesting functions found in {attempts} attempts")
        return interesting_functions
    
    # Export and integration methods
    
    def export_function_to_json(self, function: GeneratedFunction, output_path: str = None) -> str:
        """Export generated function to JSON format compatible with existing system"""
        
        function_data = {
            "id": f"generated_{hash(function.name) % 10000}",
            "name": function.name,
            "display_name": function.name.replace('_', ' ').title(),
            "description": function.description,
            "category": function.category,
            "latex_formula": function.latex_formula,
            "python_implementation": function.python_code,
            "dependencies": [],
            "parameters": {},
            "normalization_modes": ["N", "Y", "X", "Z", "XYZ"],
            "tags": [
                function.series_structure.series_type.value,
                function.series_structure.index_type.value
            ] + [comp.operator.value for comp in function.series_structure.components],
            "created_at": "2025-11-07T00:00:00.000000",
            "updated_at": "2025-11-07T00:00:00.000000", 
            "version": "1.0.0",
            "author": "MathematicalFunctionGenerator",
            "source": "systematic_generation",
            "hash": f"{hash(function.latex_formula) % 100000000:08x}",
            "mathematical_properties": function.mathematical_properties,
            "complexity_score": function.complexity_score
        }
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(function_data, f, indent=2, ensure_ascii=False)
            return output_path
        
        return json.dumps(function_data, indent=2, ensure_ascii=False)
    
    def export_batch_to_json(self, functions: List[GeneratedFunction], output_path: str = "generated_functions.json"):
        """Export batch of functions to JSON database format"""
        
        functions_dict = {}
        
        for function in functions:
            function_json = json.loads(self.export_function_to_json(function))
            functions_dict[function.name] = function_json
        
        database = {
            "functions": functions_dict,
            "metadata": {
                "version": "1.0",
                "count": len(functions),
                "updated": "2025-11-07T00:00:00.000000",
                "generated_by": "MathematicalFunctionGenerator",
                "generation_stats": self.generation_stats
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(database, f, indent=2, ensure_ascii=False)
        
        print(f"📁 Exported {len(functions)} functions to {output_path}")
        return output_path
    
    def get_generation_statistics(self) -> Dict[str, Any]:
        """Get comprehensive generation statistics"""
        
        stats = dict(self.generation_stats)
        
        if stats['complexity_distribution']:
            stats['average_complexity'] = sum(stats['complexity_distribution']) / len(stats['complexity_distribution'])
            stats['complexity_range'] = [min(stats['complexity_distribution']), max(stats['complexity_distribution'])]
        
        if stats['total_generated'] > 0:
            stats['ai_acceptance_rate'] = stats['accepted_by_ai'] / stats['total_generated']
        
        return stats


# AI Evaluation Interface (example implementation)
class AIFunctionEvaluator:
    """
    Example AI evaluator for mathematical functions.
    In practice, this would interface with your AI system.
    """
    
    def __init__(self):
        self.evaluation_criteria = {
            'novelty_weight': 0.4,
            'complexity_weight': 0.3,
            'mathematical_interest_weight': 0.3,
            'preferred_complexity_range': (1.2, 2.5),
            'preferred_operators': {OperatorType.SIN, OperatorType.COS, OperatorType.EXP},
            'preferred_series_types': {SeriesType.INFINITE_PRODUCT, SeriesType.INFINITE_SUM}
        }
    
    def evaluate_function(self, function: GeneratedFunction) -> bool:
        """
        Evaluate if a function is interesting.
        This is a simple rule-based example - replace with actual AI.
        
        Returns True if function is deemed interesting
        """
        
        score = 0.0
        
        # Complexity scoring
        complexity = function.complexity_score
        min_comp, max_comp = self.evaluation_criteria['preferred_complexity_range']
        
        if min_comp <= complexity <= max_comp:
            complexity_score = 1.0
        elif complexity < min_comp:
            complexity_score = complexity / min_comp
        else:
            complexity_score = max_comp / complexity
        
        score += complexity_score * self.evaluation_criteria['complexity_weight']
        
        # Operator preference scoring
        function_operators = set(comp.operator for comp in function.series_structure.components)
        operator_overlap = len(function_operators & self.evaluation_criteria['preferred_operators'])
        operator_score = operator_overlap / len(function_operators) if function_operators else 0
        
        score += operator_score * self.evaluation_criteria['mathematical_interest_weight']
        
        # Series type preference
        if function.series_structure.series_type in self.evaluation_criteria['preferred_series_types']:
            series_score = 1.0
        else:
            series_score = 0.5
        
        score += series_score * self.evaluation_criteria['novelty_weight']
        
        # Decision threshold
        return score > 0.6
    
    def __call__(self, function: GeneratedFunction) -> bool:
        """Make the evaluator callable"""
        return self.evaluate_function(function)


# Example usage and testing
def demo_mathematical_function_generator():
    """Demonstrate the mathematical function generator"""
    
    print("🧮 MATHEMATICAL FUNCTION GENERATOR DEMO")
    print("=" * 60)
    
    # Initialize generator
    generator = MathematicalFunctionGenerator()
    
    # Set up AI evaluator
    ai_evaluator = AIFunctionEvaluator()
    generator.set_ai_evaluator(ai_evaluator)
    
    print("\n📊 System initialized with:")
    print(f"   Loaded {len(generator.existing_functions)} existing functions")
    print(f"   Available operators: {len(generator.operators)}")
    print(f"   Index patterns: {len(generator.index_patterns)}")
    print(f"   Argument patterns: {len(generator.argument_patterns)}")
    
    # Generate some random functions
    print("\n🎲 Generating random functions...")
    random_functions = generator.generate_function_batch(5)
    
    for func in random_functions:
        print(f"\n   Function: {func.name}")
        print(f"   LaTeX: {func.latex_formula}")
        print(f"   Complexity: {func.complexity_score}")
        print(f"   Type: {func.series_structure.series_type.value}")
    
    # Generate AI-filtered functions
    print("\n🤖 Generating AI-filtered functions...")
    interesting_functions = generator.generate_with_ai_filtering(target_count=3, max_attempts=20)
    
    # Export to JSON
    if interesting_functions:
        output_file = generator.export_batch_to_json(interesting_functions, "demo_generated_functions.json")
        print(f"\n💾 Exported interesting functions to: {output_file}")
    
    # Show statistics
    stats = generator.get_generation_statistics()
    print(f"\n📈 Generation Statistics:")
    print(f"   Total generated: {stats['total_generated']}")
    print(f"   AI accepted: {stats['accepted_by_ai']}")
    print(f"   AI acceptance rate: {stats.get('ai_acceptance_rate', 0):.2%}")
    print(f"   Average complexity: {stats.get('average_complexity', 0):.2f}")
    
    return generator, interesting_functions


if __name__ == "__main__":
    demo_mathematical_function_generator()