# API Reference Guide

## Base URL
```
http://localhost:8000
```

## Core Endpoints

### Function Management

#### GET `/functions`
Returns complete function registry with metadata
```json
{
  "success": true,
  "builtin_functions": {...},
  "custom_functions": {...},
  "total_count": 37
}
```

#### GET `/function/{function_id}`
Retrieve specific function information
```json
{
  "success": true,
  "function_id": "1",
  "name": "product_of_sin",
  "display_name": "Product of Sin",
  "description": "Primary divisor wave function",
  "category": "Core Products"
}
```

### Function Evaluation

#### POST `/evaluate`
Evaluate function at complex point
```json
{
  "function_name": "product_of_sin",
  "z_real": 2.0,
  "z_imag": 1.0,
  "normalize_type": "N"
}
```

Response:
```json
{
  "success": true,
  "result": 0.8414709848,
  "input": {"z": "2.0+1.0j", "normalize_type": "N"}
}
```

### Visualization

#### POST `/plot`
Generate function plots
```json
{
  "function_name": "product_of_sin",
  "plot_type": "3D",
  "resolution": 100,
  "x_range": [-5, 5],
  "y_range": [-5, 5],
  "colormap": "viridis",
  "normalize_type": "N"
}
```

Response:
```json
{
  "success": true,
  "image": "data:image/png;base64,iVBORw0KGgoAAAA...",
  "metadata": {
    "function_name": "product_of_sin",
    "plot_type": "3D",
    "computation_time": 1.23
  }
}
```

#### POST `/plot-optimized`
High-performance plotting endpoint
```json
{
  "function_name": "1",
  "plot_type": "3D",
  "resolution": 256,
  "x_range": [-10, 10],
  "y_range": [-10, 10],
  "colormap": "viridis",
  "normalize_type": "N",
  "elevation": 30,
  "azimuth": -70
}
```

### Custom Functions

#### POST `/custom-functions`
Create custom function from LaTeX
```json
{
  "name": "my_custom_function",
  "latex_formula": "\\sin(\\pi z) + \\cos(\\pi z)",
  "description": "Sine plus cosine function",
  "category": "custom"
}
```

Response:
```json
{
  "success": true,
  "message": "Custom function 'my_custom_function' created successfully",
  "function": {
    "name": "my_custom_function",
    "latex_formula": "\\sin(\\pi z) + \\cos(\\pi z)",
    "description": "Sine plus cosine function"
  }
}
```

#### GET `/custom-functions`
List all custom functions
```json
{
  "success": true,
  "custom_functions": {...},
  "count": 3
}
```

#### DELETE `/custom-functions/{function_name}`
Remove custom function

### LaTeX Integration

#### GET `/latex/formula/{function_name}`
Retrieve LaTeX formula for function
```json
{
  "success": true,
  "function_name": "product_of_sin",
  "latex_formula": "f(z) = \\left|\\prod_{k=2}^{z} \\sin\\left(\\frac{\\pi z}{k}\\right)\\right|",
  "description": "Product of Sin - Main divisor wave function"
}
```

#### GET `/latex/formulas`
Get all available LaTeX formulas
```json
{
  "success": true,
  "total_formulas": 34,
  "formulas": {...},
  "categories": ["Core Products", "Riesz Products", ...]
}
```

#### GET `/latex/keyboard`
LaTeX symbol palette for frontend
```json
{
  "success": true,
  "keyboard_layout": {
    "symbols": {
      "Greek Letters": [...],
      "Operations": [...],
      "Functions": [...]
    },
    "templates": {...}
  }
}
```

### System Information

#### GET `/health`
System health check
```json
{
  "status": "healthy",
  "api_version": "2.1.0",
  "available_functions": 37,
  "optimizations_active": true,
  "gpu_acceleration": "available"
}
```

#### GET `/status`
Detailed system status
```json
{
  "status": "operational",
  "version": "2.1.0",
  "optimizations": {
    "jit_compilation": "Numba JIT enabled",
    "gpu_acceleration": "CuPy GPU support"
  },
  "api_info": {
    "built_in_functions": 31,
    "custom_functions": 6,
    "normalization_modes": ["X", "Y", "Z", "XYZ", "N"]
  }
}
```

#### GET `/colormaps`
Available color schemes
```json
{
  "success": true,
  "colormaps": {
    "2D": ["viridis", "plasma", "inferno", "magma"],
    "3D": ["viridis", "coolwarm", "terrain", "ocean"]
  }
}
```

## Error Responses

### Standard Error Format
```json
{
  "success": false,
  "error": "Error description",
  "status_code": 400
}
```

### Common HTTP Status Codes
- `200`: Success
- `400`: Bad Request (invalid parameters)
- `404`: Not Found (function/endpoint not found)
- `422`: Validation Error (malformed request body)
- `500`: Internal Server Error

## Request/Response Headers

### Required Headers
```
Content-Type: application/json
Accept: application/json
```

### CORS Support
All endpoints support cross-origin requests for frontend integration.

## Normalization Types

- `X`: X-axis focused normalization
- `Y`: Y-axis focused normalization (original research mode)
- `Z`: Z-axis focused normalization  
- `XYZ`: Combined axis normalization
- `N`: Neutral normalization (default)

## Function Categories

- **Core Products**: Primary divisor wave functions
- **Riesz Products**: Harmonic analysis functions
- **Prime Indicators**: Prime detection functions  
- **Gamma Variants**: Gamma function modifications
- **Logarithmic Variants**: Natural logarithm functions
- **Basic Functions**: Elementary mathematical functions
- **Custom**: User-defined functions

## Performance Notes

- Use `/plot-optimized` for high-resolution plots
- GPU acceleration automatically enabled if available
- JIT compilation provides 5-15x speedup for repeated calls
- Consider caching results for frequently accessed functions

## Rate Limiting

No rate limiting currently implemented for local development. Production deployments should implement appropriate rate limiting based on computational resources.