import json
from typing import Dict, Any
from services.llm_client import llm_client
from services.data_loader import data_loader

class SentimentAnalyst:
    """
    Sentiment Analyst Agent
    Analyzes social media sentiment from Reddit and Twitter
    Uses Claude Haiku for cost efficiency
    """

    def __init__(self):
        self.name = "Sentiment Analyst"
        self.model = "claude-haiku-20240307"

    async def analyze(self, ticker: str, date: str, lookback_days: int = 7) -> Dict[str, Any]:
        """
        Perform sentiment analysis for a given ticker and date

        Args:
            ticker: Stock ticker symbol
            date: Analysis date
            lookback_days: Number of days to look back for sentiment

        Returns:
            Dict containing sentiment analysis results
        """
        from datetime import datetime, timedelta

        # Load sentiment data
        end_date = datetime.strptime(date, "%Y-%m-%d")
        start_date = end_date - timedelta(days=lookback_days)

        sentiment_data = data_loader.load_sentiment_data(
            ticker,
            start_date.strftime("%Y-%m-%d"),
            date
        )

        # Create prompt for LLM
        prompt = f"""You are a sentiment analyst. Analyze social media sentiment for the following stock.

Ticker: {ticker}
Date: {date}

Sentiment Data (last {lookback_days} days):
- Reddit Average Sentiment: {sentiment_data['reddit_avg_sentiment']:.3f}
- Twitter Average Sentiment: {sentiment_data['twitter_avg_sentiment']:.3f}
- Total Posts: {sentiment_data['total_posts']}

Sample Reddit Posts:
{self._format_posts(sentiment_data['reddit'][:5])}

Sample Tweets:
{self._format_posts(sentiment_data['twitter'][:5])}

Based on this sentiment analysis, provide:
1. Overall sentiment score (-1 to 1)
2. Key themes and topics
3. Sentiment trend (IMPROVING, DECLINING, STABLE)
4. Recommendation impact (POSITIVE, NEGATIVE, NEUTRAL)

Respond in JSON format with keys: sentiment_score, themes, trend, impact, confidence (0-1)
"""

        # Call LLM (currently mocked)
        # TO MAKE FUNCTIONAL: Ensure llm_client.call_claude makes real API calls
        response = await llm_client.call_claude(prompt, model=self.model, temperature=0.3)

        try:
            analysis = json.loads(response)
        except json.JSONDecodeError:
            analysis = {
                "sentiment_score": 0.0,
                "themes": ["Unable to parse LLM response"],
                "trend": "STABLE",
                "impact": "NEUTRAL",
                "confidence": 0.5
            }

        # Add raw sentiment data to response
        analysis['raw_data'] = {
            'reddit_sentiment': sentiment_data['reddit_avg_sentiment'],
            'twitter_sentiment': sentiment_data['twitter_avg_sentiment'],
            'total_posts': sentiment_data['total_posts']
        }
        analysis['agent'] = self.name

        return analysis

    def _format_posts(self, posts: list) -> str:
        """Format posts for prompt"""
        if not posts:
            return "No posts available"

        formatted = []
        for i, post in enumerate(posts[:5], 1):
            if 'title' in post:  # Reddit
                formatted.append(f"{i}. {post['title']} (sentiment: {post['sentiment']:.2f})")
            elif 'text' in post:  # Twitter
                text = post['text'][:100] + "..." if len(post['text']) > 100 else post['text']
                formatted.append(f"{i}. {text} (sentiment: {post['sentiment']:.2f})")

        return "\n".join(formatted)

    def get_status(self) -> Dict[str, str]:
        """Get agent status"""
        return {
            "name": self.name,
            "model": self.model,
            "status": "active"
        }
