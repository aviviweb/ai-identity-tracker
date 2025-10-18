import os
import requests
import time


BASE_URL = os.getenv("TEST_API_BASE", "http://127.0.0.1:8001")


def wait_ready():
    for _ in range(30):
        try:
            r = requests.get(f"{BASE_URL}/health", timeout=1)
            if r.ok:
                return
        except Exception:
            time.sleep(0.2)
    raise RuntimeError("API not ready")


def test_results_flow():
    wait_ready()
    # Correlate
    r = requests.post(
        f"{BASE_URL}/analysis/correlate",
        json={"text_groups": [["hello"], ["hello there"]], "image_urls": ["https://a/b.png"]},
        timeout=3,
    )
    assert r.ok
    # Run and store
    r = requests.post(
        f"{BASE_URL}/analysis/run",
        json={
            "subject_ids": ["1", "2"],
            "text_groups": [["hello"], ["hello there"]],
            "image_urls": ["https://a/b.png"],
            "created_by": "demo@user",
        },
        timeout=3,
    )
    assert r.ok
    rid = r.json().get("id")
    assert isinstance(rid, int)

    # List results
    r = requests.get(f"{BASE_URL}/results?limit=5", timeout=3)
    assert r.ok
    assert isinstance(r.json(), list)

    # Export CSV
    r = requests.get(f"{BASE_URL}/results/{rid}/export?format=csv", timeout=3)
    assert r.ok
    assert r.headers.get("content-type", "").startswith("text/csv")

