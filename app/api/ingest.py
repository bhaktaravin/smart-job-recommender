from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.services.ingest.remotive import fetch_remotive_jobs
from app.services.job_service import save_jobs

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/remotive")
async def ingest_remotive(db: Session = Depends(get_db)):
    jobs = await fetch_remotive_jobs()
    count = save_jobs(db, jobs, "remotive")
    return {"saved": count}
