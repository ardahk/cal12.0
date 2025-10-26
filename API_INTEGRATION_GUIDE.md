# API Integration Guide

This document shows exactly where and how to integrate real API calls to make the application fully functional.

## Overview

The application is built with **clear separation between demo mode and production mode**:

- **Demo Mode** (current): Uses mock responses, works out of the box
- **Production Mode**: Requires API keys, makes real LLM calls

## 🔑 Step 1: Get API Keys

### Anthropic (Claude)
1. Go to https://console.anthropic.com/
2. Create an account or sign in
3. Navigate to API Keys
4. Create a new key
5. Copy the key (starts with `sk-ant-`)

### OpenAI (GPT-4)
1. Go to https://platform.openai.com/
2. Create an account or sign in
3. Navigate to API Keys
4. Create a new key
5. Copy the key (starts with `sk-`)

### Google (Gemini)
1. Go to https://ai.google.dev/
2. Create an account or sign in
3. Get an API key
4. Copy the key

## 🔧 Step 2: Configure Backend

### Add API Keys

Create or edit `backend/.env`:

```bash
cd backend
cp .env.example .env
```

Edit `.env`:
```env
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
OPENAI_API_KEY=sk-your-actual-key-here
GOOGLE_AI_API_KEY=your-actual-key-here

INITIAL_CAPITAL=10000.0
MAX_POSITION_SIZE=0.3

START_DATE=2020-07-01
END_DATE=2020-09-30
TICKERS=AAPL,MSFT
```

## 🎯 Step 3: Enable Real API Calls

### File 1: `backend/services/llm_client.py`

**Current (Mock Mode)**:
```python
async def call_claude(self, prompt: str, model: str = "claude-sonnet-4-20250514", temperature: float = 0.7) -> str:
    """Call Claude API"""
    # MOCK RESPONSE - Replace with real API call
    print(f"[MOCK] Claude called with model: {model}")
    return self._mock_response("claude", prompt)
```

**Change to (Production Mode)**:
```python
async def call_claude(self, prompt: str, model: str = "claude-sonnet-4-20250514", temperature: float = 0.7) -> str:
    """Call Claude API"""
    try:
        message = self.anthropic_client.messages.create(
            model=model,
            max_tokens=2048,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    except Exception as e:
        print(f"Claude API error: {e}")
        return json.dumps({"error": str(e)})
```

**Do the same for**:
- `call_gpt()` - uncomment the OpenAI code
- `call_gemini()` - uncomment the Google code

### File 2: `backend/services/data_loader.py`

**Current (Mock Mode)**:
```python
def load_market_data(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Load market data from Yahoo Finance"""
    # MOCK DATA - Replace with real yfinance call
    print(f"[MOCK] Loading market data for {ticker}")

    # Generate mock price data
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    mock_data = {
        'Open': [100 + i * 0.5 for i in range(len(date_range))],
        ...
    }
```

**Change to (Production Mode)**:
```python
def load_market_data(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Load market data from Yahoo Finance"""
    import yfinance as yf

    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date, end=end_date)
    return df
```

### File 3: `backend/services/llm_client.py` - Initialize Clients

**Current (Mock Mode)**:
```python
def __init__(self):
    # In production, initialize clients here:
    # self.anthropic_client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    # etc.
    pass
```

**Change to (Production Mode)**:
```python
def __init__(self):
    import anthropic
    import openai
    from google import generativeai as genai

    self.anthropic_client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    self.openai_client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
    genai.configure(api_key=settings.google_ai_api_key)
    self.gemini_model = genai.GenerativeModel('gemini-pro')
```

## 📝 Step 4: Test the Integration

### 1. Test Backend Directly

```bash
cd backend
python -c "
from services.llm_client import llm_client
import asyncio

async def test():
    response = await llm_client.call_claude('Say hello')
    print(response)

asyncio.run(test())
"
```

Should see a real Claude response instead of mock data!

### 2. Test via API

Start the backend:
```bash
python main.py
```

Test with curl:
```bash
# This should now use real Claude API
curl -X POST "http://localhost:8000/api/agents/debate?ticker=AAPL&date=2020-07-15&rounds=2"
```

