# AI Recruitment Automation System (ARAS)

# Low Level Design (LLD)

Version: 1.0

Date: June 2026

Project: AI Recruitment Automation System

Document Status: Development Blueprint

---

# 1. Purpose

This document provides detailed implementation-level design for the AI Recruitment Automation System.

It defines:

* Repository Structure
* Module Design
* Database Entities
* Service Layer Design
* API Layer Design
* AI Processing Flow
* Frontend Architecture
* Background Jobs
* Security Components

This document serves as the primary reference during development.

---

# 2. Complete Repository Structure

```text
AI-Recruitment-System/

├── backend/
├── frontend/
├── ai_engine/
├── deployment/
├── docs/
├── tests/
└── scripts/
```

---

# 3. Backend Structure

```text
backend/

├── app/
│
├── api/
│   ├── auth/
│   ├── users/
│   ├── jobs/
│   ├── resumes/
│   ├── candidates/
│   ├── rankings/
│   ├── reports/
│   └── analytics/
│
├── core/
│   ├── config.py
│   ├── security.py
│   ├── logging.py
│   └── exceptions.py
│
├── db/
│   ├── base.py
│   ├── session.py
│   └── migrations/
│
├── models/
│
├── schemas/
│
├── repositories/
│
├── services/
│
├── tasks/
│
├── utils/
│
└── main.py
```

---

# 4. Frontend Structure

```text
frontend/

src/

├── pages/
│
├── components/
│
├── layouts/
│
├── hooks/
│
├── services/
│
├── routes/
│
├── contexts/
│
├── store/
│
├── types/
│
├── utils/
│
└── App.tsx
```

---

# 5. AI Engine Structure

```text
ai_engine/

├── parsers/
│
├── extractors/
│
├── embeddings/
│
├── matching/
│
├── ranking/
│
├── summarization/
│
├── interview_generation/
│
└── models/
```

---

# 6. Backend Modules

---

## Authentication Module

Folder:

```text
api/auth/
```

Responsibilities:

* Registration
* Login
* Refresh Token
* Logout

Endpoints:

```text
POST /auth/register

POST /auth/login

POST /auth/refresh

POST /auth/logout
```

Services:

```text
AuthService
JWTService
PasswordService
```

---

## User Module

Folder:

```text
api/users/
```

Responsibilities:

* Profile Management
* User Information

Endpoints:

```text
GET /users/me

PUT /users/me
```

---

## Job Module

Folder:

```text
api/jobs/
```

Responsibilities:

* Create Job
* Edit Job
* Delete Job
* View Job

Endpoints:

```text
POST /jobs

GET /jobs

GET /jobs/{id}

PUT /jobs/{id}

DELETE /jobs/{id}
```

---

## Resume Module

Folder:

```text
api/resumes/
```

Responsibilities:

* Resume Upload
* Resume Storage
* Resume Retrieval

Endpoints:

```text
POST /resumes/upload

GET /resumes

GET /resumes/{id}
```

---

## Candidate Module

Folder:

```text
api/candidates/
```

Responsibilities:

* Candidate Profile
* Candidate Scores
* Candidate Summary

Endpoints:

```text
GET /candidates

GET /candidates/{id}
```

---

## Ranking Module

Folder:

```text
api/rankings/
```

Responsibilities:

* Candidate Ranking
* Ranking Generation

Endpoints:

```text
POST /rankings/generate

GET /rankings
```

---

## Report Module

Folder:

```text
api/reports/
```

Responsibilities:

* PDF Export
* CSV Export
* XLSX Export

Endpoints:

```text
GET /reports/pdf

GET /reports/csv

GET /reports/xlsx
```

---

# 7. Database Models

---

## User Model

```text
User
```

Fields:

```text
id
name
email
password_hash
role
created_at
updated_at
```

---

## Job Model

```text
Job
```

Fields:

```text
id
title
description
required_skills
experience_required
education_required
created_by
created_at
```

---

## Resume Model

```text
Resume
```

Fields:

```text
id
file_name
file_url
candidate_id
uploaded_at
```

---

## Candidate Model

```text
Candidate
```

Fields:

```text
id
name
email
phone
experience_years
education
linkedin_url
```

---

## Skill Model

```text
Skill
```

Fields:

```text
id
name
category
```

---

## CandidateSkill

```text
candidate_id
skill_id
proficiency
```

---

## CandidateScore

```text
candidate_id
job_id

skill_score

experience_score

education_score

semantic_score

final_score

rank
```

