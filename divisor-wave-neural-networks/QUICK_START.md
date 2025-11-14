# Divisor Wave Neural Networks - Quick Start Guide

## 🚀 Installation

```bash
cd divisor-wave-neural-networks
pip install -r requirements.txt
pip install -e .
```

## 🎯 Quick Examples

### 1. Tetrahedral Neural Network

```python
from divisor_wave_neural_networks import TetrahedralNetwork, TetrahedralConfig

# Create tetrahedral network configuration
config = TetrahedralConfig(
    input_dim=64,
    output_dim=10,
    max_layers=6,
    tetrahedral_scaling=1.0
)

# Build network
network = TetrahedralNetwork(config)

# Use it
x = torch.randn(32, 64)
output = network(x)
print(f"Output shape: {output.shape}")
```

### 2. Crystal Embedding Model

```python
from divisor_wave_neural_networks import CrystalEmbedding, CrystalLatticeType

# Create icosahedral crystal embedding
embedder = CrystalEmbedding.create_icosahedral_embedding(embedding_dim=512)

# Embed sequences
x = torch.randn(16, 100, 512)
embeddings = embedder(x)
```

### 3. Mathematical Discovery

```python
from divisor_wave_neural_networks import DeepDiscoveryNetwork, DiscoveryTaskType

# Create discovery network for infinite products
discovery_net = DeepDiscoveryNetwork.create_infinite_product_discoverer(input_dim=256)

# Discover new formulas
seed_formulas = torch.randn(8, 256)
discoveries = discovery_net.discover_new_formulas(seed_formulas, num_discoveries=5)
```

### 4. THRML Ising Networks

```python
from divisor_wave_neural_networks import IsingNeuralNetwork, IsingNeuralNetworkConfig

# Create Ising network
config = IsingNeuralNetworkConfig(
    lattice_size=(8, 8),
    temperature=1.0,
    use_thrml=True
)

ising_net = IsingNeuralNetwork(config)

# Sample spin configurations
spins = ising_net.sample_configuration(batch_size=16)
```

### 5. Custom Architecture Building

```python
from divisor_wave_neural_networks import ArchitectureBuilder, SequenceType

# Auto-generate architecture from mathematical sequence
builder = ArchitectureBuilder()
arch = builder.auto_generate_architecture(
    input_dim=128,
    output_dim=64,
    sequence_type=SequenceType.TETRAHEDRAL,
    num_layers=5
)

# Build the network
network = builder.build_network(arch)
```

### 6. Integration with Divisor Wave Python

```python
from divisor_wave_neural_networks import DivisorWaveBridge

# Create bridge to mathematical functions
bridge = DivisorWaveBridge()

# Load training data from mathematical formulas
training_data = bridge.generate_training_data(num_samples=1000, sequence_length=100)

# Create PyTorch dataset
dataset = bridge.create_function_dataset()
```

## 🔢 Mathematical Sequences

```python
from divisor_wave_neural_networks import MathematicalSequences, SequenceType

seq_gen = MathematicalSequences()

# Generate different mathematical sequences
tetrahedral = seq_gen.tetrahedral_numbers(10)
fibonacci = seq_gen.fibonacci_sequence(10)
primes = seq_gen.prime_sequence(10)
a287324 = seq_gen.a287324_sequence(10)  # Leo Borcherding's sequence

print(f"Tetrahedral: {tetrahedral}")
print(f"Fibonacci: {fibonacci}")
print(f"Primes: {primes}")
print(f"A287324: {a287324}")
```

## 🏗️ Custom Layers

```python
from divisor_wave_neural_networks import MathematicalLayer, LayerSpec, LayerType, ActivationType

# Create custom mathematical layer
layer_spec = LayerSpec(
    layer_type=LayerType.TETRAHEDRAL,
    input_size=64,
    output_size=32,
    activation=ActivationType.TETRAHEDRAL,
    mathematical_params={"tetrahedral_index": 3}
)

layer = MathematicalLayer(layer_spec)
```

## 📊 Complete Training Example

```python
import torch
import torch.nn as nn
from divisor_wave_neural_networks import *

# 1. Create training data
bridge = DivisorWaveBridge()
train_data = bridge.generate_training_data(num_samples=1000, sequence_length=64)

# 2. Create model
config = DeepDiscoveryConfig(
    input_dim=32,
    output_dim=32,
    use_tetrahedral_architecture=True,
    use_crystal_embeddings=True
)
model = DeepDiscoveryNetwork(config)

# 3. Set up training
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
criterion = nn.MSELoss()

# 4. Training loop
for epoch in range(100):
    optimizer.zero_grad()
    
    # Forward pass
    predictions = model(train_data["input_sequences"])
    loss = criterion(predictions, train_data["target_sequences"])
    
    # Backward pass
    loss.backward()
    optimizer.step()
    
    if epoch % 10 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item():.6f}")
```

## 🧪 Run the Demo

```bash
cd divisor-wave-neural-networks
python examples/comprehensive_demo.py
```

This will demonstrate all the key features of the library!

## 📚 Key Concepts

### Mathematical Sequences
The library uses mathematical sequences like tetrahedral numbers, Fibonacci sequences, and prime numbers to define neural network architectures and training patterns.

### Crystal Embeddings
Based on mathematical lattice structures (cubic, tetrahedral, icosahedral) to create structured semantic representations.

### THRML Integration
Uses JAX-based THRML library for energy-based models and Ising chain neural networks.

### Divisor Wave Integration
Seamlessly integrates with the divisor-wave-python mathematical functions library.

## 🔍 Advanced Usage

For advanced usage patterns, custom architectures, and mathematical discovery workflows, see the full documentation and examples in the `examples/` directory.

## 🤝 Integration with Other Projects

This library is designed to work seamlessly with:
- **divisor-wave-python**: Mathematical functions and computations
- **divisor-wave-agent**: AI agents for mathematical research  
- **divisor-wave-nextjs**: Web interface and visualization
- **divisor-wave-latex**: LaTeX document generation

## 📖 Next Steps

1. Explore the `examples/` directory for more advanced use cases
2. Check out the integration with divisor-wave-agent for AI mathematical discovery
3. Use the web interface (divisor-wave-nextjs) for interactive experimentation
4. Contribute new mathematical sequences or neural network architectures

Happy mathematical discovery! 🌊🧠