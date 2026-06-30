# AI Recruitment Automation System (ARAS)

# UI/UX Wireframes & Design Specification

Version: 1.0

Date: June 2026

Frontend Stack:

* React.js
* TypeScript
* TailwindCSS
* React Query
* Recharts

Document Status: Approved

---

# 1. UI Design Goals

The interface should be:

* Simple
* Professional
* Recruiter Friendly
* Fast
* Mobile Responsive
* Enterprise Inspired

Inspired By:

* LinkedIn Recruiter
* Greenhouse
* Workday
* Notion
* Linear

---

# 2. User Flow

Primary Flow:

```text
Login
  ↓
Dashboard
  ↓
Create Job
  ↓
Upload Resumes
  ↓
Resume Processing
  ↓
Candidate Ranking
  ↓
Candidate Analysis
  ↓
Shortlisting
  ↓
Report Export
```

Secondary Flow:

```text
Dashboard
   ↓
Analytics
   ↓
Reports
```

---

# 3. Application Navigation

Sidebar Navigation

```text
📊 Dashboard

💼 Jobs

📄 Resumes

👥 Candidates

🏆 Rankings

🤖 AI Insights

📈 Analytics

📑 Reports

⚙ Settings
```

Top Navigation

```text
Search Bar

Notifications

User Profile

Logout
```

---

# 4. Authentication Screens

---

## Login Page

Route

```text
/login
```

Wireframe

```text
+--------------------------------------+
|                                      |
|     AI Recruitment Automation        |
|                                      |
|     Email                            |
|     [______________]                 |
|                                      |
|     Password                         |
|     [______________]                 |
|                                      |
|     [ Login ]                        |
|                                      |
|     Forgot Password?                 |
|                                      |
+--------------------------------------+
```

Components

```text
LoginForm

EmailInput

PasswordInput

SubmitButton
```

---

## Register Page

Route

```text
/register
```

Fields

```text
Full Name

Email

Password

Confirm Password
```

---

# 5. Dashboard Page

Route

```text
/dashboard
```

Purpose

Recruiter overview.

---

Layout

```text
+---------------------------------------------------+
| Sidebar          | Dashboard                      |
|                  |                                |
|                  | Total Jobs                     |
|                  | Total Candidates               |
|                  | Shortlisted                    |
|                  | Rejected                       |
|                  |                                |
|                  | Analytics Charts               |
|                  |                                |
+---------------------------------------------------+
```

---

Dashboard Cards

```text
Total Jobs

Total Candidates

Shortlisted

Rejected
```

---

Charts

```text
Candidate Funnel

Score Distribution

Top Skills

Hiring Trend
```

Components

```text
StatsCard

AnalyticsChart

TopSkillsChart

HiringTrendChart
```

---

# 6. Job Management Screen

Route

```text
/jobs
```

Purpose

Manage job postings.

---

Layout

```text
+---------------------------------------------------+
| Jobs                                               |
|---------------------------------------------------|
| Search                                             |
|                                                    |
| + Create Job                                       |
|                                                    |
| Job List                                           |
|                                                    |
+---------------------------------------------------+
```

---

Job Table

Columns

```text
Title

Status

Candidates

Created Date

Actions
```

Actions

```text
View

Edit

Delete
```

---

# 7. Create Job Screen

Route

```text
/jobs/create
```

Layout

```text
Job Title

[________________]

Experience Required

[________________]

Education Required

[________________]

Job Description

[________________________]

[ Save Job ]
```

Components

```text
JobForm

SkillsInput

ExperienceInput

DescriptionEditor
```

---

# 8. Resume Upload Screen

Route

```text
/resumes/upload
```

Purpose

Upload candidate resumes.

---

Layout

```text
+------------------------------------+
| Upload Resumes                     |
|                                    |
| Drag & Drop Files                  |
|                                    |
| [ Upload ]                         |
|                                    |
+------------------------------------+
```

Supported Formats

```text
PDF

DOCX
```

---

Upload Status

```text
Uploaded

Processing

Failed

Completed
```

---

Components

```text
Dropzone

FileUploader

UploadProgress

ResumeList
```

---

# 9. Candidate List Screen

Route

```text
/candidates
```

Purpose

View all candidates.

---

Layout

```text
Search

Filters

------------------------------------

Candidate Table

------------------------------------
```

Columns

```text
Name

Skills

Experience

Score

Status
```

Filters

```text
Skills

Experience

Education

Rank
```

---

# 10. Candidate Details Screen

Route

```text
/candidates/:id
```

Purpose

