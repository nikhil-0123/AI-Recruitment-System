# AI Recruitment Automation System (ARAS)

# Software Requirements Specification (SRS)

Version: 1.0

Date: June 2026

Project Type: AI-Powered Recruitment Automation Platform

Document Status: Approved for Development

---

# 1. Introduction

## 1.1 Purpose

The purpose of this document is to define the functional and non-functional requirements of the AI Recruitment Automation System (ARAS).

This SRS serves as the official reference for:

* Developers
* AI Engineers
* Test Engineers
* Project Managers
* Stakeholders

The document describes system behavior, features, constraints, architecture assumptions, and quality requirements.

---

## 1.2 Project Overview

AI Recruitment Automation System (ARAS) is an AI-powered hiring platform designed to automate resume screening, candidate evaluation, ranking, and shortlisting.

The platform enables recruiters to:

* Upload resumes
* Upload job descriptions
* Analyze candidate profiles
* Match candidate skills
* Rank applicants
* Generate AI-powered recommendations
* Export reports

The system significantly reduces manual screening efforts while improving recruitment quality.

---

## 1.3 Business Need

Organizations face challenges such as:

* Large application volumes
* Slow screening processes
* Inconsistent evaluations
* Hiring delays
* Human bias

ARAS addresses these challenges using Artificial Intelligence and Natural Language Processing.

---

## 1.4 Objectives

The system aims to:

* Reduce screening time by 80%
* Improve candidate-job matching accuracy
* Standardize candidate evaluation
* Provide recruiter decision support
* Increase recruitment efficiency

---

# 2. Scope

## 2.1 In Scope

### User Management

* Recruiter registration
* User login
* Authentication
* Authorization
* Role management

### Resume Management

* Single upload
* Bulk upload
* Resume storage
* Resume viewing

### Resume Parsing

Extract:

* Name
* Email
* Phone
* Education
* Skills
* Experience
* Certifications
* Projects
* LinkedIn

### Job Description Management

* Create jobs
* Edit jobs
* Delete jobs
* View jobs

### AI Candidate Evaluation

* Skill matching
* Experience matching
* Education matching
* Semantic similarity scoring

### Candidate Ranking

* Candidate score generation
* Rank generation
* Recommendation generation

### Dashboard

* Analytics
* Rankings
* Statistics

### Reporting

* PDF export
* CSV export
* Excel export

---

## 2.2 Out of Scope (Version 1.0)

The following features are excluded from Version 1:

* Video interview analysis
* Voice analysis
* Automated interviewing
* Background verification
* Payroll integration
* Multi-tenant architecture
* Mobile applications

---

# 3. Stakeholders

## Primary Stakeholders

### Recruiters

Responsible for candidate screening and shortlisting.

### HR Managers

Responsible for recruitment operations.

### Hiring Managers

Responsible for interview decisions.

---

## Secondary Stakeholders

### Placement Cells

Universities and colleges.

### Recruitment Agencies

Third-party recruitment organizations.

### Startups and SMEs

Organizations with limited recruitment resources.

---

# 4. User Roles

## Recruiter

Permissions:

* Manage jobs
* Upload resumes
* View rankings
* Generate reports

---

## HR Admin

Permissions:

* Manage recruiters
* Access analytics
* Manage system settings

---

## Super Admin

Permissions:

* Full system access
* User management
* Audit logs
* System configuration

---

# 5. Functional Requirements

---

## FR-001 User Registration

Description:

Allow recruiters to create accounts.

Inputs:

* Name
* Email
* Password

Output:

* User account created

Priority:

High

---

## FR-002 User Login

Description:

Allow registered users to authenticate.

Inputs:

* Email
* Password

Output:

* JWT Access Token
* Refresh Token

Priority:

High

---

## FR-003 Resume Upload

Description:

Allow recruiters to upload resumes.

Supported Formats:

* PDF
* DOCX

Priority:

High

---

## FR-004 Bulk Resume Upload

Description:

Allow uploading multiple resumes simultaneously.

Maximum Upload:

100 files per batch

Priority:

High

---

## FR-005 Resume Parsing

Description:

Extract structured candidate information.

Extract Fields:

* Name
* Email
* Phone
* Skills
* Education
* Experience
* Projects
* Certifications

