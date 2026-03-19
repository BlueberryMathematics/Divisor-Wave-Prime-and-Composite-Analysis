# Divisor Wave Product Prime Complex Analysis

## 🌊 Mathematical Research Platform for Prime Number Theory

[link to the research paper](https://github.com/BlueberryMathematics/Divisor-Wave-Prime-and-Composite-Analysis/blob/main/divisor-wave-latex/paper/Divisor_Waves_and_their_Connection_to_the_Riemann_Hypothesis.pdf)

This repository contains revolutionary research on divisor wave product functions and their connection to prime number patterns through infinite product and infinite sum representations. The platform provides both theoretical foundations and practical computational tools for exploring these mathematical relationships.

## 📊 What is Divisor Wave Product Prime Complex Analysis?

These waveforms breakdown the structure of prime numbers and represent them in a new light. The Divisor Wave Prime Complex Analysis plotting software is an infinite domain which has been defined for researching these special functions. 

Ultimately this software contains infinitely many functions which that have not gotten the opportunity to be explored. Start transversing the complex plane for new discrete product series, and their relationship to primes, chaos, order, and mathematics. Feel free to write a paper about it and reference this software and my paper in your work.

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8+ with virtual environment
- Node.js 18+ 
- Git

### 1. Clone and Setup
```bash
git clone https://github.com/4G3NTR0LLC4G3/Divisor-Wave-Prime-and-Composite-Complex-Analysis.git
cd Divisor-Wave-Prime-and-Composite-Complex-Analysis
```

### 2. Setup Python Backend
```bash
cd divisor-wave-python
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup Next.js Frontend
```bash
cd ../divisor-wave-nextjs
npm install
```

### 4. Start the System

**Terminal 1 - Python Backend (in venv):**
```bash
cd divisor-wave-python/src/api
uvicorn plotting_api:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Next.js Frontend:**
```bash
cd divisor-wave-nextjs
npm run dev
```

### 5. Access the Platform
Open your browser to: **http://localhost:3000**

## ✨ Features

### 🎯 Real-Time Mathematical Visualization
- **Live Python-generated plots**: Direct matplotlib integration with base64 image rendering
- **Interactive parameter controls**: Adjust ranges, resolution, and normalization in real-time
- **Prime/composite analysis**: Visualize how functions behave differently at prime vs composite numbers

### 🔬 Advanced Mathematical Functions
- **Product of Sin a(z)**: `∏(k=2 to ∞) sin(πz/k)` - Shows cusps at primes
- **Double Product b(z)**: Prime indicator function with zeros at composites  
- **Riesz Products**: Normalized demonstrations of infinite product behavior
- **Viète Products**: Classical infinite products for trigonometric functions

### 📈 Multiple Visualization Modes
- **2D Real Plots**: Function behavior along the real axis with prime markers
- **3D Complex Surfaces**: Magnitude visualization over the complex plane
- **Contour Plots**: Both magnitude and phase contours for complex analysis

### 🧮 Research Tools
- **LaTeX-to-NumPy Converter**: Input mathematical formulas and get executable Python code
- **Function Database**: Save and share custom mathematical formulas
- **Prime Pattern Analysis**: Evaluate functions at integer points to study prime/composite patterns

## 📚 Mathematical Theory

### Divisor Wave Function a(z)
The infinite product `∏(k=2 to x) sin(πz/k)` creates:
- **Cusps at primes**: Only one divisor wave zeros
- **Curves at composites**: Multiple divisor waves combine
- **Complex domain**: Reveals zero distribution patterns

### Double Product b(z)  
The function `∏(k=2 to x)[πz ∏(n=2 to x)(1-z²/(n²k²))]` acts as:
- **Prime indicator**: Non-zero at primes
- **Composite detector**: Zeros at composites  
- **Riemann connection**: Links to zeta function zeros

## 🔧 System Architecture

### Backend (Python FastAPI)
- **OptimizedSpecialFunctions**: JIT-compiled mathematical functions using Numba
- **Matplotlib Integration**: High-quality plot generation with customizable styling
- **CORS-enabled API**: RESTful endpoints for function evaluation and plotting

### Frontend (Next.js React)
- **Real-time Visualization**: Canvas-based 3D rendering and API integration
- **Responsive Design**: Modern UI with Tailwind CSS styling
- **State Management**: React hooks for complex mathematical parameter handling

## 📖 Research Paper

For full comprehension of the mathematical foundations, read the research paper:
**`PDF_Files/Divisor_Waves_and_their_Connection_to_the_Riemann_Hypothesis.pdf`**

This paper contains 4 years of research on prime number patterns through complex analysis of infinite products.

## 🎨 Example Visualizations

### 3D Complex Plane Analysis
![Product of Product Representation](graphs/3D_Complex_Graphs/product_of_product_representation_of_sin/prism/Poster_formula_leoborch_special_functions_2.png)

### Prime/Composite Pattern Recognition  
![2D Complex Analysis](graphs/2D_Complex_Graphs/Infinite_Product_of_infinite_product_representation_of_sin/Complex_product_11_n[0-84]_Imaginary_scalar.png)

### Normalized Function Behavior
![Normalized 3D Plot](graphs/3D_Complex_Graphs/product_of_product_representation_of_sin/jet/ComplexPlot_prodprodforsin_15.png)

## 🤝 Contributing

This is an open-source research platform. Contributions are welcome for:
- New mathematical function implementations
- Visualization improvements  
- Performance optimizations
- Documentation enhancements

## 🏆 Previous Work

Want to see my previous work on tetrahedral families from 2017?
- [OEIS A287324](https://oeis.org/A287324)
- [Research Paper PDF](https://oeis.org/A287324/a287324_2.pdf)

## 📧 Contact

**Leo Borcherding** - Mathematical Research & Software Development

---

*"Exploring the infinite domain of prime number patterns through complex analysis and computational mathematics."*
