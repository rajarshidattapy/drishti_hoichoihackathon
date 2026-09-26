"""Assemble a SemanticTimeline from whatever stage artifacts exist so far.

Lets the episode page open immediately and fill in as stages finish. Later stages
supersede earlier ones (e.g. s07 cleaned text replaces s06 raw text as soon as it lands).
"""
from __future__ import annotations

from app.artifacts import ArtifactStore
from app.db import Database
from app.models import SemanticTimeline
from pipeline.scenes import UNKNOWN_VISUAL


def _first(store: ArtifactStore, episode_id: str, *stage_ids: str) -> dict | None:
    for stage_id in stage_ids:
        path = store.stage_path(episode_id, stage_id)
        if path.exists():
            return store.read_json(path)
    return None


def _placeholder_semantic(title: str) -> dict:
    return {"title": title, "summary": "Scene understanding is still running.", "topics": [], "mood": "neutral",
            "narrative_intensity": 0.0, "intensity_components": {}, "is_cliffhanger": False}


def assemble_partial(store: ArtifactStore, database: Database, episode_id: str) -> SemanticTimeline | None:
    """None until ingest has finished (duration unknown)."""
    ingest = _first(store, episode_id, "s01_ingest")
    if ingest is None:
        return None
    record = database.get_episode_record(episode_id)
    duration = float(ingest["duration"])
    available = [s.stage_id for s in database.get_stages(episode_id) if s.status == "done"]

    shots = (_first(store, episode_id, "s03_keyframes", "s02_shots") or {}).get("shots", [])
    utterances = (_first(store, episode_id, "s07_transcript_clean", "s06_stt") or {}).get("utterances", [])
    semantics = _first(store, episode_id, "s13_scene_semantics")
    if semantics:
        scenes = semantics["scenes"]
    else:
        draft = _first(store, episode_id, "s12_vision_targeted", "s11_entities_dialogue", "s10_scenes")
        scenes = [
            {**s, "semantic": _placeholder_semantic(s.get("draft_title") or f"Scene {i + 1}")}
            for i, s in enumerate((draft or {}).get("scenes", []))
        ] or [{
            "scene_id": "scene_pending", "start": 0.0, "end": duration, "shot_ids": [s["shot_id"] for s in shots],
            "visual": dict(UNKNOWN_VISUAL), "speakers": sorted({u["speaker"] for u in utterances}),
            "utt_ids": [u["utt_id"] for u in utterances], "audio_events": [], "music_ratio": 0.0, "entity_ids": [],
            "semantic": _placeholder_semantic("Detecting scenes…"),
        }]
    audio = _first(store, episode_id, "s08_audio_events") or {}
    captions = _first(store, episode_id, "s16_captions") or {}
    ads = _first(store, episode_id, "s14_ad_scoring") or {}
    return SemanticTimeline.model_validate({
        "episode": {"id": episode_id, "title": record.title if record else episode_id, "duration": duration,
                    "fps": ingest["fps"], "resolution": f"{ingest['width']}×{ingest['height']}", "video_available": True},
        "scenes": scenes, "shots": shots, "utterances": utterances,
        "audio_events": captions.get("events") or audio.get("events", []),
        "entities": (_first(store, episode_id, "s12_vision_targeted", "s11_entities_dialogue") or {}).get("entities", []),
        "ad_candidates": ads.get("candidates", []), "ad_decision": ads.get("decision", {}),
        "subtitles": {}, "subtitle_cues": (_first(store, episode_id, "s15_subtitles") or {}).get("cues", []),
        "cc_cues": captions.get("cues", []), "qc": (_first(store, episode_id, "s17_qc") or {}).get("issues", []),
        "curves": {"intensity": (semantics or {}).get("intensity", []), "loudness": audio.get("loudness", [])},
        "processing": {"partial": True, "available_stages": available, "total_seconds": 0, "llm_cost_usd": 0, "models": [], "cached_stages": 0},
    })
