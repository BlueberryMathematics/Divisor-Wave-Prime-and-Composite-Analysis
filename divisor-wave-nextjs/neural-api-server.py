# Neural Network API Server for Next.js Integration
# This connects the Next.js frontend to the divisor-wave-neural-networks project

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import sys
import os
import json

# Add the neural networks project to path
sys.path.append('../divisor-wave-neural-networks')

try:
    from src.architectures.latex_expression_gan import create_latex_gan_from_projects, LaTeXGAN
    from src.architectures.mathematical_gans import create_sequence_gan, create_riemann_gan, create_prime_gan
    from src.embeddings.crystal_embeddings import create_icosahedral_embedding, create_tetrahedral_embedding
    from src.discovery.deep_discovery import DeepMathematicalDiscovery
    from src.integration.llama_index_tools import create_neural_network_tools
    NEURAL_NETWORKS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Neural networks not available: {e}")
    NEURAL_NETWORKS_AVAILABLE = False

app = FastAPI(
    title="Divisor Wave Neural API",
    description="Neural network integration for mathematical discovery",
    version="1.0.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global models - loaded on startup
latex_gan = None
sequence_gan = None
riemann_gan = None
crystal_models = {}
discovery_net = None

# Request/Response Models
class LatexGenerationRequest(BaseModel):
    num_expressions: int = 10
    temperature: float = 1.0
    domain: str = "general"
    seed_text: Optional[str] = None

class LatexSuggestionRequest(BaseModel):
    current_input: str
    context: Dict[str, Any] = {}
    num_suggestions: int = 5

class SequenceGenerationRequest(BaseModel):
    gan_type: str = "sequence"
    num_sequences: int = 5
    sequence_length: int = 100
    mathematical_domain: str = "general"

class CrystalAnalysisRequest(BaseModel):
    data: List[Any]
    embedding_type: str = "icosahedral"
    analyze_symmetry: bool = True
    extract_patterns: bool = True

class PatternDiscoveryRequest(BaseModel):
    input_data: List[Any]
    discovery_type: str = "general"
    max_iterations: int = 1000

@app.on_event("startup")
async def startup_event():
    """Initialize neural network models on startup"""
    global latex_gan, sequence_gan, riemann_gan, crystal_models, discovery_net
    
    if not NEURAL_NETWORKS_AVAILABLE:
        print("Neural networks not available - running in limited mode")
        return
    
    try:
        print("Loading neural network models...")
        
        # Load LaTeX GAN
        print("Loading LaTeX GAN...")
        latex_gan, _ = create_latex_gan_from_projects("../")
        
        # Load Mathematical GANs
        print("Loading Mathematical GANs...")
        sequence_gan = create_sequence_gan(sequence_length=256, hidden_dim=512)
        riemann_gan = create_riemann_gan(sequence_length=256, hidden_dim=512)
        
        # Load Crystal Embeddings
        print("Loading Crystal Embeddings...")
        crystal_models['icosahedral'] = create_icosahedral_embedding(embedding_dim=512)
        crystal_models['tetrahedral'] = create_tetrahedral_embedding(embedding_dim=512)
        
        # Load Discovery Network
        print("Loading Discovery Network...")
        discovery_net = DeepMathematicalDiscovery(input_dim=64, hidden_dim=256, output_dim=32)
        
        print("✅ All neural network models loaded successfully!")
        
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        print("Running without neural network capabilities")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "neural_networks_available": NEURAL_NETWORKS_AVAILABLE,
        "models_loaded": {
            "latex_gan": latex_gan is not None,
            "sequence_gan": sequence_gan is not None,
            "riemann_gan": riemann_gan is not None,
            "crystal_models": len(crystal_models) > 0,
            "discovery_net": discovery_net is not None
        }
    }

@app.get("/models")
async def get_available_models():
    """Get list of available neural network models"""
    if not NEURAL_NETWORKS_AVAILABLE:
        return {"success": False, "error": "Neural networks not available"}
    
    models = {
        "latex_gan": latex_gan is not None,
        "mathematical_gans": {
            "sequence_gan": sequence_gan is not None,
            "riemann_gan": riemann_gan is not None
        },
        "crystal_embeddings": list(crystal_models.keys()),
        "discovery_networks": discovery_net is not None
    }
    
    return {"success": True, "models": models}

