from sqlalchemy.orm import Session

from app.models.job import Job


def save_jobs(db: Session, jobs: list, source: str):
    saved = 0
    for j in jobs:
        exists = db.query(Job).filter(Job.url == j["url"]).first()
        if exists:
            continue

        job = Job(
            source=source,
            title=j.get("title"),
            company=j.get("company_name"),
            location=j.get("candidate_required_location"),
            description=j.get("description"),
            url=j.get("url"),
        )
        db.add(job)
        saved += 1

    db.commit()
    return saved
