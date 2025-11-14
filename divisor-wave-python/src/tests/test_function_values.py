#!/usr/bin/env python3
"""Test script to check what values product_of_sin returns in typical ranges"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.special_functions_library import SpecialFunctionsLibrary
import numpy as np

def test_function_values():
    print("🧪 Testing product_of_sin function values...")
    
    # Initialize the library
    sf = SpecialFunctionsLibrary(use_gpu=False, enable_jit=False)  # Disable optimizations for clarity
    
    # Get the function
    func = sf.get_function('product_of_sin')
    if func is None:
        print("❌ product_of_sin function not found!")
        return
    
    print("✅ Function found")
    
    # Test some typical ranges used in plotting
    ranges_to_test = [
        # Default 3D ranges from plotting_methods.py
        ([1.5, 18.5], [-4.5, 4.5], "Default 3D"),
        # Default 2D ranges 
        ([2, 28], [-5, 5], "Default 2D"),
        # Frontend request ranges (from logs)
        ([1, 15], [0, 15], "Frontend request"),
        # Original paper ranges
        ([1, 10], [-2, 2], "Original paper")
    ]
    
    normalize_modes = ['N', 'Y', 'X', 'Z']
    
    for x_range, y_range, desc in ranges_to_test:
        print(f"\n📊 Testing range: {desc}")
        print(f"   X: [{x_range[0]}, {x_range[1]}], Y: [{y_range[0]}, {y_range[1]}]")
        
        for norm_mode in normalize_modes:
            print(f"\n   Normalization: {norm_mode}")
            
            # Test a small grid
            x_vals = np.linspace(x_range[0], x_range[1], 5)
            y_vals = np.linspace(y_range[0], y_range[1], 5)
            
            values = []
            for x in x_vals:
                for y in y_vals:
                    z = complex(x, y)
                    try:
                        val = func(z, norm_mode)
                        if np.isfinite(val):
                            values.append(val)
                        else:
                            values.append(0.0)
                    except Exception as e:
                        values.append(0.0)
            
            values = np.array(values)
            non_zero = np.count_nonzero(values)
            
            print(f"      Range: [{np.min(values):.6f}, {np.max(values):.6f}]")
            print(f"      Non-zero: {non_zero}/{len(values)} ({100*non_zero/len(values):.1f}%)")
            print(f"      Sample values: {values[:5]}")

if __name__ == "__main__":
    test_function_values()