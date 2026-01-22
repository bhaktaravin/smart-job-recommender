from typing import List, Optional

import validators
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.job import Job
from app.schemas import JobCreate, JobSchema

router = APIRouter()


class PaginatedJobsResponse(BaseModel):
    total_jobs: int
    total_pages: int
    current_page: int
    limit: int
    jobs: List[JobSchema]


@router.get("/all", response_model=PaginatedJobsResponse)
def get_all_jobs(
    db: Session = Depends(get_db),
    limit: Optional[int] = Query(20, ge=1, le=200),
    page: Optional[int] = Query(1, ge=1),
    title: Optional[str] = Query(None),
    company: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
):
    query = db.query(Job)

    if title:
        query = query.filter(Job.title.ilike(f"%{title}%"))
    if company:
        query = query.filter(Job.company.ilike(f"%{company}%"))
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))

    total_jobs = query.count()
    total_pages = (total_jobs + limit - 1) // limit

    jobs = query.order_by(Job.id.desc()).offset((page - 1) * limit).limit(limit).all()

    return {
        "total_jobs": total_jobs,
        "total_pages": total_pages,
        "current_page": page,
        "limit": limit,
        "jobs": jobs,
    }


@router.post("/save")
def save_job(job: JobCreate, db: Session = Depends(get_db)):
    existing_job = (
        db.query(Job)
        .filter(
            Job.title == job.title,
            Job.company == job.company,
            Job.location == job.location,
        )
        .first()
    )
    if existing_job:
        raise HTTPException(
            status_code=409, detail=f"Job already exists with id {existing_job.id}"
        )
    if not validators.url(job.url):
        return {"error": "Invalid URL"}, 400
    db_job = Job(
        title=job.title,
        company=job.company,
        location=job.location,
        description=job.description,
        url=str(job.url),
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    return {"message": "Job saved successfully", "job_id": db_job.id}
