from __future__ import annotations

import asyncio
import csv
import io
import shutil
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated
from uuid import uuid4

from fastapi import FastAPI, File, Form, HTTPException, Query, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response, StreamingResponse

from pipeline.errors import PipelineError
from pipeline.runner import PipelineCoordinator, PipelineRunner, STAGES, STAGE_PAIRS, resolve_stage_id
from pipeline.scoring import select_candidates
from pipeline.subtitles import write_srt, write_vtt

from .artifacts import ArtifactStore
from .db import Database, EpisodeRecord
from .demo_data import DEMO_EPISODE, DEMO_ID, DEMO_TIMELINE
from .models import AdSelectionPatch, EpisodeSummary, RerunRequest, SemanticTimeline
from .settings import Settings


def _seed_demo(settings: Settings, database: Database, store: ArtifactStore) -> None:
    if not settings.seed_demo or database.get_episode_record(DEMO_ID):
        return
    root = store.ensure_episode(DEMO_ID)
    database.create_episode(EpisodeRecord(
        id=DEMO_ID,
        title=DEMO_EPISODE.title,
        source_path="",
        duration=DEMO_EPISODE.duration,
        status="processed",
        progress=100,
        video_available=False,
    ), STAGE_PAIRS)
    for stage in STAGES:
        database.update_stage(DEMO_ID, stage.id, status="done", elapsed=.01, input_hash="seed", started_at=datetime.now(UTC), finished_at=datetime.now(UTC))
    store.write_json(root / "outputs" / "semantic_timeline.json", DEMO_TIMELINE)
    store.write_text(root / "outputs" / "episode_bn.srt", write_srt([cue.model_dump() for cue in DEMO_TIMELINE.subtitle_cues]))
    store.write_text(root / "outputs" / "episode_bn.vtt", write_vtt([cue.model_dump() for cue in DEMO_TIMELINE.subtitle_cues]))
    store.write_text(root / "outputs" / "episode_bn_cc.srt", write_srt([cue.model_dump() for cue in DEMO_TIMELINE.cc_cues]))
    store.write_text(root / "outputs" / "episode_bn_cc.vtt", write_vtt([cue.model_dump() for cue in DEMO_TIMELINE.cc_cues]))
    store.write_json(root / "outputs" / "qc_report.json", {"issues": [issue.model_dump() for issue in DEMO_TIMELINE.qc]})


