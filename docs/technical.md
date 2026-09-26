# Hoichoi Drishti — Technical Design

Companion to `prd.md`. This document covers the architecture, pipeline stages, data schema, scoring logic, API, UI implementation and the build plan.

---

## 1. Architecture overview

```
                ┌──────────────────────────────────────────┐
                │              Web UI (React)              │
                │  Library · Workspace · Timeline · Tabs   │
                └───────────────┬──────────────────────────┘
                                │ REST + SSE (progress)
                ┌───────────────▼──────────────────────────┐
                │           API (FastAPI)                  │
                │  episodes · jobs · timeline · exports    │
                └───────┬──────────────────────┬───────────┘
                        │ enqueue              │ read
                ┌───────▼────────┐     ┌───────▼───────────┐
                │ Worker (RQ)    │     │ SQLite + artifacts│
                │ Stage runner   │────►│ data/episodes/{id}│
                └───────┬────────┘     └───────────────────┘
                        │
   ┌────────────┬───────┴─────┬──────────────┬──────────────┐
   ▼            ▼             ▼              ▼              ▼
 ffmpeg     Local models   Sarvam API    OpenAI API     Local rules
 (media)    TransNetV2 /   (Bengali      (vision, LLM,  (subtitle fmt,
            PySceneDetect  speech-to-    embeddings)    QC, ad score)
            SigLIP, Demucs text, diar.)
            Silero, PANNs
            pyannote(opt)
```

**Principles**
- **Stage-based and cached.** Each stage reads the artifacts from earlier stages and writes its own. A stage that has finished is never recomputed unless it is forced.
- **Pydantic is the source of truth.** Every artifact is a Pydantic model serialized to JSON. The final `semantic_timeline.json` is assembled from those models.
- **LLM calls always use structured outputs** with JSON schemas generated from the Pydantic models, followed by validation and a retry on failure.
- **Heavy local models run on a GPU box** (Kaggle, Colab or a rented GPU). The API and UI can run anywhere and simply read the artifacts.

---

## 2. Tech stack

| Layer | Choice | Notes |
|---|---|---|
| Language | Python 3.11 | |
| API | FastAPI + Uvicorn | SSE for progress |
| Jobs | RQ + Redis | Or `asyncio` + one subprocess worker if you want no Redis |
| DB | SQLite (SQLModel) | Episode and stage status only; content lives in JSON files |
| Media | ffmpeg / ffprobe | |
| Shots | TransNetV2 (GPU), PySceneDetect `AdaptiveDetector` as fallback | |
| Frame embeddings | SigLIP (`google/siglip-base-patch16-224`) via `open_clip` / `transformers` | Deduplication plus the scene similarity signal |
| Vocal separation | Demucs `htdemucs` (`--two-stems=vocals`) | |
| VAD | Silero VAD | |
| Speech-to-text + diarization | Sarvam (Saarika) | Use batch/job mode with diarization for long audio; confirm current limits in the Sarvam docs |
| Diarization fallback | pyannote `speaker-diarization-3.1` | Needs a Hugging Face token |
| Audio events | PANNs `Cnn14` (AudioSet 527 classes) | AST is an alternative |
| Loudness | librosa RMS, pyloudnorm | |
| LLM / vision | OpenAI `gpt-4.1-mini` (default), `gpt-4.1` for scene merge if budget allows | Structured outputs |
| Embeddings (search) | `text-embedding-3-small` + LanceDB | P2 |
| Subtitles | `srt`, `webvtt-py` + custom formatter | |
| Frontend | Vite + React + TypeScript + Tailwind | |
| Player | Native `<video>` with `<track>` | Simple, and handles VTT natively |
| Timeline | Custom SVG/Canvas lanes | wavesurfer.js optional for the waveform |
| JSON viewer | `react-json-view-lite` | |

---

## 3. Repo layout

