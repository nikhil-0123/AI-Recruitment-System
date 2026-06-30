# AI Recruitment Automation System (ARAS)

# User Stories Document

Version: 1.0

Date: June 2026

Project: AI Recruitment Automation System

---

# 1. Introduction

This document defines the user stories for the AI Recruitment Automation System (ARAS).

User stories describe system behavior from the perspective of recruiters, HR administrators, and hiring managers.

Each story follows the format:

As a [user]

I want [goal]

So that [benefit]

---

# Epic 1: Authentication & User Management

## US-001 Recruiter Registration

As a recruiter,

I want to create an account,

So that I can access the recruitment platform.

Acceptance Criteria:

* Registration form is available.
* Email is unique.
* Password is securely stored.
* User receives success confirmation.

Priority: High

---

## US-002 Recruiter Login

As a recruiter,

I want to log into the platform,

So that I can manage hiring activities.

Acceptance Criteria:

* Valid credentials allow login.
* Invalid credentials show error.
* JWT token is generated.

Priority: High

---

## US-003 Password Reset

As a recruiter,

I want to reset my password,

So that I can recover account access.

Acceptance Criteria:

* Password reset email sent.
* Secure reset token generated.
* New password successfully updated.

Priority: Medium

---

## US-004 Logout

As a recruiter,

I want to logout,

So that my account remains secure.

Acceptance Criteria:

* Session terminated.
* Tokens invalidated.

Priority: High

---

# Epic 2: Job Management

## US-005 Create Job Posting

As a recruiter,

I want to create a job description,

So that candidates can be evaluated against it.

Acceptance Criteria:

* Job title entered.
* Description entered.
* Job saved successfully.

Priority: High

---

## US-006 Edit Job Posting

As a recruiter,

I want to update job details,

So that requirements remain accurate.

Acceptance Criteria:

* Existing job editable.
* Changes saved.

Priority: Medium

---

## US-007 Delete Job Posting

As a recruiter,

I want to delete a job,

So that outdated positions are removed.

Acceptance Criteria:

* Confirmation required.
* Job removed successfully.

Priority: Medium

---

## US-008 View Job Details

As a recruiter,

I want to view job information,

So that I can verify requirements.

Acceptance Criteria:

* Job information displayed.
* Skills visible.

Priority: High

---

# Epic 3: Resume Management

## US-009 Upload Single Resume

As a recruiter,

I want to upload a resume,

So that it can be evaluated.

Acceptance Criteria:

* PDF supported.
* DOCX supported.
* Upload confirmation displayed.

Priority: High

---

## US-010 Bulk Resume Upload

As a recruiter,

I want to upload multiple resumes,

So that I can process many candidates at once.

Acceptance Criteria:

* Multiple file upload supported.
* Progress displayed.
* Upload results shown.

Priority: High

---

## US-011 View Uploaded Resumes

As a recruiter,

I want to see uploaded resumes,

So that I can manage candidate data.

Acceptance Criteria:

* Resume list displayed.
* Search available.

Priority: High

---

## US-012 Delete Resume

As a recruiter,

I want to remove a resume,

So that outdated records are cleaned.

Acceptance Criteria:

* Resume deleted successfully.
* Related records updated.

Priority: Medium

---

# Epic 4: Resume Parsing

## US-013 Extract Candidate Information

As a recruiter,

I want candidate information extracted automatically,

So that I do not manually read resumes.

Acceptance Criteria:

System extracts:

* Name
* Email
* Phone
* Education
* Skills
* Experience

Priority: High

---

## US-014 Extract Projects

As a recruiter,

I want candidate projects identified,

So that I can evaluate practical experience.

Acceptance Criteria:

* Projects extracted.
* Project titles displayed.

Priority: Medium

---

## US-015 Extract Certifications

As a recruiter,

I want certifications extracted,

So that I can evaluate qualifications.

Acceptance Criteria:

* Certifications detected.
* Certifications displayed.

Priority: Medium

---

# Epic 5: Job Description Analysis

## US-016 Extract Required Skills

As a recruiter,

I want required skills automatically identified,

So that job requirements become structured.

Acceptance Criteria:

* Skills extracted.
* Skills categorized.

Priority: High

---

## US-017 Extract Experience Requirements

