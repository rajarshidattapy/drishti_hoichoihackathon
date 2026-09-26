// In-browser mock of the FastAPI backend. Enable with NEXT_PUBLIC_USE_MOCK=true.
import type {
  AdCandidate, AudioEvent, Entity, Episode, QCIssue, Scene, Stage, SubtitleCue, Timeline, Utterance,
} from "./types";

const STAGES: [string, string][] = [
  ["ingest", "Ingest & probe"],
  ["asr", "Speech recognition"],
  ["diarize", "Speaker diarization"],
  ["shots", "Shot & scene detection"],
  ["vision", "Visual understanding"],
  ["audio", "Audio events"],
  ["semantic", "Semantic layer"],
  ["ads", "Ad break scoring"],
  ["subs", "Subtitles & CC"],
  ["qc", "Quality checks"],
];

function doneStages(): Stage[] {
  return STAGES.map(([id, label], i) => ({ id, label, status: "done", elapsed: 2 + i * 1.7 }));
}

const SCENE_SEEDS: {
  title: string; summary: string; location: string; objects: string[]; activity: string;
  mood: string; topics: string[]; intensity: number; cliff: boolean; speakers: string[];
  lines: [string, string][]; events: string[];
}[] = [
  {
    title: "Morning at the Kolkata flat", summary: "Mitra makes tea while Anjali reads the newspaper; they discuss the missing heirloom.",
    location: "kitchen", objects: ["tea kettle", "newspaper", "window"], activity: "making tea", mood: "calm",
    topics: ["family", "breakfast"], intensity: 0.22, cliff: false, speakers: ["S1", "S2"],
    lines: [["S1", "চা হয়ে গেছে, খবরের কাগজটা রাখো।"], ["S2", "দিদিমার হারটা কোথাও পাচ্ছি না।"], ["S1", "আলমারিতে দেখেছ?"], ["S2", "সব জায়গায় দেখেছি।"]],
    events: ["kettle whistle"],
  },
  {
    title: "The locked almirah", summary: "Anjali finds the almirah lock broken and suspects someone in the house.",
    location: "bedroom", objects: ["almirah", "broken lock", "jewellery box"], activity: "searching", mood: "tense",
    topics: ["theft", "suspicion"], intensity: 0.58, cliff: false, speakers: ["S2", "S1"],
    lines: [["S2", "তালাটা ভাঙা! কেউ খুলেছে।"], ["S1", "শান্ত হও, পুলিশে খবর দিই?"], ["S2", "না, আগে বাড়ির লোকদের জিজ্ঞেস করি।"]],
    events: ["door creak"],
  },
  {
    title: "Market detour", summary: "Mitra buys fish at Gariahat market and overhears a jeweller talking about an old necklace.",
    location: "market", objects: ["fish stall", "shopping bag", "scooter"], activity: "shopping", mood: "lively",
    topics: ["market", "food", "clue"], intensity: 0.35, cliff: false, speakers: ["S1", "S3"],
    lines: [["S3", "দাদা, আজ ইলিশ খুব ভালো এসেছে।"], ["S1", "দুটো দিন। আর দাম একটু কমান।"], ["S3", "পাশের দোকানে একটা পুরনো হার বিক্রি হয়েছে শুনলাম।"]],
    events: ["crowd chatter", "scooter horn"],
  },
  {
    title: "Family lunch", summary: "Over lunch, the family bickers; cousin Rono avoids eye contact.",
    location: "dining room", objects: ["rice", "fish curry", "phone"], activity: "eating", mood: "awkward",
    topics: ["family", "food"], intensity: 0.3, cliff: false, speakers: ["S2", "S4", "S1"],
    lines: [["S4", "মাছটা দারুণ হয়েছে।"], ["S2", "রনো, কাল রাতে কোথায় ছিলি?"], ["S4", "বন্ধুর বাড়িতে। কেন?"], ["S1", "থাক, খাওয়ার সময় এসব নয়।"]],
    events: ["cutlery"],
  },
  {
    title: "The jeweller's shop", summary: "Mitra visits the jeweller and recognises the family necklace in the display.",
    location: "jewellery shop", objects: ["necklace", "display case", "receipt"], activity: "questioning", mood: "suspenseful",
    topics: ["clue", "jewellery"], intensity: 0.66, cliff: false, speakers: ["S1", "S5"],
    lines: [["S1", "এই হারটা কোথা থেকে এল?"], ["S5", "গত সপ্তাহে এক ছেলে বিক্রি করে গেছে।"], ["S1", "রসিদটা দেখাতে পারবেন?"]],
    events: ["shop bell"],
  },
  {
    title: "Quiet evening walk", summary: "Mitra walks along the Ganges ghat, thinking it over as the sun sets.",
    location: "river ghat", objects: ["boats", "lamps", "river"], activity: "walking", mood: "reflective",
    topics: ["reflection"], intensity: 0.18, cliff: false, speakers: ["S1"],
    lines: [["S1", "রনো কি সত্যিই এটা করতে পারে?"], ["S1", "নাকি কেউ ওকে ফাঁসাচ্ছে?"]],
    events: ["temple bells", "background music"],
  },
  {
    title: "Confrontation", summary: "Mitra confronts Rono with the receipt; Rono breaks down.",
    location: "living room", objects: ["receipt", "sofa", "photo frame"], activity: "arguing", mood: "dramatic",
    topics: ["confrontation", "family"], intensity: 0.86, cliff: false, speakers: ["S1", "S4", "S2"],
    lines: [["S1", "এই রসিদে তোর সই কেন?"], ["S4", "আমি… আমার টাকার দরকার ছিল।"], ["S2", "তুই দিদিমার হার বিক্রি করলি?"], ["S4", "আমাকে ক্ষমা করো।"]],
    events: ["crying", "tense music"],
  },
  {
    title: "A knock at midnight", summary: "Someone knocks at the door at midnight — it is the jeweller, with a warning.",
    location: "front door", objects: ["door", "torch"], activity: "answering door", mood: "ominous",
    topics: ["mystery"], intensity: 0.92, cliff: true, speakers: ["S5", "S1"],
    lines: [["S5", "হারটা আসল নয়। আসলটা এখনও কারও কাছে আছে।"], ["S1", "মানে?"]],
    events: ["door knock", "thunder"],
  },
];

