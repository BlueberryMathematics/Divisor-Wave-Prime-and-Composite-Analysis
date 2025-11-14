#!/usr/bin/env python3
"""
Installation Verification Script
Verifies all dependencies are properly installed for LaTeX <-> NumPy conversion system
"""

def check_dependencies():
    """Check all required dependencies for the system"""
    print("Checking system dependencies...")
    print("=" * 50)
    
    dependencies = [
        ("numpy", "Core numerical computing"),
        ("scipy", "Scientific computing"),
        ("matplotlib", "Plotting and visualization"),
        ("sympy", "Symbolic mathematics for LaTeX"),
        ("antlr4", "LaTeX parser backend"),
        ("fastapi", "Web API framework"),
        ("numba", "JIT compilation for performance"),
        ("cupy", "GPU acceleration (optional)")
    ]
    
    missing = []
    installed = []
    
    for package, description in dependencies:
        try:
            if package == "antlr4":
                import antlr4
            elif package == "cupy":
                import cupy
            else:
                __import__(package)
            installed.append((package, description))
            print(f"✓ {package:<12} - {description}")
        except ImportError:
            missing.append((package, description))
            print(f"✗ {package:<12} - {description} (MISSING)")
    
    print("\n" + "=" * 50)
    print(f"INSTALLED: {len(installed)}/{len(dependencies)} dependencies")
    
    if missing:
        print(f"\nMISSING PACKAGES ({len(missing)}):")
        for package, desc in missing:
            print(f"  - {package}: {desc}")
        
        print(f"\nTo install missing packages:")
        print(f"pip install -r requirements.txt")
        
        if any(pkg == "cupy" for pkg, _ in missing):
            print("\nNote: CuPy is optional for GPU acceleration")
            print("System will work fine with CPU-only processing")
    else:
        print("\n🎉 ALL DEPENDENCIES INSTALLED!")
        print("System is ready for full LaTeX <-> NumPy conversion")
    
    return len(missing) == 0

def test_latex_conversion():
    """Test LaTeX conversion capabilities"""
    print("\nTesting LaTeX conversion capabilities...")
    print("=" * 50)
    
    try:
        import sympy as sp
        from sympy.parsing.latex import parse_latex
        
        # Test basic LaTeX parsing
        test_latex = r"\sin(\pi x)"
        parsed = parse_latex(test_latex)
        print(f"✓ Basic LaTeX parsing: {test_latex} -> {parsed}")
        
        # Test function generation
        x = sp.Symbol('x')
        func = sp.lambdify(x, parsed, 'numpy')
        import numpy as np
        test_result = func(np.pi/2)
        print(f"✓ Function execution: sin(π·π/2) = {test_result:.6f}")
        
        print("✓ LaTeX -> NumPy conversion: WORKING")
        return True
        
    except ImportError as e:
        print(f"✗ Missing dependency for LaTeX parsing: {e}")
        return False
    except Exception as e:
        print(f"✗ LaTeX conversion test failed: {e}")
        return False

def test_system_integration():
    """Test system integration"""
    print("\nTesting system integration...")
    print("=" * 50)
    
    try:
        import sys
        import os
        sys.path.append('src')
        
        from core.function_registry import get_registry
        registry = get_registry()
        print(f"✓ Registry loaded: {len(registry.functions)} functions")
        
        from core.special_functions_library import SpecialFunctionsLibrary
        special_funcs = SpecialFunctionsLibrary()
        print(f"✓ Special functions: {len(special_funcs.get_available_functions())} builtin")
        
        from core.latex_function_builder import LaTeXFunctionBuilder
        builder = LaTeXFunctionBuilder()
        print("✓ LaTeX function builder: Ready")
        
        print("✓ System integration: ALL COMPONENTS LOADED")
        return True
        
    except Exception as e:
        print(f"✗ System integration failed: {e}")
        return False

def main():
    """Main verification routine"""
    print("DIVISOR WAVE SYSTEM VERIFICATION")
    print("=" * 60)
    
    deps_ok = check_dependencies()
    latex_ok = test_latex_conversion() if deps_ok else False
    system_ok = test_system_integration()
    
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    print(f"Dependencies: {'✓ PASS' if deps_ok else '✗ FAIL'}")
    print(f"LaTeX System: {'✓ PASS' if latex_ok else '✗ FAIL'}")
    print(f"Integration:  {'✓ PASS' if system_ok else '✗ FAIL'}")
    
    if deps_ok and latex_ok and system_ok:
        print("\n🎉 SYSTEM FULLY OPERATIONAL!")
        print("Ready for:")
        print("  - AI mathematical discovery")
        print("  - LaTeX <-> NumPy conversion")
        print("  - Custom function creation")
        print("  - Automated mathematical analysis")
    else:
        print("\n⚠️  SYSTEM NEEDS ATTENTION")
        if not deps_ok:
            print("  - Install missing dependencies")
        if not latex_ok:
            print("  - Fix LaTeX conversion system")
        if not system_ok:
            print("  - Check system integration")
    
    print("=" * 60)

if __name__ == "__main__":
    main()