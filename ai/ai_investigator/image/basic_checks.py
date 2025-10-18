import hashlib


def fake_reverse_image_hits(urls: list[str]) -> int:
    # Deterministic pseudo-hits based on URL hash
    digest = hashlib.sha256("|".join(sorted(urls)).encode()).hexdigest()
    return int(digest[:2], 16) % 5


def ocr_stub(urls: list[str]) -> list[str]:
    # Placeholder always empty
    return []


def image_similarity(urls: list[str]) -> dict:
    hits = fake_reverse_image_hits(urls)
    similarity = 0.5 + (hits * 0.1)
    return {
        "face_similarity": round(min(similarity, 0.95), 2),
        "reverse_image_hits": hits,
        "ocr_texts": ocr_stub(urls),
    }


