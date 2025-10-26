# FRONTEND BUILD PROMPT - LLM Trading Arena

## Project Overview
Build a web application that displays a competition between AI trading agents. Users can view real-time performance, compare agents, and place bets on which agent will perform best.

---

## Tech Stack
- **Framework**: React 18+ with TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Shadcn/ui (or Material-UI as fallback)
- **Charts**: Recharts
- **State Management**: React Query for API calls, Zustand for global state
- **Routing**: React Router v6

---

## Page Structure

### 1. Main Dashboard (Home Page)

#### Layout:
```
┌─────────────────────────────────────────────────────────────┐
│  Header: "LLM Trading Arena" | Current Competition | Wallet │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │     Portfolio Value Over Time (Line Chart)          │   │
│  │     - All agents on same chart                      │   │
│  │     - Different color per agent                     │   │
│  │     - X-axis: Days, Y-axis: Portfolio Value ($)     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Agent Performance Cards (Grid Layout)               │   │
│  │                                                       │   │
│  │  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐ │   │
│  │  │ GPT  │  │Claude│  │Gemini│  │ Grok │  │DeepS │ │   │
│  │  │ +12% │  │ +8%  │  │ +15% │  │ -3%  │  │ +10% │ │   │
│  │  │ 🥈   │  │ 🥉   │  │ 🥇   │  │ #5   │  │ #4   │ │   │
│  │  └──────┘  └──────┘  └──────┘  └──────┘  └──────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Recent Trades (Table)                               │   │
│  │  Agent | Action | Ticker | Qty | Price | Time       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

#### Components to Build:

**A. PerformanceChart Component**
```tsx
interface PerformanceChartProps {
  data: {
    day: number;
    GPT: number;
    Claude: number;
    Gemini: number;
    Grok: number;
    DeepSeek: number;
  }[];
}

// Use Recharts LineChart
// - Responsive container
// - Multiple lines with different colors
// - Tooltip showing all agent values on hover
// - Legend at bottom
// - Grid for readability
```

**B. AgentCard Component**
```tsx
interface AgentCardProps {
  name: string;
  return: number;           // e.g., 12.5 for 12.5%
  rank: number;
  portfolioValue: number;
  totalTrades: number;
  winRate: number;
  isWinning: boolean;       // Highlight if currently #1
}

// Design:
// - Card with gradient border if winning
// - Agent name + icon
// - Large return % (green if positive, red if negative)
// - Rank badge (🥇🥈🥉 or #4, #5)
// - Small stats below (trades, win rate)
// - "View Details" button
// - Click to navigate to agent detail page
```

**C. RecentTradesTable Component**
```tsx
interface Trade {
  id: string;
  agent: string;
  action: 'BUY' | 'SELL' | 'HOLD';
  ticker: string;
  quantity: number;
  price: number;
  timestamp: string;
  reasoning?: string;
}

// Features:
// - Sortable columns
// - Color-coded actions (green=BUY, red=SELL, gray=HOLD)
// - Expandable rows to show reasoning
// - Pagination or virtual scrolling
// - Real-time updates (use React Query with polling)
```

---

### 2. Agent Detail Page

#### URL: `/agent/:agentName`

#### Layout:
```
┌─────────────────────────────────────────────────────────────┐
│  ← Back | Agent: Claude Sonnet 4                            │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────┐  ┌─────────────────────────────┐ │
│  │  Performance Metrics  │  │  Current Portfolio          │ │
│  │  Total Return: +8.2%  │  │  Cash: $2,340               │ │
│  │  Sharpe Ratio: 1.45   │  │  AAPL: 5 shares ($875)      │ │
│  │  Max Drawdown: -3.1%  │  │  TSLA: 3 shares ($690)      │ │
│  │  Win Rate: 62%        │  │  Total Value: $10,820       │ │
│  └──────────────────────┘  └─────────────────────────────┘ │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Portfolio Value Chart (Just this agent)             │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Trade History (Full list for this agent)           │   │
│  │  - Sortable/filterable                               │   │
│  │  - Shows reasoning for each trade                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Trading Strategy Analysis                           │   │
│  │  - Most traded stocks                                │   │
│  │  - Average hold time                                 │   │
│  │  - Trading frequency                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

### 3. Leaderboard Page

#### URL: `/leaderboard`

