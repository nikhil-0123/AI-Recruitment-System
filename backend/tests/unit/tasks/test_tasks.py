from __future__ import annotations

import pytest
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.async_job import AsyncJob
from app.tasks.tasks import generate_ranking_task


class DummyRequest:
    id = "test-task-id"


class DummyTask:
    request = DummyRequest()


@pytest.mark.asyncio
async def test_generate_ranking_task_success(monkeypatch, async_session: AsyncSession) -> None:
    async_job_id = str(uuid4())
    job_id = str(uuid4())

    async_job = AsyncJob(
        id=async_job_id,
        job_type="ranking_generate",
        entity_type="job",
        entity_id=job_id,
        status="PENDING",
        payload_json={"job_id": job_id},
    )
    async_session.add(async_job)
    await async_session.flush()

    class FakeRankingService:
        async def generate_ranking(self, db, jid):
            assert jid == job_id

    async def fake_get_db_context():
        class DummyContext:
            async def __aenter__(self_inner):
                return async_session

            async def __aexit__(self_inner, exc_type, exc, tb):
                return False

        return DummyContext()

    monkeypatch.setattr("app.tasks.tasks.get_db_context", lambda: fake_get_db_context())
    monkeypatch.setattr("app.tasks.tasks.RankingService", lambda: FakeRankingService())
    monkeypatch.setattr("app.tasks.tasks.generate_ranking_task", DummyTask())

    result = generate_ranking_task(async_job_id, job_id)
    assert result["status"] == "completed"

    refreshed = await async_session.get(AsyncJob, async_job_id)
    assert refreshed.status == "COMPLETED"
    assert refreshed.result_json == {"message": "ranking_complete"}
    assert refreshed.celery_task_id == "test-task-id"


@pytest.mark.asyncio
async def test_generate_ranking_task_failure(monkeypatch, async_session: AsyncSession) -> None:
    async_job_id = str(uuid4())
    job_id = str(uuid4())

    async_job = AsyncJob(
        id=async_job_id,
        job_type="ranking_generate",
        entity_type="job",
        entity_id=job_id,
        status="PENDING",
        payload_json={"job_id": job_id},
    )
    async_session.add(async_job)
    await async_session.flush()

    class FakeRankingService:
        async def generate_ranking(self, db, jid):
            raise RuntimeError("ranking failed")

    async def fake_get_db_context():
        class DummyContext:
            async def __aenter__(self_inner):
                return async_session

            async def __aexit__(self_inner, exc_type, exc, tb):
                return False

        return DummyContext()

    monkeypatch.setattr("app.tasks.tasks.get_db_context", lambda: fake_get_db_context())
    monkeypatch.setattr("app.tasks.tasks.RankingService", lambda: FakeRankingService())
    monkeypatch.setattr("app.tasks.tasks.generate_ranking_task", DummyTask())

    with pytest.raises(RuntimeError, match="ranking failed"):
        generate_ranking_task(async_job_id, job_id)

    refreshed = await async_session.get(AsyncJob, async_job_id)
    assert refreshed.status == "FAILED"
    assert refreshed.error_message == "ranking failed"


def test_generate_ranking_task_celery_not_configured(monkeypatch) -> None:
    monkeypatch.setattr("app.tasks.celery_app.celery_app", None)
    with pytest.raises(RuntimeError, match="Celery is not configured"):
        generate_ranking_task()
