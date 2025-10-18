import re
from collections import Counter
from typing import Iterable


EMOJI_PATTERN = re.compile(r"[\U0001F300-\U0001FAFF]")


def normalize(text: str) -> list[str]:
    text = text.lower()
    tokens = re.findall(r"[a-z0-9]+", text)
    return tokens


def ngram(tokens: list[str], n: int = 3) -> Counter:
    return Counter(
        tuple(tokens[i : i + n]) for i in range(max(0, len(tokens) - n + 1))
    )


def emoji_count(text: str) -> int:
    return len(EMOJI_PATTERN.findall(text))


def _safe_ratio(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def style_similarity(texts_a: Iterable[str], texts_b: Iterable[str]) -> dict:
    a = " ".join(texts_a)
    b = " ".join(texts_b)

    ta = normalize(a)
    tb = normalize(b)

    # 1) Characteristic 3-gram overlap (existing)
    nga = ngram(ta, 3)
    ngb = ngram(tb, 3)
    inter = sum((nga & ngb).values())
    union = sum((nga | ngb).values()) or 1
    ngram_jaccard = _safe_ratio(inter, union)

    # 2) Emoji overlap (existing)
    ea = emoji_count(a)
    eb = emoji_count(b)
    emoji_overlap = 1 - _safe_ratio(abs(ea - eb), max(1, max(ea, eb)))

    # 3) Token set Jaccard (new)
    set_a = set(ta)
    set_b = set(tb)
    token_inter = len(set_a & set_b)
    token_union = len(set_a | set_b) or 1
    token_jaccard = _safe_ratio(token_inter, token_union)

    # 4) Length similarity (new): compare total token counts
    len_a = len(ta)
    len_b = len(tb)
    max_len = max(1, max(len_a, len_b))
    length_similarity = 1 - (abs(len_a - len_b) / max_len)

    # 5) Vocabulary richness similarity (new): type-token ratio similarity
    ttr_a = _safe_ratio(len(set_a), len_a)
    ttr_b = _safe_ratio(len(set_b), len_b)
    vocab_similarity = 1 - abs(ttr_a - ttr_b)

    return {
        "ngram_jaccard": round(ngram_jaccard, 2),
        "emoji_overlap": round(emoji_overlap, 2),
        "token_jaccard": round(token_jaccard, 2),
        "length_similarity": round(length_similarity, 2),
        "vocab_similarity": round(vocab_similarity, 2),
    }


