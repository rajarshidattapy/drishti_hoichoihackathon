# Hoichoi Drishti — Product Requirements Document

**Version:** 1.0 (hackathon build)
**Owner:** Paramarsh Labs
**Status:** Build-ready

---

## 1. Summary

Hoichoi Drishti turns a Bengali episode into a **Semantic Timeline**: a structured, time-indexed representation of what is shown, said, heard and meant, scene by scene. Two applications sit on top of it:

1. **Ad Intelligence** finds context-aware, low-disruption ad insertion points and product and topic opportunities, including products that are *mentioned but never shown*.
2. **Localization** produces Bengali subtitles (SRT/VTT), Bengali closed captions with sound events, and an automatic QC report.

It is not a subtitle generator or an ad model. It is one shared multimodal understanding layer with two consumers.

---

## 2. Problem

| Team | Today | Pain |
|---|---|---|
| Ad ops / ad sales | Mid-rolls placed at fixed intervals or by hand | Breaks interrupt emotional beats. There is no contextual inventory to sell ("smartphone moment at 21:42"). |
| Localization | Subtitles made manually or with generic ASR | Slow and expensive. Generic ASR handles Bengali punctuation, speaker turns and reading speed poorly. |
| Accessibility | Closed captions rarely produced for regional content | No `[দরজায় কড়া নাড়ার শব্দ]`-style sound cues. The content fails accessibility expectations. |
| QC | Full human watch-through | No way to jump straight to risky segments. |

---

## 3. Users

- **Ad ops manager:** wants a ranked list of break points with reasons, and contextual tags to sell against.
- **Localization editor:** wants ready subtitle files plus a short list of segments to review.
- **QC reviewer:** wants flagged timestamps and a one-click jump to each one.
- **Demo judge (hackathon):** wants to see the whole understanding pipeline and trust the scores.

---

## 4. Goals and non-goals

### Goals
- G1: Process an episode (up to 60 min) end to end into a single Semantic Timeline JSON.
- G2: Segment the episode into meaningful **scenes**, not just shots.
- G3: Detect entities from **both** dialogue and visuals, and classify each as mentioned-only, shown-only, mentioned-and-shown, or unverified.
- G4: Rank ad insertion candidates with a **transparent, decomposed score**.
- G5: Produce Bengali SRT/VTT subtitles and closed captions that follow standard timing and reading-speed rules.
- G6: Produce a QC report with timestamped issues.
- G7: Show all of the above in a simple web UI with a synced video player and timeline.

### Non-goals (this build)
- Real-time or live-stream processing.
- Face recognition that maps characters to actor identities.
- Actual ad serving or SSAI integration. The platform outputs recommendations and a cue-point export only.
- Translation into other languages. The architecture allows it later.
- Multi-tenant auth or permissions.

---

## 5. Core concept: the Semantic Timeline

Every episode becomes an ordered list of **scenes**. Each scene carries:

- **Time bounds** and the shots it contains.
- **Visual:** location, objects, activity, and visual mood from keyframes.
- **Audio:** speakers, utterances, sound events, music presence, and loudness energy.
- **Semantic:** summary, topics, mood, and narrative intensity (0–1).
- **Entities:** each with its source (dialogue, visual or both), visual presence, sentiment, confidence and timestamps.

Every downstream feature reads from this object. Nothing downstream re-analyzes the raw video.

---

## 6. Features and requirements

Priority: **P0** = must ship for the demo, **P1** = should ship, **P2** = stretch.

### F1. Upload and processing (P0)
- Upload an MP4/MKV, or register a local file path.
- Show pipeline progress per stage (queued, running, done, failed) with elapsed time.
- Stages are cached. Re-running skips completed stages, and a single stage can be re-run.
- **Acceptance:** a 3-minute clip completes in under 5 minutes. A failed stage shows its error and can be retried alone.

### F2. Transcript with speakers (P0)
- Bengali speech-to-text via Sarvam, with timestamps per utterance.
- Speaker diarization with stable labels (`SPK_A`, `SPK_B`, …).
- Punctuation and cleanup pass. The text keeps its original meaning, and code-mixed English words stay as spoken.
- Speakers can optionally be named from dialogue cues (P2), e.g. vocatives like "মিতা, …".
- **Acceptance:** every utterance has a start, end, speaker and text. Clicking an utterance seeks the player to it.

### F3. Shot detection and scene segmentation (P0)
- Detect shot boundaries.
- Merge shots into scenes using visual similarity, dialogue continuity, speaker changes, location changes and an LLM boundary check.
- Each scene gets a short title (e.g. "Restaurant conversation") and a 1–2 line summary.
- **Acceptance:** scenes cover the full duration with no gaps and no overlaps. The number of scenes is roughly 1 per 1–4 minutes of drama content.

