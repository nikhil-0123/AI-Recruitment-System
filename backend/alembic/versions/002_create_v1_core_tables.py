"""Create V1 core tables for ARAS hiring workflow

Revision ID: 002
Revises: 001
Create Date: 2026-06-23

Tables created (11 total, V1 scope only):
  users, candidates, jobs, resumes, skills,
  candidate_skills, job_skills,
  candidate_embeddings, job_embeddings,
  candidate_scores, audit_logs

Tables NOT created (deferred per scope update):
  ai_summaries      → V1.1
  interview_questions → V1.1
  reports           → V1.2
  analytics tables  → V1.2

Sources:
  08_Database_Design.md
  ARAS-Project-Scope-Update-Mandatory.md
  AI_Model.md Section 7 (VECTOR 384)
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision: str = "002"
down_revision: str = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:

    # pgvector extension must be enabled before creating VECTOR columns.
    # uuid-ossp is enabled in migration 001.
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # ── users ──────────────────────────────────────────────────────────────────
    # Source: 08_Database_Design.md Section 5
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.Text, nullable=False),
        sa.Column("role", sa.String(30), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False,
                  server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
    )
    op.create_index("idx_users_email", "users", ["email"], unique=True)
    op.create_index("idx_users_role", "users", ["role"])
    op.create_index("idx_users_is_active", "users", ["is_active"])

    # ── candidates ─────────────────────────────────────────────────────────────
    # Source: 08_Database_Design.md Section 7
    # Created before resumes and candidate_* tables (they FK into candidates).
    op.create_table(
        "candidates",
        sa.Column("id", UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("phone", sa.String(20), nullable=True),
        sa.Column("linkedin_url", sa.Text, nullable=True),
        sa.Column("experience_years", sa.Numeric(4, 1), nullable=True),
        sa.Column("education", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
    )
    op.create_index("idx_candidates_email", "candidates", ["email"])
    op.create_index("idx_candidates_full_name", "candidates", ["full_name"])

    # ── jobs ───────────────────────────────────────────────────────────────────
    # Source: 08_Database_Design.md Section 6
    # FK → users.id (RESTRICT — cannot delete user with jobs)
    op.create_table(
        "jobs",
        sa.Column("id", UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("recruiter_id", UUID(as_uuid=True),
                  sa.ForeignKey("users.id", ondelete="RESTRICT",
                                name="fk_jobs_recruiter_id_users"),
                  nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("experience_required", sa.Integer, nullable=True),
        sa.Column("education_required", sa.String(255), nullable=True),
        sa.Column("status", sa.String(50), nullable=False,
                  server_default="draft"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
    )
    op.create_index("idx_jobs_recruiter_id", "jobs", ["recruiter_id"])
    op.create_index("idx_jobs_title", "jobs", ["title"])
    op.create_index("idx_jobs_status", "jobs", ["status"])
    op.create_index("idx_jobs_recruiter_status", "jobs", ["recruiter_id", "status"])

    # ── resumes ────────────────────────────────────────────────────────────────
    # Source: 08_Database_Design.md Section 8
    # FK → candidates.id (CASCADE — resume deleted when candidate deleted)
    op.create_table(
        "resumes",
        sa.Column("id", UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("candidate_id", UUID(as_uuid=True),
                  sa.ForeignKey("candidates.id", ondelete="CASCADE",
                                name="fk_resumes_candidate_id_candidates"),
                  nullable=False),
        sa.Column("file_name", sa.Text, nullable=False),
        sa.Column("file_url", sa.Text, nullable=True),
        sa.Column("file_type", sa.String(20), nullable=True),
        sa.Column("file_size", sa.BigInteger, nullable=True),
        sa.Column("parsing_status", sa.String(50), nullable=False,
                  server_default="pending"),
        sa.Column("uploaded_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
    )
    op.create_index("idx_resumes_candidate_id", "resumes", ["candidate_id"])
    op.create_index("idx_resumes_parsing_status", "resumes", ["parsing_status"])

    # ── skills ─────────────────────────────────────────────────────────────────
    # Source: 08_Database_Design.md Section 9
    # Master skill repository. FK target for candidate_skills and job_skills.
    op.create_table(
        "skills",
        sa.Column("id", UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("skill_name", sa.String(100), nullable=False),
        sa.Column("category", sa.String(100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
    )
    op.create_index("idx_skills_skill_name", "skills", ["skill_name"], unique=True)
    op.create_index("idx_skills_category", "skills", ["category"])

    # ── candidate_skills ───────────────────────────────────────────────────────
    # Source: 08_Database_Design.md Section 10
    # M:N junction: candidates ↔ skills
    op.create_table(
        "candidate_skills",
        sa.Column("id", UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("candidate_id", UUID(as_uuid=True),
                  sa.ForeignKey("candidates.id", ondelete="CASCADE",
                                name="fk_candidate_skills_candidate_id_candidates"),
                  nullable=False),
        sa.Column("skill_id", UUID(as_uuid=True),
                  sa.ForeignKey("skills.id", ondelete="CASCADE",
                                name="fk_candidate_skills_skill_id_skills"),
                  nullable=False),
        sa.Column("proficiency_score", sa.Numeric(5, 2), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.UniqueConstraint("candidate_id", "skill_id",
                            name="uq_candidate_skills_candidate_skill"),
    )
    op.create_index("idx_candidate_skills_candidate_id",
                    "candidate_skills", ["candidate_id"])
    op.create_index("idx_candidate_skills_skill_id",
                    "candidate_skills", ["skill_id"])

    # ── job_skills ─────────────────────────────────────────────────────────────
    # Source: 08_Database_Design.md Section 11
    # M:N junction: jobs ↔ skills
    op.create_table(
        "job_skills",
        sa.Column("id", UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("job_id", UUID(as_uuid=True),
                  sa.ForeignKey("jobs.id", ondelete="CASCADE",
                                name="fk_job_skills_job_id_jobs"),
                  nullable=False),
        sa.Column("skill_id", UUID(as_uuid=True),
                  sa.ForeignKey("skills.id", ondelete="CASCADE",
                                name="fk_job_skills_skill_id_skills"),
                  nullable=False),
        sa.Column("importance_weight", sa.Numeric(5, 2), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.UniqueConstraint("job_id", "skill_id",
                            name="uq_job_skills_job_skill"),
    )
    op.create_index("idx_job_skills_job_id", "job_skills", ["job_id"])
    op.create_index("idx_job_skills_skill_id", "job_skills", ["skill_id"])

    # ── candidate_embeddings ───────────────────────────────────────────────────
    # Source: 08_Database_Design.md Section 13
    # Source: AI_Model.md Section 7 — VECTOR(384), all-MiniLM-L6-v2
    op.create_table(
        "candidate_embeddings",
        sa.Column("id", UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("candidate_id", UUID(as_uuid=True),
                  sa.ForeignKey("candidates.id", ondelete="CASCADE",
                                name="fk_candidate_embeddings_candidate_id_candidates"),
                  nullable=False, unique=True),
        sa.Column("embedding", sa.Text, nullable=False),  # stored as text, cast by pgvector
        sa.Column("model_name", sa.String(100), nullable=False,
                  server_default="all-MiniLM-L6-v2"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
    )
    # Alter column to VECTOR(384) after table creation using pgvector type
    op.execute(
        "ALTER TABLE candidate_embeddings "
        "ALTER COLUMN embedding TYPE vector(384) USING embedding::vector;"
    )
    op.create_index("idx_candidate_embeddings_candidate_id",
                    "candidate_embeddings", ["candidate_id"], unique=True)
    # IVFFlat vector index for cosine similarity search
    # Source: 08_Database_Design.md Section 13
    op.execute(
        "CREATE INDEX idx_candidate_vector "
        "ON candidate_embeddings "
        "USING ivfflat (embedding vector_cosine_ops) "
        "WITH (lists = 100);"
    )

    # ── job_embeddings ─────────────────────────────────────────────────────────
    # Source: 08_Database_Design.md Section 14
    op.create_table(
        "job_embeddings",
        sa.Column("id", UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("job_id", UUID(as_uuid=True),
                  sa.ForeignKey("jobs.id", ondelete="CASCADE",
                                name="fk_job_embeddings_job_id_jobs"),
                  nullable=False, unique=True),
        sa.Column("embedding", sa.Text, nullable=False),
        sa.Column("model_name", sa.String(100), nullable=False,
                  server_default="all-MiniLM-L6-v2"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
    )
    op.execute(
        "ALTER TABLE job_embeddings "
        "ALTER COLUMN embedding TYPE vector(384) USING embedding::vector;"
    )
    op.create_index("idx_job_embeddings_job_id",
                    "job_embeddings", ["job_id"], unique=True)
    op.execute(
        "CREATE INDEX idx_job_vector "
        "ON job_embeddings "
        "USING ivfflat (embedding vector_cosine_ops) "
        "WITH (lists = 100);"
    )

    # ── candidate_scores ───────────────────────────────────────────────────────
    # Source: 08_Database_Design.md Section 12
    # Source: ARAS-Project-Scope-Update-Mandatory.md — XAI fields
    op.create_table(
        "candidate_scores",
        sa.Column("id", UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("candidate_id", UUID(as_uuid=True),
                  sa.ForeignKey("candidates.id", ondelete="CASCADE",
                                name="fk_candidate_scores_candidate_id_candidates"),
                  nullable=False),
        sa.Column("job_id", UUID(as_uuid=True),
                  sa.ForeignKey("jobs.id", ondelete="CASCADE",
                                name="fk_candidate_scores_job_id_jobs"),
                  nullable=False),
        sa.Column("skill_score", sa.Numeric(5, 2), nullable=True),
        sa.Column("experience_score", sa.Numeric(5, 2), nullable=True),
        sa.Column("education_score", sa.Numeric(5, 2), nullable=True),
        sa.Column("semantic_score", sa.Numeric(5, 2), nullable=True),
        sa.Column("ai_score", sa.Numeric(5, 2), nullable=True),
        sa.Column("final_score", sa.Numeric(5, 2), nullable=True),
        sa.Column("rank_position", sa.Integer, nullable=True),
        # XAI fields — required by updated V1 scope
        sa.Column("matched_skills", JSONB, nullable=True),
        sa.Column("missing_skills", JSONB, nullable=True),
        sa.Column("recommendation", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.UniqueConstraint("candidate_id", "job_id",
                            name="uq_candidate_scores_candidate_job"),
    )
    op.create_index("idx_candidate_scores_final_score",
                    "candidate_scores", ["final_score"])
    op.create_index("idx_candidate_scores_candidate_id",
                    "candidate_scores", ["candidate_id"])
    op.create_index("idx_candidate_scores_job_id",
                    "candidate_scores", ["job_id"])
    op.create_index("idx_candidate_scores_rank_position",
                    "candidate_scores", ["rank_position"])

    # ── audit_logs ─────────────────────────────────────────────────────────────
    # Source: 08_Database_Design.md Section 18
    # Source: 15_Data_Governance.md Section 14
    op.create_table(
        "audit_logs",
        sa.Column("id", UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("user_id", UUID(as_uuid=True),
                  sa.ForeignKey("users.id", ondelete="SET NULL",
                                name="fk_audit_logs_user_id_users"),
                  nullable=True),
        sa.Column("action", sa.String(255), nullable=False),
        sa.Column("entity_type", sa.String(100), nullable=False),
        sa.Column("entity_id", UUID(as_uuid=True), nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
    )
    op.create_index("idx_audit_logs_user_id", "audit_logs", ["user_id"])
    op.create_index("idx_audit_logs_action", "audit_logs", ["action"])
    op.create_index("idx_audit_logs_entity_type", "audit_logs", ["entity_type"])
    op.create_index("idx_audit_logs_timestamp", "audit_logs", ["timestamp"])
    op.create_index("idx_audit_logs_entity_type_entity_id",
                    "audit_logs", ["entity_type", "entity_id"])


def downgrade() -> None:
    # Drop in strict reverse FK dependency order
    op.drop_table("audit_logs")
    op.drop_table("candidate_scores")
    op.drop_table("job_embeddings")
    op.drop_table("candidate_embeddings")
    op.drop_table("job_skills")
    op.drop_table("candidate_skills")
    op.drop_table("skills")
    op.drop_table("resumes")
    op.drop_table("jobs")
    op.drop_table("candidates")
    op.drop_table("users")
    op.execute("DROP EXTENSION IF EXISTS vector;")