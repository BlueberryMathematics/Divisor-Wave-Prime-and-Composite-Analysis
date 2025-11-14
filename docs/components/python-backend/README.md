# Python Backend Component Documentation

## Overview
The Python backend provides the core mathematical computation engine for the Divisor Wave Analysis System. It implements infinite product functions, complex function analysis, and provides a RESTful API for frontend integration.

## Core Modules

### Function Registry System
- **Location**: `src/core/function_registry.py`
- **Purpose**: Centralized management of all mathematical functions
- **Features**: 37+ functions, LaTeX integration, automatic synchronization

### Special Functions Library
- **Location**: `src/core/special_functions_library.py` 
- **Purpose**: Core mathematical function implementations
- **Features**: Numba JIT compilation, GPU acceleration, advanced normalization

### LaTeX Integration
- **LaTeX Function Builder**: `src/core/latex_function_builder.py`
- **LaTeX to NumPy Converter**: `src/core/latex_to_numpy_converter.py`
- **Python to LaTeX Converter**: `src/core/python_to_latex_converter.py`

### Visualization Engine
- **Location**: `src/core/plotting_methods.py`
- **Purpose**: 2D/3D complex function visualization
- **Features**: GPU acceleration, multiple colormaps, Base64 encoding

### API Framework
- **Location**: `src/api/main.py`
- **Framework**: FastAPI with automatic documentation
- **Features**: CORS support, comprehensive endpoints, performance optimization

## Installation

### Requirements
```
Python 3.8+
numpy>=2.3.4
scipy>=1.16.3
matplotlib>=3.10.7
sympy>=1.12.0
antlr4-python3-runtime>=4.11.0
fastapi>=0.121.0
numba>=0.56.0 (optional, for JIT acceleration)
cupy-cuda11x>=13.6.0 (optional, for GPU acceleration)
```

### Setup
```bash
# Install system
python install_system.py

# Verify installation  
python verify_installation.py

# Start API server
python src/api/main.py
```

## API Endpoints

### Core Functions
- `GET /functions` - List all available functions
- `POST /evaluate` - Evaluate function at specific points
- `POST /plot` - Generate 2D/3D visualizations
- `POST /custom-functions` - Create custom functions from LaTeX

### LaTeX Integration
- `GET /latex/formula/{name}` - Retrieve LaTeX formulas
- `GET /latex/keyboard` - Symbol palette for frontend
- `POST /latex-to-numpy` - Convert LaTeX to executable functions

## Mathematical Functions

### Function Categories
1. **Core Products** (6 functions)
   - `product_of_sin` - Primary divisor wave function
   - `product_of_product_representation_for_sin` - Double product
   - Composite variants (cos, sin of products)

2. **Riesz Products** (3 functions)  
   - Cosine, sine, tangent variants
   - Harmonic analysis applications

3. **Prime Indicators** (4 functions)
   - Binary Output Prime Indicator Function (BOPIF)
   - Prime detection and alternation series

4. **Special Function Variants** (8 functions)
   - Gamma function implementations
   - Logarithmic and rational variants

5. **Custom Functions** (16+ functions)
   - User-defined via LaTeX notation
   - AI-generated function support

### Normalization Modes
- **X**: Horizontal pattern optimization
- **Y**: Vertical analysis (original research mode)  
- **Z**: Complex magnitude enhancement
- **XYZ**: Multi-axis comprehensive analysis
- **N**: Neutral baseline (default)

## Performance Features

### JIT Compilation (Numba)
- Automatic compilation of critical functions
- 5-15x performance improvement
- CPU-optimized vectorization

### GPU Acceleration (CuPy) 
- CUDA-based acceleration for large datasets
- Automatic CPU fallback for compatibility
- Memory-optimized operations

### Parallel Processing
- Multi-core CPU utilization
- Parallel function evaluation
- Load balancing optimization

## Testing and Validation

### Test Suite
- `src/tests/test_api.py` - API endpoint testing
- `src/tests/test_function_values.py` - Mathematical validation
- `src/tests/benchmark_performance.py` - Performance analysis
- `src/tests/test_latex_system.py` - LaTeX conversion testing

### Continuous Validation
- Automatic function value verification
- Performance regression testing  
- API compatibility validation

## Configuration

### Environment Variables
- `API_HOST`: Server host (default: 0.0.0.0)
- `API_PORT`: Server port (default: 8000)  
- `GPU_ACCELERATION`: Enable GPU features (default: auto)
- `JIT_COMPILATION`: Enable JIT compilation (default: true)

### Database Configuration
- **Registry**: `src/core/function_registry.json`
- **Custom Functions**: `src/core/custom_functions.json`
- **Formulas**: `src/core/divisor_wave_formulas.json`

## Development

### Adding New Functions
1. Define function in `special_functions_library.py`
2. Add to registry via `function_registry.py`
3. Create LaTeX formula entry
4. Add tests and validation

### Custom Function Creation
```python
from core.latex_function_builder import LaTeXFunctionBuilder

builder = LaTeXFunctionBuilder()
result = builder.create_custom_function(
    name="my_function",
    latex_formula=r"\sin(\pi z) \cdot e^{i z}",
    description="Custom trigonometric exponential"
)
```

### API Extension
Add new endpoints in `src/api/main.py` following FastAPI conventions with automatic documentation generation.

## Troubleshooting

### Common Issues
1. **Missing Dependencies**: Run `pip install -r requirements.txt`
2. **GPU Not Available**: System automatically falls back to CPU
3. **LaTeX Parsing Errors**: Verify `antlr4-python3-runtime` installation
4. **Performance Issues**: Enable JIT compilation and GPU acceleration

### Performance Optimization
- Use GPU acceleration for large datasets (>10,000 points)
- Enable JIT compilation for repeated function calls
- Consider parallel processing for multiple function evaluations
- Cache frequently accessed functions

## Research Applications

### Mathematical Analysis
- Prime number theory research
- Complex function analysis  
- Infinite product convergence studies
- Special value computation

### AI Integration
- Automated function discovery
- Mathematical relationship identification
- Formula validation and testing
- Research paper generation support