def identity_confidence(style: dict, image: dict) -> dict:
    # Aggregate enhanced style metrics
    style_score = (
        0.35 * style.get("ngram_jaccard", 0)
        + 0.2 * style.get("token_jaccard", 0)
        + 0.15 * style.get("emoji_overlap", 0)
        + 0.15 * style.get("length_similarity", 0)
        + 0.15 * style.get("vocab_similarity", 0)
    )

    # Aggregate image metrics
    image_score = 0.75 * image.get("face_similarity", 0) + 0.25 * min(
        image.get("reverse_image_hits", 0) / 5, 1
    )

    score = 0.5 * style_score + 0.5 * image_score
    score = round(score, 2)

    label = (
        "high" if score >= 0.75 else "medium" if score >= 0.45 else "low"
    )

    components = {
        "style": round(style_score, 2),
        "image": round(image_score, 2),
    }

    summary = (
        f"Writing ngram {int(style.get('ngram_jaccard', 0)*100)}%, "
        f"token {int(style.get('token_jaccard', 0)*100)}%, "
        f"emoji {int(style.get('emoji_overlap', 0)*100)}%, "
        f"length {int(style.get('length_similarity', 0)*100)}%, "
        f"vocab {int(style.get('vocab_similarity', 0)*100)}%; "
        f"image {int(image.get('face_similarity', 0)*100)}% + hits {image.get('reverse_image_hits', 0)}. "
        f"Overall {int(score*100)}% ({label})."
    )

    return {"score": score, "label": label, "components": components, "summary": summary}


