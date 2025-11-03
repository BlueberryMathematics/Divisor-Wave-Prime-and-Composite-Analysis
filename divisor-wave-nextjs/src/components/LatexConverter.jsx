/*
Enhanced Next.js component for LaTeX to NumPy conversion
Provides UI for researchers to input mathematical formulas and convert them
*/

import React, { useState, useEffect } from 'react';
import axios from 'axios';

const LatexConverter = () => {
  const [latexInput, setLatexInput] = useState('');
  const [functionName, setFunctionName] = useState('');
  const [description, setDescription] = useState('');
  const [conversionResult, setConversionResult] = useState(null);
  const [patterns, setPatterns] = useState({});
  const [databaseFunctions, setDatabaseFunctions] = useState([]);
  const [selectedExample, setSelectedExample] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const API_BASE = 'http://localhost:8000';

  // Load supported patterns and examples on component mount
  useEffect(() => {
    loadPatterns();
    loadDatabaseFunctions();
  }, []);

  const loadPatterns = async () => {
    try {
      const response = await axios.get(`${API_BASE}/latex-patterns`);
      setPatterns(response.data);
    } catch (err) {
      console.error('Failed to load patterns:', err);
    }
  };

  const loadDatabaseFunctions = async () => {
    try {
      const response = await axios.get(`${API_BASE}/database/list`);
      setDatabaseFunctions(response.data.functions || {});
    } catch (err) {
      console.error('Failed to load database functions:', err);
    }
  };

  const handleExampleSelect = (exampleFormula) => {
    setLatexInput(exampleFormula);
    setSelectedExample(exampleFormula);
  };

  const convertLatexToNumpy = async () => {
    if (!latexInput.trim() || !functionName.trim()) {
      setError('Please provide both LaTeX formula and function name');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const response = await axios.post(`${API_BASE}/latex-to-numpy`, {
        latex_formula: latexInput,
        function_name: functionName,
        description: description,
        custom_parameters: {}
      });

      setConversionResult(response.data);
      
      // Refresh database functions list
      await loadDatabaseFunctions();
      
      // Clear form
      setLatexInput('');
      setFunctionName('');
      setDescription('');
      
    } catch (err) {
      setError(err.response?.data?.detail || 'Conversion failed');
    } finally {
      setIsLoading(false);
    }
  };

  const exportDatabase = async () => {
    try {
      const exportPath = `./formula_database_export_${Date.now()}.json`;
      await axios.post(`${API_BASE}/database/export`, {
        export_path: exportPath
      });
      alert(`Database exported to ${exportPath}`);
    } catch (err) {
      alert('Export failed: ' + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6 bg-gray-900 text-white rounded-lg">
      <h1 className="text-3xl font-bold mb-6 text-center">
        LaTeX to NumPy Converter
      </h1>
      <p className="text-gray-300 mb-8 text-center">
        Convert mathematical LaTeX formulas to executable NumPy code for research
      </p>

      {/* Examples Section */}
      <div className="mb-8 p-4 bg-gray-800 rounded-lg">
        <h3 className="text-xl font-semibold mb-4">Example Formulas</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {patterns.examples && Object.entries(patterns.examples).map(([key, formula]) => (
            <div key={key} className="p-3 bg-gray-700 rounded cursor-pointer hover:bg-gray-600"
                 onClick={() => handleExampleSelect(formula)}>
              <div className="font-semibold text-blue-300">{key.replace('_', ' ').toUpperCase()}</div>
              <div className="text-sm font-mono text-gray-300">{formula}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Input Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* LaTeX Input */}
        <div className="space-y-4">
          <h3 className="text-xl font-semibold">Create New Function</h3>
          
          <div>
            <label className="block text-sm font-medium mb-2">LaTeX Formula</label>
            <textarea
              value={latexInput}
              onChange={(e) => setLatexInput(e.target.value)}
              className="w-full p-3 bg-gray-800 border border-gray-600 rounded-lg font-mono"
              rows="4"
              placeholder="Enter LaTeX formula (e.g., \\prod_{k=2}^x \\sin\\left(\\frac{\\pi z}{k}\\right))"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Function Name</label>
            <input
              type="text"
              value={functionName}
              onChange={(e) => setFunctionName(e.target.value)}
              className="w-full p-3 bg-gray-800 border border-gray-600 rounded-lg"
              placeholder="my_custom_function"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Description (Optional)</label>
            <input
              type="text"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full p-3 bg-gray-800 border border-gray-600 rounded-lg"
              placeholder="Description of your mathematical function"
            />
          </div>

          <button
            onClick={convertLatexToNumpy}
            disabled={isLoading}
            className="w-full py-3 px-6 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 rounded-lg font-semibold"
          >
            {isLoading ? 'Converting...' : 'Convert to NumPy'}
          </button>

          {error && (
            <div className="p-4 bg-red-900 border border-red-600 rounded-lg text-red-200">
              {error}
            </div>
          )}
        </div>

        {/* Database Functions */}
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-xl font-semibold">Saved Functions</h3>
            <button
              onClick={exportDatabase}
              className="px-4 py-2 bg-green-600 hover:bg-green-700 rounded-lg text-sm"
            >
              Export Database
            </button>
          </div>

          <div className="max-h-96 overflow-y-auto space-y-2">
            {Object.entries(databaseFunctions).map(([name, data]) => (
              <div key={name} className="p-3 bg-gray-800 rounded-lg border border-gray-600">
                <div className="font-semibold text-blue-300">{name}</div>
                <div className="text-sm text-gray-300">{data.description}</div>
                <div className="text-xs text-gray-400 font-mono mt-1">
                  Pattern: {data.pattern_type}
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  {data.latex_formula}
                </div>
              </div>
            ))}
          </div>

          {Object.keys(databaseFunctions).length === 0 && (
            <div className="text-center text-gray-400 py-8">
              No saved functions yet. Create your first function above!
            </div>
          )}
        </div>
      </div>

      {/* Conversion Result */}
      {conversionResult && (
        <div className="mt-8 p-6 bg-gray-800 rounded-lg border border-green-600">
          <h3 className="text-xl font-semibold text-green-300 mb-4">
            ✅ Conversion Successful!
          </h3>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <h4 className="font-semibold mb-2">Function Details</h4>
              <div className="space-y-2 text-sm">
                <div><span className="text-gray-400">Name:</span> {conversionResult.function_name}</div>
                <div><span className="text-gray-400">Pattern:</span> {conversionResult.pattern_type}</div>
                <div><span className="text-gray-400">Saved:</span> {conversionResult.saved_to_database ? '✅' : '❌'}</div>
              </div>
            </div>

            <div>
              <h4 className="font-semibold mb-2">Generated NumPy Code</h4>
              <pre className="text-xs bg-gray-900 p-3 rounded border overflow-x-auto">
                <code>{conversionResult.numpy_code}</code>
              </pre>
            </div>
          </div>

          <div className="mt-4">
            <h4 className="font-semibold mb-2">Complete Function</h4>
            <pre className="text-xs bg-gray-900 p-3 rounded border overflow-x-auto max-h-40">
              <code>{conversionResult.executable_function}</code>
            </pre>
          </div>
        </div>
      )}

      {/* Usage Instructions */}
      <div className="mt-8 p-4 bg-gray-800 rounded-lg">
        <h3 className="text-lg font-semibold mb-3">How to Use</h3>
        <ol className="list-decimal list-inside space-y-2 text-sm text-gray-300">
          <li>Choose an example formula or write your own LaTeX mathematical expression</li>
          <li>Provide a unique function name (no spaces, use underscores)</li>
          <li>Add an optional description to document your function</li>
          <li>Click "Convert to NumPy" to generate executable code</li>
          <li>Your function is automatically saved to the local database</li>
          <li>Export your database to share with other researchers</li>
          <li>All functions integrate with the plotting system automatically</li>
        </ol>
      </div>
    </div>
  );
};

export default LatexConverter;