const SPEAKER_NAMES: Record<string, string> = { S1: "Mitra", S2: "Anjali", S3: "Fish seller", S4: "Rono", S5: "Jeweller" };
const SCENE_LEN = 180;

function round(value: number, digits = 2) { const f = 10 ** digits; return Math.round(value * f) / f; }

function buildTimeline(id: string, title: string): Timeline {
  const duration = SCENE_SEEDS.length * SCENE_LEN;
  const scenes: Scene[] = [];
  const utterances: Utterance[] = [];
  const audioEvents: AudioEvent[] = [];
  const subtitleCues: SubtitleCue[] = [];
  const ccCues: SubtitleCue[] = [];

  SCENE_SEEDS.forEach((seed, s) => {
    const start = s * SCENE_LEN;
    const sceneId = `sc_${String(s + 1).padStart(3, "0")}`;
    const uttIds: string[] = [];
    seed.lines.forEach(([speaker, text], i) => {
      const uStart = start + 8 + i * 22;
      const uEnd = uStart + 3.5 + text.length / 12;
      const utt_id = `u_${String(utterances.length + 1).padStart(4, "0")}`;
      uttIds.push(utt_id);
      utterances.push({ utt_id, start: uStart, end: round(uEnd), speaker, speaker_name: SPEAKER_NAMES[speaker], text, confidence: round(0.82 + ((s + i) % 5) * 0.03) });
      const cps = round(text.length / (uEnd - uStart), 1);
      subtitleCues.push({ idx: subtitleCues.length + 1, start: uStart, end: round(uEnd), lines: [text], speakers: [speaker], kind: "dialogue", cps });
      ccCues.push({ idx: ccCues.length + 1, start: uStart, end: round(uEnd), lines: [`[${SPEAKER_NAMES[speaker]}] ${text}`], speakers: [speaker], kind: "dialogue", cps });
    });
    seed.events.forEach((label, i) => {
      const eStart = start + 120 + i * 20;
      audioEvents.push({ event_id: `ae_${audioEvents.length + 1}`, label, label_bn: `[${label}]`, start: eStart, end: eStart + 4, score: round(0.7 + i * 0.1), in_cc: true });
      ccCues.push({ idx: ccCues.length + 1, start: eStart, end: eStart + 4, lines: [`[${label}]`], speakers: [], kind: "sound", cps: 0 });
    });
    scenes.push({
      scene_id: sceneId, start, end: start + SCENE_LEN,
      visual: { location: seed.location, objects: seed.objects, activity: seed.activity, visual_mood: seed.mood, people_count: seed.speakers.length, confidence: 0.88 },
      speakers: seed.speakers, utt_ids: uttIds, audio_events: seed.events,
      music_ratio: seed.events.some((e) => e.includes("music")) ? 0.45 : 0.1,
      semantic: {
        title: seed.title, summary: seed.summary, topics: seed.topics, mood: seed.mood,
        narrative_intensity: seed.intensity,
        intensity_components: { dialogue: round(seed.intensity * 0.9), music: round(seed.intensity * 0.7), motion: round(seed.intensity * 0.5) },
        is_cliffhanger: seed.cliff,
      },
      entity_ids: [],
    });
  });

  ccCues.sort((a, b) => a.start - b.start).forEach((cue, i) => { cue.idx = i + 1; });

  const entities: Entity[] = [
    { entity_id: "e_tea", name: "Tea", name_bn: "চা", kind: "beverage", brand: "Wagh Bakri", ad_categories: ["beverages", "fmcg"], mentions: [{ source: "asr", time: 8, surface: "চা" }], sentiment: "positive", presence: "mentioned_and_shown", confidence: 0.91, visual_check: { frames_checked: ["f_0010", "f_0012"], visible: true, visible_frames: ["f_0010"], confidence: 0.87, note: "Kettle and cups clearly visible" } },
    { entity_id: "e_hilsa", name: "Hilsa fish", name_bn: "ইলিশ", kind: "food", ad_categories: ["food", "grocery delivery"], mentions: [{ source: "asr", time: 368, surface: "ইলিশ" }], sentiment: "positive", presence: "mentioned_and_shown", confidence: 0.89 },
    { entity_id: "e_scooter", name: "Scooter", kind: "vehicle", brand: "Honda", ad_categories: ["automotive"], mentions: [{ source: "vision", time: 400, surface: "scooter" }], sentiment: "neutral", presence: "shown_only", confidence: 0.72 },
    { entity_id: "e_necklace", name: "Gold necklace", name_bn: "হার", kind: "jewellery", ad_categories: ["jewellery", "luxury"], mentions: [{ source: "asr", time: 30, surface: "হার" }, { source: "asr", time: 728, surface: "হারটা" }], sentiment: "negative", presence: "mentioned_and_shown", confidence: 0.94 },
    { entity_id: "e_phone", name: "Smartphone", kind: "electronics", ad_categories: ["telecom", "electronics"], mentions: [{ source: "vision", time: 560, surface: "phone" }], sentiment: "neutral", presence: "unverified", confidence: 0.48 },
  ];
  const entityScene: Record<string, number> = { e_tea: 0, e_hilsa: 2, e_scooter: 2, e_necklace: 4, e_phone: 3 };
  entities.forEach((entity) => scenes[entityScene[entity.entity_id]].entity_ids.push(entity.entity_id));

  const adCandidates: AdCandidate[] = scenes.slice(0, -1).map((scene, i) => {
    const next = scenes[i + 1];
    const low = round(1 - scene.semantic.narrative_intensity);
    const cliff = next.semantic.narrative_intensity > 0.8 ? 0.2 : 0;
    const categories = scene.entity_ids.flatMap((eid) => entities.find((e) => e.entity_id === eid)?.ad_categories ?? []);
    const total = round(0.25 + low * 0.4 + (categories.length ? 0.15 : 0) - cliff);
    return {
      cand_id: `ad_${i + 1}`, time: scene.end, scene_id: scene.scene_id, kind: "scene_boundary",
      pause_len: round(1.2 + (i % 3) * 0.6, 1),
      score: { pause: 0.8, scene_end: 1, low_intensity: low, context_match: categories.length ? 0.7 : 0.2, speech_penalty: 0, cliffhanger_penalty: cliff, total },
      disruption: total > 0.6 ? "low" : total > 0.4 ? "medium" : "high",
      matched_categories: categories,
      reason: `Scene "${scene.semantic.title}" ends on a ${scene.semantic.mood} beat${categories.length ? `; context fits ${categories.slice(0, 2).join(", ")}` : ""}.`,
      selected: false,
    };
  });
  [...adCandidates].sort((a, b) => b.score.total - a.score.total).slice(0, 3).forEach((ad) => { ad.selected = true; });

  const qc: QCIssue[] = [
    { issue_id: "qc_1", severity: "warn", rule: "reading_speed", time: subtitleCues[5].start, cue_idx: 6, message: "Reading speed above 17 cps.", suggestion: "Split into two cues or shorten the line." },
    { issue_id: "qc_2", severity: "info", rule: "speaker_label", time: utterances[10].start, message: "Low diarization confidence on speaker change." },
    { issue_id: "qc_3", severity: "error", rule: "cc_missing_sound", time: 1450, message: "Loud audio event not captioned.", suggestion: "Add [thunder] cue." },
  ];

  const intensity: [number, number][] = [];
  const loudness: [number, number][] = [];
  for (let t = 0; t <= duration; t += 10) {
    const scene = scenes[Math.min(scenes.length - 1, Math.floor(t / SCENE_LEN))];
    const wobble = Math.sin(t / 23) * 0.06;
    intensity.push([t, round(Math.max(0, Math.min(1, scene.semantic.narrative_intensity + wobble)))]);
    loudness.push([t, round(-28 + scene.semantic.narrative_intensity * 14 + Math.cos(t / 17) * 2, 1)]);
  }

  return {
    schema_version: "1.0",
    episode: { id, title, duration, video_available: false },
    scenes, utterances, audio_events: audioEvents, entities, ad_candidates: adCandidates,
    subtitles: { language: "bn", cue_count: subtitleCues.length, cc_cue_count: ccCues.length },
    subtitle_cues: subtitleCues, cc_cues: ccCues, qc,
    curves: { intensity, loudness },
    processing: { total_seconds: 184.2, llm_cost_usd: 0.42, models: ["mock-asr", "mock-vision", "mock-llm"], cached_stages: 0 },
  };
}

