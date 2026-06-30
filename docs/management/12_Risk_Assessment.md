# AI Recruitment Automation System (ARAS)

# Risk Assessment & Mitigation Plan

Version: 1.0

Date: June 2026

Project Duration: 40 Days

Team Size: 5 Members

Document Status: Approved

---

# 1. Purpose

The purpose of this document is to identify:

* Technical Risks
* AI Risks
* Security Risks
* Infrastructure Risks
* Team Risks
* Project Management Risks

and define mitigation strategies to minimize their impact on project success.

---

# 2. Risk Assessment Methodology

Risk Rating Formula

```text
Risk Score = Probability × Impact
```

Scale:

| Score | Risk Level |
| ----- | ---------- |
| 1-4   | Low        |
| 5-9   | Medium     |
| 10-16 | High       |
| 17-25 | Critical   |

---

# 3. Project Risks Overview

| ID  | Risk                        | Probability | Impact | Score | Level    |
| --- | --------------------------- | ----------- | ------ | ----- | -------- |
| R1  | Scope Creep                 | 4           | 5      | 20    | Critical |
| R2  | Team Member Delay           | 4           | 4      | 16    | High     |
| R3  | Resume Parsing Accuracy     | 4           | 4      | 16    | High     |
| R4  | AI API Failure              | 3           | 5      | 15    | High     |
| R5  | Deployment Failure          | 3           | 4      | 12    | High     |
| R6  | Database Performance Issues | 2           | 4      | 8     | Medium   |
| R7  | Security Vulnerabilities    | 2           | 5      | 10    | High     |
| R8  | Integration Problems        | 3           | 4      | 12    | High     |
| R9  | Data Quality Issues         | 4           | 3      | 12    | High     |
| R10 | Testing Delays              | 3           | 3      | 9     | Medium   |

---

# 4. Project Management Risks

---

## R1: Scope Creep

### Description

New features continuously added during development.

Examples:

* Chatbot
* Video Interviews
* Multi-Tenant SaaS
* Email Automation

while core functionality is incomplete.

---

### Impact

* Missed deadlines
* Incomplete MVP
* Team burnout

---

### Risk Level

Critical

---

### Mitigation

Lock Version 1 Features:

Allowed:

* Authentication
* Resume Upload
* Resume Parsing
* Ranking
* Dashboard
* Reports

Not Allowed:

* Video Analysis
* Voice Analysis
* Enterprise Billing
* Advanced SaaS Features

Any new feature request:

Must be scheduled for Version 2.

---

# 5. Team Risks

---

## R2: Team Member Unavailability

### Description

A team member becomes unavailable.

Examples:

* Exams
* Personal Issues
* Lack of Commitment

---

### Impact

Critical module delays.

---

### Mitigation

Every module must have:

Primary Owner

Secondary Backup Owner

Knowledge sharing every sprint.

---

### Backup Mapping

| Primary           | Backup           |
| ----------------- | ---------------- |
| AI Lead           | Backend Engineer |
| Backend Engineer  | AI Lead          |
| Frontend Engineer | QA Engineer      |
| DevOps Engineer   | Backend Engineer |
| QA Engineer       | Project Manager  |

---

# 6. AI Risks

---

## R3: Resume Parsing Accuracy

### Description

Resumes have inconsistent formats.

Examples:

* Different layouts
* Missing sections
* Scanned PDFs

---

### Impact

Incorrect candidate information.

---

### Risk Level

High

---

### Mitigation

Phase 1:

Rule-Based Extraction

Libraries:

```text
PyMuPDF

pdfplumber

python-docx
```

Phase 2:

LLM-Assisted Extraction

Validation Rules:

* Email Validation
* Phone Validation
* Skill Validation

---

## R4: Gemini/OpenAI API Failure

### Description

External AI service unavailable.

---

### Impact

AI summaries fail.

---

### Risk Level

High

---

### Mitigation

Fallback System

Primary:

Gemini API

Fallback:

Local templates

Example:

```text
Strong Skills:
Python

Missing Skills:
AWS

Recommendation:
Consider Interview
```

System must never completely fail.

---

# 7. Technical Risks

---

## R5: Deployment Failure

### Description

Application works locally but fails in production.

---

### Impact

Project cannot be demonstrated.

---

### Risk Level

High

---

### Mitigation

Use identical environments:

Development

Testing

Production

via Docker.

Deployment test on Day 20.

Do not wait until Day 40.

---

## R6: Database Performance Issues

### Description

