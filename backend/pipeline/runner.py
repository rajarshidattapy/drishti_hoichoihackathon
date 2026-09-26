from __future__ import annotations

import hashlib
import json
import threading
import time
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Callable, Iterable

from app.artifacts import ArtifactStore
from app.db import Database
from app.settings import Settings
from pipeline.errors import PipelineError
from pipeline.fetch import download
from pipeline.stages.core import (
    StageContext,
    s01_ingest, s02_shots, s03_keyframes, s04_audio_prep, s05_vad, s06_stt,
    s07_transcript_clean, s08_audio_events, s09_vision_baseline, s10_scenes,
    s11_entities_dialogue, s12_vision_targeted, s13_scene_semantics,
    s14_ad_scoring, s15_subtitles, s16_captions, s17_qc, s18_assemble,
)


@dataclass(frozen=True)
class StageSpec:
    id: str
    label: str
    dependencies: tuple[str, ...]
    version: str
    run: Callable[[StageContext], dict]


# The audio branch (s04–s08) and video branch (s02, s03, s09) are independent until s10.
STAGES: tuple[StageSpec, ...] = (
    StageSpec("s01_ingest", "Ingest", (), "3", s01_ingest),
    StageSpec("s02_shots", "Shot detection", ("s01_ingest",), "3", s02_shots),
    StageSpec("s03_keyframes", "Keyframes", ("s01_ingest", "s02_shots"), "3", s03_keyframes),
    StageSpec("s04_audio_prep", "Audio preparation", ("s01_ingest",), "3", s04_audio_prep),
    StageSpec("s05_vad", "Voice activity", ("s01_ingest", "s04_audio_prep"), "3", s05_vad),
    StageSpec("s06_stt", "Transcript + diarization", ("s04_audio_prep", "s05_vad"), "3", s06_stt),
    StageSpec("s07_transcript_clean", "Transcript cleanup", ("s06_stt",), "3", s07_transcript_clean),
    StageSpec("s08_audio_events", "Audio events", ("s04_audio_prep",), "3", s08_audio_events),
    StageSpec("s09_vision_baseline", "Visual understanding", ("s03_keyframes",), "3", s09_vision_baseline),
    StageSpec("s10_scenes", "Scene segmentation", ("s01_ingest", "s03_keyframes", "s05_vad", "s07_transcript_clean", "s09_vision_baseline"), "3", s10_scenes),
    StageSpec("s11_entities_dialogue", "Dialogue entities", ("s07_transcript_clean", "s10_scenes"), "3", s11_entities_dialogue),
    StageSpec("s12_vision_targeted", "Targeted visual checks", ("s01_ingest", "s03_keyframes", "s09_vision_baseline", "s11_entities_dialogue"), "3", s12_vision_targeted),
    StageSpec("s13_scene_semantics", "Scene semantics", ("s01_ingest", "s07_transcript_clean", "s08_audio_events", "s10_scenes", "s12_vision_targeted"), "3", s13_scene_semantics),
    StageSpec("s14_ad_scoring", "Ad scoring", ("s01_ingest", "s05_vad", "s07_transcript_clean", "s12_vision_targeted", "s13_scene_semantics"), "3", s14_ad_scoring),
    StageSpec("s15_subtitles", "Bengali subtitles", ("s07_transcript_clean",), "3", s15_subtitles),
    StageSpec("s16_captions", "Closed captions", ("s07_transcript_clean", "s08_audio_events", "s13_scene_semantics", "s15_subtitles"), "3", s16_captions),
    StageSpec("s17_qc", "Subtitle QC", ("s05_vad", "s07_transcript_clean", "s08_audio_events", "s15_subtitles"), "3", s17_qc),
    StageSpec("s18_assemble", "Assemble timeline", (
        "s01_ingest", "s02_shots", "s03_keyframes", "s05_vad", "s07_transcript_clean", "s08_audio_events", "s12_vision_targeted",
        "s13_scene_semantics", "s14_ad_scoring", "s15_subtitles", "s16_captions", "s17_qc",
    ), "3", s18_assemble),
)

STAGE_PAIRS = [(stage.id, stage.label) for stage in STAGES]
# URL episodes get one extra row in front; the rest of the pipeline is identical.
DOWNLOAD_STAGE = ("s00_download", "Download")
STAGE_BY_ID = {stage.id: stage for stage in STAGES}


def resolve_stage_id(value: str) -> str:
    """Accept full ids ("s06_stt") or prefixes ("s06")."""
    if value in STAGE_BY_ID:
        return value
    matches = [stage.id for stage in STAGES if stage.id.startswith(value + "_") or stage.id.split("_")[0] == value]
    if len(matches) != 1:
        raise PipelineError(f"Unknown stage: {value}")
    return matches[0]


