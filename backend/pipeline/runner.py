from __future__ import annotations

import json
import threading
import time
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Callable

from app.artifacts import ArtifactStore
from app.db import Database
from app.settings import Settings
from pipeline.errors import PipelineError
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


STAGES: tuple[StageSpec, ...] = (
    StageSpec("s01_ingest", "Ingest", (), "2", s01_ingest),
    StageSpec("s02_shots", "Shot detection", ("s01_ingest",), "2", s02_shots),
    StageSpec("s03_keyframes", "Keyframes", ("s01_ingest", "s02_shots"), "2", s03_keyframes),
    StageSpec("s04_audio_prep", "Audio preparation", ("s01_ingest",), "2", s04_audio_prep),
    StageSpec("s05_vad", "Voice activity", ("s01_ingest", "s04_audio_prep"), "2", s05_vad),
    StageSpec("s06_stt", "Transcript + diarization", ("s04_audio_prep", "s05_vad"), "2", s06_stt),
    StageSpec("s07_transcript_clean", "Transcript cleanup", ("s06_stt",), "2", s07_transcript_clean),
    StageSpec("s08_audio_events", "Audio events", ("s04_audio_prep",), "2", s08_audio_events),
    StageSpec("s09_vision_baseline", "Visual understanding", ("s03_keyframes",), "2", s09_vision_baseline),
    StageSpec("s10_scenes", "Scene segmentation", ("s01_ingest", "s03_keyframes", "s07_transcript_clean", "s09_vision_baseline"), "2", s10_scenes),
    StageSpec("s11_entities_dialogue", "Dialogue entities", ("s07_transcript_clean", "s10_scenes"), "2", s11_entities_dialogue),
    StageSpec("s12_vision_targeted", "Targeted visual checks", ("s03_keyframes", "s11_entities_dialogue"), "2", s12_vision_targeted),
    StageSpec("s13_scene_semantics", "Scene semantics", ("s07_transcript_clean", "s08_audio_events", "s12_vision_targeted"), "2", s13_scene_semantics),
    StageSpec("s14_ad_scoring", "Ad scoring", ("s01_ingest", "s05_vad", "s12_vision_targeted", "s13_scene_semantics"), "2", s14_ad_scoring),
    StageSpec("s15_subtitles", "Bengali subtitles", ("s07_transcript_clean",), "2", s15_subtitles),
    StageSpec("s16_captions", "Closed captions", ("s08_audio_events", "s15_subtitles"), "2", s16_captions),
    StageSpec("s17_qc", "Subtitle QC", ("s05_vad", "s07_transcript_clean", "s15_subtitles"), "2", s17_qc),
    StageSpec("s18_assemble", "Assemble timeline", ("s03_keyframes", "s07_transcript_clean", "s08_audio_events", "s12_vision_targeted", "s13_scene_semantics", "s14_ad_scoring", "s15_subtitles", "s16_captions", "s17_qc"), "2", s18_assemble),
)


STAGE_PAIRS = [(stage.id, stage.label) for stage in STAGES]


class PipelineRunner:
    def __init__(self, settings: Settings, database: Database, store: ArtifactStore):
        self.settings = settings
        self.database = database
        self.store = store

    def run(self, episode_id: str, *, from_stage: str | None = None, force: bool = False) -> None:
        context = StageContext(episode_id=episode_id, settings=self.settings, store=self.store, db=self.database)
        self.store.ensure_episode(episode_id)
        start_index = 0
        if from_stage:
            start_index = next((index for index, stage in enumerate(STAGES) if stage.id == from_stage), -1)
            if start_index < 0:
                raise PipelineError(f"Unknown stage: {from_stage}")
        self.database.update_episode(episode_id, status="processing")
        pipeline_started = time.perf_counter()
        for index, stage in enumerate(STAGES):
            if index < start_index:
                continue
            try:
                input_hash = self._input_hash(context, stage)
                stage_record = next(record for record in self.database.get_stages(episode_id) if record.stage_id == stage.id)
                artifact = self.store.stage_path(episode_id, stage.id)
                cache_valid = artifact.exists() and stage_record.input_hash == input_hash and stage_record.status == "done"
                if cache_valid and not (force and index >= start_index):
                    self._update_progress(episode_id, index + 1)
                    continue
                started = datetime.now(UTC)
                self.database.update_stage(episode_id, stage.id, status="running", error=None, started_at=started, finished_at=None)
                stage_started = time.perf_counter()
                value = stage.run(context)
                self.store.write_json(artifact, value)
                elapsed = round(time.perf_counter() - stage_started, 3)
                self.database.update_stage(
                    episode_id, stage.id, status="done", elapsed=elapsed, error=None, input_hash=input_hash,
                    finished_at=datetime.now(UTC),
                )
                self._update_progress(episode_id, index + 1)
                self._log(episode_id, {"event": "stage_done", "stage": stage.id, "elapsed": elapsed, "cached": False})
            except Exception as exc:
                message = str(exc) if isinstance(exc, PipelineError) else f"{type(exc).__name__}: {exc}"
                self.database.update_stage(episode_id, stage.id, status="failed", error=message, finished_at=datetime.now(UTC))
                self.database.update_episode(episode_id, status="failed")
                self._log(episode_id, {"event": "stage_failed", "stage": stage.id, "error": message})
                return
        self.database.update_episode(episode_id, status="processed", progress=100)
        self._log(episode_id, {"event": "pipeline_done", "elapsed": round(time.perf_counter() - pipeline_started, 3)})

    def _input_hash(self, context: StageContext, stage: StageSpec) -> str:
        base = context.store.stage_input_hash(context.episode_id, stage.id, list(stage.dependencies), stage.version)
        if stage.id != "s01_ingest":
            return base
        record = self.database.get_episode_record(context.episode_id)
        if record is None or not Path(record.source_path).exists():
            return base
        import hashlib
        digest = hashlib.sha256(base.encode())
        digest.update(context.store.file_hash(Path(record.source_path)).encode())
        return digest.hexdigest()

    def _update_progress(self, episode_id: str, completed: int) -> None:
        self.database.update_episode(episode_id, progress=round(completed / len(STAGES) * 100))

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

    def running(self, episode_id: str) -> bool:
        with self._lock:
            future = self._futures.get(episode_id)
            return bool(future and not future.done())

    def shutdown(self) -> None:
        self.executor.shutdown(wait=False, cancel_futures=False)

