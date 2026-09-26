from __future__ import annotations

import base64
import hashlib
import json
import threading
import time
from pathlib import Path
from string import Template
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from app.artifacts import ArtifactStore
from app.settings import Settings
from .errors import ConfigurationError, PipelineError


SchemaT = TypeVar("SchemaT", bound=BaseModel)

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"

# USD per 1M tokens (input, output). Unknown models fall back to the gpt-4.1 rate so estimates err high.
PRICING: dict[str, tuple[float, float]] = {
    "gpt-4.1": (2.00, 8.00),
    "gpt-4.1-mini": (0.40, 1.60),
    "gpt-4.1-nano": (0.10, 0.40),
    "gpt-4o": (2.50, 10.00),
    "gpt-4o-mini": (0.15, 0.60),
}
IMAGE_TOKENS = {"low": 85, "high": 765, "auto": 765}
ESTIMATED_OUTPUT_TOKENS = 800


class BudgetExceededError(PipelineError):
    pass


def load_prompt(name: str, **values: object) -> str:
    """Prompts live in pipeline/prompts/*.md and are versioned by filename."""
    text = (PROMPTS_DIR / f"{name}.md").read_text(encoding="utf-8")
    return Template(text).safe_substitute({key: str(value) for key, value in values.items()}).strip()


def price(model: str) -> tuple[float, float]:
    for prefix in sorted(PRICING, key=len, reverse=True):
        if model == prefix or model.startswith(prefix + "-20"):
            return PRICING[prefix]
    return PRICING["gpt-4.1"]


def cost_usd(model: str, input_tokens: int, output_tokens: int) -> float:
    rate_in, rate_out = price(model)
    return (input_tokens * rate_in + output_tokens * rate_out) / 1_000_000


def logged_cost(path: Path) -> float:
    if not path.exists():
        return 0.0
    total = 0.0
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            total += float(json.loads(line).get("cost_usd") or 0)
        except (ValueError, json.JSONDecodeError):
            continue
    return total


class StructuredLLM:
    """Responses API wrapper with schema parsing, content cache, usage/cost log and budget guardrail."""

    _semaphores: dict[str, threading.BoundedSemaphore] = {}
    _semaphore_lock = threading.Lock()
    _log_lock = threading.Lock()

    def __init__(self, settings: Settings, store: ArtifactStore, episode_id: str):
        self.settings = settings
        self.store = store
        self.episode_id = episode_id

    @property
    def log_path(self) -> Path:
        return self.store.episode_dir(self.episode_id) / "logs" / "llm_calls.jsonl"

    def available(self) -> bool:
        return bool(self.settings.openai_api_key)

    def spent(self) -> float:
        return logged_cost(self.log_path)

    @classmethod
    def _semaphore(cls, kind: str, size: int) -> threading.BoundedSemaphore:
        with cls._semaphore_lock:
            if kind not in cls._semaphores:
                cls._semaphores[kind] = threading.BoundedSemaphore(max(1, size))
            return cls._semaphores[kind]

    def estimate(self, model: str, system: str, user: str, images: int, detail: str) -> float:
        # ~4 characters per token for English; Bengali tokenizes denser, so use 2.
        text_tokens = len(system) // 4 + len(user) // 2
        return cost_usd(model, text_tokens + images * IMAGE_TOKENS.get(detail, 765), ESTIMATED_OUTPUT_TOKENS)

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
        temperature: float = 0.1,
    ) -> SchemaT:
        if not self.settings.openai_api_key:
            raise ConfigurationError("OPENAI_API_KEY is missing.")

        image_hashes = [self.store.file_hash(path) for path in images or []]
        serialized = json.dumps({"model": model, "system": system, "user": user, "schema": schema.model_json_schema(), "images": image_hashes, "detail": image_detail}, ensure_ascii=False, sort_keys=True)
        key = hashlib.sha256(serialized.encode()).hexdigest()
        cache_path = self.store.episode_dir(self.episode_id) / "cache" / "llm" / f"{key}.json"
        if cache_path.exists():
            return schema.model_validate(self.store.read_json(cache_path))

        budget = self.settings.max_llm_usd_per_episode
        estimate = self.estimate(model, system, user, len(images or []), image_detail)
        spent = self.spent()
        if spent + estimate > budget:
            raise BudgetExceededError(
                f"LLM budget exhausted: ${spent:.2f} spent, next call ~${estimate:.3f}, limit ${budget:.2f} "
                "(MAX_LLM_USD_PER_EPISODE). Raise the limit and rerun this stage."
            )

        try:
            from openai import OpenAI  # type: ignore[import-not-found]
        except ImportError as exc:
            raise ConfigurationError("OpenAI provider package is missing. Install with: pip install -e '.[providers]'") from exc

        client = OpenAI(api_key=self.settings.openai_api_key)
        kind = "vision" if images else "text"
        semaphore = self._semaphore(kind, self.settings.llm_vision_concurrency if images else self.settings.llm_text_concurrency)
        encoded_images = []
        for path in images or []:
            media_type = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
            encoded_images.append({"type": "input_image", "image_url": f"data:{media_type};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}", "detail": image_detail})

        error: Exception | None = None
        feedback = ""
        started = time.perf_counter()
        for attempt in range(max_retries + 1):
            prompt = user + feedback
            user_content: str | list[dict] = [{"type": "input_text", "text": prompt}, *encoded_images] if encoded_images else prompt
            try:
                with semaphore:
                    response = client.responses.parse(
                        model=model,
                        input=[{"role": "system", "content": system}, {"role": "user", "content": user_content}],
                        text_format=schema,
                        temperature=temperature,
                    )
                usage = getattr(response, "usage", None)
                input_tokens = int(getattr(usage, "input_tokens", 0) or 0)
                output_tokens = int(getattr(usage, "output_tokens", 0) or 0)
                self._log({
                    "stage": stage, "model": model, "cache_key": key, "prompt_hash": hashlib.sha256((system + prompt).encode()).hexdigest()[:16],
                    "latency_seconds": round(time.perf_counter() - started, 3), "input_tokens": input_tokens,
                    "output_tokens": output_tokens, "cost_usd": round(cost_usd(model, input_tokens, output_tokens), 6),
                    "attempt": attempt + 1, "images": len(encoded_images),
                })
                if response.output_parsed is None:
                    raise PipelineError("OpenAI returned no parsed structured output.")
                parsed = schema.model_validate(response.output_parsed.model_dump())
                self.store.write_json(cache_path, parsed)
                return parsed
            except (ValidationError, PipelineError) as exc:
                # Feed the validation error back so the model can correct itself.
                error = exc
                feedback = f"\n\nYour previous answer was invalid: {str(exc)[:500]}. Return output that matches the schema exactly."
            except Exception as exc:
                error = exc
                status = getattr(exc, "status_code", None)
                if status and status not in (408, 409, 429) and status < 500:
                    break
                if attempt < max_retries:
                    time.sleep(2 ** (attempt + 1) if status == 429 else 2 ** attempt)
        raise PipelineError(f"OpenAI structured output failed for {stage}: {error}") from error

    def _log(self, record: dict) -> None:
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self._log_lock, self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
