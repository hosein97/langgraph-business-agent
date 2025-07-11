from agent.schema import State, AnalysisResult

async def analyze_data(state: State) -> State:
    input_data = state["structured_input"]
    today = input_data.today
    yesterday = input_data.yesterday

    profit = today.revenue - today.cost

    revenue_change = ((today.revenue - yesterday.revenue) / yesterday.revenue * 100) if yesterday.revenue else None
    cost_change = ((today.cost - yesterday.cost) / yesterday.cost * 100) if yesterday.cost else None

    cac_today = today.cost / today.number_of_customers if today.number_of_customers else None
    cac_yesterday = yesterday.cost / yesterday.number_of_customers if yesterday.number_of_customers else None

    cac_change = (
        ((cac_today - cac_yesterday) / cac_yesterday * 100)
        if cac_today is not None and cac_yesterday not in (None, 0) else None
    )

    return {
        "result": AnalysisResult(
            profit=profit,
            revenue_change_percent=round(revenue_change, 2) if revenue_change is not None else None,
            cost_change_percent=round(cost_change, 2) if cost_change is not None else None,
            cac_change_percent=round(cac_change, 2) if cac_change is not None else None,
        )
    }