### 3. Test via Frontend

Start frontend:
```bash
cd frontend
npm run dev
```

Visit http://localhost:3000 and click "Run Debate" - you should see real AI-generated arguments!

## 🔍 How to Tell It's Working

### Mock Mode Signs:
- Console shows `[MOCK] Claude called with model: ...`
- Responses are generic and similar each time
- Instant responses (no API delay)

### Production Mode Signs:
- No `[MOCK]` messages in console
- Responses are unique and varied
- Slight delay for API calls (~1-3 seconds)
- Console shows actual API model names

## 💰 Cost Estimation

With real APIs enabled:

**Per Simulation (10 trading days)**:
- Technical Analysis: 10 calls × $0.001 = $0.01
- Sentiment Analysis: 10 calls × $0.001 = $0.01
- Debates: 10 × 2 rounds × 4 calls × $0.01 = $0.80
- Trader Decisions: 10 × 3 traders × $0.01 = $0.30

**Total per simulation: ~$1.12**

**Using Haiku for analysts saves ~90%**: Total ~$0.25

## 🎨 Frontend Configuration

The frontend automatically detects if the backend is using mock or real data. No changes needed!

However, you can configure the API URL:

Create `frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Or for production:
```env
NEXT_PUBLIC_API_URL=https://your-api.com
```

## 🚨 Common Issues

### API Key Not Working
- Check the key format (Claude: `sk-ant-`, OpenAI: `sk-`)
- Verify the key is active in the provider's dashboard
- Check you have credits/billing enabled

### Module Not Found Errors
```bash
pip install anthropic openai google-generativeai
```

### Rate Limits
- Add delays between calls: `await asyncio.sleep(1)`
- Use cheaper models (Haiku) for high-volume calls
- Cache results to avoid redundant calls

### API Timeout
- Increase timeout in API calls
- Check your internet connection
- Try a different model (some are slower)

## 📊 Monitoring API Usage

### Log Every Call

Add to `llm_client.py`:
```python
async def call_claude(self, prompt: str, model: str, temperature: float = 0.7) -> str:
    start = time.time()
    response = await self.anthropic_client.messages.create(...)
    elapsed = time.time() - start

    print(f"Claude API: {model} took {elapsed:.2f}s")
    return response.content[0].text
```

### Track Costs

```python
# In config.py
class Settings:
    track_costs: bool = True

# In llm_client.py
if settings.track_costs:
    tokens = len(response.content[0].text.split()) * 1.3  # Rough estimate
    cost = tokens * 0.000001  # Adjust per model
    print(f"Estimated cost: ${cost:.4f}")
```

## 🎯 Optimization Tips

### Use Cheaper Models for Analysis
```python
# In config.py
analyst_model: str = "claude-haiku-20240307"  # Fast & cheap
debate_model: str = "claude-sonnet-4"          # Best for reasoning
trader_model: str = "claude-sonnet-4"          # Best for decisions
```

### Cache Analysis Results
```python
# Add to data_loader.py
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_analysis(ticker, date):
    return technical_analyst.analyze(ticker, date)
```

### Batch API Calls
```python
# Instead of:
for date in dates:
    await analyze(date)

# Do:
tasks = [analyze(date) for date in dates]
await asyncio.gather(*tasks)
```

## ✅ Final Checklist

- [ ] API keys added to `backend/.env`
- [ ] Real API calls uncommented in `llm_client.py`
- [ ] Real market data enabled in `data_loader.py`
- [ ] Client initialization uncommented
- [ ] Tested with a simple API call
- [ ] Tested via API endpoint
- [ ] Tested via frontend
- [ ] Monitoring/logging set up
- [ ] Cost optimization applied

## 🎉 Success!

Once all steps are complete, your application will be using real AI models to:
- Analyze stocks with Claude Haiku
- Conduct debates with Claude Sonnet 4
- Make trading decisions with all three models
- Show real, varied, intelligent reasoning

The frontend will automatically display the real AI responses with no changes needed!

---

**Need help?** Check the inline comments in the code - every integration point is clearly marked!
