"""
Mathematical Function Similarity Search System
Advanced AI tool for checking function uniqueness and similarity based on LaTeX formulas

This system prevents duplicate discoveries and identifies related mathematical patterns
using vector embeddings, hybrid search, and mathematical similarity metrics.
"""

import os
import sys
import json
import hashlib
import asyncio
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
from datetime import datetime

# Add project paths
current_dir = Path(__file__).parent.parent.parent
sys.path.append(str(current_dir / "divisor-wave-python" / "src"))

try:
    from llama_index.core import VectorStoreIndex, StorageContext, Document
    from llama_index.core import Settings
    from llama_index.vector_stores.qdrant import QdrantVectorStore
    from qdrant_client import QdrantClient, AsyncQdrantClient
    from qdrant_client.models import Distance, VectorParams, PointStruct
    VECTOR_SEARCH_AVAILABLE = True
except ImportError:
    print("⚠️ Vector search libraries not available. Install: pip install llama-index qdrant-client")
    VECTOR_SEARCH_AVAILABLE = False

try:
    import sympy as sp
    from sympy.parsing.latex import parse_latex
    SYMPY_AVAILABLE = True
except ImportError:
    print("⚠️ SymPy not available for mathematical parsing")
    SYMPY_AVAILABLE = False

from core.function_registry import get_registry
from core.latex_function_builder import LaTeXFunctionBuilder


