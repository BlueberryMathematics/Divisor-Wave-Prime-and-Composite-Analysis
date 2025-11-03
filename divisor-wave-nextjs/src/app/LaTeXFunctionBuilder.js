/**
 * LaTeX Function Builder Component
 * Allows users to create custom mathematical functions using LaTeX notation
 */

'use client';

import { useState, useEffect } from 'react';

export default function LaTeXFunctionBuilder({ 
  isOpen, 
  onClose, 
  onFunctionCreated,
  apiBase = 'http://localhost:8000' 
}) {
  const [latexFormula, setLatexFormula] = useState('');
  const [functionName, setFunctionName] = useState('');
  const [description, setDescription] = useState('');
  const [category, setCategory] = useState('custom');
  const [isCreating, setIsCreating] = useState(false);
  const [isTesting, setIsTesting] = useState(false);
  const [testResult, setTestResult] = useState(null);
  const [symbols, setSymbols] = useState({});
  const [activeSymbolCategory, setActiveSymbolCategory] = useState('Functions');

  // Load LaTeX symbols on mount
  useEffect(() => {
    if (isOpen) {
      loadLatexSymbols();
    }
  }, [isOpen]);

  const loadLatexSymbols = async () => {
    try {
      const response = await fetch(`${apiBase}/latex-symbols`);
      const data = await response.json();
      if (data.success) {
        setSymbols(data.symbols);
      }
    } catch (error) {
      console.error('Failed to load LaTeX symbols:', error);
    }
  };

  const insertSymbol = (latexCode) => {
    setLatexFormula(prev => prev + latexCode);
  };

  const testFunction = async () => {
    if (!latexFormula.trim()) {
      alert('Please enter a LaTeX formula first');
      return;
    }

    setIsTesting(true);
    setTestResult(null);

    try {
      const response = await fetch(`${apiBase}/test-latex`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: functionName || 'test_function',
          latex_formula: latexFormula,
          description: description,
          category: category
        })
      });

      const result = await response.json();
      setTestResult(result);

      if (result.success) {
        alert('✅ Function test passed! Ready to create.');
      } else {
        alert(`❌ Function test failed: ${result.error}`);
      }

    } catch (error) {
      setTestResult({
        success: false,
        error: error.message
      });
      alert(`❌ Test failed: ${error.message}`);
    } finally {
      setIsTesting(false);
    }
  };

  const createFunction = async () => {
    if (!functionName.trim() || !latexFormula.trim()) {
      alert('Please provide both function name and LaTeX formula');
      return;
    }

    setIsCreating(true);

    try {
      const response = await fetch(`${apiBase}/custom-functions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: functionName,
          latex_formula: latexFormula,
          description: description,
          category: category
        })
      });

      const result = await response.json();

      if (result.success) {
        alert(`✅ Custom function "${functionName}" created successfully!`);
        
        // Reset form
        setFunctionName('');
        setLatexFormula('');
        setDescription('');
        setTestResult(null);
        
        // Notify parent component
        if (onFunctionCreated) {
          onFunctionCreated(result.function_data);
        }
        
        onClose();
      } else {
        alert(`❌ Failed to create function: ${result.error || 'Unknown error'}`);
      }

    } catch (error) {
      alert(`❌ Creation failed: ${error.message}`);
    } finally {
      setIsCreating(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-gray-900 border border-white/20 rounded-lg max-w-6xl w-full max-h-[90vh] overflow-y-auto">
        
        {/* Header */}
        <div className="p-6 border-b border-white/10">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-white">LaTeX Function Builder</h2>
              <p className="text-gray-400 mt-1">Create custom mathematical functions using LaTeX notation</p>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white text-2xl"
            >
              ×
            </button>
          </div>
        </div>

        <div className="p-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* LaTeX Input Section */}
          <div className="lg:col-span-2 space-y-6">
            
            {/* Function Details */}
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-white mb-2">
                  Function Name*
                </label>
                <input
                  type="text"
                  value={functionName}
                  onChange={(e) => setFunctionName(e.target.value)}
                  placeholder="my_custom_function"
                  className="w-full bg-gray-800 border border-gray-600 rounded px-3 py-2 text-white"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-white mb-2">
                  Description
                </label>
                <input
                  type="text"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Description of your custom function"
                  className="w-full bg-gray-800 border border-gray-600 rounded px-3 py-2 text-white"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-white mb-2">
                  Category
                </label>
                <select 
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  className="w-full bg-gray-800 border border-gray-600 rounded px-3 py-2 text-white"
                >
                  <option value="custom">Custom</option>
                  <option value="experimental">Experimental</option>
                  <option value="research">Research</option>
                  <option value="educational">Educational</option>
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

            {/* Preview and Test */}
            <div className="bg-gray-800 border border-gray-600 rounded p-4">
              <h4 className="text-white font-medium mb-2">Formula Preview:</h4>
              <div className="bg-black/30 rounded p-3 font-mono text-green-400 text-sm">
                {latexFormula || 'Enter LaTeX formula above...'}
              </div>
            </div>

            {/* Test Results */}
            {testResult && (
              <div className={`border rounded p-4 ${
                testResult.success 
                  ? 'bg-green-900/20 border-green-500/50' 
                  : 'bg-red-900/20 border-red-500/50'
              }`}>
                <h4 className={`font-medium mb-2 ${
                  testResult.success ? 'text-green-300' : 'text-red-300'
                }`}>
                  Test Result: {testResult.success ? '✅ Passed' : '❌ Failed'}
                </h4>
                
                {testResult.success && testResult.test_result && (
                  <div className="space-y-2 text-sm">
                    <div className="text-green-200">
                      <strong>Sample Results:</strong>
                    </div>
                    {testResult.test_result.test_results?.map((result, index) => (
                      <div key={index} className="text-green-300 font-mono">
                        f({result.input}) = {result.output.toFixed(4)}
                      </div>
                    ))}
                  </div>
                )}
                
                {!testResult.success && (
                  <div className="text-red-300 text-sm">
                    <strong>Error:</strong> {testResult.error}
                  </div>
                )}
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex space-x-4">
              <button
                onClick={testFunction}
                disabled={isTesting || !latexFormula.trim()}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white rounded transition-colors"
              >
                {isTesting ? '🔄 Testing...' : '🧪 Test Function'}
              </button>
              
              <button
                onClick={createFunction}
                disabled={isCreating || !functionName.trim() || !latexFormula.trim()}
                className="px-4 py-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 text-white rounded transition-colors"
              >
                {isCreating ? '🔄 Creating...' : '✨ Create Function'}
              </button>
            </div>
          </div>

          {/* Symbol Palette */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-white">LaTeX Symbol Palette</h3>
            
            {/* Category Tabs */}
            <div className="flex flex-wrap gap-2">
              {Object.keys(symbols).map(category => (
                <button
                  key={category}
                  onClick={() => setActiveSymbolCategory(category)}
                  className={`px-3 py-1 rounded text-sm transition-colors ${
                    activeSymbolCategory === category
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                  }`}
                >
                  {category}
                </button>
              ))}
            </div>

            {/* Symbol Grid */}
            <div className="bg-gray-800 border border-gray-600 rounded p-4 max-h-96 overflow-y-auto">
              {symbols[activeSymbolCategory] && (
                <div className="grid grid-cols-2 gap-2">
                  {Object.entries(symbols[activeSymbolCategory]).map(([symbol, latex]) => (
                    <button
                      key={symbol}
                      onClick={() => insertSymbol(latex)}
                      className="p-2 bg-gray-700 hover:bg-gray-600 rounded border border-gray-600 text-white text-sm transition-colors"
                      title={`Insert: ${latex}`}
                    >
                      <div className="font-bold">{symbol}</div>
                      <div className="text-xs text-gray-400 font-mono">{latex}</div>
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Usage Examples */}
            <div className="bg-gray-800 border border-gray-600 rounded p-4">
              <h4 className="text-white font-medium mb-2">Examples:</h4>
              <div className="space-y-2 text-xs">
                <div className="text-gray-300">
                  <strong>Product:</strong><br/>
                  <code className="text-green-400">\prod_&#123;n=2&#125;^&#123;z&#125; \sin(\pi z/n)</code>
                </div>
                <div className="text-gray-300">
                  <strong>Sum:</strong><br/>
                  <code className="text-green-400">\sum_&#123;n=1&#125;^&#123;\infty&#125; 1/n^z</code>
                </div>
                <div className="text-gray-300">
                  <strong>Fraction:</strong><br/>
                  <code className="text-green-400">\frac&#123;\sin(\pi z)&#125;&#123;z&#125;</code>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}