```
drishti/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── api/                 # routes: episodes, jobs, timeline, exports
│   │   ├── models/              # Pydantic schemas (section 5)
│   │   ├── db.py
│   │   └── settings.py          # env, thresholds, category config
│   ├── pipeline/
│   │   ├── runner.py            # stage DAG + caching
│   │   ├── stages/
│   │   │   ├── s01_ingest.py
│   │   │   ├── s02_shots.py
│   │   │   ├── s03_keyframes.py
│   │   │   ├── s04_audio_prep.py
│   │   │   ├── s05_vad.py
│   │   │   ├── s06_stt.py
│   │   │   ├── s07_transcript_clean.py
│   │   │   ├── s08_audio_events.py
│   │   │   ├── s09_vision_baseline.py
│   │   │   ├── s10_scenes.py
│   │   │   ├── s11_entities_dialogue.py
│   │   │   ├── s12_vision_targeted.py
│   │   │   ├── s13_scene_semantics.py
│   │   │   ├── s14_ad_scoring.py
│   │   │   ├── s15_subtitles.py
│   │   │   ├── s16_captions.py
│   │   │   ├── s17_qc.py
│   │   │   └── s18_assemble.py
│   │   ├── llm.py               # OpenAI wrapper: structured output, retry, cost log
│   │   ├── sarvam.py            # Sarvam client
│   │   └── prompts/             # prompt templates (.md)
│   ├── config/
│   │   ├── ad_categories.yaml
│   │   └── sound_labels_bn.yaml # AudioSet label -> Bengali CC text
│   └── pyproject.toml
├── frontend/
│   └── src/
│       ├── pages/Library.tsx
│       ├── pages/Workspace.tsx
│       ├── components/Player.tsx
│       ├── components/Timeline/  # lanes
│       ├── components/ScenePanel.tsx
│       ├── components/tabs/      # Scenes, Transcript, Entities, Ads, Subtitles, QC, Json
│       └── api.ts
└── data/episodes/{episode_id}/   # artifacts (section 4)
```

---

## 4. Artifact layout (per episode)

```
data/episodes/{id}/
├── source.mp4
├── proxy.mp4               # 720p H.264 for browser playback
├── audio/
│   ├── full_16k.wav        # mono 16 kHz
│   ├── vocals_16k.wav      # Demucs output
│   └── chunks/             # VAD-aligned chunks for speech-to-text
├── frames/
│   ├── kf_{shot_id}.jpg    # baseline keyframes
│   └── tgt_{entity_id}_{n}.jpg
├── stages/
│   ├── s01_ingest.json
│   ├── s02_shots.json
│   ├── …
│   └── s17_qc.json
├── outputs/
│   ├── semantic_timeline.json
│   ├── episode_bn.srt / .vtt
│   ├── episode_bn_cc.srt / .vtt
│   ├── ad_cuepoints.json / .csv
│   └── qc_report.json
└── logs/
    ├── pipeline.log
    └── llm_calls.jsonl      # prompt hash, model, tokens, cost, latency
```

---

## 5. Data schema (Pydantic)

All times are **seconds as floats** from the start of the episode. IDs are stable strings.

