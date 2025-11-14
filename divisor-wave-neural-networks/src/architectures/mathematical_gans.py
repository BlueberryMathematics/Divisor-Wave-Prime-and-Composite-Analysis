"""
Mathematical Generative Adversarial Networks (GANs)
===================================================

GANs specialized for mathematical discovery and sequence generation.
Includes generators for mathematical sequences, infinite products, and conjecture creation.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import math

from ..utils.mathematical_sequences import MathematicalSequences, SequenceType
from ..utils.loss_functions import SequenceLoss, RiemannLoss


class MathematicalGANType(Enum):
    """Types of mathematical GANs."""
    SEQUENCE_GAN = "sequence"
    CONJECTURE_GAN = "conjecture"
    INFINITE_PRODUCT_GAN = "infinite_product"
    RIEMANN_GAN = "riemann"
    PRIME_GAN = "prime"


@dataclass
class MathematicalGANConfig:
    """Configuration for mathematical GANs."""
    gan_type: MathematicalGANType = MathematicalGANType.SEQUENCE_GAN
    latent_dim: int = 128
    sequence_length: int = 256
    hidden_dim: int = 512
    num_layers: int = 4
    learning_rate_g: float = 0.0002
    learning_rate_d: float = 0.0002
    beta1: float = 0.5
    beta2: float = 0.999
    mathematical_constraint_weight: float = 1.0
    adversarial_weight: float = 1.0


class MathematicalGenerator(nn.Module):
    """Generator for mathematical sequences and structures."""
    
    def __init__(self, config: MathematicalGANConfig):
        super().__init__()
        
        self.config = config
        self.latent_dim = config.latent_dim
        self.sequence_length = config.sequence_length
        self.hidden_dim = config.hidden_dim
        
        # Mathematical constraint networks
        self.mathematical_encoder = self._build_mathematical_encoder()
        
        # Main generator network
        self.generator = self._build_generator()
        
        # Mathematical post-processing
        self.mathematical_postprocessor = self._build_postprocessor()
    
    def _build_mathematical_encoder(self) -> nn.Module:
        """Build encoder for mathematical constraints."""
        if self.config.gan_type == MathematicalGANType.SEQUENCE_GAN:
            return nn.Sequential(
                nn.Linear(self.latent_dim, self.hidden_dim),
                nn.LeakyReLU(0.2),
                nn.Linear(self.hidden_dim, self.hidden_dim),
                nn.BatchNorm1d(self.hidden_dim),
                nn.LeakyReLU(0.2)
            )
        elif self.config.gan_type == MathematicalGANType.RIEMANN_GAN:
            return RiemannConstraintEncoder(self.latent_dim, self.hidden_dim)
        elif self.config.gan_type == MathematicalGANType.PRIME_GAN:
            return PrimeConstraintEncoder(self.latent_dim, self.hidden_dim)
        else:
            return nn.Identity()
    
    def _build_generator(self) -> nn.Module:
        """Build main generator network."""
        layers = []
        
        # Input layer
        layers.extend([
            nn.Linear(self.hidden_dim, self.hidden_dim * 2),
            nn.BatchNorm1d(self.hidden_dim * 2),
            nn.LeakyReLU(0.2)
        ])
        
        # Hidden layers
        for _ in range(self.config.num_layers - 2):
            layers.extend([
                nn.Linear(self.hidden_dim * 2, self.hidden_dim * 2),
                nn.BatchNorm1d(self.hidden_dim * 2),
                nn.LeakyReLU(0.2)
            ])
        
        # Output layer
        layers.extend([
            nn.Linear(self.hidden_dim * 2, self.sequence_length),
            nn.Tanh()  # Normalize to [-1, 1]
        ])
        
        return nn.Sequential(*layers)
    
    def _build_postprocessor(self) -> nn.Module:
        """Build mathematical post-processor."""
        if self.config.gan_type == MathematicalGANType.SEQUENCE_GAN:
            return SequencePostprocessor(self.sequence_length)
        elif self.config.gan_type == MathematicalGANType.INFINITE_PRODUCT_GAN:
            return InfiniteProductPostprocessor(self.sequence_length)
        else:
            return nn.Identity()
    
    def forward(self, noise: torch.Tensor, mathematical_context: Optional[torch.Tensor] = None) -> torch.Tensor:
        """Generate mathematical sequences."""
        batch_size = noise.shape[0]
        
        # Encode mathematical constraints
        if mathematical_context is not None:
            combined_input = torch.cat([noise, mathematical_context], dim=1)
        else:
            combined_input = noise
        
        # Apply mathematical encoding
        encoded = self.mathematical_encoder(combined_input)
        
        # Generate sequence
        generated = self.generator(encoded)
        
        # Apply mathematical post-processing
        output = self.mathematical_postprocessor(generated)
        
        return output
    
    def generate_sequence(self, batch_size: int, mathematical_seed: Optional[torch.Tensor] = None) -> torch.Tensor:
        """Generate mathematical sequences with optional seed."""
        noise = torch.randn(batch_size, self.latent_dim)
        return self.forward(noise, mathematical_seed)


class MathematicalDiscriminator(nn.Module):
    """Discriminator that understands mathematical properties."""
    
    def __init__(self, config: MathematicalGANConfig):
        super().__init__()
        
        self.config = config
        self.sequence_length = config.sequence_length
        self.hidden_dim = config.hidden_dim
        
        # Mathematical feature extractor
        self.mathematical_features = self._build_mathematical_features()
        
        # Main discriminator
        self.discriminator = self._build_discriminator()
        
        # Mathematical validity checker
        self.validity_checker = self._build_validity_checker()
    
    def _build_mathematical_features(self) -> nn.Module:
        """Build mathematical feature extractor."""
        if self.config.gan_type == MathematicalGANType.SEQUENCE_GAN:
            return SequenceFeatureExtractor(self.sequence_length, self.hidden_dim)
        elif self.config.gan_type == MathematicalGANType.RIEMANN_GAN:
            return RiemannFeatureExtractor(self.sequence_length, self.hidden_dim)
        elif self.config.gan_type == MathematicalGANType.PRIME_GAN:
            return PrimeFeatureExtractor(self.sequence_length, self.hidden_dim)
        else:
            return nn.Sequential(
                nn.Linear(self.sequence_length, self.hidden_dim),
                nn.LeakyReLU(0.2)
            )
    
    def _build_discriminator(self) -> nn.Module:
        """Build main discriminator network."""
        layers = []
        
        # Input from mathematical features
        current_dim = self.hidden_dim
        
        for _ in range(self.config.num_layers):
            layers.extend([
                nn.Linear(current_dim, current_dim // 2),
                nn.LeakyReLU(0.2),
                nn.Dropout(0.3)
            ])
            current_dim = current_dim // 2
        
        # Output layer (real/fake probability)
        layers.append(nn.Linear(current_dim, 1))
        layers.append(nn.Sigmoid())
        
        return nn.Sequential(*layers)
    
    def _build_validity_checker(self) -> nn.Module:
        """Build mathematical validity checker."""
        return nn.Sequential(
            nn.Linear(self.hidden_dim, self.hidden_dim // 2),
            nn.LeakyReLU(0.2),
            nn.Linear(self.hidden_dim // 2, 1),
            nn.Sigmoid()
        )
    
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Discriminate real vs fake and check mathematical validity."""
        # Extract mathematical features
        features = self.mathematical_features(x)
        
        # Real/fake discrimination
        real_fake_prob = self.discriminator(features)
        
        # Mathematical validity
        validity_prob = self.validity_checker(features)
        
        return real_fake_prob, validity_prob


