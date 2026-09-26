from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from sqlmodel import Field, Session, SQLModel, create_engine, select

from .models import EpisodeSummary, StageStatus
from .settings import Settings


def utc_now() -> datetime:
    return datetime.now(UTC)


class EpisodeRecord(SQLModel, table=True):
    id: str = Field(primary_key=True)
    title: str
    source_path: str
    duration: float = 0.0
    fps: float = 0.0
    width: int = 0
    height: int = 0
    status: str = "queued"
    progress: int = 0
    video_available: bool = False
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class StageRecord(SQLModel, table=True):
    pk: int | None = Field(default=None, primary_key=True)
    episode_id: str = Field(index=True)
    stage_id: str
    label: str
    position: int
    status: str = "queued"
    elapsed: float | None = None
    error: str | None = None
    input_hash: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None


class Database:
    def __init__(self, settings: Settings):
        self.settings = settings
        settings.data_dir.mkdir(parents=True, exist_ok=True)
        connect_args = {"check_same_thread": False} if settings.sqlite_url.startswith("sqlite") else {}
        self.engine = create_engine(settings.sqlite_url, connect_args=connect_args)
        SQLModel.metadata.create_all(self.engine)

    def session(self) -> Session:
        return Session(self.engine)

    def create_episode(self, record: EpisodeRecord, stages: list[tuple[str, str]]) -> None:
        with self.session() as session:
            session.add(record)
            session.add_all([
                StageRecord(episode_id=record.id, stage_id=stage_id, label=label, position=index)
                for index, (stage_id, label) in enumerate(stages)
            ])
            session.commit()

    def get_episode_record(self, episode_id: str) -> EpisodeRecord | None:
        with self.session() as session:
            return session.get(EpisodeRecord, episode_id)

    def list_episode_records(self) -> list[EpisodeRecord]:
        with self.session() as session:
            return list(session.exec(select(EpisodeRecord).order_by(EpisodeRecord.created_at.desc())).all())

    def get_stages(self, episode_id: str) -> list[StageRecord]:
        with self.session() as session:
            statement = select(StageRecord).where(StageRecord.episode_id == episode_id).order_by(StageRecord.position)
            return list(session.exec(statement).all())

    def update_episode(self, episode_id: str, **values: object) -> EpisodeRecord:
        with self.session() as session:
            record = session.get(EpisodeRecord, episode_id)
            if record is None:
                raise KeyError(episode_id)
            for key, value in values.items():
                setattr(record, key, value)
            record.updated_at = utc_now()
            session.add(record)
            session.commit()
            session.refresh(record)
            return record

    def update_stage(self, episode_id: str, stage_id: str, **values: object) -> StageRecord:
        with self.session() as session:
            statement = select(StageRecord).where(StageRecord.episode_id == episode_id, StageRecord.stage_id == stage_id)
            record = session.exec(statement).one()
            for key, value in values.items():
                setattr(record, key, value)
            session.add(record)
            session.commit()
            session.refresh(record)
            return record

    def reset_from(self, episode_id: str, stage_id: str) -> None:
        stages = self.get_stages(episode_id)
        start = next((stage.position for stage in stages if stage.stage_id == stage_id), None)
        if start is None:
            raise KeyError(stage_id)
        with self.session() as session:
            statement = select(StageRecord).where(StageRecord.episode_id == episode_id, StageRecord.position >= start)
            for stage in session.exec(statement).all():
                stage.status = "queued"
                stage.elapsed = None
                stage.error = None
                stage.input_hash = None
                stage.started_at = None
                stage.finished_at = None
                session.add(stage)
            episode = session.get(EpisodeRecord, episode_id)
            if episode:
                episode.status = "queued"
                episode.progress = round(start / max(1, len(stages)) * 100)
                episode.updated_at = utc_now()
                session.add(episode)
            session.commit()

    def summary(self, record: EpisodeRecord) -> EpisodeSummary:
        stages = self.get_stages(record.id)
        return EpisodeSummary(
            id=record.id,
            title=record.title,
            duration=record.duration,
            status=record.status,  # type: ignore[arg-type]
            progress=record.progress,
            created_at=record.created_at.isoformat(),
            video_available=record.video_available,
            stages=[StageStatus(
                id=stage.stage_id,
                label=stage.label,
                status=stage.status,  # type: ignore[arg-type]
                elapsed=stage.elapsed,
                error=stage.error,
                started_at=stage.started_at.isoformat() if stage.started_at else None,
                finished_at=stage.finished_at.isoformat() if stage.finished_at else None,
            ) for stage in stages],
        )

    def close(self) -> None:
        self.engine.dispose()

