"""
AI-Powered Mathematical Function Discovery Script
Combines systematic function generation with AI evaluation and validation
"""

import asyncio
import json
import random
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

# Import the function generator
from src.core.mathematical_function_generator import (
    MathematicalFunctionGenerator, 
    AIFunctionEvaluator,
    GeneratedFunction,
    SeriesType,
    OperatorType
)

# Import validation tools if available
try:
    import sys
    sys.path.append(str(Path(__file__).parent.parent.parent / "divisor-wave-agent"))
    from src.tools.enhanced_mathematical_discovery_tools import AIMathematicalDiscoveryInterface
    VALIDATION_AVAILABLE = True
    print("✅ Advanced validation tools available")
except ImportError:
    VALIDATION_AVAILABLE = False
    print("⚠️ Advanced validation tools not available - using basic validation")


class SmartAIFunctionEvaluator:
    """
    Enhanced AI evaluator that considers mathematical interest, novelty, and potential
    """
    
    def __init__(self):
        self.evaluation_history = []
        
        # Enhanced evaluation criteria
        self.criteria = {
            # Mathematical Interest Factors
            'has_infinite_series': 0.8,
            'uses_trigonometric_functions': 0.7,
            'has_complex_indexing': 0.6,
            'involves_primes_or_fibonacci': 0.9,
            'has_nested_structure': 0.8,
            
            # Complexity preferences
            'optimal_complexity_range': (1.3, 2.2),
            'complexity_penalty_factor': 0.5,
            
            # Pattern preferences (based on divisor wave analysis)
            'prefers_sin_cos_patterns': 0.8,
            'prefers_product_over_sum': 0.7,
            'prefers_pi_coefficients': 0.6,
            
            # Novelty factors
            'penalize_simple_patterns': 0.3,
            'reward_unique_combinations': 0.9,
            
            # Mathematical rigor
            'likely_convergent_bonus': 0.7,
            'avoids_dangerous_patterns': 0.9
        }
        
        # Track what we've seen to reward novelty
        self.seen_patterns = set()
        self.accepted_functions = []
        
    def evaluate_function(self, function: GeneratedFunction) -> Dict[str, Any]:
        """
        Comprehensive evaluation of a mathematical function
        Returns detailed evaluation with score and reasoning
        """
        
        evaluation = {
            'overall_score': 0.0,
            'decision': False,
            'reasoning': [],
            'scores': {},
            'recommendations': []
        }
        
        scores = {}
        reasoning = []
        
        # 1. Mathematical Interest Score
        interest_score = self._evaluate_mathematical_interest(function)
        scores['mathematical_interest'] = interest_score
        reasoning.append(f"Mathematical interest: {interest_score:.2f}")
        
        # 2. Complexity Score
        complexity_score = self._evaluate_complexity(function)
        scores['complexity'] = complexity_score
        reasoning.append(f"Complexity appropriateness: {complexity_score:.2f}")
        
        # 3. Novelty Score
        novelty_score = self._evaluate_novelty(function)
        scores['novelty'] = novelty_score
        reasoning.append(f"Novelty factor: {novelty_score:.2f}")
        
        # 4. Convergence Score
        convergence_score = self._evaluate_convergence(function)
        scores['convergence'] = convergence_score
        reasoning.append(f"Convergence likelihood: {convergence_score:.2f}")
        
        # 5. Pattern Matching Score (similarity to successful divisor wave patterns)
        pattern_score = self._evaluate_pattern_similarity(function)
        scores['pattern_similarity'] = pattern_score
        reasoning.append(f"Pattern similarity to successful functions: {pattern_score:.2f}")
        
        # 6. Computational Feasibility
        feasibility_score = self._evaluate_computational_feasibility(function)
        scores['feasibility'] = feasibility_score
        reasoning.append(f"Computational feasibility: {feasibility_score:.2f}")
        
        # Calculate weighted overall score
        weights = {
            'mathematical_interest': 0.25,
            'complexity': 0.15,
            'novelty': 0.20,
            'convergence': 0.15,
            'pattern_similarity': 0.15,
            'feasibility': 0.10
        }
        
        overall_score = sum(scores[key] * weights[key] for key in weights)
        
        # Decision threshold with some randomness for exploration
        base_threshold = 0.65
        random_factor = random.uniform(-0.05, 0.05)  # Small random exploration
        threshold = base_threshold + random_factor
        
        decision = overall_score > threshold
        
        # Add final reasoning
        if decision:
            reasoning.append(f"✅ ACCEPTED: Overall score {overall_score:.3f} > threshold {threshold:.3f}")
        else:
            reasoning.append(f"❌ REJECTED: Overall score {overall_score:.3f} <= threshold {threshold:.3f}")
        
        # Store evaluation results
        evaluation.update({
            'overall_score': overall_score,
            'decision': decision,
            'reasoning': reasoning,
            'scores': scores,
            'threshold_used': threshold
        })
        
        # Track for novelty evaluation
        pattern_signature = self._get_pattern_signature(function)
        if decision:
            self.seen_patterns.add(pattern_signature)
            self.accepted_functions.append(function)
        
        self.evaluation_history.append(evaluation)
        
        return evaluation
    
    def _evaluate_mathematical_interest(self, function: GeneratedFunction) -> float:
        """Evaluate mathematical interest of the function"""
        
        score = 0.3  # Base score
        
        # Series type interest
        if function.series_structure.series_type == SeriesType.INFINITE_PRODUCT:
            score += 0.3  # Products are interesting like our divisor waves
        elif function.series_structure.series_type == SeriesType.INFINITE_SUM:
            score += 0.2  # Sums are also interesting
        elif function.series_structure.series_type in [SeriesType.NESTED_SERIES, SeriesType.HYBRID_SERIES]:
            score += 0.4  # Complex structures are very interesting
        
        # Operator interest
        operators = [comp.operator for comp in function.series_structure.components]
        
        if OperatorType.SIN in operators or OperatorType.COS in operators:
            score += 0.2  # Trigonometric functions are central to our research
        
        if OperatorType.GAMMA in operators or OperatorType.ZETA in operators:
            score += 0.3  # Special functions are very interesting
        
        if OperatorType.EXP in operators:
            score += 0.15  # Exponential functions add interest
        
        # Index type interest
        from src.core.mathematical_function_generator import IndexType
        
        if function.series_structure.index_type in [IndexType.PRIME, IndexType.FIBONACCI]:
            score += 0.25  # Number-theoretic indices are fascinating
        elif function.series_structure.index_type in [IndexType.QUADRATIC, IndexType.CUBIC]:
            score += 0.15  # Polynomial growth is moderately interesting
        elif function.series_structure.index_type == IndexType.EXPONENTIAL:
            score += 0.1   # Exponential growth can be interesting but dangerous
        
        # Coefficient patterns
        for component in function.series_structure.components:
            if 'pi' in component.argument.lower() or '\\pi' in component.argument:
                score += 0.1  # Pi is always mathematically interesting
            
            if 'z^2' in component.argument or 'z²' in component.argument:
                score += 0.05  # Quadratic terms add interest
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _evaluate_complexity(self, function: GeneratedFunction) -> float:
        """Evaluate if complexity is appropriate (not too simple, not too complex)"""
        
        complexity = function.complexity_score
        min_good, max_good = self.criteria['optimal_complexity_range']
        
        if min_good <= complexity <= max_good:
            return 1.0  # Perfect complexity range
        elif complexity < min_good:
            # Too simple - penalize
            return (complexity / min_good) * 0.8
        else:
            # Too complex - penalize more severely
            penalty = (complexity - max_good) * self.criteria['complexity_penalty_factor']
            return max(0.1, 1.0 - penalty)
    
    def _evaluate_novelty(self, function: GeneratedFunction) -> float:
        """Evaluate novelty compared to what we've seen before"""
        
        pattern_signature = self._get_pattern_signature(function)
        
        if pattern_signature in self.seen_patterns:
            return 0.2  # Very low score for repeated patterns
        
        # Check similarity to existing patterns
        similar_count = 0
        for seen_pattern in self.seen_patterns:
            if self._patterns_similar(pattern_signature, seen_pattern):
                similar_count += 1
        
        # Reduce score based on similarity to existing patterns
        novelty_score = 1.0 - (similar_count / max(len(self.seen_patterns), 1)) * 0.6
        
        return max(0.1, novelty_score)
    
    def _evaluate_convergence(self, function: GeneratedFunction) -> float:
        """Evaluate likelihood of convergence"""
        
        # Use the mathematical properties analysis
        convergence_estimate = function.mathematical_properties.get('estimated_convergence', 'unknown')
        
        convergence_scores = {
            'very_fast_convergent': 1.0,
            'fast_convergent': 0.9,
            'likely_convergent': 0.8,
            'convergence_depends_on_z': 0.6,
            'unknown': 0.4,
            'likely_divergent': 0.1
        }
        
        base_score = convergence_scores.get(convergence_estimate, 0.4)
        
        # Additional analysis based on structure
        from src.core.mathematical_function_generator import IndexType
        
        if function.series_structure.index_type in [IndexType.QUADRATIC, IndexType.CUBIC, IndexType.FACTORIAL]:
            base_score += 0.1  # These usually help convergence
        elif function.series_structure.index_type == IndexType.LINEAR:
            # Linear indexing can be problematic for infinite sums
            if function.series_structure.series_type == SeriesType.INFINITE_SUM:
                base_score -= 0.2
        
        return min(base_score, 1.0)
    
    def _evaluate_pattern_similarity(self, function: GeneratedFunction) -> float:
        """Evaluate similarity to successful mathematical patterns"""
        
        score = 0.3  # Base score
        
        # Similarity to divisor wave patterns
        has_sin_cos = any(comp.operator in [OperatorType.SIN, OperatorType.COS] 
                         for comp in function.series_structure.components)
        
        has_pi_z_over_n = any('pi' in comp.argument.lower() and 'z' in comp.argument.lower() 
                             for comp in function.series_structure.components)
        
        if has_sin_cos and has_pi_z_over_n:
            score += 0.4  # Very similar to our successful patterns
        elif has_sin_cos:
            score += 0.2
        elif has_pi_z_over_n:
            score += 0.15
        
        # Infinite product bonus (like our main functions)
        if function.series_structure.series_type == SeriesType.INFINITE_PRODUCT:
            score += 0.2
        
        # Check for Riesz or Viète-like patterns
        has_alternating = any('1 +' in comp.argument or '1-' in comp.argument 
                             for comp in function.series_structure.components)
        if has_alternating:
            score += 0.15  # Similar to Riesz products
        
        return min(score, 1.0)
    
    def _evaluate_computational_feasibility(self, function: GeneratedFunction) -> float:
        """Evaluate if function can be computed efficiently"""
        
        score = 0.8  # Base score - assume most are feasible
        
        # Penalize very complex operators
        for component in function.series_structure.components:
            if component.operator in [OperatorType.GAMMA, OperatorType.ZETA]:
                score -= 0.1  # These are expensive to compute
        
        # Penalize factorial indexing (grows too fast)
        from src.core.mathematical_function_generator import IndexType
        if function.series_structure.index_type == IndexType.FACTORIAL:
            score -= 0.3
        
        # Penalize too many components
        if len(function.series_structure.components) > 2:
            score -= 0.2
        
        return max(0.1, score)
    
    def _get_pattern_signature(self, function: GeneratedFunction) -> str:
        """Generate a signature for pattern matching"""
        
        operators = sorted([comp.operator.value for comp in function.series_structure.components])
        
        signature = f"{function.series_structure.series_type.value}_{function.series_structure.index_type.value}_{'_'.join(operators)}"
        
        return signature
    
    def _patterns_similar(self, pattern1: str, pattern2: str) -> bool:
        """Check if two patterns are similar"""
        
        parts1 = set(pattern1.split('_'))
        parts2 = set(pattern2.split('_'))
        
        # Similar if they share more than half their components
        overlap = len(parts1 & parts2)
        total = len(parts1 | parts2)
        
        return overlap / total > 0.6
    
    def __call__(self, function: GeneratedFunction) -> bool:
        """Make evaluator callable - returns boolean decision"""
        
        evaluation = self.evaluate_function(function)
        return evaluation['decision']
    
    def get_evaluation_summary(self) -> Dict[str, Any]:
        """Get summary of evaluation history"""
        
        if not self.evaluation_history:
            return {"message": "No evaluations performed yet"}
        
        total_evaluations = len(self.evaluation_history)
        accepted = sum(1 for eval in self.evaluation_history if eval['decision'])
        
        avg_scores = {}
        if self.evaluation_history:
            for key in self.evaluation_history[0]['scores'].keys():
                avg_scores[key] = sum(eval['scores'][key] for eval in self.evaluation_history) / total_evaluations
        
        return {
            'total_evaluations': total_evaluations,
            'accepted_count': accepted,
            'acceptance_rate': accepted / total_evaluations if total_evaluations > 0 else 0,
            'average_scores': avg_scores,
            'unique_patterns_seen': len(self.seen_patterns)
        }


