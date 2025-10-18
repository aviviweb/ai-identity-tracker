from ai.ai_investigator.text.style_similarity import style_similarity
from ai.ai_investigator.image.basic_checks import image_similarity
from ai.ai_investigator.correlator.identity_score import identity_confidence


def analyze_text(text_groups: list[list[str]]) -> dict:
    # Compare first two groups as a demo
    g1 = text_groups[0] if text_groups else []
    g2 = text_groups[1] if len(text_groups) > 1 else []
    return style_similarity(g1, g2)


def analyze_images(image_urls: list[str]) -> dict:
    return image_similarity(image_urls)


def correlate_profiles(text_groups: list[list[str]], image_urls: list[str]) -> dict:
    style = analyze_text(text_groups)
    img = analyze_images(image_urls)
    return identity_confidence(style, img)


