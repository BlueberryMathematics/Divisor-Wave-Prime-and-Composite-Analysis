"""
Complete Training Workflow for Divisor Wave Neural Networks
===========================================================

This script demonstrates a full training pipeline using all components
of the divisor-wave-neural-networks library.

Usage:
    python complete_training_workflow.py --config config.yaml
    python complete_training_workflow.py --architecture tetrahedral --sequence fibonacci
"""

import argparse
import logging
import yaml
from pathlib import Path
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Any, Optional, List

# Import all divisor wave neural network components
from src.architectures.tetrahedral_networks import TetrahedralNetwork
from src.architectures.geometric_networks import GeometricNetwork
from src.architectures.oeis_architectures import A287324Network
from src.embeddings.crystal_embeddings import CrystalEmbedding, IcosahedralProjection
from src.thrml_integration.ising_networks import IsingNeuralNetwork
from src.discovery.deep_discovery import DeepMathematicalDiscovery
from src.discovery.reinforcement_discovery import ReinforcementDiscoveryAgent
from src.construction.architecture_builder import ArchitectureBuilder
from src.integration.divisor_wave_bridge import DivisorWaveBridge
from src.utils import (
    MathematicalSequences, SequenceType,
    MathematicalDataLoader, SequenceDataset,
    SequenceLoss, RiemannLoss, PrimeLoss, get_loss_function,
    MathematicalAdam, PrimeScheduler, get_optimizer, get_scheduler
)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CompleteTrainingPipeline:
    """Complete training pipeline for mathematical neural networks."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Using device: {self.device}")
        
        # Initialize components
        self.model = None
        self.optimizer = None
        self.scheduler = None
        self.loss_function = None
        self.data_loader = None
        self.bridge = DivisorWaveBridge()
        
        # Training tracking
        self.train_losses = []
        self.val_losses = []
        self.best_loss = float('inf')
        
    def setup_data(self):
        """Set up data loaders based on configuration."""
        logger.info("Setting up data loaders...")
        
        sequence_type = self.config['data']['sequence_type']
        sequence_length = self.config['data']['sequence_length']
        batch_size = self.config['training']['batch_size']
        
        # Generate mathematical sequences
        seq_generator = MathematicalSequences()
        
        if sequence_type == 'tetrahedral':
            sequences = [seq_generator.tetrahedral_numbers(sequence_length)]
        elif sequence_type == 'fibonacci':
            sequences = [seq_generator.fibonacci_sequence(sequence_length)]
        elif sequence_type == 'prime':
            sequences = [seq_generator.prime_sequence(sequence_length)]
        elif sequence_type == 'A287324':
            sequences = [seq_generator.generate_A287324_sequence(sequence_length)]
        else:
            # Mixed sequences for comprehensive training
            sequences = [
                seq_generator.tetrahedral_numbers(sequence_length),
                seq_generator.fibonacci_sequence(sequence_length),
                seq_generator.prime_sequence(sequence_length)
            ]
        
        # Convert to tensors
        tensor_sequences = [torch.tensor(seq, dtype=torch.float32) for seq in sequences]
        
        # Create dataset and data loader
        dataset = SequenceDataset(tensor_sequences)
        self.data_loader = MathematicalDataLoader(batch_size=batch_size).create_loader(dataset)
        
        logger.info(f"Created dataset with {len(dataset)} sequences")
    
    def setup_model(self):
        """Set up the neural network model based on configuration."""
        logger.info("Setting up model architecture...")
        
        architecture = self.config['model']['architecture']
        input_dim = self.config['model']['input_dim']
        hidden_dim = self.config['model']['hidden_dim']
        output_dim = self.config['model']['output_dim']
        
        if architecture == 'tetrahedral':
            self.model = TetrahedralNetwork(
                input_dim=input_dim,
                hidden_dim=hidden_dim,
                output_dim=output_dim,
                num_layers=self.config['model'].get('num_layers', 3)
            )
        elif architecture == 'geometric':
            self.model = GeometricNetwork(
                input_dim=input_dim,
                hidden_dim=hidden_dim,
                output_dim=output_dim
            )
        elif architecture == 'A287324':
            self.model = A287324Network(
                input_dim=input_dim,
                hidden_dim=hidden_dim,
                output_dim=output_dim
            )
        elif architecture == 'ising':
            self.model = IsingNeuralNetwork(
                lattice_size=self.config['model'].get('lattice_size', 10),
                hidden_dim=hidden_dim
            )
        elif architecture == 'crystal_embedding':
            crystal_embedding = CrystalEmbedding(
                input_dim=input_dim,
                embedding_dim=hidden_dim,
                crystal_type='icosahedral'
            )
            self.model = nn.Sequential(
                crystal_embedding,
                nn.Linear(hidden_dim, output_dim)
            )
        elif architecture == 'custom':
            # Use architecture builder for custom models
            builder = ArchitectureBuilder()
            self.model = builder.build_from_config(self.config['model']['custom_config'])
        else:
            raise ValueError(f"Unknown architecture: {architecture}")
        
        self.model.to(self.device)
        logger.info(f"Created {architecture} model with {sum(p.numel() for p in self.model.parameters())} parameters")
    
    def setup_training_components(self):
        """Set up optimizer, scheduler, and loss function."""
        logger.info("Setting up training components...")
        
        # Optimizer
        optimizer_config = self.config['training']['optimizer']
        self.optimizer = get_optimizer(
            optimizer_config['type'],
            self.model.parameters(),
            lr=optimizer_config['learning_rate'],
            **optimizer_config.get('params', {})
        )
        
        # Scheduler
        if 'scheduler' in self.config['training']:
            scheduler_config = self.config['training']['scheduler']
            self.scheduler = get_scheduler(
                scheduler_config['type'],
                self.optimizer,
                **scheduler_config.get('params', {})
            )
        
        # Loss function
        loss_config = self.config['training']['loss']
        self.loss_function = get_loss_function(
            loss_config['type'],
            **loss_config.get('params', {})
        )
        
        logger.info(f"Set up {optimizer_config['type']} optimizer and {loss_config['type']} loss")
    
    def train_epoch(self) -> float:
        """Train for one epoch."""
        self.model.train()
        total_loss = 0.0
        num_batches = 0
        
        for batch_idx, (data, targets) in enumerate(self.data_loader):
            data, targets = data.to(self.device), targets.to(self.device)
            
            # Forward pass
            self.optimizer.zero_grad()
            outputs = self.model(data)
            loss = self.loss_function(outputs, targets)
            
            # Backward pass
            loss.backward()
            
            # Gradient clipping
            if self.config['training'].get('gradient_clipping', False):
                torch.nn.utils.clip_grad_norm_(
                    self.model.parameters(),
                    self.config['training']['gradient_clip_value']
                )
            
            self.optimizer.step()
            
            total_loss += loss.item()
            num_batches += 1
            
            # Log progress
            if batch_idx % self.config['training'].get('log_interval', 10) == 0:
                logger.info(f"Batch {batch_idx}: Loss = {loss.item():.6f}")
        
        return total_loss / num_batches if num_batches > 0 else 0.0
    
    def validate(self) -> float:
        """Validate the model."""
        self.model.eval()
        total_loss = 0.0
        num_batches = 0
        
        with torch.no_grad():
            for data, targets in self.data_loader:
                data, targets = data.to(self.device), targets.to(self.device)
                outputs = self.model(data)
                loss = self.loss_function(outputs, targets)
                total_loss += loss.item()
                num_batches += 1
        
        return total_loss / num_batches if num_batches > 0 else 0.0
    
    def train(self):
        """Complete training loop."""
        logger.info("Starting training...")
        
        num_epochs = self.config['training']['num_epochs']
        
        for epoch in range(num_epochs):
            # Training
            train_loss = self.train_epoch()
            self.train_losses.append(train_loss)
            
            # Validation
            val_loss = self.validate()
            self.val_losses.append(val_loss)
            
            # Scheduler step
            if self.scheduler is not None:
                self.scheduler.step()
            
            # Save best model
            if val_loss < self.best_loss:
                self.best_loss = val_loss
                self.save_model('best_model.pth')
            
            # Logging
            current_lr = self.optimizer.param_groups[0]['lr']
            logger.info(f"Epoch {epoch+1}/{num_epochs}: "
                       f"Train Loss = {train_loss:.6f}, "
                       f"Val Loss = {val_loss:.6f}, "
                       f"LR = {current_lr:.8f}")
            
            # Early stopping
            if self.config['training'].get('early_stopping', False):
                patience = self.config['training']['early_stopping_patience']
                if len(self.val_losses) > patience:
                    recent_losses = self.val_losses[-patience:]
                    if all(loss >= self.best_loss for loss in recent_losses):
                        logger.info(f"Early stopping at epoch {epoch+1}")
                        break
        
        logger.info("Training completed!")
    
    def save_model(self, filename: str):
        """Save the model."""
        save_path = Path(self.config['training']['save_dir']) / filename
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'config': self.config,
            'train_losses': self.train_losses,
            'val_losses': self.val_losses,
            'best_loss': self.best_loss
        }, save_path)
        
        logger.info(f"Model saved to {save_path}")
    
    def plot_training_curves(self):
        """Plot training and validation curves."""
        plt.figure(figsize=(12, 4))
        
        plt.subplot(1, 2, 1)
        plt.plot(self.train_losses, label='Training Loss')
        plt.plot(self.val_losses, label='Validation Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.title('Training and Validation Loss')
        plt.legend()
        plt.grid(True)
        
        plt.subplot(1, 2, 2)
        plt.semilogy(self.train_losses, label='Training Loss (log)')
        plt.semilogy(self.val_losses, label='Validation Loss (log)')
        plt.xlabel('Epoch')
        plt.ylabel('Loss (log scale)')
        plt.title('Training and Validation Loss (Log Scale)')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        save_path = Path(self.config['training']['save_dir']) / 'training_curves.png'
        plt.savefig(save_path)
        logger.info(f"Training curves saved to {save_path}")
        plt.show()
    
    def demonstrate_bridge_integration(self):
        """Demonstrate integration with divisor-wave-python."""
        logger.info("Demonstrating bridge integration...")
        
        try:
            # Load mathematical functions from divisor-wave-python
            functions = self.bridge.load_mathematical_functions()
            logger.info(f"Loaded {len(functions)} mathematical functions")
            
            # Evaluate a function
            if 'tetrahedral_sum' in functions:
                result = self.bridge.evaluate_function('tetrahedral_sum', [10])
                logger.info(f"tetrahedral_sum(10) = {result}")
            
            # Use model for mathematical discovery
            if hasattr(self.model, 'predict'):
                sample_input = torch.randn(1, self.config['model']['input_dim']).to(self.device)
                prediction = self.model(sample_input)
                logger.info(f"Model prediction for random input: {prediction.cpu().numpy()}")
                
        except Exception as e:
            logger.warning(f"Bridge integration failed: {e}")
    
    def run_complete_workflow(self):
        """Run the complete training workflow."""
        logger.info("="*60)
        logger.info("STARTING COMPLETE DIVISOR WAVE NEURAL NETWORK TRAINING")
        logger.info("="*60)
        
        try:
            # Setup
            self.setup_data()
            self.setup_model()
            self.setup_training_components()
            
            # Training
            self.train()
            
            # Visualization
            self.plot_training_curves()
            
            # Integration demonstration
            self.demonstrate_bridge_integration()
            
            # Final save
            self.save_model('final_model.pth')
            
            logger.info("="*60)
            logger.info("TRAINING WORKFLOW COMPLETED SUCCESSFULLY!")
            logger.info("="*60)
            
        except Exception as e:
            logger.error(f"Training workflow failed: {e}")
            raise


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    if Path(config_path).exists():
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    else:
        # Return default configuration
        return {
            'data': {
                'sequence_type': 'tetrahedral',
                'sequence_length': 100
            },
            'model': {
                'architecture': 'tetrahedral',
                'input_dim': 10,
                'hidden_dim': 64,
                'output_dim': 1,
                'num_layers': 3
            },
            'training': {
                'batch_size': 32,
                'num_epochs': 100,
                'optimizer': {
                    'type': 'mathematical_adam',
                    'learning_rate': 0.001
                },
                'scheduler': {
                    'type': 'fibonacci',
                    'params': {'scale_factor': 0.01}
                },
                'loss': {
                    'type': 'sequence'
                },
                'gradient_clipping': True,
                'gradient_clip_value': 1.0,
                'early_stopping': True,
                'early_stopping_patience': 10,
                'log_interval': 10,
                'save_dir': 'models'
            }
        }


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Complete Divisor Wave Neural Network Training')
    parser.add_argument('--config', type=str, default='config.yaml',
                       help='Path to configuration file')
    parser.add_argument('--architecture', type=str, 
                       choices=['tetrahedral', 'geometric', 'A287324', 'ising', 'crystal_embedding', 'custom'],
                       help='Architecture type (overrides config)')
    parser.add_argument('--sequence', type=str,
                       choices=['tetrahedral', 'fibonacci', 'prime', 'A287324', 'mixed'],
                       help='Sequence type (overrides config)')
    parser.add_argument('--epochs', type=int, help='Number of epochs (overrides config)')
    parser.add_argument('--batch-size', type=int, help='Batch size (overrides config)')
    parser.add_argument('--lr', type=float, help='Learning rate (overrides config)')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Override with command line arguments
    if args.architecture:
        config['model']['architecture'] = args.architecture
    if args.sequence:
        config['data']['sequence_type'] = args.sequence
    if args.epochs:
        config['training']['num_epochs'] = args.epochs
    if args.batch_size:
        config['training']['batch_size'] = args.batch_size
    if args.lr:
        config['training']['optimizer']['learning_rate'] = args.lr
    
    # Create and run training pipeline
    pipeline = CompleteTrainingPipeline(config)
    pipeline.run_complete_workflow()


if __name__ == '__main__':
    main()