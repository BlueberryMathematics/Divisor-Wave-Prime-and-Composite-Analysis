"""
Qdrant Vector Database Setup and Initialization
Automated setup for mathematical function vector search database
"""

import asyncio
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

# Core imports
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, CollectionStatus
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
import numpy as np

# Project imports
import sys
sys.path.append(str(Path(__file__).parent.parent))
from src.core.latex_function_builder import LaTeXFunctionBuilder


class QdrantDatabaseSetup:
    """
    Automated setup and initialization of Qdrant vector database
    for mathematical function similarity search.
    """
    
    def __init__(self, 
                 host: str = "localhost", 
                 port: int = 6333,
                 collection_name: str = "mathematical_functions"):
        
        self.host = host
        self.port = port
        self.collection_name = collection_name
        self.client = None
        self.embedding_model = None
        
        # Configuration
        self.config = {
            'vector_size': 384,  # sentence-transformers/all-MiniLM-L6-v2
            'distance_metric': Distance.COSINE,
            'embedding_model_name': 'sentence-transformers/all-MiniLM-L6-v2',
            'shard_number': 1,
            'replication_factor': 1,
            'write_consistency_factor': 1,
            'max_batch_size': 100
        }
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    async def initialize_database(self) -> bool:
        """
        Initialize Qdrant database with proper configuration.
        
        Returns:
            bool: True if initialization successful
        """
        
        try:
            # Step 1: Connect to Qdrant
            self.logger.info(f"🔌 Connecting to Qdrant at {self.host}:{self.port}")
            self.client = QdrantClient(self.host, port=self.port)
            
            # Test connection
            collections = self.client.get_collections()
            self.logger.info(f"✅ Connected successfully. Found {len(collections.collections)} existing collections")
            
            # Step 2: Initialize embedding model
            self.logger.info(f"🤖 Loading embedding model: {self.config['embedding_model_name']}")
            self.embedding_model = SentenceTransformer(self.config['embedding_model_name'])
            self.logger.info("✅ Embedding model loaded successfully")
            
            # Step 3: Create collection if needed
            await self._setup_collection()
            
            # Step 4: Verify setup
            collection_info = self.client.get_collection(self.collection_name)
            self.logger.info(f"✅ Collection '{self.collection_name}' ready")
            self.logger.info(f"   Vectors: {collection_info.vectors_count}")
            self.logger.info(f"   Status: {collection_info.status}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Database initialization failed: {str(e)}")
            return False
    
    async def _setup_collection(self):
        """Setup the mathematical functions collection"""
        
        # Check if collection exists
        try:
            collection_info = self.client.get_collection(self.collection_name)
            self.logger.info(f"📊 Collection '{self.collection_name}' already exists")
            
            # Verify configuration
            if collection_info.config.params.vectors.size != self.config['vector_size']:
                self.logger.warning(f"⚠️ Vector size mismatch. Expected: {self.config['vector_size']}, Found: {collection_info.config.params.vectors.size}")
                
        except Exception:
            # Collection doesn't exist, create it
            self.logger.info(f"🔨 Creating collection '{self.collection_name}'")
            
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.config['vector_size'],
                    distance=self.config['distance_metric']
                ),
                shard_number=self.config['shard_number'],
                replication_factor=self.config['replication_factor'],
                write_consistency_factor=self.config['write_consistency_factor']
            )
            
            self.logger.info(f"✅ Collection '{self.collection_name}' created successfully")
    
    async def populate_initial_data(self, function_databases: List[str]) -> Dict[str, Any]:
        """
        Populate database with initial mathematical function data.
        
        Args:
            function_databases: List of paths to function database files
            
        Returns:
            Dict with population statistics
        """
        
        if not self.client or not self.embedding_model:
            raise RuntimeError("Database not initialized. Call initialize_database() first.")
        
        self.logger.info(f"📚 Populating database from {len(function_databases)} sources")
        
        # Statistics tracking
        stats = {
            'total_functions_processed': 0,
            'functions_added': 0,
            'functions_skipped': 0,
            'errors': 0,
            'processing_time': 0,
            'sources': {}
        }
        
        import time
        start_time = time.time()
        
        # Process each database
        for db_path in function_databases:
            source_stats = await self._process_function_database(db_path)
            
            # Update overall stats
            stats['total_functions_processed'] += source_stats['processed']
            stats['functions_added'] += source_stats['added']
            stats['functions_skipped'] += source_stats['skipped']
            stats['errors'] += source_stats['errors']
            stats['sources'][db_path] = source_stats
        
        stats['processing_time'] = time.time() - start_time
        
        self.logger.info(f"📊 POPULATION COMPLETE:")
        self.logger.info(f"   Total Processed: {stats['total_functions_processed']}")
        self.logger.info(f"   Added: {stats['functions_added']}")
        self.logger.info(f"   Skipped: {stats['functions_skipped']}")
        self.logger.info(f"   Errors: {stats['errors']}")
        self.logger.info(f"   Time: {stats['processing_time']:.2f} seconds")
        
        return stats
    
    async def _process_function_database(self, db_path: str) -> Dict[str, int]:
        """Process a single function database file"""
        
        self.logger.info(f"📖 Processing database: {db_path}")
        
        stats = {'processed': 0, 'added': 0, 'skipped': 0, 'errors': 0}
        
        try:
            # Check if file exists
            if not Path(db_path).exists():
                self.logger.warning(f"⚠️ Database file not found: {db_path}")
                return stats
            
            # Load function data
            with open(db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different data formats
            functions = []
            if isinstance(data, dict):
                if 'functions' in data:
                    functions = data['functions']
                elif 'custom_functions' in data:
                    functions = data['custom_functions']
                else:
                    # Assume dict values are functions
                    functions = list(data.values())
            elif isinstance(data, list):
                functions = data
            
            self.logger.info(f"   Found {len(functions)} functions")
            
            # Process functions in batches
            batch_size = self.config['max_batch_size']
            for i in range(0, len(functions), batch_size):
                batch = functions[i:i + batch_size]
                batch_stats = await self._process_function_batch(batch, db_path)
                
                # Update stats
                stats['processed'] += batch_stats['processed']
                stats['added'] += batch_stats['added']
                stats['skipped'] += batch_stats['skipped'] 
                stats['errors'] += batch_stats['errors']
                
                # Progress update
                if i % (batch_size * 5) == 0:  # Every 5 batches
                    self.logger.info(f"   Progress: {i + len(batch)}/{len(functions)} functions")
        
        except Exception as e:
            self.logger.error(f"❌ Error processing database {db_path}: {str(e)}")
            stats['errors'] += 1
        
        return stats
    
    async def _process_function_batch(self, functions: List[Dict], source: str) -> Dict[str, int]:
        """Process a batch of functions"""
        
        stats = {'processed': 0, 'added': 0, 'skipped': 0, 'errors': 0}
        
        # Prepare batch data
        points = []
        
        for func_data in functions:
            try:
                stats['processed'] += 1
                
                # Extract function information
                function_info = self._extract_function_info(func_data, source)
                if not function_info:
                    stats['skipped'] += 1
                    continue
                
                # Generate embedding
                text_for_embedding = self._prepare_text_for_embedding(function_info)
                embedding = self.embedding_model.encode(text_for_embedding)
                
                # Create point for Qdrant
                point = models.PointStruct(
                    id=len(points) + stats['added'],  # Simple ID generation
                    vector=embedding.tolist(),
                    payload=function_info
                )
                
                points.append(point)
                
            except Exception as e:
                self.logger.error(f"❌ Error processing function: {str(e)}")
                stats['errors'] += 1
        
        # Upload batch to Qdrant
        if points:
            try:
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=points
                )
                stats['added'] += len(points)
                
            except Exception as e:
                self.logger.error(f"❌ Error uploading batch: {str(e)}")
                stats['errors'] += len(points)
        
        return stats
    
    def _extract_function_info(self, func_data: Dict, source: str) -> Optional[Dict]:
        """Extract and normalize function information"""
        
        try:
            # Handle different function data formats
            info = {
                'source': source,
                'name': func_data.get('name', 'unnamed_function'),
                'latex_formula': func_data.get('latex_formula', ''),
                'description': func_data.get('description', ''),
                'category': func_data.get('category', 'unknown'),
                'properties': func_data.get('properties', {}),
                'original_data': func_data
            }
            
            # Validate required fields
            if not info['latex_formula']:
                return None
            
            # Add additional metadata
            info['import_timestamp'] = asyncio.get_event_loop().time()
            info['vector_version'] = '1.0'
            
            return info
            
        except Exception as e:
            self.logger.error(f"Error extracting function info: {str(e)}")
            return None
    
    def _prepare_text_for_embedding(self, function_info: Dict) -> str:
        """Prepare text for embedding generation"""
        
        # Combine multiple fields for rich embeddings
        text_parts = []
        
        # Add name
        if function_info.get('name'):
            text_parts.append(f"Function: {function_info['name']}")
        
        # Add LaTeX formula (most important)
        if function_info.get('latex_formula'):
            text_parts.append(f"Formula: {function_info['latex_formula']}")
        
        # Add description
        if function_info.get('description'):
            text_parts.append(f"Description: {function_info['description']}")
        
        # Add category
        if function_info.get('category'):
            text_parts.append(f"Category: {function_info['category']}")
        
        # Add properties
        if function_info.get('properties'):
            props = function_info['properties']
            if isinstance(props, dict):
                for key, value in props.items():
                    text_parts.append(f"{key}: {value}")
        
        # Combine all parts
        combined_text = " | ".join(text_parts)
        
        # Truncate if too long (model limit)
        max_length = 500  # Conservative limit
        if len(combined_text) > max_length:
            combined_text = combined_text[:max_length] + "..."
        
        return combined_text
    
    async def optimize_database(self):
        """Optimize database performance"""
        
        self.logger.info("🔧 Optimizing database performance")
        
        try:
            # Update collection configuration for better performance
            self.client.update_collection(
                collection_name=self.collection_name,
                optimizer_config=models.OptimizersConfigDiff(
                    default_segment_number=2,
                    max_segment_size=20000,
                    memmap_threshold=20000,
                ),
                # Enable payload index for faster filtering
                params=models.CollectionParamsDiff(
                    replication_factor=1,
                    write_consistency_factor=1
                )
            )
            
            self.logger.info("✅ Database optimization complete")
            
        except Exception as e:
            self.logger.error(f"❌ Optimization failed: {str(e)}")
    
    async def create_backup(self, backup_path: str = None) -> str:
        """Create backup of the vector database"""
        
        if not backup_path:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"backups/qdrant_backup_{timestamp}.json"
        
        # Ensure backup directory exists
        Path(backup_path).parent.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"💾 Creating backup: {backup_path}")
        
        try:
            # Retrieve all points
            points = self.client.scroll(
                collection_name=self.collection_name,
                limit=10000,  # Adjust based on your data size
                with_payload=True,
                with_vectors=True
            )[0]
            
            # Prepare backup data
            backup_data = {
                'collection_name': self.collection_name,
                'backup_timestamp': asyncio.get_event_loop().time(),
                'config': self.config,
                'points_count': len(points),
                'points': [
                    {
                        'id': point.id,
                        'vector': point.vector,
                        'payload': point.payload
                    } for point in points
                ]
            }
            
            # Save backup
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"✅ Backup created: {backup_path} ({len(points)} points)")
            return backup_path
            
        except Exception as e:
            self.logger.error(f"❌ Backup failed: {str(e)}")
            raise
    
    async def restore_from_backup(self, backup_path: str):
        """Restore database from backup"""
        
        self.logger.info(f"🔄 Restoring from backup: {backup_path}")
        
        try:
            # Load backup data
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            collection_name = backup_data['collection_name']
            points_data = backup_data['points']
            
            self.logger.info(f"   Restoring {len(points_data)} points to '{collection_name}'")
            
            # Recreate collection
            try:
                self.client.delete_collection(collection_name)
            except:
                pass  # Collection might not exist
            
            await self._setup_collection()
            
            # Restore points in batches
            batch_size = self.config['max_batch_size']
            for i in range(0, len(points_data), batch_size):
                batch = points_data[i:i + batch_size]
                
                points = [
                    models.PointStruct(
                        id=point_data['id'],
                        vector=point_data['vector'],
                        payload=point_data['payload']
                    ) for point_data in batch
                ]
                
                self.client.upsert(
                    collection_name=collection_name,
                    points=points
                )
                
                self.logger.info(f"   Restored {i + len(batch)}/{len(points_data)} points")
            
            self.logger.info("✅ Backup restoration complete")
            
        except Exception as e:
            self.logger.error(f"❌ Restoration failed: {str(e)}")
            raise
    
    def get_database_stats(self) -> Dict:
        """Get comprehensive database statistics"""
        
        try:
            collection_info = self.client.get_collection(self.collection_name)
            
            stats = {
                'collection_name': self.collection_name,
                'status': collection_info.status.value if collection_info.status else 'unknown',
                'vectors_count': collection_info.vectors_count or 0,
                'indexed_vectors_count': collection_info.indexed_vectors_count or 0,
                'points_count': collection_info.points_count or 0,
                'segments_count': len(collection_info.segments) if collection_info.segments else 0,
                'config': {
                    'vector_size': collection_info.config.params.vectors.size,
                    'distance_metric': collection_info.config.params.vectors.distance.value,
                    'shard_number': collection_info.config.params.shard_number,
                    'replication_factor': collection_info.config.params.replication_factor
                },
                'disk_usage': 'unknown',  # Qdrant doesn't provide this directly
                'last_updated': asyncio.get_event_loop().time()
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting database stats: {str(e)}")
            return {'error': str(e)}


# Automated setup script
async def setup_mathematical_function_database():
    """Complete automated setup of mathematical function vector database"""
    
    print("🚀 STARTING QDRANT MATHEMATICAL FUNCTION DATABASE SETUP")
    print("=" * 70)
    
    # Initialize setup
    setup = QdrantDatabaseSetup()
    
    # Step 1: Initialize database
    print("\n📡 Step 1: Database Initialization")
    success = await setup.initialize_database()
    if not success:
        print("❌ Setup failed during initialization")
        return False
    
    # Step 2: Find function databases
    print("\n📚 Step 2: Locating Function Databases")
    
    # Look for function databases in common locations
    possible_databases = [
        "src/core/custom_functions.json",
        "divisor-wave-python/src/core/custom_functions.json",
        "../divisor-wave-python/src/core/custom_functions.json",
        "data/mathematical_functions.json",
        "examples/sample_functions.json"
    ]
    
    found_databases = []
    for db_path in possible_databases:
        if Path(db_path).exists():
            found_databases.append(str(Path(db_path).resolve()))
            print(f"   ✅ Found: {db_path}")
        else:
            print(f"   ❌ Not found: {db_path}")
    
    if not found_databases:
        print("⚠️ No function databases found. Creating with sample data...")
        # Create sample database for testing
        sample_db_path = "data/sample_functions.json"
        Path(sample_db_path).parent.mkdir(parents=True, exist_ok=True)
        
        sample_functions = {
            "functions": [
                {
                    "name": "riemann_zeta",
                    "latex_formula": r"\zeta(s) = \sum_{n=1}^{\infty} \frac{1}{n^s}",
                    "description": "Riemann zeta function",
                    "category": "special_functions",
                    "properties": {"domain": "complex", "zeros": "critical_line"}
                },
                {
                    "name": "euler_product",
                    "latex_formula": r"\prod_{p \text{ prime}} \frac{1}{1-p^{-s}}",
                    "description": "Euler product formula",
                    "category": "number_theory",
                    "properties": {"convergence": "s > 1"}
                }
            ]
        }
        
        with open(sample_db_path, 'w', encoding='utf-8') as f:
            json.dump(sample_functions, f, indent=2, ensure_ascii=False)
        
        found_databases = [sample_db_path]
        print(f"   ✅ Created sample database: {sample_db_path}")
    
    # Step 3: Populate database
    print("\n🔄 Step 3: Populating Vector Database")
    
    stats = await setup.populate_initial_data(found_databases)
    
    print(f"\n📊 POPULATION RESULTS:")
    print(f"   Functions Processed: {stats['total_functions_processed']}")
    print(f"   Functions Added: {stats['functions_added']}")
    print(f"   Processing Time: {stats['processing_time']:.2f} seconds")
    
    # Step 4: Optimize database
    print("\n⚡ Step 4: Database Optimization")
    await setup.optimize_database()
    
    # Step 5: Create initial backup
    print("\n💾 Step 5: Creating Initial Backup")
    backup_path = await setup.create_backup()
    print(f"   Backup saved: {backup_path}")
    
    # Step 6: Final verification
    print("\n✅ Step 6: Final Verification")
    final_stats = setup.get_database_stats()
    
    print(f"   Collection: {final_stats['collection_name']}")
    print(f"   Status: {final_stats['status']}")
    print(f"   Total Points: {final_stats['points_count']}")
    print(f"   Indexed Vectors: {final_stats['indexed_vectors_count']}")
    print(f"   Vector Size: {final_stats['config']['vector_size']}")
    
    print("\n🎉 QDRANT MATHEMATICAL FUNCTION DATABASE SETUP COMPLETE!")
    print("=" * 70)
    
    return True


# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Setup Qdrant Mathematical Function Database")
    parser.add_argument("--host", default="localhost", help="Qdrant host")
    parser.add_argument("--port", type=int, default=6333, help="Qdrant port")
    parser.add_argument("--collection", default="mathematical_functions", help="Collection name")
    parser.add_argument("--backup", help="Restore from backup file")
    parser.add_argument("--stats", action="store_true", help="Show database statistics")
    
    args = parser.parse_args()
    
    async def main():
        setup = QdrantDatabaseSetup(args.host, args.port, args.collection)
        
        if args.backup:
            await setup.initialize_database()
            await setup.restore_from_backup(args.backup)
        elif args.stats:
            await setup.initialize_database()
            stats = setup.get_database_stats()
            print(json.dumps(stats, indent=2))
        else:
            await setup_mathematical_function_database()
    
    asyncio.run(main())