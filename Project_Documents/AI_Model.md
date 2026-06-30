# AI Recruitment Automation System (ARAS)

# AI Model Design & Intelligence Architecture

Version: 1.0

Date: June 2026

Document Owner: AI Engineering Team

Document Status: Approved

---

# 1. Purpose

This document defines the AI architecture used in ARAS.

The objective is to build an explainable AI recruitment intelligence system capable of:

* Resume Understanding
* Job Description Understanding
* Candidate Matching
* Candidate Ranking
* Skill Gap Analysis
* Candidate Summarization
* Interview Question Generation

---

# 2. AI Architecture Overview

```text
Resume
    ↓
Resume Parser
    ↓
Candidate Profile
    ↓
Embedding Generator
    ↓
Vector Database

Job Description
    ↓
JD Parser
    ↓
Job Profile
    ↓
Embedding Generator
    ↓
Vector Database

Candidate Vector
      +
Job Vector
      ↓
Matching Engine
      ↓
Ranking Engine
      ↓
AI Evaluation
      ↓
Summary Generator
      ↓
Interview Generator
```

---

# 3. AI Modules

ARAS contains 7 AI modules.

```text
1. Resume Parsing Engine

2. Skill Extraction Engine

3. Job Description Analysis Engine

4. Embedding Engine

5. Candidate Matching Engine

6. Candidate Ranking Engine

7. Recruitment Intelligence Engine
```

---

# 4. Resume Parsing Engine

Purpose:

Convert unstructured resumes into structured candidate profiles.

---

Input

```text
PDF Resume

DOCX Resume
```

---

Output

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "skills": ["Python", "FastAPI"],
  "education": [],
  "experience": []
}
```

---

Libraries

```text
PyMuPDF

pdfplumber

python-docx

re
```

---

Pipeline

```text
Resume

↓

Text Extraction

↓

Text Cleaning

↓

Section Detection

↓

Entity Extraction

↓

JSON Output
```

---

# 5. Skill Extraction Engine

Purpose

Extract technical skills from resumes and job descriptions.

---

Input

```text
Resume Text

Job Description Text
```

---

Method

Dictionary Matching

*

NER Pattern Matching

---

Master Skills Database

```json
{
  "Programming": [
    "Python",
    "Java",
    "C++",
    "JavaScript"
  ],

  "Frontend": [
    "React",
    "Angular"
  ],

  "Backend": [
    "FastAPI",
    "Django",
    "Node.js"
  ],

  "Cloud": [
    "AWS",
    "Azure",
    "GCP"
  ]
}
```

---

Output

```json
{
  "skills": [
    "Python",
    "FastAPI",
    "AWS"
  ]
}
```

---

# 6. Job Description Analysis Engine

Purpose

Extract structured hiring requirements.

---

Input

```text
Job Description
```

---

Extract

```text
Required Skills

Preferred Skills

Experience

Education

Certifications
```

---

Output

```json
{
  "required_skills": [
    "Python",
    "FastAPI"
  ],

  "experience": 3
}
```

---

# 7. Embedding Engine

Purpose

Convert candidates and jobs into vectors.

---

Model

```text
sentence-transformers/all-MiniLM-L6-v2
```

---

Why?

```text
Fast

Small

384 Dimensions

High Semantic Quality
```

---

Input

```text
Candidate Profile
```

---

Output

```text
384-Dimensional Vector
```

---

Storage

```text
pgvector
```

---

# 8. Vector Search Engine

Purpose

Perform semantic candidate-job matching.

---

Algorithm

```text
Cosine Similarity
```

---

Formula

```text
similarity(A,B)

=

A·B

/

(|A| × |B|)
```

---

Output

```text
Semantic Score

0 - 100
```

---

# 9. Candidate Matching Engine

Purpose

Generate candidate suitability scores.

---

Scoring Components

| Component           | Weight |
| ------------------- | ------ |
| Semantic Similarity | 35%    |
| Skill Match         | 25%    |
| Experience Match    | 20%    |
| Education Match     | 10%    |
| AI Evaluation       | 10%    |

---

Final Formula

```text
Final Score

