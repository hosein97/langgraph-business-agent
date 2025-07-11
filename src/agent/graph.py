from __future__ import annotations
from langgraph.graph import StateGraph
from agent.schema import State, Configuration
from agent.nodes import analyze_data, generate_recommendations, receive_input

graph = (
    StateGraph(State, config_schema=Configuration)
    .add_node("receive_input", receive_input)
    .add_node("analyze_data", analyze_data)
    .add_node("generate_recommendations", generate_recommendations)
    .add_edge("__start__", "receive_input")
    .add_edge("receive_input", "analyze_data")
    .add_edge("analyze_data", "generate_recommendations")
    .add_edge("generate_recommendations", "__end__")
    .compile(name="BusinessGraph")
)