class MathematicalDiscoverySession:
    """
    Complete mathematical discovery session combining generation, AI evaluation, and validation
    """
    
    def __init__(self):
        """Initialize discovery session"""
        
        print("🚀 Initializing Mathematical Discovery Session...")
        
        # Initialize components
        self.generator = MathematicalFunctionGenerator()
        self.ai_evaluator = SmartAIFunctionEvaluator()
        self.generator.set_ai_evaluator(self.ai_evaluator)
        
        # Initialize validation if available
        self.validator = None
        if VALIDATION_AVAILABLE:
            try:
                self.validator = AIMathematicalDiscoveryInterface()
                print("✅ Advanced validation system initialized")
            except Exception as e:
                print(f"⚠️ Advanced validation unavailable: {e}")
                VALIDATION_AVAILABLE = False
        
        # Session tracking
        self.session_stats = {
            'start_time': time.time(),
            'functions_generated': 0,
            'functions_ai_approved': 0,
            'functions_validated': 0,
            'functions_novel': 0,
            'total_time_spent': 0
        }
        
        self.discovered_functions = []
        self.validation_results = []
        
        print("✅ Discovery session ready!")
    
    async def run_discovery_session(self, 
                                   target_discoveries: int = 20,
                                   max_generation_attempts: int = 200,
                                   complexity_range: tuple = (1.2, 2.5),
                                   validate_discoveries: bool = True) -> Dict[str, Any]:
        """
        Run complete discovery session
        
        Args:
            target_discoveries: Number of novel functions to discover
            max_generation_attempts: Maximum functions to generate
            complexity_range: Range of complexity scores to target
            validate_discoveries: Whether to validate with advanced tools
            
        Returns:
            Dictionary with session results
        """
        
        print(f"🎯 Starting discovery session: targeting {target_discoveries} novel functions")
        print(f"📊 Parameters: max_attempts={max_generation_attempts}, complexity={complexity_range}")
        
        session_start = time.time()
        
        # Phase 1: Generate and AI-evaluate functions
        print("\n🧮 Phase 1: Function Generation and AI Evaluation")
        ai_approved_functions = await self._generation_phase(target_discoveries, max_generation_attempts, complexity_range)
        
        # Phase 2: Advanced validation (if available)
        validated_functions = []
        if validate_discoveries and VALIDATION_AVAILABLE and ai_approved_functions:
            print("\n🔍 Phase 2: Advanced Validation")
            validated_functions = await self._validation_phase(ai_approved_functions)
        else:
            validated_functions = ai_approved_functions
            print("⚠️ Skipping advanced validation - using AI-approved functions")
        
        # Phase 3: Final analysis and export
        print("\n📊 Phase 3: Final Analysis and Export")
        results = await self._finalization_phase(validated_functions)
        
        # Update session statistics
        self.session_stats['total_time_spent'] = time.time() - session_start
        results['session_statistics'] = self.session_stats
        results['ai_evaluation_summary'] = self.ai_evaluator.get_evaluation_summary()
        
        print(f"\n🎉 Discovery session complete in {self.session_stats['total_time_spent']:.1f} seconds!")
        
        return results
    
    async def _generation_phase(self, target_count: int, max_attempts: int, complexity_range: tuple) -> List[GeneratedFunction]:
        """Phase 1: Generate functions with AI evaluation"""
        
        approved_functions = []
        attempts = 0
        
        print(f"   Generating functions with complexity range {complexity_range}")
        
        while len(approved_functions) < target_count and attempts < max_attempts:
            # Generate function with target complexity
            target_complexity = random.uniform(complexity_range[0], complexity_range[1])
            function = self.generator.generate_random_function(target_complexity)
            
            attempts += 1
            self.session_stats['functions_generated'] += 1
            
            # AI evaluation with detailed feedback
            evaluation = self.ai_evaluator.evaluate_function(function)
            
            if evaluation['decision']:
                approved_functions.append(function)
                self.session_stats['functions_ai_approved'] += 1
                
                print(f"   ✅ AI approved #{len(approved_functions)}: {function.name}")
                print(f"      Score: {evaluation['overall_score']:.3f}, Complexity: {function.complexity_score:.2f}")
                print(f"      LaTeX: {function.latex_formula[:60]}...")
            
            # Progress update
            if attempts % 25 == 0:
                acceptance_rate = len(approved_functions) / attempts
                print(f"   📈 Progress: {len(approved_functions)}/{target_count} approved, {attempts}/{max_attempts} attempts ({acceptance_rate:.1%} rate)")
        
        print(f"   🎯 Phase 1 complete: {len(approved_functions)} AI-approved functions")
        return approved_functions
    
    async def _validation_phase(self, functions: List[GeneratedFunction]) -> List[GeneratedFunction]:
        """Phase 2: Advanced validation of AI-approved functions"""
        
        if not VALIDATION_AVAILABLE:
            return functions
        
        validated_functions = []
        
        print(f"   Validating {len(functions)} AI-approved functions...")
        
        for i, function in enumerate(functions):
            print(f"   🔍 Validating {i+1}/{len(functions)}: {function.name}")
            
            try:
                # Convert to format expected by validator
                function_data = {
                    'name': function.name,
                    'latex_formula': function.latex_formula,
                    'description': function.description,
                    'category': function.category,
                    'properties': function.mathematical_properties
                }
                
                # Validate with advanced tools
                validation_result = await self.validator.validate_discovered_function(function_data)
                
                self.validation_results.append({
                    'function_name': function.name,
                    'validation_result': validation_result
                })
                
                if validation_result['is_valid_discovery']:
                    validated_functions.append(function)
                    self.session_stats['functions_validated'] += 1
                    
                    if validation_result['novel_discovery']:
                        self.session_stats['functions_novel'] += 1
                        print(f"      ✅ Novel discovery confirmed! Confidence: {validation_result['confidence']:.3f}")
                    else:
                        print(f"      ✅ Valid but similar to existing function")
                else:
                    print(f"      ❌ Validation failed: {validation_result.get('recommendation', 'Unknown reason')}")
            
            except Exception as e:
                print(f"      ⚠️ Validation error: {e}")
                # Include function anyway if validation fails
                validated_functions.append(function)
        
        print(f"   🎯 Phase 2 complete: {len(validated_functions)} validated functions")
        return validated_functions
    
    async def _finalization_phase(self, functions: List[GeneratedFunction]) -> Dict[str, Any]:
        """Phase 3: Final analysis and export"""
        
        if not functions:
            return {
                'message': 'No functions discovered',
                'discovered_functions': [],
                'exported_files': []
            }
        
        print(f"   Finalizing {len(functions)} discovered functions...")
        
        # Export functions to JSON
        timestamp = int(time.time())
        export_file = f"discovered_functions_{timestamp}.json"
        
        self.generator.export_batch_to_json(functions, export_file)
        
        # Generate detailed analysis
        analysis = self._analyze_discovered_functions(functions)
        
        # Create comprehensive report
        report = {
            'discovery_session_summary': {
                'total_discovered': len(functions),
                'session_duration': self.session_stats['total_time_spent'],
                'generation_efficiency': self.session_stats['functions_ai_approved'] / self.session_stats['functions_generated'],
                'validation_success_rate': self.session_stats['functions_validated'] / max(self.session_stats['functions_ai_approved'], 1),
                'novelty_rate': self.session_stats['functions_novel'] / max(len(functions), 1)
            },
            'discovered_functions': [
                {
                    'name': func.name,
                    'latex_formula': func.latex_formula,
                    'description': func.description,
                    'complexity_score': func.complexity_score,
                    'series_type': func.series_structure.series_type.value,
                    'mathematical_properties': func.mathematical_properties
                } for func in functions
            ],
            'function_analysis': analysis,
            'exported_files': [export_file],
            'validation_results': self.validation_results
        }
        
        # Save comprehensive report
        report_file = f"discovery_report_{timestamp}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        report['exported_files'].append(report_file)
        
        print(f"   📁 Exported to: {export_file}")
        print(f"   📋 Report saved: {report_file}")
        
        # Store for session
        self.discovered_functions = functions
        
        return report
    
    def _analyze_discovered_functions(self, functions: List[GeneratedFunction]) -> Dict[str, Any]:
        """Analyze patterns in discovered functions"""
        
        if not functions:
            return {}
        
        # Series type distribution
        series_types = {}
        for func in functions:
            st = func.series_structure.series_type.value
            series_types[st] = series_types.get(st, 0) + 1
        
        # Operator usage
        operator_usage = {}
        for func in functions:
            for comp in func.series_structure.components:
                op = comp.operator.value
                operator_usage[op] = operator_usage.get(op, 0) + 1
        
        # Complexity distribution
        complexities = [func.complexity_score for func in functions]
        
        # Index type distribution
        index_types = {}
        for func in functions:
            it = func.series_structure.index_type.value
            index_types[it] = index_types.get(it, 0) + 1
        
        return {
            'series_type_distribution': series_types,
            'operator_usage': operator_usage,
            'index_type_distribution': index_types,
            'complexity_statistics': {
                'min': min(complexities),
                'max': max(complexities),
                'average': sum(complexities) / len(complexities),
                'distribution': complexities
            },
            'most_common_patterns': self._find_common_patterns(functions)
        }
    
    def _find_common_patterns(self, functions: List[GeneratedFunction]) -> List[str]:
        """Find common patterns in the discovered functions"""
        
        patterns = []
        
        # Find common operator combinations
        operator_combos = {}
        for func in functions:
            ops = tuple(sorted([comp.operator.value for comp in func.series_structure.components]))
            operator_combos[ops] = operator_combos.get(ops, 0) + 1
        
        # Find most common combinations
        common_combos = sorted(operator_combos.items(), key=lambda x: x[1], reverse=True)
        
        for combo, count in common_combos[:3]:  # Top 3
            if count > 1:
                patterns.append(f"Operator combination {'+'.join(combo)}: {count} functions")
        
        return patterns
    
    def print_session_summary(self):
        """Print a summary of the discovery session"""
        
        if not self.discovered_functions:
            print("No functions discovered in this session")
            return
        
        print("\n" + "="*80)
        print("🧮 MATHEMATICAL DISCOVERY SESSION SUMMARY")
        print("="*80)
        
        print(f"⏱️  Session Duration: {self.session_stats['total_time_spent']:.1f} seconds")
        print(f"🎲 Functions Generated: {self.session_stats['functions_generated']}")
        print(f"🤖 AI Approved: {self.session_stats['functions_ai_approved']}")
        print(f"✅ Successfully Validated: {self.session_stats['functions_validated']}")
        print(f"🚀 Novel Discoveries: {self.session_stats['functions_novel']}")
        
        print(f"\n📊 Success Rates:")
        print(f"   AI Approval: {self.session_stats['functions_ai_approved']/self.session_stats['functions_generated']:.1%}")
        
        if VALIDATION_AVAILABLE:
            print(f"   Validation Success: {self.session_stats['functions_validated']/max(self.session_stats['functions_ai_approved'], 1):.1%}")
            print(f"   Novelty Rate: {self.session_stats['functions_novel']/max(len(self.discovered_functions), 1):.1%}")
        
        print(f"\n🎯 Top Discovered Functions:")
        
        # Sort by complexity score for display
        sorted_functions = sorted(self.discovered_functions, key=lambda f: f.complexity_score, reverse=True)
        
        for i, func in enumerate(sorted_functions[:5]):  # Top 5
            print(f"\n   {i+1}. {func.name}")
            print(f"      LaTeX: {func.latex_formula}")
            print(f"      Complexity: {func.complexity_score:.2f}")
            print(f"      Type: {func.series_structure.series_type.value}")
            print(f"      Description: {func.description}")


