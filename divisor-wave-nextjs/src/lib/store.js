/**
 * Zustand store for application state management
 */

import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

const defaultVisualizationSettings = {
  colormap: 'viridis',
  resolution: 50,
  xRange: [-10, 10],
  yRange: [-10, 10],
  showAxes: true,
  showGrid: true,
  normalize: false,
  animationSpeed: 1.0,
  lightingIntensity: 0.8,
};

export const useAppStore = create()(
  devtools(
    (set, get) => ({
      // Initial state
      functions: {},
      selectedFunction: null,
      functionLoading: false,
      
      plotData: null,
      plotLoading: false,
      plotError: null,
      
      visualizationSettings: defaultVisualizationSettings,
      
      sidebarOpen: true,
      currentView: '3d',
      
      // Actions
      setFunctions: (functions) => set({ functions }),
      
      setSelectedFunction: (functionId) => set({ 
        selectedFunction: functionId,
        plotData: null,
        plotError: null,
      }),
      
      setFunctionLoading: (loading) => set({ functionLoading: loading }),
      
      setPlotData: (data) => set({ 
        plotData: data,
        plotLoading: false,
        plotError: null,
      }),
      
      setPlotLoading: (loading) => set({ plotLoading: loading }),
      
      setPlotError: (error) => set({ 
        plotError: error,
        plotLoading: false,
      }),
      
      updateVisualizationSettings: (settings) => set((state) => ({
        visualizationSettings: {
          ...state.visualizationSettings,
          ...settings,
        },
      })),
      
      resetVisualizationSettings: () => set({
        visualizationSettings: defaultVisualizationSettings,
      }),
      
      setSidebarOpen: (open) => set({ sidebarOpen: open }),
      
      setCurrentView: (view) => set({ currentView: view }),
    }),
    {
      name: 'divisor-wave-store',
    }
  )
);

// Selectors for derived state
export const useSelectedFunctionInfo = () => {
  const { functions, selectedFunction } = useAppStore((state) => ({
    functions: state.functions,
    selectedFunction: state.selectedFunction,
  }));
  
  return selectedFunction ? functions[selectedFunction] : null;
};

export const usePlotSettings = () => {
  const { visualizationSettings, selectedFunction } = useAppStore((state) => ({
    visualizationSettings: state.visualizationSettings,
    selectedFunction: state.selectedFunction,
  }));
  
  return {
    ...visualizationSettings,
    functionId: selectedFunction,
  };
};