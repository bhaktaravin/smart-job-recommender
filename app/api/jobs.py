from app.services.ranking.embedding_ranker import rank_jobs


# Replace TF-IDF ranker with embedding_ranker
@router.post("/recommend/{user_id}")
def recommend(user_id: int, db: Session = Depends(get_db)):
    from app.models.user_profile import UserProfile

    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    jobs = db.query(Job).limit(200).all()
    texts = [j.description or "" for j in jobs]
    scores = rank_jobs(user.text, texts)

    ranked = sorted(zip(jobs, scores), key=lambda x: x[1], reverse=True)[:20]

    return [
        {"title": j.title, "company": j.company, "score": float(s), "url": j.url}
        for j, s in ranked
    ]
