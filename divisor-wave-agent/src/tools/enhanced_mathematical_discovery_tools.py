"""
AI Mathematical Discovery Tools - Enhanced Agent Integration
Complete integration of mathematical function validation and similarity tools with AI agents
"""

import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path

from .mathematical_function_similarity import AIFunctionSimilarityTool
from .mathematical_function_validator import AIFunctionValidatorTool


@dataclass
class DiscoveryValidationResult:
    """Combined result from similarity and uniqueness validation"""
    function_data: Dict
    similarity_result: Dict
    validation_result: Dict
    final_recommendation: str
    should_proceed: bool
    requires_review: bool
    confidence_score: float
    analysis_summary: List[str]


class EnhancedAIMathematicalDiscoveryTools:
    """
    Enhanced AI tools for mathematical discovery validation.
    
    Combines similarity search and uniqueness validation to provide
    comprehensive analysis of newly discovered mathematical functions.
    """
    
    def __init__(self):
        self.similarity_tool = AIFunctionSimilarityTool()
        self.validator_tool = AIFunctionValidatorTool()
        self.initialized = False
    
    async def initialize(self):
        """Initialize all AI tools"""
        
        if not self.initialized:
            print("🔄 Initializing Enhanced AI Mathematical Discovery Tools...")
            
            # Initialize similarity search tool
            await self.similarity_tool.initialize()
            
            # Validator tool initializes automatically
            print("✅ Enhanced AI Mathematical Discovery Tools initialized")
            self.initialized = True
    
    async def comprehensive_function_analysis(self, function_data: Dict) -> DiscoveryValidationResult:
        """
        Perform comprehensive analysis of a new mathematical function.
        
        Combines similarity search and uniqueness validation to provide
        complete assessment of the function's novelty and validity.
        
        Args:
            function_data: Dictionary containing function information
                          Keys: name, latex_formula, description, category, properties
                          
        Returns:
            DiscoveryValidationResult with comprehensive analysis
        """
        
        if not self.initialized:
            await self.initialize()
        
        print(f"🔍 Performing comprehensive analysis for: {function_data.get('name', 'unnamed function')}")
        
        # Phase 1: Similarity Analysis
        print("   Phase 1: Similarity search...")
        similarity_result = await self.similarity_tool.check_new_function(function_data)
        
        # Phase 2: Uniqueness Validation
        print("   Phase 2: Uniqueness validation...")
        validation_result = await self.validator_tool.validate_new_function(function_data)
        
        # Phase 3: Combined Analysis
        print("   Phase 3: Combined analysis...")
        combined_analysis = self._combine_analysis_results(
            function_data, similarity_result, validation_result
        )
        
        return combined_analysis
    
    def _combine_analysis_results(self, 
                                function_data: Dict,
                                similarity_result: Dict,
                                validation_result: Dict) -> DiscoveryValidationResult:
        """Combine similarity and validation results into final assessment"""
        
        # Determine final recommendation
        final_recommendation = self._determine_final_recommendation(
            similarity_result, validation_result
        )
        
        # Determine if should proceed
        should_proceed = self._should_proceed_with_function(
            similarity_result, validation_result
        )
        
        # Determine if requires human review
        requires_review = self._requires_human_review(
            similarity_result, validation_result
        )
        
        # Calculate combined confidence score
        confidence_score = self._calculate_combined_confidence(
            similarity_result, validation_result
        )
        
        # Generate analysis summary
        analysis_summary = self._generate_analysis_summary(
            similarity_result, validation_result, final_recommendation
        )
        
        return DiscoveryValidationResult(
            function_data=function_data,
            similarity_result=similarity_result,
            validation_result=validation_result,
            final_recommendation=final_recommendation,
            should_proceed=should_proceed,
            requires_review=requires_review,
            confidence_score=confidence_score,
            analysis_summary=analysis_summary
        )
    
    def _determine_final_recommendation(self, similarity_result: Dict, validation_result: Dict) -> str:
        """Determine final recommendation based on both analyses"""
        
        # Priority order: validation status > similarity status
        validation_status = validation_result.get('validation_status', '')
        similarity_status = similarity_result.get('status', '')
        
        if validation_status == 'duplicate':
            return 'REJECT_DUPLICATE'
        elif validation_status == 'highly_similar' and similarity_status == 'duplicate':
            return 'REJECT_DUPLICATE'
        elif validation_status == 'highly_similar':
            return 'REVIEW_HIGHLY_SIMILAR'
        elif similarity_status == 'similar' and validation_status == 'similar':
            return 'REVIEW_SIMILAR'
        elif validation_status == 'unique' and similarity_status == 'novel':
            return 'APPROVE_NOVEL'
        elif validation_status == 'unique':
            return 'APPROVE_UNIQUE'
        else:
            return 'REVIEW_UNCERTAIN'
    
    def _should_proceed_with_function(self, similarity_result: Dict, validation_result: Dict) -> bool:
        """Determine if function registration should proceed"""
        
        # Don't proceed with duplicates
        if (validation_result.get('validation_status') == 'duplicate' or 
            similarity_result.get('status') == 'duplicate'):
            return False
        
        # Don't proceed with highly similar functions
        if validation_result.get('validation_status') == 'highly_similar':
            return False
        
        # Proceed with unique functions
        if (validation_result.get('is_unique', False) and 
            similarity_result.get('status') == 'novel'):
            return True
        
        # Proceed with similar but not highly similar
        if (validation_result.get('validation_status') in ['unique', 'similar'] and
            similarity_result.get('status') in ['novel', 'similar']):
            return True
        
        return False
    
    def _requires_human_review(self, similarity_result: Dict, validation_result: Dict) -> bool:
        """Determine if human review is required"""
        
        # Always require review for duplicates or highly similar
        if (validation_result.get('validation_status') in ['duplicate', 'highly_similar'] or
            similarity_result.get('status') == 'duplicate'):
            return True
        
        # Require review for similar functions
        if (validation_result.get('validation_status') == 'similar' or
            similarity_result.get('status') == 'similar'):
            return True
        
        # Require review for low confidence
        if (validation_result.get('confidence_score', 0) < 0.7 or
            similarity_result.get('confidence', 0) < 0.7):
            return True
        
        return False
    
    def _calculate_combined_confidence(self, similarity_result: Dict, validation_result: Dict) -> float:
        """Calculate combined confidence score"""
        
        similarity_confidence = similarity_result.get('confidence', 0.5)
        validation_confidence = validation_result.get('confidence_score', 0.5)
        
        # Weighted average (validation gets higher weight)
        combined_confidence = (validation_confidence * 0.6 + similarity_confidence * 0.4)
        
        # Penalty for conflicts between methods
        similarity_status = similarity_result.get('status', '')
        validation_status = validation_result.get('validation_status', '')
        
        if (similarity_status == 'duplicate' and validation_status != 'duplicate') or \
           (validation_status == 'duplicate' and similarity_status != 'duplicate'):
            combined_confidence *= 0.8  # Conflict penalty
        
        return round(combined_confidence, 3)
    
    def _generate_analysis_summary(self, 
                                 similarity_result: Dict, 
                                 validation_result: Dict,
                                 final_recommendation: str) -> List[str]:
        """Generate human-readable analysis summary"""
        
        summary = []
        
        # Add main conclusion
        summary.append(f"🎯 FINAL RECOMMENDATION: {final_recommendation}")
        
        # Add similarity analysis summary
        similarity_status = similarity_result.get('status', 'unknown')
        similarity_confidence = similarity_result.get('confidence', 0)
        summary.append(f"🔍 Similarity Analysis: {similarity_status} (confidence: {similarity_confidence:.2f})")
        
        if similarity_result.get('similar_functions_count', 0) > 0:
            count = similarity_result['similar_functions_count']
            summary.append(f"   Found {count} similar function(s) in database")
        
        # Add validation analysis summary
        validation_status = validation_result.get('validation_status', 'unknown')
        validation_confidence = validation_result.get('confidence_score', 0)
        summary.append(f"✅ Uniqueness Validation: {validation_status} (confidence: {validation_confidence:.2f})")
        
        if validation_result.get('duplicate_count', 0) > 0:
            count = validation_result['duplicate_count']
            summary.append(f"   Found {count} exact duplicate(s)")
        
        if validation_result.get('similar_count', 0) > 0:
            count = validation_result['similar_count']
            summary.append(f"   Found {count} structurally similar function(s)")
        
        # Add method information
        similarity_method = similarity_result.get('details', {}).get('analysis_method', 'unknown')
        validation_methods = validation_result.get('validation_methods_used', [])
        summary.append(f"🔬 Analysis Methods: similarity({similarity_method}), validation({', '.join(validation_methods)})")
        
        # Add specific recommendations
        if final_recommendation == 'REJECT_DUPLICATE':
            summary.append("❌ DO NOT REGISTER: Function already exists")
        elif final_recommendation == 'REVIEW_HIGHLY_SIMILAR':
            summary.append("⚠️ HUMAN REVIEW REQUIRED: Highly similar function found")
        elif final_recommendation == 'REVIEW_SIMILAR':
            summary.append("ℹ️ REVIEW RECOMMENDED: Similar functions found")
        elif final_recommendation == 'APPROVE_NOVEL':
            summary.append("🚀 APPROVE: Novel mathematical discovery confirmed")
        elif final_recommendation == 'APPROVE_UNIQUE':
            summary.append("✅ APPROVE: Unique function confirmed")
        else:
            summary.append("❓ UNCERTAIN: Manual review required")
        
        return summary
    
    async def batch_analyze_functions(self, functions_list: List[Dict]) -> List[DiscoveryValidationResult]:
        """Perform comprehensive analysis on multiple functions"""
        
        if not self.initialized:
            await self.initialize()
        
        print(f"🔄 Performing batch analysis on {len(functions_list)} functions...")
        
        results = []
        
        for i, function_data in enumerate(functions_list):
            print(f"\n📊 Analyzing function {i+1}/{len(functions_list)}: {function_data.get('name', 'unnamed')}")
            
            result = await self.comprehensive_function_analysis(function_data)
            results.append(result)
            
            # Brief status update
            print(f"   Result: {result.final_recommendation} (confidence: {result.confidence_score:.2f})")
        
        return results
    
    async def generate_discovery_report(self, 
                                      analysis_results: List[DiscoveryValidationResult],
                                      output_path: Optional[str] = None) -> Dict:
        """Generate comprehensive discovery report"""
        
        # Calculate statistics
        total_functions = len(analysis_results)
        approved_functions = len([r for r in analysis_results if r.should_proceed])
        rejected_functions = len([r for r in analysis_results if r.final_recommendation.startswith('REJECT')])
        review_required = len([r for r in analysis_results if r.requires_review])
        
        # Categorize by recommendation
        recommendations_count = {}
        for result in analysis_results:
            rec = result.final_recommendation
            recommendations_count[rec] = recommendations_count.get(rec, 0) + 1
        
        # Calculate average confidence
        avg_confidence = sum(r.confidence_score for r in analysis_results) / total_functions if total_functions > 0 else 0
        
        # Generate report
        report = {
            'analysis_timestamp': asyncio.get_event_loop().time(),
            'summary_statistics': {
                'total_functions_analyzed': total_functions,
                'approved_for_registration': approved_functions,
                'rejected_duplicates': rejected_functions,
                'requiring_human_review': review_required,
                'average_confidence_score': round(avg_confidence, 3)
            },
            'recommendation_breakdown': recommendations_count,
            'detailed_results': [
                {
                    'function_name': result.function_data.get('name', 'unnamed'),
                    'final_recommendation': result.final_recommendation,
                    'should_proceed': result.should_proceed,
                    'requires_review': result.requires_review,
                    'confidence_score': result.confidence_score,
                    'analysis_summary': result.analysis_summary,
                    'similarity_analysis': {
                        'status': result.similarity_result.get('status'),
                        'confidence': result.similarity_result.get('confidence'),
                        'similar_functions_count': result.similarity_result.get('similar_functions_count', 0)
                    },
                    'validation_analysis': {
                        'status': result.validation_result.get('validation_status'),
                        'is_unique': result.validation_result.get('is_unique'),
                        'confidence': result.validation_result.get('confidence_score'),
                        'duplicate_count': result.validation_result.get('duplicate_count', 0),
                        'similar_count': result.validation_result.get('similar_count', 0)
                    }
                } for result in analysis_results
            ]
        }
        
        # Save report if path provided
        if output_path:
            import json
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"📊 Discovery report saved to: {output_path}")
        
        return report
    
    def print_analysis_summary(self, result: DiscoveryValidationResult):
        """Print a formatted analysis summary"""
        
        print(f"\n🔍 ANALYSIS SUMMARY: {result.function_data.get('name', 'Unnamed Function')}")
        print("=" * 60)
        
        for line in result.analysis_summary:
            print(f"   {line}")
        
        print(f"\n📊 COMBINED CONFIDENCE: {result.confidence_score:.3f}")
        print(f"🚦 SHOULD PROCEED: {'YES' if result.should_proceed else 'NO'}")
        print(f"👥 REQUIRES REVIEW: {'YES' if result.requires_review else 'NO'}")


