/**
 * Enhanced Divisor Wave Analysis Frontend
 * Direct integration with your Python matplotlib plotting system
 * Real-time visualization of your mathematical research
 */

'use client';

import { useEffect, useState, useRef } from 'react';

export default function DivisorWaveAnalysis() {
  // State management
  const [connectionStatus, setConnectionStatus] = useState('checking');
  const [selectedFunction, setSelectedFunction] = useState('product_of_sin');
  const [plotMode, setPlotMode] = useState('2D');
  const [normalize, setNormalize] = useState(false);
  const [xRange, setXRange] = useState([1, 15]);
  const [yRange, setYRange] = useState([0, 15]);
  const [plotImage, setPlotImage] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [functionData, setFunctionData] = useState(null);
  const [debugInfo, setDebugInfo] = useState([]);
  const [plotSettings, setPlotSettings] = useState({
    resolution: 100,
    colormap: 'viridis',
    magnification: 0.05
  });

  // Backend API base URL
  const API_BASE = 'http://localhost:8000';

  // Add debug log
  const addDebugLog = (message, type = 'info') => {
    const timestamp = new Date().toLocaleTimeString();
    setDebugInfo(prev => [...prev.slice(-10), { timestamp, message, type }]);
  };

  // Check backend connection
  const checkConnection = async () => {
    try {
      addDebugLog('Checking backend connection...', 'info');
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

  // Generate plot using your Python backend
  const generatePlot = async () => {
    if (connectionStatus !== 'connected') {
      addDebugLog('Cannot generate plot: backend not connected', 'error');
      return;
    }

    try {
      setIsGenerating(true);
      addDebugLog(`Generating ${selectedFunction} plot...`, 'info');

      // Call your existing plotting endpoint
      const plotRequest = {
        function_name: selectedFunction,
        plot_type: plotMode,
        x_min: xRange[0],
        x_max: xRange[1],
        y_min: yRange[0], 
        y_max: yRange[1],
        resolution: plotSettings.resolution,
        normalize: normalize,
        colormap: plotSettings.colormap,
        magnification: plotSettings.magnification
      };

      addDebugLog(`Plot request: ${JSON.stringify(plotRequest)}`, 'debug');

      const response = await fetch(`${API_BASE}/plot`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(plotRequest)
      });

      if (!response.ok) {
        throw new Error(`Plot generation failed: ${response.status}`);
      }

      const result = await response.json();
      
      if (result.success && result.image_base64) {
        setPlotImage(`data:image/png;base64,${result.image_base64}`);
        addDebugLog('Plot generated successfully', 'success');
        
        // Also save any function data
        if (result.function_info) {
          setFunctionData(result.function_info);
        }
      } else {
        throw new Error(result.error || 'Plot generation failed');
      }

    } catch (error) {
      addDebugLog(`Plot generation error: ${error.message}`, 'error');
      setPlotImage(null);
    } finally {
      setIsGenerating(false);
    }
  };

  // Evaluate function at specific points (for prime/composite analysis)
  const evaluateAtPoints = async () => {
    try {
      addDebugLog('Evaluating function at integer points...', 'info');
      
      const points = Array.from({length: 18}, (_, i) => i + 2); // Points 2-19
      const response = await fetch(`${API_BASE}/evaluate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          function_name: selectedFunction,
          points: points,
          normalize: normalize
        })
      });

      if (response.ok) {
        const result = await response.json();
        setFunctionData(result);
        addDebugLog(`Evaluated ${points.length} points`, 'success');
      }
    } catch (error) {
      addDebugLog(`Evaluation error: ${error.message}`, 'error');
    }
  };

  // Initialize connection check
  useEffect(() => {
    checkConnection();
    const interval = setInterval(checkConnection, 10000); // Check every 10s
    return () => clearInterval(interval);
  }, []);

  // Available divisor wave functions from your research
  const availableFunctions = [
    { id: 'product_of_sin', name: 'Product of Sin a(z)', description: 'Infinite product ∏sin(πz/k) - Shows cusps at primes' },
    { id: 'product_of_product_representation_for_sin', name: 'Double Product b(z)', description: 'Prime indicator function - Zeros at composites' },
    { id: 'complex_playground_magnification_currated_functions_DEMO', name: 'Riesz Product', description: 'Normalized Riesz product demonstration' },
    { id: 'normalized_product_of_sin', name: 'Normalized a(z)', description: 'Gamma-normalized product of sin' },
    { id: 'viete_cosine_product', name: 'Viète Cosine', description: 'Viète infinite product of cosines' }
  ];

  // Prime numbers for analysis
  const primes = [2, 3, 5, 7, 11, 13, 17, 19];
  const isPrime = (n) => primes.includes(n);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 text-white">
      {/* Header */}
      <header className="bg-black/20 backdrop-blur-sm border-b border-white/10 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                Divisor Wave Complex Analysis
              </h1>
              <p className="text-gray-300 mt-1">Leo Borcherding's Prime Number Research Platform</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className={`px-3 py-1 rounded text-sm ${
                connectionStatus === 'connected' ? 'bg-green-900/30 text-green-300' :
                connectionStatus === 'disconnected' ? 'bg-red-900/30 text-red-300' :
                'bg-yellow-900/30 text-yellow-300'
              }`}>
                {connectionStatus === 'connected' ? '✅ Python Backend Active' : 
                 connectionStatus === 'disconnected' ? '❌ Backend Offline' : 
                 '🔄 Checking Connection...'}
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          
          {/* Controls Panel */}
          <div className="lg:col-span-1 space-y-6">
            
            {/* Function Selection */}
            <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-4">Function Selection</h3>
              
              <div className="space-y-3">
                {availableFunctions.map(func => (
                  <div key={func.id}>
                    <button
                      onClick={() => setSelectedFunction(func.id)}
                      className={`w-full text-left p-3 rounded border transition-colors ${
                        selectedFunction === func.id
                          ? 'bg-blue-600/30 border-blue-400/50'
                          : 'bg-white/5 border-white/10 hover:bg-white/10'
                      }`}
                    >
                      <div className="font-medium text-sm">{func.name}</div>
                      <div className="text-xs text-gray-400 mt-1">{func.description}</div>
                    </button>
                  </div>
                ))}
              </div>
            </div>

            {/* Plot Settings */}
            <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-4">Plot Settings</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Plot Type</label>
                  <select 
                    value={plotMode}
                    onChange={(e) => setPlotMode(e.target.value)}
                    className="w-full bg-gray-800 border border-gray-600 rounded px-3 py-2 text-white"
                  >
                    <option value="2D">2D Real Plot</option>
                    <option value="3D">3D Complex Plot</option>
                    <option value="contour">Contour Plot</option>
                  </select>
                </div>

                <div>
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={normalize}
                      onChange={(e) => setNormalize(e.target.checked)}
                      className="mr-2"
                    />
                    <span className="text-sm">Gamma Normalization</span>
                  </label>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">
                    X Range: [{xRange[0]}, {xRange[1]}]
                  </label>
                  <div className="flex space-x-2">
                    <input
                      type="number"
                      value={xRange[0]}
                      onChange={(e) => setXRange([+e.target.value, xRange[1]])}
                      className="w-20 bg-gray-800 border border-gray-600 rounded px-2 py-1 text-white text-sm"
                    />
                    <input
                      type="number"
                      value={xRange[1]}
                      onChange={(e) => setXRange([xRange[0], +e.target.value])}
                      className="w-20 bg-gray-800 border border-gray-600 rounded px-2 py-1 text-white text-sm"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">
                    Resolution: {plotSettings.resolution}
                  </label>
                  <input
                    type="range"
                    min="50"
                    max="500"
                    value={plotSettings.resolution}
                    onChange={(e) => setPlotSettings(prev => ({...prev, resolution: +e.target.value}))}
                    className="w-full"
                  />
                </div>
              </div>

              <button
                onClick={generatePlot}
                disabled={isGenerating || connectionStatus !== 'connected'}
                className="w-full mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white rounded transition-colors"
              >
                {isGenerating ? '🔄 Generating Plot...' : '🎨 Generate Plot'}
              </button>
            </div>

            {/* Quick Actions */}
            <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-4">Analysis Tools</h3>
              
              <div className="space-y-2">
                <button
                  onClick={evaluateAtPoints}
                  disabled={connectionStatus !== 'connected'}
                  className="w-full px-3 py-2 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white rounded text-sm transition-colors"
                >
                  Analyze Prime Pattern
                </button>
                
                <button
                  onClick={() => setXRange([1, 50])}
                  className="w-full px-3 py-2 bg-green-600 hover:bg-green-700 text-white rounded text-sm transition-colors"
                >
                  Extended Range (1-50)
                </button>
              </div>
            </div>
          </div>

          {/* Main Visualization Area */}
          <div className="lg:col-span-3 space-y-6">
            
            {/* Plot Display */}
            <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-semibold">
                  {availableFunctions.find(f => f.id === selectedFunction)?.name || selectedFunction}
                </h3>
                <div className="text-sm text-gray-400">
                  {plotMode} • {normalize ? 'Normalized' : 'Raw'} • Range: [{xRange[0]}, {xRange[1]}]
                </div>
              </div>

              <div className="relative">
                {plotImage ? (
                  <img 
                    src={plotImage} 
                    alt={`Plot of ${selectedFunction}`}
                    className="w-full h-auto max-h-96 object-contain bg-gray-900 rounded border border-white/10"
                  />
                ) : (
                  <div className="w-full h-96 bg-gray-900 rounded border border-white/10 flex items-center justify-center">
                    <div className="text-center">
                      {connectionStatus !== 'connected' ? (
                        <>
                          <div className="text-4xl mb-4">🔌</div>
                          <p className="text-lg font-medium">Backend Disconnected</p>
                          <p className="text-gray-400 mt-2">Start your Python server to see plots</p>
                          <code className="block mt-4 p-2 bg-black/30 rounded text-green-400 text-sm">
                            python src/api/enhanced_main.py
                          </code>
                        </>
                      ) : isGenerating ? (
                        <>
                          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
                          <p className="text-lg font-medium">Computing Divisor Wave Function</p>
                          <p className="text-gray-400 mt-2">
                            Calculating {selectedFunction} with {plotSettings.resolution}×{plotSettings.resolution} points
                          </p>
                        </>
                      ) : (
                        <>
                          <div className="text-4xl mb-4">📊</div>
                          <p className="text-lg font-medium">Ready to Generate Plot</p>
                          <p className="text-gray-400 mt-2">
                            Select a function and click "Generate Plot" to visualize your divisor wave research
                          </p>
                        </>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Function Analysis Results */}
            {functionData && (
              <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-4">Prime/Composite Analysis</h3>
                
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-2 text-sm">
                  {functionData.values?.map((value, index) => {
                    const n = index + 2; // Starting from 2
                    const magnitude = Math.abs(value);
                    const isP = isPrime(n);
                    
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
                        <div className="text-xs">|f({n})| = {magnitude.toFixed(4)}</div>
                      </div>
                    );
                  })}
                </div>

                <p className="text-gray-400 text-sm mt-4">
                  <strong>Observation:</strong> Notice the distinct behavior at prime vs composite numbers. 
                  Your divisor wave theory predicts cusps at primes and curves at composites.
                </p>
              </div>
            )}

            {/* Debug Information */}
            <div className="bg-black/20 backdrop-blur-sm border border-white/10 rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-4">System Information</h3>
              
              <div className="space-y-2 max-h-40 overflow-y-auto">
                {debugInfo.map((log, index) => (
                  <div key={index} className={`text-xs p-2 rounded ${
                    log.type === 'error' ? 'bg-red-900/20 text-red-300' :
                    log.type === 'success' ? 'bg-green-900/20 text-green-300' :
                    log.type === 'debug' ? 'bg-blue-900/20 text-blue-300' :
                    'bg-gray-900/20 text-gray-300'
                  }`}>
                    <span className="text-gray-500">[{log.timestamp}]</span> {log.message}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}