import asyncio

from fastapi import FastAPI

from app.api import ingest, jobs, profiles
from app.core.database import Base, engine
from app.workers import scheduler

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Hunter API")


@app.get("/")
def read_root():
    return {"message": "Job Hunter API is running!"}


# Include routers
app.include_router(ingest.router, prefix="/ingest", tags=["Ingest"])
app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
app.include_router(profiles.router, prefix="/profiles", tags=["Profiles"])


# Start background scheduler
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(scheduler.auto_fetch())
