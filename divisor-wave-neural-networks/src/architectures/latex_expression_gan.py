"""
LaTeX Mathematical Expression GAN
=================================

GAN specifically designed to generate new LaTeX mathematical expressions
by training on existing LaTeX sequences from JSON files in the divisor-wave projects.

This creates a "Mathematical LaTeX Creativity Engine" that can:
- Learn patterns in LaTeX mathematical notation
- Generate new, syntactically valid LaTeX expressions
- Discover novel mathematical formulations
- Create LaTeX for infinite products, sums, integrals, etc.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import json
import os
import re
from typing import Dict, List, Optional, Tuple, Union, Any
from dataclasses import dataclass
from pathlib import Path
import random

# For LaTeX tokenization
from collections import Counter, defaultdict


@dataclass
class LaTeXGANConfig:
    """Configuration for LaTeX GAN."""
    vocab_size: int = 10000
    embedding_dim: int = 256
    hidden_dim: int = 512
    num_layers: int = 4
    max_sequence_length: int = 512
    learning_rate_g: float = 0.0002
    learning_rate_d: float = 0.0002
    beta1: float = 0.5
    beta2: float = 0.999
    dropout_rate: float = 0.1
    latex_constraint_weight: float = 2.0
    adversarial_weight: float = 1.0
    temperature: float = 1.0


class LaTeXTokenizer:
    """Tokenizer specifically for LaTeX mathematical expressions."""
    
    def __init__(self):
        self.token_to_id = {}
        self.id_to_token = {}
        self.vocab_size = 0
        
        # Special tokens
        self.PAD_TOKEN = "<PAD>"
        self.START_TOKEN = "<START>"
        self.END_TOKEN = "<END>"
        self.UNK_TOKEN = "<UNK>"
        
        # LaTeX-specific regex patterns
        self.latex_patterns = [
            r'\\[a-zA-Z]+',           # LaTeX commands (\sum, \int, \frac, etc.)
            r'\{[^}]*\}',             # Braced expressions {content}
            r'\[[^\]]*\]',            # Bracketed expressions [content]
            r'\([^)]*\)',             # Parenthetical expressions
            r'[0-9]+\.?[0-9]*',       # Numbers
            r'[a-zA-Z]',              # Variables
            r'[+\-*/=<>!]',           # Operators
            r'[,;:]',                 # Punctuation
            r'\^',                    # Superscript
            r'_',                     # Subscript
            r'&',                     # Alignment
            r'\\\\',                  # Line breaks
            r'\s+',                   # Whitespace
        ]
        
        self.latex_regex = '|'.join(f'({pattern})' for pattern in self.latex_patterns)
    
    def tokenize_latex(self, latex_text: str) -> List[str]:
        """Tokenize LaTeX expression into meaningful tokens."""
        # Find all matches
        matches = re.findall(self.latex_regex, latex_text)
        
        tokens = []
        for match_groups in matches:
            for token in match_groups:
                if token and token.strip():
                    tokens.append(token.strip())
        
        return tokens
    
    def build_vocabulary(self, latex_expressions: List[str]) -> None:
        """Build vocabulary from LaTeX expressions."""
        token_counts = Counter()
        
        # Add special tokens
        special_tokens = [self.PAD_TOKEN, self.START_TOKEN, self.END_TOKEN, self.UNK_TOKEN]
        for token in special_tokens:
            token_counts[token] = 1000000  # High count to ensure they're kept
        
        # Tokenize all expressions and count tokens
        for expr in latex_expressions:
            tokens = self.tokenize_latex(expr)
            token_counts.update(tokens)
        
        # Build vocabulary from most common tokens
        most_common = token_counts.most_common()
        
        self.token_to_id = {}
        self.id_to_token = {}
        
        for i, (token, count) in enumerate(most_common):
            if i >= 10000:  # Limit vocabulary size
                break
            self.token_to_id[token] = i
            self.id_to_token[i] = token
        
        self.vocab_size = len(self.token_to_id)
        print(f"Built vocabulary with {self.vocab_size} tokens")
    
    def encode(self, latex_text: str, max_length: Optional[int] = None) -> List[int]:
        """Encode LaTeX text to token IDs."""
        tokens = self.tokenize_latex(latex_text)
        
        # Add start and end tokens
        token_ids = [self.token_to_id[self.START_TOKEN]]
        
        for token in tokens:
            if token in self.token_to_id:
                token_ids.append(self.token_to_id[token])
            else:
                token_ids.append(self.token_to_id[self.UNK_TOKEN])
        
        token_ids.append(self.token_to_id[self.END_TOKEN])
        
        # Pad or truncate
        if max_length:
            if len(token_ids) < max_length:
                token_ids.extend([self.token_to_id[self.PAD_TOKEN]] * (max_length - len(token_ids)))
            else:
                token_ids = token_ids[:max_length]
        
        return token_ids
    
    def decode(self, token_ids: List[int]) -> str:
        """Decode token IDs back to LaTeX text."""
        tokens = []
        for token_id in token_ids:
            if token_id in self.id_to_token:
                token = self.id_to_token[token_id]
                if token not in [self.PAD_TOKEN, self.START_TOKEN, self.END_TOKEN]:
                    tokens.append(token)
        
        # Join tokens with appropriate spacing
        latex_text = ""
        for i, token in enumerate(tokens):
            if token.startswith('\\'):
                latex_text += token + " "
            elif token in ['{', '[', '(']:
                latex_text += token
            elif token in ['}', ']', ')']:
                latex_text = latex_text.rstrip() + token + " "
            elif token in ['^', '_']:
                latex_text = latex_text.rstrip() + token
            else:
                latex_text += token
        
        return latex_text.strip()


class LaTeXDataLoader:
    """Load LaTeX expressions from JSON files in divisor-wave projects."""
    
    def __init__(self, projects_root: str):
        self.projects_root = Path(projects_root)
        self.latex_expressions = []
    
    def load_from_divisor_wave_projects(self) -> List[str]:
        """Load LaTeX expressions from all divisor-wave project JSON files."""
        latex_expressions = []
        
        # Search for JSON files in all divisor-wave projects
        project_dirs = [
            "divisor-wave-python",
            "divisor-wave-agent", 
            "divisor-wave-nextjs",
            "divisor-wave-neural-networks"
        ]
        
        for project_dir in project_dirs:
            project_path = self.projects_root / project_dir
            if project_path.exists():
                latex_expressions.extend(self._load_from_project(project_path))
        
        # Also look for any specific LaTeX/math JSON files
        latex_expressions.extend(self._load_custom_mathematical_expressions())
        
        self.latex_expressions = latex_expressions
        print(f"Loaded {len(latex_expressions)} LaTeX expressions")
        return latex_expressions
    
    def _load_from_project(self, project_path: Path) -> List[str]:
        """Load LaTeX expressions from a specific project."""
        expressions = []
        
        # Search for JSON files recursively
        for json_file in project_path.rglob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    expressions.extend(self._extract_latex_from_json(data))
            except Exception as e:
                print(f"Error loading {json_file}: {e}")
        
        return expressions
    
    def _extract_latex_from_json(self, data: Any) -> List[str]:
        """Extract LaTeX expressions from JSON data."""
        expressions = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                # Look for keys that might contain LaTeX
                if any(keyword in key.lower() for keyword in ['latex', 'formula', 'expression', 'equation']):
                    if isinstance(value, str) and ('\\' in value or '$' in value):
                        expressions.append(value)
                
                # Recursively search nested structures
                expressions.extend(self._extract_latex_from_json(value))
                
        elif isinstance(data, list):
            for item in data:
                expressions.extend(self._extract_latex_from_json(item))
                
        elif isinstance(data, str):
            # Check if string looks like LaTeX
            if ('\\' in data or '$' in data) and len(data) > 5:
                expressions.append(data)
        
        return expressions
    
    def _load_custom_mathematical_expressions(self) -> List[str]:
        """Load additional mathematical LaTeX expressions."""
        # Common mathematical LaTeX patterns for training
        mathematical_templates = [
            r"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}",
            r"\int_{0}^{\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}",
            r"\prod_{p \text{ prime}} \left(1 - \frac{1}{p^s}\right)^{-1} = \zeta(s)",
            r"\sum_{n=0}^{\infty} \frac{x^n}{n!} = e^x",
            r"\int_{-\infty}^{\infty} e^{-\frac{x^2}{2}} dx = \sqrt{2\pi}",
            r"\sum_{k=0}^{n} \binom{n}{k} x^k y^{n-k} = (x+y)^n",
            r"\prod_{n=1}^{\infty} \left(1 + x^{2n-1}\right) = \sum_{n=0}^{\infty} x^{n^2}",
            r"\sum_{n=1}^{\infty} \frac{(-1)^{n+1}}{2n-1} = \frac{\pi}{4}",
            r"\int_{0}^{1} x^{p-1}(1-x)^{q-1} dx = \frac{\Gamma(p)\Gamma(q)}{\Gamma(p+q)}",
            r"\sum_{n=0}^{\infty} \frac{(-1)^n x^{2n+1}}{(2n+1)!} = \sin(x)"
        ]
        
        return mathematical_templates


class LaTeXGenerator(nn.Module):
    """Generator for LaTeX mathematical expressions."""
    
    def __init__(self, config: LaTeXGANConfig, tokenizer: LaTeXTokenizer):
        super().__init__()
        
        self.config = config
        self.tokenizer = tokenizer
        self.vocab_size = tokenizer.vocab_size
        
        # Embedding layer
        self.embedding = nn.Embedding(self.vocab_size, config.embedding_dim)
        
        # LSTM for sequence generation
        self.lstm = nn.LSTM(
            config.embedding_dim,
            config.hidden_dim,
            config.num_layers,
            batch_first=True,
            dropout=config.dropout_rate if config.num_layers > 1 else 0
        )
        
        # Output projection
        self.output_projection = nn.Linear(config.hidden_dim, self.vocab_size)
        
        # Mathematical constraint network
        self.constraint_network = nn.Sequential(
            nn.Linear(config.hidden_dim, config.hidden_dim),
            nn.ReLU(),
            nn.Linear(config.hidden_dim, config.hidden_dim),
            nn.LayerNorm(config.hidden_dim)
        )
    
    def forward(self, input_ids: torch.Tensor, hidden: Optional[Tuple[torch.Tensor, torch.Tensor]] = None) -> Tuple[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
        """Generate LaTeX sequences."""
        # Embedding
        embedded = self.embedding(input_ids)
        
        # LSTM
        lstm_out, hidden = self.lstm(embedded, hidden)
        
        # Apply mathematical constraints
        constrained = self.constraint_network(lstm_out)
        lstm_out = lstm_out + constrained
        
        # Output projection
        logits = self.output_projection(lstm_out)
        
        return logits, hidden
    
    def generate_latex(self, 
                      max_length: int = 256, 
                      temperature: float = 1.0,
                      seed_text: Optional[str] = None) -> str:
        """Generate a LaTeX expression."""
        self.eval()
        
        with torch.no_grad():
            # Initialize with start token or seed
            if seed_text:
                token_ids = self.tokenizer.encode(seed_text, max_length=10)
            else:
                token_ids = [self.tokenizer.token_to_id[self.tokenizer.START_TOKEN]]
            
            generated_ids = token_ids.copy()
            hidden = None
            
            for _ in range(max_length):
                # Convert to tensor
                input_tensor = torch.tensor([token_ids], dtype=torch.long)
                
                # Forward pass
                logits, hidden = self.forward(input_tensor, hidden)
                
                # Get next token probabilities
                next_token_logits = logits[0, -1, :] / temperature
                next_token_probs = F.softmax(next_token_logits, dim=-1)
                
                # Sample next token
                next_token_id = torch.multinomial(next_token_probs, 1).item()
                
                # Check for end token
                if next_token_id == self.tokenizer.token_to_id[self.tokenizer.END_TOKEN]:
                    break
                
                generated_ids.append(next_token_id)
                token_ids = [next_token_id]  # Use only the last token for next input
        
        # Decode to LaTeX
        generated_latex = self.tokenizer.decode(generated_ids)
        return generated_latex


class LaTeXDiscriminator(nn.Module):
    """Discriminator for LaTeX expressions."""
    
    def __init__(self, config: LaTeXGANConfig, tokenizer: LaTeXTokenizer):
        super().__init__()
        
        self.config = config
        self.tokenizer = tokenizer
        self.vocab_size = tokenizer.vocab_size
        
        # Embedding
        self.embedding = nn.Embedding(self.vocab_size, config.embedding_dim)
        
        # CNN for pattern recognition
        self.conv_layers = nn.ModuleList([
            nn.Conv1d(config.embedding_dim, 128, kernel_size=3, padding=1),
            nn.Conv1d(128, 256, kernel_size=3, padding=1),
            nn.Conv1d(256, 512, kernel_size=3, padding=1)
        ])
        
        # LSTM for sequential understanding
        self.lstm = nn.LSTM(
            512,
            config.hidden_dim,
            config.num_layers,
            batch_first=True,
            dropout=config.dropout_rate if config.num_layers > 1 else 0
        )
        
        # LaTeX validity checker
        self.latex_validator = nn.Sequential(
            nn.Linear(config.hidden_dim, config.hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(config.dropout_rate),
            nn.Linear(config.hidden_dim // 2, 1),
            nn.Sigmoid()
        )
        
        # Real/fake classifier
        self.classifier = nn.Sequential(
            nn.Linear(config.hidden_dim, config.hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(config.dropout_rate),
            nn.Linear(config.hidden_dim // 2, 1),
            nn.Sigmoid()
        )
    
    def forward(self, input_ids: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Classify LaTeX expressions as real/fake and valid/invalid."""
        # Embedding
        embedded = self.embedding(input_ids)  # (batch, seq, embed)
        
        # CNN processing
        x = embedded.transpose(1, 2)  # (batch, embed, seq)
        for conv in self.conv_layers:
            x = F.relu(conv(x))
            x = F.max_pool1d(x, kernel_size=2, stride=1, padding=1)
        
        x = x.transpose(1, 2)  # (batch, seq, features)
        
        # LSTM processing
        lstm_out, (hidden, _) = self.lstm(x)
        
        # Use final hidden state
        final_hidden = hidden[-1]  # Last layer's hidden state
        
        # LaTeX validity
        validity = self.latex_validator(final_hidden)
        
        # Real/fake classification
        real_fake = self.classifier(final_hidden)
        
        return real_fake, validity


