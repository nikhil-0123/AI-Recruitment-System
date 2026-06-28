# AI Recruitment Automation System (ARAS)

# Async Job Architecture

Document Number: 14

Version: 1.0

Date: June 2026

Document Owner: Backend Lead + DevOps Lead

Document Status: Approved for Implementation

Scope: ARAS Version 1.0 asynchronous processing using FastAPI, Celery, Redis, PostgreSQL, and S3-compatible storage.

---

# 1. Purpose

This document defines how ARAS handles all long-running background work in Version 1.

The goals are:

* Keep API responses fast
* Prevent request timeouts during resume processing
* Make bulk upload and AI tasks reliable
* Provide clear job status to frontend users
* Fit within the approved 40-day roadmap

This architecture does **not** introduce microservices, event streaming platforms, or distributed workflow engines. ARAS V1 remains a modular monolith with Celery workers.

---

# 2. Async Processing Principles

ARAS V1 follows these principles:

1. HTTP APIs accept work quickly and return a tracking identifier.
2. Long-running work is delegated to Celery.
3. PostgreSQL remains the source of truth for business state.
4. Redis is used as queue broker and cache, not as the permanent source of record.
5. Every async operation must be observable, retryable, and safe to re-run.
6. User-facing pages must show progress and failure states.

---

# 3. Jobs That Must Be Asynchronous

The following operations are asynchronous in V1:

| Job Type ID | Operation | Reason for Async |
| ----------- | --------- | ---------------- |
| ASJ-01 | Resume parsing | File I/O and text extraction can exceed request budget |
| ASJ-02 | Embedding generation | Model inference should not block request thread |
| ASJ-03 | Bulk resume processing | Multiple files require queued processing |
| ASJ-04 | AI summary generation | External Gemini API call can be slow or fail |
| ASJ-05 | Interview question generation | External Gemini API call can be slow or fail |
| ASJ-06 | Report generation (PDF/CSV/XLSX) | Export generation can be heavy for large result sets |
| ASJ-07 | Re-ranking after new candidates uploaded | Score recomputation across many candidates |

The following operations remain synchronous in V1:

| Operation | Reason |
| --------- | ------ |
| Login / register | Must return immediately |
| Job creation / update | Lightweight DB write |
| Candidate list retrieval | Read-only query |
| Ranking list retrieval | Reads existing computed results |
| Analytics dashboard retrieval | Pre-aggregated / query-limited |

---

# 4. High-Level Architecture

```text
React Frontend
    ↓
FastAPI API Layer
    ↓
Service Layer
    ├── Immediate DB writes (PostgreSQL)
    ├── S3 file upload
    └── Celery task dispatch
             ↓
          Redis Broker
             ↓
         Celery Workers
             ↓
    AI / Parsing / Export Services
             ↓
        PostgreSQL + S3
```

The frontend never talks directly to Celery or Redis. It only interacts with FastAPI APIs that create jobs and query job status.

---

# 5. V1 Async Job Scope

To keep V1 realistic, ARAS uses a small and stable set of job flows only.

## Supported Async Flows

```text
Flow 1: Upload resume → parse → extract skills → create/update candidate → generate embedding
Flow 2: Upload multiple resumes → enqueue one task per file → aggregate progress
Flow 3: Generate ranking for a job → compute scores → persist candidate_scores
Flow 4: Generate AI summary for candidate-job pair → persist ai_summaries
Flow 5: Generate interview questions for candidate-job pair → persist interview_questions
Flow 6: Generate report export → store output file → return download URL
```

## Explicitly Out of Scope for V1

```text
- Real-time websocket streaming
- Distributed saga orchestration
- Kafka / RabbitMQ introduction
- Multi-region processing
- Multi-tenant queue partitioning
- Human approval workflow engine
- Custom ML training pipelines
```

---

# 6. Async Job State Model

All async jobs must use a shared lifecycle state model.

## Canonical Job States

| State | Meaning |
| ----- | ------- |
| `PENDING` | Job record created, not yet picked by worker |
| `QUEUED` | Enqueued to broker |
| `STARTED` | Worker has started processing |
| `RETRYING` | Previous attempt failed, retry scheduled |
| `COMPLETED` | Finished successfully |
| `FAILED` | Finished unsuccessfully after retries |
| `CANCELLED` | Cancel requested before execution; optional in V1 |
| `PARTIAL` | Batch job completed with some item failures |

For V1, `CANCELLED` support is optional and only applies before `STARTED`.

---

# 7. Persistence Model

## 7.1 Source of Truth

PostgreSQL is the source of truth for async job status.