```python
# models/timeline.py
from pydantic import BaseModel, Field
from typing import Literal, Optional

class Shot(BaseModel):
    shot_id: str                 # "shot_0042"
    start: float
    end: float
    keyframe: Optional[str]      # path; None if deduped
    dup_of: Optional[str]        # shot_id whose keyframe represents it
    embedding_ref: Optional[str] # index into npy

class VisualTags(BaseModel):
    location: str                # "restaurant", "living room", "street" …
    indoor: Optional[bool]
    objects: list[str]
    visible_brands: list[str]
    activity: str
    visual_mood: str
    people_count: int
    confidence: float

class Word(BaseModel):
    text: str
    start: float
    end: float

class Utterance(BaseModel):
    utt_id: str
    start: float
    end: float
    speaker: str                 # "SPK_A"
    speaker_name: Optional[str]  # P2
    text_raw: str
    text: str                    # cleaned + punctuated Bengali
    words: Optional[list[Word]]
    confidence: Optional[float]
    overlap: bool = False

class AudioEvent(BaseModel):
    event_id: str
    label: str                   # AudioSet label "Knock"
    label_bn: str                # "দরজায় কড়া নাড়ার শব্দ"
    start: float
    end: float
    score: float
    in_cc: bool

PresenceClass = Literal["mentioned_and_shown","mentioned_only","shown_only","unverified"]

class EntityMention(BaseModel):
    source: Literal["dialogue","visual"]
    time: float
    utt_id: Optional[str]
    shot_id: Optional[str]
    surface: str                 # "ফোনটা" / "Samsung"

class VisualCheck(BaseModel):
    frames_checked: list[str]
    visible: Optional[bool]      # None = inconclusive
    visible_frames: list[str]
    confidence: float
    note: str

class Entity(BaseModel):
    entity_id: str
    name: str                    # canonical English: "smartphone"
    name_bn: Optional[str]
    kind: Literal["product","brand","place","food","activity","topic","other"]
    brand: Optional[str]
    ad_categories: list[str]     # ["mobile"]
    mentions: list[EntityMention]
    sentiment: Literal["positive","neutral","negative"]
    presence: PresenceClass
    visual_check: Optional[VisualCheck]
    confidence: float

class SceneSemantic(BaseModel):
    title: str
    summary: str
    topics: list[str]
    mood: str
    narrative_intensity: float   # 0..1 fused
    intensity_components: dict[str, float]  # llm, audio_energy, dialogue_density
    is_cliffhanger: bool

class Scene(BaseModel):
    scene_id: str
    start: float
    end: float
    shot_ids: list[str]
    visual: VisualTags           # aggregated over shots
    speakers: list[str]
    utt_ids: list[str]
    audio_events: list[str]
    music_ratio: float
    semantic: SceneSemantic
    entity_ids: list[str]

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
    kind: Literal["scene_boundary","dialogue_pause"]
    pause_len: float
    score: ScoreBreakdown
    disruption: Literal["low","medium","high"]
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
    kind: Literal["dialogue","sound"]
    cps: float

class QCIssue(BaseModel):
    issue_id: str
    severity: Literal["error","warn","info"]
    rule: str
    time: float
    cue_idx: Optional[int]
    message: str
    suggestion: Optional[str]

class SemanticTimeline(BaseModel):
    schema_version: str = "1.0"
    episode: dict                # id, title, duration, fps, resolution
    scenes: list[Scene]
    shots: list[Shot]
    utterances: list[Utterance]
    audio_events: list[AudioEvent]
    entities: list[Entity]
    ad_candidates: list[AdCandidate]
    subtitles: dict              # paths + cue counts
    qc: list[QCIssue]
    curves: dict                 # {"intensity":[[t,v],…], "loudness":[[t,v],…]} at 1 Hz
    processing: dict             # per-stage timing, model versions, llm cost
```

Publish the JSON Schema with `SemanticTimeline.model_json_schema()` at `GET /schema`.

---

## 6. Pipeline stages

The runner executes a DAG. Stages whose inputs are ready can run in parallel: the audio branch and the video branch are independent until stage s10.

```
s01 ingest
 ├── VIDEO: s02 shots → s03 keyframes → s09 vision_baseline ─┐
 └── AUDIO: s04 audio_prep → s05 vad → s06 stt → s07 clean ──┤
            s04 → s08 audio_events ─────────────────────────┤
                                                             ▼
                                  s10 scenes → s11 entities_dialogue
                                            → s12 vision_targeted
                                            → s13 scene_semantics
                                            → s14 ad_scoring
                          s07 → s15 subtitles → s16 captions (needs s08)
                                              → s17 qc
                                  all → s18 assemble
```

### s01 — Ingest
- `ffprobe` records duration, fps, resolution and audio streams.
- Create a proxy: `ffmpeg -i source -vf scale=-2:720 -c:v libx264 -preset veryfast -crf 26 -c:a aac -b:a 128k -movflags +faststart proxy.mp4`
- Extract audio: `ffmpeg -i source -ac 1 -ar 16000 audio/full_16k.wav`

### s02 — Shots
- TransNetV2 gives per-frame transition probabilities; threshold at 0.5.
- Fallback: `scenedetect -i proxy.mp4 detect-adaptive list-scenes`.
- Merge shots shorter than 0.4 s into their neighbour.

### s03 — Keyframes and deduplication
- One frame per shot at the midpoint. Long shots over 8 s get a second frame at 75%.
- Compute a SigLIP embedding for each keyframe.
- **Dedup:** if cosine similarity with any keyframe in the previous 10 shots is at least 0.93, set `dup_of`, which skips vision on that frame. This typically removes 40–60% of frames in dialogue-heavy drama because of shot/reverse-shot editing.
- Save the embeddings as `stages/embeddings.npy`.

### s04 — Audio prep
- `demucs --two-stems=vocals -n htdemucs` on the full audio, then resample the vocals to 16 kHz mono.
- For episodes over 30 min, run Demucs in 10-minute segments with 5 s overlap to keep memory manageable.

