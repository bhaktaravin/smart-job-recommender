import requests


BASE = "http://localhost:8000"


def test_health():
    r = requests.get(f"{BASE}/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"


def test_get_jobs_empty():
    r = requests.get(f"{BASE}/jobs/all")
    assert r.status_code == 200
    data = r.json()
    assert "total_jobs" in data
    assert isinstance(data["jobs"], list)
