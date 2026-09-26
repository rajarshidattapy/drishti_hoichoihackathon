# Drishti (built for the hoichoi hackathon)

Drishti turns a Bengali episode into one semantic timeline for ad intelligence, subtitles, closed captions, and QC. This repository contains a Next.js 16 interface and a FastAPI backend based on the product and technical specifications in [`docs/`](docs/).

<img width="1919" height="1105" alt="image" src="data/image.png" />


The app includes a populated demo episode, so all workspace interactions are available without model credentials or a source video.

## Run locally

Requirements: Node.js 20.9+ and Python 3.11+.

Start the API:

```powershell
cd backend
python -m pip install -e ".[dev,media]"
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

- Paste a YouTube or Google Drive link to download and process it through the same pipeline as uploads
- Episode pages open while processing and fill in as stages finish
- Ad decisions: hard constraints → safety → pacing → brand safety → brand fit, driven by `docs/brands.json`; "no break" when nothing qualifies
- VMAP manifest with inline VAST; the player plays the selected ad and resumes the episode; debug JSON under Export

- Episode library with drag-and-drop video upload and processing stages
- Synced player/demo playback, scene inspector, and zoomable semantic timeline
- Scenes, transcript, entities, ads, subtitles, QC, and JSON views
- Transparent ad-score components with configurable selection
- Bengali SRT/VTT and closed-caption downloads
- QC and timestamp navigation
- Timeline, cue-point, and QC exports
- FastAPI SSE progress stream and published Pydantic JSON Schema

Uploaded episodes run through a persistent, cached 18-stage pipeline. Install provider adapters and configure credentials for live Bengali diarization and multimodal understanding:

```powershell
cd backend
python -m pip install -e ".[providers]"
Copy-Item .env.example .env
# Set SARVAM_API_KEY and OPENAI_API_KEY in .env
```

Without `SARVAM_API_KEY`, a real upload stops at `s06_stt` with a retryable stage error; it never receives demo output. Stages before that point—including media probing, proxying, shot detection, keyframes, audio preparation, and VAD—remain cached. Add the key and call `POST /episodes/{id}/rerun` with `{"from_stage":"s06_stt","force":false}`.

The bundled demo is seeded as a separate processed episode. Local models from `docs/technical.md` (PySceneDetect, Silero VAD, PANNs audio events, SigLIP, Demucs) are used automatically when the `gpu` extra is installed (`pip install -e ".[gpu]"`); otherwise ffmpeg-based fallbacks run and the timeline records which method produced each artifact. Heavy stages can run on a separate GPU machine with `python -m pipeline.run --episode <id> --stages s02,s03,s04,s08`; see [`backend/README.md`](backend/README.md).

To run the UI with no backend at all, set `NEXT_PUBLIC_USE_MOCK=true` in `frontend/.env.local`.

## Deploy to Vercel

Deploy this repository as two Vercel projects. This keeps the Next.js and FastAPI runtimes isolated while they can both use Vercel:

1. Create the web project with **Root Directory** `frontend`. Vercel uses `frontend/vercel.json`, `npm ci`, and `npm run build`.
2. Create the API project from the same repository with **Root Directory** `backend`. The committed `backend/vercel.json` and `pyproject.toml` expose `app.main:app` as a FastAPI function on Python 3.12.
3. Set these web-project environment variables for Production, Preview, and Development:
   - `NEXT_PUBLIC_API_URL`: the public HTTPS origin of the API project, without a trailing slash.
   - `NEXT_PUBLIC_USE_MOCK=false`
4. Set `CORS_ORIGINS` on the API project to a comma-separated list containing the web production URL and any preview URL(s) that should access it.

On Vercel, the API automatically uses `/tmp/drishti` for its writable demo seed. That filesystem and the bundled SQLite database are ephemeral, so the deployed FastAPI function supports the seeded demo and read APIs but is not a durable video-processing service. For real upload/processing, add durable object storage, a managed database, and a queue/worker service with FFmpeg before enabling those routes.

For a frontend-only interactive demo, set `NEXT_PUBLIC_USE_MOCK=true`; no API deployment or `NEXT_PUBLIC_API_URL` value is required. These `NEXT_PUBLIC_*` variables are embedded during the build, so redeploy after changing them.

## Verify

```powershell
cd backend
python -m pytest tests -q

cd ..\frontend
npm run build
```
