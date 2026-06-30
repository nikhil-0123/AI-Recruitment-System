# AI Recruitment Automation System (ARAS)

# High Level Design (HLD)

Version: 1.0

Date: June 2026

Project: AI Recruitment Automation System

Document Status: Architecture Approved

---

# 1. Introduction

## Purpose

This High-Level Design (HLD) document describes the overall architecture, major system components, technology stack, data flow, integration points, deployment strategy, and scalability considerations for the AI Recruitment Automation System (ARAS).

The goal of this document is to provide a blueprint for developers, AI engineers, DevOps engineers, and stakeholders before implementation begins.

---

# 2. System Overview

ARAS is an AI-powered recruitment intelligence platform that automates:

* Resume Screening
* Candidate Evaluation
* Candidate Ranking
* Skill Gap Analysis
* Candidate Summarization
* Interview Question Generation

The platform enables recruiters to process large numbers of resumes efficiently while maintaining transparency and explainability.

---

# 3. Architecture Goals

## Primary Goals

* Scalable
* Modular
* Secure
* Maintainable
* Cloud Deployable
* AI-Driven
* Explainable

---

## Technical Goals

* Fast candidate processing
* Real-time ranking
* Semantic candidate search
* AI-assisted decision support
* Containerized deployment
* Easy future expansion

---

# 4. System Architecture

## High-Level Architecture

```text
+---------------------------------------------------+
|                    React Frontend                 |
+---------------------------------------------------+
                     |
                     |
                     v
+---------------------------------------------------+
|                FastAPI Backend API                |
+---------------------------------------------------+
                     |
     -----------------------------------------
     |                  |                    |
     v                  v                    v

+-----------+   +-------------+   +----------------+
| PostgreSQL|   |    Redis    |   |  AWS S3 Storage |
+-----------+   +-------------+   +----------------+

     |
     |
     v

+---------------------------------------------------+
|                 AI Processing Layer               |
+---------------------------------------------------+
|                                                   |
| Resume Parsing Engine                             |
| Skill Extraction Engine                           |
| Embedding Generator                               |
| Candidate Matching Engine                         |
| Candidate Ranking Engine                          |
| Candidate Summary Generator                       |
| Interview Question Generator                      |
|                                                   |
+---------------------------------------------------+

                     |
                     v

+---------------------------------------------------+
|                Gemini API / LLM Layer             |
+---------------------------------------------------+
```

---

# 5. Architectural Style

The system follows:

## Layered Architecture

Presentation Layer

↓

API Layer

↓

Business Logic Layer

↓

AI Services Layer

↓

Data Layer

---

## Microservice Ready Modular Monolith

Version 1:

Modular Monolith

Future:

Service extraction possible:

* AI Service
* Authentication Service
* Report Service

without major redesign.

---

# 6. Technology Stack

## Frontend

Framework:

React.js

Language:

TypeScript

UI:

TailwindCSS

State Management:

React Query

HTTP Client:

Axios

Charts:

Recharts

---

## Backend

Framework:

FastAPI

Language:

Python 3.12

ORM:

SQLAlchemy

Migration:

Alembic

Validation:

Pydantic

Authentication:

JWT

---

## Database

Primary Database:

PostgreSQL

Vector Storage:

pgvector

---

## Cache Layer

Redis

Used For:

* Session Cache
* Ranking Cache
* AI Result Cache

---

## Queue System

Celery

Message Broker:

Redis

Used For:

* Resume Processing
* AI Summarization
* Report Generation

---

## Storage

AWS S3

Stores:

* Resumes
* Generated Reports
* Exports

---

## AI Stack

Sentence Transformers

Model:

all-MiniLM-L6-v2

Uses:

* Resume Embeddings
* Job Embeddings
* Semantic Matching

LLM:

Gemini API

Uses:

* Candidate Summary
* Skill Gap Analysis
* Interview Questions

---

## DevOps

Docker

GitHub Actions

Nginx

AWS

---

# 7. Major System Components

---

## Component 1

Authentication Service

Responsibilities:

* Registration
* Login
* JWT Generation
* Role Validation

---

## Component 2

Job Management Service

Responsibilities:

* Create Job
* Update Job
* Delete Job
* Job Analysis

---

## Component 3

Resume Management Service

Responsibilities:

* Upload Resume
* Validate File
* Store File
* Track Processing

---

## Component 4

Resume Parsing Service

