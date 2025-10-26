from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any, List
from datetime import datetime, timedelta
from agents import TechnicalAnalyst, SentimentAnalyst, DebateTeam, Trader
from services.data_loader import data_loader
import json

router = APIRouter()

# Store simulation results
simulation_results: Dict[str, Any] = {}
simulation_status: Dict[str, str] = {"status": "idle", "progress": 0}

@router.post("/run")
async def run_simulation(
    background_tasks: BackgroundTasks,
    ticker: str = "AAPL",
    start_date: str = "2020-07-01",
    end_date: str = "2020-07-15",
    debate_rounds: int = 2
):
    """
    Run a full trading simulation

    **API Integration Point**: Call from frontend to start simulation

    This runs in the background and can be polled via /simulation/status

    Args:
        ticker: Stock ticker to trade
        start_date: Simulation start date
        end_date: Simulation end date
        debate_rounds: Number of debate rounds per decision
    """
    # Start simulation in background
    background_tasks.add_task(
        _run_simulation_task,
        ticker, start_date, end_date, debate_rounds
    )

    return {
        "message": "Simulation started",
        "ticker": ticker,
        "start_date": start_date,
        "end_date": end_date,
        "status_url": "/api/simulation/status"
    }

@router.get("/status")
async def get_simulation_status():
    """
    Get current simulation status

    **API Integration Point**: Poll this from frontend to show progress bar
    """
    return simulation_status

@router.get("/results")
async def get_simulation_results():
    """
    Get simulation results

    **API Integration Point**: Call from frontend to display final results

    Returns:
        Complete simulation results including all trades and performance metrics
    """
    if not simulation_results:
        return {"message": "No simulation results available. Run /simulation/run first"}

    return simulation_results

@router.get("/results/summary")
async def get_results_summary():
    """
    Get summarized simulation results

    **API Integration Point**: Call from frontend for performance charts
    """
    if not simulation_results:
        return {"message": "No results available"}

    traders = simulation_results.get("traders", [])

    summary = {
        "ticker": simulation_results.get("ticker"),
        "period": {
            "start": simulation_results.get("start_date"),
            "end": simulation_results.get("end_date"),
            "days": simulation_results.get("total_days")
        },
        "traders": []
    }

    for trader in traders:
        summary["traders"].append({
            "name": trader["name"],
            "model": trader["model"],
            "final_value": trader["final_portfolio_value"],
            "total_return": trader["total_return"],
            "total_return_pct": trader["total_return_pct"],
            "total_trades": trader["total_trades"],
            "win_rate": _calculate_win_rate(trader["trades"])
        })

    return summary

def _calculate_win_rate(trades: List[Dict]) -> float:
    """Calculate win rate from trades"""
    if not trades:
        return 0.0

    profitable = sum(1 for t in trades if t.get("cost", 0) < 0)  # Negative cost = profit from sell
    return profitable / len(trades) if trades else 0.0

async def _run_simulation_task(
    ticker: str,
    start_date: str,
    end_date: str,
    debate_rounds: int
):
    """Background task to run simulation"""
    global simulation_results, simulation_status

    try:
        simulation_status = {"status": "running", "progress": 0}

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

        # Generate trading dates
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        trading_dates = []

        current = start
        while current <= end:
            # Skip weekends
            if current.weekday() < 5:
                trading_dates.append(current.strftime("%Y-%m-%d"))
            current += timedelta(days=1)

        total_days = len(trading_dates)
        all_decisions = []

        # Run simulation for each day
        for idx, date in enumerate(trading_dates):
            simulation_status["progress"] = int((idx / total_days) * 100)

            # Get current price
            current_price = data_loader.get_latest_price(ticker, date)

            # Run analysis
            tech_analysis = await technical.analyze(ticker, date)
            sent_analysis = await sentiment.analyze(ticker, date)
            debate_result = await debate.conduct_debate(
                ticker, date, tech_analysis, sent_analysis, debate_rounds
            )

            # Each trader makes decision
            day_decisions = {
                "date": date,
                "price": current_price,
                "technical": tech_analysis,
                "sentiment": sent_analysis,
                "debate": debate_result,
                "trader_decisions": []
            }

            for trader in traders:
                decision = await trader.make_decision(
                    ticker, date, current_price,
                    tech_analysis, sent_analysis, debate_result
                )
                day_decisions["trader_decisions"].append(decision)

            all_decisions.append(day_decisions)

        # Calculate final results
        final_price = data_loader.get_latest_price(ticker, trading_dates[-1])
        current_prices = {ticker: final_price}

        trader_results = []
        for trader in traders:
            portfolio = trader.get_portfolio_summary(current_prices)
            initial_value = 10000.0
            final_value = portfolio["portfolio_value"]

            trader_results.append({
                "name": trader.name,
                "model": trader.model_type,
                "initial_value": initial_value,
                "final_portfolio_value": final_value,
                "total_return": final_value - initial_value,
                "total_return_pct": ((final_value - initial_value) / initial_value) * 100,
                "final_cash": portfolio["cash"],
                "final_holdings": portfolio["holdings"],
                "total_trades": portfolio["total_trades"],
                "trades": portfolio["trade_history"]
            })

        # Store results
        simulation_results = {
            "ticker": ticker,
            "start_date": start_date,
            "end_date": end_date,
            "total_days": total_days,
            "final_price": final_price,
            "traders": trader_results,
            "daily_decisions": all_decisions
        }

        simulation_status = {"status": "completed", "progress": 100}

    except Exception as e:
        simulation_status = {"status": "error", "error": str(e), "progress": 0}
        print(f"Simulation error: {e}")

@router.delete("/reset")
async def reset_simulation():
    """
    Reset simulation state

    **API Integration Point**: Call from frontend to reset and start fresh
    """
    global simulation_results, simulation_status

    simulation_results = {}
    simulation_status = {"status": "idle", "progress": 0}

    return {"message": "Simulation reset successfully"}