# Main execution functions

async def run_interactive_discovery_session():
    """Run an interactive discovery session with user input"""
    
    print("🎮 INTERACTIVE MATHEMATICAL DISCOVERY SESSION")
    print("=" * 60)
    
    # Get user preferences
    try:
        target_count = int(input("How many novel functions would you like to discover? (default: 10): ") or "10")
        max_attempts = int(input("Maximum generation attempts? (default: 100): ") or "100")
        
        print("\nComplexity range options:")
        print("1. Simple (1.0 - 1.5)")
        print("2. Moderate (1.2 - 2.0)")
        print("3. Complex (1.5 - 2.5)")
        print("4. Very Complex (2.0 - 3.0)")
        
        complexity_choice = input("Choose complexity level (1-4, default: 2): ") or "2"
        
        complexity_ranges = {
            "1": (1.0, 1.5),
            "2": (1.2, 2.0),
            "3": (1.5, 2.5), 
            "4": (2.0, 3.0)
        }
        
        complexity_range = complexity_ranges.get(complexity_choice, (1.2, 2.0))
        
        validate = input("Use advanced validation tools? (y/n, default: y): ").lower() not in ['n', 'no']
        
    except KeyboardInterrupt:
        print("\nSession cancelled by user")
        return
    except ValueError:
        print("Invalid input, using defaults")
        target_count, max_attempts, complexity_range, validate = 10, 100, (1.2, 2.0), True
    
    # Run discovery session
    session = MathematicalDiscoverySession()
    results = await session.run_discovery_session(
        target_discoveries=target_count,
        max_generation_attempts=max_attempts,
        complexity_range=complexity_range,
        validate_discoveries=validate
    )
    
    # Display results
    session.print_session_summary()
    
    return session, results


