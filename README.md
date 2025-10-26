# LLM Trading Arena

A full-stack multi-agent AI trading system where different AI models (Claude, GPT-4, Gemini) compete in stock trading using a unique **debate mechanism** for decision making.

## 🎯 Key Features

- **Multi-Agent System**: Technical Analyst, Sentiment Analyst, Debate Team, and Traders
- **Debate Mechanism**: Bull vs Bear debates before each trading decision (KEY INNOVATION)
- **Multiple LLM Comparison**: Claude, GPT-4, and Gemini compete side-by-side
- **Real Data**: Uses historical stock prices and sentiment data from Reddit/Twitter
- **Full Stack**: FastAPI backend + Next.js frontend
- **Explainable AI**: Every decision is backed by visible reasoning

## 📁 Project Structure

```
cal12.0/
├── backend/                 # Python/FastAPI backend
│   ├── agents/             # AI agent implementations
│   │   ├── technical_analyst.py
│   │   ├── sentiment_analyst.py
│   │   ├── debate_team.py
│   │   └── trader.py
│   ├── routers/            # API endpoints
│   │   ├── agents.py       # Agent status and analysis endpoints
│   │   └── simulation.py   # Simulation control endpoints
│   ├── services/           # Core services
│   │   ├── llm_client.py   # LLM API client (Claude, GPT, Gemini)
│   │   └── data_loader.py  # Data loading and processing
│   ├── data/               # Historical data
│   │   ├── reddit_sentiment.csv
│   │   └── twitter_sentiment.csv
│   ├── main.py             # FastAPI app
│   ├── config.py           # Configuration
│   └── requirements.txt
│
├── frontend/               # Next.js/React frontend
│   ├── src/
│   │   ├── app/           # Next.js app router
│   │   ├── components/    # React components
│   │   │   ├── AgentStatusCard.tsx
│   │   │   ├── DebateViewer.tsx      # KEY FEATURE!
│   │   │   ├── PerformanceChart.tsx
│   │   │   └── SimulationControls.tsx
│   │   └── lib/
│   │       └── api.ts     # API client with integration points
│   └── package.json
│
├── scripts/               # Utility scripts
│   └── run_simulation.py  # Standalone simulation script
│
└── claude/                # Project documentation
    ├── README.md
    ├── code_implementation_guide.md
    └── ...
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment** (optional - for real LLM calls):
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys:
   # ANTHROPIC_API_KEY=your_key
   # OPENAI_API_KEY=your_key
   # GOOGLE_AI_API_KEY=your_key
   ```

5. **Run the API server**:
   ```bash
   python main.py
   # Or use uvicorn:
   uvicorn main:app --reload
   ```

   The API will be available at:
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs (interactive Swagger UI)

### Frontend Setup

1. **Navigate to frontend directory** (in a new terminal):
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Run development server**:
   ```bash
   npm run dev
   ```

   The frontend will be available at: http://localhost:3000

### Running a Simulation (Command Line)

You can also run simulations directly from the command line:

```bash
cd scripts
python run_simulation.py
```

This will run a simulation and save results to `simulation_results.json`.

## 🔌 API Integration Points

The frontend is designed with clear API integration points. Currently, it shows mock data when the backend is unavailable.

### Key Endpoints

All endpoints are documented in the interactive API docs at http://localhost:8000/docs

**Agent Endpoints** (`/api/agents/`):
- `GET /status` - Get status of all agents
- `GET /technical/{ticker}` - Get technical analysis
- `GET /sentiment/{ticker}` - Get sentiment analysis
- `POST /debate` - Conduct a trading debate (KEY FEATURE)
- `GET /portfolio/{trader_name}` - Get trader portfolio

**Simulation Endpoints** (`/api/simulation/`):
- `POST /run` - Start a simulation
- `GET /status` - Get simulation progress
- `GET /results` - Get full simulation results
- `GET /results/summary` - Get summarized results
- `DELETE /reset` - Reset simulation state

### Making Endpoints Functional

The backend currently uses **mock LLM responses** for demonstration. To make it functional with real AI:

1. **Add API Keys** to `backend/.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   OPENAI_API_KEY=sk-...
   GOOGLE_AI_API_KEY=...
   ```

2. **Uncomment real API calls** in `backend/services/llm_client.py`:
   - Look for comments starting with `# PRODUCTION CODE`
   - Uncomment the actual API call code
   - Comment out the mock response code

3. **Update market data loader** in `backend/services/data_loader.py`:
   - Uncomment the `yfinance` call in `load_market_data()`
   - This will fetch real stock price data

The frontend automatically handles both mock and real API responses!

## 🎮 How to Use

### 1. View Agent Status
The homepage shows all active agents (Technical Analyst, Sentiment Analyst, Debate Team, and 3 Traders).

### 2. Run a Debate
Click "Run Debate" to see AI agents debate whether to buy, sell, or hold a stock. This shows:
- Bull arguments (why to buy)
- Bear arguments (why to be cautious)
- Multi-round debate
- Final decision with confidence level

