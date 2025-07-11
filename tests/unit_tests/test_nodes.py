import pytest
from langgraph.pregel import Pregel
from agent.graph import graph, analyze_data, generate_recommendations, receive_input
from agent.schema import DailyMetrics, BusinessInput, AnalysisResult, State

def test_graph_instance() -> None:
    assert isinstance(graph, Pregel)
    
@pytest.mark.anyio
async def test_receive_input_node() -> None:
    raw_input = {
        "today": {"revenue": 1200, "cost": 800, "number_of_customers": 40},
        "yesterday": {"revenue": 1000, "cost": 700, "number_of_customers": 35},
    }

    input_state: State = {
        "raw_input_data": raw_input
    }

    result = await receive_input(input_state)

    assert isinstance(result["structured_input"], BusinessInput)
    assert result["structured_input"].today.revenue == 1200
    assert result["structured_input"].yesterday.cost == 700

@pytest.mark.anyio
async def test_analyze_data_node() -> None:
    input_state: State = {
        "structured_input": BusinessInput(
            today=DailyMetrics(revenue=1200, cost=800, number_of_customers=40),
            yesterday=DailyMetrics(revenue=1000, cost=700, number_of_customers=35),
        )
    }

    state = await analyze_data(input_state)

    assert state["result"].profit == 400
    assert state["result"].cac_change_percent is not None



@pytest.mark.anyio
async def test_generate_recommendations_node() -> None:
    input_state: State = {
        "structured_input": BusinessInput(
            today=DailyMetrics(revenue=0, cost=0, number_of_customers=1),
            yesterday=DailyMetrics(revenue=0, cost=0, number_of_customers=1),
        ),
        "result": AnalysisResult(
            profit=-200,
            revenue_change_percent=15,
            cost_change_percent=18,
            cac_change_percent=22
        )
    }

    state = await generate_recommendations(input_state)
    recs = state["result"].recommendations

    assert "Reduce costs if profit is negative." in recs
    assert "Review marketing campaigns if CAC increased significantly." in recs
    assert "Consider increasing advertising budget if sales are growing." in recs


@pytest.mark.anyio
async def test_generate_recommendations_missing_metrics() -> None:
    input_state: State = {
        "structured_input": BusinessInput(
            today=DailyMetrics(revenue=0, cost=0, number_of_customers=1),
            yesterday=DailyMetrics(revenue=0, cost=0, number_of_customers=1),
        ),
        "result": AnalysisResult(
            profit=100,
            revenue_change_percent=None,
            cost_change_percent=5,
            cac_change_percent=None,
        )
    }

    state = await generate_recommendations(input_state)

    assert state["result"].recommendations == []
    assert state["result"].alerts == []
