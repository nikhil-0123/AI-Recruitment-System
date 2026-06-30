from __future__ import annotations

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.db.database import get_db
from app.repositories.exceptions import NotFoundError
from app.services.resume_service import ResumeService

logger = get_logger(__name__)
router = APIRouter(prefix="/resumes", tags=["Resumes"])


class ResumeCreateRequest(BaseModel):
    candidate_id: UUID
    file_name: str = Field(..., json_schema_extra={"example": "resume.pdf"})
    file_url: str | None = Field(None, json_schema_extra={"example": "https://storage.example.com/resume.pdf"})
    file_type: str | None = Field(None, json_schema_extra={"example": "application/pdf"})
    file_size: int | None = Field(None, json_schema_extra={"example": 123456})
    parsing_status: str | None = Field(None, json_schema_extra={"example": "pending"})


class ResumeResponse(BaseModel):
    id: UUID
    candidate_id: UUID
    file_name: str
    file_url: str | None = None
    file_type: str | None = None
    file_size: int | None = None
    parsing_status: str
    uploaded_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResumeCreateResponse(BaseModel):
    resume_id: UUID
    status: str


def get_resume_service() -> ResumeService:
    return ResumeService()


@router.post("/upload", response_model=ResumeCreateResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    payload: ResumeCreateRequest,
    db: AsyncSession = Depends(get_db),
    service: ResumeService = Depends(get_resume_service),
) -> ResumeCreateResponse:
    logger.info("upload_resume_request_received", candidate_id=str(payload.candidate_id))
    resume = await service.create_resume(db, payload.model_dump(exclude_none=True))
    return ResumeCreateResponse(resume_id=resume.id, status="uploaded")


@router.get("", response_model=list[ResumeResponse], status_code=status.HTTP_200_OK)
async def list_resumes(
    candidate_id: UUID | None = Query(None, description="Filter resumes by candidate id"),
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    service: ResumeService = Depends(get_resume_service),
) -> list[ResumeResponse]:
    items, _ = await service.list_resumes(db, candidate_id=candidate_id, page=page, page_size=page_size)
    return items


@router.get("/{resume_id}", response_model=ResumeResponse, status_code=status.HTTP_200_OK)
async def get_resume(
    resume_id: UUID,
    db: AsyncSession = Depends(get_db),
    service: ResumeService = Depends(get_resume_service),
) -> ResumeResponse:
    try:
        resume = await service.get_resume(db, resume_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)
    return resume
