from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .errors import ConfigurationError, PipelineError


class SarvamClient:
    """Current Saaras batch adapter with normalization into Drishti utterances.

    Batch mode is intentional: current Sarvam REST transcription is limited to
    short audio and does not provide speaker diarization.
    """

    def __init__(self, api_key: str | None):
        self.api_key = api_key

    def transcribe(self, audio_path: Path, output_dir: Path) -> tuple[list[dict], dict[str, Any]]:
        if not self.api_key:
            raise ConfigurationError(
                "SARVAM_API_KEY is missing. Add it to backend/.env, then rerun from s06."
            )
        try:
            from sarvamai import SarvamAI  # type: ignore[import-not-found]
        except ImportError as exc:
            raise ConfigurationError(
                "Sarvam provider package is missing. Install with: pip install -e '.[providers]'"
            ) from exc

        output_dir.mkdir(parents=True, exist_ok=True)
        client = SarvamAI(api_subscription_key=self.api_key)
        try:
            job = client.speech_to_text_job.create_job(
                model="saaras:v4",
                language_code="bn-IN",
                mode="codemix",
                with_diarization=True,
                with_timestamps=True,
            )
            job.upload_files(file_paths=[str(audio_path)])
            job.start()
            job.wait_until_complete()
            job.download_outputs(output_dir=str(output_dir))
        except Exception as exc:  # provider SDK error types are not stable
            raise PipelineError(f"Sarvam batch transcription failed: {exc}") from exc

        candidates = sorted(output_dir.rglob("*.json"), key=lambda path: path.stat().st_mtime, reverse=True)
        if not candidates:
            raise PipelineError("Sarvam completed but returned no JSON transcript.")
        raw = json.loads(candidates[0].read_text(encoding="utf-8"))
        return self.normalize(raw), raw

    @staticmethod
    def normalize(raw: dict[str, Any]) -> list[dict]:
        diarized = raw.get("diarized_transcript") or {}
        entries = diarized.get("entries") or diarized.get("segments") or diarized.get("utterances") or []
        utterances: list[dict] = []
        if entries:
            for index, entry in enumerate(entries):
                text = entry.get("transcript") or entry.get("text") or entry.get("content") or ""
                start = entry.get("start_time_seconds", entry.get("start", 0))
                end = entry.get("end_time_seconds", entry.get("end", start))
                speaker = entry.get("speaker_id") or entry.get("speaker") or entry.get("speaker_label") or "SPEAKER_00"
                utterances.append({
                    "utt_id": f"utt_{index + 1:05d}",
                    "start": float(start),
                    "end": float(end),
                    "speaker": SarvamClient._speaker_label(str(speaker)),
                    "speaker_name": None,
                    "text_raw": text.strip(),
                    "text": text.strip(),
                    "words": None,
                    "confidence": entry.get("confidence"),
                    "overlap": bool(entry.get("overlap", False)),
                })
            return utterances

        timestamps = raw.get("timestamps") or {}
        chunks = timestamps.get("chunks") or timestamps.get("words") or []
        starts = timestamps.get("start_time_seconds") or []
        ends = timestamps.get("end_time_seconds") or []
        for index, (text, start, end) in enumerate(zip(chunks, starts, ends)):
            utterances.append({
                "utt_id": f"utt_{index + 1:05d}", "start": float(start), "end": float(end),
                "speaker": "SPK_A", "speaker_name": None, "text_raw": str(text).strip(),
                "text": str(text).strip(), "words": None, "confidence": raw.get("language_probability"), "overlap": False,
            })
        if not utterances and raw.get("transcript"):
            utterances.append({
                "utt_id": "utt_00001", "start": 0.0, "end": 0.0, "speaker": "SPK_A",
                "speaker_name": None, "text_raw": raw["transcript"], "text": raw["transcript"],
                "words": None, "confidence": raw.get("language_probability"), "overlap": False,
            })
        return utterances

    @staticmethod
    def _speaker_label(value: str) -> str:
        digits = "".join(character for character in value if character.isdigit())
        index = int(digits or 0)
        return f"SPK_{chr(65 + min(index, 25))}"