Detailed candidate evaluation.

---

Layout

```text
+------------------------------------------------+
| Candidate Profile                              |
|------------------------------------------------|
| Name                                           |
| Email                                          |
| Experience                                     |
|                                                |
| Skills                                          |
|                                                |
| AI Summary                                     |
|                                                |
| Score Breakdown                                |
|                                                |
| Missing Skills                                 |
|                                                |
+------------------------------------------------+
```

---

Sections

```text
Resume Information

Skills

Experience

Projects

AI Summary

Score Breakdown

Interview Questions

Skill Gap Analysis
```

---

# 11. Ranking Screen

Route

```text
/rankings
```

Purpose

Display ranked candidates.

---

Layout

```text
+------------------------------------------------+
| Candidate Rankings                             |
|------------------------------------------------|
| Rank | Name | Score | Recommendation          |
|                                                |
+------------------------------------------------+
```

---

Columns

```text
Rank

Candidate

Final Score

Recommendation
```

Recommendation Categories

```text
Highly Recommended

Recommended

Consider

Rejected
```

---

# 12. AI Insights Screen

Route

```text
/ai-insights
```

Purpose

Display AI-generated intelligence.

---

Cards

```text
Candidate Summary

Skill Gap Analysis

Interview Questions
```

---

Layout

```text
+---------------------------------------------+
| Candidate Summary                           |
+---------------------------------------------+

+---------------------------------------------+
| Skill Gap Analysis                          |
+---------------------------------------------+

+---------------------------------------------+
| Interview Questions                         |
+---------------------------------------------+
```

---

# 13. Analytics Dashboard

Route

```text
/analytics
```

Purpose

Recruitment insights.

---

Charts

```text
Candidate Funnel

Hiring Trends

Top Skills

Application Sources

Candidate Distribution
```

---

Layout

```text
+----------------------------------------------+
| Analytics Dashboard                          |
|                                              |
| Funnel Chart                                 |
|                                              |
| Trend Chart                                  |
|                                              |
| Skills Chart                                 |
|                                              |
+----------------------------------------------+
```

---

# 14. Reports Screen

Route

```text
/reports
```

Purpose

Export recruitment reports.

---

Layout

```text
+---------------------------------------------+
| Reports                                     |
|---------------------------------------------|
| PDF                                         |
| CSV                                         |
| Excel                                       |
|                                             |
| Generate Report                             |
+---------------------------------------------+
```

Buttons

```text
Download PDF

Download CSV

Download XLSX
```

---

# 15. Settings Screen

Route

```text
/settings
```

Sections

```text
Profile

Password

Notification Settings

Account Preferences
```

---

# 16. Design System

Typography

```text
Font:
Inter
```

---

Colors

```text
Primary:
#2563EB

Secondary:
#0F172A

Success:
#22C55E

Warning:
#F59E0B

Danger:
#EF4444
```

---

Border Radius

```text
12px
```

---

Spacing

```text
8px Grid System
```

---

# 17. Reusable Components

Core Components

```text
Button

Input

Textarea

Select

Modal

Drawer

Table

Card

Badge

Tooltip

Pagination
```

Business Components

```text
JobCard

CandidateCard

ResumeUploader

RankingTable

ScoreBreakdown

AISummaryCard

SkillGapCard

InterviewQuestionCard

AnalyticsWidget
```

---

# 18. Responsive Design

Desktop

```text
≥ 1024px
```

Tablet

```text
768px – 1023px
```

Mobile

```text
≤ 767px
```

Behavior

```text
Sidebar → Drawer

Tables → Scrollable

Charts → Responsive
```

---

# 19. Page Map

```text
Login

Register

Dashboard

Jobs
 ├─ List
 ├─ Create
 └─ Details

Resumes
 ├─ Upload
 └─ List

Candidates
 ├─ List
 └─ Details

Rankings

AI Insights

Analytics

Reports

Settings
```

---

# 20. UI Development Priority

Sprint 1

```text
Login

Dashboard

Jobs

Resume Upload
```

Sprint 2

```text
Candidates

Rankings

AI Insights
```

Sprint 3

```text
Analytics

Reports

Settings
```

---

# 21. Final UX Principles

The UI must prioritize:

* Recruiter productivity
* Minimal clicks
* Fast navigation
* Clear candidate insights
* Explainable AI outputs

Every screen should answer:

1. What is the candidate's score?
2. Why did the candidate receive that score?
3. Should the recruiter interview this candidate?

If those three questions are answered quickly, the UI is successful.

Document Status: Approved
