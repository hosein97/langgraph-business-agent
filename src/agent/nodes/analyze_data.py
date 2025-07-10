# ------------- Async Node: Processing Logic -------------
from agent.schema import State
from langchain_core.runnables import RunnableConfig
from typing import Any, Dict

async def analyze_data(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Calculates profit, revenue/cost/CAC changes."""
    data = state.input_data
    today = data["today"]
    yesterday = data["yesterday"]

    profit = today["revenue"] - today["cost"]
    revenue_change = ((today["revenue"] - yesterday["revenue"]) / yesterday["revenue"]) * 100
    cost_change = ((today["cost"] - yesterday["cost"]) / yesterday["cost"]) * 100

    cac_today = today["cost"] / today["number_of_customers"]
    cac_yesterday = yesterday["cost"] / yesterday["number_of_customers"]
    cac_change = ((cac_today - cac_yesterday) / cac_yesterday) * 100

    result = {
        "profit": profit,
        "revenue_change_percent": round(revenue_change, 2),
        "cost_change_percent": round(cost_change, 2),
        "cac_change_percent": round(cac_change, 2),
    }

    return {
        "input_data": data,
        "result": result,
    }
