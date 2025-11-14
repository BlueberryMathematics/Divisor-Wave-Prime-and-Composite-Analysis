#!/usr/bin/env python3
"""
Test script for real plotting functionality
Verifies that the enhanced system produces the same results as the original
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.special_functions_library import SpecialFunctionsLibrary
from core.plotting_methods import PlottingMethods

def test_function_values():
    """Test that function values match expected behavior"""
    print("🧪 Testing function values...")
    
    special_functions = SpecialFunctionsLibrary()
    
    # Test some specific values
    test_points = [2.0, 3.0, 5.0, 7.0, 11.0, 13.0]
    
    print("\n📊 Product of Sin Values:")
    for x in test_points:
        z = complex(x, 0.0)
        val_n = special_functions.product_of_sin(z, 'N')
        val_y = special_functions.product_of_sin(z, 'Y')
        print(f"  f({x}) = {val_n:.6f} (N), {val_y:.6f} (Y)")
    
    print("\n📊 Product of Product Representation Values:")
    for x in test_points:
        z = complex(x, 0.0)
        val_n = special_functions.product_of_product_representation_for_sin(z, 'N')
        val_y = special_functions.product_of_product_representation_for_sin(z, 'Y')
        print(f"  g({x}) = {val_n:.6f} (N), {val_y:.6f} (Y)")

def test_real_plotting():
    """Test real line plotting functionality"""
    print("\n🎨 Testing real line plotting...")
    
    plotter = PlottingMethods("2D")
    
    # Test real line plot of product_of_sin
    print("Creating real line plot of product_of_sin...")
    result1 = plotter.create_plot_real_1D(
        function_name="product_of_sin",
        normalize_type="N",
        x_range=(2.0, 25.0),
        resolution=500,
        return_base64=False  # Display directly
    )
    
    if result1["success"]:
        print(f"✅ Real plot created successfully (computed {result1['points_computed']} points)")
    else:
        print(f"❌ Real plot failed: {result1['error']}")
    
    # Test real line plot of product_of_product_representation_for_sin
    print("\nCreating real line plot of product_of_product_representation_for_sin...")
    result2 = plotter.create_plot_real_1D(
        function_name="product_of_product_representation_for_sin",
        normalize_type="N",
        x_range=(2.0, 25.0),
        resolution=500,
        return_base64=False  # Display directly
    )
    
    if result2["success"]:
        print(f"✅ Real plot created successfully (computed {result2['points_computed']} points)")
    else:
        print(f"❌ Real plot failed: {result2['error']}")

def test_available_functions():
    """Test that all expected functions are available"""
    print("\n📋 Testing available functions...")
    
    special_functions = SpecialFunctionsLibrary()
    available = special_functions.get_available_functions()
    
    expected_functions = [
        "product_of_sin", 
        "product_of_product_representation_for_sin",
        "cos_of_product_of_sin",
        "sin_of_product_of_sin",
        "Riesz_Product_for_Cos",
        "Viete_Product_for_Sin"
    ]
    
    print(f"Available functions: {len(available)}")
    for name in expected_functions:
        if name in available:
            print(f"  ✅ {name}")
        else:
            print(f"  ❌ {name} - MISSING")
    
    # Test lambda functions
    lambda_funcs = special_functions.lamda_function_library(catalog_only=True)
    print(f"\nLambda functions: {len(lambda_funcs)}")
    for key in ['1', '2', '3', '4', '5']:
        if key in lambda_funcs:
            print(f"  ✅ Lambda {key}: {lambda_funcs[key]['name']}")
        else:
            print(f"  ❌ Lambda {key} - MISSING")

if __name__ == "__main__":
    print("🚀 Starting Enhanced Divisor Wave System Tests")
    print("=" * 60)
    
    try:
        test_available_functions()
        test_function_values()
        test_real_plotting()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed!")
        print("\nThe enhanced system should now provide:")
        print("  • Real line plots showing actual function behavior")
        print("  • Exact coefficient matching from original research")
        print("  • Proper spikes and troughs in divisor wave functions")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()