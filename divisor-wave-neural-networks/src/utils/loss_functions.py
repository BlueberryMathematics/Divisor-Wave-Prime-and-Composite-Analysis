"""
Common Loss Functions for Mathematical Neural Networks
=====================================================

Custom loss functions designed for mathematical sequences and patterns.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Optional, Callable

class SequenceLoss(nn.Module):
    """Loss function for sequence prediction."""
    
    def __init__(self, reduction: str = 'mean'):
        super().__init__()
        self.reduction = reduction
    
    def forward(self, predictions: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        return F.mse_loss(predictions, targets, reduction=self.reduction)


class RiemannLoss(nn.Module):
    """Loss function for Riemann Hypothesis related predictions."""
    
    def __init__(self, critical_line_weight: float = 1.0):
        super().__init__()
        self.critical_line_weight = critical_line_weight
    
    def forward(self, predictions: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        # Standard MSE loss
        mse_loss = F.mse_loss(predictions, targets)
        
        # Add penalty for deviation from critical line (Re(s) = 1/2)
        if predictions.shape[-1] >= 2:  # Complex predictions
            real_parts = predictions[..., 0]
            critical_line_penalty = torch.mean((real_parts - 0.5) ** 2)
            return mse_loss + self.critical_line_weight * critical_line_penalty
        
        return mse_loss


class PrimeLoss(nn.Module):
    """Loss function for prime number predictions."""
    
    def __init__(self, sparsity_weight: float = 0.1):
        super().__init__()
        self.sparsity_weight = sparsity_weight
    
    def forward(self, predictions: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        # Standard loss
        base_loss = F.binary_cross_entropy_with_logits(predictions, targets)
        
        # Add sparsity regularization (primes are sparse)
        sparsity_loss = torch.mean(torch.sigmoid(predictions))
        
        return base_loss + self.sparsity_weight * sparsity_loss


class DivisorWaveLoss(nn.Module):
    """Loss function for divisor wave predictions."""
    
    def __init__(self, phase_weight: float = 1.0, amplitude_weight: float = 1.0):
        super().__init__()
        self.phase_weight = phase_weight
        self.amplitude_weight = amplitude_weight
    
    def forward(self, predictions: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        if predictions.shape[-1] >= 2:  # Complex predictions
            pred_real, pred_imag = predictions[..., 0], predictions[..., 1]
            targ_real, targ_imag = targets[..., 0], targets[..., 1]
            
            # Amplitude loss
            pred_amp = torch.sqrt(pred_real**2 + pred_imag**2)
            targ_amp = torch.sqrt(targ_real**2 + targ_imag**2)
            amp_loss = F.mse_loss(pred_amp, targ_amp)
            
            # Phase loss
            pred_phase = torch.atan2(pred_imag, pred_real)
            targ_phase = torch.atan2(targ_imag, targ_real)
            phase_loss = F.mse_loss(pred_phase, targ_phase)
            
            return self.amplitude_weight * amp_loss + self.phase_weight * phase_loss
        
        return F.mse_loss(predictions, targets)


class CrystalLoss(nn.Module):
    """Loss function for crystal embedding models."""
    
    def __init__(self, symmetry_weight: float = 0.5):
        super().__init__()
        self.symmetry_weight = symmetry_weight
    
    def forward(self, embeddings: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        # Standard embedding loss
        base_loss = F.mse_loss(embeddings, targets)
        
        # Symmetry preservation loss
        # Check rotational invariance
        batch_size, embed_dim = embeddings.shape
        if embed_dim >= 3:  # 3D embeddings
            # Simple rotation around z-axis
            cos_theta, sin_theta = 0.7071, 0.7071  # 45 degrees
            rotation_matrix = torch.tensor([
                [cos_theta, -sin_theta, 0],
                [sin_theta, cos_theta, 0],
                [0, 0, 1]
            ], device=embeddings.device, dtype=embeddings.dtype)
            
            rotated_embeddings = torch.matmul(embeddings[:, :3], rotation_matrix.T)
            symmetry_loss = F.mse_loss(rotated_embeddings, embeddings[:, :3])
            
            return base_loss + self.symmetry_weight * symmetry_loss
        
        return base_loss


class ContrastiveLoss(nn.Module):
    """Contrastive loss for mathematical pattern recognition."""
    
    def __init__(self, margin: float = 1.0):
        super().__init__()
        self.margin = margin
    
    def forward(self, output1: torch.Tensor, output2: torch.Tensor, label: torch.Tensor) -> torch.Tensor:
        euclidean_distance = F.pairwise_distance(output1, output2)
        loss_contrastive = torch.mean((1-label) * torch.pow(euclidean_distance, 2) +
                                    (label) * torch.pow(torch.clamp(self.margin - euclidean_distance, min=0.0), 2))
        return loss_contrastive


def get_loss_function(loss_type: str, **kwargs) -> nn.Module:
    """Factory function to get loss functions."""
    loss_functions = {
        'sequence': SequenceLoss,
        'riemann': RiemannLoss,
        'prime': PrimeLoss,
        'divisor_wave': DivisorWaveLoss,
        'crystal': CrystalLoss,
        'contrastive': ContrastiveLoss,
        'mse': nn.MSELoss,
        'bce': nn.BCEWithLogitsLoss,
        'crossentropy': nn.CrossEntropyLoss
    }
    
    if loss_type not in loss_functions:
        raise ValueError(f"Unknown loss type: {loss_type}")
    
    return loss_functions[loss_type](**kwargs)