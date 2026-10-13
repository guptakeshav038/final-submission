"""Explainable compatibility scoring.

Base weights follow the CreatorX deck: demographics 30, niche 25, engagement 20,
location 10, content quality 10, past ROI 5. A campaign goal re-weights them.
"""
import math
import re
from collections import Counter

DIMENSIONS = ["demographics", "niche", "engagement", "location", "content_quality", "past_roi"]

GOAL_WEIGHTS = {
    "balanced": {"demographics": 0.30, "niche": 0.25, "engagement": 0.20, "location": 0.10, "content_quality": 0.10, "past_roi": 0.05},
    "awareness": {"demographics": 0.35, "niche": 0.25, "engagement": 0.15, "location": 0.10, "content_quality": 0.10, "past_roi": 0.05},
    "conversion": {"demographics": 0.25, "niche": 0.20, "engagement": 0.25, "location": 0.10, "content_quality": 0.05, "past_roi": 0.15},
    "local_launch": {"demographics": 0.25, "niche": 0.20, "engagement": 0.15, "location": 0.25, "content_quality": 0.10, "past_roi": 0.05},
}

STOPWORDS = {"a", "an", "and", "the", "of", "for", "to", "in", "on", "with", "is", "are", "we", "our", "my", "i", "you", "your", "at", "by", "from"}


def _tokens(text: str) -> Counter:
    words = re.findall(r"[a-z0-9]+", (text or "").lower())
    return Counter(w for w in words if w not in STOPWORDS and len(w) > 1)


def _cosine(a: Counter, b: Counter) -> float:
    if not a or not b:
        return 0.0
    dot = sum(a[t] * b[t] for t in a.keys() & b.keys())
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


def _pct(x: float) -> int:
    return round(x * 100)


def demographics(c, camp) -> tuple[float, str]:
    parts = []  # (share 0..1, weight, text)
    if camp.target_age_buckets:
        share = sum((c.audience_age or {}).get(b, 0) for b in camp.target_age_buckets)
        parts.append((min(share, 1.0), 0.5, f"{_pct(min(share, 1.0))}% of the audience is aged {', '.join(camp.target_age_buckets)}"))
    if camp.target_gender and camp.target_gender != "any":
        share = (c.audience_gender or {}).get(camp.target_gender, 0)
        parts.append((share, 0.25, f"{_pct(share)}% of the audience is {camp.target_gender}"))
    if camp.target_country:
        share = (c.audience_countries or {}).get(camp.target_country, 0)
        parts.append((share, 0.25, f"{_pct(share)}% of the audience is in {camp.target_country}"))
    if not parts:
        return 100.0, "The campaign sets no audience targeting"
    total_w = sum(w for _, w, _ in parts)
    score = sum(s * w for s, w, _ in parts) / total_w * 100
    return score, "; ".join(t for _, _, t in parts)


def niche(c, camp) -> tuple[float, str]:
    creator_text = f"{c.niche} {c.niche} {c.bio}"  # tags count double
    campaign_text = f"{camp.niche} {camp.niche} {camp.title} {camp.description}"
    sim = _cosine(_tokens(creator_text), _tokens(campaign_text))
    score = min(1.0, sim * 1.8) * 100  # raw cosine on short texts is low; rescale
    shared = sorted((_tokens(c.niche) & _tokens(camp.niche + " " + camp.description)).keys())
    reason = f"Content overlaps with the brief on: {', '.join(shared)}" if shared else "Little overlap between the creator's topics and the brief"
    return score, reason


def engagement(c, camp) -> tuple[float, str]:
    genuine = max(0.0, min(1.0, c.genuine_engagement_ratio))
    rate = max(0.0, c.engagement_rate)
    score = genuine * 60 + min(rate / 8.0, 1.0) * 40
    return score, f"{rate:.1f}% engagement rate, {_pct(genuine)}% of interactions look genuine"


def location(c, camp) -> tuple[float, str]:
    city, country = (camp.target_city or "").strip().lower(), (camp.target_country or "").strip().lower()
    c_city, c_country = (c.city or "").strip().lower(), (c.country or "").strip().lower()
    if city:
        if c_city == city:
            return 100.0, f"Based in {c.city}, the target city"
        if country and c_country == country:
            return 55.0, f"Based in {c.country}, but not in {camp.target_city}"
        return 0.0, f"Not based in {camp.target_city}"
    if country:
        if c_country == country:
            return 100.0, f"Based in {c.country}"
        return 0.0, f"Not based in {camp.target_country}"
    return 100.0, "The campaign sets no location target"


def content_quality(c, camp) -> tuple[float, str]:
    return float(c.content_quality), f"Production consistency rated {c.content_quality:.0f}/100"


def past_roi(c, camp) -> tuple[float, str]:
    return float(c.past_roi), f"Past campaign delivery rated {c.past_roi:.0f}/100"


SCORERS = {
    "demographics": demographics,
    "niche": niche,
    "engagement": engagement,
    "location": location,
    "content_quality": content_quality,
    "past_roi": past_roi,
}


def score_creator(creator, campaign) -> tuple[float, dict]:
    weights = GOAL_WEIGHTS.get(campaign.goal, GOAL_WEIGHTS["balanced"])
    breakdown, total = {}, 0.0
    for key in DIMENSIONS:
        value, reason = SCORERS[key](creator, campaign)
        value = max(0.0, min(100.0, value))
        points = value * weights[key]
        total += points
        breakdown[key] = {"score": round(value, 1), "weight": weights[key], "points": round(points, 1), "reason": reason}
    return round(total, 1), breakdown