Redis stores broker-level queue information only. Redis keys are not treated as durable state.

## 7.2 Database Usage

The existing database design already includes audit logging and core domain tables. This document introduces one additional operational table required for reliable async processing.

### New Table: `async_jobs`

```text
async_jobs
```

Fields:

| Field | Type | Description |
| ----- | ---- | ----------- |
| id | UUID PK | Internal job identifier |
| job_type | VARCHAR(50) | `resume_parse`, `embedding_generate`, `ranking_generate`, `summary_generate`, `questions_generate`, `report_generate`, `bulk_upload` |
| entity_type | VARCHAR(50) | `resume`, `candidate`, `job`, `report`, `batch` |
| entity_id | UUID NULL | Related business entity |
| celery_task_id | VARCHAR(255) NULL | Celery task ID |
| status | VARCHAR(20) | Canonical state |
| priority | SMALLINT | 1 = high, 5 = low |
| attempts | INTEGER | Total attempts made |
| max_attempts | INTEGER | Retry cap |
| payload_json | JSONB | Minimal safe payload reference data |
| result_json | JSONB NULL | Summary result metadata |
| error_message | TEXT NULL | Last error message |
| error_code | VARCHAR(100) NULL | Normalized application error code |
| requested_by | UUID | FK to users.id |
| parent_job_id | UUID NULL | Used for batch aggregation |
| started_at | TIMESTAMP NULL | Processing start time |
| completed_at | TIMESTAMP NULL | Completion time |
| created_at | TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP | Last update time |
```

## 7.3 Supporting Indexes

```text
INDEX idx_async_jobs_status (status)
INDEX idx_async_jobs_job_type (job_type)
INDEX idx_async_jobs_entity (entity_type, entity_id)
INDEX idx_async_jobs_requested_by (requested_by)
INDEX idx_async_jobs_parent_job_id (parent_job_id)
INDEX idx_async_jobs_created_at (created_at DESC)
UNIQUE INDEX uq_async_jobs_celery_task_id (celery_task_id)
```

---

# 8. Queue Topology

To keep deployment simple, V1 uses a single Redis broker with three logical Celery queues.

| Queue Name | Purpose | Worker Count (Initial) | Priority |
| ---------- | ------- | ---------------------- | -------- |
| `default` | Light operational jobs | 1 | Medium |
| `ai` | Summaries, questions, embeddings, ranking | 2 | High |
| `exports` | PDF/CSV/XLSX report generation | 1 | Low |

## Queue Routing Rules

| Job Type | Queue |
| -------- | ----- |
| resume_parse | `default` |
| embedding_generate | `ai` |
| ranking_generate | `ai` |
| summary_generate | `ai` |
| questions_generate | `ai` |
| report_generate | `exports` |
| bulk_upload | `default` |

This queue design is intentionally minimal for the 40-day roadmap. It allows separation between heavy export work and AI processing without requiring complex infrastructure.

---

# 9. Core Async Flows

## 9.1 Single Resume Upload Flow

```text
1. Frontend uploads file to POST /resumes/upload
2. API validates MIME type, size, and auth
3. File stored in S3-compatible storage
4. Resume DB record created with status = UPLOADED
5. async_jobs record created (job_type = resume_parse)
6. Celery task dispatched
7. API returns 202 Accepted with job_id
8. Worker parses file
9. Candidate profile created/updated
10. Skills extracted
11. Embedding job created and queued
12. Resume status updated to PARSED or FAILED
13. async_jobs updated to COMPLETED or FAILED
```

## 9.2 Bulk Resume Upload Flow

```text
1. Frontend uploads N files
2. API validates each file
3. Batch parent async_jobs record created (job_type = bulk_upload)
4. For each file:
   - Store file
   - Create resume record
   - Create child async_jobs record (resume_parse)
   - Link child.parent_job_id = parent.id
5. API returns 202 Accepted with parent job_id
6. Frontend polls parent and child progress
7. Parent transitions:
   - COMPLETED if all child jobs completed
   - PARTIAL if any child failed and at least one completed
   - FAILED if all child jobs failed
