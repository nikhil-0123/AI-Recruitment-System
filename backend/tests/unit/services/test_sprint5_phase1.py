from __future__ import annotations

from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.candidate import Candidate
from app.models.candidate_embedding import CandidateEmbedding
from app.models.job import Job
from app.models.job_embedding import JobEmbedding
from app.models.user import User
from app.services.embedding_service import EmbeddingService
from app.services.ranking_service import RankingService


@pytest.mark.asyncio
async def test_embedding_service_generates_and_persists_embeddings(async_session: AsyncSession) -> None:
    user = User(name="Riley", email="riley@example.com", password_hash="hash", role="RECRUITER")
    async_session.add(user)
    await async_session.flush()

    candidate = Candidate(
        full_name="Ada Lovelace",
        email="ada@example.com",
        experience_years=Decimal("5.0"),
        education="Bachelor's",
    )
    async_session.add(candidate)
    await async_session.flush()

    job = Job(
        recruiter_id=user.id,
        title="Python Backend Engineer",
        description="Build FastAPI services and data pipelines.",
        experience_required=4,
        education_required="Bachelor's",
    )
    async_session.add(job)
    await async_session.flush()

    service = EmbeddingService()
    await service.generate_candidate_embedding(
        async_session,
        candidate.id,
        text="Senior Python developer with FastAPI PostgreSQL and Docker experience.",
    )
    await service.generate_job_embedding(
        async_session,
        job.id,
        text="Looking for a backend engineer experienced in Python FastAPI and PostgreSQL.",
    )

    candidate_embedding = await service.get_candidate_embedding(async_session, candidate.id)
    job_embedding = await service.get_job_embedding(async_session, job.id)

    assert isinstance(candidate_embedding, CandidateEmbedding)
    assert isinstance(job_embedding, JobEmbedding)
    assert len(candidate_embedding.embedding) == 384
    assert len(job_embedding.embedding) == 384
    assert candidate_embedding.model_name == "all-MiniLM-L6-v2"
    assert job_embedding.model_name == "all-MiniLM-L6-v2"


@pytest.mark.asyncio
async def test_ranking_service_persists_candidate_scores(async_session: AsyncSession) -> None:
    user = User(name="Jordan", email="jordan@example.com", password_hash="hash", role="RECRUITER")
    async_session.add(user)
    await async_session.flush()

    candidate = Candidate(
        full_name="Sam Rivera",
        email="sam@example.com",
        experience_years=Decimal("6.0"),
        education="Master's",
    )
    job = Job(
        recruiter_id=user.id,
        title="Senior Data Engineer",
        description="Work with Python, SQL, and distributed systems.",
        experience_required=5,
        education_required="Bachelor's",
    )
    async_session.add_all([candidate, job])
    await async_session.flush()

    embedding_service = EmbeddingService()
    await embedding_service.generate_candidate_embedding(
        async_session,
        candidate.id,
        text="Experienced data engineer with Python SQL and distributed systems.",
    )
    await embedding_service.generate_job_embedding(
        async_session,
        job.id,
        text="Need a senior data engineer who knows Python SQL and distributed systems.",
    )

    ranking_service = RankingService()
    score = await ranking_service.calculate_candidate_score(async_session, candidate.id, job.id)

    assert score.final_score is not None
    assert 0 <= float(score.final_score) <= 100
    assert score.recommendation in {"Highly Recommended", "Recommended", "Consider", "Rejected"}

    persisted = await ranking_service.get_score_breakdown(async_session, job.id, candidate.id)
    assert persisted is not None
    assert persisted.candidate_id == candidate.id
    assert persisted.job_id == job.id


@pytest.mark.asyncio
async def test_embedding_service_regenerates_and_tracks_model_version(async_session: AsyncSession) -> None:
    user = User(name="Riley", email="riley2@example.com", password_hash="hash", role="RECRUITER")
    async_session.add(user)
    await async_session.flush()

    candidate = Candidate(
        full_name="Grace Hopper",
        email="grace@example.com",
        experience_years=Decimal("8.0"),
        education="Master's",
    )
    async_session.add(candidate)
    await async_session.flush()

    service = EmbeddingService()
    first = await service.generate_candidate_embedding(
        async_session,
        candidate.id,
        text="Machine learning engineer working on Python and data pipelines.",
    )
    regenerated = await service.generate_candidate_embedding(
        async_session,
        candidate.id,
        text="Senior machine learning engineer specializing in large language models and MLOps.",
        regenerate=True,
    )

    assert first.model_name == "all-MiniLM-L6-v2"
    assert regenerated.model_name == "all-MiniLM-L6-v2"
    assert regenerated.model_version == "1.0"
    assert len(regenerated.embedding) == 384
    assert len(first.embedding) == 384
    assert regenerated.updated_at is not None
    assert regenerated.updated_at >= first.updated_at
    assert sum(value * value for value in regenerated.embedding) == pytest.approx(1.0, abs=1e-6)

    persisted = await service.get_candidate_embedding(async_session, candidate.id)
    assert persisted is not None
    assert persisted.model_version == "1.0"
    assert persisted.updated_at is not None
    assert persisted.updated_at >= first.updated_at


@pytest.mark.asyncio
async def test_embedding_service_measurement_reports_dimensions_and_latency() -> None:
    service = EmbeddingService()
    metrics = await service.measure_embedding_generation("FastAPI service with Celery and PostgreSQL")

    assert metrics["dimension"] == 384
    assert metrics["model_name"] == "all-MiniLM-L6-v2"
    assert metrics["duration_ms"] >= 0.0
