#!/usr/bin/env python3
"""
Original Legacy Plotting Wrapper
This module provides a compatibility layer to use the original plotting system
exactly as it was designed, with the interactive function selection preserved.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.original_legacy_files.complex_plotting_og import Complex_Plotting_OG  
from src.original_legacy_files.special_functions_og import Special_Functions_OG

class OriginalPlottingWrapper:
    """
    Wrapper for the original plotting system that preserves exact behavior
    """
    
    def __init__(self):
        """Initialize the original plotting system"""
        self.special_functions = Special_Functions_OG()
        self.plotting = Complex_Plotting_OG()
        
        # Original function mappings for reference
        self.function_catalog = {
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
        }
        
    def show_function_catalog(self):
        """Display available functions with their IDs"""
        print("ORIGINAL FUNCTION CATALOG:")
        print("=" * 80)
        for key, value in self.function_catalog.items():
            print(f"{key:>3}: {value}")
        print("=" * 80)
        
    def get_lambda_function(self, function_id: str, normalize_type: str = 'N'):
        """
        Get a specific lambda function by ID (replicates original lambda library)
        
        Args:
            function_id: Function ID string ('1', '2', '3', etc.)
            normalize_type: 'Y' or 'N'
            
        Returns:
            Lambda function that can be called with complex z
        """
        # Exact replica of original lambda function operations
        operations = {
            '1': lambda z: self.special_functions.product_of_sin(z, normalize_type),
            '2': lambda z: self.special_functions.product_of_product_representation_for_sin(z, normalize_type),
            '3': lambda z: self.special_functions.product_of_product_representation_for_sin_COMPLEX_VARIANT(z, normalize_type),
            '4': lambda z: self.special_functions.complex_playground_magnification_currated_functions_DEMO(z, normalize_type),
            '5': lambda z: self.special_functions.Riesz_Product_for_Cos(z, normalize_type),
            '6': lambda z: self.special_functions.Riesz_Product_for_Sin(z, normalize_type),
            '7': lambda z: self.special_functions.Riesz_Product_for_Tan(z, normalize_type),
            '8': lambda z: self.special_functions.Viete_Product_for_Cos(z, normalize_type),
            '9': lambda z: self.special_functions.Viete_Product_for_Sin(z, normalize_type),
            '10': lambda z: self.special_functions.Viete_Product_for_Tan(z, normalize_type),
            '11': lambda z: self.special_functions.cos_of_product_of_sin(z, normalize_type),
            '12': lambda z: self.special_functions.sin_of_product_of_sin(z, normalize_type),
            '13': lambda z: self.special_functions.cos_of_product_of_product_representation_of_sin(z, normalize_type),
            '14': lambda z: self.special_functions.sin_of_product_of_product_representation_of_sin(z, normalize_type),
        }
        
        if function_id in operations:
            return operations[function_id]
        else:
            raise ValueError(f"Function ID '{function_id}' not found in original lambda library")
    
    def create_original_plot_2D(self, function_id: str, color_map_2D: str = "4", 
                               normalize_type: str = 'N', save_path: str = None):
        """
        Create a 2D plot using the exact original method but with function selection
        
        Args:
            function_id: Original function ID ('1', '2', '3', etc.)
            color_map_2D: Color map ID ("1" to "8")
            normalize_type: 'Y' or 'N'
            save_path: Optional path to save the plot
            
        Returns:
            Figure object and computed Z values
        """
        print(f"Creating original 2D plot for function {function_id}: {self.function_catalog.get(function_id, 'Unknown')}")
        
        # Get the lambda function
        lambda_function = self.get_lambda_function(function_id, normalize_type)
        
        # Initialize plot axis and grid point mesh (exact original logic)
        X = np.linspace(self.plotting.x_min_2D, self.plotting.x_max_2D, self.plotting.resolution_2D)
        Y = np.linspace(self.plotting.y_min_2D, self.plotting.y_max_2D, self.plotting.resolution_2D)
        X, Y = np.meshgrid(X, Y)

        # Changed dtype to float (exact original comment preserved)
        Z = np.zeros_like(X, dtype=np.float64)

        # For loop which plots the point of the selected function f(z) (exact original comment preserved)
        for i in range(self.plotting.resolution_2D):
            for j in range(self.plotting.resolution_2D):
                z = complex(X[i, j], Y[i, j])
                Z[i, j] = abs(lambda_function(z))

        # Apply colorization (exact original logic)
        if color_map_2D == "1":
            colors = self.plotting.colorization("prism", Z)
        elif color_map_2D == "2":
            colors = self.plotting.colorization("jet", Z)
        elif color_map_2D == "3":
            colors = self.plotting.colorization("plasma", Z)
        elif color_map_2D == "4":
            colors = self.plotting.colorization("viridis", Z)
        elif color_map_2D == "5":
            colors = self.plotting.colorization("magma", Z)
        elif color_map_2D == "6":
            colors = self.plotting.colorization("Spectral", Z)
        elif color_map_2D == "7":
            colors = self.plotting.colorization("RdYlBu", Z)
        elif color_map_2D == "8":
            colors = self.plotting.colorization("coolwarm", Z)
        else:
            colors = self.plotting.colorization("viridis", Z)  # Default

        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.imshow(colors, extent=(self.plotting.x_min_2D, self.plotting.x_max_2D, 
                                  self.plotting.y_min_2D, self.plotting.y_max_2D), 
                 origin='lower', aspect='auto')
        
        # Add title and labels
        function_name = self.function_catalog.get(function_id, f"Function {function_id}")
        ax.set_title(f'Original: {function_name} - Normalization: {normalize_type}')
        ax.set_xlabel('Real Axis')
        ax.set_ylabel('Imaginary Axis')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to: {save_path}")
        
        return fig, Z
    
    def interactive_plot_session(self):
        """
        Run an interactive plotting session that replicates the original experience
        """
        print("ORIGINAL INTERACTIVE PLOTTING SESSION")
        print("=" * 60)
        
        self.show_function_catalog()
        
        while True:
            print("\nChoose options:")
            function_id = input("Enter function ID (1-14, or 'q' to quit): ").strip()
            
            if function_id.lower() == 'q':
                print("Exiting plotting session.")
                break
                
            if function_id not in self.function_catalog:
                print("Invalid choice. Please try again.")
                continue
            
            normalize_type = input("Enter normalization type (Y/N, default N): ").strip().upper()
            if normalize_type not in ['Y', 'N']:
                normalize_type = 'N'
                
            color_map = input("Enter color map (1-8, default 4): ").strip()
            if color_map not in ['1', '2', '3', '4', '5', '6', '7', '8']:
                color_map = '4'
            
            try:
                fig, Z = self.create_original_plot_2D(function_id, color_map, normalize_type)
                plt.show()
                
                save = input("Save plot? (y/n): ").strip().lower()
                if save == 'y':
                    filename = f"original_plot_func{function_id}_norm{normalize_type}_color{color_map}.png"
                    fig.savefig(filename, dpi=300, bbox_inches='tight')
                    print(f"Plot saved as: {filename}")
                    
            except Exception as e:
                print(f"Error creating plot: {e}")
                continue

def main():
    """Main function for testing the original plotting wrapper"""
    wrapper = OriginalPlottingWrapper()
    
    print("Original Plotting System Wrapper")
    print("=" * 40)
    print("1. Show function catalog")
    print("2. Create specific plot")
    print("3. Interactive session")
    print("4. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            wrapper.show_function_catalog()
        elif choice == '2':
            function_id = input("Enter function ID: ").strip()
            normalize_type = input("Normalization (Y/N, default N): ").strip().upper() or 'N'
            color_map = input("Color map (1-8, default 4): ").strip() or '4'
            
            try:
                fig, Z = wrapper.create_original_plot_2D(function_id, color_map, normalize_type)
                plt.show()
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '3':
            wrapper.interactive_plot_session()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()