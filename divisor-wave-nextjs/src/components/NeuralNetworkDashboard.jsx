/**
 * Neural Network Dashboard Component
 * Provides interface for all neural network capabilities
 */

'use client';

import { useState, useEffect } from 'react';
import { neuralNetworkAPI, agentAPI, integratedAPI } from '@/lib/neural-api';

export default function NeuralNetworkDashboard({ isOpen, onClose }) {
  const [activeTab, setActiveTab] = useState('latex_gan');
  const [neuralStatus, setNeuralStatus] = useState({ connected: false, models: [] });
  const [agentStatus, setAgentStatus] = useState({ connected: false, capabilities: [] });

  // LaTeX GAN State
  const [latexGeneration, setLatexGeneration] = useState({
    expressions: [],
    isGenerating: false,
    settings: { temperature: 1.0, numExpressions: 10, domain: 'general' }
  });

  // Mathematical GAN State
  const [mathematicalSequences, setMathematicalSequences] = useState({
    sequences: [],
    isGenerating: false,
    settings: { ganType: 'sequence', numSequences: 5, sequenceLength: 100 }
  });

  // Crystal Embeddings State
  const [crystalAnalysis, setCrystalAnalysis] = useState({
    results: null,
    isAnalyzing: false,
    inputData: '',
    embeddingType: 'icosahedral'
  });

  // Agent Conversation State
  const [conversation, setConversation] = useState({
    messages: [],
    isActive: false,
    conversationId: null
  });

  useEffect(() => {
    if (isOpen) {
      checkServices();
    }
  }, [isOpen]);

  const checkServices = async () => {
    try {
      // Check neural network service
      const neuralHealth = await neuralNetworkAPI.healthCheck();
      const models = await neuralNetworkAPI.getAvailableModels();
      setNeuralStatus({ connected: true, models: models.models || [] });
      
      // Check agent service
      const agentCapabilities = await agentAPI.getAgentCapabilities();
      setAgentStatus({ connected: true, capabilities: agentCapabilities.capabilities || [] });
    } catch (error) {
      console.error('Service check failed:', error);
    }
  };

  const generateLatexExpressions = async () => {
    setLatexGeneration(prev => ({ ...prev, isGenerating: true }));
    try {
      const result = await integratedAPI.generateWithExplanation(latexGeneration.settings);
      
      if (result.success) {
        setLatexGeneration(prev => ({
          ...prev,
          expressions: result.expressions.map((expr, idx) => ({
            id: idx,
            latex: expr,
            explanation: result.explanations?.[idx] || 'AI-generated expression',
            confidence: result.confidence_scores?.[idx] || 0.8,
            analysis: result.mathematical_analysis
          })),
          isGenerating: false
        }));
      }
    } catch (error) {
      console.error('LaTeX generation failed:', error);
      setLatexGeneration(prev => ({ ...prev, isGenerating: false }));
    }
  };

  const generateMathematicalSequences = async () => {
    setMathematicalSequences(prev => ({ ...prev, isGenerating: true }));
    try {
      const result = await neuralNetworkAPI.generateMathematicalSequences(mathematicalSequences.settings);
      
      if (result.success) {
        setMathematicalSequences(prev => ({
          ...prev,
          sequences: result.sequences.map((seq, idx) => ({
            id: idx,
            data: seq,
            type: result.sequence_types?.[idx] || 'general',
            properties: result.mathematical_properties?.[idx] || {}
          })),
          isGenerating: false
        }));
      }
    } catch (error) {
      console.error('Sequence generation failed:', error);
      setMathematicalSequences(prev => ({ ...prev, isGenerating: false }));
    }
  };

  const analyzeCrystalPatterns = async () => {
    if (!crystalAnalysis.inputData.trim()) {
      alert('Please provide mathematical data to analyze');
      return;
    }

    setCrystalAnalysis(prev => ({ ...prev, isAnalyzing: true }));
    try {
      const data = JSON.parse(crystalAnalysis.inputData);
      const result = await neuralNetworkAPI.analyzeCrystalPatterns(data, crystalAnalysis.embeddingType);
      
      setCrystalAnalysis(prev => ({
        ...prev,
        results: result,
        isAnalyzing: false
      }));
    } catch (error) {
      console.error('Crystal analysis failed:', error);
      setCrystalAnalysis(prev => ({ ...prev, isAnalyzing: false }));
      alert('Failed to analyze data. Please check your input format.');
    }
  };

  const startConversation = async () => {
    try {
      const conv = await agentAPI.startConversation('mathematical_discovery');
      
      // Check if LlamaIndex is enabled or we're in demo mode
      const welcomeMessage = conv.llama_index_enabled 
        ? conv.welcome_message
        : '🤖 Demo Mode: I\'m running with limited AI capabilities. To enable full LlamaIndex agents, please configure the LLM integration (see console logs for details).';
      
      setConversation({
        messages: [{ 
          type: 'system', 
          content: welcomeMessage,
          capabilities: conv.available_capabilities || []
        }],
        isActive: true,
        conversationId: conv.conversation_id,
        llamaIndexEnabled: conv.llama_index_enabled || false
      });
      
      console.log('Conversation started:', {
        llamaIndexEnabled: conv.llama_index_enabled,
        capabilities: conv.available_capabilities
      });
    } catch (error) {
      console.error('Failed to start conversation:', error);
      // Fallback to offline mode
      setConversation({
        messages: [{ 
          type: 'system', 
          content: '⚠️ Unable to connect to AI Agent server. Please check if the agent API is running on port 8002.'
        }],
        isActive: true,
        conversationId: 'offline',
        llamaIndexEnabled: false
      });
    }
  };

  const sendMessage = async (message) => {
    if (!conversation.conversationId || !message.trim()) return;

    const userMessage = { type: 'user', content: message };
    setConversation(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage]
    }));

    try {
      const response = await agentAPI.sendMessage(conversation.conversationId, message);
      const agentMessage = { 
        type: 'agent', 
        content: response.message,
        generatedContent: response.generated_content 
      };
      
      setConversation(prev => ({
        ...prev,
        messages: [...prev.messages, agentMessage]
      }));
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-gray-900 border border-white/20 rounded-lg max-w-7xl w-full max-h-[95vh] overflow-hidden flex flex-col">
        
        {/* Header */}
        <div className="p-6 border-b border-white/10">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                🧠 Neural Network Dashboard
              </h2>
              <p className="text-gray-400 mt-1">Access all AI-powered mathematical discovery tools</p>
            </div>
            <button onClick={onClose} className="text-gray-400 hover:text-white text-2xl">×</button>
          </div>
          
          {/* Service Status */}
          <div className="mt-4 flex gap-4">
            <div className={`px-3 py-1 rounded text-sm ${neuralStatus.connected ? 'bg-green-900/20 text-green-300' : 'bg-red-900/20 text-red-300'}`}>
              Neural Networks: {neuralStatus.connected ? '✅ Connected' : '❌ Disconnected'}
            </div>
            <div className={`px-3 py-1 rounded text-sm ${agentStatus.connected ? 'bg-green-900/20 text-green-300' : 'bg-red-900/20 text-red-300'}`}>
              AI Agents: {agentStatus.connected ? '✅ Connected' : '❌ Disconnected'}
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="border-b border-white/10">
          <nav className="flex">
            {[
              { id: 'latex_gan', label: '📝 LaTeX GAN', icon: '🤖' },
              { id: 'math_sequences', label: '🔢 Math Sequences', icon: '📊' },
              { id: 'crystal_analysis', label: '💎 Crystal Analysis', icon: '🔬' },
              { id: 'ai_conversation', label: '💬 AI Chat', icon: '🗣️' }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-6 py-3 font-medium transition-colors ${
                  activeTab === tab.id
                    ? 'text-white border-b-2 border-blue-500 bg-blue-900/20'
                    : 'text-gray-400 hover:text-white hover:bg-gray-800/50'
                }`}
              >
                {tab.icon} {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="flex-1 overflow-y-auto p-6">
          
          {/* LaTeX GAN Tab */}
          {activeTab === 'latex_gan' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                
                {/* Controls */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-white">Generation Settings</h3>
                  
                  <div>
                    <label className="block text-sm font-medium text-white mb-2">Domain</label>
                    <select 
                      value={latexGeneration.settings.domain}
                      onChange={(e) => setLatexGeneration(prev => ({
                        ...prev,
                        settings: { ...prev.settings, domain: e.target.value }
                      }))}
                      className="w-full bg-gray-800 border border-gray-600 rounded px-3 py-2 text-white"
                    >
                      <option value="infinite_products">Infinite Products</option>
                      <option value="infinite_sums">Infinite Sums</option>
                      <option value="integrals">Integrals</option>
                      <option value="special_functions">Special Functions</option>
                      <option value="general">General</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-white mb-2">
                      Temperature: {latexGeneration.settings.temperature}
                    </label>
                    <input
                      type="range"
                      min="0.1"
                      max="2.0"
                      step="0.1"
                      value={latexGeneration.settings.temperature}
                      onChange={(e) => setLatexGeneration(prev => ({
                        ...prev,
                        settings: { ...prev.settings, temperature: parseFloat(e.target.value) }
                      }))}
                      className="w-full"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-white mb-2">
                      Count: {latexGeneration.settings.numExpressions}
                    </label>
                    <input
                      type="range"
                      min="1"
                      max="20"
                      value={latexGeneration.settings.numExpressions}
                      onChange={(e) => setLatexGeneration(prev => ({
                        ...prev,
                        settings: { ...prev.settings, numExpressions: parseInt(e.target.value) }
                      }))}
                      className="w-full"
                    />
                  </div>

                  <button
                    onClick={generateLatexExpressions}
                    disabled={latexGeneration.isGenerating || !neuralStatus.connected}
                    className="w-full px-4 py-2 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white rounded transition-colors"
                  >
                    {latexGeneration.isGenerating ? '🔄 Generating...' : '✨ Generate LaTeX'}
                  </button>
                </div>

                {/* Results */}
                <div className="lg:col-span-2">
                  <h3 className="text-lg font-semibold text-white mb-4">Generated Expressions</h3>
                  <div className="space-y-4 max-h-96 overflow-y-auto">
                    {latexGeneration.expressions.map((expr) => (
                      <div key={expr.id} className="bg-gray-800 border border-gray-600 rounded p-4">
                        <div className="flex justify-between items-start mb-2">
                          <div className="text-xs text-gray-400">
                            Confidence: {(expr.confidence * 100).toFixed(1)}%
                          </div>
                          <button className="text-xs text-blue-300 hover:text-blue-200">
                            Copy LaTeX
                          </button>
                        </div>
                        <div className="font-mono text-sm text-white bg-black/30 rounded p-3 mb-2">
                          {expr.latex}
                        </div>
                        <div className="text-xs text-gray-300">
                          {expr.explanation}
                        </div>
                      </div>
                    ))}
                    {latexGeneration.expressions.length === 0 && (
                      <div className="text-gray-400 text-center py-8">
                        Click "Generate LaTeX" to create mathematical expressions
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Mathematical Sequences Tab */}
          {activeTab === 'math_sequences' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                
                {/* Controls */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-white">Sequence Generation</h3>
                  
                  <div>
                    <label className="block text-sm font-medium text-white mb-2">GAN Type</label>
                    <select 
                      value={mathematicalSequences.settings.ganType}
                      onChange={(e) => setMathematicalSequences(prev => ({
                        ...prev,
                        settings: { ...prev.settings, ganType: e.target.value }
                      }))}
                      className="w-full bg-gray-800 border border-gray-600 rounded px-3 py-2 text-white"
                    >
                      <option value="sequence">General Sequence</option>
                      <option value="riemann">Riemann GAN</option>
                      <option value="prime">Prime GAN</option>
                      <option value="infinite_product">Infinite Product GAN</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-white mb-2">
                      Sequences: {mathematicalSequences.settings.numSequences}
                    </label>
                    <input
                      type="range"
                      min="1"
                      max="10"
                      value={mathematicalSequences.settings.numSequences}
                      onChange={(e) => setMathematicalSequences(prev => ({
                        ...prev,
                        settings: { ...prev.settings, numSequences: parseInt(e.target.value) }
                      }))}
                      className="w-full"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-white mb-2">
                      Length: {mathematicalSequences.settings.sequenceLength}
                    </label>
                    <input
                      type="range"
                      min="50"
                      max="500"
                      step="50"
                      value={mathematicalSequences.settings.sequenceLength}
                      onChange={(e) => setMathematicalSequences(prev => ({
                        ...prev,
                        settings: { ...prev.settings, sequenceLength: parseInt(e.target.value) }
                      }))}
                      className="w-full"
                    />
                  </div>

                  <button
                    onClick={generateMathematicalSequences}
                    disabled={mathematicalSequences.isGenerating || !neuralStatus.connected}
                    className="w-full px-4 py-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 text-white rounded transition-colors"
                  >
                    {mathematicalSequences.isGenerating ? '🔄 Generating...' : '📊 Generate Sequences'}
                  </button>
                </div>

                {/* Results */}
                <div className="lg:col-span-2">
                  <h3 className="text-lg font-semibold text-white mb-4">Generated Sequences</h3>
                  <div className="space-y-4 max-h-96 overflow-y-auto">
                    {mathematicalSequences.sequences.map((seq) => (
                      <div key={seq.id} className="bg-gray-800 border border-gray-600 rounded p-4">
                        <div className="flex justify-between items-start mb-2">
                          <div className="text-sm text-gray-300">
                            Type: {seq.type}
                          </div>
                          <button className="text-xs text-blue-300 hover:text-blue-200">
                            Export Data
                          </button>
                        </div>
                        <div className="font-mono text-xs text-white bg-black/30 rounded p-3 mb-2 overflow-x-auto">
                          [{seq.data.slice(0, 20).map(x => x.toFixed(4)).join(', ')}...]
                        </div>
                        <div className="text-xs text-gray-300">
                          Length: {seq.data.length} | First few values shown
                        </div>
                      </div>
                    ))}
                    {mathematicalSequences.sequences.length === 0 && (
                      <div className="text-gray-400 text-center py-8">
                        Click "Generate Sequences" to create mathematical sequences
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Crystal Analysis Tab */}
          {activeTab === 'crystal_analysis' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                
                {/* Input */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-white">Crystal Pattern Analysis</h3>
                  
                  <div>
                    <label className="block text-sm font-medium text-white mb-2">Embedding Type</label>
                    <select 
                      value={crystalAnalysis.embeddingType}
                      onChange={(e) => setCrystalAnalysis(prev => ({
                        ...prev,
                        embeddingType: e.target.value
                      }))}
                      className="w-full bg-gray-800 border border-gray-600 rounded px-3 py-2 text-white"
                    >
                      <option value="icosahedral">Icosahedral (20-fold)</option>
                      <option value="tetrahedral">Tetrahedral (4-fold)</option>
                      <option value="cubic">Cubic (6-fold)</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-white mb-2">
                      Mathematical Data (JSON format)
                    </label>
                    <textarea
                      value={crystalAnalysis.inputData}
                      onChange={(e) => setCrystalAnalysis(prev => ({
                        ...prev,
                        inputData: e.target.value
                      }))}
                      placeholder='[1, 0.5, 0.25, 0.125, ...] or [[1,2], [3,4], ...]'
                      rows="8"
                      className="w-full bg-gray-800 border border-gray-600 rounded px-3 py-2 text-white font-mono text-sm"
                    />
                  </div>

                  <button
                    onClick={analyzeCrystalPatterns}
                    disabled={crystalAnalysis.isAnalyzing || !neuralStatus.connected}
                    className="w-full px-4 py-2 bg-orange-600 hover:bg-orange-700 disabled:bg-gray-600 text-white rounded transition-colors"
                  >
                    {crystalAnalysis.isAnalyzing ? '🔄 Analyzing...' : '💎 Analyze Patterns'}
                  </button>
                </div>

                {/* Results */}
                <div>
                  <h3 className="text-lg font-semibold text-white mb-4">Analysis Results</h3>
                  {crystalAnalysis.results ? (
                    <div className="bg-gray-800 border border-orange-500/50 rounded p-4">
                      <div className="space-y-3 text-sm">
                        {Object.entries(crystalAnalysis.results).map(([key, value]) => (
                          <div key={key}>
                            <div className="text-orange-300 font-medium capitalize">
                              {key.replace('_', ' ')}:
                            </div>
                            <div className="text-gray-300 ml-4">
                              {typeof value === 'object' ? JSON.stringify(value, null, 2) : String(value)}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  ) : (
                    <div className="text-gray-400 text-center py-8">
                      Provide mathematical data and click "Analyze Patterns"
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* AI Conversation Tab */}
          {activeTab === 'ai_conversation' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 lg:grid-cols-1 gap-6">
                
                {/* Conversation Area */}
                <div>
                  <div className="flex justify-between items-center mb-4">
                    <div>
                      <h3 className="text-lg font-semibold text-white">AI Mathematical Agent</h3>
                      <div className="text-sm text-gray-400 mt-1">
                        {agentStatus.connected ? (
                          <span className="text-green-400">
                            ✅ LlamaIndex Agents: Connected & Ready
                          </span>
                        ) : (
                          <span className="text-yellow-400">
                            ⚠️ Demo Mode: LlamaIndex setup required for full AI
                          </span>
                        )}
                      </div>
                    </div>
                    {!conversation.isActive && (
                      <button
                        onClick={startConversation}
                        className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded transition-colors flex items-center gap-2"
                      >
                        💬 Start Conversation
                        {!agentStatus.connected && (
                          <span className="text-xs bg-yellow-600 px-1 rounded">Demo</span>
                        )}
                      </button>
                    )}
                  </div>
                  
                  {/* Messages */}
                  <div className="bg-gray-800 border border-gray-600 rounded p-4 h-96 overflow-y-auto mb-4">
                    {conversation.messages.map((msg, idx) => (
                      <div key={idx} className={`mb-4 ${msg.type === 'user' ? 'text-right' : 'text-left'}`}>
                        <div className={`inline-block p-3 rounded max-w-[80%] ${
                          msg.type === 'user' 
                            ? 'bg-blue-600 text-white' 
                            : msg.type === 'system'
                            ? 'bg-gray-700 text-gray-300'
                            : 'bg-indigo-600 text-white'
                        }`}>
                          {msg.content}
                        </div>
                        {msg.generatedContent && (
                          <div className="mt-2 text-xs text-gray-400">
                            Generated: {JSON.stringify(msg.generatedContent)}
                          </div>
                        )}
                      </div>
                    ))}
                    {conversation.messages.length === 0 && (
                      <div className="text-gray-400 text-center py-8">
                        Start a conversation to begin mathematical discovery
                      </div>
                    )}
                  </div>
                  
                  {/* Input */}
                  {conversation.isActive && (
                    <ConversationInput onSendMessage={sendMessage} />
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// Conversation Input Component
function ConversationInput({ onSendMessage }) {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim()) {
      onSendMessage(message);
      setMessage('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Ask about mathematical patterns, formulas, or discoveries..."
        className="flex-1 bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white"
      />
      <button
        type="submit"
        disabled={!message.trim()}
        className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-600 text-white rounded transition-colors"
      >
        Send
      </button>
    </form>
  );
}