# Day 5 Technical Design

## Sprint 5 Deliverables

Sprint 5 must deliver:

- AI Matching Engine
- Candidate Ranking Engine
- Score Calculation
- Recommendation Engine
- Ranking APIs
- Ranking Screen (frontend later)

The backend Sprint 5 scope is to design and implement the complete AI matching and ranking flow, persist ranking results, and expose ranking APIs over FastAPI. The frontend ranking screen is not part of backend Sprint 5 implementation but should be supported by these APIs.

### Sprint 5 execution phases

- Sprint 5 – Phase 1: Infrastructure
  - Embedding repository and service
  - Matching service scaffolding
  - CandidateScore repository
  - Ranking service foundation
  - Async job integration
  - Ranking APIs

- Sprint 5 – Phase 2: AI Matching & Semantic Ranking
  - Candidate embedding generation
  - Job embedding generation
  - Semantic similarity and semantic score computation
  - Weighted ranking score calculation
  - Recommendation assignment and persistence
  - Ranking tests and validation

---

## RankingService Architecture

The core backend component is `RankingService`.

### Responsibilities

- Generate ranking results for a job
- Calculate one candidate's score breakdown for a job
- Retrieve persisted ranking results for a job
- Retrieve score breakdown for a candidate within a job

### Proposed public methods

```python
class RankingService:
    async def generate_ranking(self, job_id: UUID) -> AsyncJobRecord
    async def calculate_candidate_score(self, candidate_id: UUID, job_id: UUID) -> CandidateScore
    async def get_rankings(self, job_id: UUID) -> list[CandidateScore]
    async def get_score_breakdown(self, job_id: UUID, candidate_id: UUID) -> CandidateScore
```

### Design notes

- `generate_ranking(job_id)` is the orchestrator for ranking creation. It should not compute the full ranking synchronously in the request path.
- `calculate_candidate_score(candidate_id, job_id)` performs the per-candidate score breakdown using the defined formula and returns a `CandidateScore` record or plain data object.
- `get_rankings(job_id)` returns persisted ranking results sorted by `final_score desc, candidate_id asc` or stable tie rule.
- `get_score_breakdown(job_id, candidate_id)` returns the persisted score breakdown for a single candidate.

### Embedding dependency status

The ranking engine depends on semantic embeddings, but the current state is only partially complete:

- `CandidateEmbedding` and `JobEmbedding` models exist.
- Alembic migrations and PGVector-backed schema/indexes exist.
- The embedding generation flow is not yet proven to run when candidates or jobs are created.

Before ranking can be reliable, the backend must ensure that a 384-dimensional vector is actually generated and persisted into `candidate_embeddings` and `job_embeddings` for each candidate/job that participates in ranking.

### Module responsibilities

The architecture should remain split across three modules rather than collapsing everything into a single service:

```python
class EmbeddingService:
    async def generate_candidate_embedding(self, candidate_id: UUID) -> None
    async def generate_job_embedding(self, job_id: UUID) -> None

class MatchingService:
    async def compute_semantic_score(
        self,
        candidate_embedding: list[float],
        job_embedding: list[float],
    ) -> float
    async def compute_skill_score(self, candidate_id: UUID, job_id: UUID) -> float
    async def compute_experience_score(self, candidate_id: UUID, job_id: UUID) -> float
    async def compute_education_score(self, candidate_id: UUID, job_id: UUID) -> float

class RankingService:
    async def calculate_final_score(self, candidate_id: UUID, job_id: UUID) -> float
    async def assign_rank(self, job_id: UUID) -> None
    async def assign_recommendation(self, final_score: float) -> str
```

Each service should have one clear responsibility:

- `EmbeddingService` stores and regenerates embeddings.
- `MatchingService` computes component scores.
- `RankingService` orchestrates ranking generation, persists results, and assigns recommendations.

Likewise, a single `EmbeddingRepository` can manage both embedding tables rather than maintaining duplicate CRUD logic for candidate and job embeddings.

---

## CandidateScore Lifecycle

