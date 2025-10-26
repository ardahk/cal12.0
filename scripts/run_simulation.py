"""
Standalone script to run a trading simulation
Can be run without the API server
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from agents import TechnicalAnalyst, SentimentAnalyst, DebateTeam, Trader
from services.data_loader import data_loader
from datetime import datetime, timedelta
import json

async def run_simulation(
    ticker: str = "AAPL",
    start_date: str = "2020-07-01",
    end_date: str = "2020-07-10",
    debug: bool = True
):
    """Run a complete trading simulation"""

    print(f"\n{'='*60}")
    print(f"LLM TRADING ARENA SIMULATION")
    print(f"{'='*60}")
    print(f"Ticker: {ticker}")
    print(f"Period: {start_date} to {end_date}")
    print(f"{'='*60}\n")

    # Initialize agents
    technical = TechnicalAnalyst()
    sentiment = SentimentAnalyst()
    debate = DebateTeam()

    # Initialize traders
    traders = [
        Trader(model_type="claude", name="Claude Trader"),
        Trader(model_type="gpt", name="GPT-4 Trader"),
        Trader(model_type="gemini", name="Gemini Trader")
    ]

    # Generate trading dates (skip weekends)
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    trading_dates = []

    current = start
    while current <= end:
        if current.weekday() < 5:  # Monday = 0, Friday = 4
            trading_dates.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)

    print(f"Trading {len(trading_dates)} days\n")

    # Run simulation
    for day_num, date in enumerate(trading_dates, 1):
        print(f"\n--- Day {day_num}: {date} ---")

        # Get current price
        current_price = data_loader.get_latest_price(ticker, date)
        print(f"Current Price: ${current_price:.2f}")

        # Run analysis
        tech_analysis = await technical.analyze(ticker, date)
        sent_analysis = await sentiment.analyze(ticker, date)

        if debug:
            print(f"  Technical: {tech_analysis.get('recommendation')} (confidence: {tech_analysis.get('confidence')})")
            print(f"  Sentiment: {sent_analysis.get('impact')} (score: {sent_analysis.get('sentiment_score')})")

        # Conduct debate
        debate_result = await debate.conduct_debate(
            ticker, date, tech_analysis, sent_analysis, rounds=2
        )

        if debug:
            print(f"  Debate Winner: {debate_result['final_decision']['winning_side']}")
            print(f"  Debate Recommendation: {debate_result['final_decision']['action']}")

        # Each trader makes decision
        for trader in traders:
            decision = await trader.make_decision(
                ticker, date, current_price,
                tech_analysis, sent_analysis, debate_result
            )

            if debug:
                print(f"  {trader.name}: {decision['action']} {decision['quantity']} shares")

    # Print final results
    print(f"\n{'='*60}")
    print(f"FINAL RESULTS")
    print(f"{'='*60}\n")

    final_price = data_loader.get_latest_price(ticker, trading_dates[-1])
    current_prices = {ticker: final_price}

    for trader in traders:
        portfolio = trader.get_portfolio_summary(current_prices)
        initial_value = 10000.0
        final_value = portfolio["portfolio_value"]
        returns = final_value - initial_value
        returns_pct = (returns / initial_value) * 100

        print(f"{trader.name}:")
        print(f"  Initial Value: ${initial_value:,.2f}")
        print(f"  Final Value: ${final_value:,.2f}")
        print(f"  Returns: ${returns:,.2f} ({returns_pct:+.2f}%)")
        print(f"  Total Trades: {portfolio['total_trades']}")
        print(f"  Final Cash: ${portfolio['cash']:,.2f}")
        print(f"  Holdings: {portfolio['holdings']}")
        print()

    # Save results to JSON
    results = {
        "ticker": ticker,
        "start_date": start_date,
        "end_date": end_date,
        "final_price": final_price,
        "traders": [
            {
                "name": trader.name,
                "model": trader.model_type,
                "final_value": trader.get_portfolio_value(current_prices),
                "trades": trader.trade_history
            }
            for trader in traders
        ]
    }

    output_file = "simulation_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    # Run simulation
    asyncio.run(run_simulation(
        ticker="AAPL",
        start_date="2020-07-01",
        end_date="2020-07-10",
        debug=True
    ))