class LaTeXGAN(nn.Module):
    """Complete LaTeX Mathematical Expression GAN."""
    
    def __init__(self, config: LaTeXGANConfig, tokenizer: LaTeXTokenizer):
        super().__init__()
        
        self.config = config
        self.tokenizer = tokenizer
        
        # Networks
        self.generator = LaTeXGenerator(config, tokenizer)
        self.discriminator = LaTeXDiscriminator(config, tokenizer)
        
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
        self.latex_loss = nn.CrossEntropyLoss(ignore_index=tokenizer.token_to_id[tokenizer.PAD_TOKEN])
    
    def train_step(self, real_sequences: torch.Tensor) -> Dict[str, float]:
        """Single training step."""
        batch_size, seq_len = real_sequences.shape
        device = real_sequences.device
        
        # Labels
        real_labels = torch.ones(batch_size, 1, device=device)
        fake_labels = torch.zeros(batch_size, 1, device=device)
        
        # Train Discriminator
        self.optimizer_d.zero_grad()
        
        # Real sequences
        real_pred, real_validity = self.discriminator(real_sequences)
        d_real_loss = self.adversarial_loss(real_pred, real_labels)
        d_real_validity_loss = self.adversarial_loss(real_validity, real_labels)
        
        # Fake sequences
        fake_sequences = self._generate_fake_sequences(batch_size, seq_len, device)
        fake_pred, fake_validity = self.discriminator(fake_sequences.detach())
        d_fake_loss = self.adversarial_loss(fake_pred, fake_labels)
        d_fake_validity_loss = self.adversarial_loss(fake_validity, fake_labels)
        
        d_loss = (d_real_loss + d_fake_loss + d_real_validity_loss + d_fake_validity_loss) / 4
        d_loss.backward()
        self.optimizer_d.step()
        
        # Train Generator
        self.optimizer_g.zero_grad()
        
        # Generate fake sequences
        fake_sequences = self._generate_fake_sequences(batch_size, seq_len, device)
        fake_pred, fake_validity = self.discriminator(fake_sequences)
        
        # Adversarial losses
        g_adv_loss = self.adversarial_loss(fake_pred, real_labels)
        g_validity_loss = self.adversarial_loss(fake_validity, real_labels)
        
        # LaTeX constraint loss (teacher forcing on real data)
        g_logits, _ = self.generator(real_sequences[:, :-1])
        g_latex_loss = self.latex_loss(g_logits.reshape(-1, self.tokenizer.vocab_size), 
                                      real_sequences[:, 1:].reshape(-1))
        
        # Combined generator loss
        g_loss = (self.config.adversarial_weight * (g_adv_loss + g_validity_loss) + 
                 self.config.latex_constraint_weight * g_latex_loss)
        
        g_loss.backward()
        self.optimizer_g.step()
        
        return {
            'discriminator_loss': d_loss.item(),
            'generator_loss': g_loss.item(),
            'latex_constraint_loss': g_latex_loss.item()
        }
    
    def _generate_fake_sequences(self, batch_size: int, seq_len: int, device: torch.device) -> torch.Tensor:
        """Generate fake LaTeX sequences."""
        fake_sequences = []
        
        for _ in range(batch_size):
            latex_expr = self.generator.generate_latex(max_length=seq_len-2, temperature=self.config.temperature)
            token_ids = self.tokenizer.encode(latex_expr, max_length=seq_len)
            fake_sequences.append(token_ids)
        
        return torch.tensor(fake_sequences, dtype=torch.long, device=device)
    
    def generate_new_latex_expressions(self, num_expressions: int = 5, temperature: float = 1.0) -> List[str]:
        """Generate new LaTeX mathematical expressions."""
        expressions = []
        
        for _ in range(num_expressions):
            latex_expr = self.generator.generate_latex(temperature=temperature)
            expressions.append(latex_expr)
        
        return expressions


