"""Open-source integration console for SportRx.

This module turns the GitHub comparable-product scan into a user-facing
positioning artifact. It is product research, not scientific evidence.
"""

from __future__ import annotations

from typing import Any


CLAIM_BOUNDARY = (
    "Open-source integration notes explain product architecture decisions only. "
    "They do not validate SportRx, compare outcomes, rank competitors, or create "
    "scientific evidence."
)


COMPARABLE_PROJECTS = [
    {
        "project": "FitOntology",
        "url": "https://github.com/Conalh/fit-ontology",
        "category": "coach decision support",
        "lesson": "Decision-support tools feel credible when every recommendation traces back to exact source rows, thresholds, and override history.",
        "decision": "Turn SportRx outputs into auditable measurement-to-handoff decisions with source labels and blocked-claim boundaries.",
        "status": "adopted",
        "boundary": "Do not add wearable recovery scoring, trainer accounts, or AI assistant workflows in the current milestone.",
    },
    {
        "project": "exercise-prescription-recommendation",
        "url": "https://github.com/keanu77/exercise-prescription-recommendation",
        "category": "exercise prescription generator",
        "lesson": "ACSM/FITT-VP exercise-plan generation is an obvious crowded baseline, so SportRx needs a sharper measurement-first position.",
        "decision": "Keep FITT-VP as the conservative training handoff layer, not the whole product.",
        "status": "adopted",
        "boundary": "Do not become a broad AI exercise prescription generator for every health condition.",
    },
    {
        "project": "WODIS",
        "url": "https://github.com/aassoiants/workout-open-data-spec",
        "category": "workout data specification",
        "lesson": "Portable records protect user-owned training history and make product trust stronger than app lock-in.",
        "decision": "Keep SportRx Benchmark Log exports raw, unit-preserving, and stable before any platform connector.",
        "status": "adopted",
        "boundary": "Do not overbuild a full workout interchange standard before SportRx benchmark sessions stabilize.",
    },
    {
        "project": "Domestique",
        "url": "https://github.com/platypus45/domestique",
        "category": "adaptive endurance planner",
        "lesson": "Adaptive training products feel real when plan-versus-actual signals can change the next prescription through explicit guardrails.",
        "decision": "Keep SportRx progression rule-coded and show the reason before friendly explanation.",
        "status": "adopted",
        "boundary": "Do not import cycling-specific load models, huge workout libraries, or opaque performance claims.",
    },
    {
        "project": "OpenAthlete",
        "url": "https://github.com/openathleteorg/openathlete",
        "category": "self-hosted endurance platform",
        "lesson": "Transparent algorithms, full export, and user-owned data are positioning features, not just engineering details.",
        "decision": "Keep SportRx local-first, export-first, and auditable before adding any cloud or platform integration.",
        "status": "adopted",
        "boundary": "Do not add Strava, Garmin, Suunto, Polar, Coros, mobile apps, or cloud accounts in this milestone.",
    },
    {
        "project": "Fit Log Web App",
        "url": "https://github.com/souzamonteiro/fitlogwebapp",
        "category": "broad fitness assessment",
        "lesson": "Users recognize assessment dashboards, progress history, and prescription summaries.",
        "decision": "Borrow the assessment-to-report rhythm while keeping medical and metabolic expansion out of scope.",
        "status": "adopted",
        "boundary": "Do not add blood metrics, BMI risk scoring, VO2max estimates, or all-in-one health assessment.",
    },
    {
        "project": "REGmon",
        "url": "https://github.com/REGmon-project/regmon",
        "category": "athlete monitoring and research data management",
        "lesson": "Sport-science products feel more credible when forms, dashboards, templates, permissions, and research data capture are treated as core workflow objects.",
        "decision": "Keep SportRx benchmark sessions, feedback, evidence files, and review exports structured enough for future small-group pilot data collection.",
        "status": "adopted",
        "boundary": "Do not add team accounts, permission systems, GDPR workflows, or a full athlete-monitoring platform now.",
    },
    {
        "project": "AthleteLoadMonitor",
        "url": "https://github.com/SaxionAMI/AthleteLoadMonitor",
        "category": "team-sport load monitoring",
        "lesson": "RPE, questionnaire context, and sensor-derived data should stay visibly separated before they are used for training decisions.",
        "decision": "Keep SportRx Safety Gate, self-report, measured benchmark results, and feedback signals in separate lanes before any handoff rule uses them.",
        "status": "adopted",
        "boundary": "Do not add predictive risk models, team-sport sensors, ACWR dashboards, or injury-risk labels in this milestone.",
    },
    {
        "project": "Athlete Report Generator",
        "url": "https://github.com/BartWil/athlete_report_generator",
        "category": "field-assessment report generator",
        "lesson": "Batch-friendly field assessment reports can be useful for coaches when required columns, profile outputs, and PDF/report handoffs are explicit.",
        "decision": "Use the idea of a strict assessment-to-report contract for future alpha reviews while keeping current SportRx reports single-user and local.",
        "status": "later",
        "boundary": "Do not add youth-athlete profiling, FMS/Y-balance scoring, batch coach dashboards, or PDF automation now.",
    },
    {
        "project": "Ballast",
        "url": "https://github.com/N-O-P-E/Ballast",
        "category": "privacy-first fitness tracker PWA",
        "lesson": "Low-friction local tracking feels trustworthy when users own their data and the app stays out of the way.",
        "decision": "Keep SportRx trial records exportable and avoid account/cloud requirements for the prototype.",
        "status": "adopted",
        "boundary": "Do not add a PWA/mobile app scope until the measurement layer is stable.",
    },
    {
        "project": "ShredTrack",
        "url": "https://github.com/shredstack/shred-track",
        "category": "HYROX/CrossFit tracker",
        "lesson": "Hybrid athletes need station-level logging, scaling, and equipment detail.",
        "decision": "Keep SportRx Hybrid Benchmark components structured and repeatable.",
        "status": "adopted",
        "boundary": "Do not add leaderboards, social competition, or workout marketplace features.",
    },
    {
        "project": "Section 11",
        "url": "https://github.com/CrankAddict/section-11",
        "category": "protocol-driven AI endurance guidance",
        "lesson": "Protocol files, dossier templates, pass/fail response checks, and bad-response examples make AI-adjacent systems less vague.",
        "decision": "Use protocol documents, evidence maps, review packs, and blocked-language checks instead of giving the LLM dosing authority.",
        "status": "adopted",
        "boundary": "Do not add an AI chat coach or endurance-platform sync.",
    },
    {
        "project": "Free Exercise DB",
        "url": "https://github.com/yuhonas/free-exercise-db",
        "category": "exercise database",
        "lesson": "Schema-backed exercise catalogs are useful only after the product knows which movements it truly needs.",
        "decision": "Defer any exercise taxonomy import until benchmark components and Starter Path movements are stable.",
        "status": "later",
        "boundary": "Do not import hundreds of exercises or build an exercise browser now.",
    },
    {
        "project": "Claude Coach",
        "url": "https://github.com/felixrieseberg/claude-coach",
        "category": "AI endurance coach",
        "lesson": "Editable exports and local data make generated plans feel tangible.",
        "decision": "Keep markdown/JSON reports and local handoff files; do not move the product center to chat.",
        "status": "later",
        "boundary": "Do not reposition SportRx as an endurance AI coach.",
    },
    {
        "project": "Coach Paddy",
        "url": "https://github.com/BorisBW/claude-fitness-cn",
        "category": "wearable-driven AI fitness coach",
        "lesson": "Plain-text local files and bilingual UX are useful product ideas, but wearable recovery dashboards are a different product.",
        "decision": "Keep Chinese-first copy and local exports; defer wearable-driven coaching.",
        "status": "later",
        "boundary": "Do not add Garmin, HRV, sleep, body battery, readiness, or daily AI coaching.",
    },
    {
        "project": "URUJ Labs",
        "url": "https://github.com/gazzycodes/uruj-labs",
        "category": "personal physiology lab",
        "lesson": "Physiology-lab style products build trust through source labels, methodology versions, and raw data ownership.",
        "decision": "Show measured, self-reported, not-tested, ignored, and protocol-provenance labels.",
        "status": "later",
        "boundary": "Do not add HRV, recovery scoring, live cycling HUDs, or wearable readiness claims now.",
    },
    {
        "project": "HYROX-Pace",
        "url": "https://github.com/willckim/HYROX-Pace",
        "category": "HYROX race execution",
        "lesson": "Race-specific tools win by making event structure concrete, but they depend on event-specific assumptions.",
        "decision": "Use HYROX vocabulary carefully in benchmark UX, without claiming race prediction or official event readiness.",
        "status": "later",
        "boundary": "Do not generate finish-time predictions, live pacing, or fake race readiness labels.",
    },
    {
        "project": "hyrox-race-insights",
        "url": "https://github.com/JamesIves/hyrox-race-insights",
        "category": "HYROX race analytics",
        "lesson": "Real race splits may later calibrate benchmark relevance.",
        "decision": "Defer race-result import until real SportRx pilot data exists.",
        "status": "later",
        "boundary": "Do not create fake finish predictions, fake percentiles, or fake athlete benchmarks.",
    },
    {
        "project": "Openweight",
        "url": "https://github.com/radupana/openweight",
        "category": "strength-training data format",
        "lesson": "Vendor-neutral schemas can become a serious moat when real user data accumulates.",
        "decision": "Learn from the schema approach later, but keep SportRx 2.2 aerobic/hybrid measurement-first.",
        "status": "later",
        "boundary": "Do not start a resistance engine or strength-log converter now.",
    },
]