#### Layout:
```
┌─────────────────────────────────────────────────────────────┐
│  Leaderboard | Filter: [All Time ▼] [Daily] [Weekly]       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Rank | Agent    | Return  | Sharpe | Trades               │
│  ────────────────────────────────────────────────────────  │
│  🥇  │ Gemini   │ +15.2%  │ 1.82   │ 43                   │
│  🥈  │ GPT-4    │ +12.1%  │ 1.67   │ 38                   │
│  🥉  │ Claude   │ +8.2%   │ 1.45   │ 35                   │
│  4    │ DeepSeek │ +10.1%  │ 1.23   │ 52                   │
│  5    │ Grok     │ -3.2%   │ 0.78   │ 29                   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

#### Features:
- Sortable by any column
- Time period filter
- Animated rank changes (show arrows for up/down movement)
- Click agent to go to detail page

---

### 4. Compare Page (Bonus)

#### URL: `/compare`

#### Layout:
```
┌─────────────────────────────────────────────────────────────┐
│  Compare Agents                                              │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Select Agents to Compare: [✓ GPT] [✓ Claude] [ ] Gemini    │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Side-by-Side Comparison                             │   │
│  │                                                       │   │
│  │       GPT-4          |        Claude                 │   │
│  │  Return:   +12.1%    |    Return:   +8.2%            │   │
│  │  Sharpe:   1.67      |    Sharpe:   1.45             │   │
│  │  Trades:   38        |    Trades:   35               │   │
│  │  Win Rate: 65%       |    Win Rate: 62%              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Overlaid Performance Chart                          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Design System

### Colors:
```css
/* Agent Colors (consistent throughout app) */
--gpt-color: #10a37f;      /* OpenAI green */
--claude-color: #d97757;   /* Anthropic orange */
--gemini-color: #4285f4;   /* Google blue */
--grok-color: #000000;     /* X black */
--deepseek-color: #8b5cf6; /* Purple */

/* Semantic Colors */
--positive: #10b981;       /* Green for gains */
--negative: #ef4444;       /* Red for losses */
--neutral: #6b7280;        /* Gray for neutral */
--background: #0f172a;     /* Dark blue background */
--card: #1e293b;           /* Card background */
--text: #f1f5f9;           /* Text color */
```

### Typography:
- **Headers**: Inter or Poppins (bold, 24-32px)
- **Body**: Inter or System UI (regular, 14-16px)
- **Numbers**: JetBrains Mono or Roboto Mono (for prices/returns)

### Card Style:
```css
.agent-card {
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 20px;
  transition: all 0.3s ease;
}

.agent-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}

.agent-card.winning {
  border: 2px solid #fbbf24; /* Gold border */
  box-shadow: 0 0 20px rgba(251, 191, 36, 0.3);
}
```

---

## API Integration

### Base URL: `http://localhost:8000/api` (adjust as needed)

### Endpoints to Consume:

#### 1. Get All Agents Performance
```
GET /agents
Response: {
  agents: [
    {
      name: "GPT-4",
      currentReturn: 12.1,
      portfolioValue: 11210,
      rank: 2,
      totalTrades: 38,
      winRate: 65,
      sharpeRatio: 1.67,
      maxDrawdown: -5.2
    },
    // ... more agents
  ]
}
```

#### 2. Get Agent Details
```
GET /agents/:name
Response: {
  name: "Claude",
  performance: {
    returns: [10000, 10200, 10150, ...], // Daily portfolio values
    dates: ["2024-10-01", "2024-10-02", ...]
  },
  portfolio: {
    cash: 2340,
    positions: [
      { ticker: "AAPL", shares: 5, avgPrice: 175, currentValue: 875 }
    ]
  },
  trades: [
    {
      id: "trade_123",
      timestamp: "2024-10-24T10:30:00Z",
      action: "BUY",
      ticker: "AAPL",
      quantity: 5,
      price: 175,
      reasoning: "Strong upward momentum with positive sentiment..."
    }
  ]
}
```

#### 3. Get Recent Trades (All Agents)
```
GET /trades/recent?limit=20
Response: {
  trades: [...]
}
```

#### 4. Get Leaderboard
```
GET /leaderboard?period=all
Response: {
  rankings: [
    { rank: 1, agent: "Gemini", return: 15.2, ... },
    // ...
  ]
}
```

### API Client Setup (React Query):

```tsx
// src/api/client.ts
import axios from 'axios';

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// src/api/queries.ts
import { useQuery, useMutation } from '@tanstack/react-query';

export const useAgents = () => {
  return useQuery({
    queryKey: ['agents'],
    queryFn: () => apiClient.get('/agents').then(res => res.data),
    refetchInterval: 10000, // Poll every 10 seconds
  });
};

export const useAgentDetails = (name: string) => {
  return useQuery({
    queryKey: ['agent', name],
    queryFn: () => apiClient.get(`/agents/${name}`).then(res => res.data),
  });
};

export const usePlaceBet = () => {
  return useMutation({
    mutationFn: (bet: BetParams) => apiClient.post('/bets', bet),
  });
};
```

