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
        return mark_overlaps(SarvamClient._normalize(raw))

    @staticmethod
    def _normalize(raw: dict[str, Any]) -> list[dict]:
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
                    "words": _words(entry.get("words")),
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


def _words(value: Any) -> list[dict] | None:
    if not isinstance(value, list):
        return None
    words = []
    for item in value:
        if not isinstance(item, dict):
            continue
        text = item.get("word") or item.get("text")
        start = item.get("start_time_seconds", item.get("start"))
        end = item.get("end_time_seconds", item.get("end"))
        if text is not None and start is not None and end is not None:
            words.append({"text": str(text), "start": float(start), "end": float(end)})
    return words or None


def mark_overlaps(utterances: list[dict], min_overlap: float = .3) -> list[dict]:
    """Flag utterances overlapped by another speaker's turn for more than `min_overlap` seconds."""
    ordered = sorted(utterances, key=lambda item: item["start"])
    for index, current in enumerate(ordered):
        for other in ordered[index + 1:]:
            if other["start"] >= current["end"]:
                break
            if other["speaker"] == current["speaker"]:
                continue
            if min(current["end"], other["end"]) - other["start"] > min_overlap:
                current["overlap"] = other["overlap"] = True
    return ordered

