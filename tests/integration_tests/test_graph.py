import pytest
from agent.graph import graph, State

pytestmark = pytest.mark.anyio

async def test_agent_simple_passthrough() -> None:
    inputs = State(
        input_data={
            "today": {"revenue": 1200, "cost": 800, "number_of_customers": 40},
            "yesterday": {"revenue": 1000, "cost": 700, "number_of_customers": 35}
        }
    )
    res = await graph.ainvoke(inputs)
    assert res['result']["profit"] == 400
    assert isinstance(res['result']["recommendations"], list)


async def test_agent_negative_profit() -> None:
    inputs = State(
        input_data={
            "today": {"revenue": 500, "cost": 1000, "number_of_customers": 20},
            "yesterday": {"revenue": 600, "cost": 900, "number_of_customers": 25}
        }
    )
    res = await graph.ainvoke(inputs)
    recs = res['result']["recommendations"]
    assert res['result']["profit"] == -500
    assert "Reduce costs if profit is negative." in recs


async def test_agent_high_cac_warning() -> None:
    inputs = State(
        input_data={
            "today": {"revenue": 800, "cost": 600, "number_of_customers": 10},
            "yesterday": {"revenue": 800, "cost": 400, "number_of_customers": 10}
        }
    )
    res = await graph.ainvoke(inputs)
    recs = res['result']["recommendations"]
    assert res['result']["cac_change_percent"] > 20
    assert "Review marketing campaigns if CAC increased significantly." in recs


async def test_agent_sales_growth_recommendation() -> None:
    inputs = State(
        input_data={
            "today": {"revenue": 1100, "cost": 800, "number_of_customers": 30},
            "yesterday": {"revenue": 900, "cost": 700, "number_of_customers": 30}
        }
    )
    res = await graph.ainvoke(inputs)
    recs = res['result']["recommendations"]
    assert res['result']["revenue_change_percent"] > 10
    assert "Consider increasing advertising budget if sales are growing." in recs  # ← added missing period


async def test_agent_zero_customers_handling() -> None:
    inputs = State(
        input_data={
            "today": {"revenue": 1000, "cost": 500, "number_of_customers": 0},
            "yesterday": {"revenue": 800, "cost": 400, "number_of_customers": 0}
        }
    )
    res = await graph.ainvoke(inputs)
    assert "cac_change_percent" in res['result']
    assert res['result']["cac_change_percent"] is None
    assert isinstance(res['result']["recommendations"], list)
    assert "Review marketing campaigns if CAC increased significantly." not in res["result"]["recommendations"]


async def test_agent_no_recommendation() -> None:
    inputs = State(
        input_data={
            "today": {"revenue": 1000, "cost": 600, "number_of_customers": 20},
            "yesterday": {"revenue": 990, "cost": 590, "number_of_customers": 20}
        }
    )
    res = await graph.ainvoke(inputs)
    recs = res['result']["recommendations"]
    assert res['result']["profit"] > 0
    assert res['result']["cac_change_percent"] < 20
    assert res['result']["revenue_change_percent"] < 10
    assert recs == []
