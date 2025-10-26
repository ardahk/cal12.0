/**
 * AgentStatusCard Component
 * Displays the status of an individual agent
 *
 * API Integration: Gets data from /api/agents/status
 */

interface AgentStatusCardProps {
  agent: {
    name: string;
    model: string;
    status: string;
    cash?: string;
    positions?: number;
  };
  type: 'analyst' | 'debate' | 'trader';
}

export default function AgentStatusCard({ agent, type }: AgentStatusCardProps) {
  const getTypeColor = () => {
    switch (type) {
      case 'analyst':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
      case 'debate':
        return 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200';
      case 'trader':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getTypeIcon = () => {
    switch (type) {
      case 'analyst':
        return '📊';
      case 'debate':
        return '⚖️';
      case 'trader':
        return '💼';
      default:
        return '🤖';
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg">
      <div className="px-4 py-5 sm:p-6">
        <div className="flex items-center">
          <div className="flex-shrink-0 text-3xl">{getTypeIcon()}</div>
          <div className="ml-5 w-0 flex-1">
            <dl>
              <dt className="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
                {agent.name}
              </dt>
              <dd className="flex items-baseline">
                <div className="text-lg font-semibold text-gray-900 dark:text-white">
                  {agent.model}
                </div>
                <div
                  className={`ml-2 flex items-baseline text-sm font-semibold ${getTypeColor()} px-2 py-0.5 rounded-full`}
                >
                  {agent.status}
                </div>
              </dd>
            </dl>
            {type === 'trader' && (
              <div className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                <div>Cash: {agent.cash}</div>
                <div>Positions: {agent.positions}</div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
