# AI Recruitment Automation System (ARAS)

# Data Governance

Document Number: 15

Version: 1.0

Date: June 2026

Document Owner: Security Lead + Backend Lead + QA Engineer

Document Status: Approved for Implementation

Scope: ARAS Version 1.0 data handling, classification, storage, retention, access, auditability, and deletion controls.

---

# 1. Purpose

This document defines how ARAS manages data throughout its lifecycle in Version 1.

The objectives are:

* Protect candidate and recruiter data
* Ensure reliable ownership and lifecycle control of uploaded resumes and derived data
* Define retention, deletion, and audit rules
* Support secure AI processing
* Keep governance lightweight enough for the 40-day roadmap

This document does **not** introduce multi-tenancy, enterprise compliance frameworks, or external governance platforms. It governs a single ARAS deployment using the approved architecture.

---

# 2. Governance Principles

ARAS V1 follows these governance principles:

1. PostgreSQL is the source of truth for structured data.
2. S3-compatible storage is the source of truth for resume and export files.
3. Derived AI data must be traceable to its source entities.
4. Data access must be role-based and least-privilege.
5. Resume and candidate data must not be exposed outside authenticated workflows.
6. Data retained must be limited to what ARAS needs to deliver V1 functionality.
7. Every critical data mutation must be auditable.

---

# 3. Data Domains

ARAS data is divided into the following domains:

| Domain ID | Domain | Examples |
| --------- | ------ | -------- |
| DG-01 | Identity Data | user name, email, password hash, role |
| DG-02 | Resume Source Data | uploaded PDF/DOCX files, file metadata |
| DG-03 | Candidate Profile Data | name, email, phone, education, skills, experience |
| DG-04 | Job Data | job title, description, required skills, creator |
| DG-05 | Derived Scoring Data | skill_score, semantic_score, final_score, rank |
| DG-06 | AI Output Data | summaries, interview questions, skill gaps |
| DG-07 | Operational Data | async job status, logs, audit logs |
| DG-08 | Export Data | generated PDF, CSV, XLSX reports |

---

# 4. Data Classification

ARAS V1 uses a four-level classification model.

| Classification | Description | Examples | Controls |
| -------------- | ----------- | -------- | -------- |
| Public | Safe for public disclosure | Product logo, static UI assets | Minimal |
| Internal | General operational metadata | job status IDs, non-sensitive metrics | Auth required |
| Confidential | Business-sensitive platform data | job descriptions, recruiter analytics | Role-based access |
| Restricted | Personal and sensitive candidate/user data | resumes, phone, email, summary outputs | Strict access + audit |

## Classification Mapping

| Data Element | Classification |
| ------------ | -------------- |
| user.email | Restricted |
| user.password_hash | Restricted |
| resume.file_url | Restricted |
| parsed_resume_text | Restricted |
| candidate.phone | Restricted |
| candidate.email | Restricted |
| candidate.skills | Confidential |
| candidate_scores.final_score | Confidential |
| ai_summaries.summary_text | Restricted |
| interview_questions | Confidential |
| analytics aggregate counts | Internal |
| system logs with IDs only | Internal |

---

# 5. System of Record

## Authoritative Sources

| Data Type | Source of Record |
| --------- | ---------------- |
| Users | PostgreSQL |
| Jobs | PostgreSQL |
| Candidates | PostgreSQL |
| Scores | PostgreSQL |
| AI summaries | PostgreSQL |
| Interview questions | PostgreSQL |
| Async job metadata | PostgreSQL |
| Resume files | S3-compatible storage |
| Report files | S3-compatible storage |
| Cache entries | Redis (non-authoritative) |

Redis must never be treated as permanent storage for candidate or scoring information.

---

# 6. Data Lineage Rules

Every derived record in ARAS must be traceable back to its source.

## Required Lineage

| Derived Record | Must Reference |
| -------------- | -------------- |
| candidate record | originating resume_id |
| candidate_skills | candidate_id |
| candidate_scores | candidate_id + job_id |
| ai_summary | candidate_id + job_id |
| interview_questions | candidate_id + job_id |
| report | generated_by + filter context |
| async_jobs | entity_type + entity_id + requested_by |

## Governance Requirement

No AI-derived output may exist without the source candidate and job relationship being identifiable.

This rule supports auditability, deletion, and regeneration.

---

# 7. Data Lifecycle

## 7.1 Resume Lifecycle

```text
Uploaded
  ↓
Validated
  ↓
Stored in S3
  ↓
Parsed
  ↓
Candidate profile created/updated
  ↓
Embedding generated
  ↓
Used in ranking / AI outputs
  ↓
Retained until deletion or retention expiry
```

