"""Scoring primitives for ad decisions (see pipeline/ads.py). Pure functions over stage data."""
from __future__ import annotations

from statistics import mean

SENTIMENT_WEIGHT = {"positive": 1.0, "neutral": 0.7, "negative": 0.3}
PRESENCE_WEIGHT = {"mentioned_and_shown": 1.0, "mentioned_only": 0.9, "shown_only": 0.8, "unverified": 0.6}


def curve_mean(curve: list[list[float]], start: float, end: float) -> float | None:
    values = [value for time_value, value in curve if start <= time_value <= end]
    return mean(values) if values else None


def context_match(time_value: float, entities: list[dict], lookback: float) -> tuple[float, list[tuple[dict, float, float]]]:
    """Best entity signal in [t - lookback, t]. Returns (score, [(entity, value, latest_mention_time)])."""
    hits: list[tuple[dict, float, float]] = []
    for entity in entities:
        times = [m["time"] for m in entity.get("mentions", []) if time_value - lookback <= m["time"] <= time_value]
        if not times:
            continue
        value = float(entity.get("confidence", 0)) * SENTIMENT_WEIGHT.get(entity.get("sentiment", "neutral"), .7) * PRESENCE_WEIGHT.get(entity.get("presence", "unverified"), .6)
        hits.append((entity, round(value, 4), max(times)))
    hits.sort(key=lambda hit: -hit[1])
    return (hits[0][1] if hits else 0.0), hits


def speech_near(time_value: float, utterances: list[dict], guard: float) -> bool:
    return any(u["start"] - guard <= time_value <= u["end"] + guard for u in utterances)


def cliffhanger_blocked(time_value: float, scenes: list[dict], intensity: list[list[float]], guard: float, snap: float, protected: set[str]) -> bool:
    """During a protected scene's build-up, up to `guard` s after its (latest) peak; cuts into or out of it are allowed."""
    for scene in scenes:
        if scene["scene_id"] not in protected:
            continue
        if abs(time_value - scene["end"]) <= snap or abs(time_value - scene["start"]) <= snap:
            continue
        inside = [(t, v) for t, v in intensity if scene["start"] <= t < scene["end"]]
        if inside:
            top = max(v for _, v in inside)
            peak = max(t for t, v in inside if v >= top - .02)
        else:
            peak = scene["end"]
        if scene["start"] <= time_value <= peak + guard:
            return True
    return False