### s05 — VAD
- Silero VAD on `vocals_16k.wav` produces speech segments.
- Build **chunks** for speech-to-text by merging speech segments up to a maximum chunk length, splitting only at silences of at least 300 ms. Set the maximum to the limit of the Sarvam endpoint you use; if you use batch mode, you can send the whole file.
- Store the silence intervals. They become the pause candidates in s14.

### s06 — Speech-to-text and diarization
- **Primary:** Sarvam speech-to-text on the vocals track with `language_code=bn-IN`, requesting timestamps and diarization. Batch/job mode is preferable for full episodes.
- Normalize the response into `Utterance[]`. If only chunk-level timestamps are returned, offset them by each chunk's start.
- **Fallback diarization:** if Sarvam diarization isn't available, run pyannote 3.1 and assign each utterance the speaker label with the largest time overlap.
- Mark an utterance `overlap=true` when two diarization turns overlap it by more than 300 ms.
- Keep `text_raw` exactly as returned.

### s07 — Transcript cleanup (LLM)
- Batch about 40 utterances per call and include the 5 previous utterances as context.
- Instruction: restore Bengali punctuation (`।`, `?`, `!`, `,`), fix obvious ASR spacing errors, **do not paraphrase**, keep code-mixed English as spoken, and return exactly the same `utt_id`s.
- Validation: the character-level edit distance between the raw and cleaned text must be at most 25%. Otherwise keep the raw text and flag it for QC.

### s08 — Audio events and loudness
- PANNs Cnn14 on `full_16k.wav` (the full mix, not the vocals track), with 1 s windows and 0.5 s hop.
- Keep labels in the `sound_labels_bn.yaml` whitelist whose score is at least the per-label threshold (default 0.3). Merge consecutive windows into events.
- `in_cc=true` if the event lasts at least 0.8 s, scores at least the label's `cc_threshold`, and does not overlap dialogue by more than 70%. Music is handled separately as a mood tag.
- Compute RMS loudness at 1 Hz, normalized to 0–1 across the episode, and the music ratio per second (the "Music" class score).

Example `sound_labels_bn.yaml`:
```yaml
Knock:            { bn: "দরজায় কড়া নাড়ার শব্দ", cc_threshold: 0.35 }
Rain:             { bn: "বৃষ্টির শব্দ",          cc_threshold: 0.40 }
Thunder:          { bn: "বজ্রপাত",               cc_threshold: 0.35 }
Telephone bell ringing: { bn: "ফোন বেজে উঠছে",    cc_threshold: 0.35 }
Ringtone:         { bn: "ফোন বেজে উঠছে",          cc_threshold: 0.35 }
Door:             { bn: "দরজা খোলার শব্দ",         cc_threshold: 0.40 }
Laughter:         { bn: "হাসির শব্দ",              cc_threshold: 0.45 }
Crying, sobbing:  { bn: "কান্নার শব্দ",             cc_threshold: 0.40 }
Crowd:            { bn: "ভিড়ের কোলাহল",            cc_threshold: 0.45 }
Vehicle horn, car horn, honking: { bn: "গাড়ির হর্ন", cc_threshold: 0.40 }
Gunshot, gunfire: { bn: "গুলির শব্দ",              cc_threshold: 0.30 }
Footsteps:        { bn: "পায়ের শব্দ",               cc_threshold: 0.50 }
```

### s09 — Vision baseline (LLM vision)
- Input: every keyframe with `dup_of == null`.
- Batch 4 keyframes per request at `detail: "low"`, each labelled with its `shot_id`, and ask for `VisualTags` for each.
- Prompt rules: name only objects that are clearly visible; list only brands that are legible or unmistakable; keep locations to a short, consistent vocabulary (provide a suggested list); use English for tags.
- Deduplicated shots inherit the tags of their `dup_of` shot.

### s10 — Scene segmentation
Scenes are built in two steps.

**Step A — Heuristic boundary scoring between consecutive shots** `i` and `i+1`:
```
b = 0.35 * (1 - cos_sim(emb_i, emb_{i+1}))       # visual change, window-averaged over ±2 shots
  + 0.25 * location_changed(tags_i, tags_{i+1})
  + 0.20 * speaker_set_change(window before, window after)
  + 0.20 * silence_at_cut (≥ 1.0 s silence spanning the cut)
```
Boundaries where `b ≥ 0.45` become candidates. Enforce a minimum scene length of 20 s by merging the weakest boundaries first.

