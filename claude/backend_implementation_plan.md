# BACKEND IMPLEMENTATION PLAN - LLM Trading Arena

## Overview
This document provides a complete plan for building the backend API that powers the LLM Trading Arena. We'll use Python with FastAPI for speed and ease of use during the hackathon.

---

## Tech Stack

### Core:
- **Framework**: FastAPI (Python 3.10+)
- **Database**: SQLite (dev) → PostgreSQL (production)
- **ORM**: SQLAlchemy
- **LLM Integration**: OpenAI SDK, Anthropic SDK, Google AI SDK
- **Market Data**: yfinance library
- **Task Queue**: (Optional) Celery for async tasks

### Libraries:
```bash
pip install fastapi uvicorn sqlalchemy pydantic python-dotenv
pip install openai anthropic google-generativeai
pip install yfinance pandas numpy
pip install python-multipart python-jose[cryptography] passlib
```

---

## Project Structure

```
backend/
├── main.py                 # FastAPI app entry point
├── config.py               # Configuration and environment variables
├── requirements.txt        # Dependencies
├── .env                    # Environment variables (API keys)
├── database/
│   ├── __init__.py
│   ├── connection.py       # Database connection
│   └── models.py           # SQLAlchemy models
├── agents/
│   ├── __init__.py
│   ├── base_agent.py       # Base agent class
│   ├── gpt_agent.py        # GPT-4 implementation
│   ├── claude_agent.py     # Claude implementation
│   ├── gemini_agent.py     # Gemini implementation
│   ├── grok_agent.py       # Grok implementation
│   └── deepseek_agent.py   # DeepSeek implementation
├── trading/
│   ├── __init__.py
│   ├── simulator.py        # Trading simulation engine
│   ├── portfolio.py        # Portfolio management
│   └── market_data.py      # Market data fetching
├── routers/
│   ├── __init__.py
│   ├── agents.py           # Agent endpoints
│   ├── trades.py           # Trade endpoints
│   └── leaderboard.py      # Leaderboard endpoints
├── services/
│   ├── __init__.py
│   ├── sentiment.py        # Social media sentiment analysis
│   └── indicators.py       # Technical indicators
├── data/
│   ├── historical_prices.csv   # Pre-downloaded market data
│   └── sentiment_data.csv      # Pre-downloaded sentiment data
└── scripts/
    ├── download_data.py        # Script to fetch historical data
    └── run_simulation.py       # Script to run trading simulation
```

---

## Step 1: Setup and Configuration

### 1.1 Install Dependencies

Create `requirements.txt`:
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-dotenv==1.0.0
openai==1.3.0
anthropic==0.7.0
google-generativeai==0.3.0
yfinance==0.2.32
pandas==2.1.3
numpy==1.26.2
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
aiosqlite==0.19.0
```

### 1.2 Environment Variables

Create `.env`:
```env
# API Keys
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
GOOGLE_AI_API_KEY=your-google-ai-key
# Add others as needed (Grok, DeepSeek)

# Database
DATABASE_URL=sqlite:///./llm_trading.db
# For production: postgresql://user:password@localhost/llm_trading

# App Config
INITIAL_CAPITAL=10000
COMPETITION_DURATION_DAYS=7
```

### 1.3 Configuration Module

Create `config.py`:
```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # API Keys
    openai_api_key: str
    anthropic_api_key: str
    google_ai_api_key: str
    
    # Database
    database_url: str = "sqlite:///./llm_trading.db"
    
    # Trading Config
    initial_capital: float = 10000.0
    competition_duration_days: int = 7
    
    # Market Config
    available_tickers: list[str] = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
```

---

## Step 2: Database Models

Create `database/models.py`:
```python
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class AgentType(str, enum.Enum):
    GPT4 = "GPT-4"
    CLAUDE = "Claude"
    GEMINI = "Gemini"
    GROK = "Grok"
    DEEPSEEK = "DeepSeek"

