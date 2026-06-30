# AI Recruitment Automation System (ARAS)

# AI Validation Plan

Document Number: 13

Version: 1.0

Date: June 2026

Document Owner: AI Lead + QA Engineer

Document Status: Approved for Implementation

Scope: ARAS Version 1.0 — No custom ML training. Uses existing sentence-transformers/all-MiniLM-L6-v2 and Gemini 2.5 Flash API only.

---

# 1. Purpose

This document defines the validation strategy for all AI components in ARAS Version 1.

It answers three critical questions for each AI module:

1. How do we confirm it produces correct output?
2. How do we detect when it produces incorrect output?
3. How do we gracefully handle failure?

Validation here does not mean model training or benchmark research. It means **functional correctness testing** — asserting that the integration between ARAS logic, sentence-transformers, and the Gemini API produces outputs that meet the acceptance criteria defined in the SRS and AI_Model.md.

---

# 2. AI Modules in Scope

| Module ID | Module Name                   | Technology              | Validation Owner |
| --------- | ----------------------------- | ----------------------- | ---------------- |
| AIV-01    | Resume Parsing Engine         | PyMuPDF, pdfplumber, re | AI Lead + QA     |
| AIV-02    | Skill Extraction Engine       | Dictionary + NER        | AI Lead          |
| AIV-03    | Job Description Analysis      | Dictionary + regex      | AI Lead          |
| AIV-04    | Embedding Engine              | all-MiniLM-L6-v2        | AI Lead          |
| AIV-05    | Candidate Matching Engine     | Cosine similarity       | AI Lead + QA     |
| AIV-06    | Candidate Ranking Engine      | Weighted formula        | QA Engineer      |
| AIV-07    | AI Summary Engine             | Gemini 2.5 Flash        | AI Lead + QA     |
| AIV-08    | Skill Gap Analysis Engine     | Set difference          | QA Engineer      |
| AIV-09    | Interview Question Generator  | Gemini 2.5 Flash        | AI Lead + QA     |

---

# 3. Validation Strategy Overview

ARAS uses a four-tier validation approach:

```text
Tier 1: Unit Validation
        ↓
Tier 2: Integration Validation
        ↓
Tier 3: End-to-End Scenario Validation
        ↓
Tier 4: Ongoing Runtime Monitoring
```

All tiers are lightweight and executable within the 40-day roadmap. No custom datasets are built from scratch. Validation is based on handcrafted test fixtures created by the QA Engineer during Sprint 4 (Days 21–25).

---

# 4. Test Fixture Specification

## 4.1 Resume Fixtures

The QA Engineer must prepare a minimum test corpus of **20 synthetic resumes** covering the following variation dimensions:

| Fixture Set | Format | Complexity | Expected Outcome         |
| ----------- | ------ | ---------- | ------------------------ |
| FX-R-01     | PDF    | Simple     | All fields extracted     |
| FX-R-02     | PDF    | Multi-page | All fields extracted     |
| FX-R-03     | DOCX   | Simple     | All fields extracted     |
| FX-R-04     | DOCX   | Multi-page | All fields extracted     |
| FX-R-05     | PDF    | Dense skills section | Skills ≥ 80% extracted |
| FX-R-06     | PDF    | No education section | Graceful null            |
| FX-R-07     | PDF    | Scanned image-only   | parsing_status = FAILED  |
| FX-R-08     | PDF    | Corrupted            | parsing_status = FAILED  |
| FX-R-09     | PDF    | Minimal (1-page, 5 fields) | Partial extraction |
| FX-R-10     | PDF    | Standard Indian format | All fields extracted   |

Each fixture must include a **ground truth JSON** file with expected values for: name, email, phone, skills, education, experience_years.

Fixtures are stored in:

```text
tests/fixtures/resumes/
tests/fixtures/ground_truth/
```

## 4.2 Job Description Fixtures

Minimum **10 job description fixtures** covering:

