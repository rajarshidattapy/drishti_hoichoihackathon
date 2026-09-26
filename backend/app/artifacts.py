from __future__ import annotations

import hashlib
import json
import logging
import os
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path, PurePosixPath
from typing import Any

from pydantic import BaseModel

from .mirror import Mirror, mirror_from_settings
from .settings import Settings

logger = logging.getLogger(__name__)

# Large working media: restored only for pipeline runs; the API redirects the browser to storage instead.
MEDIA_DIRS = {"audio", "frames"}
MEDIA_PREFIXES = ("source.", "proxy.")
_DEFAULT = object()


class ArtifactStore:
    def __init__(self, settings: Settings, mirror: Mirror | None | object = _DEFAULT):
        self.settings = settings
        self.mirror: Mirror | None = mirror_from_settings(settings) if mirror is _DEFAULT else mirror  # type: ignore[assignment]
        self._synced: dict[str, tuple[int, int]] = {}  # object key -> (size, mtime_ns) last uploaded/downloaded
        self._hydrated: dict[str, bool] = {}  # episode id -> whether media was restored too
        self._locks: dict[str, threading.Lock] = {}
        self._locks_guard = threading.Lock()

    def episode_dir(self, episode_id: str) -> Path:
        return self.settings.episodes_dir / episode_id

    def ensure_episode(self, episode_id: str) -> Path:
        root = self.episode_dir(episode_id)
        for relative in ("audio/chunks", "frames", "stages", "outputs", "logs", "cache"):
            (root / relative).mkdir(parents=True, exist_ok=True)
        return root

    def stage_path(self, episode_id: str, stage_id: str) -> Path:
        return self.episode_dir(episode_id) / "stages" / f"{stage_id}.json"

    def source_url_path(self, episode_id: str) -> Path:
        return self.episode_dir(episode_id) / "source_url.txt"

    def output_path(self, episode_id: str, name: str) -> Path:
        return self.episode_dir(episode_id) / "outputs" / name

    def write_json(self, path: Path, value: BaseModel | dict | list) -> None:
        if isinstance(value, BaseModel):
            payload = value.model_dump(mode="json")
        else:
            payload = value
        self.write_text(path, json.dumps(payload, ensure_ascii=False, indent=2))

    def write_text(self, path: Path, value: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        temp = path.with_suffix(path.suffix + ".tmp")
        temp.write_text(value, encoding="utf-8")
        os.replace(temp, path)
        if self.mirror is not None and self._key(path) is not None:
            self._upload_if_changed(path)

    def read_json(self, path: Path) -> Any:
        return json.loads(path.read_text(encoding="utf-8"))

    def file_hash(self, path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def stage_input_hash(self, episode_id: str, stage_id: str, dependencies: list[str], version: str) -> str:
        digest = hashlib.sha256(f"{stage_id}:{version}".encode())
        for dependency in dependencies:
            path = self.stage_path(episode_id, dependency)
            if not path.exists():
                raise FileNotFoundError(f"Missing dependency artifact: {path.name}")
            digest.update(self.file_hash(path).encode())
        return digest.hexdigest()

    @staticmethod
    def safe_child(root: Path, name: str) -> Path:
        candidate = (root / name).resolve()
        resolved_root = root.resolve()
        if candidate != resolved_root and resolved_root not in candidate.parents:
            raise ValueError("Path leaves the episode directory")
        return candidate

    # ------------------------------------------------------------------ durable storage mirror

    def _lock(self, episode_id: str) -> threading.Lock:
        with self._locks_guard:
            return self._locks.setdefault(episode_id, threading.Lock())

    def _key(self, path: Path) -> str | None:
        """Object key for a file under DATA_DIR/episodes, or None for anything else."""
        try:
            relative = path.resolve().relative_to(self.settings.episodes_dir.resolve())
        except ValueError:
            return None
        return self.settings.s3_prefix + str(PurePosixPath("episodes", *relative.parts))

    def _episode_prefix(self, episode_id: str) -> str:
        return f"{self.settings.s3_prefix}episodes/{episode_id}/"

    @staticmethod
    def _is_media(relative: PurePosixPath) -> bool:
        return (len(relative.parts) > 1 and relative.parts[0] in MEDIA_DIRS) or relative.name.startswith(MEDIA_PREFIXES)

    def _upload_if_changed(self, path: Path) -> None:
        key = self._key(path)
        try:
            stat = path.stat()
            signature = (stat.st_size, stat.st_mtime_ns)
            if key is None or self._synced.get(key) == signature:
                return
            self.mirror.upload(key, path)  # type: ignore[union-attr]
            self._synced[key] = signature
        except FileNotFoundError:
            return
        except Exception:
            # Left out of _synced, so the next sync retries it.
            logger.exception("Uploading %s to storage failed", key)

    def sync(self, episode_id: str) -> None:
        """Upload every new or changed file in the episode folder (a no-op without storage)."""
        if self.mirror is None:
            return
        root = self.episode_dir(episode_id)
        if not root.is_dir():
            return
        with self._lock(episode_id):
            for path in sorted(root.rglob("*")):
                if path.is_file() and path.suffix not in {".tmp", ".part"}:
                    self._upload_if_changed(path)

    def hydrate(self, episode_id: str, *, media: bool = False) -> None:
        """Restore the episode folder from storage after a restart. Media only when `media` (pipeline runs)."""
        if self.mirror is None or self._hydrated.get(episode_id) is True or (not media and episode_id in self._hydrated):
            return
        with self._lock(episode_id):
            if self._hydrated.get(episode_id) is True or (not media and episode_id in self._hydrated):
                return
            prefix = self._episode_prefix(episode_id)
            root = self.episode_dir(episode_id)
            wanted: list[tuple[str, Path]] = []
            for key, size in self.mirror.list(prefix).items():
                relative = PurePosixPath(key[len(prefix):])
                if not relative.parts or (not media and self._is_media(relative)):
                    continue
                local = root.joinpath(*relative.parts)
                if not (local.is_file() and local.stat().st_size == size):
                    wanted.append((key, local))
                elif key not in self._synced:
                    stat = local.stat()
                    self._synced[key] = (stat.st_size, stat.st_mtime_ns)

            def fetch(item: tuple[str, Path]) -> None:
                key, local = item
                self.mirror.download(key, local)  # type: ignore[union-attr]
                stat = local.stat()
                self._synced[key] = (stat.st_size, stat.st_mtime_ns)

            with ThreadPoolExecutor(max_workers=8) as pool:
                list(pool.map(fetch, wanted))
            self._hydrated[episode_id] = media or self._hydrated.get(episode_id, False)

    def remote_url(self, episode_id: str, relative: str) -> str | None:
        """Signed URL for a file in storage, e.g. to redirect the browser to a video that isn't on local disk."""
        if self.mirror is None:
            return None
        return self.mirror.url(self._episode_prefix(episode_id) + PurePosixPath(relative).as_posix())
