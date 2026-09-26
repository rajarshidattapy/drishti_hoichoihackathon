"""Durable copy of DATA_DIR in S3-compatible object storage (Cloudflare R2, S3, MinIO).

Hosts without a persistent disk (e.g. Render's free plan) wipe DATA_DIR on every restart. With
S3_BUCKET set, episode files are uploaded as they are produced and restored on demand, so the
database (episode status) and object storage (files) together survive restarts.
"""
from __future__ import annotations

from pathlib import Path
from typing import Protocol

from .settings import Settings


class Mirror(Protocol):
    def upload(self, key: str, path: Path) -> None: ...
    def download(self, key: str, path: Path) -> None: ...
    def list(self, prefix: str) -> dict[str, int]:
        """Object keys under prefix, mapped to their size in bytes."""
        ...
    def url(self, key: str) -> str:
        """A time-limited GET URL, so the browser can fetch large media directly."""
        ...


class S3Mirror:
    def __init__(self, settings: Settings):
        try:
            import boto3  # type: ignore[import-not-found]
            from botocore.config import Config  # type: ignore[import-not-found]
        except ImportError as exc:
            raise RuntimeError("S3_BUCKET is set but boto3 is not installed: pip install -e .") from exc
        self.bucket = settings.s3_bucket
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.s3_endpoint_url,
            aws_access_key_id=settings.s3_access_key_id,
            aws_secret_access_key=settings.s3_secret_access_key,
            region_name=settings.s3_region,
            # R2 rejects some of the newer default integrity checksums, so only send them when required.
            config=Config(
                signature_version="s3v4", retries={"max_attempts": 5, "mode": "standard"}, max_pool_connections=16,
                request_checksum_calculation="when_required", response_checksum_validation="when_required",
            ),
        )

    def upload(self, key: str, path: Path) -> None:
        self.client.upload_file(str(path), self.bucket, key)

    def download(self, key: str, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        temp = path.with_suffix(path.suffix + ".part")
        self.client.download_file(self.bucket, key, str(temp))
        temp.replace(path)

    def list(self, prefix: str) -> dict[str, int]:
        objects: dict[str, int] = {}
        for page in self.client.get_paginator("list_objects_v2").paginate(Bucket=self.bucket, Prefix=prefix):
            for item in page.get("Contents", []):
                objects[item["Key"]] = item["Size"]
        return objects

    def url(self, key: str) -> str:
        # Long enough to watch and seek through an episode without the link expiring.
        return self.client.generate_presigned_url("get_object", Params={"Bucket": self.bucket, "Key": key}, ExpiresIn=12 * 3600)


def mirror_from_settings(settings: Settings) -> Mirror | None:
    return S3Mirror(settings) if settings.s3_bucket else None