## 7.2 Candidate Data Lifecycle

```text
Created from parsed resume
  ↓
Enriched with skills / experience
  ↓
Scored against job(s)
  ↓
Summarized / questioned by AI
  ↓
Exported in reports
  ↓
Retained until deletion or retention expiry
```

## 7.3 Export Lifecycle

```text
Requested by authorized user
  ↓
Generated asynchronously
  ↓
Stored in S3
  ↓
Available through authenticated download
  ↓
Deleted after retention period
```

---

# 8. Storage Rules

## 8.1 PostgreSQL Storage Rules

PostgreSQL stores:

* User accounts
* Jobs
* Candidates
* Candidate skills
* Candidate scores
* Embedding vectors
* AI summaries
* Interview questions
* Reports metadata
* Audit logs
* Async job records

### Requirements

1. All primary keys use UUID.
2. All tables include created_at and updated_at where applicable.
3. All business-critical relations use foreign keys.
4. pgvector stores 384-dimensional embeddings only.
5. Sensitive free-text fields must be minimized.

## 8.2 S3 Storage Rules

S3-compatible storage stores:

* Uploaded resume files
* Generated report files

### Requirements

1. Object keys must be server-generated, not user-generated.
2. Bucket access must be private.
3. Files are accessed only through authenticated backend endpoints or signed URLs with short expiry.
4. Resume files and report files must be stored in separate logical prefixes.

### Example Key Structure

```text
resumes/{resume_id}/{stored_filename}.pdf
reports/{report_id}/{stored_filename}.xlsx
```

## 8.3 Redis Storage Rules

Redis stores:

* Celery broker messages
* Cache entries for repeated summary/question requests
* Short-lived operational data only

Redis must not store:

* Full resume text
* Password hashes
* Permanent candidate records
* Long-term audit records

---

# 9. Access Control Rules

ARAS uses JWT + RBAC as defined in the approved architecture.

## V1 Roles

| Role | Access Scope |
| ---- | ------------ |
| Admin | Full system access |
| Recruiter | Jobs, resumes, candidates, rankings, summaries, questions, reports |
| Hiring Manager | Read-only access to candidates, rankings, summaries, interview questions |

## Data Access Matrix

| Data Domain | Admin | Recruiter | Hiring Manager |
| ----------- | ----- | --------- | -------------- |
| Users | Full | Self only | Self only |
| Jobs | Full | Full | Read |
| Resumes | Full | Full | No direct raw file access by default |
| Candidates | Full | Full | Read |
| Candidate Scores | Full | Full | Read |
| AI Summaries | Full | Full | Read |
| Interview Questions | Full | Full | Read |
| Reports | Full | Full | Read if generated for accessible jobs |
| Audit Logs | Full | No | No |

## Governance Rules

1. Hiring Managers should not be given raw resume file download access by default in V1.
2. Only Admin can view audit logs.
3. All access to restricted data must pass through authenticated backend APIs.
4. Direct object-store public links are prohibited.

---

# 10. Data Minimization Rules

To keep V1 realistic and reduce privacy risk:

1. ARAS stores only fields required for recruitment workflows.
2. ARAS does not collect government IDs, birth dates, salary history, or demographic categories in V1.
3. Resume raw text must be used only for parsing, embedding, and AI generation.
4. AI prompts must include only the minimum candidate and job information needed.
5. Do not duplicate candidate PII across unnecessary tables.

## Recommended Candidate Core Fields

```text
name
email
phone
experience_years
education
linkedin_url
skills
resume_id
```

Additional custom profile enrichment is out of scope for V1.

---

# 11. Data Retention Policy

ARAS V1 uses simple fixed retention rules.

## Retention Schedule

| Data Type | Retention Period | Action After Expiry |
| --------- | ---------------- | ------------------- |
| User accounts | Until manual deactivation/deletion | Soft delete or deactivate |
| Jobs | 365 days after closure | Review or archive |
| Resume files | 180 days from upload | Delete object + metadata flag |
| Candidate profile data | 180 days from last linked resume upload or job activity | Delete or anonymize |
| Candidate scores | 180 days | Delete with candidate/job cleanup |
| AI summaries | 180 days | Delete |
| Interview questions | 180 days | Delete |
| Generated reports | 30 days | Delete object |
| Async job records | 90 days | Archive/delete operationally |
| Audit logs | 180 days minimum | Archive or delete |
| Application logs | 30 days | Rotate/delete |

## V1 Enforcement Model

Retention enforcement may be run manually or via scheduled cleanup task after launch. Automatic cleanup is recommended but not a release blocker if documented operationally.

