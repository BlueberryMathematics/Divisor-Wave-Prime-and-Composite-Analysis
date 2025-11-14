"""
Mathematical Function Uniqueness Validator
AI tool for validating uniqueness of newly discovered mathematical functions

This system checks against existing function databases, validates mathematical
properties, and ensures no duplicate discoveries are made.
"""

import os
import sys
import json
import hashlib
import asyncio
from typing import Dict, List, Tuple, Optional, Any, Set
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass

# Add project paths
current_dir = Path(__file__).parent.parent.parent
sys.path.append(str(current_dir / "divisor-wave-python" / "src"))

try:
    import sympy as sp
    from sympy.parsing.latex import parse_latex
    from sympy import symbols, simplify, expand
    SYMPY_AVAILABLE = True
except ImportError:
    print("⚠️ SymPy not available for mathematical validation")
    SYMPY_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

from core.function_registry import get_registry
from core.latex_function_builder import LaTeXFunctionBuilder


@dataclass
class ValidationResult:
    """Result of function uniqueness validation"""
    is_unique: bool
    confidence_score: float
    duplicate_functions: List[Dict]
    similar_functions: List[Dict]
    validation_methods: List[str]
    mathematical_properties: Dict
    recommendations: List[str]
    status: str  # 'unique', 'duplicate', 'similar', 'invalid'


