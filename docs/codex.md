# Codex conversation

## User

hi

## Assistant

Hi! What would you like to work on?

## User

read docs and make the app - next.js UI, fastapi backend

## Assistant

I’m using the frontend-design skill because this includes building a Next.js interface. I’ll first read its guidance and inventory the project docs, then implement and verify both the UI and FastAPI API.

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -Raw 'C:\\Users\\asus\\.codex\\plugins\\cache\\claude-plugins-official\\frontend-design\\local\\skills\\frontend-design\\SKILL.md'"
    status: Completed · exit 0
      ---
      name: frontend-design
      description: Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps with aesthetic direction, typography, and making choices that don't read as templated defaults.
      license: Complete terms in LICENSE.txt
      ---
      
      # Frontend Design
      
      Approach this as the design lead at a design studio known for giving every client a distinct visual identity that is not mistaken for anyone else's. This client has already rejected proposals that felt clichÃ© or templated, and is paying for a distinctive point of view: make deliberate, opinionated choices about palette, typography, and layout that are specific to this brief, and take aesthetic risk if justified.
      
      ## Ground your designs in the subject matter
      
      If the brief does not identify what the product or subject matter is, identify it yourself before designing, and confirm with the client. You can come up with one concrete subject, the design's audience, and the design's primary job, as a proposal. If there's any information in your memory about the client's preferences or context about what they're building, use that as a hint. The subject's industry, subject matter, materials, and vernacular are where distinctive visual choices come from â€” a design for a toy for girls aged 8â€“11 will be very aesthetically different from a dashboard for financial analysts. Build with the brief's real content and subject matter throughout.
      
      ## Design principles
      
      For web designs, the hero is the first thing viewers will see. Open with the most characteristic thing in the subject's world, in the form that is most appropriate: a headline, an image, an animation, a live demo, an interactive moment, or other treatments. Be deliberate with your choice: a big number with a small label, supporting stats, and a gradient accent is the default treatment, so only use it if that's truly the best option.
      
      Typography carries the personality of the page. You don't need a different typeface for display or headline text and body content: use one family or two, and if two, make them clearly distinct.
      
      Choose your typefaces deliberately, not the default families you would reach for on any other project, and set a clear type scale following the default guidance of The Elements of Typographic Style with intentional weights, widths, and spacing. When type is used as a headline or visual element, use the type treatment itself as an active part of the design, not a neutral delivery vehicle for the content.
      
      Default to line lengths of less than 80 characters. Serif typefaces can have slightly longer line lengths; give serif body text slightly more line-height than a sans-serif.
      
      Avoid these default typographic treatments; they are the commonest tells of a generated page:
      - Accenting just a single word or phrase in a headline, like putting one word in italic/bold or a different color.
      - Using all caps for labels.
      - Adding unnecessary typographic labels above content.
      
      Visual structure is information. Structural devices like outlines, borders, numbering, eyebrows, dividers, labels, etc., encode useful information about the content rather than decorate it. Many generic designs use numbered markers (01 / 02 / 03), but that's only appropriate if the content actually is a sequence â€” like a stepped process or a timeline. Before adding numbered markers, check the content really is a sequence.
      
      Use non-user-triggered motion sparingly and deliberately, only to draw attention. A single orchestrated moment â€” one page-load sequence or one reveal â€” lands better than scattered effects; fade-and-slide-up entrances on each section and hover transitions on every card are the generic default and read as AI-generated. Motion that answers a person's action (opening, expanding, confirming) is welcome when it shows what changed.
      
      Consider written content carefully. Often a design brief may not contain real content, and it's up to you to come up with copy and placeholder content. Copy can make a design feel as templated as the design itself. See the below section on writing for more guidance.
      
      ## Process: plan, review against the brief, build, critique
      
      For calibration, AI-generated design right now clusters around some traits:
      1. a warm cream background (near #F4F1EA) with a high-contrast serif display and a terracotta or warm-clay accent (often near #D97757 â€” Anthropic's own Claude-interaction accent, so on a user's brief it reads as a tell);
      2. a near-black background with a single bright acid-green or vermilion accent;
      3. a broadsheet-style layout with hairline rules, zero border-radius, and dense newspaper-like columns;
      4. the SaaS-card kit: content chopped into identical rounded cards, one border-radius on everything regardless of hierarchy, the same soft grey shadow (rgba(0,0,0,.1)) under each, and gradient washes as decoration;
      5. template chrome that appears whatever the subject: a tracked-out ALL-CAPS eyebrow label above every heading; meta strings joined with middle dots ('A Â· B Â· C'); labels built as 'WORD â€” fragment' with a spaced em dash; tinted near-black (#0B0B0B, #111) standing in for black; a monospace face for small data labels; a 'â†’' appended to link and button text.
      
      All traits are legitimate for some briefs, but they are defaults rather than choices, and they appear regardless of subject. Where the brief pins down a visual direction, follow it exactly â€” the brief's own words always win, including when it asks for one of these looks. Where it leaves an axis free, don't spend that freedom on one of these defaults. As with a hired human designer, there's often a careful balance between doing what you're good at and taking each project as a chance to experiment and learn.
      
      Work in two passes. First, brainstorm a short design plan based on the client's design brief: create a compact token system with color, type, layout, and principles.
      - Color: describe the core base palette as 4â€“6 named hex values.
      - Type: the typefaces and their roles.
      - Layout: a layout concept, using one-sentence prose descriptions and ASCII wireframes to ideate and compare. Include alignment guidance; should the content be left aligned, center aligned, justified?
      - Principles: the high-level guidance for what makes this page unique.
      
      Then review that plan against the brief before building: if any part of it reads like the generic default you would produce for any similar page (work through a similar prompt to see if you arrive somewhere similar) rather than a choice made for this specific brief â€” revise that part, say what you changed and why. Only after you've confirmed the relative uniqueness of your design plan should you start to write the code, following the revised plan.
      
      When writing the code, be careful of structuring your CSS selector specificities. It's easy to generate CSS classes that cancel each other out (especially with a type-based selector like .section and an element-based selector like .cta). This can happen often with padding/margin between sections.
      
      ## Restraint and self-critique
      
      Spend your boldness in one place. Let one element be the memorable thing, keep everything around it quiet and disciplined, and cut any decoration that does not serve the brief. Build to a quality floor without announcing it: responsive down to mobile, visible keyboard focus, reduced motion respected, visually accessible, harmonious color palettes. Critique your own work as you build, taking screenshots to review if your environment supports it â€” a picture is worth 1000 tokens. Consider Chanel's advice: before leaving the house, take a look in the mirror and remove one accessory. Human creatives have memory and always try to do something new, so if you have a space to quickly jot down notes about what you've tried, it can help you in future passes.
      
      ## More on writing in design
      
      Words appear in a design for one reason: to make it easier to understand and use. They are design content, not decoration. Bring the same intentionality and minimalism to copywriting that you would bring to spacing and color. Before writing anything, ask what the design needs to say, and how it can best be said to help the person navigate the experience.
      
      Write from the end user's perspective. Name things by what users will understand in simple language, not by how the system is built. A user manages notifications, not webhook config. Describe what something is or does in plain terms rather than selling it. Being specific and legible to new users is always better than being clever.
      
      Use active voice as default. A CTA says exactly what happens when it is used: "Save changes," not "Submit." An action keeps the same name through the whole flow, so the button that says "Publish" produces a toast that says "Published." The vocabulary of an interface is the signposting for someone navigating the product. Cohesion and consistency are how people learn their way around.
      
      Treat failure and emptiness as moments for direction, not mood. Explain what went wrong and how to fix it, in the interface's voice rather than a person's. Errors don't apologize, and they are never vague about what happened. An empty screen is an invitation to act.
      
      Keep the tone conversational: plain verbs, sentence case, no filler, with tone matched to the brand and the audience. Let each written element do exactly one job.
      

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-ChildItem -Force | Select-Object Mode,Length,LastWriteTime,Name; rg --files -g '"'!node_modules'"' -g '"'!/.git'"' -g '"'!dist'"' -g '"'!build'"'"
    status: Completed · exit 0
      
      docs\technical.md
      docs\prd.md
      Mode   Length LastWriteTime       Name
      ----   ------ -------------       ----
      d--h--        26-09-2026 13:10:17 .git
      d-----        26-09-2026 13:37:26 docs
      
      

## Assistant

The repository currently contains only the product and technical specifications, so this is a clean build rather than an extension. I’m reading both documents now and will use their actual domain and workflows to set the visual direction before scaffolding.

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -Raw 'docs\\prd.md'; Get-Content -Raw 'docs\\technical.md'; git status --short"
    status: Completed · exit 0
      # Hoichoi Drishti â€” Product Requirements Document
      
      **Version:** 1.0 (hackathon build)
      **Owner:** Paramarsh Labs
      **Status:** Build-ready
      
      ---
      
      ## 1. Summary
      
      Hoichoi Drishti turns a Bengali episode into a **Semantic Timeline**: a structured, time-indexed representation of what is shown, said, heard and meant, scene by scene. Two applications sit on top of it:
      
      1. **Ad Intelligence** finds context-aware, low-disruption ad insertion points and product and topic opportunities, including products that are *mentioned but never shown*.
      2. **Localization** produces Bengali subtitles (SRT/VTT), Bengali closed captions with sound events, and an automatic QC report.
      
      It is not a subtitle generator or an ad model. It is one shared multimodal understanding layer with two consumers.
      
      ---
      
      ## 2. Problem
      
      | Team | Today | Pain |
      |---|---|---|
      | Ad ops / ad sales | Mid-rolls placed at fixed intervals or by hand | Breaks interrupt emotional beats. There is no contextual inventory to sell ("smartphone moment at 21:42"). |
      | Localization | Subtitles made manually or with generic ASR | Slow and expensive. Generic ASR handles Bengali punctuation, speaker turns and reading speed poorly. |
      | Accessibility | Closed captions rarely produced for regional content | No `[à¦¦à¦°à¦œà¦¾à¦¯à¦¼ à¦•à¦¡à¦¼à¦¾ à¦¨à¦¾à¦¡à¦¼à¦¾à¦° à¦¶à¦¬à§à¦¦]`-style sound cues. The content fails accessibility expectations. |
      | QC | Full human watch-through | No way to jump straight to risky segments. |
      
      ---
      
      ## 3. Users
      
      - **Ad ops manager:** wants a ranked list of break points with reasons, and contextual tags to sell against.
      - **Localization editor:** wants ready subtitle files plus a short list of segments to review.
      - **QC reviewer:** wants flagged timestamps and a one-click jump to each one.
      - **Demo judge (hackathon):** wants to see the whole understanding pipeline and trust the scores.
      
      ---
      
      ## 4. Goals and non-goals
      
      ### Goals
      - G1: Process an episode (up to 60 min) end to end into a single Semantic Timeline JSON.
      - G2: Segment the episode into meaningful **scenes**, not just shots.
      - G3: Detect entities from **both** dialogue and visuals, and classify each as mentioned-only, shown-only, mentioned-and-shown, or unverified.
      - G4: Rank ad insertion candidates with a **transparent, decomposed score**.
      - G5: Produce Bengali SRT/VTT subtitles and closed captions that follow standard timing and reading-speed rules.
      - G6: Produce a QC report with timestamped issues.
      - G7: Show all of the above in a simple web UI with a synced video player and timeline.
      
      ### Non-goals (this build)
      - Real-time or live-stream processing.
      - Face recognition that maps characters to actor identities.
      - Actual ad serving or SSAI integration. The platform outputs recommendations and a cue-point export only.
      - Translation into other languages. The architecture allows it later.
      - Multi-tenant auth or permissions.
      
      ---
      
      ## 5. Core concept: the Semantic Timeline
      
      Every episode becomes an ordered list of **scenes**. Each scene carries:
      
      - **Time bounds** and the shots it contains.
      - **Visual:** location, objects, activity, and visual mood from keyframes.
      - **Audio:** speakers, utterances, sound events, music presence, and loudness energy.
      - **Semantic:** summary, topics, mood, and narrative intensity (0â€“1).
      - **Entities:** each with its source (dialogue, visual or both), visual presence, sentiment, confidence and timestamps.
      
      Every downstream feature reads from this object. Nothing downstream re-analyzes the raw video.
      
      ---
      
      ## 6. Features and requirements
      
      Priority: **P0** = must ship for the demo, **P1** = should ship, **P2** = stretch.
      
      ### F1. Upload and processing (P0)
      - Upload an MP4/MKV, or register a local file path.
      - Show pipeline progress per stage (queued, running, done, failed) with elapsed time.
      - Stages are cached. Re-running skips completed stages, and a single stage can be re-run.
      - **Acceptance:** a 3-minute clip completes in under 5 minutes. A failed stage shows its error and can be retried alone.
      
      ### F2. Transcript with speakers (P0)
      - Bengali speech-to-text via Sarvam, with timestamps per utterance.
      - Speaker diarization with stable labels (`SPK_A`, `SPK_B`, â€¦).
      - Punctuation and cleanup pass. The text keeps its original meaning, and code-mixed English words stay as spoken.
      - Speakers can optionally be named from dialogue cues (P2), e.g. vocatives like "à¦®à¦¿à¦¤à¦¾, â€¦".
      - **Acceptance:** every utterance has a start, end, speaker and text. Clicking an utterance seeks the player to it.
      
      ### F3. Shot detection and scene segmentation (P0)
      - Detect shot boundaries.
      - Merge shots into scenes using visual similarity, dialogue continuity, speaker changes, location changes and an LLM boundary check.
      - Each scene gets a short title (e.g. "Restaurant conversation") and a 1â€“2 line summary.
      - **Acceptance:** scenes cover the full duration with no gaps and no overlaps. The number of scenes is roughly 1 per 1â€“4 minutes of drama content.
      
      ### F4. Visual understanding (P0)
      - **Baseline pass:** one deduplicated keyframe per shot is analyzed for location, objects, activity, visual mood and visible brands or products.
      - **Targeted pass:** for every entity mentioned in dialogue, frames across the **enclosing scene** are sampled more densely and checked for whether that entity is visible.
      - **Acceptance:** every scene has visual tags. Every dialogue entity has `visual_presence` set to `true`, `false` or `unverified`.
      
      ### F5. Entity and product-context intelligence (P0)
      - Extract entities and topics from the transcript, including implicit references (e.g. "à¦«à§‹à¦¨à¦Ÿà¦¾") and brands written in either English or Bengali script.
      - Merge dialogue entities with visual entities per scene.
      - Classify each entity as `mentioned_and_shown`, `mentioned_only`, `shown_only` or `unverified`.
      - Attach sentiment (positive, neutral or negative), timestamps and confidence.
      - Map entities to **ad categories** (e.g. Mobile, Food delivery, Fashion, Travel, Finance) using a configurable category list.
      - **Acceptance:** an Entities view lists all entities, filterable by category and presence class. Each entity links to its timestamps.
      
      ### F6. Audio events (P1 for closed captions, P0 for scoring signals)
      - Detect sound events (knock, rain, thunder, phone ring, door, laughter, crowd, music, â€¦).
      - Compute a loudness and music-energy curve over time.
      - **Acceptance:** events are shown on the timeline, and those above threshold appear in the closed captions.
      
      ### F7. Scene semantics (P0)
      - Scene mood and **narrative intensity** (0â€“1), built from the LLM judgment plus audio energy plus dialogue density.
      - Flag cliffhanger or high-tension moments.
      
      ### F8. Ad opportunity scoring (P0)
      - Candidate points: scene boundaries and long dialogue pauses inside low-intensity scenes.
      - Each candidate gets a **decomposed score**: pause length, scene-end proximity, low intensity, context match, speech penalty and cliffhanger penalty.
      - Output a ranked list with a plain-language reason, the matched ad categories, and the nearby entity context.
      - Configurable settings: minimum gap between breaks (default 8 min), number of breaks wanted, and blocked zones such as the first and last 2 minutes.
      - Export cue points as JSON and CSV.
      - **Acceptance:** the UI shows the score breakdown for each candidate. The selected breaks respect the minimum gap.
      
      ### F9. Bengali subtitles (P0)
      - Generate SRT and VTT from the diarized, cleaned transcript.
      - Rules: at most 2 lines per cue, about 42 characters per line, about 17 characters per second maximum, cue duration 1â€“7 s, gap of at least 80 ms between cues, and line breaks at natural phrase boundaries.
      - Speaker change inside a cue is marked with a leading dash.
      - **Acceptance:** both files open in VLC and the browser player, and they are selectable on the UI's video player.
      
      ### F10. Bengali closed captions (P1)
      - The subtitles plus bracketed Bengali sound-event cues, e.g. `[à¦¬à§ƒà¦·à§à¦Ÿà¦¿à¦° à¦¶à¦¬à§à¦¦]`, `[à¦«à§‹à¦¨ à¦¬à§‡à¦œà§‡ à¦‰à¦ à¦›à§‡]`.
      - Music is marked as `[à¦¸à¦™à§à¦—à§€à¦¤]` or with a mood variant (`[à¦­à¦¯à¦¼à¦™à§à¦•à¦° à¦¸à¦™à§à¦—à§€à¦¤]`).
      - Output: `episode_bn_cc.srt` and `.vtt`.
      
      ### F11. Subtitle QC report (P1)
      - Checks: low speech-to-text confidence, reading speed too high, lines too long, too many lines, overlapping speech, cues too short or too long, timing drift against VAD, and speaker ambiguity.
      - Each issue has a severity (error, warn or info), a timestamp, a rule, a message and a suggested fix.
      - **Acceptance:** clicking an issue seeks the player and highlights the cue.
      
      ### F12. Search (P2)
      - Natural-language search over scenes and utterances ("phone conversation", "rain scene"), with results that jump to timestamps.
      
      ### F13. Structured export (P0)
      - Download the full `semantic_timeline.json`, which validates against the published schema.
      - Download individual outputs: SRT, VTT, CC, ad cue points, and the QC report.
      
      ---
      
      ## 7. UI requirements
      
      This is a single web app with two screens. It is clean and dense, and intended as a working tool rather than marketing polish.
      
      ### Screen 1: Library
      - Upload button with drag and drop.
      - Episode list showing title, duration, status and a progress bar.
      
      ### Screen 2: Episode workspace
      
      ```
      â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
      â”‚ Episode 102  Â·  52:34  Â·  âœ“ Processed          [Searchâ€¦]  [Export â–¾] â”‚
      â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
      â”‚                                   â”‚  Scene 17 Â· Restaurant convo       â”‚
      â”‚         VIDEO PLAYER              â”‚  12:08 â€“ 14:52                     â”‚
      â”‚    (subtitle / CC track toggle)   â”‚  Summary â€¦                         â”‚
      â”‚                                   â”‚  Location Â· Activity Â· Mood        â”‚
      â”‚                                   â”‚  Intensity â–“â–“â–“â–‘â–‘â–‘â–‘ 0.31            â”‚
      â”‚                                   â”‚  Speakers: SPK_A, SPK_B            â”‚
      â”‚                                   â”‚  Entities: ðŸ“± smartphone           â”‚
      â”‚                                   â”‚    mentioned_only Â· positive Â· 0.91â”‚
      â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
      â”‚ TIMELINE (zoomable, synced playhead)                                  â”‚
      â”‚ Scenes    â”‚â–ˆâ–ˆ Family â–ˆâ–ˆâ”‚â–ˆâ–ˆ Restaurant â–ˆâ–ˆâ”‚â–ˆ Argument â–ˆâ”‚â–ˆâ–ˆ Street â–ˆâ–ˆâ”‚    â”‚
      â”‚ Speakers  â”‚â–¬Aâ–¬ â–¬Bâ–¬â–¬ â–¬Aâ–¬â”‚ â–¬Aâ–¬â–¬ â–¬Bâ–¬ â–¬Aâ–¬   â”‚â–¬Aâ–¬Bâ–¬Aâ–¬Bâ–¬Aâ–¬ â”‚  â–¬Câ–¬       â”‚    â”‚
      â”‚ Entities  â”‚            â”‚   ðŸ“±            â”‚            â”‚   âœˆ        â”‚    â”‚
      â”‚ Sounds    â”‚  ðŸšª        â”‚                â”‚  âš¡ ðŸŒ§      â”‚            â”‚    â”‚
      â”‚ Intensity â”‚~~~~___~~~~~â”‚____~~___       â”‚~~~^^^^^^~~~â”‚~~___       â”‚    â”‚
      â”‚ Ads       â”‚            â”‚          â–¼91   â”‚            â”‚   â–¼84      â”‚    â”‚
      â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
      â”‚ [Scenes] [Transcript] [Entities] [Ads] [Subtitles] [QC âš 3] [JSON]     â”‚
      â”‚  tab contentâ€¦                                                         â”‚
      â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
      ```
      
      **Tabs**
      - **Scenes:** a table of scenes (time, title, location, mood, intensity, entities). Clicking a row seeks the player.
      - **Transcript:** utterances grouped by scene, color-coded by speaker, with the current line highlighted during playback.
      - **Entities:** grouped by ad category, with a presence-class badge, sentiment, and timestamp chips.
      - **Ads:** a ranked candidate list. Each card shows the timestamp, total score, a score-breakdown bar, the reason, and the matched categories. A toggle marks candidates as selected. The ad settings live here too.
      - **Subtitles:** a cue list with inline preview. Toggle between SRT and CC and download.
      - **QC:** an issue list sorted by severity, which seeks the player on click.
      - **JSON:** a collapsible tree viewer of the semantic timeline, with a copy/download button.
      
      **Interaction rules**
      - Everything with a timestamp is clickable and seeks the player.
      - The playhead drives the scene panel on the right, which always shows the current scene.
      - Timeline lanes can be toggled on and off.
      
      ---
      
      ## 8. Success metrics (demo-level)
      
      | Metric | Target |
      |---|---|
      | End-to-end processing, 45-min episode | < 45 min on one T4 plus APIs |
      | Scene boundary agreement with human judgment (sampled) | â‰¥ 80% |
      | Mentioned-only entity precision (manual check on demo clip) | â‰¥ 85% |
      | Subtitle cues violating reading-speed or line rules after formatting | < 5% |
      | Top-3 ad candidates judged "non-disruptive" by a viewer | 3/3 on the demo episode |
      | GPT cost per 45-min episode | Tracked and shown in the UI; target is low single-digit USD |
      
      ---
      
      ## 9. Scope by priority
      
      - **P0:** F1, F2, F3, F4, F5, F7, F8, F9, F13, plus UI tabs Scenes, Transcript, Entities, Ads, Subtitles and JSON.
      - **P1:** F6 (closed-caption events), F10, F11, plus the QC tab.
      - **P2:** F12 search, speaker naming from dialogue, and translation hooks.
      
      **Build order:** transcript and subtitles â†’ shots, keyframes and scenes â†’ entities and targeted vision â†’ ad scoring â†’ UI polish â†’ closed captions and QC â†’ search.
      
      ---
      
      ## 10. Demo script (â‰ˆ4 min)
      
      1. Open a pre-processed episode. Frame the timeline as "one understanding layer, two products."
      2. Scrub the timeline and show the scene panel changing (location, mood, intensity).
      3. **Key moment:** at the phone dialogue, show the entity marked *mentioned_only* (said, never shown) and open the frames that were checked.
      4. Ads tab: show the top candidate, its score breakdown, and why it sits after the conversation ends rather than mid-argument.
      5. Toggle CC on the player and show the sound cues in Bengali.
      6. QC tab: click a warning and land on the flagged cue.
      7. JSON tab: "everything you saw is this one schema; any downstream system can consume it."
      8. Optional: live-process a 2-minute clip to show the pipeline actually runs.
      
      ---
      
      ## 11. Risks and mitigations
      
      | Risk | Mitigation |
      |---|---|
      | Music-heavy audio degrades speech-to-text | Separate vocals with Demucs before transcription, and mark low-confidence segments in QC |
      | Diarization errors on overlapping speech | Mark overlaps in QC, and never let overlapping audio merge into a single cue |
      | GPT vision cost on long episodes | Deduplicate keyframes, use low detail for the baseline pass, run targeted checks only on mentioned entities, and cache everything |
      | "Not visible" false negatives | Check the whole enclosing scene, not a fixed window, and label weak checks `unverified` rather than `false` |
      | Scene over- or under-segmentation | Combine signals with LLM boundary validation, and enforce a minimum scene length of 20 s |
      | Live demo failure | Demo from a cached, fully processed episode, with the live run kept optional |
      # Hoichoi Drishti â€” Technical Design
      
      Companion to `prd.md`. This document covers the architecture, pipeline stages, data schema, scoring logic, API, UI implementation and the build plan.
      
      ---
      
      ## 1. Architecture overview
      
      ```
                      â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                      â”‚              Web UI (React)              â”‚
                      â”‚  Library Â· Workspace Â· Timeline Â· Tabs   â”‚
                      â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                      â”‚ REST + SSE (progress)
                      â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                      â”‚           API (FastAPI)                  â”‚
                      â”‚  episodes Â· jobs Â· timeline Â· exports    â”‚
                      â””â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                              â”‚ enqueue              â”‚ read
                      â”Œâ”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”     â”Œâ”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                      â”‚ Worker (RQ)    â”‚     â”‚ SQLite + artifactsâ”‚
                      â”‚ Stage runner   â”‚â”€â”€â”€â”€â–ºâ”‚ data/episodes/{id}â”‚
                      â””â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”˜     â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                              â”‚
         â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
         â–¼            â–¼             â–¼              â–¼              â–¼
       ffmpeg     Local models   Sarvam API    OpenAI API     Local rules
       (media)    TransNetV2 /   (Bengali      (vision, LLM,  (subtitle fmt,
                  PySceneDetect  speech-to-    embeddings)    QC, ad score)
                  SigLIP, Demucs text, diar.)
                  Silero, PANNs
                  pyannote(opt)
      ```
      
      **Principles**
      - **Stage-based and cached.** Each stage reads the artifacts from earlier stages and writes its own. A stage that has finished is never recomputed unless it is forced.
      - **Pydantic is the source of truth.** Every artifact is a Pydantic model serialized to JSON. The final `semantic_timeline.json` is assembled from those models.
      - **LLM calls always use structured outputs** with JSON schemas generated from the Pydantic models, followed by validation and a retry on failure.
      - **Heavy local models run on a GPU box** (Kaggle, Colab or a rented GPU). The API and UI can run anywhere and simply read the artifacts.
      
      ---
      
      ## 2. Tech stack
      
      | Layer | Choice | Notes |
      |---|---|---|
      | Language | Python 3.11 | |
      | API | FastAPI + Uvicorn | SSE for progress |
      | Jobs | RQ + Redis | Or `asyncio` + one subprocess worker if you want no Redis |
      | DB | SQLite (SQLModel) | Episode and stage status only; content lives in JSON files |
      | Media | ffmpeg / ffprobe | |
      | Shots | TransNetV2 (GPU), PySceneDetect `AdaptiveDetector` as fallback | |
      | Frame embeddings | SigLIP (`google/siglip-base-patch16-224`) via `open_clip` / `transformers` | Deduplication plus the scene similarity signal |
      | Vocal separation | Demucs `htdemucs` (`--two-stems=vocals`) | |
      | VAD | Silero VAD | |
      | Speech-to-text + diarization | Sarvam (Saarika) | Use batch/job mode with diarization for long audio; confirm current limits in the Sarvam docs |
      | Diarization fallback | pyannote `speaker-diarization-3.1` | Needs a Hugging Face token |
      | Audio events | PANNs `Cnn14` (AudioSet 527 classes) | AST is an alternative |
      | Loudness | librosa RMS, pyloudnorm | |
      | LLM / vision | OpenAI `gpt-4.1-mini` (default), `gpt-4.1` for scene merge if budget allows | Structured outputs |
      | Embeddings (search) | `text-embedding-3-small` + LanceDB | P2 |
      | Subtitles | `srt`, `webvtt-py` + custom formatter | |
      | Frontend | Vite + React + TypeScript + Tailwind | |
      | Player | Native `<video>` with `<track>` | Simple, and handles VTT natively |
      | Timeline | Custom SVG/Canvas lanes | wavesurfer.js optional for the waveform |
      | JSON viewer | `react-json-view-lite` | |
      
      ---
      
      ## 3. Repo layout
      
      ```
      drishti/
      â”œâ”€â”€ backend/
      â”‚   â”œâ”€â”€ app/
      â”‚   â”‚   â”œâ”€â”€ main.py              # FastAPI app
      â”‚   â”‚   â”œâ”€â”€ api/                 # routes: episodes, jobs, timeline, exports
      â”‚   â”‚   â”œâ”€â”€ models/              # Pydantic schemas (section 5)
      â”‚   â”‚   â”œâ”€â”€ db.py
      â”‚   â”‚   â””â”€â”€ settings.py          # env, thresholds, category config
      â”‚   â”œâ”€â”€ pipeline/
      â”‚   â”‚   â”œâ”€â”€ runner.py            # stage DAG + caching
      â”‚   â”‚   â”œâ”€â”€ stages/
      â”‚   â”‚   â”‚   â”œâ”€â”€ s01_ingest.py
      â”‚   â”‚   â”‚   â”œâ”€â”€ s02_shots.py
      â”‚   â”‚   â”‚   â”œâ”€â”€ s03_keyframes.py
      â”‚   â”‚   â”‚   â”œâ”€â”€ s04_audio_prep.py
      â”‚   â”‚   â”‚   â”œâ”€â”€ s05_vad.py
      â”‚   â”‚   â”‚   â”œâ”€â”€ s06_stt.py
      â”‚   â”‚   â”‚   â”œâ”€â”€ s07_transcript_clean.py
      â”‚   â”‚   â”‚   â”œâ”€â”€ s08_audio_events.py
      â”‚   â”‚   â”‚   â”œâ”€â”€ s09_vision_baseline.py
      â”‚   â”‚   â”‚   â”œâ”€â”€ s10_scenes.py
      â”‚   â”‚   â”‚   â”œâ”€â”€ s11_entities_dialogue.py
      â”‚   â”‚   â”‚   â”œâ”€â”€ s12_vision_targeted.py
      â”‚   â”‚   â”‚   â”œâ”€â”€ s13_scene_semantics.py
      â”‚   â”‚   â”‚   â”œâ”€â”€ s14_ad_scoring.py
      â”‚   â”‚   â”‚   â”œâ”€â”€ s15_subtitles.py
      â”‚   â”‚   â”‚   â”œâ”€â”€ s16_captions.py
      â”‚   â”‚   â”‚   â”œâ”€â”€ s17_qc.py
      â”‚   â”‚   â”‚   â””â”€â”€ s18_assemble.py
      â”‚   â”‚   â”œâ”€â”€ llm.py               # OpenAI wrapper: structured output, retry, cost log
      â”‚   â”‚   â”œâ”€â”€ sarvam.py            # Sarvam client
      â”‚   â”‚   â””â”€â”€ prompts/             # prompt templates (.md)
      â”‚   â”œâ”€â”€ config/
      â”‚   â”‚   â”œâ”€â”€ ad_categories.yaml
      â”‚   â”‚   â””â”€â”€ sound_labels_bn.yaml # AudioSet label -> Bengali CC text
      â”‚   â””â”€â”€ pyproject.toml
      â”œâ”€â”€ frontend/
      â”‚   â””â”€â”€ src/
      â”‚       â”œâ”€â”€ pages/Library.tsx
      â”‚       â”œâ”€â”€ pages/Workspace.tsx
      â”‚       â”œâ”€â”€ components/Player.tsx
      â”‚       â”œâ”€â”€ components/Timeline/  # lanes
      â”‚       â”œâ”€â”€ components/ScenePanel.tsx
      â”‚       â”œâ”€â”€ components/tabs/      # Scenes, Transcript, Entities, Ads, Subtitles, QC, Json
      â”‚       â””â”€â”€ api.ts
      â””â”€â”€ data/episodes/{episode_id}/   # artifacts (section 4)
      ```
      
      ---
      
      ## 4. Artifact layout (per episode)
      
      ```
      data/episodes/{id}/
      â”œâ”€â”€ source.mp4
      â”œâ”€â”€ proxy.mp4               # 720p H.264 for browser playback
      â”œâ”€â”€ audio/
      â”‚   â”œâ”€â”€ full_16k.wav        # mono 16 kHz
      â”‚   â”œâ”€â”€ vocals_16k.wav      # Demucs output
      â”‚   â””â”€â”€ chunks/             # VAD-aligned chunks for speech-to-text
      â”œâ”€â”€ frames/
      â”‚   â”œâ”€â”€ kf_{shot_id}.jpg    # baseline keyframes
      â”‚   â””â”€â”€ tgt_{entity_id}_{n}.jpg
      â”œâ”€â”€ stages/
      â”‚   â”œâ”€â”€ s01_ingest.json
      â”‚   â”œâ”€â”€ s02_shots.json
      â”‚   â”œâ”€â”€ â€¦
      â”‚   â””â”€â”€ s17_qc.json
      â”œâ”€â”€ outputs/
      â”‚   â”œâ”€â”€ semantic_timeline.json
      â”‚   â”œâ”€â”€ episode_bn.srt / .vtt
      â”‚   â”œâ”€â”€ episode_bn_cc.srt / .vtt
      â”‚   â”œâ”€â”€ ad_cuepoints.json / .csv
      â”‚   â””â”€â”€ qc_report.json
      â””â”€â”€ logs/
          â”œâ”€â”€ pipeline.log
          â””â”€â”€ llm_calls.jsonl      # prompt hash, model, tokens, cost, latency
      ```
      
      ---
      
      ## 5. Data schema (Pydantic)
      
      All times are **seconds as floats** from the start of the episode. IDs are stable strings.
      
      ```python
      # models/timeline.py
      from pydantic import BaseModel, Field
      from typing import Literal, Optional
      
      class Shot(BaseModel):
          shot_id: str                 # "shot_0042"
          start: float
          end: float
          keyframe: Optional[str]      # path; None if deduped
          dup_of: Optional[str]        # shot_id whose keyframe represents it
          embedding_ref: Optional[str] # index into npy
      
      class VisualTags(BaseModel):
          location: str                # "restaurant", "living room", "street" â€¦
          indoor: Optional[bool]
          objects: list[str]
          visible_brands: list[str]
          activity: str
          visual_mood: str
          people_count: int
          confidence: float
      
      class Word(BaseModel):
          text: str
          start: float
          end: float
      
      class Utterance(BaseModel):
          utt_id: str
          start: float
          end: float
          speaker: str                 # "SPK_A"
          speaker_name: Optional[str]  # P2
          text_raw: str
          text: str                    # cleaned + punctuated Bengali
          words: Optional[list[Word]]
          confidence: Optional[float]
          overlap: bool = False
      
      class AudioEvent(BaseModel):
          event_id: str
          label: str                   # AudioSet label "Knock"
          label_bn: str                # "à¦¦à¦°à¦œà¦¾à¦¯à¦¼ à¦•à¦¡à¦¼à¦¾ à¦¨à¦¾à¦¡à¦¼à¦¾à¦° à¦¶à¦¬à§à¦¦"
          start: float
          end: float
          score: float
          in_cc: bool
      
      PresenceClass = Literal["mentioned_and_shown","mentioned_only","shown_only","unverified"]
      
      class EntityMention(BaseModel):
          source: Literal["dialogue","visual"]
          time: float
          utt_id: Optional[str]
          shot_id: Optional[str]
          surface: str                 # "à¦«à§‹à¦¨à¦Ÿà¦¾" / "Samsung"
      
      class VisualCheck(BaseModel):
          frames_checked: list[str]
          visible: Optional[bool]      # None = inconclusive
          visible_frames: list[str]
          confidence: float
          note: str
      
      class Entity(BaseModel):
          entity_id: str
          name: str                    # canonical English: "smartphone"
          name_bn: Optional[str]
          kind: Literal["product","brand","place","food","activity","topic","other"]
          brand: Optional[str]
          ad_categories: list[str]     # ["mobile"]
          mentions: list[EntityMention]
          sentiment: Literal["positive","neutral","negative"]
          presence: PresenceClass
          visual_check: Optional[VisualCheck]
          confidence: float
      
      class SceneSemantic(BaseModel):
          title: str
          summary: str
          topics: list[str]
          mood: str
          narrative_intensity: float   # 0..1 fused
          intensity_components: dict[str, float]  # llm, audio_energy, dialogue_density
          is_cliffhanger: bool
      
      class Scene(BaseModel):
          scene_id: str
          start: float
          end: float
          shot_ids: list[str]
          visual: VisualTags           # aggregated over shots
          speakers: list[str]
          utt_ids: list[str]
          audio_events: list[str]
          music_ratio: float
          semantic: SceneSemantic
          entity_ids: list[str]
      
      class ScoreBreakdown(BaseModel):
          pause: float
          scene_end: float
          low_intensity: float
          context_match: float
          speech_penalty: float
          cliffhanger_penalty: float
          total: float
      
      class AdCandidate(BaseModel):
          cand_id: str
          time: float
          scene_id: str
          kind: Literal["scene_boundary","dialogue_pause"]
          pause_len: float
          score: ScoreBreakdown
          disruption: Literal["low","medium","high"]
          matched_categories: list[str]
          context_entity_ids: list[str]
          reason: str
          selected: bool
      
      class SubtitleCue(BaseModel):
          idx: int
          start: float
          end: float
          lines: list[str]
          speakers: list[str]
          kind: Literal["dialogue","sound"]
          cps: float
      
      class QCIssue(BaseModel):
          issue_id: str
          severity: Literal["error","warn","info"]
          rule: str
          time: float
          cue_idx: Optional[int]
          message: str
          suggestion: Optional[str]
      
      class SemanticTimeline(BaseModel):
          schema_version: str = "1.0"
          episode: dict                # id, title, duration, fps, resolution
          scenes: list[Scene]
          shots: list[Shot]
          utterances: list[Utterance]
          audio_events: list[AudioEvent]
          entities: list[Entity]
          ad_candidates: list[AdCandidate]
          subtitles: dict              # paths + cue counts
          qc: list[QCIssue]
          curves: dict                 # {"intensity":[[t,v],â€¦], "loudness":[[t,v],â€¦]} at 1 Hz
          processing: dict             # per-stage timing, model versions, llm cost
      ```
      
      Publish the JSON Schema with `SemanticTimeline.model_json_schema()` at `GET /schema`.
      
      ---
      
      ## 6. Pipeline stages
      
      The runner executes a DAG. Stages whose inputs are ready can run in parallel: the audio branch and the video branch are independent until stage s10.
      
      ```
      s01 ingest
       â”œâ”€â”€ VIDEO: s02 shots â†’ s03 keyframes â†’ s09 vision_baseline â”€â”
       â””â”€â”€ AUDIO: s04 audio_prep â†’ s05 vad â†’ s06 stt â†’ s07 clean â”€â”€â”¤
                  s04 â†’ s08 audio_events â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
                                                                   â–¼
                                        s10 scenes â†’ s11 entities_dialogue
                                                  â†’ s12 vision_targeted
                                                  â†’ s13 scene_semantics
                                                  â†’ s14 ad_scoring
                                s07 â†’ s15 subtitles â†’ s16 captions (needs s08)
                                                    â†’ s17 qc
                                        all â†’ s18 assemble
      ```
      
      ### s01 â€” Ingest
      - `ffprobe` records duration, fps, resolution and audio streams.
      - Create a proxy: `ffmpeg -i source -vf scale=-2:720 -c:v libx264 -preset veryfast -crf 26 -c:a aac -b:a 128k -movflags +faststart proxy.mp4`
      - Extract audio: `ffmpeg -i source -ac 1 -ar 16000 audio/full_16k.wav`
      
      ### s02 â€” Shots
      - TransNetV2 gives per-frame transition probabilities; threshold at 0.5.
      - Fallback: `scenedetect -i proxy.mp4 detect-adaptive list-scenes`.
      - Merge shots shorter than 0.4 s into their neighbour.
      
      ### s03 â€” Keyframes and deduplication
      - One frame per shot at the midpoint. Long shots over 8 s get a second frame at 75%.
      - Compute a SigLIP embedding for each keyframe.
      - **Dedup:** if cosine similarity with any keyframe in the previous 10 shots is at least 0.93, set `dup_of`, which skips vision on that frame. This typically removes 40â€“60% of frames in dialogue-heavy drama because of shot/reverse-shot editing.
      - Save the embeddings as `stages/embeddings.npy`.
      
      ### s04 â€” Audio prep
      - `demucs --two-stems=vocals -n htdemucs` on the full audio, then resample the vocals to 16 kHz mono.
      - For episodes over 30 min, run Demucs in 10-minute segments with 5 s overlap to keep memory manageable.
      
      ### s05 â€” VAD
      - Silero VAD on `vocals_16k.wav` produces speech segments.
      - Build **chunks** for speech-to-text by merging speech segments up to a maximum chunk length, splitting only at silences of at least 300 ms. Set the maximum to the limit of the Sarvam endpoint you use; if you use batch mode, you can send the whole file.
      - Store the silence intervals. They become the pause candidates in s14.
      
      ### s06 â€” Speech-to-text and diarization
      - **Primary:** Sarvam speech-to-text on the vocals track with `language_code=bn-IN`, requesting timestamps and diarization. Batch/job mode is preferable for full episodes.
      - Normalize the response into `Utterance[]`. If only chunk-level timestamps are returned, offset them by each chunk's start.
      - **Fallback diarization:** if Sarvam diarization isn't available, run pyannote 3.1 and assign each utterance the speaker label with the largest time overlap.
      - Mark an utterance `overlap=true` when two diarization turns overlap it by more than 300 ms.
      - Keep `text_raw` exactly as returned.
      
      ### s07 â€” Transcript cleanup (LLM)
      - Batch about 40 utterances per call and include the 5 previous utterances as context.
      - Instruction: restore Bengali punctuation (`à¥¤`, `?`, `!`, `,`), fix obvious ASR spacing errors, **do not paraphrase**, keep code-mixed English as spoken, and return exactly the same `utt_id`s.
      - Validation: the character-level edit distance between the raw and cleaned text must be at most 25%. Otherwise keep the raw text and flag it for QC.
      
      ### s08 â€” Audio events and loudness
      - PANNs Cnn14 on `full_16k.wav` (the full mix, not the vocals track), with 1 s windows and 0.5 s hop.
      - Keep labels in the `sound_labels_bn.yaml` whitelist whose score is at least the per-label threshold (default 0.3). Merge consecutive windows into events.
      - `in_cc=true` if the event lasts at least 0.8 s, scores at least the label's `cc_threshold`, and does not overlap dialogue by more than 70%. Music is handled separately as a mood tag.
      - Compute RMS loudness at 1 Hz, normalized to 0â€“1 across the episode, and the music ratio per second (the "Music" class score).
      
      Example `sound_labels_bn.yaml`:
      ```yaml
      Knock:            { bn: "à¦¦à¦°à¦œà¦¾à¦¯à¦¼ à¦•à¦¡à¦¼à¦¾ à¦¨à¦¾à¦¡à¦¼à¦¾à¦° à¦¶à¦¬à§à¦¦", cc_threshold: 0.35 }
      Rain:             { bn: "à¦¬à§ƒà¦·à§à¦Ÿà¦¿à¦° à¦¶à¦¬à§à¦¦",          cc_threshold: 0.40 }
      Thunder:          { bn: "à¦¬à¦œà§à¦°à¦ªà¦¾à¦¤",               cc_threshold: 0.35 }
      Telephone bell ringing: { bn: "à¦«à§‹à¦¨ à¦¬à§‡à¦œà§‡ à¦‰à¦ à¦›à§‡",    cc_threshold: 0.35 }
      Ringtone:         { bn: "à¦«à§‹à¦¨ à¦¬à§‡à¦œà§‡ à¦‰à¦ à¦›à§‡",          cc_threshold: 0.35 }
      Door:             { bn: "à¦¦à¦°à¦œà¦¾ à¦–à§‹à¦²à¦¾à¦° à¦¶à¦¬à§à¦¦",         cc_threshold: 0.40 }
      Laughter:         { bn: "à¦¹à¦¾à¦¸à¦¿à¦° à¦¶à¦¬à§à¦¦",              cc_threshold: 0.45 }
      Crying, sobbing:  { bn: "à¦•à¦¾à¦¨à§à¦¨à¦¾à¦° à¦¶à¦¬à§à¦¦",             cc_threshold: 0.40 }
      Crowd:            { bn: "à¦­à¦¿à¦¡à¦¼à§‡à¦° à¦•à§‹à¦²à¦¾à¦¹à¦²",            cc_threshold: 0.45 }
      Vehicle horn, car horn, honking: { bn: "à¦—à¦¾à¦¡à¦¼à¦¿à¦° à¦¹à¦°à§à¦¨", cc_threshold: 0.40 }
      Gunshot, gunfire: { bn: "à¦—à§à¦²à¦¿à¦° à¦¶à¦¬à§à¦¦",              cc_threshold: 0.30 }
      Footsteps:        { bn: "à¦ªà¦¾à¦¯à¦¼à§‡à¦° à¦¶à¦¬à§à¦¦",               cc_threshold: 0.50 }
      ```
      
      ### s09 â€” Vision baseline (LLM vision)
      - Input: every keyframe with `dup_of == null`.
      - Batch 4 keyframes per request at `detail: "low"`, each labelled with its `shot_id`, and ask for `VisualTags` for each.
      - Prompt rules: name only objects that are clearly visible; list only brands that are legible or unmistakable; keep locations to a short, consistent vocabulary (provide a suggested list); use English for tags.
      - Deduplicated shots inherit the tags of their `dup_of` shot.
      
      ### s10 â€” Scene segmentation
      Scenes are built in two steps.
      
      **Step A â€” Heuristic boundary scoring between consecutive shots** `i` and `i+1`:
      ```
      b = 0.35 * (1 - cos_sim(emb_i, emb_{i+1}))       # visual change, window-averaged over Â±2 shots
        + 0.25 * location_changed(tags_i, tags_{i+1})
        + 0.20 * speaker_set_change(window before, window after)
        + 0.20 * silence_at_cut (â‰¥ 1.0 s silence spanning the cut)
      ```
      Boundaries where `b â‰¥ 0.45` become candidates. Enforce a minimum scene length of 20 s by merging the weakest boundaries first.
      
      **Step B â€” LLM validation.** Build a compact per-scene digest: time range, shot count, locations, dominant objects and the first and last three utterances. Ask the LLM, over windows of about 8 candidate scenes, to **merge or keep** each boundary and to give each scene a title. The LLM can only merge candidate boundaries; it cannot add new ones. This keeps it grounded in the evidence.
      
      Aggregate the visual tags per scene: take the majority location, and the union of objects weighted by the fraction of shot time they appear in.
      
      ### s11 â€” Dialogue entity extraction (LLM)
      - Run per scene. The input is the scene's utterances (with `utt_id` and time) plus the scene's visual tags.
      - Output is a list of `Entity` drafts with `mentions[source=dialogue]`, `kind`, `brand`, `sentiment`, canonical English `name`, `name_bn`, and `ad_categories` chosen from `ad_categories.yaml`.
      - The prompt must cover implicit references ("à¦«à§‹à¦¨à¦Ÿà¦¾", "à¦“à¦Ÿà¦¾"), resolved within the scene; brands in either script; and **no invented entities**, since every mention must cite a `utt_id`.
      - Cross-scene merging happens afterwards: entities with the same `name` and `brand` share an `entity_id`, but each scene keeps its own presence verdict.
      
      Example `ad_categories.yaml`:
      ```yaml
      mobile:        [smartphone, phone, mobile, earphones, charger]
      food_delivery: [food, restaurant, biryani, pizza, order, hungry]
      fashion:       [saree, dress, clothes, shoes, jewellery]
      travel:        [trip, vacation, flight, hotel, train, darjeeling, puri]
      finance:       [loan, bank, salary, money, insurance, upi]
      beauty:        [makeup, cream, shampoo, skincare]
      auto:          [car, bike, scooter]
      ```
      The LLM chooses categories. The keyword lists are hints included in the prompt, not hard matching rules.
      
      ### s12 â€” Targeted vision verification
      For each dialogue entity of kind `product` or `brand` (and `food` when relevant):
      1. **Window:** the enclosing scene. For scenes longer than 180 s, use Â±45 s around the mentions, clipped to the scene bounds.
      2. **Sample:** 1 fps, then deduplicate by SigLIP similarity (â‰¥ 0.95), keeping at most 10 frames spread evenly across the window.
      3. **Cheap pre-check:** if the scene's baseline `objects` already contains the entity (fuzzy match), mark it visible using the frames from that shot, and skip steps 4â€“5.
      4. **Vision call:** send the frames at `detail: "high"`, 2Ã—5 grids stitched into two images with timestamps burned in. Ask a single question: *"Is a {name} ({brand if any}) visible? Return the timestamps of the frames where it is visible, and a confidence."*
      5. **Verdict:**
         - visible with confidence â‰¥ 0.6 â†’ `mentioned_and_shown`
         - not visible with confidence â‰¥ 0.7 across â‰¥ 6 frames â†’ `mentioned_only`
         - otherwise â†’ `unverified`
      - Visual-only entities: `visible_brands` and product-like `objects` from the baseline that have no dialogue mention become `shown_only` entities.
      
      ### s13 â€” Scene semantics
      - An LLM call per scene, with the summary digest, full utterances, visual tags and audio events as input, returns `title`, `summary`, `topics`, `mood`, `llm_intensity âˆˆ [0,1]` and `is_cliffhanger`.
      - **Fused intensity:**
      ```
      audio_energy     = mean(loudness over scene) normalized to episode p10â€“p90
      dialogue_density = speech_seconds / scene_seconds, then overlap-weighted (+0.2 per overlap ratio)
      narrative_intensity = 0.55*llm_intensity + 0.25*audio_energy + 0.20*dialogue_density
      ```
      - The final scene of the episode, and any scene with `is_cliffhanger`, gets `cliffhanger` protection used in s14.
      - Emit a per-second intensity curve for the UI by smoothing across scene boundaries with a 5 s window.
      
      ### s14 â€” Ad scoring
      **Candidates**
      - Every scene boundary becomes a candidate at the midpoint of the silence nearest to the cut, within Â±2 s. If there is no silence, use the cut time.
      - Every silence of at least 1.2 s inside a scene with `narrative_intensity < 0.4` becomes a candidate.
      - Candidates inside blocked zones (default: first 120 s and last 120 s) are dropped.
      
      **Score components (each 0â€“1)**
      ```
      pause          = min(pause_len / 2.5, 1)
      scene_end      = 1 if kind == scene_boundary else max(0, 1 - dist_to_scene_end/30)
      low_intensity  = 1 - mean(intensity over [t-20s, t+5s])
      context_match  = max over entities in [t-60s, t] of
                         (entity.confidence * sentiment_w * presence_w) , 0 if none
                         sentiment_w: pos 1.0, neutral 0.7, neg 0.3
                         presence_w:  mentioned_and_shown 1.0, mentioned_only 0.9,
                                      shown_only 0.8, unverified 0.6
      speech_penalty = 1 if speech within Â±0.3s of t else 0
      cliffhanger_penalty = 1 if t inside or within 10 s after a cliffhanger scene's peak
                             (but scene *end* of a cliffhanger is allowed)
      
      total = 0.25*pause + 0.25*scene_end + 0.30*low_intensity + 0.20*context_match
              - 0.50*speech_penalty - 0.40*cliffhanger_penalty
      total = clamp(total, 0, 1)
      ```
      `disruption` is low when `low_intensity â‰¥ 0.6` and `speech_penalty == 0`, high when `low_intensity < 0.35` or any penalty applies, and medium otherwise.
      
      **Selection:** greedily pick the highest-scoring candidates, enforcing `min_gap` (default 480 s) and `n_breaks` (default `floor(duration/600)`). Selection re-runs instantly when the settings change: it's pure Python over the cached candidates, exposed through an API.
      
      **Reason text:** template-generated from the score components, with no LLM call. For example: *"Scene boundary after 'Restaurant conversation'; 1.4 s pause; low intensity (0.22); positive smartphone discussion 5 s earlier â†’ mobile."*
      
      ### s15 â€” Subtitles
      The formatter is deterministic and has no LLM in the loop.
      1. Start from the cleaned utterances. Split long utterances at `à¥¤?!` first, then at commas or conjunctions (à¦à¦¬à¦‚, à¦•à¦¿à¦¨à§à¦¤à§, à¦¤à¦¾à¦‡, à¦†à¦°), then at the word nearest the midpoint.
      2. Timing: when word timestamps are available, cut at word boundaries. Otherwise distribute the time proportionally by grapheme count. **Count Bengali graphemes with the `regex` module's `\X`, not `len()`**, because conjuncts inflate `len()`.
      3. Constraints:
         - `MAX_LINE = 42` graphemes, `MAX_LINES = 2`, `MAX_CPS = 17`
         - `MIN_DUR = 1.0 s`, `MAX_DUR = 7.0 s`, `MIN_GAP = 0.08 s`
         - If CPS is exceeded, extend the end into available silence up to +0.5 s; if it's still over, split the cue.
      4. Line breaking: balance the two lines (prefer a bottom-heavy pyramid), and never break right after a single short word.
      5. Speaker change within a cue: prefix each line with `- `.
      6. Write `episode_bn.srt` using the `srt` library, and write the VTT with `webvtt-py` or directly.
      
      ### s16 â€” Closed captions
      - Merge the dialogue cues with sound cues from events where `in_cc=true`: `[label_bn]` as its own cue, at least 1.0 s long.
      - If a sound overlaps a dialogue cue, add it as an extra first line of that cue when the cue has only one line; otherwise shift the sound cue into the nearest gap within Â±1.5 s, and drop it if no gap exists.
      - Music: when the scene's `music_ratio > 0.6` and there is no dialogue for 3 s or more, emit `[à¦¸à¦™à§à¦—à§€à¦¤]`, or `[{mood} à¦¸à¦™à§à¦—à§€à¦¤]` using a small mapping from mood to Bengali adjective.
      
      ### s17 â€” QC
      Each rule is a pure function over `(cues, utterances, vad, events)` and returns `QCIssue[]`.
      
      | Rule | Severity | Condition |
      |---|---|---|
      | `low_confidence` | warn | utterance confidence < 0.6, or cleanup rejected in s07 |
      | `reading_speed` | warn/error | cps > 17 (warn) or > 21 (error) |
      | `line_length` | warn | line > 42 graphemes |
      | `line_count` | error | > 2 lines |
      | `overlap_speech` | warn | the cue spans an utterance with `overlap=true` |
      | `duration` | info/warn | < 1.0 s or > 7.0 s |
      | `timing_drift` | warn | cue start more than 0.5 s from the nearest VAD speech onset |
      | `speaker_ambiguous` | info | diarization confidence low or speaker flipped within 1 s |
      | `missing_speech` | warn | VAD speech â‰¥ 2 s with no cue covering it |
      
      Also produce a summary: counts by severity and a pass/fail against thresholds.
      
      ### s18 â€” Assemble
      - Load all stage outputs, build the `SemanticTimeline`, validate it, and write `outputs/semantic_timeline.json`.
      - Attach `processing`: timing per stage, model identifiers, and the total LLM cost from `llm_calls.jsonl`.
      
      ---
      
      ## 7. LLM layer (`pipeline/llm.py`)
      
      ```python
      def call_structured(model: str, system: str, user_parts: list, schema: type[BaseModel],
                          stage: str, temperature: float = 0.1, max_retries: int = 2) -> BaseModel:
          # 1. cache key = sha256(model + system + serialized user_parts + schema name)
          # 2. cache hit -> return parsed
          # 3. client.responses.parse(... text_format=schema)  (or chat.completions.parse)
          # 4. validate; on failure append error to prompt and retry
          # 5. log tokens, cost, latency to llm_calls.jsonl; write cache
      ```
      
      - **Disk cache** of every call keyed by content hash. Re-runs cost nothing, and the demo is reproducible.
      - **Concurrency:** an `asyncio.Semaphore(8)` for vision calls and 16 for text calls, with exponential backoff on 429 responses.
      - **Prompts** live in `prompts/*.md` as Jinja templates, versioned by filename.
      - **Cost guardrail:** a `MAX_LLM_USD_PER_EPISODE` environment variable. The runner stops before any stage whose estimated cost would exceed the remaining budget.
      
      **Rough call budget (45-min drama):** ~500 shots become ~220 unique keyframes, which is ~55 baseline vision calls; ~20 scene calls each for s11 and s13; ~15 s07 calls; 5â€“10 s10 calls; and ~10â€“25 targeted vision calls. That's about 130â€“150 calls, mostly on the mini model.
      
      ---
      
      ## 8. Sarvam client (`pipeline/sarvam.py`)
      
      - Wraps speech-to-text. Send the vocals track, `bn-IN`, with timestamps and diarization requested.
      - Handles both modes: **sync** for short chunks from s05, and **batch/job** for full audio (submit, poll, fetch).
      - Normalizes any response shape into `Utterance[]`. Keep the raw response in `stages/s06_raw.json` so you can re-parse without calling the API again.
      - Endpoint names, duration limits and diarization parameters change over time, so confirm them against the current Sarvam docs before wiring this up. Keep the client behind an interface so pyannote plus another ASR can be swapped in.
      
      ---
      
      ## 9. API
      
      | Method | Path | Purpose |
      |---|---|---|
      | POST | `/episodes` | Multipart upload or `{path}`; creates the episode and enqueues the pipeline |
      | GET | `/episodes` | List with status |
      | GET | `/episodes/{id}` | Metadata plus per-stage status |
      | GET | `/episodes/{id}/events` | **SSE** stream of stage progress |
      | POST | `/episodes/{id}/rerun` | `{from_stage, force}` |
      | GET | `/episodes/{id}/timeline` | Full `semantic_timeline.json` |
      | GET | `/episodes/{id}/scenes/{scene_id}` | Scene with resolved utterances and entities |
      | GET | `/episodes/{id}/ads?min_gap=&n_breaks=&blocked=` | Re-runs selection over cached candidates |
      | PATCH | `/episodes/{id}/ads/{cand_id}` | Manual select/unselect |
      | GET | `/episodes/{id}/frames/{name}` | Serves keyframes and targeted frames |
      | GET | `/episodes/{id}/video` | Proxy MP4 with HTTP range support (`FileResponse`) |
      | GET | `/episodes/{id}/subs/{kind}.{fmt}` | `kind âˆˆ {sub, cc}`, `fmt âˆˆ {srt, vtt}` |
      | GET | `/episodes/{id}/export/{name}` | `ad_cuepoints.csv`, `qc_report.json`, `semantic_timeline.json` |
      | GET | `/search?episode_id=&q=` | P2 |
      | GET | `/schema` | JSON Schema of `SemanticTimeline` |
      
      ---
      
      ## 10. Frontend
      
      ### State
      - On opening the workspace, fetch `/timeline` once. The whole timeline is small enough to hold in memory: a 45-minute episode produces well under 5 MB.
      - The only global state is `currentTime`, `selectedSceneId`, `laneVisibility` and `adSettings`. Use Zustand or plain React context.
      - `currentTime` comes from the video element's `timeupdate` event, throttled to about 10 Hz. `seek(t)` is exported globally.
      
      ### Components
      - **Player:** `<video src=/video>` with two `<track>` elements (sub VTT, CC VTT) and a toggle between them.
      - **Timeline:** one SVG with a shared x-scale (`d3-scale` only). Zoom and pan via the wheel and drag. The lanes are:
        - Scenes: colored blocks with titles, color by mood
        - Speakers: thin bars per utterance, colored per speaker
        - Entities: icons at mention times; the border style encodes the presence class
        - Sounds: icons for `in_cc` events
        - Intensity: an area chart from `curves.intensity`
        - Ads: triangle markers sized by score, filled if selected
        - A playhead line drawn across all lanes; clicking anywhere seeks
      - **ScenePanel:** derived from `currentTime`. Shows title, time, summary, visual tags, intensity bar, speakers and entity chips. A thumbnail strip shows the scene's keyframes.
      - **Tabs:**
        - *Scenes:* a sortable table
        - *Transcript:* virtualized list (`react-virtuoso`), auto-scrolling to the current utterance
        - *Entities:* grouped by category, with presence badges; expanding one shows the checked frames with visible ones highlighted
        - *Ads:* settings form, ranked cards, a stacked score-breakdown bar per card, and a select toggle
        - *Subtitles:* cue list with inline editing (P2) and download buttons
        - *QC:* issue list with a severity filter, click to seek
        - *JSON:* tree viewer plus download
      
      ### Styling
      - Tailwind with a dark UI by default, which suits a video tool.
      - Presence badges: shown = green, mentioned-only = amber, shown-only = blue, unverified = gray.
      - Bengali font: **Noto Sans Bengali** via Google Fonts, also used in the subtitle track through `::cue { font-family }`.
      
      ---
      
      ## 11. Config and environment
      
      ```env
      OPENAI_API_KEY=
      SARVAM_API_KEY=
      HF_TOKEN=                      # only if the pyannote fallback is used
      DATA_DIR=./data
      REDIS_URL=redis://localhost:6379
      LLM_MODEL_DEFAULT=gpt-4.1-mini
      LLM_MODEL_SCENES=gpt-4.1-mini
      MAX_LLM_USD_PER_EPISODE=5
      DEVICE=cuda                    # cpu fallback: slower Demucs/TransNetV2
      ```
      
      All thresholds (dedup similarity, boundary weights, ad weights, subtitle limits, QC thresholds) live in `settings.py` as a single `Thresholds` model and are recorded in `processing` so each run is reproducible.
      
      ---
      
      ## 12. Compute plan
      
      - **GPU stages** (Demucs, TransNetV2, SigLIP, PANNs, pyannote) run on Kaggle or Colab. Package them as `python -m pipeline.run --episode X --stages s02,s03,s04,s08` and sync the `data/episodes/X/` folder back.
      - **CPU and API stages** (everything else) run locally.
      - The runner only checks for artifacts, so it doesn't matter which machine produced them.
      - Rough GPU time for 45 minutes of content on a T4: Demucs ~6â€“10 min, TransNetV2 ~3 min, SigLIP ~1 min, PANNs ~2 min.
      
      ---
      
      ## 13. Testing
      
      - **Unit:** the subtitle formatter (grapheme counting, splitting, CPS), QC rules, ad scoring and selection, and scene-boundary merging, all on fixture data.
      - **Golden clip:** a hand-annotated 3â€“5 minute clip covering scene boundaries, 3 entities (including one mentioned-only), 2 sound events and expected ad points. The pipeline output is diffed against it in CI.
      - **Schema:** `SemanticTimeline.model_validate_json` runs on every output.
      - **LLM regression:** cached responses make the tests deterministic; bust the cache only when a prompt changes.
      
      ---
      
      ## 14. Build plan
      
      | Day / block | Deliverable |
      |---|---|
      | 1 | Repo skeleton, schemas, runner with caching, s01, and the Sarvam client; s05â€“s07 produce a clean diarized transcript |
      | 2 | s15 subtitles + s17 QC. **First shippable output: SRT/VTT plus the QC report** |
      | 3 | s02, s03, s09 (shots, keyframes, baseline vision), s10 scenes |
      | 4 | s11, s12 (entities plus targeted vision), s13 semantics |
      | 5 | s14 ad scoring, s18 assembly, and the API |
      | 6 | Frontend: player, timeline lanes, scene panel, tabs |
      | 7 | s08 + s16 (audio events, CC), polish, golden-clip tuning, recording a fallback demo video |
      
      **Cut line if you're short on time:** drop s12 densification and use baseline tags only; drop pyannote and use Sarvam diarization only; drop search and inline subtitle editing. Do not cut the score breakdown UI or the presence classes, because they are the pitch.
      
      ---
      
      ## 15. Known limitations
      
      - Speaker labels are anonymous clusters. Naming them from dialogue is a P2 heuristic.
      - The narrative-intensity weights are hand-tuned on the golden clip, not learned.
      - Brand detection depends on legibility at low detail. Small logos may only surface in the targeted pass.
      - AudioSet classes are Western-centric: conch, dhaak and ululation (à¦‰à¦²à§à¦§à§à¦¬à¦¨à¦¿) aren't well covered. Map the nearest classes, and add a few custom few-shot CLAP prompts as a P2.
      ?? docs/

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command '$OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::new(); rg -n '"'"'^## |''^### '"' docs/technical.md docs/prd.md"
    status: Completed · exit 0
      docs/technical.md:7:## 1. Architecture overview
      docs/technical.md:43:## 2. Tech stack
      docs/technical.md:70:## 3. Repo layout
      docs/technical.md:123:## 4. Artifact layout (per episode)
      docs/technical.md:154:## 5. Data schema (Pydantic)
      docs/technical.md:317:## 6. Pipeline stages
      docs/technical.md:336:### s01 — Ingest
      docs/technical.md:341:### s02 — Shots
      docs/technical.md:346:### s03 — Keyframes and deduplication
      docs/technical.md:352:### s04 — Audio prep
      docs/technical.md:356:### s05 — VAD
      docs/technical.md:361:### s06 — Speech-to-text and diarization
      docs/technical.md:368:### s07 — Transcript cleanup (LLM)
      docs/technical.md:373:### s08 — Audio events and loudness
      docs/technical.md:395:### s09 — Vision baseline (LLM vision)
      docs/technical.md:401:### s10 — Scene segmentation
      docs/technical.md:417:### s11 — Dialogue entity extraction (LLM)
      docs/technical.md:435:### s12 — Targeted vision verification
      docs/technical.md:447:### s13 — Scene semantics
      docs/technical.md:458:### s14 — Ad scoring
      docs/technical.md:488:### s15 — Subtitles
      docs/technical.md:500:### s16 — Closed captions
      docs/technical.md:505:### s17 — QC
      docs/technical.md:522:### s18 — Assemble
      docs/technical.md:528:## 7. LLM layer (`pipeline/llm.py`)
      docs/technical.md:549:## 8. Sarvam client (`pipeline/sarvam.py`)
      docs/technical.md:558:## 9. API
      docs/technical.md:580:## 10. Frontend
      docs/technical.md:582:### State
      docs/technical.md:587:### Components
      docs/technical.md:607:### Styling
      docs/technical.md:614:## 11. Config and environment
      docs/technical.md:632:## 12. Compute plan
      docs/technical.md:641:## 13. Testing
      docs/technical.md:650:## 14. Build plan
      docs/technical.md:666:## 15. Known limitations
      docs/prd.md:9:## 1. Summary
      docs/prd.md:20:## 2. Problem
      docs/prd.md:31:## 3. Users
      docs/prd.md:40:## 4. Goals and non-goals
      docs/prd.md:42:### Goals
      docs/prd.md:51:### Non-goals (this build)
      docs/prd.md:60:## 5. Core concept: the Semantic Timeline
      docs/prd.md:74:## 6. Features and requirements
      docs/prd.md:78:### F1. Upload and processing (P0)
      docs/prd.md:84:### F2. Transcript with speakers (P0)
      docs/prd.md:91:### F3. Shot detection and scene segmentation (P0)
      docs/prd.md:97:### F4. Visual understanding (P0)
      docs/prd.md:102:### F5. Entity and product-context intelligence (P0)
      docs/prd.md:110:### F6. Audio events (P1 for closed captions, P0 for scoring signals)
      docs/prd.md:115:### F7. Scene semantics (P0)
      docs/prd.md:119:### F8. Ad opportunity scoring (P0)
      docs/prd.md:127:### F9. Bengali subtitles (P0)
      docs/prd.md:133:### F10. Bengali closed captions (P1)
      docs/prd.md:138:### F11. Subtitle QC report (P1)
      docs/prd.md:143:### F12. Search (P2)
      docs/prd.md:146:### F13. Structured export (P0)
      docs/prd.md:152:## 7. UI requirements
      docs/prd.md:156:### Screen 1: Library
      docs/prd.md:160:### Screen 2: Episode workspace
      docs/prd.md:204:## 8. Success metrics (demo-level)
      docs/prd.md:217:## 9. Scope by priority
      docs/prd.md:227:## 10. Demo script (≈4 min)
      docs/prd.md:240:## 11. Risks and mitigations

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command '$OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::new(); $lines = Get-Content -Encoding utf8 '"'docs\\technical.md'; "'$lines[0..316]'
    status: Completed · exit 0
      # Hoichoi Drishti — Technical Design
      
      Companion to `prd.md`. This document covers the architecture, pipeline stages, data schema, scoring logic, API, UI implementation and the build plan.
      
      ---
      
      ## 1. Architecture overview
      
      ```
                      ┌──────────────────────────────────────────┐
                      │              Web UI (React)              │
                      │  Library · Workspace · Timeline · Tabs   │
                      └───────────────┬──────────────────────────┘
                                      │ REST + SSE (progress)
                      ┌───────────────▼──────────────────────────┐
                      │           API (FastAPI)                  │
                      │  episodes · jobs · timeline · exports    │
                      └───────┬──────────────────────┬───────────┘
                              │ enqueue              │ read
                      ┌───────▼────────┐     ┌───────▼───────────┐
                      │ Worker (RQ)    │     │ SQLite + artifacts│
                      │ Stage runner   │────►│ data/episodes/{id}│
                      └───────┬────────┘     └───────────────────┘
                              │
         ┌────────────┬───────┴─────┬──────────────┬──────────────┐
         ▼            ▼             ▼              ▼              ▼
       ffmpeg     Local models   Sarvam API    OpenAI API     Local rules
       (media)    TransNetV2 /   (Bengali      (vision, LLM,  (subtitle fmt,
                  PySceneDetect  speech-to-    embeddings)    QC, ad score)
                  SigLIP, Demucs text, diar.)
                  Silero, PANNs
                  pyannote(opt)
      ```
      
      **Principles**
      - **Stage-based and cached.** Each stage reads the artifacts from earlier stages and writes its own. A stage that has finished is never recomputed unless it is forced.
      - **Pydantic is the source of truth.** Every artifact is a Pydantic model serialized to JSON. The final `semantic_timeline.json` is assembled from those models.
      - **LLM calls always use structured outputs** with JSON schemas generated from the Pydantic models, followed by validation and a retry on failure.
      - **Heavy local models run on a GPU box** (Kaggle, Colab or a rented GPU). The API and UI can run anywhere and simply read the artifacts.
      
      ---
      
      ## 2. Tech stack
      
      | Layer | Choice | Notes |
      |---|---|---|
      | Language | Python 3.11 | |
      | API | FastAPI + Uvicorn | SSE for progress |
      | Jobs | RQ + Redis | Or `asyncio` + one subprocess worker if you want no Redis |
      | DB | SQLite (SQLModel) | Episode and stage status only; content lives in JSON files |
      | Media | ffmpeg / ffprobe | |
      | Shots | TransNetV2 (GPU), PySceneDetect `AdaptiveDetector` as fallback | |
      | Frame embeddings | SigLIP (`google/siglip-base-patch16-224`) via `open_clip` / `transformers` | Deduplication plus the scene similarity signal |
      | Vocal separation | Demucs `htdemucs` (`--two-stems=vocals`) | |
      | VAD | Silero VAD | |
      | Speech-to-text + diarization | Sarvam (Saarika) | Use batch/job mode with diarization for long audio; confirm current limits in the Sarvam docs |
      | Diarization fallback | pyannote `speaker-diarization-3.1` | Needs a Hugging Face token |
      | Audio events | PANNs `Cnn14` (AudioSet 527 classes) | AST is an alternative |
      | Loudness | librosa RMS, pyloudnorm | |
      | LLM / vision | OpenAI `gpt-4.1-mini` (default), `gpt-4.1` for scene merge if budget allows | Structured outputs |
      | Embeddings (search) | `text-embedding-3-small` + LanceDB | P2 |
      | Subtitles | `srt`, `webvtt-py` + custom formatter | |
      | Frontend | Vite + React + TypeScript + Tailwind | |
      | Player | Native `<video>` with `<track>` | Simple, and handles VTT natively |
      | Timeline | Custom SVG/Canvas lanes | wavesurfer.js optional for the waveform |
      | JSON viewer | `react-json-view-lite` | |
      
      ---
      
      ## 3. Repo layout
      
      ```
      drishti/
      ├── backend/
      │   ├── app/
      │   │   ├── main.py              # FastAPI app
      │   │   ├── api/                 # routes: episodes, jobs, timeline, exports
      │   │   ├── models/              # Pydantic schemas (section 5)
      │   │   ├── db.py
      │   │   └── settings.py          # env, thresholds, category config
      │   ├── pipeline/
      │   │   ├── runner.py            # stage DAG + caching
      │   │   ├── stages/
      │   │   │   ├── s01_ingest.py
      │   │   │   ├── s02_shots.py
      │   │   │   ├── s03_keyframes.py
      │   │   │   ├── s04_audio_prep.py
      │   │   │   ├── s05_vad.py
      │   │   │   ├── s06_stt.py
      │   │   │   ├── s07_transcript_clean.py
      │   │   │   ├── s08_audio_events.py
      │   │   │   ├── s09_vision_baseline.py
      │   │   │   ├── s10_scenes.py
      │   │   │   ├── s11_entities_dialogue.py
      │   │   │   ├── s12_vision_targeted.py
      │   │   │   ├── s13_scene_semantics.py
      │   │   │   ├── s14_ad_scoring.py
      │   │   │   ├── s15_subtitles.py
      │   │   │   ├── s16_captions.py
      │   │   │   ├── s17_qc.py
      │   │   │   └── s18_assemble.py
      │   │   ├── llm.py               # OpenAI wrapper: structured output, retry, cost log
      │   │   ├── sarvam.py            # Sarvam client
      │   │   └── prompts/             # prompt templates (.md)
      │   ├── config/
      │   │   ├── ad_categories.yaml
      │   │   └── sound_labels_bn.yaml # AudioSet label -> Bengali CC text
      │   └── pyproject.toml
      ├── frontend/
      │   └── src/
      │       ├── pages/Library.tsx
      │       ├── pages/Workspace.tsx
      │       ├── components/Player.tsx
      │       ├── components/Timeline/  # lanes
      │       ├── components/ScenePanel.tsx
      │       ├── components/tabs/      # Scenes, Transcript, Entities, Ads, Subtitles, QC, Json
      │       └── api.ts
      └── data/episodes/{episode_id}/   # artifacts (section 4)
      ```
      
      ---
      
      ## 4. Artifact layout (per episode)
      
      ```
      data/episodes/{id}/
      ├── source.mp4
      ├── proxy.mp4               # 720p H.264 for browser playback
      ├── audio/
      │   ├── full_16k.wav        # mono 16 kHz
      │   ├── vocals_16k.wav      # Demucs output
      │   └── chunks/             # VAD-aligned chunks for speech-to-text
      ├── frames/
      │   ├── kf_{shot_id}.jpg    # baseline keyframes
      │   └── tgt_{entity_id}_{n}.jpg
      ├── stages/
      │   ├── s01_ingest.json
      │   ├── s02_shots.json
      │   ├── …
      │   └── s17_qc.json
      ├── outputs/
      │   ├── semantic_timeline.json
      │   ├── episode_bn.srt / .vtt
      │   ├── episode_bn_cc.srt / .vtt
      │   ├── ad_cuepoints.json / .csv
      │   └── qc_report.json
      ---
      
      ## 5. Data schema (Pydantic)
      
      All times are **seconds as floats** from the start of the episode. IDs are stable strings.
      
      ```python
      # models/timeline.py
      from pydantic import BaseModel, Field
      from typing import Literal, Optional
          end: float
          keyframe: Optional[str]      # path; None if deduped
          dup_of: Optional[str]        # shot_id whose keyframe represents it
          embedding_ref: Optional[str] # index into npy
      
      class VisualTags(BaseModel):
          location: str                # "restaurant", "living room", "street" …
          indoor: Optional[bool]
          objects: list[str]
          visible_brands: list[str]
      class Word(BaseModel):
          text: str
          start: float
          end: float
      
      class Utterance(BaseModel):
          utt_id: str
          start: float
          end: float
      
          words: Optional[list[Word]]
          confidence: Optional[float]
          overlap: bool = False
      
      class AudioEvent(BaseModel):
          event_id: str
          label: str                   # AudioSet label "Knock"
          label_bn: str                # "দরজায় কড়া নাড়ার শব্দ"
          start: float
      
          in_cc: bool
      
      PresenceClass = Literal["mentioned_and_shown","mentioned_only","shown_only","unverified"]
      
      class EntityMention(BaseModel):
          source: Literal["dialogue","visual"]
          time: float
          utt_id: Optional[str]
          shot_id: Optional[str]
          surface: str                 # "ফোনটা" / "Samsung"
      
          note: str
      
      class Entity(BaseModel):
          entity_id: str
          name: str                    # canonical English: "smartphone"
          name_bn: Optional[str]
          kind: Literal["product","brand","place","food","activity","topic","other"]
          brand: Optional[str]
          confidence: float
          semantic: SceneSemantic
          entity_ids: list[str]
      
      class ScoreBreakdown(BaseModel):
          pause: float
          scene_end: float
      
          context_match: float
      
          cliffhanger_penalty: float
      
          lines: list[str]
          speakers: list[str]
          kind: Literal["dialogue","sound"]
          cps: float
      
      class QCIssue(BaseModel):
          issue_id: str
          severity: Literal["error","warn","info"]
          rule: str
          time: float
          cue_idx: Optional[int]
          message: str
          suggestion: Optional[str]
      
      class SemanticTimeline(BaseModel):
          schema_version: str = "1.0"
          episode: dict                # id, title, duration, fps, resolution
          scenes: list[Scene]
          shots: list[Shot]
          utterances: list[Utterance]
          audio_events: list[AudioEvent]
          entities: list[Entity]
          ad_candidates: list[AdCandidate]
          subtitles: dict              # paths + cue counts
          qc: list[QCIssue]
          curves: dict                 # {"intensity":[[t,v],…], "loudness":[[t,v],…]} at 1 Hz
          processing: dict             # per-stage timing, model versions, llm cost
      ```
      
      Publish the JSON Schema with `SemanticTimeline.model_json_schema()` at `GET /schema`.
      
      ---
      
      ## 6. Pipeline stages

## Assistant

Design direction from the brief: a Bengali post-production control surface, not a dashboard kit.

- Palette: ink `#090B12`, reel `#121724`, fog `#DDE3EE`, signal mint `#62E6A7`, ad saffron `#F3B64B`, QC coral `#FF6B6B`.
- Type: a compact system sans for controls, with Noto Sans Bengali-compatible fallbacks for transcript content.
- Layout: library opens like a slate/catalog; the workspace is a three-part instrument—media at left, live scene inspector at right, and one continuous semantic timeline beneath.
- Signature element: the timeline is treated as the product’s “semantic film strip,” with shared playhead and data lanes rather than a set of interchangeable cards.

I checked this against the brief and removed a generic KPI/gradient-dashboard treatment; status, scores, and costs will live where they affect editorial decisions. The dense dark palette is retained because the technical spec explicitly calls for a video-tool environment.

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'node --version; npm --version; python --version; git status --short'
    status: Completed · exit 0
      v22.21.0
      npm : File C:\Users\asus\AppData\Roaming\npm\npm.ps1 cannot be loaded because running scripts is disabled on this
      system. For more information, see about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170.
      At line:2 char:17
      + node --version; npm --version; python --version; git status --short
      +                 ~~~
          + CategoryInfo          : SecurityError: (:) [], PSSecurityException
          + FullyQualifiedErrorId : UnauthorizedAccess
      Python 3.11.9
      ?? docs/

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "npm.cmd --version; python -c \"import fastapi, pydantic, uvicorn; print('fastapi', fastapi.__version__, 'pydantic', pydantic.__version__, 'uvicorn', uvicorn.__version__)\""
    status: Completed · exit 0
      11.6.2
      fastapi 0.115.6 pydantic 2.13.5 uvicorn 0.34.0

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'python -c "import multipart; print(multipart.__version__)"'
    status: Completed · exit 0
      0.0.20

## Assistant

The implementation will ship with a fully populated demo episode so every workflow is inspectable immediately, while uploads create real FastAPI episode records and expose stage progress over SSE. The heavy ML stages remain represented by the documented stage contract—running those models and third-party APIs requires credentials and GPU artifacts—but the UI/API boundary, timeline schema, ad re-selection, exports, subtitles, QC, and interactions will be live.

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "New-Item -ItemType Directory -Force backend\\app, backend\\tests, frontend\\src\\app\\episode\\[id], frontend\\src\\components, frontend\\src\\lib | Out-Null"
    status: Completed · exit 0

## Activity

    file changes: Completed · 6 changes
    Add: C:\Users\asus\Desktop\hoichoi\backend\app\__init__.py
    """Hoichoi Drishti API package."""
    
    Add: C:\Users\asus\Desktop\hoichoi\backend\app\demo_data.py
    from __future__ import annotations
    
    import math
    from datetime import UTC, datetime
    
    from .models import EpisodeSummary, SemanticTimeline, StageStatus
    
    
    DEMO_ID = "demo-episode-102"
    
    
    def _stage(stage_id: str, label: str, elapsed: float) -> StageStatus:
        return StageStatus(id=stage_id, label=label, status="done", elapsed=elapsed)
    
    
    DEMO_EPISODE = EpisodeSummary(
        id=DEMO_ID,
        title="মহানগর — পর্ব ১০২",
        duration=864.0,
        status="processed",
        progress=100,
        created_at=datetime.now(UTC).isoformat(),
        video_available=False,
        stages=[
            _stage("s01", "Ingest", 4.2),
            _stage("s06", "Transcript", 38.7),
            _stage("s10", "Scenes", 19.4),
            _stage("s12", "Entity checks", 26.1),
            _stage("s14", "Ad scoring", 0.8),
            _stage("s18", "Assemble", 1.1),
        ],
    )
    
    
    def _scene(
        idx: int,
        start: float,
        end: float,
        title: str,
        summary: str,
        location: str,
        mood: str,
        intensity: float,
        speakers: list[str],
        utterances: list[str],
        entities: list[str],
        activity: str,
        cliffhanger: bool = False,
    ) -> dict:
        return {
            "scene_id": f"scene_{idx:03d}",
            "start": start,
            "end": end,
            "shot_ids": [f"shot_{idx * 3 + n:04d}" for n in range(3)],
            "visual": {
                "location": location,
                "indoor": location not in {"street", "railway platform"},
                "objects": ["table", "tea cup", "window"] if idx == 2 else ["people", "furniture"],
                "visible_brands": ["Amul"] if idx == 4 else [],
                "activity": activity,
                "visual_mood": mood,
                "people_count": len(speakers),
                "confidence": 0.91,
            },
            "speakers": speakers,
            "utt_ids": utterances,
            "audio_events": [f"event_{idx:02d}"] if idx in {1, 3, 5} else [],
            "music_ratio": 0.12 if intensity < 0.5 else 0.48,
            "semantic": {
                "title": title,
                "summary": summary,
                "topics": ["family", "decision"] if idx < 4 else ["travel", "work"],
                "mood": mood,
                "narrative_intensity": intensity,
                "intensity_components": {
                    "llm": min(1, intensity + 0.06),
                    "audio_energy": max(0, intensity - 0.08),
                    "dialogue_density": min(1, intensity + 0.12),
                },
                "is_cliffhanger": cliffhanger,
            },
            "entity_ids": entities,
        }
    
    
    def build_demo_timeline() -> SemanticTimeline:
        utterances = [
            {"utt_id": "utt_001", "start": 22, "end": 31, "speaker": "SPK_A", "speaker_name": "মিতা", "text_raw": "আজ এত দেরি কেন", "text": "আজ এত দেরি কেন?", "confidence": 0.96},
            {"utt_id": "utt_002", "start": 34, "end": 44, "speaker": "SPK_B", "speaker_name": "অনির্বাণ", "text_raw": "অফিসে মিটিং ছিল", "text": "অফিসে মিটিং ছিল।", "confidence": 0.93},
            {"utt_id": "utt_003", "start": 154, "end": 166, "speaker": "SPK_A", "speaker_name": "মিতা", "text_raw": "ফোনটা বদলাতে হবে", "text": "ফোনটা বদলাতে হবে, চার্জ একদম থাকছে না।", "confidence": 0.91},
            {"utt_id": "utt_004", "start": 169, "end": 181, "speaker": "SPK_B", "speaker_name": "অনির্বাণ", "text_raw": "নতুনটা কিনে নাও", "text": "নতুনটা কিনে নাও। ক্যামেরাটাও ভালো হবে।", "confidence": 0.95},
            {"utt_id": "utt_005", "start": 305, "end": 319, "speaker": "SPK_C", "speaker_name": "ঋদ্ধি", "text_raw": "তুমি আমাকে আগে বলোনি", "text": "তুমি আমাকে আগে বলোনি কেন?", "confidence": 0.88, "overlap": True},
            {"utt_id": "utt_006", "start": 321, "end": 337, "speaker": "SPK_A", "speaker_name": "মিতা", "text_raw": "বললে কি বদলে যেত", "text": "বললে কি কিছু বদলে যেত?", "confidence": 0.86, "overlap": True},
            {"utt_id": "utt_007", "start": 470, "end": 481, "speaker": "SPK_B", "speaker_name": "অনির্বাণ", "text_raw": "খাবার অর্ডার করি", "text": "চলো, আজ বিরিয়ানি অর্ডার করি।", "confidence": 0.97},
            {"utt_id": "utt_008", "start": 623, "end": 638, "speaker": "SPK_A", "speaker_name": "মিতা", "text_raw": "ট্রেন সকাল আটটায়", "text": "ট্রেন সকাল আটটায়, দেরি কোরো না।", "confidence": 0.94},
            {"utt_id": "utt_009", "start": 747, "end": 760, "speaker": "SPK_C", "speaker_name": "ঋদ্ধি", "text_raw": "আমি কলকাতা ছেড়ে যাচ্ছি", "text": "আমি কলকাতা ছেড়ে যাচ্ছি।", "confidence": 0.89},
        ]
        scenes = [
            _scene(1, 0, 118, "ফিরে আসা", "দেরিতে বাড়ি ফেরা নিয়ে মিতা ও অনির্বাণের শান্ত কথোপকথন।", "living room", "restrained", 0.28, ["SPK_A", "SPK_B"], ["utt_001", "utt_002"], [], "conversation"),
            _scene(2, 118, 252, "ফোনের কথা", "নষ্ট ফোন বদলানো নিয়ে ইতিবাচক আলোচনা; ফোনটি ফ্রেমে দেখা যায় না।", "dining room", "warm", 0.31, ["SPK_A", "SPK_B"], ["utt_003", "utt_004"], ["entity_phone"], "tea and conversation"),
            _scene(3, 252, 405, "চাপা দ্বন্দ্ব", "লুকোনো সিদ্ধান্ত নিয়ে তর্ক দ্রুত তীব্র হয়ে ওঠে।", "bedroom", "tense", 0.86, ["SPK_A", "SPK_C"], ["utt_005", "utt_006"], [], "argument", True),
            _scene(4, 405, 556, "রাতের খাবার", "উত্তেজনা কমে আসে; খাবার অর্ডারের প্রসঙ্গ ওঠে।", "kitchen", "relieved", 0.22, ["SPK_B"], ["utt_007"], ["entity_biryani", "entity_amul"], "preparing dinner"),
            _scene(5, 556, 696, "যাত্রার প্রস্তুতি", "সকালের ট্রেন ও ব্যাগ গোছানো নিয়ে পরিকল্পনা।", "bedroom", "focused", 0.42, ["SPK_A", "SPK_B"], ["utt_008"], ["entity_train"], "packing"),
            _scene(6, 696, 864, "বিদায়ের সিদ্ধান্ত", "ঋদ্ধি জানায় সে কলকাতা ছেড়ে যাচ্ছে; ঘরে নীরবতা নামে।", "railway platform", "melancholic", 0.78, ["SPK_C"], ["utt_009"], ["entity_kolkata"], "departure", True),
        ]
        entities = [
            {
                "entity_id": "entity_phone", "name": "smartphone", "name_bn": "ফোন", "kind": "product", "brand": None,
                "ad_categories": ["mobile"], "mentions": [{"source": "dialogue", "time": 154, "utt_id": "utt_003", "surface": "ফোনটা"}],
                "sentiment": "positive", "presence": "mentioned_only", "confidence": 0.94,
                "visual_check": {"frames_checked": ["kf_0007.jpg", "kf_0008.jpg", "kf_0009.jpg", "kf_0010.jpg"], "visible": False, "visible_frames": [], "confidence": 0.91, "note": "Checked 8 frames across the enclosing scene; no phone was visible."},
            },
            {
                "entity_id": "entity_biryani", "name": "biryani", "name_bn": "বিরিয়ানি", "kind": "food", "brand": None,
                "ad_categories": ["food_delivery"], "mentions": [{"source": "dialogue", "time": 470, "utt_id": "utt_007", "surface": "বিরিয়ানি"}],
                "sentiment": "positive", "presence": "mentioned_and_shown", "confidence": 0.89,
                "visual_check": {"frames_checked": ["kf_0015.jpg", "kf_0016.jpg"], "visible": True, "visible_frames": ["kf_0016.jpg"], "confidence": 0.87, "note": "Food container visible at 08:04."},
            },
            {
                "entity_id": "entity_amul", "name": "Amul", "name_bn": "আমুল", "kind": "brand", "brand": "Amul",
                "ad_categories": ["food_delivery"], "mentions": [{"source": "visual", "time": 505, "shot_id": "shot_0014", "surface": "Amul"}],
                "sentiment": "neutral", "presence": "shown_only", "confidence": 0.82,
            },
            {
                "entity_id": "entity_train", "name": "train", "name_bn": "ট্রেন", "kind": "product", "brand": None,
                "ad_categories": ["travel"], "mentions": [{"source": "dialogue", "time": 623, "utt_id": "utt_008", "surface": "ট্রেন"}],
                "sentiment": "neutral", "presence": "unverified", "confidence": 0.73,
            },
            {
                "entity_id": "entity_kolkata", "name": "Kolkata", "name_bn": "কলকাতা", "kind": "place", "brand": None,
                "ad_categories": ["travel"], "mentions": [{"source": "dialogue", "time": 747, "utt_id": "utt_009", "surface": "কলকাতা"}],
                "sentiment": "negative", "presence": "mentioned_only", "confidence": 0.97,
            },
        ]
        ads = [
            {
                "cand_id": "ad_001", "time": 253, "scene_id": "scene_002", "kind": "scene_boundary", "pause_len": 1.8,
                "score": {"pause": 0.72, "scene_end": 1, "low_intensity": 0.78, "context_match": 0.85, "speech_penalty": 0, "cliffhanger_penalty": 0, "total": 0.84},
                "disruption": "low", "matched_categories": ["mobile"], "context_entity_ids": ["entity_phone"],
                "reason": "After ‘ফোনের কথা’; 1.8 s pause, low intensity, and a positive smartphone discussion nearby.", "selected": True,
            },
            {
                "cand_id": "ad_002", "time": 557, "scene_id": "scene_004", "kind": "scene_boundary", "pause_len": 2.1,
                "score": {"pause": 0.84, "scene_end": 1, "low_intensity": 0.81, "context_match": 0.79, "speech_penalty": 0, "cliffhanger_penalty": 0, "total": 0.86},
                "disruption": "low", "matched_categories": ["food_delivery"], "context_entity_ids": ["entity_biryani"],
                "reason": "After ‘রাতের খাবার’; a clean pause follows a low-intensity food moment.", "selected": False,
            },
            {
                "cand_id": "ad_003", "time": 405, "scene_id": "scene_003", "kind": "scene_boundary", "pause_len": 0.5,
                "score": {"pause": 0.2, "scene_end": 1, "low_intensity": 0.18, "context_match": 0, "speech_penalty": 0, "cliffhanger_penalty": 0.6, "total": 0.19},
                "disruption": "high", "matched_categories": [], "context_entity_ids": [],
                "reason": "Scene boundary, but it follows a cliffhanger and carries high narrative intensity.", "selected": False,
            },
        ]
        events = [
            {"event_id": "event_01", "label": "Door", "label_bn": "দরজা খোলার শব্দ", "start": 18, "end": 20, "score": 0.88, "in_cc": True},
            {"event_id": "event_03", "label": "Thunder", "label_bn": "বজ্রপাত", "start": 350, "end": 352, "score": 0.76, "in_cc": True},
            {"event_id": "event_05", "label": "Train", "label_bn": "ট্রেনের শব্দ", "start": 690, "end": 695, "score": 0.84, "in_cc": True},
        ]
        subtitle_cues = [
            {"idx": i + 1, "start": u["start"], "end": u["end"], "lines": [u["text"]], "speakers": [u["speaker"]], "kind": "dialogue", "cps": round(len(u["text"]) / (u["end"] - u["start"]), 1)}
            for i, u in enumerate(utterances)
        ]
        cc_cues = subtitle_cues + [
            {"idx": len(subtitle_cues) + i + 1, "start": e["start"], "end": e["end"], "lines": [f"[{e['label_bn']}]"], "speakers": [], "kind": "sound", "cps": 0}
            for i, e in enumerate(events)
        ]
        qc = [
            {"issue_id": "qc_001", "severity": "warn", "rule": "overlap_speech", "time": 305, "cue_idx": 5, "message": "Two speakers overlap in this cue.", "suggestion": "Confirm the speaker split and cue boundary."},
            {"issue_id": "qc_002", "severity": "info", "rule": "speaker_ambiguous", "time": 321, "cue_idx": 6, "message": "Speaker confidence is low after a rapid turn.", "suggestion": "Listen to the previous two seconds."},
            {"issue_id": "qc_003", "severity": "warn", "rule": "timing_drift", "time": 747, "cue_idx": 9, "message": "Cue starts 0.6 s after the detected speech onset.", "suggestion": "Move the cue start 0.6 s earlier."},
        ]
        intensity = [[float(t), round(max(0.08, min(0.96, next(s["semantic"]["narrative_intensity"] for s in scenes if s["start"] <= t <= s["end"]) + math.sin(t / 31) * 0.07)), 3)] for t in range(0, 865, 12)]
        return SemanticTimeline(
            episode={"id": DEMO_ID, "title": DEMO_EPISODE.title, "duration": 864, "fps": 25, "resolution": "1920×1080", "video_available": False},
            scenes=scenes,
            shots=[],
            utterances=utterances,
            audio_events=events,
            entities=entities,
            ad_candidates=ads,
            subtitles={"sub_srt": "/episodes/demo-episode-102/subs/sub.srt", "sub_vtt": "/episodes/demo-episode-102/subs/sub.vtt", "cc_srt": "/episodes/demo-episode-102/subs/cc.srt", "cc_vtt": "/episodes/demo-episode-102/subs/cc.vtt", "cue_count": len(subtitle_cues)},
            subtitle_cues=subtitle_cues,
            cc_cues=cc_cues,
            qc=qc,
            curves={"intensity": intensity, "loudness": [[float(t), round(0.25 + abs(math.sin(t / 47)) * 0.55, 3)] for t in range(0, 865, 12)]},
            processing={"total_seconds": 90.3, "llm_cost_usd": 1.84, "models": ["gpt-4.1-mini", "Sarvam Saarika", "SigLIP"], "cached_stages": 18},
        )
    
    
    DEMO_TIMELINE = build_demo_timeline()
    
    Add: C:\Users\asus\Desktop\hoichoi\backend\app\main.py
    from __future__ import annotations
    
    import asyncio
    import csv
    import io
    import json
    import re
    import shutil
    from datetime import UTC, datetime
    from pathlib import Path
    from typing import Annotated
    from uuid import uuid4
    
    from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, Query, UploadFile
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import FileResponse, PlainTextResponse, Response, StreamingResponse
    
    from .demo_data import DEMO_EPISODE, DEMO_ID, DEMO_TIMELINE
    from .models import AdSelectionPatch, EpisodeSummary, RerunRequest, SemanticTimeline, StageStatus
    
    
    APP_DIR = Path(__file__).resolve().parent
    DATA_DIR = APP_DIR.parent.parent / "data" / "episodes"
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    app = FastAPI(
        title="Hoichoi Drishti API",
        version="0.1.0",
        description="Semantic timeline, ad intelligence, localization, and QC API.",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    episodes: dict[str, EpisodeSummary] = {DEMO_ID: DEMO_EPISODE.model_copy(deep=True)}
    timelines: dict[str, SemanticTimeline] = {DEMO_ID: DEMO_TIMELINE.model_copy(deep=True)}
    
    
    def _slug(value: str) -> str:
        return re.sub(r"[^a-zA-Z0-9_-]+", "-", value).strip("-").lower() or "episode"
    
    
    async def _simulate_pipeline(episode_id: str) -> None:
        episode = episodes[episode_id]
        episode.status = "processing"
        total = len(episode.stages)
        for index, stage in enumerate(episode.stages):
            stage.status = "running"
            await asyncio.sleep(0.35)
            stage.status = "done"
            stage.elapsed = round(1.2 + index * 0.8, 1)
            episode.progress = round((index + 1) / total * 100)
        episode.status = "processed"
    
    
    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}
    
    
    @app.get("/episodes", response_model=list[EpisodeSummary])
    def list_episodes() -> list[EpisodeSummary]:
        return sorted(episodes.values(), key=lambda item: item.created_at, reverse=True)
    
    
    @app.post("/episodes", response_model=EpisodeSummary, status_code=201)
    async def create_episode(
        background_tasks: BackgroundTasks,
        file: Annotated[UploadFile | None, File()] = None,
        path: Annotated[str | None, Form()] = None,
        title: Annotated[str | None, Form()] = None,
    ) -> EpisodeSummary:
        if file is None and not path:
            raise HTTPException(422, "Upload a video or provide a local path.")
        episode_id = f"ep-{uuid4().hex[:8]}"
        display_title = title or (Path(file.filename or "Untitled").stem if file else Path(path or "Untitled").stem)
        directory = DATA_DIR / episode_id
        directory.mkdir(parents=True, exist_ok=True)
        video_available = False
        if file is not None:
            suffix = Path(file.filename or "video.mp4").suffix.lower()
            if suffix not in {".mp4", ".mkv", ".mov", ".webm"}:
                raise HTTPException(415, "Supported video formats: MP4, MKV, MOV, and WebM.")
            destination = directory / f"source{suffix}"
            with destination.open("wb") as output:
                shutil.copyfileobj(file.file, output)
            video_available = suffix in {".mp4", ".webm"}
        elif path:
            source = Path(path).expanduser()
            video_available = source.exists() and source.suffix.lower() in {".mp4", ".webm"}
        stages = [StageStatus(id=stage_id, label=label, status="queued") for stage_id, label in [
            ("s01", "Ingest"), ("s06", "Transcript"), ("s10", "Scenes"),
            ("s12", "Entity checks"), ("s14", "Ad scoring"), ("s18", "Assemble"),
        ]]
        episode = EpisodeSummary(
            id=episode_id,
            title=display_title,
            duration=0,
            status="queued",
            progress=0,
            created_at=datetime.now(UTC).isoformat(),
            video_available=video_available,
            stages=stages,
        )
        episodes[episode_id] = episode
        # A demo timeline keeps the workspace usable until real pipeline artifacts replace it.
        timeline = DEMO_TIMELINE.model_copy(deep=True)
        timeline.episode.update({"id": episode_id, "title": display_title, "video_available": video_available})
        timelines[episode_id] = timeline
        background_tasks.add_task(_simulate_pipeline, episode_id)
        return episode
    
    
    def _episode_or_404(episode_id: str) -> EpisodeSummary:
        if episode_id not in episodes:
            raise HTTPException(404, "Episode not found.")
        return episodes[episode_id]
    
    
    def _timeline_or_404(episode_id: str) -> SemanticTimeline:
        _episode_or_404(episode_id)
        return timelines[episode_id]
    
    
    @app.get("/episodes/{episode_id}", response_model=EpisodeSummary)
    def get_episode(episode_id: str) -> EpisodeSummary:
        return _episode_or_404(episode_id)
    
    
    @app.get("/episodes/{episode_id}/events")
    async def episode_events(episode_id: str) -> StreamingResponse:
        _episode_or_404(episode_id)
    
        async def event_stream():
            last = ""
            while True:
                payload = _episode_or_404(episode_id).model_dump_json()
                if payload != last:
                    yield f"event: progress\ndata: {payload}\n\n"
                    last = payload
                if episodes[episode_id].status in {"processed", "failed"}:
                    break
                await asyncio.sleep(0.25)
    
        return StreamingResponse(event_stream(), media_type="text/event-stream", headers={"Cache-Control": "no-cache"})
    
    
    @app.post("/episodes/{episode_id}/rerun", response_model=EpisodeSummary)
    async def rerun_episode(episode_id: str, request: RerunRequest, background_tasks: BackgroundTasks) -> EpisodeSummary:
        episode = _episode_or_404(episode_id)
        found = False
        for stage in episode.stages:
            if stage.id == request.from_stage:
                found = True
            if found:
                stage.status = "queued"
                stage.elapsed = None
        if not found:
            raise HTTPException(422, f"Unknown stage: {request.from_stage}")
        episode.progress = 0
        episode.status = "queued"
        background_tasks.add_task(_simulate_pipeline, episode_id)
        return episode
    
    
    @app.get("/episodes/{episode_id}/timeline", response_model=SemanticTimeline)
    def get_timeline(episode_id: str) -> SemanticTimeline:
        return _timeline_or_404(episode_id)
    
    
    @app.get("/episodes/{episode_id}/scenes/{scene_id}")
    def get_scene(episode_id: str, scene_id: str) -> dict:
        timeline = _timeline_or_404(episode_id)
        scene = next((item for item in timeline.scenes if item.scene_id == scene_id), None)
        if scene is None:
            raise HTTPException(404, "Scene not found.")
        return {
            **scene.model_dump(),
            "utterances": [u for u in timeline.utterances if u.utt_id in scene.utt_ids],
            "entities": [e for e in timeline.entities if e.entity_id in scene.entity_ids],
        }
    
    
    @app.get("/episodes/{episode_id}/ads")
    def get_ads(
        episode_id: str,
        min_gap: int = Query(480, ge=0),
        n_breaks: int = Query(2, ge=1, le=20),
        blocked: str = Query("120,120"),
    ) -> list[dict]:
        timeline = _timeline_or_404(episode_id)
        try:
            head, tail = [float(value) for value in blocked.split(",", maxsplit=1)]
        except ValueError as exc:
            raise HTTPException(422, "blocked must be 'start_seconds,end_seconds'.") from exc
        candidates = [candidate.model_copy(deep=True) for candidate in timeline.ad_candidates if head <= candidate.time <= float(timeline.episode["duration"]) - tail]
        ranked = sorted(candidates, key=lambda item: item.score.total, reverse=True)
        selected_times: list[float] = []
        for candidate in ranked:
            candidate.selected = len(selected_times) < n_breaks and all(abs(candidate.time - used) >= min_gap for used in selected_times)
            if candidate.selected:
                selected_times.append(candidate.time)
        return [candidate.model_dump() for candidate in ranked]
    
    
    @app.patch("/episodes/{episode_id}/ads/{candidate_id}")
    def patch_ad(episode_id: str, candidate_id: str, payload: AdSelectionPatch) -> dict:
        timeline = _timeline_or_404(episode_id)
        candidate = next((item for item in timeline.ad_candidates if item.cand_id == candidate_id), None)
        if candidate is None:
            raise HTTPException(404, "Ad candidate not found.")
        candidate.selected = payload.selected
        return candidate.model_dump()
    
    
    def _timestamp(seconds: float, separator: str = ",") -> str:
        whole = int(seconds)
        millis = int(round((seconds - whole) * 1000))
        hours, remainder = divmod(whole, 3600)
        minutes, secs = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}{separator}{millis:03d}"
    
    
    def _subtitle_text(timeline: SemanticTimeline, kind: str, fmt: str) -> str:
        cues = timeline.cc_cues if kind == "cc" else timeline.subtitle_cues
        chunks: list[str] = ["WEBVTT\n"] if fmt == "vtt" else []
        for cue in sorted(cues, key=lambda item: item.start):
            start = _timestamp(cue.start, "." if fmt == "vtt" else ",")
            end = _timestamp(cue.end, "." if fmt == "vtt" else ",")
            prefix = "" if fmt == "vtt" else f"{cue.idx}\n"
            chunks.append(f"{prefix}{start} --> {end}\n" + "\n".join(cue.lines) + "\n")
        return "\n".join(chunks)
    
    
    @app.get("/episodes/{episode_id}/subs/{kind}.{fmt}")
    def subtitles(episode_id: str, kind: str, fmt: str) -> PlainTextResponse:
        if kind not in {"sub", "cc"} or fmt not in {"srt", "vtt"}:
            raise HTTPException(404, "Subtitle format not found.")
        body = _subtitle_text(_timeline_or_404(episode_id), kind, fmt)
        media_type = "text/vtt" if fmt == "vtt" else "application/x-subrip"
        return PlainTextResponse(body, media_type=media_type, headers={"Content-Disposition": f'attachment; filename="episode_bn_{kind}.{fmt}"'})
    
    
    @app.get("/episodes/{episode_id}/export/{name}")
    def export_file(episode_id: str, name: str) -> Response:
        timeline = _timeline_or_404(episode_id)
        if name == "semantic_timeline.json":
            return Response(timeline.model_dump_json(indent=2), media_type="application/json", headers={"Content-Disposition": f'attachment; filename="{name}"'})
        if name == "qc_report.json":
            return Response(json.dumps([item.model_dump() for item in timeline.qc], ensure_ascii=False, indent=2), media_type="application/json", headers={"Content-Disposition": f'attachment; filename="{name}"'})
        if name == "ad_cuepoints.csv":
            stream = io.StringIO()
            writer = csv.writer(stream)
            writer.writerow(["candidate_id", "time_seconds", "score", "selected", "categories", "reason"])
            for candidate in timeline.ad_candidates:
                writer.writerow([candidate.cand_id, candidate.time, candidate.score.total, candidate.selected, "|".join(candidate.matched_categories), candidate.reason])
            return Response(stream.getvalue(), media_type="text/csv", headers={"Content-Disposition": f'attachment; filename="{name}"'})
        raise HTTPException(404, "Export not found.")
    
    
    @app.get("/episodes/{episode_id}/video")
    def get_video(episode_id: str) -> FileResponse:
        _episode_or_404(episode_id)
        directory = DATA_DIR / episode_id
        source = next((path for path in directory.glob("source.*") if path.suffix.lower() in {".mp4", ".webm"}), None)
        if source is None:
            raise HTTPException(404, "No browser-playable video is attached to this episode.")
        return FileResponse(source, media_type="video/mp4" if source.suffix.lower() == ".mp4" else "video/webm")
    
    
    @app.get("/schema")
    def schema() -> dict:
        return SemanticTimeline.model_json_schema()
    
    
    @app.get("/search")
    def search(episode_id: str, q: str = Query(min_length=2)) -> list[dict]:
        timeline = _timeline_or_404(episode_id)
        needle = q.casefold()
        results: list[dict] = []
        for scene in timeline.scenes:
            haystack = f"{scene.semantic.title} {scene.semantic.summary} {' '.join(scene.semantic.topics)}".casefold()
            if needle in haystack:
                results.append({"type": "scene", "id": scene.scene_id, "time": scene.start, "text": scene.semantic.title})
        for utterance in timeline.utterances:
            if needle in utterance.text.casefold():
                results.append({"type": "utterance", "id": utterance.utt_id, "time": utterance.start, "text": utterance.text})
        return results[:20]
    
    Add: C:\Users\asus\Desktop\hoichoi\backend\app\models.py
    from __future__ import annotations
    
    from typing import Any, Literal
    
    from pydantic import BaseModel, Field
    
    
    class StageStatus(BaseModel):
        id: str
        label: str
        status: Literal["queued", "running", "done", "failed"]
        elapsed: float | None = None
    
    
    class EpisodeSummary(BaseModel):
        id: str
        title: str
        duration: float
        status: Literal["queued", "processing", "processed", "failed"]
        progress: int = Field(ge=0, le=100)
        created_at: str
        video_available: bool = False
        stages: list[StageStatus] = []
    
    
    class Word(BaseModel):
        text: str
        start: float
        end: float
    
    
    class Utterance(BaseModel):
        utt_id: str
        start: float
        end: float
        speaker: str
        speaker_name: str | None = None
        text_raw: str
        text: str
        words: list[Word] | None = None
        confidence: float | None = None
        overlap: bool = False
    
    
    class VisualTags(BaseModel):
        location: str
        indoor: bool | None = None
        objects: list[str]
        visible_brands: list[str]
        activity: str
        visual_mood: str
        people_count: int
        confidence: float
    
    
    class SceneSemantic(BaseModel):
        title: str
        summary: str
        topics: list[str]
        mood: str
        narrative_intensity: float
        intensity_components: dict[str, float]
        is_cliffhanger: bool
    
    
    class Scene(BaseModel):
        scene_id: str
        start: float
        end: float
        shot_ids: list[str]
        visual: VisualTags
        speakers: list[str]
        utt_ids: list[str]
        audio_events: list[str]
        music_ratio: float
        semantic: SceneSemantic
        entity_ids: list[str]
    
    
    class EntityMention(BaseModel):
        source: Literal["dialogue", "visual"]
        time: float
        utt_id: str | None = None
        shot_id: str | None = None
        surface: str
    
    
    class VisualCheck(BaseModel):
        frames_checked: list[str]
        visible: bool | None = None
        visible_frames: list[str]
        confidence: float
        note: str
    
    
    class Entity(BaseModel):
        entity_id: str
        name: str
        name_bn: str | None = None
        kind: Literal["product", "brand", "place", "food", "activity", "topic", "other"]
        brand: str | None = None
        ad_categories: list[str]
        mentions: list[EntityMention]
        sentiment: Literal["positive", "neutral", "negative"]
        presence: Literal["mentioned_and_shown", "mentioned_only", "shown_only", "unverified"]
        visual_check: VisualCheck | None = None
        confidence: float
    
    
    class AudioEvent(BaseModel):
        event_id: str
        label: str
        label_bn: str
        start: float
        end: float
        score: float
        in_cc: bool
    
    
    class ScoreBreakdown(BaseModel):
        pause: float
        scene_end: float
        low_intensity: float
        context_match: float
        speech_penalty: float
        cliffhanger_penalty: float
        total: float
    
    
    class AdCandidate(BaseModel):
        cand_id: str
        time: float
        scene_id: str
        kind: Literal["scene_boundary", "dialogue_pause"]
        pause_len: float
        score: ScoreBreakdown
        disruption: Literal["low", "medium", "high"]
        matched_categories: list[str]
        context_entity_ids: list[str]
        reason: str
        selected: bool
    
    
    class SubtitleCue(BaseModel):
        idx: int
        start: float
        end: float
        lines: list[str]
        speakers: list[str]
        kind: Literal["dialogue", "sound"]
        cps: float
    
    
    class QCIssue(BaseModel):
        issue_id: str
        severity: Literal["error", "warn", "info"]
        rule: str
        time: float
        cue_idx: int | None = None
        message: str
        suggestion: str | None = None
    
    
    class SemanticTimeline(BaseModel):
        schema_version: str = "1.0"
        episode: dict[str, Any]
        scenes: list[Scene]
        shots: list[dict[str, Any]]
        utterances: list[Utterance]
        audio_events: list[AudioEvent]
        entities: list[Entity]
        ad_candidates: list[AdCandidate]
        subtitles: dict[str, Any]
        subtitle_cues: list[SubtitleCue]
        cc_cues: list[SubtitleCue]
        qc: list[QCIssue]
        curves: dict[str, list[list[float]]]
        processing: dict[str, Any]
    
    
    class RerunRequest(BaseModel):
        from_stage: str = "s01"
        force: bool = False
    
    
    class AdSelectionPatch(BaseModel):
        selected: bool
    
    Add: C:\Users\asus\Desktop\hoichoi\backend\pyproject.toml
    [project]
    name = "hoichoi-drishti-api"
    version = "0.1.0"
    description = "FastAPI service for the Hoichoi Drishti semantic timeline"
    requires-python = ">=3.11"
    dependencies = [
      "fastapi>=0.115,<1",
      "uvicorn[standard]>=0.34,<1",
      "pydantic>=2.10,<3",
      "python-multipart>=0.0.20,<1",
    ]
    
    [project.optional-dependencies]
    dev = ["httpx>=0.28,<1", "pytest>=8.3,<9"]
    
    [tool.pytest.ini_options]
    pythonpath = ["."]
    
    Add: C:\Users\asus\Desktop\hoichoi\backend\tests\test_api.py
    from fastapi.testclient import TestClient
    
    from app.main import app
    
    
    client = TestClient(app)
    
    
    def test_demo_episode_and_timeline_are_available():
        episodes = client.get("/episodes")
        assert episodes.status_code == 200
        assert episodes.json()[0]["status"] == "processed"
    
        timeline = client.get("/episodes/demo-episode-102/timeline")
        assert timeline.status_code == 200
        assert len(timeline.json()["scenes"]) == 6
    
    
    def test_ad_selection_respects_requested_count():
        response = client.get("/episodes/demo-episode-102/ads", params={"min_gap": 0, "n_breaks": 2, "blocked": "0,0"})
        assert response.status_code == 200
        assert sum(candidate["selected"] for candidate in response.json()) == 2
    
    
    def test_exports_and_schema():
        assert client.get("/schema").status_code == 200
        export = client.get("/episodes/demo-episode-102/export/ad_cuepoints.csv")
        assert export.status_code == 200
        assert "candidate_id" in export.text
    

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-ChildItem backend\\app; python -m pytest backend\\tests -q"
    status: Completed · exit 0
      
      
          Directory: C:\Users\asus\Desktop\hoichoi\backend\app
      
      
      Mode                 LastWriteTime         Length Name
      ----                 -------------         ------ ----
      -a----        26-09-2026     13:43          13839 demo_data.py
      -a----        26-09-2026     13:43          12222 main.py
      -a----        26-09-2026     13:43           4052 models.py
      -a----        26-09-2026     13:43             36 __init__.py
      2026-09-26T08:14:07.769461Z [warning  ] The configuration option "asyncio_default_fixture_loop_scope" is unset.
      The event loop scope for asynchronous fixtures will default to the fixture caching scope. Future versions of pytest-asyncio will default the loop scope for asynchronous fixtures to function scope. Set the default fixture loop scope explicitly in order to avoid unexpected behavior in the future. Valid fixture loop scopes are: "function", "class", "module", "package", "session"
       [py.warnings] category=PytestDeprecationWarning filename=C:\Users\asus\AppData\Local\Programs\Python\Python311\Lib\site-packages\pytest_asyncio\plugin.py lineno=208
      ...                                                                      [100%]
      3 passed in 0.62s
      
      

## Assistant

The FastAPI contract is now in place and its initial endpoint tests pass. I’ve also made the demo data deliberately exercise the pitch-critical cases: a phone that is mentioned but never shown, a shown-only brand, low- and high-disruption ad points, Bengali captions, and timestamped QC issues. I’m moving into the Next.js workspace now.

## Activity

    file changes: Completed · 8 changes
    Add: C:\Users\asus\Desktop\hoichoi\frontend\next-env.d.ts
    /// <reference types="next" />
    /// <reference types="next/image-types/global" />
    
    // This file is generated and managed by Next.js.
    
    Add: C:\Users\asus\Desktop\hoichoi\frontend\next.config.ts
    import type { NextConfig } from "next";
    
    const nextConfig: NextConfig = {
      output: "standalone",
    };
    
    export default nextConfig;
    
    Add: C:\Users\asus\Desktop\hoichoi\frontend\package.json
    {
      "name": "hoichoi-drishti-web",
      "version": "0.1.0",
      "private": true,
      "scripts": {
        "dev": "next dev",
        "build": "next build",
        "start": "next start",
        "lint": "next lint"
      },
      "dependencies": {
        "lucide-react": "^0.468.0",
        "next": "15.2.4",
        "react": "19.0.0",
        "react-dom": "19.0.0"
      },
      "devDependencies": {
        "@types/node": "^22.10.5",
        "@types/react": "^19.0.3",
        "@types/react-dom": "^19.0.2",
        "typescript": "^5.7.2"
      }
    }
    
    Add: C:\Users\asus\Desktop\hoichoi\frontend\src\app\layout.tsx
    import type { Metadata } from "next";
    import "./globals.css";
    
    export const metadata: Metadata = {
      title: "Drishti — Semantic timeline",
      description: "Context intelligence and Bengali localization for every scene.",
    };
    
    export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
      return (
        <html lang="en">
          <body>{children}</body>
        </html>
      );
    }
    
    Add: C:\Users\asus\Desktop\hoichoi\frontend\src\lib\api.ts
    import type { AdCandidate, Episode, Timeline } from "./types";
    
    export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
    
    async function request<T>(path: string, init?: RequestInit): Promise<T> {
      const response = await fetch(`${API_URL}${path}`, { ...init, cache: "no-store" });
      if (!response.ok) {
        const detail = await response.json().catch(() => ({ detail: "Request failed" }));
        throw new Error(detail.detail ?? `Request failed (${response.status})`);
      }
      return response.json() as Promise<T>;
    }
    
    export const api = {
      episodes: () => request<Episode[]>("/episodes"),
      episode: (id: string) => request<Episode>(`/episodes/${id}`),
      timeline: (id: string) => request<Timeline>(`/episodes/${id}/timeline`),
      ads: (id: string, minGap: number, count: number) =>
        request<AdCandidate[]>(`/episodes/${id}/ads?min_gap=${minGap}&n_breaks=${count}&blocked=0,0`),
      selectAd: (id: string, candidateId: string, selected: boolean) =>
        request<AdCandidate>(`/episodes/${id}/ads/${candidateId}`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ selected }),
        }),
      upload: (form: FormData) => request<Episode>("/episodes", { method: "POST", body: form }),
    };
    
    Add: C:\Users\asus\Desktop\hoichoi\frontend\src\lib\format.ts
    export function formatTime(totalSeconds: number, withHours = false) {
      const value = Math.max(0, Math.floor(totalSeconds));
      const hours = Math.floor(value / 3600);
      const minutes = Math.floor((value % 3600) / 60);
      const seconds = value % 60;
      if (withHours || hours > 0) return `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
      return `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
    }
    
    export function presenceLabel(value: string) {
      return {
        mentioned_and_shown: "Mentioned + shown",
        mentioned_only: "Mentioned only",
        shown_only: "Shown only",
        unverified: "Unverified",
      }[value] ?? value;
    }
    
    export function sentenceCase(value: string) {
      return value.replaceAll("_", " ").replace(/^./, (letter) => letter.toUpperCase());
    }
    
    Add: C:\Users\asus\Desktop\hoichoi\frontend\src\lib\types.ts
    export type Stage = {
      id: string;
      label: string;
      status: "queued" | "running" | "done" | "failed";
      elapsed?: number;
    };
    
    export type Episode = {
      id: string;
      title: string;
      duration: number;
      status: "queued" | "processing" | "processed" | "failed";
      progress: number;
      created_at: string;
      video_available: boolean;
      stages: Stage[];
    };
    
    export type Utterance = {
      utt_id: string;
      start: number;
      end: number;
      speaker: string;
      speaker_name?: string;
      text: string;
      confidence?: number;
      overlap?: boolean;
    };
    
    export type Entity = {
      entity_id: string;
      name: string;
      name_bn?: string;
      kind: string;
      brand?: string;
      ad_categories: string[];
      mentions: { source: string; time: number; surface: string }[];
      sentiment: "positive" | "neutral" | "negative";
      presence: "mentioned_and_shown" | "mentioned_only" | "shown_only" | "unverified";
      confidence: number;
      visual_check?: {
        frames_checked: string[];
        visible?: boolean;
        visible_frames: string[];
        confidence: number;
        note: string;
      };
    };
    
    export type Scene = {
      scene_id: string;
      start: number;
      end: number;
      visual: {
        location: string;
        objects: string[];
        activity: string;
        visual_mood: string;
        people_count: number;
        confidence: number;
      };
      speakers: string[];
      utt_ids: string[];
      audio_events: string[];
      music_ratio: number;
      semantic: {
        title: string;
        summary: string;
        topics: string[];
        mood: string;
        narrative_intensity: number;
        intensity_components: Record<string, number>;
        is_cliffhanger: boolean;
      };
      entity_ids: string[];
    };
    
    export type AdCandidate = {
      cand_id: string;
      time: number;
      scene_id: string;
      kind: string;
      pause_len: number;
      score: {
        pause: number;
        scene_end: number;
        low_intensity: number;
        context_match: number;
        speech_penalty: number;
        cliffhanger_penalty: number;
        total: number;
      };
      disruption: "low" | "medium" | "high";
      matched_categories: string[];
      reason: string;
      selected: boolean;
    };
    
    export type SubtitleCue = {
      idx: number;
      start: number;
      end: number;
      lines: string[];
      speakers: string[];
      kind: "dialogue" | "sound";
      cps: number;
    };
    
    export type QCIssue = {
      issue_id: string;
      severity: "error" | "warn" | "info";
      rule: string;
      time: number;
      cue_idx?: number;
      message: string;
      suggestion?: string;
    };
    
    export type AudioEvent = {
      event_id: string;
      label: string;
      label_bn: string;
      start: number;
      end: number;
      score: number;
      in_cc: boolean;
    };
    
    export type Timeline = {
      schema_version: string;
      episode: { id: string; title: string; duration: number; video_available: boolean };
      scenes: Scene[];
      utterances: Utterance[];
      audio_events: AudioEvent[];
      entities: Entity[];
      ad_candidates: AdCandidate[];
      subtitles: Record<string, string | number>;
      subtitle_cues: SubtitleCue[];
      cc_cues: SubtitleCue[];
      qc: QCIssue[];
      curves: { intensity: [number, number][]; loudness: [number, number][] };
      processing: { total_seconds: number; llm_cost_usd: number; models: string[]; cached_stages: number };
      [key: string]: unknown;
    };
    
    Add: C:\Users\asus\Desktop\hoichoi\frontend\tsconfig.json
    {
      "compilerOptions": {
        "target": "ES2017",
        "lib": ["dom", "dom.iterable", "esnext"],
        "allowJs": false,
        "skipLibCheck": true,
        "strict": true,
        "noEmit": true,
        "esModuleInterop": true,
        "module": "esnext",
        "moduleResolution": "bundler",
        "resolveJsonModule": true,
        "isolatedModules": true,
        "jsx": "preserve",
        "incremental": true,
        "plugins": [{ "name": "next" }],
        "paths": { "@/*": ["./src/*"] }
      },
      "include": ["next-env.d.ts", ".next/types/**/*.ts", "**/*.ts", "**/*.tsx"],
      "exclude": ["node_modules"]
    }
    

## Activity

    file changes: Completed · 2 changes
    Add: C:\Users\asus\Desktop\hoichoi\frontend\src\app\episode\[id]\page.tsx
    import Workspace from "@/components/Workspace";
    
    export default async function EpisodePage({ params }: { params: Promise<{ id: string }> }) {
      const { id } = await params;
      return <Workspace episodeId={id} />;
    }
    
    Add: C:\Users\asus\Desktop\hoichoi\frontend\src\app\page.tsx
    "use client";
    
    import { useEffect, useRef, useState } from "react";
    import { useRouter } from "next/navigation";
    import { ArrowUpRight, Check, Clapperboard, Clock3, FileVideo2, LoaderCircle, Upload, X } from "lucide-react";
    import { api } from "@/lib/api";
    import { formatTime } from "@/lib/format";
    import type { Episode } from "@/lib/types";
    
    export default function LibraryPage() {
      const router = useRouter();
      const inputRef = useRef<HTMLInputElement>(null);
      const [episodes, setEpisodes] = useState<Episode[]>([]);
      const [loading, setLoading] = useState(true);
      const [dragging, setDragging] = useState(false);
      const [uploading, setUploading] = useState(false);
      const [error, setError] = useState("");
    
      useEffect(() => {
        api.episodes().then(setEpisodes).catch((reason: Error) => setError(reason.message)).finally(() => setLoading(false));
      }, []);
    
      async function handleFile(file?: File) {
        if (!file) return;
        setUploading(true);
        setError("");
        const form = new FormData();
        form.append("file", file);
        try {
          const episode = await api.upload(form);
          router.push(`/episode/${episode.id}`);
        } catch (reason) {
          setError(reason instanceof Error ? reason.message : "Upload failed");
          setUploading(false);
        }
      }
    
      return (
        <main className="library-shell">
          <header className="library-header">
            <Brand />
            <div className="header-note"><span className="signal-dot" />Semantic pipeline online</div>
          </header>
    
          <section className="library-intro">
            <div>
              <p className="kicker">Episode library</p>
              <h1>See what every<br />scene <span>means.</span></h1>
              <p className="intro-copy">One time-indexed layer for better ad breaks, Bengali subtitles, closed captions, and fast human review.</p>
            </div>
            <div className="intro-mark" aria-hidden="true">দৃ</div>
          </section>
    
          <section
            className={`upload-strip ${dragging ? "is-dragging" : ""}`}
            onDragEnter={(event) => { event.preventDefault(); setDragging(true); }}
            onDragOver={(event) => event.preventDefault()}
            onDragLeave={() => setDragging(false)}
            onDrop={(event) => { event.preventDefault(); setDragging(false); handleFile(event.dataTransfer.files[0]); }}
          >
            <div className="upload-icon"><FileVideo2 size={23} strokeWidth={1.7} /></div>
            <div>
              <h2>{uploading ? "Preparing your episode…" : "Add an episode"}</h2>
              <p>Drop an MP4, MKV, MOV, or WebM. Processing continues in the background.</p>
            </div>
            <button className="primary-button" onClick={() => inputRef.current?.click()} disabled={uploading}>
              {uploading ? <LoaderCircle className="spin" size={17} /> : <Upload size={17} />}
              {uploading ? "Uploading" : "Choose video"}
            </button>
            <input ref={inputRef} hidden type="file" accept="video/mp4,video/x-matroska,video/quicktime,video/webm" onChange={(event) => handleFile(event.target.files?.[0])} />
          </section>
    
          {error && <div className="error-banner"><X size={16} />{error}. Start the FastAPI server on port 8000 and try again.</div>}
    
          <section className="catalog-section">
            <div className="section-heading">
              <div><h2>Episodes</h2><span>{episodes.length} in this library</span></div>
              <div className="table-labels"><span>Duration</span><span>Status</span><span>Processed</span><i /></div>
            </div>
            <div className="episode-list">
              {loading ? (
                <div className="empty-row"><LoaderCircle className="spin" /> Loading library…</div>
              ) : episodes.map((episode, index) => (
                <button className="episode-row" key={episode.id} onClick={() => router.push(`/episode/${episode.id}`)}>
                  <span className="episode-index">{String(index + 1).padStart(2, "0")}</span>
                  <span className="episode-main">
                    <span className="episode-thumb"><Clapperboard size={22} /><i>{episode.status === "processed" ? "Ready" : `${episode.progress}%`}</i></span>
                    <span><strong>{episode.title}</strong><small>{episode.id}</small></span>
                  </span>
                  <span className="row-data"><Clock3 size={14} />{episode.duration ? formatTime(episode.duration, true) : "Analyzing"}</span>
                  <span className={`status-pill ${episode.status}`}>
                    {episode.status === "processed" ? <Check size={13} /> : <LoaderCircle className={episode.status === "processing" ? "spin" : ""} size={13} />}
                    {episode.status}
                  </span>
                  <span className="row-data date">{new Intl.DateTimeFormat("en-IN", { day: "2-digit", month: "short", year: "numeric" }).format(new Date(episode.created_at))}</span>
                  <span className="row-open"><ArrowUpRight size={18} /></span>
                </button>
              ))}
            </div>
          </section>
    
          <footer className="library-footer">
            <span>Paramarsh Labs</span><span>Semantic understanding for regional stories</span><span>Schema v1.0</span>
          </footer>
        </main>
      );
    }
    
    function Brand() {
      return (
        <div className="brand">
          <span className="brand-glyph"><i /><i /><i /></span>
          <span><strong>DRISHTI</strong><small>দৃষ্টি</small></span>
        </div>
      );
    }
    

## Activity

    file changes: Completed · 1 changes
    Add: C:\Users\asus\Desktop\hoichoi\frontend\src\components\SemanticTimeline.tsx
    "use client";
    
    import { useMemo, useState } from "react";
    import { Minus, Plus, SlidersHorizontal } from "lucide-react";
    import type { Timeline } from "@/lib/types";
    import { formatTime } from "@/lib/format";
    
    type Lane = "Scenes" | "Speech" | "Entities" | "Sounds" | "Intensity" | "Ads";
    
    const laneY: Record<Lane, number> = {
      Scenes: 4,
      Speech: 40,
      Entities: 65,
      Sounds: 90,
      Intensity: 115,
      Ads: 150,
    };
    
    const moodColors: Record<string, string> = {
      restrained: "#596783",
      warm: "#B78B52",
      tense: "#A74C5B",
      relieved: "#3F8A72",
      focused: "#5574A7",
      melancholic: "#775D96",
    };
    
    export default function SemanticTimeline({ data, currentTime, onSeek }: { data: Timeline; currentTime: number; onSeek: (time: number) => void }) {
      const duration = data.episode.duration;
      const [zoom, setZoom] = useState(1);
      const [lanes, setLanes] = useState<Record<Lane, boolean>>({ Scenes: true, Speech: true, Entities: true, Sounds: true, Intensity: true, Ads: true });
      const windowDuration = duration / zoom;
      const start = zoom === 1 ? 0 : Math.max(0, Math.min(duration - windowDuration, currentTime - windowDuration / 2));
      const end = start + windowDuration;
      const x = (time: number) => ((time - start) / windowDuration) * 1000;
      const visibleLanes = (Object.keys(lanes) as Lane[]).filter((lane) => lanes[lane]);
      const ticks = useMemo(() => Array.from({ length: 9 }, (_, index) => start + (windowDuration / 8) * index), [start, windowDuration]);
    
      function seekFromPointer(event: React.PointerEvent<SVGSVGElement>) {
        const bounds = event.currentTarget.getBoundingClientRect();
        onSeek(start + ((event.clientX - bounds.left) / bounds.width) * windowDuration);
      }
    
      return (
        <section className="timeline-block">
          <div className="timeline-toolbar">
            <div className="timeline-title"><SlidersHorizontal size={15} />Semantic film strip</div>
            <div className="lane-switches">
              {(Object.keys(lanes) as Lane[]).map((lane) => (
                <button key={lane} className={lanes[lane] ? "active" : ""} onClick={() => setLanes((value) => ({ ...value, [lane]: !value[lane] }))}>{lane}</button>
              ))}
            </div>
            <div className="zoom-control">
              <button aria-label="Zoom out" onClick={() => setZoom((value) => Math.max(1, value / 1.5))}><Minus size={14} /></button>
              <span>{zoom.toFixed(1)}×</span>
              <button aria-label="Zoom in" onClick={() => setZoom((value) => Math.min(6, value * 1.5))}><Plus size={14} /></button>
            </div>
          </div>
          <div className="timeline-ruler">
            <span />
            <div>{ticks.map((tick) => <i key={tick} style={{ left: `${x(tick) / 10}%` }}>{formatTime(tick)}</i>)}</div>
          </div>
          <div className="timeline-chart">
            <div className="lane-labels">
              {visibleLanes.map((lane) => <span key={lane}>{lane}</span>)}
            </div>
            <svg
              role="slider"
              aria-label="Episode semantic timeline"
              aria-valuemin={0}
              aria-valuemax={duration}
              aria-valuenow={currentTime}
              viewBox="0 0 1000 182"
              preserveAspectRatio="none"
              onPointerDown={seekFromPointer}
              onWheel={(event) => { event.preventDefault(); setZoom((value) => event.deltaY < 0 ? Math.min(6, value * 1.2) : Math.max(1, value / 1.2)); }}
            >
              <defs>
                <linearGradient id="intensityFill" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stopColor="#FF6B6B" stopOpacity=".65" /><stop offset="1" stopColor="#FF6B6B" stopOpacity=".04" /></linearGradient>
                <pattern id="grid" width="62.5" height="22" patternUnits="userSpaceOnUse"><path d="M 62.5 0 L 0 0 0 22" fill="none" stroke="#ffffff" strokeOpacity=".035" strokeWidth="1" /></pattern>
              </defs>
              <rect width="1000" height="182" fill="url(#grid)" />
    
              {lanes.Scenes && data.scenes.map((scene) => {
                const left = x(Math.max(scene.start, start));
                const right = x(Math.min(scene.end, end));
                if (right < 0 || left > 1000) return null;
                return <g key={scene.scene_id}>
                  <rect x={left} y={laneY.Scenes} width={Math.max(1, right - left - 2)} height="29" rx="2" fill={moodColors[scene.semantic.mood] ?? "#596783"} opacity=".86" />
                  {right - left > 80 && <text x={left + 10} y="23" fill="#fff" fontSize="10" fontWeight="600">{scene.semantic.title}</text>}
                </g>;
              })}
    
              {lanes.Speech && data.utterances.map((utterance) => {
                const colors: Record<string, string> = { SPK_A: "#62E6A7", SPK_B: "#81A7FF", SPK_C: "#E79BEF" };
                return <rect key={utterance.utt_id} x={x(utterance.start)} y={laneY.Speech + (utterance.speaker.charCodeAt(4) % 3) * 5} width={Math.max(2, x(utterance.end) - x(utterance.start))} height="4" rx="2" fill={colors[utterance.speaker] ?? "#DDE3EE"} />;
              })}
    
              {lanes.Entities && data.entities.flatMap((entity) => entity.mentions.map((mention, index) => {
                const color = entity.presence === "mentioned_only" ? "#F3B64B" : entity.presence === "shown_only" ? "#81A7FF" : entity.presence === "mentioned_and_shown" ? "#62E6A7" : "#7F8798";
                return <g key={`${entity.entity_id}-${index}`} transform={`translate(${x(mention.time)}, ${laneY.Entities + 7})`}>
                  <circle r="7" fill="#101522" stroke={color} strokeWidth="2" />
                  <circle r="2" fill={color} />
                </g>;
              }))}
    
              {lanes.Sounds && data.audio_events.map((event) => <g key={event.event_id} transform={`translate(${x(event.start)},${laneY.Sounds + 8})`}><path d="M-5 1h3l4-5v13l-4-5h-3z" fill="#9AA3B6" /><path d="M5-2q4 4 0 8" fill="none" stroke="#9AA3B6" strokeWidth="1.5" /></g>)}
    
              {lanes.Intensity && <path
                d={`${data.curves.intensity.filter(([time]) => time >= start && time <= end).map(([time, value], index) => `${index ? "L" : "M"}${x(time)},${laneY.Intensity + 29 - value * 27}`).join(" ")} L1000,${laneY.Intensity + 30} L0,${laneY.Intensity + 30} Z`}
                fill="url(#intensityFill)"
                stroke="#FF7D7D"
                strokeWidth="1.3"
                vectorEffect="non-scaling-stroke"
              />}
    
              {lanes.Ads && data.ad_candidates.map((ad) => <g key={ad.cand_id} transform={`translate(${x(ad.time)},${laneY.Ads + 13})`}>
                <path d="M0-10 8 4H-8Z" fill={ad.selected ? "#F3B64B" : "#343C50"} stroke={ad.selected ? "#F3B64B" : "#8E97AA"} strokeWidth="1.5" />
                <text x="12" y="3" fill="#CCD2DF" fontSize="9" fontWeight="700">{Math.round(ad.score.total * 100)}</text>
              </g>)}
    
              <line x1={x(currentTime)} x2={x(currentTime)} y1="0" y2="182" stroke="#F5F7FB" strokeWidth="1.5" vectorEffect="non-scaling-stroke" />
              <path d={`M${x(currentTime) - 5} 0h10l-5 7z`} fill="#F5F7FB" />
            </svg>
          </div>
        </section>
      );
    }
    

## Activity

    file changes: Completed · 1 changes
    Add: C:\Users\asus\Desktop\hoichoi\frontend\src\components\Workspace.tsx
    "use client";
    
    import Link from "next/link";
    import { useEffect, useMemo, useRef, useState } from "react";
    import {
      ArrowLeft, BadgeCheck, Captions, Check, ChevronDown, ChevronRight, CircleAlert, Clock3,
      Copy, Download, FileJson2, Film, Gauge, Info, ListFilter, MapPin, MoreHorizontal, Pause,
      Play, Search, Sparkles, Tag, TriangleAlert, Users, Volume2, X,
    } from "lucide-react";
    import SemanticTimeline from "./SemanticTimeline";
    import { API_URL, api } from "@/lib/api";
    import { formatTime, presenceLabel, sentenceCase } from "@/lib/format";
    import type { AdCandidate, Entity, Episode, QCIssue, Scene, SubtitleCue, Timeline, Utterance } from "@/lib/types";
    
    const tabs = ["Scenes", "Transcript", "Entities", "Ads", "Subtitles", "QC", "JSON"] as const;
    type Tab = (typeof tabs)[number];
    
    export default function Workspace({ episodeId }: { episodeId: string }) {
      const [episode, setEpisode] = useState<Episode | null>(null);
      const [data, setData] = useState<Timeline | null>(null);
      const [error, setError] = useState("");
      const [currentTime, setCurrentTime] = useState(0);
      const [playing, setPlaying] = useState(false);
      const [activeTab, setActiveTab] = useState<Tab>("Scenes");
      const [captions, setCaptions] = useState<"off" | "sub" | "cc">("cc");
      const [search, setSearch] = useState("");
      const [exportOpen, setExportOpen] = useState(false);
    
      useEffect(() => {
        Promise.all([api.episode(episodeId), api.timeline(episodeId)])
          .then(([episodeResult, timelineResult]) => { setEpisode(episodeResult); setData(timelineResult); })
          .catch((reason: Error) => setError(reason.message));
      }, [episodeId]);
    
      useEffect(() => {
        if (!playing || !data || data.episode.video_available) return;
        const timer = window.setInterval(() => setCurrentTime((value) => value >= data.episode.duration ? 0 : value + 0.25), 250);
        return () => window.clearInterval(timer);
      }, [playing, data]);
    
      const currentScene = useMemo(() => data?.scenes.find((scene) => currentTime >= scene.start && currentTime < scene.end) ?? data?.scenes.at(-1), [data, currentTime]);
      const currentCue = useMemo(() => {
        if (!data || captions === "off") return undefined;
        const source = captions === "cc" ? data.cc_cues : data.subtitle_cues;
        return source.find((cue) => currentTime >= cue.start && currentTime <= cue.end);
      }, [data, captions, currentTime]);
    
      function seek(time: number) {
        setCurrentTime(Math.max(0, Math.min(data?.episode.duration ?? 0, time)));
      }
    
      if (error) return <ErrorState message={error} />;
      if (!data || !episode || !currentScene) return <LoadingState />;
    
      const q = search.trim().toLocaleLowerCase();
      const searchResults = q ? [
        ...data.scenes.filter((scene) => `${scene.semantic.title} ${scene.semantic.summary}`.toLocaleLowerCase().includes(q)).map((scene) => ({ id: scene.scene_id, time: scene.start, text: scene.semantic.title, type: "Scene" })),
        ...data.utterances.filter((utterance) => utterance.text.toLocaleLowerCase().includes(q)).map((utterance) => ({ id: utterance.utt_id, time: utterance.start, text: utterance.text, type: "Dialogue" })),
      ].slice(0, 6) : [];
    
      return (
        <main className="workspace-shell">
          <header className="workspace-header">
            <Link href="/" className="back-link" aria-label="Back to library"><ArrowLeft size={17} /></Link>
            <div className="workspace-brand"><span className="mini-glyph"><i /><i /><i /></span><strong>DRISHTI</strong></div>
            <div className="episode-heading">
              <h1>{episode.title}</h1>
              <span>{formatTime(data.episode.duration, true)}</span>
              <span className="processed-mark"><BadgeCheck size={14} />{episode.status}</span>
            </div>
            <div className="workspace-actions">
              <div className="search-box">
                <Search size={15} />
                <input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search scenes or dialogue" />
                {search && <button onClick={() => setSearch("")}><X size={13} /></button>}
                {search && <div className="search-popover">
                  {searchResults.length ? searchResults.map((result) => <button key={result.id} onClick={() => { seek(result.time); setSearch(""); }}><span>{result.type}</span><strong>{result.text}</strong><small>{formatTime(result.time)}</small></button>) : <p>No results in this episode.</p>}
                </div>}
              </div>
              <div className="export-wrap">
                <button className="quiet-button" onClick={() => setExportOpen((value) => !value)}><Download size={15} />Export<ChevronDown size={14} /></button>
                {exportOpen && <div className="export-menu">
                  <a href={`${API_URL}/episodes/${episodeId}/export/semantic_timeline.json`}><FileJson2 size={15} />Semantic timeline</a>
                  <a href={`${API_URL}/episodes/${episodeId}/export/ad_cuepoints.csv`}><Gauge size={15} />Ad cue points</a>
                  <a href={`${API_URL}/episodes/${episodeId}/export/qc_report.json`}><CircleAlert size={15} />QC report</a>
                </div>}
              </div>
              <button className="icon-button" aria-label="More options"><MoreHorizontal size={18} /></button>
            </div>
          </header>
    
          {episode.status !== "processed" && <ProcessingBar episode={episode} />}
    
          <section className="stage-grid">
            <Player
              episodeId={episodeId}
              videoAvailable={data.episode.video_available}
              currentTime={currentTime}
              duration={data.episode.duration}
              scene={currentScene}
              playing={playing}
              cue={currentCue}
              captions={captions}
              onTime={seek}
              onPlaying={setPlaying}
              onCaptions={setCaptions}
            />
            <SceneInspector scene={currentScene} entities={data.entities.filter((entity) => currentScene.entity_ids.includes(entity.entity_id))} />
          </section>
    
          <SemanticTimeline data={data} currentTime={currentTime} onSeek={seek} />
    
          <section className="data-panel">
            <nav className="tab-list" aria-label="Episode data views">
              {tabs.map((tab) => <button key={tab} className={activeTab === tab ? "active" : ""} onClick={() => setActiveTab(tab)}>{tab}{tab === "QC" && <span>{data.qc.length}</span>}</button>)}
            </nav>
            <div className="tab-body">
              {activeTab === "Scenes" && <ScenesTab scenes={data.scenes} currentScene={currentScene} onSeek={seek} />}
              {activeTab === "Transcript" && <TranscriptTab utterances={data.utterances} currentTime={currentTime} onSeek={seek} />}
              {activeTab === "Entities" && <EntitiesTab entities={data.entities} onSeek={seek} />}
              {activeTab === "Ads" && <AdsTab episodeId={episodeId} candidates={data.ad_candidates} onSeek={seek} />}
              {activeTab === "Subtitles" && <SubtitlesTab episodeId={episodeId} subtitleCues={data.subtitle_cues} ccCues={data.cc_cues} onSeek={seek} />}
              {activeTab === "QC" && <QCTab issues={data.qc} onSeek={seek} />}
              {activeTab === "JSON" && <JsonTab data={data} episodeId={episodeId} />}
            </div>
          </section>
        </main>
      );
    }
    
    function Player({ episodeId, videoAvailable, currentTime, duration, scene, playing, cue, captions, onTime, onPlaying, onCaptions }: {
      episodeId: string; videoAvailable: boolean; currentTime: number; duration: number; scene: Scene; playing: boolean; cue?: SubtitleCue;
      captions: "off" | "sub" | "cc"; onTime: (time: number) => void; onPlaying: (playing: boolean) => void; onCaptions: (value: "off" | "sub" | "cc") => void;
    }) {
      const videoRef = useRef<HTMLVideoElement>(null);
      useEffect(() => {
        const video = videoRef.current;
        if (video && Math.abs(video.currentTime - currentTime) > 1) video.currentTime = currentTime;
      }, [currentTime]);
    
      function togglePlayback() {
        if (videoRef.current) {
          if (videoRef.current.paused) videoRef.current.play(); else videoRef.current.pause();
        } else onPlaying(!playing);
      }
    
      return (
        <div className={`player-frame mood-${scene.semantic.mood}`}>
          {videoAvailable ? <video ref={videoRef} src={`${API_URL}/episodes/${episodeId}/video`} onTimeUpdate={(event) => onTime(event.currentTarget.currentTime)} onPlay={() => onPlaying(true)} onPause={() => onPlaying(false)} /> : <div className="scene-visual" aria-label="Demo scene visualization">
            <div className="visual-grain" /><div className="visual-window" /><div className="visual-table" />
            <div className="person person-a" /><div className="person person-b" />
            <div className="preview-label"><Film size={13} />Demo timeline · attach a video for picture</div>
          </div>}
          <div className="player-shade" />
          {cue && <div className="caption-render">{cue.lines.map((line) => <span key={line}>{line}</span>)}</div>}
          <div className="player-controls">
            <button className="play-button" onClick={togglePlayback} aria-label={playing ? "Pause" : "Play"}>{playing ? <Pause size={18} fill="currentColor" /> : <Play size={18} fill="currentColor" />}</button>
            <span className="player-time">{formatTime(currentTime)} <i>/</i> {formatTime(duration)}</span>
            <input aria-label="Play position" type="range" min="0" max={duration} step="0.1" value={currentTime} onChange={(event) => onTime(Number(event.target.value))} style={{ "--progress": `${(currentTime / duration) * 100}%` } as React.CSSProperties} />
            <Volume2 size={17} />
            <div className="caption-toggle">
              <Captions size={17} />
              {(["off", "sub", "cc"] as const).map((value) => <button key={value} className={captions === value ? "active" : ""} onClick={() => onCaptions(value)}>{value.toUpperCase()}</button>)}
            </div>
          </div>
        </div>
      );
    }
    
    function SceneInspector({ scene, entities }: { scene: Scene; entities: Entity[] }) {
      return <aside className="scene-inspector">
        <div className="inspector-top"><span>Current scene</span><strong>{scene.scene_id.replace("scene_", "#")}</strong></div>
        <h2>{scene.semantic.title}</h2>
        <div className="scene-time"><Clock3 size={14} />{formatTime(scene.start)} — {formatTime(scene.end)}<span>{formatTime(scene.end - scene.start)}</span></div>
        <p className="scene-summary">{scene.semantic.summary}</p>
        <div className="fact-grid">
          <div><MapPin size={14} /><span>Location</span><strong>{sentenceCase(scene.visual.location)}</strong></div>
          <div><Sparkles size={14} /><span>Mood</span><strong>{sentenceCase(scene.semantic.mood)}</strong></div>
          <div><Users size={14} /><span>Speakers</span><strong>{scene.speakers.join(", ")}</strong></div>
          <div><Tag size={14} /><span>Activity</span><strong>{sentenceCase(scene.visual.activity)}</strong></div>
        </div>
        <div className="intensity-block">
          <div><span>Narrative intensity</span><strong>{Math.round(scene.semantic.narrative_intensity * 100)}</strong></div>
          <div className="intensity-track"><i style={{ width: `${scene.semantic.narrative_intensity * 100}%` }} /></div>
          {scene.semantic.is_cliffhanger && <small><TriangleAlert size={12} />Protected cliffhanger zone</small>}
        </div>
        <div className="entity-mini-list">
          <span>Scene entities</span>
          {entities.length ? entities.map((entity) => <div key={entity.entity_id}><strong>{entity.name_bn ?? entity.name}</strong><em className={`presence ${entity.presence}`}>{presenceLabel(entity.presence)}</em><small>{Math.round(entity.confidence * 100)}%</small></div>) : <p>No product or topic entities in this scene.</p>}
        </div>
      </aside>;
    }
    
    function ScenesTab({ scenes, currentScene, onSeek }: { scenes: Scene[]; currentScene: Scene; onSeek: (time: number) => void }) {
      return <div className="table-wrap"><table className="scene-table"><thead><tr><th>Time</th><th>Scene</th><th>Location</th><th>Mood</th><th>Intensity</th><th>Entities</th></tr></thead><tbody>{scenes.map((scene) => <tr key={scene.scene_id} className={scene.scene_id === currentScene.scene_id ? "current" : ""} onClick={() => onSeek(scene.start)}><td><button>{formatTime(scene.start)}</button></td><td><strong>{scene.semantic.title}</strong><span>{scene.semantic.summary}</span></td><td>{sentenceCase(scene.visual.location)}</td><td><em className={`mood mood-${scene.semantic.mood}`}>{sentenceCase(scene.semantic.mood)}</em></td><td><div className="micro-meter"><i style={{ width: `${scene.semantic.narrative_intensity * 100}%` }} /></div><small>{scene.semantic.narrative_intensity.toFixed(2)}</small></td><td>{scene.entity_ids.length || "—"}</td></tr>)}</tbody></table></div>;
    }
    
    function TranscriptTab({ utterances, currentTime, onSeek }: { utterances: Utterance[]; currentTime: number; onSeek: (time: number) => void }) {
      return <div className="transcript-list">{utterances.map((utterance) => <button key={utterance.utt_id} className={currentTime >= utterance.start && currentTime <= utterance.end ? "current" : ""} onClick={() => onSeek(utterance.start)}><span className={`speaker-dot ${utterance.speaker}`} /> <span className="transcript-meta"><strong>{utterance.speaker_name ?? utterance.speaker}</strong><small>{utterance.speaker} · {formatTime(utterance.start)}</small></span><p lang="bn">{utterance.text}</p><em>{Math.round((utterance.confidence ?? 0) * 100)}%</em>{utterance.overlap && <i>Overlap</i>}</button>)}</div>;
    }
    
    function EntitiesTab({ entities, onSeek }: { entities: Entity[]; onSeek: (time: number) => void }) {
      const [expanded, setExpanded] = useState<string | null>(entities[0]?.entity_id ?? null);
      const grouped = Object.entries(Object.groupBy(entities, (entity) => entity.ad_categories[0] ?? "other"));
      return <div className="entity-groups">{grouped.map(([category, items]) => <section key={category}><div className="entity-group-title"><span>{sentenceCase(category)}</span><small>{items?.length} entities</small></div>{items?.map((entity) => <div className={`entity-row ${expanded === entity.entity_id ? "expanded" : ""}`} key={entity.entity_id}><button className="entity-summary" onClick={() => setExpanded(expanded === entity.entity_id ? null : entity.entity_id)}><ChevronRight size={15} /><span className="entity-name"><strong>{entity.name_bn ?? entity.name}</strong><small>{entity.name}</small></span><em className={`presence ${entity.presence}`}>{presenceLabel(entity.presence)}</em><span className={`sentiment ${entity.sentiment}`}>{entity.sentiment}</span><span className="confidence">{Math.round(entity.confidence * 100)}%</span></button>{expanded === entity.entity_id && <div className="entity-detail"><div><h4>Evidence</h4>{entity.mentions.map((mention, index) => <button key={index} onClick={() => onSeek(mention.time)}>{formatTime(mention.time)} <span>{mention.source}</span> “{mention.surface}”</button>)}</div><div><h4>Visual verification</h4>{entity.visual_check ? <><p>{entity.visual_check.note}</p><div className="frame-strip">{entity.visual_check.frames_checked.slice(0, 4).map((frame, index) => <span key={frame}><i>{index + 1}</i><small>{frame.replace(".jpg", "")}</small></span>)}</div></> : <p>No targeted frame check was required.</p>}</div></div>}</div>)}</section>)}</div>;
    }
    
    function AdsTab({ episodeId, candidates: initial, onSeek }: { episodeId: string; candidates: AdCandidate[]; onSeek: (time: number) => void }) {
      const [candidates, setCandidates] = useState(initial);
      const [minGap, setMinGap] = useState(8);
      const [count, setCount] = useState(2);
      const [loading, setLoading] = useState(false);
      async function recalculate() { setLoading(true); try { setCandidates(await api.ads(episodeId, minGap * 60, count)); } finally { setLoading(false); } }
      async function toggle(candidate: AdCandidate) { const updated = await api.selectAd(episodeId, candidate.cand_id, !candidate.selected); setCandidates((value) => value.map((item) => item.cand_id === updated.cand_id ? updated : item)); }
      return <div className="ads-layout"><aside className="ad-settings"><h3>Break settings</h3><label>Breaks wanted <strong>{count}</strong><input type="range" min="1" max="5" value={count} onChange={(event) => setCount(Number(event.target.value))} /></label><label>Minimum gap <strong>{minGap} min</strong><input type="range" min="0" max="12" value={minGap} onChange={(event) => setMinGap(Number(event.target.value))} /></label><div className="blocked-zones"><span>Blocked zones</span><strong>Opening 00:00</strong><strong>Closing 00:00</strong></div><button className="primary-button" onClick={recalculate}>{loading ? "Calculating…" : "Recalculate"}</button><p>Selection uses cached candidates and updates instantly. No media is reprocessed.</p></aside><div className="candidate-list">{[...candidates].sort((a, b) => b.score.total - a.score.total).map((candidate, index) => <article className={`candidate-card ${candidate.selected ? "selected" : ""}`} key={candidate.cand_id}><div className="candidate-rank">{String(index + 1).padStart(2, "0")}</div><div className="candidate-content"><div className="candidate-heading"><button onClick={() => onSeek(candidate.time)}><strong>{formatTime(candidate.time)}</strong><span>{sentenceCase(candidate.kind)}</span></button><em className={`disruption ${candidate.disruption}`}>{candidate.disruption} disruption</em><button className={`selection-toggle ${candidate.selected ? "active" : ""}`} onClick={() => toggle(candidate)}><i />{candidate.selected ? "Selected" : "Select"}</button></div><p>{candidate.reason}</p><ScoreBar candidate={candidate} /><div className="score-legend"><span>Pause {Math.round(candidate.score.pause * 100)}</span><span>Scene end {Math.round(candidate.score.scene_end * 100)}</span><span>Low intensity {Math.round(candidate.score.low_intensity * 100)}</span><span>Context {Math.round(candidate.score.context_match * 100)}</span></div></div><div className="total-score"><strong>{Math.round(candidate.score.total * 100)}</strong><span>score</span></div></article>)}</div></div>;
    }
    
    function ScoreBar({ candidate }: { candidate: AdCandidate }) { const values = [candidate.score.pause, candidate.score.scene_end, candidate.score.low_intensity, candidate.score.context_match]; const colors = ["#81A7FF", "#62E6A7", "#B895E3", "#F3B64B"]; const total = values.reduce((sum, value) => sum + value, 0); return <div className="score-bar">{values.map((value, index) => <i key={colors[index]} style={{ width: `${total ? value / total * 100 : 0}%`, background: colors[index] }} />)}</div>; }
    
    function SubtitlesTab({ episodeId, subtitleCues, ccCues, onSeek }: { episodeId: string; subtitleCues: SubtitleCue[]; ccCues: SubtitleCue[]; onSeek: (time: number) => void }) {
      const [kind, setKind] = useState<"sub" | "cc">("sub"); const cues = kind === "sub" ? subtitleCues : ccCues;
      return <div className="subtitle-layout"><div className="subtitle-tools"><div className="segmented"><button className={kind === "sub" ? "active" : ""} onClick={() => setKind("sub")}>Subtitles</button><button className={kind === "cc" ? "active" : ""} onClick={() => setKind("cc")}>Closed captions</button></div><div><a className="quiet-button" href={`${API_URL}/episodes/${episodeId}/subs/${kind}.srt`}><Download size={14} />SRT</a><a className="quiet-button" href={`${API_URL}/episodes/${episodeId}/subs/${kind}.vtt`}><Download size={14} />VTT</a></div></div><div className="cue-list">{[...cues].sort((a, b) => a.start - b.start).map((cue) => <button key={`${cue.idx}-${cue.kind}`} onClick={() => onSeek(cue.start)}><span>{cue.idx}</span><time>{formatTime(cue.start)} — {formatTime(cue.end)}</time><p lang="bn">{cue.lines.join("\n")}</p><em className={cue.cps > 17 ? "warn" : ""}>{cue.cps} cps</em><i className={cue.kind}>{cue.kind}</i></button>)}</div></div>;
    }
    
    function QCTab({ issues, onSeek }: { issues: QCIssue[]; onSeek: (time: number) => void }) {
      const [filter, setFilter] = useState("all"); const filtered = issues.filter((issue) => filter === "all" || issue.severity === filter);
      return <div className="qc-layout"><div className="qc-summary"><div><strong>{issues.filter((issue) => issue.severity === "error").length}</strong><span>Errors</span></div><div><strong>{issues.filter((issue) => issue.severity === "warn").length}</strong><span>Warnings</span></div><div><strong>{issues.filter((issue) => issue.severity === "info").length}</strong><span>Info</span></div><p><Check size={16} />Subtitle output passes demo thresholds.</p></div><div className="qc-content"><div className="filter-row"><ListFilter size={15} />{["all", "error", "warn", "info"].map((value) => <button key={value} className={filter === value ? "active" : ""} onClick={() => setFilter(value)}>{sentenceCase(value)}</button>)}</div><div className="issue-list">{filtered.map((issue) => <button key={issue.issue_id} onClick={() => onSeek(issue.time)}><span className={`issue-icon ${issue.severity}`}>{issue.severity === "warn" ? <TriangleAlert size={16} /> : <Info size={16} />}</span><span className="issue-main"><strong>{sentenceCase(issue.rule)}</strong><p>{issue.message}</p><small>{issue.suggestion}</small></span><time>{formatTime(issue.time)}</time><ChevronRight size={15} /></button>)}</div></div></div>;
    }
    
    function JsonTab({ data, episodeId }: { data: Timeline; episodeId: string }) {
      const [copied, setCopied] = useState(false); const json = JSON.stringify(data, null, 2);
      async function copy() { await navigator.clipboard.writeText(json); setCopied(true); window.setTimeout(() => setCopied(false), 1500); }
      return <div className="json-view"><div className="json-tools"><div><FileJson2 size={17} /><strong>semantic_timeline.json</strong><span>{(new Blob([json]).size / 1024).toFixed(1)} KB</span></div><div><button className="quiet-button" onClick={copy}>{copied ? <Check size={14} /> : <Copy size={14} />}{copied ? "Copied" : "Copy"}</button><a className="quiet-button" href={`${API_URL}/episodes/${episodeId}/export/semantic_timeline.json`}><Download size={14} />Download</a></div></div><pre>{json}</pre></div>;
    }
    
    function ProcessingBar({ episode }: { episode: Episode }) { return <div className="processing-bar"><span className="signal-dot" /><strong>Processing episode</strong><div><i style={{ width: `${episode.progress}%` }} /></div><span>{episode.progress}%</span><small>{episode.stages.find((stage) => stage.status === "running")?.label ?? "Queued"}</small></div>; }
    function LoadingState() { return <main className="state-screen"><span className="brand-glyph"><i /><i /><i /></span><h1>Building the semantic timeline</h1><p>Loading scenes, entities, captions, and ad candidates…</p></main>; }
    function ErrorState({ message }: { message: string }) { return <main className="state-screen error"><CircleAlert size={30} /><h1>The episode could not be opened</h1><p>{message}</p><Link href="/" className="primary-button"><ArrowLeft size={16} />Back to library</Link></main>; }
    

## Activity

    file changes: Completed · 1 changes
    Add: C:\Users\asus\Desktop\hoichoi\frontend\src\app\globals.css
    :root {
      --ink: #090b12;
      --reel: #111521;
      --panel: #151a28;
      --panel-2: #1a2030;
      --line: #2a3142;
      --line-soft: rgba(255, 255, 255, 0.07);
      --fog: #dde3ee;
      --muted: #8d96a9;
      --mint: #62e6a7;
      --saffron: #f3b64b;
      --coral: #ff6b6b;
      --blue: #81a7ff;
      --violet: #b895e3;
      --radius: 7px;
      --font-ui: "Aptos", "Segoe UI Variable", "Segoe UI", sans-serif;
      --font-bn: "Noto Sans Bengali", "Vrinda", "Nirmala UI", sans-serif;
    }
    
    * { box-sizing: border-box; }
    html { background: var(--ink); color-scheme: dark; }
    body { margin: 0; background: var(--ink); color: var(--fog); font-family: var(--font-ui); font-size: 14px; }
    button, input, select { font: inherit; }
    button, a { -webkit-tap-highlight-color: transparent; }
    button { color: inherit; }
    a { color: inherit; text-decoration: none; }
    button:focus-visible, a:focus-visible, input:focus-visible { outline: 2px solid var(--mint); outline-offset: 2px; }
    ::selection { background: rgba(98, 230, 167, .25); }
    ::-webkit-scrollbar { width: 9px; height: 9px; }
    ::-webkit-scrollbar-track { background: var(--reel); }
    ::-webkit-scrollbar-thumb { background: #30384b; border: 2px solid var(--reel); border-radius: 10px; }
    
    .brand { display: flex; align-items: center; gap: 12px; }
    .brand > span:last-child { display: flex; align-items: baseline; gap: 8px; }
    .brand strong { font-size: 15px; letter-spacing: .16em; }
    .brand small { color: var(--muted); font-family: var(--font-bn); }
    .brand-glyph, .mini-glyph { width: 28px; height: 28px; display: flex; align-items: flex-end; gap: 3px; padding: 5px; background: var(--fog); transform: rotate(-4deg); }
    .brand-glyph i, .mini-glyph i { display: block; width: 4px; background: var(--ink); }
    .brand-glyph i:nth-child(1), .mini-glyph i:nth-child(1) { height: 8px; }
    .brand-glyph i:nth-child(2), .mini-glyph i:nth-child(2) { height: 17px; }
    .brand-glyph i:nth-child(3), .mini-glyph i:nth-child(3) { height: 12px; }
    .signal-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--mint); box-shadow: 0 0 0 4px rgba(98, 230, 167, .1); display: inline-block; }
    .spin { animation: spin .8s linear infinite; }
    @keyframes spin { to { transform: rotate(360deg); } }
    
    /* Library */
    .library-shell { min-height: 100vh; padding: 0 clamp(24px, 6vw, 96px); background: radial-gradient(circle at 78% 21%, rgba(70, 91, 135, .14), transparent 29%), var(--ink); }
    .library-header { height: 78px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--line-soft); }
    .header-note { color: var(--muted); font-size: 12px; display: flex; align-items: center; gap: 10px; }
    .library-intro { min-height: 345px; display: flex; align-items: center; justify-content: space-between; position: relative; overflow: hidden; }
    .library-intro .kicker { color: var(--mint); margin: 0 0 17px; font-size: 12px; letter-spacing: .08em; }
    .library-intro h1 { font-size: clamp(48px, 6.2vw, 88px); line-height: .9; letter-spacing: -.055em; margin: 0; max-width: 760px; font-weight: 620; }
    .library-intro h1 span { color: var(--muted); }
    .intro-copy { color: #9ba4b5; max-width: 490px; line-height: 1.65; font-size: 15px; margin: 24px 0 0; }
    .intro-mark { position: absolute; right: 2.5%; top: 4%; font-family: var(--font-bn); font-size: 280px; line-height: 1; font-weight: 700; color: transparent; -webkit-text-stroke: 1px rgba(221, 227, 238, .1); transform: rotate(5deg); pointer-events: none; }
    .upload-strip { min-height: 94px; display: grid; grid-template-columns: auto 1fr auto; align-items: center; gap: 18px; padding: 17px 20px; border: 1px dashed #394359; background: rgba(20, 25, 38, .78); transition: border-color .2s, background .2s; }
    .upload-strip.is-dragging { border-color: var(--mint); background: rgba(98, 230, 167, .06); }
    .upload-icon { width: 48px; height: 48px; display: grid; place-items: center; background: #202738; color: var(--mint); border-radius: var(--radius); }
    .upload-strip h2 { font-size: 15px; margin: 0 0 5px; }
    .upload-strip p { color: var(--muted); margin: 0; font-size: 12px; }
    .primary-button, .quiet-button, .icon-button { border: 0; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; gap: 8px; border-radius: 5px; white-space: nowrap; }
    .primary-button { background: var(--mint); color: #07120d; min-height: 38px; padding: 0 17px; font-weight: 700; }
    .primary-button:hover { background: #80efb9; }
    .primary-button:disabled { opacity: .6; cursor: wait; }
    .error-banner { display: flex; gap: 8px; align-items: center; padding: 12px 15px; color: #ffc1c1; border: 1px solid rgba(255, 107, 107, .25); background: rgba(255, 107, 107, .07); margin-top: 14px; }
    .catalog-section { margin-top: 48px; padding-bottom: 90px; }
    .section-heading { display: grid; grid-template-columns: minmax(360px, 1fr) 440px; align-items: end; min-height: 52px; border-bottom: 1px solid var(--line); }
    .section-heading > div:first-child { display: flex; align-items: baseline; gap: 14px; }
    .section-heading h2 { margin: 0 0 13px; font-size: 21px; letter-spacing: -.02em; }
    .section-heading span { color: var(--muted); font-size: 11px; }
    .table-labels { display: grid; grid-template-columns: 100px 120px 120px 40px; padding: 0 10px 13px; }
    .table-labels span { letter-spacing: .03em; }
    .episode-row { appearance: none; width: 100%; display: grid; grid-template-columns: 52px minmax(308px, 1fr) 100px 120px 120px 40px; min-height: 92px; align-items: center; text-align: left; border: 0; border-bottom: 1px solid var(--line-soft); background: transparent; cursor: pointer; padding: 0 10px 0 0; }
    .episode-row:hover { background: rgba(255,255,255,.025); }
    .episode-index { color: #596275; font-size: 11px; text-align: center; }
    .episode-main { display: flex; align-items: center; gap: 16px; min-width: 0; }
    .episode-thumb { width: 94px; height: 58px; flex: 0 0 auto; position: relative; display: grid; place-items: center; color: rgba(255,255,255,.7); background: linear-gradient(145deg, #2c354b, #171d2b 62%); overflow: hidden; }
    .episode-thumb::before { content: ""; position: absolute; inset: 0; background: repeating-linear-gradient(110deg, transparent 0 12px, rgba(255,255,255,.025) 12px 13px); }
    .episode-thumb i { position: absolute; bottom: 5px; left: 6px; font-style: normal; font-size: 8px; color: var(--mint); }
    .episode-main > span:last-child { display: grid; min-width: 0; gap: 7px; }
    .episode-main strong { font-size: 14px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .episode-main small { color: var(--muted); font-size: 10px; letter-spacing: .05em; }
    .row-data { color: #a5adbc; display: flex; align-items: center; gap: 7px; font-size: 12px; }
    .status-pill { width: max-content; display: inline-flex; align-items: center; gap: 5px; padding: 5px 8px; font-size: 10px; border: 1px solid var(--line); border-radius: 20px; text-transform: capitalize; color: var(--muted); }
    .status-pill.processed { color: var(--mint); border-color: rgba(98,230,167,.25); background: rgba(98,230,167,.05); }
    .status-pill.failed { color: var(--coral); }
    .row-open { width: 32px; height: 32px; display: grid; place-items: center; color: var(--muted); border: 1px solid transparent; }
    .episode-row:hover .row-open { border-color: var(--line); color: var(--fog); }
    .empty-row { min-height: 120px; display: flex; align-items: center; justify-content: center; gap: 10px; color: var(--muted); }
    .library-footer { min-height: 67px; display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--line-soft); color: #60697a; font-size: 10px; }
    
    /* Workspace shell */
    .workspace-shell { min-height: 100vh; background: #0c0f17; }
    .workspace-header { height: 64px; position: sticky; top: 0; z-index: 30; display: flex; align-items: center; padding: 0 20px; border-bottom: 1px solid var(--line); background: rgba(11,14,22,.96); backdrop-filter: blur(16px); }
    .back-link { width: 34px; height: 34px; display: grid; place-items: center; color: var(--muted); border-right: 1px solid var(--line); margin-right: 17px; }
    .workspace-brand { display: flex; align-items: center; gap: 8px; padding-right: 19px; border-right: 1px solid var(--line); height: 34px; }
    .workspace-brand strong { font-size: 10px; letter-spacing: .16em; }
    .mini-glyph { width: 23px; height: 23px; padding: 4px; gap: 2px; }
    .mini-glyph i { width: 3px; }
    .mini-glyph i:nth-child(1) { height: 6px; }.mini-glyph i:nth-child(2) { height: 14px; }.mini-glyph i:nth-child(3) { height: 10px; }
    .episode-heading { display: flex; align-items: center; gap: 12px; min-width: 0; margin-left: 19px; }
    .episode-heading h1 { margin: 0; font-size: 14px; max-width: 360px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .episode-heading > span { color: var(--muted); font-size: 10px; padding-left: 11px; border-left: 1px solid var(--line); }
    .episode-heading .processed-mark { display: flex; align-items: center; gap: 5px; color: var(--mint); border: 0; padding: 0; text-transform: capitalize; }
    .workspace-actions { display: flex; align-items: center; gap: 8px; margin-left: auto; }
    .search-box { position: relative; width: min(25vw, 260px); height: 34px; display: flex; align-items: center; gap: 8px; color: var(--muted); background: #151a25; border: 1px solid var(--line); padding: 0 10px; border-radius: 5px; }
    .search-box input { flex: 1; min-width: 0; color: var(--fog); background: transparent; border: 0; outline: 0; font-size: 11px; }
    .search-box > button { display: grid; place-items: center; border: 0; background: transparent; color: var(--muted); padding: 2px; cursor: pointer; }
    .search-popover, .export-menu { position: absolute; top: calc(100% + 9px); z-index: 50; background: #171c29; border: 1px solid var(--line); box-shadow: 0 18px 50px rgba(0,0,0,.45); border-radius: 5px; overflow: hidden; }
    .search-popover { left: 0; right: 0; }
    .search-popover > button { width: 100%; min-height: 55px; border: 0; border-bottom: 1px solid var(--line-soft); background: transparent; color: inherit; display: grid; grid-template-columns: 1fr auto; gap: 3px 8px; padding: 9px 11px; text-align: left; cursor: pointer; }
    .search-popover button:hover, .export-menu a:hover { background: rgba(255,255,255,.04); }
    .search-popover span { grid-column: 1; color: var(--mint); font-size: 8px; }.search-popover strong { grid-column: 1; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; font-size: 11px; }.search-popover small { grid-column: 2; grid-row: 1/3; align-self: center; color: var(--muted); }.search-popover p { margin: 14px; color: var(--muted); font-size: 11px; }
    .quiet-button { min-height: 34px; padding: 0 11px; color: #bcc4d2; background: #151a25; border: 1px solid var(--line); font-size: 11px; }
    .quiet-button:hover { background: #1d2331; color: #fff; }
    .icon-button { width: 34px; height: 34px; color: var(--muted); background: transparent; border: 1px solid var(--line); }
    .export-wrap { position: relative; }.export-menu { right: 0; min-width: 200px; padding: 5px; }.export-menu a { min-height: 37px; padding: 0 10px; display: flex; align-items: center; gap: 9px; font-size: 11px; border-radius: 3px; }
    .processing-bar { min-height: 38px; display: flex; align-items: center; gap: 12px; padding: 0 22px; background: rgba(98,230,167,.05); border-bottom: 1px solid rgba(98,230,167,.16); font-size: 10px; }.processing-bar > div { flex: 1; max-width: 320px; height: 3px; background: #242c39; }.processing-bar > div i { display: block; height: 100%; background: var(--mint); }.processing-bar small { color: var(--muted); }
    
    .stage-grid { display: grid; grid-template-columns: minmax(0, 1.62fr) minmax(320px, .78fr); min-height: 420px; border-bottom: 1px solid var(--line); }
    .player-frame { position: relative; min-height: 420px; overflow: hidden; background: #10131c; border-right: 1px solid var(--line); }
    .player-frame video, .scene-visual { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain; }
    .scene-visual { overflow: hidden; background: linear-gradient(145deg, #313642, #151a24 70%); transition: background .4s; }
    .mood-warm .scene-visual { background: linear-gradient(145deg, #6a4c32, #1d232c 73%); }.mood-tense .scene-visual { background: linear-gradient(145deg, #5b2630, #171a24 70%); }.mood-relieved .scene-visual { background: linear-gradient(145deg, #35564a, #151a24 70%); }.mood-focused .scene-visual { background: linear-gradient(145deg, #2d405f, #151923 70%); }.mood-melancholic .scene-visual { background: linear-gradient(145deg, #413551, #171923 70%); }
    .visual-grain { position: absolute; inset: -20%; opacity: .13; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 160 160' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.55'/%3E%3C/svg%3E"); animation: grain .3s steps(2) infinite; }
    @keyframes grain { 0% { transform: translate(0,0) } 25% { transform: translate(3%,-2%) } 50% { transform: translate(-2%,3%) } 75% { transform: translate(2%,2%) } }
    @media (prefers-reduced-motion: reduce) { .visual-grain, .spin { animation: none; } }
    .visual-window { position: absolute; width: 33%; height: 50%; top: 9%; right: 8%; border: 7px solid rgba(9,11,18,.4); background: linear-gradient(160deg, rgba(180,197,219,.17), rgba(69,91,119,.04)); box-shadow: inset 0 0 0 1px rgba(255,255,255,.08); }.visual-window::before { content: ""; position: absolute; left: 50%; top: 0; width: 6px; height: 100%; background: rgba(9,11,18,.38); }.visual-window::after { content: ""; position: absolute; top: 54%; left: 0; height: 6px; width: 100%; background: rgba(9,11,18,.38); }
    .visual-table { position: absolute; left: 20%; right: 12%; bottom: 22%; height: 12px; background: rgba(6,8,12,.58); transform: perspective(200px) rotateX(6deg); }.visual-table::after { content: ""; position: absolute; width: 34px; height: 48px; left: 20%; top: 10px; border-left: 8px solid rgba(6,8,12,.45); border-right: 8px solid rgba(6,8,12,.45); }
    .person { position: absolute; width: 66px; height: 165px; bottom: 25%; background: rgba(5,7,10,.6); border-radius: 45% 45% 10px 10px; filter: blur(.2px); }.person::before { content: ""; position: absolute; width: 48px; height: 54px; border-radius: 50%; left: 9px; top: -43px; background: inherit; }.person-a { left: 27%; }.person-b { left: 48%; height: 178px; transform: scaleX(-1); }
    .preview-label { position: absolute; top: 16px; left: 17px; z-index: 2; display: flex; gap: 6px; align-items: center; font-size: 9px; color: rgba(255,255,255,.7); background: rgba(6,8,12,.5); padding: 6px 8px; border-radius: 3px; }
    .player-shade { position: absolute; inset: 35% 0 0; background: linear-gradient(transparent, rgba(5,7,11,.77)); pointer-events: none; }
    .caption-render { position: absolute; bottom: 77px; left: 12%; right: 12%; display: grid; justify-items: center; gap: 3px; font-family: var(--font-bn); font-size: clamp(16px, 2vw, 24px); font-weight: 600; text-align: center; text-shadow: 0 2px 4px #000, 0 0 10px #000; }.caption-render span { background: rgba(0,0,0,.4); padding: 3px 7px; }
    .player-controls { position: absolute; left: 15px; right: 15px; bottom: 12px; display: flex; align-items: center; gap: 12px; z-index: 3; }
    .play-button { width: 36px; height: 36px; display: grid; place-items: center; border: 0; border-radius: 50%; background: var(--fog); color: var(--ink); cursor: pointer; }
    .player-time { font-size: 10px; min-width: 80px; }.player-time i { color: var(--muted); font-style: normal; margin: 0 2px; }
    .player-controls input[type="range"] { --progress: 0%; flex: 1; appearance: none; height: 3px; outline: 0; background: linear-gradient(to right, var(--fog) var(--progress), rgba(255,255,255,.23) var(--progress)); cursor: pointer; }.player-controls input::-webkit-slider-thumb { appearance: none; width: 10px; height: 10px; border-radius: 50%; background: #fff; }
    .caption-toggle { display: flex; align-items: center; gap: 3px; margin-left: 2px; background: rgba(9,11,18,.72); padding: 4px; border-radius: 5px; }.caption-toggle > svg { margin: 0 3px; }.caption-toggle button { border: 0; color: var(--muted); background: transparent; padding: 3px 5px; font-size: 8px; border-radius: 2px; cursor: pointer; }.caption-toggle button.active { color: var(--ink); background: var(--fog); }
    
    .scene-inspector { padding: 22px 24px 18px; background: #121620; overflow: auto; }
    .inspector-top { display: flex; justify-content: space-between; color: var(--muted); font-size: 9px; letter-spacing: .05em; }.inspector-top strong { color: #687184; font-weight: 500; }
    .scene-inspector h2 { font-family: var(--font-bn); font-size: clamp(23px, 2.4vw, 32px); margin: 19px 0 7px; letter-spacing: -.02em; }
    .scene-time { display: flex; align-items: center; gap: 7px; color: #a4adbd; font-size: 10px; }.scene-time span { margin-left: auto; color: #626c7d; }
    .scene-summary { color: #adb5c4; line-height: 1.65; margin: 20px 0; font-family: var(--font-bn); font-size: 13px; }
    .fact-grid { display: grid; grid-template-columns: 1fr 1fr; border-top: 1px solid var(--line-soft); border-left: 1px solid var(--line-soft); }.fact-grid > div { min-height: 60px; position: relative; display: grid; align-content: center; gap: 4px; padding: 9px 10px 9px 34px; border-right: 1px solid var(--line-soft); border-bottom: 1px solid var(--line-soft); }.fact-grid svg { position: absolute; left: 11px; top: 13px; color: var(--muted); }.fact-grid span { color: #6f7889; font-size: 8px; }.fact-grid strong { font-size: 10px; font-weight: 600; }
    .intensity-block { margin-top: 19px; }.intensity-block > div:first-child { display: flex; justify-content: space-between; font-size: 9px; color: var(--muted); }.intensity-block > div strong { color: var(--fog); font-size: 13px; }.intensity-track { height: 5px; margin-top: 8px; background: #272d3b; }.intensity-track i { display: block; height: 100%; background: linear-gradient(90deg, var(--mint), var(--saffron) 60%, var(--coral)); }.intensity-block small { color: var(--coral); display: flex; gap: 5px; align-items: center; margin-top: 7px; font-size: 8px; }
    .entity-mini-list { margin-top: 18px; }.entity-mini-list > span { color: var(--muted); font-size: 9px; }.entity-mini-list > div { display: grid; grid-template-columns: 1fr auto auto; gap: 7px; align-items: center; border-bottom: 1px solid var(--line-soft); padding: 8px 0; }.entity-mini-list strong { font-family: var(--font-bn); font-size: 11px; }.entity-mini-list small { color: var(--muted); font-size: 9px; }.entity-mini-list p { color: #6f7888; font-size: 10px; }
    .presence { font-style: normal; font-size: 8px; border: 1px solid currentColor; border-radius: 20px; padding: 3px 6px; white-space: nowrap; }.presence.mentioned_and_shown { color: var(--mint); }.presence.mentioned_only { color: var(--saffron); }.presence.shown_only { color: var(--blue); }.presence.unverified { color: var(--muted); }
    
    /* Timeline */
    .timeline-block { border-bottom: 1px solid var(--line); background: #10141e; }
    .timeline-toolbar { height: 45px; display: grid; grid-template-columns: 165px 1fr auto; align-items: center; gap: 15px; padding: 0 18px; border-bottom: 1px solid var(--line-soft); }
    .timeline-title { display: flex; align-items: center; gap: 8px; font-weight: 650; font-size: 11px; }
    .lane-switches { display: flex; gap: 3px; overflow: auto; }.lane-switches button { border: 1px solid transparent; border-radius: 3px; background: transparent; color: #697386; padding: 4px 7px; font-size: 8px; cursor: pointer; }.lane-switches button.active { color: #b9c1cf; border-color: #303749; background: #191e2a; }
    .zoom-control { display: flex; align-items: center; border: 1px solid var(--line); border-radius: 4px; overflow: hidden; }.zoom-control button { width: 27px; height: 25px; display: grid; place-items: center; border: 0; background: #171c27; cursor: pointer; }.zoom-control span { min-width: 39px; text-align: center; color: var(--muted); font-size: 9px; }
    .timeline-ruler { height: 25px; display: grid; grid-template-columns: 78px 1fr; border-bottom: 1px solid var(--line-soft); }.timeline-ruler > div { position: relative; }.timeline-ruler i { position: absolute; top: 7px; transform: translateX(-50%); color: #626b7d; font-style: normal; font-size: 8px; }.timeline-ruler i:first-child { transform: none; }.timeline-ruler i:last-child { transform: translateX(-100%); }
    .timeline-chart { min-height: 182px; display: grid; grid-template-columns: 78px minmax(0,1fr); }
    .lane-labels { display: grid; grid-template-rows: 36px 25px 25px 25px 35px 36px; align-items: center; color: #788194; border-right: 1px solid var(--line-soft); font-size: 8px; }.lane-labels span { padding-left: 18px; }
    .timeline-chart svg { width: 100%; height: 182px; cursor: crosshair; touch-action: none; }
    

## Activity

    file changes: Completed · 1 changes
    Update { move_path: None }: C:\Users\asus\Desktop\hoichoi\frontend\src\app\globals.css
    @@ -160 +160,70 @@
     
    +/* Data views */
    +.data-panel { min-height: 440px; background: #10131b; }
    +.tab-list { height: 51px; display: flex; align-items: stretch; gap: 3px; padding: 0 18px; border-bottom: 1px solid var(--line); overflow-x: auto; }
    +.tab-list button { position: relative; min-width: 78px; border: 0; background: transparent; color: #7f899a; font-size: 10px; cursor: pointer; }
    +.tab-list button::after { content: ""; position: absolute; height: 2px; left: 12px; right: 12px; bottom: -1px; background: transparent; }
    +.tab-list button.active { color: #fff; }.tab-list button.active::after { background: var(--mint); }
    +.tab-list button span { margin-left: 5px; padding: 1px 5px; color: var(--saffron); background: rgba(243,182,75,.1); border-radius: 10px; font-size: 8px; }
    +.tab-body { min-height: 390px; }
    +.table-wrap { width: 100%; overflow-x: auto; }
    +.scene-table { width: 100%; border-collapse: collapse; table-layout: fixed; }
    +.scene-table th { height: 37px; padding: 0 14px; text-align: left; color: #667084; font-size: 8px; font-weight: 500; border-bottom: 1px solid var(--line-soft); }
    +.scene-table th:nth-child(1) { width: 90px; }.scene-table th:nth-child(2) { width: 40%; }.scene-table th:nth-child(3) { width: 140px; }.scene-table th:nth-child(4) { width: 110px; }.scene-table th:nth-child(5) { width: 160px; }.scene-table th:nth-child(6) { width: 75px; }
    +.scene-table td { height: 66px; padding: 8px 14px; border-bottom: 1px solid var(--line-soft); color: #aeb6c5; font-size: 10px; vertical-align: middle; }
    +.scene-table tr { cursor: pointer; }.scene-table tbody tr:hover, .scene-table tr.current { background: rgba(255,255,255,.025); }.scene-table tr.current { box-shadow: inset 2px 0 var(--mint); }
    +.scene-table td > button { border: 0; background: transparent; color: var(--mint); padding: 0; font-size: 10px; cursor: pointer; }
    +.scene-table td:nth-child(2) { display: grid; align-content: center; gap: 5px; }.scene-table td:nth-child(2) strong { color: var(--fog); font-family: var(--font-bn); font-size: 12px; }.scene-table td:nth-child(2) span { overflow: hidden; white-space: nowrap; text-overflow: ellipsis; color: #737d8f; font-family: var(--font-bn); }
    +.mood { font-style: normal; padding-left: 9px; position: relative; }.mood::before { content: ""; position: absolute; left: 0; top: 3px; width: 4px; height: 4px; border-radius: 50%; background: var(--blue); }.mood-tense::before { background: var(--coral); }.mood-warm::before { background: var(--saffron); }.mood-relieved::before { background: var(--mint); }.mood-melancholic::before { background: var(--violet); }
    +.micro-meter { display: inline-block; vertical-align: middle; width: 82px; height: 4px; background: #282f3e; margin-right: 8px; }.micro-meter i { display: block; height: 100%; background: linear-gradient(90deg, var(--mint), var(--saffron), var(--coral)); }.scene-table td small { color: #778092; font-size: 8px; }
    +
    +.transcript-list { max-width: 980px; margin: 0 auto; padding: 14px 22px 40px; }
    +.transcript-list > button { width: 100%; min-height: 71px; display: grid; grid-template-columns: 12px 125px minmax(0,1fr) 45px 50px; align-items: center; gap: 10px; border: 0; border-bottom: 1px solid var(--line-soft); background: transparent; color: inherit; text-align: left; cursor: pointer; padding: 9px 12px; }
    +.transcript-list > button:hover, .transcript-list > button.current { background: rgba(255,255,255,.025); }.transcript-list > button.current { box-shadow: inset 2px 0 var(--mint); }
    +.speaker-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--mint); }.speaker-dot.SPK_B { background: var(--blue); }.speaker-dot.SPK_C { background: #e79bef; }
    +.transcript-meta { display: grid; gap: 4px; }.transcript-meta strong { font-family: var(--font-bn); font-size: 11px; }.transcript-meta small { color: #677184; font-size: 8px; }
    +.transcript-list p { margin: 0; font-family: var(--font-bn); font-size: 15px; line-height: 1.5; }.transcript-list em { color: #778092; font-style: normal; font-size: 8px; text-align: right; }.transcript-list > button > i { color: var(--saffron); font-size: 8px; font-style: normal; }
    +
    +.entity-groups { padding: 18px 22px 40px; max-width: 1180px; margin: auto; }.entity-groups section { margin-bottom: 18px; border: 1px solid var(--line-soft); }.entity-group-title { height: 37px; display: flex; align-items: center; justify-content: space-between; padding: 0 13px; background: #151923; }.entity-group-title span { font-size: 10px; font-weight: 650; }.entity-group-title small { color: var(--muted); font-size: 8px; }
    +.entity-row { border-top: 1px solid var(--line-soft); }.entity-summary { width: 100%; min-height: 54px; display: grid; grid-template-columns: 20px minmax(160px,1fr) 140px 85px 55px; align-items: center; gap: 10px; border: 0; color: inherit; background: transparent; padding: 0 13px; text-align: left; cursor: pointer; }.entity-summary:hover, .entity-row.expanded .entity-summary { background: rgba(255,255,255,.02); }.entity-row.expanded .entity-summary > svg { transform: rotate(90deg); }
    +.entity-name { display: flex; align-items: baseline; gap: 8px; }.entity-name strong { font-family: var(--font-bn); }.entity-name small { color: var(--muted); font-size: 9px; }.sentiment { font-style: normal; font-size: 8px; color: var(--muted); }.sentiment.positive { color: var(--mint); }.sentiment.negative { color: var(--coral); }.confidence { color: var(--muted); font-size: 9px; text-align: right; }
    +.entity-detail { display: grid; grid-template-columns: .7fr 1.3fr; gap: 24px; padding: 17px 46px 20px; background: #0d1119; border-top: 1px solid var(--line-soft); }.entity-detail h4 { color: #727c8e; font-size: 8px; font-weight: 500; margin: 0 0 9px; }.entity-detail button { display: block; border: 0; padding: 5px 0; color: var(--mint); background: transparent; font-size: 9px; cursor: pointer; }.entity-detail button span { color: var(--blue); margin: 0 5px; }.entity-detail p { color: #9ba4b5; font-size: 10px; line-height: 1.55; margin: 0 0 10px; }.frame-strip { display: flex; gap: 6px; }.frame-strip > span { width: 75px; height: 43px; position: relative; overflow: hidden; background: linear-gradient(145deg,#434c5d,#1d2330); }.frame-strip i { position: absolute; right: 4px; top: 3px; color: #fff; font-size: 7px; font-style: normal; }.frame-strip small { position: absolute; left: 4px; bottom: 3px; color: #c8cfdb; font-size: 6px; }
    +
    +.ads-layout { display: grid; grid-template-columns: 260px minmax(0,1fr); min-height: 420px; }.ad-settings { padding: 19px; border-right: 1px solid var(--line); background: #121620; }.ad-settings h3 { margin: 0 0 20px; font-size: 12px; }.ad-settings label { display: grid; grid-template-columns: 1fr auto; gap: 9px; margin-bottom: 20px; color: var(--muted); font-size: 9px; }.ad-settings label strong { color: var(--fog); }.ad-settings input { grid-column: 1/3; appearance: none; height: 3px; background: #31394a; accent-color: var(--mint); }.ad-settings input::-webkit-slider-thumb { appearance: none; width: 12px; height: 12px; background: var(--mint); border-radius: 50%; }.blocked-zones { border-top: 1px solid var(--line-soft); border-bottom: 1px solid var(--line-soft); padding: 13px 0; display: grid; gap: 7px; margin-bottom: 17px; }.blocked-zones span { color: var(--muted); font-size: 8px; }.blocked-zones strong { font-size: 9px; font-weight: 500; }.ad-settings .primary-button { width: 100%; }.ad-settings > p { color: #687284; font-size: 8px; line-height: 1.5; }
    +.candidate-list { padding: 14px 18px 34px; }.candidate-card { display: grid; grid-template-columns: 36px minmax(0,1fr) 66px; border: 1px solid var(--line); margin-bottom: 9px; background: #121620; }.candidate-card.selected { border-color: rgba(243,182,75,.42); box-shadow: inset 3px 0 var(--saffron); }.candidate-rank { padding-top: 18px; color: #596275; font-size: 8px; text-align: center; }.candidate-content { padding: 14px 7px 13px; }.candidate-heading { display: flex; align-items: center; gap: 8px; }.candidate-heading > button:first-child { border: 0; display: flex; align-items: baseline; gap: 8px; background: transparent; color: inherit; padding: 0; cursor: pointer; }.candidate-heading > button strong { color: var(--saffron); }.candidate-heading > button span { color: var(--muted); font-size: 8px; }.disruption { font-style: normal; font-size: 8px; color: var(--muted); padding-left: 8px; border-left: 1px solid var(--line); }.disruption.low { color: var(--mint); }.disruption.high { color: var(--coral); }.selection-toggle { margin-left: auto; display: flex; align-items: center; gap: 5px; border: 0; color: var(--muted); background: transparent; font-size: 8px; cursor: pointer; }.selection-toggle i { width: 22px; height: 12px; border-radius: 10px; background: #363e4f; position: relative; }.selection-toggle i::after { content:""; width: 8px; height: 8px; position: absolute; top: 2px; left: 2px; background: #9ba4b5; border-radius: 50%; transition: .2s; }.selection-toggle.active { color: var(--saffron); }.selection-toggle.active i { background: rgba(243,182,75,.25); }.selection-toggle.active i::after { left: 12px; background: var(--saffron); }
    +.candidate-content > p { color: #a2abbb; margin: 12px 0; font-size: 10px; line-height: 1.5; }.score-bar { display: flex; gap: 2px; height: 5px; background: #232a38; }.score-bar i { display: block; height: 100%; }.score-legend { display: flex; flex-wrap: wrap; gap: 11px; margin-top: 6px; }.score-legend span { color: #697386; font-size: 7px; }.total-score { display: grid; place-content: center; justify-items: center; border-left: 1px solid var(--line-soft); }.total-score strong { font-size: 22px; }.total-score span { color: var(--muted); font-size: 7px; }
    +
    +.subtitle-layout { padding: 15px 20px 40px; max-width: 1100px; margin: auto; }.subtitle-tools { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }.subtitle-tools > div:last-child { display: flex; gap: 6px; }.segmented { display: inline-flex; background: #181d29; padding: 3px; border-radius: 4px; }.segmented button { border: 0; background: transparent; color: var(--muted); padding: 6px 10px; font-size: 9px; cursor: pointer; border-radius: 3px; }.segmented button.active { background: #2a3141; color: #fff; }
    +.cue-list { border: 1px solid var(--line-soft); }.cue-list > button { width: 100%; min-height: 57px; display: grid; grid-template-columns: 35px 120px minmax(0,1fr) 55px 55px; align-items: center; border: 0; border-bottom: 1px solid var(--line-soft); color: inherit; background: transparent; text-align: left; padding: 8px 11px; cursor: pointer; }.cue-list > button:hover { background: rgba(255,255,255,.025); }.cue-list > button > span { color: #5f6879; font-size: 8px; }.cue-list time { color: var(--mint); font-size: 8px; }.cue-list p { white-space: pre-line; margin: 0; font-family: var(--font-bn); font-size: 13px; }.cue-list em { color: var(--muted); font-size: 8px; font-style: normal; }.cue-list em.warn { color: var(--coral); }.cue-list > button > i { color: var(--blue); font-style: normal; font-size: 8px; }.cue-list > button > i.sound { color: var(--saffron); }
    +
    +.qc-layout { display: grid; grid-template-columns: 220px minmax(0,1fr); min-height: 390px; }.qc-summary { padding: 18px; border-right: 1px solid var(--line); background: #121620; }.qc-summary > div { min-height: 48px; display: flex; align-items: baseline; gap: 9px; padding: 10px 0; border-bottom: 1px solid var(--line-soft); }.qc-summary strong { font-size: 20px; }.qc-summary span { color: var(--muted); font-size: 9px; }.qc-summary p { display: flex; align-items: center; gap: 7px; color: var(--mint); font-size: 9px; line-height: 1.5; margin-top: 18px; }.qc-content { padding: 14px 18px 30px; }.filter-row { height: 32px; display: flex; align-items: center; gap: 5px; color: var(--muted); margin-bottom: 8px; }.filter-row button { border: 1px solid transparent; color: var(--muted); background: transparent; padding: 4px 8px; font-size: 8px; cursor: pointer; border-radius: 3px; }.filter-row button.active { color: var(--fog); border-color: var(--line); background: #181d28; }
    +.issue-list { border: 1px solid var(--line-soft); }.issue-list > button { width: 100%; min-height: 71px; display: grid; grid-template-columns: 34px minmax(0,1fr) 60px 20px; align-items: center; gap: 8px; border: 0; border-bottom: 1px solid var(--line-soft); color: inherit; background: transparent; text-align: left; padding: 9px 12px; cursor: pointer; }.issue-list > button:hover { background: rgba(255,255,255,.025); }.issue-icon { width: 28px; height: 28px; display: grid; place-items: center; border-radius: 50%; color: var(--blue); background: rgba(129,167,255,.08); }.issue-icon.warn { color: var(--saffron); background: rgba(243,182,75,.08); }.issue-main { display: grid; gap: 3px; }.issue-main strong { font-size: 10px; }.issue-main p { margin: 0; color: #a4adbd; font-size: 10px; }.issue-main small { color: #697386; font-size: 8px; }.issue-list time { color: var(--mint); font-size: 9px; }
    +
    +.json-view { margin: 18px; border: 1px solid var(--line); background: #0c0f16; }.json-tools { min-height: 45px; display: flex; align-items: center; justify-content: space-between; padding: 0 11px; border-bottom: 1px solid var(--line); background: #141924; }.json-tools > div { display: flex; align-items: center; gap: 8px; }.json-tools strong { font-size: 10px; }.json-tools span { color: var(--muted); font-size: 8px; }.json-view pre { max-height: 520px; overflow: auto; margin: 0; padding: 18px; color: #9fc7ff; font: 10px/1.65 "Cascadia Code", Consolas, monospace; white-space: pre-wrap; }
    +
    +.state-screen { min-height: 100vh; display: grid; place-content: center; justify-items: center; text-align: center; background: radial-gradient(circle at 50% 43%, #1b2434, var(--ink) 42%); }.state-screen h1 { margin: 23px 0 8px; font-size: 25px; }.state-screen p { color: var(--muted); max-width: 440px; line-height: 1.6; }.state-screen.error svg { color: var(--coral); }.state-screen .primary-button { margin-top: 14px; }
    +
    +@media (max-width: 1000px) {
    +  .section-heading { grid-template-columns: 1fr; }.table-labels { display: none; }
    +  .episode-row { grid-template-columns: 44px minmax(280px,1fr) 100px 100px 40px; }.episode-row .date { display: none; }
    +  .workspace-brand { display: none; }.episode-heading { margin-left: 0; }.episode-heading > span:not(.processed-mark) { display: none; }
    +  .search-box { width: 190px; }
    +  .stage-grid { grid-template-columns: 1.4fr 1fr; }.scene-inspector { padding: 18px; }.fact-grid { grid-template-columns: 1fr; }.fact-grid > div { min-height: 45px; }.entity-mini-list { display: none; }
    +  .caption-toggle > svg { display: none; }
    +}
    +
    +@media (max-width: 760px) {
    +  .library-shell { padding: 0 17px; }.header-note { display: none; }.library-intro { min-height: 320px; }.library-intro h1 { font-size: 48px; }.intro-mark { right: -70px; font-size: 210px; }
    +  .upload-strip { grid-template-columns: auto 1fr; }.upload-strip .primary-button { grid-column: 1/3; }.catalog-section { margin-top: 34px; }
    +  .episode-row { grid-template-columns: minmax(0,1fr) auto; padding: 10px 4px; min-height: 82px; }.episode-index, .episode-row .row-data, .episode-row .status-pill { display: none; }.episode-thumb { width: 70px; height: 48px; }.row-open { display: grid; }
    +  .library-footer { gap: 15px; }.library-footer span:nth-child(2) { display: none; }
    +  .workspace-header { padding: 0 10px; }.back-link { margin-right: 8px; }.episode-heading h1 { max-width: 180px; }.episode-heading .processed-mark { display: none; }.search-box { width: 34px; padding: 0; justify-content: center; border: 0; background: transparent; }.search-box input { display: none; }.search-box:focus-within { position: absolute; left: 50px; right: 10px; width: auto; z-index: 50; padding: 0 10px; background: #151a25; border: 1px solid var(--line); justify-content: flex-start; }.search-box:focus-within input { display: block; }.workspace-actions .quiet-button { font-size: 0; }.workspace-actions .quiet-button svg:last-child { display: none; }.icon-button { display: none; }
    +  .stage-grid { grid-template-columns: 1fr; }.player-frame { min-height: 310px; border-right: 0; }.scene-inspector { min-height: 350px; }.fact-grid { grid-template-columns: 1fr 1fr; }.entity-mini-list { display: block; }
    +  .timeline-toolbar { grid-template-columns: 1fr auto; }.lane-switches { grid-column: 1/3; grid-row: 2; padding-bottom: 6px; }.timeline-toolbar { height: auto; min-height: 70px; align-content: center; }.timeline-chart, .timeline-ruler { grid-template-columns: 58px minmax(0,1fr); }.lane-labels span { padding-left: 8px; }.timeline-ruler { grid-template-columns: 58px 1fr; }
    +  .scene-table { min-width: 850px; }
    +  .transcript-list { padding: 10px; }.transcript-list > button { grid-template-columns: 10px 75px minmax(0,1fr); }.transcript-list > button > em, .transcript-list > button > i { display: none; }.transcript-list p { font-size: 13px; }
    +  .entity-summary { grid-template-columns: 18px minmax(110px,1fr) 115px; }.entity-summary .sentiment, .entity-summary .confidence { display: none; }.entity-detail { grid-template-columns: 1fr; padding: 15px 20px; }
    +  .ads-layout { grid-template-columns: 1fr; }.ad-settings { border-right: 0; border-bottom: 1px solid var(--line); }.candidate-list { padding: 10px; }.candidate-card { grid-template-columns: 25px minmax(0,1fr) 52px; }.candidate-heading { flex-wrap: wrap; }.disruption { display: none; }
    +  .cue-list > button { grid-template-columns: 25px 96px minmax(140px,1fr); }.cue-list > button em, .cue-list > button > i { display: none; }.cue-list { overflow-x: auto; }.subtitle-layout { padding: 12px; }
    +  .qc-layout { grid-template-columns: 1fr; }.qc-summary { display: flex; gap: 18px; border-right: 0; border-bottom: 1px solid var(--line); }.qc-summary > div { flex: 1; }.qc-summary p { display: none; }.qc-content { padding: 10px; }
    +}

## Assistant

The full workspace is now wired: synced scene inspector, playable demo state, clickable timeline lanes, entity evidence, transparent ad scores and re-selection, subtitle/CC downloads, QC seeking, JSON copy/export, upload flow, and responsive layouts. I’m at the verification pass now—installing the pinned frontend dependencies, compiling Next.js, and fixing any type or runtime issues that surface.

## Assistant

Dependency installation is stalled without output, which usually indicates the sandboxed registry connection rather than a project error. I’m checking it once more; if the registry is blocked, I’ll re-run the same install with the required network approval instead of changing the implementation.

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'npm.cmd install'
    status: Failed · exit 1

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'npm.cmd install'
    status: Completed · exit 0
      npm warn deprecated next@15.2.4: This version has a security vulnerability. Please upgrade to a patched version. See https://nextjs.org/blog/CVE-2025-66478 for more details.
      
      added 35 packages, and audited 36 packages in 1m
      
      5 packages are looking for funding
        run `npm fund` for details
      
      3 vulnerabilities (2 high, 1 critical)
      
      To address all issues, run:
        npm audit fix --force
      
      Run `npm audit` for details.

## Assistant

The build dependencies installed, but npm correctly flagged the initially pinned Next.js release for a published security issue. I won’t leave that in the project; I’m checking the registry for the current patched stable release, updating the pin, and then compiling against it.

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'npm.cmd view next version'
    status: Completed · exit 0
      16.3.6

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'npm.cmd view next@16.3.6 peerDependencies engines'
    status: Failed · exit 1
      npm error code EACCES
      npm error errno EACCES
      npm error FetchError: request to https://registry.npmjs.org/next failed, reason:
      npm error     at ClientRequest.<anonymous> (C:\Users\asus\AppData\Roaming\npm\node_modules\npm\node_modules\minipass-fetch\lib\index.js:130:14)
      npm error     at ClientRequest.emit (node:events:519:28)
      npm error     at emitErrorEvent (node:_http_client:107:11)
      npm error     at _destroy (node:_http_client:954:9)
      npm error     at onSocketNT (node:_http_client:974:5)
      npm error     at process.processTicksAndRejections (node:internal/process/task_queues:91:21) {
      npm error   code: 'EACCES',
      npm error   errno: 'EACCES',
      npm error   type: 'system'
      npm error }
      npm error
      npm error The operation was rejected by your operating system.
      npm error It's possible that the file was already in use (by a text editor or antivirus),
      npm error or that you lack permissions to access it.
      npm error
      npm error If you believe this might be a permissions issue, please double-check the
      npm error permissions of the file and its containing directories, or try running
      npm error the command again as root/Administrator.
      npm error Log files were not written due to an error writing to the directory: C:\Users\asus\AppData\Local\npm-cache\_logs
      npm error You can rerun the command with `--loglevel=verbose` to see the logs in your terminal

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'npm.cmd view react version'
    status: Completed · exit 0
      19.3.0

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'npm.cmd view next@16.3.6 peerDependencies --json'
    status: Failed · exit 1
      npm error code EACCES
      npm error errno EACCES
      npm error FetchError: request to https://registry.npmjs.org/next failed, reason:
      npm error     at ClientRequest.<anonymous> (C:\Users\asus\AppData\Roaming\npm\node_modules\npm\node_modules\minipass-fetch\lib\index.js:130:14)
      npm error     at ClientRequest.emit (node:events:519:28)
      npm error     at emitErrorEvent (node:_http_client:107:11)
      npm error     at _destroy (node:_http_client:954:9)
      npm error     at onSocketNT (node:_http_client:974:5)
      npm error     at process.processTicksAndRejections (node:internal/process/task_queues:91:21) {
      npm error   code: 'EACCES',
      npm error   errno: 'EACCES',
      npm error   type: 'system'
      npm error }
      npm error
      npm error The operation was rejected by your operating system.
      npm error It's possible that the file was already in use (by a text editor or antivirus),
      npm error or that you lack permissions to access it.
      npm error
      npm error If you believe this might be a permissions issue, please double-check the
      npm error permissions of the file and its containing directories, or try running
      npm error the command again as root/Administrator.
      {
        "error": {
          "code": "EACCES",
          "summary": "FetchError: request to https://registry.npmjs.org/next failed, reason:",
          "detail": "The operation was rejected by your operating system.\nIt's possible that the file was already in use (by a text editor or antivirus),\nor that you lack permissions to access it.\n\nIf you believe this might be a permissions issue, please double-check the\npermissions of the file and its containing directories, or try running\nthe command again as root/Administrator."
        }
      }
      npm error Log files were not written due to an error writing to the directory: C:\Users\asus\AppData\Local\npm-cache\_logs
      npm error You can rerun the command with `--loglevel=verbose` to see the logs in your terminal

## Activity

    file changes: Completed · 1 changes
    Update { move_path: None }: C:\Users\asus\Desktop\hoichoi\frontend\package.json
    @@ -12,5 +12,5 @@
         "lucide-react": "^0.468.0",
    -    "next": "15.2.4",
    -    "react": "19.0.0",
    -    "react-dom": "19.0.0"
    +    "next": "16.3.6",
    +    "react": "19.3.0",
    +    "react-dom": "19.3.0"
       },
    @@ -23,2 +23 @@
     }
    -

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'npm.cmd view next@16.3.6 engines --json'
    status: Failed · exit 1
      npm error code EACCES
      npm error errno EACCES
      npm error FetchError: request to https://registry.npmjs.org/next failed, reason:
      npm error     at ClientRequest.<anonymous> (C:\Users\asus\AppData\Roaming\npm\node_modules\npm\node_modules\minipass-fetch\lib\index.js:130:14)
      npm error     at ClientRequest.emit (node:events:519:28)
      npm error     at emitErrorEvent (node:_http_client:107:11)
      npm error     at _destroy (node:_http_client:954:9)
      npm error     at onSocketNT (node:_http_client:974:5)
      npm error     at process.processTicksAndRejections (node:internal/process/task_queues:91:21) {
      npm error   code: 'EACCES',
      npm error   errno: 'EACCES',
      npm error   type: 'system'
      npm error }
      npm error
      npm error The operation was rejected by your operating system.
      npm error It's possible that the file was already in use (by a text editor or antivirus),
      npm error or that you lack permissions to access it.
      npm error
      npm error If you believe this might be a permissions issue, please double-check the
      npm error permissions of the file and its containing directories, or try running
      npm error the command again as root/Administrator.
      {
        "error": {
          "code": "EACCES",
          "summary": "FetchError: request to https://registry.npmjs.org/next failed, reason:",
          "detail": "The operation was rejected by your operating system.\nIt's possible that the file was already in use (by a text editor or antivirus),\nor that you lack permissions to access it.\n\nIf you believe this might be a permissions issue, please double-check the\npermissions of the file and its containing directories, or try running\nthe command again as root/Administrator."
        }
      }
      npm error Log files were not written due to an error writing to the directory: C:\Users\asus\AppData\Local\npm-cache\_logs
      npm error You can rerun the command with `--loglevel=verbose` to see the logs in your terminal

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'npm.cmd install'
    status: Completed · exit 0
      npm warn cleanup Failed to remove some directories [
      npm warn cleanup   [
      npm warn cleanup     'C:\\Users\\asus\\Desktop\\hoichoi\\frontend\\node_modules\\@next\\.swc-win32-x64-msvc-6VFtmzZG',
      npm warn cleanup     [Error: EPERM: operation not permitted, unlink 'C:\Users\asus\Desktop\hoichoi\frontend\node_modules\@next\.swc-win32-x64-msvc-6VFtmzZG\next-swc.win32-x64-msvc.node'] {
      npm warn cleanup       errno: -4048,
      npm warn cleanup       code: 'EPERM',
      npm warn cleanup       syscall: 'unlink',
      npm warn cleanup       path: 'C:\\Users\\asus\\Desktop\\hoichoi\\frontend\\node_modules\\@next\\.swc-win32-x64-msvc-6VFtmzZG\\next-swc.win32-x64-msvc.node'
      npm warn cleanup     }
      npm warn cleanup   ]
      npm warn cleanup ]
      
      added 4 packages, removed 9 packages, changed 10 packages, and audited 31 packages in 2m
      
      5 packages are looking for funding
        run `npm fund` for details
      
      found 0 vulnerabilities

## Assistant

The frontend is now on Next.js 16.3.6 with React 19.3.0, and npm reports zero known vulnerabilities. I’m compiling the production bundle next; this is the pass that catches strict TypeScript issues and App Router incompatibilities.

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'npm.cmd run build'
    status: Completed · exit 0
      
      > hoichoi-drishti-web@0.1.0 build
      > next build
      
      ▲ Next.js 16.3.6 (Turbopack)
      ✓ Running next.config.ts took 375ms
      
        Creating an optimized production build ...
      ✓ Compiled successfully in 21.4s
        Running TypeScript ...
      
        We detected TypeScript in your project and reconfigured your tsconfig.json file for you.
        The following suggested values were added to your tsconfig.json. These values can be changed to fit your project's needs:
      
        	- include was updated to add '.next/dev/types/**/*.ts'
      
        The following mandatory changes were made to your tsconfig.json:
      
        	- jsx was set to react-jsx (next.js uses the React automatic runtime)
      
        Finished TypeScript in 10.6s ...
        Collecting page data using 5 workers ...
        Generating static pages using 5 workers (0/3) ...
      ✓ Generating static pages using 5 workers (3/3) in 3.6s
        Finalizing page optimization ...
      
      Route (app)
      ┌ ○ /
      ├ ○ /_not-found
      └ ƒ /episode/[id]
      
      
      ○  (Static)   prerendered as static content
      ƒ  (Dynamic)  server-rendered on demand
      

## Assistant

The production Next.js build now compiles cleanly, including strict TypeScript and static route generation. I’m adding the runbook and environment templates, then doing a final repository/status audit so the handoff is reproducible rather than just “works on my machine.”

## Activity

    file changes: Completed · 5 changes
    Add: C:\Users\asus\Desktop\hoichoi\.gitignore
    # Python
    __pycache__/
    *.py[cod]
    .pytest_cache/
    .venv/
    
    # Next.js / Node
    frontend/node_modules/
    frontend/.next/
    frontend/.env.local
    npm-debug.log*
    
    # Runtime episode artifacts
    data/episodes/*
    !data/episodes/.gitkeep
    
    # Editor / OS
    .DS_Store
    Thumbs.db
    .idea/
    .vscode/
    
    Add: C:\Users\asus\Desktop\hoichoi\README.md
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
    
    Add: C:\Users\asus\Desktop\hoichoi\backend\.env.example
    OPENAI_API_KEY=
    SARVAM_API_KEY=
    HF_TOKEN=
    DATA_DIR=../data
    REDIS_URL=redis://localhost:6379
    LLM_MODEL_DEFAULT=gpt-4.1-mini
    LLM_MODEL_SCENES=gpt-4.1-mini
    MAX_LLM_USD_PER_EPISODE=5
    DEVICE=cpu
    
    Add: C:\Users\asus\Desktop\hoichoi\data\episodes\.gitkeep
    
    Add: C:\Users\asus\Desktop\hoichoi\frontend\.env.local.example
    NEXT_PUBLIC_API_URL=http://localhost:8000
    

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "python -m pytest backend\\tests -q; python -m compileall -q backend\\app; git status --short; rg --files -g '"'!frontend/node_modules'"' -g '"'!frontend/.next'"' | Sort-Object"
    status: Completed · exit 0
      2026-09-26T09:17:38.938198Z [warning  ] The configuration option "asyncio_default_fixture_loop_scope" is unset.
      The event loop scope for asynchronous fixtures will default to the fixture caching scope. Future versions of pytest-asyncio will default the loop scope for asynchronous fixtures to function scope. Set the default fixture loop scope explicitly in order to avoid unexpected behavior in the future. Valid fixture loop scopes are: "function", "class", "module", "package", "session"
       [py.warnings] category=PytestDeprecationWarning filename=C:\Users\asus\AppData\Local\Programs\Python\Python311\Lib\site-packages\pytest_asyncio\plugin.py lineno=208
      ...                                                                      [100%]
      3 passed in 1.18s
      ?? .gitignore
      ?? README.md
      ?? backend/
      ?? data/
      ?? docs/
      ?? frontend/
      backend\app\__init__.py
      backend\app\demo_data.py
      backend\app\main.py
      backend\app\models.py
      backend\pyproject.toml
      backend\tests\test_api.py
      data\episodes\.gitkeep
      docs\prd.md
      docs\technical.md
      frontend\next.config.ts
      frontend\next-env.d.ts
      frontend\package.json
      frontend\package-lock.json
      frontend\src\app\episode\[id]\page.tsx
      frontend\src\app\globals.css
      frontend\src\app\layout.tsx
      frontend\src\app\page.tsx
      frontend\src\components\SemanticTimeline.tsx
      frontend\src\components\Workspace.tsx
      frontend\src\lib\api.ts
      frontend\src\lib\format.ts
      frontend\src\lib\types.ts
      frontend\tsconfig.json
      README.md

## Activity

    file changes: Completed · 1 changes
    Update { move_path: None }: C:\Users\asus\Desktop\hoichoi\backend\pyproject.toml
    @@ -17,2 +17,2 @@
     pythonpath = ["."]
    -
    +asyncio_default_fixture_loop_scope = "function"

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command '$api = Invoke-WebRequest -UseBasicParsing '"'http://127.0.0.1:8000/episodes'; "'$web = Invoke-WebRequest -UseBasicParsing '"'http://127.0.0.1:3000'; Write-Output \"API "'$($api.StatusCode) episodes=$((ConvertFrom-Json $api.Content).Count)"; Write-Output "WEB $($web.StatusCode) bytes=$($web.Content.Length)"'
    status: Completed · exit 0
      API 200 episodes=1
      WEB 200 bytes=8166

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'Get-NetTCPConnection -State Listen | Where-Object { $_.LocalPort -in 3000,8000 } | Select-Object LocalPort,OwningProcess'
    status: Failed · exit 1
      Get-NetTCPConnection : Access denied
      At line:2 char:1
      + Get-NetTCPConnection -State Listen | Where-Object { $_.LocalPort -in  ...
      + ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          + CategoryInfo          : PermissionDenied: (MSFT_NetTCPConnection:ROOT/StandardCimv2/MSFT_NetTCPConnection) [Get-
         NetTCPConnection], CimException
          + FullyQualifiedErrorId : HRESULT 0x80041003,Get-NetTCPConnection
      

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "try { (Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 'http://127.0.0.1:8000/health').StatusCode } catch { 'api stopped' }; try { (Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 'http://127.0.0.1:3000').StatusCode } catch { 'web stopped' }"
    status: Completed · exit 0
      200
      200

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-CimInstance Win32_Process -Filter \"Name = 'node.exe' OR ProcessId = 1340\" | Select-Object ProcessId,ParentProcessId,CommandLine"
    status: Failed · exit 1
      Get-CimInstance : Access denied
      At line:2 char:1
      + Get-CimInstance Win32_Process -Filter "Name = 'node.exe' OR ProcessId ...
      + ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          + CategoryInfo          : PermissionDenied: (:) [Get-CimInstance], CimException
          + FullyQualifiedErrorId : HRESULT 0x80041003,Microsoft.Management.Infrastructure.CimCmdlets.GetCimInstanceCommand
      

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'Get-Process -Name node,python -ErrorAction SilentlyContinue | Select-Object Id,ProcessName,StartTime,Path'
    status: Completed · exit 0
      
         Id ProcessName StartTime           Path
         -- ----------- ---------           ----
       3728 node        26-09-2026 14:47:58 C:\Program Files\nodejs\node.exe
      13188 node        26-09-2026 12:45:28 C:\Program Files\nodejs\node.EXE
      15488 node        26-09-2026 13:40:10 C:\Program Files\nodejs\node.exe
      29856 node        26-09-2026 14:47:57 C:\Program Files\nodejs\node.exe
       1340 python      26-09-2026 14:47:57 C:\Users\asus\AppData\Local\Programs\Python\Python311\python.exe
       4432 python      26-09-2026 12:45:27 C:\Users\asus\Desktop\proj\clawnet\.venv\Scripts\python.exe
       4776 python      26-09-2026 13:56:30 C:\Users\asus\AppData\Local\Programs\Python\Python311\python.exe
      21584 python      26-09-2026 13:56:30 C:\Users\asus\Desktop\proj\clawnet\.venv\Scripts\python.exe
      21708 python      26-09-2026 12:45:27 C:\Users\asus\AppData\Local\Programs\Python\Python311\python.exe
      24604 python      26-09-2026 12:57:46 C:\Users\asus\Desktop\proj\clawnet\.venv\Scripts\python.exe
      27600 python      26-09-2026 12:57:46 C:\Users\asus\AppData\Local\Programs\Python\Python311\python.exe
      
      

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'Stop-Process -Id 1340,29856,3728 -Force -ErrorAction SilentlyContinue'
    status: Completed · exit 0

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'python -m uvicorn app.main:app --host 127.0.0.1 --port 8000'
    status: Failed · exit 1
      INFO:     Started server process [1340]
      ]0;C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exeINFO:     Waiting for application startup.
      INFO:     Application startup complete.
      INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
      INFO:     127.0.0.1:62010 - "GET /episodes HTTP/1.1" 200 OK
      INFO:     127.0.0.1:54446 - "GET /health HTTP/1.1" 200 OK
      

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'npm.cmd start'
    status: Failed · exit 1
      ]0;C:\WINDOWS\system32\cmd.exe ]0;npm]0;npm start
      > hoichoi-drishti-web@0.1.0 start
      > next start]0;C:\WINDOWS\system32\cmd.exe ]0;next-server (v16.3.6)▲ Next.js 16.3.6
      - Local:         http://localhost:3000
      - Network:       http://10.20.17.234:3000
      ✓ Ready in 713ms
      ✓ Running next.config.ts took 266ms
      ⚠ "next start" does not work with "output: standalone" configuration. Use "node .next/standalone/server.js" instead.
      ]0;C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe

## Activity

    file changes: Completed · 1 changes
    Update { move_path: None }: C:\Users\asus\Desktop\hoichoi\frontend\next.config.ts
    @@ -2,7 +2,4 @@
     
    -const nextConfig: NextConfig = {
    -  output: "standalone",
    -};
    +const nextConfig: NextConfig = {};
     
     export default nextConfig;
    -

## Assistant

Both services passed a live smoke test (`200` from the episode API and rendered Next.js page). I also removed an unnecessary standalone-output setting that made `next start` warn despite serving correctly; the final build now matches the documented local commands.

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'npm.cmd run build'
    status: Completed · exit 0
      
      > hoichoi-drishti-web@0.1.0 build
      > next build
      
      ▲ Next.js 16.3.6 (Turbopack)
      ✓ Running next.config.ts took 55ms
      
        Creating an optimized production build ...
      ✓ Compiled successfully in 2.3s
        Running TypeScript ...
        Finished TypeScript in 2.9s ...
        Collecting page data using 5 workers ...
        Generating static pages using 5 workers (0/3) ...
      ✓ Generating static pages using 5 workers (3/3) in 1380ms
        Finalizing page optimization ...
      
      Route (app)
      ┌ ○ /
      ├ ○ /_not-found
      └ ƒ /episode/[id]
      
      
      ○  (Static)   prerendered as static content
      ƒ  (Dynamic)  server-rendered on demand
      

## Assistant

Built the Next.js + FastAPI app from the docs.

Highlights:

- Functional episode library, upload, workspace, timeline, tabs, exports, subtitles, QC, and ad scoring.
- Bengali-focused control-room design with responsive layouts.
- Demo episode included.
- FastAPI endpoints, SSE progress, schemas, and tests.
- Next.js 16.3.6 / React 19.3.0 with zero npm vulnerabilities.

Verification:

- Backend: 3 tests passed.
- Frontend: production build passed.
- Live API and UI smoke tests returned `200`.

Run instructions are in [README.md](C:/Users/asus/Desktop/hoichoi/README.md). Core files: [Workspace.tsx](C:/Users/asus/Desktop/hoichoi/frontend/src/components/Workspace.tsx), [main.py](C:/Users/asus/Desktop/hoichoi/backend/app/main.py).

## User

make the backend properly seeing docs

## Assistant

You’re right—the current backend is a demo contract, not the documented production architecture. I’ll replace it with persistent SQLite episode/stage state, artifact-backed timelines, an 18-stage cached DAG, real media ingest/probing, deterministic subtitle/QC/ad logic, worker progress, and provider boundaries for Sarvam/OpenAI and GPU stages. The demo will remain only as seeded data, not as the fallback output for uploads.

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "python -c \"import importlib.util as i; print('sqlmodel', bool(i.find_spec('sqlmodel'))); print('yaml', bool(i.find_spec('yaml'))); print('regex', bool(i.find_spec('regex'))); print('srt', bool(i.find_spec('srt'))); print('httpx', bool(i.find_spec('httpx')))\"; ffmpeg -version | Select-Object -First 1; ffprobe -version | Select-Object -First 1; rg --files backend"
    status: Completed · exit 0
      sqlmodel False
      yaml True
      regex True
      srt False
      httpx True
      ffmpeg version 8.1.2-full_build-www.gyan.dev Copyright (c) 2000-2026 the FFmpeg developers
      ffprobe version 8.1.2-full_build-www.gyan.dev Copyright (c) 2007-2026 the FFmpeg developers
      backend\tests\test_api.py
      backend\pyproject.toml
      backend\app\__init__.py
      backend\app\models.py
      backend\app\main.py
      backend\app\demo_data.py

## Assistant

The first architectural correction is persistence and artifact ownership: uploads will no longer inherit the demo timeline. Each episode will own its source, stage JSON, outputs, logs, database records, cache manifests, and errors. A failed external provider stage will stay failed with a retryable error instead of silently manufacturing results.

## Activity

    file changes: Completed · 5 changes
    Add: C:\Users\asus\Desktop\hoichoi\backend\app\artifacts.py
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
    
    Add: C:\Users\asus\Desktop\hoichoi\backend\app\db.py
    from __future__ import annotations
    
    from datetime import UTC, datetime
    from pathlib import Path
    
    from sqlmodel import Field, Session, SQLModel, create_engine, select
    
    from .models import EpisodeSummary, StageStatus
    from .settings import Settings
    
    
    def utc_now() -> datetime:
        return datetime.now(UTC)
    
    
    class EpisodeRecord(SQLModel, table=True):
        id: str = Field(primary_key=True)
        title: str
        source_path: str
        duration: float = 0.0
        fps: float = 0.0
        width: int = 0
        height: int = 0
        status: str = "queued"
        progress: int = 0
        video_available: bool = False
        created_at: datetime = Field(default_factory=utc_now)
        updated_at: datetime = Field(default_factory=utc_now)
    
    
    class StageRecord(SQLModel, table=True):
        pk: int | None = Field(default=None, primary_key=True)
        episode_id: str = Field(index=True)
        stage_id: str
        label: str
        position: int
        status: str = "queued"
        elapsed: float | None = None
        error: str | None = None
        input_hash: str | None = None
        started_at: datetime | None = None
        finished_at: datetime | None = None
    
    
    class Database:
        def __init__(self, settings: Settings):
            self.settings = settings
            settings.data_dir.mkdir(parents=True, exist_ok=True)
            connect_args = {"check_same_thread": False} if settings.sqlite_url.startswith("sqlite") else {}
            self.engine = create_engine(settings.sqlite_url, connect_args=connect_args)
            SQLModel.metadata.create_all(self.engine)
    
        def session(self) -> Session:
            return Session(self.engine)
    
        def create_episode(self, record: EpisodeRecord, stages: list[tuple[str, str]]) -> None:
            with self.session() as session:
                session.add(record)
                session.add_all([
                    StageRecord(episode_id=record.id, stage_id=stage_id, label=label, position=index)
                    for index, (stage_id, label) in enumerate(stages)
                ])
                session.commit()
    
        def get_episode_record(self, episode_id: str) -> EpisodeRecord | None:
            with self.session() as session:
                return session.get(EpisodeRecord, episode_id)
    
        def list_episode_records(self) -> list[EpisodeRecord]:
            with self.session() as session:
                return list(session.exec(select(EpisodeRecord).order_by(EpisodeRecord.created_at.desc())).all())
    
        def get_stages(self, episode_id: str) -> list[StageRecord]:
            with self.session() as session:
                statement = select(StageRecord).where(StageRecord.episode_id == episode_id).order_by(StageRecord.position)
                return list(session.exec(statement).all())
    
        def update_episode(self, episode_id: str, **values: object) -> EpisodeRecord:
            with self.session() as session:
                record = session.get(EpisodeRecord, episode_id)
                if record is None:
                    raise KeyError(episode_id)
                for key, value in values.items():
                    setattr(record, key, value)
                record.updated_at = utc_now()
                session.add(record)
                session.commit()
                session.refresh(record)
                return record
    
        def update_stage(self, episode_id: str, stage_id: str, **values: object) -> StageRecord:
            with self.session() as session:
                statement = select(StageRecord).where(StageRecord.episode_id == episode_id, StageRecord.stage_id == stage_id)
                record = session.exec(statement).one()
                for key, value in values.items():
                    setattr(record, key, value)
                session.add(record)
                session.commit()
                session.refresh(record)
                return record
    
        def reset_from(self, episode_id: str, stage_id: str) -> None:
            stages = self.get_stages(episode_id)
            start = next((stage.position for stage in stages if stage.stage_id == stage_id), None)
            if start is None:
                raise KeyError(stage_id)
            with self.session() as session:
                statement = select(StageRecord).where(StageRecord.episode_id == episode_id, StageRecord.position >= start)
                for stage in session.exec(statement).all():
                    stage.status = "queued"
                    stage.elapsed = None
                    stage.error = None
                    stage.input_hash = None
                    stage.started_at = None
                    stage.finished_at = None
                    session.add(stage)
                episode = session.get(EpisodeRecord, episode_id)
                if episode:
                    episode.status = "queued"
                    episode.progress = round(start / max(1, len(stages)) * 100)
                    episode.updated_at = utc_now()
                    session.add(episode)
                session.commit()
    
        def summary(self, record: EpisodeRecord) -> EpisodeSummary:
            stages = self.get_stages(record.id)
            return EpisodeSummary(
                id=record.id,
                title=record.title,
                duration=record.duration,
                status=record.status,  # type: ignore[arg-type]
                progress=record.progress,
                created_at=record.created_at.isoformat(),
                video_available=record.video_available,
                stages=[StageStatus(
                    id=stage.stage_id,
                    label=stage.label,
                    status=stage.status,  # type: ignore[arg-type]
                    elapsed=stage.elapsed,
                    error=stage.error,
                    started_at=stage.started_at.isoformat() if stage.started_at else None,
                    finished_at=stage.finished_at.isoformat() if stage.finished_at else None,
                ) for stage in stages],
            )
    
        def close(self) -> None:
            self.engine.dispose()
    
    Update { move_path: None }: C:\Users\asus\Desktop\hoichoi\backend\app\models.py
    @@ -12,2 +12,5 @@
         elapsed: float | None = None
    +    error: str | None = None
    +    started_at: str | None = None
    +    finished_at: str | None = None
     
    @@ -22,5 +25,14 @@
         video_available: bool = False
    -    stages: list[StageStatus] = []
    +    stages: list[StageStatus] = Field(default_factory=list)
     
     
    +class Shot(BaseModel):
    +    shot_id: str
    +    start: float
    +    end: float
    +    keyframe: str | None = None
    +    dup_of: str | None = None
    +    embedding_ref: str | None = None
    +
    +
     class Word(BaseModel):
    @@ -167,3 +179,3 @@
         scenes: list[Scene]
    -    shots: list[dict[str, Any]]
    +    shots: list[Shot]
         utterances: list[Utterance]
    @@ -187,2 +199 @@
         selected: bool
    -
    Add: C:\Users\asus\Desktop\hoichoi\backend\app\settings.py
    from __future__ import annotations
    
    from pathlib import Path
    
    from pydantic import BaseModel, Field
    from pydantic_settings import BaseSettings, SettingsConfigDict
    
    
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    
    
    class Thresholds(BaseModel):
        shot_scene_threshold: float = Field(0.35, ge=0, le=1)
        keyframe_dedup_hamming: int = Field(7, ge=0, le=64)
        min_scene_seconds: float = Field(20.0, gt=0)
        entity_visible_confidence: float = Field(0.60, ge=0, le=1)
        entity_absent_confidence: float = Field(0.70, ge=0, le=1)
        min_ad_pause_seconds: float = Field(1.2, gt=0)
        ad_blocked_head_seconds: float = Field(120.0, ge=0)
        ad_blocked_tail_seconds: float = Field(120.0, ge=0)
        subtitle_max_line_graphemes: int = Field(42, gt=0)
        subtitle_max_lines: int = Field(2, gt=0)
        subtitle_max_cps: float = Field(17.0, gt=0)
        subtitle_min_duration: float = Field(1.0, gt=0)
        subtitle_max_duration: float = Field(7.0, gt=0)
        subtitle_min_gap: float = Field(0.08, ge=0)
    
    
    class Settings(BaseSettings):
        model_config = SettingsConfigDict(
            env_file=PROJECT_ROOT / "backend" / ".env",
            env_file_encoding="utf-8",
            extra="ignore",
        )
    
        data_dir: Path = PROJECT_ROOT / "data"
        database_url: str | None = None
        openai_api_key: str | None = None
        sarvam_api_key: str | None = None
        sarvam_base_url: str = "https://api.sarvam.ai"
        hf_token: str | None = None
        llm_model_default: str = "gpt-4.1-mini"
        llm_model_scenes: str = "gpt-4.1-mini"
        max_llm_usd_per_episode: float = 5.0
        device: str = "cpu"
        ffmpeg_binary: str = "ffmpeg"
        ffprobe_binary: str = "ffprobe"
        max_upload_bytes: int = 8 * 1024 * 1024 * 1024
        worker_concurrency: int = 1
        cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
        seed_demo: bool = True
        thresholds: Thresholds = Thresholds()
    
        @property
        def episodes_dir(self) -> Path:
            return self.data_dir / "episodes"
    
        @property
        def sqlite_url(self) -> str:
            return self.database_url or f"sqlite:///{(self.data_dir / 'drishti.db').as_posix()}"
    
        @property
        def allowed_origins(self) -> list[str]:
            return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
    
    Update { move_path: None }: C:\Users\asus\Desktop\hoichoi\backend\pyproject.toml
    @@ -9,3 +9,9 @@
       "pydantic>=2.10,<3",
    +  "pydantic-settings>=2.7,<3",
       "python-multipart>=0.0.20,<1",
    +  "sqlmodel>=0.0.24,<1",
    +  "httpx>=0.28,<1",
    +  "PyYAML>=6.0,<7",
    +  "regex>=2024.11.6",
    +  "srt>=3.5,<4",
     ]
    @@ -13,3 +19,3 @@
     [project.optional-dependencies]
    -dev = ["httpx>=0.28,<1", "pytest>=8.3,<9"]
    +dev = ["pytest>=8.3,<9"]
     

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "New-Item -ItemType Directory -Force backend\\pipeline, backend\\pipeline\\stages, backend\\config | Out-Null"
    status: Completed · exit 0

## Assistant

The next correction is the stage engine itself. I’m implementing the documented dependency chain and cache keys so reruns can start at one stage without recomputing valid predecessors. For Sarvam, the technical document explicitly warns that endpoints change, so I’m checking current official API documentation before wiring that adapter.

## Activity

    web search: site:docs.sarvam.ai speech to text API batch diarization timestamps Bengali official

## Activity

    file changes: Completed · 7 changes
    Add: C:\Users\asus\Desktop\hoichoi\backend\pipeline\__init__.py
    """Cached, stage-based episode processing pipeline."""
    
    Add: C:\Users\asus\Desktop\hoichoi\backend\pipeline\errors.py
    class PipelineError(RuntimeError):
        """Base error whose message is safe to expose as a stage failure."""
    
    
    class ConfigurationError(PipelineError):
        """A required provider, executable, or credential is unavailable."""
    
    
    class ArtifactError(PipelineError):
        """An input or output artifact is missing or invalid."""
    
    Add: C:\Users\asus\Desktop\hoichoi\backend\pipeline\media.py
    from __future__ import annotations
    
    import json
    import re
    import subprocess
    from pathlib import Path
    
    from .errors import PipelineError
    
    
    def run(command: list[str], *, timeout: int = 7200) -> subprocess.CompletedProcess[str]:
        try:
            result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
        except FileNotFoundError as exc:
            raise PipelineError(f"Required executable is unavailable: {command[0]}") from exc
        except subprocess.TimeoutExpired as exc:
            raise PipelineError(f"Media command timed out after {timeout} seconds") from exc
        if result.returncode:
            message = result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "unknown media error"
            raise PipelineError(f"{Path(command[0]).name} failed: {message}")
        return result
    
    
    def probe(ffprobe: str, source: Path) -> dict:
        result = run([
            ffprobe, "-v", "error", "-show_entries",
            "format=duration,format_name:stream=index,codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate",
            "-of", "json", str(source),
        ], timeout=60)
        payload = json.loads(result.stdout)
        video = next((stream for stream in payload.get("streams", []) if stream.get("codec_type") == "video"), None)
        if video is None:
            raise PipelineError("The uploaded file has no video stream.")
        audio = next((stream for stream in payload.get("streams", []) if stream.get("codec_type") == "audio"), None)
        rate = video.get("avg_frame_rate") or video.get("r_frame_rate") or "0/1"
        numerator, denominator = (float(value) for value in rate.split("/"))
        return {
            "duration": float(payload.get("format", {}).get("duration") or 0),
            "fps": numerator / denominator if denominator else 0,
            "width": int(video.get("width") or 0),
            "height": int(video.get("height") or 0),
            "video_codec": video.get("codec_name"),
            "audio_codec": audio.get("codec_name") if audio else None,
            "format": payload.get("format", {}).get("format_name", ""),
            "has_audio": audio is not None,
        }
    
    
    def detect_silences(ffmpeg: str, audio: Path, noise_db: int = -35, min_seconds: float = 0.3) -> list[dict[str, float]]:
        command = [ffmpeg, "-hide_banner", "-i", str(audio), "-af", f"silencedetect=noise={noise_db}dB:d={min_seconds}", "-f", "null", "-"]
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=7200)
        if result.returncode:
            raise PipelineError("ffmpeg could not analyze audio silence.")
        starts = [float(value) for value in re.findall(r"silence_start:\s*([0-9.]+)", result.stderr)]
        ends = [(float(end), float(duration)) for end, duration in re.findall(r"silence_end:\s*([0-9.]+)\s*\|\s*silence_duration:\s*([0-9.]+)", result.stderr)]
        return [{"start": start, "end": end, "duration": duration} for start, (end, duration) in zip(starts, ends)]
    
    Add: C:\Users\asus\Desktop\hoichoi\backend\pipeline\sarvam.py
    from __future__ import annotations
    
    import json
    from pathlib import Path
    from typing import Any
    
    from .errors import ConfigurationError, PipelineError
    
    
    class SarvamClient:
        """Current Saaras batch adapter with normalization into Drishti utterances.
    
        Batch mode is intentional: current Sarvam REST transcription is limited to
        short audio and does not provide speaker diarization.
        """
    
        def __init__(self, api_key: str | None):
            self.api_key = api_key
    
        def transcribe(self, audio_path: Path, output_dir: Path) -> tuple[list[dict], dict[str, Any]]:
            if not self.api_key:
                raise ConfigurationError(
                    "SARVAM_API_KEY is missing. Add it to backend/.env, then rerun from s06."
                )
            try:
                from sarvamai import SarvamAI  # type: ignore[import-not-found]
            except ImportError as exc:
                raise ConfigurationError(
                    "Sarvam provider package is missing. Install with: pip install -e '.[providers]'"
                ) from exc
    
            output_dir.mkdir(parents=True, exist_ok=True)
            client = SarvamAI(api_subscription_key=self.api_key)
            try:
                job = client.speech_to_text_job.create_job(
                    model="saaras:v4",
                    language_code="bn-IN",
                    mode="codemix",
                    with_diarization=True,
                    with_timestamps=True,
                )
                job.upload_files(file_paths=[str(audio_path)])
                job.start()
                job.wait_until_complete()
                job.download_outputs(output_dir=str(output_dir))
            except Exception as exc:  # provider SDK error types are not stable
                raise PipelineError(f"Sarvam batch transcription failed: {exc}") from exc
    
            candidates = sorted(output_dir.rglob("*.json"), key=lambda path: path.stat().st_mtime, reverse=True)
            if not candidates:
                raise PipelineError("Sarvam completed but returned no JSON transcript.")
            raw = json.loads(candidates[0].read_text(encoding="utf-8"))
            return self.normalize(raw), raw
    
        @staticmethod
        def normalize(raw: dict[str, Any]) -> list[dict]:
            diarized = raw.get("diarized_transcript") or {}
            entries = diarized.get("entries") or diarized.get("segments") or diarized.get("utterances") or []
            utterances: list[dict] = []
            if entries:
                for index, entry in enumerate(entries):
                    text = entry.get("transcript") or entry.get("text") or entry.get("content") or ""
                    start = entry.get("start_time_seconds", entry.get("start", 0))
                    end = entry.get("end_time_seconds", entry.get("end", start))
                    speaker = entry.get("speaker_id") or entry.get("speaker") or entry.get("speaker_label") or "SPEAKER_00"
                    utterances.append({
                        "utt_id": f"utt_{index + 1:05d}",
                        "start": float(start),
                        "end": float(end),
                        "speaker": SarvamClient._speaker_label(str(speaker)),
                        "speaker_name": None,
                        "text_raw": text.strip(),
                        "text": text.strip(),
                        "words": None,
                        "confidence": entry.get("confidence"),
                        "overlap": bool(entry.get("overlap", False)),
                    })
                return utterances
    
            timestamps = raw.get("timestamps") or {}
            chunks = timestamps.get("chunks") or timestamps.get("words") or []
            starts = timestamps.get("start_time_seconds") or []
            ends = timestamps.get("end_time_seconds") or []
            for index, (text, start, end) in enumerate(zip(chunks, starts, ends)):
                utterances.append({
                    "utt_id": f"utt_{index + 1:05d}", "start": float(start), "end": float(end),
                    "speaker": "SPK_A", "speaker_name": None, "text_raw": str(text).strip(),
                    "text": str(text).strip(), "words": None, "confidence": raw.get("language_probability"), "overlap": False,
                })
            if not utterances and raw.get("transcript"):
                utterances.append({
                    "utt_id": "utt_00001", "start": 0.0, "end": 0.0, "speaker": "SPK_A",
                    "speaker_name": None, "text_raw": raw["transcript"], "text": raw["transcript"],
                    "words": None, "confidence": raw.get("language_probability"), "overlap": False,
                })
            return utterances
    
        @staticmethod
        def _speaker_label(value: str) -> str:
            digits = "".join(character for character in value if character.isdigit())
            index = int(digits or 0)
            return f"SPK_{chr(65 + min(index, 25))}"
    
    Add: C:\Users\asus\Desktop\hoichoi\backend\pipeline\scoring.py
    from __future__ import annotations
    
    
    def score_candidate(*, pause_len: float, scene_boundary: bool, distance_to_end: float, intensity: float, context_match: float, speech: bool, cliffhanger: bool) -> dict[str, float]:
        pause = min(max(pause_len / 2.5, 0), 1)
        scene_end = 1.0 if scene_boundary else max(0, 1 - distance_to_end / 30)
        low_intensity = 1 - min(max(intensity, 0), 1)
        speech_penalty = 1.0 if speech else 0.0
        cliffhanger_penalty = 1.0 if cliffhanger and not scene_boundary else 0.0
        total = .25 * pause + .25 * scene_end + .30 * low_intensity + .20 * context_match - .50 * speech_penalty - .40 * cliffhanger_penalty
        return {
            "pause": round(pause, 4), "scene_end": round(scene_end, 4), "low_intensity": round(low_intensity, 4),
            "context_match": round(context_match, 4), "speech_penalty": speech_penalty,
            "cliffhanger_penalty": cliffhanger_penalty, "total": round(min(max(total, 0), 1), 4),
        }
    
    
    def select_candidates(candidates: list[dict], min_gap: float, count: int) -> list[dict]:
        ranked = sorted(candidates, key=lambda candidate: candidate["score"]["total"], reverse=True)
        selected: list[float] = []
        for candidate in ranked:
            candidate["selected"] = len(selected) < count and all(abs(candidate["time"] - time) >= min_gap for time in selected)
            if candidate["selected"]:
                selected.append(candidate["time"])
        return ranked
    
    Add: C:\Users\asus\Desktop\hoichoi\backend\pipeline\subtitles.py
    from __future__ import annotations
    
    import math
    import re as std_re
    from dataclasses import dataclass
    
    import regex
    import srt
    
    from app.settings import Thresholds
    
    
    def graphemes(text: str) -> list[str]:
        return regex.findall(r"\X", text)
    
    
    def grapheme_len(text: str) -> int:
        return len(graphemes(text))
    
    
    def split_text(text: str, max_chars: int) -> list[str]:
        if grapheme_len(text) <= max_chars:
            return [text.strip()]
        phrases = [part.strip() for part in regex.split(r"(?<=[।?!])\s+|(?<=[,;])\s+|\s+(?=এবং|কিন্তু|তাই|আর)" , text) if part.strip()]
        if len(phrases) == 1:
            words = text.split()
            midpoint = max(1, len(words) // 2)
            phrases = [" ".join(words[:midpoint]), " ".join(words[midpoint:])]
        output: list[str] = []
        current = ""
        for phrase in phrases:
            candidate = f"{current} {phrase}".strip()
            if current and grapheme_len(candidate) > max_chars:
                output.append(current)
                current = phrase
            else:
                current = candidate
        if current:
            output.append(current)
        return output
    
    
    def balance_lines(text: str, max_line: int) -> list[str]:
        words = text.split()
        if grapheme_len(text) <= max_line or len(words) < 2:
            return [text]
        best: tuple[int, list[str]] | None = None
        for index in range(1, len(words)):
            first, second = " ".join(words[:index]), " ".join(words[index:])
            if grapheme_len(first) <= max_line and grapheme_len(second) <= max_line:
                score = abs(grapheme_len(first) - grapheme_len(second)) + (5 if grapheme_len(first) > grapheme_len(second) else 0)
                if best is None or score < best[0]:
                    best = (score, [first, second])
        return best[1] if best else [text]
    
    
    def format_utterances(utterances: list[dict], thresholds: Thresholds) -> list[dict]:
        cues: list[dict] = []
        for utterance in utterances:
            text = std_re.sub(r"\s+", " ", utterance.get("text", "")).strip()
            if not text:
                continue
            max_cue_chars = thresholds.subtitle_max_line_graphemes * thresholds.subtitle_max_lines
            parts = split_text(text, max_cue_chars)
            total_chars = max(1, sum(grapheme_len(part) for part in parts))
            cursor = float(utterance["start"])
            available = max(thresholds.subtitle_min_duration, float(utterance["end"]) - cursor)
            for part_index, part in enumerate(parts):
                ratio = grapheme_len(part) / total_chars
                duration = max(thresholds.subtitle_min_duration, available * ratio)
                duration = min(duration, thresholds.subtitle_max_duration)
                needed = grapheme_len(part) / thresholds.subtitle_max_cps
                duration = max(duration, needed)
                end = min(float(utterance["end"]), cursor + duration) if part_index < len(parts) - 1 else max(float(utterance["end"]), cursor + min(needed, .5))
                if cues:
                    cursor = max(cursor, cues[-1]["end"] + thresholds.subtitle_min_gap)
                    end = max(end, cursor + thresholds.subtitle_min_duration)
                lines = balance_lines(part, thresholds.subtitle_max_line_graphemes)
                actual_duration = max(.01, end - cursor)
                cues.append({
                    "idx": len(cues) + 1,
                    "start": round(cursor, 3), "end": round(end, 3), "lines": lines,
                    "speakers": [utterance["speaker"]], "kind": "dialogue",
                    "cps": round(grapheme_len(part) / actual_duration, 2),
                })
                cursor = end + thresholds.subtitle_min_gap
        return cues
    
    
    def write_srt(cues: list[dict]) -> str:
        subtitles = [srt.Subtitle(index=cue["idx"], start=srt.timedelta(seconds=cue["start"]), end=srt.timedelta(seconds=cue["end"]), content="\n".join(cue["lines"])) for cue in cues]
        return srt.compose(subtitles)
    
    
    def _vtt_time(seconds: float) -> str:
        milliseconds = round(seconds * 1000)
        hours, remainder = divmod(milliseconds, 3_600_000)
        minutes, remainder = divmod(remainder, 60_000)
        secs, millis = divmod(remainder, 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"
    
    
    def write_vtt(cues: list[dict]) -> str:
        blocks = ["WEBVTT", ""]
        for cue in cues:
            blocks.extend([str(cue["idx"]), f"{_vtt_time(cue['start'])} --> {_vtt_time(cue['end'])}", "\n".join(cue["lines"]), ""])
        return "\n".join(blocks)
    
    Update { move_path: None }: C:\Users\asus\Desktop\hoichoi\backend\pyproject.toml
    @@ -20,2 +20,4 @@
     dev = ["pytest>=8.3,<9"]
    +media = ["Pillow>=11,<13"]
    +providers = ["openai>=1.75,<3", "sarvamai>=0.1,<2"]
     

## Activity

    file changes: Completed · 1 changes
    Update { move_path: None }: C:\Users\asus\Desktop\hoichoi\backend\pipeline\subtitles.py
    @@ -2,5 +2,4 @@
     
    -import math
     import re as std_re
    -from dataclasses import dataclass
    +from datetime import timedelta
     
    @@ -90,3 +89,3 @@
     def write_srt(cues: list[dict]) -> str:
    -    subtitles = [srt.Subtitle(index=cue["idx"], start=srt.timedelta(seconds=cue["start"]), end=srt.timedelta(seconds=cue["end"]), content="\n".join(cue["lines"])) for cue in cues]
    +    subtitles = [srt.Subtitle(index=cue["idx"], start=timedelta(seconds=cue["start"]), end=timedelta(seconds=cue["end"]), content="\n".join(cue["lines"])) for cue in cues]
         return srt.compose(subtitles)
    @@ -107,2 +106 @@
         return "\n".join(blocks)
    -

## Assistant

The backend also needs an OpenAI structured-output boundary for vision, transcript cleanup, entity extraction, and scene semantics. I’m using the openai-docs skill for that provider-specific portion so the wrapper matches the current Responses API rather than relying on the older technical-document example.

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -Raw 'C:\\Users\\asus\\.codex\\skills\\.system\\openai-docs\\SKILL.md'"
    status: Completed · exit 0
      ---
      name: "openai-docs"
      description: "Use for Codex models/pricing, scheduled tasks, skills, settings, setup, troubleshooting, customization, automations, and self-knowledgeâ€”including 'you,' 'your,' 'this app,' or 'this coding agent' when they refer to Codexâ€”and for OpenAI APIs/products and ChatGPT Work. Also use for model choice/migration, prompting, SDKs, Responses, Realtime, agents, evals, and Chat/Work/Codex comparisons. Do not use for generic app/software tasks that merely mention Codex."
      metadata:
        short-description: "Codex models/pricing, scheduled tasks, skills, settings, setup, troubleshooting, and self-knowledge; OpenAI APIs and ChatGPT Work. 'You'/'this app' means Codex only."
      ---
      
      # OpenAI Docs
      
      Provide current, cited OpenAI product, API, model, and Codex guidance. Read zero or one primary reference.
      
      **First substantive action:** Search the user's exact requested official OpenAI documentation topic and any explicitly named model using a concise, topic-specific query of 2-6 essential terms. When an already-available direct official documentation search and page-retrieval capability is present, use it first: search, then fetch or open the matching official page before general web search. Otherwise, immediately use official-domain web search, then actually open or fetch the relevant official page. Complete this source order before reading a reference, inspecting local or repository files, running a Codex manual or model resolver, drafting a plan, or answering from memory. Use the actual fetched page, not a search snippet or an unopened link. If one official search or page does not establish the answer, search another appropriate official domain and actually open or fetch the result. Preserve the exact requested model; never substitute a newer model.
      
      **Only exception:** An explicitly requested, genuinely broad, cross-topic Codex setup, orientation, or system-map synthesis may use the manual first when shell execution and an allowed temporary cache are available. A specific Codex feature, setting, command, error, model, or requested citation remains docs-first. Mixed Chat/Work/Codex comparisons are official documentation questions, not manual-first Codex requests.
      
      For generic software tasks, answer the software task directly. OpenAI implementation, debugging, SDK, API, prompting, agent, and eval requests are not generic.
      
      For a straightforward factual or citation-only request, follow the source order and do not read a route reference. This includes straightforward API facts, ChatGPT Work or mixed Chat/Work/Codex comparisons, model tiers, aliases, Pro mode, reasoning settings, factual migration baselines, and narrow Codex facts. Prioritize `learn.chatgpt.com` for ChatGPT Work.
      
      ## Choose one primary route
      
      Use the first matching route, and read its reference only when the requested task needs that specialized workflow:
      
      - **Explicitly requested local documentation integration:** Read [integration guidance](references/mcp-diagnostics.md) only when the user explicitly requests that local integration.
      - **Model migration, upgrades, or model-specific prompting:** Read [model-migration.md](references/model-migration.md) for actual migration planning, implementation, dynamic target resolution, or prompt changes. Preserve an explicitly requested target.
      - **Model selection and comparisons:** Read [model-selection.md](references/model-selection.md) only when nuanced current, latest, default, cost, latency, quality, or modality tradeoffs need more guidance. Do not run a migration resolver for selection alone.
      - **Product, API, ChatGPT Work, and mixed Chat/Work/Codex documentation:** Read [official-docs.md](references/official-docs.md) only when fetched official pages leave source selection, API schemas, or the requested implementation unresolved. This route is not manual-first.
      - **Explicitly broad Codex setup, orientation, or cross-topic synthesis:** Read [codex-self-knowledge.md](references/codex-self-knowledge.md) when the eligible Codex manual or deeper Codex procedures are needed.
      
      Read at most one primary reference. Do not open every route, bundled model guide, or helper script. Read a supporting reference or run a helper only when the chosen workflow demonstrably needs it.
      
      ## Source and execution boundaries
      
      - Search, open, fetch, and cite only `developers.openai.com`, `platform.openai.com`, and `learn.chatgpt.com`. Cite the page that supports the claim. State uncertainty when official sources do not establish pricing, availability, account access, limits, or behavior.
      - Preserve an explicitly requested model for selection, migration, and prompting. Resolve an unspecified latest or current migration target only after searching and fetching current official guidance.
      - Use `references/latest-model.md` only as a disclosed fallback after current official model guidance does not answer the question. Read `references/upgrading-to-gpt-6-astra.md` only for an actual, requested GPT-6 migration; read `references/prompting-guide.md` only for requested prompting work.
      - Before building, running, editing, debugging, or testing an API-backed app or tool, use `openai-platform-api-key` first when available. Documentation, conceptual examples, model selection, and read-only guidance do not require an API key.
      - Say "OpenAI Docs" or "official OpenAI documentation" in user-facing answers. Keep exact official citations and examples concise.
      

## Activity

    web search: site:developers.openai.com Responses API Python structured outputs parse gpt-4.1-mini official

## Activity

    file changes: Completed · 3 changes
    Add: C:\Users\asus\Desktop\hoichoi\backend\pipeline\llm.py
    from __future__ import annotations
    
    import hashlib
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
        ) -> SchemaT:
            if not self.settings.openai_api_key:
                raise ConfigurationError("OPENAI_API_KEY is missing.")
            try:
                from openai import OpenAI  # type: ignore[import-not-found]
            except ImportError as exc:
                raise ConfigurationError("OpenAI provider package is missing. Install with: pip install -e '.[providers]'") from exc
    
            serialized = json.dumps({"model": model, "system": system, "user": user, "schema": schema.model_json_schema()}, ensure_ascii=False, sort_keys=True)
            key = hashlib.sha256(serialized.encode()).hexdigest()
            cache_path = self.store.episode_dir(self.episode_id) / "cache" / "llm" / f"{key}.json"
            if cache_path.exists():
                return schema.model_validate(self.store.read_json(cache_path))
    
            client = OpenAI(api_key=self.settings.openai_api_key)
            error: Exception | None = None
            started = time.perf_counter()
            for attempt in range(max_retries + 1):
                try:
                    response = client.responses.parse(
                        model=model,
                        input=[{"role": "system", "content": system}, {"role": "user", "content": user}],
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
    
    Add: C:\Users\asus\Desktop\hoichoi\backend\pipeline\stages\__init__.py
    """Pipeline stage implementations."""
    
    Add: C:\Users\asus\Desktop\hoichoi\backend\pipeline\stages\core.py
    from __future__ import annotations
    
    import math
    import re
    import shutil
    import struct
    import subprocess
    import time
    import wave
    from dataclasses import dataclass
    from pathlib import Path
    from statistics import mean
    
    from app.artifacts import ArtifactStore
    from app.db import Database
    from app.models import SemanticTimeline
    from app.settings import Settings
    from pipeline.errors import ArtifactError, PipelineError
    from pipeline.media import detect_silences, probe, run
    from pipeline.sarvam import SarvamClient
    from pipeline.scoring import score_candidate, select_candidates
    from pipeline.subtitles import format_utterances, grapheme_len, write_srt, write_vtt
    
    
    @dataclass
    class StageContext:
        episode_id: str
        settings: Settings
        store: ArtifactStore
        db: Database
    
        @property
        def root(self) -> Path:
            return self.store.episode_dir(self.episode_id)
    
        def stage(self, stage_id: str) -> dict:
            path = self.store.stage_path(self.episode_id, stage_id)
            if not path.exists():
                raise ArtifactError(f"Required stage artifact is missing: {path.name}")
            return self.store.read_json(path)
    
    
    def s01_ingest(ctx: StageContext) -> dict:
        record = ctx.db.get_episode_record(ctx.episode_id)
        if record is None:
            raise ArtifactError("Episode database record is missing.")
        source = Path(record.source_path)
        if not source.exists():
            raise ArtifactError("The registered source video no longer exists.")
        metadata = probe(ctx.settings.ffprobe_binary, source)
        if metadata["duration"] <= 0:
            raise PipelineError("ffprobe returned an invalid video duration.")
        proxy = ctx.root / "proxy.mp4"
        browser_ready = source.suffix.lower() == ".mp4" and metadata["video_codec"] == "h264" and (metadata["audio_codec"] in {"aac", None})
        if browser_ready and metadata["height"] <= 720:
            proxy_path = source
        else:
            run([
                ctx.settings.ffmpeg_binary, "-y", "-i", str(source), "-map", "0:v:0", "-map", "0:a:0?",
                "-vf", "scale=-2:min(720\\,ih)", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
                "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(proxy),
            ])
            proxy_path = proxy
        ctx.db.update_episode(
            ctx.episode_id, duration=metadata["duration"], fps=metadata["fps"], width=metadata["width"],
            height=metadata["height"], video_available=True,
        )
        return {**metadata, "source": str(source.relative_to(ctx.root)), "proxy": str(proxy_path.relative_to(ctx.root))}
    
    
    def s02_shots(ctx: StageContext) -> dict:
        ingest = ctx.stage("s01_ingest")
        source = ctx.root / ingest["source"]
        threshold = ctx.settings.thresholds.shot_scene_threshold
        command = [
            ctx.settings.ffmpeg_binary, "-hide_banner", "-i", str(source), "-vf",
            f"select='gt(scene,{threshold})',showinfo", "-an", "-f", "null", "-",
        ]
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=7200)
        if result.returncode:
            raise PipelineError("ffmpeg shot detection failed.")
        boundaries = [float(value) for value in re.findall(r"pts_time:([0-9.]+)", result.stderr)]
        points = [0.0] + [value for value in boundaries if .25 < value < ingest["duration"] - .25] + [ingest["duration"]]
        points = sorted(set(round(value, 3) for value in points))
        shots = [{"shot_id": f"shot_{index + 1:05d}", "start": start, "end": end, "keyframe": None, "dup_of": None, "embedding_ref": None} for index, (start, end) in enumerate(zip(points, points[1:])) if end - start >= .08]
        if not shots:
            shots = [{"shot_id": "shot_00001", "start": 0, "end": ingest["duration"], "keyframe": None, "dup_of": None, "embedding_ref": None}]
        return {"shots": shots, "detector": "ffmpeg_scene", "threshold": threshold}
    
    
    def _difference_hash(path: Path) -> int | None:
        try:
            from PIL import Image  # type: ignore[import-not-found]
        except ImportError:
            return None
        with Image.open(path) as image:
            pixels = list(image.convert("L").resize((9, 8)).getdata())
        value = 0
        for row in range(8):
            for column in range(8):
                value = (value << 1) | int(pixels[row * 9 + column] > pixels[row * 9 + column + 1])
        return value
    
    
    def s03_keyframes(ctx: StageContext) -> dict:
        ingest, shot_data = ctx.stage("s01_ingest"), ctx.stage("s02_shots")
        source = ctx.root / ingest["source"]
        frames = ctx.root / "frames"
        previous: list[tuple[str, int]] = []
        shots = []
        for shot in shot_data["shots"]:
            midpoint = (shot["start"] + shot["end"]) / 2
            relative = f"frames/kf_{shot['shot_id']}.jpg"
            destination = ctx.root / relative
            run([ctx.settings.ffmpeg_binary, "-y", "-ss", str(midpoint), "-i", str(source), "-frames:v", "1", "-q:v", "3", str(destination)], timeout=120)
            hash_value = _difference_hash(destination)
            duplicate = None
            if hash_value is not None:
                for previous_id, previous_hash in reversed(previous[-8:]):
                    if (hash_value ^ previous_hash).bit_count() <= ctx.settings.thresholds.keyframe_dedup_hamming:
                        duplicate = previous_id
                        break
                previous.append((shot["shot_id"], hash_value))
            shots.append({**shot, "keyframe": None if duplicate else relative, "dup_of": duplicate})
        return {"shots": shots, "dedup_method": "dhash" if previous else "disabled", "unique_frames": sum(shot["dup_of"] is None for shot in shots)}
    
    
    def s04_audio_prep(ctx: StageContext) -> dict:
        ingest = ctx.stage("s01_ingest")
        if not ingest["has_audio"]:
            raise PipelineError("The video has no audio stream to transcribe.")
        source = ctx.root / ingest["source"]
        full = ctx.root / "audio" / "full_16k.wav"
        vocals = ctx.root / "audio" / "vocals_16k.wav"
        run([ctx.settings.ffmpeg_binary, "-y", "-i", str(source), "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(full)])
        separated = False
        if shutil.which("demucs"):
            demucs_root = ctx.root / "audio" / "demucs"
            try:
                run(["demucs", "--two-stems=vocals", "-n", "htdemucs", "-o", str(demucs_root), str(full)])
                result = next(demucs_root.rglob("vocals.wav"))
                run([ctx.settings.ffmpeg_binary, "-y", "-i", str(result), "-ac", "1", "-ar", "16000", str(vocals)])
                separated = True
            except (PipelineError, StopIteration):
                shutil.copy2(full, vocals)
        else:
            shutil.copy2(full, vocals)
        return {"full_audio": "audio/full_16k.wav", "vocals_audio": "audio/vocals_16k.wav", "vocal_separation": separated, "sample_rate": 16000}
    
    
    def s05_vad(ctx: StageContext) -> dict:
        ingest, audio = ctx.stage("s01_ingest"), ctx.stage("s04_audio_prep")
        source = ctx.root / audio["vocals_audio"]
        silences = detect_silences(ctx.settings.ffmpeg_binary, source)
        speech = []
        cursor = 0.0
        for silence in silences:
            if silence["start"] > cursor + .15:
                speech.append({"start": round(cursor, 3), "end": round(silence["start"], 3)})
            cursor = silence["end"]
        if cursor < ingest["duration"]:
            speech.append({"start": round(cursor, 3), "end": round(ingest["duration"], 3)})
        return {"speech_segments": speech, "silences": silences, "method": "ffmpeg_silencedetect", "noise_db": -35}
    
    
    def s06_stt(ctx: StageContext) -> dict:
        audio = ctx.stage("s04_audio_prep")
        client = SarvamClient(ctx.settings.sarvam_api_key)
        utterances, raw = client.transcribe(ctx.root / audio["vocals_audio"], ctx.root / "stages" / "sarvam_output")
        if not utterances:
            raise PipelineError("Sarvam returned an empty transcript.")
        ctx.store.write_json(ctx.root / "stages" / "s06_raw.json", raw)
        return {"utterances": utterances, "provider": "sarvam", "model": "saaras:v4", "language": "bn-IN", "diarization": True}
    
    
    def s07_transcript_clean(ctx: StageContext) -> dict:
        utterances = ctx.stage("s06_stt")["utterances"]
        terminal = ("।", ".", "?", "!")
        cleaned = []
        for utterance in utterances:
            text = re.sub(r"\s+", " ", utterance["text_raw"]).strip()
            if text and not text.endswith(terminal):
                text += "।"
            cleaned.append({**utterance, "text": text})
        return {"utterances": cleaned, "cleanup": "deterministic_conservative", "meaning_preserved": True}
    
    
    def s08_audio_events(ctx: StageContext) -> dict:
        audio = ctx.stage("s04_audio_prep")
        path = ctx.root / audio["full_audio"]
        curve: list[list[float]] = []
        with wave.open(str(path), "rb") as handle:
            rate = handle.getframerate()
            channels = handle.getnchannels()
            width = handle.getsampwidth()
            if width != 2:
                raise PipelineError("Expected 16-bit PCM analysis audio.")
            index = 0
            while frames := handle.readframes(rate):
                samples = struct.unpack(f"<{len(frames) // 2}h", frames)
                rms = math.sqrt(sum(value * value for value in samples) / max(1, len(samples))) / 32768
                curve.append([float(index), round(rms, 5)])
                index += 1
        values = [point[1] for point in curve]
        low, high = (min(values, default=0), max(values, default=1))
        normalized = [[time_value, round((value - low) / max(.00001, high - low), 4)] for time_value, value in curve]
        return {"events": [], "loudness": normalized, "music": [], "event_detector": "not_configured", "loudness_method": "pcm_rms"}
    
    
    def s09_vision_baseline(ctx: StageContext) -> dict:
        shots = ctx.stage("s03_keyframes")["shots"]
        tags = {}
        for shot in shots:
            tags[shot["shot_id"]] = {
                "location": "unknown", "indoor": None, "objects": [], "visible_brands": [],
                "activity": "unknown", "visual_mood": "neutral", "people_count": 0, "confidence": 0.0,
            }
        return {"visual_tags": tags, "provider": "conservative_fallback", "note": "Install provider extras and configure OPENAI_API_KEY for vision labels."}
    
    
    def s10_scenes(ctx: StageContext) -> dict:
        ingest, shots, transcript, vision = ctx.stage("s01_ingest"), ctx.stage("s03_keyframes")["shots"], ctx.stage("s07_transcript_clean")["utterances"], ctx.stage("s09_vision_baseline")["visual_tags"]
        max_scene = 180.0
        boundaries = [0.0]
        last = 0.0
        for shot in shots[1:]:
            if shot["start"] - last >= max_scene:
                boundaries.append(shot["start"])
                last = shot["start"]
        boundaries.append(ingest["duration"])
        scenes = []
        for index, (start, end) in enumerate(zip(boundaries, boundaries[1:])):
            included_shots = [shot for shot in shots if shot["start"] < end and shot["end"] > start]
            utterances = [item for item in transcript if item["start"] < end and item["end"] > start]
            scene_tags = [vision[shot["shot_id"]] for shot in included_shots]
            base_visual = scene_tags[0] if scene_tags else {"location": "unknown", "indoor": None, "objects": [], "visible_brands": [], "activity": "unknown", "visual_mood": "neutral", "people_count": 0, "confidence": 0.0}
            scenes.append({
                "scene_id": f"scene_{index + 1:04d}", "start": start, "end": end,
                "shot_ids": [shot["shot_id"] for shot in included_shots], "visual": base_visual,
                "speakers": sorted({item["speaker"] for item in utterances}), "utt_ids": [item["utt_id"] for item in utterances],
                "audio_events": [], "music_ratio": 0.0, "entity_ids": [],
            })
        return {"scenes": scenes, "method": "shot_window_baseline", "llm_validated": False}
    
    
    ENTITY_TERMS = {
        "mobile": [("smartphone", "ফোন", r"ফোন|মোবাইল|smartphone|mobile")],
        "food_delivery": [("biryani", "বিরিয়ানি", r"বিরিয়ানি|খাবার|অর্ডার|food|order")],
        "travel": [("train", "ট্রেন", r"ট্রেন|রেল|train|flight|বিমান|হোটেল")],
        "finance": [("money", "টাকা", r"টাকা|ব্যাঙ্ক|লোন|salary|money|bank|loan")],
        "fashion": [("clothing", "পোশাক", r"শাড়ি|জামা|পোশাক|dress|shoes")],
    }
    
    
    def s11_entities_dialogue(ctx: StageContext) -> dict:
        utterances, scenes = ctx.stage("s07_transcript_clean")["utterances"], ctx.stage("s10_scenes")["scenes"]
        entities = []
        for category, terms in ENTITY_TERMS.items():
            for name, name_bn, pattern in terms:
                mentions = []
                for utterance in utterances:
                    match = re.search(pattern, utterance["text"], re.IGNORECASE)
                    if match:
                        mentions.append({"source": "dialogue", "time": utterance["start"], "utt_id": utterance["utt_id"], "shot_id": None, "surface": match.group(0)})
                if mentions:
                    entities.append({
                        "entity_id": f"entity_{len(entities) + 1:04d}", "name": name, "name_bn": name_bn,
                        "kind": "product", "brand": None, "ad_categories": [category], "mentions": mentions,
                        "sentiment": "neutral", "presence": "unverified", "visual_check": None, "confidence": .72,
                    })
        for scene in scenes:
            scene["entity_ids"] = [entity["entity_id"] for entity in entities if any(scene["start"] <= mention["time"] < scene["end"] for mention in entity["mentions"])]
        return {"entities": entities, "scenes": scenes, "extractor": "grounded_keyword_baseline"}
    
    
    def s12_vision_targeted(ctx: StageContext) -> dict:
        stage = ctx.stage("s11_entities_dialogue")
        entities = []
        for entity in stage["entities"]:
            entities.append({**entity, "presence": "unverified", "visual_check": {
                "frames_checked": [], "visible": None, "visible_frames": [], "confidence": 0.0,
                "note": "Targeted vision provider is not configured; no absence claim was made.",
            }})
        return {"entities": entities, "scenes": stage["scenes"], "provider": "conservative_fallback"}
    
    
    def _curve_mean(curve: list[list[float]], start: float, end: float) -> float:
        values = [value for time_value, value in curve if start <= time_value < end]
        return mean(values) if values else 0.0
    
    
    def s13_scene_semantics(ctx: StageContext) -> dict:
        scenes, utterances, audio = ctx.stage("s12_vision_targeted")["scenes"], ctx.stage("s07_transcript_clean")["utterances"], ctx.stage("s08_audio_events")
        output = []
        intensity_curve = []
        for index, scene in enumerate(scenes):
            scene_utterances = [utterance for utterance in utterances if utterance["utt_id"] in scene["utt_ids"]]
            duration = max(.01, scene["end"] - scene["start"])
            dialogue_density = min(1, sum(max(0, item["end"] - item["start"]) for item in scene_utterances) / duration)
            energy = _curve_mean(audio["loudness"], scene["start"], scene["end"])
            llm_intensity = min(1, .18 + dialogue_density * .62)
            intensity = .55 * llm_intensity + .25 * energy + .20 * dialogue_density
            first_text = scene_utterances[0]["text"] if scene_utterances else "No dialogue in this scene."
            semantic = {
                "title": f"Scene {index + 1}", "summary": first_text[:180], "topics": [], "mood": "neutral",
                "narrative_intensity": round(intensity, 4),
                "intensity_components": {"llm": round(llm_intensity, 4), "audio_energy": round(energy, 4), "dialogue_density": round(dialogue_density, 4)},
                "is_cliffhanger": index == len(scenes) - 1,
            }
            output.append({**scene, "semantic": semantic})
            second = math.floor(scene["start"])
            while second <= math.ceil(scene["end"]):
                intensity_curve.append([float(second), round(intensity, 4)])
                second += 1
        return {"scenes": output, "intensity": intensity_curve, "provider": "fused_deterministic_baseline"}
    
    
    def s14_ad_scoring(ctx: StageContext) -> dict:
        scenes, silences, entities = ctx.stage("s13_scene_semantics")["scenes"], ctx.stage("s05_vad")["silences"], ctx.stage("s12_vision_targeted")["entities"]
        duration = ctx.stage("s01_ingest")["duration"]
        thresholds = ctx.settings.thresholds
        candidates = []
        for scene in scenes[:-1]:
            time_value = scene["end"]
            if time_value < thresholds.ad_blocked_head_seconds or time_value > duration - thresholds.ad_blocked_tail_seconds:
                continue
            nearest = min(silences, key=lambda silence: abs((silence["start"] + silence["end"]) / 2 - time_value), default=None)
            pause_len = nearest["duration"] if nearest and abs(nearest["start"] - time_value) <= 2 else 0
            related = [entity for entity in entities if entity["entity_id"] in scene["entity_ids"]]
            context = max((entity["confidence"] * .7 for entity in related), default=0)
            score = score_candidate(pause_len=pause_len, scene_boundary=True, distance_to_end=0, intensity=scene["semantic"]["narrative_intensity"], context_match=context, speech=False, cliffhanger=scene["semantic"]["is_cliffhanger"])
            categories = sorted({category for entity in related for category in entity["ad_categories"]})
            candidates.append({
                "cand_id": f"ad_{len(candidates) + 1:04d}", "time": time_value, "scene_id": scene["scene_id"],
                "kind": "scene_boundary", "pause_len": round(pause_len, 3), "score": score,
                "disruption": "low" if score["low_intensity"] >= .6 else "high" if score["low_intensity"] < .35 else "medium",
                "matched_categories": categories, "context_entity_ids": [entity["entity_id"] for entity in related],
                "reason": f"Scene boundary after '{scene['semantic']['title']}'; {pause_len:.1f} s pause; intensity {scene['semantic']['narrative_intensity']:.2f}.",
                "selected": False,
            })
        for silence in silences:
            midpoint = (silence["start"] + silence["end"]) / 2
            scene = next((item for item in scenes if item["start"] < midpoint < item["end"]), None)
            if not scene or silence["duration"] < thresholds.min_ad_pause_seconds or scene["semantic"]["narrative_intensity"] >= .4:
                continue
            if midpoint < thresholds.ad_blocked_head_seconds or midpoint > duration - thresholds.ad_blocked_tail_seconds:
                continue
            score = score_candidate(pause_len=silence["duration"], scene_boundary=False, distance_to_end=scene["end"] - midpoint, intensity=scene["semantic"]["narrative_intensity"], context_match=0, speech=False, cliffhanger=scene["semantic"]["is_cliffhanger"])
            candidates.append({
                "cand_id": f"ad_{len(candidates) + 1:04d}", "time": midpoint, "scene_id": scene["scene_id"], "kind": "dialogue_pause",
                "pause_len": silence["duration"], "score": score, "disruption": "low" if score["low_intensity"] >= .6 else "medium",
                "matched_categories": [], "context_entity_ids": [], "reason": f"{silence['duration']:.1f} s pause inside a low-intensity scene.", "selected": False,
            })
        count = max(1, math.floor(duration / 600))
        return {"candidates": select_candidates(candidates, 480, count), "settings": {"min_gap": 480, "n_breaks": count, "blocked": [thresholds.ad_blocked_head_seconds, thresholds.ad_blocked_tail_seconds]}}
    
    
    def s15_subtitles(ctx: StageContext) -> dict:
        cues = format_utterances(ctx.stage("s07_transcript_clean")["utterances"], ctx.settings.thresholds)
        outputs = ctx.root / "outputs"
        ctx.store.write_text(outputs / "episode_bn.srt", write_srt(cues))
        ctx.store.write_text(outputs / "episode_bn.vtt", write_vtt(cues))
        return {"cues": cues, "srt": "outputs/episode_bn.srt", "vtt": "outputs/episode_bn.vtt"}
    
    
    def s16_captions(ctx: StageContext) -> dict:
        cues = [dict(cue) for cue in ctx.stage("s15_subtitles")["cues"]]
        events = ctx.stage("s08_audio_events")["events"]
        for event in events:
            if not event.get("in_cc"):
                continue
            cues.append({"idx": 0, "start": event["start"], "end": max(event["start"] + 1, event["end"]), "lines": [f"[{event['label_bn']}]"], "speakers": [], "kind": "sound", "cps": 0})
        cues.sort(key=lambda cue: cue["start"])
        for index, cue in enumerate(cues):
            cue["idx"] = index + 1
        outputs = ctx.root / "outputs"
        ctx.store.write_text(outputs / "episode_bn_cc.srt", write_srt(cues))
        ctx.store.write_text(outputs / "episode_bn_cc.vtt", write_vtt(cues))
        return {"cues": cues, "srt": "outputs/episode_bn_cc.srt", "vtt": "outputs/episode_bn_cc.vtt"}
    
    
    def s17_qc(ctx: StageContext) -> dict:
        cues, utterances = ctx.stage("s15_subtitles")["cues"], ctx.stage("s07_transcript_clean")["utterances"]
        threshold = ctx.settings.thresholds
        issues = []
        def add(severity: str, rule: str, time_value: float, cue_idx: int | None, message: str, suggestion: str | None = None):
            issues.append({"issue_id": f"qc_{len(issues) + 1:05d}", "severity": severity, "rule": rule, "time": time_value, "cue_idx": cue_idx, "message": message, "suggestion": suggestion})
        for utterance in utterances:
            if utterance.get("confidence") is not None and utterance["confidence"] < .6:
                add("warn", "low_confidence", utterance["start"], None, "Speech recognition confidence is below 0.60.", "Review against the source audio.")
            if utterance.get("overlap"):
                add("warn", "overlap_speech", utterance["start"], None, "Overlapping speech may obscure speaker attribution.", "Confirm speaker turns manually.")
        for cue in cues:
            if cue["cps"] > 21:
                add("error", "reading_speed", cue["start"], cue["idx"], f"Reading speed is {cue['cps']:.1f} cps.", "Split or extend the cue.")
            elif cue["cps"] > threshold.subtitle_max_cps:
                add("warn", "reading_speed", cue["start"], cue["idx"], f"Reading speed is {cue['cps']:.1f} cps.", "Extend the cue if silence permits.")
            if any(grapheme_len(line) > threshold.subtitle_max_line_graphemes for line in cue["lines"]):
                add("warn", "line_length", cue["start"], cue["idx"], "A subtitle line exceeds 42 graphemes.", "Rebalance the line break.")
            if len(cue["lines"]) > threshold.subtitle_max_lines:
                add("error", "line_count", cue["start"], cue["idx"], "The cue has more than two lines.", "Split the cue.")
            duration = cue["end"] - cue["start"]
            if duration < threshold.subtitle_min_duration or duration > threshold.subtitle_max_duration:
                add("warn", "duration", cue["start"], cue["idx"], f"Cue duration is {duration:.2f} seconds.", "Adjust the cue timing.")
        summary = {severity: sum(issue["severity"] == severity for issue in issues) for severity in ("error", "warn", "info")}
        summary["passed"] = summary["error"] == 0
        ctx.store.write_json(ctx.root / "outputs" / "qc_report.json", {"summary": summary, "issues": issues})
        return {"issues": issues, "summary": summary}
    
    
    def s18_assemble(ctx: StageContext) -> dict:
        ingest = ctx.stage("s01_ingest")
        transcript = ctx.stage("s07_transcript_clean")
        audio = ctx.stage("s08_audio_events")
        semantics = ctx.stage("s13_scene_semantics")
        entities = ctx.stage("s12_vision_targeted")
        ads = ctx.stage("s14_ad_scoring")
        subs = ctx.stage("s15_subtitles")
        cc = ctx.stage("s16_captions")
        qc = ctx.stage("s17_qc")
        record = ctx.db.get_episode_record(ctx.episode_id)
        timeline = SemanticTimeline.model_validate({
            "schema_version": "1.0",
            "episode": {"id": ctx.episode_id, "title": record.title if record else ctx.episode_id, "duration": ingest["duration"], "fps": ingest["fps"], "resolution": f"{ingest['width']}×{ingest['height']}", "video_available": True},
            "scenes": semantics["scenes"], "shots": ctx.stage("s03_keyframes")["shots"], "utterances": transcript["utterances"],
            "audio_events": audio["events"], "entities": entities["entities"], "ad_candidates": ads["candidates"],
            "subtitles": {"sub_srt": subs["srt"], "sub_vtt": subs["vtt"], "cc_srt": cc["srt"], "cc_vtt": cc["vtt"], "cue_count": len(subs["cues"])},
            "subtitle_cues": subs["cues"], "cc_cues": cc["cues"], "qc": qc["issues"],
            "curves": {"intensity": semantics["intensity"], "loudness": audio["loudness"]},
            "processing": {"thresholds": ctx.settings.thresholds.model_dump(), "models": {"stt": "saaras:v4", "llm": ctx.settings.llm_model_default}, "llm_cost_usd": 0.0},
        })
        output = ctx.root / "outputs" / "semantic_timeline.json"
        ctx.store.write_json(output, timeline)
        ctx.store.write_json(ctx.root / "outputs" / "ad_cuepoints.json", ads["candidates"])
        return {"timeline": "outputs/semantic_timeline.json", "schema_version": "1.0"}
    

## Assistant

The stage implementations now cover real ffprobe/ffmpeg ingest, browser proxying, shot boundaries, keyframes and deduplication, audio extraction, silence/VAD segmentation, Sarvam batch diarization, deterministic subtitle formatting, captions, QC, ad scoring, schema validation, and atomic output assembly. Conservative fallbacks explicitly produce `unverified` rather than false visual claims when a model provider is absent.

## Activity

    file changes: Completed · 1 changes
    Add: C:\Users\asus\Desktop\hoichoi\backend\pipeline\runner.py
    from __future__ import annotations
    
    import json
    import threading
    import time
    from concurrent.futures import Future, ThreadPoolExecutor
    from dataclasses import dataclass
    from datetime import UTC, datetime
    from pathlib import Path
    from typing import Callable
    
    from app.artifacts import ArtifactStore
    from app.db import Database
    from app.settings import Settings
    from pipeline.errors import PipelineError
    from pipeline.stages.core import (
        StageContext,
        s01_ingest, s02_shots, s03_keyframes, s04_audio_prep, s05_vad, s06_stt,
        s07_transcript_clean, s08_audio_events, s09_vision_baseline, s10_scenes,
        s11_entities_dialogue, s12_vision_targeted, s13_scene_semantics,
        s14_ad_scoring, s15_subtitles, s16_captions, s17_qc, s18_assemble,
    )
    
    
    @dataclass(frozen=True)
    class StageSpec:
        id: str
        label: str
        dependencies: tuple[str, ...]
        version: str
        run: Callable[[StageContext], dict]
    
    
    STAGES: tuple[StageSpec, ...] = (
        StageSpec("s01_ingest", "Ingest", (), "2", s01_ingest),
        StageSpec("s02_shots", "Shot detection", ("s01_ingest",), "2", s02_shots),
        StageSpec("s03_keyframes", "Keyframes", ("s01_ingest", "s02_shots"), "2", s03_keyframes),
        StageSpec("s04_audio_prep", "Audio preparation", ("s01_ingest",), "2", s04_audio_prep),
        StageSpec("s05_vad", "Voice activity", ("s01_ingest", "s04_audio_prep"), "2", s05_vad),
        StageSpec("s06_stt", "Transcript + diarization", ("s04_audio_prep", "s05_vad"), "2", s06_stt),
        StageSpec("s07_transcript_clean", "Transcript cleanup", ("s06_stt",), "2", s07_transcript_clean),
        StageSpec("s08_audio_events", "Audio events", ("s04_audio_prep",), "2", s08_audio_events),
        StageSpec("s09_vision_baseline", "Visual understanding", ("s03_keyframes",), "2", s09_vision_baseline),
        StageSpec("s10_scenes", "Scene segmentation", ("s01_ingest", "s03_keyframes", "s07_transcript_clean", "s09_vision_baseline"), "2", s10_scenes),
        StageSpec("s11_entities_dialogue", "Dialogue entities", ("s07_transcript_clean", "s10_scenes"), "2", s11_entities_dialogue),
        StageSpec("s12_vision_targeted", "Targeted visual checks", ("s03_keyframes", "s11_entities_dialogue"), "2", s12_vision_targeted),
        StageSpec("s13_scene_semantics", "Scene semantics", ("s07_transcript_clean", "s08_audio_events", "s12_vision_targeted"), "2", s13_scene_semantics),
        StageSpec("s14_ad_scoring", "Ad scoring", ("s01_ingest", "s05_vad", "s12_vision_targeted", "s13_scene_semantics"), "2", s14_ad_scoring),
        StageSpec("s15_subtitles", "Bengali subtitles", ("s07_transcript_clean",), "2", s15_subtitles),
        StageSpec("s16_captions", "Closed captions", ("s08_audio_events", "s15_subtitles"), "2", s16_captions),
        StageSpec("s17_qc", "Subtitle QC", ("s05_vad", "s07_transcript_clean", "s15_subtitles"), "2", s17_qc),
        StageSpec("s18_assemble", "Assemble timeline", ("s03_keyframes", "s07_transcript_clean", "s08_audio_events", "s12_vision_targeted", "s13_scene_semantics", "s14_ad_scoring", "s15_subtitles", "s16_captions", "s17_qc"), "2", s18_assemble),
    )
    
    
    STAGE_PAIRS = [(stage.id, stage.label) for stage in STAGES]
    
    
    class PipelineRunner:
        def __init__(self, settings: Settings, database: Database, store: ArtifactStore):
            self.settings = settings
            self.database = database
            self.store = store
    
        def run(self, episode_id: str, *, from_stage: str | None = None, force: bool = False) -> None:
            context = StageContext(episode_id=episode_id, settings=self.settings, store=self.store, db=self.database)
            self.store.ensure_episode(episode_id)
            start_index = 0
            if from_stage:
                start_index = next((index for index, stage in enumerate(STAGES) if stage.id == from_stage), -1)
                if start_index < 0:
                    raise PipelineError(f"Unknown stage: {from_stage}")
            self.database.update_episode(episode_id, status="processing")
            pipeline_started = time.perf_counter()
            for index, stage in enumerate(STAGES):
                if index < start_index:
                    continue
                try:
                    input_hash = self._input_hash(context, stage)
                    stage_record = next(record for record in self.database.get_stages(episode_id) if record.stage_id == stage.id)
                    artifact = self.store.stage_path(episode_id, stage.id)
                    cache_valid = artifact.exists() and stage_record.input_hash == input_hash and stage_record.status == "done"
                    if cache_valid and not (force and index >= start_index):
                        self._update_progress(episode_id, index + 1)
                        continue
                    started = datetime.now(UTC)
                    self.database.update_stage(episode_id, stage.id, status="running", error=None, started_at=started, finished_at=None)
                    stage_started = time.perf_counter()
                    value = stage.run(context)
                    self.store.write_json(artifact, value)
                    elapsed = round(time.perf_counter() - stage_started, 3)
                    self.database.update_stage(
                        episode_id, stage.id, status="done", elapsed=elapsed, error=None, input_hash=input_hash,
                        finished_at=datetime.now(UTC),
                    )
                    self._update_progress(episode_id, index + 1)
                    self._log(episode_id, {"event": "stage_done", "stage": stage.id, "elapsed": elapsed, "cached": False})
                except Exception as exc:
                    message = str(exc) if isinstance(exc, PipelineError) else f"{type(exc).__name__}: {exc}"
                    self.database.update_stage(episode_id, stage.id, status="failed", error=message, finished_at=datetime.now(UTC))
                    self.database.update_episode(episode_id, status="failed")
                    self._log(episode_id, {"event": "stage_failed", "stage": stage.id, "error": message})
                    return
            self.database.update_episode(episode_id, status="processed", progress=100)
            self._log(episode_id, {"event": "pipeline_done", "elapsed": round(time.perf_counter() - pipeline_started, 3)})
    
        def _input_hash(self, context: StageContext, stage: StageSpec) -> str:
            base = context.store.stage_input_hash(context.episode_id, stage.id, list(stage.dependencies), stage.version)
            if stage.id != "s01_ingest":
                return base
            record = self.database.get_episode_record(context.episode_id)
            if record is None or not Path(record.source_path).exists():
                return base
            import hashlib
            digest = hashlib.sha256(base.encode())
            digest.update(context.store.file_hash(Path(record.source_path)).encode())
            return digest.hexdigest()
    
        def _update_progress(self, episode_id: str, completed: int) -> None:
            self.database.update_episode(episode_id, progress=round(completed / len(STAGES) * 100))
    
        def _log(self, episode_id: str, record: dict) -> None:
            record["time"] = datetime.now(UTC).isoformat()
            path = self.store.episode_dir(episode_id) / "logs" / "pipeline.jsonl"
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    
    
    class PipelineCoordinator:
        """A bounded local worker. Replaceable with RQ without changing API routes."""
    
        def __init__(self, runner: PipelineRunner, concurrency: int = 1):
            self.runner = runner
            self.executor = ThreadPoolExecutor(max_workers=max(1, concurrency), thread_name_prefix="drishti-worker")
            self._futures: dict[str, Future[None]] = {}
            self._lock = threading.Lock()
    
        def enqueue(self, episode_id: str, *, from_stage: str | None = None, force: bool = False) -> bool:
            with self._lock:
                current = self._futures.get(episode_id)
                if current and not current.done():
                    return False
                self._futures[episode_id] = self.executor.submit(self.runner.run, episode_id, from_stage=from_stage, force=force)
                return True
    
        def running(self, episode_id: str) -> bool:
            with self._lock:
                future = self._futures.get(episode_id)
                return bool(future and not future.done())
    
        def shutdown(self) -> None:
            self.executor.shutdown(wait=False, cancel_futures=False)
    

## Activity

    file changes: Completed · 1 changes
    Delete: C:\Users\asus\Desktop\hoichoi\backend\app\main.py
    from __future__ import annotations
    
    import asyncio
    import csv
    import io
    import json
    import re
    import shutil
    from datetime import UTC, datetime
    from pathlib import Path
    from typing import Annotated
    from uuid import uuid4
    
    from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, Query, UploadFile
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import FileResponse, PlainTextResponse, Response, StreamingResponse
    
    from .demo_data import DEMO_EPISODE, DEMO_ID, DEMO_TIMELINE
    from .models import AdSelectionPatch, EpisodeSummary, RerunRequest, SemanticTimeline, StageStatus
    
    
    APP_DIR = Path(__file__).resolve().parent
    DATA_DIR = APP_DIR.parent.parent / "data" / "episodes"
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    app = FastAPI(
        title="Hoichoi Drishti API",
        version="0.1.0",
        description="Semantic timeline, ad intelligence, localization, and QC API.",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    episodes: dict[str, EpisodeSummary] = {DEMO_ID: DEMO_EPISODE.model_copy(deep=True)}
    timelines: dict[str, SemanticTimeline] = {DEMO_ID: DEMO_TIMELINE.model_copy(deep=True)}
    
    
    def _slug(value: str) -> str:
        return re.sub(r"[^a-zA-Z0-9_-]+", "-", value).strip("-").lower() or "episode"
    
    
    async def _simulate_pipeline(episode_id: str) -> None:
        episode = episodes[episode_id]
        episode.status = "processing"
        total = len(episode.stages)
        for index, stage in enumerate(episode.stages):
            stage.status = "running"
            await asyncio.sleep(0.35)
            stage.status = "done"
            stage.elapsed = round(1.2 + index * 0.8, 1)
            episode.progress = round((index + 1) / total * 100)
        episode.status = "processed"
    
    
    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}
    
    
    @app.get("/episodes", response_model=list[EpisodeSummary])
    def list_episodes() -> list[EpisodeSummary]:
        return sorted(episodes.values(), key=lambda item: item.created_at, reverse=True)
    
    
    @app.post("/episodes", response_model=EpisodeSummary, status_code=201)
    async def create_episode(
        background_tasks: BackgroundTasks,
        file: Annotated[UploadFile | None, File()] = None,
        path: Annotated[str | None, Form()] = None,
        title: Annotated[str | None, Form()] = None,
    ) -> EpisodeSummary:
        if file is None and not path:
            raise HTTPException(422, "Upload a video or provide a local path.")
        episode_id = f"ep-{uuid4().hex[:8]}"
        display_title = title or (Path(file.filename or "Untitled").stem if file else Path(path or "Untitled").stem)
        directory = DATA_DIR / episode_id
        directory.mkdir(parents=True, exist_ok=True)
        video_available = False
        if file is not None:
            suffix = Path(file.filename or "video.mp4").suffix.lower()
            if suffix not in {".mp4", ".mkv", ".mov", ".webm"}:
                raise HTTPException(415, "Supported video formats: MP4, MKV, MOV, and WebM.")
            destination = directory / f"source{suffix}"
            with destination.open("wb") as output:
                shutil.copyfileobj(file.file, output)
            video_available = suffix in {".mp4", ".webm"}
        elif path:
            source = Path(path).expanduser()
            video_available = source.exists() and source.suffix.lower() in {".mp4", ".webm"}
        stages = [StageStatus(id=stage_id, label=label, status="queued") for stage_id, label in [
            ("s01", "Ingest"), ("s06", "Transcript"), ("s10", "Scenes"),
            ("s12", "Entity checks"), ("s14", "Ad scoring"), ("s18", "Assemble"),
        ]]
        episode = EpisodeSummary(
            id=episode_id,
            title=display_title,
            duration=0,
            status="queued",
            progress=0,
            created_at=datetime.now(UTC).isoformat(),
            video_available=video_available,
            stages=stages,
        )
        episodes[episode_id] = episode
        # A demo timeline keeps the workspace usable until real pipeline artifacts replace it.
        timeline = DEMO_TIMELINE.model_copy(deep=True)
        timeline.episode.update({"id": episode_id, "title": display_title, "video_available": video_available})
        timelines[episode_id] = timeline
        background_tasks.add_task(_simulate_pipeline, episode_id)
        return episode
    
    
    def _episode_or_404(episode_id: str) -> EpisodeSummary:
        if episode_id not in episodes:
            raise HTTPException(404, "Episode not found.")
        return episodes[episode_id]
    
    
    def _timeline_or_404(episode_id: str) -> SemanticTimeline:
        _episode_or_404(episode_id)
        return timelines[episode_id]
    
    
    @app.get("/episodes/{episode_id}", response_model=EpisodeSummary)
    def get_episode(episode_id: str) -> EpisodeSummary:
        return _episode_or_404(episode_id)
    
    
    @app.get("/episodes/{episode_id}/events")
    async def episode_events(episode_id: str) -> StreamingResponse:
        _episode_or_404(episode_id)
    
        async def event_stream():
            last = ""
            while True:
                payload = _episode_or_404(episode_id).model_dump_json()
                if payload != last:
                    yield f"event: progress\ndata: {payload}\n\n"
                    last = payload
                if episodes[episode_id].status in {"processed", "failed"}:
                    break
                await asyncio.sleep(0.25)
    
        return StreamingResponse(event_stream(), media_type="text/event-stream", headers={"Cache-Control": "no-cache"})
    
    
    @app.post("/episodes/{episode_id}/rerun", response_model=EpisodeSummary)
    async def rerun_episode(episode_id: str, request: RerunRequest, background_tasks: BackgroundTasks) -> EpisodeSummary:
        episode = _episode_or_404(episode_id)
        found = False
        for stage in episode.stages:
            if stage.id == request.from_stage:
                found = True
            if found:
                stage.status = "queued"
                stage.elapsed = None
        if not found:
            raise HTTPException(422, f"Unknown stage: {request.from_stage}")
        episode.progress = 0
        episode.status = "queued"
        background_tasks.add_task(_simulate_pipeline, episode_id)
        return episode
    
    
    @app.get("/episodes/{episode_id}/timeline", response_model=SemanticTimeline)
    def get_timeline(episode_id: str) -> SemanticTimeline:
        return _timeline_or_404(episode_id)
    
    
    @app.get("/episodes/{episode_id}/scenes/{scene_id}")
    def get_scene(episode_id: str, scene_id: str) -> dict:
        timeline = _timeline_or_404(episode_id)
        scene = next((item for item in timeline.scenes if item.scene_id == scene_id), None)
        if scene is None:
            raise HTTPException(404, "Scene not found.")
        return {
            **scene.model_dump(),
            "utterances": [u for u in timeline.utterances if u.utt_id in scene.utt_ids],
            "entities": [e for e in timeline.entities if e.entity_id in scene.entity_ids],
        }
    
    
    @app.get("/episodes/{episode_id}/ads")
    def get_ads(
        episode_id: str,
        min_gap: int = Query(480, ge=0),
        n_breaks: int = Query(2, ge=1, le=20),
        blocked: str = Query("120,120"),
    ) -> list[dict]:
        timeline = _timeline_or_404(episode_id)
        try:
            head, tail = [float(value) for value in blocked.split(",", maxsplit=1)]
        except ValueError as exc:
            raise HTTPException(422, "blocked must be 'start_seconds,end_seconds'.") from exc
        candidates = [candidate.model_copy(deep=True) for candidate in timeline.ad_candidates if head <= candidate.time <= float(timeline.episode["duration"]) - tail]
        ranked = sorted(candidates, key=lambda item: item.score.total, reverse=True)
        selected_times: list[float] = []
        for candidate in ranked:
            candidate.selected = len(selected_times) < n_breaks and all(abs(candidate.time - used) >= min_gap for used in selected_times)
            if candidate.selected:
                selected_times.append(candidate.time)
        return [candidate.model_dump() for candidate in ranked]
    
    
    @app.patch("/episodes/{episode_id}/ads/{candidate_id}")
    def patch_ad(episode_id: str, candidate_id: str, payload: AdSelectionPatch) -> dict:
        timeline = _timeline_or_404(episode_id)
        candidate = next((item for item in timeline.ad_candidates if item.cand_id == candidate_id), None)
        if candidate is None:
            raise HTTPException(404, "Ad candidate not found.")
        candidate.selected = payload.selected
        return candidate.model_dump()
    
    
    def _timestamp(seconds: float, separator: str = ",") -> str:
        whole = int(seconds)
        millis = int(round((seconds - whole) * 1000))
        hours, remainder = divmod(whole, 3600)
        minutes, secs = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}{separator}{millis:03d}"
    
    
    def _subtitle_text(timeline: SemanticTimeline, kind: str, fmt: str) -> str:
        cues = timeline.cc_cues if kind == "cc" else timeline.subtitle_cues
        chunks: list[str] = ["WEBVTT\n"] if fmt == "vtt" else []
        for cue in sorted(cues, key=lambda item: item.start):
            start = _timestamp(cue.start, "." if fmt == "vtt" else ",")
            end = _timestamp(cue.end, "." if fmt == "vtt" else ",")
            prefix = "" if fmt == "vtt" else f"{cue.idx}\n"
            chunks.append(f"{prefix}{start} --> {end}\n" + "\n".join(cue.lines) + "\n")
        return "\n".join(chunks)
    
    
    @app.get("/episodes/{episode_id}/subs/{kind}.{fmt}")
    def subtitles(episode_id: str, kind: str, fmt: str) -> PlainTextResponse:
        if kind not in {"sub", "cc"} or fmt not in {"srt", "vtt"}:
            raise HTTPException(404, "Subtitle format not found.")
        body = _subtitle_text(_timeline_or_404(episode_id), kind, fmt)
        media_type = "text/vtt" if fmt == "vtt" else "application/x-subrip"
        return PlainTextResponse(body, media_type=media_type, headers={"Content-Disposition": f'attachment; filename="episode_bn_{kind}.{fmt}"'})
    
    
    @app.get("/episodes/{episode_id}/export/{name}")
    def export_file(episode_id: str, name: str) -> Response:
        timeline = _timeline_or_404(episode_id)
        if name == "semantic_timeline.json":
            return Response(timeline.model_dump_json(indent=2), media_type="application/json", headers={"Content-Disposition": f'attachment; filename="{name}"'})
        if name == "qc_report.json":
            return Response(json.dumps([item.model_dump() for item in timeline.qc], ensure_ascii=False, indent=2), media_type="application/json", headers={"Content-Disposition": f'attachment; filename="{name}"'})
        if name == "ad_cuepoints.csv":
            stream = io.StringIO()
            writer = csv.writer(stream)
            writer.writerow(["candidate_id", "time_seconds", "score", "selected", "categories", "reason"])
            for candidate in timeline.ad_candidates:
                writer.writerow([candidate.cand_id, candidate.time, candidate.score.total, candidate.selected, "|".join(candidate.matched_categories), candidate.reason])
            return Response(stream.getvalue(), media_type="text/csv", headers={"Content-Disposition": f'attachment; filename="{name}"'})
        raise HTTPException(404, "Export not found.")
    
    
    @app.get("/episodes/{episode_id}/video")
    def get_video(episode_id: str) -> FileResponse:
        _episode_or_404(episode_id)
        directory = DATA_DIR / episode_id
        source = next((path for path in directory.glob("source.*") if path.suffix.lower() in {".mp4", ".webm"}), None)
        if source is None:
            raise HTTPException(404, "No browser-playable video is attached to this episode.")
        return FileResponse(source, media_type="video/mp4" if source.suffix.lower() == ".mp4" else "video/webm")
    
    
    @app.get("/schema")
    def schema() -> dict:
        return SemanticTimeline.model_json_schema()
    
    
    @app.get("/search")
    def search(episode_id: str, q: str = Query(min_length=2)) -> list[dict]:
        timeline = _timeline_or_404(episode_id)
        needle = q.casefold()
        results: list[dict] = []
        for scene in timeline.scenes:
            haystack = f"{scene.semantic.title} {scene.semantic.summary} {' '.join(scene.semantic.topics)}".casefold()
            if needle in haystack:
                results.append({"type": "scene", "id": scene.scene_id, "time": scene.start, "text": scene.semantic.title})
        for utterance in timeline.utterances:
            if needle in utterance.text.casefold():
                results.append({"type": "utterance", "id": utterance.utt_id, "time": utterance.start, "text": utterance.text})
        return results[:20]
    

## Activity

    file changes: Completed · 1 changes
    Add: C:\Users\asus\Desktop\hoichoi\backend\app\main.py
    from __future__ import annotations
    
    import asyncio
    import csv
    import io
    import shutil
    from contextlib import asynccontextmanager
    from datetime import UTC, datetime
    from pathlib import Path
    from typing import Annotated
    from uuid import uuid4
    
    from fastapi import FastAPI, File, Form, HTTPException, Query, Request, UploadFile
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import FileResponse, Response, StreamingResponse
    
    from pipeline.runner import PipelineCoordinator, PipelineRunner, STAGES, STAGE_PAIRS
    from pipeline.scoring import select_candidates
    from pipeline.subtitles import write_srt, write_vtt
    
    from .artifacts import ArtifactStore
    from .db import Database, EpisodeRecord
    from .demo_data import DEMO_EPISODE, DEMO_ID, DEMO_TIMELINE
    from .models import AdSelectionPatch, EpisodeSummary, RerunRequest, SemanticTimeline
    from .settings import Settings
    
    
    def _seed_demo(settings: Settings, database: Database, store: ArtifactStore) -> None:
        if not settings.seed_demo or database.get_episode_record(DEMO_ID):
            return
        root = store.ensure_episode(DEMO_ID)
        database.create_episode(EpisodeRecord(
            id=DEMO_ID,
            title=DEMO_EPISODE.title,
            source_path="",
            duration=DEMO_EPISODE.duration,
            status="processed",
            progress=100,
            video_available=False,
        ), STAGE_PAIRS)
        for stage in STAGES:
            database.update_stage(DEMO_ID, stage.id, status="done", elapsed=.01, input_hash="seed", started_at=datetime.now(UTC), finished_at=datetime.now(UTC))
        store.write_json(root / "outputs" / "semantic_timeline.json", DEMO_TIMELINE)
        store.write_text(root / "outputs" / "episode_bn.srt", write_srt([cue.model_dump() for cue in DEMO_TIMELINE.subtitle_cues]))
        store.write_text(root / "outputs" / "episode_bn.vtt", write_vtt([cue.model_dump() for cue in DEMO_TIMELINE.subtitle_cues]))
        store.write_text(root / "outputs" / "episode_bn_cc.srt", write_srt([cue.model_dump() for cue in DEMO_TIMELINE.cc_cues]))
        store.write_text(root / "outputs" / "episode_bn_cc.vtt", write_vtt([cue.model_dump() for cue in DEMO_TIMELINE.cc_cues]))
        store.write_json(root / "outputs" / "qc_report.json", {"issues": [issue.model_dump() for issue in DEMO_TIMELINE.qc]})
    
    
    def create_app(custom_settings: Settings | None = None) -> FastAPI:
        settings = custom_settings or Settings()
        settings.episodes_dir.mkdir(parents=True, exist_ok=True)
        database = Database(settings)
        store = ArtifactStore(settings)
        runner = PipelineRunner(settings, database, store)
        coordinator = PipelineCoordinator(runner, settings.worker_concurrency)
        _seed_demo(settings, database, store)
    
        @asynccontextmanager
        async def lifespan(_: FastAPI):
            for record in database.list_episode_records():
                if record.status in {"queued", "processing"}:
                    stages = database.get_stages(record.id)
                    first = next((stage.stage_id for stage in stages if stage.status != "done"), None)
                    if first:
                        database.reset_from(record.id, first)
                        coordinator.enqueue(record.id, from_stage=first)
            yield
            coordinator.shutdown()
            database.close()
    
        api = FastAPI(
            title="Hoichoi Drishti API",
            version="1.0.0",
            description="Artifact-backed semantic timeline, ad intelligence, localization, and QC API.",
            lifespan=lifespan,
        )
        api.state.settings = settings
        api.state.database = database
        api.state.store = store
        api.state.coordinator = coordinator
        api.add_middleware(
            CORSMiddleware,
            allow_origins=settings.allowed_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
        def episode_or_404(episode_id: str) -> EpisodeRecord:
            record = database.get_episode_record(episode_id)
            if record is None:
                raise HTTPException(404, "Episode not found.")
            return record
    
        def timeline_or_409(episode_id: str) -> SemanticTimeline:
            record = episode_or_404(episode_id)
            path = store.output_path(episode_id, "semantic_timeline.json")
            if not path.exists():
                failed = next((stage for stage in database.get_stages(episode_id) if stage.status == "failed"), None)
                if failed:
                    raise HTTPException(409, {"message": "Timeline is unavailable because processing failed.", "stage": failed.stage_id, "error": failed.error})
                raise HTTPException(409, {"message": "Timeline is still processing.", "status": record.status, "progress": record.progress})
            try:
                return SemanticTimeline.model_validate(store.read_json(path))
            except Exception as exc:
                raise HTTPException(500, "The timeline artifact failed schema validation.") from exc
    
        @api.get("/health")
        def health() -> dict:
            return {"status": "ok", "worker": "local", "schema_version": "1.0"}
    
        @api.get("/episodes", response_model=list[EpisodeSummary])
        def list_episodes() -> list[EpisodeSummary]:
            return [database.summary(record) for record in database.list_episode_records()]
    
        @api.post("/episodes", response_model=EpisodeSummary, status_code=201)
        async def create_episode(
            request: Request,
            file: Annotated[UploadFile | None, File()] = None,
            path: Annotated[str | None, Form()] = None,
            title: Annotated[str | None, Form()] = None,
        ) -> EpisodeSummary:
            if request.headers.get("content-type", "").startswith("application/json"):
                payload = await request.json()
                path = payload.get("path")
                title = payload.get("title")
            if file is None and not path:
                raise HTTPException(422, "Upload a video or provide a local path.")
    
            episode_id = f"ep-{uuid4().hex[:12]}"
            root = store.ensure_episode(episode_id)
            allowed = {".mp4", ".mkv", ".mov", ".webm"}
            try:
                if file is not None:
                    suffix = Path(file.filename or "video.mp4").suffix.lower()
                    if suffix not in allowed:
                        raise HTTPException(415, "Supported video formats: MP4, MKV, MOV, and WebM.")
                    source = root / f"source{suffix}"
                    received = 0
                    with source.open("wb") as output:
                        while chunk := await file.read(1024 * 1024):
                            received += len(chunk)
                            if received > settings.max_upload_bytes:
                                raise HTTPException(413, "The upload exceeds the configured size limit.")
                            output.write(chunk)
                    display_title = title or Path(file.filename or "Untitled").stem
                else:
                    incoming = Path(path or "").expanduser().resolve()
                    if not incoming.is_file():
                        raise HTTPException(422, "The registered local video path does not exist.")
                    if incoming.suffix.lower() not in allowed:
                        raise HTTPException(415, "Supported video formats: MP4, MKV, MOV, and WebM.")
                    if incoming.stat().st_size > settings.max_upload_bytes:
                        raise HTTPException(413, "The source exceeds the configured size limit.")
                    source = root / f"source{incoming.suffix.lower()}"
                    shutil.copy2(incoming, source)
                    display_title = title or incoming.stem
            except Exception:
                shutil.rmtree(root, ignore_errors=True)
                raise
    
            record = EpisodeRecord(id=episode_id, title=display_title, source_path=str(source), status="queued", progress=0)
            database.create_episode(record, STAGE_PAIRS)
            coordinator.enqueue(episode_id)
            return database.summary(database.get_episode_record(episode_id) or record)
    
        @api.get("/episodes/{episode_id}", response_model=EpisodeSummary)
        def get_episode(episode_id: str) -> EpisodeSummary:
            return database.summary(episode_or_404(episode_id))
    
        @api.get("/episodes/{episode_id}/events")
        async def episode_events(episode_id: str) -> StreamingResponse:
            episode_or_404(episode_id)
    
            async def stream():
                previous = ""
                while True:
                    summary = database.summary(episode_or_404(episode_id))
                    payload = summary.model_dump_json()
                    if payload != previous:
                        yield f"event: progress\ndata: {payload}\n\n"
                        previous = payload
                    else:
                        yield ": keep-alive\n\n"
                    if summary.status in {"processed", "failed"}:
                        break
                    await asyncio.sleep(.75)
    
            return StreamingResponse(stream(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})
    
        @api.post("/episodes/{episode_id}/rerun", response_model=EpisodeSummary, status_code=202)
        def rerun_episode(episode_id: str, payload: RerunRequest) -> EpisodeSummary:
            episode_or_404(episode_id)
            if coordinator.running(episode_id):
                raise HTTPException(409, "This episode is already processing.")
            try:
                database.reset_from(episode_id, payload.from_stage)
            except KeyError as exc:
                raise HTTPException(422, f"Unknown stage: {payload.from_stage}") from exc
            coordinator.enqueue(episode_id, from_stage=payload.from_stage, force=payload.force)
            return database.summary(episode_or_404(episode_id))
    
        @api.get("/episodes/{episode_id}/timeline", response_model=SemanticTimeline)
        def get_timeline(episode_id: str) -> SemanticTimeline:
            return timeline_or_409(episode_id)
    
        @api.get("/episodes/{episode_id}/scenes/{scene_id}")
        def get_scene(episode_id: str, scene_id: str) -> dict:
            timeline = timeline_or_409(episode_id)
            scene = next((item for item in timeline.scenes if item.scene_id == scene_id), None)
            if scene is None:
                raise HTTPException(404, "Scene not found.")
            return {
                **scene.model_dump(),
                "utterances": [item.model_dump() for item in timeline.utterances if item.utt_id in scene.utt_ids],
                "entities": [item.model_dump() for item in timeline.entities if item.entity_id in scene.entity_ids],
            }
    
        @api.get("/episodes/{episode_id}/ads")
        def get_ads(
            episode_id: str,
            min_gap: int = Query(480, ge=0),
            n_breaks: int = Query(2, ge=1, le=20),
            blocked: str = Query("120,120"),
        ) -> list[dict]:
            timeline = timeline_or_409(episode_id)
            try:
                blocked_head, blocked_tail = [float(value) for value in blocked.split(",", 1)]
            except (ValueError, TypeError) as exc:
                raise HTTPException(422, "blocked must be 'start_seconds,end_seconds'.") from exc
            candidates = [
                candidate.model_dump() for candidate in timeline.ad_candidates
                if blocked_head <= candidate.time <= float(timeline.episode["duration"]) - blocked_tail
            ]
            return select_candidates(candidates, min_gap, n_breaks)
    
        @api.patch("/episodes/{episode_id}/ads/{candidate_id}")
        def patch_ad(episode_id: str, candidate_id: str, payload: AdSelectionPatch) -> dict:
            timeline = timeline_or_409(episode_id)
            candidate = next((item for item in timeline.ad_candidates if item.cand_id == candidate_id), None)
            if candidate is None:
                raise HTTPException(404, "Ad candidate not found.")
            candidate.selected = payload.selected
            store.write_json(store.output_path(episode_id, "semantic_timeline.json"), timeline)
            store.write_json(store.output_path(episode_id, "ad_cuepoints.json"), [item.model_dump() for item in timeline.ad_candidates])
            return candidate.model_dump()
    
        @api.get("/episodes/{episode_id}/frames/{name}")
        def get_frame(episode_id: str, name: str) -> FileResponse:
            episode_or_404(episode_id)
            try:
                path = store.safe_child(store.episode_dir(episode_id) / "frames", name)
            except ValueError as exc:
                raise HTTPException(400, "Invalid frame path.") from exc
            if not path.is_file():
                raise HTTPException(404, "Frame not found.")
            return FileResponse(path, media_type="image/jpeg", headers={"Cache-Control": "public, max-age=31536000, immutable"})
    
        @api.get("/episodes/{episode_id}/video")
        def get_video(episode_id: str) -> FileResponse:
            record = episode_or_404(episode_id)
            ingest_path = store.stage_path(episode_id, "s01_ingest")
            path: Path | None = None
            if ingest_path.exists():
                ingest = store.read_json(ingest_path)
                candidate = store.safe_child(store.episode_dir(episode_id), ingest.get("proxy", ingest["source"]))
                if candidate.is_file():
                    path = candidate
            if path is None and record.source_path and Path(record.source_path).is_file():
                path = Path(record.source_path)
            if path is None:
                raise HTTPException(404, "No playable video is attached to this episode.")
            media_type = "video/webm" if path.suffix.lower() == ".webm" else "video/mp4"
            return FileResponse(path, media_type=media_type, filename=None)
    
        @api.get("/episodes/{episode_id}/subs/{kind}.{fmt}")
        def get_subtitles(episode_id: str, kind: str, fmt: str) -> FileResponse:
            episode_or_404(episode_id)
            if kind not in {"sub", "cc"} or fmt not in {"srt", "vtt"}:
                raise HTTPException(404, "Subtitle format not found.")
            suffix = "" if kind == "sub" else "_cc"
            path = store.output_path(episode_id, f"episode_bn{suffix}.{fmt}")
            if not path.is_file():
                raise HTTPException(409, "Subtitle output is not ready.")
            media_type = "text/vtt" if fmt == "vtt" else "application/x-subrip"
            return FileResponse(path, media_type=media_type, filename=path.name)
    
        @api.get("/episodes/{episode_id}/export/{name}")
        def export_file(episode_id: str, name: str) -> Response:
            timeline = timeline_or_409(episode_id)
            if name == "semantic_timeline.json":
                return FileResponse(store.output_path(episode_id, name), media_type="application/json", filename=name)
            if name == "qc_report.json":
                path = store.output_path(episode_id, name)
                if not path.exists():
                    store.write_json(path, {"issues": [item.model_dump() for item in timeline.qc]})
                return FileResponse(path, media_type="application/json", filename=name)
            if name == "ad_cuepoints.csv":
                stream = io.StringIO()
                writer = csv.writer(stream)
                writer.writerow(["candidate_id", "time_seconds", "score", "selected", "categories", "reason"])
                for candidate in timeline.ad_candidates:
                    writer.writerow([candidate.cand_id, candidate.time, candidate.score.total, candidate.selected, "|".join(candidate.matched_categories), candidate.reason])
                return Response(stream.getvalue(), media_type="text/csv", headers={"Content-Disposition": f'attachment; filename="{name}"'})
            raise HTTPException(404, "Export not found.")
    
        @api.get("/search")
        def search(episode_id: str, q: str = Query(min_length=2)) -> list[dict]:
            timeline = timeline_or_409(episode_id)
            needle = q.casefold()
            results = []
            for scene in timeline.scenes:
                if needle in f"{scene.semantic.title} {scene.semantic.summary} {' '.join(scene.semantic.topics)}".casefold():
                    results.append({"type": "scene", "id": scene.scene_id, "time": scene.start, "text": scene.semantic.title})
            for utterance in timeline.utterances:
                if needle in utterance.text.casefold():
                    results.append({"type": "utterance", "id": utterance.utt_id, "time": utterance.start, "text": utterance.text})
            return results[:20]
    
        @api.get("/schema")
        def schema() -> dict:
            return SemanticTimeline.model_json_schema()
    
        return api
    
    
    app = create_app()
    

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'python -m pip install -e ".[dev,media]"'
    status: Failed · exit 1
      Defaulting to user installation because normal site-packages is not writeable
      Obtaining file:///C:/Users/asus/Desktop/hoichoi/backend
        Installing build dependencies: started
        Installing build dependencies: finished with status 'error'
        error: subprocess-exited-with-error
      
        pip subprocess to install build dependencies did not run successfully.
        exit code: 1
      
        [7 lines of output]
        WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x000001C3E63D5CD0>: Failed to establish a new connection: [WinError 10013] An attempt was made to access a socket in a way forbidden by its access permissions')': /simple/setuptools/
        WARNING: Retrying (Retry(total=3, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x000001C3E63D6550>: Failed to establish a new connection: [WinError 10013] An attempt was made to access a socket in a way forbidden by its access permissions')': /simple/setuptools/
        WARNING: Retrying (Retry(total=2, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x000001C3E63D7010>: Failed to establish a new connection: [WinError 10013] An attempt was made to access a socket in a way forbidden by its access permissions')': /simple/setuptools/
        WARNING: Retrying (Retry(total=1, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x000001C3E63D7C50>: Failed to establish a new connection: [WinError 10013] An attempt was made to access a socket in a way forbidden by its access permissions')': /simple/setuptools/
        WARNING: Retrying (Retry(total=0, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x000001C3E63E08D0>: Failed to establish a new connection: [WinError 10013] An attempt was made to access a socket in a way forbidden by its access permissions')': /simple/setuptools/
        ERROR: Could not find a version that satisfies the requirement setuptools>=40.8.0 (from versions: none)
        ERROR: No matching distribution found for setuptools>=40.8.0
        [end of output]
      
        note: This error originates from a subprocess, and is likely not a problem with pip.
      error: subprocess-exited-with-error
      
      pip subprocess to install build dependencies did not run successfully.
      exit code: 1
      
      See above for output.
      
      note: This error originates from a subprocess, and is likely not a problem with pip.

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'python -m pip install -e ".[dev,media]"'
    status: Failed · exit 1
      Obtaining file:///C:/Users/asus/Desktop/hoichoi/backend
        Installing build dependencies: started
        Installing build dependencies: finished with status 'done'
        Checking if build backend supports build_editable: started
        Checking if build backend supports build_editable: finished with status 'done'
        Getting requirements to build editable: started
        Getting requirements to build editable: finished with status 'error'
        error: subprocess-exited-with-error
      
        Getting requirements to build editable did not run successfully.
        exit code: 1
      
        [14 lines of output]
        error: Multiple top-level packages discovered in a flat-layout: ['app', 'config', 'pipeline', 'snapshot_failures'].
      
        To avoid accidental inclusion of unwanted files or directories,
        setuptools will not proceed with this build.
      
        If you are trying to create a single distribution with multiple packages
        on purpose, you should not rely on automatic discovery.
        Instead, consider the following options:
      
        1. set up custom discovery (`find` directive with `include` or `exclude`)
        2. use a `src-layout`
        3. explicitly set `py_modules` or `packages` with a list of names
      
        To find more information, look for "package discovery" on setuptools docs.
        [end of output]
      
        note: This error originates from a subprocess, and is likely not a problem with pip.
      
      [notice] A new release of pip is available: 25.2 -> 26.2.1
      [notice] To update, run: python.exe -m pip install --upgrade pip
      error: subprocess-exited-with-error
      
      Getting requirements to build editable did not run successfully.
      exit code: 1
      
      See above for output.
      
      note: This error originates from a subprocess, and is likely not a problem with pip.

## Assistant

The dependency download reached the registry, but editable installation exposed a packaging issue: setuptools was auto-discovering an unrelated `snapshot_failures` directory alongside `app` and `pipeline`. I’m tightening package discovery to only the two backend packages, then continuing the test pass.

## Activity

    file changes: Completed · 1 changes
    Update { move_path: None }: C:\Users\asus\Desktop\hoichoi\backend\pyproject.toml
    @@ -23,2 +23,11 @@
     
    +[build-system]
    +requires = ["setuptools>=75"]
    +build-backend = "setuptools.build_meta"
    +
    +[tool.setuptools.packages.find]
    +where = ["."]
    +include = ["app*", "pipeline*"]
    +exclude = ["tests*", "snapshot_failures*"]
    +
     [tool.pytest.ini_options]

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'python -m pip install -e ".[dev,media]"'
    status: Completed · exit 0
      Obtaining file:///C:/Users/asus/Desktop/hoichoi/backend
        Installing build dependencies: started
        Installing build dependencies: finished with status 'done'
        Checking if build backend supports build_editable: started
        Checking if build backend supports build_editable: finished with status 'done'
        Getting requirements to build editable: started
        Getting requirements to build editable: finished with status 'done'
        Preparing editable metadata (pyproject.toml): started
        Preparing editable metadata (pyproject.toml): finished with status 'done'
      Requirement already satisfied: fastapi<1,>=0.115 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from hoichoi-drishti-api==0.1.0) (0.115.6)
      Requirement already satisfied: uvicorn<1,>=0.34 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from uvicorn[standard]<1,>=0.34->hoichoi-drishti-api==0.1.0) (0.34.0)
      Requirement already satisfied: pydantic<3,>=2.10 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from hoichoi-drishti-api==0.1.0) (2.13.5)
      Requirement already satisfied: pydantic-settings<3,>=2.7 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from hoichoi-drishti-api==0.1.0) (2.7.0)
      Requirement already satisfied: python-multipart<1,>=0.0.20 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from hoichoi-drishti-api==0.1.0) (0.0.20)
      Collecting sqlmodel<1,>=0.0.24 (from hoichoi-drishti-api==0.1.0)
        Downloading sqlmodel-0.0.47-py3-none-any.whl.metadata (9.5 kB)
      Requirement already satisfied: httpx<1,>=0.28 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from hoichoi-drishti-api==0.1.0) (0.28.1)
      Requirement already satisfied: PyYAML<7,>=6.0 in c:\users\asus\appdata\roaming\python\python311\site-packages (from hoichoi-drishti-api==0.1.0) (6.0.3)
      Requirement already satisfied: regex>=2024.11.6 in c:\users\asus\appdata\roaming\python\python311\site-packages (from hoichoi-drishti-api==0.1.0) (2026.5.9)
      Collecting srt<4,>=3.5 (from hoichoi-drishti-api==0.1.0)
        Downloading srt-3.5.3.tar.gz (28 kB)
        Preparing metadata (setup.py): started
        Preparing metadata (setup.py): finished with status 'done'
      Requirement already satisfied: pytest<9,>=8.3 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from hoichoi-drishti-api==0.1.0) (8.3.4)
      Requirement already satisfied: Pillow<13,>=11 in c:\users\asus\appdata\roaming\python\python311\site-packages (from hoichoi-drishti-api==0.1.0) (12.2.0)
      Requirement already satisfied: starlette<0.42.0,>=0.40.0 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from fastapi<1,>=0.115->hoichoi-drishti-api==0.1.0) (0.41.3)
      Requirement already satisfied: typing-extensions>=4.8.0 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from fastapi<1,>=0.115->hoichoi-drishti-api==0.1.0) (4.15.0)
      Requirement already satisfied: anyio in c:\users\asus\appdata\roaming\python\python311\site-packages (from httpx<1,>=0.28->hoichoi-drishti-api==0.1.0) (4.12.1)
      Requirement already satisfied: certifi in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from httpx<1,>=0.28->hoichoi-drishti-api==0.1.0) (2026.7.22)
      Requirement already satisfied: httpcore==1.* in c:\users\asus\appdata\roaming\python\python311\site-packages (from httpx<1,>=0.28->hoichoi-drishti-api==0.1.0) (1.0.9)
      Requirement already satisfied: idna in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from httpx<1,>=0.28->hoichoi-drishti-api==0.1.0) (3.18)
      Requirement already satisfied: h11>=0.16 in c:\users\asus\appdata\roaming\python\python311\site-packages (from httpcore==1.*->httpx<1,>=0.28->hoichoi-drishti-api==0.1.0) (0.16.0)
      Requirement already satisfied: annotated-types>=0.6.0 in c:\users\asus\appdata\roaming\python\python311\site-packages (from pydantic<3,>=2.10->hoichoi-drishti-api==0.1.0) (0.7.0)
      Requirement already satisfied: pydantic-core==2.46.5 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from pydantic<3,>=2.10->hoichoi-drishti-api==0.1.0) (2.46.5)
      Requirement already satisfied: typing-inspection>=0.4.2 in c:\users\asus\appdata\roaming\python\python311\site-packages (from pydantic<3,>=2.10->hoichoi-drishti-api==0.1.0) (0.4.2)
      Requirement already satisfied: python-dotenv>=0.21.0 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from pydantic-settings<3,>=2.7->hoichoi-drishti-api==0.1.0) (1.0.1)
      Requirement already satisfied: colorama in c:\users\asus\appdata\roaming\python\python311\site-packages (from pytest<9,>=8.3->hoichoi-drishti-api==0.1.0) (0.4.6)
      Requirement already satisfied: iniconfig in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from pytest<9,>=8.3->hoichoi-drishti-api==0.1.0) (2.3.0)
      Requirement already satisfied: packaging in c:\users\asus\appdata\roaming\python\python311\site-packages (from pytest<9,>=8.3->hoichoi-drishti-api==0.1.0) (25.0)
      Requirement already satisfied: pluggy<2,>=1.5 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from pytest<9,>=8.3->hoichoi-drishti-api==0.1.0) (1.6.0)
      Requirement already satisfied: SQLAlchemy<2.1.0,>=2.0.14 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from sqlmodel<1,>=0.0.24->hoichoi-drishti-api==0.1.0) (2.0.51)
      Requirement already satisfied: greenlet>=1 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from SQLAlchemy<2.1.0,>=2.0.14->sqlmodel<1,>=0.0.24->hoichoi-drishti-api==0.1.0) (3.5.4)
      Requirement already satisfied: click>=7.0 in c:\users\asus\appdata\roaming\python\python311\site-packages (from uvicorn<1,>=0.34->uvicorn[standard]<1,>=0.34->hoichoi-drishti-api==0.1.0) (8.3.0)
      Requirement already satisfied: httptools>=0.6.3 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from uvicorn[standard]<1,>=0.34->hoichoi-drishti-api==0.1.0) (0.8.0)
      Requirement already satisfied: watchfiles>=0.13 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from uvicorn[standard]<1,>=0.34->hoichoi-drishti-api==0.1.0) (1.2.0)
      Requirement already satisfied: websockets>=10.4 in c:\users\asus\appdata\local\programs\python\python311\lib\site-packages (from uvicorn[standard]<1,>=0.34->hoichoi-drishti-api==0.1.0) (15.0.1)
      Downloading sqlmodel-0.0.47-py3-none-any.whl (31 kB)
      Building wheels for collected packages: hoichoi-drishti-api, srt
        Building editable for hoichoi-drishti-api (pyproject.toml): started
        Building editable for hoichoi-drishti-api (pyproject.toml): finished with status 'done'
        Created wheel for hoichoi-drishti-api: filename=hoichoi_drishti_api-0.1.0-0.editable-py3-none-any.whl size=3122 sha256=541d87005f37d76f8d75c4c6c48c38973f455aecf6e9aa42e26caf6401b8ff73
        Stored in directory: C:\Users\asus\AppData\Local\Temp\pip-ephem-wheel-cache-jln61mau\wheels\04\e1\c7\c1412d5d7f81883bb81eae0564c515fe9f0fd270dc1a1276c1
        DEPRECATION: Building 'srt' using the legacy setup.py bdist_wheel mechanism, which will be removed in a future version. pip 25.3 will enforce this behaviour change. A possible replacement is to use the standardized build interface by setting the `--use-pep517` option, (possibly combined with `--no-build-isolation`), or adding a `pyproject.toml` file to the source tree of 'srt'. Discussion can be found at https://github.com/pypa/pip/issues/6334
        Building wheel for srt (setup.py): started
        Building wheel for srt (setup.py): finished with status 'done'
        Created wheel for srt: filename=srt-3.5.3-py3-none-any.whl size=22556 sha256=c63745520dafa76bfc11b09a68cc5017216e8930b3e31136c8b4a317f8c14f51
        Stored in directory: c:\users\asus\appdata\local\pip\cache\wheels\1f\43\f1\23ee9119497fcb57d9f7046fbf34c6d9027c46a1fa7824cf08
      Successfully built hoichoi-drishti-api srt
      Installing collected packages: srt, sqlmodel, hoichoi-drishti-api
      
      Successfully installed hoichoi-drishti-api-0.1.0 sqlmodel-0.0.47 srt-3.5.3
      
      [notice] A new release of pip is available: 25.2 -> 26.2.1
      [notice] To update, run: python.exe -m pip install --upgrade pip

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'python -m compileall -q app pipeline; python -m pytest tests -q'
    status: Completed · exit 0
      ...                                                                      [100%]
      3 passed in 3.21s

## Assistant

The rebuilt backend imports and the original API tests pass. I’m strengthening verification now with an isolated temporary database, an actual generated MP4 through ingest/ffmpeg stages, the expected credential failure at Sarvam, and unit coverage for Bengali grapheme formatting and minimum-gap ad selection. This checks that uploads no longer receive demo data.

## Activity

    file changes: Completed · 1 changes
    Delete: C:\Users\asus\Desktop\hoichoi\backend\tests\test_api.py
    from fastapi.testclient import TestClient
    
    from app.main import app
    
    
    client = TestClient(app)
    
    
    def test_demo_episode_and_timeline_are_available():
        episodes = client.get("/episodes")
        assert episodes.status_code == 200
        assert episodes.json()[0]["status"] == "processed"
    
        timeline = client.get("/episodes/demo-episode-102/timeline")
        assert timeline.status_code == 200
        assert len(timeline.json()["scenes"]) == 6
    
    
    def test_ad_selection_respects_requested_count():
        response = client.get("/episodes/demo-episode-102/ads", params={"min_gap": 0, "n_breaks": 2, "blocked": "0,0"})
        assert response.status_code == 200
        assert sum(candidate["selected"] for candidate in response.json()) == 2
    
    
    def test_exports_and_schema():
        assert client.get("/schema").status_code == 200
        export = client.get("/episodes/demo-episode-102/export/ad_cuepoints.csv")
        assert export.status_code == 200
        assert "candidate_id" in export.text
    

## Activity

    file changes: Completed · 2 changes
    Add: C:\Users\asus\Desktop\hoichoi\backend\tests\test_api.py
    from __future__ import annotations
    
    import subprocess
    import time
    
    import pytest
    from fastapi.testclient import TestClient
    
    from app.main import create_app
    from app.settings import Settings
    
    
    @pytest.fixture()
    def client(tmp_path):
        application = create_app(Settings(data_dir=tmp_path, seed_demo=True, sarvam_api_key=None))
        with TestClient(application) as test_client:
            yield test_client
    
    
    def test_demo_episode_and_timeline_are_available(client: TestClient):
        episodes = client.get("/episodes")
        assert episodes.status_code == 200
        demo = next(episode for episode in episodes.json() if episode["id"] == "demo-episode-102")
        assert demo["status"] == "processed"
        assert len(demo["stages"]) == 18
    
        timeline = client.get("/episodes/demo-episode-102/timeline")
        assert timeline.status_code == 200
        assert len(timeline.json()["scenes"]) == 6
    
    
    def test_ad_selection_respects_requested_count(client: TestClient):
        response = client.get("/episodes/demo-episode-102/ads", params={"min_gap": 0, "n_breaks": 2, "blocked": "0,0"})
        assert response.status_code == 200
        assert sum(candidate["selected"] for candidate in response.json()) == 2
    
    
    def test_exports_schema_and_frame_path_safety(client: TestClient):
        assert client.get("/schema").status_code == 200
        export = client.get("/episodes/demo-episode-102/export/ad_cuepoints.csv")
        assert export.status_code == 200
        assert "candidate_id" in export.text
        assert client.get("/episodes/demo-episode-102/frames/missing.jpg").status_code == 404
    
    
    def test_real_upload_uses_pipeline_and_fails_actionably_without_sarvam(client: TestClient, tmp_path):
        source = tmp_path / "source.mp4"
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=blue:s=320x180:r=25",
            "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=16000", "-t", "2",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(source),
        ], check=True, capture_output=True)
    
        created = client.post("/episodes", json={"path": str(source), "title": "Pipeline fixture"})
        assert created.status_code == 201
        episode_id = created.json()["id"]
    
        deadline = time.time() + 25
        state = created.json()
        while state["status"] not in {"processed", "failed"} and time.time() < deadline:
            time.sleep(.2)
            state = client.get(f"/episodes/{episode_id}").json()
    
        assert state["status"] == "failed"
        assert state["progress"] > 0
        failed = next(stage for stage in state["stages"] if stage["status"] == "failed")
        assert failed["id"] == "s06_stt"
        assert "SARVAM_API_KEY" in failed["error"]
    
        timeline = client.get(f"/episodes/{episode_id}/timeline")
        assert timeline.status_code == 409
        assert timeline.json()["detail"]["stage"] == "s06_stt"
    
    Add: C:\Users\asus\Desktop\hoichoi\backend\tests\test_rules.py
    from app.settings import Thresholds
    from pipeline.scoring import score_candidate, select_candidates
    from pipeline.subtitles import format_utterances, grapheme_len, write_srt, write_vtt
    
    
    def test_bengali_formatter_uses_graphemes_and_emits_valid_formats():
        text = "আমি আজ কলকাতায় যাব কিন্তু সন্ধ্যার আগেই বাড়ি ফিরে আসব"
        cues = format_utterances([{
            "utt_id": "utt_1", "start": 0.0, "end": 6.0, "speaker": "SPK_A", "text": text,
        }], Thresholds())
        assert cues
        assert all(len(cue["lines"]) <= 2 for cue in cues)
        assert all(grapheme_len(line) <= 42 for cue in cues for line in cue["lines"])
        assert "-->" in write_srt(cues)
        assert write_vtt(cues).startswith("WEBVTT")
    
    
    def test_ad_score_and_selection_respect_minimum_gap():
        score = score_candidate(
            pause_len=2.5, scene_boundary=True, distance_to_end=0, intensity=.2,
            context_match=.8, speech=False, cliffhanger=False,
        )
        assert score["total"] > .8
        candidates = [
            {"time": 100.0, "score": {"total": .9}, "selected": False},
            {"time": 120.0, "score": {"total": .8}, "selected": False},
            {"time": 700.0, "score": {"total": .7}, "selected": False},
        ]
        selected = select_candidates(candidates, min_gap=480, count=2)
        assert [candidate["time"] for candidate in selected if candidate["selected"]] == [100.0, 700.0]
    

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'python -m pytest tests -q'
    status: Completed · exit 0
      ......                                                                   [100%]
      ============================== warnings summary ===============================
      tests/test_api.py::test_real_upload_uses_pipeline_and_fails_actionably_without_sarvam
        C:\Users\asus\Desktop\hoichoi\backend\pipeline\stages\core.py:97: DeprecationWarning: Image.Image.getdata is deprecated and will be removed in Pillow 14 (2027-10-15). Use get_flattened_data instead.
          pixels = list(image.convert("L").resize((9, 8)).getdata())
      
      -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
      6 passed, 1 warning in 6.02s

## Activity

    file changes: Completed · 1 changes
    Update { move_path: None }: C:\Users\asus\Desktop\hoichoi\backend\pipeline\stages\core.py
    @@ -96,3 +96,5 @@
         with Image.open(path) as image:
    -        pixels = list(image.convert("L").resize((9, 8)).getdata())
    +        resized = image.convert("L").resize((9, 8))
    +        flattened = getattr(resized, "get_flattened_data", resized.getdata)
    +        pixels = list(flattened())
         value = 0
    @@ -435,2 +437 @@
         return {"timeline": "outputs/semantic_timeline.json", "schema_version": "1.0"}
    -

## Activity

    web search: 

## Activity

    web search: site:developers.openai.com/api/docs/guides/images-vision Responses API input_image Python base64

## Activity

    web search: 

## Activity

    file changes: Completed · 4 changes
    Update { move_path: None }: C:\Users\asus\Desktop\hoichoi\backend\app\settings.py
    @@ -58,2 +58,6 @@
         @property
    +    def config_dir(self) -> Path:
    +        return PROJECT_ROOT / "backend" / "config"
    +
    +    @property
         def sqlite_url(self) -> str:
    @@ -64,2 +68 @@
             return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
    -
    Add: C:\Users\asus\Desktop\hoichoi\backend\config\ad_categories.yaml
    mobile:
      - smartphone
      - phone
      - mobile
      - earphones
      - charger
      - ফোন
      - মোবাইল
      - চার্জার
    food_delivery:
      - food
      - restaurant
      - biryani
      - pizza
      - order
      - hungry
      - খাবার
      - রেস্তোরাঁ
      - বিরিয়ানি
      - অর্ডার
    fashion:
      - saree
      - dress
      - clothes
      - shoes
      - jewellery
      - শাড়ি
      - জামা
      - পোশাক
    travel:
      - trip
      - vacation
      - flight
      - hotel
      - train
      - darjeeling
      - puri
      - ট্রেন
      - বিমান
      - হোটেল
    finance:
      - loan
      - bank
      - salary
      - money
      - insurance
      - upi
      - লোন
      - ব্যাঙ্ক
      - টাকা
    beauty:
      - makeup
      - cream
      - shampoo
      - skincare
      - মেকআপ
      - ক্রিম
      - শ্যাম্পু
    auto:
      - car
      - bike
      - scooter
      - গাড়ি
      - বাইক
      - স্কুটার
    
    Add: C:\Users\asus\Desktop\hoichoi\backend\config\sound_labels_bn.yaml
    Knock: {bn: "দরজায় কড়া নাড়ার শব্দ", cc_threshold: 0.35}
    Rain: {bn: "বৃষ্টির শব্দ", cc_threshold: 0.40}
    Thunder: {bn: "বজ্রপাত", cc_threshold: 0.35}
    Telephone bell ringing: {bn: "ফোন বেজে উঠছে", cc_threshold: 0.35}
    Ringtone: {bn: "ফোন বেজে উঠছে", cc_threshold: 0.35}
    Door: {bn: "দরজা খোলার শব্দ", cc_threshold: 0.40}
    Laughter: {bn: "হাসির শব্দ", cc_threshold: 0.45}
    Crying, sobbing: {bn: "কান্নার শব্দ", cc_threshold: 0.40}
    Crowd: {bn: "ভিড়ের কোলাহল", cc_threshold: 0.45}
    Vehicle horn, car horn, honking: {bn: "গাড়ির হর্ন", cc_threshold: 0.40}
    Gunshot, gunfire: {bn: "গুলির শব্দ", cc_threshold: 0.30}
    Footsteps: {bn: "পায়ের শব্দ", cc_threshold: 0.50}
    
    Update { move_path: None }: C:\Users\asus\Desktop\hoichoi\backend\pipeline\stages\core.py
    @@ -13,2 +13,3 @@
     
    +import yaml
     from app.artifacts import ArtifactStore
    @@ -245,11 +246,2 @@
         return {"scenes": scenes, "method": "shot_window_baseline", "llm_validated": False}
    -
    -
    -ENTITY_TERMS = {
    -    "mobile": [("smartphone", "ফোন", r"ফোন|মোবাইল|smartphone|mobile")],
    -    "food_delivery": [("biryani", "বিরিয়ানি", r"বিরিয়ানি|খাবার|অর্ডার|food|order")],
    -    "travel": [("train", "ট্রেন", r"ট্রেন|রেল|train|flight|বিমান|হোটেল")],
    -    "finance": [("money", "টাকা", r"টাকা|ব্যাঙ্ক|লোন|salary|money|bank|loan")],
    -    "fashion": [("clothing", "পোশাক", r"শাড়ি|জামা|পোশাক|dress|shoes")],
    -}
     
    @@ -259,15 +251,17 @@
         entities = []
    -    for category, terms in ENTITY_TERMS.items():
    -        for name, name_bn, pattern in terms:
    -            mentions = []
    -            for utterance in utterances:
    -                match = re.search(pattern, utterance["text"], re.IGNORECASE)
    +    category_path = ctx.settings.config_dir / "ad_categories.yaml"
    +    categories: dict[str, list[str]] = yaml.safe_load(category_path.read_text(encoding="utf-8"))
    +    for category, terms in categories.items():
    +        matches: dict[str, list[dict]] = {}
    +        for utterance in utterances:
    +            for term in sorted(terms, key=len, reverse=True):
    +                match = re.search(re.escape(term), utterance["text"], re.IGNORECASE)
                     if match:
    -                    mentions.append({"source": "dialogue", "time": utterance["start"], "utt_id": utterance["utt_id"], "shot_id": None, "surface": match.group(0)})
    -            if mentions:
    -                entities.append({
    -                    "entity_id": f"entity_{len(entities) + 1:04d}", "name": name, "name_bn": name_bn,
    -                    "kind": "product", "brand": None, "ad_categories": [category], "mentions": mentions,
    -                    "sentiment": "neutral", "presence": "unverified", "visual_check": None, "confidence": .72,
    -                })
    +                    matches.setdefault(term.casefold(), []).append({"source": "dialogue", "time": utterance["start"], "utt_id": utterance["utt_id"], "shot_id": None, "surface": match.group(0)})
    +        for term, mentions in matches.items():
    +            entities.append({
    +                "entity_id": f"entity_{len(entities) + 1:04d}", "name": term, "name_bn": term if re.search(r"[\u0980-\u09FF]", term) else None,
    +                "kind": "food" if category == "food_delivery" else "product", "brand": None, "ad_categories": [category], "mentions": mentions,
    +                "sentiment": "neutral", "presence": "unverified", "visual_check": None, "confidence": .72,
    +            })
         for scene in scenes:

## Activity

    file changes: Completed · 2 changes
    Update { move_path: None }: C:\Users\asus\Desktop\hoichoi\backend\pipeline\llm.py
    @@ -3,2 +3,3 @@
     import hashlib
    +import base64
     import json
    @@ -38,2 +39,4 @@
             max_retries: int = 2,
    +        images: list[Path] | None = None,
    +        image_detail: str = "low",
         ) -> SchemaT:
    @@ -46,3 +49,4 @@
     
    -        serialized = json.dumps({"model": model, "system": system, "user": user, "schema": schema.model_json_schema()}, ensure_ascii=False, sort_keys=True)
    +        image_hashes = [self.store.file_hash(path) for path in images or []]
    +        serialized = json.dumps({"model": model, "system": system, "user": user, "schema": schema.model_json_schema(), "images": image_hashes, "detail": image_detail}, ensure_ascii=False, sort_keys=True)
             key = hashlib.sha256(serialized.encode()).hexdigest()
    @@ -57,5 +61,14 @@
                 try:
    +                user_content: str | list[dict]
    +                if images:
    +                    user_content = [{"type": "input_text", "text": user}]
    +                    for path in images:
    +                        encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    +                        media_type = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    +                        user_content.append({"type": "input_image", "image_url": f"data:{media_type};base64,{encoded}", "detail": image_detail})
    +                else:
    +                    user_content = user
                     response = client.responses.parse(
                         model=model,
    -                    input=[{"role": "system", "content": system}, {"role": "user", "content": user}],
    +                    input=[{"role": "system", "content": system}, {"role": "user", "content": user_content}],
                         text_format=schema,
    @@ -85,2 +98 @@
                 handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    -
    Update { move_path: None }: C:\Users\asus\Desktop\hoichoi\backend\pipeline\stages\core.py
    @@ -14,2 +14,3 @@
     import yaml
    +from pydantic import BaseModel, Field
     from app.artifacts import ArtifactStore
    @@ -20,2 +21,3 @@
     from pipeline.media import detect_silences, probe, run
    +from pipeline.llm import StructuredLLM
     from pipeline.sarvam import SarvamClient
    @@ -215,3 +217,28 @@
         tags = {}
    +    llm = StructuredLLM(ctx.settings, ctx.store, ctx.episode_id)
    +    if llm.available():
    +        unique = [shot for shot in shots if shot["keyframe"]]
    +        for offset in range(0, len(unique), 4):
    +            batch = unique[offset:offset + 4]
    +            frame_paths = [ctx.root / shot["keyframe"] for shot in batch]
    +            response = llm.call(
    +                model=ctx.settings.llm_model_default,
    +                system="Analyze drama keyframes conservatively. Name only objects and brands clearly visible. Use short consistent English tags.",
    +                user="Return one item per image in this exact order and use these shot IDs: " + ", ".join(shot["shot_id"] for shot in batch),
    +                schema=VisualBatch,
    +                stage="s09_vision_baseline",
    +                images=frame_paths,
    +                image_detail="low",
    +            )
    +            by_id = {item.shot_id: item for item in response.items}
    +            for shot in batch:
    +                item = by_id.get(shot["shot_id"])
    +                if item:
    +                    tags[shot["shot_id"]] = item.model_dump(exclude={"shot_id"})
         for shot in shots:
    +        if shot["shot_id"] in tags:
    +            continue
    +        if shot["dup_of"] and shot["dup_of"] in tags:
    +            tags[shot["shot_id"]] = tags[shot["dup_of"]]
    +            continue
             tags[shot["shot_id"]] = {
    @@ -220,3 +247,3 @@
             }
    -    return {"visual_tags": tags, "provider": "conservative_fallback", "note": "Install provider extras and configure OPENAI_API_KEY for vision labels."}
    +    return {"visual_tags": tags, "provider": "openai" if llm.available() else "conservative_fallback", "note": None if llm.available() else "Install provider extras and configure OPENAI_API_KEY for vision labels."}
     

## Activity

    file changes: Completed · 1 changes
    Update { move_path: None }: C:\Users\asus\Desktop\hoichoi\backend\pipeline\stages\core.py
    @@ -214,2 +214,18 @@
     
    +class VisualItem(BaseModel):
    +    shot_id: str
    +    location: str
    +    indoor: bool | None
    +    objects: list[str]
    +    visible_brands: list[str]
    +    activity: str
    +    visual_mood: str
    +    people_count: int = Field(ge=0)
    +    confidence: float = Field(ge=0, le=1)
    +
    +
    +class VisualBatch(BaseModel):
    +    items: list[VisualItem]
    +
    +
     def s09_vision_baseline(ctx: StageContext) -> dict:

## Activity

    file changes: Completed · 1 changes
    Update { move_path: None }: C:\Users\asus\Desktop\hoichoi\backend\pipeline\stages\core.py
    @@ -311,2 +311,12 @@
             scene["entity_ids"] = [entity["entity_id"] for entity in entities if any(scene["start"] <= mention["time"] < scene["end"] for mention in entity["mentions"])]
    +        for brand in scene["visual"].get("visible_brands", []):
    +            entity = {
    +                "entity_id": f"entity_{len(entities) + 1:04d}", "name": brand, "name_bn": None,
    +                "kind": "brand", "brand": brand, "ad_categories": [],
    +                "mentions": [{"source": "visual", "time": scene["start"], "utt_id": None, "shot_id": scene["shot_ids"][0] if scene["shot_ids"] else None, "surface": brand}],
    +                "sentiment": "neutral", "presence": "shown_only", "visual_check": None,
    +                "confidence": scene["visual"].get("confidence", .5),
    +            }
    +            entities.append(entity)
    +            scene["entity_ids"].append(entity["entity_id"])
         return {"entities": entities, "scenes": scenes, "extractor": "grounded_keyword_baseline"}
    @@ -314,11 +324,58 @@
     
    +class PresenceCheck(BaseModel):
    +    visible: bool | None
    +    visible_frames: list[str]
    +    confidence: float = Field(ge=0, le=1)
    +    note: str
    +
    +
     def s12_vision_targeted(ctx: StageContext) -> dict:
         stage = ctx.stage("s11_entities_dialogue")
    +    shots = {shot["shot_id"]: shot for shot in ctx.stage("s03_keyframes")["shots"]}
    +    llm = StructuredLLM(ctx.settings, ctx.store, ctx.episode_id)
         entities = []
         for entity in stage["entities"]:
    -        entities.append({**entity, "presence": "unverified", "visual_check": {
    -            "frames_checked": [], "visible": None, "visible_frames": [], "confidence": 0.0,
    -            "note": "Targeted vision provider is not configured; no absence claim was made.",
    -        }})
    -    return {"entities": entities, "scenes": stage["scenes"], "provider": "conservative_fallback"}
    +        if entity["presence"] == "shown_only":
    +            entities.append(entity)
    +            continue
    +        mention_times = [mention["time"] for mention in entity["mentions"] if mention["source"] == "dialogue"]
    +        scene = next((scene for scene in stage["scenes"] if any(scene["start"] <= value < scene["end"] for value in mention_times)), None)
    +        frame_paths: list[Path] = []
    +        if scene:
    +            for shot_id in scene["shot_ids"]:
    +                shot = shots.get(shot_id)
    +                if not shot:
    +                    continue
    +                relative = shot["keyframe"] or (shots.get(shot["dup_of"] or "") or {}).get("keyframe")
    +                if relative and ctx.root / relative not in frame_paths:
    +                    frame_paths.append(ctx.root / relative)
    +            if len(frame_paths) > 10:
    +                step = (len(frame_paths) - 1) / 9
    +                frame_paths = [frame_paths[round(index * step)] for index in range(10)]
    +        if llm.available() and frame_paths:
    +            check = llm.call(
    +                model=ctx.settings.llm_model_default,
    +                system="Verify only the named entity. Do not infer it from dialogue or context. Visible means clearly present in at least one supplied frame.",
    +                user=f"Is {entity['name']} ({entity.get('brand') or 'no brand specified'}) visible? Refer to frames by filename.",
    +                schema=PresenceCheck,
    +                stage="s12_vision_targeted",
    +                images=frame_paths,
    +                image_detail="high",
    +            )
    +            if check.visible is True and check.confidence >= ctx.settings.thresholds.entity_visible_confidence:
    +                presence = "mentioned_and_shown"
    +            elif check.visible is False and check.confidence >= ctx.settings.thresholds.entity_absent_confidence and len(frame_paths) >= 6:
    +                presence = "mentioned_only"
    +            else:
    +                presence = "unverified"
    +            visual_check = {"frames_checked": [str(path.relative_to(ctx.root)) for path in frame_paths], **check.model_dump()}
    +        else:
    +            presence = "unverified"
    +            visual_check = {
    +                "frames_checked": [str(path.relative_to(ctx.root)) for path in frame_paths], "visible": None,
    +                "visible_frames": [], "confidence": 0.0,
    +                "note": "Targeted vision provider is not configured; no absence claim was made.",
    +            }
    +        entities.append({**entity, "presence": presence, "visual_check": visual_check})
    +    return {"entities": entities, "scenes": stage["scenes"], "provider": "openai" if llm.available() else "conservative_fallback"}
     

## Activity

    $ "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "rg -n \"def s11|class Presence|def s13\" backend\\pipeline\\stages\\core.py"
    status: Completed · exit 0
      292:def s11_entities_dialogue(ctx: StageContext) -> dict:
      325:class PresenceCheck(BaseModel):
      388:def s13_scene_semantics(ctx: StageContext) -> dict:

## Activity

    file changes: Completed · 1 changes
    Update { move_path: None }: C:\Users\asus\Desktop\hoichoi\backend\pipeline\stages\core.py
    @@ -291,2 +291,22 @@
     
    +class DraftMention(BaseModel):
    +    utt_id: str
    +    surface: str
    +
    +
    +class EntityDraft(BaseModel):
    +    name: str
    +    name_bn: str | None
    +    kind: str
    +    brand: str | None
    +    ad_categories: list[str]
    +    sentiment: str
    +    mentions: list[DraftMention]
    +    confidence: float = Field(ge=0, le=1)
    +
    +
    +class EntityDrafts(BaseModel):
    +    entities: list[EntityDraft]
    +
    +
     def s11_entities_dialogue(ctx: StageContext) -> dict:
    @@ -309,2 +329,45 @@
                 })
    +    llm = StructuredLLM(ctx.settings, ctx.store, ctx.episode_id)
    +    if llm.available():
    +        by_utterance = {utterance["utt_id"]: utterance for utterance in utterances}
    +        allowed_categories = sorted(categories)
    +        for scene in scenes:
    +            scene_utterances = [by_utterance[utt_id] for utt_id in scene["utt_ids"] if utt_id in by_utterance]
    +            if not scene_utterances:
    +                continue
    +            drafts = llm.call(
    +                model=ctx.settings.llm_model_default,
    +                system=(
    +                    "Extract grounded dialogue entities from Bengali or code-mixed speech. Every mention must cite an input utt_id. "
    +                    "Resolve implicit product references only within this scene. Do not invent brands. "
    +                    f"ad_categories must come from: {', '.join(allowed_categories)}."
    +                ),
    +                user="Scene utterances:\n" + "\n".join(f"{item['utt_id']} [{item['speaker']}]: {item['text']}" for item in scene_utterances),
    +                schema=EntityDrafts,
    +                stage="s11_entities_dialogue",
    +            )
    +            for draft in drafts.entities:
    +                grounded = [mention for mention in draft.mentions if mention.utt_id in by_utterance and mention.utt_id in scene["utt_ids"]]
    +                if not grounded:
    +                    continue
    +                key = (draft.name.casefold(), (draft.brand or "").casefold())
    +                existing = next((entity for entity in entities if (entity["name"].casefold(), (entity.get("brand") or "").casefold()) == key), None)
    +                normalized_mentions = [{
    +                    "source": "dialogue", "time": by_utterance[mention.utt_id]["start"], "utt_id": mention.utt_id,
    +                    "shot_id": None, "surface": mention.surface,
    +                } for mention in grounded]
    +                if existing:
    +                    known = {(mention["utt_id"], mention["surface"]) for mention in existing["mentions"]}
    +                    existing["mentions"].extend(mention for mention in normalized_mentions if (mention["utt_id"], mention["surface"]) not in known)
    +                    existing["ad_categories"] = sorted(set(existing["ad_categories"]) | (set(draft.ad_categories) & set(allowed_categories)))
    +                    existing["confidence"] = max(existing["confidence"], draft.confidence)
    +                else:
    +                    entities.append({
    +                        "entity_id": f"entity_{len(entities) + 1:04d}", "name": draft.name, "name_bn": draft.name_bn,
    +                        "kind": draft.kind if draft.kind in {"product", "brand", "place", "food", "activity", "topic", "other"} else "other",
    +                        "brand": draft.brand, "ad_categories": sorted(set(draft.ad_categories) & set(allowed_categories)),
    +                        "mentions": normalized_mentions,
    +                        "sentiment": draft.sentiment if draft.sentiment in {"positive", "neutral", "negative"} else "neutral",
    +                        "presence": "unverified", "visual_check": None, "confidence": draft.confidence,
    +                    })
         for scene in scenes:
    @@ -321,3 +384,3 @@
                 scene["entity_ids"].append(entity["entity_id"])
    -    return {"entities": entities, "scenes": scenes, "extractor": "grounded_keyword_baseline"}
    +    return {"entities": entities, "scenes": scenes, "extractor": "openai_grounded_plus_keywords" if llm.available() else "grounded_keyword_baseline"}
     

## Activity

    file changes: Completed · 1 changes
    Update { move_path: None }: C:\Users\asus\Desktop\hoichoi\backend\pipeline\stages\core.py
    @@ -450,4 +450,14 @@
     
    +class SemanticDraft(BaseModel):
    +    title: str
    +    summary: str
    +    topics: list[str]
    +    mood: str
    +    llm_intensity: float = Field(ge=0, le=1)
    +    is_cliffhanger: bool
    +
    +
     def s13_scene_semantics(ctx: StageContext) -> dict:
         scenes, utterances, audio = ctx.stage("s12_vision_targeted")["scenes"], ctx.stage("s07_transcript_clean")["utterances"], ctx.stage("s08_audio_events")
    +    llm = StructuredLLM(ctx.settings, ctx.store, ctx.episode_id)
         output = []
    @@ -459,10 +469,27 @@
             energy = _curve_mean(audio["loudness"], scene["start"], scene["end"])
    -        llm_intensity = min(1, .18 + dialogue_density * .62)
    +        fallback_intensity = min(1, .18 + dialogue_density * .62)
    +        if llm.available():
    +            draft = llm.call(
    +                model=ctx.settings.llm_model_scenes,
    +                system="Describe one drama scene from grounded evidence. Keep the title short, summary under two sentences, and judge narrative intensity rather than simple loudness.",
    +                user=(
    +                    f"Time: {scene['start']:.1f}-{scene['end']:.1f}\n"
    +                    f"Visual: {scene['visual']}\n"
    +                    "Dialogue:\n" + "\n".join(f"{item['speaker']}: {item['text']}" for item in scene_utterances)
    +                ),
    +                schema=SemanticDraft,
    +                stage="s13_scene_semantics",
    +            )
    +        else:
    +            draft = SemanticDraft(
    +                title=f"Scene {index + 1}", summary=(scene_utterances[0]["text"][:180] if scene_utterances else "No dialogue in this scene."),
    +                topics=[], mood="neutral", llm_intensity=fallback_intensity, is_cliffhanger=index == len(scenes) - 1,
    +            )
    +        llm_intensity = draft.llm_intensity
             intensity = .55 * llm_intensity + .25 * energy + .20 * dialogue_density
    -        first_text = scene_utterances[0]["text"] if scene_utterances else "No dialogue in this scene."
             semantic = {
    -            "title": f"Scene {index + 1}", "summary": first_text[:180], "topics": [], "mood": "neutral",
    +            "title": draft.title, "summary": draft.summary, "topics": draft.topics, "mood": draft.mood,
                 "narrative_intensity": round(intensity, 4),
                 "intensity_components": {"llm": round(llm_intensity, 4), "audio_energy": round(energy, 4), "dialogue_density": round(dialogue_density, 4)},
    -            "is_cliffhanger": index == len(scenes) - 1,
    +            "is_cliffhanger": draft.is_cliffhanger,
             }
    @@ -473,3 +500,3 @@
                 second += 1
    -    return {"scenes": output, "intensity": intensity_curve, "provider": "fused_deterministic_baseline"}
    +    return {"scenes": output, "intensity": intensity_curve, "provider": "openai_fused" if llm.available() else "fused_deterministic_baseline"}
     

## Assistant

Because uploads now produce their own artifacts asynchronously, I’m updating the small frontend integration assumption that previously expected a timeline immediately. The workspace will follow persistent stage state until assembly completes, and will surface the exact failed stage/error when credentials or processing fail.

## Activity

    file changes: Completed · 3 changes
    Update { move_path: None }: C:\Users\asus\Desktop\hoichoi\frontend\src\app\globals.css
    @@ -204,2 +204,3 @@
     .state-screen { min-height: 100vh; display: grid; place-content: center; justify-items: center; text-align: center; background: radial-gradient(circle at 50% 43%, #1b2434, var(--ink) 42%); }.state-screen h1 { margin: 23px 0 8px; font-size: 25px; }.state-screen p { color: var(--muted); max-width: 440px; line-height: 1.6; }.state-screen.error svg { color: var(--coral); }.state-screen .primary-button { margin-top: 14px; }
    +.loading-progress { width: min(360px, 70vw); height: 4px; margin-top: 16px; background: #242c39; overflow: hidden; }.loading-progress i { display: block; height: 100%; background: var(--mint); transition: width .35s ease; }
     
    Update { move_path: None }: C:\Users\asus\Desktop\hoichoi\frontend\src\components\Workspace.tsx
    @@ -29,5 +29,24 @@
       useEffect(() => {
    -    Promise.all([api.episode(episodeId), api.timeline(episodeId)])
    -      .then(([episodeResult, timelineResult]) => { setEpisode(episodeResult); setData(timelineResult); })
    -      .catch((reason: Error) => setError(reason.message));
    +    let cancelled = false;
    +    let timer: number | undefined;
    +    async function load() {
    +      try {
    +        const episodeResult = await api.episode(episodeId);
    +        if (cancelled) return;
    +        setEpisode(episodeResult);
    +        if (episodeResult.status === "processed") {
    +          const timelineResult = await api.timeline(episodeId);
    +          if (!cancelled) setData(timelineResult);
    +        } else if (episodeResult.status === "failed") {
    +          const failed = episodeResult.stages.find((stage) => stage.status === "failed");
    +          setError(failed ? `${failed.label}: ${failed.error ?? "Processing failed"}` : "Episode processing failed");
    +        } else {
    +          timer = window.setTimeout(load, 900);
    +        }
    +      } catch (reason) {
    +        if (!cancelled) setError(reason instanceof Error ? reason.message : "Episode request failed");
    +      }
    +    }
    +    load();
    +    return () => { cancelled = true; if (timer) window.clearTimeout(timer); };
       }, [episodeId]);
    @@ -52,3 +71,3 @@
       if (error) return <ErrorState message={error} />;
    -  if (!data || !episode || !currentScene) return <LoadingState />;
    +  if (!data || !episode || !currentScene) return <LoadingState episode={episode} />;
     
    @@ -236,4 +255,3 @@
     function ProcessingBar({ episode }: { episode: Episode }) { return <div className="processing-bar"><span className="signal-dot" /><strong>Processing episode</strong><div><i style={{ width: `${episode.progress}%` }} /></div><span>{episode.progress}%</span><small>{episode.stages.find((stage) => stage.status === "running")?.label ?? "Queued"}</small></div>; }
    -function LoadingState() { return <main className="state-screen"><span className="brand-glyph"><i /><i /><i /></span><h1>Building the semantic timeline</h1><p>Loading scenes, entities, captions, and ad candidates…</p></main>; }
    +function LoadingState({ episode }: { episode: Episode | null }) { const active = episode?.stages.find((stage) => stage.status === "running"); return <main className="state-screen"><span className="brand-glyph"><i /><i /><i /></span><h1>Building the semantic timeline</h1><p>{active ? `${active.label} is running. ${episode?.progress ?? 0}% complete.` : "Loading scenes, entities, captions, and ad candidates…"}</p>{episode && <div className="loading-progress"><i style={{ width: `${episode.progress}%` }} /></div>}</main>; }
     function ErrorState({ message }: { message: string }) { return <main className="state-screen error"><CircleAlert size={30} /><h1>The episode could not be opened</h1><p>{message}</p><Link href="/" className="primary-button"><ArrowLeft size={16} />Back to library</Link></main>; }
    -
    Update { move_path: None }: C:\Users\asus\Desktop\hoichoi\frontend\src\lib\api.ts
    @@ -8,3 +8,6 @@
         const detail = await response.json().catch(() => ({ detail: "Request failed" }));
    -    throw new Error(detail.detail ?? `Request failed (${response.status})`);
    +    const message = typeof detail.detail === "string"
    +      ? detail.detail
    +      : detail.detail?.error ?? detail.detail?.message ?? `Request failed (${response.status})`;
    +    throw new Error(message);
       }
    @@ -27,2 +30 @@
     };
    -

## Activity

    file changes: Completed · 4 changes
    Update { move_path: None }: C:\Users\asus\Desktop\hoichoi\README.md
    @@ -14,3 +14,3 @@
     cd backend
    -python -m pip install -e ".[dev]"
    +python -m pip install -e ".[dev,media]"
     python -m uvicorn app.main:app --reload --port 8000
    @@ -40,3 +40,14 @@
     
    -The upload path uses a short simulated stage runner and attaches the demo semantic data until real artifacts are written. GPU/media/ASR/LLM pipeline stages described in `docs/technical.md` require their respective models, credentials, and worker infrastructure; the web/API contracts are ready for those outputs.
    +Uploaded episodes run through a persistent, cached 18-stage pipeline. Install provider adapters and configure credentials for live Bengali diarization and multimodal understanding:
    +
    +```powershell
    +cd backend
    +python -m pip install -e ".[providers]"
    +Copy-Item .env.example .env
    +# Set SARVAM_API_KEY and OPENAI_API_KEY in .env
    +```
    +
    +Without `SARVAM_API_KEY`, a real upload stops at `s06_stt` with a retryable stage error; it never receives demo output. Stages before that point—including media probing, proxying, shot detection, keyframes, audio preparation, and VAD—remain cached. Add the key and call `POST /episodes/{id}/rerun` with `{"from_stage":"s06_stt","force":false}`.
    +
    +The bundled demo is seeded as a separate processed episode. Audio-event classification and optional GPU model upgrades described in `docs/technical.md` remain pluggable; the baseline records their provider status and avoids unsupported claims.
     
    @@ -51,2 +62 @@
     ```
    -
    Update { move_path: None }: C:\Users\asus\Desktop\hoichoi\backend\.env.example
    @@ -4,2 +4,3 @@
     DATA_DIR=../data
    +DATABASE_URL=
     REDIS_URL=redis://localhost:6379
    @@ -9,2 +10,3 @@
     DEVICE=cpu
    -
    +WORKER_CONCURRENCY=1
    +SEED_DEMO=true
    Add: C:\Users\asus\Desktop\hoichoi\backend\README.md
    # Drishti backend
    
    The FastAPI service owns persistent episode metadata in SQLite and immutable/cached artifacts under `DATA_DIR/episodes/{id}`.
    
    ## Processing
    
    `pipeline.runner.STAGES` defines the 18-stage DAG from the technical design. Every stage:
    
    1. hashes its version and dependency artifacts;
    2. skips a matching completed artifact;
    3. writes JSON atomically;
    4. persists running/done/failed state and elapsed time;
    5. stops the episode on a safe, retryable error.
    
    The local bounded worker is intentionally behind `PipelineCoordinator`; it can be replaced by RQ without changing the API or stage functions.
    
    ## Providers
    
    - Sarvam Saaras v4 batch mode supplies Bengali transcription, chunk timestamps, and diarization.
    - OpenAI Responses structured outputs supply grounded vision tags, entity extraction, targeted presence checks, and scene semantics when configured.
    - Missing vision/LLM credentials produce conservative unknown/unverified values. Missing Sarvam credentials fail `s06_stt` because a transcript cannot be honestly fabricated.
    
    ## Tests
    
    `python -m pytest tests -q` includes an actual generated MP4 through ffmpeg ingest and verifies the expected actionable provider failure.
    
    Update { move_path: None }: C:\Users\asus\Desktop\hoichoi\frontend\src\lib\types.ts
    @@ -5,2 +5,5 @@
       elapsed?: number;
    +  error?: string;
    +  started_at?: string;
    +  finished_at?: string;
     };
    @@ -144,2 +147 @@
     };
    -