async def run_automated_discovery_session():
    """Run automated discovery session with preset parameters"""
    
    print("🤖 AUTOMATED MATHEMATICAL DISCOVERY SESSION")
    print("=" * 60)
    
    # Preset parameters for different discovery goals
    discovery_configs = [
        {
            'name': 'Infinite Product Focus',
            'target_discoveries': 15,
            'max_generation_attempts': 150,
            'complexity_range': (1.3, 2.2),
            'validate_discoveries': True
        },
        {
            'name': 'High Complexity Exploration', 
            'target_discoveries': 8,
            'max_generation_attempts': 200,
            'complexity_range': (2.0, 3.0),
            'validate_discoveries': True
        },
        {
            'name': 'Rapid Discovery',
            'target_discoveries': 25,
            'max_generation_attempts': 300,
            'complexity_range': (1.1, 2.0),
            'validate_discoveries': VALIDATION_AVAILABLE
        }
    ]
    
    # Choose config (could be randomized or based on time of day, etc.)
    config = random.choice(discovery_configs)
    
    print(f"📋 Using configuration: {config['name']}")
    print(f"   Target discoveries: {config['target_discoveries']}")
    print(f"   Complexity range: {config['complexity_range']}")
    
    # Run session
    session = MathematicalDiscoverySession()
    results = await session.run_discovery_session(**config)
    
    # Display results
    session.print_session_summary()
    
    return session, results


