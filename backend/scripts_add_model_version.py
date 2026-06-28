from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.SYNC_DATABASE_URL)
with engine.begin() as conn:
    conn.execute(text('ALTER TABLE candidate_embeddings ADD COLUMN IF NOT EXISTS model_version VARCHAR(50) DEFAULT \'1.0\' NOT NULL'))
    conn.execute(text('ALTER TABLE job_embeddings ADD COLUMN IF NOT EXISTS model_version VARCHAR(50) DEFAULT \'1.0\' NOT NULL'))
    print('columns added')