### 3. Run a Simulation
Use the Simulation Controls to:
- Select a ticker (AAPL, MSFT, NVDA)
- Set date range
- Run full simulation

The simulation will:
1. Analyze each trading day
2. Conduct debates
3. Let each trader make decisions
4. Track portfolio performance

### 4. View Results
After simulation completes, see:
- Performance comparison chart
- Detailed results table
- Individual trader portfolios

## 🏗️ Architecture

### Backend (Python/FastAPI)

**Multi-Agent System**:
- `TechnicalAnalyst`: Analyzes price data and technical indicators
- `SentimentAnalyst`: Analyzes Reddit/Twitter sentiment
- `DebateTeam`: Conducts bull vs bear debates (KEY INNOVATION)
- `Trader`: Makes trading decisions (3 instances with different LLMs)

**Services**:
- `LLMClient`: Handles API calls to Claude, GPT-4, Gemini
- `DataLoader`: Loads and processes market + sentiment data

### Frontend (Next.js/React)

**Components**:
- `AgentStatusCard`: Shows agent status
- `DebateViewer`: Shows debate transcript (KEY FEATURE)
- `PerformanceChart`: Shows performance results
- `SimulationControls`: Run simulations

**API Client** (`src/lib/api.ts`):
- Clear integration points for all endpoints
- Falls back to mock data when backend unavailable
- Type-safe with TypeScript interfaces

## 📊 Data

The project includes historical data:
- **Reddit Sentiment** (`backend/data/reddit_sentiment.csv`): 2020 posts about AAPL, MSFT
- **Twitter Sentiment** (`backend/data/twitter_sentiment.csv`): 2020 tweets about AAPL, MSFT

Market data is fetched via `yfinance` (or mocked if not available).

## 🎯 Key Innovation: Debate Mechanism

Unlike traditional trading bots that make instant decisions, this system uses a **structured debate**:

1. **Technical & Sentiment Analysis** first
2. **Bull Agent** makes case for buying
3. **Bear Agent** argues for caution
4. **Multi-round debate** refines arguments
5. **Final synthesis** determines action

This provides:
- **Explainability**: See WHY decisions were made
- **Better reasoning**: Considers multiple perspectives
- **Transparency**: Every decision is auditable

## 🔧 Customization

### Add New Tickers
Edit `backend/config.py`:
```python
tickers: str = "AAPL,MSFT,NVDA,TSLA"
```

### Change Date Range
Edit `backend/config.py` or pass to simulation API:
```python
start_date: str = "2020-07-01"
end_date: str = "2020-09-30"
```

### Adjust Models
Edit `backend/config.py`:
```python
analyst_model: str = "claude-haiku"      # Fast, cheap
debate_model: str = "claude-sonnet-4"    # Best reasoning
trader_model: str = "claude-sonnet-4"    # Your choice
```

### Add More Traders
In `backend/routers/agents.py`, add:
```python
new_trader = Trader(model_type="claude", name="Conservative Trader")
```

## 📝 Development Notes

### Mock vs Real Data

The system is designed to work in two modes:

**Mock Mode** (current default):
- Uses generated responses for LLM calls
- Uses generated market data
- Perfect for development and demonstration

**Production Mode**:
- Requires API keys for Claude, GPT-4, Gemini
- Fetches real market data via yfinance
- See "Making Endpoints Functional" section above

### API Documentation

Visit http://localhost:8000/docs for interactive API documentation with:
- All endpoints listed
- Request/response schemas
- Try it out functionality

## 🎓 Learning Resources

- **Project Documentation**: See `claude/` directory
- **API Docs**: http://localhost:8000/docs
- **Code Comments**: All files have inline comments explaining functionality

## 🐛 Troubleshooting

**Backend won't start**:
- Check Python version: `python --version` (need 3.10+)
- Install dependencies: `pip install -r requirements.txt`
- Check port 8000 is free: `lsof -i :8000`

**Frontend won't start**:
- Check Node version: `node --version` (need 18+)
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- Check port 3000 is free

**API calls failing**:
- Backend running? Check http://localhost:8000/api/health
- CORS errors? Backend has CORS enabled for localhost:3000
- Using mock data? That's normal - set API keys to use real LLMs

**No data showing**:
- Check CSV files in `backend/data/`
- Check date range matches available data (2020)
- Use ticker AAPL or MSFT (others may not have data)

## 🚀 Next Steps

1. **Add API Keys** to use real LLM calls
2. **Extend date range** with more historical data
3. **Add more tickers** to the simulation
4. **Implement backtesting** with different strategies
5. **Add real-time trading** (paper trading)
6. **Deploy** to production (backend + frontend)

## 📄 License

This project is for educational and demonstration purposes.

## 🙏 Acknowledgments

- Built for Cal Hacks hackathon
- Based on TradingAgents research
- Uses Claude, GPT-4, and Gemini APIs
- Market data from yfinance
- Sentiment data from Kaggle

---

**Ready to see AI agents debate trading decisions? Start the servers and visit http://localhost:3000!**
