# Divisor Wave Neural Networks

## 🧠 Mathematical Discovery Neural Networks Library

A comprehensive PyTorch-based neural networks library for mathematical discovery, sequence prediction, and custom architectures inspired by Leo J. Borcherding's research on divisor waves, infinite products, and tetrahedral sequences.

## 🎯 Core Capabilities

### 1. **Mathematical Discovery Networks**
- **Deep Learning Discovery**: Neural networks that discover new infinite products and sums
- **Reinforcement Learning**: RL agents that explore mathematical spaces to find novel formulas
- **Pole & Zero Detection**: Networks trained to identify poles and zeros in complex functions
- **Prime Pattern Learning**: Models that learn from prime sequences and mathematical structures

### 2. **Function Prediction Models** 
- **Sequence Prediction**: PyTorch models trained on specific sequences like b(z)
- **Complex Function Approximation**: Neural networks that predict outputs of mathematical functions
- **Series Continuation**: Models that extend mathematical series beyond known terms

### 3. **Sequence-Architected Networks**
- **Tetrahedral Networks**: Neural architectures based on tetrahedral number sequences
- **Geometric Series Networks**: Networks structured using geometric progressions
- **OEIS-Based Architectures**: Custom architectures derived from OEIS sequences like A287324

### 4. **Embedding Models**
- **Crystal Embedding Models**: Hyperdimensional embedding using mathematical lattices
- **Tetrahedral Embeddings**: Embedding spaces structured by tetrahedral numbers
- **Mathematical Sequence Embeddings**: Custom embeddings based on number-theoretic sequences

### 5. **THRML Integration**
- **Ising Chain Networks**: Neural networks using THRML Ising model compute blocks
- **Energy-Based Models**: EBMs with JAX/THRML backend for efficient sampling
- **Probabilistic Graphical Models**: PGMs for mathematical structure discovery

### 6. **Model Construction System**
- **Custom Architecture Builder**: Tool for creating novel neural network architectures
- **Mathematical Layer Library**: Specialized layers based on mathematical operations
- **Training Pipeline System**: Automated training pipelines for different model types

## 📁 Project Structure

```
divisor-wave-neural-networks/
├── README.md
├── requirements.txt
├── setup.py
├── examples/                           # Example usage and demos
├── docs/                              # Documentation
├── src/
│   ├── __init__.py
│   ├── discovery/                     # Mathematical discovery networks
│   │   ├── __init__.py
│   │   ├── deep_discovery.py          # Deep learning for formula discovery
│   │   ├── reinforcement_discovery.py # RL-based mathematical exploration
│   │   └── pole_zero_detection.py     # Networks for pole/zero identification
│   ├── prediction/                    # Function prediction models
│   │   ├── __init__.py
│   │   ├── sequence_prediction.py     # Sequence continuation models
│   │   └── function_approximation.py  # Complex function approximators
│   ├── architectures/                 # Sequence-based architectures
│   │   ├── __init__.py
│   │   ├── tetrahedral_networks.py    # Tetrahedral-based architectures
│   │   ├── geometric_networks.py      # Geometric series architectures
│   │   └── oeis_architectures.py      # OEIS sequence-based networks
│   ├── embeddings/                    # Custom embedding models
│   │   ├── __init__.py
│   │   ├── crystal_embeddings.py      # Crystal lattice embeddings
│   │   ├── tetrahedral_embeddings.py  # Tetrahedral space embeddings
│   │   └── sequence_embeddings.py     # Mathematical sequence embeddings
│   ├── thrml_integration/             # THRML/JAX integration
│   │   ├── __init__.py
│   │   ├── ising_networks.py          # Ising model neural networks
│   │   ├── energy_models.py           # Energy-based models
│   │   └── pgm_discovery.py           # PGM-based discovery
│   ├── construction/                  # Model construction system
│   │   ├── __init__.py
│   │   ├── architecture_builder.py    # Custom architecture builder
│   │   ├── mathematical_layers.py     # Mathematical operation layers
│   │   └── training_pipelines.py      # Automated training systems
│   ├── utils/                         # Utilities and helpers
│   │   ├── __init__.py
│   │   ├── mathematical_sequences.py  # Sequence generators
│   │   ├── data_loaders.py            # Data loading utilities
│   │   └── visualization.py           # Visualization tools
│   └── integration/                   # Integration with other projects
│       ├── __init__.py
│       ├── divisor_wave_bridge.py     # Bridge to divisor-wave-python
│       ├── agent_integration.py       # Integration with divisor-wave-agent
│       └── web_interface.py           # Web interface integration
└── tests/                             # Test suite
    ├── __init__.py
    ├── test_discovery.py
    ├── test_prediction.py
    ├── test_architectures.py
    ├── test_embeddings.py
    ├── test_thrml.py
    └── test_construction.py
```

## 🚀 Key Features

### Mathematical Discovery
- **Formula Discovery Networks**: Deep networks that generate new infinite products and sums
- **Pattern Recognition**: RL agents that identify mathematical patterns in sequences
- **Structure Learning**: Networks that learn the underlying structure of mathematical objects

### Sequence-Based Architectures
- **Tetrahedral Networks**: Architectures where layer sizes follow tetrahedral numbers
- **Fibonacci Networks**: Layers structured using Fibonacci sequences
- **Prime-Based Networks**: Architectures using prime number distributions

### Advanced Embeddings
- **Crystal Lattice Embeddings**: Multi-dimensional embeddings using mathematical lattices
- **Hyperdimensional Embeddings**: High-dimensional representations of mathematical concepts
- **Geometric Embeddings**: Embeddings based on geometric progressions and series

### Energy-Based Models
- **THRML Integration**: JAX-based energy models for mathematical sampling
- **Ising Chain Networks**: Neural networks with Ising model compute blocks
- **Probabilistic Discovery**: PGMs for discovering mathematical relationships

## 📖 Integration with Divisor Wave Project

This library integrates seamlessly with:
- **divisor-wave-python**: Mathematical functions and computational backend
- **divisor-wave-agent**: AI agents for mathematical research
- **divisor-wave-nextjs**: Web interface for visualization and interaction

## 🔬 Research Applications

Based on Leo J. Borcherding's research:
- Divisor wave product analysis
- Prime and composite number relationships
- Infinite product representations
- Tetrahedral sequence families
- Mathematical structure discovery

## 🛠️ Installation

```bash
cd divisor-wave-neural-networks
pip install -r requirements.txt
pip install -e .
```

## 📚 Quick Start

```python
from divisor_wave_neural_networks import (
    TetrahedralNetwork,
    CrystalEmbedding,
    FormulaDiscoveryAgent,
    IsingNeuralNetwork
)

# Create a tetrahedral-architected network
net = TetrahedralNetwork(input_dim=64, max_layers=10)

# Train a formula discovery model
discovery_agent = FormulaDiscoveryAgent()
discovery_agent.train_on_sequences(prime_sequences, formula_database)

# Use crystal embeddings
embedder = CrystalEmbedding(lattice_type='icosahedral', dim=512)
mathematical_embeddings = embedder.embed(mathematical_concepts)
```

## 🎓 Academic References

This work builds upon:
- "Divisor Waves and their Connection to the Riemann Hypothesis" - Leo J. Borcherding
- "The Unified Tetrahedral Family Defined by Pascal's Triangle" - Leo J. Borcherding
- "Unified Hyperdimensional Crystal Embedding Model" - Leo J. Borcherding
- OEIS sequence A287324 and the tetrahedral family

---

*"Neural networks architected by mathematical sequences for the discovery of new mathematical structures."*