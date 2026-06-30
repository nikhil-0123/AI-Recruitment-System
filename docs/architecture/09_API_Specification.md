# AI Recruitment Automation System (ARAS)

# API Specification Document

Version: 1.0

Date: June 2026

API Style: RESTful API

Protocol: HTTPS

Authentication: JWT Bearer Token

Base URL:

```text
Development:
http://localhost:8000/api/v1

Production:
https://api.aras.ai/api/v1
```

Document Status: Approved

---

# 1. API Standards

## Request Format

```json
{
  "data": {}
}
```

## Success Response

```json
{
  "success": true,
  "message": "Operation successful",
  "data": {}
}
```

## Error Response

```json
{
  "success": false,
  "message": "Validation Error",
  "errors": []
}
```

---

# 2. Authentication APIs

## Register User

### Endpoint

```http
POST /auth/register
```

### Request

```json
{
  "name": "Nikhil Chaugule",
  "email": "nikhil@example.com",
  "password": "StrongPassword123"
}
```

### Response

```json
{
  "success": true,
  "message": "User registered successfully"
}
```

### Status Codes

```text
201 Created
400 Bad Request
409 Conflict
```

---

## Login User

### Endpoint

```http
POST /auth/login
```

### Request

```json
{
  "email": "nikhil@example.com",
  "password": "StrongPassword123"
}
```

### Response

```json
{
  "access_token": "jwt_token",
  "refresh_token": "refresh_token",
  "token_type": "bearer"
}
```

### Status Codes

```text
200 OK
401 Unauthorized
```

---

## Refresh Token

### Endpoint

```http
POST /auth/refresh
```

### Response

```json
{
  "access_token": "new_token"
}
```

---

## Logout

### Endpoint

```http
POST /auth/logout
```

---

# 3. User APIs

## Get Current User

### Endpoint

```http
GET /users/me
```

### Response

```json
{
  "id": "uuid",
  "name": "Nikhil",
  "email": "nikhil@example.com",
  "role": "recruiter"
}
```

---

## Update Profile

### Endpoint

```http
PUT /users/me
```

### Request

```json
{
  "name": "Updated Name"
}
```

---

# 4. Job Management APIs

## Create Job

### Endpoint

```http
POST /jobs
```

### Request

```json
{
  "title": "Backend Developer",
  "description": "FastAPI developer with PostgreSQL experience",
  "experience_required": 2,
  "education_required": "Bachelor Degree"
}
```

### Response

```json
{
  "job_id": "uuid",
  "status": "created"
}
```

---

## Get All Jobs

### Endpoint

```http
GET /jobs
```

### Query Parameters

```text
?page=1
&limit=10
&status=active
```

---

## Get Job By ID

### Endpoint

```http
GET /jobs/{job_id}
```

---

## Update Job

### Endpoint

```http
PUT /jobs/{job_id}
```

---

## Delete Job

### Endpoint

```http
DELETE /jobs/{job_id}
```

---

# 5. Resume APIs

## Upload Single Resume

### Endpoint

```http
POST /resumes/upload
```

### Content Type

```text
multipart/form-data
```

### Request

```text
file = resume.pdf
job_id = uuid
```

### Response

```json
{
  "resume_id": "uuid",
  "status": "uploaded"
}
```

---

## Upload Multiple Resumes

### Endpoint

```http
POST /resumes/upload-bulk
```

### Content Type

```text
multipart/form-data
```

### Request

```text
files[] = multiple resumes
job_id = uuid
```

### Response

```json
{
  "processed": 25,
  "failed": 1
}
```

---

## Get Resume

### Endpoint

```http
GET /resumes/{resume_id}
```

---

## Delete Resume

### Endpoint

```http
DELETE /resumes/{resume_id}
```

---

# 6. Candidate APIs

## Get All Candidates

### Endpoint

```http
GET /candidates
```

### Query Parameters

```text
?page=1
&limit=20
&job_id=uuid
```

---

## Get Candidate Details

### Endpoint

```http
GET /candidates/{candidate_id}
```

### Response

```json
{
  "candidate_id": "uuid",
  "name": "John Doe",
  "email": "john@example.com",
  "skills": [
    "Python",
    "FastAPI",
    "Docker"
  ]
}
```

---

## Search Candidates

### Endpoint

```http
GET /candidates/search
```

### Query

```text
?skill=Python
```

---

# 7. Ranking APIs

## Generate Ranking

### Endpoint

```http
POST /rankings/generate/{job_id}
```

### Response

```json
{
  "status": "ranking_started"
}
```

---

## Get Rankings

### Endpoint

```http
GET /rankings/{job_id}
```

### Response