# Example usage for AI agents
class AIMathematicalDiscoveryInterface:
    """
    Simplified interface for AI agents to use mathematical discovery tools.
    Provides high-level functions optimized for AI agent integration.
    """
    
    def __init__(self):
        self.tools = EnhancedAIMathematicalDiscoveryTools()
    
    async def validate_discovered_function(self, function_data: Dict) -> Dict:
        """
        Main interface for AI agents to validate discovered functions.
        
        Returns simplified result suitable for AI decision making.
        """
        
        result = await self.tools.comprehensive_function_analysis(function_data)
        
        # Simplified result for AI consumption
        return {
            'function_name': function_data.get('name', 'unnamed'),
            'is_valid_discovery': result.should_proceed,
            'recommendation': result.final_recommendation,
            'confidence': result.confidence_score,
            'requires_human_review': result.requires_review,
            'reasoning': result.analysis_summary[:3],  # Top 3 summary points
            'duplicate_detected': 'DUPLICATE' in result.final_recommendation,
            'novel_discovery': 'NOVEL' in result.final_recommendation or 'UNIQUE' in result.final_recommendation
        }
    
    async def check_function_novelty(self, latex_formula: str, function_name: str = None) -> bool:
        """
        Quick novelty check for AI agents.
        Returns True if function appears to be novel.
        """
        
        function_data = {
            'name': function_name or 'ai_generated_function',
            'latex_formula': latex_formula,
            'description': 'AI-generated mathematical function',
            'category': 'ai_generated'
        }
        
        result = await self.validate_discovered_function(function_data)
        return result['is_valid_discovery'] and not result['duplicate_detected']
    
    async def batch_validate_discoveries(self, functions_list: List[Dict]) -> Dict:
        """
        Batch validation for AI agents.
        Returns summary suitable for AI processing.
        """
        
        results = await self.tools.batch_analyze_functions(functions_list)
        
        # Summarize for AI
        valid_discoveries = [r for r in results if r.should_proceed]
        novel_discoveries = [r for r in results if 'NOVEL' in r.final_recommendation or 'UNIQUE' in r.final_recommendation]
        duplicates = [r for r in results if 'DUPLICATE' in r.final_recommendation]
        
        return {
            'total_analyzed': len(functions_list),
            'valid_discoveries': len(valid_discoveries),
            'novel_discoveries': len(novel_discoveries),
            'duplicates_found': len(duplicates),
            'success_rate': len(valid_discoveries) / len(functions_list) if functions_list else 0,
            'novelty_rate': len(novel_discoveries) / len(functions_list) if functions_list else 0,
            'detailed_results': [
                {
                    'name': r.function_data.get('name'),
                    'valid': r.should_proceed,
                    'novel': 'NOVEL' in r.final_recommendation or 'UNIQUE' in r.final_recommendation,
                    'confidence': r.confidence_score
                } for r in results
            ]
        }


