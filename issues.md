# Job Hunter Backend - Issues & Milestones

## Milestone 1 — Core Enhancements (Quick Wins)
**Goal:** Improve usability, speed, and data quality.

### Issues
- **Add pagination to GET `/jobs/all`**
  - Add `limit` and `offset` query parameters
  - Return jobs with pagination metadata

- **Add job filters**
  - Optional query parameters: `location`, `company`, `source`
  - Support filtering `/jobs/all` endpoint

- **Background ingestion scheduler**
  - Fetch jobs every 6 hours automatically
  - Use `APScheduler` or FastAPI background task

- **Cache job embeddings**
  - Precompute embeddings for jobs to speed up semantic ranking

- **Incremental job ingestion**
  - Only save new jobs, skip duplicates by URL

---

## Milestone 2 — User & Resume Features
**Goal:** Make system more personalized and user-friendly.

### Issues
- **Multiple resumes per user**
  - Allow uploading multiple resumes per profile
  - Let user select “active” resume for recommendations

- **Skill extraction from resumes**
  - Automatically tag key skills (e.g., Python, AWS)

- **Profile embeddings**
  - Compute embeddings for user resumes once and store them

- **Resume file type support**
  - Accept PDF, DOCX, TXT resumes

- **Upload endpoint validation**
  - Check file type & size limits
  - Return clear error messages

---

## Milestone 3 — Advanced Job & Recommendation Features
**Goal:** Improve recommendation quality and job data coverage.

### Issues
- **Add multiple job sources**
  - Integrate Adzuna, Indeed, USAJobs APIs

- **Hybrid ranking algorithm**
  - Combine semantic similarity with job recency or other metrics

- **Recommended jobs endpoint**
  - GET endpoint to return top-ranked jobs per user

- **Bookmark & applied status per job**
  - Track whether a job is bookmarked, applied, or interviewed

- **Job deduplication & normalization**
  - Merge similar jobs from multiple sources

---

## Milestone 4 — Production & Deployment
**Goal:** Make the backend production-ready.

### Issues
- **Dockerize backend**
  - Add `Dockerfile` and optional `docker-compose.yml`

- **Environment variables**
  - Move DB URL, scheduler interval, and model paths to `.env`

- **Upgrade DB**
  - Switch from SQLite to PostgreSQL/MySQL

- **Logging & monitoring**
  - Add structured logging and optional Sentry/Prometheus integration

- **Authentication & multi-user support**
  - Add JWT-based login and secure endpoints

- **Rate limiting**
  - Prevent API abuse if scraping multiple job sources

---

## Milestone 5 — Optional Frontend & Analytics
**Goal:** Visualize data and improve UX.

### Issues
- **Dashboard frontend**
  - Angular or React UI for jobs, recommendations, and profile management

- **Filters & search UI**
  - Add location, company, remote/full-time options in frontend

- **Charts & analytics**
  - Visualize top skills, companies, or job trends

- **Notifications system**
  - Send emails or push notifications for new matching jobs
