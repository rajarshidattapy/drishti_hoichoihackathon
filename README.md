# Hoichoi Drishti

Hoichoi Drishti turns a Bengali episode into one semantic timeline for ad intelligence, subtitles, closed captions, and QC. This repository contains a Next.js 16 interface and a FastAPI backend based on the product and technical specifications in [`docs/`](docs/).

The app includes a populated demo episode, so all workspace interactions are available without model credentials or a source video.

## Run locally

Requirements: Node.js 20.9+ and Python 3.11+.

Start the API:

```powershell
cd backend
python -m pip install -e ".[dev]"
python -m uvicorn app.main:app --reload --port 8000
```

In a second terminal, start the web app:

```powershell
cd frontend
npm install
Copy-Item .env.local.example .env.local
npm run dev
```

Open `http://localhost:3000`. FastAPI docs are at `http://localhost:8000/docs`.

## Included

- Episode library with drag-and-drop video upload and processing stages
- Synced player/demo playback, scene inspector, and zoomable semantic timeline
- Scenes, transcript, entities, ads, subtitles, QC, and JSON views
- Transparent ad-score components with configurable selection
- Bengali SRT/VTT and closed-caption downloads
- QC and timestamp navigation
- Timeline, cue-point, and QC exports
- FastAPI SSE progress stream and published Pydantic JSON Schema

The upload path uses a short simulated stage runner and attaches the demo semantic data until real artifacts are written. GPU/media/ASR/LLM pipeline stages described in `docs/technical.md` require their respective models, credentials, and worker infrastructure; the web/API contracts are ready for those outputs.

## Verify

```powershell
cd backend
python -m pytest tests -q

cd ..\frontend
npm run build
```

