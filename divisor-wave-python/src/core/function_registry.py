"""
Unified Function Registry System
Centralized management of all mathematical functions for the divisor wave analysis system

This registry eliminates redundancy by providing a single source of truth for:
- Function definitions and metadata
- LaTeX formula mappings
- Python code implementations
- Function categories and relationships
- Auto-synchronization with legacy systems

Architecture benefits:
- Single point of maintenance for adding new functions
- Automatic consistency across all components
- Extensible plugin system for custom functions
- Bidirectional LaTeX ↔ NumPy conversion
- Version control and migration support

11/6/2025 - Unified architecture design
"""

import json
import os
import inspect
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable, Union
from dataclasses import dataclass, asdict, field
from datetime import datetime
import hashlib

@dataclass
class FunctionDefinition:
    """Complete definition of a mathematical function"""
    id: str
    name: str
    display_name: str = ""
    description: str = ""
    category: str = "Miscellaneous"
    latex_formula: str = ""
    python_implementation: str = ""
    dependencies: List[str] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    normalization_modes: List[str] = field(default_factory=lambda: ["N", "Y", "X", "Z", "XYZ"])
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    version: str = "1.0.0"
    author: str = "System"
    source: str = "builtin"  # builtin, custom, imported
    hash: str = ""

    def __post_init__(self):
        """Generate hash for change detection and set defaults"""
        if not self.display_name:
            self.display_name = self.name.replace('_', ' ').title()
        if not self.python_implementation:
            self.python_implementation = self.name
        
        content = f"{self.name}{self.latex_formula}{self.python_implementation}"
        self.hash = hashlib.md5(content.encode()).hexdigest()[:8]