As a recruiter,

I want experience requirements extracted,

So that candidates can be compared properly.

Acceptance Criteria:

* Years of experience identified.

Priority: High

---

# Epic 6: Candidate Matching

## US-018 Calculate Skill Match Score

As a recruiter,

I want the system to calculate skill match percentage,

So that candidate suitability is measurable.

Acceptance Criteria:

* Score displayed.
* Score range 0–100.

Priority: High

---

## US-019 Calculate Experience Match Score

As a recruiter,

I want experience comparison performed,

So that relevant candidates are prioritized.

Acceptance Criteria:

* Experience score generated.

Priority: High

---

## US-020 Calculate Education Match Score

As a recruiter,

I want education requirements checked,

So that qualification fit is measured.

Acceptance Criteria:

* Education score generated.

Priority: Medium

---

## US-021 Calculate Semantic Similarity

As a recruiter,

I want AI-based semantic matching,

So that context is considered.

Acceptance Criteria:

* Sentence Transformer similarity generated.

Priority: High

---

# Epic 7: Candidate Ranking

## US-022 Generate Overall Score

As a recruiter,

I want a final candidate score,

So that candidates can be compared objectively.

Acceptance Criteria:

* Final score generated.
* Range 0–100.

Priority: High

---

## US-023 Generate Candidate Rank

As a recruiter,

I want candidates ranked,

So that top candidates are visible first.

Acceptance Criteria:

* Ranking order generated.
* Rank numbers displayed.

Priority: High

---

## US-024 Categorize Candidates

As a recruiter,

I want candidates grouped by recommendation level,

So that shortlisting becomes easier.

Acceptance Criteria:

Categories:

* Highly Recommended
* Recommended
* Consider
* Rejected

Priority: High

---

# Epic 8: AI Features

## US-025 Generate Candidate Summary

As a recruiter,

I want AI-generated summaries,

So that I can quickly understand candidates.

Acceptance Criteria:

Summary contains:

* Strengths
* Weaknesses
* Recommendations

Priority: High

---

## US-026 Generate Skill Gap Analysis

As a recruiter,

I want missing skills identified,

So that training needs are visible.

Acceptance Criteria:

* Missing skills displayed.

Priority: High

---

## US-027 Generate Interview Questions

As a recruiter,

I want interview questions automatically generated,

So that interviews are more effective.

Acceptance Criteria:

Generate:

* Technical Questions
* Coding Questions
* Behavioral Questions

Priority: Medium

---

# Epic 9: Dashboard

## US-028 View Recruitment Dashboard

As a recruiter,

I want a dashboard,

So that I can monitor recruitment activity.

Acceptance Criteria:

Display:

* Jobs
* Candidates
* Rankings

Priority: High

---

## US-029 View Analytics

As a recruiter,

I want recruitment analytics,

So that hiring performance is measurable.

Acceptance Criteria:

Display:

* Hiring Funnel
* Candidate Statistics
* Score Distribution

Priority: Medium

---

# Epic 10: Reporting

## US-030 Export PDF Report

As a recruiter,

I want PDF reports,

So that candidate evaluations can be shared.

Acceptance Criteria:

* PDF generated.
* Download available.

Priority: High

---

## US-031 Export CSV Report

As a recruiter,

I want CSV exports,

So that data can be analyzed externally.

Acceptance Criteria:

* CSV generated.
* Download available.

Priority: Medium

---

## US-032 Export Excel Report

As a recruiter,

I want Excel reports,

So that HR teams can perform advanced analysis.

Acceptance Criteria:

* XLSX generated.
* Download available.

Priority: Medium

---

# Epic 11: Security & Administration

## US-033 Role-Based Access Control

As an administrator,

I want role-based permissions,

So that users access only authorized features.

Priority: High

---

## US-034 Audit Logging

As an administrator,

I want system activities recorded,

So that security events can be tracked.

Priority: Medium

---

## US-035 Monitor System Health

As an administrator,

I want health monitoring,

So that service availability is maintained.

Priority: Medium

---

# User Story Summary

Total User Stories: 35

High Priority: 22

Medium Priority: 13

Low Priority: 0

Release 1.0 Scope:

US-001 to US-030

Release 2.0 Scope:

US-031 to US-035
