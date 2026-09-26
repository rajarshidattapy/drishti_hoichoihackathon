from app.settings import Thresholds
from pipeline.captions import build_cc, finalize_events
from pipeline.qc import run_qc
from pipeline.runner import descendants, resolve_stage_id
from pipeline.sarvam import mark_overlaps
from pipeline.scenes import aggregate_visual, enforce_min_length, merge_scenes, score_boundaries
from pipeline.scoring import cliffhanger_blocked, context_match, disruption, score_candidate
from pipeline.stages.core import build_chunks, edit_ratio, merge_short_shots, smooth_curve
from pipeline.subtitles import format_utterances

T = Thresholds()


def tag(location, objects=(), brands=()):
    return {"location": location, "indoor": True, "objects": list(objects), "visible_brands": list(brands), "activity": "talking", "visual_mood": "calm", "people_count": 2, "confidence": .8}


def test_boundary_scoring_combines_visual_location_speaker_and_silence():
    shots = [
        {"shot_id": "a", "start": 0, "end": 30, "dhash": "0000000000000000"},
        {"shot_id": "b", "start": 30, "end": 60, "dhash": "ffffffffffffffff"},
    ]
    utterances = [{"speaker": "SPK_A", "start": 10, "end": 12}, {"speaker": "SPK_B", "start": 40, "end": 42}]
    silences = [{"start": 29.5, "end": 31, "duration": 1.5}]
    [boundary] = score_boundaries(shots, {"a": tag("kitchen"), "b": tag("street")}, utterances, silences, T)
    assert boundary["components"] == {"visual": 1.0, "location": 1.0, "speakers": 1.0, "silence": 1.0}
    assert boundary["score"] == 1.0


def test_min_scene_length_merges_weakest_boundary_first():
    boundaries = [{"time": 30, "score": .9}, {"time": 40, "score": .5}, {"time": 80, "score": .7}]
    kept = enforce_min_length(boundaries, 120, 20)
    assert [b["time"] for b in kept] == [30, 80]


def test_merge_scenes_and_aggregate_visual():
    scenes = [{"scene_id": "x", "start": 0, "end": 10, "shot_ids": ["a"]}, {"scene_id": "y", "start": 10, "end": 30, "shot_ids": ["b"]}]
    merged = merge_scenes(scenes, {0})
    assert merged == [{"scene_id": "scene_0001", "start": 0, "end": 30, "shot_ids": ["a", "b"]}]
    visual = aggregate_visual(
        [{"shot_id": "a", "start": 0, "end": 10}, {"shot_id": "b", "start": 10, "end": 40}],
        {"a": tag("kitchen", ["kettle"]), "b": tag("street", ["car"], ["Amul"])},
    )
    assert visual["location"] == "street"
    assert visual["objects"][0] == "car" and "kettle" in visual["objects"]
    assert visual["visible_brands"] == ["Amul"]


def test_context_match_uses_sentiment_and_presence_weights():
    entities = [
        {"entity_id": "e1", "name": "phone", "confidence": 1.0, "sentiment": "positive", "presence": "mentioned_only", "mentions": [{"time": 100}]},
        {"entity_id": "e2", "name": "loan", "confidence": 1.0, "sentiment": "negative", "presence": "mentioned_and_shown", "mentions": [{"time": 120}]},
        {"entity_id": "e3", "name": "car", "confidence": 1.0, "sentiment": "positive", "presence": "mentioned_and_shown", "mentions": [{"time": 10}]},
    ]
    value, hits = context_match(130, entities, 60)
    assert value == .9
    assert [hit[0]["entity_id"] for hit in hits] == ["e1", "e2"]


def test_penalties_force_high_disruption_and_cliffhanger_end_is_allowed():
    score = score_candidate(pause_len=2, scene_boundary=True, distance_to_end=0, intensity=.1, context_match=0, speech=True, cliffhanger=False)
    assert disruption(score) == "high"
    scenes = [{"scene_id": "s1", "start": 0, "end": 100}]
    curve = [[float(t), .9 if t == 50 else .3] for t in range(100)]
    assert cliffhanger_blocked(55, scenes, curve, 10, 2, {"s1"})
    assert not cliffhanger_blocked(70, scenes, curve, 10, 2, {"s1"})
    assert not cliffhanger_blocked(100, scenes, curve, 10, 2, {"s1"})
    assert not cliffhanger_blocked(55, scenes, curve, 10, 2, set())


def test_qc_rules_cover_documented_checks():
    cues = [
        {"idx": 1, "start": 0.0, "end": 0.5, "lines": ["a" * 50, "b", "c"], "speakers": ["SPK_A"], "utt_ids": ["u1"], "kind": "dialogue", "cps": 25.0},
    ]
    utterances = [
        {"utt_id": "u1", "start": 0.0, "end": 2.0, "speaker": "SPK_A", "confidence": .4, "overlap": True},
        {"utt_id": "u2", "start": 2.1, "end": 2.5, "speaker": "SPK_B", "confidence": .9},
        {"utt_id": "u3", "start": 2.6, "end": 4.0, "speaker": "SPK_A", "confidence": .9},
    ]
    speech = [{"start": 1.0, "end": 2.0}, {"start": 10.0, "end": 14.0}]
    issues, summary = run_qc(cues, utterances, speech, [], T, {"u3"})
    rules = {issue["rule"] for issue in issues}
    assert {"low_confidence", "reading_speed", "line_length", "line_count", "overlap_speech", "duration", "timing_drift", "speaker_ambiguous", "missing_speech"} <= rules
    assert summary["error"] >= 2 and summary["passed"] is False


