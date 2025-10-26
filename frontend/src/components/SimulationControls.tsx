/**
 * SimulationControls Component
 * Controls for running simulations
 *
 * API Integration:
 * - POST /api/simulation/run
 * - GET /api/simulation/status
 */

'use client';

import { useState } from 'react';

interface SimulationControlsProps {
  onRunSimulation: (ticker: string, startDate: string, endDate: string) => void;
  loading: boolean;
  status: any;
}

export default function SimulationControls({
  onRunSimulation,
  loading,
  status,
}: SimulationControlsProps) {
  const [ticker, setTicker] = useState('AAPL');
  const [startDate, setStartDate] = useState('2020-07-01');
  const [endDate, setEndDate] = useState('2020-07-15');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onRunSimulation(ticker, startDate, endDate);
  };

  return (
    <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
        Simulation Controls
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label
              htmlFor="ticker"
              className="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >
              Ticker
            </label>
            <select
              id="ticker"
              value={ticker}
              onChange={(e) => setTicker(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            >
              <option value="AAPL">AAPL</option>
              <option value="MSFT">MSFT</option>
              <option value="NVDA">NVDA</option>
            </select>
          </div>

          <div>
            <label
              htmlFor="startDate"
              className="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >
              Start Date
            </label>
            <input
              type="date"
              id="startDate"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            />
          </div>

          <div>
            <label
              htmlFor="endDate"
              className="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >
              End Date
            </label>
            <input
              type="date"
              id="endDate"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            />
          </div>
        </div>

        <div className="flex items-center justify-between">
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-2 bg-primary text-white rounded-md hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Running Simulation...' : 'Run Simulation'}
          </button>

          {status && (
            <div className="text-sm text-gray-600 dark:text-gray-400">
              Status: <span className="font-semibold">{status.status}</span>
              {status.progress > 0 && ` - ${status.progress}% complete`}
            </div>
          )}
        </div>
      </form>

      {/* Progress Bar */}
      {loading && status?.progress > 0 && (
        <div className="mt-4">
          <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
            <div
              className="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
              style={{ width: `${status.progress}%` }}
            ></div>
          </div>
        </div>
      )}
    </div>
  );
}
