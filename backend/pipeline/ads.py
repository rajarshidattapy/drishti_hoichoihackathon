"""Ad decision pipeline, in strict order:

1. hard constraints            -> reasons attached to each candidate
2. eliminate invalid candidates -> `eligible = False`
3. boundary safety scoring     -> `score.total` (placement quality only, no brand signal)
4. pacing / ad-load            -> greedy by safety with min_gap, n_breaks and a safety floor
5. negative-context filtering  -> brands whose negative_contexts match are excluded (hard)
6. contextual brand ranking    -> remaining brands ranked from catalogue metadata

Everything is derived from stage data and the catalogue (`docs/brands.json`); there are no
hard-coded timestamps, scenes or brand assignments. "No break" is a valid outcome.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from app.settings import Thresholds
from pipeline.scoring import cliffhanger_blocked, context_match, curve_mean, speech_near

TOKEN = re.compile(r"[^\s.,;:!?।\"'()\[\]{}/\\\-–—]+")


def load_catalogue(path: Path) -> list[dict]:
    """Advertiser catalogue (docs/brands.json). Adding a brand there needs no code change or reprocessing."""
    brands = []
    for brand in json.loads(path.read_text(encoding="utf-8")):
        brands.append({
            "brand_id": str(brand["brand_id"]), "name": str(brand.get("display_name", brand["brand_id"])),
            "category": str(brand.get("category", "")),
            "preferred_contexts": [str(v) for v in brand.get("target_contexts", [])],
            "negative_contexts": [str(v) for v in brand.get("negative_contexts", [])],
            "creatives": [
                {"id": str(c.get("id") or f"{brand['brand_id']}_{i}"), "duration": float(c.get("duration_sec", 15)),
                 "language": str(c.get("language", "")).lower(), "url": c.get("url")}
                for i, c in enumerate(brand.get("creatives", []))
            ],
        })
    return brands


# Longest ad a break can carry, by boundary safety: cleaner breaks tolerate longer creatives.
CREATIVE_LENGTH_BY_SAFETY = ((.75, 30.0), (.60, 20.0), (0.0, 15.0))


def pick_creative(brand: dict, safety: float, language: str) -> dict | None:
    """Episode-language creatives first (any language only if the brand has none),
    then the longest one the break's safety allows, else the shortest available."""
    creatives = brand.get("creatives", [])
    matching = [c for c in creatives if c["language"] == language] or creatives
    if not matching:
        return None
    limit = next(seconds for floor, seconds in CREATIVE_LENGTH_BY_SAFETY if safety >= floor)
    fitting = [c for c in matching if c["duration"] <= limit]
    choice = max(fitting, key=lambda c: c["duration"]) if fitting else min(matching, key=lambda c: c["duration"])
    return {**choice, "max_seconds": limit, "language_match": choice["language"] == language}


def category_terms(category: str) -> list[str]:
    """Free-text categories ("food/spices/cooking") become matchable words."""
    return [term.strip() for term in re.split(r"[/,|]", category) if term.strip()]


def tokens(text: str) -> list[str]:
    return TOKEN.findall(text.casefold())


def phrase_in(phrase: str, words: list[str]) -> bool:
    """Whole-phrase match on tokens; single words also match inflected/plural forms by prefix (ফোনটা, phones)."""
    needle = tokens(phrase)
    if not needle:
        return False
    if len(needle) == 1:
        word = needle[0]
        # Bengali words are short in code points (চা, ফোন); require 3+ only for Latin script.
        minimum = 3 if word.isascii() else 2
        return any(t == word or (len(word) >= minimum and t.startswith(word)) for t in words)
    return any(words[i:i + len(needle)] == needle for i in range(len(words) - len(needle) + 1))