class MathematicalFunctionValidator:
    """
    Comprehensive validator for mathematical function uniqueness.
    
    Features:
    - Multiple validation methods (hash, structure, symbolic)
    - Mathematical property analysis
    - Cross-reference with existing databases
    - Confidence scoring system
    - Detailed validation reports
    """
    
    def __init__(self):
        self.function_registry = get_registry()
        self.latex_builder = LaTeXFunctionBuilder()
        
        # Load existing function databases
        self.existing_functions = self._load_all_function_databases()
        
        # Mathematical property analyzers
        self.property_analyzers = self._initialize_property_analyzers()
        
        print("✅ Mathematical Function Validator initialized")
    
    def _load_all_function_databases(self) -> Dict:
        """Load all available function databases"""
        
        databases = {}
        
        # Load main function registry
        try:
            registry_functions = self.function_registry.get_all_functions()
            databases['function_registry'] = registry_functions
            print(f"📚 Loaded {len(registry_functions)} functions from registry")
        except Exception as e:
            print(f"⚠️ Failed to load function registry: {e}")
            databases['function_registry'] = {}
        
        # Load custom functions JSON
        try:
            custom_functions_path = current_dir / "divisor-wave-python" / "src" / "core" / "custom_functions.json"
            if custom_functions_path.exists():
                with open(custom_functions_path, 'r', encoding='utf-8') as f:
                    custom_data = json.load(f)
                    databases['custom_functions'] = custom_data.get('functions', {})
                    print(f"📚 Loaded {len(databases['custom_functions'])} custom functions")
            else:
                databases['custom_functions'] = {}
        except Exception as e:
            print(f"⚠️ Failed to load custom functions: {e}")
            databases['custom_functions'] = {}
        
        # Load divisor wave formulas
        try:
            formulas_path = current_dir / "divisor-wave-python" / "src" / "core" / "divisor_wave_formulas.json"
            if formulas_path.exists():
                with open(formulas_path, 'r', encoding='utf-8') as f:
                    formulas_data = json.load(f)
                    databases['divisor_wave_formulas'] = formulas_data.get('formulas', {})
                    print(f"📚 Loaded {len(databases['divisor_wave_formulas'])} divisor wave formulas")
            else:
                databases['divisor_wave_formulas'] = {}
        except Exception as e:
            print(f"⚠️ Failed to load divisor wave formulas: {e}")
            databases['divisor_wave_formulas'] = {}
        
        return databases
    
    def _initialize_property_analyzers(self) -> Dict:
        """Initialize mathematical property analyzers"""
        
        return {
            'latex_hash': self._analyze_latex_hash,
            'normalized_latex': self._analyze_normalized_latex,
            'symbolic_equivalence': self._analyze_symbolic_equivalence,
            'structural_similarity': self._analyze_structural_similarity,
            'mathematical_properties': self._analyze_mathematical_properties,
            'coefficient_patterns': self._analyze_coefficient_patterns
        }
    
    async def validate_function_uniqueness(self, function_data: Dict) -> ValidationResult:
        """
        Comprehensive validation of function uniqueness
        
        Args:
            function_data: Dictionary containing function information
                          Keys: name, latex_formula, description, category, properties
                          
        Returns:
            ValidationResult with comprehensive analysis
        """
        
        print(f"🔍 Validating uniqueness for function: {function_data.get('name', 'unnamed')}")
        
        # Initialize validation results
        duplicate_functions = []
        similar_functions = []
        validation_methods = []
        mathematical_properties = {}
        
        # Validation Method 1: Exact hash matching
        hash_results = await self._validate_by_hash(function_data)
        validation_methods.append('hash_comparison')
        if hash_results['duplicates']:
            duplicate_functions.extend(hash_results['duplicates'])
        
        # Validation Method 2: Normalized LaTeX comparison
        latex_results = await self._validate_by_normalized_latex(function_data)
        validation_methods.append('normalized_latex')
        if latex_results['duplicates']:
            duplicate_functions.extend(latex_results['duplicates'])
        if latex_results['similar']:
            similar_functions.extend(latex_results['similar'])
        
        # Validation Method 3: Symbolic equivalence (if SymPy available)
        if SYMPY_AVAILABLE:
            symbolic_results = await self._validate_by_symbolic_equivalence(function_data)
            validation_methods.append('symbolic_equivalence')
            if symbolic_results['duplicates']:
                duplicate_functions.extend(symbolic_results['duplicates'])
            if symbolic_results['similar']:
                similar_functions.extend(symbolic_results['similar'])
        
        # Validation Method 4: Structural analysis
        structural_results = await self._validate_by_structure(function_data)
        validation_methods.append('structural_analysis')
        if structural_results['similar']:
            similar_functions.extend(structural_results['similar'])
        
        # Analyze mathematical properties
        mathematical_properties = await self._extract_mathematical_properties(function_data)
        
        # Remove duplicates from results
        duplicate_functions = self._deduplicate_results(duplicate_functions)
        similar_functions = self._deduplicate_results(similar_functions)
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(
            duplicate_functions, similar_functions, validation_methods
        )
        
        # Determine uniqueness status
        is_unique = len(duplicate_functions) == 0
        status = self._determine_status(duplicate_functions, similar_functions)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            duplicate_functions, similar_functions, status
        )
        
        return ValidationResult(
            is_unique=is_unique,
            confidence_score=confidence_score,
            duplicate_functions=duplicate_functions,
            similar_functions=similar_functions,
            validation_methods=validation_methods,
            mathematical_properties=mathematical_properties,
            recommendations=recommendations,
            status=status
        )
    
    async def _validate_by_hash(self, function_data: Dict) -> Dict:
        """Validate using hash comparison"""
        
        new_latex = function_data.get('latex_formula', '')
        new_hash = self._generate_latex_hash(new_latex)
        
        duplicates = []
        
        # Check against all databases
        for db_name, db_functions in self.existing_functions.items():
            for func_id, func_data in db_functions.items():
                existing_hash = func_data.get('hash', '')
                if not existing_hash:
                    # Generate hash if not present
                    existing_latex = func_data.get('latex_formula', '')
                    existing_hash = self._generate_latex_hash(existing_latex)
                
                if new_hash == existing_hash and existing_hash != '':
                    duplicates.append({
                        'database': db_name,
                        'function_id': func_id,
                        'name': func_data.get('name', ''),
                        'latex_formula': func_data.get('latex_formula', ''),
                        'match_type': 'exact_hash',
                        'confidence': 1.0
                    })
        
        return {'duplicates': duplicates}
    
    async def _validate_by_normalized_latex(self, function_data: Dict) -> Dict:
        """Validate using normalized LaTeX comparison"""
        
        new_latex = function_data.get('latex_formula', '')
        new_normalized = self._normalize_latex(new_latex)
        
        duplicates = []
        similar = []
        
        for db_name, db_functions in self.existing_functions.items():
            for func_id, func_data in db_functions.items():
                existing_latex = func_data.get('latex_formula', '')
                existing_normalized = self._normalize_latex(existing_latex)
                
                # Exact normalized match
                if new_normalized == existing_normalized and existing_normalized != '':
                    duplicates.append({
                        'database': db_name,
                        'function_id': func_id,
                        'name': func_data.get('name', ''),
                        'latex_formula': existing_latex,
                        'match_type': 'normalized_exact',
                        'confidence': 0.95
                    })
                
                # Similar normalized structure
                elif self._calculate_latex_similarity(new_normalized, existing_normalized) > 0.8:
                    similarity_score = self._calculate_latex_similarity(new_normalized, existing_normalized)
                    similar.append({
                        'database': db_name,
                        'function_id': func_id,
                        'name': func_data.get('name', ''),
                        'latex_formula': existing_latex,
                        'match_type': 'normalized_similar',
                        'confidence': similarity_score
                    })
        
        return {'duplicates': duplicates, 'similar': similar}
    
    async def _validate_by_symbolic_equivalence(self, function_data: Dict) -> Dict:
        """Validate using symbolic mathematical equivalence"""
        
        if not SYMPY_AVAILABLE:
            return {'duplicates': [], 'similar': []}
        
        new_latex = function_data.get('latex_formula', '')
        
        try:
            new_expr = parse_latex(new_latex)
            new_simplified = simplify(new_expr)
        except Exception as e:
            print(f"⚠️ Failed to parse new function LaTeX: {e}")
            return {'duplicates': [], 'similar': []}
        
        duplicates = []
        similar = []
        
        for db_name, db_functions in self.existing_functions.items():
            for func_id, func_data in db_functions.items():
                existing_latex = func_data.get('latex_formula', '')
                if not existing_latex:
                    continue
                
                try:
                    existing_expr = parse_latex(existing_latex)
                    existing_simplified = simplify(existing_expr)
                    
                    # Check symbolic equivalence
                    if new_simplified.equals(existing_simplified):
                        duplicates.append({
                            'database': db_name,
                            'function_id': func_id,
                            'name': func_data.get('name', ''),
                            'latex_formula': existing_latex,
                            'match_type': 'symbolic_equivalent',
                            'confidence': 0.98
                        })
                    
                    # Check structural similarity
                    elif self._check_symbolic_similarity(new_simplified, existing_simplified) > 0.7:
                        similarity_score = self._check_symbolic_similarity(new_simplified, existing_simplified)
                        similar.append({
                            'database': db_name,
                            'function_id': func_id,
                            'name': func_data.get('name', ''),
                            'latex_formula': existing_latex,
                            'match_type': 'symbolic_similar',
                            'confidence': similarity_score
                        })
                
                except Exception:
                    continue  # Skip functions that can't be parsed
        
        return {'duplicates': duplicates, 'similar': similar}
    
    async def _validate_by_structure(self, function_data: Dict) -> Dict:
        """Validate using mathematical structure analysis"""
        
        new_latex = function_data.get('latex_formula', '')
        new_structure = self._analyze_mathematical_structure(new_latex)
        
        similar = []
        
        for db_name, db_functions in self.existing_functions.items():
            for func_id, func_data in db_functions.items():
                existing_latex = func_data.get('latex_formula', '')
                existing_structure = self._analyze_mathematical_structure(existing_latex)
                
                # Calculate structural similarity
                similarity_score = self._calculate_structural_similarity(
                    new_structure, existing_structure
                )
                
                if similarity_score > 0.6:  # Significant structural similarity
                    similar.append({
                        'database': db_name,
                        'function_id': func_id,
                        'name': func_data.get('name', ''),
                        'latex_formula': existing_latex,
                        'match_type': 'structural_similar',
                        'confidence': similarity_score
                    })
        
        return {'similar': similar}
    
    def _generate_latex_hash(self, latex_formula: str) -> str:
        """Generate normalized hash for LaTeX formula"""
        
        normalized = self._normalize_latex(latex_formula)
        return hashlib.sha256(normalized.encode()).hexdigest()[:12]
    
    def _normalize_latex(self, latex_formula: str) -> str:
        """Normalize LaTeX formula for comparison"""
        
        if not latex_formula:
            return ''
        
        # Basic normalization
        normalized = latex_formula.strip().lower()
        
        # Remove extra whitespace
        normalized = ' '.join(normalized.split())
        
        # Normalize common variations
        replacements = {
            '\\cdot': '*',
            '\\times': '*',
            '\\,': ' ',
            '\\;': ' ',
            '\\quad': ' ',
            '\\qquad': ' ',
        }
        
        for old, new in replacements.items():
            normalized = normalized.replace(old, new)
        
        return normalized
    
    def _calculate_latex_similarity(self, latex1: str, latex2: str) -> float:
        """Calculate similarity between two LaTeX strings"""
        
        if not latex1 or not latex2:
            return 0.0
        
        # Convert to sets of tokens
        tokens1 = set(latex1.split())
        tokens2 = set(latex2.split())
        
        # Jaccard similarity
        intersection = len(tokens1.intersection(tokens2))
        union = len(tokens1.union(tokens2))
        
        return intersection / union if union > 0 else 0.0
    
    def _check_symbolic_similarity(self, expr1, expr2) -> float:
        """Check similarity between SymPy expressions"""
        
        if not SYMPY_AVAILABLE:
            return 0.0
        
        try:
            # Get atoms and functions from expressions
            atoms1 = expr1.atoms()
            atoms2 = expr2.atoms()
            
            # Calculate atom similarity
            if not atoms1 and not atoms2:
                return 1.0
            
            common_atoms = len(atoms1.intersection(atoms2))
            total_atoms = len(atoms1.union(atoms2))
            
            atom_similarity = common_atoms / total_atoms if total_atoms > 0 else 0.0
            
            # Get function types
            funcs1 = {type(atom).__name__ for atom in atoms1 if hasattr(atom, '__call__')}
            funcs2 = {type(atom).__name__ for atom in atoms2 if hasattr(atom, '__call__')}
            
            if funcs1 or funcs2:
                common_funcs = len(funcs1.intersection(funcs2))
                total_funcs = len(funcs1.union(funcs2))
                func_similarity = common_funcs / total_funcs if total_funcs > 0 else 0.0
            else:
                func_similarity = 1.0
            
            # Combined similarity
            return (atom_similarity + func_similarity) / 2
            
        except Exception:
            return 0.0
    
    def _analyze_mathematical_structure(self, latex_formula: str) -> Dict:
        """Analyze the mathematical structure of a formula"""
        
        structure = {
            'operators': set(),
            'functions': set(),
            'symbols': set(),
            'patterns': set(),
            'complexity': 0
        }
        
        latex_lower = latex_formula.lower()
        
        # Detect operators
        operators = {
            'sum': '\\sum' in latex_lower,
            'product': '\\prod' in latex_lower,
            'integral': '\\int' in latex_lower,
            'fraction': '\\frac' in latex_lower,
            'power': '^' in latex_lower,
            'subscript': '_' in latex_lower,
            'sqrt': '\\sqrt' in latex_lower
        }
        
        for op, present in operators.items():
            if present:
                structure['operators'].add(op)
        
        # Detect functions
        functions = {
            'sin': '\\sin' in latex_lower,
            'cos': '\\cos' in latex_lower,
            'tan': '\\tan' in latex_lower,
            'exp': '\\exp' in latex_lower or 'e^' in latex_lower,
            'log': '\\log' in latex_lower or '\\ln' in latex_lower,
            'gamma': '\\gamma' in latex_lower,
            'zeta': '\\zeta' in latex_lower,
            'eta': '\\eta' in latex_lower
        }
        
        for func, present in functions.items():
            if present:
                structure['functions'].add(func)
        
        # Detect special symbols
        symbols = {
            'pi': '\\pi' in latex_lower,
            'infinity': '\\infty' in latex_lower,
            'alpha': '\\alpha' in latex_lower,
            'beta': '\\beta' in latex_lower,
            'theta': '\\theta' in latex_lower
        }
        
        for symbol, present in symbols.items():
            if present:
                structure['symbols'].add(symbol)
        
        # Detect patterns
        if 'product' in structure['operators'] and 'infinity' in structure['symbols']:
            structure['patterns'].add('infinite_product')
        if 'sum' in structure['operators'] and 'infinity' in structure['symbols']:
            structure['patterns'].add('infinite_sum')
        if any(trig in structure['functions'] for trig in ['sin', 'cos', 'tan']):
            structure['patterns'].add('trigonometric')
        
        # Calculate complexity
        structure['complexity'] = (
            len(structure['operators']) * 2 +
            len(structure['functions']) * 3 +
            len(structure['symbols']) * 1 +
            len(structure['patterns']) * 4
        )
        
        return structure
    
    def _calculate_structural_similarity(self, struct1: Dict, struct2: Dict) -> float:
        """Calculate similarity between mathematical structures"""
        
        total_similarity = 0.0
        weight_sum = 0.0
        
        # Compare operators
        if struct1['operators'] or struct2['operators']:
            op_jaccard = self._jaccard_similarity(struct1['operators'], struct2['operators'])
            total_similarity += op_jaccard * 3
            weight_sum += 3
        
        # Compare functions
        if struct1['functions'] or struct2['functions']:
            func_jaccard = self._jaccard_similarity(struct1['functions'], struct2['functions'])
            total_similarity += func_jaccard * 4
            weight_sum += 4
        
        # Compare symbols
        if struct1['symbols'] or struct2['symbols']:
            symbol_jaccard = self._jaccard_similarity(struct1['symbols'], struct2['symbols'])
            total_similarity += symbol_jaccard * 2
            weight_sum += 2
        
        # Compare patterns
        if struct1['patterns'] or struct2['patterns']:
            pattern_jaccard = self._jaccard_similarity(struct1['patterns'], struct2['patterns'])
            total_similarity += pattern_jaccard * 5
            weight_sum += 5
        
        return total_similarity / weight_sum if weight_sum > 0 else 0.0
    
    def _jaccard_similarity(self, set1: Set, set2: Set) -> float:
        """Calculate Jaccard similarity between two sets"""
        
        if not set1 and not set2:
            return 1.0
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0
    
    async def _extract_mathematical_properties(self, function_data: Dict) -> Dict:
        """Extract mathematical properties from function"""
        
        properties = {}
        latex_formula = function_data.get('latex_formula', '')
        
        # Basic structure analysis
        structure = self._analyze_mathematical_structure(latex_formula)
        properties['structure'] = dict(structure)
        
        # Convert sets to lists for JSON serialization
        for key, value in properties['structure'].items():
            if isinstance(value, set):
                properties['structure'][key] = list(value)
        
        # Domain analysis
        properties['likely_domain'] = self._infer_domain(latex_formula)
        
        # Function type classification
        properties['function_type'] = self._classify_function_type(structure)
        
        # Complexity metrics
        properties['complexity_score'] = structure['complexity']
        properties['complexity_level'] = self._classify_complexity(structure['complexity'])
        
        return properties
    
    def _infer_domain(self, latex_formula: str) -> str:
        """Infer the likely domain of the function"""
        
        latex_lower = latex_formula.lower()
        
        if 'complex' in latex_lower or 'z' in latex_lower:
            return 'complex'
        elif any(trig in latex_lower for trig in ['sin', 'cos', 'tan']):
            return 'real_or_complex'
        elif '\\mathbb{n}' in latex_lower or 'n=' in latex_lower:
            return 'positive_integers'
        elif '\\mathbb{z}' in latex_lower:
            return 'integers'
        elif '\\mathbb{r}' in latex_lower:
            return 'real'
        else:
            return 'unknown'
    
    def _classify_function_type(self, structure: Dict) -> str:
        """Classify the type of mathematical function"""
        
        if 'infinite_product' in structure['patterns']:
            if any(trig in structure['functions'] for trig in ['sin', 'cos', 'tan']):
                return 'infinite_trigonometric_product'
            else:
                return 'infinite_product'
        elif 'infinite_sum' in structure['patterns']:
            return 'infinite_series'
        elif 'trigonometric' in structure['patterns']:
            return 'trigonometric_function'
        elif 'gamma' in structure['functions'] or 'zeta' in structure['functions']:
            return 'special_function'
        elif 'exp' in structure['functions'] or 'log' in structure['functions']:
            return 'transcendental_function'
        else:
            return 'general_function'
    
    def _classify_complexity(self, complexity_score: int) -> str:
        """Classify complexity level"""
        
        if complexity_score <= 5:
            return 'simple'
        elif complexity_score <= 15:
            return 'moderate'
        elif complexity_score <= 25:
            return 'complex'
        else:
            return 'very_complex'
    
    def _deduplicate_results(self, results: List[Dict]) -> List[Dict]:
        """Remove duplicate results"""
        
        seen = set()
        deduplicated = []
        
        for result in results:
            key = (result['database'], result['function_id'])
            if key not in seen:
                seen.add(key)
                deduplicated.append(result)
        
        # Sort by confidence score
        deduplicated.sort(key=lambda x: x['confidence'], reverse=True)
        
        return deduplicated
    
    def _calculate_confidence_score(self, duplicates: List, similar: List, methods: List) -> float:
        """Calculate overall confidence score for validation"""
        
        base_confidence = 0.5
        
        # Penalty for duplicates found
        if duplicates:
            base_confidence -= 0.4 * len(duplicates)
        
        # Penalty for similar functions
        if similar:
            similarity_penalty = sum(s['confidence'] for s in similar) / len(similar) * 0.2
            base_confidence -= similarity_penalty
        
        # Bonus for multiple validation methods
        method_bonus = len(methods) * 0.05
        base_confidence += method_bonus
        
        return max(0.0, min(1.0, base_confidence))
    
    def _determine_status(self, duplicates: List, similar: List) -> str:
        """Determine validation status"""
        
        if duplicates:
            return 'duplicate'
        elif similar and any(s['confidence'] > 0.8 for s in similar):
            return 'highly_similar'
        elif similar:
            return 'similar'
        else:
            return 'unique'
    
    def _generate_recommendations(self, duplicates: List, similar: List, status: str) -> List[str]:
        """Generate recommendations based on validation results"""
        
        recommendations = []
        
        if status == 'duplicate':
            recommendations.append("❌ DUPLICATE FUNCTION DETECTED")
            recommendations.append("🔍 This function already exists in the database")
            recommendations.append("⚠️ Do not proceed with registration")
            
            if duplicates:
                top_duplicate = duplicates[0]
                recommendations.append(f"📊 Duplicate found: {top_duplicate['name']} in {top_duplicate['database']}")
        
        elif status == 'highly_similar':
            recommendations.append("⚠️ HIGHLY SIMILAR FUNCTION DETECTED")
            recommendations.append("🔍 Review similar functions before proceeding")
            recommendations.append("💡 Consider if this is a meaningful variation")
            
            if similar:
                top_similar = similar[0]
                recommendations.append(f"📊 Most similar: {top_similar['name']} (confidence: {top_similar['confidence']:.2f})")
        
        elif status == 'similar':
            recommendations.append("ℹ️ SIMILAR FUNCTIONS FOUND")
            recommendations.append("🔍 Review for potential relationships")
            recommendations.append("✅ Proceed with caution")
        
        else:
            recommendations.append("✅ UNIQUE FUNCTION CONFIRMED")
            recommendations.append("🚀 This appears to be a novel mathematical discovery")
            recommendations.append("📝 Proceed with registration")
        
        return recommendations
    
    # Additional analysis methods for specific properties
    def _analyze_latex_hash(self, function_data: Dict) -> Dict:
        """Analyze LaTeX hash properties"""
        
        latex_formula = function_data.get('latex_formula', '')
        return {
            'hash': self._generate_latex_hash(latex_formula),
            'normalized_latex': self._normalize_latex(latex_formula)
        }
    
    def _analyze_normalized_latex(self, function_data: Dict) -> Dict:
        """Analyze normalized LaTeX properties"""
        
        latex_formula = function_data.get('latex_formula', '')
        normalized = self._normalize_latex(latex_formula)
        
        return {
            'original_length': len(latex_formula),
            'normalized_length': len(normalized),
            'compression_ratio': len(normalized) / len(latex_formula) if latex_formula else 0,
            'token_count': len(normalized.split())
        }
    
    def _analyze_symbolic_equivalence(self, function_data: Dict) -> Dict:
        """Analyze symbolic equivalence properties"""
        
        if not SYMPY_AVAILABLE:
            return {'available': False}
        
        latex_formula = function_data.get('latex_formula', '')
        
        try:
            expr = parse_latex(latex_formula)
            simplified = simplify(expr)
            
            return {
                'available': True,
                'parseable': True,
                'symbols_count': len(expr.free_symbols),
                'symbols': [str(s) for s in expr.free_symbols],
                'atoms_count': len(expr.atoms()),
                'simplified_form': str(simplified)
            }
        
        except Exception as e:
            return {
                'available': True,
                'parseable': False,
                'error': str(e)
            }
    
    def _analyze_structural_similarity(self, function_data: Dict) -> Dict:
        """Analyze structural similarity properties"""
        
        latex_formula = function_data.get('latex_formula', '')
        structure = self._analyze_mathematical_structure(latex_formula)
        
        # Convert sets to lists for JSON serialization
        serializable_structure = {}
        for key, value in structure.items():
            if isinstance(value, set):
                serializable_structure[key] = list(value)
            else:
                serializable_structure[key] = value
        
        return serializable_structure
    
    def _analyze_mathematical_properties(self, function_data: Dict) -> Dict:
        """Analyze general mathematical properties"""
        
        latex_formula = function_data.get('latex_formula', '')
        
        properties = {
            'has_infinite_operations': any(op in latex_formula.lower() for op in ['\\sum', '\\prod', '\\int']),
            'has_trigonometric': any(trig in latex_formula.lower() for trig in ['\\sin', '\\cos', '\\tan']),
            'has_exponential': any(exp in latex_formula.lower() for exp in ['\\exp', 'e^']),
            'has_logarithmic': any(log in latex_formula.lower() for log in ['\\log', '\\ln']),
            'has_special_functions': any(sf in latex_formula.lower() for sf in ['\\gamma', '\\zeta', '\\eta']),
            'character_count': len(latex_formula),
            'estimated_computational_complexity': self._estimate_computational_complexity(latex_formula)
        }
        
        return properties
    
    def _analyze_coefficient_patterns(self, function_data: Dict) -> Dict:
        """Analyze coefficient patterns in the function"""
        
        latex_formula = function_data.get('latex_formula', '')
        
        # Extract numeric patterns
        import re
        
        # Find numbers in the LaTeX
        numbers = re.findall(r'\d+\.?\d*', latex_formula)
        fractions = re.findall(r'\\frac\{([^}]+)\}\{([^}]+)\}', latex_formula)
        
        return {
            'numeric_coefficients': numbers,
            'fraction_count': len(fractions),
            'has_pi': '\\pi' in latex_formula.lower(),
            'has_e': 'e' in latex_formula.lower() or '\\exp' in latex_formula.lower(),
            'coefficient_patterns': self._identify_coefficient_patterns(numbers)
        }
    
    def _estimate_computational_complexity(self, latex_formula: str) -> str:
        """Estimate computational complexity of the function"""
        
        complexity_score = 0
        latex_lower = latex_formula.lower()
        
        # Add complexity for different operations
        if '\\prod' in latex_lower and '\\infty' in latex_lower:
            complexity_score += 10  # Infinite product
        if '\\sum' in latex_lower and '\\infty' in latex_lower:
            complexity_score += 8   # Infinite sum
        if '\\int' in latex_lower:
            complexity_score += 6   # Integration
        
        # Add complexity for special functions
        special_functions = ['\\gamma', '\\zeta', '\\eta', '\\sin', '\\cos', '\\tan']
        complexity_score += sum(2 for sf in special_functions if sf in latex_lower)
        
        # Classify complexity
        if complexity_score <= 5:
            return 'low'
        elif complexity_score <= 15:
            return 'medium'
        elif complexity_score <= 25:
            return 'high'
        else:
            return 'very_high'
    
    def _identify_coefficient_patterns(self, numbers: List[str]) -> List[str]:
        """Identify patterns in numeric coefficients"""
        
        if not numbers:
            return []
        
        patterns = []
        
        # Convert to floats for analysis
        try:
            numeric_values = [float(n) for n in numbers]
            
            # Check for common mathematical constants (approximate)
            constants = {
                3.14159: 'pi',
                2.71828: 'e',
                1.41421: 'sqrt_2',
                1.73205: 'sqrt_3',
                0.57721: 'euler_gamma'
            }
            
            for value in numeric_values:
                for const_val, const_name in constants.items():
                    if abs(value - const_val) < 0.01:
                        patterns.append(f'contains_{const_name}')
            
            # Check for integer sequences
            if all(v.is_integer() for v in numeric_values):
                patterns.append('integer_coefficients')
            
            # Check for fractional patterns
            if any(0 < v < 1 for v in numeric_values):
                patterns.append('fractional_coefficients')
        
        except ValueError:
            patterns.append('non_numeric_coefficients')
        
        return patterns


