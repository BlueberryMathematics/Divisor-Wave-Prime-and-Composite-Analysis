"""
Complex_Plotting.py
    The Complex Plotting class is a set of tools for plotting in the complex plane utilizing matplotlib.
    The Tool is capable of graphing polynomial functions, trig functions, infinite summations, and infinite
    products in the complex plane. These products are related to the distribution of prime numbers and the Riemann
    Hypothesis. The methods in call methods from the file Special_Functions.py for infinite product formulas.
4/9/2023
@LeoBorcherding
"""
import http
import os
import pprint
import socketserver
import subprocess
import sys

import numpy as np
#import pyqtgraph as pg
import matplotlib.pyplot as plt

import vispy.app
from vispy.scene import SceneCanvas
from vispy import visuals, scene

from matplotlib.colors import ListedColormap
from matplotlib import ticker
from matplotlib import cm
from matplotlib.colors import LightSource
from matplotlib.colors import PowerNorm

# # Import bindings and graphics modules
# import cplusplus_extensions
# from cplusplus_extensions import bindings
# print(cplusplus_extensions.__file__)

from Special_Functions import Special_Functions

# print(sys.path)
plt.style.use('dark_background')

# -----------------------------------------------------------------------------------------------------------------
class Complex_Plotting :
    """
    A Class for plotting complex functions. This tool provides the plotting functions for 2D and 3D graphics for
    infinite series such as the riemann zeta function, the infinite product of the product representation for
    sin(pi*z/n) as well as any other function that can be formulated in the complex plane.
    """
    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, plot_type):
        """
        Initialization the Special_Functions Object
        """
        #TODO Implement Default Values & preselected data ranges for "nice" areas. (pretty areas?)

        #TODO Add variable for 2D vs 3D plot, take the plotting code from Infinite_Prod_of_Prod_Representation_Of_Sin_Complex_Plot.py
        # and incorporate that code into Product_Fractal.py by adding a second create_plot function where it decides
        # which plotting function to use based on the selector

        # TODO Values for x & y selector

        # TODO the following groups are nice areas to explore for the complex plane

        # if user selected 2D plot, graph the plot with the given values
        if plot_type == "2D":

            # Default Values, Copy these if you are going to change them
            # self.resolution_2D = 500
            # self.x_min_2D = 1
            # self.x_max_2D = 22
            # self.y_min_2D = -3
            # self.y_max_2D = 3

            # Default Values, Copy these if you are going to change them
            # self.resolution_2D = 750
            self.resolution_2D = 750
            # self.resolution_2D = 500
            # self.x_min_2D = 1.5
            # self.x_max_2D = 14.5
            # self.y_min_2D = -0.5
            # self.y_max_2D = 0.5

            # self.x_min_2D = 1.5
            # self.x_max_2D = 5.5
            # self.y_min_2D = -0.5
            # self.y_max_2D = 0.5

            # self.x_min_2D = 1.5
            # self.x_max_2D = 18.5
            # self.y_min_2D = -6.5
            # self.y_max_2D = 6.5


            # self.x_min_2D = 1.5
            # self.x_max_2D = 28.5
            # self.y_min_2D = -9.5
            # self.y_max_2D = 9.5

            # self.x_min_2D = 2
            # self.x_max_2D = 7
            # self.y_min_2D = -2
            # self.y_max_2D = 2

            # self.x_min_2D = 7
            # self.x_max_2D = 13
            # self.y_min_2D = -2
            # self.y_max_2D = 2

            self.x_min_2D = 2
            self.x_max_2D = 28
            self.y_min_2D = -5
            self.y_max_2D = 5

            # self.x_min_2D = 0
            # self.x_max_2D = 13
            # self.y_min_2D = -32
            # self.y_max_2D = 32

            # self.x_min_2D = 1.5
            # self.x_max_2D = 10.5
            # self.y_min_2D = -5.5
            # self.y_max_2D = 5.5

        # if user selected 2D plot, graph the plot with the given values
        if plot_type == "3D":

            # Default Values, Copy these if you are going to change them
            # self.resolution_3D = 0.1899
            # self.resolution_3D = 0.1199
            # self.resolution_3D = 0.0949
            # self.resolution_3D = 0.0899
            # self.resolution_3D = 0.0599

            #TODO Real Fast !!!!!!!!!!!!!
            # self.resolution_3D = 0.0449

            #TODO good fast
            # self.resolution_3D = 0.0349

            #TODO medium HD !?!?!?!?!?!?!
            # self.resolution_3D = 0.0249

            #TODO better slow
            self.resolution_3D = 0.0199

            #TODO very slow !!!!!!!!!!!!!
            # self.resolution_3D = 0.0149

            ##TODO ULTRA HD (1 min)
            # self.resolution_3D = 0.0099

            #TODO ULTRA HD + (2 min)
            # self.resolution_3D = 0.0060

            # self.resolution_3D = 0.0010

            # self.resolution_3D = 0.0001

            #TODO RANGE FOR X & Y VALUES

            # self.x_min_3D = 2
            # self.x_max_3D = 12.5
            # self.y_min_3D = -2.5
            # self.y_max_3D = 2.5

            # self.x_min_3D = 1
            # self.x_max_3D = 8
            # self.y_min_3D = -1
            # self.y_max_3D = 1

            # self.x_min_3D = 1
            # self.x_max_3D = 12
            # self.y_min_3D = -3
            # self.y_max_3D = 3

            # self.x_min_3D = 1
            # self.x_max_3D = 7
            # self.y_min_3D = -1
            # self.y_max_3D = 1

            # self.x_min_3D = 2
            # self.x_max_3D = 5
            # self.y_min_3D = -.75
            # self.y_max_3D = .75

            # self.x_min_3D = 0.5
            # self.x_max_3D = 6.5
            # self.y_min_3D = -3
            # self.y_max_3D = 3

            # self.x_min_3D = 1.5
            # self.x_max_3D = 18.5
            # self.y_min_3D = -6.5
            # self.y_max_3D = 6.5

            # self.x_min_3D = 6.5
            # self.x_max_3D = 14.5
            # self.y_min_3D = -2.5
            # self.y_max_3D = 2.5

            # self.x_min_3D = 1.5
            # self.x_max_3D = 14.5
            # self.y_min_3D = -4.5
            # self.y_max_3D = 4.5

            self.x_min_3D = 1.5
            self.x_max_3D = 18.5
            self.y_min_3D = -4.5
            self.y_max_3D = 4.5

            # self.x_min_3D = 11
            # self.x_max_3D = 13
            # self.y_min_3D = -0.5
            # self.y_max_3D = 0.5

            # self.x_min_3D = 5.5
            # self.x_max_3D = 12.5

            # self.x_min_3D = 5.5
            # self.x_max_3D = 8.5

            # self.x_min_3D = 9.5
            # self.x_max_3D = 14.5

            # self.y_min_3D = -.314
            # self.y_max_3D = .314


            # self.x_min_3D = -5.5
            # self.x_max_3D = 6
            # self.y_min_3D = 0
            # self.y_max_3D = 12

            # Default for function 3
            # self.x_min_3D = 2
            # self.x_max_3D = 19
            # self.y_min_3D = -7
            # self.y_max_3D = 7

        return

    # -----------------------------------------------------------------------------------------------------------------
    def colorization(self, color_selection, Z):
        """
        Args:
            color_selection (str): the name of the color map to use
            Z (numpy.ndarray): the array to apply colorization to
            resolution_2D
        Returns:
        """

        #pprint.pprint(Z)

        # TODO create better Selector for colorization Methods and Ultimately implement a color slider
        if color_selection == "custom_colors1":
            # Default Colorization, it is based upon the angle change around the point of f(z)
            colors = np.zeros((self.resolution_2D, self.resolution_2D, 3))
            colors[:, :, 0] = np.sin(2 * np.pi * np.real(Z) / 8.0)
            colors[:, :, 1] = np.sin(2 * np.pi * np.real(Z) / 9.0)
            colors[:, :, 2] = np.sin(2 * np.pi * np.real(Z) / 10.0)
            return colors
        elif color_selection == "custom_colors1":
            # Alternate Colorization, it is based upon the angle change around the point of f(z)
            colors = np.zeros((self.resolution_2D, self.resolution_2D, 3))
            colors[:, :, 0] = np.sin(2 * np.pi * np.real(Z) / 12)
            colors[:, :, 1] = np.sin(2 * np.pi * np.real(Z) / 14)
            colors[:, :, 2] = np.sin(2 * np.pi * np.real(Z) / 16)
            return colors
        elif color_selection == "custom_colors1":
            # Attempt at mandelbrot level detail with color gradient selector
            colors = np.zeros((self.resolution_2D, self.resolution_2D, 3))
            for i in range(self.resolution_2D):
                for j in range(self.resolution_2D):
                    colors[i, j, :] = [(i * j) % 256 / 255, (i + j) % 256 / 255, (i * j + i + j) % 256 / 255]
            return colors
        elif color_selection == "prism":
            # Base plasma color map
            cmap = plt.get_cmap('prism')
        elif color_selection == "jet":
            # Base plasma color map
            cmap = plt.get_cmap('jet')
        elif color_selection == "plasma":
            # Base magma color map
            cmap = plt.get_cmap('plasma')
        elif color_selection == "viridis":
            # Base viridis color map
            cmap = plt.get_cmap('viridis')
        elif color_selection == "magma":
            # Base viridis color map
            cmap = plt.get_cmap('twilight_shifted')
        else:
            # apply color selection to the grid map
            cmap = ListedColormap(color_selection)

        # store the colorized grid map and return
        colors = cmap(Z / np.max(Z))
        #colors = cmap((Z - np.min(Z)) / (np.max(Z) - np.min(Z)))

        # TODO Implement On off for lightshading and improve its colorization
        # # Apply shading to the colorized image
        # light = LightSource(azdeg=315, altdeg=10)
        # shaded_colors = \
        #     light.shade(colors, cmap=plt.cm.hot, vert_exag=1.0, norm=PowerNorm(0.3), blend_mode='hsv')
        return colors

    # -----------------------------------------------------------------------------------------------------------------
    def create_plot_2D(self, color_map_2D, Normalize_type):
        """
        Args:
            resolution_2D:
            x_min_2D:
            x_max_2D:
            y_min_2D:
            y_max_2D:
            color_map:
        Returns:
            Matlab plot
        """
        #Initialize plot axis and grid point mesh
        X = np.linspace(self.x_min_2D, self.x_max_2D, self.resolution_2D)
        Y = np.linspace(self.y_min_2D, self.y_max_2D, self.resolution_2D)
        X, Y = np.meshgrid(X, Y)

        # changed dtype to float
        Z = np.zeros_like(X, dtype=np.float64)

        # calculate special functions object f(z)
        lamda_function_array = special_functions_object.lamda_function_library(Normalize_type)

        # for loop which plots the point of the selected function f(z)
        for i in range(self.resolution_2D):
            for j in range(self.resolution_2D):
                z = complex(X[i, j], Y[i, j])
                Z[i, j] = abs(lamda_function_array(z))

        # colors = np.zeros((300, 300, 3))
        # colors[:, :, 0] = np.sin(2 * np.pi * np.real(Z) / 8.0)
        # colors[:, :, 1] = np.sin(2 * np.pi * np.real(Z) / 9.0)
        # colors[:, :, 2] = np.sin(2 * np.pi * np.real(Z) / 10.0)

        if color_map_2D == "1":
            colors = self.colorization("prism", Z)
        elif color_map_2D == "2":
            colors = self.colorization("jet", Z)
        elif color_map_2D == "3":
            colors = self.colorization("plasma", Z)
        elif color_map_2D == "4":
            colors = self.colorization("viridis", Z)
        elif color_map_2D == "5":
            colors = self.colorization("magma", Z)
        elif color_map_2D == "6":
            colors = self.colorization("custom_colors2", Z)
        elif color_map_2D == "7":
            colors = self.colorization("custom_colors3", Z)
        elif color_map_2D == "8":
            colors = self.colorization("custom_colors1", Z)
        # #Set Square Canvas
        # fig, ax1 = plt.subplots(figsize=(8, 8))

        #Set Rectangular Canvas
        # fig, ax1 = plt.subplots(figsize=(12, 8))
        fig, ax1 = plt.subplots(figsize=(16,9))

        # TODO IMPLEMENT 2nd Subplot where 2D fractal is on 1 side, and 3D Fractal is on the other, have this be
        #  optional through user input

        #TODO Selector for OG colorization vs light source ==============================
        ax1.imshow(colors, extent=(self.x_min_2D, self.x_max_2D, self.y_min_2D, self.y_max_2D), origin='lower', aspect='auto')
        # ax1.imshow(np.log(Z), extent=(x_min_2D, x_max_2D, y_min_2D, y_max_2D), origin='lower')

        # shaded_colors = colors

        # # Plot the shaded image
        # ax1.imshow(shaded_colors, extent=(x_min_2D, x_max_2D, y_min_2D, y_max_2D), origin='lower',
        #            aspect='auto')
        #TODO ===========================================================================

        # Add Title To Plot
        ax1.set_title(f'Colorization {special_functions_object}')

        # Set tick locators and formatters for the x and y axes
        ax1.xaxis.set_major_locator(ticker.MultipleLocator(1))  # show tick marks every 2 units
        ax1.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))  # format tick labels as integers
        # ax1.yaxis.set_major_locator(ticker.MultipleLocator(2))  # show tick marks every 2 units
        # ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))  # format tick labels as integers

        plt.tight_layout()
        plt.show()

        return

    # -----------------------------------------------------------------------------------------------------------------
    def create_plot_3D(self, color_map_3D, Normalize_type):
        """
        Plotting function.

        Args:
            m - index value used for function when updating and creating plot
        Returns:
            NA
        """

        # calculate special functions object f(z)
        lamda_function_array = special_functions_object.lamda_function_library(Normalize_type)

        R = self.resolution_3D
        X = np.arange(self.x_min_3D, self.x_max_3D, R)
        Y = np.arange(self.y_min_3D, self.y_max_3D, R)

        X, Y = np.meshgrid(X, Y)
        xn, yn = X.shape
        W = X * 0

        for xk in range(xn):
            for yk in range(yn):
                try:
                    z = complex(X[xk, yk], Y[xk, yk])
                    w = float(lamda_function_array(z))

                    if w != w:
                        raise ValueError
                    W[xk, yk] = w

                except (ValueError, TypeError, ZeroDivisionError):
                    # can handle special values here
                    pass

        # -----------------------------------------------------------------------------------------------------------------------
        # Set up the plot
        fig = plt.figure(figsize=(19, 11))

        # create 3d subplot
        ax = fig.add_subplot(111, projection='3d')

        # Set initial plot angles
        # ax.view_init(elev=30, azim=70)
        ax.view_init(elev=30, azim=-70)
        # ax.view_init(elev=210, azim=-70)

        # ax.view_init(elev=30, azim=-110)
        # ax.view_init(elev=210, azim=-45)
        # ax.view_init(elev=90, azim=0)

        ax.dist = 10
        ax.set_box_aspect((5, 5, 1))
        ax.auto_scale_xyz([-1, 1], [-1, 1], [-1, 1])

        # Set the aspect ratio to be 1:1:0.5 # Was originally that ratio
        ax.set_box_aspect((5, 5, 1))
        # ax.set_box_aspect((8, 4, 1))
        # ax.set_box_aspect((4, 4, 7))


        # prism - fractal color gradient
        # viridis - simple color gradient
        # plasma - simple color gradient

        if color_map_3D == "1":
            ax.plot_surface(X, Y, W, rstride=1, cstride=1, cmap=cm.prism)
        if color_map_3D == "2":
            ax.plot_surface(X, Y, W, rstride=1, cstride=1, cmap=cm.jet)
        if color_map_3D == "3":
            ax.plot_surface(X, Y, W, rstride=1, cstride=1, cmap=cm.plasma)
        if color_map_3D == "4":
            ax.plot_surface(X, Y, W, rstride=1, cstride=1, cmap=cm.viridis)
        if color_map_3D == "5":
            ax.plot_surface(X, Y, W, rstride=1, cstride=1, cmap=cm.twilight_shifted)


        # ax.plot_surface(X, Y, W, rstride=1, cstride=1, cmap=cm.prism)
        # ax.plot_wireframe(X, Y, W, rstride=5, cstride=5)
        #
        # ax.set_xlim(0, 18)  # Adjust the limits as needed
        # ax.set_ylim(-4, 4)  # Adjust the limits as needed
        # ax.set_zlim(0, 2)  # Adjust the limits as needed

        # Adjust grid line size
        # ax.tick_params(axis='both', which='major', pad=10, width=2)  # You can adjust pad and width as needed

        ax.set_xlabel('Real Axis')
        ax.set_ylabel('Imaginary Axis')
        ax.set_zlabel('Value')
        ax.set_title(f"Product of Sin(x) via Sin(x) product Representation")
        plt.draw()
        plt.show()

        return