def test_closed_captions_merge_shift_and_music():
    dialogue = [
        {"idx": 1, "start": 0.0, "end": 2.0, "lines": ["একটি লাইন"], "speakers": ["A"], "kind": "dialogue", "cps": 5},
        {"idx": 2, "start": 5.0, "end": 7.0, "lines": ["প্রথম", "দ্বিতীয়"], "speakers": ["A"], "kind": "dialogue", "cps": 5},
    ]
    events = [
        {"event_id": "ae1", "label": "Knock", "label_bn": "দরজায় কড়া নাড়ার শব্দ", "start": 0.5, "end": 1.5, "score": .9, "in_cc": True},
        {"event_id": "ae2", "label": "Thunder", "label_bn": "বজ্রপাত", "start": 5.2, "end": 6.2, "score": .9, "in_cc": True},
    ]
    scenes = [{"scene_id": "s1", "start": 0, "end": 30, "music_ratio": .8, "semantic": {"mood": "tense"}}]
    cues = build_cc(dialogue, events, scenes, T)
    assert cues[0]["lines"][0] == "[দরজায় কড়া নাড়ার শব্দ]"
    thunder = next(c for c in cues if c["lines"] == ["[বজ্রপাত]"])
    assert thunder["kind"] == "sound" and (thunder["end"] <= 5.0 or thunder["start"] >= 7.0)
    assert any(c["lines"] == ["[উত্তেজনাপূর্ণ সঙ্গীত]"] for c in cues)
    assert [c["idx"] for c in cues] == list(range(1, len(cues) + 1))
    utterances = [{"start": 0, "end": 10}]
    assert finalize_events(events, utterances, T)[0]["in_cc"] is False


def test_subtitles_pair_quick_exchanges_with_dashes():
    cues = format_utterances([
        {"utt_id": "u1", "start": 0.0, "end": 0.8, "speaker": "SPK_A", "text": "কে?"},
        {"utt_id": "u2", "start": 1.0, "end": 2.2, "speaker": "SPK_B", "text": "আমি।"},
    ], T)
    assert len(cues) == 1
    assert cues[0]["lines"] == ["- কে?", "- আমি।"]


def test_cleanup_edit_ratio_and_helpers():
    assert edit_ratio("আমি যাব", "আমি যাব।") < .25
    assert edit_ratio("আমি যাব", "তুমি আসবে না কেন") > .25
    assert merge_short_shots([0, 5, 5.2, 10], .4) == [0, 5, 10]
    assert build_chunks([{"start": 0, "end": 10}, {"start": 12, "end": 25}, {"start": 26, "end": 40}], 30) == [{"start": 0, "end": 25}, {"start": 26, "end": 40}]
    assert smooth_curve([0, 0, 1, 0, 0], 3)[2] == 1 / 3


def test_overlap_marking_and_stage_resolution():
    marked = mark_overlaps([
        {"utt_id": "a", "start": 0, "end": 3, "speaker": "SPK_A", "overlap": False},
        {"utt_id": "b", "start": 2.5, "end": 4, "speaker": "SPK_B", "overlap": False},
        {"utt_id": "c", "start": 5, "end": 6, "speaker": "SPK_A", "overlap": False},
    ])
    assert [u["overlap"] for u in marked] == [True, True, False]
    assert resolve_stage_id("s06") == "s06_stt"
    assert {"s07_transcript_clean", "s15_subtitles", "s18_assemble"} <= descendants(["s06_stt"])
    assert "s02_shots" not in descendants(["s06_stt"])


def test_llm_budget_guardrail_and_prompts(tmp_path):
    import json

    import pytest
    from pydantic import BaseModel

    from app.artifacts import ArtifactStore
    from app.settings import Settings
    from pipeline.llm import BudgetExceededError, StructuredLLM, cost_usd, load_prompt

    settings = Settings(data_dir=tmp_path, openai_api_key="test", max_llm_usd_per_episode=1.0)
    store = ArtifactStore(settings)
    llm = StructuredLLM(settings, store, "ep")
    llm.log_path.parent.mkdir(parents=True)
    llm.log_path.write_text(json.dumps({"cost_usd": 0.9999}) + "\n", encoding="utf-8")
    assert llm.spent() == pytest.approx(.9999)

    class Out(BaseModel):
        ok: bool

    with pytest.raises(BudgetExceededError):
        llm.call(model="gpt-4.1-mini", system="s", user="u" * 5000, schema=Out, stage="test")
    assert cost_usd("gpt-4.1-mini", 1_000_000, 0) == pytest.approx(.40)
    assert "ads, fmcg" in load_prompt("s11_entities_v1", categories="ads, fmcg", hints="")
