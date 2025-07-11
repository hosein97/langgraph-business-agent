from typing import TypedDict
from pydantic import BaseModel


class Configuration(TypedDict):
    """Optional runtime config (not used here)."""
    my_configurable_param: str


class DailyMetrics(BaseModel):
    revenue: float
    cost: float
    number_of_customers: int


class BusinessInput(BaseModel):
    today: DailyMetrics
    yesterday: DailyMetrics


class AnalysisResult(BaseModel):
    profit: float | None = None
    revenue_change_percent: float | None = None
    cost_change_percent: float | None = None
    cac_change_percent: float | None = None
    alerts: list[str] | None = None
    recommendations: list[str] | None = None


class State(TypedDict):
    raw_input_data: dict[str, any]
    structured_input: BusinessInput | None = None
    result: AnalysisResult | None = None
