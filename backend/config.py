from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    # API Keys
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    google_ai_api_key: str = ""

    # Trading Config
    initial_capital: float = 10000.0
    max_position_size: float = 0.3  # Max 30% per trade

    # Simulation Config
    start_date: str = "2020-07-01"
    end_date: str = "2020-09-30"
    tickers: str = "AAPL,MSFT"

    # Model Selection
    analyst_model: str = "claude-haiku"
    debate_model: str = "claude-sonnet-4"
    trader_model: str = "claude-sonnet-4"

    class Config:
        env_file = ".env"

    def get_tickers_list(self) -> List[str]:
        return [t.strip() for t in self.tickers.split(",")]

@lru_cache()
def get_settings():
    return Settings()
