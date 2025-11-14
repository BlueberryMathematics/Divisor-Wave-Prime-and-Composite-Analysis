#!/usr/bin/env python3
"""
Performance Benchmark for Optimized Divisor Wave API
Tests JIT compilation, GPU acceleration, and multiprocessing improvements

Run this to compare performance between optimized and standard implementations
"""

import time
import sys
import os
import numpy as np
import psutil
from concurrent.futures import ProcessPoolExecutor

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def benchmark_function_evaluation():
    """Benchmark single function evaluations"""
    print("=" * 60)
    print("BENCHMARK 1: Single Function Evaluation")
    print("=" * 60)
    
    try:
        from core.special_functions_library import SpecialFunctionsLibrary
        
        # Test points
        test_points = [
            complex(3.0, 2.0),
            complex(5.0, 1.0), 
            complex(7.0, -1.5),
            complex(10.0, 3.0),
            complex(15.0, -2.0)
        ]
        
        # Initialize libraries
        print("\n1. CPU-only version:")
        lib_cpu = SpecialFunctionsLibrary(use_gpu=False, use_jit=False)
        
        print("\n2. JIT-optimized version:")
        lib_jit = SpecialFunctionsLibrary(use_gpu=False, use_jit=True)
        
        print("\n3. GPU+JIT version (if available):")
        lib_gpu = SpecialFunctionsLibrary(use_gpu=True, use_jit=True)
        
        # Benchmark each version
        libraries = [
            ("CPU-only", lib_cpu),
            ("JIT-optimized", lib_jit), 
            ("GPU+JIT", lib_gpu)
        ]
        
        results = {}
        
        for lib_name, lib in libraries:
            print(f"\n🔥 Testing {lib_name}...")
            
            start_time = time.time()
            for i, z in enumerate(test_points * 20):  # 100 total evaluations
                result = lib.product_of_sin(z, "N")
                if i == 0:
                    sample_result = result
            
            elapsed = time.time() - start_time
            results[lib_name] = {
                'time': elapsed,
                'sample_result': sample_result,
                'rate': len(test_points) * 20 / elapsed
            }
            
            print(f"   Time: {elapsed:.4f}s")
            print(f"   Rate: {results[lib_name]['rate']:.1f} evaluations/sec")
            print(f"   Sample result: {sample_result:.6f}")
        
        # Calculate speedup
        cpu_time = results["CPU-only"]["time"]
        for lib_name in ["JIT-optimized", "GPU+JIT"]:
            if lib_name in results:
                speedup = cpu_time / results[lib_name]["time"]
                print(f"\n🚀 {lib_name} speedup: {speedup:.2f}x")
        
        return results
        
    except Exception as e:
        print(f"❌ Benchmark 1 failed: {e}")
        return {}

def benchmark_mesh_generation():
    """Benchmark mesh generation for plotting"""
    print("\n" + "=" * 60)
    print("BENCHMARK 2: Mesh Generation (Plotting)")
    print("=" * 60)
    
    try:
        from core.plotting_methods import PlottingMethods
        
        # Test different resolutions
        resolutions = [50, 100, 200]
        
        for resolution in resolutions:
            print(f"\n🎯 Testing {resolution}x{resolution} mesh ({resolution**2} points)")
            
            # CPU version
            print("   CPU version:")
            plotter_cpu = PlottingMethods("2D", use_gpu=False, use_jit=False)
            
            start_time = time.time()
            X, Y, Z = plotter_cpu.create_optimized_mesh(
                x_range=(2, 8), 
                y_range=(-2, 2), 
                resolution=resolution
            )
            cpu_time = time.time() - start_time
            print(f"      Time: {cpu_time:.4f}s")
            
            # GPU+JIT version (if available)
            print("   GPU+JIT version:")
            plotter_gpu = PlottingMethods("2D", use_gpu=True, use_jit=True)
            
            start_time = time.time()
            X_gpu, Y_gpu, Z_gpu = plotter_gpu.create_optimized_mesh(
                x_range=(2, 8),
                y_range=(-2, 2),
                resolution=resolution
            )
            gpu_time = time.time() - start_time
            print(f"      Time: {gpu_time:.4f}s")
            
            speedup = cpu_time / gpu_time if gpu_time > 0 else 1.0
            print(f"      Speedup: {speedup:.2f}x")
        
    except Exception as e:
        print(f"❌ Benchmark 2 failed: {e}")

