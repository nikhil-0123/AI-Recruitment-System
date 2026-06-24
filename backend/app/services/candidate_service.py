from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.candidate import Candidate
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.pagination import PageParams
from app.repositories.sort import SortOrder, SortParams


class CandidateService:
    def __init__(self, repository: CandidateRepository | None = None) -> None:
        self.repository = repository or CandidateRepository()

    async def create_candidate(self, db: AsyncSession, candidate_data: dict[str, Any]) -> Candidate:
        sanitized_data = {k: v for k, v in candidate_data.items() if v is not None}
        return await self.repository.create(db, sanitized_data)

    async def get_candidate(self, db: AsyncSession, candidate_id: object) -> Candidate:
        return await self.repository.get_by_id_or_raise(db, candidate_id)

    async def list_candidates(
        self,
        db: AsyncSession,
        page: int = 1,
        page_size: int = 25,
        sort_desc: bool = True,
    ) -> tuple[list[Candidate], int]:
        sort_params = SortParams(
            sort_by="created_at",
            sort_order=SortOrder.DESC if sort_desc else SortOrder.ASC,
        )
        page_params = PageParams(page=page, page_size=page_size)
        paginated = await self.repository.list(
            db,
            sort_params=sort_params,
            page_params=page_params,
        )
        return paginated.items, paginated.total
