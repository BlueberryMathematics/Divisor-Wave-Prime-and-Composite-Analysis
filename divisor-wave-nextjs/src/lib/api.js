/**
 * API client for Divisor Wave Complex Analysis backend
 */

import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 second timeout for complex computations
  headers: {
    'Content-Type': 'application/json',
  },
});

// API Functions for Divisor Wave Analysis
export const divisorWaveAPI = {
  // Get all available functions
  getFunctions: async () => {
    const response = await api.get('/functions');
    return response.data;
  },

  // Get detailed information about a specific function
  getFunctionInfo: async (functionId) => {
    const response = await api.get(`/function/${functionId}`);
    return response.data;
  },

  // Evaluate function at specific points
  evaluateFunction: async (functionId, points, normalize = false) => {
    const response = await api.post('/evaluate-function', {
      function_id: functionId,
      points,
      normalize,
    });
    return response.data;
  },

  // Get plotting data for visualization
  getPlotData: async (request) => {
    const response = await api.post('/plot-data', request);
    return response.data;
  },

  // LaTeX conversion endpoints
  convertLatexToNumpy: async (latexFormula, functionName = null, description = null) => {
    const response = await api.post('/latex-to-numpy', {
      latex_formula: latexFormula,
      function_name: functionName || `custom_${Date.now()}`,
      description: description || 'Custom function from LaTeX input',
      custom_parameters: {}
    });
    return response.data;
  },

  // Get LaTeX patterns
  getLatexPatterns: async () => {
    const response = await api.get('/latex-patterns');
    return response.data;
  },

  // Database operations
  listDatabaseFunctions: async () => {
    const response = await api.get('/database/list');
    return response.data;
  },

  getDatabaseFunction: async (functionName) => {
    const response = await api.get(`/database/function/${functionName}`);
    return response.data;
  },

  // Health check
  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },

  // Generate real-time plot for specific divisor wave functions
  generateDivisorWavePlot: async (functionId = 'product_of_sin', options = {}) => {
    const request = {
      function_id: functionId,
      x_range: options.xRange || [1, 15],
      y_range: options.yRange || [0, 15], 
      resolution: options.resolution || 50,
      normalize: options.normalize || false,
      plot_type: options.plotType || '3D'
    };
    
    return await api.post('/plot-data', request);
  },

  // Evaluate divisor wave functions at prime/composite points
  checkPrimeCompositePattern: async (functionId = 'product_of_sin', maxN = 20) => {
    const points = [];
    for (let i = 2; i <= maxN; i++) {
      points.push([i, 0]); // Real axis points
    }
    
    return await api.post('/evaluate-function', {
      function_id: functionId,
      points,
      normalize: false
    });
  },
};

// Error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    
    if (error.response?.status === 404) {
      throw new Error('Function not found');
    } else if (error.response?.status === 400) {
      throw new Error(error.response.data?.detail || 'Invalid request');
    } else if (error.code === 'ECONNREFUSED') {
      throw new Error('Cannot connect to backend server. Please ensure the Python API is running on port 8000.');
    } else if (error.code === 'TIMEOUT') {
      throw new Error('Request timed out. Complex calculations may take longer.');
    }
    
    throw error;
  }
);

export default api;