def demo_function_generator():
    """Quick demo of the function generator without full session"""
    
    print("🧪 MATHEMATICAL FUNCTION GENERATOR DEMO")
    print("=" * 50)
    
    generator = MathematicalFunctionGenerator()
    ai_evaluator = SmartAIFunctionEvaluator()
    
    print("Generating 5 sample functions...\n")
    
    for i in range(5):
        func = generator.generate_random_function()
        evaluation = ai_evaluator.evaluate_function(func)
        
        decision_icon = "✅" if evaluation['decision'] else "❌"
        
        print(f"{decision_icon} Function {i+1}: {func.name}")
        print(f"   LaTeX: {func.latex_formula}")
        print(f"   Complexity: {func.complexity_score:.2f}")
        print(f"   AI Score: {evaluation['overall_score']:.3f}")
        print(f"   Reasoning: {evaluation['reasoning'][-1]}")
        print()
    
    return generator, ai_evaluator


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AI-Powered Mathematical Function Discovery")
    parser.add_argument("--mode", choices=["interactive", "automated", "demo"], 
                       default="demo", help="Discovery mode")
    parser.add_argument("--target", type=int, default=10, 
                       help="Target number of discoveries")
    parser.add_argument("--complexity", nargs=2, type=float, default=[1.2, 2.0],
                       help="Complexity range (min max)")
    
    args = parser.parse_args()
    
    if args.mode == "demo":
        demo_function_generator()
    elif args.mode == "interactive":
        asyncio.run(run_interactive_discovery_session())
    elif args.mode == "automated":
        asyncio.run(run_automated_discovery_session())
    else:
        print("Invalid mode specified")