"use client";

import CompactCalculator from './compact-calculator';
import AIEnhancedLatexBuilder from '@/components/AIEnhancedLatexBuilder';
import NeuralNetworkDashboard from '@/components/NeuralNetworkDashboard';
import { useState } from 'react';

export function AIIntegratedPage() {
  const [showAIBuilder, setShowAIBuilder] = useState(false);
  const [showNeuralDashboard, setShowNeuralDashboard] = useState(false);

  return (
    <div className="min-h-screen bg-gray-950">
      {/* AI Enhancement Bar */}
      <div className="bg-gradient-to-r from-purple-900/20 to-blue-900/20 border-b border-white/10 p-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-white">🧠 AI-Enhanced Divisor Wave Analysis</h1>
            <p className="text-gray-400 text-sm">Neural networks and AI agents for mathematical discovery</p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={() => setShowAIBuilder(true)}
              className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded transition-colors flex items-center gap-2"
            >
              ✨ AI LaTeX Builder
            </button>
            <button
              onClick={() => setShowNeuralDashboard(true)}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors flex items-center gap-2"
            >
              🧠 Neural Dashboard
            </button>
          </div>
        </div>
      </div>

      {/* Main Calculator */}
      <CompactCalculator />

      {/* AI Components */}
      <AIEnhancedLatexBuilder
        isOpen={showAIBuilder}
        onClose={() => setShowAIBuilder(false)}
        onFunctionCreated={(func) => {
          console.log('AI function created:', func);
          setShowAIBuilder(false);
        }}
      />

      <NeuralNetworkDashboard
        isOpen={showNeuralDashboard}
        onClose={() => setShowNeuralDashboard(false)}
      />
    </div>
  );
}

export default function Page() {
  return <AIIntegratedPage />
}
