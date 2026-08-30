"""Reusable race-check result object for SportRx event packs."""

from __future__ import annotations

from typing import Any

from .output_prerequisites import build_output_prerequisites
from .performance_lab import assess_hybrid_performance
from .quick_match import quick_match
from .starter_path import build_starter_path
from .safety_gate import automated_handoff_allowed


def build_readiness_passport(profile: dict[str, Any], event_pack: str = "hybrid_race") -> dict[str, Any]:
    """Build the result object shared by future SportRx event packs."""

    if event_pack != "hybrid_race":
        match = quick_match(profile)
        top = match["top_matches"][0]
        return {
            "event_profile_match": top["event_profile"],
            "experimental_readiness_score": None,
            "current_measured_picture": "Not enough measured data",
            "readiness_category": "Not enough measured data",
            "safety_gate": match["safety_gate"],
            "athlete_type": match["athlete_profile_label"],
            "training_profile": match["athlete_profile_label"],
            "dimension_scores": {},
            "performance_profile": {},
            "training_context": {},
            "metric_sources": {
                "schema": "sportrx.metric_source_register",
                "schema_version": "0.1",
                "summary": {"total_metrics": 0, "measured_performance_metrics": 0, "not_tested_metrics": 0, "unsupported_inputs": 0},
                "performance_metrics": [],
                "context_metrics": [],
                "safety_metrics": [],
                "unsupported_inputs": [],
                "all_metrics": [],
                "claim_boundary": "Metric source labels document provenance only.",
            },
            "output_prerequisites": {
                "schema": "sportrx.output_prerequisites",
                "schema_version": "0.1",
                "outputs": [],
                "summary": {"total_outputs": 0, "active_outputs": 0, "blocked_outputs": 0, "provisional_outputs": 0, "waiting_outputs": 0},
                "claim_boundary": "Output prerequisites explain product gates only.",
            },
            "strongest_capability": top["strongest_capability"],
            "primary_limiter": top["obvious_limiter"],
            "strongest_area": top["strongest_capability"],
            "main_gap": top["obvious_limiter"],
            "top_3_priorities": ["Enter the relevant Performance Lab when this pack is enabled."],
            "assessment_completeness": "LOW",
            "areas_assessed": {"level": "LOW", "assessed": 0, "total": 5, "label": "0 of 5 key areas assessed"},
            "measured_performance_areas": {"count": 0, "areas": [], "label": "0 measured performance areas"},
            "what_we_know": [],
            "what_we_do_not_know": ["This pack has not been assessed in a Performance Lab yet."],
            "what_to_measure_next": ["Open the relevant Performance Lab when this pack is enabled."],
            "next_action": top["cta"],
            "rule_evidence_explanation": "This pack is registry-ready and uses Quick Match only.",
            "starter_path": {"available": False, "reason": "Pack not fully enabled.", "weeks": []},
            "community_route": external_community_route(top["pack_id"]),
        }

    lab = assess_hybrid_performance(profile)
    starter_path = build_starter_path(lab)
    if starter_path["available"]:
        next_action = "Build 4-week Starter Path"
    elif not automated_handoff_allowed(lab["safety_gate"]):
        next_action = "Resolve safety gate before training"
    else:
        next_action = "Complete SportRx Hybrid Benchmark v1"
    result = {
        "event_profile_match": lab["event_profile"],
        "experimental_readiness_score": lab["readiness_score"],
        "current_measured_picture": lab["current_measured_picture"],
        "readiness_category": lab["readiness_category"],
        "safety_gate": lab["safety_gate"],
        "athlete_type": lab["athlete_type"],
        "training_profile": lab["training_profile"],
        "dimension_scores": lab["dimension_scores"],
        "performance_profile": lab["performance_profile"],
        "training_context": lab["training_context"],
        "metric_sources": lab["metric_sources"],
        "lab_test_quality": lab["lab_test_quality"],
        "strongest_capability": lab["strongest_area"],
        "primary_limiter": lab["main_gap"],
        "strongest_area": lab["strongest_area"],
        "main_gap": lab["main_gap"],
        "top_3_priorities": lab["top_3_priorities"],
        "assessment_completeness": lab["assessment_completeness"],
        "areas_assessed": lab["areas_assessed"],
        "measured_performance_areas": lab["measured_performance_areas"],
        "what_we_know": lab["what_we_know"],
        "what_we_do_not_know": lab["what_we_do_not_know"],
        "what_to_measure_next": lab["what_to_measure_next"],
        "next_action": next_action,
        "rule_evidence_explanation": (
            "This check uses the safety gate, reported training, completed performance tests, and missing measurements. "
            "Tests completed is data completeness, not predictive confidence."
        ),
        "starter_path": starter_path,
        "community_route": external_community_route("hybrid_race"),
        "retest_cta": "Retest after 4 weeks or after your next benchmark session.",
    }
    result["output_prerequisites"] = build_output_prerequisites(result)
    return result


def external_community_route(pack_id: str) -> dict[str, str]:
    """Return an external route placeholder without building a social network."""

    routes = {
        "hybrid_race": "Find a local hybrid race, HYROX-style gym class, or running group.",
        "running_5k_10k": "Find a local 5K/10K running group or beginner race calendar.",
    }
    return {
        "type": "external_route_only",
        "label": routes.get(pack_id, "Find a relevant external training community."),
    }
