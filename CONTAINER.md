Containerization quickstart

- Build CPU image:

```bash
docker build -t smart-job-recommender:local .
```

- Run with docker-compose (creates Postgres + app):

```bash
docker compose up --build
```

- GPU image (requires NVIDIA Container Toolkit on host):

```bash
docker build -f Dockerfile.gpu -t smart-job-recommender:gpu .
docker run --gpus all -p 8000:8000 smart-job-recommender:gpu
```

Notes:
- The app expects a Postgres database; docker-compose provides one for local dev.
- For production, use environment variables for DB credentials and consider multi-stage builds.
