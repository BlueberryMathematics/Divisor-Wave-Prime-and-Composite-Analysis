#!/usr/bin/env python3
"""
Divisor Wave Neural Networks - Comprehensive Example
====================================================

This example demonstrates the key features of the divisor wave neural networks library:

1. Tetrahedral Network Architecture
2. Crystal Embedding Models
3. Mathematical Discovery Networks
4. THRML Ising Networks
5. Integration with divisor-wave-python
6. Custom Architecture Building

Run this script to see the library in action!
"""

import torch
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import our library components
from divisor_wave_neural_networks import (
    # Architectures
    TetrahedralNetwork,
    TetrahedralConfig,
    
    # Embeddings
    CrystalEmbedding,
    CrystalEmbeddingConfig,
    CrystalLatticeType,
    
    # Discovery
    DeepDiscoveryNetwork,
    DeepDiscoveryConfig,
    DiscoveryTaskType,
    
    # THRML Integration
    IsingNeuralNetwork,
    IsingNeuralNetworkConfig,
    
    # Construction
    ArchitectureBuilder,
    LayerType,
    ActivationType,
    
    # Utils
    MathematicalSequences,
    SequenceType,
    
    # Integration
    DivisorWaveBridge,
)


def demonstrate_tetrahedral_networks():
    """Demonstrate tetrahedral neural network architectures."""
    print("🔺 TETRAHEDRAL NEURAL NETWORKS")
    print("=" * 50)
    
    # Create a tetrahedral network configuration
    config = TetrahedralConfig(
        input_dim=64,
        output_dim=10,
        max_layers=6,
        tetrahedral_scaling=1.0,
        activation="relu",
        use_batch_norm=True
    )
    
    # Build the network
    tet_network = TetrahedralNetwork(config)
    print(f"✅ Created tetrahedral network with {sum(p.numel() for p in tet_network.parameters())} parameters")
    
    # Test forward pass
    batch_size = 32
    x = torch.randn(batch_size, 64)
    output = tet_network(x)
    print(f"✅ Forward pass successful: {x.shape} → {output.shape}")
    
    # Get network info
    info = tet_network.get_layer_info()
    print(f"✅ Network layers: {info['layer_sizes']}")
    print(f"✅ Tetrahedral numbers: {info['tetrahedral_numbers']}")
    
    return tet_network


def demonstrate_crystal_embeddings():
    """Demonstrate crystal embedding models."""
    print("\n💎 CRYSTAL EMBEDDING MODELS")
    print("=" * 50)
    
    # Create icosahedral crystal embedding
    config = CrystalEmbeddingConfig(
        embedding_dim=512,
        lattice_type=CrystalLatticeType.ICOSAHEDRAL,
        num_heads=20,  # Match icosahedral faces
        num_layers=6
    )
    
    crystal_embedder = CrystalEmbedding(config)
    print(f"✅ Created icosahedral crystal embedding with {sum(p.numel() for p in crystal_embedder.parameters())} parameters")
    
    # Test embedding
    batch_size = 16
    seq_length = 100
    x = torch.randn(batch_size, seq_length, 512)
    embeddings = crystal_embedder(x)
    print(f"✅ Crystal embedding successful: {x.shape} → {embeddings.shape}")
    
    # Get crystal structure info
    structure_info = crystal_embedder.get_crystal_structure_info()
    print(f"✅ Lattice type: {structure_info['lattice_type']}")
    print(f"✅ Lattice constants: {structure_info['lattice_constants'][:3]}...")
    
    return crystal_embedder


def demonstrate_mathematical_sequences():
    """Demonstrate mathematical sequence generation."""
    print("\n🔢 MATHEMATICAL SEQUENCES")
    print("=" * 50)
    
    seq_gen = MathematicalSequences()
    
    # Generate different types of sequences
    sequences = {
        "Tetrahedral": seq_gen.tetrahedral_numbers(10),
        "Triangular": seq_gen.triangular_numbers(10),
        "Fibonacci": seq_gen.fibonacci_sequence(10),
        "A287324": seq_gen.a287324_sequence(10),
        "Prime": seq_gen.prime_sequence(10)
    }
    
    for name, sequence in sequences.items():
        print(f"✅ {name}: {sequence.tolist()[:5]}...")
    
    # Generate architecture sequence
    arch_sizes = seq_gen.generate_architecture_sequence(
        SequenceType.TETRAHEDRAL, max_layers=5, scale_factor=0.5
    )
    print(f"✅ Architecture sizes: {arch_sizes}")
    
    return sequences


