from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from .errors import PipelineError


def run(command: list[str], *, timeout: int = 7200) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    except FileNotFoundError as exc:
        raise PipelineError(f"Required executable is unavailable: {command[0]}") from exc
    except subprocess.TimeoutExpired as exc:
        raise PipelineError(f"Media command timed out after {timeout} seconds") from exc
    if result.returncode:
        message = result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "unknown media error"
        raise PipelineError(f"{Path(command[0]).name} failed: {message}")
    return result


def probe(ffprobe: str, source: Path) -> dict:
    result = run([
        ffprobe, "-v", "error", "-show_entries",
        "format=duration,format_name:stream=index,codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate",
        "-of", "json", str(source),
    ], timeout=60)
    payload = json.loads(result.stdout)
    video = next((stream for stream in payload.get("streams", []) if stream.get("codec_type") == "video"), None)
    if video is None:
        raise PipelineError("The uploaded file has no video stream.")
    audio = next((stream for stream in payload.get("streams", []) if stream.get("codec_type") == "audio"), None)
    rate = video.get("avg_frame_rate") or video.get("r_frame_rate") or "0/1"
    numerator, denominator = (float(value) for value in rate.split("/"))
    return {
        "duration": float(payload.get("format", {}).get("duration") or 0),
        "fps": numerator / denominator if denominator else 0,
        "width": int(video.get("width") or 0),
        "height": int(video.get("height") or 0),
        "video_codec": video.get("codec_name"),
        "audio_codec": audio.get("codec_name") if audio else None,
        "format": payload.get("format", {}).get("format_name", ""),
        "has_audio": audio is not None,
    }


def detect_silences(ffmpeg: str, audio: Path, noise_db: int = -35, min_seconds: float = 0.3) -> list[dict[str, float]]:
    command = [ffmpeg, "-hide_banner", "-i", str(audio), "-af", f"silencedetect=noise={noise_db}dB:d={min_seconds}", "-f", "null", "-"]
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=7200)
    if result.returncode:
        raise PipelineError("ffmpeg could not analyze audio silence.")
    starts = [float(value) for value in re.findall(r"silence_start:\s*([0-9.]+)", result.stderr)]
    ends = [(float(end), float(duration)) for end, duration in re.findall(r"silence_end:\s*([0-9.]+)\s*\|\s*silence_duration:\s*([0-9.]+)", result.stderr)]
    return [{"start": start, "end": end, "duration": duration} for start, (end, duration) in zip(starts, ends)]

