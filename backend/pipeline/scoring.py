"""Ad-break scoring (s14). Pure functions over cached stage data; no LLM calls."""
from __future__ import annotations

from statistics import mean

SENTIMENT_WEIGHT = {"positive": 1.0, "neutral": 0.7, "negative": 0.3}
PRESENCE_WEIGHT = {"mentioned_and_shown": 1.0, "mentioned_only": 0.9, "shown_only": 0.8, "unverified": 0.6}


def score_candidate(*, pause_len: float, scene_boundary: bool, distance_to_end: float, intensity: float, context_match: float, speech: bool, cliffhanger: bool) -> dict[str, float]:
    pause = min(max(pause_len / 2.5, 0), 1)
    scene_end = 1.0 if scene_boundary else max(0, 1 - distance_to_end / 30)
    low_intensity = 1 - min(max(intensity, 0), 1)
    speech_penalty = 1.0 if speech else 0.0
    cliffhanger_penalty = 1.0 if cliffhanger else 0.0
    total = .25 * pause + .25 * scene_end + .30 * low_intensity + .20 * context_match - .50 * speech_penalty - .40 * cliffhanger_penalty
    return {
        "pause": round(pause, 4), "scene_end": round(scene_end, 4), "low_intensity": round(low_intensity, 4),
        "context_match": round(context_match, 4), "speech_penalty": speech_penalty,
        "cliffhanger_penalty": cliffhanger_penalty, "total": round(min(max(total, 0), 1), 4),
    }


def disruption(score: dict[str, float]) -> str:
    penalised = score["speech_penalty"] > 0 or score["cliffhanger_penalty"] > 0
    if score["low_intensity"] < .35 or penalised:
        return "high"
    if score["low_intensity"] >= .6:
        return "low"
    return "medium"


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
    """During a protected scene's build-up, up to `guard` s after its (latest) peak; the scene *end* itself is allowed."""
    for scene in scenes:
        if scene["scene_id"] not in protected:
            continue
        # Breaking at the cut into or out of the scene is not inside its build-up.
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


def reason_text(kind: str, scene: dict, pause_len: float, score: dict[str, float], hits: list[tuple[dict, float, float]], time_value: float) -> str:
    parts = [f"Scene boundary after '{scene['semantic']['title']}'" if kind == "scene_boundary" else f"Dialogue pause inside '{scene['semantic']['title']}'"]
    parts.append(f"{pause_len:.1f} s pause" if pause_len else "no measured pause")
    level = "low" if score["low_intensity"] >= .6 else "high" if score["low_intensity"] < .35 else "moderate"
    parts.append(f"{level} intensity ({1 - score['low_intensity']:.2f})")
    if hits:
        entity, _, mention_time = hits[0]
        categories = ", ".join(entity.get("ad_categories") or []) or "no category"
        parts.append(f"{entity.get('sentiment', 'neutral')} {entity['name']} mention {time_value - mention_time:.0f} s earlier → {categories}")
    if score["speech_penalty"]:
        parts.append("speech at the cut")
    if score["cliffhanger_penalty"]:
        parts.append("inside cliffhanger build-up")
    return "; ".join(parts) + "."


def select_candidates(candidates: list[dict], min_gap: float, count: int) -> list[dict]:
    ranked = sorted(candidates, key=lambda candidate: candidate["score"]["total"], reverse=True)
    selected: list[float] = []
    for candidate in ranked:
        candidate["selected"] = len(selected) < count and all(abs(candidate["time"] - time) >= min_gap for time in selected)
        if candidate["selected"]:
            selected.append(candidate["time"])
    return ranked
