/**
 * PerformanceChart Component
 * Displays performance comparison between different traders
 *
 * API Integration: Gets data from GET /api/simulation/results/summary
 */

'use client';

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface TraderResult {
  name: string;
  model: string;
  final_value: number;
  total_return: number;
  total_return_pct: number;
  total_trades: number;
}

interface PerformanceChartProps {
  data: {
    ticker: string;
    period: {
      start: string;
      end: string;
      days: number;
    };
    traders: TraderResult[];
  };
}

export default function PerformanceChart({ data }: PerformanceChartProps) {
  const { ticker, period, traders } = data;

  // Format data for chart
  const chartData = traders.map((trader) => ({
    name: trader.name,
    'Return %': trader.total_return_pct,
    'Final Value': trader.final_value,
    Trades: trader.total_trades,
  }));

  return (
    <div className="space-y-6">
      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-4">
          <div className="text-sm text-gray-600 dark:text-gray-400">Ticker</div>
          <div className="text-2xl font-bold text-gray-900 dark:text-white">
            {ticker}
          </div>
        </div>
        <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-4">
          <div className="text-sm text-gray-600 dark:text-gray-400">Period</div>
          <div className="text-lg font-bold text-gray-900 dark:text-white">
            {period.start} to {period.end}
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">
            {period.days} trading days
          </div>
        </div>
        <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-4">
          <div className="text-sm text-gray-600 dark:text-gray-400">
            Best Performer
          </div>
          <div className="text-2xl font-bold text-green-600">
            {traders.sort((a, b) => b.total_return_pct - a.total_return_pct)[0]?.name}
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">
            +{traders.sort((a, b) => b.total_return_pct - a.total_return_pct)[0]?.total_return_pct.toFixed(2)}%
          </div>
        </div>
      </div>

      {/* Performance Chart */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Return Comparison
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="Return %" fill="#10B981" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Detailed Results Table */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Detailed Results
        </h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-300 dark:divide-gray-600">
            <thead className="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-white">
                  Trader
                </th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-white">
                  Model
                </th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-white">
                  Final Value
                </th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-white">
                  Return
                </th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-white">
                  Return %
                </th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-white">
                  Trades
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-700 bg-white dark:bg-gray-800">
              {traders.map((trader, idx) => (
                <tr key={idx}>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-900 dark:text-white">
                    {trader.name}
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500 dark:text-gray-400">
                    {trader.model}
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-900 dark:text-white">
                    ${trader.final_value.toLocaleString()}
                  </td>
                  <td
                    className={`whitespace-nowrap px-3 py-4 text-sm ${
                      trader.total_return >= 0 ? 'text-green-600' : 'text-red-600'
                    }`}
                  >
                    ${trader.total_return.toLocaleString()}
                  </td>
                  <td
                    className={`whitespace-nowrap px-3 py-4 text-sm font-semibold ${
                      trader.total_return_pct >= 0 ? 'text-green-600' : 'text-red-600'
                    }`}
                  >
                    {trader.total_return_pct >= 0 ? '+' : ''}
                    {trader.total_return_pct.toFixed(2)}%
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500 dark:text-gray-400">
                    {trader.total_trades}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