def create_latex_gan_from_projects(projects_root: str) -> LaTeXGAN:
    """Create and initialize LaTeX GAN from divisor-wave projects."""
    
    print("Loading LaTeX expressions from divisor-wave projects...")
    data_loader = LaTeXDataLoader(projects_root)
    latex_expressions = data_loader.load_from_divisor_wave_projects()
    
    if not latex_expressions:
        print("No LaTeX expressions found, using default mathematical templates.")
        latex_expressions = data_loader._load_custom_mathematical_expressions()
    
    print("Building tokenizer...")
    tokenizer = LaTeXTokenizer()
    tokenizer.build_vocabulary(latex_expressions)
    
    print("Creating LaTeX GAN...")
    config = LaTeXGANConfig(vocab_size=tokenizer.vocab_size)
    latex_gan = LaTeXGAN(config, tokenizer)
    
    print(f"LaTeX GAN created with vocabulary size: {tokenizer.vocab_size}")
    return latex_gan, latex_expressions


# Example usage and integration
if __name__ == "__main__":
    # Create LaTeX GAN from divisor-wave projects
    projects_root = "../../.."  # Adjust path as needed
    latex_gan, training_data = create_latex_gan_from_projects(projects_root)
    
    # Generate some new LaTeX expressions
    new_expressions = latex_gan.generate_new_latex_expressions(num_expressions=5)
    
    print("\nGenerated LaTeX Expressions:")
    for i, expr in enumerate(new_expressions, 1):
        print(f"{i}. {expr}")