import os
import shutil

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.resume_parser import extract_text_from_pdf

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/all")
def get_all_jobs(
    limit: int = Query(50, ge=1, le=200, description="Max number of jobs to return"),
    offset: int = Query(0, ge=0, description="Number of jobs to skip"),
    location: str | None = Query(None, description="Filter by job location"),
    company: str | None = Query(None, description="Filter by company"),
    source: str | None = Query(None, description="Filter by job source"),
    db: Session = Depends(get_db),
):
    """
    Returns saved jobs with optional pagination and filters.
    """
    query = db.query(Job)

    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    if company:
        query = query.filter(Job.company.ilike(f"%{company}%"))
    if source:
        query = query.filter(Job.source.ilike(f"%{source}%"))

    jobs = query.offset(offset).limit(limit).all()

    return [
        {
            "id": j.id,
            "title": j.title,
            "company": j.company,
            "location": j.location,
            "source": j.source,
            "url": j.url,
        }
        for j in jobs
    ]
