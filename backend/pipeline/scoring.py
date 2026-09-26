from __future__ import annotations


def score_candidate(*, pause_len: float, scene_boundary: bool, distance_to_end: float, intensity: float, context_match: float, speech: bool, cliffhanger: bool) -> dict[str, float]:
    pause = min(max(pause_len / 2.5, 0), 1)
    scene_end = 1.0 if scene_boundary else max(0, 1 - distance_to_end / 30)
    low_intensity = 1 - min(max(intensity, 0), 1)
    speech_penalty = 1.0 if speech else 0.0
    cliffhanger_penalty = 1.0 if cliffhanger and not scene_boundary else 0.0
    total = .25 * pause + .25 * scene_end + .30 * low_intensity + .20 * context_match - .50 * speech_penalty - .40 * cliffhanger_penalty
    return {
        "pause": round(pause, 4), "scene_end": round(scene_end, 4), "low_intensity": round(low_intensity, 4),
        "context_match": round(context_match, 4), "speech_penalty": speech_penalty,
        "cliffhanger_penalty": cliffhanger_penalty, "total": round(min(max(total, 0), 1), 4),
    }


def select_candidates(candidates: list[dict], min_gap: float, count: int) -> list[dict]:
    ranked = sorted(candidates, key=lambda candidate: candidate["score"]["total"], reverse=True)
    selected: list[float] = []
    for candidate in ranked:
        candidate["selected"] = len(selected) < count and all(abs(candidate["time"] - time) >= min_gap for time in selected)
        if candidate["selected"]:
            selected.append(candidate["time"])
    return ranked

