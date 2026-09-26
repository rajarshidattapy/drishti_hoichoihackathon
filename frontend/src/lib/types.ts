export type Stage = {
  id: string;
  label: string;
  status: "queued" | "running" | "done" | "failed";
  elapsed?: number;
  error?: string;
  started_at?: string;
  finished_at?: string;
};

export type Episode = {
  id: string;
  title: string;
  duration: number;
  status: "queued" | "processing" | "processed" | "failed";
  progress: number;
  created_at: string;
  video_available: boolean;
  stages: Stage[];
};

export type Utterance = {
  utt_id: string;
  start: number;
  end: number;
  speaker: string;
  speaker_name?: string;
  text: string;
  confidence?: number;
  overlap?: boolean;
};

export type Entity = {
  entity_id: string;
  name: string;
  name_bn?: string;
  kind: string;
  brand?: string;
  ad_categories: string[];
  mentions: { source: string; time: number; surface: string }[];
  sentiment: "positive" | "neutral" | "negative";
  presence: "mentioned_and_shown" | "mentioned_only" | "shown_only" | "unverified";
  confidence: number;
  visual_check?: {
    frames_checked: string[];
    visible?: boolean;
    visible_frames: string[];
    confidence: number;
    note: string;
  };
};

export type Scene = {
  scene_id: string;
  start: number;
  end: number;
  visual: {
    location: string;
    objects: string[];
    activity: string;
    visual_mood: string;
    people_count: number;
    confidence: number;
  };
  speakers: string[];
  utt_ids: string[];
  audio_events: string[];
  music_ratio: number;
  semantic: {
    title: string;
    summary: string;
    topics: string[];
    mood: string;
    narrative_intensity: number;
    intensity_components: Record<string, number>;
    is_cliffhanger: boolean;
  };
  entity_ids: string[];
};

export type AdCandidate = {
  cand_id: string;
  time: number;
  scene_id: string;
  kind: string;
  pause_len: number;
  score: {
    pause: number;
    scene_end: number;
    low_intensity: number;
    context_match: number;
    speech_penalty: number;
    cliffhanger_penalty: number;
    total: number;
  };
  disruption: "low" | "medium" | "high";
  matched_categories: string[];
  reason: string;
  selected: boolean;
};

export type SubtitleCue = {
  idx: number;
  start: number;
  end: number;
  lines: string[];
  speakers: string[];
  kind: "dialogue" | "sound";
  cps: number;
};

export type QCIssue = {
  issue_id: string;
  severity: "error" | "warn" | "info";
  rule: string;
  time: number;
  cue_idx?: number;
  message: string;
  suggestion?: string;
};

export type AudioEvent = {
  event_id: string;
  label: string;
  label_bn: string;
  start: number;
  end: number;
  score: number;
  in_cc: boolean;
};

export type Timeline = {
  schema_version: string;
  episode: { id: string; title: string; duration: number; video_available: boolean };
  scenes: Scene[];
  utterances: Utterance[];
  audio_events: AudioEvent[];
  entities: Entity[];
  ad_candidates: AdCandidate[];
  subtitles: Record<string, string | number>;
  subtitle_cues: SubtitleCue[];
  cc_cues: SubtitleCue[];
  qc: QCIssue[];
  curves: { intensity: [number, number][]; loudness: [number, number][] };
  processing: { total_seconds: number; llm_cost_usd: number; models: string[]; cached_stages: number };
  [key: string]: unknown;
};