class MathematicalFunctionSimilarity:
    """
    AI tool for mathematical function similarity search and duplicate detection.
    
    Features:
    - LaTeX formula vector embeddings
    - Hybrid search (semantic + keyword)
    - Mathematical structure analysis
    - Duplicate detection with confidence scores
    - Pattern similarity identification
    """
    
    def __init__(self, qdrant_host="localhost", qdrant_port=6333):
        self.qdrant_host = qdrant_host
        self.qdrant_port = qdrant_port
        self.collection_name = "mathematical_functions"
        
        # Initialize components
        self.function_registry = get_registry()
        self.latex_builder = LaTeXFunctionBuilder()
        
        # Initialize vector store if available
        if VECTOR_SEARCH_AVAILABLE:
            self.client = QdrantClient(host=qdrant_host, port=qdrant_port)
            self.aclient = AsyncQdrantClient(host=qdrant_host, port=qdrant_port)
            self._initialize_vector_store()
        else:
            self.client = None
            self.aclient = None
            print("⚠️ Vector search disabled - using fallback similarity methods")
    
    def _initialize_vector_store(self):
        """Initialize Qdrant vector store for mathematical functions"""
        
        try:
            # Create vector store with hybrid indexing
            self.vector_store = QdrantVectorStore(
                collection_name=self.collection_name,
                client=self.client,
                aclient=self.aclient,
                enable_hybrid=True,
                fastembed_sparse_model="Qdrant/bm25",
                batch_size=20,
            )
            
            # Configure LlamaIndex settings
            Settings.chunk_size = 512
            
            # Create storage context
            self.storage_context = StorageContext.from_defaults(
                vector_store=self.vector_store
            )
            
            print("✅ Vector store initialized successfully")
            
        except Exception as e:
            print(f"⚠️ Vector store initialization failed: {e}")
            self.vector_store = None
            self.storage_context = None
    
    async def index_existing_functions(self):
        """Index all existing functions in the registry for similarity search"""
        
        if not VECTOR_SEARCH_AVAILABLE or not self.vector_store:
            print("⚠️ Vector search not available - skipping indexing")
            return
        
        print("🔄 Indexing existing mathematical functions...")
        
        # Get all functions from registry
        all_functions = self.function_registry.get_all_functions()
        
        # Create documents for indexing
        documents = []
        
        for func_id, func_data in all_functions.items():
            
            # Create rich document content
            content = self._create_function_document_content(func_data)
            
            # Create LlamaIndex document
            doc = Document(
                text=content,
                metadata={
                    'function_id': func_id,
                    'name': func_data.get('name', ''),
                    'category': func_data.get('category', ''),
                    'latex_formula': func_data.get('latex_formula', ''),
                    'hash': func_data.get('hash', ''),
                    'indexed_date': datetime.now().isoformat()
                }
            )
            
            documents.append(doc)
        
        # Create or update index
        try:
            self.index = VectorStoreIndex.from_documents(
                documents,
                storage_context=self.storage_context,
            )
            
            # Create query engine
            self.query_engine = self.index.as_query_engine(
                similarity_top_k=5,
                sparse_top_k=15,
                vector_store_query_mode="hybrid"
            )
            
            print(f"✅ Indexed {len(documents)} mathematical functions")
            
        except Exception as e:
            print(f"❌ Function indexing failed: {e}")
            self.index = None
            self.query_engine = None
    
    def _create_function_document_content(self, func_data: Dict) -> str:
        """Create rich document content for vector indexing"""
        
        content_parts = []
        
        # Function name and description
        if 'name' in func_data:
            content_parts.append(f"Function name: {func_data['name']}")
        
        if 'description' in func_data:
            content_parts.append(f"Description: {func_data['description']}")
        
        # LaTeX formula
        if 'latex_formula' in func_data:
            content_parts.append(f"LaTeX formula: {func_data['latex_formula']}")
        
        # Mathematical properties
        if 'properties' in func_data:
            properties = func_data['properties']
            if isinstance(properties, dict):
                for key, value in properties.items():
                    content_parts.append(f"{key}: {value}")
        
        # Category and tags
        if 'category' in func_data:
            content_parts.append(f"Category: {func_data['category']}")
        
        # Mathematical structure keywords
        latex_formula = func_data.get('latex_formula', '')
        structure_keywords = self._extract_mathematical_keywords(latex_formula)
        if structure_keywords:
            content_parts.append(f"Mathematical structures: {', '.join(structure_keywords)}")
        
        return " | ".join(content_parts)
    
    def _extract_mathematical_keywords(self, latex_formula: str) -> List[str]:
        """Extract mathematical structure keywords from LaTeX formula"""
        
        keywords = []
        
        # Common mathematical structures
        structure_patterns = {
            'infinite_product': ['prod', 'infty'],
            'infinite_sum': ['sum', 'infty'],
            'trigonometric': ['sin', 'cos', 'tan'],
            'exponential': ['exp', 'e^'],
            'logarithmic': ['log', 'ln'],
            'gamma_function': ['Gamma', 'gamma'],
            'zeta_function': ['zeta', 'eta'],
            'factorial': ['!', 'factorial'],
            'complex_analysis': ['z', 'complex'],
            'prime_related': ['prime', 'p_n'],
            'divisor': ['divisor', 'd(n)'],
            'harmonic': ['harmonic', 'H_n']
        }
        
        latex_lower = latex_formula.lower()
        
        for keyword, patterns in structure_patterns.items():
            if any(pattern in latex_lower for pattern in patterns):
                keywords.append(keyword)
        
        return keywords
    
    async def check_function_similarity(self, 
                                      new_function_data: Dict,
                                      similarity_threshold: float = 0.8) -> Dict:
        """
        Check if a new function is similar to existing functions
        
        Args:
            new_function_data: Dictionary containing function data
            similarity_threshold: Threshold for similarity detection (0.0-1.0)
            
        Returns:
            Dictionary with similarity results
        """
        
        similarity_results = {
            'is_duplicate': False,
            'is_similar': False,
            'similarity_score': 0.0,
            'similar_functions': [],
            'analysis_method': 'hybrid',
            'recommendations': []
        }
        
        # Method 1: Vector similarity search (if available)
        if VECTOR_SEARCH_AVAILABLE and hasattr(self, 'query_engine') and self.query_engine:
            vector_results = await self._vector_similarity_search(new_function_data)
            similarity_results.update(vector_results)
        
        # Method 2: Hash-based duplicate detection
        hash_results = await self._hash_based_duplicate_check(new_function_data)
        if hash_results['is_duplicate']:
            similarity_results.update(hash_results)
            similarity_results['analysis_method'] = 'hash_exact'
            return similarity_results
        
        # Method 3: LaTeX structure similarity (fallback)
        if not similarity_results['is_similar']:
            latex_results = await self._latex_structure_similarity(new_function_data)
            if latex_results['similarity_score'] > similarity_results['similarity_score']:
                similarity_results.update(latex_results)
                similarity_results['analysis_method'] = 'latex_structure'
        
        # Method 4: Mathematical symbol analysis
        symbol_results = await self._mathematical_symbol_analysis(new_function_data)
        if symbol_results['similarity_score'] > similarity_results['similarity_score']:
            similarity_results.update(symbol_results)
            similarity_results['analysis_method'] = 'mathematical_symbols'
        
        # Generate recommendations
        similarity_results['recommendations'] = self._generate_similarity_recommendations(
            similarity_results
        )
        
        return similarity_results
    
    async def _vector_similarity_search(self, new_function_data: Dict) -> Dict:
        """Perform vector-based similarity search"""
        
        try:
            # Create query from function data
            query_content = self._create_function_document_content(new_function_data)
            
            # Perform hybrid search
            response = self.query_engine.query(query_content)
            
            # Parse results
            similar_functions = []
            max_similarity = 0.0
            
            # Extract similarity information from response
            if hasattr(response, 'source_nodes'):
                for node in response.source_nodes:
                    similarity_score = getattr(node, 'score', 0.0)
                    metadata = node.metadata
                    
                    similar_functions.append({
                        'function_id': metadata.get('function_id'),
                        'name': metadata.get('name'),
                        'similarity_score': similarity_score,
                        'latex_formula': metadata.get('latex_formula'),
                        'match_type': 'vector_similarity'
                    })
                    
                    max_similarity = max(max_similarity, similarity_score)
            
            return {
                'is_similar': max_similarity > 0.7,
                'similarity_score': max_similarity,
                'similar_functions': similar_functions[:5],  # Top 5 matches
                'search_method': 'vector_hybrid'
            }
            
        except Exception as e:
            print(f"⚠️ Vector similarity search failed: {e}")
            return {'is_similar': False, 'similarity_score': 0.0, 'similar_functions': []}
    
    async def _hash_based_duplicate_check(self, new_function_data: Dict) -> Dict:
        """Check for exact duplicates using hash comparison"""
        
        # Generate hash for new function
        new_latex = new_function_data.get('latex_formula', '')
        new_hash = self._generate_latex_hash(new_latex)
        
        # Check against existing functions
        all_functions = self.function_registry.get_all_functions()
        
        for func_id, func_data in all_functions.items():
            existing_hash = func_data.get('hash', '')
            
            if new_hash == existing_hash and existing_hash != '':
                return {
                    'is_duplicate': True,
                    'is_similar': True,
                    'similarity_score': 1.0,
                    'similar_functions': [{
                        'function_id': func_id,
                        'name': func_data.get('name', ''),
                        'similarity_score': 1.0,
                        'latex_formula': func_data.get('latex_formula', ''),
                        'match_type': 'exact_duplicate'
                    }]
                }
        
        return {'is_duplicate': False}
    
    async def _latex_structure_similarity(self, new_function_data: Dict) -> Dict:
        """Analyze LaTeX structure similarity"""
        
        new_latex = new_function_data.get('latex_formula', '')
        if not new_latex:
            return {'is_similar': False, 'similarity_score': 0.0, 'similar_functions': []}
        
        # Get structure components
        new_structure = self._analyze_latex_structure(new_latex)
        
        similar_functions = []
        all_functions = self.function_registry.get_all_functions()
        
        for func_id, func_data in all_functions.items():
            existing_latex = func_data.get('latex_formula', '')
            if not existing_latex:
                continue
            
            existing_structure = self._analyze_latex_structure(existing_latex)
            
            # Calculate structure similarity
            similarity_score = self._calculate_structure_similarity(
                new_structure, existing_structure
            )
            
            if similarity_score > 0.5:  # Reasonable similarity threshold
                similar_functions.append({
                    'function_id': func_id,
                    'name': func_data.get('name', ''),
                    'similarity_score': similarity_score,
                    'latex_formula': existing_latex,
                    'match_type': 'structure_similarity'
                })
        
        # Sort by similarity score
        similar_functions.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        max_similarity = similar_functions[0]['similarity_score'] if similar_functions else 0.0
        
        return {
            'is_similar': max_similarity > 0.7,
            'similarity_score': max_similarity,
            'similar_functions': similar_functions[:5]
        }
    
    def _analyze_latex_structure(self, latex_formula: str) -> Dict:
        """Analyze the mathematical structure of a LaTeX formula"""
        
        structure = {
            'operators': [],
            'functions': [],
            'symbols': [],
            'structures': [],
            'complexity_score': 0
        }
        
        latex_lower = latex_formula.lower()
        
        # Detect mathematical operators
        operators = ['\\sum', '\\prod', '\\int', '\\frac', '\\sqrt', '^', '_']
        for op in operators:
            if op in latex_lower:
                structure['operators'].append(op)
        
        # Detect mathematical functions
        functions = ['\\sin', '\\cos', '\\tan', '\\exp', '\\log', '\\ln', '\\gamma']
        for func in functions:
            if func in latex_lower:
                structure['functions'].append(func)
        
        # Detect special symbols
        symbols = ['\\pi', '\\infty', '\\zeta', '\\eta', '\\alpha', '\\beta', '\\gamma']
        for symbol in symbols:
            if symbol in latex_lower:
                structure['symbols'].append(symbol)
        
        # Detect structural patterns
        if '\\prod' in latex_lower and '\\infty' in latex_lower:
            structure['structures'].append('infinite_product')
        if '\\sum' in latex_lower and '\\infty' in latex_lower:
            structure['structures'].append('infinite_sum')
        if any(trig in latex_lower for trig in ['\\sin', '\\cos', '\\tan']):
            structure['structures'].append('trigonometric')
        
        # Calculate complexity score
        structure['complexity_score'] = (
            len(structure['operators']) * 2 +
            len(structure['functions']) * 3 +
            len(structure['symbols']) * 1 +
            len(structure['structures']) * 4
        )
        
        return structure
    
    def _calculate_structure_similarity(self, struct1: Dict, struct2: Dict) -> float:
        """Calculate similarity between two mathematical structures"""
        
        total_similarity = 0.0
        weight_sum = 0.0
        
        # Compare operators (weight: 3)
        if struct1['operators'] or struct2['operators']:
            op_similarity = self._calculate_list_similarity(
                struct1['operators'], struct2['operators']
            )
            total_similarity += op_similarity * 3
            weight_sum += 3
        
        # Compare functions (weight: 4)
        if struct1['functions'] or struct2['functions']:
            func_similarity = self._calculate_list_similarity(
                struct1['functions'], struct2['functions']
            )
            total_similarity += func_similarity * 4
            weight_sum += 4
        
        # Compare symbols (weight: 2)
        if struct1['symbols'] or struct2['symbols']:
            symbol_similarity = self._calculate_list_similarity(
                struct1['symbols'], struct2['symbols']
            )
            total_similarity += symbol_similarity * 2
            weight_sum += 2
        
        # Compare structures (weight: 5)
        if struct1['structures'] or struct2['structures']:
            structure_similarity = self._calculate_list_similarity(
                struct1['structures'], struct2['structures']
            )
            total_similarity += structure_similarity * 5
            weight_sum += 5
        
        return total_similarity / weight_sum if weight_sum > 0 else 0.0
    
    def _calculate_list_similarity(self, list1: List, list2: List) -> float:
        """Calculate Jaccard similarity between two lists"""
        
        set1 = set(list1)
        set2 = set(list2)
        
        if not set1 and not set2:
            return 1.0
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0
    
    async def _mathematical_symbol_analysis(self, new_function_data: Dict) -> Dict:
        """Analyze mathematical symbols and patterns"""
        
        if not SYMPY_AVAILABLE:
            return {'is_similar': False, 'similarity_score': 0.0, 'similar_functions': []}
        
        new_latex = new_function_data.get('latex_formula', '')
        
        try:
            # Parse LaTeX with SymPy
            new_expr = parse_latex(new_latex)
            new_symbols = list(new_expr.free_symbols)
            new_atoms = new_expr.atoms()
            
            similar_functions = []
            all_functions = self.function_registry.get_all_functions()
            
            for func_id, func_data in all_functions.items():
                existing_latex = func_data.get('latex_formula', '')
                if not existing_latex:
                    continue
                
                try:
                    existing_expr = parse_latex(existing_latex)
                    existing_symbols = list(existing_expr.free_symbols)
                    existing_atoms = existing_expr.atoms()
                    
                    # Calculate symbol similarity
                    symbol_similarity = self._calculate_symbol_similarity(
                        new_symbols, existing_symbols
                    )
                    
                    # Calculate atomic structure similarity
                    atom_similarity = self._calculate_atom_similarity(
                        new_atoms, existing_atoms
                    )
                    
                    # Combined similarity
                    combined_similarity = (symbol_similarity + atom_similarity) / 2
                    
                    if combined_similarity > 0.4:
                        similar_functions.append({
                            'function_id': func_id,
                            'name': func_data.get('name', ''),
                            'similarity_score': combined_similarity,
                            'latex_formula': existing_latex,
                            'match_type': 'mathematical_symbols'
                        })
                
                except Exception:
                    continue  # Skip functions that can't be parsed
            
            # Sort by similarity
            similar_functions.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            max_similarity = similar_functions[0]['similarity_score'] if similar_functions else 0.0
            
            return {
                'is_similar': max_similarity > 0.6,
                'similarity_score': max_similarity,
                'similar_functions': similar_functions[:5]
            }
            
        except Exception as e:
            print(f"⚠️ Mathematical symbol analysis failed: {e}")
            return {'is_similar': False, 'similarity_score': 0.0, 'similar_functions': []}
    
    def _calculate_symbol_similarity(self, symbols1: List, symbols2: List) -> float:
        """Calculate similarity between symbol sets"""
        
        if not symbols1 and not symbols2:
            return 1.0
        
        symbol_names1 = {str(s) for s in symbols1}
        symbol_names2 = {str(s) for s in symbols2}
        
        intersection = len(symbol_names1.intersection(symbol_names2))
        union = len(symbol_names1.union(symbol_names2))
        
        return intersection / union if union > 0 else 0.0
    
    def _calculate_atom_similarity(self, atoms1: set, atoms2: set) -> float:
        """Calculate similarity between atomic structures"""
        
        if not atoms1 and not atoms2:
            return 1.0
        
        # Convert atoms to comparable format
        atom_types1 = {type(atom).__name__ for atom in atoms1}
        atom_types2 = {type(atom).__name__ for atom in atoms2}
        
        intersection = len(atom_types1.intersection(atom_types2))
        union = len(atom_types1.union(atom_types2))
        
        return intersection / union if union > 0 else 0.0
    
    def _generate_latex_hash(self, latex_formula: str) -> str:
        """Generate a normalized hash for LaTeX formula"""
        
        # Normalize LaTeX formula
        normalized = latex_formula.strip().lower()
        normalized = ' '.join(normalized.split())  # Normalize whitespace
        
        # Generate SHA-256 hash
        return hashlib.sha256(normalized.encode()).hexdigest()[:8]
    
    def _generate_similarity_recommendations(self, results: Dict) -> List[str]:
        """Generate recommendations based on similarity analysis"""
        
        recommendations = []
        
        if results['is_duplicate']:
            recommendations.append("⚠️ DUPLICATE DETECTED: This function already exists in the registry")
            recommendations.append("🔍 Review the existing function before proceeding")
        
        elif results['is_similar']:
            recommendations.append(f"⚠️ SIMILAR FUNCTION FOUND: {results['similarity_score']:.2f} similarity")
            recommendations.append("🔍 Consider if this is a meaningful variation or extension")
            
            if results['similar_functions']:
                top_match = results['similar_functions'][0]
                recommendations.append(f"📊 Most similar: {top_match['name']} (ID: {top_match['function_id']})")
        
        else:
            recommendations.append("✅ NOVEL FUNCTION: No significant similarity detected")
            recommendations.append("🚀 This appears to be a unique mathematical discovery")
        
        # Analysis method info
        recommendations.append(f"🔬 Analysis method: {results['analysis_method']}")
        
        return recommendations
    
    async def batch_similarity_check(self, new_functions: List[Dict]) -> List[Dict]:
        """Check similarity for multiple functions in batch"""
        
        results = []
        
        for i, func_data in enumerate(new_functions):
            print(f"🔍 Checking similarity for function {i+1}/{len(new_functions)}")
            
            similarity_result = await self.check_function_similarity(func_data)
            similarity_result['function_data'] = func_data
            
            results.append(similarity_result)
        
        return results
    
    async def export_similarity_report(self, results: List[Dict], output_path: str):
        """Export similarity analysis results to JSON report"""
        
        report = {
            'analysis_date': datetime.now().isoformat(),
            'total_functions_checked': len(results),
            'duplicates_found': len([r for r in results if r['is_duplicate']]),
            'similar_functions_found': len([r for r in results if r['is_similar']]),
            'novel_functions': len([r for r in results if not r['is_similar']]),
            'results': results
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Similarity report exported to: {output_path}")


# AI Tool Interface for Integration
class AIFunctionSimilarityTool:
    """
    AI tool interface for mathematical function similarity checking.
    Designed for integration with AI agents.
    """
    
    def __init__(self):
        self.similarity_checker = MathematicalFunctionSimilarity()
        self.initialized = False
    
    async def initialize(self):
        """Initialize the similarity checker with existing functions"""
        
        if not self.initialized:
            await self.similarity_checker.index_existing_functions()
            self.initialized = True
            print("✅ AI Function Similarity Tool initialized")
    
    async def check_new_function(self, function_data: Dict) -> Dict:
        """
        AI tool interface for checking new function similarity
        
        Args:
            function_data: Dictionary with keys: name, latex_formula, description, category
            
        Returns:
            Dictionary with similarity analysis results
        """
        
        if not self.initialized:
            await self.initialize()
        
        results = await self.similarity_checker.check_function_similarity(function_data)
        
        # Format results for AI consumption
        ai_results = {
            'status': 'duplicate' if results['is_duplicate'] else 'similar' if results['is_similar'] else 'novel',
            'confidence': results['similarity_score'],
            'analysis_method': results['analysis_method'],
            'similar_functions_count': len(results['similar_functions']),
            'recommendations': results['recommendations'],
            'should_proceed': not results['is_duplicate'],
            'requires_review': results['is_similar'],
            'details': results
        }
        
        return ai_results
    
    async def batch_check_functions(self, functions_list: List[Dict]) -> List[Dict]:
        """Check multiple functions for similarity"""
        
        if not self.initialized:
            await self.initialize()
        
        return await self.similarity_checker.batch_similarity_check(functions_list)


# Example usage and testing
async def main():
    """Example usage of the Mathematical Function Similarity system"""
    
    print("🧪 Testing Mathematical Function Similarity System")
    print("=" * 60)
    
    # Initialize the similarity checker
    similarity_checker = MathematicalFunctionSimilarity()
    await similarity_checker.index_existing_functions()
    
    # Test function (potentially similar to existing ones)
    test_function = {
        'name': 'test_product_function',
        'latex_formula': r'\prod_{n=1}^{\infty} \sin\left(\frac{\pi z}{n}\right)',
        'description': 'Test infinite product of sine functions',
        'category': 'test_functions'
    }
    
    # Check similarity
    results = await similarity_checker.check_function_similarity(test_function)
    
    print("\n🔍 Similarity Analysis Results:")
    print(f"   Is Duplicate: {results['is_duplicate']}")
    print(f"   Is Similar: {results['is_similar']}")
    print(f"   Similarity Score: {results['similarity_score']:.3f}")
    print(f"   Analysis Method: {results['analysis_method']}")
    
    if results['similar_functions']:
        print("\n📊 Similar Functions Found:")
        for func in results['similar_functions'][:3]:
            print(f"   - {func['name']} (Score: {func['similarity_score']:.3f})")
    
    print("\n💡 Recommendations:")
    for rec in results['recommendations']:
        print(f"   {rec}")
    
    print("\n✅ Mathematical Function Similarity System test complete!")


if __name__ == "__main__":
    asyncio.run(main())