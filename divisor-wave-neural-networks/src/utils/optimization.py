"""
Optimization Tools for Mathematical Neural Networks
==================================================

Custom optimizers and learning rate schedulers for mathematical pattern discovery.
"""

import torch
import torch.optim as optim
from torch.optim.lr_scheduler import _LRScheduler
import math
from typing import Dict, Any, Optional, List

class MathematicalAdam(optim.Adam):
    """Adam optimizer with mathematical sequence-aware learning rates."""
    
    def __init__(self, params, lr=1e-3, sequence_decay=0.99, **kwargs):
        super().__init__(params, lr=lr, **kwargs)
        self.sequence_decay = sequence_decay
        self.step_count = 0
    
    def step(self, closure=None):
        self.step_count += 1
        
        # Adjust learning rate based on mathematical sequence
        for group in self.param_groups:
            # Golden ratio decay
            phi = (1 + math.sqrt(5)) / 2
            decay_factor = 1 / (1 + self.step_count / (phi * 100))
            group['lr'] = group['lr'] * decay_factor
        
        return super().step(closure)


class PrimeScheduler(_LRScheduler):
    """Learning rate scheduler based on prime numbers."""
    
    def __init__(self, optimizer, max_primes=100, last_epoch=-1):
        self.primes = self._generate_primes(max_primes)
        self.prime_index = 0
        super().__init__(optimizer, last_epoch)
    
    def _generate_primes(self, max_val: int) -> List[int]:
        sieve = [True] * (max_val + 1)
        sieve[0] = sieve[1] = False
        
        for i in range(2, int(max_val**0.5) + 1):
            if sieve[i]:
                for j in range(i*i, max_val + 1, i):
                    sieve[j] = False
        
        return [i for i in range(2, max_val + 1) if sieve[i]]
    
    def get_lr(self):
        if self.last_epoch in self.primes:
            # Boost learning rate at prime epochs
            return [base_lr * 1.1 for base_lr in self.base_lrs]
        else:
            # Normal decay
            return [base_lr * 0.99 for base_lr in self.base_lrs]


class FibonacciScheduler(_LRScheduler):
    """Learning rate scheduler based on Fibonacci sequence."""
    
    def __init__(self, optimizer, scale_factor=0.01, last_epoch=-1):
        self.scale_factor = scale_factor
        self.fib_a, self.fib_b = 1, 1
        super().__init__(optimizer, last_epoch)
    
    def get_lr(self):
        # Update Fibonacci sequence
        self.fib_a, self.fib_b = self.fib_b, self.fib_a + self.fib_b
        
        # Use Fibonacci ratio for learning rate adjustment
        ratio = self.fib_a / self.fib_b if self.fib_b != 0 else 1.0
        adjustment = 1.0 + self.scale_factor * (ratio - 0.618)  # Golden ratio target
        
        return [base_lr * adjustment for base_lr in self.base_lrs]


class TetrahedralScheduler(_LRScheduler):
    """Learning rate scheduler based on tetrahedral numbers."""
    
    def __init__(self, optimizer, scale_factor=0.001, last_epoch=-1):
        self.scale_factor = scale_factor
        super().__init__(optimizer, last_epoch)
    
    def tetrahedral_number(self, n: int) -> int:
        """Calculate the nth tetrahedral number."""
        return n * (n + 1) * (n + 2) // 6
    
    def get_lr(self):
        n = max(1, self.last_epoch)
        tet_n = self.tetrahedral_number(n)
        tet_prev = self.tetrahedral_number(n - 1) if n > 1 else 1
        
        # Use growth rate of tetrahedral numbers
        growth_rate = tet_n / tet_prev if tet_prev != 0 else 1.0
        adjustment = 1.0 / (1.0 + self.scale_factor * growth_rate)
        
        return [base_lr * adjustment for base_lr in self.base_lrs]


