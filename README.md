# AI Recruitment System (ARAS)

<div align="center">

### 🚀 Production-Grade AI-Powered Recruitment Platform

**Parse • Match • Rank • Recommend • Hire**

An end-to-end recruitment platform that leverages Artificial Intelligence, Natural Language Processing (NLP), semantic search, and explainable ranking algorithms to automate candidate screening and hiring workflows.

---

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

# Overview

AI Recruitment System (ARAS) is a modern recruitment platform that automates the hiring pipeline using AI-powered resume analysis, semantic candidate matching, explainable ranking, and intelligent recommendations.

Instead of manually reviewing hundreds of resumes, recruiters upload a Job Description and candidate resumes. The system extracts structured information, evaluates candidate suitability using multiple scoring strategies, and generates transparent rankings with detailed explanations.

---

# Features

## Resume Processing

* PDF Resume Upload
* OCR-ready architecture
* Resume Parsing
* Skill Extraction
* Experience Extraction
* Education Detection
* Contact Information Extraction
* Duplicate Detection

---

## Job Management

* Create Jobs
* Update Jobs
* Delete Jobs
* Job Requirements
* Required Skills
* Preferred Skills
* Experience Requirements
* Education Requirements

---

## AI Candidate Ranking

* Semantic Matching
* Skill Matching
* Experience Score
* Education Score
* Keyword Score
* Weighted Ranking
* Explainable AI
* Confidence Score

---

## Recommendation Engine

* Best Candidate Detection
* Skill Gap Analysis
* Missing Skills
* Candidate Strengths
* Improvement Suggestions
* Hiring Recommendation

---

## Dashboard

* Recruiter Dashboard
* Candidate Statistics
* Ranking Dashboard
* Processing Status
* Analytics
* Search & Filters

---

# System Architecture

```
Frontend (React)

        │

FastAPI Backend

        │

Business Services

        │

Repository Layer

        │

PostgreSQL Database

        │

AI Services

 ├── Resume Parser
 ├── Embedding Engine
 ├── Ranking Engine
 ├── Recommendation Engine
 └── Validation Engine
```

---

# Technology Stack

## Backend

* Python
* FastAPI
* SQLAlchemy
* Alembic
* PostgreSQL
* Pydantic

## AI / ML

* Sentence Transformers
* HuggingFace Transformers
* spaCy
* Scikit-learn
* ONNX Runtime
* NumPy
* Pandas

## Frontend

* React
* TypeScript
* Vite
* TailwindCSS
* Axios

## DevOps

* Docker
* Docker Compose
* GitHub Actions
* Nginx

---

# Project Structure

```
AI-Recruitment-System

backend/
    app/
        api/
        core/
        models/
        repositories/
        schemas/
        services/
        workers/
        utils/

frontend/
    src/

deployment/
    docker/

docs/

tests/

Project_Documents/

README.md
```

---

# AI Pipeline

```
Upload Resume

        │

Extract Text

        │

Parse Resume

        │

Normalize Data

        │

Generate Embeddings

        │

Calculate Scores

        │

Rank Candidates

        │

Generate Recommendations

        │

Display Results
```

---

# Candidate Scoring

The final ranking score combines multiple evaluation metrics.

```
Final Score =

40% Semantic Similarity

25% Skills Match

15% Experience Match

10% Education Match

5% Certifications

5% Additional Factors
```

All rankings include explainable scoring so recruiters understand why candidates were recommended.

---

# API Modules

* Authentication
* Users
* Jobs
* Candidates
* Resume Upload
* Resume Parsing
* Candidate Ranking
* Recommendations
* Dashboard
* Analytics
* Health Check

---

# Security

* JWT Authentication
* Role-Based Access Control (RBAC)
* Password Hashing
* Input Validation
* SQL Injection Protection
* Rate Limiting
* Audit Logs
* Secure File Upload
* HTTPS Ready

---

# Performance

* Async FastAPI
* Background Workers
* Database Indexing
* Connection Pooling
* Pagination
* Caching
* Batch Resume Processing
* Parallel Ranking

---

# Testing

* Unit Tests
* Integration Tests
* API Tests
* Repository Tests
* Service Tests
* Performance Tests

---

# Development Roadmap

### Phase 1

* Authentication
* Job Management
* Resume Upload
* Resume Parsing

### Phase 2

* Candidate Ranking
* Recommendation Engine
* Explainable AI

### Phase 3

* Analytics Dashboard
* Email Notifications
* Interview Scheduling

### Phase 4

* LLM Resume Insights
* AI Interview Assistant
* Multi-language Resume Support

---

# Future Enhancements

* Resume Chat
* AI Career Advisor
* ATS Score Generator
* Candidate Skill Graph
* Organization Dashboard
* AI Resume Improvement
* Voice Interview Analysis
* Video Interview Intelligence

---

# Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push the branch
5. Open a Pull Request

---

# License

This project is licensed under the MIT License.

---

# Author

**Nikhil Chaugule**

Bachelor of Engineering (Artificial Intelligence & Data Science)

Passionate about AI, Machine Learning, Backend Engineering, Distributed Systems, and Production-Grade Software Development.

---

⭐ If you found this project useful, consider giving it a star!
