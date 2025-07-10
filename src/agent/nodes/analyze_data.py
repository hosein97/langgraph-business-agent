# ------------- Async Node: Processing Logic -------------
from agent.schema import State
from langchain_core.runnables import RunnableConfig
from typing import Any, Dict

async def analyze_data(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Calculates profit, revenue/cost/CAC changes."""
    data = state.input_data
    today = data["today"]
    yesterday = data["yesterday"]

    # Calculate profit
    profit = today["revenue"] - today["cost"]

    # Safe revenue and cost change calculations
    revenue_change = (
        ((today["revenue"] - yesterday["revenue"]) / yesterday["revenue"]) * 100
        if yesterday["revenue"] != 0 else None
    )

    cost_change = (
        ((today["cost"] - yesterday["cost"]) / yesterday["cost"]) * 100
        if yesterday["cost"] != 0 else None
    )

    # Safe CAC calculations
    cac_today = (
        today["cost"] / today["number_of_customers"]
        if today["number_of_customers"] != 0 else None
    )

    cac_yesterday = (
        yesterday["cost"] / yesterday["number_of_customers"]
        if yesterday["number_of_customers"] != 0 else None
    )

    # Safe CAC change calculation
    if cac_today is not None and cac_yesterday not in (None, 0):
        cac_change = ((cac_today - cac_yesterday) / cac_yesterday) * 100
    else:
        cac_change = None

    result = {
        "profit": profit,
        "revenue_change_percent": round(revenue_change, 2) if revenue_change is not None else None,
        "cost_change_percent": round(cost_change, 2) if cost_change is not None else None,
        "cac_change_percent": round(cac_change, 2) if cac_change is not None else None,
    }

    return {
        "input_data": data,
        "result": result,
    }
