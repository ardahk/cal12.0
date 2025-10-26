from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from agents import TechnicalAnalyst, SentimentAnalyst, DebateTeam, Trader

router = APIRouter()

# Initialize agents
technical_analyst = TechnicalAnalyst()
sentiment_analyst = SentimentAnalyst()
debate_team = DebateTeam()

# Initialize traders with different models (Claude and Gemini only)
claude_trader = Trader(model_type="claude", name="Claude Trader")
gemini_trader = Trader(model_type="gemini", name="Gemini Trader")

@router.get("/status")
async def get_agents_status():
    """
    Get status of all agents

    **API Integration Point**: Call this from frontend to display agent cards
    """
    return {
        "analysts": [
            technical_analyst.get_status(),
            sentiment_analyst.get_status()
        ],
        "debate_team": debate_team.get_status(),
        "traders": [
            claude_trader.get_status(),
            gemini_trader.get_status()
        ]
    }

@router.get("/technical/{ticker}")
async def get_technical_analysis(ticker: str, date: str = "2020-07-15"):
    """
    Get technical analysis for a ticker

    **API Integration Point**: Call from frontend to show technical indicators

    Args:
        ticker: Stock ticker (e.g., AAPL, MSFT)
        date: Analysis date (YYYY-MM-DD)
    """
    try:
        analysis = await technical_analyst.analyze(ticker, date)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sentiment/{ticker}")
async def get_sentiment_analysis(ticker: str, date: str = "2020-07-15"):
    """
    Get sentiment analysis for a ticker

    **API Integration Point**: Call from frontend to show sentiment metrics

    Args:
        ticker: Stock ticker (e.g., AAPL, MSFT)
        date: Analysis date (YYYY-MM-DD)
    """
    try:
        analysis = await sentiment_analyst.analyze(ticker, date)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/debate")
async def conduct_debate(
    ticker: str,
    date: str = "2020-07-15",
    rounds: int = 2
):
    """
    Conduct a trading debate for a ticker

    **API Integration Point**: Call from frontend to show debate viewer (KEY FEATURE!)

    Args:
        ticker: Stock ticker (e.g., AAPL, MSFT)
        date: Analysis date (YYYY-MM-DD)
        rounds: Number of debate rounds (1-3)
    """
    try:
        # Get analysis first
        technical = await technical_analyst.analyze(ticker, date)
        sentiment = await sentiment_analyst.analyze(ticker, date)

        # Conduct debate
        debate = await debate_team.conduct_debate(
            ticker, date, technical, sentiment, rounds
        )

        return {
            "technical_analysis": technical,
            "sentiment_analysis": sentiment,
            "debate": debate
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/portfolio/{trader_name}")
async def get_portfolio(trader_name: str):
    """
    Get portfolio summary for a specific trader

    **API Integration Point**: Call from frontend to show trader portfolios

    Args:
        trader_name: One of "claude", "gemini"
    """
    trader_map = {
        "claude": claude_trader,
        "gemini": gemini_trader
    }

    trader = trader_map.get(trader_name.lower())
    if not trader:
        raise HTTPException(status_code=404, detail="Trader not found")

    # Get current prices (mock for now)
    current_prices = {"AAPL": 105.0, "MSFT": 110.0, "NVDA": 120.0}

    return trader.get_portfolio_summary(current_prices)
