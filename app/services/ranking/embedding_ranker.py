from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")


def rank_jobs(profile_text: str, job_texts: list[str]):
    """
    Returns similarity scores of each job description to profile text.
    """
    if not job_texts:
        return []

    embeddings = model.encode([profile_text] + job_texts, convert_to_tensor=True)
    cosine_scores = util.cos_sim(embeddings[0], embeddings[1:])
    return cosine_scores.cpu().numpy().flatten()