def demonstrate_discovery_networks():
    """Demonstrate mathematical discovery networks."""
    print("\n🔬 MATHEMATICAL DISCOVERY NETWORKS")
    print("=" * 50)
    
    # Create infinite product discovery network
    config = DeepDiscoveryConfig(
        input_dim=256,
        hidden_dim=512,
        discovery_task=DiscoveryTaskType.INFINITE_PRODUCT,
        use_tetrahedral_architecture=True,
        use_crystal_embeddings=True
    )
    
    discovery_net = DeepDiscoveryNetwork(config)
    print(f"✅ Created discovery network with {sum(p.numel() for p in discovery_net.parameters())} parameters")
    
    # Test discovery
    batch_size = 8
    seed_formulas = torch.randn(batch_size, 256)
    
    # Discover new formulas
    discoveries = discovery_net.discover_new_formulas(
        seed_formulas, num_discoveries=3, diversity_threshold=0.7
    )
    print(f"✅ Discovered {len(discoveries)} new mathematical formulas")
    
    for i, discovery in enumerate(discoveries):
        validity = torch.mean(discovery["validity"]).item()
        print(f"   Formula {i+1}: Validity = {validity:.3f}")
    
    return discovery_net


def demonstrate_ising_networks():
    """Demonstrate THRML Ising neural networks."""
    print("\n🧲 ISING NEURAL NETWORKS (THRML)")
    print("=" * 50)
    
    # Create Ising network configuration
    config = IsingNeuralNetworkConfig(
        lattice_size=(8, 8),
        temperature=1.0,
        coupling_strength=1.5,
        num_layers=4,
        use_thrml=True
    )
    
    ising_net = IsingNeuralNetwork(config)
    print(f"✅ Created Ising network with {sum(p.numel() for p in ising_net.parameters())} parameters")
    
    # Test forward pass
    batch_size = 16
    x = torch.randn(batch_size, 64)  # Will be projected to lattice size
    output = ising_net(x)
    print(f"✅ Ising network forward pass: {x.shape} → {output.shape}")
    
    # Sample spin configuration
    spin_config = ising_net.sample_configuration(batch_size=4)
    print(f"✅ Sampled spin configurations: {spin_config.shape}")
    
    # Get energy statistics
    energy_stats = ising_net.get_energy_statistics()
    print(f"✅ Energy statistics: mean = {energy_stats['mean_energy']:.3f}")
    
    return ising_net


def demonstrate_architecture_builder():
    """Demonstrate custom architecture building."""
    print("\n🏗️ CUSTOM ARCHITECTURE BUILDER")
    print("=" * 50)
    
    builder = ArchitectureBuilder()
    
    # Create custom architecture
    arch = builder.create_architecture(
        "custom_mathematical_network",
        "Custom network with mathematical layers"
    )
    arch.input_dim = 128
    arch.output_dim = 64
    
    # Add different types of layers
    builder.add_layer(arch.name, "tetrahedral")
    builder.add_layer(arch.name, "fibonacci") 
    builder.add_layer(arch.name, "prime")
    builder.add_layer(arch.name, "fractal")
    
    print(f"✅ Created custom architecture with {len(arch.layers)} layers")
    
    # Build the actual network
    custom_network = builder.build_network(arch)
    print(f"✅ Built network with {sum(p.numel() for p in custom_network.parameters())} parameters")
    
    # Test the custom network
    x = torch.randn(8, 128)
    output = custom_network(x)
    print(f"✅ Custom network forward pass: {x.shape} → {output.shape}")
    
    # Get architecture info
    info = custom_network.get_architecture_info()
    print(f"✅ Architecture: {info['name']} - {info['num_layers']} layers")
    
    return custom_network


def demonstrate_divisor_wave_integration():
    """Demonstrate integration with divisor-wave-python."""
    print("\n🌊 DIVISOR WAVE INTEGRATION")
    print("=" * 50)
    
    # Create bridge to divisor-wave-python
    bridge = DivisorWaveBridge()
    
    # Validate connection
    status = bridge.validate_connection()
    print(f"✅ Bridge available: {status['available']}")
    print(f"✅ Data path exists: {status['data_path_exists']}")
    
    if status['available']:
        # Load mathematical formulas
        formulas = bridge.load_mathematical_formulas()
        print(f"✅ Loaded {len(formulas)} formula categories")
        
        # Generate training data
        training_data = bridge.generate_training_data(num_samples=100, sequence_length=50)
        print(f"✅ Generated training data: {training_data['input_sequences'].shape}")
        
        # Get mathematical constants
        constants = bridge.get_mathematical_constants()
        print(f"✅ Mathematical constants: π = {constants['pi']:.6f}, φ = {constants['golden_ratio']:.6f}")
    else:
        print("⚠️ divisor-wave-python not available, using mock data")
        # Still demonstrate with mock data
        training_data = bridge.generate_training_data(num_samples=100, sequence_length=50)
        print(f"✅ Generated mock training data: {training_data['input_sequences'].shape}")
    
    return bridge