def benchmark_memory_usage():
    """Benchmark memory usage with different backends"""
    print("\n" + "=" * 60)
    print("BENCHMARK 3: Memory Usage")
    print("=" * 60)
    
    process = psutil.Process()
    
    try:
        # Get baseline memory
        baseline_memory = process.memory_info().rss / 1024 / 1024  # MB
        print(f"Baseline memory usage: {baseline_memory:.1f} MB")
        
        # Test CPU version
        print("\n🧠 CPU version memory usage:")
        from core.special_functions_library import SpecialFunctionsLibrary
        lib_cpu = SpecialFunctionsLibrary(use_gpu=False, use_jit=False)
        
        cpu_memory = process.memory_info().rss / 1024 / 1024
        print(f"   After initialization: {cpu_memory:.1f} MB (+{cpu_memory - baseline_memory:.1f} MB)")
        
        # Test large computation
        test_points = [complex(i/10, j/10) for i in range(50) for j in range(50)]
        for z in test_points[:100]:  # Sample
            lib_cpu.product_of_sin(z, "N")
        
        after_computation = process.memory_info().rss / 1024 / 1024
        print(f"   After computation: {after_computation:.1f} MB (+{after_computation - cpu_memory:.1f} MB)")
        
        # Test GPU version memory
        print("\n🚀 GPU+JIT version memory usage:")
        lib_gpu = SpecialFunctionsLibrary(use_gpu=True, use_jit=True)
        
        gpu_memory = process.memory_info().rss / 1024 / 1024
        print(f"   After initialization: {gpu_memory:.1f} MB (+{gpu_memory - after_computation:.1f} MB)")
        
        # Test same computation
        for z in test_points[:100]:
            lib_gpu.product_of_sin(z, "N")
        
        final_memory = process.memory_info().rss / 1024 / 1024
        print(f"   After computation: {final_memory:.1f} MB (+{final_memory - gpu_memory:.1f} MB)")
        
    except Exception as e:
        print(f"❌ Benchmark 3 failed: {e}")

def benchmark_parallel_processing():
    """Benchmark parallel processing capabilities"""
    print("\n" + "=" * 60)
    print("BENCHMARK 4: Parallel Processing")
    print("=" * 60)
    
    try:
        from core.special_functions_library import SpecialFunctionsLibrary
        
        # Generate test data
        n_points = 1000
        test_points = [complex(i/100, j/100) for i in range(int(np.sqrt(n_points))) 
                      for j in range(int(np.sqrt(n_points)))][:n_points]
        
        print(f"Testing with {len(test_points)} function evaluations...")
        
        lib = SpecialFunctionsLibrary(use_gpu=True, use_jit=True)
        func = lib.get_function("product_of_sin")
        
        # Sequential processing
        print("\n📝 Sequential processing:")
        start_time = time.time()
        results_seq = [func(z, "N") for z in test_points]
        seq_time = time.time() - start_time
        print(f"   Time: {seq_time:.4f}s")
        print(f"   Rate: {len(test_points)/seq_time:.1f} evaluations/sec")
        
        # Parallel processing
        print("\n⚡ Parallel processing:")
        start_time = time.time()
        results_par = lib.parallel_evaluate_function(func, test_points, "N")
        par_time = time.time() - start_time
        print(f"   Time: {par_time:.4f}s")
        print(f"   Rate: {len(test_points)/par_time:.1f} evaluations/sec")
        
        speedup = seq_time / par_time if par_time > 0 else 1.0
        print(f"\n🚀 Parallel speedup: {speedup:.2f}x")
        
        # Verify results are consistent
        diff = np.mean([abs(a - b) for a, b in zip(results_seq[:10], results_par[:10])])
        print(f"✓ Result consistency: avg diff = {diff:.2e}")
        
    except Exception as e:
        print(f"❌ Benchmark 4 failed: {e}")

def system_info():
    """Display system information"""
    print("=" * 60)
    print("SYSTEM INFORMATION")
    print("=" * 60)
    
    import platform
    
    print(f"Platform: {platform.platform()}")
    print(f"Python: {platform.python_version()}")
    print(f"CPU cores: {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count(logical=True)} logical")
    
    memory = psutil.virtual_memory()
    print(f"RAM: {memory.total / 1024**3:.1f} GB total, {memory.available / 1024**3:.1f} GB available")
    
    # Check for optimization libraries
    optimizations = []
    
    try:
        import numba
        optimizations.append(f"Numba {numba.__version__}")
    except ImportError:
        optimizations.append("Numba: NOT AVAILABLE")
    
    try:
        import cupy
        optimizations.append(f"CuPy {cupy.__version__}")
    except ImportError:
        optimizations.append("CuPy: NOT AVAILABLE")
    
    print(f"Optimizations: {', '.join(optimizations)}")

def main():
    """Run complete performance benchmark suite"""
    print("🚀 DIVISOR WAVE API PERFORMANCE BENCHMARK")
    print("Enhanced with JIT, GPU acceleration, and multiprocessing")
    print()
    
    system_info()
    
    # Run benchmarks
    function_results = benchmark_function_evaluation()
    benchmark_mesh_generation()
    benchmark_memory_usage()
    benchmark_parallel_processing()
    
    # Summary
    print("\n" + "=" * 60)
    print("BENCHMARK SUMMARY")
    print("=" * 60)
    
    if function_results:
        cpu_time = function_results.get("CPU-only", {}).get("time", 1.0)
        jit_time = function_results.get("JIT-optimized", {}).get("time", cpu_time)
        gpu_time = function_results.get("GPU+JIT", {}).get("time", cpu_time)
        
        print(f"Function evaluation speedups:")
        print(f"  JIT compilation: {cpu_time/jit_time:.2f}x faster")
        print(f"  GPU+JIT: {cpu_time/gpu_time:.2f}x faster")
    
    print("\n✅ Benchmark complete!")
    print("\nTo install optimization libraries:")
    print("pip install numba cupy-cuda11x  # Adjust CUDA version as needed")

if __name__ == "__main__":
    main()