# Makefile for AI Recruitment System

.PHONY: up down test-backend test-frontend test

up:
	docker compose -f deployment/docker-compose.yml up -d --build

down:
	docker compose -f deployment/docker-compose.yml down

test-backend:
	cd backend && pytest

test-frontend:
	cd frontend && npm run test

test: test-backend test-frontend