class FunctionRegistry:
    """
    Centralized registry for all mathematical functions
    Replaces scattered function mappings with unified system
    """
    
    def __init__(self, registry_path: str = None):
        if registry_path is None:
            registry_path = Path(__file__).parent / "../data/registry/function_registry.json"
        
        self.registry_path = Path(registry_path)
        self.functions: Dict[str, FunctionDefinition] = {}
        self.legacy_mappings = {
            'lambda_catalog': {},
            'api_mappings': {},
            'latex_database': {}
        }
        
        # Auto-load existing data
        self.load_registry()
        self._initialize_builtin_functions()
        self._import_legacy_data()
    
    def _initialize_builtin_functions(self):
        """Initialize core builtin functions from Leo J. Borcherding's research"""
        builtin_functions = [
            {
                "id": "1",
                "name": "product_of_sin",
                "display_name": "Product of Sin",
                "description": "Main divisor wave function a(z) - Product of Sin via Sin product representation",
                "category": "Core Products",
                "latex_formula": "f(z) = \\left|\\prod_{k=2}^{z} \\beta \\cdot \\frac{z}{k} \\cdot \\sin\\left(\\frac{\\pi z}{k}\\right)\\right|^{-m}",
                "python_implementation": "product_of_sin",
                "tags": ["core", "infinite-product", "prime-analysis"],
                "author": "Leo J. Borcherding"
            },
            {
                "id": "2", 
                "name": "product_of_product_representation_for_sin",
                "display_name": "Product of Product Representation for Sin",
                "description": "Double infinite product representation using sin product formula",
                "category": "Core Products",
                "latex_formula": "g(z) = \\left|\\prod_{n=2}^{z} \\beta \\cdot \\frac{z}{n} \\cdot \\left(\\pi z \\cdot \\prod_{k=2}^{z} \\left(1 - \\frac{z^2}{n^2 k^2}\\right)\\right)\\right|^{-m}",
                "python_implementation": "product_of_product_representation_for_sin",
                "tags": ["core", "double-product", "prime-analysis"],
                "author": "Leo J. Borcherding"
            },
            {
                "id": "3",
                "name": "complex_playground_magnification_currated_functions_DEMO",
                "display_name": "Complex Playground Magnification Demo",
                "description": "Curated complex function for demonstration and exploration",
                "category": "Demonstration",
                "latex_formula": "h(z) = \\text{Complex magnification function}",
                "python_implementation": "complex_playground_magnification_currated_functions_DEMO",
                "tags": ["demo", "complex-analysis"],
                "author": "Leo J. Borcherding"
            },
            # Riesz Products
            {
                "id": "4",
                "name": "Riesz_Product_for_Cos",
                "display_name": "Riesz Product for Cosine",
                "description": "Riesz product representation using cosine functions",
                "category": "Riesz Products",
                "latex_formula": "R_\\cos(z) = \\prod_{n=2}^{z} \\cos\\left(\\frac{\\pi z}{2^n}\\right)",
                "python_implementation": "Riesz_Product_for_Cos",
                "tags": ["riesz", "cosine", "infinite-product"]
            },
            {
                "id": "5",
                "name": "Riesz_Product_for_Sin", 
                "display_name": "Riesz Product for Sine",
                "description": "Riesz product representation using sine functions",
                "category": "Riesz Products",
                "latex_formula": "R_\\sin(z) = \\prod_{n=2}^{z} \\sin\\left(\\frac{\\pi z}{2^n}\\right)",
                "python_implementation": "Riesz_Product_for_Sin",
                "tags": ["riesz", "sine", "infinite-product"]
            },
            {
                "id": "6",
                "name": "Riesz_Product_for_Tan",
                "display_name": "Riesz Product for Tangent", 
                "description": "Riesz product representation using tangent functions",
                "category": "Riesz Products",
                "latex_formula": "R_\\tan(z) = \\prod_{n=2}^{z} \\tan\\left(\\frac{\\pi z}{2^n}\\right)",
                "python_implementation": "Riesz_Product_for_Tan",
                "tags": ["riesz", "tangent", "infinite-product"]
            },
            # Viète Products
            {
                "id": "7",
                "name": "Viete_Product_for_Cos",
                "display_name": "Viète Product for Cosine",
                "description": "Viète infinite product formula for cosine",
                "category": "Viète Products", 
                "latex_formula": "V_\\cos(z) = \\prod_{n=1}^{\\infty} \\cos\\left(\\frac{z}{2^n}\\right)",
                "python_implementation": "Viete_Product_for_Cos",
                "tags": ["viete", "cosine", "infinite-product"]
            },
            {
                "id": "8",
                "name": "Viete_Product_for_Sin",
                "display_name": "Viète Product for Sine", 
                "description": "Viète infinite product formula for sine",
                "category": "Viète Products",
                "latex_formula": "V_\\sin(z) = \\prod_{n=1}^{\\infty} \\sin\\left(\\frac{z}{2^n}\\right)",
                "python_implementation": "Viete_Product_for_Sin", 
                "tags": ["viete", "sine", "infinite-product"]
            },
            {
                "id": "9", 
                "name": "Viete_Product_for_Tan",
                "display_name": "Viète Product for Tangent",
                "description": "Viète infinite product formula for tangent",
                "category": "Viète Products",
                "latex_formula": "V_\\tan(z) = \\prod_{n=1}^{\\infty} \\tan\\left(\\frac{z}{2^n}\\right)",
                "python_implementation": "Viete_Product_for_Tan",
                "tags": ["viete", "tangent", "infinite-product"]
            },
            # Composite Functions
            {
                "id": "10",
                "name": "cos_of_product_of_sin",
                "display_name": "Cosine of Product of Sin", 
                "description": "Cosine applied to the main product of sin function",
                "category": "Composite Functions",
                "latex_formula": "\\cos(f(z))",
                "python_implementation": "cos_of_product_of_sin",
                "dependencies": ["product_of_sin"],
                "tags": ["composite", "cosine", "derived"]
            },
            {
                "id": "11",
                "name": "sin_of_product_of_sin",
                "display_name": "Sine of Product of Sin",
                "description": "Sine applied to the main product of sin function", 
                "category": "Composite Functions",
                "latex_formula": "\\sin(f(z))",
                "python_implementation": "sin_of_product_of_sin",
                "dependencies": ["product_of_sin"],
                "tags": ["composite", "sine", "derived"]
            },
            {
                "id": "12",
                "name": "cos_of_product_of_product_representation_of_sin",
                "display_name": "Cosine of Double Product", 
                "description": "Cosine applied to the double product representation",
                "category": "Composite Functions",
                "latex_formula": "\\cos(g(z))",
                "python_implementation": "cos_of_product_of_product_representation_of_sin",
                "dependencies": ["product_of_product_representation_for_sin"],
                "tags": ["composite", "cosine", "double-product"]
            },
            {
                "id": "13",
                "name": "sin_of_product_of_product_representation_of_sin",
                "display_name": "Sine of Double Product",
                "description": "Sine applied to the double product representation",
                "category": "Composite Functions", 
                "latex_formula": "\\sin(g(z))",
                "python_implementation": "sin_of_product_of_product_representation_of_sin",
                "dependencies": ["product_of_product_representation_for_sin"],
                "tags": ["composite", "sine", "double-product"]
            },
            # Prime Indicators
            {
                "id": "14",
                "name": "Binary_Output_Prime_Indicator_Function_H",
                "display_name": "Binary Output Prime Indicator Function (H)",
                "description": "Binary prime indicator function based on divisor wave analysis",
                "category": "Prime Indicators",
                "latex_formula": "H(z) = \\text{Binary prime indicator}",
                "python_implementation": "Binary_Output_Prime_Indicator_Function_H",
                "tags": ["prime", "indicator", "binary"],
                "dependencies": ["product_of_sin"]
            },
            {
                "id": "15", 
                "name": "Prime_Output_Indicator_J",
                "display_name": "Prime Output Indicator (J)",
                "description": "Prime output indicator function J for prime detection",
                "category": "Prime Indicators",
                "latex_formula": "J(z) = \\text{Prime indicator output}",
                "python_implementation": "Prime_Output_Indicator_J",
                "tags": ["prime", "indicator", "detection"],
                "dependencies": ["Binary_Output_Prime_Indicator_Function_H"]
            },
            {
                "id": "16",
                "name": "BOPIF_Q_Alternation_Series", 
                "display_name": "BOPIF Q Alternation Series",
                "description": "Binary Output Prime Indicator alternating series Q",
                "category": "Prime Indicators",
                "latex_formula": "Q(z) = \\sum (-1)^n H(n)",
                "python_implementation": "BOPIF_Q_Alternation_Series",
                "tags": ["prime", "series", "alternating"],
                "dependencies": ["Binary_Output_Prime_Indicator_Function_H"]
            },
            {
                "id": "17",
                "name": "Dirichlet_Eta_Derived_From_BOPIF",
                "display_name": "Dirichlet Eta from BOPIF",
                "description": "Dirichlet eta function derived from Binary Output Prime Indicator", 
                "category": "Prime Indicators",
                "latex_formula": "\\eta(z) = \\text{Derived from BOPIF}",
                "python_implementation": "Dirichlet_Eta_Derived_From_BOPIF",
                "tags": ["dirichlet", "eta", "prime", "derived"],
                "dependencies": ["Binary_Output_Prime_Indicator_Function_H"]
            },
            # Basic Functions
            {
                "id": "18",
                "name": "abs_loggamma",
                "display_name": "Absolute Log Gamma", 
                "description": "Absolute value of log gamma function",
                "category": "Basic Functions",
                "latex_formula": "|\\log\\Gamma(z)|",
                "python_implementation": "abs_loggamma",
                "tags": ["gamma", "logarithm", "basic"]
            },
            {
                "id": "19", 
                "name": "rational_one_plus_z_squared",
                "display_name": "Rational 1 + z²",
                "description": "Simple rational function 1/(1 + z²)",
                "category": "Basic Functions",
                "latex_formula": "\\frac{1}{1 + z^2}",
                "python_implementation": "rational_one_plus_z_squared", 
                "tags": ["rational", "basic"]
            },
            {
                "id": "20",
                "name": "abs_z_to_z",
                "display_name": "Absolute z^z",
                "description": "Absolute value of z raised to the power z",
                "category": "Basic Functions",
                "latex_formula": "|z^z|",
                "python_implementation": "abs_z_to_z",
                "tags": ["power", "basic"]
            },
            {
                "id": "21",
                "name": "gamma_function", 
                "display_name": "Gamma Function",
                "description": "Standard gamma function implementation",
                "category": "Basic Functions",
                "latex_formula": "\\Gamma(z)",
                "python_implementation": "gamma_function",
                "tags": ["gamma", "special", "basic"]
            }
        ]
        
        # Add remaining functions (22-31) from the current system
        additional_functions = [
            {
                "id": "22",
                "name": "gamma_of_product_of_product_representation_for_sin",
                "display_name": "Gamma of Double Product",
                "description": "Gamma function applied to the double product representation",
                "category": "Gamma Variants",
                "latex_formula": "\\Gamma(g(z))",
                "python_implementation": "gamma_of_product_of_product_representation_for_sin",
                "dependencies": ["product_of_product_representation_for_sin"],
                "tags": ["gamma", "composite", "double-product"]
            },
            {
                "id": "23", 
                "name": "natural_logarithm_of_product_of_product_representation_for_sin",
                "display_name": "Natural Log of Double Product",
                "description": "Natural logarithm applied to the double product representation",
                "category": "Logarithmic Variants",
                "latex_formula": "\\ln(g(z))",
                "python_implementation": "natural_logarithm_of_product_of_product_representation_for_sin",
                "dependencies": ["product_of_product_representation_for_sin"],
                "tags": ["logarithm", "composite", "double-product"]
            },
            {
                "id": "24",
                "name": "gamma_form_product_of_product_representation_for_sin", 
                "display_name": "Gamma Form Double Product",
                "description": "Gamma-form representation of the double product function",
                "category": "Gamma Variants",
                "latex_formula": "\\Gamma\\text{-form}(g(z))",
                "python_implementation": "gamma_form_product_of_product_representation_for_sin",
                "dependencies": ["product_of_product_representation_for_sin"],
                "tags": ["gamma", "form", "double-product"]
            },
            {
                "id": "25",
                "name": "Custom_Riesz_Product_for_Tan",
                "display_name": "Custom Riesz Product for Tangent",
                "description": "Custom variant of Riesz product using tangent functions",
                "category": "Riesz Products",
                "latex_formula": "R_{\\tan}^{custom}(z) = \\prod_{n=2}^{z} \\tan\\left(\\frac{\\pi z}{2^n}\\right)",
                "python_implementation": "Custom_Riesz_Product_for_Tan",
                "tags": ["riesz", "tangent", "custom"]
            },
            {
                "id": "26",
                "name": "Custom_Viete_Product_for_Cos", 
                "display_name": "Custom Viète Product for Cosine",
                "description": "Custom variant of Viète product using cosine functions",
                "category": "Viète Products",
                "latex_formula": "V_{\\cos}^{custom}(z) = \\prod_{n=1}^{\\infty} \\cos\\left(\\frac{z}{2^n}\\right)",
                "python_implementation": "Custom_Viete_Product_for_Cos",
                "tags": ["viete", "cosine", "custom"]
            },
            {
                "id": "27",
                "name": "Log_power_base_Viete_Product_for_Sin",
                "display_name": "Log Power Base Viète Product for Sine", 
                "description": "Logarithmic power base variant of Viète product for sine",
                "category": "Viète Products",
                "latex_formula": "V_{\\sin}^{log}(z) = \\log\\left(\\prod_{n=1}^{\\infty} \\sin\\left(\\frac{z}{2^n}\\right)^{1/2^n}\\right)",
                "python_implementation": "Log_power_base_Viete_Product_for_Sin",
                "tags": ["viete", "sine", "logarithm", "power"]
            },
            {
                "id": "28",
                "name": "Riesz_Product_for_Tan_and_Prime_indicator_combination",
                "display_name": "Riesz Tan + Prime Indicator Combination",
                "description": "Combination of Riesz tangent product with prime indicator function",
                "category": "Prime Indicators",
                "latex_formula": "R_{\\tan}(z) \\cdot H(z)",
                "python_implementation": "Riesz_Product_for_Tan_and_Prime_indicator_combination",
                "dependencies": ["Binary_Output_Prime_Indicator_Function_H"],
                "tags": ["riesz", "prime", "indicator", "combination"]
            },
            {
                "id": "29",
                "name": "Nested_roots_product_for_2", 
                "display_name": "Nested Roots Product for 2",
                "description": "Nested radical product representation for the constant 2",
                "category": "Special Functions",
                "latex_formula": "\\sqrt{2 + \\sqrt{2 + \\sqrt{2 + \\cdots}}}",
                "python_implementation": "Nested_roots_product_for_2",
                "tags": ["nested", "roots", "constant", "special"]
            },
            {
                "id": "30",
                "name": "Half_Base_Viete_Product_for_Sin",
                "display_name": "Half Base Viète Product for Sine",
                "description": "Half-base variant of Viète product for sine function",
                "category": "Viète Products",
                "latex_formula": "V_{\\sin}^{1/2}(z) = \\prod_{n=1}^{\\infty} \\sin\\left(\\frac{z}{2^{n+1}}\\right)",
                "python_implementation": "Half_Base_Viete_Product_for_Sin",
                "tags": ["viete", "sine", "half-base"]
            },
            {
                "id": "31",
                "name": "product_factory",
                "display_name": "Product Factory",
                "description": "Factory function for generating custom infinite products",
                "category": "Factory Functions",
                "latex_formula": "\\text{Factory}(\\text{params}) \\rightarrow \\prod_{n=a}^{b} f(n, z)",
                "python_implementation": "product_factory",
                "tags": ["factory", "generator", "utility"]
            }
        ]
        
        # Merge all function definitions
        for func_data in builtin_functions + additional_functions:
            func_def = FunctionDefinition(**func_data)
            self.functions[func_def.id] = func_def
    
    def _import_legacy_data(self):
        """Import data from existing JSON files to maintain compatibility"""
        try:
            # Import from divisor_wave_formulas.json
            formulas_path = Path(__file__).parent / "../data/formulas/core_functions.json"
            if formulas_path.exists():
                with open(formulas_path) as f:
                    formulas_data = json.load(f)
                    
                for name, formula_info in formulas_data.get('formulas', {}).items():
                    # Update existing functions with better LaTeX formulas
                    for func_id, func_def in self.functions.items():
                        if func_def.name == name and formula_info.get('latex'):
                            func_def.latex_formula = formula_info['latex']
                            func_def.description = formula_info.get('description', func_def.description)
                            
            # Import custom functions
            custom_path = Path(__file__).parent / "../data/formulas/custom_functions.json"
            if custom_path.exists():
                with open(custom_path) as f:
                    custom_data = json.load(f)
                    
                for name, func_info in custom_data.get('functions', {}).items():
                    custom_func = FunctionDefinition(
                        id=f"custom_{len([f for f in self.functions.values() if f.source == 'custom']) + 1}",
                        name=name,
                        display_name=func_info.get('name', name),
                        description=func_info.get('description', ''),
                        category=func_info.get('category', 'Custom'),
                        latex_formula=func_info.get('latex_formula', ''),
                        python_implementation=func_info.get('python_code', ''),
                        source='custom'
                    )
                    self.functions[custom_func.id] = custom_func
                    
        except Exception as e:
            print(f"Warning: Could not import legacy data: {e}")
    
    def register_function(self, func_def: FunctionDefinition) -> bool:
        """Register a new function in the registry"""
        try:
            func_def.updated_at = datetime.now().isoformat()
            self.functions[func_def.id] = func_def
            self.save_registry()
            return True
        except Exception as e:
            print(f"Error registering function {func_def.name}: {e}")
            return False
    
    def get_function(self, identifier: str) -> Optional[FunctionDefinition]:
        """Get function by ID or name"""
        # Try by ID first
        if identifier in self.functions:
            return self.functions[identifier]
            
        # Try by name
        for func_def in self.functions.values():
            if func_def.name == identifier:
                return func_def
                
        return None
    
    def get_functions_by_category(self) -> Dict[str, List[FunctionDefinition]]:
        """Group functions by category for frontend display"""
        categories = {}
        for func_def in self.functions.values():
            if func_def.category not in categories:
                categories[func_def.category] = []
            categories[func_def.category].append(func_def)
        
        return categories
    
    def get_lambda_catalog(self) -> Dict[str, str]:
        """Generate lambda catalog for backward compatibility"""
        return {func_def.id: func_def.name for func_def in self.functions.values()}
    
    def get_api_mappings(self) -> Dict[str, str]:
        """Generate API function mappings"""
        return {func_def.id: func_def.name for func_def in self.functions.values()}
    
    def get_latex_database(self) -> Dict[str, Dict[str, Any]]:
        """Generate LaTeX formula database"""
        latex_db = {}
        for func_def in self.functions.values():
            latex_db[func_def.name] = {
                'latex': func_def.latex_formula,
                'description': func_def.description,
                'category': func_def.category,
                'id': func_def.id
            }
        return latex_db
    
    def search_functions(self, query: str, filters: Dict[str, Any] = None) -> List[FunctionDefinition]:
        """Search functions by various criteria"""
        results = []
        query_lower = query.lower()
        
        for func_def in self.functions.values():
            # Text search
            if (query_lower in func_def.name.lower() or 
                query_lower in func_def.display_name.lower() or
                query_lower in func_def.description.lower() or
                any(query_lower in tag for tag in func_def.tags)):
                
                # Apply filters
                if filters:
                    if filters.get('category') and func_def.category != filters['category']:
                        continue
                    if filters.get('source') and func_def.source != filters['source']:
                        continue
                    if filters.get('tags') and not any(tag in func_def.tags for tag in filters['tags']):
                        continue
                        
                results.append(func_def)
        
        return results
    
    def add_custom_function(self, name: str, latex_formula: str, description: str = "", 
                          category: str = "Custom", python_code: str = "") -> str:
        """Add a new custom function"""
        custom_id = f"custom_{len([f for f in self.functions.values() if f.source == 'custom']) + 1}"
        
        func_def = FunctionDefinition(
            id=custom_id,
            name=name,
            display_name=name.replace('_', ' ').title(),
            description=description,
            category=category,
            latex_formula=latex_formula,
            python_implementation=python_code,
            source='custom',
            author='User'
        )
        
        if self.register_function(func_def):
            return custom_id
        return None
    
    def update_function(self, identifier: str, updates: Dict[str, Any]) -> bool:
        """Update an existing function"""
        func_def = self.get_function(identifier)
        if not func_def:
            return False
            
        for key, value in updates.items():
            if hasattr(func_def, key):
                setattr(func_def, key, value)
        
        func_def.updated_at = datetime.now().isoformat()
        return self.register_function(func_def)
    
    def delete_function(self, identifier: str) -> bool:
        """Delete a function (only custom functions)"""
        func_def = self.get_function(identifier)
        if not func_def or func_def.source != 'custom':
            return False
            
        if func_def.id in self.functions:
            del self.functions[func_def.id]
            self.save_registry()
            return True
        return False
    
    def export_for_component(self, component: str) -> Dict[str, Any]:
        """Export data in format expected by specific component"""
        if component == 'lambda_catalog':
            return {func_def.id: func_def.name for func_def in self.functions.values()}
            
        elif component == 'api_functions':
            result = {}
            for func_def in self.functions.values():
                result[func_def.name] = {
                    'id': func_def.id,
                    'display_name': func_def.display_name,
                    'description': func_def.description,
                    'category': func_def.category,
                    'latex_formula': func_def.latex_formula,
                    'tags': func_def.tags,
                    'dependencies': func_def.dependencies
                }
            return result
            
        elif component == 'latex_formulas':
            result = {'formulas': {}}
            for func_def in self.functions.values():
                result['formulas'][func_def.name] = {
                    'latex': func_def.latex_formula,
                    'description': func_def.description,
                    'category': func_def.category
                }
            return result
            
        elif component == 'frontend_dropdown':
            categories = self.get_functions_by_category()
            result = {}
            for category, functions in categories.items():
                result[category] = []
                for func_def in functions:
                    result[category].append({
                        'id': func_def.id,
                        'name': func_def.name,
                        'display_name': func_def.display_name,
                        'description': func_def.description,
                        'latex_formula': func_def.latex_formula
                    })
            return result
        
        return {}
    
    def save_registry(self):
        """Save the complete registry to JSON"""
        registry_data = {
            'metadata': {
                'version': '1.0.0',
                'created': datetime.now().isoformat(),
                'total_functions': len(self.functions)
            },
            'functions': {}
        }
        
        for func_id, func_def in self.functions.items():
            registry_data['functions'][func_id] = asdict(func_def)
        
        with open(self.registry_path, 'w') as f:
            json.dump(registry_data, f, indent=2)
    
    def load_registry(self):
        """Load registry from JSON file"""
        if not self.registry_path.exists():
            return
            
        try:
            with open(self.registry_path) as f:
                registry_data = json.load(f)
                
            for func_id, func_data in registry_data.get('functions', {}).items():
                self.functions[func_id] = FunctionDefinition(**func_data)
                
        except Exception as e:
            print(f"Warning: Could not load registry: {e}")
    
    def sync_legacy_files(self):
        """Synchronize with legacy JSON files for backward compatibility"""
        # Update divisor_wave_formulas.json
        latex_data = self.export_for_component('latex_formulas')
        formulas_path = Path(__file__).parent / "../data/formulas/core_functions.json"
        
        # Add metadata to match expected format
        latex_data.update({
            'normalization_info': {
                'N': 'No gamma normalization',
                'Y': 'With gamma normalization: result / Γ(result)',
                'X': 'Real axis normalization',
                'Z': 'Imaginary axis normalization', 
                'XYZ': 'Combined axis normalization'
            },
            'coefficient_explanation': {
                'm': 'Exponential magnification coefficient',
                'beta': 'Lead scaling coefficient',
                'description': 'Coefficients may vary based on normalization type (N vs Y)'
            },
            'metadata': {
                'version': '1.1',
                'updated': datetime.now().isoformat(),
                'description': 'LaTeX formulas for all divisor wave functions from Leo J. Borcherding\'s research',
                'total_formulas': len([f for f in self.functions.values() if f.source == 'builtin'])
            }
        })
        
        with open(formulas_path, 'w') as f:
            json.dump(latex_data, f, indent=2)
            
        # Update custom_functions.json
        custom_funcs = {f.name: asdict(f) for f in self.functions.values() if f.source == 'custom'}
        if custom_funcs:
            custom_path = Path(__file__).parent / "../data/formulas/custom_functions.json"
            custom_data = {
                'functions': custom_funcs,
                'metadata': {
                    'version': '1.0',
                    'count': len(custom_funcs),
                    'updated': datetime.now().isoformat()
                }
            }
            with open(custom_path, 'w') as f:
                json.dump(custom_data, f, indent=2)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get registry statistics"""
        categories = {}
        sources = {}
        
        for func_def in self.functions.values():
            categories[func_def.category] = categories.get(func_def.category, 0) + 1
            sources[func_def.source] = sources.get(func_def.source, 0) + 1
        
        return {
            'total_functions': len(self.functions),
            'by_category': categories,
            'by_source': sources,
            'latest_update': max((f.updated_at for f in self.functions.values()), default='Never')
        }


# Global registry instance
_registry = None

def get_registry() -> FunctionRegistry:
    """Get the global function registry instance"""
    global _registry
    if _registry is None:
        _registry = FunctionRegistry()
    return _registry


# Example usage and testing
if __name__ == "__main__":
    # Initialize registry
    registry = FunctionRegistry()
    
    # Print statistics
    stats = registry.get_stats()
    print("Function Registry Statistics:")
    print(f"Total Functions: {stats['total_functions']}")
    print(f"Categories: {list(stats['by_category'].keys())}")
    print(f"Sources: {stats['by_source']}")
    
    # Test search
    prime_functions = registry.search_functions("prime")
    print(f"\nFound {len(prime_functions)} functions related to 'prime'")
    
    # Test exports
    lambda_catalog = registry.export_for_component('lambda_catalog')
    print(f"\nLambda catalog has {len(lambda_catalog)} entries")
    
    # Test adding custom function
    custom_id = registry.add_custom_function(
        name="test_function",
        latex_formula="f(x) = x^2",
        description="Simple test function"
    )
    print(f"Added custom function with ID: {custom_id}")
    
    # Save and sync
    registry.save_registry()
    registry.sync_legacy_files()
    print("Registry saved and synchronized with legacy files")