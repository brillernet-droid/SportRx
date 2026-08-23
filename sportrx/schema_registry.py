"""Measurement schema registry for SportRx.

The registry documents local prototype data contracts. It is a release and
review artifact, not a validation layer.
"""

from __future__ import annotations

from typing import Any


CLAIM_BOUNDARY = (
    "Measurement Schema Registry documents local SportRx data objects and export "
    "coverage only. It does not validate measures, create athlete norms, predict "
    "outcomes, or provide medical clearance."
)


SCHEMA_OBJECTS = [
    {
        "id": "profile_snapshot",
        "label": "Profile Snapshot",
        "owner": "Core / Session Snapshot",
        "export_artifact_id": "session_snapshot_json",
        "required_fields": ["age", "training_days", "weekly_training_minutes", "equipment_access"],
        "not_tested_policy": "Missing performance tests are stored separately as Not tested.",
        "used_by": ["Safety Gate", "Quick Match", "Training Profile", "Export Center"],
    },
    {
        "id": "safety_gate_result",
        "label": "Safety Gate Result",
        "owner": "Safety Gate",
        "export_artifact_id": "session_snapshot_json",
        "required_fields": ["status", "reasons", "claim_boundary"],
        "not_tested_policy": "Safety can block training handoff but does not raise or lower performance.",
        "used_by": ["Workbench", "HYROX Check", "Benchmark Protocol", "Training Handoff"],
    },
    {
        "id": "benchmark_protocol",
        "label": "Benchmark Protocol",
        "owner": "Benchmark Protocol",
        "export_artifact_id": "protocol_markdown",
        "required_fields": ["name", "path", "version", "component_protocols", "global_stop_rules"],
        "not_tested_policy": "Protocol defines how to test; it does not infer missing results.",
        "used_by": ["Benchmark Protocol", "Test-Day Brief", "Test Session Operator"],
    },
    {
        "id": "test_session_operator",
        "label": "Test Session Operator",
        "owner": "Benchmark Protocol",
        "export_artifact_id": "test_session_operator_markdown",
        "required_fields": ["safety_gate_status", "steps", "component_steps", "global_stop_rules"],
        "not_tested_policy": "Operator guides execution only; incomplete components remain Not tested.",
        "used_by": ["Benchmark Protocol", "Benchmark Log"],
    },
    {
        "id": "benchmark_session",
        "label": "Benchmark Session",
        "owner": "Benchmark Log",
        "export_artifact_id": "benchmark_log_json",
        "required_fields": ["session_id", "date", "benchmark_path", "protocol_version", "component_results"],
        "not_tested_policy": "Only completed components with raw values count as measured.",
        "used_by": ["Benchmark Log", "Training Profile", "Retest", "Export Center"],
    },
    {
        "id": "component_result",
        "label": "Component Result",
        "owner": "Benchmark Log",
        "export_artifact_id": "benchmark_log_json",
        "required_fields": ["component_id", "completed", "value", "value_unit", "rpe_0_10", "equipment", "notes"],
        "not_tested_policy": "Missing component values are not replaced by averages, midpoint scores, or defaults.",
        "used_by": ["Benchmark Log", "Retest", "HYROX Check Import"],
    },
    {
        "id": "session_quality",
        "label": "Session Quality Review",
        "owner": "Benchmark Log",
        "export_artifact_id": "benchmark_log_json",
        "required_fields": ["status", "save_allowed", "completed_components", "measured_area_count", "issues", "warnings"],
        "not_tested_policy": "Quality checks data completeness only, not performance level.",
        "used_by": ["Benchmark Log Review & Save"],
    },
    {
        "id": "import_compatibility",
        "label": "HYROX Import Compatibility",
        "owner": "Benchmark Log",
        "export_artifact_id": "benchmark_log_json",
        "required_fields": ["status", "importable_fields", "needs_detail", "raw_only", "claim_boundary"],
        "not_tested_policy": "Raw-only results stay in Benchmark Log and are not converted into synthetic scores.",
        "used_by": ["Benchmark Log", "HYROX Check"],
    },
    {
        "id": "training_profile_report",
        "label": "Training Profile Report",
        "owner": "Training Profile",
        "export_artifact_id": "training_profile_markdown",
        "required_fields": ["measurement", "known", "unknown", "starter_path_status", "claim_boundary"],
        "not_tested_policy": "Unknown areas remain visible and block tailored Starter Path when insufficient.",
        "used_by": ["Training Profile", "Starter Path", "Reviewer Handoff"],
    },
    {
        "id": "training_block",
        "label": "4-Week Training Block",
        "owner": "Training Block",
        "export_artifact_id": "training_block_markdown",
        "required_fields": ["available", "weeks", "sessions", "handoff", "claim_boundary"],
        "not_tested_policy": "Tailored block remains gated when measured data are insufficient.",
        "used_by": ["Training", "Feedback Loop"],
    },
    {
        "id": "feedback_dashboard",
        "label": "Feedback Dashboard",
        "owner": "Feedback Loop",
        "export_artifact_id": "feedback_dashboard_markdown",
        "required_fields": ["adherence", "plan_actual_reasons", "retest_comparisons", "claim_boundary"],
        "not_tested_policy": "Non-comparable retests are kept as context rather than interpreted change.",
        "used_by": ["Retest", "Training Adjustment", "Export Center"],
    },
    {
        "id": "pilot_feedback_entry",
        "label": "Pilot Feedback Entry",
        "owner": "Pilot Feedback",
        "export_artifact_id": "pilot_feedback_json",
        "required_fields": ["reviewer_role", "ratings", "comments", "contact_consent"],
        "not_tested_policy": "Pilot feedback is product feedback, not scientific validation data.",
        "used_by": ["Pilot Review", "Public Beta Readiness"],
    },
    {
        "id": "export_bundle_manifest",
        "label": "Export Bundle Manifest",
        "owner": "Export Center",
        "export_artifact_id": "manifest_json",
        "required_fields": ["schema", "artifact_count", "artifacts", "claim_boundary"],
        "not_tested_policy": "Manifest reports local files only; it does not certify scientific validity.",
        "used_by": ["Export Center", "Review Pack", "Release QA"],
    },
]


