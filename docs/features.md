Improve the existing Hoichoi Drishti MVP without changing the core UI unnecessarily.

1. **Ad decision pipeline**
   - Enforce the hierarchy: hard constraints → eliminate invalid candidates → boundary safety scoring → pacing/ad-load constraints → hard negative-context brand filtering → contextual brand ranking.
   - Allow **"no break"** when no candidate satisfies the constraints.
   - Brand matching must be catalogue-driven using structured metadata (`category`, `preferred_contexts`, `negative_contexts`) and must generalise to unseen brands with zero code changes.
   - Ensure no hard-coded timestamps, scenes, or brand assignments.
   - Improve semantic scene segmentation using dialogue, characters, activity, location and narrative context—not just shot boundaries.

2. **Progressive episode route**
   - Keep `/episode/{episode_number}` accessible immediately while processing is ongoing.
   - Stream/update results progressively as they become available instead of waiting for the entire pipeline to finish.
   - Show believable processing states and incrementally populate the timeline, transcript, scenes, ad candidates, etc., so the platform feels fast and responsive.

3. **URL ingestion**
   - Add a simple UI where users can paste a **Google Drive or YouTube video URL**.
   - Download/fetch the video server-side, then send it through the exact same processing pipeline as uploaded files.
   - Show download → processing → completion status.
   - Do not create a separate processing path for URL inputs.

4. **Demo reliability**
   - Preserve the existing playable demo.
   - Ensure the generated VMAP manifest actually inserts the selected ad and resumes the episode.
   - Keep debug JSON available for judges to inspect decisions and scores.