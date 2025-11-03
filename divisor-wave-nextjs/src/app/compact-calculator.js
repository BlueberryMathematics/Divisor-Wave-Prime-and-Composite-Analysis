/**
 * Compact Graphing Calculator Interface
 * Minimal scrolling, dropdown organization, integrated custom functions
 */

'use client';

import { useEffect, useState } from 'react';
import LaTeXFunctionBuilder from './LaTeXFunctionBuilder';

export default function CompactCalculator() {
  // Core state
  const [connectionStatus, setConnectionStatus] = useState('checking');
  const [functions, setFunctions] = useState({});
  const [selectedFunction, setSelectedFunction] = useState('product_of_sin');
  const [plotImage, setPlotImage] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [functionData, setFunctionData] = useState(null);
  const [debugInfo, setDebugInfo] = useState([]);
  
  // Settings - Complete set matching Special_Functions.py
  const [plotType, setPlotType] = useState('2D_Complex');
  const [normalizeType, setNormalizeType] = useState('Y');
  const [xRange, setXRange] = useState([1, 15]);
  const [yRange, setYRange] = useState([0, 15]);
  const [zRange, setZRange] = useState([-10, 10]); // Added Z-range for 3D plots
  const [resolution, setResolution] = useState(200);
  const [colormap, setColormap] = useState('6');
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

  const API_BASE = 'http://localhost:8000';

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
      setFunctions(data.functions_by_category || {});
      addDebugLog(`Loaded ${Object.keys(data.functions_by_category || {}).length} categories`, 'success');
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
        setSelectedFunction(functionData.name);
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
        if (selectedFunction === functionName) {
          setSelectedFunction('product_of_sin');
        }
      }
    } catch (error) {
      addDebugLog(`Failed to delete function: ${error.message}`, 'error');
    }
  };

  // Generate plot
  const generatePlot = async () => {
    if (connectionStatus !== 'connected') {
      addDebugLog('Backend not connected', 'error');
      return;
    }

    setIsGenerating(true);
    addDebugLog(`Generating ${plotType} plot...`, 'info');

    try {
      const response = await fetch(`${API_BASE}/plot`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          function_name: selectedFunction,
          plot_type: plotType,
          normalize_type: normalizeType,
          x_min: xRange[0],
          x_max: xRange[1],
          y_min: yRange[0],
          y_max: yRange[1],
          z_min: zRange[0],  // Added Z-range support
          z_max: zRange[1],  // Added Z-range support
          resolution: resolution,
          colormap: colormap,
          canvas_size: canvasSize,
          light_shading: lightShading,
          axis_tick_spacing: axisTick,
          title_override: titleOverride || '',
          m_coefficient: mCoefficient,      // Aesthetic scaling coefficients
          beta_coefficient: betaCoefficient // Aesthetic scaling coefficients
        })
      });

      const data = await response.json();
      
      if (response.ok) {
        setPlotImage(`data:image/png;base64,${data.image_base64}`);
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
    
    // Built-in functions
    Object.entries(functions).forEach(([category, categoryFunctions]) => {
      const categoryOptions = Object.entries(categoryFunctions).map(([funcId, funcInfo]) => ({
        value: funcId,
        label: `${funcInfo.name} (${category})`,
        category: category,
        isCustom: false
      }));
      options.push(...categoryOptions);
    });
    
    // Custom functions
    Object.entries(customFunctions).forEach(([funcName, funcData]) => {
      options.push({
        value: funcName,
        label: `${funcName} (Custom)`,
        category: 'Custom',
        isCustom: true
      });
    });
    
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

  const functionOptions = createFunctionOptions();

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 text-white">
      {/* Compact Header */}
      <header className="bg-black/20 backdrop-blur-sm border-b border-white/10 p-3">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              Compact Mathematical Calculator
            </h1>
            <p className="text-gray-300 text-xs">Ultra-compact interface • No scrolling • Smart organization</p>
          </div>
          <div className={`px-2 py-1 rounded text-xs ${
            connectionStatus === 'connected' ? 'bg-green-900/30 text-green-300' :
            connectionStatus === 'disconnected' ? 'bg-red-900/30 text-red-300' :
            'bg-yellow-900/30 text-yellow-300'
          }`}>
            {connectionStatus === 'connected' ? '✅ Online' : 
             connectionStatus === 'disconnected' ? '❌ Offline' : 
             '🔄 Connecting...'}
          </div>
        </div>
      </header>

      <div className="max-w-[1800px] mx-auto p-6">
        <div className="grid grid-cols-1 xl:grid-cols-4 gap-6">
          
          {/* LEFT: Controls Panel - More spacious */}
          <div className="xl:col-span-1 space-y-6">
            
            {/* Function Selection */}
            <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-lg p-4">
              <label className="block text-sm font-medium mb-3 text-blue-400">📊 FUNCTION</label>
              
              <div className="space-y-3">
                {/* Function Dropdown */}
                <select
                  value={selectedFunction}
                  onChange={(e) => setSelectedFunction(e.target.value)}
                  className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-lg text-sm"
                >
                  {functionOptions.map(option => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
                
                {/* Add Function Button */}
                <button
                  onClick={() => setShowLatexBuilder(true)}
                  className="w-full px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg text-sm font-medium transition-colors"
                  title="Create Custom Function"
                >
                  ➕ Add Custom Function
                </button>
                
                {/* Custom function management */}
                {functionOptions.find(f => f.value === selectedFunction && f.isCustom) && (
                  <button
                    onClick={() => deleteCustomFunction(selectedFunction)}
                    className="w-full px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg text-sm font-medium transition-colors"
                  >
                    🗑️ Delete Custom Function
                  </button>
                )}
              </div>
            </div>

            {/* Plot Mode Selection */}
            <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-lg p-4">
              <label className="block text-sm font-medium mb-3 text-orange-400">🎮 PLOT MODE</label>
              <select
                value={plotType}
                onChange={(e) => setPlotType(e.target.value)}
                className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-lg text-sm"
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
                  <label className="block text-sm font-medium mb-3 text-green-400">📐 WINDOW RANGE</label>
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
                          className="px-2 py-2 bg-gray-800 border border-gray-600 rounded text-sm"
                          title="X-axis minimum value"
                        />
                        <input
                          type="number"
                          value={xRange[1]}
                          onChange={(e) => setXRange([xRange[0], parseFloat(e.target.value) || 0])}
                          placeholder="X max"
                          className="px-2 py-2 bg-gray-800 border border-gray-600 rounded text-sm"
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
                  <label className="block text-sm font-medium mb-3 text-purple-400">🎨 VISUAL STYLE</label>
                  <div className="space-y-3">
                    <div>
                      <label className="block text-xs text-gray-300 mb-1">Resolution</label>
                      <select
                        value={resolution}
                        onChange={(e) => setResolution(parseInt(e.target.value))}
                        className="w-full px-2 py-2 bg-gray-800 border border-gray-600 rounded text-sm"
                      >
                        <option value={100}>100×100 (Fast)</option>
                        <option value={200}>200×200 (Normal)</option>
                        <option value={400}>400×400 (High)</option>
                        <option value={600}>600×600 (Ultra)</option>
                      </select>
                    </div>
                    
                    <div>
                      <label className="block text-xs text-gray-300 mb-1">Color Scheme</label>
                      <select
                        value={colormap}
                        onChange={(e) => setColormap(e.target.value)}
                        className="w-full px-2 py-2 bg-gray-800 border border-gray-600 rounded text-sm"
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
              <details className="mt-4">
                <summary className="text-sm text-gray-400 cursor-pointer hover:text-white font-medium">⚙️ Advanced Options</summary>
                <div className="mt-4 space-y-4">
                  
                  {/* First Row: Normalization and Canvas */}
                  <div className="grid grid-cols-1 gap-3 text-sm">
                    <div>
                      <label className="block text-sm mb-2">Normalization</label>
                      <select
                        value={normalizeType}
                        onChange={(e) => setNormalizeType(e.target.value)}
                        className="w-full px-2 py-2 bg-gray-800 border border-gray-600 rounded"
                        title="Mathematical normalization method"
                      >
                        <option value="Y">Y-axis normalize</option>
                        <option value="N">No normalization</option>
                        <option value="Z">Z-axis normalize</option>
                      </select>
                    </div>
                    
                    <div>
                      <label className="block text-sm mb-2">Canvas Ratio</label>
                      <select
                        value={canvasSize}
                        onChange={(e) => setCanvasSize(e.target.value)}
                        className="w-full px-2 py-2 bg-gray-800 border border-gray-600 rounded"
                        title="Plot aspect ratio"
                      >
                        <option value="16x9">16:9 Widescreen</option>
                        <option value="4x3">4:3 Standard</option>
                        <option value="1x1">1:1 Square</option>
                      </select>
                    </div>
                  </div>

                  {/* Second Row: Shading and Tick Spacing */}
                  <div className="grid grid-cols-1 gap-3 text-sm">
                    <div className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={lightShading}
                        onChange={(e) => setLightShading(e.target.checked)}
                        className="rounded"
                        title="Enable 3D light shading for enhanced depth perception"
                      />
                      <label className="text-sm">3D Light Shading</label>
                    </div>
                    
                    <div>
                      <label className="block text-sm mb-2">Axis Tick Spacing</label>
                      <input
                        type="number"
                        step="0.1"
                        value={axisTick}
                        onChange={(e) => setAxisTick(parseFloat(e.target.value) || 1.0)}
                        placeholder="Tick spacing"
                        className="w-full px-2 py-2 bg-gray-800 border border-gray-600 rounded"
                        title="Spacing between axis tick marks"
                      />
                    </div>
                  </div>

                  {/* Third Row: Coefficient Controls */}
                  <div className="grid grid-cols-1 gap-3 text-sm">
                    <div>
                      <label className="block text-sm mb-2 text-purple-300">M Coefficient (Magnification)</label>
                      <input
                        type="number"
                        step="0.001"
                        value={mCoefficient}
                        onChange={(e) => setMCoefficient(parseFloat(e.target.value) || 0.36)}
                        placeholder="Magnification scalar"
                        className="w-full px-2 py-2 bg-gray-800 border border-gray-600 rounded"
                        title="Magnification exponent for plot scaling - adjusts visual appearance and detail level"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm mb-2 text-purple-300">Beta Coefficient (Scaling)</label>
                      <input
                        type="number"
                        step="0.001"
                        value={betaCoefficient}
                        onChange={(e) => setBetaCoefficient(parseFloat(e.target.value) || 0.1468)}
                        placeholder="Scaling factor"
                        className="w-full px-2 py-2 bg-gray-800 border border-gray-600 rounded"
                        title="Scaling coefficient for aesthetic control - affects plot visual characteristics"
                      />
                    </div>
                  </div>

                  {/* Custom Title */}
                  <div>
                    <label className="block text-sm mb-2">Custom Title</label>
                    <input
                      type="text"
                      value={titleOverride}
                      onChange={(e) => setTitleOverride(e.target.value)}
                      placeholder="Leave empty for auto-generated title"
                      className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded text-sm"
                      title="Override the automatic plot title"
                    />
                  </div>

                  {/* Info Panel */}
                  <div className="mt-4 p-3 bg-gray-800/50 rounded text-sm text-gray-300">
                    <div className="font-medium mb-2">Current Settings Summary:</div>
                    <div className="space-y-1">
                      <div>Range: X[{xRange[0]}, {xRange[1]}] Y[{yRange[0]}, {yRange[1]}] {plotType.includes('3D') && `Z[${zRange[0]}, ${zRange[1]}]`}</div>
                      <div>Resolution: {resolution}×{resolution} • Type: {plotType}</div>
                      <div>Colormap: {colormap} • Normalization: {normalizeType}</div>
                      <div>Coefficients: M={mCoefficient} • Beta={betaCoefficient}</div>
                    </div>
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
              <button
                onClick={() => {
                  const link = document.createElement('a');
                  link.href = plotImage;
                  link.download = `${selectedFunction}_${plotType}.png`;
                  link.click();
                }}
                className="w-full py-3 bg-green-600 hover:bg-green-700 rounded-lg text-sm font-medium transition-colors"
              >
                💾 Save Plot Image
              </button>
            )}

            {/* Status Panel */}
            <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-lg p-4">
              <h3 className="text-sm font-semibold mb-3">System Status</h3>
              <div className="space-y-2 text-sm">
                {debugInfo.map((log, index) => (
                  <div key={index} className={`${
                    log.type === 'error' ? 'text-red-400' :
                    log.type === 'success' ? 'text-green-400' :
                    'text-gray-300'
                  }`}>
                    <span className="text-gray-500">{log.timestamp}</span> {log.message}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* RIGHT: Large Plot Display */}
          <div className="xl:col-span-3">
            <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-lg p-6 min-h-[900px]">
              <div className="mb-4">
                <h3 className="text-lg font-bold">📊 DISPLAY</h3>
              </div>

              <div className="relative">
                {plotImage ? (
                  <div>
                    <img
                      src={plotImage}
                      alt={`${selectedFunction} plot`}
                      className="w-full h-auto rounded border border-white/10"
                    />
                    {functionData && (
                      <div className="mt-2 p-2 bg-gray-900/50 rounded text-xs">
                        <div className="grid grid-cols-4 gap-2">
                          <span>Function: {selectedFunction}</span>
                          <span>Type: {plotType}</span>
                          <span>Resolution: {resolution}×{resolution}</span>
                          <span>Time: {functionData.generation_time?.toFixed(1)}s</span>
                        </div>
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="w-full h-[750px] bg-gray-900 rounded border border-white/10 flex items-center justify-center">
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
    </div>
  );
}