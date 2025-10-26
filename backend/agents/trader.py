import json
from typing import Dict, Any, Optional
from services.llm_client import llm_client

class Trader:
    """
    Trader Agent
    Makes final trading decisions based on all available analysis
    Can use different LLM models (Claude, Gemini) for comparison
    """

    def __init__(self, model_type: str = "claude", name: Optional[str] = None):
        """
        Initialize trader with specific LLM model

        Args:
            model_type: One of "claude", "gemini"
            name: Custom name for the trader (defaults to model type)
        """
        self.model_type = model_type
        self.name = name or f"{model_type.upper()} Trader"

        # Portfolio tracking
        self.cash = 10000.0
        self.holdings: Dict[str, int] = {}  # {ticker: quantity}
        self.trade_history: List[Dict] = []

    async def make_decision(
        self,
        ticker: str,
        date: str,
        current_price: float,
        technical_analysis: Dict[str, Any],
        sentiment_analysis: Dict[str, Any],
        debate_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Make a trading decision based on all available analysis

        Args:
            ticker: Stock ticker symbol
            date: Trading date
            current_price: Current stock price
            technical_analysis: Results from TechnicalAnalyst
            sentiment_analysis: Results from SentimentAnalyst
            debate_result: Results from DebateTeam

        Returns:
            Dict containing trading decision
        """
        # Format all analysis for the LLM
        context = self._format_trading_context(
            ticker, date, current_price,
            technical_analysis, sentiment_analysis, debate_result
        )

        # Add portfolio context
        current_position = self.holdings.get(ticker, 0)
        portfolio_value = self.get_portfolio_value({ticker: current_price})

        prompt = f"""You are an expert trader making a decision for {ticker} on {date}.

CURRENT PORTFOLIO:
- Cash: ${self.cash:,.2f}
- Current Position in {ticker}: {current_position} shares
- Portfolio Value: ${portfolio_value:,.2f}

MARKET ANALYSIS:
{context}

Based on this comprehensive analysis, make a trading decision:
1. Action: BUY, SELL, or HOLD
2. Quantity: Number of shares (0 if HOLD)
3. Reasoning: Brief explanation of your decision
4. Confidence: How confident are you? (0-1)

Consider:
- The debate outcome and strength of arguments
- Technical and sentiment indicators
- Your current position and available cash
- Risk management (max 30% of portfolio per position)

Respond in JSON format with keys: action, quantity, reasoning, confidence
"""

        # Call appropriate LLM based on model_type
        # TO MAKE FUNCTIONAL: Ensure these make real API calls (see llm_client.py)
        if self.model_type == "claude":
            response = await llm_client.call_claude(prompt, temperature=0.7)
        elif self.model_type == "gemini":
            response = await llm_client.call_gemini(prompt, temperature=0.7)
        else:
            response = json.dumps({"action": "HOLD", "quantity": 0, "reasoning": "Unknown model", "confidence": 0.5})

        try:
            decision = json.loads(response)
        except:
            decision = {
                "action": "HOLD",
                "quantity": 0,
                "reasoning": "Unable to parse LLM response",
                "confidence": 0.5
            }

        # Validate and execute decision
        executed_decision = self._execute_trade(
            ticker, date, current_price,
            decision['action'],
            decision['quantity']
        )

        return {
            "agent": self.name,
            "model": self.model_type,
            "date": date,
            "ticker": ticker,
            "price": current_price,
            **executed_decision,
            "reasoning": decision['reasoning'],
            "confidence": decision['confidence']
        }

    def _execute_trade(
        self,
        ticker: str,
        date: str,
        price: float,
        action: str,
        quantity: int
    ) -> Dict[str, Any]:
        """Execute a trade and update portfolio"""
        actual_action = action
        actual_quantity = 0
        cost = 0.0

        if action == "BUY" and quantity > 0:
            cost = price * quantity
            if cost <= self.cash:
                self.cash -= cost
                self.holdings[ticker] = self.holdings.get(ticker, 0) + quantity
                actual_quantity = quantity
            else:
                # Buy what we can afford
                affordable = int(self.cash / price)
                if affordable > 0:
                    cost = price * affordable
                    self.cash -= cost
                    self.holdings[ticker] = self.holdings.get(ticker, 0) + affordable
                    actual_quantity = affordable
                else:
                    actual_action = "HOLD"

        elif action == "SELL" and quantity > 0:
            current_position = self.holdings.get(ticker, 0)
            sell_quantity = min(quantity, current_position)
            if sell_quantity > 0:
                proceeds = price * sell_quantity
                self.cash += proceeds
                self.holdings[ticker] -= sell_quantity
                actual_quantity = sell_quantity
                cost = -proceeds  # negative cost = gain
            else:
                actual_action = "HOLD"

        # Log trade
        trade = {
            "date": date,
            "ticker": ticker,
            "action": actual_action,
            "quantity": actual_quantity,
            "price": price,
            "cost": cost,
            "cash_after": self.cash
        }
        self.trade_history.append(trade)

        return {
            "action": actual_action,
            "quantity": actual_quantity,
            "cost": cost,
            "cash_remaining": self.cash
        }

    def _format_trading_context(
        self,
        ticker: str,
        date: str,
        price: float,
        technical: Dict,
        sentiment: Dict,
        debate: Dict
    ) -> str:
        """Format all analysis into readable context"""
        return f"""
Current Price: ${price:.2f}

Technical Analysis:
- Trend: {technical.get('trend', 'N/A')}
- Recommendation: {technical.get('recommendation', 'N/A')}
- Confidence: {technical.get('confidence', 'N/A')}

Sentiment Analysis:
- Score: {sentiment.get('sentiment_score', 'N/A')}
- Trend: {sentiment.get('trend', 'N/A')}
- Impact: {sentiment.get('impact', 'N/A')}

Debate Outcome:
- Winning Side: {debate.get('final_decision', {}).get('winning_side', 'N/A')}
- Recommended Action: {debate.get('final_decision', {}).get('action', 'N/A')}
- Debate Confidence: {debate.get('final_decision', {}).get('confidence', 'N/A')}
- Key Reasons: {', '.join(debate.get('final_decision', {}).get('key_reasons', []))}
"""

    def get_portfolio_value(self, current_prices: Dict[str, float]) -> float:
        """Calculate total portfolio value"""
        holdings_value = sum(
            qty * current_prices.get(ticker, 0)
            for ticker, qty in self.holdings.items()
        )
        return self.cash + holdings_value

    def get_portfolio_summary(self, current_prices: Dict[str, float]) -> Dict[str, Any]:
        """Get current portfolio summary"""
        return {
            "agent": self.name,
            "cash": self.cash,
            "holdings": dict(self.holdings),
            "portfolio_value": self.get_portfolio_value(current_prices),
            "total_trades": len(self.trade_history),
            "trade_history": self.trade_history
        }

    def get_status(self) -> Dict[str, str]:
        """Get agent status"""
        return {
            "name": self.name,
            "model": self.model_type,
            "status": "active",
            "cash": f"${self.cash:,.2f}",
            "positions": len(self.holdings)
        }