**Step B — LLM validation.** Build a compact per-scene digest: time range, shot count, locations, dominant objects and the first and last three utterances. Ask the LLM, over windows of about 8 candidate scenes, to **merge or keep** each boundary and to give each scene a title. The LLM can only merge candidate boundaries; it cannot add new ones. This keeps it grounded in the evidence.

Aggregate the visual tags per scene: take the majority location, and the union of objects weighted by the fraction of shot time they appear in.

### s11 — Dialogue entity extraction (LLM)
- Run per scene. The input is the scene's utterances (with `utt_id` and time) plus the scene's visual tags.
- Output is a list of `Entity` drafts with `mentions[source=dialogue]`, `kind`, `brand`, `sentiment`, canonical English `name`, `name_bn`, and `ad_categories` chosen from `ad_categories.yaml`.
- The prompt must cover implicit references ("ফোনটা", "ওটা"), resolved within the scene; brands in either script; and **no invented entities**, since every mention must cite a `utt_id`.
- Cross-scene merging happens afterwards: entities with the same `name` and `brand` share an `entity_id`, but each scene keeps its own presence verdict.

Example `ad_categories.yaml`:
```yaml
mobile:        [smartphone, phone, mobile, earphones, charger]
food_delivery: [food, restaurant, biryani, pizza, order, hungry]
fashion:       [saree, dress, clothes, shoes, jewellery]
travel:        [trip, vacation, flight, hotel, train, darjeeling, puri]
finance:       [loan, bank, salary, money, insurance, upi]
beauty:        [makeup, cream, shampoo, skincare]
auto:          [car, bike, scooter]
```
The LLM chooses categories. The keyword lists are hints included in the prompt, not hard matching rules.

### s12 — Targeted vision verification
For each dialogue entity of kind `product` or `brand` (and `food` when relevant):
1. **Window:** the enclosing scene. For scenes longer than 180 s, use ±45 s around the mentions, clipped to the scene bounds.
2. **Sample:** 1 fps, then deduplicate by SigLIP similarity (≥ 0.95), keeping at most 10 frames spread evenly across the window.
3. **Cheap pre-check:** if the scene's baseline `objects` already contains the entity (fuzzy match), mark it visible using the frames from that shot, and skip steps 4–5.
4. **Vision call:** send the frames at `detail: "high"`, 2×5 grids stitched into two images with timestamps burned in. Ask a single question: *"Is a {name} ({brand if any}) visible? Return the timestamps of the frames where it is visible, and a confidence."*
5. **Verdict:**
   - visible with confidence ≥ 0.6 → `mentioned_and_shown`
   - not visible with confidence ≥ 0.7 across ≥ 6 frames → `mentioned_only`
   - otherwise → `unverified`
- Visual-only entities: `visible_brands` and product-like `objects` from the baseline that have no dialogue mention become `shown_only` entities.

### s13 — Scene semantics
- An LLM call per scene, with the summary digest, full utterances, visual tags and audio events as input, returns `title`, `summary`, `topics`, `mood`, `llm_intensity ∈ [0,1]` and `is_cliffhanger`.
- **Fused intensity:**
```
audio_energy     = mean(loudness over scene) normalized to episode p10–p90
dialogue_density = speech_seconds / scene_seconds, then overlap-weighted (+0.2 per overlap ratio)
narrative_intensity = 0.55*llm_intensity + 0.25*audio_energy + 0.20*dialogue_density
```
- The final scene of the episode, and any scene with `is_cliffhanger`, gets `cliffhanger` protection used in s14.
- Emit a per-second intensity curve for the UI by smoothing across scene boundaries with a 5 s window.

### s14 — Ad scoring
**Candidates**
- Every scene boundary becomes a candidate at the midpoint of the silence nearest to the cut, within ±2 s. If there is no silence, use the cut time.
- Every silence of at least 1.2 s inside a scene with `narrative_intensity < 0.4` becomes a candidate.
- Candidates inside blocked zones (default: first 120 s and last 120 s) are dropped.