def _scene_terms(scene: dict | None) -> list[str]:
    if not scene:
        return []
    semantic, visual = scene.get("semantic", {}), scene.get("visual", {})
    parts = [semantic.get("title", ""), semantic.get("summary", ""), semantic.get("mood", ""), " ".join(semantic.get("topics", [])),
             visual.get("location", ""), visual.get("activity", ""), " ".join(visual.get("objects", [])), " ".join(visual.get("visible_brands", []))]
    return tokens(" ".join(p for p in parts if p and p not in {"unknown", "neutral"}))


def candidate_context(time_value: float, scene: dict, next_scene: dict | None, entities: list[dict], utterances: list[dict], lookback: float) -> dict:
    """Context around a break: what came before (brand fit and safety) and what follows (safety only)."""
    recent_entities = [
        e for e in entities
        if e["entity_id"] in scene.get("entity_ids", []) or any(time_value - lookback <= m["time"] <= time_value for m in e.get("mentions", []))
    ]
    recent_dialogue = [u["text"] for u in utterances if time_value - lookback <= u["start"] <= time_value]
    before = _scene_terms(scene) + tokens(" ".join(
        [e["name"] for e in recent_entities] + [e.get("name_bn") or "" for e in recent_entities] + recent_dialogue
    ))
    upcoming = [u["text"] for u in utterances if time_value <= u["start"] <= time_value + 30]
    after = _scene_terms(next_scene) + tokens(" ".join(upcoming))
    categories = sorted({c for e in recent_entities for c in e.get("ad_categories", [])})
    before += tokens(" ".join(c.replace("_", " ") for c in categories))
    return {"before": sorted(set(before)), "after": sorted(set(after)), "categories": categories}


def generate_candidates(
    *, duration: float, scenes: list[dict], silences: list[dict], utterances: list[dict], entities: list[dict],
    intensity: list[list[float]], protected: set[str], t: Thresholds,
) -> list[dict]:
    """Candidate positions with hard-constraint flags, safety components and context. No selection here."""
    raw: list[tuple[str, float, float, int]] = []
    used: set[int] = set()
    for index, scene in enumerate(scenes[:-1]):
        cut = scene["end"]
        near = [(i, s) for i, s in enumerate(silences) if abs((s["start"] + s["end"]) / 2 - cut) <= t.ad_snap_to_silence_seconds]
        if near:
            i, silence = min(near, key=lambda item: abs((item[1]["start"] + item[1]["end"]) / 2 - cut))
            used.add(i)
            raw.append(("scene_boundary", round((silence["start"] + silence["end"]) / 2, 3), silence["duration"], index))
        else:
            raw.append(("scene_boundary", cut, 0.0, index))
    cuts = [scene["end"] for scene in scenes[:-1]]
    for i, silence in enumerate(silences):
        if i in used:
            continue
        midpoint = (silence["start"] + silence["end"]) / 2
        if any(abs(midpoint - cut) < 5 for cut in cuts):
            continue  # the scene-boundary candidate already covers this spot
        index = next((n for n, s in enumerate(scenes) if s["start"] < midpoint < s["end"]), None)
        if index is not None:
            raw.append(("dialogue_pause", round(midpoint, 3), silence["duration"], index))

    candidates = []
    for kind, time_value, pause_len, index in sorted(raw, key=lambda item: item[1]):
        scene = scenes[index]
        next_scene = scenes[index + 1] if index + 1 < len(scenes) else None
        window = curve_mean(intensity, time_value - 20, time_value + 5)
        level = scene["semantic"]["narrative_intensity"] if window is None else window
        speech = speech_near(time_value, utterances, t.ad_speech_guard_seconds)
        cliff = cliffhanger_blocked(time_value, scenes, intensity, t.ad_cliffhanger_guard_seconds, t.ad_snap_to_silence_seconds, protected)
        rejections = []
        if speech:
            rejections.append("speech_at_cut")
        if cliff:
            rejections.append("cliffhanger_buildup")
        if kind == "dialogue_pause" and pause_len < t.min_ad_pause_seconds:
            rejections.append("pause_too_short")
        if kind == "dialogue_pause" and scene["semantic"]["narrative_intensity"] >= t.ad_pause_intensity_ceiling:
            rejections.append("mid_scene_intensity")
        best, hits = context_match(time_value, entities, t.ad_context_lookback)
        pause = min(max(pause_len / 2.5, 0), 1)
        scene_end = 1.0 if kind == "scene_boundary" else max(0.0, 1 - (scene["end"] - time_value) / 30)
        low = 1 - min(max(level, 0), 1)
        candidates.append({
            "cand_id": f"ad_{len(candidates) + 1:04d}", "time": time_value, "scene_id": scene["scene_id"], "kind": kind,
            "pause_len": round(pause_len, 3),
            "score": {
                "pause": round(pause, 4), "scene_end": round(scene_end, 4), "low_intensity": round(low, 4),
                "context_match": round(best, 4), "speech_penalty": float(speech), "cliffhanger_penalty": float(cliff),
                "total": round(.3 * pause + .3 * scene_end + .4 * low, 4),
            },
            "disruption": "low" if low >= .6 else "high" if low < .35 else "medium",
            "matched_categories": sorted({c for e, v, _ in hits if v > 0 for c in e.get("ad_categories", [])}),
            "context_entity_ids": [e["entity_id"] for e, v, _ in hits if v > 0],
            "context": candidate_context(time_value, scene, next_scene, entities, utterances, t.ad_context_lookback),
            "scene_title": scene["semantic"]["title"], "hard_rejections": rejections,
            "reason": "", "selected": False, "eligible": not rejections, "rejections": list(rejections),
            "brand": None, "brand_ranking": [], "excluded_brands": [],
        })
    return candidates


