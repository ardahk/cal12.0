import json
from typing import Dict, Any, Optional
from config import get_settings

settings = get_settings()

class LLMClient:
    """
    LLM Client for calling Claude and Gemini AI models

    MOCK MODE (default): Returns mock responses for demo
    PRODUCTION MODE: Uncomment initialization code and API calls below
    """

    def __init__(self):
        # PRODUCTION MODE: Uncomment these lines when you have API keys
        # import anthropic
        # from google import generativeai as genai
        #
        # self.anthropic_client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        # genai.configure(api_key=settings.google_ai_api_key)
        # self.gemini_model = genai.GenerativeModel('gemini-pro')
        pass

    async def call_claude(self, prompt: str, model: str = "claude-sonnet-4-20250514", temperature: float = 0.7) -> str:
        """
        Call Claude API

        PRODUCTION CODE (uncomment when API keys are set):
        ```python
        try:
            message = await self.anthropic_client.messages.create(
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
        """
        # MOCK RESPONSE - Replace with real API call
        print(f"[MOCK] Claude called with model: {model}")
        return self._mock_response("claude", prompt)


    async def call_gemini(self, prompt: str, temperature: float = 0.7) -> str:
        """
        Call Gemini API

        PRODUCTION CODE (uncomment when API keys are set):
        ```python
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = await model.generate_content_async(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=temperature,
                )
            )
            return response.text
        except Exception as e:
            print(f"Gemini API error: {e}")
            return json.dumps({"error": str(e)})
        ```
        """
        # MOCK RESPONSE - Replace with real API call
        print(f"[MOCK] Gemini called")
        return self._mock_response("gemini", prompt)

    def _mock_response(self, model: str, prompt: str) -> str:
        """Generate mock responses based on prompt type"""
        if "technical analysis" in prompt.lower():
            return json.dumps({
                "analysis": f"{model.upper()} Technical Analysis",
                "trend": "bullish",
                "indicators": {
                    "rsi": 65.3,
                    "macd": "positive",
                    "moving_averages": "golden cross"
                },
                "recommendation": "BUY",
                "confidence": 0.75
            })
        elif "sentiment" in prompt.lower():
            return json.dumps({
                "analysis": f"{model.upper()} Sentiment Analysis",
                "overall_sentiment": 0.42,
                "reddit_sentiment": 0.38,
                "twitter_sentiment": 0.46,
                "key_topics": ["earnings", "product launch", "market growth"],
                "recommendation": "POSITIVE"
            })
        elif "bull" in prompt.lower() or "bear" in prompt.lower():
            is_bull = "bull" in prompt.lower()
            return json.dumps({
                "role": "bull" if is_bull else "bear",
                "argument": f"Strong {'bullish' if is_bull else 'bearish'} signals based on technical and sentiment data",
                "key_points": [
                    f"{'Positive' if is_bull else 'Negative'} momentum indicators",
                    f"{'Favorable' if is_bull else 'Unfavorable'} market sentiment",
                    f"{'Strong' if is_bull else 'Weak'} fundamentals"
                ],
                "risk_factors": ["market volatility", "economic uncertainty"],
                "conviction": 0.8 if is_bull else 0.7
            })
        elif "trading decision" in prompt.lower():
            return json.dumps({
                "action": "BUY",
                "quantity": 10,
                "reasoning": f"{model.upper()}: Based on positive technical and sentiment analysis, bullish debate outcome",
                "confidence": 0.78,
                "risk_level": "MEDIUM"
            })
        else:
            return json.dumps({"response": f"Mock response from {model}"})

# Global client instance
llm_client = LLMClient()
