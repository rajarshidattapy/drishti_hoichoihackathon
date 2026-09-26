"""Deterministic Bengali subtitle formatter (s15). No LLM in the loop."""
from __future__ import annotations

import re as std_re
from datetime import timedelta

import regex
import srt

from app.settings import Thresholds


def graphemes(text: str) -> list[str]:
    return regex.findall(r"\X", text)


def grapheme_len(text: str) -> int:
    return len(graphemes(text))


def split_text(text: str, max_chars: int) -> list[str]:
    """Split at sentence ends, then commas/conjunctions, then the word nearest the midpoint."""
    text = text.strip()
    if grapheme_len(text) <= max_chars:
        return [text]
    for pattern in (r"(?<=[।?!])\s+", r"(?<=[,;])\s+|\s+(?=(?:এবং|কিন্তু|তাই|আর)\s)"):
        phrases = [part.strip() for part in regex.split(pattern, text) if part.strip()]
        if len(phrases) > 1:
            break
    else:
        words = text.split()
        if len(words) < 2:
            return [text]
        total = grapheme_len(text)
        running, midpoint = 0, 1
        for index, word in enumerate(words[:-1]):
            running += grapheme_len(word) + 1
            if running >= total / 2:
                midpoint = index + 1
                break
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
    # Any piece still too long is split again at its midpoint.
    result: list[str] = []
    for piece in output:
        result.extend(split_text(piece, max_chars) if grapheme_len(piece) > max_chars and piece != text else [piece])
    return result


def balance_lines(text: str, max_line: int) -> list[str]:
    """Two balanced lines, preferring a bottom-heavy pyramid; never break after a single short word."""
    words = text.split()
    if grapheme_len(text) <= max_line or len(words) < 2:
        return [text]
    best: tuple[float, list[str]] | None = None
    for index in range(1, len(words)):
        first, second = " ".join(words[:index]), " ".join(words[index:])
        a, b = grapheme_len(first), grapheme_len(second)
        if a > max_line or b > max_line:
            continue
        score = abs(a - b) + (5 if a > b else 0) + (20 if index == 1 and a <= 3 else 0)
        if best is None or score < best[0]:
            best = (score, [first, second])
    return best[1] if best else [text]


def _part_times(utterance: dict, parts: list[str]) -> list[tuple[float, float]]:
    start, end = float(utterance["start"]), float(utterance["end"])
    words = utterance.get("words") or []
    if words and len(parts) > 1:
        # Cut at word boundaries by matching each part's word count.
        times, cursor = [], 0
        for part in parts:
            count = len(part.split())
            chunk = words[cursor:cursor + count] or words[-1:]
            times.append((float(chunk[0]["start"]), float(chunk[-1]["end"])))
            cursor += count
        return times
    total = max(1, sum(grapheme_len(part) for part in parts))
    times, cursor = [], start
    for part in parts:
        share = (end - start) * grapheme_len(part) / total
        times.append((cursor, cursor + share))
        cursor += share
    return times


def _merge_short_exchanges(utterances: list[dict], thresholds: Thresholds) -> list[dict]:
    """Pair quick back-and-forth lines from different speakers into one dash-prefixed cue."""
    output: list[dict] = []
    index = 0
    while index < len(utterances):
        current = utterances[index]
        following = utterances[index + 1] if index + 1 < len(utterances) else None
        if (
            following is not None
            and following["speaker"] != current["speaker"]
            and following["start"] - current["end"] <= .5
            and following["end"] - current["start"] <= thresholds.subtitle_max_duration
            and grapheme_len(current["text"]) + 2 <= thresholds.subtitle_max_line_graphemes
            and grapheme_len(following["text"]) + 2 <= thresholds.subtitle_max_line_graphemes
            and current["end"] - current["start"] < thresholds.subtitle_min_duration * 1.5
        ):
            output.append({
                "utt_ids": [current["utt_id"], following["utt_id"]], "start": current["start"], "end": following["end"],
                "speakers": [current["speaker"], following["speaker"]],
                "lines": [f"- {current['text']}", f"- {following['text']}"],
            })
            index += 2
            continue
        output.append({**current, "utt_ids": [current["utt_id"]], "speakers": [current["speaker"]]})
        index += 1
    return output


