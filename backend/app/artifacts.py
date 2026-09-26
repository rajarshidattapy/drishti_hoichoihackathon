from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from .settings import Settings


class ArtifactStore:
    def __init__(self, settings: Settings):
        self.settings = settings

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

