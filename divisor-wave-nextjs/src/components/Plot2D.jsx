'use client';

import { useMemo } from 'react';
import dynamic from 'next/dynamic';

// Dynamically import Plotly to avoid SSR issues
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

export default function Plot2D({ 
  data, 
  colormap = 'Viridis',
  showContours = false,
  showColorbar = true 
}) {
  const plotData = useMemo(() => {
    const { x_values, y_values, z_values } = data;
    
    return [{
      type: 'heatmap',
      x: x_values,
      y: y_values,
      z: z_values,
      colorscale: colormap,
      showscale: showColorbar,
      hoverongaps: false,
      hovertemplate: 
        '<b>Real</b>: %{x:.3f}<br>' +
        '<b>Imaginary</b>: %{y:.3f}<br>' +
        '<b>|f(z)|</b>: %{z:.6f}<br>' +
        '<extra></extra>',
    }];
  }, [data, colormap, showColorbar]);

  const contourData = useMemo(() => {
    if (!showContours) return [];
    
    const { x_values, y_values, z_values } = data;
    
    return [{
      type: 'contour',
      x: x_values,
      y: y_values,
      z: z_values,
      showscale: false,
      contours: {
        coloring: 'lines',
        showlabels: true,
        labelfont: { size: 10, color: 'white' },
      },
      line: { color: 'rgba(255, 255, 255, 0.6)', width: 1 },
      opacity: 0.8,
    }];
  }, [data, showContours]);

  const layout = useMemo(() => ({
    title: {
      text: `${data.metadata.function_name} - 2D Heatmap`,
      font: { color: 'white', size: 16 },
    },
    xaxis: {
      title: { text: 'Real Part (Re z)', font: { color: 'white' } },
      color: 'white',
      gridcolor: 'rgba(255, 255, 255, 0.2)',
      zerolinecolor: 'rgba(255, 255, 255, 0.4)',
    },
    yaxis: {
      title: { text: 'Imaginary Part (Im z)', font: { color: 'white' } },
      color: 'white',
      gridcolor: 'rgba(255, 255, 255, 0.2)',
      zerolinecolor: 'rgba(255, 255, 255, 0.4)',
    },
    plot_bgcolor: 'rgba(0, 0, 0, 0)',
    paper_bgcolor: 'rgba(0, 0, 0, 0)',
    font: { color: 'white' },
    coloraxis: {
      colorbar: {
        title: { text: '|f(z)|', font: { color: 'white' } },
        tickfont: { color: 'white' },
        outlinecolor: 'rgba(255, 255, 255, 0.3)',
        bordercolor: 'rgba(255, 255, 255, 0.3)',
      },
    },
    margin: { t: 60, r: 80, b: 60, l: 80 },
    autosize: true,
  }), [data.metadata.function_name]);

  const config = {
    responsive: true,
    displayModeBar: true,
    displaylogo: false,
    modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
    toImageButtonOptions: {
      format: 'png',
      filename: `${data.metadata.function_name}_2d_plot`,
      height: 800,
      width: 1200,
      scale: 2,
    },
  };

  return (
    <div className="w-full h-full bg-black rounded-lg border border-white/10 overflow-hidden">
      <div className="p-4">
        {/* Function Info */}
        <div className="mb-4 text-white">
          <div className="flex justify-between items-start">
            <div>
              <h3 className="text-lg font-semibold">{data.metadata.function_name}</h3>
              <p className="text-sm text-gray-400">
                Resolution: {data.metadata.resolution}×{data.metadata.resolution} | 
                Range: Re ∈ [{data.metadata.x_range[0]}, {data.metadata.x_range[1]}], 
                Im ∈ [{data.metadata.y_range[0]}, {data.metadata.y_range[1]}]
              </p>
            </div>
            <div className="text-right text-sm text-gray-400">
              <div>Min: {data.metadata.statistics.z_min.toFixed(6)}</div>
              <div>Max: {data.metadata.statistics.z_max.toFixed(6)}</div>
              <div>Mean: {data.metadata.statistics.z_mean.toFixed(6)}</div>
            </div>
          </div>
        </div>
        
        {/* Plot */}
        <div className="aspect-square">
          <Plot
            data={[...plotData, ...contourData]}
            layout={layout}
            config={config}
            style={{ width: '100%', height: '100%' }}
            useResizeHandler={true}
          />
        </div>
        
        {/* Color Scale Options */}
        <div className="mt-4 flex flex-wrap gap-2">
          <span className="text-sm text-gray-400">Color scales:</span>
          {['Viridis', 'Plasma', 'Inferno', 'Magma', 'Cividis', 'Hot', 'Cool', 'RdYlBu', 'Spectral'].map((scale) => (
            <button
              key={scale}
              onClick={() => {/* TODO: Update colormap */}}
              className={`px-2 py-1 text-xs rounded transition-colors ${
                colormap === scale 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
            >
              {scale}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}