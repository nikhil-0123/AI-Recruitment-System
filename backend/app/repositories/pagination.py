from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Generic, List, TypeVar

MAX_PAGE_SIZE = 100
T = TypeVar("T")


@dataclass(frozen=True)
class PageParams:
    page: int = 1
    page_size: int = 25

    def __post_init__(self) -> None:
        if self.page < 1:
            raise ValueError("page must be >= 1")
        if self.page_size < 1 or self.page_size > MAX_PAGE_SIZE:
            raise ValueError(f"page_size must be between 1 and {MAX_PAGE_SIZE}")


@dataclass
class PaginatedResult(Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool
    has_prev: bool

    @classmethod
    def create(
        cls,
        items: List[T],
        total: int,
        page: int = 1,
        page_size: int = 25,
    ) -> "PaginatedResult[T]":
        pages = max(1, math.ceil(total / page_size)) if total > 0 else 1
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1,
        )
