from sportrx import generate_prescription, load_program_packs, resolve_program_pack, validate_program_packs


def _healthy_profile(**overrides):
    profile = {
        "age": 36,
        "goal": "build_activity_habit",
        "exercise_days_last_4w": 0,
        "mvpa_minutes_per_week": 0,
        "available_days_per_week": 3,
        "max_minutes_per_session": 30,
        "preferred_activity": "brisk walking",
        "symptoms": [],
        "known_conditions": [],
    }
    profile.update(overrides)
    return profile


def test_program_pack_registry_is_versioned_and_valid():
    result = validate_program_packs(load_program_packs())

    assert result["valid"] is True
    assert result["pack_count"] == 4
    assert "low_activity_aerobic_v1" in result["pack_ids"]


def test_low_activity_goal_resolves_to_released_self_service_pack():
    route = resolve_program_pack(_healthy_profile())

    assert route["route"] == "self_service"
    assert route["automation_allowed"] is True
    assert route["pack"]["id"] == "low_activity_aerobic_v1"
    assert route["pack"]["rule_ids"] == ["SAFE-001", "CORE-002", "INT-001"]


def test_general_fitness_pack_is_explicitly_limited_to_aerobic_automation():
    route = resolve_program_pack(_healthy_profile(goal="general_fitness"))

    assert route["automation_allowed"] is True
    assert route["pack"]["id"] == "general_fitness_foundation_v1"
    assert "basic_strength_movements" in route["pack"]["content_mapping"]["content_only"]


def test_assessment_only_pack_cannot_generate_automatic_dose():
    result = generate_prescription(_healthy_profile(goal="performance_entry"))

    assert result["safety"]["auto_prescription"] is True
    assert result["program_route"]["route"] == "assessment_only"
    assert result["program_route"]["automation_allowed"] is False
    assert result["weeks"] == []


def test_out_of_scope_context_routes_to_professional_collaboration():
    route = resolve_program_pack(_healthy_profile(age=65))

    assert route["route"] == "professional_collaboration"
    assert route["automation_allowed"] is False
    assert route["pack"] is None
