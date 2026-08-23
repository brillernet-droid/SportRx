from sportrx.plan_actual import classify_plan_actual, provisional_plan_actual
from sportrx.progression import evaluate_week


def test_plan_actual_classifies_high_completion_target_rpe():
    result = classify_plan_actual(3, 3, 5)

    assert result["action"] == "small_increase"
    assert result["reason_codes"] == ["HIGH_COMPLETION_TARGET_RPE"]
    assert result["flags"] == []
    assert "risk predictions" in result["claim_boundary"]


def test_plan_actual_classifies_low_completion_high_rpe():
    result = classify_plan_actual(3, 1, 8, felt_too_hard=True)

    assert result["action"] == "decrease"
    assert "LOW_COMPLETION_HIGH_RPE" in result["reason_codes"]
    assert "FELT_TOO_HARD" in result["flags"]
    assert "COMPLETION_BELOW_TARGET" in result["flags"]
    assert "RPE_ABOVE_TARGET" in result["flags"]


def test_evaluate_week_includes_reason_codes():
    decision = evaluate_week(planned_sessions=3, completed_sessions=3, average_rpe=3)

    assert decision["action"] == "increase"
    assert decision["reason_codes"] == ["HIGH_COMPLETION_LOW_RPE", "RPE_BELOW_TARGET"]
    assert decision["plan_actual"]["action_label"] == "Increase dose"


def test_provisional_plan_actual_is_explicitly_not_adaptive_feedback():
    result = provisional_plan_actual(3)

    assert result["action"] == "small_increase"
    assert result["reason_codes"] == ["PROVISIONAL_NO_FEEDBACK"]
    assert "provisional preview" in result["claim_boundary"]