# AI Tool Interface
class AIFunctionValidatorTool:
    """
    AI tool interface for mathematical function validation.
    Designed for integration with AI discovery agents.
    """
    
    def __init__(self):
        self.validator = MathematicalFunctionValidator()
        print("✅ AI Function Validator Tool initialized")
    
    async def validate_new_function(self, function_data: Dict) -> Dict:
        """
        AI tool interface for validating new functions
        
        Args:
            function_data: Dictionary with function information
            
        Returns:
            Dictionary with validation results formatted for AI consumption
        """
        
        validation_result = await self.validator.validate_function_uniqueness(function_data)
        
        # Format for AI consumption
        ai_result = {
            'validation_status': validation_result.status,
            'is_unique': validation_result.is_unique,
            'confidence_score': validation_result.confidence_score,
            'should_proceed': validation_result.status in ['unique', 'similar'],
            'requires_human_review': validation_result.status in ['highly_similar', 'duplicate'],
            'duplicate_count': len(validation_result.duplicate_functions),
            'similar_count': len(validation_result.similar_functions),
            'recommendations': validation_result.recommendations,
            'mathematical_properties': validation_result.mathematical_properties,
            'validation_methods_used': validation_result.validation_methods,
            'detailed_results': {
                'duplicates': validation_result.duplicate_functions,
                'similar': validation_result.similar_functions
            }
        }
        
        return ai_result
    
    async def batch_validate_functions(self, functions_list: List[Dict]) -> List[Dict]:
        """Validate multiple functions in batch"""
        
        results = []
        
        for i, function_data in enumerate(functions_list):
            print(f"🔍 Validating function {i+1}/{len(functions_list)}: {function_data.get('name', 'unnamed')}")
            
            result = await self.validate_new_function(function_data)
            result['batch_index'] = i
            result['function_data'] = function_data
            
            results.append(result)
        
        return results


