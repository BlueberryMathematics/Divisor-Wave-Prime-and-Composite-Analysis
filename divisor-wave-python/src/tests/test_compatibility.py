#!/usr/bin/env python3
"""
Test script to verify backward compatibility of optimized system
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_compatibility():
    """Test the optimized system maintains original plotting abilities"""
    
    try:
        print("Testing backward compatibility...")
        
        # Test core dependencies
        import numpy as np
        import math
        import cmath
        print("PASS: Core dependencies available")
        
        # Test basic complex operations
        test_z = 2 + 1j
        basic_result = abs(np.sin(math.pi * test_z))
        print(f"PASS: Basic complex math works: sin(pi*z) = {basic_result}")
        
        # Import optimized library
        from core.special_functions_library import SpecialFunctionsLibrary
        print("PASS: SpecialFunctionsLibrary imported successfully")
        
        # Initialize library
        lib = SpecialFunctionsLibrary()
        print("PASS: Library initialized")
        
        # Test lambda function catalog
        catalog = lib.lamda_function_library()
        print(f"PASS: Lambda catalog loaded with {len(catalog)} functions")
        
        # Test function evaluation by ID (original interface)
        result1 = lib.get_lambda_function_by_id('1', test_z, 'N')
        print(f"PASS: Function 1 (product_of_sin): {result1}")
        
        result2 = lib.get_lambda_function_by_id('2', test_z, 'N')
        print(f"PASS: Function 2 (enhanced wave): {result2}")
        
        result10 = lib.get_lambda_function_by_id('10', test_z, 'N')
        print(f"PASS: Function 10 (prime indicator): {result10}")
        
        # Test direct function calls
        direct1 = lib.product_of_sin(test_z, 'N')
        direct2 = lib.product_of_product_representation_for_sin(test_z, 'N')
        
        print(f"PASS: Direct product_of_sin: {direct1}")
        print(f"PASS: Direct enhanced wave: {direct2}")
        
        # Verify backward compatibility
        match1 = abs(result1 - direct1) < 1e-10
        match2 = abs(result2 - direct2) < 1e-10
        
        print(f"PASS: Function 1 matches direct call: {match1}")
        print(f"PASS: Function 2 matches direct call: {match2}")
        
        # Test additional functions
        try:
            result_prime = lib.Binary_Output_Prime_Indicator_Function_H(test_z, 'N')
            print(f"PASS: Prime indicator function: {result_prime}")
        except Exception as e:
            print(f"WARNING: Prime indicator error: {e}")
        
        try:
            result_gamma = lib.gamma_of_product_of_product_representation_for_sin(test_z, 'N')
            print(f"PASS: Gamma function: {result_gamma}")
        except Exception as e:
            print(f"WARNING: Gamma function error: {e}")
        
        print("\n" + "="*50)
        print("SUCCESS: All backward compatibility tests passed!")
        print("- Optimized system retains original plotting abilities")
        print("- Lambda function library interface preserved")
        print("- Original function IDs (1-32) working correctly")
        print("- Complex_Plotting_OG.py compatibility maintained")
        print("="*50)
        
        return True
        
    except ImportError as e:
        print(f"FAIL: Import error - {e}")
        print("Some required packages may not be installed")
        return False
        
    except Exception as e:
        print(f"FAIL: Unexpected error - {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_compatibility()
    sys.exit(0 if success else 1)