```

## 9.3 Ranking Generation Flow

```text
1. Frontend triggers POST /rankings/generate
2. API validates job exists and candidates available
3. async_jobs record created (ranking_generate)
4. Worker loads job requirements + candidate data
5. Worker computes semantic, skill, experience, education, AI scores
6. candidate_scores rows inserted/updated
7. Rankings sorted and persisted
8. async_jobs status = COMPLETED
```

## 9.4 AI Summary / Interview Questions Flow

```text
1. Frontend requests summary/questions
2. API checks if existing result already stored
3. If found, return existing record immediately
4. If not found, create async_jobs record and queue task
5. Worker calls Gemini with timeout + retry policy
6. On success, persist structured response
7. On failure, generate deterministic fallback and persist with is_fallback = true
8. async_jobs status = COMPLETED unless internal processing fully failed
```

## 9.5 Report Generation Flow

```text
1. Frontend requests export
2. API creates async_jobs record (report_generate)
3. Worker generates file in temp location
4. File uploaded to S3-compatible storage
5. reports table updated with file path and metadata
6. async_jobs result_json stores report_id and file_key
7. Frontend polls job and receives download endpoint when complete
```

---

# 10. Idempotency Rules

All async jobs must be safe to retry.

## Idempotency Principles

1. Every worker task must re-check current business state before mutating data.
2. Re-running the same task must not create duplicate candidates, duplicate score rows, or duplicate summary rows.
3. Writes should use upsert semantics where appropriate.

## Required Idempotency Rules by Job Type

| Job Type | Rule |
| -------- | ---- |
| resume_parse | If resume already has `processing_status = COMPLETED`, task exits safely |
| embedding_generate | If embedding exists and source hash unchanged, do not regenerate |
| ranking_generate | Upsert `candidate_scores` by `(candidate_id, job_id)` |
| summary_generate | Upsert by `(candidate_id, job_id)` in `ai_summaries` |
| questions_generate | Upsert by `(candidate_id, job_id)` in `interview_questions` |
| report_generate | Create new report row only once per request; re-run updates same async job result |

---

# 11. Retry Policy

Retries are required for transient failures only.

## Retryable Failure Types

| Failure Type | Retry? | Notes |
| ------------ | ------ | ----- |
| Redis broker temporary issue | Yes | exponential backoff |
| Gemini API 429 | Yes | up to max attempts |
| Gemini API timeout | Yes | up to max attempts |
| S3 transient upload error | Yes | up to max attempts |
| PostgreSQL deadlock / transient connection error | Yes | retry transaction |
| Corrupted resume file | No | business failure, mark FAILED |
| Unsupported file format | No | validation failure before queue |
| Deterministic parse failure on scanned image | No | mark FAILED |

## Standard Retry Configuration

| Job Type | Max Attempts | Backoff Strategy |
| -------- | ------------ | ---------------- |
| resume_parse | 2 | 30s, 60s |
| embedding_generate | 2 | 15s, 30s |
| ranking_generate | 2 | 30s, 60s |
| summary_generate | 3 | 30s, 60s, 120s |
| questions_generate | 3 | 30s, 60s, 120s |
| report_generate | 2 | 30s, 60s |

After max attempts are exhausted, job status becomes `FAILED` and the error is persisted.

---

# 12. API Contract for Async Operations

ARAS V1 must expose a consistent async API contract.

## 12.1 Create Async Work

APIs that enqueue work return:

```json
{
  "success": true,
  "message": "Job accepted",
  "data": {
    "job_id": "uuid",
    "status": "QUEUED",
    "job_type": "resume_parse"
  }
}
```

HTTP status: `202 Accepted`

## 12.2 Query Job Status

New endpoint required:

```text
GET /jobs/status/{job_id}
```

Response:

```json
{
  "success": true,
  "message": "Job status fetched",
  "data": {
    "job_id": "uuid",
    "job_type": "summary_generate",
    "status": "STARTED",
    "attempts": 1,
    "progress": 60,
    "entity_type": "candidate",
    "entity_id": "uuid",
    "parent_job_id": null,
    "error_message": null,
    "created_at": "2026-06-21T10:00:00Z",
    "started_at": "2026-06-21T10:00:05Z",
    "completed_at": null,
    "result": null
  }
}
```

## 12.3 Batch Job Status

For parent jobs:

```json
{
  "success": true,
  "message": "Batch job status fetched",
  "data": {
    "job_id": "uuid",
    "job_type": "bulk_upload",
    "status": "PARTIAL",
    "total_items": 10,
    "completed_items": 8,
    "failed_items": 2,
    "progress": 80,
    "children": [
      {
        "job_id": "uuid-child-1",
        "status": "COMPLETED"
      },
      {
        "job_id": "uuid-child-2",
        "status": "FAILED"
      }
    ]
  }
}
```

---

# 13. Progress Reporting Rules

V1 progress reporting must stay simple and deterministic.

## Progress Values by Flow

| Flow | Progress Rule |
| ---- | ------------- |
| resume_parse | 0 = created, 20 = stored, 50 = text extracted, 80 = candidate saved, 100 = completed |
| bulk_upload | `(completed + failed) / total × 100` |
| ranking_generate | 20 = data loaded, 60 = scores computed, 90 = ranks persisted, 100 = completed |
| summary_generate | 30 = queued, 60 = Gemini requested, 90 = response parsed, 100 = stored |
| questions_generate | same as summary |
| report_generate | 20 = query built, 60 = file generated, 80 = uploaded, 100 = metadata stored |

Progress is stored in `result_json.progress` or an added `progress` integer column if the team chooses explicit schema support. For V1, a dedicated `progress` column is recommended for simplicity.

---

# 14. Failure Handling

## 14.1 Failure Categories

| Category | Example | User Message |
| -------- | ------- | ------------ |
| Validation failure | unsupported file type | "File could not be accepted." |
| Processing failure | corrupted PDF | "Resume could not be parsed." |
| External AI failure | Gemini timeout | "AI result delayed; fallback used." |
| Export failure | PDF render exception | "Report generation failed." |
| Infrastructure transient | Redis unavailable | "Processing delayed. Please retry shortly." |

## 14.2 Failure Recording Rules

When a task fails, the worker must:

1. Update `async_jobs.status`
2. Persist `error_code`
3. Persist `error_message` (safe, non-sensitive)
4. Write structured application log
5. Update related business entity status where applicable

### Examples

| Business Entity | Failure Update |
| --------------- | ------------- |
| resume | `processing_status = FAILED` |
| ai_summary | fallback persisted where possible |
| interview_questions | fallback persisted where possible |
| report | `status = FAILED` |

---

# 15. Security Requirements for Async Jobs

Async processing handles sensitive candidate data and must follow these controls.

## Required Controls

1. Do not place raw resume content in Celery payloads.
2. Pass only IDs and minimal metadata in task payloads.
3. Workers must fetch full data from PostgreSQL/S3 inside trusted backend network.
4. Logs must not store full resume text, JWTs, or secrets.
5. External AI prompts must include only required candidate/job context.
6. Temporary export files must be deleted after upload.
7. Download endpoints for generated files must remain authenticated.

## Safe Task Payload Example

```json
{
  "resume_id": "uuid",
  "requested_by": "uuid"
}
```

## Unsafe Task Payload Example

```json
{
  "resume_pdf_contents": "<full text>",
  "jwt": "..."
}
```

---

# 16. Observability and Logging

Every async task must emit structured logs at these lifecycle points:

```text
- job_created
- job_enqueued
- job_started
- job_retry_scheduled
- job_completed
- job_failed
```

## Required Log Fields

```json
{
  "event": "job_started",
  "job_id": "uuid",
  "celery_task_id": "string",
  "job_type": "resume_parse",
  "status": "STARTED",
  "entity_type": "resume",
  "entity_id": "uuid",
  "attempt": 1,
  "requested_by": "uuid",
  "timestamp": "ISO8601"
}
```

## Operational Metrics

| Metric | Target |
| ------ | ------ |
| Resume parse success rate | ≥ 85% on valid uploads |
| Bulk upload parent completion accuracy | 100% |
| Ranking job completion time | ≤ 5 seconds for normal job sizes |
| Summary generation fallback rate | ≤ 5% in healthy environment |
| Report generation completion | ≤ 30 seconds for standard export |

---

# 17. Worker Design

## 17.1 Worker Responsibilities

Celery workers are thin orchestration units. They must:

* Load target entity by ID
* Call service-layer logic
* Update async_jobs state
* Persist result metadata
* Handle retry and failure policies

Workers must **not** contain business rules duplicated from services.

## 17.2 Service Ownership

| Worker Task | Service Called |
| ----------- | -------------- |
| parse_resume_task | `ParsingService` |
| generate_embedding_task | `EmbeddingService` |
| generate_ranking_task | `RankingService` |
| generate_summary_task | `SummaryService` |
| generate_interview_questions_task | `InterviewQuestionService` |
| generate_report_task | `ReportService` |

This preserves Clean Architecture and avoids business logic drift.

---

# 18. Concurrency Rules

To avoid duplicate work and race conditions in V1:

1. One active ranking job per `job_id` at a time.
2. One active summary job per `(candidate_id, job_id)` at a time.
3. One active interview question job per `(candidate_id, job_id)` at a time.
4. One active parse job per `resume_id` at a time.

## Locking Strategy

V1 uses application-level checks backed by PostgreSQL unique constraints where possible.

Examples:

* `candidate_scores` unique on `(candidate_id, job_id)`
* `ai_summaries` unique on `(candidate_id, job_id)`
* `interview_questions` unique on `(candidate_id, job_id)`
* `async_jobs` partial uniqueness enforced at service level for active states

If an equivalent active job already exists, the API returns the existing `job_id` instead of creating a duplicate.

---

# 19. Frontend Interaction Model

The frontend must treat async flows explicitly.

## Required UI States

| State | UI Behavior |
| ----- | ----------- |
| QUEUED | Show pending indicator |
| STARTED | Show progress bar/spinner |
| RETRYING | Show "Retrying" with non-blocking notice |
| COMPLETED | Refresh related data view |
| FAILED | Show retry action and safe error message |
| PARTIAL | Show completed/failed counts for batch |

## Polling Strategy

V1 uses polling, not websockets.

| Operation | Poll Interval |
| --------- | ------------- |
| single resume parse | 2 seconds |
| bulk upload | 3 seconds |
| ranking generation | 2 seconds |
| summary/questions | 2 seconds |
| report generation | 3 seconds |

Polling stops when state is `COMPLETED`, `FAILED`, or `PARTIAL`.

---

# 20. DevOps and Deployment Requirements

## Celery Deployment Units

ARAS deployment must include:

```text
- FastAPI container
- Celery worker container
- Celery beat container (optional in V1; only if scheduled cleanup is implemented)
- Redis container
- PostgreSQL container
- Nginx container
```

## Initial Worker Configuration

```text
celery -A app.tasks.worker worker --queues default,ai,exports --concurrency=4
```

Recommended initial split:

* 1 process handling `default`
* 2 processes handling `ai`
* 1 process handling `exports`

For Docker Compose V1, a single worker container with routed queues is acceptable.

---

# 21. Cleanup Policies

## Operational Cleanup

To keep V1 maintainable:

1. Async job records are retained in PostgreSQL for at least 90 days.
2. Temporary local export files must be deleted immediately after S3 upload.
3. Failed jobs are not auto-purged in V1.
4. Old Redis queue metadata may expire naturally; Redis is not the source of truth.

Optional scheduled cleanup may be added later through Celery Beat, but it is not required for V1 release.

---

# 22. Testing Requirements

## Unit Tests

```text
- Task dispatch creates async_jobs record
- Worker updates status transitions correctly
- Retryable failures schedule retry
- Non-retryable failures mark FAILED
- Parent batch status aggregation is correct
```

## Integration Tests

```text
- Resume upload returns 202 + job_id
- GET /jobs/status/{job_id} returns live status
- Bulk upload shows PARTIAL when one child fails
- Summary generation stores fallback on Gemini failure
- Report job uploads file and exposes download metadata
```

## Performance Tests

```text
- Queue 20 resume parse jobs and confirm no API timeout
- Generate ranking for 100 candidates and verify completion target
- Export standard CSV and verify job completion under target
```

---

# 23. Roadmap Alignment

This async architecture is mapped to the approved 40-day roadmap.

| Sprint | Days | Async Deliverables |
| ------ | ---- | ------------------ |
| Sprint 1 | 6–10 | Redis, Celery, worker bootstrap, async_jobs migration |
| Sprint 3 | 16–20 | Resume upload async dispatch + status API |
| Sprint 4 | 21–25 | Parse pipeline + embedding chain |
| Sprint 5 | 26–30 | Ranking async execution |
| Sprint 6 | 31–35 | Summary + interview question async flows with fallback |
| Sprint 7 | 36–38 | Report generation async flow |
| Sprint 8 | 39–40 | End-to-end async regression + deployment validation |

This sequencing stays within the approved V1 plan and does not require additional roles or infrastructure.

---

# 24. Required Specification Updates

The following existing project documents must be updated to align with this architecture:

## 09_API_Specification.md

Add:

```text
GET /jobs/status/{job_id}
GET /jobs/status/{job_id}/children (optional)
202 Accepted responses for async endpoints
```

## 08_Database_Design.md

Add:

```text
async_jobs table
Optional progress column
is_fallback column in ai_summaries
```

## 07_LLD.md

Expand:

```text
backend/app/tasks/
Job status service
Queue routing configuration
```

---

# 25. Conclusion

This async job architecture provides a production-ready, V1-realistic background processing model for ARAS using the already approved technology stack.

It avoids premature complexity, keeps PostgreSQL as the durable source of truth, uses Celery and Redis in a controlled way, and gives the frontend a clear status model for long-running operations. The design is achievable within the existing 40-day roadmap and directly supports resume processing, ranking, AI generation, and exports without changing ARAS into a distributed system.

