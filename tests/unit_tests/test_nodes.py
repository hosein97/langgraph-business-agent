from langgraph.pregel import Pregel
from agent.graph import graph, analyze_data, generate_recommendations, State
import pytest

from agent.graph import graph


@pytest.mark.anyio
async def test_analyze_data_node() -> None:
    input_state = State(
        input_data={
            "today": {"revenue": 1200, "cost": 800, "number_of_customers": 40},
            "yesterday": {"revenue": 1000, "cost": 700, "number_of_customers": 35}
        }
    )
    config = {"configurable": {}}
    result = await analyze_data(input_state, config)
    assert result["result"]["profit"] == 400
    assert "cac_change_percent" in result["result"]
    assert result["result"]["cac_change_percent"] is not None


@pytest.mark.anyio
async def test_generate_recommendations_node() -> None:
    input_state = State(
        input_data={},
        result={
            "profit": -200,
            "revenue_change_percent": 15,
            "cost_change_percent": 18,
            "cac_change_percent": 22
        }
    )
    config = {"configurable": {}}
    result = await generate_recommendations(input_state, config)
    recs = result["result"]["recommendations"]
    assert "Reduce costs if profit is negative." in recs
    assert "Review marketing campaigns if CAC increased significantly." in recs
    assert "Consider increasing advertising budget if sales are growing." in recs


@pytest.mark.anyio
async def test_generate_recommendations_missing_metrics() -> None:
    input_state = State(
        input_data={},
        result={
            "profit": 100,
            "revenue_change_percent": None,
            "cost_change_percent": 5,
            "cac_change_percent": None
        }
    )
    config = {"configurable": {}}
    result = await generate_recommendations(input_state, config)
    assert result["result"]["recommendations"] == []
    assert result["result"]["alerts"] == []
