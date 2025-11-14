"""
Registry Integration Adapter
Seamlessly integrates the new FunctionRegistry with existing system components
without breaking backward compatibility

This adapter provides:
- Transparent replacement of scattered function mappings
- Automatic synchronization between registry and legacy components  
- Migration utilities for existing data
- Plugin architecture for extending functionality

11/6/2025 - Integration layer for unified function management
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from dataclasses import asdict
import json

# Import the new unified registry  
try:
    from .function_registry import FunctionRegistry, get_registry
except ImportError:
    from function_registry import FunctionRegistry, get_registry

class RegistryAdapter:
    """
    Adapter that makes the unified registry compatible with existing system components
    Provides drop-in replacement for scattered function mappings
    """
    
    def __init__(self):
        self.registry = get_registry()
        self._legacy_special_functions = None
        self._legacy_plotter = None
        
    def setup_special_functions_integration(self, special_functions_instance):
        """Integrate registry with SpecialFunctionsLibrary"""
        self._legacy_special_functions = special_functions_instance
        
        # Replace lambda function library with registry-based version
        original_lamda_function_library = special_functions_instance.lamda_function_library
        
        def enhanced_lamda_function_library(normalize_type='N', catalog_only=False):
            if catalog_only:
                # Return registry-based catalog
                return self.registry.get_lambda_catalog()
            
            # Return lambda functions that call registry-mapped implementations
            operations = {}
            for func_id, func_def in self.registry.functions.items():
                if hasattr(special_functions_instance, func_def.python_implementation):
                    method = getattr(special_functions_instance, func_def.python_implementation)
                    operations[func_id] = lambda z, m=method: m(z, normalize_type)
                else:
                    # For custom functions, create a wrapper
                    operations[func_id] = lambda z: self._evaluate_custom_function(func_def, z, normalize_type)
            
            return operations
        
        # Replace the method
        special_functions_instance.lamda_function_library = enhanced_lamda_function_library
        
        # Enhance get_available_functions with registry data
        def enhanced_get_available_functions():
            return self.registry.export_for_component('api_functions')
            
        special_functions_instance.get_available_functions = enhanced_get_available_functions
        
    def setup_plotting_integration(self, plotting_instance):
        """Integrate registry with PlottingMethods"""
        self._legacy_plotter = plotting_instance
        
        # Replace LaTeX formula loading with registry-based version
        def enhanced_get_function_latex(function_name, normalize_type='N'):
            func_def = self.registry.get_function(function_name)
            if func_def and func_def.latex_formula:
                return func_def.latex_formula
            
            # Fallback to legacy method if available
            if hasattr(plotting_instance, '_original_get_function_latex'):
                return plotting_instance._original_get_function_latex(function_name, normalize_type)
            
            return f"\\text{{{function_name}}}"
        
        # Backup original method and replace
        plotting_instance._original_get_function_latex = getattr(plotting_instance, 'get_function_latex', None)
        plotting_instance.get_function_latex = enhanced_get_function_latex
    
    def setup_api_integration(self, api_app):
        """Integrate registry with FastAPI application"""
        # Add new registry endpoints
        @api_app.get("/registry/functions")
        async def get_registry_functions():
            """Get all functions from unified registry"""
            return self.registry.export_for_component('frontend_dropdown')
        
        @api_app.get("/registry/stats")
        async def get_registry_stats():
            """Get registry statistics"""
            return self.registry.get_stats()
        
        @api_app.post("/registry/functions")
        async def add_registry_function(func_data: dict):
            """Add new function to registry"""
            try:
                custom_id = self.registry.add_custom_function(
                    name=func_data['name'],
                    latex_formula=func_data.get('latex_formula', ''),
                    description=func_data.get('description', ''),
                    category=func_data.get('category', 'Custom'),
                    python_code=func_data.get('python_code', '')
                )
                
                # Sync with legacy files
                self.registry.sync_legacy_files()
                
                return {"success": True, "function_id": custom_id}
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        @api_app.get("/registry/search")
        async def search_registry_functions(q: str, category: str = None, source: str = None):
            """Search functions in registry"""
            filters = {}
            if category:
                filters['category'] = category
            if source:
                filters['source'] = source
                
            results = self.registry.search_functions(q, filters)
            return [
                {
                    'id': func.id,
                    'name': func.name,
                    'display_name': func.display_name,
                    'description': func.description,
                    'category': func.category,
                    'latex_formula': func.latex_formula,
                    'tags': func.tags
                }
                for func in results
            ]
            
        # Enhanced LaTeX formula endpoint
        @api_app.get("/registry/latex/formula/{identifier}")
        async def get_registry_latex_formula(identifier: str, normalize_type: str = 'N'):
            """Get LaTeX formula using registry"""
            func_def = self.registry.get_function(identifier)
            if func_def:
                return {
                    "function_name": identifier,
                    "mapped_function_name": func_def.name,
                    "formula": func_def.latex_formula,
                    "description": func_def.description,
                    "category": func_def.category
                }
            else:
                return {"error": "Function not found"}
    
    def migrate_legacy_data(self):
        """Migrate data from legacy system to registry"""
        print("Migrating legacy data to unified registry...")
        
        # Migration is handled automatically during registry initialization
        # But we can trigger explicit sync here
        self.registry.sync_legacy_files()
        
        print("Legacy data migration completed")
        
    def _evaluate_custom_function(self, func_def, z, normalize_type):
        """Evaluate a custom function"""
        try:
            # This would execute custom Python code
            # For now, return a placeholder
            return 1.0
        except Exception as e:
            print(f"Error evaluating custom function {func_def.name}: {e}")
            return 0.0
    
    def validate_system_consistency(self) -> Dict[str, Any]:
        """Validate that all system components are consistent with registry"""
        issues = []
        
        # Check if all registry functions exist in special functions library
        if self._legacy_special_functions:
            for func_def in self.registry.functions.values():
                if (func_def.source == 'builtin' and 
                    not hasattr(self._legacy_special_functions, func_def.python_implementation)):
                    issues.append(f"Missing implementation: {func_def.python_implementation}")
        
        # Check for missing LaTeX formulas
        missing_latex = [f.name for f in self.registry.functions.values() if not f.latex_formula]
        if missing_latex:
            issues.append(f"Missing LaTeX formulas: {missing_latex}")
        
        # Check for duplicate function names
        names = [f.name for f in self.registry.functions.values()]
        duplicates = [name for name in set(names) if names.count(name) > 1]
        if duplicates:
            issues.append(f"Duplicate function names: {duplicates}")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "total_functions": len(self.registry.functions),
            "function_count_by_source": {
                source: len([f for f in self.registry.functions.values() if f.source == source])
                for source in set(f.source for f in self.registry.functions.values())
            }
        }
    
    def create_function_documentation(self) -> Dict[str, Any]:
        """Generate comprehensive function documentation from registry"""
        categories = self.registry.get_functions_by_category()
        documentation = {}
        
        for category, functions in categories.items():
            documentation[category] = []
            for func_def in functions:
                doc_entry = {
                    'id': func_def.id,
                    'name': func_def.name,
                    'display_name': func_def.display_name,
                    'description': func_def.description,
                    'latex_formula': func_def.latex_formula,
                    'python_implementation': func_def.python_implementation,
                    'dependencies': func_def.dependencies,
                    'tags': func_def.tags,
                    'normalization_modes': func_def.normalization_modes,
                    'author': func_def.author,
                    'created_at': func_def.created_at,
                    'updated_at': func_def.updated_at
                }
                documentation[category].append(doc_entry)
        
        return documentation
    
    def export_for_external_tools(self, format_type: str = 'json') -> Union[str, Dict]:
        """Export registry data for external tools and documentation"""
        if format_type == 'json':
            return {
                'metadata': {
                    'version': '1.0.0',
                    'generated_at': self.registry.functions.get('1', None).updated_at if self.registry.functions else None,
                    'total_functions': len(self.registry.functions)
                },
                'functions': [asdict(func) for func in self.registry.functions.values()]
            }
        elif format_type == 'markdown':
            return self._generate_markdown_documentation()
        elif format_type == 'latex_table':
            return self._generate_latex_table()
        
        return {}
    
    def _generate_markdown_documentation(self) -> str:
        """Generate Markdown documentation"""
        categories = self.registry.get_functions_by_category()
        markdown = "# Divisor Wave Function Registry\n\n"
        
        for category, functions in categories.items():
            markdown += f"## {category}\n\n"
            for func in functions:
                markdown += f"### {func.display_name} (ID: {func.id})\n\n"
                markdown += f"**Description:** {func.description}\n\n"
                if func.latex_formula:
                    markdown += f"**Formula:** ${func.latex_formula}$\n\n"
                if func.dependencies:
                    markdown += f"**Dependencies:** {', '.join(func.dependencies)}\n\n"
                if func.tags:
                    markdown += f"**Tags:** {', '.join(func.tags)}\n\n"
                markdown += "---\n\n"
        
        return markdown
    
    def _generate_latex_table(self) -> str:
        """Generate LaTeX table of all functions"""
        latex = "\\begin{longtable}{|l|l|l|l|}\n"
        latex += "\\hline\n"
        latex += "\\textbf{ID} & \\textbf{Name} & \\textbf{Category} & \\textbf{Formula} \\\\\n"
        latex += "\\hline\n"
        latex += "\\endhead\n"
        
        for func in self.registry.functions.values():
            name = func.display_name.replace('_', '\\_')
            category = func.category.replace('_', '\\_')
            formula = func.latex_formula.replace('\\', '\\\\') if func.latex_formula else 'N/A'
            
            latex += f"{func.id} & {name} & {category} & ${formula}$ \\\\\n"
            latex += "\\hline\n"
        
        latex += "\\end{longtable}\n"
        return latex


class LegacyCompatibilityLayer:
    """
    Provides exact backward compatibility for existing code
    Maps old scattered function calls to new unified registry
    """
    
    def __init__(self, adapter: RegistryAdapter):
        self.adapter = adapter
        self.registry = adapter.registry
    
    def get_divisor_wave_formulas(self) -> Dict[str, Any]:
        """Legacy interface for divisor_wave_formulas.json"""
        return self.registry.export_for_component('latex_formulas')
    
    def get_custom_functions(self) -> Dict[str, Any]:
        """Legacy interface for custom_functions.json"""
        custom_funcs = {f.name: f for f in self.registry.functions.values() if f.source == 'custom'}
        return {
            'functions': {name: asdict(func) for name, func in custom_funcs.items()},
            'metadata': {
                'version': '1.0',
                'count': len(custom_funcs)
            }
        }
    
    def get_lambda_catalog(self, normalize_type: str = 'N') -> Dict[str, callable]:
        """Legacy interface for lambda function catalog"""
        return self.registry.get_lambda_catalog()
    
    def get_api_function_mappings(self) -> Dict[str, str]:
        """Legacy interface for API function ID mappings"""
        return self.registry.get_api_mappings()


# Global adapter instance for easy integration
_adapter = None

def get_adapter() -> RegistryAdapter:
    """Get the global registry adapter instance"""
    global _adapter
    if _adapter is None:
        _adapter = RegistryAdapter()
    return _adapter

def integrate_with_existing_system(special_functions=None, plotting_methods=None, api_app=None):
    """
    One-command integration with existing system
    Call this function to seamlessly upgrade to unified registry
    """
    adapter = get_adapter()
    
    print("Integrating unified function registry...")
    
    if special_functions:
        adapter.setup_special_functions_integration(special_functions)
        print("✓ SpecialFunctionsLibrary integrated")
    
    if plotting_methods:
        adapter.setup_plotting_integration(plotting_methods)
        print("✓ PlottingMethods integrated")
    
    if api_app:
        adapter.setup_api_integration(api_app)
        print("✓ FastAPI endpoints enhanced")
    
    # Migrate legacy data
    adapter.migrate_legacy_data()
    print("✓ Legacy data migrated")
    
    # Validate system consistency
    validation = adapter.validate_system_consistency()
    if validation['valid']:
        print("✓ System validation passed")
    else:
        print(f"⚠ Validation issues found: {validation['issues']}")
    
    print(f"Integration complete! Managing {validation['total_functions']} functions")
    return adapter


# Usage example for existing main.py
def upgrade_main_py():
    """
    Example of how to upgrade main.py with minimal changes
    """
    # In main.py, replace this:
    # special_functions = SpecialFunctionsLibrary()
    # plotter_2d = PlottingMethods("2D") 
    # plotter_3d = PlottingMethods("3D")
    
    # With this:
    """
    from core.registry_adapter import integrate_with_existing_system
    
    special_functions = SpecialFunctionsLibrary()
    plotter_2d = PlottingMethods("2D")
    plotter_3d = PlottingMethods("3D")
    
    # Single line to upgrade entire system
    adapter = integrate_with_existing_system(
        special_functions=special_functions,
        plotting_methods=plotter_2d,  # or both 2D and 3D
        api_app=app
    )
    """
    pass


if __name__ == "__main__":
    # Test the integration system
    adapter = RegistryAdapter()
    
    # Generate documentation
    docs = adapter.create_function_documentation()
    print(f"Generated documentation for {len(docs)} categories")
    
    # Export for external tools
    json_export = adapter.export_for_external_tools('json')
    print(f"JSON export contains {len(json_export.get('functions', []))} functions")
    
    # Validate system
    validation = adapter.validate_system_consistency()
    print(f"System validation: {'PASSED' if validation['valid'] else 'FAILED'}")
    if not validation['valid']:
        for issue in validation['issues']:
            print(f"  - {issue}")