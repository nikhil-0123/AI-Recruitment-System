# AI Recruitment Automation System (ARAS)

# Database Design Document

Version: 1.0

Date: June 2026

Database: PostgreSQL 16 + pgvector

Document Status: Approved

---

# 1. Purpose

This document defines:

* Database Architecture
* Table Structures
* Relationships
* Constraints
* Indexes
* Data Types
* Future Scalability Design

The database is designed to support:

* Authentication
* Resume Management
* Candidate Management
* Job Management
* AI Matching
* Candidate Ranking
* Reporting
* Analytics

---

# 2. Database Technology

Database Engine:

PostgreSQL 16

Extensions:

```sql
uuid-ossp
pgvector
```

Reason:

* ACID Compliance
* Scalability
* Reliability
* Vector Search Support

---

# 3. High Level ER Diagram

```text
Users
  |
  | 1:N
  |
Jobs
  |
  | 1:N
  |
CandidateScores
  |
  | N:1
  |
Candidates
  |
  | 1:N
  |
Resumes

Candidates
  |
  | M:N
  |
Skills

Jobs
  |
  | M:N
  |
Skills

Candidates
  |
  | 1:N
  |
AI_Summaries

Candidates
  |
  | 1:N
  |
Interview_Questions
```

---

# 4. Database Tables

Total Tables:

```text
users
jobs
resumes
candidates
skills
candidate_skills
job_skills
candidate_scores
candidate_embeddings
job_embeddings
ai_summaries
interview_questions
reports
audit_logs
```

---

# 5. Users Table

Purpose:

System users.

---

Table Name

```sql
users
```

Columns

| Column        | Type         | Constraint    |
| ------------- | ------------ | ------------- |
| id            | UUID         | PK            |
| name          | VARCHAR(100) | NOT NULL      |
| email         | VARCHAR(255) | UNIQUE        |
| password_hash | TEXT         | NOT NULL      |
| role          | VARCHAR(30)  | NOT NULL      |
| is_active     | BOOLEAN      | DEFAULT TRUE  |
| created_at    | TIMESTAMP    | DEFAULT NOW() |
| updated_at    | TIMESTAMP    | DEFAULT NOW() |

---

Indexes

```sql
CREATE UNIQUE INDEX idx_users_email
ON users(email);
```

---

# 6. Jobs Table

Purpose:

Store job descriptions.

---

Table Name

```sql
jobs
```

Columns

| Column              | Type         |
| ------------------- | ------------ |
| id                  | UUID         |
| recruiter_id        | UUID         |
| title               | VARCHAR(255) |
| description         | TEXT         |
| experience_required | INTEGER      |
| education_required  | VARCHAR(255) |
| status              | VARCHAR(50)  |
| created_at          | TIMESTAMP    |
| updated_at          | TIMESTAMP    |

---

Relationships

```text
User (1)
   |
   |
   V
Jobs (N)
```

---

# 7. Candidates Table

Purpose:

Store candidate profiles.

---

Table Name

```sql
candidates
```

Columns

| Column           | Type         |
| ---------------- | ------------ |
| id               | UUID         |
| full_name        | VARCHAR(255) |
| email            | VARCHAR(255) |
| phone            | VARCHAR(20)  |
| linkedin_url     | TEXT         |
| experience_years | NUMERIC(4,1) |
| education        | TEXT         |
| created_at       | TIMESTAMP    |

---

Indexes

```sql
CREATE INDEX idx_candidate_email
ON candidates(email);
```

---

# 8. Resumes Table

Purpose:

Store uploaded resumes.

---

Table Name

```sql
resumes
```

Columns

| Column         | Type        |
| -------------- | ----------- |
| id             | UUID        |
| candidate_id   | UUID        |
| file_name      | TEXT        |
| file_url       | TEXT        |
| file_type      | VARCHAR(20) |
| file_size      | BIGINT      |
| parsing_status | VARCHAR(50) |
| uploaded_at    | TIMESTAMP   |

---

Relationships

```text
Candidate (1)
      |
      |
      V
Resume (N)
```

---

# 9. Skills Table

Purpose:

Master skill repository.

---

Table Name

```sql
skills
```

Columns

| Column     | Type         |
| ---------- | ------------ |
| id         | UUID         |
| skill_name | VARCHAR(100) |
| category   | VARCHAR(100) |

---

Examples

```text
Python
FastAPI
React
Docker
AWS
PostgreSQL
Machine Learning
```

---

# 10. Candidate Skills Table

Purpose:

Many-to-many mapping.

---

Table Name

```sql
candidate_skills
```

Columns

| Column            | Type         |
| ----------------- | ------------ |
| id                | UUID         |
| candidate_id      | UUID         |
| skill_id          | UUID         |
| proficiency_score | NUMERIC(5,2) |

---

Relationship

```text
Candidates M:N Skills
```

---

# 11. Job Skills Table

Purpose:

Required skills per job.

---

Table Name

```sql
job_skills
```

Columns

| Column            | Type         |
| ----------------- | ------------ |
| id                | UUID         |
| job_id            | UUID         |
| skill_id          | UUID         |
| importance_weight | NUMERIC(5,2) |

