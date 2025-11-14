/**
 * Compact Graphing Calculator Interface
 * Minimal scrolling, dropdown organization, integrated custom functions
 */

'use client';

import { useEffect, useState } from 'react';
import LaTeXFunctionBuilder from './LaTeXFunctionBuilder';

// Import KaTeX for LaTeX rendering
import 'katex/dist/katex.min.css';
import { InlineMath, BlockMath } from 'react-katex';

export default function CompactCalculator() {
  // State to prevent hydration mismatch
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  // Core state
  const [connectionStatus, setConnectionStatus] = useState('checking');
  const [functions, setFunctions] = useState({});
  const [selectedFunction, setSelectedFunction] = useState('builtin_1');  // Will resolve to 'product_of_sin'
  const [plotImage, setPlotImage] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [functionData, setFunctionData] = useState(null);
  const [debugInfo, setDebugInfo] = useState([]);
  
  // Settings - Complete set matching Special_Functions.py
  const [plotType, setPlotType] = useState('2D_Complex');
  const [normalizeType, setNormalizeType] = useState('Y');
  const [xRange, setXRange] = useState([2, 28]);
  const [yRange, setYRange] = useState([-5, 5]);
  const [zRange, setZRange] = useState([-10, 10]); // Added Z-range for 3D plots
  const [resolution, setResolution] = useState(750);
  const [colormap, setColormap] = useState('4');
  const [canvasSize, setCanvasSize] = useState('16x9');
  const [lightShading, setLightShading] = useState(false);
  const [axisTick, setAxisTick] = useState(1.0);
  const [titleOverride, setTitleOverride] = useState('');
  
  // Coefficient controls for aesthetic plot scaling
  const [mCoefficient, setMCoefficient] = useState(0.36);
  const [betaCoefficient, setBetaCoefficient] = useState(0.1468);
  
  // Custom function state
  const [showLatexBuilder, setShowLatexBuilder] = useState(false);
  const [customFunctions, setCustomFunctions] = useState({});
  
  // LaTeX formula display state
  const [latexFormula, setLatexFormula] = useState('');
  const [latexDescription, setLatexDescription] = useState('');
  const [showLatexOnSave, setShowLatexOnSave] = useState(false);
  const [showLatexInspector, setShowLatexInspector] = useState(false);
  
  // Performance optimization controls
  const [useOptimizedPlotter, setUseOptimizedPlotter] = useState(true);
  const [enableGPU, setEnableGPU] = useState(true);
  const [performanceMode, setPerformanceMode] = useState('balanced'); // 'fast', 'balanced', 'quality'

  // UI state for draggable status bar and fullscreen
  const [statusBarHeight, setStatusBarHeight] = useState(30);
  const [isDragging, setIsDragging] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [isStatusBarMinimized, setIsStatusBarMinimized] = useState(true);

  const API_BASE = 'http://localhost:8000';

  // Helper function to extract original function name from prefixed value
  const getOriginalFunctionName = (prefixedValue) => {
    if (prefixedValue.startsWith('builtin_')) {
      const functionId = prefixedValue.substring(8); // Remove 'builtin_' prefix to get ID
      // Look up the actual function name by ID
      for (const [category, categoryFunctions] of Object.entries(functions)) {
        for (const [id, funcInfo] of Object.entries(categoryFunctions)) {
          if (id === functionId) {
            return funcInfo.name; // Return the actual function name
          }
        }
      }
      return functionId; // Fallback to ID if not found
    } else if (prefixedValue.startsWith('custom_')) {
      return prefixedValue.substring(7); // Remove 'custom_' prefix
    }
    return prefixedValue; // Fallback for old format
  };

  // Helper function to check if function is custom
  const isCustomFunction = (prefixedValue) => {
    return prefixedValue.startsWith('custom_');
  };

  // Add debug log
  const addDebugLog = (message, type = 'info') => {
    const timestamp = new Date().toLocaleTimeString();
    setDebugInfo(prev => [...prev.slice(-4), { timestamp, message, type }]);
  };

  // Check backend connection
  const checkConnection = async () => {
    try {
      const response = await fetch(`${API_BASE}/health`);
      const data = await response.json();
      
      if (response.ok) {
        setConnectionStatus('connected');
        addDebugLog('Backend connected', 'success');
        return true;
      } else {
        throw new Error('Backend error');
      }
    } catch (error) {
      setConnectionStatus('disconnected');
      addDebugLog(`Connection failed: ${error.message}`, 'error');
      return false;
    }
  };

  // Load functions from API
  const loadFunctions = async () => {
    try {
      const response = await fetch(`${API_BASE}/functions`);
      const data = await response.json();
      // The API returns functions directly organized by category
      setFunctions(data || {});
      addDebugLog(`Loaded ${Object.keys(data || {}).length} categories`, 'success');
    } catch (error) {
      addDebugLog(`Failed to load functions: ${error.message}`, 'error');
    }
  };

  // Load custom functions
  const loadCustomFunctions = async () => {
    try {
      const response = await fetch(`${API_BASE}/custom-functions`);
      const data = await response.json();
      setCustomFunctions(data.functions || {});
    } catch (error) {
      console.log('No custom functions found');
    }
  };

  // Handle custom function creation
  const handleFunctionCreated = async (functionData) => {
    try {
      const response = await fetch(`${API_BASE}/custom-functions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(functionData)
      });
      
      if (response.ok) {
        addDebugLog(`Custom function "${functionData.name}" created`, 'success');
        loadCustomFunctions();
        setSelectedFunction(`custom_${functionData.name}`);
        setShowLatexBuilder(false);
      }
    } catch (error) {
      addDebugLog(`Failed to create function: ${error.message}`, 'error');
    }
  };

  // Delete custom function
  const deleteCustomFunction = async (functionName) => {
    if (!window.confirm(`Delete "${functionName}"?`)) return;
    
    try {
      const response = await fetch(`${API_BASE}/custom-functions/${functionName}`, {
        method: 'DELETE'
      });
      
      if (response.ok) {
        addDebugLog(`Function "${functionName}" deleted`, 'success');
        loadCustomFunctions();
        if (selectedFunction === `custom_${functionName}`) {
          setSelectedFunction('builtin_1');  // Will resolve to 'product_of_sin'
        }
      }
    } catch (error) {
      addDebugLog(`Failed to delete function: ${error.message}`, 'error');
    }
  };

  // Drag handlers for status bar with snap-to-close
  const handleDragStart = (e) => {
    console.log('Drag start triggered', e.target);
    e.preventDefault();
    e.stopPropagation();
    
    const startY = e.clientY;
    const startHeight = statusBarHeight;
    let isCurrentlyDragging = true;
    let hasMoved = false; // Track if user actually dragged
    let currentHeight = startHeight;
    let animationFrame = null;
    
    // Get reference to the status bar element for direct manipulation
    const statusBarElement = e.target.closest('[data-status-bar]');
    
    console.log('Start Y:', startY, 'Start Height:', startHeight);
    
    const updateHeight = (newHeight) => {
      currentHeight = newHeight;
      // Update DOM directly for smooth movement
      if (statusBarElement) {
        statusBarElement.style.height = `${newHeight}px`;
      }
      // Throttle React state updates for better performance
      if (animationFrame) {
        cancelAnimationFrame(animationFrame);
      }
      animationFrame = requestAnimationFrame(() => {
        setStatusBarHeight(newHeight);
        // Update minimized state during drag
        setIsStatusBarMinimized(newHeight <= 40);
      });
    };
    
    const handleMove = (moveEvent) => {
      if (!isCurrentlyDragging) return;
      moveEvent.preventDefault();
      
      const deltaY = startY - moveEvent.clientY; // Invert for bottom-up dragging
      let newHeight = startHeight + deltaY;
      
      // Mark as moved if significant movement
      if (Math.abs(deltaY) > 3) {
        hasMoved = true;
      }
      
      // Constrain height but don't auto-snap during drag
      newHeight = Math.max(25, Math.min(600, newHeight));
      
      // Update height smoothly
      updateHeight(newHeight);
    };
    
    const handleEnd = () => {
      console.log('Drag end triggered, hasMoved:', hasMoved);
      isCurrentlyDragging = false;
      document.removeEventListener('mousemove', handleMove);
      document.removeEventListener('mouseup', handleEnd);
      
      // Cancel any pending animation frame
      if (animationFrame) {
        cancelAnimationFrame(animationFrame);
      }
      
      // Only apply snapping if user actually dragged
      if (hasMoved) {
        // More forgiving snap zones
        if (currentHeight < 60) {
          // Snap to minimized state
          currentHeight = 30;
          setIsStatusBarMinimized(true);
          addDebugLog('Status bar snapped to minimized', 'info');
        } else if (currentHeight < 120) {
          // Snap to default height
          currentHeight = 200;
          setIsStatusBarMinimized(false);
          addDebugLog('Status bar snapped to default height', 'info');
        } else {
          // Keep current height but ensure not minimized
          setIsStatusBarMinimized(false);
        }
        
        // Smooth transition to final height
        if (statusBarElement) {
          statusBarElement.style.transition = 'height 0.2s ease-out';
          statusBarElement.style.height = `${currentHeight}px`;
          setTimeout(() => {
            statusBarElement.style.transition = '';
          }, 200);
        }
        
        setStatusBarHeight(currentHeight);
      }
      
      setIsDragging(false);
    };
    
    document.addEventListener('mousemove', handleMove);
    document.addEventListener('mouseup', handleEnd);
    setIsDragging(true);
    addDebugLog('Status bar drag started', 'info');
  };

  // Toggle status bar
  const toggleStatusBar = (e) => {
    console.log('Toggle status bar triggered, current minimized:', isStatusBarMinimized);
    e?.preventDefault();
    e?.stopPropagation();
    
    if (isStatusBarMinimized) {
      setStatusBarHeight(200);
      setIsStatusBarMinimized(false);
      addDebugLog('Status bar expanded via toggle', 'info');
    } else {
      setStatusBarHeight(30);
      setIsStatusBarMinimized(true);
      addDebugLog('Status bar minimized via toggle', 'info');
    }
  };

  // Fullscreen handlers
  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);
  };

  const exitFullscreen = () => {
    setIsFullscreen(false);
  };

  // Fetch LaTeX formula for selected function
  const fetchLatexFormula = async (functionName, normalizeType = 'N') => {
    try {
      // Extract the actual function name from selected function using the same logic as getOriginalFunctionName
      const actualFunctionName = getOriginalFunctionName(functionName);

      addDebugLog(`Fetching LaTeX for: ${actualFunctionName}`, 'info');
      const response = await fetch(`http://localhost:8000/latex/formula/ui/${actualFunctionName}?normalize_type=${normalizeType}`);
      
      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          setLatexFormula(data.formula || '');
          setLatexDescription(data.description || '');
          addDebugLog(`LaTeX formula loaded for ${actualFunctionName}`, 'success');
        } else {
          setLatexFormula('');
          setLatexDescription('');
          addDebugLog(`LaTeX API returned success=false for ${actualFunctionName}`, 'warn');
        }
      } else {
        setLatexFormula('');
        setLatexDescription('');
        addDebugLog(`LaTeX API failed (${response.status}) for ${actualFunctionName}`, 'error');
      }
    } catch (error) {
      console.error('Error fetching LaTeX formula:', error);
      setLatexFormula('');
      setLatexDescription('');
      addDebugLog(`Error fetching LaTeX formula: ${error.message}`, 'error');
    }
  };

  // Copy LaTeX to clipboard
  const copyLatexToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(latexFormula);
      addDebugLog('LaTeX formula copied to clipboard', 'success');
    } catch (error) {
      // Fallback for older browsers
      const textArea = document.createElement('textarea');
      textArea.value = latexFormula;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      addDebugLog('LaTeX formula copied to clipboard', 'success');
    }
  };

  // Toggle LaTeX inspector
  const toggleLatexInspector = () => {
    setShowLatexInspector(!showLatexInspector);
  };

  // Generate plot
  const generatePlot = async () => {
    if (connectionStatus !== 'connected') {
      addDebugLog('Backend not connected', 'error');
      return;
    }

    setIsGenerating(true);
    const functionName = getOriginalFunctionName(selectedFunction);
    addDebugLog(`Generating ${plotType} plot for: ${functionName}`, 'info');

    try {
      // Map frontend colormap numbers to backend colormap names
      const colormapMapping = {
        '1': 'prism',
        '2': 'jet', 
        '3': 'plasma',
        '4': 'viridis',
        '5': 'magma',
        '6': 'rainbow',
        '7': 'rainbow',
        '8': 'rainbow'
      };

      // Adjust resolution based on plot type and performance mode
      let effectiveResolution = resolution;
      
      if (plotType === '3D_Complex') {
        // For 3D plots, use step size instead of point count
        // Original used 0.0199, scale based on resolution setting
        const resolutionScale = resolution / 750; // 750 is our base resolution
        effectiveResolution = 0.0199 / resolutionScale;
        effectiveResolution = Math.max(0.005, Math.min(0.05, effectiveResolution)); // Clamp to reasonable range
      } else {
        // For 2D plots, use the user's chosen resolution
        // Performance mode only affects optimization features, not resolution
        effectiveResolution = resolution;
      }

      // Choose endpoint based on optimization settings
      const endpoint = useOptimizedPlotter ? '/plot-optimized' : '/plot';
      addDebugLog(`Using ${useOptimizedPlotter ? 'optimized' : 'standard'} plotter (${performanceMode} mode)`, 'info');
      addDebugLog(`Resolution: ${plotType === '3D_Complex' ? 'step size' : 'points'} = ${effectiveResolution}`, 'info');

      // Use appropriate ranges for plot type (from original code)
      let plotXRange = xRange;
      let plotYRange = yRange;
      
      if (plotType === '3D_Complex') {
        // Use original 3D ranges if current ranges are 2D defaults
        if (xRange[0] === 2 && xRange[1] === 28) {
          plotXRange = [1.5, 18.5];
        }
        if (yRange[0] === -5 && yRange[1] === 5) {
          plotYRange = [-4.5, 4.5];
        }
      }
      
      addDebugLog(`Plot ranges: x[${plotXRange[0]}, ${plotXRange[1]}], y[${plotYRange[0]}, ${plotYRange[1]}]`, 'info');

      const response = await fetch(`${API_BASE}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          function_name: getOriginalFunctionName(selectedFunction),
          plot_type: plotType,
          normalize_type: normalizeType,
          x_range: plotXRange,
          y_range: plotYRange,
          resolution: effectiveResolution,
          colormap: colormapMapping[colormap] || 'viridis',
          canvas_size: canvasSize === '16x9' ? [512, 288] : canvasSize === '4x3' ? [512, 384] : [512, 512],
          light_shading: lightShading,
          axis_tick: axisTick,
          title_override: titleOverride || null
        })
      });

      const data = await response.json();
      
      if (response.ok) {
        addDebugLog(`Response data keys: ${Object.keys(data).join(', ')}`, 'info');
        addDebugLog(`Image data length: ${data.image ? data.image.length : 'undefined'}`, 'info');
        
        // Show performance information if available
        if (data.metadata?.computation_time) {
          addDebugLog(`⏱️ Computation time: ${data.metadata.computation_time.toFixed(3)}s`, 'success');
        }
        if (data.metadata?.performance) {
          addDebugLog(`🚀 Performance: ${data.metadata.performance}`, 'success');
        }
        if (data.metadata?.optimization?.gpu_used) {
          addDebugLog(`🎮 GPU acceleration: ${data.metadata.optimization.gpu_used ? 'Enabled' : 'Disabled'}`, 'info');
        }
        
        setPlotImage(data.image);  // Backend already includes data:image/png;base64, prefix
        setFunctionData(data);
        addDebugLog('Plot generated successfully', 'success');
      } else {
        throw new Error(data.detail || 'Plot generation failed');
      }
    } catch (error) {
      addDebugLog(`Plot failed: ${error.message}`, 'error');
    } finally {
      setIsGenerating(false);
    }
  };

  // Create dropdown options for functions
  const createFunctionOptions = () => {
    const options = [];
    
    // Define category order and display names
    const categoryOrder = [
      { key: 'core', name: '🎯 Core Divisor Waves', description: 'Primary a(z) and b(z) functions' },
      { key: 'composite', name: '🔄 Composite Functions', description: 'cos/sin of core functions' },
      { key: 'riesz', name: '🌊 Riesz Products', description: 'Infinite products with trigonometric terms' },
      { key: 'viete', name: '⭐ Viète Products', description: 'Products with powers of 2' },
      { key: 'special', name: '🔬 Special Functions', description: 'Prime indicators and advanced combinations' },
      { key: 'basic', name: '⚙️ Basic Functions', description: 'Fundamental mathematical operations' }
    ];
    
    // Organize functions by category
    const categorizedFunctions = {
      core: [],
      composite: [],
      riesz: [],
      viete: [],
      special: [],
      basic: []
    };
    
    // Built-in functions - categorize by function name patterns
    Object.entries(functions).forEach(([category, categoryFunctions]) => {
      Object.entries(categoryFunctions).map(([funcId, funcInfo]) => {
        const funcName = funcInfo.name;
        let targetCategory = 'special'; // default
        
        // Categorize based on function name
        if ((funcName.includes('product_of_sin') || funcName.includes('product_of_product_representation_for_sin')) && !funcName.includes('cos_of') && !funcName.includes('sin_of')) {
          targetCategory = 'core';
        } else if (funcName.includes('cos_of') || funcName.includes('sin_of')) {
          targetCategory = 'composite';
        } else if (funcName.includes('Riesz')) {
          targetCategory = 'riesz';
        } else if (funcName.includes('Viete')) {
          targetCategory = 'viete';
        } else if (funcName.includes('BASIC')) {
          targetCategory = 'basic';
        }
        
        categorizedFunctions[targetCategory].push({
          value: `builtin_${funcId}`,
          originalValue: funcId,
          label: `${funcId}: ${funcInfo.name}`,
          category: targetCategory,
          isCustom: false,
          sortOrder: parseInt(funcId)
        });
      });
    });
    
    // Sort functions within each category by ID
    Object.keys(categorizedFunctions).forEach(cat => {
      categorizedFunctions[cat].sort((a, b) => a.sortOrder - b.sortOrder);
    });
    
    // Build options with category headers
    categoryOrder.forEach(({ key, name, description }) => {
      if (categorizedFunctions[key].length > 0) {
        // Add category header (disabled option)
        options.push({
          value: `header_${key}`,
          label: `${name} (${categorizedFunctions[key].length} functions)`,
          isHeader: true,
          disabled: true
        });
        
        // Add functions in this category
        options.push(...categorizedFunctions[key]);
      }
    });
    
    // Custom functions section
    const customEntries = Object.entries(customFunctions);
    if (customEntries.length > 0) {
      options.push({
        value: 'header_custom',
        label: `🎨 Custom Functions (${customEntries.length} functions)`,
        isHeader: true,
        disabled: true
      });
      
      customEntries.forEach(([funcName, funcData]) => {
        options.push({
          value: `custom_${funcName}`,
          originalValue: funcName,
          label: `${funcName}: ${funcData.description || 'Custom function'}`,
          category: 'Custom',
          isCustom: true
        });
      });
    }
    
    return options;
  };

  // Load data on mount
  useEffect(() => {
    checkConnection();
    const interval = setInterval(checkConnection, 30000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (connectionStatus === 'connected') {
      loadFunctions();
      loadCustomFunctions();
    }
  }, [connectionStatus]);

  // Fetch LaTeX formula when function or normalize type changes
  useEffect(() => {
    if (connectionStatus === 'connected' && selectedFunction) {
      fetchLatexFormula(selectedFunction, normalizeType);
    }
  }, [selectedFunction, normalizeType, connectionStatus]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      // ESC to exit fullscreen
      if (e.key === 'Escape' && isFullscreen) {
        exitFullscreen();
      }
      // F11 or F to toggle fullscreen (when plot is visible)
      if ((e.key === 'F11' || e.key === 'f') && plotImage && !showLatexBuilder) {
        e.preventDefault();
        toggleFullscreen();
      }
      // G to generate plot
      if (e.key === 'g' && !showLatexBuilder && !isFullscreen) {
        generatePlot();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isFullscreen, plotImage, showLatexBuilder]);

  const functionOptions = createFunctionOptions();

  // Prevent hydration mismatch by only rendering on client
  if (!isClient) {
    return <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 text-white flex items-center justify-center">
      <div className="text-lg">Loading...</div>
    </div>;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 text-white">
      {/* Compact Header */}
      <header className="bg-black/20 backdrop-blur-sm border-b border-white/10 p-3">
        <div className="max-w-7xl mx-auto">
          <div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              Compact Mathematical Calculator
            </h1>
            <p className="text-gray-300 text-xs">Ultra-compact interface • No scrolling • Smart organization</p>
          </div>
        </div>
      </header>

      <div 
        className="max-w-full mx-auto p-4 transition-all duration-300"
        style={{ paddingBottom: `${statusBarHeight + 16}px` }}
      >
        <div className="grid grid-cols-1 xl:grid-cols-5 gap-4">
          
          {/* LEFT: Controls Panel - More compact */}
          <div className="xl:col-span-1 space-y-4">
            
            {/* Function Selection */}
            <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-lg p-3">
              <label className="block text-xs font-medium mb-2 text-blue-400">📊 FUNCTION</label>
              
              <div className="space-y-2">
                {/* Function Dropdown */}
                <select
                  value={selectedFunction}
                  onChange={(e) => setSelectedFunction(e.target.value)}
                  className="w-full px-2 py-1 bg-gray-800 border border-gray-600 rounded-lg text-xs"
                >
                  {functionOptions.map((option, index) => (
                    <option 
                      key={`${option.value}_${index}`} 
                      value={option.value}
                      disabled={option.disabled || option.isHeader}
                      className={option.isHeader ? 'font-bold bg-gray-700 text-blue-300' : ''}
                    >
                      {option.label}
                    </option>
                  ))}
                </select>
                
                {/* Add Function Button */}
                <button
                  onClick={() => setShowLatexBuilder(true)}
                  className="w-full px-3 py-1 bg-purple-600 hover:bg-purple-700 rounded-lg text-xs font-medium transition-colors"
                  title="Create Custom Function"
                >
                  ➕ Add Custom Function
                </button>
                
                {/* Custom function management */}
                {functionOptions.find(f => f.value === selectedFunction && f.isCustom) && (
                  <button
                    onClick={() => deleteCustomFunction(getOriginalFunctionName(selectedFunction))}
                    className="w-full px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg text-sm font-medium transition-colors"
                  >
                    🗑️ Delete Custom Function
                  </button>
                )}
              </div>
            </div>

            {/* Plot Mode Selection */}
            <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-lg p-3">
              <label className="block text-xs font-medium mb-2 text-orange-400">🎮 PLOT MODE</label>
              <select
                value={plotType}
                onChange={(e) => setPlotType(e.target.value)}
                className="w-full px-2 py-1 bg-gray-800 border border-gray-600 rounded-lg text-xs"
              >
                <option value="2D_Real">2D Real Plot</option>
                <option value="2D_Complex">2D Complex Plot</option>
                <option value="3D_Real">3D Real Plot</option>
                <option value="3D_Complex">3D Complex Plot</option>
              </select>
            </div>

            {/* Window & Style Settings */}
            <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-lg p-4">
              <div className="space-y-4">
                
                {/* Window Settings */}
                <div>
                  <label className="block text-xs font-medium mb-2 text-green-400">📐 WINDOW RANGE</label>
                  <div className="space-y-3">
                    {/* X Range */}
                    <div>
                      <label className="block text-xs text-gray-300 mb-1">X-Axis Range</label>
                      <div className="grid grid-cols-2 gap-2">
                        <input
                          type="number"
                          value={xRange[0]}
                          onChange={(e) => setXRange([parseFloat(e.target.value) || 0, xRange[1]])}
                          placeholder="X min"
                          className="px-2 py-1 bg-gray-800 border border-gray-600 rounded text-xs"
                          title="X-axis minimum value"
                        />
                        <input
                          type="number"
                          value={xRange[1]}
                          onChange={(e) => setXRange([xRange[0], parseFloat(e.target.value) || 0])}
                          placeholder="X max"
                          className="px-2 py-1 bg-gray-800 border border-gray-600 rounded text-xs"
                          title="X-axis maximum value"
                        />
                      </div>
                    </div>
                    
                    {/* Y Range */}
                    <div>
                      <label className="block text-xs text-gray-300 mb-1">Y-Axis Range</label>
                      <div className="grid grid-cols-2 gap-2">
                        <input
                          type="number"
                          value={yRange[0]}
                          onChange={(e) => setYRange([parseFloat(e.target.value) || 0, yRange[1]])}
                          placeholder="Y min"
                          className="px-2 py-2 bg-gray-800 border border-gray-600 rounded text-sm"
                          title="Y-axis minimum value"
                        />
                        <input
                          type="number"
                          value={yRange[1]}
                          onChange={(e) => setYRange([yRange[0], parseFloat(e.target.value) || 0])}
                          placeholder="Y max"
                          className="px-2 py-2 bg-gray-800 border border-gray-600 rounded text-sm"
                          title="Y-axis maximum value"
                        />
                      </div>
                    </div>
                    
                    {/* Z Range - Only show for 3D plots */}
                    {plotType.includes('3D') && (
                      <div>
                        <div className="flex items-center justify-between mb-1">
                          <label className="block text-xs text-blue-300">Z-Axis Range (3D)</label>
                          <button
                            onClick={() => setZRange([0, 0])} // Set to 0,0 to trigger auto-range
                            className="px-2 py-1 bg-blue-600 hover:bg-blue-700 rounded text-xs transition-colors"
                            title="Auto-calculate optimal Z range based on function values"
                          >
                            Auto
                          </button>
                        </div>
                        <div className="grid grid-cols-2 gap-2">
                          <input
                            type="number"
                            value={zRange[0]}
                            onChange={(e) => setZRange([parseFloat(e.target.value) || 0, zRange[1]])}
                            placeholder="Z min"
                            className="px-2 py-2 bg-gray-800 border border-blue-600 rounded text-sm"
                            title="Z-axis minimum value (3D only)"
                          />
                          <input
                            type="number"
                            value={zRange[1]}
                            onChange={(e) => setZRange([zRange[0], parseFloat(e.target.value) || 0])}
                            placeholder="Z max"
                            className="px-2 py-2 bg-gray-800 border border-blue-600 rounded text-sm"
                            title="Z-axis maximum value (3D only)"
                          />
                        </div>
                        {zRange[0] === zRange[1] && (
                          <div className="text-xs text-blue-300 mt-1">
                            ℹ️ Auto Z-range enabled - will be calculated from function values
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>

                {/* Style Settings */}
                <div>
                  <label className="block text-xs font-medium mb-2 text-purple-400">🎨 VISUAL STYLE</label>
                  <div className="space-y-3">
                    <div>
                      <label className="block text-xs text-gray-300 mb-1">Resolution</label>
                      <select
                        value={resolution}
                        onChange={(e) => setResolution(parseInt(e.target.value))}
                        className="w-full px-2 py-1 bg-gray-800 border border-gray-600 rounded text-xs"
                      >
                        <option value={100}>100×100 (Fast)</option>
                        <option value={200}>200×200 (Normal)</option>
                        <option value={400}>400×400 (High)</option>
                        <option value={600}>600×600 (Ultra)</option>
                        <option value={750}>750×750 (Original)</option>
                      </select>
                    </div>
                    
                    <div>
                      <label className="block text-xs text-gray-300 mb-1">Color Scheme</label>
                      <select
                        value={colormap}
                        onChange={(e) => setColormap(e.target.value)}
                        className="w-full px-2 py-1 bg-gray-800 border border-gray-600 rounded text-xs"
                        title="Color scheme for the plot visualization"
                      >
                        <option value="1">Prism (Fast)</option>
                        <option value="2">Jet (Fast)</option>
                        <option value="3">Plasma (Fast)</option>
                        <option value="4">Viridis (Fast)</option>
                        <option value="5">Twilight (Fast)</option>
                        <option value="6">Custom Colors 2 (Vectorized)</option>
                        <option value="7">Custom Colors 3 (Vectorized)</option>
                        <option value="8">Custom Colors 1 (Vectorized)</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>

              {/* Advanced Options (Collapsible) */}
              <details className="mt-2">
                <summary className="text-xs text-gray-400 cursor-pointer hover:text-white font-medium">⚙️ Advanced Options</summary>
                <div className="mt-2 space-y-2">
                  
                  {/* Compact Grid Layout */}
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    {/* Normalization */}
                    <div>
                      <label className="block text-xs mb-1">Normalize</label>
                      <select
                        value={normalizeType}
                        onChange={(e) => setNormalizeType(e.target.value)}
                        className="w-full px-1 py-1 bg-gray-800 border border-gray-600 rounded text-xs"
                      >
                        <option value="Y">Y-axis</option>
                        <option value="X">X-axis</option>
                        <option value="Z">Z-axis</option>
                        <option value="XYZ">All axes</option>
                        <option value="N">None</option>
                      </select>
                    </div>
                    
                    {/* Canvas Ratio */}
                    <div>
                      <label className="block text-xs mb-1">Ratio</label>
                      <select
                        value={canvasSize}
                        onChange={(e) => setCanvasSize(e.target.value)}
                        className="w-full px-1 py-1 bg-gray-800 border border-gray-600 rounded text-xs"
                      >
                        <option value="16x9">16:9</option>
                        <option value="4x3">4:3</option>
                        <option value="1x1">1:1</option>
                      </select>
                    </div>
                    
                    {/* M Coefficient */}
                    <div>
                      <label className="block text-xs mb-1 text-purple-300">M Coeff</label>
                      <input
                        type="number"
                        step="0.01"
                        value={mCoefficient}
                        onChange={(e) => setMCoefficient(parseFloat(e.target.value) || 0.36)}
                        className="w-full px-1 py-1 bg-gray-800 border border-gray-600 rounded text-xs"
                      />
                    </div>
                    
                    {/* Beta Coefficient */}
                    <div>
                      <label className="block text-xs mb-1 text-purple-300">Beta</label>
                      <input
                        type="number"
                        step="0.01"
                        value={betaCoefficient}
                        onChange={(e) => setBetaCoefficient(parseFloat(e.target.value) || 0.1468)}
                        className="w-full px-1 py-1 bg-gray-800 border border-gray-600 rounded text-xs"
                      />
                    </div>
                  </div>

                  {/* Single row for checkboxes and small inputs */}
                  <div className="grid grid-cols-3 gap-2 text-xs">
                    <div className="flex items-center space-x-1">
                      <input
                        type="checkbox"
                        checked={lightShading}
                        onChange={(e) => setLightShading(e.target.checked)}
                        className="w-3 h-3"
                      />
                      <label className="text-xs">3D Light</label>
                    </div>
                    
                    <div>
                      <label className="block text-xs mb-1">Tick</label>
                      <input
                        type="number"
                        step="0.1"
                        value={axisTick}
                        onChange={(e) => setAxisTick(parseFloat(e.target.value) || 1.0)}
                        className="w-full px-1 py-1 bg-gray-800 border border-gray-600 rounded text-xs"
                      />
                    </div>
                    
                    <div className="flex items-center space-x-1">
                      <input
                        type="checkbox"
                        checked={useOptimizedPlotter}
                        onChange={(e) => setUseOptimizedPlotter(e.target.checked)}
                        className="w-3 h-3"
                      />
                      <label className="text-xs">GPU</label>
                    </div>
                  </div>

                  {/* Custom Title - single line */}
                  <div>
                    <input
                      type="text"
                      value={titleOverride}
                      onChange={(e) => setTitleOverride(e.target.value)}
                      placeholder="Custom title (optional)"
                      className="w-full px-2 py-1 bg-gray-800 border border-gray-600 rounded text-xs"
                    />
                  </div>
                </div>
              </details>
            </div>

            {/* GRAPH Button */}
            <button
              onClick={generatePlot}
              disabled={isGenerating || connectionStatus !== 'connected'}
              className={`w-full py-4 rounded-lg text-lg font-bold transition-all ${
                isGenerating || connectionStatus !== 'connected'
                  ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                  : 'bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700 hover:scale-105 shadow-lg'
              }`}
            >
              {isGenerating ? '⏳ Computing...' : '📈 GENERATE PLOT'}
            </button>

            {/* Save Button - Only show when plot exists */}
            {plotImage && (
              <div className="space-y-2">
                {/* Include LaTeX formula option */}
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="include-latex"
                    checked={showLatexOnSave}
                    onChange={(e) => setShowLatexOnSave(e.target.checked)}
                    className="rounded"
                  />
                  <label htmlFor="include-latex" className="text-sm text-gray-300">
                    Include formula on plot
                  </label>
                </div>
                
                <button
                  onClick={async () => {
                    if (showLatexOnSave) {
                      // Generate a new plot with LaTeX formula included
                      addDebugLog('Generating plot with LaTeX formula for save...', 'info');
                      try {
                        // Use the same parameters as current plot but with show_latex enabled
                        const colormapMapping = {
                          '1': 'prism', '2': 'jet', '3': 'plasma', '4': 'viridis',
                          '5': 'magma', '6': 'rainbow', '7': 'rainbow', '8': 'rainbow'
                        };
                        
                        let effectiveResolution = resolution;
                        if (plotType === '3D_Complex') {
                          const resolutionScale = resolution / 750;
                          effectiveResolution = 0.0199 / resolutionScale;
                          effectiveResolution = Math.max(0.005, Math.min(0.05, effectiveResolution));
                        }
                        
                        let plotXRange = xRange;
                        let plotYRange = yRange;
                        if (plotType === '3D_Complex') {
                          if (xRange[0] === 2 && xRange[1] === 28) plotXRange = [1.5, 18.5];
                          if (yRange[0] === -5 && yRange[1] === 5) plotYRange = [-4.5, 4.5];
                        }
                        
                        const response = await fetch(`${API_BASE}/plot-optimized`, {
                          method: 'POST',
                          headers: { 'Content-Type': 'application/json' },
                          body: JSON.stringify({
                            function_name: getOriginalFunctionName(selectedFunction),
                            plot_type: plotType,
                            normalize_type: normalizeType,
                            x_range: plotXRange,
                            y_range: plotYRange,
                            resolution: effectiveResolution,
                            colormap: colormapMapping[colormap] || 'viridis',
                            canvas_size: canvasSize === '16x9' ? [512, 288] : canvasSize === '4x3' ? [512, 384] : [512, 512],
                            light_shading: lightShading,
                            axis_tick: axisTick,
                            title_override: titleOverride || null,
                            show_latex: true,  // Enable LaTeX for save
                            custom_latex: latexFormula  // Send the frontend's rendered LaTeX
                          })
                        });
                        
                        const data = await response.json();
                        if (response.ok && data.image) {
                          // Save the plot with LaTeX
                          const link = document.createElement('a');
                          link.href = data.image;
                          link.download = `${selectedFunction}_${plotType}_with_formula.png`;
                          link.click();
                          addDebugLog('Plot with LaTeX formula saved successfully', 'success');
                        } else {
                          throw new Error(data.error || 'Failed to generate plot with LaTeX');
                        }
                      } catch (error) {
                        addDebugLog(`Error saving plot with LaTeX: ${error.message}`, 'error');
                        // Fallback to regular save
                        const link = document.createElement('a');
                        link.href = plotImage;
                        link.download = `${selectedFunction}_${plotType}.png`;
                        link.click();
                      }
                    } else {
                      // Regular save without LaTeX
                      const link = document.createElement('a');
                      link.href = plotImage;
                      link.download = `${selectedFunction}_${plotType}.png`;
                      link.click();
                    }
                  }}
                  className="w-full py-3 bg-green-600 hover:bg-green-700 rounded-lg text-sm font-medium transition-colors"
                >
                  💾 Save Plot Image{showLatexOnSave ? ' + Formula' : ''}
                </button>
              </div>
            )}

          </div>

          {/* RIGHT: Large Plot Display */}
          <div className="xl:col-span-4">
            <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-lg p-4 min-h-[900px]">
              <div className="mb-3 flex justify-between items-center">
                <h3 className="text-lg font-bold">📊 DISPLAY</h3>
                <button
                  onClick={toggleFullscreen}
                  className="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-xs transition-colors"
                  title="Toggle fullscreen"
                >
                  {isFullscreen ? '🗗 Exit' : '🗖 Fullscreen'}
                </button>
              </div>

              <div className="relative">
                {plotImage ? (
                  <div className="relative group">
                    {/* Fullscreen button overlay on image */}
                    <button
                      onClick={toggleFullscreen}
                      className="absolute top-2 right-2 z-10 px-2 py-1 bg-black/70 hover:bg-black/90 rounded text-xs text-white opacity-0 group-hover:opacity-100 transition-opacity"
                      title="Toggle fullscreen"
                    >
                      {isFullscreen ? '🗗' : '🗖'}
                    </button>
                    
                    <img
                      src={plotImage}
                      alt={`${selectedFunction} plot`}
                      className="h-auto rounded border border-white/10 mx-auto block"
                      style={{ 
                        width: '60%',  // Reduced from 75% to 60%
                        maxHeight: isFullscreen ? '95vh' : '500px',  // Further reduced from 640px
                        objectFit: 'contain' 
                      }}
                    />
                    
                    {/* LaTeX Formula Display */}
                    {latexFormula && (
                      <div className="mt-3 p-3 bg-gray-900/70 rounded border border-white/10">
                        <div className="flex justify-between items-center mb-2">
                          <div className="text-sm text-gray-300 font-semibold flex items-center">
                            <span className="mr-2">📐</span>
                            Mathematical Formula
                          </div>
                          <div className="flex space-x-2">
                            <button
                              onClick={copyLatexToClipboard}
                              className="px-2 py-1 bg-blue-600 hover:bg-blue-700 rounded text-xs text-white transition-colors"
                              title="Copy LaTeX to clipboard"
                            >
                              📋 Copy
                            </button>
                            <button
                              onClick={toggleLatexInspector}
                              className="px-2 py-1 bg-purple-600 hover:bg-purple-700 rounded text-xs text-white transition-colors"
                              title="Inspect LaTeX source"
                            >
                              🔍 Inspect
                            </button>
                          </div>
                        </div>
                        
                        {/* Rendered LaTeX using KaTeX */}
                        <div 
                          className="text-white bg-gray-800/50 p-4 rounded border border-gray-700 mb-2 text-center"
                          style={{ 
                            fontSize: '18px', 
                            lineHeight: '1.6'
                          }}
                        >
                          <div className="latex-rendered">
                            {/* Use KaTeX BlockMath for proper LaTeX rendering */}
                            <BlockMath 
                              math={latexFormula} 
                              renderError={(error) => {
                                console.error('KaTeX rendering error:', error);
                                return (
                                  <div className="text-red-400 text-sm">
                                    LaTeX rendering error: {error.message}
                                  </div>
                                );
                              }}
                            />
                          </div>
                        </div>
                        
                        {latexDescription && (
                          <div className="text-xs text-gray-400 mb-2">
                            {latexDescription}
                          </div>
                        )}
                        
                        {/* LaTeX Inspector Modal */}
                        {showLatexInspector && (
                          <div className="mt-2 p-2 bg-gray-800/80 rounded border border-gray-600">
                            <div className="flex justify-between items-center mb-2">
                              <span className="text-xs text-gray-300 font-semibold">LaTeX Source:</span>
                              <button
                                onClick={toggleLatexInspector}
                                className="text-gray-400 hover:text-white text-xs"
                              >
                                ✕
                              </button>
                            </div>
                            <pre className="text-xs text-green-300 font-mono whitespace-pre-wrap bg-gray-900/50 p-2 rounded overflow-x-auto">
                              {latexFormula}
                            </pre>
                          </div>
                        )}
                      </div>
                    )}
                    
                    {functionData && (
                      <div className="mt-2 p-2 bg-gray-900/50 rounded text-xs">
                        <div className="grid grid-cols-2 gap-2 text-center">
                          <span>Function: {selectedFunction}</span>
                          <span>Type: {plotType}</span>
                          <span>Resolution: {resolution}×{resolution}</span>
                          <span>Time: {functionData.generation_time?.toFixed(1)}s</span>
                        </div>
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="w-full h-[800px] bg-gray-900 rounded border border-white/10 flex items-center justify-center">
                    <div className="text-center">
                      {connectionStatus !== 'connected' ? (
                        <>
                          <div className="text-4xl mb-4">🔌</div>
                          <p className="text-lg font-medium">Backend Offline</p>
                          <p className="text-gray-400 text-sm">Start the Python server</p>
                        </>
                      ) : isGenerating ? (
                        <>
                          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
                          <p className="text-lg font-medium">Computing Plot</p>
                          <p className="text-gray-400 text-sm">{plotType} • {resolution}×{resolution}</p>
                        </>
                      ) : (
                        <>
                          <div className="text-4xl mb-4">📊</div>
                          <p className="text-lg font-medium">Ready to Plot</p>
                          <p className="text-gray-400 text-sm">Select function and press GRAPH</p>
                        </>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* LaTeX Function Builder Modal */}
      {showLatexBuilder && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 rounded-lg border border-white/10 max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold">Custom LaTeX Function Builder</h2>
                <button
                  onClick={() => setShowLatexBuilder(false)}
                  className="text-gray-400 hover:text-white text-2xl"
                >
                  ×
                </button>
              </div>
              <LaTeXFunctionBuilder
                onFunctionCreated={handleFunctionCreated}
                onClose={() => setShowLatexBuilder(false)}
              />
            </div>
          </div>
        </div>
      )}

      {/* Fullscreen Plot Overlay */}
      {isFullscreen && plotImage && (
        <div className="fixed inset-0 bg-black/95 flex items-center justify-center z-50">
          <div className="relative w-full h-full flex items-center justify-center p-2">
            {/* Exit fullscreen button */}
            <button
              onClick={exitFullscreen}
              className="absolute top-4 right-4 z-10 px-4 py-2 bg-red-600 hover:bg-red-700 rounded text-white transition-colors"
              title="Exit fullscreen"
            >
              ✕ Exit Fullscreen
            </button>
            
            {/* Fullscreen image - made larger */}
            <img
              src={plotImage}
              alt={`${selectedFunction} plot - Fullscreen`}
              className="object-contain"
              style={{ 
                width: '98%',  // Use more of the screen width
                height: '98%', // Use more of the screen height
                maxWidth: '98vw',
                maxHeight: '98vh'
              }}
            />
            
            {/* Function info overlay */}
            {functionData && (
              <div className="absolute bottom-4 left-4 p-3 bg-black/70 rounded text-white text-sm">
                <div className="font-medium mb-1">{selectedFunction}</div>
                <div>Type: {plotType} • Resolution: {resolution}×{resolution}</div>
                <div>Generation time: {functionData.generation_time?.toFixed(1)}s</div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Draggable Status Bar at Bottom */}
      <div 
        data-status-bar
        className={`fixed bottom-0 left-0 right-0 bg-gray-900/95 backdrop-blur-sm border-t border-white/10 z-50 ${
          isDragging ? '' : 'transition-all duration-300'
        }`}
        style={{ 
          height: `${statusBarHeight}px`,
          ...(isDragging ? { transition: 'none' } : {})
        }}
      >
        {/* Enhanced Drag Handle */}
        <div
          className={`w-full bg-gray-600/80 hover:bg-gray-500/90 cursor-ns-resize flex items-center justify-center border-b border-gray-500/70 transition-colors select-none ${
            isStatusBarMinimized ? 'h-8' : 'h-6'
          }`}
          onMouseDown={handleDragStart}
          onDoubleClick={toggleStatusBar}
          onClick={(e) => {
            // If minimized, also allow single click to expand
            if (isStatusBarMinimized) {
              console.log('Single click on minimized bar - expanding');
              toggleStatusBar(e);
            }
          }}
          onMouseEnter={() => console.log('Mouse entered drag handle')}
          title={isStatusBarMinimized ? 
            "Click to expand • Drag to resize" : 
            "Double-click to minimize • Drag to resize"
          }
          style={{ 
            userSelect: 'none',
            WebkitUserSelect: 'none',
            MozUserSelect: 'none',
            msUserSelect: 'none',
            pointerEvents: 'auto',
            touchAction: 'none'
          }}
        >
          <div className="flex items-center space-x-2 pointer-events-none w-full justify-center">
            <div className="w-16 h-1.5 bg-gray-300 rounded-full shadow-sm"></div>
            {isStatusBarMinimized ? (
              <div className="text-xs text-gray-300 font-medium">
                Status Panel (Click to expand)
              </div>
            ) : (
              <div className="text-xs text-gray-400 font-medium">
                Drag to resize • Double-click to minimize
              </div>
            )}
            {isStatusBarMinimized && (
              <div className={`px-2 py-1 rounded text-xs ml-auto ${
                connectionStatus === 'connected' ? 'bg-green-900/30 text-green-300' :
                connectionStatus === 'disconnected' ? 'bg-red-900/30 text-red-300' :
                'bg-yellow-900/30 text-yellow-300'
              }`}>
                {connectionStatus === 'connected' ? '🟢' : 
                 connectionStatus === 'disconnected' ? '🔴' : 
                 '🟡'}
              </div>
            )}
          </div>
        </div>
        
        {/* Status Content - Hide when minimized */}
        {!isStatusBarMinimized && (
          <div className="p-4 h-full overflow-y-auto">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 h-full">
              
              {/* Connection Status */}
              <div className="bg-black/20 rounded-lg p-3">
                <h4 className="text-sm font-medium mb-2 text-blue-400">🔗 Connection Status</h4>
                <div className={`px-2 py-1 rounded text-xs inline-block ${
                  connectionStatus === 'connected' ? 'bg-green-900/30 text-green-300' :
                  connectionStatus === 'disconnected' ? 'bg-red-900/30 text-red-300' :
                  'bg-yellow-900/30 text-yellow-300'
                }`}>
                  {connectionStatus === 'connected' ? '✅ Backend Online' : 
                   connectionStatus === 'disconnected' ? '❌ Backend Offline' : 
                   '🔄 Connecting...'}
                </div>
              </div>

              {/* System Info */}
              <div className="bg-black/20 rounded-lg p-3">
                <h4 className="text-sm font-medium mb-2 text-purple-400">⚡ Performance</h4>
                <div className="text-xs space-y-1">
                  <div>GPU: {enableGPU ? '✅ Enabled' : '❌ Disabled'}</div>
                  <div>Mode: {performanceMode}</div>
                  <div>Optimized: {useOptimizedPlotter ? '✅ Yes' : '❌ No'}</div>
                </div>
              </div>

              {/* Debug Log */}
              {/* System Summary Panel */}
              <div className="bg-gradient-to-r from-blue-900/30 to-purple-900/30 rounded-lg p-3 border border-blue-500/20">
                <h4 className="text-sm font-medium mb-2 text-blue-300">🌟 Divisor Wave Visualization System</h4>
                <div className="grid grid-cols-2 gap-3 text-xs">
                  <div>
                    <div className="text-gray-400">Functions Available:</div>
                    <div className="text-green-400 font-medium">{Object.keys(functions).reduce((total, cat) => total + Object.keys(functions[cat]).length, 0)} Built-in</div>
                    <div className="text-purple-400 font-medium">{Object.keys(customFunctions).length} Custom</div>
                  </div>
                  <div>
                    <div className="text-gray-400">Backend Status:</div>
                    <div className={`font-medium ${connectionStatus === 'connected' ? 'text-green-400' : 'text-red-400'}`}>
                      {connectionStatus === 'connected' ? '✅ GPU+JIT Ready' : '❌ Disconnected'}
                    </div>
                    <div className="text-blue-400">Real-time LaTeX</div>
                  </div>
                </div>
                <div className="mt-2 text-xs text-gray-400">
                  Research-grade mathematical visualization based on Leo J. Borcherding's divisor wave analysis
                </div>
              </div>

              <div className="bg-black/20 rounded-lg p-3">
                <h4 className="text-sm font-medium mb-2 text-orange-400">📋 Debug Log</h4>
                <div className="space-y-1 max-h-24 overflow-y-auto">
                  {debugInfo.slice(-5).map((log, idx) => (
                    <div key={idx} className={`text-xs ${
                      log.type === 'error' ? 'text-red-400' :
                      log.type === 'success' ? 'text-green-400' :
                      'text-gray-300'
                    }`}>
                      <span className="text-gray-500">[{log.timestamp}]</span> {log.message}
                    </div>
                  ))}
                </div>
              </div>
              
            </div>
          </div>
        )}
      </div>

    </div>
  );
}