Responsibilities:

Extract:

* Skills
* Education
* Experience
* Certifications
* Projects

---

## Component 5

Embedding Service

Responsibilities:

Generate vectors for:

* Resumes
* Jobs

Store vectors in pgvector.

---

## Component 6

Matching Service

Responsibilities:

Calculate:

* Skill Match
* Experience Match
* Education Match
* Semantic Similarity

---

## Component 7

Ranking Service

Responsibilities:

Generate:

* Candidate Score
* Candidate Rank

Formula:

Final Score =
35% Semantic Match +
25% Skill Match +
20% Experience Match +
10% Education Match +
10% AI Evaluation

---

## Component 8

Candidate Intelligence Service

Responsibilities:

Generate:

* Candidate Summary
* Skill Gap Analysis
* Interview Questions

---

## Component 9

Reporting Service

Responsibilities:

Generate:

* PDF Reports
* CSV Reports
* Excel Reports

---

## Component 10

Analytics Service

Responsibilities:

Generate:

* Dashboard Metrics
* Hiring Funnel
* Candidate Trends

---

# 8. Data Flow

## Resume Processing Flow

```text
Resume Upload

↓

File Validation

↓

S3 Storage

↓

Text Extraction

↓

Resume Parsing

↓

Skill Extraction

↓

Embedding Generation

↓

Database Storage
```

---

## Candidate Ranking Flow

```text
Job Description

↓

Job Analysis

↓

Job Embedding

↓

Candidate Embedding

↓

Similarity Calculation

↓

Score Calculation

↓

Ranking Generation
```

---

## AI Recommendation Flow

```text
Candidate Profile

↓

Gemini API

↓

Candidate Summary

↓

Skill Gap Analysis

↓

Interview Questions
```

---

# 9. Security Architecture

Authentication:

JWT

Authorization:

RBAC

Encryption:

HTTPS/TLS

Password Storage:

bcrypt

File Upload Security:

* File Type Validation
* File Size Validation
* Malware Scan Ready

API Protection:

* Rate Limiting
* Input Validation
* SQL Injection Protection

---

# 10. Scalability Design

Target Capacity

* 10,000 Resumes
* 1,000 Jobs
* 500 Concurrent Users

---

Horizontal Scaling

Backend:

Multiple FastAPI Instances

Database:

PostgreSQL Read Replicas

Cache:

Redis Cluster

Storage:

AWS S3

---

# 11. Fault Tolerance

Database Failure

* Automated Backups

AI Failure

* Retry Mechanism

Queue Failure

* Celery Retries

Storage Failure

* S3 Redundancy

---

# 12. Deployment Architecture

```text
Internet
     |
     v

+-----------+
|   Nginx   |
+-----------+

     |
     v

+-------------------+
| React Frontend    |
+-------------------+

     |
     v

+-------------------+
| FastAPI Backend   |
+-------------------+

     |
--------------------------------
|              |               |
v              v               v

PostgreSQL    Redis          S3

                 |
                 v

            Celery Worker

                 |
                 v

           Gemini API
```

---

# 13. Monitoring & Logging

Logging:

Python Logging

Future:

ELK Stack

Metrics:

Prometheus

Visualization:

Grafana

Error Tracking:

Sentry

---

# 14. Future Expansion

Version 2

* Multi-Tenant SaaS
* Recruiter Copilot
* AI Candidate Search
* Email Automation

Version 3

* Interview Scheduling
* Video Interview Analysis
* Enterprise Integrations

Version 4

* Autonomous Recruitment Agent

---

# 15. Architecture Decisions

| Decision   | Reason                          |
| ---------- | ------------------------------- |
| FastAPI    | High performance Python backend |
| PostgreSQL | Reliable relational database    |
| pgvector   | Semantic candidate search       |
| Redis      | Fast caching and queues         |
| Celery     | Background processing           |
| React      | Modern frontend framework       |
| Gemini API | Advanced AI capabilities        |
| Docker     | Consistent deployment           |
| AWS S3     | Scalable file storage           |

---

# 16. Conclusion

The proposed architecture provides a scalable, modular, and AI-driven foundation for the AI Recruitment Automation System.

The design supports current project requirements while allowing future expansion into a full-scale Recruitment Intelligence Platform.

The architecture balances development speed, maintainability, AI capability, and cloud scalability, making it suitable for both academic and commercial deployment.
