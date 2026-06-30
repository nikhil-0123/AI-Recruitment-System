# AI Recruitment Automation System (ARAS)

> An AI-powered recruitment platform that automates resume screening, candidate ranking, skill gap analysis, and recruitment intelligence using Explainable AI (XAI), semantic search, and Large Language Models.

---

## Project Status

**Current Phase:** Day 1–3 Verification (Audit)

**Version:** v0.1.0

**Branch:** `audit/day1-day3`

**Development Status:**

- ✅ Project Foundation
- ✅ Backend Architecture
- ✅ Database Models
- ✅ Documentation
- 🔄 Day 1–3 Verification
- ⏳ Day 4 Development

---

# Features

## Current (Implemented)

- FastAPI Backend Foundation
- React + TypeScript Frontend
- PostgreSQL Database
- SQLAlchemy ORM
- Alembic Migrations
- Repository Pattern
- Clean Architecture
- Modular AI Engine
- Docker Support
- GitHub Actions CI
- Comprehensive Project Documentation

## Planned

- Resume Parsing
- Job Description Analysis
- Semantic Candidate Matching
- AI Candidate Ranking
- Skill Gap Analysis
- Explainable AI (XAI)
- AI Candidate Summaries
- Interview Question Generation
- Recruiter Dashboard
- Analytics & Reports

---

# Technology Stack

## Backend

- Python 3.12+
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pydantic

## Frontend

- React
- TypeScript
- Vite

## AI

- Sentence Transformers
- Gemini API
- pgvector
- PyMuPDF
- pdfplumber

## DevOps

- Docker
- Docker Compose
- GitHub Actions

---

# Repository Structure

```text
AI-Recruitment-System/
│
├── ai_engine/
├── backend/
├── frontend/
├── deployment/
├── docs/
├── tests/
│
├── CONTRIBUTING.md
├── Makefile
└── README.md
```

---

# Documentation

## Requirements

- Project Vision
- Software Requirements Specification (SRS)
- User Stories
- Use Cases
- Competitor Analysis

## Architecture

- High Level Design
- Low Level Design
- Database Design
- API Specification
- UI/UX Design
- AI Model Design
- Async Job Architecture
- Data Governance

## Project Management

- Project Roadmap
- Risk Assessment
- AI Validation Plan

## Audit

- PROJECT_IMPLEMENTATION_STATUS.md
- AUDIT_CHECKLIST.md

---

# Getting Started

## Clone Repository

```bash
git clone https://github.com/nikhil-0123/AI-Recruitment-System.git
cd AI-Recruitment-System
```

---

## Backend

```bash
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

Run:

```bash
uvicorn app.main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

## Docker

```bash
docker compose -f deployment/docker-compose.yml up --build
```

---

# Architecture

```text
Frontend
      │
      ▼
FastAPI API Layer
      │
      ▼
Services
      │
      ▼
Repositories
      │
      ▼
PostgreSQL

             │
             ▼

AI Engine

Resume Parser

↓

Skill Extraction

↓

Embeddings

↓

Matching

↓

Ranking

↓

LLM Intelligence
```

---

# Development Workflow

```
main
│
develop
│
feature/*
│
audit/*
│
fix/*
```

Follow the guidelines in **CONTRIBUTING.md**.

---

# Testing

Backend

```bash
cd backend
pytest
```

---

# Documentation Audit

Current audit focuses on:

- Day 1
- Day 2
- Day 3

Day 4+ development will begin only after successful verification.

---

# Roadmap

- ✅ Phase 1 – Foundation
- 🔄 Phase 2 – Verification
- ⏳ Phase 3 – Core APIs
- ⏳ Phase 4 – AI Services
- ⏳ Phase 5 – Frontend Features
- ⏳ Phase 6 – Production Deployment

---

# License

This project is currently under development.

A license will be added before the first public release.

---

# Author

**Nikhil Chaugule**

Bachelor of Engineering (Artificial Intelligence & Data Science)

Savitribai Phule Pune University

---

## Acknowledgements

This project is being developed as a production-oriented AI Recruitment Automation System with a strong emphasis on software engineering best practices, explainable AI, and scalable architecture.