import os
import time
import subprocess
import sys

import requests


BASE_URL = os.getenv("TEST_API_BASE", "http://127.0.0.1:8001")


def wait_for_healthy(timeout_seconds: int = 10) -> None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            r = requests.get(f"{BASE_URL}/health", timeout=1)
            if r.ok:
                return
        except Exception:
            pass
        time.sleep(0.2)
    raise RuntimeError("API not healthy in time")


def test_health_and_profiles():
    wait_for_healthy()
    r = requests.get(f"{BASE_URL}/health", timeout=2)
    assert r.ok
    assert r.json().get("status") == "ok"

    r = requests.get(f"{BASE_URL}/profiles?mode=demo", timeout=3)
    assert r.ok
    assert isinstance(r.json(), list)


def test_analysis_endpoints():
    wait_for_healthy()
    r = requests.post(
        f"{BASE_URL}/analysis/text",
        json={"texts": [["hello world 😊"], ["world hello 😊"]]},
        timeout=3,
    )
    assert r.ok
    data = r.json()
    assert "ngram_jaccard" in data and "emoji_overlap" in data

    r = requests.post(
        f"{BASE_URL}/analysis/image",
        json={"image_urls": ["https://example.com/a.png", "https://example.com/b.png"]},
        timeout=3,
    )
    assert r.ok
    data = r.json()
    assert "face_similarity" in data and "reverse_image_hits" in data

    r = requests.post(
        f"{BASE_URL}/analysis/correlate",
        json={
            "text_groups": [["hello world 😊"], ["world hello 😊"]],
            "image_urls": ["https://example.com/a.png", "https://example.com/b.png"],
        },
        timeout=3,
    )
    assert r.ok
    data = r.json()
    assert "score" in data and "summary" in data



