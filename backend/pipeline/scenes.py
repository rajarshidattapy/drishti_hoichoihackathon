"""Scene segmentation helpers for s10: boundary scoring, merging and tag aggregation."""
from __future__ import annotations

from collections import defaultdict
from typing import Sequence

from app.settings import Thresholds


UNKNOWN_VISUAL = {
    "location": "unknown", "indoor": None, "objects": [], "visible_brands": [],
    "activity": "unknown", "visual_mood": "neutral", "people_count": 0, "confidence": 0.0,
}


def hash_distance(a: str | None, b: str | None) -> float | None:
    """Normalised dHash distance in 0..1. Unrelated images differ in about half of 64 bits."""
    if not a or not b:
        return None
    bits = (int(a, 16) ^ int(b, 16)).bit_count()
    return min(1.0, bits / 32)


def color_distance(a: Sequence[float] | None, b: Sequence[float] | None) -> float | None:
    """Mean-RGB distance in 0..1 (half the RGB-cube diagonal saturates at 1)."""
    if not a or not b:
        return None
    return min(1.0, sum((x - y) ** 2 for x, y in zip(a, b)) ** .5 / (255 * 3 ** .5 / 2))


def cosine_distance(a: Sequence[float] | None, b: Sequence[float] | None) -> float | None:
    if a is None or b is None:
        return None
    dot = sum(x * y for x, y in zip(a, b))
    norm = (sum(x * x for x in a) ** .5) * (sum(y * y for y in b) ** .5)
    if not norm:
        return None
    return max(0.0, min(1.0, 1 - dot / norm))


def visual_change(shots: list[dict], index: int, embeddings: dict[str, list[float]] | None = None, window: int = 2) -> float:
    """Dissimilarity across the cut after shots[index], averaged over ±window shots."""
    before = shots[max(0, index - window + 1): index + 1]
    after = shots[index + 1: index + 1 + window]
    distances: list[float] = []
    for left in before:
        for right in after:
            if embeddings:
                value = cosine_distance(embeddings.get(left["shot_id"]), embeddings.get(right["shot_id"]))
            else:
                signals = [d for d in (hash_distance(left.get("dhash"), right.get("dhash")), color_distance(left.get("color"), right.get("color"))) if d is not None]
                value = max(signals) if signals else None
            if value is not None:
                distances.append(value)
    return sum(distances) / len(distances) if distances else 0.0


def location_changed(left: dict, right: dict) -> float:
    a, b = (left.get("location") or "unknown").casefold(), (right.get("location") or "unknown").casefold()
    if "unknown" in (a, b):
        return 0.0
    return float(a != b)


def speaker_set_change(utterances: list[dict], cut: float, window: float) -> float:
    before = {u["speaker"] for u in utterances if cut - window <= u["start"] < cut}
    after = {u["speaker"] for u in utterances if cut <= u["start"] < cut + window}
    if not before or not after:
        return 0.0
    return 1 - len(before & after) / len(before | after)


def silence_at_cut(silences: list[dict], cut: float, min_seconds: float, tolerance: float = .25) -> float:
    return float(any(
        s["duration"] >= min_seconds and s["start"] - tolerance <= cut <= s["end"] + tolerance
        for s in silences
    ))


def score_boundaries(
    shots: list[dict], tags: dict[str, dict], utterances: list[dict], silences: list[dict],
    thresholds: Thresholds, embeddings: dict[str, list[float]] | None = None,
) -> list[dict]:
    """Score every cut between consecutive shots (step A of s10)."""
    output = []
    for index in range(len(shots) - 1):
        cut = shots[index]["end"]
        components = {
            "visual": visual_change(shots, index, embeddings),
            "location": location_changed(tags.get(shots[index]["shot_id"], UNKNOWN_VISUAL), tags.get(shots[index + 1]["shot_id"], UNKNOWN_VISUAL)),
            "speakers": speaker_set_change(utterances, cut, thresholds.scene_speaker_window_seconds),
            "silence": silence_at_cut(silences, cut, thresholds.scene_silence_at_cut_seconds),
        }
        score = (
            thresholds.scene_weight_visual * components["visual"]
            + thresholds.scene_weight_location * components["location"]
            + thresholds.scene_weight_speakers * components["speakers"]
            + thresholds.scene_weight_silence * components["silence"]
        )
        output.append({"after_shot": index, "time": cut, "score": round(score, 4), "components": {k: round(v, 4) for k, v in components.items()}})
    return output


def enforce_min_length(boundaries: list[dict], duration: float, min_seconds: float) -> list[dict]:
    """Drop the weakest boundary touching a too-short scene until every scene is long enough."""
    kept = sorted(boundaries, key=lambda b: b["time"])
    while kept:
        edges = [0.0] + [b["time"] for b in kept] + [duration]
        short = [i for i in range(len(edges) - 1) if edges[i + 1] - edges[i] < min_seconds]
        if not short:
            break
        touching: set[int] = set()
        for scene_index in short:
            if scene_index > 0:
                touching.add(scene_index - 1)
            if scene_index < len(kept):
                touching.add(scene_index)
        weakest = min(touching, key=lambda i: kept[i]["score"])
        kept.pop(weakest)
    return kept


