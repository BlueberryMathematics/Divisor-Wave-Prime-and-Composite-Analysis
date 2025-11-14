"""
Legacy Compatibility Integration for Enhanced Plotting System
Modifies the existing enhanced system to work exactly like the original
while preserving GPU acceleration and JIT compilation
"""

import sys
import os
from typing import Optional, Dict, Any, Callable

# Add original legacy files to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'original_legacy_files'))

from special_functions_og import Special_Functions_OG
from plotting_methods import PlottingMethods
from special_functions_library import SpecialFunctionsLibrary

class LegacyCompatibilityWrapper:
    """
    Wrapper that makes the enhanced system behave exactly like the original
    while keeping GPU/JIT performance optimizations
    """
    
    def __init__(self):
        """Initialize legacy-compatible enhanced system"""
        
        # Initialize original special functions for exact mathematical compatibility
        self.special_functions_og = Special_Functions_OG()
        
        # Initialize enhanced system
        self.special_functions_enhanced = SpecialFunctionsLibrary()
        self.plotting_enhanced = PlottingMethods("2D", use_gpu=True, use_jit=True)
        
        # Original function catalog (preserved exactly)
        self.original_catalog = {
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
        
        print("Legacy Compatibility Wrapper initialized")
        print("- Uses original mathematical functions for exact replication")
        print("- Enhanced with GPU acceleration and JIT compilation")
        print("- Preserves original interactive behavior")
    
    def get_original_lambda_function_library(self, normalize_type: str = 'N'):
        """
        EXACT REPLICA of original lambda function library with interactive selection
        Returns the selected function for plotting
        """
        
        # Create function operations using original special functions
        operations = {
            '1': lambda z: self.special_functions_og.product_of_sin(z, normalize_type),
            '2': lambda z: self.special_functions_og.product_of_product_representation_for_sin(z, normalize_type),
            '3': lambda z: self.special_functions_og.product_of_product_representation_for_sin_COMPLEX_VARIANT(z, normalize_type),
            '4': lambda z: self.special_functions_og.complex_playground_magnification_currated_functions_DEMO(z, normalize_type),
            '5': lambda z: self.special_functions_og.Riesz_Product_for_Cos(z, normalize_type),
            '6': lambda z: self.special_functions_og.Riesz_Product_for_Sin(z, normalize_type),
            '7': lambda z: self.special_functions_og.Riesz_Product_for_Tan(z, normalize_type),
            '8': lambda z: self.special_functions_og.Viete_Product_for_Cos(z, normalize_type),
            '9': lambda z: self.special_functions_og.Viete_Product_for_Sin(z, normalize_type),
            '10': lambda z: self.special_functions_og.Viete_Product_for_Tan(z, normalize_type),
            '11': lambda z: self.special_functions_og.cos_of_product_of_sin(z, normalize_type),
            '12': lambda z: self.special_functions_og.sin_of_product_of_sin(z, normalize_type),
            '13': lambda z: self.special_functions_og.cos_of_product_of_product_representation_of_sin(z, normalize_type),
            '14': lambda z: self.special_functions_og.sin_of_product_of_product_representation_of_sin(z, normalize_type),
            '15': lambda z: self.special_functions_og.Binary_Output_Prime_Indicator_Function_H(z, normalize_type),
            '16': lambda z: self.special_functions_og.Prime_Output_Indicator_J(z, normalize_type),
            '17': lambda z: self.special_functions_og.BOPIF_Q_Alternation_Series(z, normalize_type),
            '18': lambda z: self.special_functions_og.Dirichlet_Eta_Derived_From_BOPIF(z, normalize_type),
        }
        
        # Display catalog (exactly like original)
        print("\nAvailable functions:")
        for key, value in self.original_catalog.items():
            print(f"{key}: {value}")
        
        # Original interactive user input loop
        while True:
            user_input = input('Enter your choice: ')
            if user_input in operations:
                print(f"Selected: {self.original_catalog.get(user_input, 'Unknown function')}")
                return operations[user_input], user_input
            else:
                print("Invalid choice. Please try again.")
    
    def create_plot_2D_original_behavior(self, color_map_2D: str = "4", normalize_type: str = 'N', 
                                       interactive: bool = True, function_id: str = None):
        """
        Create 2D plot with EXACT original behavior but enhanced performance
        
        Args:
            color_map_2D: Color map ID ("1" to "8")
            normalize_type: 'Y' or 'N' 
            interactive: Use interactive function selection (original behavior)
            function_id: Direct function ID if not interactive
        """
        
        print("Creating plot with original behavior + GPU/JIT acceleration...")
        
        # Get function using original selection method
        if interactive and function_id is None:
            selected_function, function_id = self.get_original_lambda_function_library(normalize_type)
        else:
            # Non-interactive mode
            if function_id is None:
                function_id = '1'  # Default to product_of_sin
            
            operations = {
                '1': lambda z: self.special_functions_og.product_of_sin(z, normalize_type),
                '2': lambda z: self.special_functions_og.product_of_product_representation_for_sin(z, normalize_type),
                '3': lambda z: self.special_functions_og.product_of_product_representation_for_sin_COMPLEX_VARIANT(z, normalize_type),
                '4': lambda z: self.special_functions_og.complex_playground_magnification_currated_functions_DEMO(z, normalize_type),
                '5': lambda z: self.special_functions_og.Riesz_Product_for_Cos(z, normalize_type),
                '6': lambda z: self.special_functions_og.Riesz_Product_for_Sin(z, normalize_type),
                '7': lambda z: self.special_functions_og.Riesz_Product_for_Tan(z, normalize_type),
                '8': lambda z: self.special_functions_og.Viete_Product_for_Cos(z, normalize_type),
                '9': lambda z: self.special_functions_og.Viete_Product_for_Sin(z, normalize_type),
                '10': lambda z: self.special_functions_og.Viete_Product_for_Tan(z, normalize_type),
                '11': lambda z: self.special_functions_og.cos_of_product_of_sin(z, normalize_type),
                '12': lambda z: self.special_functions_og.sin_of_product_of_sin(z, normalize_type),
                '13': lambda z: self.special_functions_og.cos_of_product_of_product_representation_of_sin(z, normalize_type),
                '14': lambda z: self.special_functions_og.sin_of_product_of_product_representation_of_sin(z, normalize_type),
                '15': lambda z: self.special_functions_og.Binary_Output_Prime_Indicator_Function_H(z, normalize_type),
                '16': lambda z: self.special_functions_og.Prime_Output_Indicator_J(z, normalize_type),
                '17': lambda z: self.special_functions_og.BOPIF_Q_Alternation_Series(z, normalize_type),
                '18': lambda z: self.special_functions_og.Dirichlet_Eta_Derived_From_BOPIF(z, normalize_type),
            }
            
            selected_function = operations.get(function_id, operations['1'])
        
        # Now use the enhanced plotting system but with original function and behavior
        result = self.plotting_enhanced.create_plot_2D_with_custom_function(
            custom_function=selected_function,
            function_display_name=self.original_catalog.get(function_id, f"Function {function_id}"),
            color_map_2D=color_map_2D,
            normalize_type=normalize_type
        )
        
        return result
    
    def start_interactive_session(self):
        """Start interactive plotting session with original behavior"""
        print("=" * 80)
        print("LEGACY-COMPATIBLE ENHANCED PLOTTING SYSTEM")
        print("Original behavior with GPU acceleration and JIT compilation")
        print("=" * 80)
        
        while True:
            print("\nOptions:")
            print("1. Create 2D plot (original interactive selection)")
            print("2. Create 2D plot (specify function ID)")
            print("3. Show function catalog")
            print("4. Exit")
            
            choice = input("Enter choice (1-4): ").strip()
            
            if choice == '1':
                # Original interactive mode
                normalize_type = input("Enter normalization type (Y/N, default N): ").strip().upper()
                if normalize_type not in ['Y', 'N']:
                    normalize_type = 'N'
                    
                color_map = input("Enter color map (1-8, default 4): ").strip()
                if color_map not in ['1', '2', '3', '4', '5', '6', '7', '8']:
                    color_map = '4'
                
                try:
                    result = self.create_plot_2D_original_behavior(
                        color_map_2D=color_map,
                        normalize_type=normalize_type,
                        interactive=True
                    )
                    
                    # Display plot
                    import matplotlib.pyplot as plt
                    plt.show()
                    
                    save = input("Save plot? (y/n): ").strip().lower()
                    if save == 'y':
                        filename = f"legacy_enhanced_plot_norm{normalize_type}_color{color_map}.png"
                        if 'figure' in result:
                            result['figure'].savefig(filename, dpi=300, bbox_inches='tight')
                            print(f"Plot saved as: {filename}")
                        
                except Exception as e:
                    print(f"Error creating plot: {e}")
                    import traceback
                    traceback.print_exc()
                    continue
            
            elif choice == '2':
                # Direct function ID mode
                function_id = input("Enter function ID (1-18): ").strip()
                if function_id not in self.original_catalog:
                    print("Invalid function ID")
                    continue
                    
                normalize_type = input("Enter normalization type (Y/N, default N): ").strip().upper()
                if normalize_type not in ['Y', 'N']:
                    normalize_type = 'N'
                    
                color_map = input("Enter color map (1-8, default 4): ").strip()
                if color_map not in ['1', '2', '3', '4', '5', '6', '7', '8']:
                    color_map = '4'
                
                try:
                    result = self.create_plot_2D_original_behavior(
                        color_map_2D=color_map,
                        normalize_type=normalize_type,
                        interactive=False,
                        function_id=function_id
                    )
                    
                    # Display plot
                    import matplotlib.pyplot as plt
                    plt.show()
                    
                    save = input("Save plot? (y/n): ").strip().lower()
                    if save == 'y':
                        filename = f"legacy_enhanced_plot_func{function_id}_norm{normalize_type}_color{color_map}.png"
                        if 'figure' in result:
                            result['figure'].savefig(filename, dpi=300, bbox_inches='tight')
                            print(f"Plot saved as: {filename}")
                        
                except Exception as e:
                    print(f"Error creating plot: {e}")
                    import traceback
                    traceback.print_exc()
                    continue
            
            elif choice == '3':
                # Show function catalog
                print("\nOriginal Function Catalog:")
                print("=" * 50)
                for key, value in self.original_catalog.items():
                    print(f"{key:>3}: {value}")
                print("=" * 50)
                
            elif choice == '4':
                print("Exiting session.")
                break
            else:
                print("Invalid choice. Please try again.")

# Main execution
if __name__ == "__main__":
    wrapper = LegacyCompatibilityWrapper()
    wrapper.start_interactive_session()