def build_measurement_schema_registry(export_file_ids: set[str] | list[str] | None = None) -> dict[str, Any]:
    """Build a registry of SportRx local data objects and export coverage."""

    provided_ids = set(export_file_ids or [])
    objects = []
    for item in SCHEMA_OBJECTS:
        exported = not provided_ids or item["export_artifact_id"] in provided_ids
        objects.append(
            {
                **item,
                "field_count": len(item["required_fields"]),
                "export_status": "included" if exported else "missing_from_current_bundle",
            }
        )

    missing = [item for item in objects if item["export_status"] != "included"]
    source_types = sorted({item["owner"] for item in objects})
    return {
        "schema": "sportrx.measurement_schema_registry",
        "schema_version": "0.1",
        "status": "complete" if not missing else "missing_export_coverage",
        "object_count": len(objects),
        "exported_object_count": len(objects) - len(missing),
        "missing_export_count": len(missing),
        "owner_count": len(source_types),
        "owners": source_types,
        "objects": objects,
        "missing_exports": missing,
        "primary_message": "SportRx keeps a documented local data contract before adding external integrations.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def measurement_schema_registry_markdown(registry: dict[str, Any]) -> str:
    """Export the measurement schema registry as Markdown."""

    lines = [
        "# SportRx Measurement Schema Registry",
        "",
        f"- Status: {registry['status']}",
        f"- Objects: {registry['object_count']}",
        f"- Exported objects: {registry['exported_object_count']}",
        f"- Missing export coverage: {registry['missing_export_count']}",
        f"- Claim boundary: {registry['claim_boundary']}",
        "",
        "## Objects",
    ]
    for item in registry["objects"]:
        lines.extend(
            [
                "",
                f"### {item['label']}",
                "",
                f"- ID: `{item['id']}`",
                f"- Owner: {item['owner']}",
                f"- Export artifact: `{item['export_artifact_id']}` ({item['export_status']})",
                f"- Required fields: {', '.join(item['required_fields'])}",
                f"- Not-tested policy: {item['not_tested_policy']}",
                f"- Used by: {', '.join(item['used_by'])}",
            ]
        )
    return "\n".join(lines) + "\n"