def build_open_source_integration_console() -> dict[str, Any]:
    """Summarize what SportRx adopted, deferred, and refused from GitHub scans."""

    adopted = [item for item in COMPARABLE_PROJECTS if item["status"] == "adopted"]
    later = [item for item in COMPARABLE_PROJECTS if item["status"] == "later"]
    integration_lanes = [
        {
            "id": "decision_support_traceability",
            "lane": "Decision Support Traceability",
            "borrow_from": "FitOntology",
            "sport_rx_action": "Every recommendation-like output should expose source labels, thresholds, missing tests, and blocked claims.",
            "status": "adopted",
        },
        {
            "id": "benchmark_log_contract",
            "lane": "Benchmark Log Contract",
            "borrow_from": "WODIS, ShredTrack, Ballast",
            "sport_rx_action": "Keep raw component results, units, RPE, equipment path, substitutions, protocol version, and local exports as the core data object.",
            "status": "adopted",
        },
        {
            "id": "fitt_vp_handoff",
            "lane": "FITT-VP Handoff",
            "borrow_from": "exercise-prescription-recommendation",
            "sport_rx_action": "Use FITT-VP only after measurement gates allow a conservative Starter Path.",
            "status": "adopted",
        },
        {
            "id": "event_specific_later",
            "lane": "Event-Specific Tools Later",
            "borrow_from": "HYROX-Pace, hyrox-race-insights",
            "sport_rx_action": "Retain HYROX language where useful, but defer race prediction, pacing, and official-readiness claims.",
            "status": "later",
        },
        {
            "id": "external_platform_later",
            "lane": "External Platforms Later",
            "borrow_from": "OpenAthlete, Claude Coach, Coach Paddy",
            "sport_rx_action": "Export local files first; connect platforms only after schemas survive self-use and alpha data.",
            "status": "later",
        },
        {
            "id": "protocol_documents",
            "lane": "Protocol Documents",
            "borrow_from": "Section 11",
            "sport_rx_action": "Keep benchmark protocol, evidence maps, bad-language checks, and Review Pack artifacts as first-class product surfaces.",
            "status": "adopted",
        },
        {
            "id": "pilot_data_capture",
            "lane": "Pilot Data Capture",
            "borrow_from": "REGmon, AthleteLoadMonitor, Athlete Report Generator",
            "sport_rx_action": "Treat forms, benchmark logs, weekly RPE, protocol deviations, and export reports as future alpha-dataset objects, while keeping safety, self-report, and measured performance separated.",
            "status": "adopted",
        },
    ]
    verified_sources = [
        {
            "source": "GitHub comparable-product scan",
            "date": "2026-08-22",
            "status": "product_research_only",
            "note": "Used to shape product architecture and UX boundaries, not scientific validity.",
        }
    ]
    rejected_boundaries = [
        "AI chat coach",
        "wearable readiness dashboard",
        "fake percentile benchmark",
        "race finish prediction",
        "social leaderboard",
        "medical risk percentage",
        "official event readiness label",
        "large exercise browser",
        "platform sync before stable local schemas",
    ]
    cards = [
        {
            "id": "measurement_records",
            "label": "Measurement Records",
            "value": "Adopted",
            "detail": "Benchmark Log keeps raw results, units, RPE, equipment, substitutions, notes, and protocol versions.",
            "status": "ready",
        },
        {
            "id": "source_labels",
            "label": "Metric Sources",
            "value": "Adopted",
            "detail": "User-facing outputs separate measured, self-reported, not-tested, ignored, and protocol-provenance fields.",
            "status": "ready",
        },
        {
            "id": "export_first",
            "label": "Export First",
            "value": "Adopted",
            "detail": "Local review packs, markdown reports, JSON/CSV logs, and session snapshots come before external integrations.",
            "status": "ready",
        },
        {
            "id": "traceable_decisions",
            "label": "Traceable Decisions",
            "value": "Adopted",
            "detail": "Open-source decision-support projects confirm that every output needs visible source rows, thresholds, and override boundaries.",
            "status": "ready",
        },
        {
            "id": "product_research_boundary",
            "label": "Research Boundary",
            "value": "Product only",
            "detail": "GitHub references guide UX and architecture; evidence claims still need the SportRx evidence pipeline.",
            "status": "ready",
        },
        {
            "id": "pilot_data_capture",
            "label": "Pilot Data Capture",
            "value": "Adopted",
            "detail": "Athlete-monitoring projects reinforce that forms, RPE, benchmark logs, and reports should become clean alpha data records.",
            "status": "ready",
        },
        {
            "id": "future_integrations",
            "label": "Future Integrations",
            "value": f"{len(later)} later",
            "detail": "Race split analysis and platform export wait until SportRx has stable schemas and real pilot data.",
            "status": "waiting",
        },
    ]

    return {
        "schema": "sportrx.open_source_integration_console",
        "schema_version": "0.1",
        "status": "architecture_positioned",
        "adopted_count": len(adopted),
        "later_count": len(later),
        "rejected_count": len(rejected_boundaries),
        "verified_sources": verified_sources,
        "cards": cards,
        "projects": COMPARABLE_PROJECTS,
        "integration_lanes": integration_lanes,
        "rejected_boundaries": rejected_boundaries,
        "primary_message": "SportRx borrows traceable decision support, measurement records, export formats, protocol documents, and station-level logging without becoming an AI coach, wearable dashboard, or HYROX race predictor.",
        "next_action": "Use this console to integrate only product mechanisms that make measurement more honest: source labels, benchmark logs, FITT-VP handoff, protocol documents, and export integrity before apps, wearables, race tools, or AI chat.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def open_source_integration_markdown(console: dict[str, Any]) -> str:
    """Export open-source integration notes as Markdown."""

    lines = [
        "# SportRx Open-Source Integration Notes",
        "",
        f"- Status: {console['status']}",
        f"- Adopted: {console['adopted_count']}",
        f"- Later: {console['later_count']}",
        f"- Explicitly rejected: {console['rejected_count']}",
        f"- Claim boundary: {console['claim_boundary']}",
        "",
        "## Source Boundary",
        "",
        "These GitHub references are comparable-product research. They can shape product architecture, UX, export formats, and scope boundaries. They do not validate SportRx rules, athlete outcomes, medical safety, or performance predictions.",
        "",
        "## Scan Record",
    ]
    for item in console["verified_sources"]:
        lines.extend(
            [
                "",
                f"- Source: {item['source']}",
                f"- Date: {item['date']}",
                f"- Status: {item['status']}",
                f"- Note: {item['note']}",
            ]
        )
    lines.extend(
        [
            "",
            "## Product Position",
            "",
            console["primary_message"],
            "",
            "## Adopted / Deferred Lessons",
        ]
    )
    for item in console["projects"]:
        lines.extend(
            [
                "",
                f"### {item['project']}",
                "",
                f"- Source: {item['url']}",
                f"- Category: {item['category']}",
                f"- Status: {item['status']}",
                f"- Lesson: {item['lesson']}",
                f"- SportRx decision: {item['decision']}",
                f"- Boundary: {item['boundary']}",
            ]
        )
    lines.extend(["", "## Integration Lanes"])
    for item in console["integration_lanes"]:
        lines.extend(
            [
                "",
                f"### {item['lane']}",
                "",
                f"- Borrow from: {item['borrow_from']}",
                f"- Status: {item['status']}",
                f"- SportRx action: {item['sport_rx_action']}",
            ]
        )
    lines.extend(["", "## Rejected Boundaries"])
    for item in console["rejected_boundaries"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Next Action", "", console["next_action"]])
    return "\n".join(lines) + "\n"
