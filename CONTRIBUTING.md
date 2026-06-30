# Contributing to ARAS

Welcome to the AI Recruitment Automation System (ARAS).

This document defines the development workflow, coding standards, Git strategy, and review process for all contributors.

---

# Project Goals

- Maintain a clean and scalable architecture.
- Follow the approved project documentation.
- Keep the codebase production-ready.
- Prevent architectural drift.
- Ensure all changes are tested before merging.

---

# Development Workflow

Development follows the approved roadmap.

Current Audit Phase:

- Verify Day 1
- Verify Day 2
- Verify Day 3

Do not implement Day 4+ features until the audit is complete.

---

# Git Workflow

## Main Branches

```
main
```

Production-ready releases only.

```
develop
```

Active development.

---

## Feature Branches

Use:

```
feature/<feature-name>
```

Examples

```
feature/authentication

feature/resume-upload

feature/database-models
```

---

## Bug Fixes

```
fix/<issue-name>
```

Example

```
fix/login-validation
```

---

## Audit

```
audit/day1-day3

audit/document-verification
```

---

## Documentation

```
docs/api-update

docs/database-design
```

---

# Commit Message Convention

Use Conventional Commits.

Examples

```
feat(auth): implement JWT authentication

fix(database): resolve migration issue

docs(api): update authentication endpoints

test(ranking): add repository tests

refactor(service): simplify ranking service

chore(ci): update GitHub workflow
```

---

# Pull Request Rules

Every Pull Request must:

- Build successfully.
- Pass all tests.
- Follow project architecture.
- Update documentation if required.
- Avoid unrelated changes.

---

# Coding Standards

## Python

- Python 3.12+
- Follow PEP 8
- Use type hints
- Use docstrings for public APIs
- Prefer dependency injection
- Keep business logic inside services
- Avoid duplicate code

---

## FastAPI

- Thin API routes
- Business logic inside services
- Database access through repositories
- Validation using Pydantic schemas

---

## Database

- UUID primary keys
- Alembic migrations only
- No direct schema modifications
- Use SQLAlchemy ORM

---

## Frontend

- React + TypeScript
- Functional components
- Reusable UI components
- Avoid inline styles
- Follow ESLint rules

---

# Testing

Every feature should include appropriate tests.

Minimum requirements:

- Unit tests
- Integration tests (when applicable)

Tests must pass before merging.

---

# Documentation

When changing architecture or APIs, update the relevant documentation.

Examples:

- SRS
- API Specification
- Database Design
- HLD
- LLD

Implementation should remain consistent with the approved documents.

---

# Code Review Checklist

Before requesting review:

- Code builds successfully.
- Tests pass.
- No unnecessary files.
- No commented-out code.
- No secrets or API keys.
- Documentation updated if needed.
- Imports organized.
- Linting completed.

---

# Security

Never commit:

- `.env`
- API keys
- Passwords
- Tokens
- Database credentials

Use `.env.example` for configuration templates.

---

# AI Development Guidelines

AI assistants (Antigravity, Codex, Copilot, ChatGPT, etc.) must:

- Follow the project architecture.
- Avoid introducing unnecessary dependencies.
- Respect existing folder structure.
- Avoid modifying unrelated files.
- Explain architectural changes before implementation.

---

# Branch Protection

Only merge into `main` after:

- Documentation verified
- Tests passing
- Code review completed
- Audit checklist approved

---

# Architecture Principles

- Clean Architecture
- SOLID Principles
- Repository Pattern
- Service Layer Pattern
- Dependency Injection
- Modular Monolith (Version 1)

---

# Current Status

Current development stage:

✔ Day 1 Foundation
✔ Day 2 Repository Layer
✔ Day 3 Database Layer

Current focus:

Repository audit and verification before continuing with Day 4.

---

Thank you for contributing to ARAS.