| Fixture ID | Role Type          | Expected Required Skills Count |
| ---------- | ------------------ | ------------------------------ |
| FX-JD-01   | Backend Developer  | ≥ 5                            |
| FX-JD-02   | Frontend Developer | ≥ 4                            |
| FX-JD-03   | Data Scientist     | ≥ 6                            |
| FX-JD-04   | DevOps Engineer    | ≥ 5                            |
| FX-JD-05   | Full Stack         | ≥ 8                            |
| FX-JD-06   | Minimal JD         | ≥ 2 (graceful extraction)      |
| FX-JD-07   | Verbose JD         | Correct deduplication          |
| FX-JD-08   | Non-technical role | ≥ 2 soft skills                |
| FX-JD-09   | Entry-level role   | Experience = 0 accepted        |
| FX-JD-10   | Senior role        | Experience ≥ 5                 |

## 4.3 Ranking Scenario Fixtures

Minimum **5 ranking scenarios** where ground truth rankings are known in advance:

| Scenario ID | Candidates | Job       | Expected Top Candidate               |
| ----------- | ---------- | --------- | ------------------------------------- |
| FX-RK-01    | 5          | Backend   | Python + FastAPI + Docker candidate  |
| FX-RK-02    | 5          | Frontend  | React + TypeScript candidate         |
| FX-RK-03    | 5          | Data Sci  | Python + ML + SQL candidate          |
| FX-RK-04    | 10         | Full Stack| Both frontend and backend skills     |
| FX-RK-05    | 3 identical| Backend   | Tie handling — stable sort by name   |

---

# 5. Module Validation: AIV-01 — Resume Parsing Engine

## Acceptance Criteria

| Field          | Minimum Extraction Rate |
| -------------- | ----------------------- |
| Name           | 90%                     |
| Email          | 95%                     |
| Phone          | 80%                     |
| Skills         | 80%                     |
| Education      | 75%                     |
| Experience     | 75%                     |

Extraction Rate = (Correctly Extracted / Total Fixtures) × 100

Partial extraction (missing phone, missing education) is **not a failure** provided parsing_status is set accurately.

## Failure Classification

| Status         | Condition                                            |
| -------------- | ---------------------------------------------------- |
| `COMPLETED`    | ≥ 3 fields extracted including name and email        |
| `PARTIAL`      | name or email extracted but ≥ 2 other fields missing |
| `FAILED`       | Cannot extract text (scanned, corrupted, empty)      |

## Test Cases

```text
TC-P-01: Parse valid PDF — verify name, email, phone match ground truth
TC-P-02: Parse valid DOCX — verify skills list not empty
TC-P-03: Parse scanned PDF — verify parsing_status = FAILED, no exception raised
TC-P-04: Parse corrupted file — verify parsing_status = FAILED, error logged
TC-P-05: Parse resume with no education section — verify education = null, status = PARTIAL
TC-P-06: Parse bulk upload of 10 resumes — verify all return within 60 seconds
TC-P-07: Parse resume with 20+ skills — verify all skills captured
TC-P-08: Parse resume with non-English characters in name — verify graceful handling
```

## Validation Tool

```python
# tests/unit/ai/test_resume_parser.py
def test_parse_valid_pdf(fixture_path, ground_truth):
    result = ResumeParser().parse(fixture_path)
    assert result.email == ground_truth["email"]
    assert result.name == ground_truth["name"]
    assert result.parsing_status in ["COMPLETED", "PARTIAL"]

def test_parse_corrupted_pdf(corrupted_fixture_path):
    result = ResumeParser().parse(corrupted_fixture_path)
    assert result.parsing_status == "FAILED"
    # Must not raise exception — failures are data, not exceptions
```

---

# 6. Module Validation: AIV-02 — Skill Extraction Engine

## Acceptance Criteria

- Skill extraction precision: ≥ 85% (no false positives — "Python" must not be confused with "Pythonista")
- Skill extraction recall: ≥ 80% (must not miss common skills listed in master dictionary)
- Case-insensitive matching: 100% required
- Deduplication: no duplicate skills in output list