# Specialized Components for Different Mathematical Domains

class RiemannConstraintEncoder(nn.Module):
    """Encoder for Riemann hypothesis constraints."""
    
    def __init__(self, latent_dim: int, hidden_dim: int):
        super().__init__()
        
        self.encoder = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.Linear(hidden_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.LeakyReLU(0.2)
        )
        
        # Riemann-specific constraints
        self.zeta_constraint = nn.Linear(hidden_dim, hidden_dim)
        self.critical_line_constraint = nn.Linear(hidden_dim, hidden_dim)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        encoded = self.encoder(x)
        
        # Apply Riemann constraints
        zeta_constrained = self.zeta_constraint(encoded)
        critical_constrained = self.critical_line_constraint(encoded)
        
        # Combine constraints
        combined = encoded + 0.5 * (zeta_constrained + critical_constrained)
        
        return combined


class PrimeConstraintEncoder(nn.Module):
    """Encoder for prime number constraints."""
    
    def __init__(self, latent_dim: int, hidden_dim: int):
        super().__init__()
        
        self.encoder = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.Linear(hidden_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.LeakyReLU(0.2)
        )
        
        # Prime-specific constraints
        self.sieve_constraint = nn.Linear(hidden_dim, hidden_dim)
        self.distribution_constraint = nn.Linear(hidden_dim, hidden_dim)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        encoded = self.encoder(x)
        
        # Apply prime constraints
        sieve_constrained = self.sieve_constraint(encoded)
        dist_constrained = self.distribution_constraint(encoded)
        
        # Combine constraints
        combined = encoded + 0.5 * (sieve_constrained + dist_constrained)
        
        return combined


