from sportrx.safety_gate import evaluate_safety_gate
from sportrx.screening_provider_registry import validate_screening_provider_registry
from sportrx.test_session_operator import build_test_session_operator
from sportrx.venue_entry import build_venue_entry_assessment


ROOT = "."
APPROVED_PROVIDER = {
    "id": "CN-APPROVED-TEST",
    "deployment_status": "approved_for_venue",
}


def _profile(**screening):
    return {
        "age": 30,
        "symptoms": ["chest_pain"],  # Venue routing must never read this legacy field.
        "venue_screening": {
            "provider_id": "CN-APPROVED-TEST",
            "provider_version": "v-test",
            "consent": True,
            "member_reported_outcome": "completed_continue",
            "health_changed_since_screening": False,
            **screening,
        },
    }


def test_venue_safety_gate_truth_table():
    cases = [
        ({}, "eligible_for_benchmark", "GREEN", True),
        ({"consent": False}, "screening_follow_up_needed", "YELLOW", False),
        ({"member_reported_outcome": "not_completed"}, "screening_follow_up_needed", "YELLOW", False),
        ({"member_reported_outcome": "follow_up_needed"}, "screening_follow_up_needed", "YELLOW", False),
        ({"health_changed_since_screening": True}, "stop_automation", "RED", False),
    ]

    for screening, route, status, allowed in cases:
        result = evaluate_safety_gate(_profile(**screening), providers=[APPROVED_PROVIDER])
        assert result["route"] == route
        assert result["status"] == status
        assert result["benchmark_allowed"] is allowed
        assert result["automated_handoff_allowed"] is allowed


def test_venue_safety_gate_stops_non_adult_scope_and_unapproved_provider():
    adult_scope = evaluate_safety_gate({**_profile(), "age": 17}, providers=[APPROVED_PROVIDER])
    unapproved = evaluate_safety_gate(_profile(), providers=[])

    assert adult_scope["route"] == "stop_automation"
    assert adult_scope["benchmark_allowed"] is False
    assert unapproved["route"] == "screening_follow_up_needed"
    assert unapproved["deployment_status"] == "demo_only"


def test_non_green_venue_route_cannot_open_test_operator():
    gate = evaluate_safety_gate(
        _profile(member_reported_outcome="follow_up_needed"), providers=[APPROVED_PROVIDER]
    )
    operator = build_test_session_operator([], safety_gate=gate)

    assert operator["status"] == "blocked_by_safety_gate"
    assert operator["preflight_steps"][0]["status"] == "blocked"


def test_default_registry_is_explicitly_research_required():
    registry = validate_screening_provider_registry(ROOT)

    assert registry["status"] == "research_required"
    assert registry["approved_provider_count"] == 0
    assert registry["errors"] == []


def test_member_export_whitelists_routing_metadata_only():
    assessment = build_venue_entry_assessment(
        {
            **_profile(provider_id="CN-VENUE-SCREENING-PENDING"),
            "name": "member name",
            "phone": "123456",
            "known_conditions": ["metabolic_disease"],
        }
    )
    exported = assessment["member_export"]
    forbidden = {"name", "phone", "symptoms", "known_conditions", "screening_answers", "diagnoses", "source_url"}

    assert set(exported).isdisjoint(forbidden)
    assert exported["route"] == "screening_follow_up_needed"
    assert exported["benchmark_allowed"] is False