The candidate ranking lifecycle must use persistence.

### Persistence decisions

- Rankings are not recomputed on every GET request.
- Ranking results are persisted in the existing `candidate_scores` table.
- Each job/candidate pair has exactly one `candidate_scores` row.
- `generate_ranking` writes or updates this table.

### Persisted fields

The `candidate_scores` table must include:

- `candidate_id`
- `job_id`
- `skill_score`
- `experience_score`
- `education_score`
- `semantic_score`
- `ai_score`
- `final_score`
- `rank_position`
- `matched_skills`
- `missing_skills`
- `recommendation`

### Validation constraints

- All component scores and `final_score` are between `0` and `100`.
- `rank_position` is a positive integer.
- Unique key on `(candidate_id, job_id)`.

---

## Score Formula

The final score formula is fixed:

- `final_score = semantic_score * 0.35 + skill_score * 0.25 + experience_score * 0.20 + education_score * 0.10 + ai_score * 0.10`

### Score interpretation

- Each component should be expressed on a `0-100` scale.
- The final score is also `0-100`.
- The service should round or normalize values consistently (e.g. two decimal places) before persisting.

### Weight configuration

The scoring weights should not be hardcoded in business logic. They should live in a constants or configuration module such as:

```python
DEFAULT_RANKING_WEIGHTS = {
    "semantic": 0.35,
    "skill": 0.25,
    "experience": 0.20,
    "education": 0.10,
    "ai": 0.10,
}
```

This keeps the algorithm tunable without changing the service implementation every time the weighting strategy changes.

---

## Recommendation Categories

Use fixed thresholds defined by the AI Validation Plan:

- `85-100` → `Highly Recommended`
- `65-84` → `Recommended`
- `45-64` → `Consider`
- `0-44` → `Rejected`

### Recommendation assignment

- `recommendation` is derived from `final_score`.
- If `final_score` is exactly on a threshold boundary, assign to the higher category following the rule above.
- This should be computed once during ranking generation and persisted alongside the score.

### Embedding versioning

Embedding records should include a version field such as `model_name`, `model_version`, or `embedding_version` so that old vectors can be distinguished from newly generated ones. This avoids ambiguity when the model changes later and prevents accidental reuse of stale embeddings.

---

## Async Ranking Flow

Ranking generation must follow the async job architecture.

### Request flow

1. Client calls `POST /rankings/generate/{job_id}`.
2. API creates an `async_jobs` record with `job_type = ranking_generate` and `entity_type = job`, `entity_id = job_id`.
3. API dispatches a Celery task to compute the ranking.
4. API returns `202 Accepted` with task reference or async job metadata.

### Background flow

1. Celery worker receives the ranking generation task.
2. Worker loads job details, candidate roster, resumes/skills, and any supporting data.
3. Worker calls `RankingService.calculate_candidate_score` for each candidate.
4. Worker calculates `final_score`, rank positions, and recommendations.
5. Worker writes or upserts `candidate_scores` records.
6. Worker updates the `async_jobs` record to `COMPLETED` or `FAILED`.

### Important behavior

- Ranking generation should be idempotent for the same `job_id` if the job is still active.
- The request immediately returns without waiting for computation.
- The system may optionally reject concurrent ranking generation requests for the same job when an active ranking task exists.

### Ranking freshness rules

Ranking results should be treated as stale when relevant data changes. The following triggers should invalidate or require re-ranking:

- Job updated
- Candidate profile updated
- Resume re-parsed
- Embedding regenerated
- Scoring weights changed

These rules should be documented so that the system can decide when to refresh rankings instead of serving outdated results.

---

## API Contract

Implement exactly the contract from the API specification:

- `POST /rankings/generate/{job_id}`
  - Creates the async ranking job
  - Returns `202 Accepted`
  - Does not return ranking results directly

- `GET /rankings/{job_id}`
  - Returns ordered ranking results for the job
  - Results come from persisted `candidate_scores`