### F4. Visual understanding (P0)
- **Baseline pass:** one deduplicated keyframe per shot is analyzed for location, objects, activity, visual mood and visible brands or products.
- **Targeted pass:** for every entity mentioned in dialogue, frames across the **enclosing scene** are sampled more densely and checked for whether that entity is visible.
- **Acceptance:** every scene has visual tags. Every dialogue entity has `visual_presence` set to `true`, `false` or `unverified`.

### F5. Entity and product-context intelligence (P0)
- Extract entities and topics from the transcript, including implicit references (e.g. "ফোনটা") and brands written in either English or Bengali script.
- Merge dialogue entities with visual entities per scene.
- Classify each entity as `mentioned_and_shown`, `mentioned_only`, `shown_only` or `unverified`.
- Attach sentiment (positive, neutral or negative), timestamps and confidence.
- Map entities to **ad categories** (e.g. Mobile, Food delivery, Fashion, Travel, Finance) using a configurable category list.
- **Acceptance:** an Entities view lists all entities, filterable by category and presence class. Each entity links to its timestamps.

### F6. Audio events (P1 for closed captions, P0 for scoring signals)
- Detect sound events (knock, rain, thunder, phone ring, door, laughter, crowd, music, …).
- Compute a loudness and music-energy curve over time.
- **Acceptance:** events are shown on the timeline, and those above threshold appear in the closed captions.

### F7. Scene semantics (P0)
- Scene mood and **narrative intensity** (0–1), built from the LLM judgment plus audio energy plus dialogue density.
- Flag cliffhanger or high-tension moments.

### F8. Ad opportunity scoring (P0)
- Candidate points: scene boundaries and long dialogue pauses inside low-intensity scenes.
- Each candidate gets a **decomposed score**: pause length, scene-end proximity, low intensity, context match, speech penalty and cliffhanger penalty.
- Output a ranked list with a plain-language reason, the matched ad categories, and the nearby entity context.
- Configurable settings: minimum gap between breaks (default 8 min), number of breaks wanted, and blocked zones such as the first and last 2 minutes.
- Export cue points as JSON and CSV.
- **Acceptance:** the UI shows the score breakdown for each candidate. The selected breaks respect the minimum gap.

### F9. Bengali subtitles (P0)
- Generate SRT and VTT from the diarized, cleaned transcript.
- Rules: at most 2 lines per cue, about 42 characters per line, about 17 characters per second maximum, cue duration 1–7 s, gap of at least 80 ms between cues, and line breaks at natural phrase boundaries.
- Speaker change inside a cue is marked with a leading dash.
- **Acceptance:** both files open in VLC and the browser player, and they are selectable on the UI's video player.

### F10. Bengali closed captions (P1)
- The subtitles plus bracketed Bengali sound-event cues, e.g. `[বৃষ্টির শব্দ]`, `[ফোন বেজে উঠছে]`.
- Music is marked as `[সঙ্গীত]` or with a mood variant (`[ভয়ঙ্কর সঙ্গীত]`).
- Output: `episode_bn_cc.srt` and `.vtt`.

### F11. Subtitle QC report (P1)
- Checks: low speech-to-text confidence, reading speed too high, lines too long, too many lines, overlapping speech, cues too short or too long, timing drift against VAD, and speaker ambiguity.
- Each issue has a severity (error, warn or info), a timestamp, a rule, a message and a suggested fix.
- **Acceptance:** clicking an issue seeks the player and highlights the cue.

### F12. Search (P2)
- Natural-language search over scenes and utterances ("phone conversation", "rain scene"), with results that jump to timestamps.

### F13. Structured export (P0)
- Download the full `semantic_timeline.json`, which validates against the published schema.
- Download individual outputs: SRT, VTT, CC, ad cue points, and the QC report.

---

## 7. UI requirements

This is a single web app with two screens. It is clean and dense, and intended as a working tool rather than marketing polish.

### Screen 1: Library
- Upload button with drag and drop.
- Episode list showing title, duration, status and a progress bar.

### Screen 2: Episode workspace

