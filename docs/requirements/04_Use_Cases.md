# AI Recruitment Automation System (ARAS)

# Use Case Specification Document

Version: 1.0

Date: June 2026

Project: AI Recruitment Automation System

---

# 1. Introduction

This document describes the major use cases of the AI Recruitment Automation System (ARAS).

Each use case contains:

* Use Case ID
* Description
* Actors
* Preconditions
* Main Flow
* Alternate Flow
* Postconditions

These use cases define how users interact with the system and serve as the basis for API design, backend implementation, and testing.

---

# UC-001 User Registration

## Description

A recruiter creates a new account on the platform.

## Primary Actor

Recruiter

## Preconditions

* Recruiter is not registered.
* Internet connection is available.

## Trigger

Recruiter clicks "Register".

## Main Flow

1. Recruiter enters:

   * Full Name
   * Email
   * Password

2. System validates input.

3. System checks email uniqueness.

4. System hashes password.

5. System creates user account.

6. System stores recruiter information.

7. System returns success response.

## Alternate Flow

3a. Email already exists.

* Registration rejected.
* Error message displayed.

## Postconditions

* Recruiter account created successfully.

---

# UC-002 User Login

## Description

Recruiter authenticates into the system.

## Primary Actor

Recruiter

## Preconditions

* User account exists.

## Trigger

Recruiter submits login form.

## Main Flow

1. Enter email.
2. Enter password.
3. System validates credentials.
4. JWT token generated.
5. Refresh token generated.
6. User redirected to dashboard.

## Alternate Flow

Invalid credentials.

* Authentication fails.
* Error message displayed.

## Postconditions

* User authenticated.

---

# UC-003 Create Job Description

## Description

Recruiter creates a new job opening.

## Primary Actor

Recruiter

## Preconditions

* Recruiter logged in.

## Trigger

Recruiter clicks "Create Job".

## Main Flow

1. Enter job title.

2. Enter job description.

3. Enter required skills.

4. Enter experience requirement.

5. Save job.

6. System stores job.

7. System initiates AI job analysis.

## Alternate Flow

Required fields missing.

* Validation error shown.

## Postconditions

* New job created.

---

# UC-004 AI Job Requirement Extraction

## Description

System extracts structured requirements from a job description.

## Primary Actor

System

## Preconditions

* Job description exists.

## Trigger

Job created.

## Main Flow

1. Retrieve job description.

2. NLP processor analyzes text.

3. Extract:

   * Skills
   * Education
   * Experience
   * Certifications

4. Store extracted requirements.

## Alternate Flow

Parsing failure.

* Manual review required.

## Postconditions

* Structured job requirements available.

---

# UC-005 Upload Single Resume

## Description

Recruiter uploads a candidate resume.

## Primary Actor

Recruiter

## Preconditions

* User authenticated.

## Trigger

Recruiter selects resume file.

## Main Flow

1. Upload PDF/DOCX.
2. File validated.
3. Resume stored.
4. Parsing job queued.

## Alternate Flow

Unsupported file format.

* Upload rejected.

## Postconditions

* Resume stored successfully.

---

# UC-006 Bulk Resume Upload

## Description

Recruiter uploads multiple resumes simultaneously.

## Primary Actor

Recruiter

## Preconditions

* User authenticated.

## Trigger

Recruiter selects multiple files.

## Main Flow

1. Select resumes.
2. Upload batch.
3. System validates files.
4. Files stored.
5. Parsing tasks queued.

## Alternate Flow

One file invalid.

* Invalid file skipped.
* Remaining files processed.

## Postconditions

* Valid resumes uploaded.

---

# UC-007 Resume Parsing

## Description

System extracts candidate information.

## Primary Actor

System

## Preconditions

* Resume uploaded.

## Trigger

Resume processing starts.

## Main Flow

1. Extract text.

2. Detect sections.

3. Extract:

   * Name
   * Email
   * Phone
   * Skills
   * Education
   * Experience
   * Projects
   * Certifications

4. Store structured data.

## Alternate Flow

Resume corrupted.

* Resume flagged.
* Processing stopped.

## Postconditions

* Candidate profile created.

---

# UC-008 Generate Candidate Embeddings

## Description

System creates vector representations of candidate profiles.

## Primary Actor

System

## Preconditions

* Candidate profile exists.

## Trigger

Resume parsing completed.

## Main Flow

1. Gather candidate information.
2. Generate embeddings.
3. Store vectors in pgvector.

## Alternate Flow

Embedding model unavailable.

* Retry processing.

