from app.settings import Settings, Thresholds
from pipeline.ads import decide, generate_candidates, load_catalogue, phrase_in, pick_creative, rank_brands, tokens
from pipeline.vmap import build_vmap

T = Thresholds()
CATALOGUE = [
    {"brand_id": "food", "name": "Food Co", "category": "food_delivery", "preferred_contexts": ["dinner", "biryani"], "negative_contexts": ["funeral"], "creatives": [{"id": "food_15", "duration": 15, "language": "bn", "url": None}, {"id": "food_30", "duration": 30, "language": "bn", "url": None}]},
    {"brand_id": "phone", "name": "Phone Co", "category": "mobile", "preferred_contexts": ["phone"], "negative_contexts": ["theft"], "creatives": [{"id": "phone_15", "duration": 15, "language": "bn", "url": None}, {"id": "phone_30", "duration": 30, "language": "bn", "url": None}]},
]


def candidate(cand_id, time, safety, *, before=(), after=(), categories=(), rejections=()):
    return {
        "cand_id": cand_id, "time": time, "scene_id": "s", "kind": "scene_boundary", "pause_len": 2.0,
        "score": {"pause": .8, "scene_end": 1, "low_intensity": .8, "context_match": 0, "speech_penalty": 0, "cliffhanger_penalty": 0, "total": safety},
        "disruption": "low", "matched_categories": [], "context_entity_ids": [], "scene_title": "Scene", "reason": "",
        "context": {"before": tokens(" ".join(before)), "after": tokens(" ".join(after)), "categories": list(categories)},
        "hard_rejections": list(rejections), "selected": False,
    }


def run(candidates, **overrides):
    settings = {"duration": 3000, "min_gap": 480, "n_breaks": 3, "blocked": (120, 120), "min_safety": .45, **overrides}
    decided, summary = decide(candidates, CATALOGUE, **settings)
    return {c["cand_id"]: c for c in decided}, summary


def test_hierarchy_hard_constraints_then_safety_then_pacing():
    by_id, summary = run([
        candidate("speech", 600, .95, rejections=["speech_at_cut"]),
        candidate("blocked", 60, .9),
        candidate("unsafe", 900, .3),
        candidate("best", 1200, .9, before=["dinner"]),
        candidate("too_close", 1300, .85, before=["dinner"]),
        candidate("second", 2000, .7, before=["phone"]),
    ], n_breaks=2)
    assert by_id["speech"]["rejections"] == ["speech_at_cut"] and not by_id["speech"]["selected"]
    assert by_id["blocked"]["rejections"] == ["blocked_zone"]
    assert by_id["unsafe"]["rejections"] == ["below_safety_floor"]
    assert by_id["too_close"]["eligible"] and by_id["too_close"]["decision_note"] == "min_gap"
    assert [c["cand_id"] for c in by_id.values() if c["selected"]] == ["best", "second"]
    assert by_id["best"]["brand"]["brand_id"] == "food" and by_id["second"]["brand"]["brand_id"] == "phone"
    assert summary["outcome"] == "breaks"


def test_negative_context_is_a_hard_filter_and_can_drop_a_break():
    by_id, _ = run([
        candidate("funeral", 1000, .9, before=["dinner", "funeral"], after=["theft"]),
        candidate("fallback", 2000, .6, before=["dinner"]),
    ], n_breaks=1)
    assert by_id["funeral"]["decision_note"] == "no_brand_safe" and not by_id["funeral"]["selected"]
    assert {b["brand_id"] for b in by_id["funeral"]["excluded_brands"]} == {"food", "phone"}
    assert by_id["fallback"]["selected"]  # next eligible candidate takes the slot


def test_no_break_is_a_valid_outcome():
    by_id, summary = run([candidate("a", 1000, .2), candidate("b", 60, .9)])
    assert not any(c["selected"] for c in by_id.values())
    assert summary["outcome"] == "no_break" and summary["reason"]


def test_unseen_brand_works_from_catalogue_metadata_alone():
    new_brand = {"brand_id": "chai", "name": "Brand New Chai", "category": "beverages", "preferred_contexts": ["tea", "চা"], "negative_contexts": [], "creatives": []}
    ranked, _ = rank_brands({"before": tokens("ওরা চায়ের দোকানে tea খাচ্ছে"), "after": [], "categories": []}, CATALOGUE + [new_brand], 0)
    assert ranked[0]["brand_id"] == "chai" and ranked[0]["matched_preferred"] == ["tea", "চা"]


