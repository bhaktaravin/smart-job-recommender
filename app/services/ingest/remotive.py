import httpx

REMOTIVE_URL = "https://remotive.com/api/remote-jobs"


async def fetch_remotive_jobs():
    async with httpx.AsyncClient() as client:
        r = await client.get(REMOTIVE_URL)
        r.raise_for_status()
        return r.json()["jobs"]