---

Relationship

```text
Jobs M:N Skills
```

---

# 12. Candidate Scores Table

Purpose:

Store ranking calculations.

---

Table Name

```sql
candidate_scores
```

Columns

| Column           | Type         |
| ---------------- | ------------ |
| id               | UUID         |
| candidate_id     | UUID         |
| job_id           | UUID         |
| skill_score      | NUMERIC(5,2) |
| experience_score | NUMERIC(5,2) |
| education_score  | NUMERIC(5,2) |
| semantic_score   | NUMERIC(5,2) |
| ai_score         | NUMERIC(5,2) |
| final_score      | NUMERIC(5,2) |
| rank_position    | INTEGER      |
| created_at       | TIMESTAMP    |

---

# 13. Candidate Embeddings Table

Purpose:

Store vector embeddings.

---

Table Name

```sql
candidate_embeddings
```

Columns

| Column       | Type         |
| ------------ | ------------ |
| id           | UUID         |
| candidate_id | UUID         |
| embedding    | VECTOR(384)  |
| model_name   | VARCHAR(100) |
| created_at   | TIMESTAMP    |

---

Vector Index

```sql
CREATE INDEX idx_candidate_vector
ON candidate_embeddings
USING ivfflat (embedding vector_cosine_ops);
```

---

# 14. Job Embeddings Table

Purpose:

Store job vectors.

---

Table Name

```sql
job_embeddings
```

Columns

| Column     | Type         |
| ---------- | ------------ |
| id         | UUID         |
| job_id     | UUID         |
| embedding  | VECTOR(384)  |
| model_name | VARCHAR(100) |

---

# 15. AI Summaries Table

Purpose:

Store AI-generated summaries.

---

Table Name

```sql
ai_summaries
```

Columns

| Column         | Type      |
| -------------- | --------- |
| id             | UUID      |
| candidate_id   | UUID      |
| summary        | TEXT      |
| strengths      | JSONB     |
| weaknesses     | JSONB     |
| recommendation | TEXT      |
| created_at     | TIMESTAMP |

---

# 16. Interview Questions Table

Purpose:

Store AI-generated interview questions.

---

Table Name

```sql
interview_questions
```

Columns

| Column        | Type        |
| ------------- | ----------- |
| id            | UUID        |
| candidate_id  | UUID        |
| job_id        | UUID        |
| question_type | VARCHAR(50) |
| question_text | TEXT        |
| created_at    | TIMESTAMP   |

---

Question Types

```text
Technical
Coding
Behavioral
```

---

# 17. Reports Table

Purpose:

Store generated reports.

---

Table Name

```sql
reports
```

Columns

| Column       | Type        |
| ------------ | ----------- |
| id           | UUID        |
| recruiter_id | UUID        |
| report_type  | VARCHAR(50) |
| file_url     | TEXT        |
| generated_at | TIMESTAMP   |

---

# 18. Audit Logs Table

Purpose:

Security auditing.

---

Table Name

```sql
audit_logs
```

Columns

| Column      | Type         |
| ----------- | ------------ |
| id          | UUID         |
| user_id     | UUID         |
| action      | VARCHAR(255) |
| entity_type | VARCHAR(100) |
| entity_id   | UUID         |
| timestamp   | TIMESTAMP    |

---

Examples

```text
LOGIN

CREATE_JOB

UPLOAD_RESUME

GENERATE_REPORT
```

---

# 19. Foreign Key Relationships

```sql
jobs.recruiter_id
→ users.id

resumes.candidate_id
→ candidates.id

candidate_skills.candidate_id
→ candidates.id

candidate_skills.skill_id
→ skills.id

job_skills.job_id
→ jobs.id

job_skills.skill_id
→ skills.id

candidate_scores.candidate_id
→ candidates.id

candidate_scores.job_id
→ jobs.id

candidate_embeddings.candidate_id
→ candidates.id

job_embeddings.job_id
→ jobs.id

reports.recruiter_id
→ users.id
```

---

# 20. Performance Optimization

Indexes

```sql
users.email

candidates.email

candidate_scores.final_score

jobs.title

skills.skill_name
```

Vector Search Index

```sql
ivfflat
```

Caching Layer

```text
Redis
```

Used For:

* Dashboard Metrics
* Rankings
* AI Summaries

---

# 21. Backup Strategy

Daily Backup

```text
02:00 AM UTC
```

Retention

```text
30 Days
```

Storage

```text
AWS S3
```

---

# 22. Future Tables (Version 2)

```text
notifications

interview_schedules

email_templates

candidate_feedback

recruiter_copilot_logs

organization_settings

billing

subscriptions
```

---

# 23. Database Design Summary

| Area            | Count |
| --------------- | ----- |
| Core Tables     | 14    |
| Relationships   | 20+   |
| Vector Tables   | 2     |
| AI Tables       | 2     |
| Security Tables | 1     |

The database design supports scalable recruitment workflows, semantic candidate search, AI-powered evaluation, and future SaaS expansion while maintaining high performance and data integrity.