def test_phrase_matching_handles_inflection_and_phrases():
    assert phrase_in("ফোন", tokens("ফোনটা বদলাতে হবে"))
    assert phrase_in("phone", tokens("two phones"))
    assert phrase_in("hungry child", tokens("a hungry child cried"))
    assert not phrase_in("hungry child", tokens("the child was not hungry"))
    assert not phrase_in("ab", tokens("abc"))


def test_generated_candidates_carry_constraints_and_context():
    scenes = [
        {"scene_id": "s1", "start": 0, "end": 300, "entity_ids": ["e1"], "visual": {"location": "kitchen", "activity": "cooking", "objects": []},
         "semantic": {"title": "Dinner", "summary": "They order biryani.", "topics": ["food"], "mood": "warm", "narrative_intensity": .2, "is_cliffhanger": False}},
        {"scene_id": "s2", "start": 300, "end": 600, "entity_ids": [], "visual": {"location": "street", "activity": "walking", "objects": []},
         "semantic": {"title": "Walk", "summary": "", "topics": [], "mood": "calm", "narrative_intensity": .3, "is_cliffhanger": False}},
    ]
    entities = [{"entity_id": "e1", "name": "biryani", "name_bn": "বিরিয়ানি", "ad_categories": ["food_delivery"], "confidence": .9,
                 "sentiment": "positive", "presence": "mentioned_only", "mentions": [{"time": 100}]}]
    utterances = [{"utt_id": "u1", "start": 299.8, "end": 301, "speaker": "A", "text": "হ্যাঁ"}]
    [c] = generate_candidates(duration=600, scenes=scenes, silences=[], utterances=utterances, entities=entities,
                              intensity=[[float(t), .2] for t in range(600)], protected=set(), t=T)
    assert c["time"] == 300 and c["hard_rejections"] == ["speech_at_cut"]
    assert "biryani" in c["context"]["before"] and c["context"]["categories"] == ["food_delivery"]


def test_vmap_lists_selected_breaks_with_inline_vast():
    by_id, _ = run([candidate("best", 1234.5, .9, before=["dinner"])])
    xml = build_vmap(list(by_id.values()), CATALOGUE, "http://x/ads/creatives/{brand_id}/{creative_id}.mp4")
    assert 'timeOffset="00:20:34.500"' in xml and "http://x/ads/creatives/food/food_30.mp4" in xml and "<Duration>00:00:30</Duration>" in xml


def test_shipped_catalogue_loads_and_matches_free_text_categories():
    catalogue = load_catalogue(Settings().brand_catalogue)
    assert catalogue and all(b["category"] and b["preferred_contexts"] and b["creatives"] for b in catalogue)
    assert all(c["language"] and c["duration"] > 0 for b in catalogue for c in b["creatives"])
    ranked, _ = rank_brands({"before": tokens("family dinner in the kitchen"), "after": [], "categories": ["food_delivery"]}, catalogue, .9)
    assert ranked[0]["category_match"] and "food" in ranked[0]["category"]


def test_creative_choice_uses_language_and_break_safety():
    brand = {"brand_id": "b", "creatives": [
        {"id": "en_30", "duration": 30, "language": "en", "url": None},
        {"id": "bn_15", "duration": 15, "language": "bn", "url": None},
        {"id": "bn_20", "duration": 20, "language": "bn", "url": None},
        {"id": "bn_30", "duration": 30, "language": "bn", "url": None},
    ]}
    assert pick_creative(brand, .9, "bn")["id"] == "bn_30"    # very safe break: longest episode-language spot
    assert pick_creative(brand, .65, "bn")["id"] == "bn_20"   # medium: capped at 20 s
    assert pick_creative(brand, .5, "bn")["id"] == "bn_15"    # marginal: shortest
    only_long = {"brand_id": "c", "creatives": [{"id": "bn_30", "duration": 30, "language": "bn", "url": None}]}
    assert pick_creative(only_long, .5, "bn")["id"] == "bn_30"  # nothing fits: shortest available
    english = {"brand_id": "d", "creatives": [{"id": "en_15", "duration": 15, "language": "en", "url": None}]}
    picked = pick_creative(english, .9, "bn")
    assert picked["id"] == "en_15" and picked["language_match"] is False  # fallback to other language
    assert pick_creative({"brand_id": "e", "creatives": []}, .9, "bn") is None
