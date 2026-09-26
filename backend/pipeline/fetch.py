"""Server-side download of YouTube / Google Drive videos. The result is handed to the normal pipeline."""
from __future__ import annotations

from pathlib import Path
from typing import Callable
from urllib.parse import urlparse

from .errors import PipelineError

ALLOWED_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be", "drive.google.com", "docs.google.com"}


def validate_url(url: str) -> str:
    parsed = urlparse(url.strip())
    if parsed.scheme not in {"http", "https"} or (parsed.hostname or "").lower() not in ALLOWED_HOSTS:
        raise ValueError("Paste a YouTube or Google Drive video link.")
    return url.strip()


def download(url: str, destination: Path, *, max_bytes: int, on_progress: Callable[[int], None]) -> tuple[Path, str]:
    """Download to destination/source.<ext> (≤720p MP4 when available). Returns (path, title)."""
    try:
        from yt_dlp import YoutubeDL  # type: ignore[import-not-found]
    except ImportError as exc:
        raise PipelineError("URL ingestion needs yt-dlp: pip install -e .") from exc

    def hook(status: dict) -> None:
        if status.get("status") == "downloading":
            total = status.get("total_bytes") or status.get("total_bytes_estimate")
            if total:
                on_progress(min(99, int(status.get("downloaded_bytes", 0) * 100 / total)))

    options = {
        "outtmpl": str(destination / "source.%(ext)s"),
        "format": "bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720][ext=mp4]/bv*[height<=720]+ba/b",
        "merge_output_format": "mp4",
        "noplaylist": True, "quiet": True, "no_warnings": True, "noprogress": True,
        "max_filesize": max_bytes, "progress_hooks": [hook],
    }
    try:
        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
    except Exception as exc:  # yt-dlp raises many unrelated types
        raise PipelineError(f"Could not download the video: {str(exc).splitlines()[0][:300]}") from exc
    files = [p for p in destination.glob("source.*") if p.suffix.lower() in {".mp4", ".mkv", ".webm", ".mov"}]
    if not files:
        raise PipelineError("The link did not produce a downloadable video file.")
    on_progress(100)
    return max(files, key=lambda p: p.stat().st_size), str((info or {}).get("title") or "Untitled video")
