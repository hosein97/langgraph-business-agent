"""LangGraph business agent for analyzing sales data and generating recommendations."""
from __future__ import annotations

from langgraph.graph import StateGraph

from agent.schema import State, Configuration
from agent.nodes import analyze_data
from agent.nodes import generate_recommendations


# ------------- Graph Definition -------------

graph = (
    StateGraph(State, config_schema=Configuration)
    .add_node("analyze_data", analyze_data)
    .add_node("generate_recommendations", generate_recommendations)
    .add_edge("__start__", "analyze_data")
    .add_edge("analyze_data", "generate_recommendations")
    .compile(name="Business Intelligence Agent")
)
