#!/usr/bin/env python3
"""
Compare Original vs Enhanced Systems
Direct comparison of function outputs to verify mathematical equivalence
"""

import sys
import os
import numpy as np
import math

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def compare_systems():
    print("🔬 COMPARING ORIGINAL vs ENHANCED SYSTEMS")
    print("=" * 60)
    
    try:
        # Import original system
        from original_legacy_files.special_functions_og import Special_Functions as OriginalSF
        print("✅ Original system imported successfully")
        
        # Import enhanced system
        from core.special_functions_library import SpecialFunctionsLibrary
        print("✅ Enhanced system imported successfully")
        
        # Initialize both systems
        original = OriginalSF("2D")
        enhanced = SpecialFunctionsLibrary(use_gpu=False)
        
        print("\n📊 Function Value Comparison:")
        print("-" * 40)
        
        # Test values from typical plotting ranges
        test_points = [2.0, 3.0, 5.0, 7.0, 11.0, 13.0]
        
        for normalize_type in ['N', 'Y']:
            print(f"\n🔧 Normalization Type: {normalize_type}")
            print("Point | Original     | Enhanced     | Difference")
            print("-" * 50)
            
            for x in test_points:
                z = complex(x, 0)  # Real values first
                
                # Get results from both systems
                try:
                    original_result = original.product_of_sin(z, normalize_type)
                    enhanced_result = enhanced.product_of_sin(z, normalize_type)
                    
                    diff = abs(original_result - enhanced_result)
                    match_symbol = "✅" if diff < 1e-10 else "❌" if diff > 1e-6 else "⚠️"
                    
                    print(f"{x:5.1f} | {original_result:11.6e} | {enhanced_result:11.6e} | {diff:8.2e} {match_symbol}")
                    
                except Exception as e:
                    print(f"{x:5.1f} | ERROR: {str(e)[:30]}...")
        
        # Test complex values
        print(f"\n🔧 Complex Values Test (Normalize: N):")
        print("Point        | Original     | Enhanced     | Difference")
        print("-" * 55)
        
        complex_points = [2+1j, 3+0.5j, 5+2j]
        for z in complex_points:
            try:
                original_result = original.product_of_sin(z, 'N')
                enhanced_result = enhanced.product_of_sin(z, 'N')
                
                diff = abs(original_result - enhanced_result)
                match_symbol = "✅" if diff < 1e-10 else "❌" if diff > 1e-6 else "⚠️"
                
                print(f"{str(z):12} | {original_result:11.6e} | {enhanced_result:11.6e} | {diff:8.2e} {match_symbol}")
                
            except Exception as e:
                print(f"{str(z):12} | ERROR: {str(e)[:30]}...")
        
        print(f"\n🧮 Testing Second Function (product_of_product_representation):")
        print("Point | Original     | Enhanced     | Difference")
        print("-" * 50)
        
        for x in [2.0, 3.0, 5.0]:
            z = complex(x, 0)
            try:
                original_result = original.product_of_product_representation_for_sin(z, 'N')
                enhanced_result = enhanced.product_of_product_representation_for_sin(z, 'N')
                
                diff = abs(original_result - enhanced_result)
                match_symbol = "✅" if diff < 1e-10 else "❌" if diff > 1e-6 else "⚠️"
                
                print(f"{x:5.1f} | {original_result:11.6e} | {enhanced_result:11.6e} | {diff:8.2e} {match_symbol}")
                
            except Exception as e:
                print(f"{x:5.1f} | ERROR: {str(e)[:30]}...")
        
        print(f"\n📈 Testing Parameter Differences:")
        print("-" * 40)
        
        # Check if coefficients are the same
        print("Checking coefficient consistency...")
        z_test = complex(5, 0)
        
        # Test different normalization types to see coefficient differences
        orig_n = original.product_of_sin(z_test, 'N')
        orig_y = original.product_of_sin(z_test, 'Y')
        enh_n = enhanced.product_of_sin(z_test, 'N')
        enh_y = enhanced.product_of_sin(z_test, 'Y')
        
        print(f"Original N: {orig_n:.6e}, Y: {orig_y:.6e}")
        print(f"Enhanced N: {enh_n:.6e}, Y: {enh_y:.6e}")
        print(f"N Ratio: {enh_n/orig_n:.6f}, Y Ratio: {enh_y/orig_y:.6f}")
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure both systems are available in the src directory")
        
    except Exception as e:
        print(f"❌ Error during comparison: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    compare_systems()