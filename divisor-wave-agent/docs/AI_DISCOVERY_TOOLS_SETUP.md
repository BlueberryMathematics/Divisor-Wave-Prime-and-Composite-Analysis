# Enhanced AI Mathematical Discovery Tools - Setup Guide

This guide provides comprehensive setup instructions for the enhanced AI mathematical discovery tools that integrate function similarity checking and uniqueness validation.

## 🎯 Overview

The Enhanced AI Mathematical Discovery Tools combine:
- **Vector-based similarity search** using llama_index and qdrant
- **Multi-method uniqueness validation** with symbolic analysis
- **AI agent integration** for automated mathematical discovery
- **Comprehensive analysis reporting** for human review

## 📋 Prerequisites

### System Requirements
- Python 3.9+
- At least 4GB RAM (8GB recommended for large function databases)
- 2GB free disk space for vector databases

### Required Python Packages

```bash
# Core dependencies
pip install llama-index-core
pip install llama-index-vector-stores-qdrant
pip install llama-index-embeddings-huggingface
pip install qdrant-client
pip install sympy
pip install numpy
pip install scipy

# Optional performance enhancements
pip install torch  # For GPU acceleration
pip install sentence-transformers  # Advanced embeddings
```

## 🔧 Installation Steps

### 1. Install Qdrant Vector Database

#### Option A: Docker Installation (Recommended)
```bash
# Pull and run Qdrant
docker pull qdrant/qdrant
docker run -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage:z qdrant/qdrant
```

#### Option B: Local Installation
```bash
# Install Qdrant locally
pip install qdrant-client[fastembed]
```

### 2. Verify Installation

```python
# Test script: test_installation.py
import asyncio
from enhanced_mathematical_discovery_tools import EnhancedAIMathematicalDiscoveryTools

async def test_installation():
    tools = EnhancedAIMathematicalDiscoveryTools()
    await tools.initialize()
    print("✅ Installation successful!")

if __name__ == "__main__":
    asyncio.run(test_installation())
```

## ⚙️ Configuration

### 1. Qdrant Configuration

Create `config/qdrant_config.yaml`:

```yaml
qdrant:
  host: "localhost"
  port: 6333
  collection_name: "mathematical_functions"
  vector_size: 384  # Matches sentence-transformers model
  distance_metric: "Cosine"
  
embeddings:
  model_name: "sentence-transformers/all-MiniLM-L6-v2"
  max_sequence_length: 512
  
similarity_thresholds:
  exact_match: 0.95
  high_similarity: 0.85
  moderate_similarity: 0.70
  low_similarity: 0.55
```

### 2. Function Database Paths

Create `config/database_paths.yaml`:

```yaml
databases:
  primary_functions: "src/core/custom_functions.json"
  legacy_functions: "src/original_legacy_files/"
  user_functions: "data/user_functions.json"
  ai_generated: "data/ai_generated_functions.json"
  
backup:
  enabled: true
  interval_hours: 24
  max_backups: 7
  backup_directory: "backups/function_databases/"
```

## 🚀 Usage Examples

### Basic Function Validation

```python
import asyncio
from enhanced_mathematical_discovery_tools import AIMathematicalDiscoveryInterface

async def validate_new_function():
    ai_interface = AIMathematicalDiscoveryInterface()
    
    # Define new function
    new_function = {
        'name': 'novel_infinite_product',
        'latex_formula': r'\prod_{n=1}^{\infty} \cos\left(\frac{\pi z}{n^3}\right)',
        'description': 'Infinite product with cubic denominators',
        'category': 'infinite_products',
        'properties': {
            'convergence_type': 'conditional',
            'domain': 'complex_plane',
            'zeros_locations': 'integer_cubes'
        }
    }
    
    # Validate function
    result = await ai_interface.validate_discovered_function(new_function)
    
    print(f"Function: {result['function_name']}")
    print(f"Valid Discovery: {result['is_valid_discovery']}")
    print(f"Novel: {result['novel_discovery']}")
    print(f"Confidence: {result['confidence']:.3f}")
    
    if result['requires_human_review']:
        print("⚠️ Human review recommended")
    
    return result

# Run validation
asyncio.run(validate_new_function())
```

### Batch Analysis

```python
async def batch_validation_example():
    ai_interface = AIMathematicalDiscoveryInterface()
    
    # Multiple functions to validate
    functions = [
        {
            'name': 'function_1',
            'latex_formula': r'\sum_{n=1}^{\infty} \frac{\sin(nz)}{n^2}',
            'description': 'Sine series with quadratic decay',
            'category': 'infinite_series'
        },
        {
            'name': 'function_2', 
            'latex_formula': r'\prod_{p \text{ prime}} \left(1 + \frac{z}{p}\right)',
            'description': 'Euler product over primes',
            'category': 'euler_products'
        }
        # Add more functions...
    ]
    
    # Batch validate
    batch_result = await ai_interface.batch_validate_discoveries(functions)
    
    print(f"📊 BATCH VALIDATION RESULTS:")
    print(f"   Total Analyzed: {batch_result['total_analyzed']}")
    print(f"   Valid Discoveries: {batch_result['valid_discoveries']}")
    print(f"   Novel Discoveries: {batch_result['novel_discoveries']}")
    print(f"   Success Rate: {batch_result['success_rate']:.2%}")
    print(f"   Novelty Rate: {batch_result['novelty_rate']:.2%}")
    
    return batch_result

asyncio.run(batch_validation_example())
```

## 🔍 Advanced Features

### Custom Similarity Thresholds

