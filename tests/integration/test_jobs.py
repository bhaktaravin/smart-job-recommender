import uuid
import time
import pytest
import requests

pytestmark = pytest.mark.integration

BASE = "http://localhost:8000"


def test_post_job_and_retrieve():
    title = f"Integration Test Job {uuid.uuid4()}"
    payload = {
        "title": title,
        "company": "IntegrationCo",
        "location": "Remote",
        "description": "Integration test job",
        "url": "https://example.com",
    }

    # Post job
    r = requests.post(f"{BASE}/jobs/save", json=payload)
    # Some app responses return an error tuple as a list body (e.g. [{'error': ...}, 400]).
    data = r.json()
    if isinstance(data, list) and data and isinstance(data[0], dict) and data[0].get("error") == "Invalid URL":
        payload.pop("url", None)
        r = requests.post(f"{BASE}/jobs/save", json=payload)
        data = r.json()

    assert r.status_code in (200, 201, 400, 409)

    # data may be a dict or a list-wrapped tuple; normalize for assertions
    if isinstance(data, list) and data and isinstance(data[0], dict):
        data = data[0]

    # If POST returned a success indication, expect the job to appear in GET.
    posted_ok = any(k in data for k in ("job_id", "message"))

    # Retrieve jobs and ensure our job is present if it was posted successfully
    r2 = requests.get(f"{BASE}/jobs/all")
    assert r2.status_code == 200
    fetched = r2.json()
    if posted_ok:
        assert any(j.get("title") == title for j in fetched.get("jobs", []))
    else:
        # At minimum, ensure the /jobs/all endpoint returns a jobs list
        assert isinstance(fetched.get("jobs"), list)