# -----------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    """
    If name main, main function for the SpecialFunctions and ComplexPlotting Classes
    Initializes SpecialFunctions() object, and ComplexPlotting() object
    the SpecialFunctions() object is plotted on the ComplexPlotting() object
    with the create_plot_2D() or create_plot_3D() method
    """

    # get user input for plot type
    plot_type = input("Enter 2D for 2D plot, 3D for 3D plot, or PyQt for PyQt plot: ")

    # Check if the input is valid
    while plot_type not in ["2D", "3D", "PyQt"]:
        print("Invalid input. Please enter either '2D', '3D', or 'PyQt'.")
        plot_type = input("Enter 2D for 2D plot, 3D for 3D plot, or PyQt for PyQt plot: ")

    # instantiate the objects
    special_functions_object = Special_Functions(plot_type)
    complex_plotting_object = Complex_Plotting(plot_type)

    # ------------------------------------------------------------------------------------------------------------
    # 2D Plotting Menu
    if plot_type == "2D":
        color_map_dict = \
            {
             "1": "prism",
             "2": "jet",
             "3": "plasma",
             "4": "viridis",
             "5": "magma",
             "6": "custom_colors1",
             "7": "custom_colors2_exp",
             "8": "custom_colors3_exp",
            }
        print("Here are the color map functions, please enter the number on the left")
        print("to choose that color for the render.")

        for key in color_map_dict:
            print(f'"{key}" : "{color_map_dict[key]}"')
        # Get x-axis min range from user input
        color_map_2D = input('Select color map python default or custom: \n')

        # get user input for plot type
        print("Utilize exponential product normalization (Y/N)?")
        Normalize_type = input()

    # if user selected 2D plot, graph the plot with the given values
    if plot_type == "2D":
        complex_plotting_object.create_plot_2D(color_map_2D, Normalize_type)

    # ------------------------------------------------------------------------------------------------------------
    # 3D Plotting Menu
    if plot_type == "3D":
        color_map_dict = \
            {
             "1": "prism",
             "2": "jet",
             "3": "plasma",
             "4": "viridis",
             "5": "magma",
            }
        print("Here are the color map functions, please enter the number on the left")
        print("to choose that color for the render.")

        for key in color_map_dict:
            print(f'"{key}" : "{color_map_dict[key]}"')
        # Get x-axis min range from user input
        color_map_3D = input('Select color map python default or custom: \n')

        # get user input for plot type
        print("Utilize exponential product normalization (Y/N)?")
        Normalize_type = input()

    # if user selected 2D plot, graph the plot with the given values
    if plot_type == "3D":
        complex_plotting_object.create_plot_3D(color_map_3D, Normalize_type)

    # # if user selected 3D plot with accelerated GPU processing, graph the plot with the given values
    # if plot_type == "3D":
    #     complex_plotting_object.create_plot_3D_GPU(color_map_3D)