def candidate_boundaries(scored: list[dict], duration: float, thresholds: Thresholds) -> list[dict]:
    chosen = [b for b in scored if b["score"] >= thresholds.scene_boundary_threshold]
    return enforce_min_length(chosen, duration, thresholds.min_scene_seconds)


def build_scenes(shots: list[dict], boundaries: list[dict], duration: float) -> list[dict]:
    edges = [0.0] + sorted(b["time"] for b in boundaries) + [duration]
    scenes = []
    for index, (start, end) in enumerate(zip(edges, edges[1:])):
        if end - start <= 0:
            continue
        members = [s["shot_id"] for s in shots if s["start"] < end - 1e-6 and s["end"] > start + 1e-6]
        scenes.append({"scene_id": f"scene_{len(scenes) + 1:04d}", "start": round(start, 3), "end": round(end, 3), "shot_ids": members})
    return scenes


def merge_scenes(scenes: list[dict], merge_after: set[int]) -> list[dict]:
    """Merge scene i with i+1 for every i in merge_after, then renumber."""
    merged: list[dict] = []
    for index, scene in enumerate(scenes):
        if merged and (index - 1) in merge_after:
            merged[-1] = {**merged[-1], "end": scene["end"], "shot_ids": merged[-1]["shot_ids"] + scene["shot_ids"]}
        else:
            merged.append(dict(scene))
    for index, scene in enumerate(merged):
        scene["scene_id"] = f"scene_{index + 1:04d}"
    return merged


def aggregate_visual(shots: list[dict], tags: dict[str, dict]) -> dict:
    """Duration-weighted majority location plus objects weighted by the share of shot time they appear in."""
    total = sum(max(0.0, s["end"] - s["start"]) for s in shots)
    if not shots or total <= 0:
        return dict(UNKNOWN_VISUAL)
    location_weight: dict[str, float] = defaultdict(float)
    activity_weight: dict[str, float] = defaultdict(float)
    mood_weight: dict[str, float] = defaultdict(float)
    indoor_weight: dict[bool, float] = defaultdict(float)
    object_weight: dict[str, float] = defaultdict(float)
    brands: list[str] = []
    people = 0
    confidence = 0.0
    for shot in shots:
        weight = max(0.0, shot["end"] - shot["start"]) / total
        tag = tags.get(shot["shot_id"]) or UNKNOWN_VISUAL
        location_weight[tag["location"]] += weight
        activity_weight[tag["activity"]] += weight
        mood_weight[tag["visual_mood"]] += weight
        if tag.get("indoor") is not None:
            indoor_weight[bool(tag["indoor"])] += weight
        for item in set(tag.get("objects", [])):
            object_weight[item] += weight
        for brand in tag.get("visible_brands", []):
            if brand not in brands:
                brands.append(brand)
        people = max(people, int(tag.get("people_count", 0)))
        confidence += weight * float(tag.get("confidence", 0))

    def majority(weights: dict[str, float], default: str) -> str:
        known = {k: v for k, v in weights.items() if k and k != "unknown"}
        return max(known, key=known.__getitem__) if known else default

    objects = [name for name, weight in sorted(object_weight.items(), key=lambda kv: -kv[1]) if weight >= .1]
    return {
        "location": majority(location_weight, "unknown"),
        "indoor": max(indoor_weight, key=indoor_weight.__getitem__) if indoor_weight else None,
        "objects": objects[:12],
        "visible_brands": brands,
        "activity": majority(activity_weight, "unknown"),
        "visual_mood": majority(mood_weight, "neutral"),
        "people_count": people,
        "confidence": round(confidence, 4),
    }


def scene_digest(scene: dict, shots: list[dict], tags: dict[str, dict], utterances: list[dict]) -> str:
    scene_shots = [s for s in shots if s["shot_id"] in set(scene["shot_ids"])]
    visual = aggregate_visual(scene_shots, tags)
    lines = [u for u in utterances if scene["start"] <= u["start"] < scene["end"]]
    head = lines[:3]
    tail = lines[-3:] if len(lines) > 3 else []
    dialogue = "\n".join(f"  {u['speaker']}: {u['text']}" for u in head)
    if tail:
        dialogue += "\n  …\n" + "\n".join(f"  {u['speaker']}: {u['text']}" for u in tail)
    return (
        f"{scene['start']:.1f}-{scene['end']:.1f}s, {len(scene_shots)} shots, location={visual['location']}, "
        f"objects={', '.join(visual['objects'][:6]) or 'none'}\n{dialogue or '  (no dialogue)'}"
    )