## Test Cases

```text
TC-SE-01: Resume with known skills in master dict — verify all extracted
TC-SE-02: Resume with skill aliases ("JS" → "JavaScript") — verify normalization
TC-SE-03: Resume with skills in a comma-separated sentence — verify split and match
TC-SE-04: Resume with no skills section — verify empty list returned, no exception
TC-SE-05: JD with preferred vs required section — verify both extracted separately
TC-SE-06: Duplicate skill in resume — verify output contains only one instance
TC-SE-07: Skill with version suffix ("Python 3.10") — verify "Python" is extracted
```

## Master Skills Dictionary Coverage

The master skills dictionary (stored in `ai_engine/extractors/skills_master.json`) must contain a minimum of:

| Category      | Minimum Skills |
| ------------- | -------------- |
| Programming   | 20             |
| Frontend      | 15             |
| Backend       | 15             |
| Cloud         | 10             |
| Databases     | 10             |
| DevOps/Tools  | 10             |
| Soft Skills   | 10             |

Total minimum: **90 skills** before launch.

---

# 7. Module Validation: AIV-04 — Embedding Engine

## Acceptance Criteria

- Embedding dimension: exactly 384
- Embedding type: float32 numpy array
- Embedding generation time per document: ≤ 1 second (from AI_Model.md)
- Model loaded once at application startup (no per-request model reload)

## Test Cases

```text
TC-E-01: Generate embedding from candidate profile JSON — verify shape == (384,)
TC-E-02: Generate embedding from job description text — verify shape == (384,)
TC-E-03: Generate embedding from empty string — verify graceful handling, log warning
TC-E-04: Generate embeddings for same text twice — verify output is identical (deterministic)
TC-E-05: Generate embedding — verify type is float32
TC-E-06: Measure embedding time for 10 consecutive requests — verify p95 ≤ 1 second
```

## Vector Storage Validation

After embedding storage:

```text
TC-E-07: Store embedding in pgvector — verify retrieval matches original vector
TC-E-08: Query nearest neighbors for a known job vector — verify top candidate is in expected set
TC-E-09: ivfflat index present — verify query uses index (via EXPLAIN ANALYZE)
```

---

# 8. Module Validation: AIV-05 — Candidate Matching Engine

## Acceptance Criteria

The weighted scoring formula from AI_Model.md must be validated:

```text
Final Score = (0.35 × Semantic) + (0.25 × Skill) + (0.20 × Experience) + (0.10 × Education) + (0.10 × AI Score)
```

All component scores must be in range [0, 100]. Final score must be in range [0, 100]. Scores must be deterministic for the same inputs.

## Test Cases

```text
TC-M-01: Perfect match candidate (all required skills, exact experience) — verify final_score ≥ 90
TC-M-02: Zero match candidate (no overlapping skills) — verify final_score ≤ 20
TC-M-03: Partial match candidate (50% skills, 1yr short on experience) — verify 40 ≤ score ≤ 70
TC-M-04: Verify formula weights sum to 1.0 — unit test on constant definitions
TC-M-05: Skill score calculation — 5/5 skills matched → skill_score = 100
TC-M-06: Skill score calculation — 3/5 skills matched → skill_score = 60
TC-M-07: Experience score — candidate has 3 years, job requires 2 → experience_score = 100
TC-M-08: Experience score — candidate has 1 year, job requires 3 → experience_score ≤ 50
TC-M-09: Education score — exact match → 100, one-level below → 70, no match → 30
TC-M-10: Semantic score range — verify always in [0, 100] after cosine-to-percentage conversion
```

## Score Normalization Contract

Cosine similarity returns [-1, 1]. The matching engine must normalize to [0, 100]:

```python
# Required implementation contract
semantic_score = max(0.0, cosine_similarity) * 100
```

---

# 9. Module Validation: AIV-06 — Candidate Ranking Engine

## Acceptance Criteria

