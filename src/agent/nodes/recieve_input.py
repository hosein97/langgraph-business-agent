from agent.schema import BusinessInput, DailyMetrics, State

async def receive_input(state: State) -> State:
    """Validates and parses raw input data into structured format."""
    try:
        raw = state["raw_input_data"]

        structured_input = BusinessInput(
            today=DailyMetrics(**raw["today"]),
            yesterday=DailyMetrics(**raw["yesterday"])
        )

        return {
            "structured_input": structured_input
        }

    except Exception as e:
        raise ValueError(f"Failed to parse input: {e}")
