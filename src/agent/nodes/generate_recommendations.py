# ------------- Async Node: Recommendation Logic -------------
from agent.schema import State, Configuration
from langchain_core.runnables import RunnableConfig
from typing import Any, Dict


async def generate_recommendations(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Generates alerts and recommendations based on available metrics."""
    result = state.result
    alerts = []
    recommendations = []

    profit = result.get("profit")
    cac_change = result.get("cac_change_percent")
    revenue_change = result.get("revenue_change_percent")

    # Recommend if there is a loss
    if profit is not None and profit < 0:
        alerts.append("Warning: Loss recorded today.")
        recommendations.append("Reduce costs if profit is negative.")

    # Recommend if CAC increased significantly
    if cac_change is not None and cac_change > 20:
        alerts.append("Alert: CAC increased more than 20%.")
        recommendations.append("Review marketing campaigns if CAC increased significantly.")

    # Recommend if revenue is growing
    if revenue_change is not None and revenue_change > 10:
        recommendations.append("Consider increasing advertising budget if sales are growing.")

    result["alerts"] = alerts
    result["recommendations"] = recommendations

    return {
        "input_data": state.input_data,
        "result": result
    }

