# Drishti API: FastAPI + in-process pipeline worker. Build from backend/:
#   docker build -t drishti-api .
#   docker run -p 8000:8000 --env-file .env -v drishti-data:/data drishti-api
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DATA_DIR=/data \
    PORT=8000

# System ffmpeg provides both ffmpeg and ffprobe.
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies from pyproject first so code edits don't invalidate this layer.
COPY pyproject.toml .
RUN python -c "import tomllib; p = tomllib.load(open('pyproject.toml', 'rb'))['project']; extras = p['optional-dependencies']; print('\n'.join(p['dependencies'] + extras['providers'] + extras['media']))" > /tmp/requirements.txt \
    && pip install -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

COPY app ./app
COPY pipeline ./pipeline
COPY config ./config

# Episodes, uploads and (without DATABASE_URL) the SQLite database live in /data. Mount a
# persistent volume there (Render: a disk at /data); /health reports data_dir_mounted.
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import os, urllib.request; urllib.request.urlopen(f'http://127.0.0.1:{os.environ[\"PORT\"]}/health', timeout=4)"

# One process only: the job queue lives in memory, so extra workers wouldn't see each other's jobs.
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --proxy-headers --forwarded-allow-ips='*'"]
