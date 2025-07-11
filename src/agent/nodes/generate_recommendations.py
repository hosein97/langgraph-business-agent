from agent.schema import State, AnalysisResult

async def generate_recommendations(state: State) -> State:
    result: AnalysisResult = state["result"]
    alerts = []
    recommendations = []

    if result and result.profit is not None and result.profit < 0:
        alerts.append("Warning: Loss recorded today.")
        recommendations.append("Reduce costs if profit is negative.")

    if result and result.cac_change_percent is not None and result.cac_change_percent > 20:
        alerts.append("Alert: CAC increased more than 20%.")
        recommendations.append("Review marketing campaigns if CAC increased significantly.")

    if result and result.revenue_change_percent is not None and result.revenue_change_percent > 10:
        recommendations.append("Consider increasing advertising budget if sales are growing.")

    result.alerts = alerts
    result.recommendations = recommendations

    return {
        "result": result
    }