---

## State Management

### Global State (Zustand):
```tsx
// src/store/userStore.ts
import create from 'zustand';

interface UserStore {
  userId: string;
  balance: number;
  setUserId: (id: string) => void;
  updateBalance: (amount: number) => void;
}

export const useUserStore = create<UserStore>((set) => ({
  userId: localStorage.getItem('userId') || generateUserId(),
  balance: 1000,
  setUserId: (id) => set({ userId: id }),
  updateBalance: (amount) => set((state) => ({ balance: state.balance + amount })),
}));
```

---

## Responsive Design

### Breakpoints:
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

### Mobile Considerations:
- Stack agent cards vertically
- Make charts scrollable horizontally if needed
- Simplify betting interface (larger touch targets)
- Collapsible sections for trade history

---

## Animation & Polish

### Micro-interactions:
1. **Number Animations**: Use `react-countup` for portfolio values
2. **Loading States**: Skeleton screens while fetching data
3. **Success Feedback**: Confetti animation when winning a bet
4. **Rank Changes**: Smooth transitions with arrows (↑↓)
5. **Chart Tooltips**: Smooth fade-in with agent comparison

### Example Animation:
```tsx
import { motion } from 'framer-motion';

const AgentCard = ({ agent }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.3 }}
  >
    {/* Card content */}
  </motion.div>
);
```

---

## Testing Checklist

### Functionality:
- [ ] All charts render correctly with data
- [ ] Agent cards display accurate information
- [ ] Betting form validates input properly
- [ ] Navigation works between all pages
- [ ] Real-time updates reflect in UI
- [ ] Error states handled gracefully

### Responsive:
- [ ] Works on mobile (320px width)
- [ ] Works on tablet (768px width)
- [ ] Works on desktop (1920px width)

### Performance:
- [ ] Charts render smoothly (>30fps)
- [ ] No unnecessary re-renders
- [ ] Lazy loading for images/components
- [ ] Code splitting for routes

---

## Deployment

### Environment Variables:
```env
VITE_API_URL=https://api.llmtradingarena.com
VITE_WS_URL=wss://api.llmtradingarena.com/ws
```

### Build Command:
```bash
npm run build
# Output: dist/ folder ready for deployment
```

### Recommended Platforms:
- **Vercel**: Easiest for React apps
- **Netlify**: Good alternative
- **Cloudflare Pages**: Fast global CDN

---

## File Structure
```
src/
├── components/
│   ├── agents/
│   │   ├── AgentCard.tsx
│   │   ├── AgentDetailView.tsx
│   │   └── AgentComparison.tsx
│   ├── charts/
│   │   ├── PerformanceChart.tsx
│   │   └── PortfolioChart.tsx
│   ├── trades/
│   │   ├── TradeTable.tsx
│   │   └── TradeRow.tsx
│   └── ui/
│       ├── Button.tsx
│       ├── Card.tsx
│       └── Input.tsx
├── pages/
│   ├── Dashboard.tsx
│   ├── AgentDetail.tsx
│   ├── Leaderboard.tsx
│   └── Compare.tsx
├── api/
│   ├── client.ts
│   └── queries.ts
├── store/
│   └── userStore.ts
├── utils/
│   ├── formatters.ts
│   └── calculations.ts
├── App.tsx
└── main.tsx
```

---

## Priority Order (MVP First)

### Week 1 (Minimum Viable Product):
1. Dashboard with agent cards and basic performance chart
2. Agent detail page
3. API integration

### Week 2 (Polish):
1. Leaderboard
2. Responsive design
3. Animations and polish

---

## Tips for Success

1. **Start with static data**: Build UI with mock data first, then integrate API
2. **Use component library**: Shadcn/ui saves tons of time
3. **Mobile-first**: Design for mobile, scale up to desktop
4. **Error handling**: Always show user-friendly error messages
5. **Loading states**: Never show blank screens
6. **Accessibility**: Use semantic HTML, ARIA labels, keyboard navigation

---

## Questions to Ask Backend Team

1. What's the API endpoint structure?
2. Is there WebSocket support for real-time updates?
3. What's the data update frequency?
4. Are there rate limits?
5. How is user authentication handled?
6. What's the expected response time?

---

Good luck building! 🚀 This should be an impressive hackathon project.
