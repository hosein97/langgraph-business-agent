from typing import Any, Dict, List, TypedDict

from dataclasses import dataclass
from dataclasses import dataclass


class Configuration(TypedDict):
    """Optional runtime config (not used here)."""
    my_configurable_param: str


@dataclass
class State:
    """Input and intermediate state passed between nodes."""
    input_data: Dict[str, Any]
    result: Dict[str, Any] = None