**Score components (each 0–1)**
```
pause          = min(pause_len / 2.5, 1)
scene_end      = 1 if kind == scene_boundary else max(0, 1 - dist_to_scene_end/30)
low_intensity  = 1 - mean(intensity over [t-20s, t+5s])
context_match  = max over entities in [t-60s, t] of
                   (entity.confidence * sentiment_w * presence_w) , 0 if none
                   sentiment_w: pos 1.0, neutral 0.7, neg 0.3
                   presence_w:  mentioned_and_shown 1.0, mentioned_only 0.9,
                                shown_only 0.8, unverified 0.6
speech_penalty = 1 if speech within ±0.3s of t else 0
cliffhanger_penalty = 1 if t inside or within 10 s after a cliffhanger scene's peak
                       (but scene *end* of a cliffhanger is allowed)

total = 0.25*pause + 0.25*scene_end + 0.30*low_intensity + 0.20*context_match
        - 0.50*speech_penalty - 0.40*cliffhanger_penalty
total = clamp(total, 0, 1)
```
`disruption` is low when `low_intensity ≥ 0.6` and `speech_penalty == 0`, high when `low_intensity < 0.35` or any penalty applies, and medium otherwise.

**Selection:** greedily pick the highest-scoring candidates, enforcing `min_gap` (default 480 s) and `n_breaks` (default `floor(duration/600)`). Selection re-runs instantly when the settings change: it's pure Python over the cached candidates, exposed through an API.

**Reason text:** template-generated from the score components, with no LLM call. For example: *"Scene boundary after 'Restaurant conversation'; 1.4 s pause; low intensity (0.22); positive smartphone discussion 5 s earlier → mobile."*

### s15 — Subtitles
The formatter is deterministic and has no LLM in the loop.
1. Start from the cleaned utterances. Split long utterances at `।?!` first, then at commas or conjunctions (এবং, কিন্তু, তাই, আর), then at the word nearest the midpoint.
2. Timing: when word timestamps are available, cut at word boundaries. Otherwise distribute the time proportionally by grapheme count. **Count Bengali graphemes with the `regex` module's `\X`, not `len()`**, because conjuncts inflate `len()`.
3. Constraints:
   - `MAX_LINE = 42` graphemes, `MAX_LINES = 2`, `MAX_CPS = 17`
   - `MIN_DUR = 1.0 s`, `MAX_DUR = 7.0 s`, `MIN_GAP = 0.08 s`
   - If CPS is exceeded, extend the end into available silence up to +0.5 s; if it's still over, split the cue.
4. Line breaking: balance the two lines (prefer a bottom-heavy pyramid), and never break right after a single short word.
5. Speaker change within a cue: prefix each line with `- `.
6. Write `episode_bn.srt` using the `srt` library, and write the VTT with `webvtt-py` or directly.

### s16 — Closed captions
- Merge the dialogue cues with sound cues from events where `in_cc=true`: `[label_bn]` as its own cue, at least 1.0 s long.
- If a sound overlaps a dialogue cue, add it as an extra first line of that cue when the cue has only one line; otherwise shift the sound cue into the nearest gap within ±1.5 s, and drop it if no gap exists.
- Music: when the scene's `music_ratio > 0.6` and there is no dialogue for 3 s or more, emit `[সঙ্গীত]`, or `[{mood} সঙ্গীত]` using a small mapping from mood to Bengali adjective.

### s17 — QC
Each rule is a pure function over `(cues, utterances, vad, events)` and returns `QCIssue[]`.

| Rule | Severity | Condition |
|---|---|---|
| `low_confidence` | warn | utterance confidence < 0.6, or cleanup rejected in s07 |
| `reading_speed` | warn/error | cps > 17 (warn) or > 21 (error) |
| `line_length` | warn | line > 42 graphemes |
| `line_count` | error | > 2 lines |
| `overlap_speech` | warn | the cue spans an utterance with `overlap=true` |
| `duration` | info/warn | < 1.0 s or > 7.0 s |
| `timing_drift` | warn | cue start more than 0.5 s from the nearest VAD speech onset |
| `speaker_ambiguous` | info | diarization confidence low or speaker flipped within 1 s |
| `missing_speech` | warn | VAD speech ≥ 2 s with no cue covering it |

Also produce a summary: counts by severity and a pass/fail against thresholds.

### s18 — Assemble
- Load all stage outputs, build the `SemanticTimeline`, validate it, and write `outputs/semantic_timeline.json`.
- Attach `processing`: timing per stage, model identifiers, and the total LLM cost from `llm_calls.jsonl`.

---

## 7. LLM layer (`pipeline/llm.py`)

