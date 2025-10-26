import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import yfinance as yf
from pathlib import Path

class DataLoader:
    """Load and process market and sentiment data"""

    def __init__(self, data_path: str = "backend/data"):
        self.data_path = Path(data_path)

    def load_sentiment_data(self, ticker: str, start_date: str, end_date: str) -> Dict:
        """Load sentiment data from Reddit and Twitter CSV files"""
        reddit_df = pd.read_csv(self.data_path / "reddit_sentiment.csv")
        twitter_df = pd.read_csv(self.data_path / "twitter_sentiment.csv")

        # Parse dates
        reddit_df['date'] = pd.to_datetime(reddit_df['date'])
        twitter_df['date'] = pd.to_datetime(twitter_df['date'])

        # Filter by ticker and date range
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)

        reddit_data = reddit_df[
            (reddit_df['ticker'] == ticker) &
            (reddit_df['date'] >= start) &
            (reddit_df['date'] <= end)
        ]

        twitter_data = twitter_df[
            (twitter_df['ticker'] == ticker) &
            (twitter_df['date'] >= start) &
            (twitter_df['date'] <= end)
        ]

        return {
            "reddit": reddit_data.to_dict('records') if not reddit_data.empty else [],
            "twitter": twitter_data.to_dict('records') if not twitter_data.empty else [],
            "reddit_avg_sentiment": float(reddit_data['sentiment'].mean()) if not reddit_data.empty else 0.0,
            "twitter_avg_sentiment": float(twitter_data['sentiment'].mean()) if not twitter_data.empty else 0.0,
            "total_posts": len(reddit_data) + len(twitter_data)
        }

    def load_market_data(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Load market data from Yahoo Finance

        PRODUCTION CODE:
        ```python
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date)
        return df
        ```
        """
        # MOCK DATA - Replace with real yfinance call
        print(f"[MOCK] Loading market data for {ticker} from {start_date} to {end_date}")

        # Generate mock price data
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        mock_data = {
            'Open': [100 + i * 0.5 for i in range(len(date_range))],
            'High': [102 + i * 0.5 for i in range(len(date_range))],
            'Low': [99 + i * 0.5 for i in range(len(date_range))],
            'Close': [101 + i * 0.5 for i in range(len(date_range))],
            'Volume': [1000000 + i * 10000 for i in range(len(date_range))],
        }

        df = pd.DataFrame(mock_data, index=date_range)
        return df

    def get_latest_price(self, ticker: str, date: str) -> float:
        """Get the closing price for a specific date"""
        df = self.load_market_data(ticker, date, date)
        if not df.empty:
            return float(df['Close'].iloc[-1])
        return 100.0  # fallback

    def calculate_technical_indicators(self, df: pd.DataFrame) -> Dict:
        """Calculate technical indicators from price data"""
        if df.empty or len(df) < 14:
            return {
                "sma_20": 0,
                "sma_50": 0,
                "rsi": 50,
                "macd": 0,
                "signal": 0
            }

        # Simple Moving Averages
        sma_20 = df['Close'].rolling(window=min(20, len(df))).mean().iloc[-1]
        sma_50 = df['Close'].rolling(window=min(50, len(df))).mean().iloc[-1]

        # RSI (simplified)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        return {
            "sma_20": float(sma_20) if not pd.isna(sma_20) else 0,
            "sma_50": float(sma_50) if not pd.isna(sma_50) else 0,
            "rsi": float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else 50,
            "current_price": float(df['Close'].iloc[-1]),
            "volume": int(df['Volume'].iloc[-1])
        }

# Global instance
data_loader = DataLoader()
