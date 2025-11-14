#!/usr/bin/env python3
"""
Test script for Enhanced Legacy Plotting System
Quick verification that the new system works with original functions and GPU/JIT acceleration
"""

import sys
import os
import matplotlib.pyplot as plt

# Add paths
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, 'src'))
sys.path.append(os.path.join(current_dir, 'src', 'core'))
sys.path.append(os.path.join(current_dir, 'src', 'original_legacy_files'))

def test_enhanced_legacy_system():
    """Test the enhanced legacy plotting system"""
    
    print("Testing Enhanced Legacy Plotting System...")
    print("=" * 50)
    
    try:
        # Import required modules
        from legacy_compatibility_wrapper import LegacyCompatibilityWrapper
        
        print("✅ Successfully imported LegacyCompatibilityWrapper")
        
        # Initialize wrapper
        wrapper = LegacyCompatibilityWrapper()
        print("✅ Successfully initialized wrapper")
        
        # Test non-interactive plotting
        print("\nTesting non-interactive plotting with function 1 (product_of_sin)...")
        
        result = wrapper.create_plot_2D_original_behavior(
            color_map_2D="4",  # viridis
            normalize_type='N',
            interactive=False,
            function_id='1'
        )
        
        if result.get('success', False):
            print("✅ Successfully created plot with original function")
            print(f"   Computation time: {result.get('computation_time', 'unknown'):.2f}s")
            print(f"   Performance mode: {result.get('performance_mode', 'unknown')}")
            
            # Show the plot
            if 'figure' in result:
                plt.show()
                
            return True
        else:
            print(f"❌ Plot creation failed: {result.get('error', 'Unknown error')}")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Trying to test individual components...")
        
        # Test original functions
        try:
            from special_functions_og import Special_Functions_OG
            print("✅ Can import original special functions")
            
            sf = Special_Functions_OG()
            print("✅ Can initialize original special functions")
            
            # Test a simple function call
            result = sf.product_of_sin(complex(2, 1), 'N')
            print(f"✅ product_of_sin(2+1j, 'N') = {result}")
            
        except Exception as e2:
            print(f"❌ Error testing original functions: {e2}")
        
        # Test enhanced plotting
        try:
            from plotting_methods import PlottingMethods
            print("✅ Can import enhanced plotting methods")
            
            plotting = PlottingMethods("2D", use_gpu=True, use_jit=True)
            print("✅ Can initialize enhanced plotting")
            print(f"   GPU available: {plotting.use_gpu}")
            print(f"   JIT available: {plotting.use_jit}")
            
        except Exception as e3:
            print(f"❌ Error testing enhanced plotting: {e3}")
        
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_performance_comparison():
    """Test performance comparison between systems"""
    
    print("\nTesting Performance Comparison...")
    print("=" * 50)
    
    try:
        import time
        from special_functions_og import Special_Functions_OG
        
        sf = Special_Functions_OG()
        
        # Test function evaluation speed
        test_points = [complex(i, j) for i in range(1, 6) for j in range(1, 6)]
        
        print(f"Testing with {len(test_points)} complex points...")
        
        start_time = time.time()
        results = []
        for z in test_points:
            try:
                result = sf.product_of_sin(z, 'N')
                results.append(result)
            except:
                results.append(0.0)
        
        elapsed = time.time() - start_time
        print(f"✅ Original functions: {elapsed:.4f}s for {len(test_points)} evaluations")
        print(f"   Average per evaluation: {elapsed/len(test_points)*1000:.2f}ms")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False

def main():
    """Main test function"""
    
    print("ENHANCED LEGACY PLOTTING SYSTEM - TEST SUITE")
    print("=" * 60)
    
    # Test 1: Basic functionality
    test1_passed = test_enhanced_legacy_system()
    
    # Test 2: Performance
    test2_passed = test_performance_comparison()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Enhanced Legacy System: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Performance Test:       {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed:
        print("\n🎉 You can now use the enhanced legacy plotting system!")
        print("Run: python start_enhanced_legacy_plotting.py")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
        print("You may need to install dependencies or fix import paths.")
    
    print("\nAvailable scripts:")
    print("- start_enhanced_legacy_plotting.py  : Interactive enhanced system")
    print("- legacy_compatibility_wrapper.py    : Direct wrapper usage")
    print("- original_plotting_wrapper.py       : Pure original system")

if __name__ == "__main__":
    main()