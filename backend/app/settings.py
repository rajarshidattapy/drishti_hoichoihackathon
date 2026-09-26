from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Thresholds(BaseModel):
    shot_scene_threshold: float = Field(0.35, ge=0, le=1)
    keyframe_dedup_hamming: int = Field(7, ge=0, le=64)
    min_scene_seconds: float = Field(20.0, gt=0)
    entity_visible_confidence: float = Field(0.60, ge=0, le=1)
    entity_absent_confidence: float = Field(0.70, ge=0, le=1)
    min_ad_pause_seconds: float = Field(1.2, gt=0)
    ad_blocked_head_seconds: float = Field(120.0, ge=0)
    ad_blocked_tail_seconds: float = Field(120.0, ge=0)
    subtitle_max_line_graphemes: int = Field(42, gt=0)
    subtitle_max_lines: int = Field(2, gt=0)
    subtitle_max_cps: float = Field(17.0, gt=0)
    subtitle_min_duration: float = Field(1.0, gt=0)
    subtitle_max_duration: float = Field(7.0, gt=0)
    subtitle_min_gap: float = Field(0.08, ge=0)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / "backend" / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    data_dir: Path = PROJECT_ROOT / "data"
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
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    seed_demo: bool = True
    thresholds: Thresholds = Thresholds()

    @property
    def episodes_dir(self) -> Path:
        return self.data_dir / "episodes"

    @property
    def sqlite_url(self) -> str:
        return self.database_url or f"sqlite:///{(self.data_dir / 'drishti.db').as_posix()}"

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

