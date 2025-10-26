'use client';

import { useState, useEffect } from 'react';
import AgentStatusCard from '@/components/AgentStatusCard';
import DebateViewer from '@/components/DebateViewer';
import PerformanceChart from '@/components/PerformanceChart';
import SimulationControls from '@/components/SimulationControls';
import {
  getAgentsStatus,
  conductDebate,
  getSimulationSummary,
  runSimulation,
  getSimulationStatus,
} from '@/lib/api';

export default function Home() {
  const [agentsStatus, setAgentsStatus] = useState<any>(null);
  const [debateData, setDebateData] = useState<any>(null);
  const [simulationData, setSimulationData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [simulationStatus, setSimulationStatus] = useState<any>(null);

  // Load agents status on mount
  useEffect(() => {
    loadAgentsStatus();
  }, []);

  const loadAgentsStatus = async () => {
    const data = await getAgentsStatus();
    setAgentsStatus(data);
  };

  const handleRunDebate = async () => {
    setLoading(true);
    try {
      const data = await conductDebate('AAPL', '2020-07-15', 2);
      setDebateData(data.debate);
    } catch (error) {
      console.error('Error running debate:', error);
    }
    setLoading(false);
  };

  const handleRunSimulation = async (ticker: string, startDate: string, endDate: string) => {
    setLoading(true);
    try {
      await runSimulation(ticker, startDate, endDate);

      // Poll for status
      const pollInterval = setInterval(async () => {
        const status = await getSimulationStatus();
        setSimulationStatus(status);

        if (status.status === 'completed') {
          clearInterval(pollInterval);
          const summary = await getSimulationSummary();
          setSimulationData(summary);
          setLoading(false);
        } else if (status.status === 'error') {
          clearInterval(pollInterval);
          setLoading(false);
        }
      }, 1000);
    } catch (error) {
      console.error('Error running simulation:', error);
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            LLM Trading Arena
          </h1>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Multi-agent AI trading system with debate mechanism
          </p>
        </div>
      </header>

      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Simulation Controls */}
        <div className="px-4 py-6 sm:px-0">
          <SimulationControls
            onRunSimulation={handleRunSimulation}
            loading={loading}
            status={simulationStatus}
          />
        </div>

        {/* Agent Status Cards */}
        <div className="px-4 py-6 sm:px-0">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
            Active Agents
          </h2>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {agentsStatus?.analysts?.map((agent: any, idx: number) => (
              <AgentStatusCard key={idx} agent={agent} type="analyst" />
            ))}
            {agentsStatus?.debate_team && (
              <AgentStatusCard agent={agentsStatus.debate_team} type="debate" />
            )}
            {agentsStatus?.traders?.map((agent: any, idx: number) => (
              <AgentStatusCard key={idx} agent={agent} type="trader" />
            ))}
          </div>
        </div>

        {/* Debate Viewer - THE KEY FEATURE */}
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
            <div className="flex justify-between items-center mb-4">
              <div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                  Debate Viewer
                </h2>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  Watch AI agents debate trading decisions in real-time
                </p>
              </div>
              <button
                onClick={handleRunDebate}
                disabled={loading}
                className="px-4 py-2 bg-primary text-white rounded-md hover:bg-blue-600 disabled:opacity-50"
              >
                {loading ? 'Running...' : 'Run Debate'}
              </button>
            </div>
            {debateData ? (
              <DebateViewer debate={debateData} />
            ) : (
              <div className="text-center py-12 text-gray-500">
                Click &quot;Run Debate&quot; to see AI agents debate a trading decision
              </div>
            )}
          </div>
        </div>

        {/* Performance Chart */}
        {simulationData && (
          <div className="px-4 py-6 sm:px-0">
            <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                Performance Results
              </h2>
              <PerformanceChart data={simulationData} />
            </div>
          </div>
        )}

        {/* API Integration Guide */}
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-blue-50 dark:bg-blue-900 border-l-4 border-blue-400 p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg
                  className="h-5 w-5 text-blue-400"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                    clipRule="evenodd"
                  />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-blue-800 dark:text-blue-200">
                  API Integration Points
                </h3>
                <div className="mt-2 text-sm text-blue-700 dark:text-blue-300">
                  <p>
                    This frontend is ready to connect to the backend API. Check{' '}
                    <code className="bg-blue-100 dark:bg-blue-800 px-1 rounded">
                      src/lib/api.ts
                    </code>{' '}
                    for all API integration points.
                  </p>
                  <ul className="list-disc list-inside mt-2 space-y-1">
                    <li>Backend API: http://localhost:8000</li>
                    <li>API Docs: http://localhost:8000/docs</li>
                    <li>Currently showing mock data when API is unavailable</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
