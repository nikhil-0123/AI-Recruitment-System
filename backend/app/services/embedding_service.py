from __future__ import annotations

import sys
import time
import uuid
from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.candidate import Candidate
from app.models.candidate_embedding import CandidateEmbedding
from app.models.job import Job
from app.models.job_embedding import JobEmbedding
from app.repositories.embedding_repository import EmbeddingRepository
from app.repositories.exceptions import NotFoundError


class EmbeddingService:
    """Generate and persist semantic embeddings for candidates and jobs."""

    def __init__(self, repository: EmbeddingRepository | None = None) -> None:
        self.repository = repository or EmbeddingRepository()
        self.model_name = "all-MiniLM-L6-v2"
        self.embedding_dim = 384
        self.model_version = "1.0"

    async def generate_candidate_embedding(
        self,
        db: AsyncSession,
        candidate_id: uuid.UUID,
        text: str,
        regenerate: bool = False,
    ) -> CandidateEmbedding:
        candidate = await self._get_candidate_or_raise(db, candidate_id)
        embedding = await self._generate_embedding(text)
        if regenerate:
            existing = await self.repository.get_candidate_embedding(db, candidate_id)
            if existing is not None and existing.embedding is not None:
                existing.embedding = embedding
                existing.model_name = self.model_name
                existing.model_version = self.model_version
                await db.flush()
                return existing
        return await self.repository.upsert_candidate_embedding(
            db,
            candidate.id,
            embedding,
            self.model_name,
            self.model_version,
        )

    async def generate_job_embedding(
        self,
        db: AsyncSession,
        job_id: uuid.UUID,
        text: str,
        regenerate: bool = False,
    ) -> JobEmbedding:
        job = await self._get_job_or_raise(db, job_id)
        embedding = await self._generate_embedding(text)
        if regenerate:
            existing = await self.repository.get_job_embedding(db, job_id)
            if existing is not None and existing.embedding is not None:
                existing.embedding = embedding
                existing.model_name = self.model_name
                existing.model_version = self.model_version
                await db.flush()
                return existing
        return await self.repository.upsert_job_embedding(
            db,
            job.id,
            embedding,
            self.model_name,
            self.model_version,
        )

    async def get_candidate_embedding(
        self,
        db: AsyncSession,
        candidate_id: uuid.UUID,
    ) -> CandidateEmbedding | None:
        return await self.repository.get_candidate_embedding(db, candidate_id)

    async def get_job_embedding(
        self,
        db: AsyncSession,
        job_id: uuid.UUID,
    ) -> JobEmbedding | None:
        return await self.repository.get_job_embedding(db, job_id)

    async def measure_embedding_generation(self, text: str) -> dict[str, Any]:
        started = time.perf_counter()
        embedding = await self._generate_embedding(text)
        duration_ms = (time.perf_counter() - started) * 1000.0
        return {
            "dimension": len(embedding),
            "model_name": self.model_name,
            "duration_ms": round(duration_ms, 3),
        }

    async def _generate_embedding(self, text: str) -> list[float]:
        project_root = Path(__file__).resolve().parents[3]
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))

        from ai_engine.embeddings.embedding_service import EmbeddingService as AIEmbeddingService

        ai_service = AIEmbeddingService()
        return ai_service.embed_text(text)

    async def _get_candidate_or_raise(self, db: AsyncSession, candidate_id: uuid.UUID) -> Candidate:
        candidate = await db.get(Candidate, candidate_id)
        if candidate is None:
            raise NotFoundError("Candidate", candidate_id)
        return candidate

    async def _get_job_or_raise(self, db: AsyncSession, job_id: uuid.UUID) -> Job:
        job = await db.get(Job, job_id)
        if job is None:
            raise NotFoundError("Job", job_id)
        return job
