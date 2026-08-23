from sportrx.intensity import calculate_intensity, estimate_hrmax


def test_estimate_hrmax_uses_simple_age_formula():
    assert estimate_hrmax(40) == 180


def test_moderate_intensity_returns_hr_rpe_and_talk_test():
    result = calculate_intensity({"age": 40, "resting_hr": 68}, "moderate")

    assert result["target_hr_zone_bpm"] == (115, 137)
    assert result["hrr_target_zone_bpm"] == (113, 134)
    assert result["rpe_0_10"] == (5, 6)
    assert "talk" in result["talk_test"].lower()