=

0.35 × Semantic

+

0.25 × Skill

+

0.20 × Experience

+

0.10 × Education

+

0.10 × AI Score
```

---

Output

```json
{
  "candidate": "John",
  "score": 88
}
```

---

# 10. Candidate Ranking Engine

Purpose

Rank all candidates for a job.

---

Input

```text
Candidate Scores
```

---

Process

```text
Sort Descending

Assign Rank
```

---

Output

```json
[
  {
    "rank": 1,
    "score": 92
  },
  {
    "rank": 2,
    "score": 87
  }
]
```

---

# 11. AI Candidate Summary Engine

Purpose

Generate recruiter-friendly summaries.

---

Model

```text
Gemini 2.5 Flash
```

---

Prompt Structure

```text
Analyze candidate profile.

Provide:

1. Strengths

2. Weaknesses

3. Missing Skills

4. Recommendation
```

---

Output

```json
{
  "strengths": [
    "Python",
    "FastAPI"
  ],

  "weaknesses": [
    "AWS"
  ],

  "recommendation":
  "Interview Round 1"
}
```

---

# 12. Skill Gap Analysis Engine

Purpose

Identify missing requirements.

---

Input

```text
Required Skills

Candidate Skills
```

---

Process

```text
Set Difference
```

---

Example

Required

```text
Python

FastAPI

Docker

AWS
```

Candidate

```text
Python

FastAPI

Docker
```

Output

```text
Missing:

AWS
```

---

# 13. Interview Question Generator

Purpose

Generate interview questions.

---

Model

```text
Gemini 2.5 Flash
```

---

Generate

```text
Technical Questions

Coding Questions

Behavioral Questions
```

---

Example

```text
1. Explain dependency injection in FastAPI.

2. Difference between PostgreSQL and Redis.
```

---

# 14. Explainable AI Layer

Purpose

Show recruiters why candidates received scores.

---

Output Example

```json
{
  "final_score": 89,

  "reason": {
    "skills": 92,
    "experience": 85,
    "education": 80,
    "semantic": 94
  }
}
```

---

# 15. AI Processing Pipeline

```text
Resume Upload
        ↓
Resume Parsing
        ↓
Skill Extraction
        ↓
Candidate Profile
        ↓
Embedding Generation
        ↓
Vector Storage
        ↓
Job Matching
        ↓
Score Calculation
        ↓
Ranking
        ↓
Summary Generation
        ↓
Interview Questions
```

---

# 16. AI Data Storage

Tables Used

```text
candidate_embeddings

job_embeddings

candidate_scores

ai_summaries

interview_questions
```

---

# 17. AI Performance Targets

| Metric               | Target   |
| -------------------- | -------- |
| Resume Parsing       | < 5 sec  |
| Embedding Generation | < 1 sec  |
| Candidate Ranking    | < 3 sec  |
| Summary Generation   | < 10 sec |
| Interview Questions  | < 10 sec |

---

# 18. AI Monitoring Metrics

Track:

```text
Parsing Accuracy

Skill Extraction Accuracy

Ranking Accuracy

LLM Response Time

Embedding Generation Time
```

---

# 19. Future AI Roadmap

Version 2

```text
RAG-based Candidate Search

Recruiter Copilot

Natural Language Queries

Multi-Agent Recruitment Workflow
```

---

Version 3

```text
Resume Fraud Detection

Experience Verification

AI Interview Agent

Hiring Prediction Models
```

---

# 20. Conclusion

The ARAS AI architecture combines:

* NLP
* Embeddings
* Vector Search
* Explainable Scoring
* LLM Intelligence

to provide recruiters with a transparent, scalable, and modern recruitment intelligence platform.

This architecture is suitable for MVP deployment while remaining extensible for future enterprise AI capabilities.
