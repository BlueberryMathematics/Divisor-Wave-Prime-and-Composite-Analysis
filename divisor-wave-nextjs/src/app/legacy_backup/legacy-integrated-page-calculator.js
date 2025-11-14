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
        addDebugLog(`Backend connected: ${data.message}`, 'success');
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

  // Load functions from API
  const loadFunctions = async () => {
    try {
      const response = await fetch(`${API_BASE}/functions`);
      const data = await response.json();
      setFunctions(data.functions_by_category || {});
      addDebugLog(`Loaded ${Object.keys(data.functions_by_category || {}).length} function categories`, 'success');
    } catch (error) {
      addDebugLog(`Failed to load functions: ${error.message}`, 'error');
    }
  };

  // Handle custom function creation
  const handleFunctionCreated = (functionData) => {
    addDebugLog(`Custom function "${functionData.name}" created successfully`, 'success');
    loadFunctions(); // Reload functions to include the new one
    setSelectedFunction(functionData.name);
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
        loadFunctions();
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
      addDebugLog('Cannot generate plot: backend not connected', 'error');
      return;
    }

    setIsGenerating(true);
    addDebugLog(`Generating ${plotType} plot for ${selectedFunction}...`, 'info');

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
          resolution: resolution,
          colormap: colormap,
          canvas_size: canvasSize,
          light_shading: lightShading,
          axis_tick_spacing: axisTick,
          title_override: titleOverride || ''
        })
      });

      const data = await response.json();
      
      if (response.ok) {
        setPlotImage(`data:image/png;base64,${data.image_base64}`);
        setFunctionData(data);
        addDebugLog(`Plot generated successfully (${resolution}×${resolution})`, 'success');
      } else {
        throw new Error(data.detail || 'Plot generation failed');
      }
    } catch (error) {
      addDebugLog(`Plot generation failed: ${error.message}`, 'error');
    } finally {
      setIsGenerating(false);
    }
  };

  // Load functions when connected
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
      {/* Header */}
      <header className="bg-black/20 backdrop-blur-sm border-b border-white/10 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                Advanced Divisor Wave Analysis - Calculator Mode
              </h1>
              <p className="text-gray-300 text-sm">Graphing Calculator Style Interface</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className={`px-3 py-1 rounded text-sm ${
                connectionStatus === 'connected' ? 'bg-green-900/30 text-green-300' :
                connectionStatus === 'disconnected' ? 'bg-red-900/30 text-red-300' :
                'bg-yellow-900/30 text-yellow-300'
              }`}>
                {connectionStatus === 'connected' ? '✅ Backend Connected' : 
                 connectionStatus === 'disconnected' ? '❌ Offline' : 
                 '🔄 Checking...'}
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          
          {/* LEFT PANEL - Calculator Controls */}
          <div className="lg:col-span-1 space-y-4">
            
            {/* FUNCTION Section (Y= equivalent) */}
            <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-lg p-4">
              <h3 className="text-lg font-bold mb-3 text-blue-400 border-b border-blue-400/30 pb-2">
                📊 FUNCTION (Y=)
              </h3>
              
              <div className="space-y-3">
                {Object.entries(functions).map(([category, categoryFunctions]) => (
                  <div key={category} className="space-y-2">
                    <h4 className="text-sm font-semibold text-gray-300 uppercase tracking-wide">
                      {category}
                    </h4>
                    <div className="grid grid-cols-1 gap-1">
                      {Object.entries(categoryFunctions).map(([funcId, funcInfo]) => (
                        <button
                          key={funcId}
                          onClick={() => setSelectedFunction(funcId)}
                          className={`p-2 rounded text-xs text-left transition-colors ${
                            selectedFunction === funcId
                              ? 'bg-blue-600 text-white border border-blue-400'
                              : 'bg-gray-800 text-gray-300 hover:bg-gray-700 border border-transparent'
                          }`}
                        >
                          <div className="font-medium">{funcInfo.name}</div>
                          <div className="text-xs opacity-75">{funcInfo.description}</div>
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
                
                {/* Custom Function Builder */}
                <button
                  onClick={() => setShowLatexBuilder(true)}
                  className="w-full p-3 bg-purple-600 hover:bg-purple-700 rounded text-sm font-medium transition-colors"
                >
                  ➕ Build Custom Function
                </button>
              </div>
            </div>

            {/* WINDOW Section (Range Settings) */}
            <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-lg p-4">
              <h3 className="text-lg font-bold mb-3 text-green-400 border-b border-green-400/30 pb-2">
                📐 WINDOW
              </h3>
              
              <div className="space-y-3">
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <label className="block text-xs font-medium mb-1">Xmin</label>
                    <input
                      type="number"
                      value={xRange[0]}
                      onChange={(e) => setXRange([parseFloat(e.target.value) || 0, xRange[1]])}
                      className="w-full px-2 py-1 bg-gray-800 border border-gray-600 rounded text-sm"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium mb-1">Xmax</label>
                    <input
                      type="number"
                      value={xRange[1]}
                      onChange={(e) => setXRange([xRange[0], parseFloat(e.target.value) || 0])}
                      className="w-full px-2 py-1 bg-gray-800 border border-gray-600 rounded text-sm"
                    />
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <label className="block text-xs font-medium mb-1">Ymin</label>
                    <input
                      type="number"
                      value={yRange[0]}
                      onChange={(e) => setYRange([parseFloat(e.target.value) || 0, yRange[1]])}
                      className="w-full px-2 py-1 bg-gray-800 border border-gray-600 rounded text-sm"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium mb-1">Ymax</label>
                    <input
                      type="number"
                      value={yRange[1]}
                      onChange={(e) => setYRange([yRange[0], parseFloat(e.target.value) || 0])}
                      className="w-full px-2 py-1 bg-gray-800 border border-gray-600 rounded text-sm"
                    />
                  </div>
                </div>
                
                <div>
                  <label className="block text-xs font-medium mb-1">Resolution</label>
                  <select
                    value={resolution}
                    onChange={(e) => setResolution(parseInt(e.target.value))}
                    className="w-full px-2 py-1 bg-gray-800 border border-gray-600 rounded text-sm"
                  >
                    <option value={100}>100×100 (Fast)</option>
                    <option value={200}>200×200 (Normal)</option>
                    <option value={400}>400×400 (High)</option>
                    <option value={600}>600×600 (Ultra)</option>
                  </select>
                </div>
              </div>
            </div>

            {/* MODE Section (Plot Type) */}
            <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-lg p-4">
              <h3 className="text-lg font-bold mb-3 text-orange-400 border-b border-orange-400/30 pb-2">
                🎮 MODE
              </h3>
              
              <div className="space-y-2">
                {[
                  { value: '2D_Real', label: '2D Real Plot', desc: 'Real domain visualization' },
                  { value: '2D_Complex', label: '2D Complex Plot', desc: 'Complex plane mapping' },
                  { value: '3D_Real', label: '3D Real Plot', desc: '3D surface visualization' },
                  { value: '3D_Complex', label: '3D Complex Plot', desc: '3D complex surface' }
                ].map(type => (
                  <button
                    key={type.value}
                    onClick={() => setPlotType(type.value)}
                    className={`w-full p-2 rounded text-left text-sm transition-colors ${
                      plotType === type.value
                        ? 'bg-orange-600 text-white border border-orange-400'
                        : 'bg-gray-800 text-gray-300 hover:bg-gray-700 border border-transparent'
                    }`}
                  >
                    <div className="font-medium">{type.label}</div>
                    <div className="text-xs opacity-75">{type.desc}</div>
                  </button>
                ))}
              </div>
              
              <div className="mt-3 pt-3 border-t border-gray-700">
                <label className="block text-xs font-medium mb-1">Normalize</label>
                <select
                  value={normalizeType}
                  onChange={(e) => setNormalizeType(e.target.value)}
                  className="w-full px-2 py-1 bg-gray-800 border border-gray-600 rounded text-sm"
                >
                  <option value="Y">Y-axis normalization</option>
                  <option value="N">No normalization</option>
                  <option value="Z">Z-axis normalization</option>
                </select>
              </div>
            </div>

            {/* FORMAT Section (Visual Settings) */}
            <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-lg p-4">
              <h3 className="text-lg font-bold mb-3 text-purple-400 border-b border-purple-400/30 pb-2">
                🎨 FORMAT
              </h3>
              
              <div className="space-y-3">
                <div>
                  <label className="block text-xs font-medium mb-1">Colormap</label>
                  <select
                    value={colormap}
                    onChange={(e) => setColormap(e.target.value)}
                    className="w-full px-2 py-1 bg-gray-800 border border-gray-600 rounded text-sm"
                  >
                    <option value="6">Viridis (Default)</option>
                    <option value="1">Plasma</option>
                    <option value="2">Inferno</option>
                    <option value="3">Magma</option>
                    <option value="4">Cividis</option>
                    <option value="5">Twilight</option>
                    <option value="7">Coolwarm</option>
                    <option value="8">Rainbow</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-xs font-medium mb-1">Canvas Size</label>
                  <select
                    value={canvasSize}
                    onChange={(e) => setCanvasSize(e.target.value)}
                    className="w-full px-2 py-1 bg-gray-800 border border-gray-600 rounded text-sm"
                  >
                    <option value="16x9">16:9 Widescreen</option>
                    <option value="4x3">4:3 Standard</option>
                    <option value="1x1">1:1 Square</option>
                  </select>
                </div>
                
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={lightShading}
                    onChange={(e) => setLightShading(e.target.checked)}
                    className="rounded"
                  />
                  <label className="text-xs font-medium">Light Shading</label>
                </div>
                
                <div>
                  <label className="block text-xs font-medium mb-1">Axis Tick Spacing</label>
                  <input
                    type="number"
                    step="0.1"
                    value={axisTick}
                    onChange={(e) => setAxisTick(parseFloat(e.target.value) || 1.0)}
                    className="w-full px-2 py-1 bg-gray-800 border border-gray-600 rounded text-sm"
                  />
                </div>
                
                <div>
                  <label className="block text-xs font-medium mb-1">Custom Title</label>
                  <input
                    type="text"
                    value={titleOverride}
                    onChange={(e) => setTitleOverride(e.target.value)}
                    placeholder="Leave empty for auto-title"
                    className="w-full px-2 py-1 bg-gray-800 border border-gray-600 rounded text-sm"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* RIGHT PANEL - Display and Controls */}
          <div className="lg:col-span-3 space-y-6">
            
            {/* DISPLAY Section (Main Graph Area) */}
            <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-lg p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-bold text-gray-100">📊 DISPLAY</h3>
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
                          <span>Res: {functionData.resolution}×{functionData.resolution}</span>
                          <span>X: [{functionData.x_min}, {functionData.x_max}] Y: [{functionData.y_min}, {functionData.y_max}]</span>
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
                          <p className="text-gray-400 mt-2">Start the Python backend server</p>
                        </>
                      ) : isGenerating ? (
                        <>
                          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
                          <p className="text-lg font-medium">Computing Plot</p>
                          <p className="text-gray-400 mt-2">
                            {plotType.replace('_', ' ')} visualization with {resolution}×{resolution} resolution
                          </p>
                        </>
                      ) : (
                        <>
                          <div className="text-4xl mb-4">📊</div>
                          <p className="text-lg font-medium">Ready to Plot</p>
                          <p className="text-gray-400 mt-2">
                            Configure settings and press GRAPH to generate visualization
                          </p>
                        </>
                      )}
                    </div>
                  </div>
                )}
              </div>

              {/* GRAPH Button - Calculator Style */}
              <div className="mt-6 flex justify-center">
                <button
                  onClick={generatePlot}
                  disabled={isGenerating || connectionStatus !== 'connected'}
                  className={`px-8 py-4 rounded-lg text-lg font-bold transition-all transform ${
                    isGenerating || connectionStatus !== 'connected'
                      ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                      : 'bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700 hover:scale-105 shadow-lg hover:shadow-xl'
                  }`}
                >
                  {isGenerating ? (
                    <>
                      <span className="animate-pulse">Computing...</span>
                    </>
                  ) : (
                    <>
                      📈 GRAPH
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* Status and Info Panels */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              
              {/* Function Analysis */}
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

              {/* System Status */}
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
                
                <div className="mt-3 pt-3 border-t border-gray-700 text-xs text-gray-300 space-y-1">
                  <div>Function: <span className="text-white">{selectedFunction}</span></div>
                  <div>Plot Type: <span className="text-white">{plotType.replace('_', ' ')}</span></div>
                  <div>Resolution: <span className="text-white">{resolution}×{resolution}</span></div>
                  <div>Total Functions: <span className="text-white">{Object.values(functions).reduce((total, category) => total + Object.keys(category).length, 0)}</span></div>
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