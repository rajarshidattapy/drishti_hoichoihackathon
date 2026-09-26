"""Object-storage mirror: episodes survive a server restart that wipes DATA_DIR (e.g. Render's free plan)."""
from __future__ import annotations

import json
import shutil
import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import app.artifacts as artifacts_module
from app.db import Database, EpisodeRecord
from app.main import create_app
from app.settings import Settings
from pipeline.runner import STAGE_PAIRS
from pipeline.sarvam import SarvamClient
from tests.test_pipeline_e2e import clip, fake_transcribe  # noqa: F401  (pytest fixture)


class FolderMirror:
    """Stands in for an S3/R2 bucket."""

    def __init__(self, root: Path):
        self.root = root

    def upload(self, key: str, path: Path) -> None:
        target = self.root / key
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)

    def download(self, key: str, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(self.root / key, path)

    def list(self, prefix: str) -> dict[str, int]:
        return {
            path.relative_to(self.root).as_posix(): path.stat().st_size
            for path in self.root.rglob("*") if path.is_file() and path.relative_to(self.root).as_posix().startswith(prefix)
        }

    def url(self, key: str) -> str:
        return f"https://storage.test/{key}"


def wait_for(client: TestClient, episode_id: str, timeout: float = 120) -> dict:
    deadline = time.time() + timeout
    state = client.get(f"/episodes/{episode_id}").json()
    while state["status"] not in {"processed", "failed"} and time.time() < deadline:
        time.sleep(.3)
        state = client.get(f"/episodes/{episode_id}").json()
    return state


def test_processed_episode_survives_a_restart_that_wipes_the_disk(tmp_path, clip, monkeypatch):  # noqa: F811
    bucket = FolderMirror(tmp_path / "bucket")
    monkeypatch.setattr(artifacts_module, "mirror_from_settings", lambda settings: bucket)
    monkeypatch.setattr(SarvamClient, "transcribe", fake_transcribe)
    database_url = f"sqlite:///{(tmp_path / 'shared.db').as_posix()}"

    def settings(name: str) -> Settings:
        return Settings(data_dir=tmp_path / name, database_url=database_url, seed_demo=False, sarvam_api_key="test", openai_api_key=None)

    # Before the restart: process an upload.
    with TestClient(create_app(settings("before"))) as client:
        episode_id = client.post("/episodes", json={"path": str(clip), "title": "Durable"}).json()["id"]
        state = wait_for(client, episode_id)
        assert state["status"] == "processed", [s for s in state["stages"] if s["status"] == "failed"]

    prefix = f"episodes/{episode_id}/"
    stored = bucket.list(prefix)
    assert f"{prefix}outputs/semantic_timeline.json" in stored
    assert f"{prefix}source.mp4" in stored
    assert any(key.startswith(f"{prefix}frames/") for key in stored)
    assert any(key.startswith(f"{prefix}audio/") for key in stored)

    # The restart wipes the disk. It comes back with the same DATA_DIR path (so the stored source path
    # still names this environment), an empty folder, the same database and the same bucket.
    shutil.rmtree(tmp_path / "before")
    with TestClient(create_app(settings("before"))) as client:
        assert client.get("/health").json()["object_storage"] is True
        timeline = client.get(f"/episodes/{episode_id}/timeline")
        assert timeline.status_code == 200, timeline.text
        assert client.get(f"/episodes/{episode_id}/subs/sub.vtt").status_code == 200

        # Opening the episode restores only the small files; media stays in storage.
        restored = tmp_path / "before" / "episodes" / episode_id
        assert (restored / "outputs" / "semantic_timeline.json").is_file()
        assert not (restored / "source.mp4").exists()
        assert not (restored / "audio").exists() or not any((restored / "audio").iterdir())

        video = client.get(f"/episodes/{episode_id}/video", follow_redirects=False)
        assert video.status_code == 307
        assert video.headers["location"].startswith(f"https://storage.test/{prefix}")
        frame = next(key for key in stored if key.startswith(f"{prefix}frames/")).rsplit("/", 1)[1]
        redirected = client.get(f"/episodes/{episode_id}/frames/{frame}", follow_redirects=False)
        assert redirected.status_code == 307
        assert redirected.headers["location"] == f"https://storage.test/{prefix}frames/{frame}"

        # A rerun restores everything first, so upstream stages are cache hits rather than recomputed.
        assert client.post(f"/episodes/{episode_id}/rerun", json={"from_stage": "s07", "force": False}).status_code == 202
        state = wait_for(client, episode_id)
        assert state["status"] == "processed", [s for s in state["stages"] if s["status"] == "failed"]
        log = [json.loads(line) for line in (restored / "logs" / "pipeline.jsonl").read_text(encoding="utf-8").splitlines()]
        last = log[max(i for i, event in enumerate(log) if event["event"] == "pipeline_start"):]
        cached = {event["stage"] for event in last if event["event"] == "stage_cached"}
        assert {"s01_ingest", "s02_shots", "s03_keyframes", "s04_audio_prep", "s05_vad", "s06_stt"} <= cached


def test_startup_leaves_other_machines_episodes_alone(tmp_path):
    settings = Settings(data_dir=tmp_path / "data", seed_demo=False)
    database = Database(settings)
    foreign = str(Path("/some/other/machine/episodes/ep-foreign/source.mp4"))
    database.create_episode(EpisodeRecord(id="ep-foreign", title="Elsewhere", source_path=foreign, status="processing"), STAGE_PAIRS)
    database.close()

    with TestClient(create_app(settings)) as client:
        time.sleep(1)
        state = client.get("/episodes/ep-foreign").json()
        assert state["status"] == "processing"
        assert all(stage["status"] != "failed" for stage in state["stages"])
        # Marked processed elsewhere but without files here: a clear 404 rather than "still processing".
    database = Database(settings)
    database.update_episode("ep-foreign", status="processed")
    database.close()
    with TestClient(create_app(settings)) as client:
        response = client.get("/episodes/ep-foreign/timeline")
        assert response.status_code == 404
        assert "aren't on this server" in response.json()["detail"]["message"]


@pytest.mark.parametrize("relative, media", [
    ("source.mp4", True), ("proxy.mp4", True), ("audio/full_16k.wav", True), ("frames/shot_001.jpg", True),
    ("stages/s01_ingest.json", False), ("outputs/semantic_timeline.json", False), ("cache/llm/abc.json", False),
])
def test_media_classification(relative, media):
    from pathlib import PurePosixPath
    assert artifacts_module.ArtifactStore._is_media(PurePosixPath(relative)) is media
