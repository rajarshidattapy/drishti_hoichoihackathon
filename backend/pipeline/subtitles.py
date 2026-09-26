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
