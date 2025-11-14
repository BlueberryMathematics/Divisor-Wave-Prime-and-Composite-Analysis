"""
Embedding Models Package
========================

Embedding module for the divisor wave neural networks library.
"""

from .crystal_embeddings import (
    CrystalEmbedding,
    CrystalEmbeddingConfig,
    CrystalSequence,
    IcosahedronProjection,
    SierpinskiCircletTransformer,
    CrystalLatticeType,
    CrystalSymmetryGroup,
    create_icosahedral_embedding,
    create_tetrahedral_embedding,
)

from .tetrahedral_embeddings import (
    TetrahedralEmbedding,
    TetrahedralEmbeddingConfig,
    TetrahedralSpace,
)

from .sequence_embeddings import (
    SequenceEmbedding,
    SequenceEmbeddingConfig,
    MathematicalSequenceEncoder,
)

__all__ = [
    # Crystal embeddings
    "CrystalEmbedding",
    "CrystalEmbeddingConfig",
    "CrystalSequence",
    "IcosahedronProjection", 
    "SierpinskiCircletTransformer",
    "CrystalLatticeType",
    "CrystalSymmetryGroup",
    
    # Tetrahedral embeddings
    "TetrahedralEmbedding",
    "TetrahedralEmbeddingConfig",
    "TetrahedralSpace",
    
    # Sequence embeddings
    "SequenceEmbedding",
    "SequenceEmbeddingConfig",
    "MathematicalSequenceEncoder",
    
    # Factory functions
    "create_icosahedral_embedding",
    "create_tetrahedral_embedding",
]