# Example usage and testing
async def main():
    """Example usage of the Mathematical Function Validator"""
    
    print("🧪 Testing Mathematical Function Validator")
    print("=" * 50)
    
    # Test function
    test_function = {
        'name': 'test_infinite_product',
        'latex_formula': r'\prod_{n=1}^{\infty} \sin\left(\frac{\pi z}{n}\right)',
        'description': 'Test infinite product function',
        'category': 'test_functions',
        'properties': {
            'domain': 'complex',
            'type': 'infinite_product'
        }
    }
    
    # Initialize validator
    validator_tool = AIFunctionValidatorTool()
    
    # Validate function
    result = await validator_tool.validate_new_function(test_function)
    
    print("\n🔍 Validation Results:")
    print(f"   Status: {result['validation_status']}")
    print(f"   Is Unique: {result['is_unique']}")
    print(f"   Confidence: {result['confidence_score']:.3f}")
    print(f"   Should Proceed: {result['should_proceed']}")
    print(f"   Duplicates Found: {result['duplicate_count']}")
    print(f"   Similar Functions: {result['similar_count']}")
    
    print("\n💡 Recommendations:")
    for rec in result['recommendations']:
        print(f"   {rec}")
    
    print("\n✅ Mathematical Function Validator test complete!")


if __name__ == "__main__":
    asyncio.run(main())