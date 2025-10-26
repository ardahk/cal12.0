/**
 * API Client for LLM Trading Arena Backend
 *
 * THIS FILE SHOWS WHERE TO INTEGRATE REAL API CALLS
 * Currently returns mock data for demonstration
 * Replace mock data with axios calls when backend is running
 */

import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types
export interface AgentStatus {
  name: string;
  model: string;
  status: string;
}

export interface TechnicalAnalysis {
  trend: string;
  recommendation: string;
  confidence: number;
  indicators: {
    sma_20: number;
    sma_50: number;
    rsi: number;
    current_price: number;
  };
}

export interface SentimentAnalysis {
  sentiment_score: number;
  trend: string;
  impact: string;
  confidence: number;
}

export interface DebateEntry {
  round: number;
  speaker: string;
  argument: string;
}

export interface DebateResult {
  debate_log: DebateEntry[];
  final_decision: {
    winning_side: string;
    action: string;
    confidence: number;
    key_reasons: string[];
  };
}

export interface TraderResult {
  name: string;
  model: string;
  final_value: number;
  total_return: number;
  total_return_pct: number;
  total_trades: number;
}

export interface SimulationSummary {
  ticker: string;
  period: {
    start: string;
    end: string;
    days: number;
  };
  traders: TraderResult[];
}

// API Functions

/**
 * Get status of all agents
 * REAL API CALL: GET /api/agents/status
 */
export async function getAgentsStatus(): Promise<any> {
  try {
    const response = await api.get('/api/agents/status');
    return response.data;
  } catch (error) {
    console.error('API Error - using mock data:', error);
    // MOCK DATA - Replace with real API response
    return {
      analysts: [
        { name: 'Technical Analyst', model: 'claude-haiku', status: 'active' },
        { name: 'Sentiment Analyst', model: 'claude-haiku', status: 'active' },
      ],
      debate_team: { name: 'Debate Team', model: 'claude-sonnet-4', status: 'active' },
      traders: [
        { name: 'Claude Trader', model: 'claude', status: 'active', cash: '$10,000.00', positions: 0 },
        { name: 'Gemini Trader', model: 'gemini', status: 'active', cash: '$10,000.00', positions: 0 },
      ],
    };
  }
}

/**
 * Get technical analysis for a ticker
 * REAL API CALL: GET /api/agents/technical/{ticker}?date={date}
 */
export async function getTechnicalAnalysis(ticker: string, date: string): Promise<TechnicalAnalysis> {
  try {
    const response = await api.get(`/api/agents/technical/${ticker}?date=${date}`);
    return response.data;
  } catch (error) {
    console.error('API Error - using mock data:', error);
    // MOCK DATA
    return {
      trend: 'BULLISH',
      recommendation: 'BUY',
      confidence: 0.75,
      indicators: {
        sma_20: 103.5,
        sma_50: 101.2,
        rsi: 65.3,
        current_price: 105.0,
      },
    };
  }
}

/**
 * Get sentiment analysis for a ticker
 * REAL API CALL: GET /api/agents/sentiment/{ticker}?date={date}
 */
export async function getSentimentAnalysis(ticker: string, date: string): Promise<SentimentAnalysis> {
  try {
    const response = await api.get(`/api/agents/sentiment/${ticker}?date=${date}`);
    return response.data;
  } catch (error) {
    console.error('API Error - using mock data:', error);
    // MOCK DATA
    return {
      sentiment_score: 0.42,
      trend: 'IMPROVING',
      impact: 'POSITIVE',
      confidence: 0.68,
    };
  }
}

/**
 * Conduct a debate
 * REAL API CALL: POST /api/agents/debate?ticker={ticker}&date={date}&rounds={rounds}
 */
export async function conductDebate(ticker: string, date: string, rounds: number = 2): Promise<any> {
  try {
    const response = await api.post('/api/agents/debate', null, {
      params: { ticker, date, rounds },
    });
    return response.data;
  } catch (error) {
    console.error('API Error - using mock data:', error);
    // MOCK DATA
    return {
      debate: {
        debate_log: [
          {
            round: 1,
            speaker: 'Bull',
            argument: 'Strong technical indicators show bullish momentum with RSI at 65 and golden cross formation. Positive sentiment trending upward.',
          },
          {
            round: 1,
            speaker: 'Bear',
            argument: 'However, market volatility remains high and sentiment could reverse quickly. Technical indicators may be overextended.',
          },
          {
            round: 2,
            speaker: 'Bull',
            argument: 'The sentiment data shows consistent positive trend over 7 days, not just a spike. Volume supports the price movement.',
          },
          {
            round: 2,
            speaker: 'Bear',
            argument: 'Fair point, but we must consider broader market risks and potential correction after recent gains.',
          },
        ],
        final_decision: {
          winning_side: 'Bull',
          action: 'BUY',
          confidence: 0.72,
          key_reasons: ['Strong technical momentum', 'Positive sentiment trend', 'Volume confirmation'],
        },
      },
    };
  }
}

/**
 * Run simulation
 * REAL API CALL: POST /api/simulation/run?ticker={ticker}&start_date={start}&end_date={end}
 */
export async function runSimulation(ticker: string, startDate: string, endDate: string): Promise<any> {
  try {
    const response = await api.post('/api/simulation/run', null, {
      params: {
        ticker,
        start_date: startDate,
        end_date: endDate,
      },
    });
    return response.data;
  } catch (error) {
    console.error('API Error - using mock data:', error);
    return {
      message: 'Simulation started',
      status_url: '/api/simulation/status',
    };
  }
}

/**
 * Get simulation status
 * REAL API CALL: GET /api/simulation/status
 */
export async function getSimulationStatus(): Promise<any> {
  try {
    const response = await api.get('/api/simulation/status');
    return response.data;
  } catch (error) {
    console.error('API Error - using mock data:', error);
    return { status: 'idle', progress: 0 };
  }
}

/**
 * Get simulation results summary
 * REAL API CALL: GET /api/simulation/results/summary
 */
export async function getSimulationSummary(): Promise<SimulationSummary> {
  try {
    const response = await api.get('/api/simulation/results/summary');
    return response.data;
  } catch (error) {
    console.error('API Error - using mock data:', error);
    // MOCK DATA
    return {
      ticker: 'AAPL',
      period: {
        start: '2020-07-01',
        end: '2020-07-15',
        days: 10,
      },
      traders: [
        {
          name: 'Claude Trader',
          model: 'claude',
          final_value: 10850,
          total_return: 850,
          total_return_pct: 8.5,
          total_trades: 12,
        },
        {
          name: 'Gemini Trader',
          model: 'gemini',
          final_value: 10730,
          total_return: 730,
          total_return_pct: 7.3,
          total_trades: 11,
        },
      ],
    };
  }
}

export default api;
