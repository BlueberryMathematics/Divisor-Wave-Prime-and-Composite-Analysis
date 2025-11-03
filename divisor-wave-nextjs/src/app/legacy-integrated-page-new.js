/**
 * Advanced Divisor Wave Analysis Frontend - Graphing Calculator Layout
 * Organized like a real graphing calculator with logical setting groups
 */

'use client';

import { useEffect, useState } from 'react';
import LaTeXFunctionBuilder from './LaTeXFunctionBuilder';

export default function AdvancedDivisorWaveAnalysis() {
  // Core state management
  const [connectionStatus, setConnectionStatus] = useState('checking');
  const [functions, setFunctions] = useState({});
  const [selectedFunction, setSelectedFunction] = useState('product_of_sin');
  const [plotImage, setPlotImage] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [functionData, setFunctionData] = useState(null);
  const [debugInfo, setDebugInfo] = useState([]);
  
  // Plot type and normalization controls (legacy system)
  const [plotType, setPlotType] = useState('2D_Complex');
  const [normalizeType, setNormalizeType] = useState('Y');
  
  // Range controls (legacy system)
  const [xRange, setXRange] = useState([1, 15]);
  const [yRange, setYRange] = useState([0, 15]);
  const [resolution, setResolution] = useState(200);
  
  // Advanced plotting options from legacy system
  const [colormap, setColormap] = useState('6');
  const [canvasSize, setCanvasSize] = useState('16x9');
  const [lightShading, setLightShading] = useState(false);
  const [axisTick, setAxisTick] = useState(1.0);
  const [titleOverride, setTitleOverride] = useState('');
  
  // LaTeX Function Builder state
  const [showLatexBuilder, setShowLatexBuilder] = useState(false);

  const API_BASE = 'http://localhost:8000';

  // Add debug log
  const addDebugLog = (message, type = 'info') => {
    const timestamp = new Date().toLocaleTimeString();
    setDebugInfo(prev => [...prev.slice(-10), { timestamp, message, type }]);
  };

  // Check backend connection
  const checkConnection = async () => {
    try {
      addDebugLog('Checking advanced backend connection...', 'info');
      const response = await fetch(`${API_BASE}/health`);
      const data = await response.json();
      
      if (response.ok) {
        setConnectionStatus('connected');
        addDebugLog(`Backend connected`, 'success');
        return true;
      } else {
        throw new Error('Backend responded with error');
      }
    } catch (error) {
      setConnectionStatus('disconnected');
      addDebugLog(`Connection failed: ${error.message}`, 'error');
      return false;
    }
  };

  // Load all functions
  const loadFunctions = async () => {
    try {
      const response = await fetch(`${API_BASE}/functions`);
      const data = await response.json();
      setFunctions(data.functions_by_category || {});
      addDebugLog(`Loaded ${data.total_functions} functions`, 'success');
    } catch (error) {
      addDebugLog(`Failed to load functions: ${error.message}`, 'error');
    }
  };

  // Handle custom function creation
  const handleFunctionCreated = (functionData) => {
    addDebugLog(`Custom function "${functionData.name}" created successfully`, 'success');
    loadFunctions(); // Reload all functions
  };

  // Delete custom function
  const deleteCustomFunction = async (functionName) => {
    if (!window.confirm(`Are you sure you want to delete "${functionName}"?`)) {
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/custom-functions/${functionName}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        addDebugLog(`Custom function "${functionName}" deleted`, 'success');
        loadFunctions(); // Reload functions
      } else {
        throw new Error('Failed to delete function');
      }
    } catch (error) {
      addDebugLog(`Failed to delete function: ${error.message}`, 'error');
    }
  };

  // Generate plot with advanced controls
  const generatePlot = async () => {
    if (!selectedFunction || isGenerating) return;
    
    setIsGenerating(true);
    addDebugLog(`Generating ${plotType} plot for ${selectedFunction}...`, 'info');

    try {
      const plotRequest = {
        function_name: selectedFunction,
        plot_type: plotType,
        x_min: xRange[0],
        x_max: xRange[1], 
        y_min: yRange[0],
        y_max: yRange[1],
        resolution: resolution,
        normalize_type: normalizeType,
        colormap: colormap,
        canvas_size: canvasSize,
        light_shading: lightShading,
        axis_tick_spacing: axisTick,
        title_override: titleOverride
      };

      const response = await fetch(`${API_BASE}/plot`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(plotRequest)
      });

      const data = await response.json();

      if (response.ok && data.success) {
        setPlotImage(`data:image/png;base64,${data.plot_image}`);
        setFunctionData(data.function_data);
        addDebugLog(`Plot generated successfully in ${data.generation_time}s`, 'success');
      } else {
        throw new Error(data.error || 'Plot generation failed');
      }
    } catch (error) {
      addDebugLog(`Plot generation failed: ${error.message}`, 'error');
    } finally {
      setIsGenerating(false);
    }
  };

  // Effect hooks
  useEffect(() => {
    checkConnection();
    const interval = setInterval(checkConnection, 30000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (connectionStatus === 'connected') {
      loadFunctions();
    }
  }, [connectionStatus]);

  const functionCategories = Object.keys(functions);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 text-white">
      {/* Header */}
      <header className="bg-black/20 backdrop-blur-sm border-b border-white/10 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                Mathematical Graphing Calculator
              </h1>
              <p className="text-gray-300 text-sm">Advanced Function Visualization Tool</p>
            </div>
            <div className={`px-3 py-1 rounded text-sm ${
              connectionStatus === 'connected' ? 'bg-green-900/30 text-green-300' :
              connectionStatus === 'disconnected' ? 'bg-red-900/30 text-red-300' :
              'bg-yellow-900/30 text-yellow-300'
            }`}>
              {connectionStatus === 'connected' ? '✅ Connected' : 
               connectionStatus === 'disconnected' ? '❌ Offline' : 
               '🔄 Connecting...'}
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="grid grid-cols-12 gap-6">
          
          {/* Calculator-Style Control Panel - Left Side */}
          <div className="col-span-12 lg:col-span-4 space-y-4">
            
            {/* FUNCTION SELECTION - Like choosing equation on calculator */}
            <div className="bg-black/30 backdrop-blur-sm border border-white/20 rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-lg font-bold text-blue-300">📊 FUNCTION (Y=)</h3>
                <button
                  onClick={() => setShowLatexBuilder(true)}
                  className="px-2 py-1 bg-purple-600 hover:bg-purple-700 rounded text-xs"
                >
                  + Custom
                </button>
              </div>
              
              <div className="space-y-2 max-h-48 overflow-y-auto bg-gray-900/50 rounded p-2">
                {functionCategories.map(category => (
                  <div key={category}>
                    <h4 className="text-xs font-bold text-gray-400 uppercase mb-1">{category}</h4>
                    {Object.entries(functions[category] || {}).map(([funcId, funcInfo]) => (
                      <button
                        key={funcId}
                        onClick={() => setSelectedFunction(funcId)}
                        className={`w-full text-left p-2 rounded text-sm transition-colors ${
                          selectedFunction === funcId
                            ? 'bg-blue-600 text-white border border-blue-400'
                            : 'bg-gray-800 hover:bg-gray-700 text-gray-200'
                        }`}
                      >
                        <div className="font-medium truncate">{funcInfo.name}</div>
                        <div className="text-xs text-gray-400 truncate">{funcInfo.description}</div>
                      </button>
                    ))}
                  </div>
                ))}
              </div>
            </div>

            {/* WINDOW SETTINGS - Like WINDOW button on calculator */}
            <div className="bg-black/30 backdrop-blur-sm border border-white/20 rounded-lg p-4">
              <h3 className="text-lg font-bold text-green-300 mb-3">📐 WINDOW</h3>
              
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <label className="block text-gray-300 font-medium mb-1">Xmin</label>
                  <input
                    type="number"
                    value={xRange[0]}
                    onChange={(e) => setXRange([+e.target.value, xRange[1]])}
                    className="w-full bg-gray-800 border border-gray-600 rounded px-2 py-1 text-white"
                  />
                </div>
                <div>
                  <label className="block text-gray-300 font-medium mb-1">Xmax</label>
                  <input
                    type="number"
                    value={xRange[1]}
                    onChange={(e) => setXRange([xRange[0], +e.target.value])}
                    className="w-full bg-gray-800 border border-gray-600 rounded px-2 py-1 text-white"
                  />
                </div>
                <div>
                  <label className="block text-gray-300 font-medium mb-1">Ymin</label>
                  <input
                    type="number"
                    value={yRange[0]}
                    onChange={(e) => setYRange([+e.target.value, yRange[1]])}
                    className="w-full bg-gray-800 border border-gray-600 rounded px-2 py-1 text-white"
                  />
                </div>
                <div>
                  <label className="block text-gray-300 font-medium mb-1">Ymax</label>
                  <input
                    type="number"
                    value={yRange[1]}
                    onChange={(e) => setYRange([yRange[0], +e.target.value])}
                    className="w-full bg-gray-800 border border-gray-600 rounded px-2 py-1 text-white"
                  />
                </div>
              </div>
              
              <div className="mt-3">
                <label className="block text-gray-300 font-medium mb-1">Resolution: {resolution}</label>
                <input
                  type="range"
                  min="50"
                  max="500"
                  value={resolution}
                  onChange={(e) => setResolution(+e.target.value)}
                  className="w-full"
                />
                <div className="flex justify-between text-xs text-gray-400 mt-1">
                  <span>Fast</span>
                  <span>High Quality</span>
                </div>
              </div>
            </div>

            {/* GRAPH TYPE - Like MODE button on calculator */}
            <div className="bg-black/30 backdrop-blur-sm border border-white/20 rounded-lg p-4">
              <h3 className="text-lg font-bold text-yellow-300 mb-3">📈 MODE</h3>
              
              <div className="grid grid-cols-2 gap-2 mb-3">
                {['2D_Real', '2D_Complex', '3D_Real', '3D_Complex'].map(type => (
                  <button
                    key={type}
                    onClick={() => setPlotType(type)}
                    className={`p-2 rounded text-sm font-medium transition-colors ${
                      plotType === type
                        ? 'bg-yellow-600 text-black'
                        : 'bg-gray-700 hover:bg-gray-600 text-white'
                    }`}
                  >
                    {type.replace('_', ' ')}
                  </button>
                ))}
              </div>
              
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <label className="block text-gray-300 font-medium mb-1">Normalize</label>
                  <select 
                    value={normalizeType}
                    onChange={(e) => setNormalizeType(e.target.value)}
                    className="w-full bg-gray-800 border border-gray-600 rounded px-2 py-1 text-white text-sm"
                  >
                    <option value="Y">Gamma (Y)</option>
                    <option value="N">Raw (N)</option>
                  </select>
                </div>
                <div>
                  <label className="block text-gray-300 font-medium mb-1">Canvas</label>
                  <select 
                    value={canvasSize}
                    onChange={(e) => setCanvasSize(e.target.value)}
                    className="w-full bg-gray-800 border border-gray-600 rounded px-2 py-1 text-white text-sm"
                  >
                    <option value="16x9">16:9</option>
                    <option value="4x3">4:3</option>
                    <option value="1x1">1:1</option>
                  </select>
                </div>
              </div>
            </div>

            {/* FORMAT SETTINGS - Like FORMAT button on calculator */}
            <div className="bg-black/30 backdrop-blur-sm border border-white/20 rounded-lg p-4">
              <h3 className="text-lg font-bold text-purple-300 mb-3">🎨 FORMAT</h3>
              
              <div className="space-y-3 text-sm">
                <div>
                  <label className="block text-gray-300 font-medium mb-1">Color Scheme</label>
                  <select 
                    value={colormap}
                    onChange={(e) => setColormap(e.target.value)}
                    className="w-full bg-gray-800 border border-gray-600 rounded px-2 py-1 text-white"
                  >
                    <optgroup label="Calculator Themes">
                      <option value="1">Theme 1</option>
                      <option value="2">Theme 2</option>
                      <option value="3">Theme 3</option>
                      <option value="4">Theme 4</option>
                      <option value="5">Theme 5</option>
                      <option value="6">Theme 6</option>
                    </optgroup>
                    <optgroup label="Standard">
                      <option value="viridis">Viridis</option>
                      <option value="plasma">Plasma</option>
                      <option value="hot">Hot</option>
                      <option value="cool">Cool</option>
                      <option value="rainbow">Rainbow</option>
                    </optgroup>
                  </select>
                </div>
                
                <div>
                  <label className="block text-gray-300 font-medium mb-1">Axis Spacing</label>
                  <input
                    type="number"
                    step="0.1"
                    value={axisTick}
                    onChange={(e) => setAxisTick(+e.target.value)}
                    className="w-full bg-gray-800 border border-gray-600 rounded px-2 py-1 text-white"
                  />
                </div>
                
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="lightShading"
                    checked={lightShading}
                    onChange={(e) => setLightShading(e.target.checked)}
                    className="mr-2"
                  />
                  <label htmlFor="lightShading" className="text-sm text-gray-300">
                    Enhanced Shading
                  </label>
                </div>
                
                <div>
                  <label className="block text-gray-300 font-medium mb-1">Title (optional)</label>
                  <input
                    type="text"
                    value={titleOverride}
                    onChange={(e) => setTitleOverride(e.target.value)}
                    placeholder="Custom title..."
                    className="w-full bg-gray-800 border border-gray-600 rounded px-2 py-1 text-white text-sm"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Main Display and Generate Button - Right Side */}
          <div className="col-span-12 lg:col-span-8">
            
            {/* CALCULATOR DISPLAY */}
            <div className="bg-black/30 backdrop-blur-sm border border-white/20 rounded-lg p-6 mb-4">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-bold">📺 DISPLAY</h3>
                {plotImage && (
                  <button
                    onClick={() => {
                      const link = document.createElement('a');
                      link.href = plotImage;
                      link.download = `${selectedFunction}_${plotType}.png`;
                      link.click();
                    }}
                    className="px-3 py-1 bg-green-600 hover:bg-green-700 rounded text-sm"
                  >
                    💾 Save
                  </button>
                )}
              </div>
              
              <div className="relative bg-gray-900 rounded-lg border-2 border-gray-700 p-4">
                {plotImage ? (
                  <div className="w-full">
                    <img 
                      src={plotImage} 
                      alt={`${selectedFunction} plot`}
                      className="w-full h-auto rounded"
                    />
                    {functionData && (
                      <div className="mt-3 p-2 bg-gray-800/70 rounded text-xs">
                        <div className="grid grid-cols-4 gap-2">
                          <span>Type: {functionData.plot_type}</span>
                          <span>Res: {functionData.resolution}×{functionData.resolution}</span>
                          <span>X: [{functionData.x_min}, {functionData.x_max}]</span>
                          <span>Y: [{functionData.y_min}, {functionData.y_max}]</span>
                        </div>
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="w-full h-96 flex items-center justify-center">
                    <div className="text-center">
                      {connectionStatus !== 'connected' ? (
                        <>
                          <div className="text-6xl mb-4">🔌</div>
                          <p className="text-xl font-bold">Backend Offline</p>
                          <p className="text-gray-400">Start the Python server</p>
                        </>
                      ) : isGenerating ? (
                        <>
                          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-400 mx-auto mb-4"></div>
                          <p className="text-xl font-bold">Computing...</p>
                          <p className="text-gray-400">
                            {plotType.replace('_', ' ')} • {resolution}×{resolution}
                          </p>
                        </>
                      ) : (
                        <>
                          <div className="text-6xl mb-4">📊</div>
                          <p className="text-xl font-bold">Ready to Graph</p>
                          <p className="text-gray-400">Configure settings and press GRAPH</p>
                        </>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* GRAPH BUTTON - Like the big GRAPH button on calculators */}
            <div className="bg-black/30 backdrop-blur-sm border border-white/20 rounded-lg p-6">
              <div className="grid grid-cols-3 gap-4">
                
                {/* Current Settings Display */}
                <div className="col-span-2 bg-gray-900/50 rounded-lg p-4">
                  <h4 className="font-bold mb-2 text-gray-300">Current Settings:</h4>
                  <div className="grid grid-cols-2 gap-2 text-sm text-gray-400">
                    <div>Function: <span className="text-white">{selectedFunction}</span></div>
                    <div>Mode: <span className="text-white">{plotType.replace('_', ' ')}</span></div>
                    <div>Window: <span className="text-white">[{xRange[0]}, {xRange[1]}] × [{yRange[0]}, {yRange[1]}]</span></div>
                    <div>Resolution: <span className="text-white">{resolution}×{resolution}</span></div>
                  </div>
                </div>
                
                {/* Big Graph Button */}
                <div className="flex items-center">
                  <button
                    onClick={generatePlot}
                    disabled={isGenerating || connectionStatus !== 'connected'}
                    className={`w-full h-full rounded-lg font-bold text-xl transition-all transform ${
                      isGenerating || connectionStatus !== 'connected'
                        ? 'bg-gray-600 cursor-not-allowed scale-95'
                        : 'bg-gradient-to-br from-green-600 to-blue-600 hover:from-green-500 hover:to-blue-500 hover:scale-105 shadow-lg hover:shadow-xl'
                    }`}
                  >
                    {isGenerating ? (
                      <div className="flex flex-col items-center">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white mb-2"></div>
                        <span className="text-sm">COMPUTING</span>
                      </div>
                    ) : connectionStatus !== 'connected' ? (
                      <div className="flex flex-col items-center">
                        <span className="text-2xl">❌</span>
                        <span className="text-sm">OFFLINE</span>
                      </div>
                    ) : (
                      <div className="flex flex-col items-center">
                        <span className="text-3xl">📊</span>
                        <span>GRAPH</span>
                      </div>
                    )}
                  </button>
                </div>
              </div>
            </div>

            {/* Analysis Results - Calculator Style */}
            {functionData?.evaluation && (
              <div className="mt-4 bg-black/30 backdrop-blur-sm border border-white/20 rounded-lg p-4">
                <h3 className="text-lg font-bold text-blue-300 mb-3">🔍 ANALYSIS</h3>
                
                <div className="grid grid-cols-4 gap-2 text-xs">
                  {functionData.evaluation.prime_analysis?.slice(0, 12).map((analysis, index) => {
                    const n = analysis.n;
                    const magnitude = analysis.magnitude;
                    const isP = analysis.is_prime;
                    
                    return (
                      <div 
                        key={n}
                        className={`p-2 rounded text-center ${
                          isP 
                            ? 'bg-blue-900/50 text-blue-200' 
                            : 'bg-orange-900/50 text-orange-200'
                        }`}
                      >
                        <div className="font-bold">n={n}</div>
                        <div className="text-xs">{isP ? 'Prime' : 'Comp'}</div>
                        <div className="text-xs">|f|={magnitude.toFixed(2)}</div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Status Panel */}
            <div className="mt-4 bg-black/30 backdrop-blur-sm border border-white/20 rounded-lg p-4">
              <h3 className="text-lg font-bold text-gray-300 mb-2">📡 STATUS</h3>
              <div className="space-y-1 text-xs">
                {debugInfo.slice(-3).map((log, index) => (
                  <div key={index} className={`${
                    log.type === 'error' ? 'text-red-400' :
                    log.type === 'success' ? 'text-green-400' :
                    'text-gray-400'
                  }`}>
                    <span className="text-gray-500">{log.timestamp}</span> {log.message}
                  </div>
                ))}
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
                <h2 className="text-2xl font-bold">Custom Function Builder</h2>
                <button
                  onClick={() => setShowLatexBuilder(false)}
                  className="text-gray-400 hover:text-white text-2xl"
                >
                  ×
                </button>
              </div>
              <LaTeXFunctionBuilder
                onFunctionCreated={(functionData) => {
                  handleFunctionCreated(functionData);
                  setShowLatexBuilder(false);
                }}
                onClose={() => setShowLatexBuilder(false)}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
  const [canvasSize, setCanvasSize] = useState('16x9');
  const [lightShading, setLightShading] = useState(false);
  const [axisTick, setAxisTick] = useState(1.0);
  const [titleOverride, setTitleOverride] = useState('');
  
  // LaTeX Function Builder state
  const [showLatexBuilder, setShowLatexBuilder] = useState(false);

  const API_BASE = 'http://localhost:8000';

  // Add debug log
  const addDebugLog = (message, type = 'info') => {
    const timestamp = new Date().toLocaleTimeString();
    setDebugInfo(prev => [...prev.slice(-10), { timestamp, message, type }]);
  };

  // Check backend connection
  const checkConnection = async () => {
    try {
      addDebugLog('Checking advanced backend connection...', 'info');
      const response = await fetch(`${API_BASE}/health`);
      const data = await response.json();
      
      if (response.ok) {
        setConnectionStatus('connected');
        addDebugLog(`Backend connected`, 'success');
        return true;
      } else {
        throw new Error('Backend responded with error');
      }
    } catch (error) {
      setConnectionStatus('disconnected');
      addDebugLog(`Connection failed: ${error.message}`, 'error');
      return false;
    }
  };

  // Load all functions
  const loadFunctions = async () => {
    try {
      const response = await fetch(`${API_BASE}/functions`);
      const data = await response.json();
      setFunctions(data.functions_by_category || {});
      addDebugLog(`Loaded ${data.total_functions} functions`, 'success');
    } catch (error) {
      addDebugLog(`Failed to load functions: ${error.message}`, 'error');
    }
  };

  // Handle custom function creation
  const handleFunctionCreated = (functionData) => {
    addDebugLog(`Custom function "${functionData.name}" created successfully`, 'success');
    loadFunctions(); // Reload all functions
  };

  // Delete custom function
  const deleteCustomFunction = async (functionName) => {
    if (!window.confirm(`Are you sure you want to delete "${functionName}"?`)) {
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/custom-functions/${functionName}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        addDebugLog(`Custom function "${functionName}" deleted`, 'success');
        loadFunctions(); // Reload functions
      } else {
        throw new Error('Failed to delete function');
      }
    } catch (error) {
      addDebugLog(`Failed to delete function: ${error.message}`, 'error');
    }
  };

  // Generate plot with advanced controls
  const generatePlot = async () => {
    if (!selectedFunction || isGenerating) return;
    
    setIsGenerating(true);
    addDebugLog(`Generating ${plotType} plot for ${selectedFunction}...`, 'info');

    try {
      const plotRequest = {
        function_name: selectedFunction,
        plot_type: plotType,
        x_min: xRange[0],
        x_max: xRange[1], 
        y_min: yRange[0],
        y_max: yRange[1],
        resolution: resolution,
        normalize_type: normalizeType,
        colormap: colormap,
        canvas_size: canvasSize,
        light_shading: lightShading,
        axis_tick_spacing: axisTick,
        title_override: titleOverride
      };

      const response = await fetch(`${API_BASE}/plot`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(plotRequest)
      });

      const data = await response.json();

      if (response.ok && data.success) {
        setPlotImage(`data:image/png;base64,${data.plot_image}`);
        setFunctionData(data.function_data);
        addDebugLog(`Plot generated successfully in ${data.generation_time}s`, 'success');
      } else {
        throw new Error(data.error || 'Plot generation failed');
      }
    } catch (error) {
      addDebugLog(`Plot generation failed: ${error.message}`, 'error');
    } finally {
      setIsGenerating(false);
    }
  };

  // Effect hooks
  useEffect(() => {
    checkConnection();
    const interval = setInterval(checkConnection, 30000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (connectionStatus === 'connected') {
      loadFunctions();
    }
  }, [connectionStatus]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 text-white">
      {/* Compact Header */}
      <header className="bg-black/20 backdrop-blur-sm border-b border-white/10 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                Advanced Divisor Wave Analysis v3.0
              </h1>
              <p className="text-gray-300 text-sm">Complete Legacy Integration - All Plot Types & Advanced Controls</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className={`px-3 py-1 rounded text-sm ${
                connectionStatus === 'connected' ? 'bg-green-900/30 text-green-300' :
                connectionStatus === 'disconnected' ? 'bg-red-900/30 text-red-300' :
                'bg-yellow-900/30 text-yellow-300'
              }`}>
                {connectionStatus === 'connected' ? '✅ Backend v3.0' : 
                 connectionStatus === 'disconnected' ? '❌ Offline' : 
                 '🔄 Checking...'}
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-6">
        {/* Compact Tabbed Control Panel */}
        <div className="mb-6">
          <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-lg p-4">
            <ControlTabs 
              functions={functions}
              selectedFunction={selectedFunction}
              setSelectedFunction={setSelectedFunction}
              plotType={plotType}
              setPlotType={setPlotType}
              normalizeType={normalizeType}
              setNormalizeType={setNormalizeType}
              xRange={xRange}
              setXRange={setXRange}
              yRange={yRange}
              setYRange={setYRange}
              resolution={resolution}
              setResolution={setResolution}
              colormap={colormap}
              setColormap={setColormap}
              canvasSize={canvasSize}
              setCanvasSize={setCanvasSize}
              lightShading={lightShading}
              setLightShading={setLightShading}
              axisTick={axisTick}
              setAxisTick={setAxisTick}
              titleOverride={titleOverride}
              setTitleOverride={setTitleOverride}
              generatePlot={generatePlot}
              isGenerating={isGenerating}
              connectionStatus={connectionStatus}
              deleteCustomFunction={deleteCustomFunction}
              setShowLatexBuilder={setShowLatexBuilder}
            />
          </div>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
          
          {/* Main Plot Display */}
          <div className="xl:col-span-2">
            <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-lg p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-semibold">Mathematical Visualization</h3>
                {plotImage && (
                  <button
                    onClick={() => {
                      const link = document.createElement('a');
                      link.href = plotImage;
                      link.download = `${selectedFunction}_${plotType}.png`;
                      link.click();
                    }}
                    className="px-3 py-1 bg-green-600 hover:bg-green-700 rounded text-sm transition-colors"
                  >
                    💾 Save Plot
                  </button>
                )}
              </div>
              
              <div className="relative">
                {plotImage ? (
                  <div className="w-full">
                    <img 
                      src={plotImage} 
                      alt={`${selectedFunction} plot`}
                      className="w-full h-auto rounded border border-white/10"
                    />
                    {functionData && (
                      <div className="mt-3 p-3 bg-gray-900/50 rounded text-sm">
                        <div className="grid grid-cols-3 gap-2 text-xs">
                          <span>Type: {functionData.plot_type}</span>
                          <span>Resolution: {functionData.resolution}×{functionData.resolution}</span>
                          <span>Range: [{functionData.x_min}, {functionData.x_max}] × [{functionData.y_min}, {functionData.y_max}]</span>
                        </div>
                        {functionData.latex_formula && (
                          <div className="mt-2 text-green-400 font-mono text-xs">
                            LaTeX: {functionData.latex_formula}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="w-full h-96 bg-gray-900 rounded border border-white/10 flex items-center justify-center">
                    <div className="text-center">
                      {connectionStatus !== 'connected' ? (
                        <>
                          <div className="text-4xl mb-4">🔌</div>
                          <p className="text-lg font-medium">Backend Disconnected</p>
                          <p className="text-gray-400 mt-2">Start the advanced Python server</p>
                          <code className="block mt-4 p-2 bg-black/30 rounded text-green-400 text-sm">
                            .\start-system.ps1
                          </code>
                        </>
                      ) : isGenerating ? (
                        <>
                          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
                          <p className="text-lg font-medium">Computing Advanced Plot</p>
                          <p className="text-gray-400 mt-2">
                            {plotType.replace('_', ' ')} visualization with {resolution}×{resolution} resolution
                          </p>
                        </>
                      ) : (
                        <>
                          <div className="text-4xl mb-4">📊</div>
                          <p className="text-lg font-medium">Ready for Advanced Plotting</p>
                          <p className="text-gray-400 mt-2">
                            Select function and plot type, then generate your mathematical visualization
                          </p>
                        </>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Compact Side Panel */}
          <div className="xl:col-span-1 space-y-4">
            
            {/* Function Analysis Results */}
            {functionData?.evaluation && (
              <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-lg p-4">
                <h3 className="text-lg font-semibold mb-3">Pattern Analysis</h3>
                
                <div className="grid grid-cols-2 gap-2 text-xs">
                  {functionData.evaluation.prime_analysis?.slice(0, 8).map((analysis, index) => {
                    const n = analysis.n;
                    const magnitude = analysis.magnitude;
                    const isP = analysis.is_prime;
                    
                    return (
                      <div 
                        key={n}
                        className={`p-2 rounded border ${
                          isP 
                            ? 'bg-blue-900/30 border-blue-500/50 text-blue-200' 
                            : 'bg-orange-900/30 border-orange-500/50 text-orange-200'
                        }`}
                      >
                        <div className="font-medium">n = {n}</div>
                        <div className="text-xs">{isP ? 'Prime' : 'Composite'}</div>
                        <div className="text-xs">|f({n})| = {magnitude.toFixed(3)}</div>
                      </div>
                    );
                  })}
                </div>

                <p className="text-gray-400 text-xs mt-3">
                  <strong>Pattern:</strong> Primes create cusps while composites create smooth curves.
                </p>
              </div>
            )}

            {/* Debug Information - Compact */}
            <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-lg p-4">
              <h3 className="text-lg font-semibold mb-3">System Status</h3>
              
              <div className="space-y-2 text-xs">
                {debugInfo.slice(-5).map((log, index) => (
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

            {/* Quick Info Panel */}
            <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-lg p-4">
              <h3 className="text-lg font-semibold mb-3">Quick Info</h3>
              
              <div className="text-xs text-gray-300 space-y-2">
                <div>
                  <strong>Selected:</strong> {selectedFunction}
                </div>
                <div>
                  <strong>Plot Type:</strong> {plotType.replace('_', ' ')}
                </div>
                <div>
                  <strong>Resolution:</strong> {resolution}×{resolution}
                </div>
                <div>
                  <strong>Functions:</strong> {Object.values(functions).reduce((total, category) => total + Object.keys(category).length, 0)} total
                </div>
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
                <h2 className="text-2xl font-bold">LaTeX Function Builder</h2>
                <button
                  onClick={() => setShowLatexBuilder(false)}
                  className="text-gray-400 hover:text-white text-2xl"
                >
                  ×
                </button>
              </div>
              <LaTeXFunctionBuilder
                onFunctionCreated={(functionData) => {
                  handleFunctionCreated(functionData);
                  setShowLatexBuilder(false);
                }}
                onClose={() => setShowLatexBuilder(false)}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}