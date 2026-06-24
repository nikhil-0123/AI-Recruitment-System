from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


@dataclass
class SortParams:
    sort_by: str | None = None
    sort_order: SortOrder = SortOrder.ASC
