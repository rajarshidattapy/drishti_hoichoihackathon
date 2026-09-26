"""Run pipeline stages from the command line, e.g. on a GPU box:

    python -m pipeline.run --episode ep-123 --stages s02,s03,s04,s08
    python -m pipeline.run --episode ep-123 --from s06 --force
    python -m pipeline.run --register path/to/video.mp4 --title "Episode 1"

The runner only looks at artifacts under DATA_DIR/episodes/{id}, so which machine
produced them doesn't matter: sync the folder back and the API resumes the rest.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path
from uuid import uuid4

from app.artifacts import ArtifactStore
from app.db import Database, EpisodeRecord
from app.settings import Settings
from pipeline.runner import STAGE_PAIRS, PipelineRunner


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m pipeline.run", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--episode", help="Existing episode id")
    target.add_argument("--register", metavar="VIDEO", help="Register a local video as a new episode, then run it")
    parser.add_argument("--title", help="Title for --register")
    parser.add_argument("--stages", help="Comma-separated stages to run (ids or prefixes, e.g. s02,s03)")
    parser.add_argument("--from", dest="from_stage", help="Restart from this stage and run everything downstream")
    parser.add_argument("--force", action="store_true", help="Recompute even when a cached artifact is valid")
    args = parser.parse_args(argv)

    settings = Settings()
    database = Database(settings)
    store = ArtifactStore(settings)
    episode_id = args.episode
    if args.register:
        source = Path(args.register).expanduser().resolve()
        if not source.is_file():
            parser.error(f"No such file: {source}")
        episode_id = f"ep-{uuid4().hex[:12]}"
        root = store.ensure_episode(episode_id)
        destination = root / f"source{source.suffix.lower()}"
        shutil.copy2(source, destination)
        database.create_episode(EpisodeRecord(id=episode_id, title=args.title or source.stem, source_path=str(destination)), STAGE_PAIRS)
        print(f"Registered {episode_id}")
    elif database.get_episode_record(episode_id) is None:
        parser.error(f"Unknown episode: {episode_id}")

    only = [value.strip() for value in args.stages.split(",") if value.strip()] if args.stages else None
    if args.from_stage and not only:
        from pipeline.runner import resolve_stage_id

        database.reset_from(episode_id, resolve_stage_id(args.from_stage))
    PipelineRunner(settings, database, store).run(episode_id, from_stage=args.from_stage, force=args.force, only=only)

    failed = [stage for stage in database.get_stages(episode_id) if stage.status == "failed"]
    for stage in database.get_stages(episode_id):
        marker = {"done": "ok", "failed": "FAIL", "running": ".."}.get(stage.status, "--")
        detail = f" {stage.elapsed:.1f}s" if stage.elapsed else ""
        print(f"  {marker:<4} {stage.stage_id:<24}{detail}{'  ' + stage.error if stage.error else ''}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