def create_app(custom_settings: Settings | None = None) -> FastAPI:
    settings = custom_settings or Settings()
    settings.episodes_dir.mkdir(parents=True, exist_ok=True)
    database = Database(settings)
    store = ArtifactStore(settings)
    runner = PipelineRunner(settings, database, store)
    coordinator = PipelineCoordinator(runner, settings.worker_concurrency)
    _seed_demo(settings, database, store)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        # Resume interrupted or partially processed episodes (e.g. GPU stages synced from another
        # machine); valid artifacts are detected by the runner's hash sidecars and skipped.
        for record in database.list_episode_records():
            if record.status in {"queued", "processing"} and record.source_path:
                coordinator.enqueue(record.id)
        yield
        coordinator.shutdown()
        database.close()

    api = FastAPI(
        title="Hoichoi Drishti API",
        version="1.0.0",
        description="Artifact-backed semantic timeline, ad intelligence, localization, and QC API.",
        lifespan=lifespan,
    )
    api.state.settings = settings
    api.state.database = database
    api.state.store = store
    api.state.coordinator = coordinator
    api.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    def episode_or_404(episode_id: str) -> EpisodeRecord:
        record = database.get_episode_record(episode_id)
        if record is None:
            raise HTTPException(404, "Episode not found.")
        return record

    def timeline_or_409(episode_id: str) -> SemanticTimeline:
        record = episode_or_404(episode_id)
        path = store.output_path(episode_id, "semantic_timeline.json")
        if not path.exists():
            failed = next((stage for stage in database.get_stages(episode_id) if stage.status == "failed"), None)
            if failed:
                raise HTTPException(409, {"message": "Timeline is unavailable because processing failed.", "stage": failed.stage_id, "error": failed.error})
            raise HTTPException(409, {"message": "Timeline is still processing.", "status": record.status, "progress": record.progress})
        try:
            return SemanticTimeline.model_validate(store.read_json(path))
        except Exception as exc:
            raise HTTPException(500, "The timeline artifact failed schema validation.") from exc

    @api.get("/health")
    def health() -> dict:
        return {"status": "ok", "worker": "local", "schema_version": "1.0"}

    @api.get("/episodes", response_model=list[EpisodeSummary])
    def list_episodes() -> list[EpisodeSummary]:
        return [database.summary(record) for record in database.list_episode_records()]

    @api.post("/episodes", response_model=EpisodeSummary, status_code=201)
    async def create_episode(
        request: Request,
        file: Annotated[UploadFile | None, File()] = None,
        path: Annotated[str | None, Form()] = None,
        title: Annotated[str | None, Form()] = None,
    ) -> EpisodeSummary:
        if request.headers.get("content-type", "").startswith("application/json"):
            payload = await request.json()
            path = payload.get("path")
            title = payload.get("title")
        if file is None and not path:
            raise HTTPException(422, "Upload a video or provide a local path.")

        episode_id = f"ep-{uuid4().hex[:12]}"
        root = store.ensure_episode(episode_id)
        allowed = {".mp4", ".mkv", ".mov", ".webm"}
        try:
            if file is not None:
                suffix = Path(file.filename or "video.mp4").suffix.lower()
                if suffix not in allowed:
                    raise HTTPException(415, "Supported video formats: MP4, MKV, MOV, and WebM.")
                source = root / f"source{suffix}"
                received = 0
                with source.open("wb") as output:
                    while chunk := await file.read(1024 * 1024):
                        received += len(chunk)
                        if received > settings.max_upload_bytes:
                            raise HTTPException(413, "The upload exceeds the configured size limit.")
                        output.write(chunk)
                display_title = title or Path(file.filename or "Untitled").stem
            else:
                incoming = Path(path or "").expanduser().resolve()
                if not incoming.is_file():
                    raise HTTPException(422, "The registered local video path does not exist.")
                if incoming.suffix.lower() not in allowed:
                    raise HTTPException(415, "Supported video formats: MP4, MKV, MOV, and WebM.")
                if incoming.stat().st_size > settings.max_upload_bytes:
                    raise HTTPException(413, "The source exceeds the configured size limit.")
                source = root / f"source{incoming.suffix.lower()}"
                shutil.copy2(incoming, source)
                display_title = title or incoming.stem
        except Exception:
            shutil.rmtree(root, ignore_errors=True)
            raise

        record = EpisodeRecord(id=episode_id, title=display_title, source_path=str(source), status="queued", progress=0)
        database.create_episode(record, STAGE_PAIRS)
        coordinator.enqueue(episode_id)
        return database.summary(database.get_episode_record(episode_id) or record)

    @api.get("/episodes/{episode_id}", response_model=EpisodeSummary)
    def get_episode(episode_id: str) -> EpisodeSummary:
        return database.summary(episode_or_404(episode_id))

    @api.get("/episodes/{episode_id}/events")
    async def episode_events(episode_id: str) -> StreamingResponse:
        episode_or_404(episode_id)

        async def stream():
            previous = ""
            while True:
                summary = database.summary(episode_or_404(episode_id))
                payload = summary.model_dump_json()
                if payload != previous:
                    yield f"event: progress\ndata: {payload}\n\n"
                    previous = payload
                else:
                    yield ": keep-alive\n\n"
                if summary.status in {"processed", "failed"}:
                    break
                await asyncio.sleep(.75)

        return StreamingResponse(stream(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

    @api.post("/episodes/{episode_id}/rerun", response_model=EpisodeSummary, status_code=202)
    def rerun_episode(episode_id: str, payload: RerunRequest) -> EpisodeSummary:
        episode_or_404(episode_id)
        if coordinator.running(episode_id):
            raise HTTPException(409, "This episode is already processing.")
        try:
            stage_id = resolve_stage_id(payload.from_stage)
            database.reset_from(episode_id, stage_id)
        except (KeyError, PipelineError) as exc:
            raise HTTPException(422, f"Unknown stage: {payload.from_stage}") from exc
        coordinator.enqueue(episode_id, from_stage=stage_id, force=payload.force)
        return database.summary(episode_or_404(episode_id))

    @api.get("/episodes/{episode_id}/timeline", response_model=SemanticTimeline)
    def get_timeline(episode_id: str) -> SemanticTimeline:
        return timeline_or_409(episode_id)

    @api.get("/episodes/{episode_id}/scenes/{scene_id}")
    def get_scene(episode_id: str, scene_id: str) -> dict:
        timeline = timeline_or_409(episode_id)
        scene = next((item for item in timeline.scenes if item.scene_id == scene_id), None)
        if scene is None:
            raise HTTPException(404, "Scene not found.")
        return {
            **scene.model_dump(),
            "utterances": [item.model_dump() for item in timeline.utterances if item.utt_id in scene.utt_ids],
            "entities": [item.model_dump() for item in timeline.entities if item.entity_id in scene.entity_ids],
        }

    @api.get("/episodes/{episode_id}/ads")
    def get_ads(
        episode_id: str,
        min_gap: int = Query(480, ge=0),
        n_breaks: int = Query(2, ge=1, le=20),
        blocked: str = Query("120,120"),
    ) -> list[dict]:
        timeline = timeline_or_409(episode_id)
        try:
            blocked_head, blocked_tail = [float(value) for value in blocked.split(",", 1)]
        except (ValueError, TypeError) as exc:
            raise HTTPException(422, "blocked must be 'start_seconds,end_seconds'.") from exc
        candidates = [
            candidate.model_dump() for candidate in timeline.ad_candidates
            if blocked_head <= candidate.time <= float(timeline.episode["duration"]) - blocked_tail
        ]
        return select_candidates(candidates, min_gap, n_breaks)

    @api.patch("/episodes/{episode_id}/ads/{candidate_id}")
    def patch_ad(episode_id: str, candidate_id: str, payload: AdSelectionPatch) -> dict:
        timeline = timeline_or_409(episode_id)
        candidate = next((item for item in timeline.ad_candidates if item.cand_id == candidate_id), None)
        if candidate is None:
            raise HTTPException(404, "Ad candidate not found.")
        candidate.selected = payload.selected
        store.write_json(store.output_path(episode_id, "semantic_timeline.json"), timeline)
        store.write_json(store.output_path(episode_id, "ad_cuepoints.json"), [item.model_dump() for item in timeline.ad_candidates])
        return candidate.model_dump()

    @api.get("/episodes/{episode_id}/frames/{name}")
    def get_frame(episode_id: str, name: str) -> FileResponse:
        episode_or_404(episode_id)
        try:
            path = store.safe_child(store.episode_dir(episode_id) / "frames", name)
        except ValueError as exc:
            raise HTTPException(400, "Invalid frame path.") from exc
        if not path.is_file():
            raise HTTPException(404, "Frame not found.")
        return FileResponse(path, media_type="image/jpeg", headers={"Cache-Control": "public, max-age=31536000, immutable"})

    @api.get("/episodes/{episode_id}/video")
    def get_video(episode_id: str) -> FileResponse:
        record = episode_or_404(episode_id)
        ingest_path = store.stage_path(episode_id, "s01_ingest")
        path: Path | None = None
        if ingest_path.exists():
            ingest = store.read_json(ingest_path)
            candidate = store.safe_child(store.episode_dir(episode_id), ingest.get("proxy", ingest["source"]))
            if candidate.is_file():
                path = candidate
        if path is None and record.source_path and Path(record.source_path).is_file():
            path = Path(record.source_path)
        if path is None:
            raise HTTPException(404, "No playable video is attached to this episode.")
        media_type = "video/webm" if path.suffix.lower() == ".webm" else "video/mp4"
        return FileResponse(path, media_type=media_type, filename=None)

    @api.get("/episodes/{episode_id}/subs/{kind}.{fmt}")
    def get_subtitles(episode_id: str, kind: str, fmt: str) -> FileResponse:
        episode_or_404(episode_id)
        if kind not in {"sub", "cc"} or fmt not in {"srt", "vtt"}:
            raise HTTPException(404, "Subtitle format not found.")
        suffix = "" if kind == "sub" else "_cc"
        path = store.output_path(episode_id, f"episode_bn{suffix}.{fmt}")
        if not path.is_file():
            raise HTTPException(409, "Subtitle output is not ready.")
        media_type = "text/vtt" if fmt == "vtt" else "application/x-subrip"
        return FileResponse(path, media_type=media_type, filename=path.name)

    @api.get("/episodes/{episode_id}/export/{name}")
    def export_file(episode_id: str, name: str) -> Response:
        timeline = timeline_or_409(episode_id)
        if name == "semantic_timeline.json":
            return FileResponse(store.output_path(episode_id, name), media_type="application/json", filename=name)
        if name == "qc_report.json":
            path = store.output_path(episode_id, name)
            if not path.exists():
                store.write_json(path, {"issues": [item.model_dump() for item in timeline.qc]})
            return FileResponse(path, media_type="application/json", filename=name)
        if name == "ad_cuepoints.csv":
            stream = io.StringIO()
            writer = csv.writer(stream)
            writer.writerow(["candidate_id", "time_seconds", "score", "selected", "categories", "reason"])
            for candidate in timeline.ad_candidates:
                writer.writerow([candidate.cand_id, candidate.time, candidate.score.total, candidate.selected, "|".join(candidate.matched_categories), candidate.reason])
            return Response(stream.getvalue(), media_type="text/csv", headers={"Content-Disposition": f'attachment; filename="{name}"'})
        raise HTTPException(404, "Export not found.")

    @api.get("/search")
    def search(episode_id: str, q: str = Query(min_length=2)) -> list[dict]:
        timeline = timeline_or_409(episode_id)
        needle = q.casefold()
        results = []
        for scene in timeline.scenes:
            if needle in f"{scene.semantic.title} {scene.semantic.summary} {' '.join(scene.semantic.topics)}".casefold():
                results.append({"type": "scene", "id": scene.scene_id, "time": scene.start, "text": scene.semantic.title})
        for utterance in timeline.utterances:
            if needle in utterance.text.casefold():
                results.append({"type": "utterance", "id": utterance.utt_id, "time": utterance.start, "text": utterance.text})
        return results[:20]

    @api.get("/schema")
    def schema() -> dict:
        return SemanticTimeline.model_json_schema()

    return api


app = create_app()

