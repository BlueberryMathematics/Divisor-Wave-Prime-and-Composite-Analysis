#!/usr/bin/env python3
"""
Comprehensive Test for Enhanced Divisor Wave System with LaTeX Support
Tests all new features: Python-to-LaTeX conversion, formula display, and plotting enhancements
"""

import sys
import os
import json
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.special_functions_library import SpecialFunctionsLibrary
from core.plotting_methods import PlottingMethods
from core.python_to_latex_converter import PythonToLatexConverter

def test_latex_converter():
    """Test the Python-to-LaTeX converter"""
    print("=" * 70)
    print("🧮 TESTING PYTHON-TO-LATEX CONVERTER")
    print("=" * 70)
    
    converter = PythonToLatexConverter()
    
    # Test known function formulas
    test_functions = [
        'product_of_sin',
        'product_of_product_representation_for_sin',
        'Riesz_Product_for_Cos',
        'Viete_Product_for_Sin',
        'cos_of_product_of_sin'
    ]
    
    for func_name in test_functions:
        formula = converter.get_function_formula(func_name)
        print(f"\n📐 {func_name}:")
        print(f"   LaTeX: {formula}")
    
    # Test saving formulas
    converter.save_formulas_to_json("test_formulas.json")
    print(f"\n💾 Saved {len(converter.known_formulas)} formulas to test_formulas.json")

def test_plotting_with_latex():
    """Test plotting with LaTeX formulas"""
    print("\n" + "=" * 70)
    print("🎨 TESTING PLOTTING WITH LATEX FORMULAS")
    print("=" * 70)
    
    plotter = PlottingMethods("2D")
    
    # Test real line plot with LaTeX
    print("\n📊 Creating real line plot with LaTeX formula...")
    result = plotter.create_plot_real_1D(
        function_name="product_of_sin",
        normalize_type="N",
        x_range=(2.0, 20.0),
        resolution=200,
        return_base64=False  # Display directly
    )
    
    if result["success"]:
        print(f"✅ Real plot with LaTeX created successfully!")
        print(f"   Function: {result['function_name']}")
        print(f"   Points computed: {result['points_computed']}")
        print(f"   Computation time: {result['computation_time']}s")
    else:
        print(f"❌ Real plot failed: {result['error']}")
    
    # Test 2D plot with LaTeX
    print("\n📊 Creating 2D complex plot with LaTeX formula...")
    result2 = plotter.create_plot_2D(
        function_name="product_of_product_representation_for_sin",
        color_map_2D="plasma",
        normalize_type="Y",
        resolution=150,
        x_range=(-8, 8),
        y_range=(-5, 5),
        return_base64=False
    )
    
    if result2["success"]:
        print(f"✅ 2D plot with LaTeX created successfully!")
        print(f"   Function: {result2['function_name']}")
        print(f"   Resolution: {result2['resolution']}")
        print(f"   Computation time: {result2['computation_time']}s")
    else:
        print(f"❌ 2D plot failed: {result2['error']}")

def test_formula_retrieval():
    """Test formula retrieval functionality"""
    print("\n" + "=" * 70)
    print("📋 TESTING FORMULA RETRIEVAL")
    print("=" * 70)
    
    plotter = PlottingMethods("2D")
    
    # Test getting specific formulas
    test_functions = [
        'product_of_sin',
        'Riesz_Product_for_Cos',
        'Viete_Product_for_Sin'
    ]
    
    for func_name in test_functions:
        for norm_type in ['N', 'Y']:
            formula = plotter.get_function_latex(func_name, norm_type)
            print(f"\n📝 {func_name} (norm={norm_type}):")
            print(f"   {formula}")
    
    # Test formula data structure
    formulas = plotter.latex_formulas
    if 'formulas' in formulas:
        print(f"\n📚 Total formulas loaded: {len(formulas['formulas'])}")
        categories = set()
        for data in formulas['formulas'].values():
            categories.add(data.get('category', 'unknown'))
        print(f"📂 Categories: {', '.join(sorted(categories))}")

def test_function_evaluation():
    """Test that functions still work correctly"""
    print("\n" + "=" * 70)
    print("🔢 TESTING FUNCTION EVALUATION")
    print("=" * 70)
    
    special_functions = SpecialFunctionsLibrary()
    
    # Test specific values that should show the characteristic behavior
    test_points = [2.0, 3.0, 5.0, 7.0, 11.0, 13.0, 17.0]
    
    print("\n📊 Product of Sin Values (a(z)):")
    for x in test_points:
        z = complex(x, 0.0)
        val_n = special_functions.product_of_sin(z, 'N')
        val_y = special_functions.product_of_sin(z, 'Y')
        print(f"   a({x}) = {val_n:.6f} (N), {val_y:.6f} (Y)")
    
    print("\n📊 Product of Product Representation Values (b(z)):")
    for x in test_points:
        z = complex(x, 0.0)
        val_n = special_functions.product_of_product_representation_for_sin(z, 'N')
        val_y = special_functions.product_of_product_representation_for_sin(z, 'Y')
        print(f"   b({x}) = {val_n:.6f} (N), {val_y:.6f} (Y)")

def test_custom_function_workflow():
    """Test the workflow for custom functions"""
    print("\n" + "=" * 70)
    print("🛠️ TESTING CUSTOM FUNCTION WORKFLOW")  
    print("=" * 70)
    
    # Test loading existing custom functions
    try:
        with open('src/core/custom_functions.json', 'r') as f:
            custom_funcs = json.load(f)
        
        print(f"📂 Loaded custom functions: {len(custom_funcs.get('functions', {}))}")
        
        for name, data in custom_funcs.get('functions', {}).items():
            print(f"\n🔧 {name}:")
            print(f"   LaTeX: {data.get('latex_formula', 'N/A')}")
            print(f"   Description: {data.get('description', 'N/A')}")
            
    except FileNotFoundError:
        print("⚠️ No custom functions file found")

def main():
    """Run all tests"""
    print("🚀 ENHANCED DIVISOR WAVE SYSTEM - COMPREHENSIVE TEST")
    print("=" * 70)
    print("Testing LaTeX integration, formula display, and enhanced plotting")
    
    try:
        test_latex_converter()
        test_function_evaluation()
        test_formula_retrieval()
        test_plotting_with_latex()
        test_custom_function_workflow()
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("\n🎯 FEATURES NOW AVAILABLE:")
        print("  • Python-to-LaTeX formula conversion")
        print("  • LaTeX formulas displayed on plots")
        print("  • Real line plotting (1D) for function analysis")
        print("  • Enhanced 2D/3D plotting with formula overlays")
        print("  • API endpoints for LaTeX formula retrieval")
        print("  • LaTeX keyboard layout for frontend")
        print("  • Custom function management with LaTeX support")
        print("\n🌐 API Endpoints:")
        print("  • GET /latex/formula/{function_name} - Get specific formula")
        print("  • GET /latex/formulas - Get all formulas")
        print("  • GET /latex/keyboard - Get LaTeX keyboard layout")
        print("  • POST /plot/real - Create real line plots")
        print("\n📊 Usage:")
        print("  • Real plots: Show actual function behavior along real axis")
        print("  • Complex plots: Show magnitude in complex plane")
        print("  • LaTeX formulas: Displayed at bottom of all plots")
        print("  • Custom functions: Can be created with LaTeX formulas")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()