- Ranking is a strict descending sort by final_score
- Tied scores produce a stable sort (deterministic rank assignment using candidate UUID as tiebreaker)
- Ranks are 1-indexed (1 = highest score)
- Recommendation categories are assigned based on defined thresholds

## Recommendation Category Thresholds

| Score Range | Category            |
| ----------- | ------------------- |
| 85 – 100    | Highly Recommended  |
| 65 – 84     | Recommended         |
| 45 – 64     | Consider            |
| 0 – 44      | Rejected            |

These thresholds are defined as constants in `ai_engine/ranking/thresholds.py` and must not be hardcoded inline.

## Test Cases

```text
TC-RK-01: Rank 5 candidates with known scores — verify order matches expected
TC-RK-02: Two candidates with identical score — verify stable sort, no crash
TC-RK-03: Single candidate — verify rank = 1
TC-RK-04: Score 87 → category = Highly Recommended
TC-RK-05: Score 70 → category = Recommended
TC-RK-06: Score 50 → category = Consider
TC-RK-07: Score 30 → category = Rejected
TC-RK-08: Ranking API returns results sorted by rank ascending
TC-RK-09: Re-running ranking for same job after adding new candidate — existing ranks updated correctly
```

---

# 10. Module Validation: AIV-07 — AI Summary Engine (Gemini)

## Acceptance Criteria

- Gemini API call must complete within 10 seconds (AI_Model.md target)
- Response must be parseable into the defined JSON schema
- On API failure, fallback template must activate (per Risk R4 mitigation)
- Generated summary must never be stored if it contains an error marker

## Expected Output Schema

```json
{
  "strengths": ["string", "..."],
  "weaknesses": ["string", "..."],
  "recommendation": "Interview Round 1 | Interview Round 2 | Rejected",
  "summary_text": "string (max 300 words)"
}
```

## Prompt Validation Rules

The Gemini prompt must be version-controlled in:

```text
ai_engine/summarization/prompts/summary_v1.txt
```

The prompt must include:

1. System role instruction: "You are a professional recruiter assistant."
2. Candidate profile data (name, skills, experience, education)
3. Job requirements (required skills, experience, education)
4. Output format instruction — JSON only, no markdown
5. Maximum output token limit: 500

## Test Cases

```text
TC-S-01: Call summary engine with complete candidate + job data — verify schema-valid JSON returned
TC-S-02: Parse JSON response — verify "strengths" is a list, "recommendation" is a string
TC-S-03: Simulate Gemini timeout (mock) — verify fallback template returned, no exception raised
TC-S-04: Simulate Gemini 429 rate limit (mock) — verify retry with exponential backoff (max 3 retries)
TC-S-05: Simulate Gemini 500 error (mock) — verify fallback template returned, error logged
TC-S-06: Verify summary stored only if valid — invalid JSON response must not persist
TC-S-07: Re-request summary when already cached — verify Redis cache hit, no Gemini call
```

## Fallback Template Contract

When Gemini is unavailable, the system returns a deterministic template-based summary:

```json
{
  "strengths": ["<skills that match job requirements>"],
  "weaknesses": ["<skills in job requirements missing from candidate>"],
  "recommendation": "Consider",
  "summary_text": "AI summary unavailable. Score-based evaluation: candidate matches X of Y required skills.",
  "is_fallback": true
}
```

`is_fallback: true` must be stored in `ai_summaries.is_fallback` column (new column — add to migration).

---

# 11. Module Validation: AIV-08 — Skill Gap Analysis Engine

## Acceptance Criteria

- Skill gap = set difference: required_skills − candidate_skills
- Matching must be case-insensitive
- Output must not include skills the candidate already possesses
- Empty gap (perfect match) is a valid output: `missing_skills: []`

## Test Cases