class SequenceFeatureExtractor(nn.Module):
    """Extract mathematical features from sequences."""
    
    def __init__(self, sequence_length: int, hidden_dim: int):
        super().__init__()
        
        self.sequence_length = sequence_length
        self.hidden_dim = hidden_dim
        
        # Feature extraction layers
        self.conv_features = nn.Sequential(
            nn.Conv1d(1, 32, kernel_size=3, padding=1),
            nn.LeakyReLU(0.2),
            nn.Conv1d(32, 64, kernel_size=3, padding=1),
            nn.LeakyReLU(0.2),
            nn.AdaptiveAvgPool1d(hidden_dim // 4)
        )
        
        self.statistical_features = nn.Linear(sequence_length, hidden_dim // 4)
        self.growth_features = nn.Linear(sequence_length - 1, hidden_dim // 4)
        self.pattern_features = nn.Linear(sequence_length, hidden_dim // 4)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch_size = x.shape[0]
        
        # Convolutional features
        conv_input = x.unsqueeze(1)  # Add channel dimension
        conv_feats = self.conv_features(conv_input).view(batch_size, -1)
        
        # Statistical features
        stat_feats = self.statistical_features(x)
        
        # Growth rate features
        growth_rates = x[:, 1:] - x[:, :-1]
        growth_feats = self.growth_features(growth_rates)
        
        # Pattern features (simplified)
        pattern_feats = self.pattern_features(x)
        
        # Combine all features
        combined = torch.cat([conv_feats, stat_feats, growth_feats, pattern_feats], dim=1)
        
        return combined


class RiemannFeatureExtractor(nn.Module):
    """Extract Riemann-specific features."""
    
    def __init__(self, sequence_length: int, hidden_dim: int):
        super().__init__()
        
        self.base_extractor = SequenceFeatureExtractor(sequence_length, hidden_dim // 2)
        
        # Riemann-specific features
        self.zeta_features = nn.Linear(sequence_length, hidden_dim // 4)
        self.critical_features = nn.Linear(sequence_length, hidden_dim // 4)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Base features
        base_feats = self.base_extractor(x)
        
        # Riemann-specific features
        zeta_feats = self.zeta_features(x)
        critical_feats = self.critical_features(x)
        
        # Combine
        combined = torch.cat([base_feats, zeta_feats, critical_feats], dim=1)
        
        return combined


class PrimeFeatureExtractor(nn.Module):
    """Extract prime-specific features."""
    
    def __init__(self, sequence_length: int, hidden_dim: int):
        super().__init__()
        
        self.base_extractor = SequenceFeatureExtractor(sequence_length, hidden_dim // 2)
        
        # Prime-specific features
        self.gap_features = nn.Linear(sequence_length - 1, hidden_dim // 4)
        self.density_features = nn.Linear(sequence_length, hidden_dim // 4)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Base features
        base_feats = self.base_extractor(x)
        
        # Prime gap features
        gaps = x[:, 1:] - x[:, :-1]
        gap_feats = self.gap_features(gaps)
        
        # Prime density features
        density_feats = self.density_features(x)
        
        # Combine
        combined = torch.cat([base_feats, gap_feats, density_feats], dim=1)
        
        return combined


# Post-processors

class SequencePostprocessor(nn.Module):
    """Post-process generated sequences to ensure mathematical validity."""
    
    def __init__(self, sequence_length: int):
        super().__init__()
        self.sequence_length = sequence_length
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Ensure monotonic growth for certain sequence types
        x_cumsum = torch.cumsum(torch.abs(x), dim=1)
        return x_cumsum


class InfiniteProductPostprocessor(nn.Module):
    """Post-process for infinite product generation."""
    
    def __init__(self, sequence_length: int):
        super().__init__()
        self.sequence_length = sequence_length
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Ensure convergence properties
        x_normalized = torch.sigmoid(x)  # Ensure [0,1] range
        x_product_ready = 1.0 + 0.1 * (x_normalized - 0.5)  # Near 1 for convergence
        return x_product_ready


class MathematicalGAN(nn.Module):
    """Complete Mathematical GAN system."""
    
    def __init__(self, config: MathematicalGANConfig):
        super().__init__()
        
        self.config = config
        self.generator = MathematicalGenerator(config)
        self.discriminator = MathematicalDiscriminator(config)
        
        # Optimizers
        self.optimizer_g = torch.optim.Adam(
            self.generator.parameters(),
            lr=config.learning_rate_g,
            betas=(config.beta1, config.beta2)
        )
        
        self.optimizer_d = torch.optim.Adam(
            self.discriminator.parameters(),
            lr=config.learning_rate_d,
            betas=(config.beta1, config.beta2)
        )
        
        # Loss functions
        self.adversarial_loss = nn.BCELoss()
        if config.gan_type == MathematicalGANType.SEQUENCE_GAN:
            self.mathematical_loss = SequenceLoss()
        elif config.gan_type == MathematicalGANType.RIEMANN_GAN:
            self.mathematical_loss = RiemannLoss()
        else:
            self.mathematical_loss = nn.MSELoss()
    
    def train_step(self, real_data: torch.Tensor) -> Dict[str, float]:
        """Single training step."""
        batch_size = real_data.shape[0]
        device = real_data.device
        
        # Labels
        real_labels = torch.ones(batch_size, 1, device=device)
        fake_labels = torch.zeros(batch_size, 1, device=device)
        
        # Train Discriminator
        self.optimizer_d.zero_grad()
        
        # Real data
        real_pred, real_validity = self.discriminator(real_data)
        d_real_loss = self.adversarial_loss(real_pred, real_labels)
        d_real_validity_loss = self.adversarial_loss(real_validity, real_labels)
        
        # Fake data
        noise = torch.randn(batch_size, self.config.latent_dim, device=device)
        fake_data = self.generator(noise)
        fake_pred, fake_validity = self.discriminator(fake_data.detach())
        d_fake_loss = self.adversarial_loss(fake_pred, fake_labels)
        d_fake_validity_loss = self.adversarial_loss(fake_validity, fake_labels)
        
        d_loss = (d_real_loss + d_fake_loss + d_real_validity_loss + d_fake_validity_loss) / 4
        d_loss.backward()
        self.optimizer_d.step()
        
        # Train Generator
        self.optimizer_g.zero_grad()
        
        # Generate fake data
        noise = torch.randn(batch_size, self.config.latent_dim, device=device)
        fake_data = self.generator(noise)
        fake_pred, fake_validity = self.discriminator(fake_data)
        
        # Adversarial loss
        g_adv_loss = self.adversarial_loss(fake_pred, real_labels)
        g_validity_loss = self.adversarial_loss(fake_validity, real_labels)
        
        # Mathematical constraint loss
        g_math_loss = self.mathematical_loss(fake_data, real_data[:batch_size])
        
        # Combined generator loss
        g_loss = (self.config.adversarial_weight * (g_adv_loss + g_validity_loss) + 
                 self.config.mathematical_constraint_weight * g_math_loss)
        
        g_loss.backward()
        self.optimizer_g.step()
        
        return {
            'discriminator_loss': d_loss.item(),
            'generator_loss': g_loss.item(),
            'mathematical_loss': g_math_loss.item()
        }
    
    def generate_mathematical_sequences(self, num_sequences: int, seed: Optional[int] = None) -> torch.Tensor:
        """Generate mathematical sequences."""
        if seed is not None:
            torch.manual_seed(seed)
        
        noise = torch.randn(num_sequences, self.config.latent_dim)
        
        with torch.no_grad():
            generated = self.generator(noise)
        
        return generated


# Factory functions

def create_sequence_gan(sequence_length: int = 256, hidden_dim: int = 512) -> MathematicalGAN:
    """Create GAN for mathematical sequence generation."""
    config = MathematicalGANConfig(
        gan_type=MathematicalGANType.SEQUENCE_GAN,
        sequence_length=sequence_length,
        hidden_dim=hidden_dim
    )
    return MathematicalGAN(config)


def create_riemann_gan(sequence_length: int = 256, hidden_dim: int = 512) -> MathematicalGAN:
    """Create GAN for Riemann hypothesis exploration."""
    config = MathematicalGANConfig(
        gan_type=MathematicalGANType.RIEMANN_GAN,
        sequence_length=sequence_length,
        hidden_dim=hidden_dim,
        mathematical_constraint_weight=2.0  # Higher weight for mathematical constraints
    )
    return MathematicalGAN(config)


def create_prime_gan(sequence_length: int = 256, hidden_dim: int = 512) -> MathematicalGAN:
    """Create GAN for prime number generation and analysis."""
    config = MathematicalGANConfig(
        gan_type=MathematicalGANType.PRIME_GAN,
        sequence_length=sequence_length,
        hidden_dim=hidden_dim,
        mathematical_constraint_weight=1.5
    )
    return MathematicalGAN(config)