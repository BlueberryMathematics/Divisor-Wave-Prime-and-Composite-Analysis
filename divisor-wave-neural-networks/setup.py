from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="divisor-wave-neural-networks",
    version="0.1.0",
    author="Leo J. Borcherding",
    author_email="leo@example.com",
    description="Mathematical Discovery Neural Networks Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/R0b0ticDucky6326/Divisor-Wave-Product-Prime-and-Composite-Analysis",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "cuda11": ["cupy-cuda11x>=12.0.0"],
        "cuda12": ["cupy-cuda12x>=12.0.0"],
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "docs": [
            "sphinx>=7.1.0",
            "sphinx-rtd-theme>=1.3.0",
        ],
        "viz": [
            "manim>=0.17.0",
            "tikzplotlib>=0.10.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "dvnn-discover=divisor_wave_neural_networks.cli.discover:main",
            "dvnn-train=divisor_wave_neural_networks.cli.train:main",
            "dvnn-build=divisor_wave_neural_networks.cli.build:main",
        ],
    },
    keywords=[
        "neural networks",
        "mathematical discovery",
        "infinite products",
        "tetrahedral sequences",
        "prime numbers",
        "divisor waves",
        "deep learning",
        "reinforcement learning",
        "mathematical sequences",
        "THRML",
        "energy-based models",
    ],
    project_urls={
        "Documentation": "https://divisor-wave-neural-networks.readthedocs.io/",
        "Source": "https://github.com/R0b0ticDucky6326/Divisor-Wave-Product-Prime-and-Composite-Analysis",
        "Bug Reports": "https://github.com/R0b0ticDucky6326/Divisor-Wave-Product-Prime-and-Composite-Analysis/issues",
    },
)