from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def rank_jobs(profile_text: str, job_texts: list[str]):
    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    docs = [profile_text] + job_texts
    tfidf = vectorizer.fit_transform(docs)
    sims = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()
    return sims
