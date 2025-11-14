# NextJS Frontend Component Documentation

## Overview
The NextJS frontend provides an interactive web interface for the Divisor Wave Analysis System. It offers real-time function visualization, custom function creation, and mathematical exploration tools.

## Architecture

### Framework Stack
- **NextJS 14+**: React-based framework with SSR support
- **React 18**: Component-based UI library  
- **Tailwind CSS**: Utility-first styling
- **JavaScript/JSX**: Primary development language

### Key Components

#### Main Calculator Interface
- **Location**: `src/app/page.jsx`
- **Purpose**: Primary user interface for function analysis
- **Features**: Function selection, parameter controls, real-time plotting

#### LaTeX Function Builder  
- **Location**: `src/app/LaTeXFunctionBuilder.js`
- **Purpose**: Visual LaTeX formula editor
- **Features**: Symbol palette, real-time preview, function validation

#### Compact Calculator
- **Location**: `src/app/compact-calculator.js` 
- **Purpose**: Streamlined function evaluation interface
- **Features**: Quick plotting, parameter adjustment, export capabilities

### Visualization Components

#### 2D Plotting
- **Location**: `src/components/Plot2D.jsx`
- **Purpose**: Complex function contour visualization
- **Features**: Interactive zoom, colormap selection, export options

#### 3D Plotting  
- **Location**: `src/components/Plot3D.jsx`
- **Purpose**: Surface visualization of complex functions
- **Features**: Rotation controls, lighting effects, high-resolution rendering

#### Divisor Wave Plot
- **Location**: `src/components/DivisorWavePlot3D.js`
- **Purpose**: Specialized visualization for divisor wave functions
- **Features**: Optimized rendering, mathematical overlays

### Utility Components

#### LaTeX Converter
- **Location**: `src/components/LatexConverter.jsx`
- **Purpose**: LaTeX formula rendering and conversion
- **Features**: MathJax integration, formula validation

#### API Interface
- **Location**: `src/lib/api.js`
- **Purpose**: Backend API communication
- **Features**: Request handling, error management, response caching

#### State Management
- **Location**: `src/lib/store.js`
- **Purpose**: Application state management  
- **Features**: Function data caching, UI state persistence

## Installation and Setup

### Prerequisites
```bash
Node.js 18+ 
npm or yarn package manager
```

### Installation
```bash
# Install dependencies
npm install

# Development server
npm run dev

# Production build
npm run build
npm start
```

### Environment Configuration
```env
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NODE_ENV=development
NEXT_TELEMETRY_DISABLED=1
```

## Features

### Function Visualization
- **Real-time Plotting**: Interactive 2D/3D visualization
- **Multiple Colormaps**: Viridis, plasma, inferno, magma schemes
- **High Resolution**: Configurable resolution up to 512x512 points
- **Export Options**: PNG, SVG, base64 formats

### Custom Function Creation
- **Visual LaTeX Editor**: Symbol palette with common mathematical notation
- **Real-time Preview**: Immediate formula rendering and validation
- **Function Testing**: Built-in validation with sample point evaluation  
- **Integration**: Seamless addition to function library

### Mathematical Analysis
- **Function Evaluation**: Point-wise evaluation at complex coordinates
- **Parameter Exploration**: Real-time parameter adjustment
- **Comparison Tools**: Side-by-side function analysis
- **Research Mode**: Advanced controls for mathematical investigation

### User Interface
- **Responsive Design**: Mobile and desktop compatibility
- **Dark Theme**: Mathematical research optimized color scheme
- **Keyboard Shortcuts**: Power user efficiency features
- **Accessibility**: Screen reader compatible, keyboard navigation

## API Integration

### Backend Communication
The frontend communicates with the Python backend via RESTful API:

```javascript
// Function plotting
const response = await fetch(`${API_URL}/plot-optimized`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    function_name: 'product_of_sin',
    plot_type: '3D',
    resolution: 256,
    x_range: [-5, 5],
    y_range: [-5, 5],
    normalize_type: 'N'
  })
});
```

### Error Handling
- **Network Errors**: Automatic retry with exponential backoff
- **Validation Errors**: User-friendly error messages
- **API Timeouts**: Configurable timeout with progress indicators

### Performance Optimization
- **Request Caching**: Intelligent caching of function data
- **Lazy Loading**: On-demand component loading
- **Image Optimization**: Automatic image compression and caching