type MockRecord = { episode: Episode; timeline?: Timeline; startedAt?: number };

const store = new Map<string, MockRecord>();

function seed() {
  if (store.size) return;
  const demos: [string, string, string][] = [
    ["ep_mitra_s01e01", "Mitra Investigates · S01E01 — The Missing Heirloom", "2026-09-20T10:30:00Z"],
    ["ep_mitra_s01e02", "Mitra Investigates · S01E02 — Midnight Visitor", "2026-09-22T14:05:00Z"],
  ];
  for (const [id, title, created_at] of demos) {
    const timeline = buildTimeline(id, title);
    store.set(id, {
      timeline,
      episode: { id, title, duration: timeline.episode.duration, status: "processed", progress: 100, created_at, video_available: false, stages: doneStages() },
    });
  }
}

// Simulated processing time for uploaded episodes.
const PROCESS_MS = 8000;

function advance(record: MockRecord) {
  if (record.episode.status === "processed" || record.startedAt === undefined) return;
  const fraction = Math.min(1, (Date.now() - record.startedAt) / PROCESS_MS);
  const doneCount = Math.floor(fraction * STAGES.length);
  record.episode.progress = Math.round(fraction * 100);
  record.episode.status = fraction >= 1 ? "processed" : "processing";
  record.episode.stages = STAGES.map(([id, label], i) => ({
    id, label,
    status: i < doneCount ? "done" : i === doneCount && fraction < 1 ? "running" : fraction >= 1 ? "done" : "queued",
    elapsed: i < doneCount ? round((PROCESS_MS / 1000 / STAGES.length), 1) : undefined,
  }));
  if (fraction >= 1) {
    record.episode.duration = SCENE_SEEDS.length * SCENE_LEN;
    record.timeline = buildTimeline(record.episode.id, record.episode.title);
  }
}

