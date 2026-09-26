from __future__ import annotations

import subprocess
import time

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.settings import Settings


@pytest.fixture()
def client(tmp_path):
    application = create_app(Settings(data_dir=tmp_path, seed_demo=True, sarvam_api_key=None))
    with TestClient(application) as test_client:
        yield test_client


def test_demo_episode_and_timeline_are_available(client: TestClient):
    episodes = client.get("/episodes")
    assert episodes.status_code == 200
    demo = next(episode for episode in episodes.json() if episode["id"] == "demo-episode-102")
    assert demo["status"] == "processed"
    assert len(demo["stages"]) == 18

    timeline = client.get("/episodes/demo-episode-102/timeline")
    assert timeline.status_code == 200
    assert len(timeline.json()["scenes"]) == 6


def test_ad_selection_respects_requested_count(client: TestClient):
    response = client.get("/episodes/demo-episode-102/ads", params={"min_gap": 0, "n_breaks": 2, "blocked": "0,0"})
    assert response.status_code == 200
    assert sum(candidate["selected"] for candidate in response.json()) == 2


def test_exports_schema_and_frame_path_safety(client: TestClient):
    assert client.get("/schema").status_code == 200
    export = client.get("/episodes/demo-episode-102/export/ad_cuepoints.csv")
    assert export.status_code == 200
    assert "candidate_id" in export.text
    assert client.get("/episodes/demo-episode-102/frames/missing.jpg").status_code == 404


def test_real_upload_uses_pipeline_and_fails_actionably_without_sarvam(client: TestClient, tmp_path):
    source = tmp_path / "source.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=blue:s=320x180:r=25",
        "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=16000", "-t", "2",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(source),
    ], check=True, capture_output=True)

    created = client.post("/episodes", json={"path": str(source), "title": "Pipeline fixture"})
    assert created.status_code == 201
    episode_id = created.json()["id"]

    deadline = time.time() + 25
    state = created.json()
    while state["status"] not in {"processed", "failed"} and time.time() < deadline:
        time.sleep(.2)
        state = client.get(f"/episodes/{episode_id}").json()

    assert state["status"] == "failed"
    assert state["progress"] > 0
    failed = next(stage for stage in state["stages"] if stage["status"] == "failed")
    assert failed["id"] == "s06_stt"
    assert "SARVAM_API_KEY" in failed["error"]

    timeline = client.get(f"/episodes/{episode_id}/timeline")
    assert timeline.status_code == 409
    assert timeline.json()["detail"]["stage"] == "s06_stt"



def test_vmap_inserts_selected_ad_with_a_playable_creative(client: TestClient):
    xml = client.get("/episodes/demo-episode-102/ads/vmap.xml").text
    assert xml.count("<vmap:AdBreak") >= 1 and "<MediaFile" in xml
    creative = xml.split("<![CDATA[")[1].split("]]>")[0]
    video = client.get(creative.replace("http://testserver", ""))
    assert video.status_code == 200 and video.headers["content-type"] == "video/mp4" and len(video.content) > 1000


def test_ad_debug_and_manual_override_respect_constraints(client: TestClient):
    debug = client.get("/episodes/demo-episode-102/ads/debug").json()
    assert debug["decision"]["outcome"] in {"breaks", "no_break"} and debug["catalogue"]
    ineligible = next(c for c in debug["candidates"] if not c["eligible"])
    response = client.patch(f"/episodes/demo-episode-102/ads/{ineligible['cand_id']}", json={"selected": True})
    assert response.status_code == 409
    eligible = next(c for c in debug["candidates"] if c["eligible"] and not c["selected"])
    selected = client.patch(f"/episodes/demo-episode-102/ads/{eligible['cand_id']}", json={"selected": True}).json()
    assert selected["selected"] and selected["brand"]
    assert f'breakId="{eligible["cand_id"]}"' in client.get("/episodes/demo-episode-102/ads/vmap.xml").text


def test_no_break_when_nothing_satisfies_constraints(client: TestClient):
    candidates = client.get("/episodes/demo-episode-102/ads", params={"blocked": "432,432"}).json()
    assert not any(c["selected"] for c in candidates)
    assert client.get("/episodes/demo-episode-102/ads/debug").json()["decision"]["outcome"] == "no_break"


def test_url_ingestion_rejects_other_hosts(client: TestClient):
    assert client.post("/episodes", json={"url": "https://example.com/video.mp4"}).status_code == 422