def create_comprehensive_example():
    """Create a comprehensive example combining multiple components."""
    print("\n🚀 COMPREHENSIVE EXAMPLE")
    print("=" * 50)
    
    # 1. Create mathematical training data
    bridge = DivisorWaveBridge()
    training_data = bridge.generate_training_data(num_samples=200, sequence_length=64)
    
    # 2. Create a hybrid architecture
    config = DeepDiscoveryConfig(
        input_dim=32,  # Half of sequence length for prediction task
        hidden_dim=256,
        output_dim=32,  # Predict remaining half
        discovery_task=DiscoveryTaskType.SEQUENCE_GENERATION,
        use_tetrahedral_architecture=True,
        use_crystal_embeddings=True
    )
    
    model = DeepDiscoveryNetwork(config)
    print(f"✅ Created hybrid model with {sum(p.numel() for p in model.parameters())} parameters")
    
    # 3. Test with real data
    input_data = training_data["input_sequences"]
    target_data = training_data["target_sequences"]
    
    # Forward pass
    with torch.no_grad():
        predictions = model(input_data)
    
    print(f"✅ Model prediction: {input_data.shape} → {predictions.shape}")
    
    # 4. Calculate simple loss
    if predictions.shape == target_data.shape:
        loss = torch.nn.functional.mse_loss(predictions, target_data)
        print(f"✅ MSE Loss: {loss.item():.6f}")
    
    return model, training_data


def visualize_results(sequences, save_plots=False):
    """Create visualizations of the results."""
    print("\n📊 VISUALIZATION")
    print("=" * 50)
    
    try:
        import matplotlib.pyplot as plt
        
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle("Divisor Wave Neural Networks - Mathematical Sequences", fontsize=16)
        
        sequence_names = list(sequences.keys())[:6]  # First 6 sequences
        
        for i, name in enumerate(sequence_names):
            row, col = i // 3, i % 3
            sequence = sequences[name][:20]  # First 20 terms
            
            axes[row, col].plot(sequence.numpy(), 'o-', linewidth=2, markersize=6)
            axes[row, col].set_title(f"{name} Sequence", fontsize=12)
            axes[row, col].grid(True, alpha=0.3)
            axes[row, col].set_xlabel("Term Index")
            axes[row, col].set_ylabel("Value")
        
        plt.tight_layout()
        
        if save_plots:
            plt.savefig("divisor_wave_neural_networks_demo.png", dpi=300, bbox_inches='tight')
            print("✅ Saved visualization to 'divisor_wave_neural_networks_demo.png'")
        else:
            plt.show()
        
        print("✅ Created sequence visualizations")
        
    except ImportError:
        print("⚠️ Matplotlib not available for visualization")
    except Exception as e:
        print(f"⚠️ Visualization error: {e}")


def main():
    """Main demonstration function."""
    print("🌊 DIVISOR WAVE NEURAL NETWORKS - COMPREHENSIVE DEMO")
    print("=" * 60)
    print("Based on Leo J. Borcherding's mathematical research")
    print("=" * 60)
    
    try:
        # Set random seeds for reproducibility
        torch.manual_seed(42)
        np.random.seed(42)
        
        # Demonstrate each component
        tet_network = demonstrate_tetrahedral_networks()
        crystal_embedder = demonstrate_crystal_embeddings()
        sequences = demonstrate_mathematical_sequences()
        discovery_net = demonstrate_discovery_networks()
        ising_net = demonstrate_ising_networks()
        custom_net = demonstrate_architecture_builder()
        bridge = demonstrate_divisor_wave_integration()
        
        # Comprehensive example
        model, training_data = create_comprehensive_example()
        
        # Visualizations
        visualize_results(sequences, save_plots=True)
        
        print("\n🎉 DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("Key Features Demonstrated:")
        print("✅ Tetrahedral neural network architectures")
        print("✅ Crystal embedding models with icosahedral structure")
        print("✅ Mathematical sequence generation (tetrahedral, Fibonacci, primes)")
        print("✅ Deep learning networks for mathematical discovery")
        print("✅ THRML Ising model integration")
        print("✅ Custom architecture building system")
        print("✅ Integration with divisor-wave-python")
        print("✅ Comprehensive training pipeline")
        
        print("\n📚 Next Steps:")
        print("- Train models on your mathematical data")
        print("- Experiment with different sequence types")
        print("- Use THRML for energy-based discovery")
        print("- Build custom architectures for specific problems")
        print("- Integrate with the divisor-wave-agent for AI discovery")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()