```text
TC-SG-01: required=[Python, Docker, AWS], candidate=[Python, Docker] → missing=[AWS]
TC-SG-02: required=[Python, FastAPI], candidate=[Python, FastAPI] → missing=[]
TC-SG-03: required=[python], candidate=[Python] → missing=[] (case-insensitive)
TC-SG-04: required=[], candidate=[Python] → missing=[]
TC-SG-05: required=[Python], candidate=[] → missing=[Python]
TC-SG-06: result includes match_percentage = (matched / required) × 100
```

---

# 12. Module Validation: AIV-09 — Interview Question Generator (Gemini)

## Acceptance Criteria

- Response must contain all three question categories: technical, coding, behavioral
- Each category must have a minimum of 3 questions
- Questions must be specific to candidate skills and job requirements (not generic)
- On API failure, fallback question bank activates

## Expected Output Schema

```json
{
  "technical": ["string", "..."],
  "coding": ["string", "..."],
  "behavioral": ["string", "..."]
}
```

## Test Cases

```text
TC-IQ-01: Generate questions for Python + FastAPI role — verify technical questions mention Python/FastAPI
TC-IQ-02: Verify each category has ≥ 3 questions
TC-IQ-03: Simulate Gemini failure — verify fallback question bank returns pre-defined questions
TC-IQ-04: Questions already generated for same candidate+job pair — verify cache hit used
TC-IQ-05: Parse Gemini response — verify valid JSON, all three keys present
```

## Fallback Question Bank

Stored in: `ai_engine/interview_generation/fallback_questions.json`

Structure:

```json
{
  "technical": [
    "Explain the difference between SQL and NoSQL databases.",
    "What is a REST API and how does it work?",
    "Describe how indexing improves database performance."
  ],
  "coding": [
    "Write a function to reverse a string.",
    "Implement a basic JWT authentication flow.",
    "Write a SQL query to find the top 5 candidates by score."
  ],
  "behavioral": [
    "Describe a time you solved a complex technical problem.",
    "How do you handle tight deadlines?",
    "Tell me about a project you are most proud of."
  ]
}
```

---

# 13. Validation Schedule (Roadmap Alignment)

| Sprint     | Days    | Validation Activity                                            | Owner          |
| ---------- | ------- | -------------------------------------------------------------- | -------------- |
| Sprint 0   | 1–5     | Create test fixture directory, fixture schema, ground truth template | QA Engineer |
| Sprint 4   | 21–25   | Create 20 resume fixtures and 10 JD fixtures with ground truth | QA Engineer   |
| Sprint 4   | 21–25   | Write and run TC-P-01 to TC-P-08, TC-SE-01 to TC-SE-07        | QA + AI Lead   |
| Sprint 5   | 26–30   | Write and run TC-E-01 to TC-E-09, TC-M-01 to TC-M-10, TC-RK-01 to TC-RK-09 | QA + AI |
| Sprint 6   | 31–35   | Write and run TC-S-01 to TC-S-07, TC-SG-01 to TC-SG-06, TC-IQ-01 to TC-IQ-05 | QA + AI |
| Sprint 7   | 36–38   | Full end-to-end scenario validation (FX-RK-01 to FX-RK-05)   | All Team       |
| Sprint 8   | 39–40   | Regression run, validation report, sign-off                   | QA Engineer    |

---

# 14. End-to-End Validation Scenarios

These scenarios test the full AI pipeline from upload to ranking.

## Scenario E2E-01: Standard Ranking Flow

```text
Given: 5 resumes uploaded for "Backend Developer" job
When:  ranking is triggered
Then:
  - All 5 candidates are ranked (rank 1 to 5)
  - The candidate with Python + FastAPI + Docker has rank 1 or 2
  - All final_scores are in range [0, 100]
  - candidate_scores table has 5 rows for this job_id
  - No AI call errors in logs
```

## Scenario E2E-02: Bulk Upload + Parse

```text
Given: 20 resumes uploaded at once for a job
When:  Celery tasks complete
Then:
  - At least 17 of 20 resumes have parsing_status = COMPLETED or PARTIAL
  - All 20 have a corresponding candidate record
  - Embeddings exist for all COMPLETED/PARTIAL candidates
  - Bulk operation completes within 3 minutes
```

