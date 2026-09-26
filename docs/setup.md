Everything is installed and working. I started the API and checked the demo episode, its timeline and ad breaks, and the browser access rule for localhost:3000. Earlier, all 20 backend tests passed and the frontend production build succeeded. Ports 8000 and 3000 are free.

What I set up:
- Installed the backend with its test, image and provider packages. Before this, the Sarvam package was missing, so real uploads would have failed.
- Created backend/.env from the example file.

Following YAGNI, I left out the optional GPU packages. The ffmpeg fallbacks cover everything without them, and you can add them later with pip install -e ".[gpu]".

Run it in two terminals:
cd backend; python -m uvicorn app.main:app --reload --port 8000
cd frontend; npm run dev
Then open http://localhost:3000.

Two things you need to decide:
1. frontend/.env.local has NEXT_PUBLIC_USE_MOCK=true, so the UI uses the mock data and ignores the backend. Set it to false to use the real API, and restart npm run dev after changing it.
2. API keys: backend/.env has empty SARVAM_API_KEY and OPENAI_API_KEY. The demo episode works without them.
   - Without the Sarvam key, a real upload stops at the transcription stage (s06) with a clear error. After you add the key, rerun that episode from s06 and it picks up from there.
   - Without the OpenAI key, uploads still finish, but vision tags come back as "unknown", entities as "unverified", and scene titles are generic.