from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.job import Job
from app.schemas.job import JobCreate

router = APIRouter()


# Save a job
@router.post("/save")
def save_job(job: JobCreate, db: Session = Depends(get_db)):
    job_data = job.dict()

    # Convert HttpUrl to string
    if job_data.get("url"):
        job_data["url"] = str(job_data["url"])

    db_job = Job(**job_data)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return {"message": "Job saved successfully", "job_id": db_job.id}


# Get all jobs
@router.get("/all", response_model=List[JobCreate])
def get_all_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    return [
        {
            key: value
            for key, value in job.__dict__.items()
            if key != "_sa_instance_state"
        }
        for job in jobs
    ]
