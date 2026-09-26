from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_ROOT.parent


def default_data_dir() -> Path:
    """Use Vercel's only writable filesystem location for the serverless demo."""
    return Path(tempfile.gettempdir()) / "drishti" if os.getenv("VERCEL") else PROJECT_ROOT / "data"


def running_on_vercel() -> bool:
    return bool(os.getenv("VERCEL") or os.getenv("VERCEL_ENV"))


def resolve_ffmpeg(binary: str) -> str:
    """Prefer ffmpeg on PATH; otherwise use the static build bundled with imageio-ffmpeg (no system packages needed)."""
    if shutil.which(binary):
        return binary
    try:
        import imageio_ffmpeg  # type: ignore[import-not-found]
        return imageio_ffmpeg.get_ffmpeg_exe()
    except (ImportError, RuntimeError):
        return binary


class Thresholds(BaseModel):
    # s02 / s03
    shot_scene_threshold: float = Field(default=0.35, ge=0, le=1)
    min_shot_seconds: float = Field(default=0.4, ge=0)
    keyframe_dedup_hamming: int = Field(default=7, ge=0, le=64)
    keyframe_dedup_similarity: float = Field(default=0.93, ge=0, le=1)
    keyframe_dedup_window: int = Field(default=10, gt=0)
    keyframe_second_frame_after: float = Field(default=8.0, gt=0)
    # s05
    vad_min_silence_seconds: float = Field(default=0.3, gt=0)
    # s07
    cleanup_batch_size: int = Field(default=40, gt=0)
    cleanup_context: int = Field(default=5, ge=0)
    cleanup_max_edit_ratio: float = Field(default=0.25, ge=0, le=1)
    # s08
    audio_event_default_threshold: float = Field(default=0.3, ge=0, le=1)
    audio_event_min_cc_seconds: float = Field(default=0.8, ge=0)
    audio_event_max_dialogue_overlap: float = Field(default=0.7, ge=0, le=1)
    # s10
    scene_weight_visual: float = 0.30
    scene_weight_location: float = 0.20
    scene_weight_activity: float = 0.10
    scene_weight_speakers: float = 0.20
    scene_weight_dialogue: float = 0.10
    scene_weight_silence: float = 0.10
    # Long pauses far from any shot cut are scene-boundary candidates too (dialogue-driven scene changes).
    scene_pause_cut_seconds: float = Field(default=2.0, gt=0)
    scene_boundary_threshold: float = Field(default=0.45, ge=0, le=1)
    scene_silence_at_cut_seconds: float = Field(default=1.0, ge=0)
    scene_speaker_window_seconds: float = Field(default=30.0, gt=0)
    min_scene_seconds: float = Field(default=20.0, gt=0)
    scene_llm_window: int = Field(default=8, gt=1)
    # s12
    entity_visible_confidence: float = Field(default=0.60, ge=0, le=1)
    entity_absent_confidence: float = Field(default=0.70, ge=0, le=1)
    entity_absent_min_frames: int = Field(default=6, ge=1)
    entity_window_long_scene: float = Field(default=180.0, gt=0)
    entity_window_padding: float = Field(default=45.0, gt=0)
    entity_max_frames: int = Field(default=10, gt=0)
    # s13
    intensity_weight_llm: float = 0.55
    intensity_weight_audio: float = 0.25
    intensity_weight_dialogue: float = 0.20
    intensity_smoothing_seconds: int = Field(default=5, ge=1)
    # s14
    min_ad_pause_seconds: float = Field(default=1.2, gt=0)
    ad_pause_intensity_ceiling: float = Field(default=0.4, ge=0, le=1)
    ad_snap_to_silence_seconds: float = Field(default=2.0, ge=0)
    ad_blocked_head_seconds: float = Field(default=120.0, ge=0)
    ad_blocked_tail_seconds: float = Field(default=120.0, ge=0)
    ad_default_min_gap: float = Field(default=480.0, ge=0)
    ad_context_lookback: float = Field(default=60.0, ge=0)
    ad_speech_guard_seconds: float = Field(default=0.3, ge=0)
    ad_cliffhanger_guard_seconds: float = Field(default=10.0, ge=0)
    ad_min_safety: float = Field(default=0.45, ge=0, le=1)
    # s15 / s16
    subtitle_max_line_graphemes: int = Field(default=42, gt=0)
    subtitle_max_lines: int = Field(default=2, gt=0)
    subtitle_max_cps: float = Field(default=17.0, gt=0)
    subtitle_min_duration: float = Field(default=1.0, gt=0)
    subtitle_max_duration: float = Field(default=7.0, gt=0)
    subtitle_min_gap: float = Field(default=0.08, ge=0)
    subtitle_cps_extension: float = Field(default=0.5, ge=0)
    cc_sound_shift_seconds: float = Field(default=1.5, ge=0)
    cc_music_ratio: float = Field(default=0.6, ge=0, le=1)
    cc_music_min_gap: float = Field(default=3.0, ge=0)
    # s17
    qc_error_cps: float = Field(default=21.0, gt=0)
    qc_low_confidence: float = Field(default=0.6, ge=0, le=1)
    qc_timing_drift_seconds: float = Field(default=0.5, ge=0)
    qc_missing_speech_seconds: float = Field(default=2.0, ge=0)
    qc_speaker_flip_seconds: float = Field(default=1.0, ge=0)
    qc_max_errors: int = Field(default=0, ge=0)
    qc_max_warnings: int = Field(default=25, ge=0)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BACKEND_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    data_dir: Path = Field(default_factory=default_data_dir)
    database_url: str | None = None
    openai_api_key: str | None = None
    sarvam_api_key: str | None = None
    sarvam_base_url: str = "https://api.sarvam.ai"
    hf_token: str | None = None
    llm_model_default: str = "gpt-4.1-mini"
    llm_model_scenes: str = "gpt-4.1-mini"
    max_llm_usd_per_episode: float = 5.0
    device: str = "cpu"
    ffmpeg_binary: str = "ffmpeg"
    ffprobe_binary: str = "ffprobe"
    max_upload_bytes: int = 8 * 1024 * 1024 * 1024
    worker_concurrency: int = 1
    stage_parallelism: int = 2
    # "dhash" (fast, no model download) or "siglip" (google/siglip-base-patch16-224 via transformers).
    frame_embedder: str = "dhash"
    llm_vision_concurrency: int = 8
    llm_text_concurrency: int = 16
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    seed_demo: bool = True
    thresholds: Thresholds = Field(default_factory=Thresholds)

    def model_post_init(self, __context: object) -> None:
        # A local .env must never redirect a Vercel function to its read-only bundle.
        if running_on_vercel():
            self.data_dir = Path(tempfile.gettempdir()) / "drishti"
        self.ffmpeg_binary = resolve_ffmpeg(self.ffmpeg_binary)

    @property
    def episodes_dir(self) -> Path:
        return self.data_dir / "episodes"

    @property
    def brand_catalogue(self) -> Path:
        canonical = PROJECT_ROOT / "docs" / "brands.json"
        # A Vercel project rooted at backend/ cannot access repository-level docs/.
        return canonical if canonical.is_file() else self.config_dir / "brands.json"

    @property
    def config_dir(self) -> Path:
        return BACKEND_ROOT / "config"

    @property
    def sqlite_url(self) -> str:
        return self.database_url or f"sqlite:///{(self.data_dir / 'drishti.db').as_posix()}"

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