```python
# Adjust similarity detection sensitivity
from mathematical_function_similarity import AIFunctionSimilarityTool

similarity_tool = AIFunctionSimilarityTool()
similarity_tool.config.update({
    'exact_match_threshold': 0.98,  # Very strict for exact matches
    'high_similarity_threshold': 0.90,  # Stricter high similarity
    'similarity_threshold': 0.75  # Moderate similarity
})
```

### Custom Validation Methods

```python
# Enable/disable specific validation methods
from mathematical_function_validator import AIFunctionValidatorTool

validator = AIFunctionValidatorTool()
validator.config.update({
    'enable_hash_validation': True,
    'enable_latex_normalization': True,
    'enable_symbolic_equivalence': True,
    'enable_structural_analysis': True,
    'enable_property_matching': True
})
```

### Performance Optimization

```python
# Configure for high-performance analysis
config = {
    'batch_size': 100,  # Process functions in batches
    'parallel_workers': 4,  # Parallel processing
    'cache_embeddings': True,  # Cache vector embeddings
    'use_gpu_acceleration': True  # Enable GPU if available
}
```

## 📊 Monitoring and Reporting

### Analysis Reports

The system generates comprehensive reports:

```python
# Generate detailed discovery report
report = await discovery_tools.generate_discovery_report(
    analysis_results, 
    output_path="reports/discovery_analysis_2024.json"
)

# Report includes:
# - Summary statistics
# - Recommendation breakdown  
# - Detailed per-function analysis
# - Confidence scores
# - Similarity analysis results
# - Validation method results
```

### Real-time Monitoring

```python
# Monitor discovery tool performance
async def monitor_discovery_tools():
    tools = EnhancedAIMathematicalDiscoveryTools()
    
    # Performance metrics
    start_time = time.time()
    
    # Your analysis here...
    result = await tools.comprehensive_function_analysis(function_data)
    
    analysis_time = time.time() - start_time
    print(f"⏱️ Analysis completed in {analysis_time:.2f} seconds")
    print(f"🎯 Confidence: {result.confidence_score:.3f}")
    print(f"📊 Recommendation: {result.final_recommendation}")
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Qdrant Connection Issues
```bash
# Check if Qdrant is running
curl http://localhost:6333/health

# Restart Qdrant if needed
docker restart qdrant_container
```

#### 2. Memory Issues with Large Databases
```python
# Reduce batch size for large datasets
config = {
    'batch_size': 50,  # Smaller batches
    'max_memory_usage': '4GB',
    'enable_streaming': True
}
```

#### 3. Slow Similarity Search
```python
# Optimize embedding model
similarity_tool.config.update({
    'embedding_model': 'sentence-transformers/all-MiniLM-L6-v2',  # Faster model
    'embedding_cache_size': 10000,
    'use_approximate_search': True
})
```

### Debug Mode

```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with debug information
tools = EnhancedAIMathematicalDiscoveryTools()
tools.debug_mode = True
```

## 📈 Performance Benchmarks

Expected performance on standard hardware:

| Operation | Time (single) | Time (batch 100) | Memory Usage |
|-----------|---------------|------------------|--------------|
| Similarity Check | 50-200ms | 5-15s | 200-500MB |
| Uniqueness Validation | 10-50ms | 1-5s | 100-300MB |
| Combined Analysis | 100-300ms | 10-25s | 400-800MB |

## 🔧 Maintenance

### Regular Maintenance Tasks

1. **Update Vector Database**
```bash
# Weekly update of function embeddings
python scripts/update_vector_database.py --full-rebuild
```

2. **Backup Function Databases**
```bash
# Daily backup of all function databases
python scripts/backup_databases.py --include-vectors
```

3. **Performance Monitoring**
```bash
# Monitor system performance
python scripts/performance_monitor.py --duration 24h
```

### Database Optimization

```python
# Optimize vector database performance
async def optimize_vector_database():
    from qdrant_client import QdrantClient
    
    client = QdrantClient("localhost", port=6333)
    
    # Optimize collection
    client.update_collection(
        collection_name="mathematical_functions",
        optimizer_config=models.OptimizersConfigDiff(
            default_segment_number=2,
            max_segment_size=20000,
            memmap_threshold=20000,
        )
    )
```

## 🔄 Integration with AI Agents

### Agent Integration Example

```python
class MathematicalDiscoveryAgent:
    def __init__(self):
        self.discovery_tools = AIMathematicalDiscoveryInterface()
    
    async def discover_and_validate_function(self, generation_params):
        # Step 1: Generate new function (your AI logic here)
        new_function = await self.generate_function(generation_params)
        
        # Step 2: Validate with discovery tools
        validation_result = await self.discovery_tools.validate_discovered_function(new_function)
        
        # Step 3: Make decision based on result
        if validation_result['is_valid_discovery']:
            if validation_result['novel_discovery']:
                print("🚀 Novel mathematical discovery confirmed!")
                await self.register_new_function(new_function)
            else:
                print("✅ Valid but existing function found")
        else:
            print("❌ Function rejected - duplicate or invalid")
        
        return validation_result
```

## 🎯 Next Steps

After successful setup:

1. **Test with sample functions** from your existing database
2. **Configure similarity thresholds** based on your domain requirements  
3. **Integrate with your AI agents** using the provided interfaces
4. **Set up monitoring and reporting** for production use
5. **Scale up** vector database for large-scale discovery

For additional support, refer to the main documentation in the `docs/` directory or check the integration examples in `examples/`.

---

**Enhanced AI Mathematical Discovery Tools v1.0**  
*Empowering mathematical discovery through AI-assisted validation*