## Postconditions

* Candidate vectors stored.

---

# UC-009 Match Candidate to Job

## Description

System compares candidate profiles with job requirements.

## Primary Actor

System

## Preconditions

* Candidate profile exists.
* Job exists.

## Trigger

Matching process initiated.

## Main Flow

1. Load candidate data.

2. Load job requirements.

3. Calculate:

   * Skill Match
   * Experience Match
   * Education Match
   * Semantic Similarity

4. Generate scores.

## Alternate Flow

Missing candidate data.

* Candidate flagged.

## Postconditions

* Match scores available.

---

# UC-010 Generate Candidate Ranking

## Description

System ranks candidates.

## Primary Actor

System

## Preconditions

* Matching completed.

## Trigger

Ranking request initiated.

## Main Flow

1. Retrieve candidate scores.
2. Calculate final score.
3. Sort descending.
4. Assign rank.
5. Store rankings.

## Alternate Flow

No candidates available.

* Ranking aborted.

## Postconditions

* Ranked candidate list generated.

---

# UC-011 Generate Candidate Summary

## Description

System generates AI-powered candidate summaries.

## Primary Actor

System

## Preconditions

* Candidate profile exists.

## Trigger

Recruiter opens candidate profile.

## Main Flow

1. Retrieve candidate information.

2. Send profile to AI model.

3. Generate:

   * Strengths
   * Weaknesses
   * Recommendation

4. Save summary.

## Alternate Flow

AI service unavailable.

* Retry request.

## Postconditions

* Candidate summary generated.

---

# UC-012 Generate Interview Questions

## Description

System creates interview questions.

## Primary Actor

System

## Preconditions

* Candidate evaluated.

## Trigger

Recruiter requests interview questions.

## Main Flow

1. Analyze candidate skills.

2. Analyze job requirements.

3. Generate:

   * Technical Questions
   * Coding Questions
   * Behavioral Questions

4. Save generated questions.

## Postconditions

* Interview question set available.

---

# UC-013 Shortlist Candidates

## Description

Recruiter generates shortlist.

## Primary Actor

Recruiter

## Preconditions

* Rankings exist.

## Trigger

Recruiter clicks "Generate Shortlist".

## Main Flow

1. Retrieve ranked candidates.
2. Apply threshold rules.

Categories:

* Highly Recommended
* Recommended
* Consider
* Rejected

3. Save shortlist.

## Postconditions

* Shortlist generated.

---

# UC-014 View Dashboard

## Description

Recruiter accesses analytics dashboard.

## Primary Actor

Recruiter

## Preconditions

* User authenticated.

## Trigger

Dashboard page opened.

## Main Flow

1. Load analytics.
2. Load statistics.
3. Display:

   * Jobs
   * Candidates
   * Rankings
   * Funnel Metrics

## Alternate Flow

No data available.

* Show empty dashboard.

## Postconditions

* Dashboard displayed.

---

# UC-015 Export Reports

## Description

Recruiter exports hiring reports.

## Primary Actor

Recruiter

## Preconditions

* Rankings available.

## Trigger

Recruiter clicks export.

## Main Flow

1. Select report format.
2. Generate report.
3. Create file.
4. Download report.

Formats:

* PDF
* CSV
* XLSX

## Alternate Flow

Export generation failure.

* Error displayed.

## Postconditions

* Report downloaded.

---

# UC-016 View Candidate Profile

## Description

Recruiter reviews detailed candidate information.

## Primary Actor

Recruiter

## Preconditions

* Candidate exists.

## Trigger

Recruiter selects candidate.

## Main Flow

1. Open profile.
2. View:

   * Resume
   * Skills
   * Experience
   * Scores
   * Summary
   * Missing Skills

## Postconditions

* Candidate profile displayed.

---

# UC-017 System Health Monitoring

## Description

Administrator monitors system status.

## Primary Actor

Administrator

## Preconditions

* Admin logged in.

## Trigger

Admin opens monitoring panel.

## Main Flow

1. Check API health.
2. Check database health.
3. Check Redis health.
4. Check AI service status.

## Postconditions

* System status displayed.

---

# Use Case Summary

| Category             | Count |
| -------------------- | ----- |
| Authentication       | 2     |
| Job Management       | 2     |
| Resume Management    | 3     |
| AI Processing        | 5     |
| Candidate Management | 3     |
| Reporting            | 1     |
| Administration       | 1     |
| Total Use Cases      | 17    |

This document becomes the foundation for API endpoints, service-layer implementation, database design, test cases, and sprint planning.
