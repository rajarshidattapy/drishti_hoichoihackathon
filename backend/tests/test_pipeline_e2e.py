"""Full 18-stage run on a generated clip, with the Sarvam call stubbed out."""
import json
import subprocess
import time

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.models import SemanticTimeline
from app.settings import Settings, Thresholds
from pipeline.sarvam import SarvamClient


@pytest.fixture()
def clip(tmp_path):
    source = tmp_path / "clip.mp4"
    # 50 s: blue then red (a hard cut at 25 s); a tone with a 2 s gap around the cut.
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "color=c=blue:s=160x90:r=10:d=25",
        "-f", "lavfi", "-i", "color=c=red:s=160x90:r=10:d=25",
        "-f", "lavfi", "-i", "sine=frequency=300:sample_rate=16000:duration=24",
        "-f", "lavfi", "-i", "anullsrc=r=16000:cl=mono:d=2",
        "-f", "lavfi", "-i", "sine=frequency=500:sample_rate=16000:duration=24",
        "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0[v];[2:a][3:a][4:a]concat=n=3:v=0:a=1[a]",
        "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(source),
    ], check=True, capture_output=True)
    return source


def fake_transcribe(self, audio_path, output_dir):
    raw = {"diarized_transcript": {"entries": [
        {"transcript": "আজ নতুন ফোনটা কিনলাম", "start_time_seconds": 2.0, "end_time_seconds": 5.0, "speaker_id": "0"},
        {"transcript": "দারুণ তো", "start_time_seconds": 5.2, "end_time_seconds": 6.4, "speaker_id": "1"},
        {"transcript": "চলো বাইরে খেতে যাই বিরিয়ানি খাব", "start_time_seconds": 30.0, "end_time_seconds": 34.0, "speaker_id": "1"},
    ]}}
    return SarvamClient.normalize(raw), raw


def test_full_pipeline_produces_valid_timeline(tmp_path, clip, monkeypatch):
    monkeypatch.setattr(SarvamClient, "transcribe", fake_transcribe)
    thresholds = Thresholds(ad_blocked_head_seconds=0, ad_blocked_tail_seconds=0)
    app = create_app(Settings(data_dir=tmp_path / "data", seed_demo=False, sarvam_api_key="test", openai_api_key=None, thresholds=thresholds))
    with TestClient(app) as client:
        created = client.post("/episodes", json={"path": str(clip), "title": "E2E"})
        assert created.status_code == 201
        episode_id = created.json()["id"]
        deadline = time.time() + 90
        state = created.json()
        while state["status"] not in {"processed", "failed"} and time.time() < deadline:
            time.sleep(.3)
            state = client.get(f"/episodes/{episode_id}").json()
        failed = [s for s in state["stages"] if s["status"] == "failed"]
        assert state["status"] == "processed", failed

        response = client.get(f"/episodes/{episode_id}/timeline")
        assert response.status_code == 200
        timeline = SemanticTimeline.model_validate(response.json())
        assert timeline.episode["duration"] == pytest.approx(50, abs=1)
        assert len(timeline.utterances) == 3
        # The blue→red cut plus the silence and speaker change around 25 s make a scene boundary.
        assert [round(s.start) for s in timeline.scenes] == [0, 25]
        assert any(c.kind == "scene_boundary" and abs(c.time - 25) < 2 for c in timeline.ad_candidates)
        assert timeline.scenes[-1].end == pytest.approx(timeline.episode["duration"], abs=.01)
        assert {e.name for e in timeline.entities} >= {"ফোন", "বিরিয়ানি"}
        assert all(e.presence == "unverified" for e in timeline.entities)  # no vision provider -> no claims
        assert timeline.subtitle_cues and timeline.cc_cues
        assert len(timeline.curves["intensity"]) >= 50
        assert timeline.processing["llm_cost_usd"] == 0
        assert client.get(f"/episodes/{episode_id}/subs/cc.vtt").text.startswith("WEBVTT")
        assert "candidate_id" in client.get(f"/episodes/{episode_id}/export/ad_cuepoints.csv").text

        # Reruns hit the cache for every stage upstream of the restart point.
        for _ in range(20):  # the worker future finishes a moment after status flips to processed
            rerun = client.post(f"/episodes/{episode_id}/rerun", json={"from_stage": "s15", "force": False})
            if rerun.status_code != 409:
                break
            time.sleep(.1)
        assert rerun.status_code == 202
        deadline = time.time() + 30
        while time.time() < deadline:
            state = client.get(f"/episodes/{episode_id}").json()
            if state["status"] in {"processed", "failed"}:
                break
            time.sleep(.2)
        assert state["status"] == "processed"
        log = (tmp_path / "data" / "episodes" / episode_id / "logs" / "pipeline.jsonl").read_text(encoding="utf-8").splitlines()
        last_run = log[max(i for i, line in enumerate(log) if json.loads(line)["event"] == "pipeline_start"):]
        cached = {json.loads(line).get("stage") for line in last_run if json.loads(line)["event"] == "stage_cached"}
        assert {"s01_ingest", "s06_stt", "s13_scene_semantics"} <= cached
        assert "s15_subtitles" not in cached