# Example usage and integration test
async def main():
    """Example usage of the Enhanced AI Mathematical Discovery Tools"""
    
    print("🧪 Testing Enhanced AI Mathematical Discovery Tools")
    print("=" * 60)
    
    # Test functions
    test_functions = [
        {
            'name': 'test_novel_function',
            'latex_formula': r'\prod_{n=1}^{\infty} \cos\left(\frac{\pi z}{n^2}\right)',
            'description': 'Novel infinite product with squared denominators',
            'category': 'test_functions'
        },
        {
            'name': 'test_existing_function',
            'latex_formula': r'\prod_{n=1}^{\infty} \sin\left(\frac{\pi z}{n}\right)',
            'description': 'Known infinite product (should be detected as similar)',
            'category': 'test_functions'
        }
    ]
    
    # Initialize discovery tools
    discovery_tools = EnhancedAIMathematicalDiscoveryTools()
    await discovery_tools.initialize()
    
    # Test individual function analysis
    print("\n🔍 Testing Individual Function Analysis:")
    result = await discovery_tools.comprehensive_function_analysis(test_functions[0])
    discovery_tools.print_analysis_summary(result)
    
    # Test batch analysis
    print("\n📊 Testing Batch Analysis:")
    batch_results = await discovery_tools.batch_analyze_functions(test_functions)
    
    # Generate report
    report = await discovery_tools.generate_discovery_report(batch_results)
    
    print(f"\n📈 BATCH ANALYSIS REPORT:")
    print(f"   Total Functions: {report['summary_statistics']['total_functions_analyzed']}")
    print(f"   Approved: {report['summary_statistics']['approved_for_registration']}")
    print(f"   Rejected: {report['summary_statistics']['rejected_duplicates']}")
    print(f"   Review Required: {report['summary_statistics']['requiring_human_review']}")
    print(f"   Average Confidence: {report['summary_statistics']['average_confidence_score']:.3f}")
    
    # Test AI interface
    print("\n🤖 Testing AI Agent Interface:")
    ai_interface = AIMathematicalDiscoveryInterface()
    
    quick_result = await ai_interface.validate_discovered_function(test_functions[0])
    print(f"   Function: {quick_result['function_name']}")
    print(f"   Valid Discovery: {quick_result['is_valid_discovery']}")
    print(f"   Novel: {quick_result['novel_discovery']}")
    print(f"   Recommendation: {quick_result['recommendation']}")
    
    print("\n✅ Enhanced AI Mathematical Discovery Tools test complete!")


if __name__ == "__main__":
    asyncio.run(main())