---

# 12. Deletion Rules

Deletion must be controlled and auditable.

## 12.1 Resume Deletion

When a resume is deleted:

1. Delete S3 object
2. Mark resume record as deleted or remove per implementation choice
3. Trigger cleanup of derived artifacts only if no other active dependency exists
4. Write audit log entry

## 12.2 Candidate Deletion

When a candidate is deleted:

1. Delete candidate_scores rows
2. Delete ai_summaries rows
3. Delete interview_questions rows
4. Delete candidate_skills rows
5. Delete embedding row
6. Delete candidate record
7. Delete linked resume file if no retention exception applies
8. Write audit log entry

## 12.3 Report Deletion

When a report expires or is deleted:

1. Delete S3 object
2. Update reports record status
3. Write audit log entry

---

# 13. Update and Correction Rules

Candidate and job data may need correction after parsing or manual review.

## Governance Rules

1. Manual corrections to candidate fields are allowed for authorized users.
2. Manual changes must update `updated_at`.
3. Important corrections should be audited, especially to candidate PII and ranking-relevant fields.
4. If ranking-relevant fields change, ranking should be regenerated for related jobs.

## Ranking-Relevant Fields

```text
skills
experience_years
education
job required skills
job experience requirement
job education requirement
```

---

# 14. Audit Logging Requirements

ARAS already includes audit logging in the architecture. This document defines minimum audited events.

## Events That Must Be Audited

| Event Category | Examples |
| -------------- | -------- |
| Authentication | login, logout, failed login, token refresh |
| User management | profile update, role change |
| Job management | create, update, delete |
| Resume operations | upload, delete, parse failure |
| Candidate operations | create from parse, update, delete |
| Ranking operations | ranking generation requested, completed, failed |
| AI operations | summary generated, fallback used, questions generated |
| Export operations | report generated, downloaded, deleted |
| Governance actions | retention cleanup, manual deletion |

## Minimum Audit Fields

```text
audit_log.id
audit_log.actor_user_id
audit_log.action
audit_log.entity_type
audit_log.entity_id
audit_log.old_value (optional JSON)
audit_log.new_value (optional JSON)
audit_log.ip_address
audit_log.created_at
```

Sensitive full resume text must never be written into audit logs.

---

# 15. Logging and Privacy Rules

Operational logs must support debugging without leaking sensitive content.

## Allowed in Logs

* UUIDs
* status values
* timing values
* normalized error codes
* queue/job IDs

## Prohibited in Logs

* password hashes
* access tokens
* full resume text
* full AI prompts
* personal phone numbers
* exported file contents

## Logging Example

Safe:

```json
{
  "event": "resume_parse_failed",
  "resume_id": "uuid",
  "error_code": "PARSE_CORRUPTED_FILE",
  "status": "FAILED"
}
```

Unsafe:

```json
{
  "resume_text": "<entire resume contents>",
  "jwt": "..."
}
```

---

# 16. AI Data Governance Rules

AI-generated content must be governed because it influences hiring decisions.

## Rules

1. AI outputs are assistive, not authoritative.
2. Final hiring decisions remain with human users.
3. AI summaries and interview questions must be traceable to candidate and job IDs.
4. Fallback-generated outputs must be marked with `is_fallback = true`.
5. Invalid AI output must not be persisted.
6. Prompt templates must be version-controlled in the repository.
7. AI output regeneration is allowed and should replace prior output only when requested or when underlying source data changes.

## Required Metadata for AI Outputs

| Table | Metadata Required |
| ----- | ----------------- |
| ai_summaries | candidate_id, job_id, is_fallback, created_at |
| interview_questions | candidate_id, job_id, created_at |

Prompt text itself does not need to be stored in the database for V1, but prompt files must remain version-controlled.

---

# 17. Export Governance

Reports contain candidate and scoring data and must be handled carefully.

## Rules

1. Report generation requires authentication.
2. Report download requires authentication.
3. Reports must be linked to the generating user.
4. Reports expire after retention period.
5. Report file names should be system-generated.
6. Audit log entry required for report generation and download.

## Minimum Report Metadata

| Field | Purpose |
| ----- | ------- |
| report_id | Unique identifier |
| report_type | PDF / CSV / XLSX |
| generated_by | User responsible |
| file_key | S3 object reference |
| status | generated / failed / deleted |
| created_at | lifecycle tracking |

---

# 18. Backup and Recovery Rules

ARAS V1 must support practical recovery without over-engineering.

## PostgreSQL

* Daily automated backup recommended
* Pre-release restore test required
* Backups retained for at least 7 days in non-production, 30 days in production