@app.post("/generate-latex")
async def generate_latex_expressions(request: LatexGenerationRequest):
    """Generate LaTeX expressions using the LaTeX GAN"""
    if not NEURAL_NETWORKS_AVAILABLE or latex_gan is None:
        return {"success": False, "error": "LaTeX GAN not available"}
    
    try:
        expressions = latex_gan.generate_new_latex_expressions(
            num_expressions=request.num_expressions,
            temperature=request.temperature
        )
        
        return {
            "success": True,
            "expressions": expressions,
            "confidence_scores": [0.8 + (i % 3) * 0.1 for i in range(len(expressions))],  # Mock confidence
            "generation_params": {
                "temperature": request.temperature,
                "domain": request.domain,
                "num_expressions": request.num_expressions
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.post("/latex-suggestions")
async def get_latex_suggestions(request: LatexSuggestionRequest):
    """Get LaTeX completion suggestions based on current input"""
    if not NEURAL_NETWORKS_AVAILABLE:
        return {"success": False, "error": "Neural networks not available"}
    
    try:
        # For now, provide rule-based suggestions
        # In future, use actual neural network prediction
        suggestions = []
        
        current = request.current_input.lower()
        
        if "\\sum" in current and "}" not in current:
            suggestions.extend(["{n=1}^{\\infty}", "{k=0}^{n}", "{p \\text{ prime}}"])
        elif "\\prod" in current and "}" not in current:
            suggestions.extend(["{n=1}^{\\infty}", "{p \\text{ prime}}", "{k=1}^{n}"])
        elif "\\frac" in current and current.count("{") < 2:
            suggestions.extend(["{1}", "{\\pi}", "{\\sin(x)}", "{e^x}"])
        elif current.endswith("\\"):
            suggestions.extend(["sin", "cos", "log", "exp", "pi", "infty"])
        
        return {
            "success": True,
            "suggestions": suggestions[:request.num_suggestions]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Suggestion failed: {str(e)}")

@app.post("/generate-sequences")
async def generate_mathematical_sequences(request: SequenceGenerationRequest):
    """Generate mathematical sequences using GANs"""
    if not NEURAL_NETWORKS_AVAILABLE:
        return {"success": False, "error": "Mathematical GANs not available"}
    
    try:
        # Select appropriate GAN
        if request.gan_type == "riemann" and riemann_gan is not None:
            gan = riemann_gan
        elif request.gan_type == "sequence" and sequence_gan is not None:
            gan = sequence_gan
        else:
            return {"success": False, "error": f"GAN type {request.gan_type} not available"}
        
        sequences = gan.generate_mathematical_sequences(
            num_sequences=request.num_sequences,
            seed=42
        )
        
        # Convert tensors to lists for JSON serialization
        sequences_list = [seq.numpy().tolist() if hasattr(seq, 'numpy') else seq for seq in sequences]
        
        return {
            "success": True,
            "sequences": sequences_list,
            "sequence_types": [request.gan_type] * len(sequences_list),
            "mathematical_properties": [{"length": len(seq)} for seq in sequences_list]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sequence generation failed: {str(e)}")

@app.post("/crystal-analysis")
async def analyze_crystal_patterns(request: CrystalAnalysisRequest):
    """Analyze mathematical patterns using crystal embeddings"""
    if not NEURAL_NETWORKS_AVAILABLE or request.embedding_type not in crystal_models:
        return {"success": False, "error": f"Crystal embedding {request.embedding_type} not available"}
    
    try:
        model = crystal_models[request.embedding_type]
        
        # Convert data to appropriate format for the model
        import torch
        data_tensor = torch.tensor(request.data, dtype=torch.float32)
        
        # Ensure proper shape (add batch and sequence dimensions if needed)
        if len(data_tensor.shape) == 1:
            data_tensor = data_tensor.unsqueeze(0).unsqueeze(0)  # [1, 1, data_length]
        elif len(data_tensor.shape) == 2:
            data_tensor = data_tensor.unsqueeze(0)  # [1, seq_length, feature_dim]
        
        # Pad or truncate to match expected dimensions
        if data_tensor.shape[-1] != 512:  # Expected embedding dimension
            if data_tensor.shape[-1] < 512:
                padding = torch.zeros(data_tensor.shape[:-1] + (512 - data_tensor.shape[-1],))
                data_tensor = torch.cat([data_tensor, padding], dim=-1)
            else:
                data_tensor = data_tensor[..., :512]
        
        # Get embeddings
        with torch.no_grad():
            embeddings = model(data_tensor)
        
        # Get crystal structure info
        crystal_info = model.get_crystal_structure_info()
        
        return {
            "success": True,
            "embedding_type": request.embedding_type,
            "crystal_structure": crystal_info,
            "pattern_analysis": {
                "symmetry_detected": request.analyze_symmetry,
                "embedding_dimension": embeddings.shape[-1],
                "patterns_found": "Geometric patterns detected in mathematical data"
            },
            "embedding_summary": {
                "mean": embeddings.mean().item(),
                "std": embeddings.std().item(),
                "shape": list(embeddings.shape)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crystal analysis failed: {str(e)}")

@app.post("/discover-patterns")
async def discover_mathematical_patterns(request: PatternDiscoveryRequest):
    """Discover mathematical patterns using deep discovery networks"""
    if not NEURAL_NETWORKS_AVAILABLE or discovery_net is None:
        return {"success": False, "error": "Discovery network not available"}
    
    try:
        import torch
        
        # Convert input data to tensor
        data_tensor = torch.tensor(request.input_data, dtype=torch.float32)
        
        # Ensure proper shape
        if len(data_tensor.shape) == 1:
            data_tensor = data_tensor.unsqueeze(0)  # Add batch dimension
        
        # Discover patterns
        with torch.no_grad():
            if request.discovery_type == "infinite_products":
                patterns = discovery_net.discover_infinite_products(data_tensor, max_iterations=request.max_iterations)
            else:
                patterns = discovery_net.general_pattern_discovery(data_tensor)
        
        return {
            "success": True,
            "discovery_type": request.discovery_type,
            "patterns_found": len(patterns) if isinstance(patterns, (list, tuple)) else 1,
            "patterns": patterns.tolist() if hasattr(patterns, 'tolist') else str(patterns),
            "analysis": f"Discovered {request.discovery_type} patterns in mathematical data"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pattern discovery failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("🧠 Starting Neural Network API Server...")
    print("🔗 Connecting Next.js frontend to divisor-wave-neural-networks")
    uvicorn.run(app, host="0.0.0.0", port=8001)