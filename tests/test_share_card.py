from sportrx.passport import build_readiness_passport
from sportrx.quick_match import quick_match
from sportrx.share_card import build_readiness_passport_card, build_sport_match_card


PROFILE = {
    "age": 35,
    "training_days": 4,
    "weekly_training_minutes": 200,
    "running_minutes_per_week": 100,
    "longest_continuous_run_minutes": 35,
    "strength_days_per_week": 2,
    "high_intensity_sessions_last_4w": 4,
    "loaded_movement_sessions_last_4w": 4,
    "available_days_per_week": 4,
    "max_minutes_per_session": 60,
    "symptoms": [],
    "known_conditions": [],
}


def test_sport_match_card_is_qr_ready():
    card = build_sport_match_card(quick_match(PROFILE), short_url="sportrx.test/match")

    assert card["brand"] == "SportRx Labs"
    assert card["qr_ready"] is True
    assert "percentile" not in str(card).lower()


def test_passport_card_is_qr_ready():
    card = build_readiness_passport_card(build_readiness_passport(PROFILE), short_url="sportrx.test/passport")

    assert card["card_type"] == "race_check"
    assert card["qr_ready"] is True
    assert "readiness" not in card
    assert "current_picture" in card
    assert "tested" in card
