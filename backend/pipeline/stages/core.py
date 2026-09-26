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

