from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.candidate_embedding import CandidateEmbedding
from app.models.job_embedding import JobEmbedding


class EmbeddingRepository:
    async def get_candidate_embedding(
        self,
        db: AsyncSession,
        candidate_id: uuid.UUID,
    ) -> CandidateEmbedding | None:
        query = select(CandidateEmbedding).where(CandidateEmbedding.candidate_id == candidate_id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_job_embedding(self, db: AsyncSession, job_id: uuid.UUID) -> JobEmbedding | None:
        query = select(JobEmbedding).where(JobEmbedding.job_id == job_id)
        result = await db.execute(query)
        return result.scalars().first()

    async def upsert_candidate_embedding(
        self,
        db: AsyncSession,
        candidate_id: uuid.UUID,
        embedding: list[float],
        model_name: str,
        model_version: str = "1.0",
    ) -> CandidateEmbedding:
        existing = await self.get_candidate_embedding(db, candidate_id)
        if existing is not None:
            existing.embedding = embedding
            existing.model_name = model_name
            existing.model_version = model_version
            await db.flush()
            return existing

        record = CandidateEmbedding(
            candidate_id=candidate_id,
            embedding=embedding,
            model_name=model_name,
            model_version=model_version,
        )
        db.add(record)
        await db.flush()
        return record

    async def upsert_job_embedding(
        self,
        db: AsyncSession,
        job_id: uuid.UUID,
        embedding: list[float],
        model_name: str,
        model_version: str = "1.0",
    ) -> JobEmbedding:
        existing = await self.get_job_embedding(db, job_id)
        if existing is not None:
            existing.embedding = embedding
            existing.model_name = model_name
            existing.model_version = model_version
            await db.flush()
            return existing

        record = JobEmbedding(
            job_id=job_id,
            embedding=embedding,
            model_name=model_name,
            model_version=model_version,
        )
        db.add(record)
        await db.flush()
        return record
