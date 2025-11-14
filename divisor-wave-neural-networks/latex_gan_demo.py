"""
LaTeX Expression GAN Demonstration
==================================

Demonstration of training and using the LaTeX Expression GAN to generate
new mathematical expressions from divisor-wave project data.

This script shows how to:
1. Load LaTeX expressions from JSON files
2. Train the GAN on mathematical LaTeX patterns  
3. Generate new mathematical expressions
4. Validate and analyze generated expressions
"""

import sys
import os
from pathlib import Path
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import matplotlib.pyplot as plt
import json
from typing import List, Dict, Any

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.architectures.latex_expression_gan import (
    LaTeXGAN, LaTeXGANConfig, LaTeXTokenizer, LaTeXDataLoader,
    create_latex_gan_from_projects
)


class LaTeXDataset(Dataset):
    """Dataset for LaTeX expressions."""
    
    def __init__(self, latex_expressions: List[str], tokenizer: LaTeXTokenizer, max_length: int = 256):
        self.expressions = latex_expressions
        self.tokenizer = tokenizer
        self.max_length = max_length
        
        # Pre-encode all expressions
        self.encoded_expressions = []
        for expr in latex_expressions:
            encoded = tokenizer.encode(expr, max_length=max_length)
            self.encoded_expressions.append(encoded)
    
    def __len__(self):
        return len(self.encoded_expressions)
    
    def __getitem__(self, idx):
        return torch.tensor(self.encoded_expressions[idx], dtype=torch.long)


def demonstrate_latex_loading():
    """Demonstrate loading LaTeX expressions from divisor-wave projects."""
    print("=" * 60)
    print("LATEX EXPRESSION LOADING DEMONSTRATION")
    print("=" * 60)
    
    # Load LaTeX expressions
    projects_root = "."
    data_loader = LaTeXDataLoader(projects_root)
    latex_expressions = data_loader.load_from_divisor_wave_projects()
    
    print(f"Loaded {len(latex_expressions)} LaTeX expressions")
    
    if latex_expressions:
        print("\nSample LaTeX expressions:")
        for i, expr in enumerate(latex_expressions[:5], 1):
            print(f"{i}. {expr}")
    else:
        print("No LaTeX expressions found in JSON files.")
        print("Using default mathematical templates...")
        latex_expressions = data_loader._load_custom_mathematical_expressions()
        
        print("\nDefault mathematical templates:")
        for i, expr in enumerate(latex_expressions[:5], 1):
            print(f"{i}. {expr}")
    
    return latex_expressions


def demonstrate_tokenization(latex_expressions: List[str]):
    """Demonstrate LaTeX tokenization."""
    print("\n" + "=" * 60)
    print("LATEX TOKENIZATION DEMONSTRATION")
    print("=" * 60)
    
    # Create tokenizer and build vocabulary
    tokenizer = LaTeXTokenizer()
    tokenizer.build_vocabulary(latex_expressions)
    
    print(f"Built vocabulary with {tokenizer.vocab_size} tokens")
    
    # Show tokenization examples
    if latex_expressions:
        sample_expr = latex_expressions[0]
        print(f"\nSample expression: {sample_expr}")
        
        tokens = tokenizer.tokenize_latex(sample_expr)
        print(f"Tokens: {tokens}")
        
        encoded = tokenizer.encode(sample_expr)
        print(f"Encoded: {encoded[:20]}..." if len(encoded) > 20 else f"Encoded: {encoded}")
        
        decoded = tokenizer.decode(encoded)
        print(f"Decoded: {decoded}")
    
    return tokenizer


