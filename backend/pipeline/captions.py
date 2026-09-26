"""Closed-caption assembly (s16): dialogue cues plus sound and music cues."""
from __future__ import annotations

from app.settings import Thresholds

MOOD_BN = {
    "tense": "উত্তেজনাপূর্ণ", "suspenseful": "রহস্যময়", "ominous": "রহস্যময়", "mysterious": "রহস্যময়",
    "sad": "বিষণ্ণ", "melancholic": "বিষণ্ণ", "somber": "বিষণ্ণ", "romantic": "রোমান্টিক",
    "happy": "আনন্দের", "joyful": "আনন্দের", "playful": "হালকা", "calm": "শান্ত", "reflective": "শান্ত",
    "dramatic": "নাটকীয়", "energetic": "উচ্ছল", "lively": "উচ্ছল",
}


def dialogue_overlap_ratio(start: float, end: float, utterances: list[dict]) -> float:
    span = max(1e-6, end - start)
    covered = sum(max(0.0, min(end, u["end"]) - max(start, u["start"])) for u in utterances)
    return min(1.0, covered / span)


def finalize_events(events: list[dict], utterances: list[dict], thresholds: Thresholds) -> list[dict]:
    """Apply the dialogue-overlap part of the in_cc rule (needs the transcript, so it runs here)."""
    output = []
    for event in events:
        in_cc = bool(event.get("in_cc")) and dialogue_overlap_ratio(event["start"], event["end"], utterances) <= thresholds.audio_event_max_dialogue_overlap
        output.append({**event, "in_cc": in_cc})
    return output


def _overlapping(cues: list[dict], start: float, end: float) -> list[dict]:
    return [cue for cue in cues if cue["start"] < end and cue["end"] > start]


def _find_gap(cues: list[dict], wanted: float, length: float, shift: float, gap: float) -> float | None:
    """Earliest-nearest start in [wanted - shift, wanted + shift] where `length` seconds fit between cues."""
    ordered = sorted(cues, key=lambda cue: cue["start"])
    edges = [(-float("inf"), 0.0)] + [(c["start"], c["end"]) for c in ordered] + [(float("inf"), float("inf"))]
    best: float | None = None
    for (_, previous_end), (next_start, _) in zip(edges, edges[1:]):
        free_start, free_end = max(0.0, previous_end + gap), next_start - gap
        if free_end - free_start < length:
            continue
        candidate = min(max(wanted, free_start), free_end - length)
        if abs(candidate - wanted) <= shift and (best is None or abs(candidate - wanted) < abs(best - wanted)):
            best = candidate
    return best


def build_cc(dialogue: list[dict], events: list[dict], scenes: list[dict], thresholds: Thresholds) -> list[dict]:
    cues = [dict(cue, lines=list(cue["lines"])) for cue in dialogue]
    sound: list[dict] = []
    for event in sorted((e for e in events if e.get("in_cc")), key=lambda e: e["start"]):
        label = f"[{event['label_bn']}]"
        start = float(event["start"])
        end = min(start + thresholds.subtitle_max_duration, max(start + thresholds.subtitle_min_duration, float(event["end"])))
        hits = _overlapping(cues, start, end)
        if hits:
            first = hits[0]
            if len(first["lines"]) == 1:
                first["lines"] = [label] + first["lines"]
                continue
            placed = _find_gap(cues + sound, start, thresholds.subtitle_min_duration, thresholds.cc_sound_shift_seconds, thresholds.subtitle_min_gap)
            if placed is None:
                continue
            start, end = placed, placed + thresholds.subtitle_min_duration
        elif _overlapping(sound, start, end):
            continue
        sound.append({"idx": 0, "start": round(start, 3), "end": round(end, 3), "lines": [label], "speakers": [], "kind": "sound", "cps": 0.0})

    for scene in scenes:
        if scene.get("music_ratio", 0) <= thresholds.cc_music_ratio:
            continue
        occupied = sorted(_overlapping(cues + sound, scene["start"], scene["end"]), key=lambda cue: cue["start"])
        cursor = scene["start"]
        free = None
        for cue in occupied + [{"start": scene["end"], "end": scene["end"]}]:
            if cue["start"] - cursor >= thresholds.cc_music_min_gap:
                free = cursor
                break
            cursor = max(cursor, cue["end"])
        if free is None:
            continue
        adjective = MOOD_BN.get(str(scene.get("semantic", {}).get("mood", "")).casefold())
        label = f"[{adjective} সঙ্গীত]" if adjective else "[সঙ্গীত]"
        start = free + thresholds.subtitle_min_gap
        sound.append({"idx": 0, "start": round(start, 3), "end": round(start + 2.0, 3), "lines": [label], "speakers": [], "kind": "sound", "cps": 0.0})

    merged = sorted(cues + sound, key=lambda cue: (cue["start"], cue["kind"] != "sound"))
    for index, cue in enumerate(merged):
        cue["idx"] = index + 1
    return merged