```python
def call_structured(model: str, system: str, user_parts: list, schema: type[BaseModel],
                    stage: str, temperature: float = 0.1, max_retries: int = 2) -> BaseModel:
    # 1. cache key = sha256(model + system + serialized user_parts + schema name)
    # 2. cache hit -> return parsed
    # 3. client.responses.parse(... text_format=schema)  (or chat.completions.parse)
    # 4. validate; on failure append error to prompt and retry
    # 5. log tokens, cost, latency to llm_calls.jsonl; write cache
```

- **Disk cache** of every call keyed by content hash. Re-runs cost nothing, and the demo is reproducible.
- **Concurrency:** an `asyncio.Semaphore(8)` for vision calls and 16 for text calls, with exponential backoff on 429 responses.
- **Prompts** live in `prompts/*.md` as Jinja templates, versioned by filename.
- **Cost guardrail:** a `MAX_LLM_USD_PER_EPISODE` environment variable. The runner stops before any stage whose estimated cost would exceed the remaining budget.

**Rough call budget (45-min drama):** ~500 shots become ~220 unique keyframes, which is ~55 baseline vision calls; ~20 scene calls each for s11 and s13; ~15 s07 calls; 5–10 s10 calls; and ~10–25 targeted vision calls. That's about 130–150 calls, mostly on the mini model.

---

## 8. Sarvam client (`pipeline/sarvam.py`)

- Wraps speech-to-text. Send the vocals track, `bn-IN`, with timestamps and diarization requested.
- Handles both modes: **sync** for short chunks from s05, and **batch/job** for full audio (submit, poll, fetch).
- Normalizes any response shape into `Utterance[]`. Keep the raw response in `stages/s06_raw.json` so you can re-parse without calling the API again.
- Endpoint names, duration limits and diarization parameters change over time, so confirm them against the current Sarvam docs before wiring this up. Keep the client behind an interface so pyannote plus another ASR can be swapped in.

---

## 9. API

| Method | Path | Purpose |
|---|---|---|
| POST | `/episodes` | Multipart upload or `{path}`; creates the episode and enqueues the pipeline |
| GET | `/episodes` | List with status |
| GET | `/episodes/{id}` | Metadata plus per-stage status |
| GET | `/episodes/{id}/events` | **SSE** stream of stage progress |
| POST | `/episodes/{id}/rerun` | `{from_stage, force}` |
| GET | `/episodes/{id}/timeline` | Full `semantic_timeline.json` |
| GET | `/episodes/{id}/scenes/{scene_id}` | Scene with resolved utterances and entities |
| GET | `/episodes/{id}/ads?min_gap=&n_breaks=&blocked=` | Re-runs selection over cached candidates |
| PATCH | `/episodes/{id}/ads/{cand_id}` | Manual select/unselect |
| GET | `/episodes/{id}/frames/{name}` | Serves keyframes and targeted frames |
| GET | `/episodes/{id}/video` | Proxy MP4 with HTTP range support (`FileResponse`) |
| GET | `/episodes/{id}/subs/{kind}.{fmt}` | `kind ∈ {sub, cc}`, `fmt ∈ {srt, vtt}` |
| GET | `/episodes/{id}/export/{name}` | `ad_cuepoints.csv`, `qc_report.json`, `semantic_timeline.json` |
| GET | `/search?episode_id=&q=` | P2 |
| GET | `/schema` | JSON Schema of `SemanticTimeline` |

---

## 10. Frontend

### State
- On opening the workspace, fetch `/timeline` once. The whole timeline is small enough to hold in memory: a 45-minute episode produces well under 5 MB.
- The only global state is `currentTime`, `selectedSceneId`, `laneVisibility` and `adSettings`. Use Zustand or plain React context.
- `currentTime` comes from the video element's `timeupdate` event, throttled to about 10 Hz. `seek(t)` is exported globally.

### Components
- **Player:** `<video src=/video>` with two `<track>` elements (sub VTT, CC VTT) and a toggle between them.
- **Timeline:** one SVG with a shared x-scale (`d3-scale` only). Zoom and pan via the wheel and drag. The lanes are:
  - Scenes: colored blocks with titles, color by mood
  - Speakers: thin bars per utterance, colored per speaker
  - Entities: icons at mention times; the border style encodes the presence class
  - Sounds: icons for `in_cc` events
  - Intensity: an area chart from `curves.intensity`
  - Ads: triangle markers sized by score, filled if selected
  - A playhead line drawn across all lanes; clicking anywhere seeks
