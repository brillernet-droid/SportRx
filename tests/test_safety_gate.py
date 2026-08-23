from sportrx.safety_gate import evaluate_safety_gate


def test_safety_gate_green_for_low_flag_profile():
    result = evaluate_safety_gate({"age": 35, "symptoms": [], "known_conditions": []})

    assert result["status"] == "GREEN"
    assert result["training_handoff_allowed"] is True


def test_safety_gate_yellow_for_known_condition_without_high_intensity():
    result = evaluate_safety_gate(
        {
            "age": 45,
            "known_conditions": ["metabolic_disease"],
            "symptoms": [],
            "intended_intensity": "moderate",
        }
    )

    assert result["status"] == "YELLOW"
    assert result["training_handoff_allowed"] is True


def test_safety_gate_red_for_warning_symptom():
    result = evaluate_safety_gate({"age": 45, "symptoms": ["chest_pain"], "known_conditions": []})

    assert result["status"] == "RED"
    assert result["training_handoff_allowed"] is False


def test_age_alone_does_not_make_safety_gate_yellow():
    result = evaluate_safety_gate({"age": 68, "symptoms": [], "known_conditions": []})

    assert result["status"] == "GREEN"
