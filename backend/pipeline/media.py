from __future__ import annotations

import json
import re
import shutil
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


def probe(ffprobe: str, source: Path, ffmpeg: str = "ffmpeg") -> dict:
    """Read container/stream metadata. Falls back to parsing `ffmpeg -i` where ffprobe isn't installed."""
    if not shutil.which(ffprobe):
        return probe_with_ffmpeg(ffmpeg, source)
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


def probe_with_ffmpeg(ffmpeg: str, source: Path) -> dict:
    # `ffmpeg -i` with no output exits non-zero by design, so read stderr rather than the return code.
    try:
        result = subprocess.run([ffmpeg, "-hide_banner", "-i", str(source)], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
    except FileNotFoundError as exc:
        raise PipelineError(f"Required executable is unavailable: {ffmpeg}") from exc
    except subprocess.TimeoutExpired as exc:
        raise PipelineError("Media command timed out after 60 seconds") from exc
    info = result.stderr
    container = re.search(r"^Input #0, (.+?), from ", info, re.MULTILINE)
    if container is None:
        lines = info.strip().splitlines()
        raise PipelineError(f"ffmpeg could not read the video: {lines[-1] if lines else 'unknown media error'}")
    video = re.search(r"Stream #0:\d+.*?: Video: (\w+).*", info)
    if video is None:
        raise PipelineError("The uploaded file has no video stream.")
    audio = re.search(r"Stream #0:\d+.*?: Audio: (\w+)", info)
    duration = re.search(r"Duration: (\d+):(\d{2}):(\d{2}(?:\.\d+)?)", info)
    size = re.search(r", (\d{2,5})x(\d{2,5})", video.group(0))
    rate = re.search(r"([\d.]+)(k?) (?:fps|tbr)", video.group(0))
    return {
        "duration": int(duration[1]) * 3600 + int(duration[2]) * 60 + float(duration[3]) if duration else 0.0,
        "fps": float(rate[1]) * (1000 if rate[2] else 1) if rate else 0.0,
        "width": int(size[1]) if size else 0,
        "height": int(size[2]) if size else 0,
        "video_codec": video[1],
        "audio_codec": audio[1] if audio else None,
        "format": container[1],
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