```json
[
  {
    "rank": 1,
    "candidate": "John Doe",
    "score": 92.5
  }
]
```

---

## Get Candidate Score Breakdown

### Endpoint

```http
GET /rankings/{job_id}/{candidate_id}
```

### Response

```json
{
  "skill_score": 90,
  "experience_score": 85,
  "education_score": 80,
  "semantic_score": 95,
  "final_score": 91
}
```

---

# 8. AI Summary APIs

## Generate Candidate Summary

### Endpoint

```http
POST /ai/summaries/{candidate_id}
```

### Response

```json
{
  "status": "summary_generated"
}
```

---

## Get Candidate Summary

### Endpoint

```http
GET /ai/summaries/{candidate_id}
```

### Response

```json
{
  "strengths": [
    "Python",
    "FastAPI"
  ],
  "weaknesses": [
    "AWS"
  ],
  "recommendation": "Interview Round 1"
}
```

---

# 9. Skill Gap Analysis APIs

## Generate Skill Gap Report

### Endpoint

```http
GET /ai/skill-gap/{candidate_id}/{job_id}
```

### Response

```json
{
  "required_skills": [
    "Python",
    "Docker",
    "AWS"
  ],
  "missing_skills": [
    "AWS"
  ]
}
```

---

# 10. Interview Question APIs

## Generate Questions

### Endpoint

```http
POST /ai/interview-questions
```

### Request

```json
{
  "candidate_id": "uuid",
  "job_id": "uuid"
}
```

### Response

```json
{
  "status": "generated"
}
```

---

## Get Questions

### Endpoint

```http
GET /ai/interview-questions/{candidate_id}/{job_id}
```

### Response

```json
{
  "technical": [],
  "coding": [],
  "behavioral": []
}
```

---

# 11. Analytics APIs

## Dashboard Overview

### Endpoint

```http
GET /analytics/dashboard
```

### Response

```json
{
  "jobs": 12,
  "candidates": 245,
  "shortlisted": 32,
  "rejected": 143
}
```

---

## Hiring Funnel

### Endpoint

```http
GET /analytics/funnel
```

---

## Skill Trends

### Endpoint

```http
GET /analytics/skills
```

---

# 12. Report APIs

## Generate PDF Report

### Endpoint

```http
POST /reports/pdf/{job_id}
```

---

## Generate CSV Report

### Endpoint

```http
POST /reports/csv/{job_id}
```

---

## Generate Excel Report

### Endpoint

```http
POST /reports/xlsx/{job_id}
```

---

## Download Report

### Endpoint

```http
GET /reports/download/{report_id}
```

---

# 13. Admin APIs

## Get Audit Logs

### Endpoint

```http
GET /admin/audit-logs
```

---

## Get System Health

### Endpoint

```http
GET /admin/health
```

### Response

```json
{
  "database": "healthy",
  "redis": "healthy",
  "storage": "healthy",
  "api": "healthy"
}
```

---

# 14. Common Status Codes

| Code | Meaning               |
| ---- | --------------------- |
| 200  | Success               |
| 201  | Created               |
| 204  | No Content            |
| 400  | Bad Request           |
| 401  | Unauthorized          |
| 403  | Forbidden             |
| 404  | Not Found             |
| 409  | Conflict              |
| 422  | Validation Error      |
| 429  | Rate Limited          |
| 500  | Internal Server Error |

---

# 15. Authentication Requirements

Protected endpoints require:

```http
Authorization: Bearer <JWT_TOKEN>
```

Example:

```http
GET /jobs

Authorization: Bearer eyJhbGci...
```

---

# 16. API Versioning Strategy

Current Version:

```text
v1
```

Pattern:

```text
/api/v1/jobs

/api/v1/candidates

/api/v1/rankings
```

Future:

```text
/api/v2/jobs
```

---

# 17. Rate Limiting

Authentication Endpoints:

```text
10 requests/minute
```

Resume Upload:

```text
20 requests/minute
```

AI Endpoints:

```text
30 requests/minute
```

---

# 18. API Security

Security Features:

* JWT Authentication
* RBAC Authorization
* Request Validation
* File Validation
* Rate Limiting
* SQL Injection Protection
* CORS Protection
* HTTPS Enforcement

---

# 19. API Summary

| Module         | Endpoints |
| -------------- | --------- |
| Authentication | 4         |
| Users          | 2         |
| Jobs           | 5         |
| Resumes        | 4         |
| Candidates     | 3         |
| Rankings       | 3         |
| AI Services    | 5         |
| Analytics      | 3         |
| Reports        | 4         |
| Admin          | 2         |
| Total APIs     | 35        |

This API specification serves as the official contract between the frontend, backend, AI, QA, and DevOps teams for ARAS Version 1.0.