---

# 8. Repository Layer

Pattern:

Repository Pattern

Example:

```text
UserRepository

JobRepository

ResumeRepository

CandidateRepository

ScoreRepository
```

Responsibilities:

* Database access
* Query abstraction
* CRUD operations

---

# 9. Service Layer

---

## AuthService

Responsibilities:

* User Registration
* Authentication

---

## ResumeService

Responsibilities:

* Upload Resume
* Validate Resume

---

## JobService

Responsibilities:

* Job CRUD

---

## ParsingService

Responsibilities:

* Extract Resume Data

---

## MatchingService

Responsibilities:

* Compare Candidate and Job

---

## RankingService

Responsibilities:

* Generate Rankings

---

## ReportService

Responsibilities:

* Create Reports

---

# 10. AI Processing Pipeline

---

## Resume Parsing Flow

```text
Resume

↓

PDF Extraction

↓

Text Cleaning

↓

Section Detection

↓

Entity Extraction

↓

Structured JSON
```

Output:

```json
{
  "name": "",
  "skills": [],
  "education": [],
  "experience": []
}
```

---

## Embedding Generation Flow

```text
Candidate Profile

↓

Sentence Transformer

↓

Vector Embedding

↓

pgvector Storage
```

Model:

```text
all-MiniLM-L6-v2
```

Dimension:

```text
384
```

---

## Matching Pipeline

Inputs:

```text
Candidate Vector

Job Vector
```

Process:

```text
Cosine Similarity
```

Outputs:

```text
Semantic Score
```

---

## Final Scoring Formula

```text
Final Score =

35% Semantic Score

25% Skill Score

20% Experience Score

10% Education Score

10% AI Evaluation
```

---

# 11. Celery Background Jobs

Folder:

```text
tasks/
```

---

Task 1

```text
parse_resume_task
```

Responsibilities:

* Resume Parsing

---

Task 2

```text
generate_embedding_task
```

Responsibilities:

* Vector Creation

---

Task 3

```text
generate_summary_task
```

Responsibilities:

* AI Summary

---

Task 4

```text
generate_interview_questions_task
```

Responsibilities:

* Question Generation

---

Task 5

```text
generate_report_task
```

Responsibilities:

* Report Export

---

# 12. Frontend Pages

---

## Authentication

```text
Login Page

Register Page
```

---

## Dashboard

Widgets:

```text
Jobs

Candidates

Top Scores

Analytics
```

---

## Job Management

```text
Create Job

Edit Job

Delete Job
```

---

## Resume Upload

Features:

```text
Single Upload

Bulk Upload
```

---

## Candidate Ranking

Features:

```text
Ranking Table

Score Breakdown

Summary View
```

---

## Reports

Features:

```text
PDF Export

CSV Export

Excel Export
```

---

# 13. Security Design

Authentication:

```text
JWT
```

Authorization:

```text
RBAC
```

Password Hashing:

```text
bcrypt
```

Input Validation:

```text
Pydantic
```

File Validation:

```text
PDF

DOCX

Size Limit
```

Rate Limiting:

```text
SlowAPI
```

---

# 14. Error Handling

Global Exception Handler

Examples:

```text
401 Unauthorized

403 Forbidden

404 Not Found

422 Validation Error

500 Internal Error
```

---

# 15. Logging Strategy

Log Levels:

```text
INFO

WARNING

ERROR

CRITICAL
```

Log Storage:

```text
logs/app.log
```

Future:

```text
ELK Stack
```

---

# 16. Testing Structure

```text
tests/

├── unit/
├── integration/
├── api/
└── e2e/
```

Coverage Target:

```text
80%+
```

Tools:

```text
Pytest

React Testing Library
```

---

# 17. Deployment Structure

```text
deployment/

├── Dockerfile

├── docker-compose.yml

├── nginx.conf

├── github-actions/

└── terraform/
```

---

# 18. Development Responsibilities

AI Engineer

* Parsing Engine
* Matching Engine
* Ranking Engine

Backend Engineer

* FastAPI
* Database
* APIs

Frontend Engineer

* React Dashboard
* UI Components

DevOps Engineer

* Docker
* CI/CD
* Deployment

QA Engineer

* Testing
* Documentation

---

# 19. Conclusion

This Low Level Design converts the high-level architecture into implementable software modules. The structure promotes scalability, maintainability, security, and future expansion while enabling parallel development by all team members.
