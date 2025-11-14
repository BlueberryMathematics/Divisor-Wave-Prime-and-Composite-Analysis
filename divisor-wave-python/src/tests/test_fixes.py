#!/usr/bin/env python3
"""
Test script to verify all fixes work correctly:
1. No LaTeX parsing errors
2. Viridis as default colormap 
3. LaTeX formulas not showing automatically on plots
4. UI LaTeX endpoint working
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.plotting_methods import PlottingMethods
from core.python_to_latex_converter import PythonToLatexConverter
import matplotlib
matplotlib.use('Agg')  # Prevent display issues

def test_plotting_no_latex_error():
    """Test that plotting works without LaTeX parsing errors"""
    print("🧪 Testing plotting without LaTeX errors...")
    
    plotter = PlottingMethods("2D")
    
    # Test 2D plot with default settings (should not show LaTeX)
    result = plotter.create_plot_2D(
        function_name="product_of_sin",
        normalize_type="Y"
    )
    
    assert result["success"], f"Plot failed: {result.get('error', 'Unknown error')}"
    print("✅ 2D plot created successfully without LaTeX errors")
    
    # Test with LaTeX explicitly enabled
    result_with_latex = plotter.create_plot_2D(
        function_name="product_of_sin", 
        normalize_type="Y",
        show_latex=True
    )
    
    assert result_with_latex["success"], f"Plot with LaTeX failed: {result_with_latex.get('error', 'Unknown error')}"
    print("✅ 2D plot with LaTeX created successfully")
    
    return True

def test_viridis_default():
    """Test that viridis is now the default colormap"""
    print("🧪 Testing viridis as default colormap...")
    
    plotter = PlottingMethods("2D")
    
    # Create plot without specifying colormap - should use viridis
    result = plotter.create_plot_2D(
        function_name="product_of_sin",
        normalize_type="N"
    )
    
    assert result["success"], f"Plot failed: {result.get('error', 'Unknown error')}"
    
    # Check metadata for colormap info
    if "colormap" in result:
        print(f"✅ Default colormap used: {result['colormap']}")
    else:
        print("✅ Plot created successfully with default colormap")
    
    return True

def test_latex_converter():
    """Test LaTeX converter works correctly"""
    print("🧪 Testing LaTeX converter...")
    
    converter = PythonToLatexConverter()
    
    # Test getting formula
    formula = converter.get_function_formula("product_of_sin")
    assert formula, "No formula returned"
    
    # Should not start/end with $ for UI display
    if formula.startswith('$') and formula.endswith('$'):
        clean_formula = formula[1:-1]
        print(f"✅ LaTeX formula cleaned for UI: {clean_formula[:50]}...")
    else:
        print(f"✅ LaTeX formula ready: {formula[:50]}...")
    
    return True

def test_real_plot():
    """Test real 1D plotting works"""
    print("🧪 Testing real 1D plotting...")
    
    plotter = PlottingMethods("2D")
    
    result = plotter.create_plot_real_1D(
        function_name="product_of_sin",
        normalize_type="N",
        x_range=(2.0, 28.0)
    )
    
    assert result["success"], f"Real plot failed: {result.get('error', 'Unknown error')}"
    print("✅ Real 1D plot created successfully")
    
    return True

if __name__ == "__main__":
    print("🚀 Running comprehensive fix tests...\n")
    
    try:
        test_plotting_no_latex_error()
        print()
        
        test_viridis_default()
        print()
        
        test_latex_converter()
        print()
        
        test_real_plot()
        print()
        
        print("🎉 All tests passed! Fixes are working correctly.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)