# ------------- Async Node: Recommendation Logic -------------
from agent.schema import State, Configuration
from langchain_core.runnables import RunnableConfig
from typing import Any, Dict

async def generate_recommendations(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Generates alerts and recommendations based on metrics."""
    result = state.result
    alerts = []
    recommendations = []

    if result["profit"] < 0:
        alerts.append("Warning: Loss recorded today.")
        recommendations.append("Reduce costs if profit is negative.")

    if result["cac_change_percent"] > 20:
        alerts.append("Alert: CAC increased more than 20%.")
        recommendations.append("Review marketing campaigns if CAC increased significantly.")

    if result["revenue_change_percent"] > 10:
        recommendations.append("Consider increasing advertising budget if sales are growing.")

    result["alerts"] = alerts
    result["recommendations"] = recommendations

    return {
        "input_data": state.input_data,
        "result": result
    }
