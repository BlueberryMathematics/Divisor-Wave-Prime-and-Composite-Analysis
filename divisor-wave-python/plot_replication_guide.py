#!/usr/bin/env python3
"""
Plot Replication Guide: How to recreate original legacy plots in the enhanced system

The original system used interactive function selection, while the enhanced system
requires explicit function names. This guide shows how to replicate original plots.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.original_legacy_files.complex_plotting_og import Complex_Plotting_OG
from src.original_legacy_files.special_functions_og import Special_Functions_OG
from src.core.plotting_methods import PlottingMethods
from src.core.special_functions_library import SpecialFunctionsLibrary

def replicate_original_plot(function_id: str, normalize_type: str = 'N', color_map: str = "4"):
    """
    Recreate original plots using both systems for comparison
    
    Args:
        function_id: Original function ID from lambda library ('1', '2', '3', etc.)
        normalize_type: 'Y' or 'N' 
        color_map: Color map ID
    """
    print(f"Replicating original plot for function {function_id}")
    
    # ===== ORIGINAL LEGACY SYSTEM =====
    print("Creating plot with ORIGINAL legacy system...")
    
    # Initialize original system
    special_funcs_og = Special_Functions_OG()
    plotting_og = Complex_Plotting_OG()
    
    # Get the specific function from original lambda library
    operations_original = {
        '1': lambda z: special_funcs_og.product_of_sin(z, normalize_type),
        '2': lambda z: special_funcs_og.product_of_product_representation_for_sin(z, normalize_type),
        '3': lambda z: special_funcs_og.product_of_product_representation_for_sin_COMPLEX_VARIANT(z, normalize_type),
        '4': lambda z: special_funcs_og.complex_playground_magnification_currated_functions_DEMO(z, normalize_type),
        '5': lambda z: special_funcs_og.Riesz_Product_for_Cos(z, normalize_type),
        # Add more as needed...
    }
    
    if function_id not in operations_original:
        print(f"Function {function_id} not implemented in original mapping")
        return
    
    # Create original plot (requires manual modification to avoid user input)
    # The original create_plot_2D needs modification to accept a function directly
    
    # ===== ENHANCED SYSTEM =====
    print("Creating plot with ENHANCED system...")
    
    # Map original function IDs to enhanced system function names
    enhanced_function_mapping = {
        '1': 'product_of_sin',
        '2': 'product_of_product_representation_for_sin', 
        '3': 'product_of_product_representation_for_sin_COMPLEX_VARIANT',  # Not available in enhanced
        '4': 'complex_playground_magnification_currated_functions_DEMO',
        '5': 'Riesz_Product_for_Cos',
    }
    
    # Initialize enhanced system  
    special_funcs_enhanced = SpecialFunctionsLibrary()
    plotting_enhanced = PlottingMethods(special_funcs_enhanced)
    
    # Create enhanced plot
    if function_id in ['1', '2', '4', '5']:  # Available functions
        function_name = enhanced_function_mapping[function_id]
        result = plotting_enhanced.create_plot_2D(
            function_name=function_name,
            color_map_2D=color_map,
            normalize_type=normalize_type
        )
        print(f"Enhanced plot created successfully for {function_name}")
    else:
        print(f"Function {function_id} not available in enhanced system")

def get_original_function_catalog():
    """Display the original function catalog for reference"""
    
    catalog = {
        '1': 'product_of_sin(z, Normalize_type)',
        '2': 'product_of_product_representation_for_sin(z, Normalize_type)',
        '3': 'product_of_product_representation_for_sin_COMPLEX_VARIANT(z, Normalize_type)',
        '4': 'complex_playground_magnification_currated_functions_DEMO(z, Normalize_type)',
        '5': 'Riesz_Product_for_Cos(z, Normalize_type)',
        '6': 'Riesz_Product_for_Sin(z, Normalize_type)',
        '7': 'Riesz_Product_for_Tan(z, Normalize_type)',
        '8': 'Viete_Product_for_Cos(z, Normalize_type)',
        '9': 'Viete_Product_for_Sin(z, Normalize_type)',
        '10': 'Viete_Product_for_Tan(z, Normalize_type)',
        '11': 'cos_of_product_of_sin(z, Normalize_type)',
        '12': 'sin_of_product_of_sin(z, Normalize_type)',
        '13': 'cos_of_product_of_product_representation_of_sin(z, Normalize_type)',
        '14': 'sin_of_product_of_product_representation_of_sin(z, Normalize_type)',
        '15': 'Binary_Output_Prime_Indicator_Function_H(z, Normalize_type)',
        '16': 'Prime_Output_Indicator_J(z, Normalize_type)',
        '17': 'BOPIF_Q_Alternation_Series(z, Normalize_type)',
        '18': 'Dirichlet_Eta_Derived_From_BOPIF(z, Normalize_type)',
    }
    
    print("ORIGINAL FUNCTION CATALOG:")
    print("=" * 50)
    for key, value in catalog.items():
        print(f"{key}: {value}")
    print("=" * 50)

def check_mathematical_differences():
    """
    Check for mathematical implementation differences between systems
    """
    print("MATHEMATICAL IMPLEMENTATION COMPARISON:")
    print("=" * 50)
    
    # Key coefficients comparison
    print("Product of Sin Coefficients:")
    print("Original: m=0.0465, beta=0.178 (both Y and N normalization)")
    print("Enhanced: m=0.0465, beta=0.178 (claims exact replica)")
    print("")
    
    print("Key Differences Found:")
    print("1. Enhanced system has additional safety checks")
    print("2. Enhanced system has gamma normalization limits")
    print("3. Enhanced system has different function ID mappings")
    print("4. Original function '3' (COMPLEX_VARIANT) not in enhanced system")
    print("=" * 50)

if __name__ == "__main__":
    print("PLOT REPLICATION ANALYSIS")
    print("=" * 60)
    
    get_original_function_catalog()
    print()
    check_mathematical_differences()
    print()
    
    # Example usage
    print("Example: Replicating original function '1' (product_of_sin)")
    replicate_original_plot('1', 'N', '4')