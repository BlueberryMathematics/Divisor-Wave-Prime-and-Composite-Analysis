#!/usr/bin/env python3
"""
Enhanced Legacy Plotting System
Start script that provides the original interactive behavior with GPU/JIT acceleration

This script gives you the exact original plotting experience with modern performance
"""

import sys
import os

# Add all necessary paths
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, 'src'))
sys.path.append(os.path.join(current_dir, 'src', 'core'))
sys.path.append(os.path.join(current_dir, 'src', 'original_legacy_files'))

def main():
    """Main entry point for the enhanced legacy plotting system"""
    
    print("=" * 80)
    print("ENHANCED LEGACY PLOTTING SYSTEM")
    print("Original behavior with GPU acceleration and JIT compilation")
    print("=" * 80)
    
    try:
        from legacy_compatibility_wrapper import LegacyCompatibilityWrapper
        
        # Initialize the wrapper
        wrapper = LegacyCompatibilityWrapper()
        
        # Start interactive session
        wrapper.start_interactive_session()
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Falling back to basic original system...")
        
        try:
            # Fallback to original system
            from original_legacy_files.complex_plotting_og import Complex_Plotting_OG
            from original_legacy_files.special_functions_og import Special_Functions_OG
            
            plotting = Complex_Plotting_OG()
            
            print("Using original plotting system (no GPU acceleration)")
            
            while True:
                print("\nOriginal System Options:")
                print("1. Create 2D plot")
                print("2. Exit")
                
                choice = input("Enter choice (1-2): ").strip()
                
                if choice == '1':
                    normalize_type = input("Enter normalization type (Y/N, default N): ").strip().upper()
                    if normalize_type not in ['Y', 'N']:
                        normalize_type = 'N'
                        
                    color_map = input("Enter color map (1-8, default 4): ").strip()
                    if color_map not in ['1', '2', '3', '4', '5', '6', '7', '8']:
                        color_map = '4'
                    
                    try:
                        # This would require modifying the original to not use input()
                        print("Note: Original system requires interactive function selection")
                        print("Please run the original files directly if you need the exact original behavior")
                        
                    except Exception as e:
                        print(f"Error: {e}")
                        
                elif choice == '2':
                    break
                else:
                    print("Invalid choice.")
                    
        except ImportError as e2:
            print(f"Could not import original files: {e2}")
            print("Please ensure the original legacy files are in src/original_legacy_files/")
    
    except Exception as e:
        print(f"Error starting enhanced system: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()