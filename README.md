# AI-Recruitment-System

## Quick start

From a fresh clone:

1. Start the supporting services:
   ```bash
   docker compose -f deployment/docker-compose.yml up -d db redis
   ```
2. Run the database migrations:
   ```bash
   cd backend
   alembic upgrade head
   ```
3. Start the FastAPI app:
   ```bash
   uvicorn app.main:app --reload
   ```
4. Start the Celery worker:
   ```bash
   celery -A app.tasks.celery_app worker --loglevel=info --queues default,ai,exports --concurrency=2
   ```

### Environment variables

The backend reads the following settings from environment variables or a local `.env` file:

- `DATABASE_URL`
- `CELERY_BROKER_URL`

### Docker Compose services

The deployment stack includes:

- PostgreSQL with pgvector
- Redis
- Celery worker
- Nginx