```
┌───────────────────────────────────────────────────────────────────────┐
│ Episode 102  ·  52:34  ·  ✓ Processed          [Search…]  [Export ▾] │
├───────────────────────────────────┬───────────────────────────────────┤
│                                   │  Scene 17 · Restaurant convo       │
│         VIDEO PLAYER              │  12:08 – 14:52                     │
│    (subtitle / CC track toggle)   │  Summary …                         │
│                                   │  Location · Activity · Mood        │
│                                   │  Intensity ▓▓▓░░░░ 0.31            │
│                                   │  Speakers: SPK_A, SPK_B            │
│                                   │  Entities: 📱 smartphone           │
│                                   │    mentioned_only · positive · 0.91│
├───────────────────────────────────┴───────────────────────────────────┤
│ TIMELINE (zoomable, synced playhead)                                  │
│ Scenes    │██ Family ██│██ Restaurant ██│█ Argument █│██ Street ██│    │
│ Speakers  │▬A▬ ▬B▬▬ ▬A▬│ ▬A▬▬ ▬B▬ ▬A▬   │▬A▬B▬A▬B▬A▬ │  ▬C▬       │    │
│ Entities  │            │   📱            │            │   ✈        │    │
│ Sounds    │  🚪        │                │  ⚡ 🌧      │            │    │
│ Intensity │~~~~___~~~~~│____~~___       │~~~^^^^^^~~~│~~___       │    │
│ Ads       │            │          ▼91   │            │   ▼84      │    │
├───────────────────────────────────────────────────────────────────────┤
│ [Scenes] [Transcript] [Entities] [Ads] [Subtitles] [QC ⚠3] [JSON]     │
│  tab content…                                                         │
└───────────────────────────────────────────────────────────────────────┘
```

**Tabs**
- **Scenes:** a table of scenes (time, title, location, mood, intensity, entities). Clicking a row seeks the player.
- **Transcript:** utterances grouped by scene, color-coded by speaker, with the current line highlighted during playback.
- **Entities:** grouped by ad category, with a presence-class badge, sentiment, and timestamp chips.
- **Ads:** a ranked candidate list. Each card shows the timestamp, total score, a score-breakdown bar, the reason, and the matched categories. A toggle marks candidates as selected. The ad settings live here too.
- **Subtitles:** a cue list with inline preview. Toggle between SRT and CC and download.
- **QC:** an issue list sorted by severity, which seeks the player on click.
- **JSON:** a collapsible tree viewer of the semantic timeline, with a copy/download button.

**Interaction rules**
- Everything with a timestamp is clickable and seeks the player.
- The playhead drives the scene panel on the right, which always shows the current scene.
- Timeline lanes can be toggled on and off.

---

## 8. Success metrics (demo-level)

| Metric | Target |
|---|---|
| End-to-end processing, 45-min episode | < 45 min on one T4 plus APIs |
| Scene boundary agreement with human judgment (sampled) | ≥ 80% |
| Mentioned-only entity precision (manual check on demo clip) | ≥ 85% |
| Subtitle cues violating reading-speed or line rules after formatting | < 5% |
| Top-3 ad candidates judged "non-disruptive" by a viewer | 3/3 on the demo episode |
| GPT cost per 45-min episode | Tracked and shown in the UI; target is low single-digit USD |

---

## 9. Scope by priority

- **P0:** F1, F2, F3, F4, F5, F7, F8, F9, F13, plus UI tabs Scenes, Transcript, Entities, Ads, Subtitles and JSON.
- **P1:** F6 (closed-caption events), F10, F11, plus the QC tab.
- **P2:** F12 search, speaker naming from dialogue, and translation hooks.

**Build order:** transcript and subtitles → shots, keyframes and scenes → entities and targeted vision → ad scoring → UI polish → closed captions and QC → search.

---

## 10. Demo script (≈4 min)

1. Open a pre-processed episode. Frame the timeline as "one understanding layer, two products."
2. Scrub the timeline and show the scene panel changing (location, mood, intensity).
3. **Key moment:** at the phone dialogue, show the entity marked *mentioned_only* (said, never shown) and open the frames that were checked.
4. Ads tab: show the top candidate, its score breakdown, and why it sits after the conversation ends rather than mid-argument.
5. Toggle CC on the player and show the sound cues in Bengali.
6. QC tab: click a warning and land on the flagged cue.
7. JSON tab: "everything you saw is this one schema; any downstream system can consume it."
8. Optional: live-process a 2-minute clip to show the pipeline actually runs.

---

## 11. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Music-heavy audio degrades speech-to-text | Separate vocals with Demucs before transcription, and mark low-confidence segments in QC |
| Diarization errors on overlapping speech | Mark overlaps in QC, and never let overlapping audio merge into a single cue |
| GPT vision cost on long episodes | Deduplicate keyframes, use low detail for the baseline pass, run targeted checks only on mentioned entities, and cache everything |
| "Not visible" false negatives | Check the whole enclosing scene, not a fixed window, and label weak checks `unverified` rather than `false` |
| Scene over- or under-segmentation | Combine signals with LLM boundary validation, and enforce a minimum scene length of 20 s |
| Live demo failure | Demo from a cached, fully processed episode, with the live run kept optional |