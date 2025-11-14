/**
 * Neural Network API client for Divisor Wave Neural Networks
 * Connects to the divisor-wave-neural-networks project
 */

import axios from 'axios';

const NEURAL_API_BASE_URL = process.env.NEXT_PUBLIC_NEURAL_API_URL || 'http://localhost:8001';
const AGENT_API_BASE_URL = process.env.NEXT_PUBLIC_AGENT_API_URL || 'http://localhost:8002';

const neuralApi = axios.create({
  baseURL: NEURAL_API_BASE_URL,
  timeout: 60000, // 60 seconds for neural network computations
  headers: {
    'Content-Type': 'application/json',
  },
});

const agentApi = axios.create({
  baseURL: AGENT_API_BASE_URL,
  timeout: 120000, // 2 minutes for agent conversations
  headers: {
    'Content-Type': 'application/json',
  },
});

// Neural Network API Functions
export const neuralNetworkAPI = {
  // LaTeX Expression GAN
  generateLatexExpressions: async (params = {}) => {
    const response = await neuralApi.post('/generate-latex', {
      num_expressions: params.numExpressions || 10,
      temperature: params.temperature || 1.0,
      domain: params.domain || 'general',
      seed_text: params.seedText || null
    });
    return response.data;
  },

  // Get LaTeX generation suggestions based on current input
  getLatexSuggestions: async (currentInput, context = {}) => {
    const response = await neuralApi.post('/latex-suggestions', {
      current_input: currentInput,
      context: context,
      num_suggestions: context.numSuggestions || 5
    });
    return response.data;
  },

  // Mathematical GAN - generate numerical sequences
  generateMathematicalSequences: async (params = {}) => {
    const response = await neuralApi.post('/generate-sequences', {
      gan_type: params.ganType || 'sequence',
      num_sequences: params.numSequences || 5,
      sequence_length: params.sequenceLength || 100,
      mathematical_domain: params.domain || 'general'
    });
    return response.data;
  },

  // Crystal Embeddings - analyze mathematical patterns
  analyzeCrystalPatterns: async (mathematicalData, embeddingType = 'icosahedral') => {
    const response = await neuralApi.post('/crystal-analysis', {
      data: mathematicalData,
      embedding_type: embeddingType,
      analyze_symmetry: true,
      extract_patterns: true
    });
    return response.data;
  },

  // Deep Mathematical Discovery
  discoverMathematicalPatterns: async (inputData, discoveryType = 'general') => {
    const response = await neuralApi.post('/discover-patterns', {
      input_data: inputData,
      discovery_type: discoveryType,
      max_iterations: 1000
    });
    return response.data;
  },

  // Get available neural network models
  getAvailableModels: async () => {
    const response = await neuralApi.get('/models');
    return response.data;
  },

  // Health check for neural network service
  healthCheck: async () => {
    const response = await neuralApi.get('/health');
    return response.data;
  }
};

// AI Agent API Functions
export const agentAPI = {
  // Start a mathematical conversation with an AI agent
  startConversation: async (agentType = 'mathematical_discovery') => {
    const response = await agentApi.post('/start-conversation', {
      agent_type: agentType,
      capabilities: ['latex_generation', 'pattern_discovery', 'validation']
    });
    return response.data;
  },

  // Send message to AI agent
  sendMessage: async (conversationId, message, context = {}) => {
    const response = await agentApi.post(`/conversation/${conversationId}/message`, {
      message: message,
      context: context,
      use_tools: true
    });
    return response.data;
  },

  // Get mathematical insights from AI agent
  getMathematicalInsights: async (mathematicalContent) => {
    const response = await agentApi.post('/analyze', {
      content: mathematicalContent,
      analysis_type: 'comprehensive',
      include_suggestions: true
    });
    return response.data;
  },

  // Generate mathematical research report
  generateResearchReport: async (discoveries, reportType = 'summary') => {
    const response = await agentApi.post('/generate-report', {
      discoveries: discoveries,
      report_type: reportType,
      include_latex: true,
      include_validation: true
    });
    return response.data;
  },

  // Get agent capabilities
  getAgentCapabilities: async () => {
    const response = await agentApi.get('/capabilities');
    return response.data;
  }
};

// Combined Neural + Agent Functions
export const integratedAPI = {
  // Generate LaTeX with AI explanation
  generateWithExplanation: async (params = {}) => {
    try {
      // Generate LaTeX expressions
      const latexResult = await neuralNetworkAPI.generateLatexExpressions(params);
      
      // Get AI explanation for the expressions
      const agentInsights = await agentAPI.getMathematicalInsights({
        latex_expressions: latexResult.expressions,
        generation_params: params
      });

      return {
        success: true,
        expressions: latexResult.expressions,
        explanations: agentInsights.insights,
        confidence_scores: latexResult.confidence_scores,
        mathematical_analysis: agentInsights.mathematical_properties
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  },

  // Interactive mathematical discovery session
  discoverInteractively: async (userQuery, previousContext = []) => {
    try {
      // Start or continue conversation with discovery agent
      let conversationId;
      if (previousContext.length === 0) {
        const conversation = await agentAPI.startConversation('mathematical_discovery');
        conversationId = conversation.conversation_id;
      } else {
        conversationId = previousContext[previousContext.length - 1].conversation_id;
      }

      // Send query to agent
      const agentResponse = await agentAPI.sendMessage(conversationId, userQuery, {
        previous_context: previousContext,
        enable_neural_tools: true
      });

      // If agent suggests generating expressions, do it
      if (agentResponse.suggested_actions?.includes('generate_latex')) {
        const generatedExpressions = await neuralNetworkAPI.generateLatexExpressions({
          domain: agentResponse.suggested_domain,
          numExpressions: 5
        });

        agentResponse.generated_content = generatedExpressions;
      }

      return {
        success: true,
        conversation_id: conversationId,
        agent_response: agentResponse.message,
        generated_content: agentResponse.generated_content,
        suggestions: agentResponse.suggestions,
        context: [...previousContext, {
          conversation_id: conversationId,
          user_query: userQuery,
          agent_response: agentResponse
        }]
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }
};

// Error handling
const handleApiError = (error, apiType) => {
  console.error(`${apiType} API Error:`, error);
  
  if (error.code === 'ECONNREFUSED') {
    throw new Error(`Cannot connect to ${apiType} server. Please ensure the service is running.`);
  } else if (error.code === 'TIMEOUT') {
    throw new Error(`${apiType} request timed out. Neural computations may take longer.`);
  } else if (error.response?.status === 500) {
    throw new Error(`${apiType} server error. Please check the service logs.`);
  }
  
  throw error;
};

// Add error interceptors
neuralApi.interceptors.response.use(
  (response) => response,
  (error) => handleApiError(error, 'Neural Network')
);

agentApi.interceptors.response.use(
  (response) => response,
  (error) => handleApiError(error, 'AI Agent')
);

export default { neuralNetworkAPI, agentAPI, integratedAPI };