class TradeAction(str, enum.Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    agent_type = Column(Enum(AgentType))
    initial_capital = Column(Float)
    current_capital = Column(Float)
    portfolio_value = Column(Float)
    total_return = Column(Float)
    sharpe_ratio = Column(Float, nullable=True)
    max_drawdown = Column(Float, nullable=True)
    win_rate = Column(Float, nullable=True)
    total_trades = Column(Integer, default=0)
    
    trades = relationship("Trade", back_populates="agent")
    performance_history = relationship("PerformanceSnapshot", back_populates="agent")

class Trade(Base):
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    action = Column(Enum(TradeAction))
    ticker = Column(String)
    quantity = Column(Integer)
    price = Column(Float)
    reasoning = Column(String, nullable=True)
    
    agent = relationship("Agent", back_populates="trades")

class PerformanceSnapshot(Base):
    __tablename__ = "performance_snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    portfolio_value = Column(Float)
    cash = Column(Float)
    positions = Column(String)  # JSON string of positions

    agent = relationship("Agent", back_populates="performance_history")
```

Create `database/connection.py`:
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import get_settings
from database.models import Base

settings = get_settings()

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## Step 3: Agent Implementation

### 3.1 Base Agent Class

Create `agents/base_agent.py`:
```python
from abc import ABC, abstractmethod
from typing import Dict, Any
import json

class BaseAgent(ABC):
    def __init__(self, name: str, initial_capital: float):
        self.name = name
        self.cash = initial_capital
        self.positions: Dict[str, int] = {}  # ticker -> quantity
        
    @abstractmethod
    async def make_decision(self, market_data: Dict[str, Any], sentiment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a trading decision based on market data and sentiment.
        
        Returns:
            {
                "action": "BUY" | "SELL" | "HOLD",
                "ticker": "AAPL",
                "quantity": 10,
                "reasoning": "explanation"
            }
        """
        pass
    
    def get_portfolio_value(self, current_prices: Dict[str, float]) -> float:
        """Calculate total portfolio value."""
        value = self.cash
        for ticker, quantity in self.positions.items():
            value += quantity * current_prices.get(ticker, 0)
        return value
    
    def execute_trade(self, action: str, ticker: str, quantity: int, price: float) -> bool:
        """Execute a trade if valid."""
        if action == "BUY":
            cost = quantity * price
            if self.cash >= cost:
                self.cash -= cost
                self.positions[ticker] = self.positions.get(ticker, 0) + quantity
                return True
            return False
            
        elif action == "SELL":
            if self.positions.get(ticker, 0) >= quantity:
                self.cash += quantity * price
                self.positions[ticker] -= quantity
                if self.positions[ticker] == 0:
                    del self.positions[ticker]
                return True
            return False
            
        return True  # HOLD
    
    def _format_prompt(self, market_data: Dict[str, Any], sentiment_data: Dict[str, Any]) -> str:
        """Format the prompt for LLM."""
        prompt = f"""You are a professional day trader managing a portfolio. Analyze the following data and make a trading decision.

MARKET DATA:
{json.dumps(market_data, indent=2)}

SENTIMENT DATA:
{json.dumps(sentiment_data, indent=2)}

YOUR PORTFOLIO:
- Cash available: ${self.cash:.2f}
- Current positions: {json.dumps(self.positions, indent=2)}

Respond in JSON format:
{{
  "action": "BUY|SELL|HOLD",
  "ticker": "TICKER_SYMBOL",
  "quantity": <number>,
  "reasoning": "Your detailed explanation"
}}

Important rules:
1. Only trade if you're confident (don't trade just for the sake of trading)
2. Consider risk management (don't use all your cash on one trade)
3. Factor in both technical indicators and sentiment
4. Provide clear reasoning for your decision
"""
        return prompt
```

### 3.2 GPT-4 Agent

Create `agents/gpt_agent.py`:
```python
from agents.base_agent import BaseAgent
from openai import AsyncOpenAI
from config import get_settings
import json

class GPTAgent(BaseAgent):
    def __init__(self, name: str = "GPT-4", initial_capital: float = 10000):
        super().__init__(name, initial_capital)
        settings = get_settings()
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
    
    async def make_decision(self, market_data: dict, sentiment_data: dict) -> dict:
        prompt = self._format_prompt(market_data, sentiment_data)
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are an expert trading AI. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            decision = json.loads(response.choices[0].message.content)
            return decision
            
        except Exception as e:
            print(f"Error in GPT agent: {e}")
            return {
                "action": "HOLD",
                "ticker": "",
                "quantity": 0,
                "reasoning": f"Error occurred: {str(e)}"
            }
```

### 3.3 Claude Agent

Create `agents/claude_agent.py`:
```python
from agents.base_agent import BaseAgent
from anthropic import AsyncAnthropic
from config import get_settings
import json
import re

class ClaudeAgent(BaseAgent):
    def __init__(self, name: str = "Claude", initial_capital: float = 10000):
        super().__init__(name, initial_capital)
        settings = get_settings()
        self.client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    
    async def make_decision(self, market_data: dict, sentiment_data: dict) -> dict:
        prompt = self._format_prompt(market_data, sentiment_data)
        
        try:
            message = await self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = message.content[0].text
            
            # Extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                decision = json.loads(json_match.group())
            else:
                decision = json.loads(content)
                
            return decision
            
        except Exception as e:
            print(f"Error in Claude agent: {e}")
            return {
                "action": "HOLD",
                "ticker": "",
                "quantity": 0,
                "reasoning": f"Error occurred: {str(e)}"
            }
```

### 3.4 Gemini Agent

Create `agents/gemini_agent.py`:
```python
from agents.base_agent import BaseAgent
import google.generativeai as genai
from config import get_settings
import json
import re

class GeminiAgent(BaseAgent):
    def __init__(self, name: str = "Gemini", initial_capital: float = 10000):
        super().__init__(name, initial_capital)
        settings = get_settings()
        genai.configure(api_key=settings.google_ai_api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def make_decision(self, market_data: dict, sentiment_data: dict) -> dict:
        prompt = self._format_prompt(market_data, sentiment_data)
        
        try:
            response = await self.model.generate_content_async(prompt)
            content = response.text
            
            # Extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                decision = json.loads(json_match.group())
            else:
                decision = json.loads(content)
                
            return decision
            
        except Exception as e:
            print(f"Error in Gemini agent: {e}")
            return {
                "action": "HOLD",
                "ticker": "",
                "quantity": 0,
                "reasoning": f"Error occurred: {str(e)}"
            }
```

**Note**: For Grok and DeepSeek, follow similar patterns. If APIs aren't available, you can:
1. Use placeholder implementations that return random/rule-based decisions
2. Use open-source models via Hugging Face
3. Skip them for MVP and add later

---

## Step 4: Trading Simulator

Create `trading/simulator.py`:
```python
from typing import Dict, List
from datetime import datetime, timedelta
from agents.base_agent import BaseAgent
from database.models import Agent as AgentModel, Trade, PerformanceSnapshot
from sqlalchemy.orm import Session
import json

class TradingSimulator:
    def __init__(self, agents: List[BaseAgent], market_data: Dict, sentiment_data: Dict):
        self.agents = agents
        self.market_data = market_data
        self.sentiment_data = sentiment_data
        self.current_day = 0
        
    async def run_simulation(self, db: Session, num_days: int = 30):
        """Run the trading simulation for specified number of days."""
        
        for day in range(num_days):
            self.current_day = day
            print(f"\n=== Day {day + 1} ===")
            
            # Get market data for this day
            day_market_data = self._get_day_data(day)
            day_sentiment_data = self._get_sentiment_data(day)
            current_prices = day_market_data["prices"]
            
            # Each agent makes a decision
            for agent in self.agents:
                try:
                    # Get agent decision
                    decision = await agent.make_decision(day_market_data, day_sentiment_data)
                    
                    # Execute trade
                    if decision["action"] != "HOLD":
                        success = agent.execute_trade(
                            decision["action"],
                            decision["ticker"],
                            decision["quantity"],
                            current_prices[decision["ticker"]]
                        )
                        
                        if success:
                            # Record trade in database
                            self._record_trade(db, agent, decision, current_prices)
                    
                    # Record performance snapshot
                    self._record_performance(db, agent, current_prices, day)
                    
                    print(f"{agent.name}: {decision['action']} {decision.get('quantity', 0)} {decision.get('ticker', '')} - {decision['reasoning'][:50]}...")
                    
                except Exception as e:
                    print(f"Error with {agent.name}: {e}")
            
            # Update database
            db.commit()
    
    def _get_day_data(self, day: int) -> Dict:
        """Get market data for a specific day."""
        # This would fetch from your historical data
        # For now, simplified version:
        return {
            "day": day,
            "prices": self.market_data["prices"][day],
            "volume": self.market_data["volume"][day],
            "indicators": self.market_data["indicators"][day]
        }
    
    def _get_sentiment_data(self, day: int) -> Dict:
        """Get sentiment data for a specific day."""
        return self.sentiment_data.get(day, {})
    
    def _record_trade(self, db: Session, agent: BaseAgent, decision: Dict, prices: Dict):
        """Record a trade in the database."""
        # Get or create agent in DB
        agent_db = db.query(AgentModel).filter(AgentModel.name == agent.name).first()
        
        trade = Trade(
            agent_id=agent_db.id,
            action=decision["action"],
            ticker=decision["ticker"],
            quantity=decision["quantity"],
            price=prices[decision["ticker"]],
            reasoning=decision["reasoning"]
        )
        db.add(trade)
        
        # Update agent stats
        agent_db.total_trades += 1
    
    def _record_performance(self, db: Session, agent: BaseAgent, prices: Dict, day: int):
        """Record performance snapshot."""
        agent_db = db.query(AgentModel).filter(AgentModel.name == agent.name).first()
        
        portfolio_value = agent.get_portfolio_value(prices)
        
        snapshot = PerformanceSnapshot(
            agent_id=agent_db.id,
            portfolio_value=portfolio_value,
            cash=agent.cash,
            positions=json.dumps(agent.positions)
        )
        db.add(snapshot)
        
        # Update agent current values
        agent_db.current_capital = agent.cash
        agent_db.portfolio_value = portfolio_value
        agent_db.total_return = ((portfolio_value - agent_db.initial_capital) / agent_db.initial_capital) * 100
```

---

## Step 5: Market Data Module

Create `trading/market_data.py`:
```python
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict

class MarketDataManager:
    def __init__(self, tickers: List[str]):
        self.tickers = tickers
        
    def download_historical_data(self, start_date: str, end_date: str) -> Dict:
        """Download historical market data."""
        data = {}
        
        for ticker in self.tickers:
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(start=start_date, end=end_date)
                
                data[ticker] = {
                    "prices": hist["Close"].tolist(),
                    "volume": hist["Volume"].tolist(),
                    "dates": hist.index.strftime("%Y-%m-%d").tolist()
                }
                
                # Calculate technical indicators
                data[ticker]["rsi"] = self._calculate_rsi(hist["Close"]).tolist()
                data[ticker]["sma_20"] = hist["Close"].rolling(window=20).mean().tolist()
                
            except Exception as e:
                print(f"Error downloading {ticker}: {e}")
        
        return data
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI indicator."""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def format_for_agents(self, data: Dict, day_index: int) -> Dict:
        """Format data for agent consumption."""
        formatted = {
            "prices": {},
            "volume": {},
            "indicators": {}
        }
        
        for ticker in self.tickers:
            if day_index < len(data[ticker]["prices"]):
                formatted["prices"][ticker] = data[ticker]["prices"][day_index]
                formatted["volume"][ticker] = data[ticker]["volume"][day_index]
                formatted["indicators"][ticker] = {
                    "rsi": data[ticker]["rsi"][day_index] if day_index < len(data[ticker]["rsi"]) else None,
                    "sma_20": data[ticker]["sma_20"][day_index] if day_index < len(data[ticker]["sma_20"]) else None
                }
        
        return formatted
```

---

## Step 6: API Endpoints

Create `routers/agents.py`:
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import Agent, PerformanceSnapshot, Trade
from typing import List
import json

router = APIRouter(prefix="/agents", tags=["agents"])

@router.get("")
async def get_all_agents(db: Session = Depends(get_db)):
    """Get all agents with current performance."""
    agents = db.query(Agent).all()
    
    result = []
    for agent in agents:
        result.append({
            "name": agent.name,
            "agent_type": agent.agent_type,
            "currentReturn": round(agent.total_return, 2),
            "portfolioValue": round(agent.portfolio_value, 2),
            "rank": 0,  # Will be calculated
            "totalTrades": agent.total_trades,
            "winRate": round(agent.win_rate, 2) if agent.win_rate else 0,
            "sharpeRatio": round(agent.sharpe_ratio, 2) if agent.sharpe_ratio else 0,
            "maxDrawdown": round(agent.max_drawdown, 2) if agent.max_drawdown else 0
        })
    
    # Sort by return and assign ranks
    result.sort(key=lambda x: x["currentReturn"], reverse=True)
    for i, agent in enumerate(result):
        agent["rank"] = i + 1
    
    return {"agents": result}

@router.get("/{agent_name}")
async def get_agent_details(agent_name: str, db: Session = Depends(get_db)):
    """Get detailed information about a specific agent."""
    agent = db.query(Agent).filter(Agent.name == agent_name).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Get performance history
    snapshots = db.query(PerformanceSnapshot).filter(
        PerformanceSnapshot.agent_id == agent.id
    ).order_by(PerformanceSnapshot.timestamp).all()
    
    performance = {
        "returns": [s.portfolio_value for s in snapshots],
        "dates": [s.timestamp.strftime("%Y-%m-%d") for s in snapshots]
    }
    
    # Get current portfolio
    latest_snapshot = snapshots[-1] if snapshots else None
    portfolio = {
        "cash": round(agent.current_capital, 2),
        "positions": []
    }
    
    if latest_snapshot and latest_snapshot.positions:
        positions = json.loads(latest_snapshot.positions)
        for ticker, quantity in positions.items():
            portfolio["positions"].append({
                "ticker": ticker,
                "shares": quantity,
                # Would need current price to calculate value
            })
    
    # Get trades
    trades = db.query(Trade).filter(
        Trade.agent_id == agent.id
    ).order_by(Trade.timestamp.desc()).limit(50).all()
    
    trades_list = [{
        "id": str(trade.id),
        "timestamp": trade.timestamp.isoformat(),
        "action": trade.action,
        "ticker": trade.ticker,
        "quantity": trade.quantity,
        "price": trade.price,
        "reasoning": trade.reasoning
    } for trade in trades]
    
    return {
        "name": agent.name,
        "performance": performance,
        "portfolio": portfolio,
        "trades": trades_list,
        "metrics": {
            "totalReturn": round(agent.total_return, 2),
            "sharpeRatio": round(agent.sharpe_ratio, 2) if agent.sharpe_ratio else 0,
            "maxDrawdown": round(agent.max_drawdown, 2) if agent.max_drawdown else 0,
            "winRate": round(agent.win_rate, 2) if agent.win_rate else 0
        }
    }
```

Create `main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.connection import init_db
from routers import agents
import uvicorn

app = FastAPI(title="LLM Trading Arena API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
async def startup():
    init_db()

# Include routers
app.include_router(agents.router)

@app.get("/")
async def root():
    return {"message": "LLM Trading Arena API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

---

## Step 7: Data Preparation Script

Create `scripts/download_data.py`:
```python
import sys
sys.path.append('..')

from trading.market_data import MarketDataManager
from config import get_settings
import json

def main():
    settings = get_settings()
    
    manager = MarketDataManager(settings.available_tickers)
    
    print("Downloading historical data...")
    data = manager.download_historical_data(
        start_date="2024-04-01",
        end_date="2024-10-24"
    )
    
    # Save to file
    with open("../data/historical_prices.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Downloaded data for {len(data)} tickers")
    print(f"Date range: {data[settings.available_tickers[0]]['dates'][0]} to {data[settings.available_tickers[0]]['dates'][-1]}")

if __name__ == "__main__":
    main()
```

---

## Step 8: Run Simulation Script

Create `scripts/run_simulation.py`:
```python
import sys
sys.path.append('..')

import asyncio
from trading.simulator import TradingSimulator
from agents.gpt_agent import GPTAgent
from agents.claude_agent import ClaudeAgent
from agents.gemini_agent import GeminiAgent
from database.connection import SessionLocal, init_db
from database.models import Agent as AgentModel
from config import get_settings
import json

async def main():
    settings = get_settings()
    
    # Initialize database
    init_db()
    db = SessionLocal()
    
    # Load historical data
    with open("../data/historical_prices.json", "r") as f:
        historical_data = json.load(f)
    
    # Initialize agents
    agents = [
        GPTAgent("GPT-4", settings.initial_capital),
        ClaudeAgent("Claude", settings.initial_capital),
        GeminiAgent("Gemini", settings.initial_capital),
        # Add more agents as needed
    ]
    
    # Create agent entries in database
    for agent in agents:
        agent_db = AgentModel(
            name=agent.name,
            agent_type=agent.name,
            initial_capital=settings.initial_capital,
            current_capital=settings.initial_capital,
            portfolio_value=settings.initial_capital,
            total_return=0.0
        )
        db.merge(agent_db)
    db.commit()
    
    # Create simulator
    simulator = TradingSimulator(
        agents=agents,
        market_data=historical_data,
        sentiment_data={}  # Add sentiment data if available
    )
    
    # Run simulation
    print("Starting simulation...")
    await simulator.run_simulation(db, num_days=30)
    
    print("\nSimulation complete!")
    
    # Print final results
    print("\n=== Final Results ===")
    for agent in agents:
        final_value = agent.get_portfolio_value(
            {ticker: historical_data[ticker]["prices"][-1] for ticker in settings.available_tickers}
        )
        returns = ((final_value - settings.initial_capital) / settings.initial_capital) * 100
        print(f"{agent.name}: ${final_value:.2f} ({returns:+.2f}%)")
    
    db.close()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Step 9: Running the Backend

### Setup:
```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env and add your API keys

# 4. Download historical data
python scripts/download_data.py

# 5. Run simulation (this populates the database)
python scripts/run_simulation.py

# 6. Start API server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### API will be available at:
- Swagger docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Quick Start for Hackathon

If you're short on time, here's a streamlined approach:

1. **Day 1 Morning**: Set up project structure, install dependencies
2. **Day 1 Afternoon**: Implement 2-3 agents (GPT, Claude, Gemini)
3. **Day 1 Evening**: Download historical data, run basic simulation
4. **Day 2 Morning**: Build core API endpoints (agents, trades)
5. **Day 2 Afternoon**: Test API with Postman, fix bugs
6. **Day 2 Evening**: Add betting endpoints
7. **Day 3**: Integration with frontend, polish, demo prep

---

## Testing the API

Use these curl commands to test:

```bash
# Get all agents
curl http://localhost:8000/agents

# Get agent details
curl http://localhost:8000/agents/GPT-4
```

---

## Deployment

### Option 1: Railway (Easiest)
1. Push code to GitHub
2. Connect Railway to your repo
3. Add environment variables in Railway dashboard
4. Deploy

### Option 2: Heroku
```bash
# Add Procfile
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
heroku create llm-trading-arena
git push heroku main
```

### Option 3: DigitalOcean App Platform
- Similar to Railway, connect GitHub repo
- Configure build/run commands
- Add environment variables

---

## Cost Optimization

1. **Cache LLM responses** during development
2. **Use cheaper models** (GPT-3.5 instead of GPT-4)
3. **Run simulation once**, save results to DB
4. **Limit API calls** during testing
5. **Use mock agents** for frontend development

---

Good luck with your hackathon! This should give you a solid foundation to build an impressive demo. 🚀