- **ScenePanel:** derived from `currentTime`. Shows title, time, summary, visual tags, intensity bar, speakers and entity chips. A thumbnail strip shows the scene's keyframes.
- **Tabs:**
  - *Scenes:* a sortable table
  - *Transcript:* virtualized list (`react-virtuoso`), auto-scrolling to the current utterance
  - *Entities:* grouped by category, with presence badges; expanding one shows the checked frames with visible ones highlighted
  - *Ads:* settings form, ranked cards, a stacked score-breakdown bar per card, and a select toggle
  - *Subtitles:* cue list with inline editing (P2) and download buttons
  - *QC:* issue list with a severity filter, click to seek
  - *JSON:* tree viewer plus download

### Styling
- Tailwind with a dark UI by default, which suits a video tool.
- Presence badges: shown = green, mentioned-only = amber, shown-only = blue, unverified = gray.
- Bengali font: **Noto Sans Bengali** via Google Fonts, also used in the subtitle track through `::cue { font-family }`.

---

## 11. Config and environment

```env
OPENAI_API_KEY=
SARVAM_API_KEY=
HF_TOKEN=                      # only if the pyannote fallback is used
DATA_DIR=./data
REDIS_URL=redis://localhost:6379
LLM_MODEL_DEFAULT=gpt-4.1-mini
LLM_MODEL_SCENES=gpt-4.1-mini
MAX_LLM_USD_PER_EPISODE=5
DEVICE=cuda                    # cpu fallback: slower Demucs/TransNetV2
```

All thresholds (dedup similarity, boundary weights, ad weights, subtitle limits, QC thresholds) live in `settings.py` as a single `Thresholds` model and are recorded in `processing` so each run is reproducible.

---

## 12. Compute plan

- **GPU stages** (Demucs, TransNetV2, SigLIP, PANNs, pyannote) run on Kaggle or Colab. Package them as `python -m pipeline.run --episode X --stages s02,s03,s04,s08` and sync the `data/episodes/X/` folder back.
- **CPU and API stages** (everything else) run locally.
- The runner only checks for artifacts, so it doesn't matter which machine produced them.
- Rough GPU time for 45 minutes of content on a T4: Demucs ~6–10 min, TransNetV2 ~3 min, SigLIP ~1 min, PANNs ~2 min.

---

## 13. Testing

- **Unit:** the subtitle formatter (grapheme counting, splitting, CPS), QC rules, ad scoring and selection, and scene-boundary merging, all on fixture data.
- **Golden clip:** a hand-annotated 3–5 minute clip covering scene boundaries, 3 entities (including one mentioned-only), 2 sound events and expected ad points. The pipeline output is diffed against it in CI.
- **Schema:** `SemanticTimeline.model_validate_json` runs on every output.
- **LLM regression:** cached responses make the tests deterministic; bust the cache only when a prompt changes.

---

## 14. Build plan

| Day / block | Deliverable |
|---|---|
| 1 | Repo skeleton, schemas, runner with caching, s01, and the Sarvam client; s05–s07 produce a clean diarized transcript |
| 2 | s15 subtitles + s17 QC. **First shippable output: SRT/VTT plus the QC report** |
| 3 | s02, s03, s09 (shots, keyframes, baseline vision), s10 scenes |
| 4 | s11, s12 (entities plus targeted vision), s13 semantics |
| 5 | s14 ad scoring, s18 assembly, and the API |
| 6 | Frontend: player, timeline lanes, scene panel, tabs |
| 7 | s08 + s16 (audio events, CC), polish, golden-clip tuning, recording a fallback demo video |

**Cut line if you're short on time:** drop s12 densification and use baseline tags only; drop pyannote and use Sarvam diarization only; drop search and inline subtitle editing. Do not cut the score breakdown UI or the presence classes, because they are the pitch.

---

## 15. Known limitations

- Speaker labels are anonymous clusters. Naming them from dialogue is a P2 heuristic.
- The narrative-intensity weights are hand-tuned on the golden clip, not learned.
- Brand detection depends on legibility at low detail. Small logos may only surface in the targeted pass.
- AudioSet classes are Western-centric: conch, dhaak and ululation (উলুধ্বনি) aren't well covered. Map the nearest classes, and add a few custom few-shot CLAP prompts as a P2.