Slow ranking queries.

---

### Impact

Poor user experience.

---

### Mitigation

Indexes:

```sql
users.email

jobs.title

candidate_scores.final_score
```

Use Redis caching.

Use pagination everywhere.

---

## R7: Frontend-Backend Integration Issues

### Description

API responses differ from frontend expectations.

---

### Impact

Broken UI functionality.

---

### Mitigation

Single Source of Truth:

```text
09_API_Specification.md
```

Frontend must consume mock APIs before backend completion.

---

# 8. Security Risks

---

## R8: Unauthorized Access

### Description

Users access protected endpoints.

---

### Impact

Data breach.

---

### Mitigation

Implement:

* JWT Authentication
* RBAC
* Protected Routes

---

## R9: File Upload Attacks

### Description

Malicious files uploaded.

---

### Impact

System compromise.

---

### Mitigation

Allow:

```text
PDF

DOCX
```

Reject:

```text
EXE

BAT

JS

ZIP
```

Maximum File Size:

```text
10 MB
```

---

## R10: SQL Injection

### Description

Malicious user input.

---

### Impact

Database compromise.

---

### Mitigation

Use:

* SQLAlchemy ORM
* Parameterized Queries
* Input Validation

Never use raw SQL from user input.

---

# 9. Infrastructure Risks

---

## R11: Redis Failure

### Description

Redis service unavailable.

---

### Impact

Caching disabled.

Queue failures.

---

### Mitigation

Application must continue without cache.

Graceful fallback.

---

## R12: PostgreSQL Failure

### Description

Database unavailable.

---

### Impact

Application outage.

---

### Mitigation

Daily backups.

Neon automatic backup support.

---

## R13: Storage Failure

### Description

Resume files unavailable.

---

### Impact

Resume access broken.

---

### Mitigation

Primary:

AWS S3

Backup:

Local Development Storage

---

# 10. Data Risks

---

## R14: Duplicate Candidates

### Description

Same candidate uploads multiple resumes.

---

### Impact

Duplicate rankings.

---

### Mitigation

Duplicate Detection:

Using:

* Email
* Phone
* Similarity Checks

---

## R15: Poor Resume Quality

### Description

Scanned images.

Corrupted files.

Incomplete resumes.

---

### Impact

Poor extraction accuracy.

---

### Mitigation

Validation Status:

```text
Valid

Needs Review

Rejected
```

---

# 11. Testing Risks

---

## R16: Inadequate Testing

### Description

Bugs discovered during demo.

---

### Impact

Project failure.

---

### Mitigation

Testing starts on Day 15.

Not Day 39.

---

Testing Types

```text
Unit Testing

API Testing

Integration Testing

UI Testing
```

---

Coverage Goal

```text
80%
```

---

# 12. Deployment Risks

---

## R17: Environment Configuration Errors

### Description

Incorrect environment variables.

---

### Impact

Production crashes.

---

### Mitigation

Maintain:

```text
.env.example
```

Required Variables:

```text
DATABASE_URL

JWT_SECRET

REDIS_URL

GEMINI_API_KEY

AWS_ACCESS_KEY
```

---

# 13. Risk Monitoring Plan

Review Frequency

Weekly

Owner

Project Manager

---

Weekly Questions

1. Are we on schedule?
2. Any blocked tasks?
3. Any integration issues?
4. Any deployment concerns?
5. Any scope changes?

---

# 14. Emergency Recovery Plan

If Project Falls Behind

Priority Order:

```text
1. Authentication

2. Resume Upload

3. Resume Parsing

4. Candidate Ranking

5. Dashboard

6. Reports

7. AI Features
```

If time becomes limited:

Drop:

```text
Interview Questions

Advanced Analytics

Excel Reports
```

Never drop:

```text
Resume Parsing

Candidate Ranking

Dashboard
```

---

# 15. Go / No-Go Checklist

Before Deployment

✓ Authentication Working

✓ Resume Upload Working

✓ Parsing Working

✓ Ranking Working

✓ Dashboard Working

✓ Reports Working

✓ Tests Passing

✓ Docker Working

✓ Documentation Complete

---

# 16. Conclusion

The primary threats to project success are:

1. Scope Creep
2. Team Delays
3. AI Parsing Accuracy
4. Deployment Problems
5. Integration Failures

By following the mitigation strategies defined in this document, the team can significantly reduce risk and improve the probability of delivering a successful production-ready AI Recruitment Automation System within the 40-day schedule.

Document Status: Approved