def descendants(stage_ids: Iterable[str]) -> set[str]:
    result = set(stage_ids)
    changed = True
    while changed:
        changed = False
        for stage in STAGES:
            if stage.id not in result and any(dep in result for dep in stage.dependencies):
                result.add(stage.id)
                changed = True
    return result


class PipelineRunner:
    def __init__(self, settings: Settings, database: Database, store: ArtifactStore):
        self.settings = settings
        self.database = database
        self.store = store

    def run(self, episode_id: str, *, from_stage: str | None = None, force: bool = False, only: list[str] | None = None) -> None:
        """Run the DAG. `from_stage` restarts there (and everything downstream); `only` runs just those stages."""
        context = StageContext(episode_id=episode_id, settings=self.settings, store=self.store, db=self.database)
        self.store.ensure_episode(episode_id)
        try:
            start = resolve_stage_id(from_stage) if from_stage else None
            selected = {resolve_stage_id(value) for value in only} if only else None
        except PipelineError as exc:
            self._log(episode_id, {"event": "pipeline_failed", "error": str(exc)})
            raise
        # from_stage: that stage recomputes and downstream stages rerun only if their inputs changed;
        # with force, every descendant recomputes too.
        if start:
            forced = descendants([start]) if force else {start}
        else:
            forced = set(selected or ()) if force else set()
        targets = selected or set(STAGE_BY_ID)

        self.database.update_episode(episode_id, status="processing")
        self._log(episode_id, {"event": "pipeline_start", "from_stage": start, "only": sorted(selected) if selected else None, "force": force})
        pipeline_started = time.perf_counter()

        done: set[str] = set()
        failed: str | None = None
        running: dict[Future, StageSpec] = {}
        lock = threading.Lock()

        def satisfied(stage: StageSpec) -> bool:
            # Stages outside `only` count as satisfied when their artifact already exists.
            return all(dep in done or (dep not in targets and self.store.stage_path(episode_id, dep).exists()) for dep in stage.dependencies)

        with ThreadPoolExecutor(max_workers=max(1, self.settings.stage_parallelism), thread_name_prefix=f"stage-{episode_id[:8]}") as pool:
            pending = [stage for stage in STAGES if stage.id in targets]
            while pending or running:
                if failed is None:
                    for stage in [s for s in pending if satisfied(s)]:
                        pending.remove(stage)
                        running[pool.submit(self._run_stage, context, stage, stage.id in forced, lock)] = stage
                if not running:
                    if pending and failed is None:
                        failed = pending[0].id
                        self.database.update_stage(episode_id, failed, status="failed", error="Upstream artifacts are missing; run the preceding stages first.")
                    break
                finished, _ = wait(running, return_when=FIRST_COMPLETED)
                for future in finished:
                    stage = running.pop(future)
                    if future.result():
                        done.add(stage.id)
                        self._update_progress(episode_id)
                    elif failed is None:
                        failed = stage.id

        if failed:
            self.database.update_episode(episode_id, status="failed")
            return
        complete = all(record.status == "done" for record in self.database.get_stages(episode_id))
        if complete:
            self.database.update_episode(episode_id, status="processed", progress=100)
        else:
            # A partial (`only`) run, e.g. GPU stages on another machine; the API worker resumes the rest.
            self.database.update_episode(episode_id, status="queued")
        self._log(episode_id, {"event": "pipeline_done", "elapsed": round(time.perf_counter() - pipeline_started, 3)})

    def _hash_path(self, episode_id: str, stage_id: str) -> Path:
        return self.store.stage_path(episode_id, stage_id).with_suffix(".hash")

    def fetch_and_run(self, episode_id: str, url: str) -> None:
        """Download a linked video, then run the exact same pipeline as an upload."""
        stage_id = DOWNLOAD_STAGE[0]
        self.database.update_episode(episode_id, status="downloading", progress=0)
        self.database.update_stage(episode_id, stage_id, status="running", error=None, started_at=datetime.now(UTC), finished_at=None)
        started, last = time.perf_counter(), [-5]

        def progress(percent: int) -> None:
            if percent >= last[0] + 5 or percent == 100:
                last[0] = percent
                self.database.update_episode(episode_id, progress=percent)

        try:
            path, title = download(url, self.store.ensure_episode(episode_id), max_bytes=self.settings.max_upload_bytes, on_progress=progress)
        except Exception as exc:
            message = str(exc) if isinstance(exc, PipelineError) else f"{type(exc).__name__}: {exc}"
            self.database.update_stage(episode_id, stage_id, status="failed", error=message, finished_at=datetime.now(UTC))
            self.database.update_episode(episode_id, status="failed")
            self._log(episode_id, {"event": "stage_failed", "stage": stage_id, "error": message})
            return
        record = self.database.get_episode_record(episode_id)
        updates: dict = {"source_path": str(path), "status": "queued", "progress": 0}
        if record is not None and record.title == url:
            updates["title"] = title
        self.database.update_episode(episode_id, **updates)
        self.database.update_stage(episode_id, stage_id, status="done", elapsed=round(time.perf_counter() - started, 3), finished_at=datetime.now(UTC))
        self._log(episode_id, {"event": "stage_done", "stage": stage_id})
        self.run(episode_id)

    def _run_stage(self, context: StageContext, stage: StageSpec, force: bool, lock: threading.Lock) -> bool:
        episode_id = context.episode_id
        try:
            input_hash = self._input_hash(context, stage)
            artifact = self.store.stage_path(episode_id, stage.id)
            sidecar = self._hash_path(episode_id, stage.id)
            # Cache validity lives next to the artifact, so folders synced from another machine count.
            if not force and artifact.exists() and sidecar.exists() and sidecar.read_text(encoding="utf-8").strip() == input_hash:
                with lock:
                    record = next(r for r in self.database.get_stages(episode_id) if r.stage_id == stage.id)
                    if record.status != "done":
                        self.database.update_stage(episode_id, stage.id, status="done", error=None, input_hash=input_hash, finished_at=datetime.now(UTC))
                self._log(episode_id, {"event": "stage_cached", "stage": stage.id})
                return True
            with lock:
                self.database.update_stage(episode_id, stage.id, status="running", error=None, started_at=datetime.now(UTC), finished_at=None)
            started = time.perf_counter()
            value = stage.run(context)
            self.store.write_json(artifact, value)
            self.store.write_text(sidecar, input_hash)
            elapsed = round(time.perf_counter() - started, 3)
            with lock:
                self.database.update_stage(episode_id, stage.id, status="done", elapsed=elapsed, error=None, input_hash=input_hash, finished_at=datetime.now(UTC))
            self._log(episode_id, {"event": "stage_done", "stage": stage.id, "elapsed": elapsed})
            return True
        except Exception as exc:
            message = str(exc) if isinstance(exc, PipelineError) else f"{type(exc).__name__}: {exc}"
            with lock:
                self.database.update_stage(episode_id, stage.id, status="failed", error=message, finished_at=datetime.now(UTC))
            self._log(episode_id, {"event": "stage_failed", "stage": stage.id, "error": message})
            return False

    def _input_hash(self, context: StageContext, stage: StageSpec) -> str:
        base = context.store.stage_input_hash(context.episode_id, stage.id, list(stage.dependencies), stage.version)
        digest = hashlib.sha256(base.encode())
        # Thresholds are part of every stage's inputs so a config change invalidates the cache.
        digest.update(json.dumps(self.settings.thresholds.model_dump(), sort_keys=True).encode())
        if stage.id == "s01_ingest":
            record = self.database.get_episode_record(context.episode_id)
            if record is not None and Path(record.source_path).exists():
                digest.update(context.store.file_hash(Path(record.source_path)).encode())
        return digest.hexdigest()

    def _update_progress(self, episode_id: str) -> None:
        stages = self.database.get_stages(episode_id)
        completed = sum(stage.status == "done" for stage in stages)
        self.database.update_episode(episode_id, progress=round(completed / max(1, len(stages)) * 100))

    def _log(self, episode_id: str, record: dict) -> None:
        record["time"] = datetime.now(UTC).isoformat()
        path = self.store.episode_dir(episode_id) / "logs" / "pipeline.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


class PipelineCoordinator:
    """A bounded local worker. Replaceable with RQ without changing API routes."""

    def __init__(self, runner: PipelineRunner, concurrency: int = 1):
        self.runner = runner
        self.executor = ThreadPoolExecutor(max_workers=max(1, concurrency), thread_name_prefix="drishti-worker")
        self._futures: dict[str, Future[None]] = {}
        self._lock = threading.Lock()

    def enqueue(self, episode_id: str, *, from_stage: str | None = None, force: bool = False) -> bool:
        with self._lock:
            current = self._futures.get(episode_id)
            if current and not current.done():
                return False
            self._futures[episode_id] = self.executor.submit(self.runner.run, episode_id, from_stage=from_stage, force=force)
            return True

    def enqueue_url(self, episode_id: str, url: str) -> bool:
        with self._lock:
            current = self._futures.get(episode_id)
            if current and not current.done():
                return False
            self._futures[episode_id] = self.executor.submit(self.runner.fetch_and_run, episode_id, url)
            return True

    def running(self, episode_id: str) -> bool:
        with self._lock:
            future = self._futures.get(episode_id)
            return bool(future and not future.done())

    def shutdown(self) -> None:
        self.executor.shutdown(wait=False, cancel_futures=False)
