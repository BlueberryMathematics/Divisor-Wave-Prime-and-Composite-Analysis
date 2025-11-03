/**
 * DivisorWavePlot3D - Real-time 3D visualization of divisor wave functions
 * Integrates with your Python backend to display actual mathematical computations
 */

'use client';

import { useEffect, useRef, useState } from 'react';
import { divisorWaveAPI } from '@/lib/api';

export default function DivisorWavePlot3D({ 
  functionId = 'product_of_sin', 
  normalize = false,
  width = 800,
  height = 600,
  xRange = [1, 15],
  yRange = [0, 15],
  resolution = 30
}) {
  const canvasRef = useRef(null);
  const [plotData, setPlotData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Generate the plot data from your Python backend
  const generatePlot = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await divisorWaveAPI.generateDivisorWavePlot(functionId, {
        xRange,
        yRange,
        resolution,
        normalize,
        plotType: '3D'
      });
      
      if (response.data?.success) {
        setPlotData(response.data.data);
      } else {
        throw new Error('Failed to generate plot data');
      }
      
    } catch (err) {
      setError(err.message);
      console.error('Plot generation error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Draw the 3D surface using Canvas 2D context (simplified 3D projection)
  const drawPlot = () => {
    if (!plotData || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    const { x, y, z } = plotData;
    const rows = z.length;
    const cols = z[0].length;
    
    // Simple 3D projection parameters
    const scale = Math.min(width, height) / Math.max(xRange[1] - xRange[0], yRange[1] - yRange[0]);
    const centerX = width / 2;
    const centerY = height / 2;
    const angleX = Math.PI / 6; // 30 degrees
    const angleY = Math.PI / 4; // 45 degrees
    
    // Find min/max for color mapping
    const flatZ = z.flat();
    const minZ = Math.min(...flatZ);
    const maxZ = Math.max(...flatZ);
    const zRange = maxZ - minZ;
    
    // Function to project 3D to 2D
    const project3D = (x3d, y3d, z3d) => {
      const x2d = centerX + (x3d * Math.cos(angleY) - y3d * Math.sin(angleY)) * scale * 0.1;
      const y2d = centerY - (x3d * Math.sin(angleY) * Math.sin(angleX) + 
                           y3d * Math.cos(angleY) * Math.sin(angleX) + 
                           z3d * Math.cos(angleX)) * scale * 0.1;
      return [x2d, y2d];
    };
    
    // Color function based on function value
    const getColor = (zVal) => {
      const normalized = zRange > 0 ? (zVal - minZ) / zRange : 0;
      
      // Create beautiful color gradient for your divisor waves
      if (normalized < 0.2) {
        // Deep blue for zeros (primes create cusps near zero)
        return `rgb(${Math.floor(normalized * 255)}, ${Math.floor(normalized * 100)}, 255)`;
      } else if (normalized < 0.5) {
        // Purple to pink transition
        const t = (normalized - 0.2) / 0.3;
        return `rgb(${Math.floor(100 + t * 155)}, ${Math.floor(t * 100)}, ${Math.floor(255 - t * 100)})`;
      } else {
        // Yellow to red for high values (composite number peaks)
        const t = (normalized - 0.5) / 0.5;
        return `rgb(255, ${Math.floor(255 - t * 155)}, ${Math.floor((1 - t) * 100)})`;
      }
    };
    
    // Draw the surface as small rectangles
    for (let i = 0; i < rows - 1; i++) {
      for (let j = 0; j < cols - 1; j++) {
        const x1 = x[i][j];
        const y1 = y[i][j];
        const z1 = z[i][j];
        
        const x2 = x[i][j + 1];
        const y2 = y[i][j + 1];
        const z2 = z[i][j + 1];
        
        const x3 = x[i + 1][j];
        const y3 = y[i + 1][j];
        const z3 = z[i + 1][j];
        
        // Project corners
        const [px1, py1] = project3D(x1, y1, z1);
        const [px2, py2] = project3D(x2, y2, z2);
        const [px3, py3] = project3D(x3, y3, z3);
        
        // Average height for color
        const avgZ = (z1 + z2 + z3) / 3;
        
        ctx.fillStyle = getColor(avgZ);
        ctx.beginPath();
        ctx.moveTo(px1, py1);
        ctx.lineTo(px2, py2);
        ctx.lineTo(px3, py3);
        ctx.closePath();
        ctx.fill();
      }
    }
    
    // Add function information overlay
    ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
    ctx.fillRect(10, 10, 300, 100);
    ctx.fillStyle = 'black';
    ctx.font = '14px monospace';
    ctx.fillText(`Function: ${functionId}`, 20, 30);
    ctx.fillText(`Range: x[${xRange[0]}, ${xRange[1]}], y[${yRange[0]}, ${yRange[1]}]`, 20, 50);
    ctx.fillText(`Normalized: ${normalize ? 'Yes' : 'No'}`, 20, 70);
    ctx.fillText(`Min/Max: ${minZ.toFixed(3)} / ${maxZ.toFixed(3)}`, 20, 90);
  };

  // Generate plot when component mounts or parameters change
  useEffect(() => {
    generatePlot();
  }, [functionId, normalize, xRange, yRange, resolution]);

  // Draw plot when data is available
  useEffect(() => {
    if (plotData) {
      drawPlot();
    }
  }, [plotData, width, height]);

  const handleRegeneratePlot = () => {
    generatePlot();
  };

  return (
    <div className="divisor-wave-plot-3d">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold">
          Divisor Wave 3D Visualization: {functionId}
        </h3>
        <button
          onClick={handleRegeneratePlot}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-500 text-white rounded transition-colors"
        >
          {loading ? '🔄 Computing...' : '🔄 Regenerate'}
        </button>
      </div>
      
      {error ? (
        <div className="bg-red-900/20 border border-red-500/50 rounded p-4 text-red-300">
          <p className="font-medium">Plotting Error:</p>
          <p className="text-sm mt-1">{error}</p>
          <button 
            onClick={handleRegeneratePlot}
            className="mt-2 px-3 py-1 bg-red-600 hover:bg-red-700 text-white rounded text-sm"
          >
            Retry
          </button>
        </div>
      ) : (
        <div className="relative">
          <canvas
            ref={canvasRef}
            width={width}
            height={height}
            className="border border-white/20 rounded bg-gray-900"
            style={{ display: loading ? 'none' : 'block' }}
          />
          
          {loading && (
            <div 
              className="flex items-center justify-center bg-gray-900 border border-white/20 rounded"
              style={{ width, height }}
            >
              <div className="text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
                <p className="text-white">Computing divisor wave function...</p>
                <p className="text-gray-400 text-sm mt-1">
                  Evaluating {resolution}×{resolution} complex points
                </p>
              </div>
            </div>
          )}
        </div>
      )}
      
      <div className="mt-4 text-sm text-gray-400">
        <p>
          <strong>Visualization Info:</strong> This plot shows the magnitude of your {functionId} function
          in the complex plane. Cusps indicate prime numbers, curves indicate composite numbers.
        </p>
        <p className="mt-1">
          <strong>Color Scale:</strong> Blue (zeros/cusps) → Purple → Pink → Yellow → Red (peaks)
        </p>
      </div>
    </div>
  );
}