- `GET /rankings/{job_id}/{candidate_id}`
  - Returns the detailed candidate score breakdown and recommendation
  - Data comes from the persisted row in `candidate_scores`

### Expected payloads

- `POST /rankings/generate/{job_id}`
  - Response example:

```json
{
  "success": true,
  "message": "Job accepted",
  "data": {
    "job_id": "uuid",
    "status": "QUEUED",
    "job_type": "ranking_generate"
  }
}
```

- `GET /rankings/{job_id}`
  - Response example:

```json
[
  {
    "rank": 1,
    "candidate_id": "uuid",
    "final_score": 92.5,
    "recommendation": "Highly Recommended"
  }
]
```

- `GET /rankings/{job_id}/{candidate_id}`
  - Response example:

```json
{
  "candidate_id": "uuid",
  "job_id": "uuid",
  "skill_score": 88.0,
  "experience_score": 72.5,
  "education_score": 90.0,
  "semantic_score": 94.0,
  "ai_score": 80.0,
  "final_score": 86.9,
  "rank_position": 1,
  "recommendation": "Highly Recommended"
}
```

---

## Failure handling

The ranking pipeline should fail gracefully when prerequisites are missing or errors occur. Explicit behavior should be defined for:

- Candidate has no embedding
- Job has no embedding
- Embedding generation fails
- Similarity computation throws an error

In those cases, the service should avoid partial or misleading ranking data and update the async job status to `FAILED` with a meaningful error message instead of silently succeeding.

---

## Test Plan

Day 5 backend must include service and API tests that verify:

- Ranking generation triggers an async job record and returns `202`.
- Rankings are persisted and are not recomputed on GET.
- `GET /rankings/{job_id}` returns results sorted descending by `final_score`.
- Rank positions start at `1`.
- Ties are handled stably and deterministically.
- `final_score` values are within `0-100`.
- Recommendation categories map final score ranges correctly.
- Score breakdown endpoint returns all component scores and recommendation.
- Candidate score persistence uses one row per `(candidate_id, job_id)`.
- Async worker updates `async_jobs` status correctly.

### Mandatory validation cases

- Sorted descending by `final_score`.
- Rank positions `1, 2, 3...`.
- Equal final scores preserve stable ranking order.
- Scores outside `0-100` are rejected by persistence constraints.
- Category thresholds:
  - `95` → `Highly Recommended`
  - `75` → `Recommended`
  - `55` → `Consider`
  - `35` → `Rejected`

---

## Sprint 5 Implementation Order

Follow this sequence for Sprint 5:

1. `EmbeddingRepository` implementation
2. `EmbeddingService` implementation
3. `MatchingService` implementation
4. `CandidateScoreRepository` implementation
5. `RankingService` implementation
6. Async ranking Celery task
7. Ranking router and async submission endpoint
8. Unit tests for embedding, matching, and ranking services
9. API tests for ranking endpoints and async submission

### Sprint 5 – Phase 2 follow-up work

Once the infrastructure path is stable, the AI-specific matching and scoring logic should be completed in the second phase:

1. Generate candidate embeddings on create/update flows
2. Generate job embeddings on create/update flows
3. Compute cosine similarity between candidate and job vectors
4. Convert similarity into semantic score
5. Apply the weighted final score formula and persist ranking results
6. Add end-to-end ranking tests for semantic scoring

---

## Key design decisions to lock now

- Rankings are persisted in `candidate_scores`.
- The embedding dependency is only partially complete: models and migrations exist, but the actual generation-and-storage pipeline still needs to be implemented and verified.
- Day 5 should provide infrastructure support for embeddings via a single `EmbeddingService` and `EmbeddingRepository`.
- Ranking generation is asynchronous via `async_jobs` and Celery.
- The API contract is exactly the documented three endpoints.
- Scores use the fixed 35/25/20/10/10 formula.
- Recommendation categories are the fixed thresholds from the AI Validation Plan.
- Service layer comes before routers.

This document should guide Sprint 5 implementation and keep the backend aligned with the ranking dependency chain.