## User Interface Components

### Function Selection
- **Dropdown Interface**: Organized by mathematical category
- **Search Functionality**: Quick function discovery
- **Favorites System**: Bookmark frequently used functions
- **Recent Functions**: Quick access to recently analyzed functions

### Parameter Controls
- **Range Sliders**: Interactive domain specification
- **Resolution Control**: Quality vs performance balance
- **Normalization Options**: X, Y, Z, XYZ, N mode selection
- **Colormap Selection**: Visual style customization

### Visualization Controls
- **2D Controls**: Zoom, pan, colormap selection
- **3D Controls**: Rotation, elevation, azimuth adjustment
- **Export Options**: High-resolution image generation
- **Animation**: Parameter sweeps and time evolution

## Development

### Component Structure
```
src/
├── app/
│   ├── page.jsx                 # Main application page
│   ├── layout.jsx              # Root layout component
│   ├── LaTeXFunctionBuilder.js # Custom function creator
│   └── compact-calculator.js   # Streamlined interface
├── components/
│   ├── Plot2D.jsx              # 2D visualization
│   ├── Plot3D.jsx              # 3D visualization  
│   ├── DivisorWavePlot3D.js    # Specialized plotting
│   └── LatexConverter.jsx      # LaTeX processing
└── lib/
    ├── api.js                  # Backend communication
    └── store.js                # State management
```

### Adding New Features

#### New Visualization Component
```jsx
import { useState, useEffect } from 'react';

export default function NewVisualization({ functionName, parameters }) {
  const [plotData, setPlotData] = useState(null);
  
  useEffect(() => {
    // Fetch data from backend
    fetchVisualizationData(functionName, parameters)
      .then(setPlotData);
  }, [functionName, parameters]);
  
  return (
    <div className="visualization-container">
      {plotData && <canvas>/* Render visualization */</canvas>}
    </div>
  );
}
```

#### API Integration
```javascript
// Add new API endpoint
export async function callNewEndpoint(parameters) {
  const response = await fetch(`${API_BASE}/new-endpoint`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(parameters)
  });
  
  if (!response.ok) {
    throw new Error(`API call failed: ${response.statusText}`);
  }
  
  return response.json();
}
```

## Configuration

### Build Configuration
- **nextjs.config.js**: Next.js build settings
- **tailwind.config.js**: CSS framework configuration
- **package.json**: Dependencies and scripts

### Performance Settings
```javascript
// next.config.js
const nextConfig = {
  images: {
    domains: ['localhost'],
    formats: ['image/webp', 'image/avif'],
  },
  experimental: {
    optimizeCss: true,
    optimizeImages: true,
  }
};
```

## Testing

### Component Testing
- **Unit Tests**: Individual component functionality
- **Integration Tests**: API communication validation
- **UI Tests**: User interaction workflows
- **Performance Tests**: Rendering speed and memory usage

### Manual Testing Checklist
1. Function selection and plotting
2. Custom function creation workflow
3. Parameter adjustment responsiveness
4. Export functionality
5. Cross-browser compatibility
6. Mobile responsiveness

## Deployment

### Development
```bash
npm run dev
# Access at http://localhost:3000
```

### Production
```bash
npm run build
npm start
# Access at http://localhost:3000
```

### Environment Variables
- **NEXT_PUBLIC_API_URL**: Backend API endpoint
- **NODE_ENV**: Development/production mode
- **NEXT_TELEMETRY_DISABLED**: Disable telemetry collection

## Troubleshooting

### Common Issues
1. **API Connection**: Verify backend is running on correct port
2. **Build Errors**: Check Node.js version compatibility
3. **Styling Issues**: Verify Tailwind CSS configuration
4. **Performance**: Monitor bundle size and optimize imports

### Performance Optimization
- **Code Splitting**: Use dynamic imports for large components
- **Image Optimization**: Implement Next.js Image component
- **Caching**: Leverage browser caching for static assets
- **Bundle Analysis**: Use webpack-bundle-analyzer

## Research Applications

### Mathematical Exploration
- Interactive parameter space exploration
- Real-time hypothesis testing  
- Visual pattern recognition
- Collaborative research interface

### Educational Use
- Mathematical concept visualization
- Interactive demonstrations
- Student exploration tools
- Classroom presentation mode