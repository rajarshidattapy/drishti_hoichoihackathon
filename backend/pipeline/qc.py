"""Subtitle QC rules (s17). Each rule is a pure function returning issue drafts."""
from __future__ import annotations

from typing import Callable

from app.settings import Thresholds
from pipeline.subtitles import grapheme_len

Issue = dict


def _issue(severity: str, rule: str, time: float, message: str, cue_idx: int | None = None, suggestion: str | None = None) -> Issue:
    return {"severity": severity, "rule": rule, "time": round(time, 3), "cue_idx": cue_idx, "message": message, "suggestion": suggestion}


def low_confidence(cues, utterances, speech, events, t: Thresholds, rejected: set[str]) -> list[Issue]:
    issues = []
    for u in utterances:
        if u["utt_id"] in rejected:
            issues.append(_issue("warn", "low_confidence", u["start"], "Transcript cleanup was rejected (edit distance too large); raw ASR text kept.", suggestion="Review the line against the audio."))
        elif u.get("confidence") is not None and u["confidence"] < t.qc_low_confidence:
            issues.append(_issue("warn", "low_confidence", u["start"], f"Speech recognition confidence is {u['confidence']:.2f}.", suggestion="Review against the source audio."))
    return issues


def reading_speed(cues, utterances, speech, events, t: Thresholds, rejected) -> list[Issue]:
    issues = []
    for cue in cues:
        if cue["kind"] != "dialogue":
            continue
        if cue["cps"] > t.qc_error_cps:
            issues.append(_issue("error", "reading_speed", cue["start"], f"Reading speed is {cue['cps']:.1f} cps.", cue["idx"], "Split the cue or condense the text."))
        elif cue["cps"] > t.subtitle_max_cps:
            issues.append(_issue("warn", "reading_speed", cue["start"], f"Reading speed is {cue['cps']:.1f} cps.", cue["idx"], "Extend into silence if possible."))
    return issues


def line_length(cues, utterances, speech, events, t: Thresholds, rejected) -> list[Issue]:
    return [
        _issue("warn", "line_length", cue["start"], f"A line has {max(grapheme_len(line) for line in cue['lines'])} graphemes (max {t.subtitle_max_line_graphemes}).", cue["idx"], "Rebalance the line break.")
        for cue in cues if any(grapheme_len(line) > t.subtitle_max_line_graphemes for line in cue["lines"])
    ]


def line_count(cues, utterances, speech, events, t: Thresholds, rejected) -> list[Issue]:
    return [
        _issue("error", "line_count", cue["start"], f"The cue has {len(cue['lines'])} lines.", cue["idx"], "Split the cue.")
        for cue in cues if len(cue["lines"]) > t.subtitle_max_lines
    ]


def overlap_speech(cues, utterances, speech, events, t: Thresholds, rejected) -> list[Issue]:
    overlapped = [u for u in utterances if u.get("overlap")]
    issues = []
    for cue in cues:
        if cue["kind"] == "dialogue" and any(u["start"] < cue["end"] and u["end"] > cue["start"] for u in overlapped):
            issues.append(_issue("warn", "overlap_speech", cue["start"], "Cue spans overlapping speech.", cue["idx"], "Confirm speaker turns manually."))
    return issues


def duration(cues, utterances, speech, events, t: Thresholds, rejected) -> list[Issue]:
    issues = []
    for cue in cues:
        length = cue["end"] - cue["start"]
        if length < t.subtitle_min_duration - 1e-6:
            issues.append(_issue("info", "duration", cue["start"], f"Cue is only {length:.2f} s long.", cue["idx"], "Extend to at least 1 s."))
        elif length > t.subtitle_max_duration + 1e-6:
            issues.append(_issue("warn", "duration", cue["start"], f"Cue is {length:.2f} s long.", cue["idx"], "Split the cue."))
    return issues


def timing_drift(cues, utterances, speech, events, t: Thresholds, rejected) -> list[Issue]:
    onsets = [segment["start"] for segment in speech]
    if not onsets:
        return []
    utterance_starts = {u["utt_id"]: u["start"] for u in utterances}
    issues = []
    for cue in cues:
        if cue["kind"] != "dialogue":
            continue
        # Only the first cue of an utterance should align with a speech onset.
        first_ids = [uid for uid in cue.get("utt_ids", []) if abs(utterance_starts.get(uid, -99) - cue["start"]) < .05]
        if not first_ids:
            continue
        drift = min(abs(cue["start"] - onset) for onset in onsets)
        if drift > t.qc_timing_drift_seconds:
            issues.append(_issue("warn", "timing_drift", cue["start"], f"Cue starts {drift:.2f} s from the nearest speech onset.", cue["idx"], "Re-sync the cue to the audio."))
    return issues


def speaker_ambiguous(cues, utterances, speech, events, t: Thresholds, rejected) -> list[Issue]:
    issues = []
    ordered = sorted(utterances, key=lambda u: u["start"])
    for index, u in enumerate(ordered):
        if u.get("speaker_confidence") is not None and u["speaker_confidence"] < .5:
            issues.append(_issue("info", "speaker_ambiguous", u["start"], "Low diarization confidence."))
            continue
        if 0 < index < len(ordered) - 1:
            before, after = ordered[index - 1], ordered[index + 1]
            if before["speaker"] == after["speaker"] != u["speaker"] and after["start"] - before["end"] <= t.qc_speaker_flip_seconds + (u["end"] - u["start"]) and u["end"] - u["start"] < t.qc_speaker_flip_seconds:
                issues.append(_issue("info", "speaker_ambiguous", u["start"], f"Speaker flips {before['speaker']}→{u['speaker']}→{after['speaker']} within {t.qc_speaker_flip_seconds:.0f} s.", suggestion="Check the speaker label."))
    return issues


def missing_speech(cues, utterances, speech, events, t: Thresholds, rejected) -> list[Issue]:
    dialogue = [cue for cue in cues if cue["kind"] == "dialogue"]
    issues = []
    for segment in speech:
        if segment["end"] - segment["start"] < t.qc_missing_speech_seconds:
            continue
        if not any(cue["start"] < segment["end"] and cue["end"] > segment["start"] for cue in dialogue):
            issues.append(_issue("warn", "missing_speech", segment["start"], f"{segment['end'] - segment['start']:.1f} s of detected speech has no subtitle.", suggestion="Check for untranscribed dialogue."))
    return issues


RULES: tuple[Callable[..., list[Issue]], ...] = (
    low_confidence, reading_speed, line_length, line_count, overlap_speech,
    duration, timing_drift, speaker_ambiguous, missing_speech,
)


def run_qc(cues: list[dict], utterances: list[dict], speech: list[dict], events: list[dict], thresholds: Thresholds, rejected: set[str] | None = None) -> tuple[list[Issue], dict]:
    issues: list[Issue] = []
    for rule in RULES:
        issues.extend(rule(cues, utterances, speech, events, thresholds, rejected or set()))
    issues.sort(key=lambda issue: (issue["time"], issue["rule"]))
    for index, issue in enumerate(issues):
        issue["issue_id"] = f"qc_{index + 1:05d}"
    summary: dict = {severity: sum(issue["severity"] == severity for issue in issues) for severity in ("error", "warn", "info")}
    summary["by_rule"] = {rule.__name__: sum(issue["rule"] == rule.__name__ for issue in issues) for rule in RULES}
    summary["passed"] = summary["error"] <= thresholds.qc_max_errors and summary["warn"] <= thresholds.qc_max_warnings
    return issues, summary
