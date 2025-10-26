/**
 * DebateViewer Component - THE KEY INNOVATION
 * Shows the bull vs bear debate in a conversational format
 *
 * API Integration: Gets data from POST /api/agents/debate
 */

interface DebateEntry {
  round: number;
  speaker: string;
  argument: string;
}

interface DebateViewerProps {
  debate: {
    debate_log: DebateEntry[];
    final_decision: {
      winning_side: string;
      action: string;
      confidence: number;
      key_reasons: string[];
    };
  };
}

export default function DebateViewer({ debate }: DebateViewerProps) {
  const { debate_log, final_decision } = debate;

  return (
    <div className="space-y-6">
      {/* Debate Transcript */}
      <div className="space-y-4">
        {debate_log.map((entry, idx) => {
          const isBull = entry.speaker === 'Bull';
          return (
            <div
              key={idx}
              className={`flex ${isBull ? 'justify-start' : 'justify-end'}`}
            >
              <div
                className={`max-w-3xl rounded-lg px-4 py-3 ${
                  isBull
                    ? 'bg-green-100 dark:bg-green-900 text-green-900 dark:text-green-100'
                    : 'bg-red-100 dark:bg-red-900 text-red-900 dark:text-red-100'
                }`}
              >
                <div className="flex items-center mb-2">
                  <span className="text-lg mr-2">{isBull ? '🐂' : '🐻'}</span>
                  <span className="font-semibold">
                    {entry.speaker} - Round {entry.round}
                  </span>
                </div>
                <p className="text-sm">{entry.argument}</p>
              </div>
            </div>
          );
        })}
      </div>

      {/* Final Decision */}
      <div className="border-t-2 border-gray-300 dark:border-gray-600 pt-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Final Decision
        </h3>
        <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-4">
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <span className="text-sm text-gray-600 dark:text-gray-400">
                Winning Side:
              </span>
              <div className="text-xl font-bold text-gray-900 dark:text-white">
                {final_decision.winning_side === 'Bull' ? '🐂' : '🐻'}{' '}
                {final_decision.winning_side}
              </div>
            </div>
            <div>
              <span className="text-sm text-gray-600 dark:text-gray-400">
                Recommended Action:
              </span>
              <div
                className={`text-xl font-bold ${
                  final_decision.action === 'BUY'
                    ? 'text-green-600'
                    : final_decision.action === 'SELL'
                    ? 'text-red-600'
                    : 'text-gray-600'
                }`}
              >
                {final_decision.action}
              </div>
            </div>
          </div>
          <div className="mb-4">
            <span className="text-sm text-gray-600 dark:text-gray-400">
              Confidence:
            </span>
            <div className="w-full bg-gray-300 rounded-full h-2.5 dark:bg-gray-600 mt-1">
              <div
                className="bg-blue-600 h-2.5 rounded-full"
                style={{ width: `${final_decision.confidence * 100}%` }}
              ></div>
            </div>
            <span className="text-sm text-gray-600 dark:text-gray-400">
              {(final_decision.confidence * 100).toFixed(0)}%
            </span>
          </div>
          <div>
            <span className="text-sm text-gray-600 dark:text-gray-400 block mb-2">
              Key Reasons:
            </span>
            <ul className="list-disc list-inside space-y-1 text-sm text-gray-700 dark:text-gray-300">
              {final_decision.key_reasons.map((reason, idx) => (
                <li key={idx}>{reason}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
