from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class FilterOperator(str, Enum):
    EQ = "eq"


@dataclass(frozen=True)
class Filter:
    field: str
    value: Any
    operator: FilterOperator = FilterOperator.EQ


@dataclass
class FilterParams:
    filters: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return self.filters.copy()
