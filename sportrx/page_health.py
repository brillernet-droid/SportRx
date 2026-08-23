"""Page-level product health matrix for SportRx.

The matrix explains what each page is responsible for and what it must not be
used to claim. It is a release-review artifact, not a scoring layer.
"""

from __future__ import annotations

from typing import Any


CLAIM_BOUNDARY = (
    "Page Health Matrix documents product navigation, page responsibilities, "
    "success signals, and claim boundaries. It does not validate SportRx, score "
    "performance, predict outcomes, or provide medical clearance."
)


PAGE_SPECS = [
    {
        "page": "Workbench",
        "lane": "Start",
        "primary_question": "Where should a first-time user start?",
        "success_signal": "User can choose full demo, Quick Match, or Benchmark-first trial without reading docs.",
        "primary_evidence": "Lab Workflow Board, Trial Mode Launcher, First Run Guide.",
        "blocked_claim": "The Workbench is not evidence that SportRx is validated.",
    },
    {
        "page": "Quick Match",
        "lane": "Intake",
        "primary_question": "Is this self-reported intake usable for rough routing?",
        "success_signal": "Recent behavior fields are numeric and Intake Precision Audit labels the data as self-report.",
        "primary_evidence": "Quick Match Input Review and Intake Precision Audit.",
        "blocked_claim": "Quick Match is not a measured performance test or readiness score.",
    },
    {
        "page": "HYROX Check",
        "lane": "Measurement",
        "primary_question": "Which performance fields are measured, not tested, or only context?",
        "success_signal": "Missing tests remain Not tested and at least two measured dimensions are required for gap comparison.",
        "primary_evidence": "Measurement Review, Lab Test Quality, Measurement Intake Matrix.",
        "blocked_claim": "HYROX Check does not create percentiles, norms, or injury-risk estimates.",
    },
    {
        "page": "Benchmark Protocol",
        "lane": "Measurement",
        "primary_question": "How should the benchmark be run consistently?",
        "success_signal": "Standard and low-equipment paths list setup, order, stop rules, and record fields.",
        "primary_evidence": "Protocol command console, Test Session Operator, Test-Day Brief.",
        "blocked_claim": "The protocol is not medical clearance or a validated population benchmark.",
    },
    {
        "page": "Benchmark Log",
        "lane": "Raw Data",
        "primary_question": "Can raw test data be saved with enough context?",
        "success_signal": "Raw values, units, RPE, equipment, substitutions, and notes are saved before interpretation.",
        "primary_evidence": "Session quality review, import compatibility, JSON/CSV logs.",
        "blocked_claim": "A single log is not a validated performance change or athlete norm.",
    },
    {
        "page": "Training Profile",
        "lane": "Handoff",
        "primary_question": "What is currently known, unknown, and blocked?",
        "success_signal": "Known/unknown metrics and Starter Path gate are visible before any training plan.",
        "primary_evidence": "Training Profile Report, Output Prerequisite Register.",
        "blocked_claim": "The profile is not a diagnostic label or validated readiness score.",
    },
    {
        "page": "训练",
        "lane": "Handoff",
        "primary_question": "Is a conservative Starter Path allowed?",
        "success_signal": "Training block appears only after Safety Gate and measurement gates allow it.",
        "primary_evidence": "Training Handoff Console and 4-week Training Block.",
        "blocked_claim": "The block is not individualized medical treatment or guaranteed outcome.",
    },
    {
        "page": "复测",
        "lane": "Feedback",
        "primary_question": "How did execution and retest context affect next steps?",
        "success_signal": "Completion, RPE, plan-actual reasons, and retest context are visible before interpretation.",
        "primary_evidence": "Adaptive Loop Console, Retest Interpretation Guard.",
        "blocked_claim": "Retest deltas are not validated meaningful-change thresholds.",
    },
    {
        "page": "Pilot Feedback",
        "lane": "Pilot",
        "primary_question": "Can local alpha feedback and future data capture be structured?",
        "success_signal": "Reviewer feedback and alpha dataset templates can be exported locally.",
        "primary_evidence": "Pilot Review Console and Alpha Dataset Template.",
        "blocked_claim": "Pilot feedback is not validation evidence or proof of effectiveness.",
    },
    {
        "page": "Evidence Library",
        "lane": "Evidence",
        "primary_question": "Which sources support current rules and boundaries?",
        "success_signal": "Evidence tiers, product use, limitations, and required files are visible.",
        "primary_evidence": "Evidence Library and Evidence Coverage.",
        "blocked_claim": "Saved sources do not validate the current software implementation.",
    },
    {
        "page": "Export Center",
        "lane": "Release",
        "primary_question": "Can the local trial be reviewed, restored, and shared?",
        "success_signal": "Artifacts, Session Snapshot, Review Pack ZIP, and catalog are downloadable.",
        "primary_evidence": "Export Bundle, Artifact Catalog, Review Pack Integrity.",
        "blocked_claim": "Exports are review artifacts, not scientific validation.",
    },
    {
        "page": "Release QA",
        "lane": "Release",
        "primary_question": "Are product readiness checks and claim boundaries passing?",
        "success_signal": "Release QA, Runtime Doctor, Launch Readiness, and Public Beta gates are visible.",
        "primary_evidence": "Release QA checks and public package manifest.",
        "blocked_claim": "Passing QA does not prove safety, effectiveness, or validation.",
    },
]


def build_page_health_matrix(walkthrough: dict[str, Any]) -> dict[str, Any]:
    """Build a page health matrix from static page contracts and current state."""

    statuses = {step["page"]: step["status"] for step in walkthrough.get("steps", [])}
    rows = []
    for spec in PAGE_SPECS:
        status = statuses.get(spec["page"], "supporting")
        rows.append({**spec, "status": status})

    release_pages = [row for row in rows if row["lane"] == "Release"]
    complete_count = sum(1 for row in rows if row["status"] == "complete")
    waiting_count = sum(1 for row in rows if row["status"] not in {"complete", "supporting"})
    return {
        "schema": "sportrx.page_health_matrix",
        "schema_version": "0.1",
        "status": "ready_for_page_review",
        "page_count": len(rows),
        "complete_pages": complete_count,
        "waiting_pages": waiting_count,
        "release_page_count": len(release_pages),
        "rows": rows,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def page_health_matrix_markdown(matrix: dict[str, Any]) -> str:
    """Export the page health matrix as Markdown."""

    lines = [
        "# SportRx Page Health Matrix",
        "",
        f"- Status: {matrix['status']}",
        f"- Pages: {matrix['page_count']}",
        f"- Complete pages: {matrix['complete_pages']}",
        f"- Waiting pages: {matrix['waiting_pages']}",
        f"- Claim boundary: {matrix['claim_boundary']}",
        "",
        "## Pages",
    ]
    for row in matrix["rows"]:
        lines.extend(
            [
                "",
                f"### {row['page']}",
                f"- Lane: {row['lane']}",
                f"- Status: {row['status']}",
                f"- Primary question: {row['primary_question']}",
                f"- Success signal: {row['success_signal']}",
                f"- Primary evidence: {row['primary_evidence']}",
                f"- Blocked claim: {row['blocked_claim']}",
            ]
        )
    return "\n".join(lines) + "\n"