function clone<T>(value: T): T { return structuredClone(value); }
function delay<T>(value: T, ms = 250): Promise<T> { return new Promise((resolve) => setTimeout(() => resolve(clone(value)), ms)); }

function get(id: string): MockRecord {
  seed();
  const record = store.get(id);
  if (!record) throw new Error(`Episode ${id} not found`);
  advance(record);
  return record;
}

export const mockApi = {
  episodes: async () => {
    seed();
    store.forEach(advance);
    return delay([...store.values()].map((r) => r.episode).sort((a, b) => b.created_at.localeCompare(a.created_at)));
  },
  episode: async (id: string) => delay(get(id).episode),
  timeline: async (id: string) => {
    const record = get(id);
    if (!record.timeline) throw new Error("Episode is still processing");
    return delay(record.timeline, 400);
  },
  ads: async (id: string, minGap: number, count: number) => {
    const timeline = get(id).timeline;
    if (!timeline) throw new Error("Episode is still processing");
    const picked: AdCandidate[] = [];
    for (const ad of [...timeline.ad_candidates].sort((a, b) => b.score.total - a.score.total)) {
      if (picked.length >= count) break;
      if (picked.every((p) => Math.abs(p.time - ad.time) >= minGap)) picked.push(ad);
    }
    timeline.ad_candidates.forEach((ad) => { ad.selected = picked.includes(ad); });
    return delay(timeline.ad_candidates);
  },
  selectAd: async (id: string, candidateId: string, selected: boolean) => {
    const ad = get(id).timeline?.ad_candidates.find((c) => c.cand_id === candidateId);
    if (!ad) throw new Error(`Ad candidate ${candidateId} not found`);
    ad.selected = selected;
    return delay(ad, 120);
  },
  upload: async (form: FormData) => {
    seed();
    const file = form.get("file");
    const name = file instanceof File ? file.name.replace(/\.[^.]+$/, "") : "Untitled episode";
    const id = `ep_mock_${Date.now().toString(36)}`;
    const record: MockRecord = {
      startedAt: Date.now(),
      episode: {
        id, title: name, duration: 0, status: "queued", progress: 0, created_at: new Date().toISOString(), video_available: false,
        stages: STAGES.map(([sid, label]) => ({ id: sid, label, status: "queued" })),
      },
    };
    store.set(id, record);
    return delay(record.episode, 600);
  },
};