Priority:

High

---

## FR-006 Job Creation

Description:

Create new job postings.

Fields:

* Title
* Description
* Required Skills
* Experience
* Education

Priority:

High

---

## FR-007 Job Editing

Description:

Modify existing jobs.

Priority:

Medium

---

## FR-008 Candidate Matching

Description:

Compare candidate profiles with job requirements.

Outputs:

* Skill Match Score
* Experience Match Score
* Education Match Score
* Semantic Similarity Score

Priority:

High

---

## FR-009 Candidate Ranking

Description:

Generate overall candidate ranking.

Output:

Score Range:

0–100

Priority:

High

---

## FR-010 Candidate Categorization

Description:

Classify candidates.

Categories:

* Highly Recommended
* Recommended
* Consider
* Rejected

Priority:

High

---

## FR-011 AI Candidate Summary

Description:

Generate recruiter-friendly summaries.

Output Example:

Strengths

Weaknesses

Recommendations

Priority:

Medium

---

## FR-012 Interview Question Generation

Description:

Generate interview questions automatically.

Types:

* Technical
* Coding
* Behavioral

Priority:

Medium

---

## FR-013 Dashboard Analytics

Description:

Display recruitment insights.

Metrics:

* Candidate Count
* Job Count
* Ranking Distribution
* Hiring Funnel

Priority:

High

---

## FR-014 Report Export

Description:

Export reports.

Formats:

* PDF
* CSV
* XLSX

Priority:

Medium

---

# 6. Non-Functional Requirements

## Performance Requirements

Resume Processing:

≤ 10 seconds

Candidate Ranking:

≤ 5 seconds

Dashboard Loading:

≤ 2 seconds

API Response Time:

≤ 500 ms

---

## Scalability Requirements

Support:

* 10,000 resumes
* 1,000 jobs
* 500 concurrent users

---

## Reliability Requirements

System Availability:

99% uptime

Backup Frequency:

Daily

---

## Security Requirements

Authentication:

JWT

Password Hashing:

bcrypt

Authorization:

RBAC

File Validation:

Required

Rate Limiting:

Enabled

Audit Logging:

Enabled

HTTPS:

Mandatory

---

## Maintainability Requirements

Code Coverage:

Minimum 80%

Architecture:

Modular

Documentation:

Mandatory

API Standards:

RESTful

---

# 7. System Constraints

## Technical Constraints

Frontend:

* React
* TypeScript

Backend:

* FastAPI

Database:

* PostgreSQL

Vector Database:

* pgvector

Cache:

* Redis

Queue:

* Celery

Storage:

* AWS S3

AI Models:

* Sentence Transformers
* Gemini API

---

## Resource Constraints

Development Time:

40 Days

Team Size:

5 Members

Budget:

Student Project Budget

---

# 8. Assumptions

The following assumptions are made:

* Recruiters possess basic technical skills.
* Internet connectivity is available.
* Uploaded resumes are valid PDF or DOCX files.
* AI APIs remain available during operation.
* PostgreSQL database remains accessible.

---

# 9. Acceptance Criteria

The system shall be considered complete when:

✓ User authentication works

✓ Job management works

✓ Resume upload works

✓ Resume parsing works

✓ Candidate ranking works

✓ Dashboard works

✓ Reports can be exported

✓ Application is deployed

✓ Documentation is completed

✓ End-to-end testing passes

---

# 10. Risks

| Risk                | Impact | Mitigation                |
| ------------------- | ------ | ------------------------- |
| Poor Resume Parsing | High   | Build validation pipeline |
| API Failure         | Medium | Retry mechanisms          |
| Large File Uploads  | Medium | Upload limits             |
| AI Service Downtime | High   | Local fallback models     |
| Scope Creep         | High   | Strict sprint planning    |

---

# 11. Success Metrics

Business Metrics

* 80% reduction in screening time
* 85% ranking accuracy
* 90% recruiter satisfaction

Technical Metrics

* < 2 sec dashboard load time
* < 10 sec resume processing
* 99% uptime

---

# 12. Approval

This SRS document serves as the baseline requirement specification for the AI Recruitment Automation System (ARAS) and will be used throughout design, development, testing, deployment, and maintenance phases.

Document Status: Approved

Version: 1.0
