from sportrx.intake_precision import build_intake_precision_audit, intake_precision_markdown


def test_intake_precision_audit_separates_numeric_measured_and_safety_inputs():
    audit = build_intake_precision_audit(
        {
            "age": 35,
            "training_days": 3,
            "weekly_training_minutes": 120,
            "running_minutes_per_week": 60,
            "longest_continuous_run_minutes": 20,
            "strength_days_per_week": 1,
            "available_days_per_week": 3,
            "max_minutes_per_session": 45,
            "one_km_run_seconds": 310,
            "station_test_score": None,
            "symptoms": [],
            "known_conditions": [],
        }
    )
    rows = {item["field_id"]: item for item in audit["rows"]}

    assert audit["schema"] == "sportrx.intake_precision_audit"
    assert rows["age"]["precision_class"] == "direct_numeric"
    assert rows["one_km_run_seconds"]["precision_class"] == "measured_test"
    assert rows["station_test_score"]["status"] == "not_tested"
    assert rows["known_conditions"]["precision_class"] == "safety_only"
    assert "never changes performance" in rows["known_conditions"]["user_boundary"]
    assert audit["summary"]["measured_tests_recorded"] == 1
    assert audit["summary"]["direct_numeric_collected"] >= 8


def test_intake_precision_flags_legacy_and_unsupported_fields_as_ignored():
    audit = build_intake_precision_audit(
        {
            "age": 35,
            "running_comfort": 5,
            "vo2max": 52,
            "hrmax": 190,
        }
    )
    rows = {item["field_id"]: item for item in audit["rows"]}

    assert audit["status"] == "review_ignored_fields"
    assert rows["running_comfort"]["precision_class"] == "legacy_subjective_ignored"
    assert rows["vo2max"]["precision_class"] == "unsupported_ignored"
    assert rows["hrmax"]["affects_output"] is False
    assert audit["summary"]["ignored_or_legacy_fields"] == 3
    assert audit["summary"]["problematic_ignored_fields"] == 3


def test_intake_precision_does_not_warn_for_backward_compatible_aliases_only():
    audit = build_intake_precision_audit(
        {
            "age": 35,
            "training_days": 3,
            "weekly_training_minutes": 120,
            "exercise_days_last_4w": 3,
            "mvpa_minutes_per_week": 120,
        }
    )
    rows = {item["field_id"]: item for item in audit["rows"]}

    assert audit["status"] == "intake_contract_ready"
    assert rows["exercise_days_last_4w"]["precision_class"] == "legacy_alias"
    assert rows["mvpa_minutes_per_week"]["precision_class"] == "legacy_alias"
    assert audit["summary"]["problematic_ignored_fields"] == 0


def test_intake_precision_markdown_exports_user_boundaries():
    markdown = intake_precision_markdown(build_intake_precision_audit({"age": 35, "one_km_run_seconds": 300}))

    assert "# SportRx Intake Precision Audit" in markdown
    assert "direct_numeric" in markdown
    assert "measured_test" in markdown
    assert "does not validate SportRx" in markdown