def format_utterances(utterances: list[dict], thresholds: Thresholds) -> list[dict]:
    cleaned = []
    for utterance in sorted(utterances, key=lambda item: item["start"]):
        text = std_re.sub(r"\s+", " ", utterance.get("text", "")).strip()
        if text:
            cleaned.append({**utterance, "text": text, "utt_id": utterance.get("utt_id", f"utt_{len(cleaned) + 1}")})
    units = _merge_short_exchanges(cleaned, thresholds)
    max_cue = thresholds.subtitle_max_line_graphemes * thresholds.subtitle_max_lines

    raw: list[dict] = []
    for unit_index, unit in enumerate(units):
        next_start = units[unit_index + 1]["start"] if unit_index + 1 < len(units) else float("inf")
        if "lines" in unit:
            raw.append({"start": unit["start"], "end": unit["end"], "lines": unit["lines"], "speakers": unit["speakers"], "utt_ids": unit["utt_ids"], "limit": next_start})
            continue
        parts = split_text(unit["text"], max_cue)
        for part, (start, end) in zip(parts, _part_times(unit, parts)):
            needed = grapheme_len(part) / thresholds.subtitle_max_cps
            # Extend into available silence first; split only if still too fast.
            if end - start < needed:
                end = min(start + needed, end + thresholds.subtitle_cps_extension, next_start - thresholds.subtitle_min_gap)
            if (end - start) > 0 and grapheme_len(part) / (end - start) > thresholds.subtitle_max_cps and len(part.split()) > 3:
                halves = split_text(part, max(1, grapheme_len(part) // 2 + 1))
                if len(halves) > 1:
                    pieces = _part_times({"start": start, "end": end}, halves)
                    for half, (half_start, half_end) in zip(halves, pieces):
                        raw.append({"start": half_start, "end": half_end, "text": half, "speakers": unit["speakers"], "utt_ids": unit["utt_ids"], "limit": next_start})
                    continue
            raw.append({"start": start, "end": end, "text": part, "speakers": unit["speakers"], "utt_ids": unit["utt_ids"], "limit": next_start})

    cues: list[dict] = []
    for item in raw:
        start, end = float(item["start"]), float(item["end"])
        if end - start < thresholds.subtitle_min_duration:
            end = start + thresholds.subtitle_min_duration
        end = min(end, start + thresholds.subtitle_max_duration)
        if cues and start < cues[-1]["end"] + thresholds.subtitle_min_gap:
            trimmed = start - thresholds.subtitle_min_gap
            if trimmed - cues[-1]["start"] >= thresholds.subtitle_min_duration:
                cues[-1]["end"] = round(trimmed, 3)
            else:
                shift = cues[-1]["end"] + thresholds.subtitle_min_gap - start
                start, end = start + shift, end + shift
        lines = item.get("lines") or balance_lines(item["text"], thresholds.subtitle_max_line_graphemes)
        text_len = sum(grapheme_len(line) for line in lines)
        cues.append({
            "idx": len(cues) + 1, "start": round(start, 3), "end": round(end, 3), "lines": lines,
            "speakers": item["speakers"], "utt_ids": item["utt_ids"], "kind": "dialogue", "cps": 0.0,
            "_len": text_len,
        })
    for cue in cues:
        cue["cps"] = round(cue.pop("_len") / max(.01, cue["end"] - cue["start"]), 2)
    return cues


def write_srt(cues: list[dict]) -> str:
    subtitles = [srt.Subtitle(index=cue["idx"], start=timedelta(seconds=cue["start"]), end=timedelta(seconds=cue["end"]), content="\n".join(cue["lines"])) for cue in cues]
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
