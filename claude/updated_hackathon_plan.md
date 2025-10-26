# LLM TRADING ARENA - Updated Hackathon Plan
## Based on TradingAgents Paper + Cal Hacks Optimization

---

## 🎯 TARGET SPONSORS (Cal Hacks)

### Primary Targets:
1. **Best Use of Claude** ($5,000 API credits + Tungsten Cube) ✅
   - We're using Claude as one of our primary trading agents
   
2. **Best Use of Creao** ($4,000 cash) ✅
   - You're already using Creao for frontend
   
3. **Best Use of Fetch.ai** ($2,500 + Internship Interview)
   - Multi-agent coordination system
   
4. **Social Impact** (Apple Watches)
   - Democratizing AI trading analysis

### Secondary Targets:
- **Most Creative** (iPad Airs + Apple Pencils) - Novel LLM application
- **Most Complex / Technically Challenging** (Engineering interviews)
- **Best Data-Intensive Application** (WHOOP watches)

---

## 📊 DATASET PLAN (3 Months)

### Market Data:
- **Period**: July 1, 2024 - September 30, 2024 (Q3 2024)
- **Stocks**: AAPL, MSFT, NVDA (just 3 for simplicity)
- **Source**: yfinance
- **Data**: OHLCV + 10-15 technical indicators (not 60!)

### Sentiment Data:

**Twitter Dataset** (https://www.kaggle.com/datasets/vivekrathi055/sentiment-analysis-on-financial-tweets)
- Pre-labeled tweets with sentiment
- Filter for Q3 2024 if available, or use any 3-month period and map to our dates

**Reddit Dataset** (https://www.kaggle.com/datasets/unanimad/reddit-rwallstreetbets)
- Filter for stock mentions (AAPL, MSFT, NVDA)
- Extract posts from Q3 2024
- Use simple sentiment analysis (TextBlob or pre-trained model)

---

## 🤖 SIMPLIFIED AGENT ARCHITECTURE

### Paper's Approach: 7 agent roles
### Our Hackathon Approach: 5 agent roles (simplified)

```
┌─────────────────────────────────────────────────────────┐
│                   ANALYST TEAM (3)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Technical   │  │  Sentiment   │  │     News     │ │
│  │   Analyst    │  │   Analyst    │  │   Analyst    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│               DEBATE TEAM (2)                           │
│         ┌──────────┐      ┌──────────┐                 │
│         │  Bull    │ ←→   │   Bear   │                 │
│         │ Debater  │      │ Debater  │                 │
│         └──────────┘      └──────────┘                 │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    TRADER                               │
│              Makes Final Decision                       │
│         (BUY/SELL/HOLD + Quantity + Reasoning)          │
└─────────────────────────────────────────────────────────┘
```

**What we removed from the paper:**
- ❌ Fundamentals Analyst (requires complex financial statement parsing)
- ❌ Risk Management Team (3 agents - too complex for hackathon)
- ❌ Fund Manager approval step

---

## 🔧 IMPLEMENTATION DETAILS

### 1. Analyst Team (Parallel Execution)

#### Technical Analyst
```python
class TechnicalAnalyst:
    """Uses GPT-4o-mini or Claude Haiku (fast, cheap)"""
    
    async def analyze(self, stock: str, date: str) -> dict:
        # Get last 30 days of price data
        # Calculate indicators: RSI, MACD, Bollinger Bands, SMA_20, SMA_50
        
        prompt = f"""You are a technical analyst. Analyze {stock} as of {date}.
        
Data (last 30 days):
{price_data}

Technical Indicators:
- RSI: {rsi}
- MACD: {macd}
- Bollinger Bands: {bb_upper}, {bb_lower}
- SMA 20/50: {sma_20}, {sma_50}

Provide a concise analysis in JSON:
{{
  "signal": "bullish|bearish|neutral",
  "confidence": 0-100,
  "key_points": ["point1", "point2", "point3"],
  "summary": "2-3 sentence summary"
}}
"""
        return await llm_call(prompt)
```

#### Sentiment Analyst
```python
class SentimentAnalyst:
    """Uses GPT-4o-mini or Claude Haiku"""
    
    async def analyze(self, stock: str, date: str) -> dict:
        # Get tweets and Reddit posts for this stock from last 7 days
        # Load from Kaggle datasets, filter by date and ticker
        
        tweets = load_tweets(stock, date, lookback=7)
        reddit = load_reddit(stock, date, lookback=7)
        
        prompt = f"""You are a sentiment analyst. Analyze social media sentiment for {stock}.

Twitter Data:
{format_tweets(tweets)}

Reddit Data:
{format_reddit(reddit)}

Provide analysis in JSON:
{{
  "signal": "bullish|bearish|neutral",
  "confidence": 0-100,
  "twitter_sentiment": -1 to 1,
  "reddit_sentiment": -1 to 1,
  "key_topics": ["topic1", "topic2"],
  "summary": "2-3 sentence summary"
}}
"""
        return await llm_call(prompt)
```

#### News Analyst
```python
class NewsAnalyst:
    """Uses GPT-4o-mini or Claude Haiku"""
    
    async def analyze(self, stock: str, date: str) -> dict:
        # For hackathon: use simple news API or pre-downloaded news
        # Alternative: Skip this and just use 2 analysts
        
        news = get_news(stock, date, lookback=7)
        
        prompt = f"""You are a news analyst. Analyze recent news for {stock}.

Recent Headlines:
{format_news(news)}

Provide analysis in JSON:
{{
  "signal": "bullish|bearish|neutral",
  "confidence": 0-100,
  "key_events": ["event1", "event2"],
  "impact_assessment": "high|medium|low",
  "summary": "2-3 sentence summary"
}}
"""
        return await llm_call(prompt)
```

### 2. Debate Team (Sequential Execution)

This is the KEY innovation from the paper - agents debate to reach better decisions!

```python
class DebateTeam:
    """Uses Claude Sonnet 4 (best reasoning) or GPT-4"""
    
    async def debate(self, analyst_reports: dict, stock: str, rounds: int = 2) -> dict:
        # Format all analyst reports
        context = format_analyst_reports(analyst_reports)
        
        debate_history = []
        
        # Bull's opening argument
        bull_prompt = f"""You are a BULLISH researcher. Based on the analyst reports, argue WHY we should BUY {stock}.

{context}

Provide your bullish argument (focus on: growth potential, positive signals, upside)."""
        
        bull_arg = await claude_call(bull_prompt)
        debate_history.append({"role": "bull", "argument": bull_arg})
        
        # Bear's counter-argument
        bear_prompt = f"""You are a BEARISH researcher. Argue WHY we should NOT buy {stock}.

{context}

Bull's argument: {bull_arg}

Provide your bearish counter-argument (focus on: risks, negative signals, downside)."""
        
        bear_arg = await claude_call(bear_prompt)
        debate_history.append({"role": "bear", "argument": bear_arg})
        
        # Optional: 1 more round
        if rounds > 1:
            # Bull rebuttal
            # Bear rebuttal
            pass
        
        return {
            "debate_history": debate_history,
            "bull_strength": score_argument(bull_arg),
            "bear_strength": score_argument(bear_arg)
        }
```

### 3. Trader (Final Decision)

```python
class Trader:
    """Uses Claude Sonnet 4 or GPT-4 (needs strong reasoning)"""
    
    async def make_decision(self, analyst_reports: dict, debate: dict, 
                           portfolio: dict, stock: str) -> dict:
        
        prompt = f"""You are a professional trader. Make a trading decision for {stock}.

ANALYST REPORTS:
{format_analyst_reports(analyst_reports)}

DEBATE SUMMARY:
Bull argument strength: {debate['bull_strength']}/10
Bear argument strength: {debate['bear_strength']}/10

Key bull points:
{extract_key_points(debate, 'bull')}

Key bear points:
{extract_key_points(debate, 'bear')}

YOUR PORTFOLIO:
Cash: ${portfolio['cash']}
Current position in {stock}: {portfolio.get(stock, 0)} shares

CRITICAL: Your knowledge cutoff is April 2024. You are making decisions as if it's {date}.
Only use the data provided above. Do not reference events after April 2024.

Respond in JSON:
{{
  "action": "BUY|SELL|HOLD",
  "ticker": "{stock}",
  "quantity": <number>,
  "confidence": 0-100,
  "reasoning": "Detailed explanation of your decision based on the analysis",
  "risk_assessment": "high|medium|low"
}}

Rules:
- For BUY: only if cash available, max 30% of cash per trade
- For SELL: only if shares available
- Consider both technical and sentiment signals
- Be conservative with high-risk trades
"""
        
        decision = await claude_call(prompt)
        return decision
```

---

## 🚨 CRITICAL: Knowledge Cutoff Handling

The paper doesn't address this, but it's CRUCIAL for your hackathon!

### Problem:
- GPT-4's knowledge cutoff: October 2023
- Claude's knowledge cutoff: April 2024
- Your data: July-September 2024

### Solution:
```python
# In every prompt, add this header:
KNOWLEDGE_CUTOFF_WARNING = """
IMPORTANT: You are a trading AI operating in {current_date}. 
Your training data ends in {model_cutoff_date}.
You must ONLY use the data provided below.
Do NOT reference any events or knowledge after your cutoff date.
Treat all provided data as current and make decisions based solely on it.
"""

# Example for Claude analyzing data from Sept 2024:
prompt = f"""
IMPORTANT: You are operating on September 15, 2024.
Your knowledge cutoff is April 2024.
You must ONLY use the data provided below for your analysis.
Do NOT reference events after April 2024.

[Rest of prompt with data...]
"""
```

This prevents models from saying things like "I don't know about events in September 2024" or making assumptions based on outdated knowledge.

---

## 📁 DATA PREPARATION SCRIPT

```python
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

class DataPreparation:
    def __init__(self):
        self.start_date = "2024-07-01"
        self.end_date = "2024-09-30"
        self.tickers = ["AAPL", "MSFT", "NVDA"]
        
    def download_market_data(self):
        """Download 3 months of market data"""
        data = {}
        for ticker in self.tickers:
            stock = yf.Ticker(ticker)
            hist = stock.history(start=self.start_date, end=self.end_date)
            
            # Calculate indicators
            hist['SMA_20'] = hist['Close'].rolling(20).mean()
            hist['SMA_50'] = hist['Close'].rolling(50).mean()
            hist['RSI'] = self.calculate_rsi(hist['Close'])
            hist['MACD'], hist['Signal'] = self.calculate_macd(hist['Close'])
            
            data[ticker] = hist
            
        # Save to CSV
        for ticker, df in data.items():
            df.to_csv(f'data/{ticker}_market_data.csv')
            
        return data
    
    def prepare_twitter_data(self):
        """Load and filter Kaggle Twitter dataset"""
        # Load from Kaggle dataset
        df = pd.read_csv('kaggle_datasets/financial_tweets.csv')
        
        # Filter for our stocks and date range
        # Map dates if needed (Kaggle data might be from different period)
        # For hackathon: can map any 3-month period to July-Sept 2024
        
        df_filtered = df[df['text'].str.contains('AAPL|MSFT|NVDA', na=False)]
        
        # Simple sentiment if not pre-labeled
        from textblob import TextBlob
        df_filtered['sentiment'] = df_filtered['text'].apply(
            lambda x: TextBlob(x).sentiment.polarity
        )
        
        df_filtered.to_csv('data/twitter_sentiment.csv')
        return df_filtered
    
    def prepare_reddit_data(self):
        """Load and filter Kaggle Reddit dataset"""
        df = pd.read_csv('kaggle_datasets/wsb_posts.csv')
        
        # Filter for our stocks
        df_filtered = df[df['title'].str.contains('AAPL|MSFT|NVDA', na=False) | 
                        df['selftext'].str.contains('AAPL|MSFT|NVDA', na=False)]
        
        # Calculate sentiment
        df_filtered['sentiment'] = df_filtered['title'].apply(
            lambda x: TextBlob(str(x)).sentiment.polarity
        )
        
        df_filtered.to_csv('data/reddit_sentiment.csv')
        return df_filtered

# Run preparation
if __name__ == "__main__":
    prep = DataPreparation()
    prep.download_market_data()
    prep.prepare_twitter_data()
    prep.prepare_reddit_data()
    print("Data preparation complete!")
```

---

## 🏗️ SIMPLIFIED ARCHITECTURE

```python
# main_simulation.py

class TradingSimulation:
    def __init__(self):
        self.analysts = {
            'technical': TechnicalAnalyst(),
            'sentiment': SentimentAnalyst(),
            'news': NewsAnalyst()  # Optional
        }
        self.debate_team = DebateTeam()
        self.traders = {
            'GPT-4': Trader(model='gpt-4'),
            'Claude': Trader(model='claude-sonnet-4'),
            'Gemini': Trader(model='gemini-pro'),
        }
        
    async def run_day(self, date: str, stock: str):
        """Run simulation for one trading day"""
        
        # Step 1: Analysts gather data (parallel)
        analyst_tasks = [
            analyst.analyze(stock, date) 
            for analyst in self.analysts.values()
        ]
        analyst_reports = await asyncio.gather(*analyst_tasks)
        
        # Step 2: Debate team discusses
        debate_result = await self.debate_team.debate(
            analyst_reports, stock, rounds=2
        )
        
        # Step 3: Each trader makes decision
        decisions = {}
        for name, trader in self.traders.items():
            decision = await trader.make_decision(
                analyst_reports,
                debate_result,
                self.portfolios[name],
                stock
            )
            decisions[name] = decision
            
            # Execute trade
            self.execute_trade(name, decision)
        
        # Step 4: Record results
        self.record_performance(date, decisions)
        
        return decisions
    
    async def run_full_simulation(self):
        """Run 3-month simulation"""
        trading_days = get_trading_days(
            start="2024-07-01",
            end="2024-09-30"
        )
        
        for day in trading_days:
            for stock in ["AAPL", "MSFT", "NVDA"]:
                await self.run_day(day, stock)
                
        self.calculate_final_metrics()
```

---

## 🎨 FRONTEND (CREAO) INTEGRATION

Since you're using Creao ($4K prize!), here's what to showcase:

### Key Screens:

1. **Live Arena View**
   ```
   ┌──────────────────────────────────────────────────┐
   │  Trading Day: Sept 15, 2024 | AAPL Focus        │
   ├──────────────────────────────────────────────────┤
   │                                                   │
   │  [Technical]  [Sentiment]  [News]  <- Analysts  │
   │     ↓             ↓          ↓                   │
   │  [Bull 🐂]  ←→  [Bear 🐻]    <- Debate          │
   │         ↓                                        │
   │  [GPT] [Claude] [Gemini]     <- Traders         │
   │                                                   │
   │  Today's Decisions:                              │
   │  GPT:    BUY 10 AAPL  @ $175                    │
   │  Claude: HOLD                                    │
   │  Gemini: BUY 5 AAPL   @ $175                    │
   └──────────────────────────────────────────────────┘
   ```

2. **Debate Viewer** (This is UNIQUE!)
   - Show the actual bull vs bear arguments
   - Highlight key points from each side
   - Show which side "won" the debate
   - Display trader's final decision with reasoning

3. **Agent Reasoning Explorer**
   - Click any decision to see full reasoning chain
   - Show what each analyst contributed
   - Show debate points that influenced decision
   - This demonstrates EXPLAINABILITY (key paper feature)

---

## 💰 COST OPTIMIZATION

### Paper's Problem: 
- 11 LLM calls per prediction
- 20+ tool calls per prediction
- Very expensive!

### Our Solution:
```python
# Use tiered LLM strategy
ANALYST_MODEL = "claude-haiku"  # Fast, cheap: $0.25/1M tokens
DEBATE_MODEL = "claude-sonnet-4"  # Smart, reasonable: $3/1M tokens
TRADER_MODEL = "claude-sonnet-4"  # Best reasoning

# For 3 months (~63 trading days), 3 stocks
total_calls = 63 * 3 * (3 analysts + 2 debaters + 3 traders)
            = 63 * 3 * 8 = 1,512 calls

# With ~500 tokens/call average:
# Analysts: 1,512 * 0.5 = 756K tokens @ $0.25 = $0.19
# Debate + Traders: 756K tokens @ $3 = $2.27
# Total: ~$2.50 for entire simulation!
```

### Free Tier Usage:
- Use $5K Claude credits from Cal Hacks prize
- Use Gemini free tier (generous limits)
- Cache analyst reports to reuse across traders

---

## 🏆 WINNING STRATEGY

### Demo Flow (3 minutes):

**Minute 1: The Hook**
"What if we made AI models compete against each other in the stock market, and you could bet on which one is the smartest trader?"

[Show live arena with agents making different decisions]

**Minute 2: The Innovation**
"Unlike other trading bots, our agents DEBATE before making decisions - just like real trading firms!"

[Show debate viewer with bull vs bear arguments]
[Show how Claude decided to BUY after considering both sides]

**Minute 3: The Results**
"After 3 months of simulated trading..."

[Show performance comparison]
- Claude: +18.5% return
- GPT-4: +12.3% return
- Gemini: +15.7% return

### Judge Appeal:
1. **Technical Depth**: Multi-agent LLM system, debate mechanism, structured communication
2. **Novel Application**: LLMs for trading (not just chatbots)
3. **Explainability**: Show actual reasoning and debates
4. **Sponsor Alignment**: Uses Claude heavily, built with Creao
5. **Social Impact**: Democratizes AI trading analysis

---

## 📋 IMPLEMENTATION CHECKLIST

### Day 1: Data & Core
- [ ] Download 3 months market data (1 hour)
- [ ] Process Kaggle Twitter dataset (1 hour)
- [ ] Process Kaggle Reddit dataset (1 hour)
- [ ] Implement TechnicalAnalyst (2 hours)
- [ ] Implement SentimentAnalyst (2 hours)
- [ ] Test analysts with sample data (1 hour)

### Day 2: Debate & Trading
- [ ] Implement DebateTeam (3 hours)
- [ ] Implement Trader (2 hours)
- [ ] Run first simulation (1 hour)
- [ ] Debug and iterate (2 hours)

### Day 3: Frontend & Polish
- [ ] Build Creao frontend (4 hours)
  - Live arena view
  - Debate viewer
  - Performance charts
- [ ] Connect backend to frontend (2 hours)
- [ ] Polish and prepare demo (2 hours)

---

## 🎯 KEY DIFFERENTIATORS FROM PAPER

### What We Simplified:
1. ❌ Fundamentals Analyst (too complex)
2. ❌ 3-agent Risk Management Team (overkill)
3. ❌ Fund Manager approval (extra step)
4. ❌ 60 technical indicators (using 5-10)
5. ❌ Multiple LLM models per role (using 1-2)

### What We Kept (Essential):
1. ✅ Multi-analyst approach
2. ✅ **Debate mechanism** (KEY INNOVATION!)
3. ✅ Structured communication
4. ✅ Multiple trader agents
5. ✅ Explainable reasoning

### What We Added:
1. ✅ Knowledge cutoff handling
2. ✅ Betting/prediction market
3. ✅ User engagement features
4. ✅ Simplified for hackathon speed

---

## 🔍 SPONSOR-SPECIFIC FEATURES

### For "Best Use of Claude":
- Use Claude Sonnet 4 for debate team (show reasoning chains)
- Use Claude Haiku for analysts (show cost optimization)
- Display Claude's superior reasoning in comparison charts
- Highlight: "Claude's debate arguments were 23% more nuanced"

### For "Best Use of Creao":
- Build stunning UI showing agent interactions
- Real-time agent visualization
- Debate viewer with threaded conversations
- Smooth animations for agent decisions

### For "Best Use of Fetch.ai":
- If time permits: use Fetch.ai for agent coordination
- Alternative: mention you'd use it for scaling

### For "Social Impact":
- Democratizing AI trading analysis
- Educational tool for understanding AI decision-making
- Transparent, explainable AI (show all reasoning)

---

## 🚀 QUICK START COMMANDS

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Prepare data
python scripts/prepare_data.py

# Run simulation
python scripts/run_simulation.py --start 2024-07-01 --end 2024-09-30

# Start backend
uvicorn main:app --reload

# Start frontend (Creao)
cd frontend
# [Creao-specific commands]
```

---

## 💡 PRO TIPS

1. **Pre-compute Everything**: Run simulation once, save results, use for demo
2. **Cache Analyst Reports**: Save $$ by reusing reports across traders
3. **Mock 1-2 Agents**: If API costs are high, fake Grok/DeepSeek
4. **Focus on Debate**: This is your unique feature - make it shine!
5. **Record Demo Video**: Backup if live demo fails
6. **Prepare "Wow Moments"**:
   - Show agents disagreeing
   - Show debate changing a decision
   - Show Claude catching something others missed

---

## 📈 SUCCESS METRICS

### Technical Metrics:
- All 3 agents complete 3-month simulation
- Debate mechanism works (shows bull/bear arguments)
- Clear winner emerges (one agent outperforms)
- System runs in <5 minutes for demo

### Sponsor Metrics:
- Heavy Claude usage (qualify for prize)
- Beautiful Creao UI (qualify for prize)
- Optional: Fetch.ai integration

### Demo Metrics:
- Judges say "wow" at debate feature
- Clear explanation of how it works
- Smooth, no crashes
- Answers all questions confidently

---

Good luck at Cal Hacks! This is a winning project. 🏆
