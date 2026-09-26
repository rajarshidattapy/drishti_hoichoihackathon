# Drishti backend

The FastAPI service owns persistent episode metadata in SQLite and immutable/cached artifacts under `DATA_DIR/episodes/{id}`.

## Processing

`pipeline.runner.STAGES` defines the 18-stage DAG from `docs/technical.md`. The runner executes it with `STAGE_PARALLELISM` workers, so the video branch (s02, s03, s09) and the audio branch (s04–s08) run side by side until s10. Every stage:

1. hashes its version, its dependency artifacts and the `Thresholds` config;
2. skips a matching completed artifact (logged as `stage_cached`);
3. writes JSON atomically;
4. persists running/done/failed state and elapsed time;
5. stops the episode on a safe, retryable error.

The local bounded worker is intentionally behind `PipelineCoordinator`; it can be replaced by RQ without changing the API or stage functions.

| Stage | Implementation | Optional upgrade |
|---|---|---|
| s01 ingest | ffprobe + 720p H.264 proxy | |
| s02 shots | ffmpeg scene filter, short shots merged | PySceneDetect `AdaptiveDetector` |
| s03 keyframes | midpoint frame (+75% frame for shots > 8 s), dHash + mean-colour dedup over the previous 10 shots | SigLIP embeddings (`FRAME_EMBEDDER=siglip`), saved to `stages/embeddings.npy` |
| s04 audio prep | 16 kHz mono WAV | Demucs vocals (10-min segments for episodes > 30 min) |
| s05 VAD | ffmpeg `silencedetect`, STT chunks | Silero VAD |
| s06 STT | Sarvam Saaras v4 batch with diarization; overlap marking; raw response kept in `stages/s06_raw.json` and re-parsed on rerun | |
| s07 cleanup | LLM punctuation restore in batches of 40 (+5 context), rejected when edit distance > 25% | |
| s08 audio | 1 Hz RMS loudness | PANNs Cnn14 events (whitelist in `config/sound_labels_bn.yaml`) and music ratio |
| s09 vision | OpenAI low-detail tags, 4 keyframes per call; dedup shots inherit tags | |
| s10 scenes | weighted boundary score (visual, location, speakers, silence), 20 s minimum, LLM merge/keep validation | |
| s11 entities | grounded LLM extraction per scene (every mention must cite a `utt_id`); keyword baseline without a key | |
| s12 verification | baseline-tag pre-check, 1 fps window sampling, timestamped frame strips, presence verdicts; shown-only entities | |
| s13 semantics | LLM title/summary/mood + fused intensity (0.55 LLM, 0.25 audio p10–p90, 0.20 dialogue density), 5 s smoothed curve | |
| s14 ads | documented score formula, snap to silence, blocked zones, cliffhanger protection, template reasons | |
| s15 subtitles | grapheme-aware formatter, CPS extension into silence, `- ` speaker-change cues | |
| s16 captions | sound cues merged / shifted ±1.5 s / dropped, `[… সঙ্গীত]` music cues | |
| s17 QC | all nine documented rules + pass/fail summary | |
| s18 assemble | validated `SemanticTimeline`, cue points JSON/CSV, per-stage timing and LLM cost | |

All thresholds live in `app.settings.Thresholds` and are recorded in `processing.thresholds`.

## Providers

- Sarvam Saaras v4 batch mode supplies Bengali transcription, chunk timestamps, and diarization.
- OpenAI Responses structured outputs supply transcript cleanup, vision tags, scene validation, entity extraction, targeted presence checks, and scene semantics. Prompts are versioned files in `pipeline/prompts/`. Calls are cached by content hash in `cache/llm/`, logged with tokens and cost to `logs/llm_calls.jsonl`, and refused once `MAX_LLM_USD_PER_EPISODE` would be exceeded.
- Missing vision/LLM credentials produce conservative unknown/unverified values. Missing Sarvam credentials fail `s06_stt` because a transcript cannot be honestly fabricated.

```powershell
python -m pip install -e ".[providers]"   # Sarvam + OpenAI
python -m pip install -e ".[gpu]"         # PySceneDetect, Silero, PANNs, SigLIP, Demucs
```

## GPU box workflow

Heavy stages can run elsewhere; the runner only checks artifacts:

```powershell
python -m pipeline.run --register path\to\episode.mp4 --title "Episode 1"
python -m pipeline.run --episode ep-123 --stages s02,s03,s04,s08 --force
python -m pipeline.run --episode ep-123 --from s06
```

Sync `data/episodes/ep-123/` back and the API worker resumes the remaining stages on startup.

## Tests

`python -m pytest tests -q` covers the formatter, QC rules, captions, scene boundaries, ad scoring, the LLM budget guardrail, and two end-to-end runs of all 18 stages on a generated MP4 (Sarvam stubbed; one run with a stubbed structured-output LLM to check grounding and presence verdicts).
