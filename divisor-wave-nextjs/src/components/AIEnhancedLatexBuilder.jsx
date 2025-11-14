/**
 * AI-Enhanced LaTeX Function Builder
 * Integrates neural networks and AI agents for intelligent formula generation
 */

'use client';

import { useState, useEffect } from 'react';
import { neuralNetworkAPI, agentAPI, integratedAPI } from '@/lib/neural-api';

export default function AIEnhancedLatexBuilder({ 
  isOpen, 
  onClose, 
  onFunctionCreated,
  apiBase = 'http://localhost:8000'
}) {
  const [latexFormula, setLatexFormula] = useState('');
  const [functionName, setFunctionName] = useState('');
  const [description, setDescription] = useState('');
  const [category, setCategory] = useState('ai_generated');
  
  // AI Enhancement States
  const [aiSuggestions, setAiSuggestions] = useState([]);
  const [generatedExpressions, setGeneratedExpressions] = useState([]);
  const [aiInsights, setAiInsights] = useState(null);
  const [conversationHistory, setConversationHistory] = useState([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  
  // AI Settings
  const [aiSettings, setAiSettings] = useState({
    temperature: 1.0,
    numExpressions: 10,
    domain: 'infinite_products',
    enableRealTimeSuggestions: true,
    enableConversationalDiscovery: true
  });

  // Load AI capabilities on mount
  useEffect(() => {
    if (isOpen) {
      checkAIServices();
    }
  }, [isOpen]);

  // Real-time suggestions based on current input
  useEffect(() => {
    if (aiSettings.enableRealTimeSuggestions && latexFormula.length > 3) {
      const debounceTimer = setTimeout(() => {
        getAISuggestions();
      }, 1000);
      
      return () => clearTimeout(debounceTimer);
    }
  }, [latexFormula, aiSettings.enableRealTimeSuggestions]);

  const checkAIServices = async () => {
    try {
      await neuralNetworkAPI.healthCheck();
      console.log('Neural network service connected');
    } catch (error) {
      console.warn('Neural network service not available:', error.message);
    }
  };

  const getAISuggestions = async () => {
    try {
      const suggestions = await neuralNetworkAPI.getLatexSuggestions(latexFormula, {
        domain: aiSettings.domain,
        numSuggestions: 5
      });
      
      if (suggestions.success) {
        setAiSuggestions(suggestions.suggestions);
      }
    } catch (error) {
      console.error('Failed to get AI suggestions:', error);
    }
  };

  const generateLatexExpressions = async () => {
    setIsGenerating(true);
    try {
      const result = await integratedAPI.generateWithExplanation({
        numExpressions: aiSettings.numExpressions,
        temperature: aiSettings.temperature,
        domain: aiSettings.domain,
        seedText: latexFormula || null
      });

      if (result.success) {
        setGeneratedExpressions(result.expressions.map((expr, idx) => ({
          id: idx,
          latex: expr,
          explanation: result.explanations?.[idx] || 'AI-generated mathematical expression',
          confidence: result.confidence_scores?.[idx] || 0.8
        })));
        
        setAiInsights(result.mathematical_analysis);
      } else {
        alert(`Failed to generate expressions: ${result.error}`);
      }
    } catch (error) {
      alert(`Generation failed: ${error.message}`);
    } finally {
      setIsGenerating(false);
    }
  };

  const selectGeneratedExpression = (expression) => {
    setLatexFormula(expression.latex);
    setDescription(expression.explanation);
    
    // Auto-generate function name if not set
    if (!functionName) {
      const name = `ai_gen_${Date.now()}`;
      setFunctionName(name);
    }
  };

  const analyzeCurrentFormula = async () => {
    if (!latexFormula.trim()) {
      alert('Please enter a LaTeX formula first');
      return;
    }

    setIsAnalyzing(true);
    try {
      const insights = await agentAPI.getMathematicalInsights({
        latex_expression: latexFormula,
        context: { domain: aiSettings.domain }
      });

      if (insights.success) {
        setAiInsights(insights.insights);
      }
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const startConversationalDiscovery = async (query) => {
    try {
      const result = await integratedAPI.discoverInteractively(query, conversationHistory);
      
      if (result.success) {
        setConversationHistory(result.context);
        
        // If agent generated LaTeX expressions, add them to suggestions
        if (result.generated_content?.expressions) {
          const newExpressions = result.generated_content.expressions.map((expr, idx) => ({
            id: `conv_${Date.now()}_${idx}`,
            latex: expr,
            explanation: `From conversation: ${result.agent_response}`,
            confidence: 0.9
          }));
          setGeneratedExpressions(prev => [...prev, ...newExpressions]);
        }
        
        return result.agent_response;
      }
    } catch (error) {
      console.error('Conversational discovery failed:', error);
      return `Sorry, I encountered an error: ${error.message}`;
    }
  };

  // Original function creation logic
  const createFunction = async () => {
    if (!functionName.trim() || !latexFormula.trim()) {
      alert('Please provide both function name and LaTeX formula');
      return;
    }

    try {
      const response = await fetch(`${apiBase}/custom-functions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: functionName,
          latex_formula: latexFormula,
          description: description,
          category: category,
          ai_generated: category === 'ai_generated',
          ai_confidence: generatedExpressions.find(e => e.latex === latexFormula)?.confidence || null
        })
      });

      const result = await response.json();

      if (result.success) {
        alert(`✅ AI-enhanced function "${functionName}" created successfully!`);
        
        // Reset form
        setFunctionName('');
        setLatexFormula('');
        setDescription('');
        setGeneratedExpressions([]);
        setAiInsights(null);
        
        if (onFunctionCreated) {
          onFunctionCreated(result.function_data);
        }
        
        onClose();
      } else {
        alert(`❌ Failed to create function: ${result.error || 'Unknown error'}`);
      }
    } catch (error) {
      alert(`❌ Creation failed: ${error.message}`);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-gray-900 border border-white/20 rounded-lg max-w-7xl w-full max-h-[95vh] overflow-y-auto">
        
        {/* Header */}
        <div className="p-6 border-b border-white/10">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                🤖 AI-Enhanced LaTeX Builder
              </h2>
              <p className="text-gray-400 mt-1">Generate and analyze mathematical expressions using neural networks and AI agents</p>
            </div>
            <button onClick={onClose} className="text-gray-400 hover:text-white text-2xl">×</button>
          </div>
        </div>

        <div className="p-6 grid grid-cols-1 lg:grid-cols-4 gap-6">
          
          {/* AI Controls Panel */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-white">🎛️ AI Settings</h3>
            
            <div>
              <label className="block text-sm font-medium text-white mb-2">Domain</label>
              <select 
                value={aiSettings.domain}
                onChange={(e) => setAiSettings(prev => ({...prev, domain: e.target.value}))}
                className="w-full bg-gray-800 border border-gray-600 rounded px-3 py-2 text-white"
              >
                <option value="infinite_products">Infinite Products</option>
                <option value="infinite_sums">Infinite Sums</option>
                <option value="integrals">Integrals</option>
                <option value="special_functions">Special Functions</option>
                <option value="number_theory">Number Theory</option>
                <option value="general">General</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-white mb-2">
                Creativity: {aiSettings.temperature}
              </label>
              <input
                type="range"
                min="0.1"
                max="2.0"
                step="0.1"
                value={aiSettings.temperature}
                onChange={(e) => setAiSettings(prev => ({...prev, temperature: parseFloat(e.target.value)}))}
                className="w-full"
              />
              <div className="text-xs text-gray-400 mt-1">
                Low = Conservative, High = Creative
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-white mb-2">
                Generate: {aiSettings.numExpressions} expressions
              </label>
              <input
                type="range"
                min="1"
                max="20"
                value={aiSettings.numExpressions}
                onChange={(e) => setAiSettings(prev => ({...prev, numExpressions: parseInt(e.target.value)}))}
                className="w-full"
              />
            </div>

            <button
              onClick={generateLatexExpressions}
              disabled={isGenerating}
              className="w-full px-4 py-2 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white rounded transition-colors"
            >
              {isGenerating ? '🔄 Generating...' : '✨ Generate with AI'}
            </button>

            <button
              onClick={analyzeCurrentFormula}
              disabled={isAnalyzing || !latexFormula.trim()}
              className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white rounded transition-colors"
            >
              {isAnalyzing ? '🔄 Analyzing...' : '🔍 Analyze Formula'}
            </button>
          </div>

          {/* Main Input Section */}
          <div className="lg:col-span-2 space-y-6">
            
            {/* Function Details */}
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-white mb-2">Function Name*</label>
                <input
                  type="text"
                  value={functionName}
                  onChange={(e) => setFunctionName(e.target.value)}
                  placeholder="ai_generated_function"
                  className="w-full bg-gray-800 border border-gray-600 rounded px-3 py-2 text-white"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-white mb-2">Description</label>
                <input
                  type="text"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="AI-generated mathematical function"
                  className="w-full bg-gray-800 border border-gray-600 rounded px-3 py-2 text-white"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-white mb-2">Category</label>
                <select 
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  className="w-full bg-gray-800 border border-gray-600 rounded px-3 py-2 text-white"
                >
                  <option value="ai_generated">AI Generated</option>
                  <option value="neural_discovery">Neural Discovery</option>
                  <option value="agent_assisted">Agent Assisted</option>
                  <option value="experimental">Experimental</option>
                </select>
              </div>
            </div>

            {/* LaTeX Formula Input */}
            <div>
              <label className="block text-sm font-medium text-white mb-2">
                LaTeX Formula* <span className="text-gray-400">(use z as the complex variable)</span>
              </label>
              <textarea
                value={latexFormula}
                onChange={(e) => setLatexFormula(e.target.value)}
                placeholder="\\prod_{n=2}^{z} \\sin\\left(\\frac{\\pi z}{n}\\right)"
                rows="6"
                className="w-full bg-gray-800 border border-gray-600 rounded px-3 py-2 text-white font-mono text-sm"
              />
            </div>

            {/* AI Suggestions */}
            {aiSuggestions.length > 0 && (
              <div className="bg-gray-800 border border-blue-500/50 rounded p-4">
                <h4 className="text-blue-300 font-medium mb-2">💡 AI Suggestions:</h4>
                <div className="space-y-2">
                  {aiSuggestions.map((suggestion, idx) => (
                    <button
                      key={idx}
                      onClick={() => setLatexFormula(prev => prev + suggestion)}
                      className="block w-full text-left p-2 bg-blue-900/20 hover:bg-blue-900/40 rounded border border-blue-500/30 text-blue-200 font-mono text-sm"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Formula Preview */}
            <div className="bg-gray-800 border border-gray-600 rounded p-4">
              <h4 className="text-white font-medium mb-2">Formula Preview:</h4>
              <div className="bg-black/30 rounded p-3 font-mono text-green-400 text-sm min-h-[60px]">
                {latexFormula || 'Enter LaTeX formula above or generate with AI...'}
              </div>
            </div>

            {/* AI Insights */}
            {aiInsights && (
              <div className="bg-gray-800 border border-green-500/50 rounded p-4">
                <h4 className="text-green-300 font-medium mb-2">🧠 AI Mathematical Analysis:</h4>
                <div className="text-green-200 text-sm space-y-2">
                  {typeof aiInsights === 'string' ? (
                    <p>{aiInsights}</p>
                  ) : (
                    Object.entries(aiInsights).map(([key, value]) => (
                      <div key={key}>
                        <strong className="capitalize">{key.replace('_', ' ')}:</strong> {value}
                      </div>
                    ))
                  )}
                </div>
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex space-x-4">
              <button
                onClick={createFunction}
                disabled={!functionName.trim() || !latexFormula.trim()}
                className="px-4 py-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 text-white rounded transition-colors"
              >
                ✨ Create AI Function
              </button>
            </div>
          </div>

          {/* Generated Expressions Panel */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-white">🎲 Generated Expressions</h3>
            
            <div className="bg-gray-800 border border-gray-600 rounded p-4 max-h-96 overflow-y-auto">
              {generatedExpressions.length === 0 ? (
                <p className="text-gray-400 text-sm">Click "Generate with AI" to create mathematical expressions</p>
              ) : (
                <div className="space-y-3">
                  {generatedExpressions.map((expr) => (
                    <div key={expr.id} className="border border-gray-600 rounded p-3 hover:border-purple-500/50 transition-colors">
                      <div className="flex justify-between items-start mb-2">
                        <div className="text-xs text-gray-400">
                          Confidence: {(expr.confidence * 100).toFixed(1)}%
                        </div>
                        <button
                          onClick={() => selectGeneratedExpression(expr)}
                          className="text-xs text-purple-300 hover:text-purple-200"
                        >
                          Use This
                        </button>
                      </div>
                      <div className="font-mono text-sm text-white bg-black/30 rounded p-2 mb-2">
                        {expr.latex}
                      </div>
                      <div className="text-xs text-gray-300">
                        {expr.explanation}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Conversational Discovery */}
            <div className="bg-gray-800 border border-gray-600 rounded p-4">
              <h4 className="text-white font-medium mb-2">💬 Ask AI Agent</h4>
              <ConversationalDiscovery onDiscovery={startConversationalDiscovery} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Conversational Discovery Component
function ConversationalDiscovery({ onDiscovery }) {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [isThinking, setIsThinking] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsThinking(true);
    try {
      const result = await onDiscovery(query);
      setResponse(result);
      setQuery('');
    } catch (error) {
      setResponse(`Error: ${error.message}`);
    } finally {
      setIsThinking(false);
    }
  };

  return (
    <div className="space-y-3">
      <form onSubmit={handleSubmit} className="space-y-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask about mathematical patterns..."
          className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white text-sm"
        />
        <button
          type="submit"
          disabled={isThinking || !query.trim()}
          className="w-full px-3 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-600 text-white rounded text-sm transition-colors"
        >
          {isThinking ? '🤔 Thinking...' : '💬 Ask AI'}
        </button>
      </form>
      
      {response && (
        <div className="bg-indigo-900/20 border border-indigo-500/30 rounded p-3">
          <div className="text-indigo-200 text-sm">{response}</div>
        </div>
      )}
    </div>
  );
}