def demonstrate_gan_training(latex_expressions: List[str], tokenizer: LaTeXTokenizer, num_epochs: int = 10):
    """Demonstrate GAN training process."""
    print("\n" + "=" * 60)
    print("LATEX GAN TRAINING DEMONSTRATION")
    print("=" * 60)
    
    # Create GAN
    config = LaTeXGANConfig(
        vocab_size=tokenizer.vocab_size,
        max_sequence_length=256,
        hidden_dim=256,  # Smaller for demo
        num_layers=2     # Fewer layers for speed
    )
    
    latex_gan = LaTeXGAN(config, tokenizer)
    print(f"Created LaTeX GAN with {sum(p.numel() for p in latex_gan.parameters())} parameters")
    
    # Create dataset and dataloader
    dataset = LaTeXDataset(latex_expressions, tokenizer, max_length=config.max_sequence_length)
    dataloader = DataLoader(dataset, batch_size=8, shuffle=True)
    
    print(f"Training on {len(dataset)} expressions for {num_epochs} epochs")
    
    # Training loop
    train_losses = []
    
    for epoch in range(num_epochs):
        epoch_losses = []
        
        for batch_idx, batch in enumerate(dataloader):
            losses = latex_gan.train_step(batch)
            epoch_losses.append(losses)
            
            if batch_idx == 0:  # Show first batch of each epoch
                print(f"Epoch {epoch+1}/{num_epochs}, Batch 1: "
                      f"D_loss={losses['discriminator_loss']:.4f}, "
                      f"G_loss={losses['generator_loss']:.4f}, "
                      f"LaTeX_loss={losses['latex_constraint_loss']:.4f}")
        
        # Average losses for epoch
        avg_d_loss = sum(l['discriminator_loss'] for l in epoch_losses) / len(epoch_losses)
        avg_g_loss = sum(l['generator_loss'] for l in epoch_losses) / len(epoch_losses)
        avg_latex_loss = sum(l['latex_constraint_loss'] for l in epoch_losses) / len(epoch_losses)
        
        train_losses.append({
            'epoch': epoch + 1,
            'discriminator_loss': avg_d_loss,
            'generator_loss': avg_g_loss,
            'latex_constraint_loss': avg_latex_loss
        })
        
        print(f"Epoch {epoch+1} complete - Avg D_loss: {avg_d_loss:.4f}, Avg G_loss: {avg_g_loss:.4f}")
    
    return latex_gan, train_losses


def demonstrate_generation(latex_gan: LaTeXGAN, num_expressions: int = 10):
    """Demonstrate LaTeX expression generation."""
    print("\n" + "=" * 60)
    print("LATEX EXPRESSION GENERATION DEMONSTRATION")
    print("=" * 60)
    
    # Generate expressions with different temperatures
    temperatures = [0.5, 1.0, 1.5]
    
    for temp in temperatures:
        print(f"\nGenerating with temperature {temp} (lower = more conservative):")
        expressions = latex_gan.generate_new_latex_expressions(
            num_expressions=num_expressions // len(temperatures),
            temperature=temp
        )
        
        for i, expr in enumerate(expressions, 1):
            print(f"  {i}. {expr}")


def demonstrate_analysis(latex_gan: LaTeXGAN):
    """Demonstrate analysis of generated expressions."""
    print("\n" + "=" * 60)
    print("GENERATED EXPRESSION ANALYSIS")
    print("=" * 60)
    
    # Generate expressions for analysis
    generated_expressions = latex_gan.generate_new_latex_expressions(num_expressions=20)
    
    # Analyze patterns
    analysis = {
        'total_generated': len(generated_expressions),
        'avg_length': sum(len(expr) for expr in generated_expressions) / len(generated_expressions),
        'contains_sum': sum(1 for expr in generated_expressions if '\\sum' in expr),
        'contains_product': sum(1 for expr in generated_expressions if '\\prod' in expr),
        'contains_integral': sum(1 for expr in generated_expressions if '\\int' in expr),
        'contains_fraction': sum(1 for expr in generated_expressions if '\\frac' in expr),
        'contains_infinity': sum(1 for expr in generated_expressions if '\\infty' in expr),
        'unique_expressions': len(set(generated_expressions))
    }
    
    print("Analysis Results:")
    for key, value in analysis.items():
        print(f"  {key}: {value}")
    
    # Show diversity
    print(f"\nExpression diversity: {analysis['unique_expressions']/analysis['total_generated']*100:.1f}%")
    
    # Mathematical validity check
    valid_expressions = []
    for expr in generated_expressions:
        if (len(expr) > 5 and 
            expr.count('{') == expr.count('}') and 
            '\\' in expr and 
            not expr.startswith('<')):
            valid_expressions.append(expr)
    
    print(f"Valid expressions: {len(valid_expressions)}/{len(generated_expressions)} ({len(valid_expressions)/len(generated_expressions)*100:.1f}%)")
    
    if valid_expressions:
        print("\nSample valid expressions:")
        for i, expr in enumerate(valid_expressions[:5], 1):
            print(f"  {i}. {expr}")


