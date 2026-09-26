from __future__ import annotations

import math
from datetime import UTC, datetime

from .models import EpisodeSummary, SemanticTimeline, StageStatus


DEMO_ID = "demo-episode-102"


def _stage(stage_id: str, label: str, elapsed: float) -> StageStatus:
    return StageStatus(id=stage_id, label=label, status="done", elapsed=elapsed)


DEMO_EPISODE = EpisodeSummary(
    id=DEMO_ID,
    title="মহানগর — পর্ব ১০২",
    duration=864.0,
    status="processed",
    progress=100,
    created_at=datetime.now(UTC).isoformat(),
    video_available=False,
    stages=[
        _stage("s01", "Ingest", 4.2),
        _stage("s06", "Transcript", 38.7),
        _stage("s10", "Scenes", 19.4),
        _stage("s12", "Entity checks", 26.1),
        _stage("s14", "Ad scoring", 0.8),
        _stage("s18", "Assemble", 1.1),
    ],
)


def _scene(
    idx: int,
    start: float,
    end: float,
    title: str,
    summary: str,
    location: str,
    mood: str,
    intensity: float,
    speakers: list[str],
    utterances: list[str],
    entities: list[str],
    activity: str,
    cliffhanger: bool = False,
) -> dict:
    return {
        "scene_id": f"scene_{idx:03d}",
        "start": start,
        "end": end,
        "shot_ids": [f"shot_{idx * 3 + n:04d}" for n in range(3)],
        "visual": {
            "location": location,
            "indoor": location not in {"street", "railway platform"},
            "objects": ["table", "tea cup", "window"] if idx == 2 else ["people", "furniture"],
            "visible_brands": ["Amul"] if idx == 4 else [],
            "activity": activity,
            "visual_mood": mood,
            "people_count": len(speakers),
            "confidence": 0.91,
        },
        "speakers": speakers,
        "utt_ids": utterances,
        "audio_events": [f"event_{idx:02d}"] if idx in {1, 3, 5} else [],
        "music_ratio": 0.12 if intensity < 0.5 else 0.48,
        "semantic": {
            "title": title,
            "summary": summary,
            "topics": ["family", "decision"] if idx < 4 else ["travel", "work"],
            "mood": mood,
            "narrative_intensity": intensity,
            "intensity_components": {
                "llm": min(1, intensity + 0.06),
                "audio_energy": max(0, intensity - 0.08),
                "dialogue_density": min(1, intensity + 0.12),
            },
            "is_cliffhanger": cliffhanger,
        },
        "entity_ids": entities,
    }


