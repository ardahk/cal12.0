# Quick Start Guide

Get the LLM Trading Arena running in 5 minutes!

## Terminal 1: Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
python main.py
```

✅ Backend running at http://localhost:8000
✅ API Docs at http://localhost:8000/docs

## Terminal 2: Frontend

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

✅ Frontend running at http://localhost:3000

## What You'll See

1. **Agent Status Cards** - 6 AI agents ready to trade
2. **Simulation Controls** - Run a simulation with AAPL, MSFT, or NVDA
3. **Debate Viewer** - Watch bull vs bear AI debates (click "Run Debate")
4. **Performance Charts** - See which AI model trades best

## Current Mode: Mock Data

The app currently uses **mock LLM responses** for demonstration. This lets you:
- ✅ See the full UI and UX
- ✅ Understand the architecture
- ✅ Test all API endpoints
- ✅ View debates and simulations

## Make It Functional with Real AI

### Step 1: Get API Keys

- **Anthropic (Claude)**: https://console.anthropic.com/
- **OpenAI (GPT-4)**: https://platform.openai.com/
- **Google (Gemini)**: https://ai.google.dev/

### Step 2: Add to Backend

```bash
cd backend
cp .env.example .env
# Edit .env and add your keys
```

### Step 3: Enable Real API Calls

In `backend/services/llm_client.py`:
1. Find the `# PRODUCTION CODE` comments
2. Uncomment the real API call code
3. Comment out the `_mock_response()` calls

In `backend/services/data_loader.py`:
1. Uncomment the `yfinance` call in `load_market_data()`
2. Comment out the mock data generation

### Step 4: Restart Backend

```bash
# Stop the backend (Ctrl+C)
python main.py
```

Now you're using real AI models!

## Test the API

Visit http://localhost:8000/docs and try:

- `GET /api/agents/status` - See all agents
- `POST /api/agents/debate` - Run a debate with ticker=AAPL
- `POST /api/simulation/run` - Start a simulation

## Example API Calls

### Using curl:

```bash
# Get agent status
curl http://localhost:8000/api/agents/status

# Run a debate
curl -X POST "http://localhost:8000/api/agents/debate?ticker=AAPL&date=2020-07-15&rounds=2"

# Start simulation
curl -X POST "http://localhost:8000/api/simulation/run?ticker=AAPL&start_date=2020-07-01&end_date=2020-07-10"

# Check status
curl http://localhost:8000/api/simulation/status

# Get results
curl http://localhost:8000/api/simulation/results/summary
```

## Troubleshooting

**Port already in use?**
```bash
# Backend (8000)
lsof -i :8000
kill -9 <PID>

# Frontend (3000)
lsof -i :3000
kill -9 <PID>
```

**Dependencies not installing?**
```bash
# Backend
python --version  # Need 3.10+
pip install --upgrade pip

# Frontend
node --version  # Need 18+
npm cache clean --force
```

**API calls failing?**
- Check backend is running: http://localhost:8000/api/health
- Check browser console for errors
- Backend logs show request details

## What to Try

1. **Run a Debate**: Click "Run Debate" to see bull vs bear arguments
2. **Start a Simulation**: Pick AAPL, 2020-07-01 to 2020-07-10
3. **Check API Docs**: http://localhost:8000/docs
4. **View Agent Status**: See all 6 agents on the homepage
5. **Compare Models**: See which AI (Claude/GPT/Gemini) trades best

## Next Steps

- Read the full [README.md](README.md) for architecture details
- Check [claude/](claude/) directory for project documentation
- Explore the code - it's well commented!
- Add your API keys to use real AI models

---

**Questions?** Check README.md or the code comments - everything is documented!
