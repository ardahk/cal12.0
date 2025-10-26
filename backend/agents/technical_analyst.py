import json
from typing import Dict, Any
from services.llm_client import llm_client
from services.data_loader import data_loader

class TechnicalAnalyst:
    """
    Technical Analyst Agent
    Analyzes price data and technical indicators
    Uses Claude Haiku for cost efficiency
    """

    def __init__(self):
        self.name = "Technical Analyst"
        self.model = "claude-haiku-20240307"

    async def analyze(self, ticker: str, date: str, lookback_days: int = 30) -> Dict[str, Any]:
        """
        Perform technical analysis for a given ticker and date

        Args:
            ticker: Stock ticker symbol
            date: Analysis date
            lookback_days: Number of days to look back for analysis

        Returns:
            Dict containing technical analysis results
        """
        from datetime import datetime, timedelta

        # Load market data
        end_date = datetime.strptime(date, "%Y-%m-%d")
        start_date = end_date - timedelta(days=lookback_days)

        market_data = data_loader.load_market_data(
            ticker,
            start_date.strftime("%Y-%m-%d"),
            date
        )

        # Calculate technical indicators
        indicators = data_loader.calculate_technical_indicators(market_data)

        # Create prompt for LLM
        prompt = f"""You are a technical analyst. Analyze the following stock data and provide insights.

Ticker: {ticker}
Date: {date}

Technical Indicators:
- Current Price: ${indicators['current_price']:.2f}
- 20-day SMA: ${indicators['sma_20']:.2f}
- 50-day SMA: ${indicators['sma_50']:.2f}
- RSI: {indicators['rsi']:.2f}
- Volume: {indicators['volume']:,}

Based on this technical analysis, provide:
1. Overall trend (BULLISH, BEARISH, or NEUTRAL)
2. Key technical signals
3. Price momentum assessment
4. Recommendation (BUY, SELL, or HOLD)

Respond in JSON format with keys: trend, signals, momentum, recommendation, confidence (0-1)
"""

        # Call LLM (currently mocked)
        # TO MAKE FUNCTIONAL: Ensure llm_client.call_claude makes real API calls
        response = await llm_client.call_claude(prompt, model=self.model, temperature=0.3)

        try:
            analysis = json.loads(response)
        except json.JSONDecodeError:
            # Fallback if response is not JSON
            analysis = {
                "trend": "NEUTRAL",
                "signals": ["Unable to parse LLM response"],
                "momentum": "NEUTRAL",
                "recommendation": "HOLD",
                "confidence": 0.5
            }

        # Add raw indicators to response
        analysis['indicators'] = indicators
        analysis['agent'] = self.name

        return analysis

    def get_status(self) -> Dict[str, str]:
        """Get agent status"""
        return {
            "name": self.name,
            "model": self.model,
            "status": "active"
        }