def build_demo_timeline() -> SemanticTimeline:
    utterances = [
        {"utt_id": "utt_001", "start": 22, "end": 31, "speaker": "SPK_A", "speaker_name": "মিতা", "text_raw": "আজ এত দেরি কেন", "text": "আজ এত দেরি কেন?", "confidence": 0.96},
        {"utt_id": "utt_002", "start": 34, "end": 44, "speaker": "SPK_B", "speaker_name": "অনির্বাণ", "text_raw": "অফিসে মিটিং ছিল", "text": "অফিসে মিটিং ছিল।", "confidence": 0.93},
        {"utt_id": "utt_003", "start": 154, "end": 166, "speaker": "SPK_A", "speaker_name": "মিতা", "text_raw": "ফোনটা বদলাতে হবে", "text": "ফোনটা বদলাতে হবে, চার্জ একদম থাকছে না।", "confidence": 0.91},
        {"utt_id": "utt_004", "start": 169, "end": 181, "speaker": "SPK_B", "speaker_name": "অনির্বাণ", "text_raw": "নতুনটা কিনে নাও", "text": "নতুনটা কিনে নাও। ক্যামেরাটাও ভালো হবে।", "confidence": 0.95},
        {"utt_id": "utt_005", "start": 305, "end": 319, "speaker": "SPK_C", "speaker_name": "ঋদ্ধি", "text_raw": "তুমি আমাকে আগে বলোনি", "text": "তুমি আমাকে আগে বলোনি কেন?", "confidence": 0.88, "overlap": True},
        {"utt_id": "utt_006", "start": 321, "end": 337, "speaker": "SPK_A", "speaker_name": "মিতা", "text_raw": "বললে কি বদলে যেত", "text": "বললে কি কিছু বদলে যেত?", "confidence": 0.86, "overlap": True},
        {"utt_id": "utt_007", "start": 470, "end": 481, "speaker": "SPK_B", "speaker_name": "অনির্বাণ", "text_raw": "খাবার অর্ডার করি", "text": "চলো, আজ বিরিয়ানি অর্ডার করি।", "confidence": 0.97},
        {"utt_id": "utt_008", "start": 623, "end": 638, "speaker": "SPK_A", "speaker_name": "মিতা", "text_raw": "ট্রেন সকাল আটটায়", "text": "ট্রেন সকাল আটটায়, দেরি কোরো না।", "confidence": 0.94},
        {"utt_id": "utt_009", "start": 747, "end": 760, "speaker": "SPK_C", "speaker_name": "ঋদ্ধি", "text_raw": "আমি কলকাতা ছেড়ে যাচ্ছি", "text": "আমি কলকাতা ছেড়ে যাচ্ছি।", "confidence": 0.89},
    ]
    scenes = [
        _scene(1, 0, 118, "ফিরে আসা", "দেরিতে বাড়ি ফেরা নিয়ে মিতা ও অনির্বাণের শান্ত কথোপকথন।", "living room", "restrained", 0.28, ["SPK_A", "SPK_B"], ["utt_001", "utt_002"], [], "conversation"),
        _scene(2, 118, 252, "ফোনের কথা", "নষ্ট ফোন বদলানো নিয়ে ইতিবাচক আলোচনা; ফোনটি ফ্রেমে দেখা যায় না।", "dining room", "warm", 0.31, ["SPK_A", "SPK_B"], ["utt_003", "utt_004"], ["entity_phone"], "tea and conversation"),
        _scene(3, 252, 405, "চাপা দ্বন্দ্ব", "লুকোনো সিদ্ধান্ত নিয়ে তর্ক দ্রুত তীব্র হয়ে ওঠে।", "bedroom", "tense", 0.86, ["SPK_A", "SPK_C"], ["utt_005", "utt_006"], [], "argument", True),
        _scene(4, 405, 556, "রাতের খাবার", "উত্তেজনা কমে আসে; খাবার অর্ডারের প্রসঙ্গ ওঠে।", "kitchen", "relieved", 0.22, ["SPK_B"], ["utt_007"], ["entity_biryani", "entity_amul"], "preparing dinner"),
        _scene(5, 556, 696, "যাত্রার প্রস্তুতি", "সকালের ট্রেন ও ব্যাগ গোছানো নিয়ে পরিকল্পনা।", "bedroom", "focused", 0.42, ["SPK_A", "SPK_B"], ["utt_008"], ["entity_train"], "packing"),
        _scene(6, 696, 864, "বিদায়ের সিদ্ধান্ত", "ঋদ্ধি জানায় সে কলকাতা ছেড়ে যাচ্ছে; ঘরে নীরবতা নামে।", "railway platform", "melancholic", 0.78, ["SPK_C"], ["utt_009"], ["entity_kolkata"], "departure", True),
    ]
    entities = [
        {
            "entity_id": "entity_phone", "name": "smartphone", "name_bn": "ফোন", "kind": "product", "brand": None,
            "ad_categories": ["mobile"], "mentions": [{"source": "dialogue", "time": 154, "utt_id": "utt_003", "surface": "ফোনটা"}],
            "sentiment": "positive", "presence": "mentioned_only", "confidence": 0.94,
            "visual_check": {"frames_checked": ["kf_0007.jpg", "kf_0008.jpg", "kf_0009.jpg", "kf_0010.jpg"], "visible": False, "visible_frames": [], "confidence": 0.91, "note": "Checked 8 frames across the enclosing scene; no phone was visible."},
        },
        {
            "entity_id": "entity_biryani", "name": "biryani", "name_bn": "বিরিয়ানি", "kind": "food", "brand": None,
            "ad_categories": ["food_delivery"], "mentions": [{"source": "dialogue", "time": 470, "utt_id": "utt_007", "surface": "বিরিয়ানি"}],
            "sentiment": "positive", "presence": "mentioned_and_shown", "confidence": 0.89,
            "visual_check": {"frames_checked": ["kf_0015.jpg", "kf_0016.jpg"], "visible": True, "visible_frames": ["kf_0016.jpg"], "confidence": 0.87, "note": "Food container visible at 08:04."},
        },
        {
            "entity_id": "entity_amul", "name": "Amul", "name_bn": "আমুল", "kind": "brand", "brand": "Amul",
            "ad_categories": ["food_delivery"], "mentions": [{"source": "visual", "time": 505, "shot_id": "shot_0014", "surface": "Amul"}],
            "sentiment": "neutral", "presence": "shown_only", "confidence": 0.82,
        },
        {
            "entity_id": "entity_train", "name": "train", "name_bn": "ট্রেন", "kind": "product", "brand": None,
            "ad_categories": ["travel"], "mentions": [{"source": "dialogue", "time": 623, "utt_id": "utt_008", "surface": "ট্রেন"}],
            "sentiment": "neutral", "presence": "unverified", "confidence": 0.73,
        },
        {
            "entity_id": "entity_kolkata", "name": "Kolkata", "name_bn": "কলকাতা", "kind": "place", "brand": None,
            "ad_categories": ["travel"], "mentions": [{"source": "dialogue", "time": 747, "utt_id": "utt_009", "surface": "কলকাতা"}],
            "sentiment": "negative", "presence": "mentioned_only", "confidence": 0.97,
        },
    ]
    ads = [
        {
            "cand_id": "ad_001", "time": 253, "scene_id": "scene_002", "kind": "scene_boundary", "pause_len": 1.8,
            "score": {"pause": 0.72, "scene_end": 1, "low_intensity": 0.78, "context_match": 0.85, "speech_penalty": 0, "cliffhanger_penalty": 0, "total": 0.84},
            "disruption": "low", "matched_categories": ["mobile"], "context_entity_ids": ["entity_phone"],
            "reason": "After ‘ফোনের কথা’; 1.8 s pause, low intensity, and a positive smartphone discussion nearby.", "selected": True,
        },
        {
            "cand_id": "ad_002", "time": 557, "scene_id": "scene_004", "kind": "scene_boundary", "pause_len": 2.1,
            "score": {"pause": 0.84, "scene_end": 1, "low_intensity": 0.81, "context_match": 0.79, "speech_penalty": 0, "cliffhanger_penalty": 0, "total": 0.86},
            "disruption": "low", "matched_categories": ["food_delivery"], "context_entity_ids": ["entity_biryani"],
            "reason": "After ‘রাতের খাবার’; a clean pause follows a low-intensity food moment.", "selected": False,
        },
        {
            "cand_id": "ad_003", "time": 405, "scene_id": "scene_003", "kind": "scene_boundary", "pause_len": 0.5,
            "score": {"pause": 0.2, "scene_end": 1, "low_intensity": 0.18, "context_match": 0, "speech_penalty": 0, "cliffhanger_penalty": 0.6, "total": 0.19},
            "disruption": "high", "matched_categories": [], "context_entity_ids": [],
            "reason": "Scene boundary, but it follows a cliffhanger and carries high narrative intensity.", "selected": False,
        },
    ]
    events = [
        {"event_id": "event_01", "label": "Door", "label_bn": "দরজা খোলার শব্দ", "start": 18, "end": 20, "score": 0.88, "in_cc": True},
        {"event_id": "event_03", "label": "Thunder", "label_bn": "বজ্রপাত", "start": 350, "end": 352, "score": 0.76, "in_cc": True},
        {"event_id": "event_05", "label": "Train", "label_bn": "ট্রেনের শব্দ", "start": 690, "end": 695, "score": 0.84, "in_cc": True},
    ]
    subtitle_cues = [
        {"idx": i + 1, "start": u["start"], "end": u["end"], "lines": [u["text"]], "speakers": [u["speaker"]], "kind": "dialogue", "cps": round(len(u["text"]) / (u["end"] - u["start"]), 1)}
        for i, u in enumerate(utterances)
    ]
    cc_cues = subtitle_cues + [
        {"idx": len(subtitle_cues) + i + 1, "start": e["start"], "end": e["end"], "lines": [f"[{e['label_bn']}]"], "speakers": [], "kind": "sound", "cps": 0}
        for i, e in enumerate(events)
    ]
    qc = [
        {"issue_id": "qc_001", "severity": "warn", "rule": "overlap_speech", "time": 305, "cue_idx": 5, "message": "Two speakers overlap in this cue.", "suggestion": "Confirm the speaker split and cue boundary."},
        {"issue_id": "qc_002", "severity": "info", "rule": "speaker_ambiguous", "time": 321, "cue_idx": 6, "message": "Speaker confidence is low after a rapid turn.", "suggestion": "Listen to the previous two seconds."},
        {"issue_id": "qc_003", "severity": "warn", "rule": "timing_drift", "time": 747, "cue_idx": 9, "message": "Cue starts 0.6 s after the detected speech onset.", "suggestion": "Move the cue start 0.6 s earlier."},
    ]
    intensity = [[float(t), round(max(0.08, min(0.96, next(s["semantic"]["narrative_intensity"] for s in scenes if s["start"] <= t <= s["end"]) + math.sin(t / 31) * 0.07)), 3)] for t in range(0, 865, 12)]
    return SemanticTimeline(
        episode={"id": DEMO_ID, "title": DEMO_EPISODE.title, "duration": 864, "fps": 25, "resolution": "1920×1080", "video_available": False},
        scenes=scenes,
        shots=[],
        utterances=utterances,
        audio_events=events,
        entities=entities,
        ad_candidates=ads,
        subtitles={"sub_srt": "/episodes/demo-episode-102/subs/sub.srt", "sub_vtt": "/episodes/demo-episode-102/subs/sub.vtt", "cc_srt": "/episodes/demo-episode-102/subs/cc.srt", "cc_vtt": "/episodes/demo-episode-102/subs/cc.vtt", "cue_count": len(subtitle_cues)},
        subtitle_cues=subtitle_cues,
        cc_cues=cc_cues,
        qc=qc,
        curves={"intensity": intensity, "loudness": [[float(t), round(0.25 + abs(math.sin(t / 47)) * 0.55, 3)] for t in range(0, 865, 12)]},
        processing={"total_seconds": 90.3, "llm_cost_usd": 1.84, "models": ["gpt-4.1-mini", "Sarvam Saarika", "SigLIP"], "cached_stages": 18},
    )


DEMO_TIMELINE = build_demo_timeline()

