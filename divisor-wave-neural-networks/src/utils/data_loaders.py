"""
Data Loaders for Mathematical Functions
=======================================

Specialized data loaders for mathematical sequences, formulas, and patterns.
"""

import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
from typing import List, Dict, Tuple, Optional

class MathematicalDataLoader:
    """Specialized data loader for mathematical data."""
    
    def __init__(self, batch_size: int = 32, shuffle: bool = True):
        self.batch_size = batch_size
        self.shuffle = shuffle
    
    def create_loader(self, dataset: Dataset) -> DataLoader:
        return DataLoader(dataset, batch_size=self.batch_size, shuffle=self.shuffle)


class SequenceDataset(Dataset):
    """Dataset for mathematical sequences."""
    
    def __init__(self, sequences: List[torch.Tensor], targets: Optional[List[torch.Tensor]] = None):
        self.sequences = sequences
        self.targets = targets or sequences
    
    def __len__(self):
        return len(self.sequences)
    
    def __getitem__(self, idx):
        return self.sequences[idx], self.targets[idx]


class FormulaDataset(Dataset):
    """Dataset for mathematical formulas."""
    
    def __init__(self, formulas: Dict[str, torch.Tensor]):
        self.formulas = list(formulas.values())
    
    def __len__(self):
        return len(self.formulas)
    
    def __getitem__(self, idx):
        return self.formulas[idx], self.formulas[idx]  # Self-supervised


class PrimeDataset(Dataset):
    """Dataset for prime number sequences."""
    
    def __init__(self, max_prime: int = 1000):
        self.primes = self._generate_primes(max_prime)
    
    def _generate_primes(self, max_val: int) -> List[int]:
        sieve = [True] * (max_val + 1)
        sieve[0] = sieve[1] = False
        
        for i in range(2, int(max_val**0.5) + 1):
            if sieve[i]:
                for j in range(i*i, max_val + 1, i):
                    sieve[j] = False
        
        return [i for i in range(2, max_val + 1) if sieve[i]]
    
    def __len__(self):
        return len(self.primes) - 1
    
    def __getitem__(self, idx):
        # Predict next prime
        return torch.tensor(self.primes[:idx+1], dtype=torch.float32), torch.tensor(self.primes[idx+1], dtype=torch.float32)