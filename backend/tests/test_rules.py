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