def fake_llm_call(self, *, model, system, user, schema, stage, images=None, **_):
    """Deterministic stand-in for OpenAI structured outputs, dispatched on the requested schema."""
    import re

    from pipeline.stages import core

    if schema is core.CleanBatch:
        lines = user.split("Clean these:\n", 1)[1].splitlines()
        return schema(items=[{"utt_id": line.split(": ", 1)[0], "text": line.split(": ", 1)[1] + "।"} for line in lines])
    if schema is core.VisualBatch:
        ids = user.split(": ", 1)[1].split(", ")
        return schema(items=[{"shot_id": i, "location": "kitchen" if n % 2 == 0 else "street", "indoor": True, "objects": ["table"], "visible_brands": [],
                              "activity": "talking", "visual_mood": "calm", "people_count": 2, "confidence": .8} for n, i in enumerate(ids)])
    if schema is core.SceneMergeWindow:
        scenes = [int(n) for n in re.findall(r"^Scene (\d+):", user, re.M)]
        return schema(decisions=[{"after_scene": n, "action": "keep"} for n in scenes[:-1]], titles=[{"scene": n, "title": f"Title {n}"} for n in scenes])
    if schema is core.EntityDrafts:
        mentions = re.findall(r"^(utt_\d+) \[.*?\]: .*ফোন", user, re.M)
        return schema(entities=[{"name": "smartphone", "name_bn": "ফোন", "kind": "product", "brand": None, "ad_categories": ["mobile", "not_a_category"],
                                 "sentiment": "positive", "mentions": [{"utt_id": m, "surface": "ফোনটা"} for m in mentions] + [{"utt_id": "utt_99999", "surface": "x"}],
                                 "confidence": .9}] if mentions else [])
    if schema is core.PresenceCheck:
        assert images and all(p.exists() for p in images)
        return schema(visible=False, visible_timestamps=[], confidence=.9, note="No phone visible.")
    if schema is core.SemanticDraft:
        return schema(title="Phone talk", summary="They discuss a phone.", topics=["shopping"], mood="tense", llm_intensity=.7, is_cliffhanger=False)
    raise AssertionError(f"unexpected schema {schema}")


def test_llm_stages_are_grounded_and_validated(tmp_path, clip, monkeypatch):
    from pipeline.llm import StructuredLLM

    monkeypatch.setattr(SarvamClient, "transcribe", fake_transcribe)
    monkeypatch.setattr(StructuredLLM, "call", fake_llm_call)
    thresholds = Thresholds(ad_blocked_head_seconds=0, ad_blocked_tail_seconds=0, entity_absent_min_frames=1)
    app = create_app(Settings(data_dir=tmp_path / "data", seed_demo=False, sarvam_api_key="test", openai_api_key="test", thresholds=thresholds))
    with TestClient(app) as client:
        episode_id = client.post("/episodes", json={"path": str(clip), "title": "LLM"}).json()["id"]
        deadline = time.time() + 90
        while time.time() < deadline:
            state = client.get(f"/episodes/{episode_id}").json()
            if state["status"] in {"processed", "failed"}:
                break
            time.sleep(.3)
        assert state["status"] == "processed", [s for s in state["stages"] if s["status"] == "failed"]
        timeline = SemanticTimeline.model_validate(client.get(f"/episodes/{episode_id}/timeline").json())

    assert all(u.text.endswith("।") for u in timeline.utterances)
    assert [s.semantic.title for s in timeline.scenes] == ["Phone talk", "Phone talk"]
    assert timeline.scenes[0].visual.location == "kitchen" and timeline.scenes[1].visual.location == "street"
    [phone] = [e for e in timeline.entities if e.name == "smartphone"]
    assert phone.ad_categories == ["mobile"]                         # unknown categories are dropped
    assert all(m.utt_id != "utt_99999" for m in phone.mentions)       # ungrounded mentions are dropped
    assert phone.presence == "mentioned_only" and phone.visual_check and phone.visual_check.frames_checked
    assert timeline.scenes[0].semantic.intensity_components["llm"] == .7


def test_artifacts_synced_from_another_machine_are_reused(tmp_path, clip, monkeypatch):
    """GPU-box workflow: stages produced elsewhere count as cached because validity lives with the artifacts."""
    import shutil

    from app.artifacts import ArtifactStore
    from app.db import Database, EpisodeRecord
    from pipeline.runner import STAGE_PAIRS, PipelineRunner

    monkeypatch.setattr(SarvamClient, "transcribe", fake_transcribe)
    remote = Settings(data_dir=tmp_path / "remote", seed_demo=False, sarvam_api_key="test")
    remote_db, remote_store = Database(remote), ArtifactStore(remote)
    root = remote_store.ensure_episode("ep-sync")
    shutil.copy2(clip, root / "source.mp4")
    remote_db.create_episode(EpisodeRecord(id="ep-sync", title="Sync", source_path=str(root / "source.mp4")), STAGE_PAIRS)
    PipelineRunner(remote, remote_db, remote_store).run("ep-sync", only=["s01", "s02", "s03", "s04", "s08"])
    assert remote_db.get_episode_record("ep-sync").status == "queued"
    remote_db.close()

    # "Sync" the episode folder into a fresh data dir with its own database.
    local = Settings(data_dir=tmp_path / "local", seed_demo=False, sarvam_api_key="test")
    local_db, local_store = Database(local), ArtifactStore(local)
    shutil.copytree(root, local_store.episode_dir("ep-sync"))
    local_root = local_store.episode_dir("ep-sync")
    local_db.create_episode(EpisodeRecord(id="ep-sync", title="Sync", source_path=str(local_root / "source.mp4")), STAGE_PAIRS)
    PipelineRunner(local, local_db, local_store).run("ep-sync")
    assert local_db.get_episode_record("ep-sync").status == "processed"
    log = [json.loads(line) for line in (local_root / "logs" / "pipeline.jsonl").read_text(encoding="utf-8").splitlines()]
    last = log[max(i for i, event in enumerate(log) if event["event"] == "pipeline_start"):]
    cached = {event["stage"] for event in last if event["event"] == "stage_cached"}
    assert {"s02_shots", "s03_keyframes", "s04_audio_prep", "s08_audio_events"} <= cached
    local_db.close()
