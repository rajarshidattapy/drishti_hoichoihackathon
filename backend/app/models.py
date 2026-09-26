from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class StageStatus(BaseModel):
    id: str
    label: str
    status: Literal["queued", "running", "done", "failed"]
    elapsed: float | None = None
    error: str | None = None
    started_at: str | None = None
    finished_at: str | None = None


class EpisodeSummary(BaseModel):
    id: str
    title: str
    duration: float
    status: Literal["queued", "processing", "processed", "failed"]
    progress: int = Field(ge=0, le=100)
    created_at: str
    video_available: bool = False
    stages: list[StageStatus] = Field(default_factory=list)


class Shot(BaseModel):
    shot_id: str
    start: float
    end: float
    keyframe: str | None = None
    dup_of: str | None = None
    embedding_ref: str | None = None


class Word(BaseModel):
    text: str
    start: float
    end: float


class Utterance(BaseModel):
    utt_id: str
    start: float
    end: float
    speaker: str
    speaker_name: str | None = None
    text_raw: str
    text: str
    words: list[Word] | None = None
    confidence: float | None = None
    overlap: bool = False


class VisualTags(BaseModel):
    location: str
    indoor: bool | None = None
    objects: list[str]
    visible_brands: list[str]
    activity: str
    visual_mood: str
    people_count: int
    confidence: float


class SceneSemantic(BaseModel):
    title: str
    summary: str
    topics: list[str]
    mood: str
    narrative_intensity: float
    intensity_components: dict[str, float]
    is_cliffhanger: bool


class Scene(BaseModel):
    scene_id: str
    start: float
    end: float
    shot_ids: list[str]
    visual: VisualTags
    speakers: list[str]
    utt_ids: list[str]
    audio_events: list[str]
    music_ratio: float
    semantic: SceneSemantic
    entity_ids: list[str]


class EntityMention(BaseModel):
    source: Literal["dialogue", "visual"]
    time: float
    utt_id: str | None = None
    shot_id: str | None = None
    surface: str


class VisualCheck(BaseModel):
    frames_checked: list[str]
    visible: bool | None = None
    visible_frames: list[str]
    confidence: float
    note: str


class Entity(BaseModel):
    entity_id: str
    name: str
    name_bn: str | None = None
    kind: Literal["product", "brand", "place", "food", "activity", "topic", "other"]
    brand: str | None = None
    ad_categories: list[str]
    mentions: list[EntityMention]
    sentiment: Literal["positive", "neutral", "negative"]
    presence: Literal["mentioned_and_shown", "mentioned_only", "shown_only", "unverified"]
    visual_check: VisualCheck | None = None
    confidence: float


class AudioEvent(BaseModel):
    event_id: str
    label: str
    label_bn: str
    start: float
    end: float
    score: float
    in_cc: bool


class ScoreBreakdown(BaseModel):
    pause: float
    scene_end: float
    low_intensity: float
    context_match: float
    speech_penalty: float
    cliffhanger_penalty: float
    total: float


class AdCandidate(BaseModel):
    cand_id: str
    time: float
    scene_id: str
    kind: Literal["scene_boundary", "dialogue_pause"]
    pause_len: float
    score: ScoreBreakdown
    disruption: Literal["low", "medium", "high"]
    matched_categories: list[str]
    context_entity_ids: list[str]
    reason: str
    selected: bool


class SubtitleCue(BaseModel):
    idx: int
    start: float
    end: float
    lines: list[str]
    speakers: list[str]
    kind: Literal["dialogue", "sound"]
    cps: float


class QCIssue(BaseModel):
    issue_id: str
    severity: Literal["error", "warn", "info"]
    rule: str
    time: float
    cue_idx: int | None = None
    message: str
    suggestion: str | None = None


class SemanticTimeline(BaseModel):
    schema_version: str = "1.0"
    episode: dict[str, Any]
    scenes: list[Scene]
    shots: list[Shot]
    utterances: list[Utterance]
    audio_events: list[AudioEvent]
    entities: list[Entity]
    ad_candidates: list[AdCandidate]
    subtitles: dict[str, Any]
    subtitle_cues: list[SubtitleCue]
    cc_cues: list[SubtitleCue]
    qc: list[QCIssue]
    curves: dict[str, list[list[float]]]
    processing: dict[str, Any]


class RerunRequest(BaseModel):
    from_stage: str = "s01"
    force: bool = False


class AdSelectionPatch(BaseModel):
    selected: bool
