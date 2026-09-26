from app.settings import Thresholds
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

