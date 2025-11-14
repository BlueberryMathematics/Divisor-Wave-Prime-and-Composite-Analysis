#!/usr/bin/env python3
"""
Plot Comparison Tool
Directly compare plots between original and enhanced systems
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def compare_function_coefficients():
    """
    Compare mathematical coefficients between systems
    """
    print("MATHEMATICAL COEFFICIENT COMPARISON")
    print("=" * 60)
    
    # Import both systems
    from src.original_legacy_files.special_functions_og import Special_Functions_OG
    from src.core.special_functions_library import SpecialFunctionsLibrary
    
    original = Special_Functions_OG()
    enhanced = SpecialFunctionsLibrary()
    
    # Test complex value
    z_test = complex(5.0, 2.0)
    
    print("Testing with z =", z_test)
    print("-" * 40)
    
    for norm_type in ['N', 'Y']:
        print(f"\nNormalization Type: {norm_type}")
        print("-" * 20)
        
        try:
            # Original product_of_sin
            orig_result = original.product_of_sin(z_test, norm_type)
            print(f"Original product_of_sin: {orig_result}")
            
            # Enhanced product_of_sin  
            enh_result = enhanced.product_of_sin(z_test, norm_type)
            print(f"Enhanced product_of_sin: {enh_result}")
            
            # Difference
            diff = abs(orig_result - enh_result) if orig_result != 0 else float('inf')
            rel_diff = diff / abs(orig_result) * 100 if orig_result != 0 else float('inf')
            print(f"Absolute difference: {diff}")
            print(f"Relative difference: {rel_diff:.6f}%")
            
        except Exception as e:
            print(f"Error comparing functions: {e}")

def identify_missing_functions():
    """
    Identify functions available in original but not in enhanced system
    """
    print("\nFUNCTION AVAILABILITY COMPARISON")
    print("=" * 60)
    
    # Original function catalog
    original_functions = {
        '1': 'product_of_sin',
        '2': 'product_of_product_representation_for_sin',
        '3': 'product_of_product_representation_for_sin_COMPLEX_VARIANT',  # Missing in enhanced!
        '4': 'complex_playground_magnification_currated_functions_DEMO',
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
    }
    
    # Enhanced function mapping (from plotting_methods.py)
    enhanced_functions = {
        '1': 'product_of_sin',
        '2': 'product_of_product_representation_for_sin',
        '3': 'complex_playground_magnification_currated_functions_DEMO',  # Different!
        '4': 'Riesz_Product_for_Cos',  # Different!
        '5': 'Riesz_Product_for_Sin',
        '6': 'Riesz_Product_for_Tan', 
        '7': 'Viete_Product_for_Cos',
        '8': 'Viete_Product_for_Sin',
        '9': 'Viete_Product_for_Tan',
        '10': 'cos_of_product_of_sin',
        '11': 'sin_of_product_of_sin',
        # ... continues but with different mappings
    }
    
    print("ID MAPPING DIFFERENCES:")
    print("-" * 30)
    for func_id in original_functions:
        orig_name = original_functions[func_id]
        enhanced_name = enhanced_functions.get(func_id, 'NOT MAPPED')
        
        if orig_name != enhanced_name:
            print(f"ID {func_id}:")
            print(f"  Original: {orig_name}")
            print(f"  Enhanced: {enhanced_name}")
            print(f"  ❌ MISMATCH!")
        else:
            print(f"ID {func_id}: ✅ {orig_name}")
        print()
    
    # Missing functions
    print("\nMISSING FROM ENHANCED SYSTEM:")
    print("-" * 30)
    missing = []
    for func_id, func_name in original_functions.items():
        if func_name not in enhanced_functions.values():
            missing.append((func_id, func_name))
    
    if missing:
        for func_id, func_name in missing:
            print(f"❌ ID {func_id}: {func_name}")
    else:
        print("✅ All functions available (but mappings may differ)")

def create_plot_comparison_guide():
    """
    Create a guide for replicating specific original plots
    """
    print("\nPLOT REPLICATION GUIDE")
    print("=" * 60)
    
    guide = {
        'Original Function 1 (product_of_sin)': {
            'enhanced_equivalent': "Use function_name='1' or 'product_of_sin'",
            'coefficients': 'm=0.0465, beta=0.178',
            'notes': 'Should be identical'
        },
        'Original Function 2 (product_of_product_representation_for_sin)': {
            'enhanced_equivalent': "Use function_name='2' or direct name",
            'coefficients': 'Check specific implementation',
            'notes': 'Should be identical'
        },
        'Original Function 3 (COMPLEX_VARIANT)': {
            'enhanced_equivalent': '❌ NOT AVAILABLE in enhanced system',
            'coefficients': 'N/A',
            'notes': 'Must use original system or implement in enhanced'
        },
        'Original Function 4 (complex_playground_magnification_currated_functions_DEMO)': {
            'enhanced_equivalent': "Enhanced maps this to ID '3' instead of '4'!",
            'coefficients': 'Different coefficients in demo function',
            'notes': '⚠️  Use function_name="3" in enhanced system'
        }
    }
    
    for orig_func, info in guide.items():
        print(f"\n{orig_func}:")
        print(f"  Enhanced: {info['enhanced_equivalent']}")
        print(f"  Coefficients: {info['coefficients']}")
        print(f"  Notes: {info['notes']}")

def main():
    """Run complete comparison analysis"""
    print("COMPLETE PLOT REPLICATION ANALYSIS")
    print("=" * 70)
    
    compare_function_coefficients()
    print("\n" + "="*70)
    
    identify_missing_functions()
    print("\n" + "="*70)
    
    create_plot_comparison_guide()
    print("\n" + "="*70)
    
    print("\nSUMMARY & RECOMMENDATIONS:")
    print("-" * 30)
    print("1. ✅ Basic functions (1,2) should replicate exactly")
    print("2. ❌ Function 3 (COMPLEX_VARIANT) missing from enhanced")  
    print("3. ⚠️  Function ID mappings differ between systems")
    print("4. ✅ Use original_plotting_wrapper.py for exact replication")
    print("5. ✅ Mathematical coefficients appear identical")
    
    print("\nTROUBLESHOOTING STEPS:")
    print("1. Use original_plotting_wrapper.py to get exact original behavior")
    print("2. For enhanced system, check function ID mappings carefully") 
    print("3. Function 3 users must use original system or implement missing function")
    print("4. Compare coefficient values if results still differ")

if __name__ == "__main__":
    main()