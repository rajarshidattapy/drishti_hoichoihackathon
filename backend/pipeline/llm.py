from __future__ import annotations

import hashlib
import base64
import json
import time
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel

from app.artifacts import ArtifactStore
from app.settings import Settings
from .errors import ConfigurationError, PipelineError


SchemaT = TypeVar("SchemaT", bound=BaseModel)


class StructuredLLM:
    """Responses API wrapper with schema parsing, content cache, and usage log."""

    def __init__(self, settings: Settings, store: ArtifactStore, episode_id: str):
        self.settings = settings
        self.store = store
        self.episode_id = episode_id

    def available(self) -> bool:
        return bool(self.settings.openai_api_key)

    def call(
        self,
        *,
        model: str,
        system: str,
        user: str,
        schema: type[SchemaT],
        stage: str,
        max_retries: int = 2,
        images: list[Path] | None = None,
        image_detail: str = "low",
    ) -> SchemaT:
        if not self.settings.openai_api_key:
            raise ConfigurationError("OPENAI_API_KEY is missing.")
        try:
            from openai import OpenAI  # type: ignore[import-not-found]
        except ImportError as exc:
            raise ConfigurationError("OpenAI provider package is missing. Install with: pip install -e '.[providers]'") from exc

        image_hashes = [self.store.file_hash(path) for path in images or []]
        serialized = json.dumps({"model": model, "system": system, "user": user, "schema": schema.model_json_schema(), "images": image_hashes, "detail": image_detail}, ensure_ascii=False, sort_keys=True)
        key = hashlib.sha256(serialized.encode()).hexdigest()
        cache_path = self.store.episode_dir(self.episode_id) / "cache" / "llm" / f"{key}.json"
        if cache_path.exists():
            return schema.model_validate(self.store.read_json(cache_path))

        client = OpenAI(api_key=self.settings.openai_api_key)
        error: Exception | None = None
        started = time.perf_counter()
        for attempt in range(max_retries + 1):
            try:
                user_content: str | list[dict]
                if images:
                    user_content = [{"type": "input_text", "text": user}]
                    for path in images:
                        encoded = base64.b64encode(path.read_bytes()).decode("ascii")
                        media_type = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
                        user_content.append({"type": "input_image", "image_url": f"data:{media_type};base64,{encoded}", "detail": image_detail})
                else:
                    user_content = user
                response = client.responses.parse(
                    model=model,
                    input=[{"role": "system", "content": system}, {"role": "user", "content": user_content}],
                    text_format=schema,
                    temperature=0.1,
                )
                if response.output_parsed is None:
                    raise PipelineError("OpenAI returned no parsed structured output.")
                parsed = response.output_parsed
                self.store.write_json(cache_path, parsed)
                usage = getattr(response, "usage", None)
                self._log({
                    "stage": stage, "model": model, "cache_key": key, "latency_seconds": round(time.perf_counter() - started, 3),
                    "input_tokens": getattr(usage, "input_tokens", None), "output_tokens": getattr(usage, "output_tokens", None),
                    "attempt": attempt + 1,
                })
                return parsed
            except Exception as exc:
                error = exc
                if attempt < max_retries:
                    time.sleep(2 ** attempt)
        raise PipelineError(f"OpenAI structured output failed: {error}") from error

    def _log(self, record: dict) -> None:
        path = self.store.episode_dir(self.episode_id) / "logs" / "llm_calls.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
