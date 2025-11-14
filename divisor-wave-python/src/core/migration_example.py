
# Example: How to update your main.py to use the unified registry

# BEFORE (scattered function management):
# special_functions = SpecialFunctionsLibrary()
# plotter_2d = PlottingMethods("2D")
# plotter_3d = PlottingMethods("3D")

# AFTER (unified registry):
from core.registry_adapter import integrate_with_existing_system

special_functions = SpecialFunctionsLibrary()
plotter_2d = PlottingMethods("2D")
plotter_3d = PlottingMethods("3D")

# Single line to upgrade entire system to unified registry
adapter = integrate_with_existing_system(
    special_functions=special_functions,
    plotting_methods=plotter_2d,
    api_app=app
)

# Now all function mappings are managed centrally!
# - No more scattered JSON files to maintain
# - Automatic consistency across all components  
# - Easy addition of new functions
# - Built-in validation and documentation

# Optional: Access the registry directly
registry = adapter.registry

# Add a new custom function
new_func_id = registry.add_custom_function(
    name="my_custom_function",
    latex_formula="f(z) = z^3 + 1", 
    description="My custom mathematical function",
    category="User Functions"
)

# Search functions
prime_functions = registry.search_functions("prime")
riemann_functions = registry.search_functions("riemann", filters={'category': 'Prime Indicators'})

# Get comprehensive documentation
docs = adapter.create_function_documentation()