## S3 Storage

* Versioning preferred if available
* Bucket lifecycle policy recommended for expired exports

## Redis

* No dependency on Redis persistence for core data recovery

## Recovery Priority

1. PostgreSQL
2. Resume files in S3
3. Report files in S3
4. Redis queue/cache recreation

---

# 19. Data Quality Rules

Good governance also requires data quality controls.

## Required Quality Checks

| Entity | Check |
| ------ | ----- |
| User | email unique |
| Job | title required, description required |
| Resume | file type must be PDF/DOCX, size ≤ allowed limit |
| Candidate | email format valid if present |
| Candidate skills | deduplicated normalized names |
| Candidate scores | score values within 0–100 |
| Embeddings | dimension = 384 |
| AI summaries | schema-valid JSON before persistence |
| Interview questions | all categories present |

These checks must be enforced via API validation, service-layer checks, and tests.

---

# 20. Data Ownership and Responsibility

| Responsibility Area | Primary Owner | Secondary Owner |
| ------------------- | ------------- | --------------- |
| User/account data | Backend Lead | Security Lead |
| Resume file storage | Backend Lead | DevOps Lead |
| Candidate and job data | Backend Lead | QA Engineer |
| AI outputs | AI Lead | QA Engineer |
| Audit logs | Security Lead | Backend Lead |
| Retention cleanup | DevOps Lead | Backend Lead |
| Validation and test fixtures | QA Engineer | AI Lead |

---

# 21. Governance Process for V1

To keep governance practical within 40 days, ARAS adopts the following lightweight process:

## Before Development

```text
- Approve this document
- Confirm retention values
- Confirm audit event list
- Confirm async job metadata table requirements
```

## During Development

```text
- Backend enforces validation and access rules
- QA verifies data quality rules in tests
- AI Lead verifies AI output persistence rules
- Security Lead reviews file, log, and access controls
```

## Before Release

```text
- Verify restricted data is not exposed in logs
- Verify report and resume download auth
- Verify deletion actions create audit entries
- Verify retention policy documented operationally
```

---

# 22. Roadmap Alignment

This governance model is intentionally sized for the approved 40-day roadmap.

| Sprint | Days | Governance Deliverables |
| ------ | ---- | ----------------------- |
| Sprint 1 | 6–10 | storage configuration, private bucket setup, logging baseline |
| Sprint 2 | 11–15 | role access rules enforced in auth layer |
| Sprint 3 | 16–20 | resume validation, object key rules, upload audit events |
| Sprint 4 | 21–25 | candidate lineage and parsing audit coverage |
| Sprint 5 | 26–30 | score validation and ranking audit coverage |
| Sprint 6 | 31–35 | AI output governance, fallback markers, prompt version control |
| Sprint 7 | 36–38 | export governance, download auth, retention metadata |
| Sprint 8 | 39–40 | release review, governance checklist sign-off |

This plan does not require new platforms or roles beyond the existing ARAS team.

---

# 23. Required Specification Updates

The following documents should be updated to align with this governance model.

## 08_Database_Design.md

Add or confirm:

```text
- async_jobs table
- ai_summaries.is_fallback column
- reports.status field if missing
- deletion/audit-related status columns as needed
```

## 09_API_Specification.md

Add or confirm:

```text
- authenticated report download contract
- deletion endpoints audit behavior
- standardized restricted-data access rules
```

## 12_Risk_Assessment.md

Add governance references for:

```text
- data leakage risk
- retention enforcement risk
- restricted log exposure risk
```

---

# 24. Release Governance Checklist

Before Day 38 code freeze, the Architecture Review Board must confirm:

```text
[ ] Resume uploads stored in private object storage
[ ] No raw resume text stored in application logs
[ ] Restricted fields protected by authenticated APIs
[ ] Hiring Manager role cannot directly download raw resumes by default
[ ] Candidate scores validated within 0–100
[ ] AI summaries marked with is_fallback when fallback used
[ ] Report downloads authenticated and audited
[ ] Audit events implemented for required categories
[ ] Retention schedule documented for operations team
[ ] Backup and restore procedure verified
[ ] Redis not used as system of record for core data
```

---

# 25. Conclusion

This data governance document provides a complete and implementation-ready framework for handling ARAS V1 data securely and consistently without expanding project scope.

It uses the approved architecture, avoids multi-tenancy, avoids compliance-heavy overhead, and focuses on the practical controls required for resume files, candidate data, AI outputs, reports, logs, retention, and auditability. The model is achievable within the 40-day roadmap and should be treated as the operational policy baseline for ARAS development and release.

