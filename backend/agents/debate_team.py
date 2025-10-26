import json
from typing import Dict, Any, List
from services.llm_client import llm_client

class DebateTeam:
    """
    Debate Team Agent - THE KEY INNOVATION
    Conducts bull vs bear debates before making trading decisions
    Uses Claude Sonnet 4 for superior reasoning
    """

    def __init__(self):
        self.name = "Debate Team"
        self.model = "claude-sonnet-4-20250514"

    async def conduct_debate(
        self,
        ticker: str,
        date: str,
        technical_analysis: Dict[str, Any],
        sentiment_analysis: Dict[str, Any],
        rounds: int = 2
    ) -> Dict[str, Any]:
        """
        Conduct a structured debate between bull and bear perspectives

        Args:
            ticker: Stock ticker symbol
            date: Analysis date
            technical_analysis: Results from TechnicalAnalyst
            sentiment_analysis: Results from SentimentAnalyst
            rounds: Number of debate rounds

        Returns:
            Dict containing debate transcript and final recommendation
        """
        debate_log = []

        # Round 1: Initial arguments
        bull_arg_1 = await self._generate_bull_argument(
            ticker, date, technical_analysis, sentiment_analysis, []
        )
        debate_log.append({"round": 1, "speaker": "Bull", "argument": bull_arg_1})

        bear_arg_1 = await self._generate_bear_argument(
            ticker, date, technical_analysis, sentiment_analysis, [bull_arg_1]
        )
        debate_log.append({"round": 1, "speaker": "Bear", "argument": bear_arg_1})

        # Round 2: Rebuttals (if requested)
        if rounds >= 2:
            bull_arg_2 = await self._generate_bull_argument(
                ticker, date, technical_analysis, sentiment_analysis, [bull_arg_1, bear_arg_1]
            )
            debate_log.append({"round": 2, "speaker": "Bull", "argument": bull_arg_2})

            bear_arg_2 = await self._generate_bear_argument(
                ticker, date, technical_analysis, sentiment_analysis, [bull_arg_1, bear_arg_1, bull_arg_2]
            )
            debate_log.append({"round": 2, "speaker": "Bear", "argument": bear_arg_2})

        # Synthesize final recommendation
        final_decision = await self._synthesize_decision(ticker, date, debate_log)

        return {
            "agent": self.name,
            "ticker": ticker,
            "date": date,
            "debate_log": debate_log,
            "final_decision": final_decision,
            "rounds_conducted": rounds
        }

    async def _generate_bull_argument(
        self,
        ticker: str,
        date: str,
        technical: Dict,
        sentiment: Dict,
        previous_arguments: List[str]
    ) -> str:
        """Generate bullish argument"""
        context = self._format_context(technical, sentiment)
        previous = "\n".join([f"- {arg}" for arg in previous_arguments[-2:]])

        prompt = f"""You are the BULL advocate in a trading debate for {ticker} on {date}.

MARKET DATA:
{context}

PREVIOUS ARGUMENTS:
{previous if previous else "This is your opening argument."}

Provide a BULLISH argument for why to BUY {ticker}. Focus on:
1. Positive technical signals
2. Favorable sentiment
3. Growth opportunities
4. Counter-arguments to any bearish points raised

Be specific, data-driven, and persuasive. Respond in JSON format with:
- argument: Your main bullish case (string)
- key_points: List of 3-5 supporting points
- conviction: Your confidence level (0-1)
"""

        # Call LLM (currently mocked)
        # TO MAKE FUNCTIONAL: Ensure llm_client.call_claude makes real API calls
        response = await llm_client.call_claude(prompt, model=self.model, temperature=0.8)

        try:
            result = json.loads(response)
            return result.get('argument', 'Bull argument generated')
        except:
            return "Strong bullish signals based on technical and sentiment analysis"

    async def _generate_bear_argument(
        self,
        ticker: str,
        date: str,
        technical: Dict,
        sentiment: Dict,
        previous_arguments: List[str]
    ) -> str:
        """Generate bearish argument"""
        context = self._format_context(technical, sentiment)
        previous = "\n".join([f"- {arg}" for arg in previous_arguments[-2:]])

        prompt = f"""You are the BEAR advocate in a trading debate for {ticker} on {date}.

MARKET DATA:
{context}

PREVIOUS ARGUMENTS:
{previous if previous else "This is your opening argument."}

Provide a BEARISH argument for why to be cautious about {ticker}. Focus on:
1. Concerning technical signals
2. Negative sentiment indicators
3. Risk factors
4. Counter-arguments to bullish points raised

Be specific, data-driven, and persuasive. Respond in JSON format with:
- argument: Your main bearish case (string)
- key_points: List of 3-5 supporting points
- conviction: Your confidence level (0-1)
"""

        # Call LLM (currently mocked)
        # TO MAKE FUNCTIONAL: Ensure llm_client.call_claude makes real API calls
        response = await llm_client.call_claude(prompt, model=self.model, temperature=0.8)

        try:
            result = json.loads(response)
            return result.get('argument', 'Bear argument generated')
        except:
            return "Significant risk factors warrant caution on this position"

    async def _synthesize_decision(self, ticker: str, date: str, debate_log: List[Dict]) -> Dict[str, Any]:
        """Synthesize final decision from debate"""
        debate_summary = "\n".join([
            f"Round {d['round']} - {d['speaker']}: {d['argument']}"
            for d in debate_log
        ])

        prompt = f"""You are a neutral judge reviewing a trading debate for {ticker} on {date}.

DEBATE TRANSCRIPT:
{debate_summary}

Based on the arguments presented, provide a final decision:
1. Which side (Bull or Bear) made the stronger case?
2. What is the recommended action? (BUY, SELL, or HOLD)
3. How confident are you in this recommendation? (0-1)
4. What are the key reasons?

Respond in JSON format with keys: winning_side, action, confidence, key_reasons (list)
"""

        # Call LLM (currently mocked)
        # TO MAKE FUNCTIONAL: Ensure llm_client.call_claude makes real API calls
        response = await llm_client.call_claude(prompt, model=self.model, temperature=0.5)

        try:
            decision = json.loads(response)
        except:
            decision = {
                "winning_side": "Bull",
                "action": "HOLD",
                "confidence": 0.6,
                "key_reasons": ["Balanced arguments on both sides"]
            }

        return decision

    def _format_context(self, technical: Dict, sentiment: Dict) -> str:
        """Format analysis context for prompts"""
        tech_summary = f"""
Technical Analysis:
- Trend: {technical.get('trend', 'N/A')}
- Recommendation: {technical.get('recommendation', 'N/A')}
- RSI: {technical.get('indicators', {}).get('rsi', 'N/A')}
"""

        sent_summary = f"""
Sentiment Analysis:
- Overall Sentiment: {sentiment.get('sentiment_score', 'N/A')}
- Trend: {sentiment.get('trend', 'N/A')}
- Impact: {sentiment.get('impact', 'N/A')}
"""

        return tech_summary + sent_summary

    def get_status(self) -> Dict[str, str]:
        """Get agent status"""
        return {
            "name": self.name,
            "model": self.model,
            "status": "active"
        }