def rank_brands(context: dict, catalogue: list[dict], entities_weight: float) -> tuple[list[dict], list[dict]]:
    """Steps 5 and 6: hard negative-context filter, then contextual ranking of what survives."""
    before, after = context.get("before", []), context.get("after", [])
    excluded, ranked = [], []
    for brand in catalogue:
        negatives = [term for term in brand["negative_contexts"] if phrase_in(term, before) or phrase_in(term, after)]
        if negatives:
            excluded.append({"brand_id": brand["brand_id"], "name": brand["name"], "matched_negative": negatives})
            continue
        preferred = list(dict.fromkeys(term for term in brand["preferred_contexts"] + category_terms(brand["category"]) if phrase_in(term, before)))
        # Entity ad categories (e.g. "food_delivery") against the brand's category words (e.g. "food/spices/cooking").
        entity_words = tokens(" ".join(c.replace("_", " ") for c in context.get("categories", [])))
        category = 1.0 if any(phrase_in(term, entity_words) for term in category_terms(brand["category"])) else 0.0
        fit = min(1.0, len(preferred) / 3) if brand["preferred_contexts"] else 0.0
        score = round(.6 * category * max(entities_weight, .5) + .4 * fit, 4)
        ranked.append({"brand_id": brand["brand_id"], "name": brand["name"], "category": brand["category"], "score": score,
                       "matched_preferred": preferred, "category_match": bool(category)})
    ranked.sort(key=lambda item: (-item["score"], item["name"]))
    return ranked, excluded


def _reason(candidate: dict) -> str:
    kind = "Scene boundary after" if candidate["kind"] == "scene_boundary" else "Pause inside"
    s = candidate["score"]
    parts = [f"{kind} '{candidate['scene_title']}'", f"{candidate['pause_len']:.1f} s pause" if candidate["pause_len"] else "no measured pause",
             f"safety {s['total']:.2f} (intensity {1 - s['low_intensity']:.2f})"]
    if candidate["rejections"]:
        parts.append("rejected: " + ", ".join(r.replace("_", " ") for r in candidate["rejections"]))
    brand = candidate.get("brand")
    if brand:
        why = ", ".join(brand["matched_preferred"][:3]) or ("category match" if brand["category_match"] else "best remaining fit")
        creative = candidate.get("creative")
        spot = f", {creative['duration']:.0f} s {creative['language'] or 'any-language'} spot" if creative else ""
        parts.append(f"→ {brand['name']} ({why}{spot})")
    if candidate["excluded_brands"]:
        parts.append("excluded " + ", ".join(f"{b['name']} ({b['matched_negative'][0]})" for b in candidate["excluded_brands"][:2]))
    return "; ".join(parts) + "."