def plot_training_curves(train_losses: List[Dict[str, Any]]):
    """Plot training loss curves."""
    print("\n" + "=" * 60)
    print("PLOTTING TRAINING CURVES")
    print("=" * 60)
    
    epochs = [loss['epoch'] for loss in train_losses]
    d_losses = [loss['discriminator_loss'] for loss in train_losses]
    g_losses = [loss['generator_loss'] for loss in train_losses]
    latex_losses = [loss['latex_constraint_loss'] for loss in train_losses]
    
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    plt.plot(epochs, d_losses, 'b-', label='Discriminator Loss')
    plt.plot(epochs, g_losses, 'r-', label='Generator Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Adversarial Losses')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(1, 3, 2)
    plt.plot(epochs, latex_losses, 'g-', label='LaTeX Constraint Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('LaTeX Constraint Loss')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(1, 3, 3)
    plt.plot(epochs, d_losses, 'b-', label='Discriminator')
    plt.plot(epochs, g_losses, 'r-', label='Generator')
    plt.plot(epochs, latex_losses, 'g-', label='LaTeX Constraint')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('All Losses')
    plt.legend()
    plt.grid(True)
    plt.yscale('log')
    
    plt.tight_layout()
    plt.savefig('latex_gan_training_curves.png', dpi=300, bbox_inches='tight')
    print("Training curves saved to 'latex_gan_training_curves.png'")
    plt.show()


def save_generated_expressions(latex_gan: LaTeXGAN, filename: str = "generated_latex_expressions.json"):
    """Save generated expressions to file."""
    print(f"\nSaving generated expressions to {filename}...")
    
    # Generate a variety of expressions
    generated_data = {
        'metadata': {
            'generator': 'LaTeX Expression GAN',
            'model_config': {
                'vocab_size': latex_gan.tokenizer.vocab_size,
                'embedding_dim': latex_gan.config.embedding_dim,
                'hidden_dim': latex_gan.config.hidden_dim,
                'num_layers': latex_gan.config.num_layers
            }
        },
        'expressions': {
            'conservative': latex_gan.generate_new_latex_expressions(10, temperature=0.5),
            'balanced': latex_gan.generate_new_latex_expressions(10, temperature=1.0),
            'creative': latex_gan.generate_new_latex_expressions(10, temperature=1.5)
        }
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(generated_data, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {sum(len(exprs) for exprs in generated_data['expressions'].values())} expressions saved!")


def main():
    """Main demonstration function."""
    print("🧠 LaTeX Expression GAN Demonstration")
    print("=====================================")
    print("This demonstration shows how to train a GAN on LaTeX mathematical expressions")
    print("from the divisor-wave projects and generate new mathematical formulations.\n")
    
    try:
        # 1. Load LaTeX expressions
        latex_expressions = demonstrate_latex_loading()
        
        if not latex_expressions:
            print("❌ No LaTeX expressions found. Cannot proceed with demonstration.")
            return
        
        # 2. Demonstrate tokenization
        tokenizer = demonstrate_tokenization(latex_expressions)
        
        # 3. Train GAN (short demo)
        print(f"\n⚠️  Training GAN for demo purposes (limited epochs)...")
        latex_gan, train_losses = demonstrate_gan_training(latex_expressions, tokenizer, num_epochs=5)
        
        # 4. Generate new expressions
        demonstrate_generation(latex_gan)
        
        # 5. Analyze generated expressions
        demonstrate_analysis(latex_gan)
        
        # 6. Plot training curves
        plot_training_curves(train_losses)
        
        # 7. Save generated expressions
        save_generated_expressions(latex_gan)
        
        print("\n" + "=" * 60)
        print("🎉 DEMONSTRATION COMPLETE!")
        print("=" * 60)
        print("The LaTeX Expression GAN can now:")
        print("✅ Load LaTeX expressions from your divisor-wave projects")
        print("✅ Learn patterns in mathematical notation")
        print("✅ Generate new, valid LaTeX expressions")
        print("✅ Create novel mathematical formulations")
        print("✅ Integrate with LlamaIndex agents as a tool")
        print("\nThis creates a 'Mathematical LaTeX Creativity Engine' for your research!")
        
    except Exception as e:
        print(f"❌ Demonstration failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()