## Scenario E2E-03: AI Summary + Fallback

```text
Given: Gemini API is disabled (environment variable mock)
When:  Summary is requested for a candidate
Then:
  - Response contains fallback summary with is_fallback = true
  - UI displays summary (no broken state)
  - No 500 error returned to frontend
```

## Scenario E2E-04: Ranking Consistency

```text
Given: Ranking generated for a job with 10 candidates
When:  Ranking is re-generated without any new resumes
Then:
  - All ranks remain identical to original run
  - No score variance (deterministic)
```

---

# 15. Quality Gates

Before implementation of each AI module is merged into the `develop` branch, the following gates must pass:

| Gate ID | Requirement                                   | Enforced By          |
| ------- | --------------------------------------------- | -------------------- |
| QG-01   | All unit tests for module pass                | GitHub Actions CI    |
| QG-02   | No exception raised on any fixture            | Pytest               |
| QG-03   | Fallback mechanism tested and verified        | QA Engineer          |
| QG-04   | Performance target met (AI_Model.md targets)  | Manual timing test   |
| QG-05   | Output schema validated against Pydantic model| Pydantic schema test |

---

# 16. Runtime Monitoring (Post-Deployment)

For V1, monitoring is lightweight and implemented via structured logging. No external APM tool is required.

## Metrics to Log

Every AI operation must emit a structured log entry:

```json
{
  "event": "ai_operation",
  "module": "resume_parser | embedding | matching | summary | questions",
  "status": "success | failed | fallback",
  "duration_ms": 1234,
  "resume_id": "uuid",
  "job_id": "uuid",
  "timestamp": "ISO8601"
}
```

## Thresholds to Alert

| Metric                         | Warning Threshold | Critical Threshold |
| ------------------------------ | ----------------- | ------------------ |
| Parsing FAILED rate            | > 10%             | > 25%              |
| Gemini fallback activation rate| > 5%              | > 20%              |
| Embedding generation time      | > 2s              | > 5s               |
| Summary generation time        | > 15s             | > 30s              |

Alerts are written to `logs/ai_alerts.log` and reported during daily standup.

---

# 17. Validation Sign-Off Checklist

Before final deployment (Day 38), the AI Lead and QA Engineer must jointly confirm:

```text
[ ] All 9 AI modules have passed unit tests
[ ] All 5 ranking scenario fixtures produce correct top-ranked candidates
[ ] Fallback tested for both Gemini modules (AIV-07, AIV-09)
[ ] Performance targets from AI_Model.md verified against fixtures
[ ] Parsing extraction rate ≥ 80% on 20 resume fixture corpus
[ ] No AI module raises unhandled exceptions on any test fixture
[ ] Structured AI logs active in production Docker container
[ ] is_fallback column added to ai_summaries table via Alembic migration
[ ] All quality gates (QG-01 to QG-05) passed
[ ] End-to-end scenarios E2E-01 to E2E-04 passed
```

Both the AI Lead and QA Engineer must sign this checklist in the Sprint 8 review.

---

# 18. Document Relationships

| Document              | Relationship                                                        |
| --------------------- | ------------------------------------------------------------------- |
| AI_Model.md           | Source of truth for modules, scoring formula, and performance targets |
| 08_Database_Design.md | Defines tables: candidate_scores, ai_summaries, interview_questions |
| 09_API_Specification.md | API contracts for AI endpoints validated here                     |
| 12_Risk_Assessment.md | R3 (parsing accuracy) and R4 (API failure) mitigated by this plan  |
| 14_Async_Job_Architecture.md | Celery tasks that execute these AI modules                  |

---

# 19. Conclusion

This validation plan provides a complete, implementation-safe framework for verifying all AI components in ARAS V1 without requiring custom ML training, external datasets, or research-grade evaluation infrastructure.

All validation activities fit within the existing 40-day roadmap with existing team roles. The QA Engineer and AI Lead own joint accountability for every quality gate before production merge.

