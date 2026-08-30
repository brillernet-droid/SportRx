from sportrx.screening import screen_user


def test_screening_allows_apparently_healthy_adult():
    result = screen_user({"age": 40, "symptoms": [], "known_conditions": []})

    assert result["auto_prescription"] is True
    assert result["flags"] == []


def test_screening_blocks_warning_symptom():
    result = screen_user({"age": 40, "symptoms": ["chest_pain"], "known_conditions": []})

    assert result["auto_prescription"] is False
    assert "SYMPTOM_CHEST_PAIN" in result["flags"]


def test_screening_blocks_out_of_scope_older_adult():
    result = screen_user({"age": 70, "symptoms": [], "known_conditions": []})

    assert result["auto_prescription"] is False
    assert "AGE_OVER_V01_SCOPE" in result["flags"]


def test_screening_blocks_a_non_specific_warning_or_condition_report():
    symptom_result = screen_user({"age": 40, "symptoms": ["reported_warning_symptom"], "known_conditions": []})
    condition_result = screen_user({"age": 40, "symptoms": [], "known_conditions": ["reported_relevant_condition"]})

    assert symptom_result["auto_prescription"] is False
    assert condition_result["auto_prescription"] is False
