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

from pipeline.ads import decide, load_catalogue, select_brand_for
from pipeline.errors import PipelineError
from pipeline.fetch import validate_url
from pipeline.partial import assemble_partial
from pipeline.runner import DOWNLOAD_STAGE, PipelineCoordinator, PipelineRunner, STAGES, STAGE_PAIRS, resolve_stage_id
from pipeline.subtitles import write_srt, write_vtt
from pipeline.vmap import build_vmap, ensure_creative

from .artifacts import ArtifactStore
from .db import Database, EpisodeRecord
from .demo_data import DEMO_EPISODE, DEMO_ID, build_demo_timeline
from .models import AdSelectionPatch, EpisodeSummary, RerunRequest, SemanticTimeline
from .settings import Settings


def _seed_demo(settings: Settings, database: Database, store: ArtifactStore) -> None:
    if not settings.seed_demo:
        return
    root = store.ensure_episode(DEMO_ID)
    if database.get_episode_record(DEMO_ID) is None:
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
    # Rebuilt on every start so the demo always reflects the current decision engine and catalogue.
    DEMO_TIMELINE = build_demo_timeline(settings.brand_catalogue, settings.thresholds)
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
            elif record.status == "downloading" and store.source_url_path(record.id).exists():
                coordinator.enqueue_url(record.id, store.source_url_path(record.id).read_text(encoding="utf-8").strip())
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

    def save_timeline(episode_id: str, timeline: SemanticTimeline) -> None:
        store.write_json(store.output_path(episode_id, "semantic_timeline.json"), timeline)

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
        url = None
        if request.headers.get("content-type", "").startswith("application/json"):
            payload = await request.json()
            path, title, url = payload.get("path"), payload.get("title"), payload.get("url")
        if url:
            # Linked video: download first, then the same pipeline as an upload.
            try:
                url = validate_url(url)
            except ValueError as exc:
                raise HTTPException(422, str(exc)) from exc
            episode_id = f"ep-{uuid4().hex[:12]}"
            store.ensure_episode(episode_id)
            store.source_url_path(episode_id).write_text(url, encoding="utf-8")
            database.create_episode(EpisodeRecord(id=episode_id, title=title or url, source_path="", status="downloading", progress=0), [DOWNLOAD_STAGE, *STAGE_PAIRS])
            coordinator.enqueue_url(episode_id, url)
            return database.summary(episode_or_404(episode_id))
        if file is None and not path:
            raise HTTPException(422, "Upload a video, paste a link, or provide a local path.")

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
    def get_timeline(episode_id: str, partial: bool = False) -> SemanticTimeline:
        """With partial=true, returns whatever is ready so far while the episode is still processing."""
        if partial and not store.output_path(episode_id, "semantic_timeline.json").exists():
            record = episode_or_404(episode_id)
            timeline = assemble_partial(store, database, episode_id)
            if timeline is None:
                raise HTTPException(409, {"message": "Nothing is ready yet.", "status": record.status})
            return timeline
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
        min_gap: float | None = Query(None, ge=0),
        n_breaks: int | None = Query(None, ge=1, le=20),
        blocked: str | None = Query(None),
    ) -> list[dict]:
        """Re-run the decision pipeline over cached candidates with new settings and persist the result."""
        timeline = timeline_or_409(episode_id)
        t = settings.thresholds
        duration = float(timeline.episode["duration"])
        try:
            head, tail = [float(v) for v in blocked.split(",", 1)] if blocked else (t.ad_blocked_head_seconds, t.ad_blocked_tail_seconds)
        except (ValueError, TypeError) as exc:
            raise HTTPException(422, "blocked must be 'start_seconds,end_seconds'.") from exc
        decided, summary = decide(
            [c.model_dump() for c in timeline.ad_candidates], load_catalogue(settings.brand_catalogue), duration=duration,
            min_gap=t.ad_default_min_gap if min_gap is None else min_gap,
            n_breaks=n_breaks or max(1, int(duration // 600)), blocked=(head, tail), min_safety=t.ad_min_safety,
        )
        save_timeline(episode_id, SemanticTimeline.model_validate({**timeline.model_dump(), "ad_candidates": decided, "ad_decision": summary}))
        return decided

    @api.patch("/episodes/{episode_id}/ads/{candidate_id}")
    def patch_ad(episode_id: str, candidate_id: str, payload: AdSelectionPatch) -> dict:
        """Manual override. Hard constraints and brand safety still apply."""
        timeline = timeline_or_409(episode_id)
        data = timeline.model_dump()
        candidate = next((c for c in data["ad_candidates"] if c["cand_id"] == candidate_id), None)
        if candidate is None:
            raise HTTPException(404, "Ad candidate not found.")
        if payload.selected:
            if not candidate["eligible"]:
                raise HTTPException(409, f"This position violates: {', '.join(candidate['rejections'])}.")
            candidate.update(select_brand_for(candidate, load_catalogue(settings.brand_catalogue)))
            if candidate["brand"] is None:
                raise HTTPException(409, "No advertiser in the catalogue is brand-safe for this position.")
        candidate["selected"] = payload.selected
        candidate["decision_note"] = "manual_select" if payload.selected else "manual_unselect"
        chosen = [c for c in data["ad_candidates"] if c["selected"] and c["brand"]]
        data["ad_decision"] = {**data["ad_decision"], "outcome": "breaks" if chosen else "no_break",
                               "selected": [{"cand_id": c["cand_id"], "time": c["time"], "brand_id": c["brand"]["brand_id"], "creative_id": (c.get("creative") or {}).get("id")} for c in chosen]}
        save_timeline(episode_id, SemanticTimeline.model_validate(data))
        return candidate

    @api.get("/episodes/{episode_id}/ads/vmap.xml")
    def get_vmap(episode_id: str, request: Request) -> Response:
        timeline = timeline_or_409(episode_id)
        creative = str(request.base_url).rstrip("/") + "/ads/creatives/{brand_id}/{creative_id}.mp4"
        xml = build_vmap([c.model_dump() for c in timeline.ad_candidates], load_catalogue(settings.brand_catalogue), creative)
        return Response(xml, media_type="application/xml", headers={"Cache-Control": "no-store"})

    @api.get("/episodes/{episode_id}/ads/debug")
    def get_ad_debug(episode_id: str) -> dict:
        """Everything behind the ad decision: settings, per-candidate constraints, scores, brand rankings and exclusions."""
        timeline = timeline_or_409(episode_id)
        return {"decision": timeline.ad_decision, "catalogue": load_catalogue(settings.brand_catalogue),
                "candidates": [c.model_dump() for c in timeline.ad_candidates]}

    @api.get("/ads/creatives/{brand_id}/{creative_id}.mp4")
    def get_creative(brand_id: str, creative_id: str) -> FileResponse:
        brand = next((b for b in load_catalogue(settings.brand_catalogue) if b["brand_id"] == brand_id), None)
        creative = next((c for c in (brand or {}).get("creatives", []) if c["id"] == creative_id), None)
        if brand is None or creative is None:
            raise HTTPException(404, "Unknown brand or creative.")
        try:
            path = ensure_creative(brand, creative, settings.brand_catalogue.parent, settings.data_dir / "creatives", settings.ffmpeg_binary)
        except PipelineError as exc:
            raise HTTPException(500, str(exc)) from exc
        return FileResponse(path, media_type="video/mp4")

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
            writer.writerow(["candidate_id", "time_seconds", "safety_score", "eligible", "selected", "brand", "rejections", "reason"])
            for c in timeline.ad_candidates:
                writer.writerow([c.cand_id, c.time, c.score.total, c.eligible, c.selected, (c.brand or {}).get("brand_id", ""), "|".join(c.rejections), c.reason])
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

