import asyncio

from app.core.database import SessionLocal
from app.services.ingest.remotive import fetch_remotive_jobs
from app.services.job_service import save_jobs


async def auto_fetch():
    while True:
        print("Fetching Remotive jobs...")
        jobs = await fetch_remotive_jobs()
        db = SessionLocal()
        try:
            saved = save_jobs(db, jobs, "remotive")
            print(f"Saved {saved} new jobs")
        finally:
            db.close()
        await asyncio.sleep(6 * 60 * 60)  # every 6 hours