def decide(candidates: list[dict], catalogue: list[dict], *, duration: float, min_gap: float, n_breaks: int,
           blocked: tuple[float, float], min_safety: float, language: str = "bn") -> tuple[list[dict], dict]:
    """Run steps 1-6 over cached candidates. Pure and fast, so the API re-runs it on every settings change."""
    head, tail = blocked
    output = []
    for original in candidates:
        c = {**original, "selected": False, "brand": None, "creative": None, "brand_ranking": [], "excluded_brands": [], "decision_note": None}
        rejections = list(c.get("hard_rejections", []))
        if not head <= c["time"] <= duration - tail:
            rejections.append("blocked_zone")
        if not rejections and c["score"]["total"] < min_safety:
            rejections.append("below_safety_floor")
        c["rejections"], c["eligible"] = rejections, not rejections
        if c["eligible"]:
            # Ranked for every eligible position so the debug output shows the full reasoning.
            c["brand_ranking"], c["excluded_brands"] = rank_brands(c["context"], catalogue, c["score"]["context_match"])
        else:
            c["decision_note"] = "ineligible"
        output.append(c)

    chosen: list[float] = []
    for c in sorted((c for c in output if c["eligible"]), key=lambda c: -c["score"]["total"]):
        if len(chosen) >= n_breaks:
            c["decision_note"] = "ad_load_limit"
            continue
        if any(abs(c["time"] - t) < min_gap for t in chosen):
            c["decision_note"] = "min_gap"
            continue
        if not c["brand_ranking"]:
            c["decision_note"] = "no_brand_safe"
            continue
        c["brand"], c["selected"], c["decision_note"] = c["brand_ranking"][0], True, "selected"
        brand = next(b for b in catalogue if b["brand_id"] == c["brand"]["brand_id"])
        c["creative"] = pick_creative(brand, c["score"]["total"], language)
        chosen.append(c["time"])
    for c in output:
        c["reason"] = _reason(c)

    selected = sorted((c for c in output if c["selected"]), key=lambda c: c["time"])
    summary = {
        "outcome": "breaks" if selected else "no_break",
        "selected": [{"cand_id": c["cand_id"], "time": c["time"], "brand_id": c["brand"]["brand_id"], "creative_id": (c["creative"] or {}).get("id")} for c in selected],
        "settings": {"min_gap": min_gap, "n_breaks": n_breaks, "blocked": list(blocked), "min_safety": min_safety, "language": language},
        "counts": {"candidates": len(output), "eligible": sum(c["eligible"] for c in output), "selected": len(selected)},
        "reason": None if selected else "No candidate satisfied the hard constraints, safety floor, pacing and brand-safety rules.",
        "catalogue_brands": [b["brand_id"] for b in catalogue],
    }
    return sorted(output, key=lambda c: c["time"]), summary


def select_brand_for(candidate: dict, catalogue: list[dict], language: str = "bn") -> dict:
    """Manual selection from the UI: still subject to the hard constraints and brand-safety filter."""
    ranked, excluded = rank_brands(candidate["context"], catalogue, candidate["score"]["context_match"])
    brand = next((b for b in catalogue if ranked and b["brand_id"] == ranked[0]["brand_id"]), None)
    creative = pick_creative(brand, candidate["score"]["total"], language) if brand else None
    return {**candidate, "brand_ranking": ranked, "excluded_brands": excluded, "brand": ranked[0] if ranked else None, "creative": creative}

