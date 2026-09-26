# Drishti backend

The FastAPI service owns persistent episode metadata in SQLite and immutable/cached artifacts under `DATA_DIR/episodes/{id}`.

## Processing

`pipeline.runner.STAGES` defines the 18-stage DAG from the technical design. Every stage:

1. hashes its version and dependency artifacts;
2. skips a matching completed artifact;
3. writes JSON atomically;
4. persists running/done/failed state and elapsed time;
5. stops the episode on a safe, retryable error.

The local bounded worker is intentionally behind `PipelineCoordinator`; it can be replaced by RQ without changing the API or stage functions.

## Providers

- Sarvam Saaras v4 batch mode supplies Bengali transcription, chunk timestamps, and diarization.
- OpenAI Responses structured outputs supply grounded vision tags, entity extraction, targeted presence checks, and scene semantics when configured.
- Missing vision/LLM credentials produce conservative unknown/unverified values. Missing Sarvam credentials fail `s06_stt` because a transcript cannot be honestly fabricated.

## Tests

`python -m pytest tests -q` includes an actual generated MP4 through ffmpeg ingest and verifies the expected actionable provider failure.