class RiemannScheduler(_LRScheduler):
    """Learning rate scheduler inspired by Riemann zeta function."""
    
    def __init__(self, optimizer, s_real=2.0, scale_factor=0.1, last_epoch=-1):
        self.s_real = s_real
        self.scale_factor = scale_factor
        super().__init__(optimizer, last_epoch)
    
    def zeta_approximation(self, s: float, terms: int = 1000) -> float:
        """Approximate Riemann zeta function."""
        return sum(1 / (n ** s) for n in range(1, terms + 1))
    
    def get_lr(self):
        # Use zeta function values to modulate learning rate
        epoch_s = self.s_real + 0.01 * self.last_epoch
        zeta_val = self.zeta_approximation(epoch_s, terms=100)
        
        # Normalize and apply to learning rate
        adjustment = 1.0 / (1.0 + self.scale_factor * zeta_val)
        
        return [base_lr * adjustment for base_lr in self.base_lrs]


class AdaptiveMathOptimizer:
    """Adaptive optimizer that chooses optimization strategy based on loss behavior."""
    
    def __init__(self, model_params, initial_lr=1e-3):
        self.model_params = list(model_params)
        self.initial_lr = initial_lr
        self.loss_history = []
        self.current_optimizer = None
        self.current_scheduler = None
        self._initialize_optimizer('adam')
    
    def _initialize_optimizer(self, optimizer_type: str):
        """Initialize optimizer based on type."""
        if optimizer_type == 'adam':
            self.current_optimizer = optim.Adam(self.model_params, lr=self.initial_lr)
            self.current_scheduler = None
        elif optimizer_type == 'sgd':
            self.current_optimizer = optim.SGD(self.model_params, lr=self.initial_lr, momentum=0.9)
            self.current_scheduler = PrimeScheduler(self.current_optimizer)
        elif optimizer_type == 'mathematical_adam':
            self.current_optimizer = MathematicalAdam(self.model_params, lr=self.initial_lr)
            self.current_scheduler = FibonacciScheduler(self.current_optimizer)
    
    def step(self, loss_value: float, closure=None):
        """Step the optimizer and potentially switch strategies."""
        self.loss_history.append(loss_value)
        
        # Switch optimization strategy based on loss behavior
        if len(self.loss_history) > 100:
            recent_losses = self.loss_history[-50:]
            old_losses = self.loss_history[-100:-50]
            
            recent_avg = sum(recent_losses) / len(recent_losses)
            old_avg = sum(old_losses) / len(old_losses)
            
            # If loss plateaued, switch optimizer
            if abs(recent_avg - old_avg) < 1e-6:
                current_type = type(self.current_optimizer).__name__
                if current_type == 'Adam':
                    self._initialize_optimizer('mathematical_adam')
                elif current_type == 'MathematicalAdam':
                    self._initialize_optimizer('sgd')
                else:
                    self._initialize_optimizer('adam')
        
        # Step the optimizer
        result = self.current_optimizer.step(closure)
        
        # Step the scheduler if it exists
        if self.current_scheduler is not None:
            self.current_scheduler.step()
        
        return result
    
    def zero_grad(self):
        """Zero gradients."""
        self.current_optimizer.zero_grad()


def get_optimizer(optimizer_type: str, model_params, **kwargs) -> torch.optim.Optimizer:
    """Factory function for optimizers."""
    optimizers = {
        'adam': optim.Adam,
        'sgd': optim.SGD,
        'rmsprop': optim.RMSprop,
        'mathematical_adam': MathematicalAdam,
        'adaptive': lambda params, **kw: AdaptiveMathOptimizer(params, **kw)
    }
    
    if optimizer_type not in optimizers:
        raise ValueError(f"Unknown optimizer type: {optimizer_type}")
    
    return optimizers[optimizer_type](model_params, **kwargs)


def get_scheduler(scheduler_type: str, optimizer, **kwargs) -> _LRScheduler:
    """Factory function for learning rate schedulers."""
    schedulers = {
        'prime': PrimeScheduler,
        'fibonacci': FibonacciScheduler,
        'tetrahedral': TetrahedralScheduler,
        'riemann': RiemannScheduler,
        'step': optim.lr_scheduler.StepLR,
        'exponential': optim.lr_scheduler.ExponentialLR,
        'cosine': optim.lr_scheduler.CosineAnnealingLR
    }
    
    if scheduler_type not in schedulers:
        raise ValueError(f"Unknown scheduler type: {scheduler_type}")
    
    return schedulers[scheduler_type](optimizer, **kwargs)