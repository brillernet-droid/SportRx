import json

from sportrx.benchmark_log import (
    benchmark_profile_patch,
    benchmark_log_entry_contract_markdown,
    build_benchmark_import_compatibility,
    build_benchmark_log_entry_contract,
    build_component_result,
    compare_retest_sessions,
    create_benchmark_session,
    evaluate_benchmark_session_quality,
    export_sessions_csv,
    export_sessions_json,
    summarize_benchmark_sessions,
)
from sportrx.performance_lab import assess_hybrid_performance


def test_benchmark_session_stores_raw_results_without_score_claims():
    session = create_benchmark_session(
        {"age": 35, "equipment_access": ["row", "kettlebell"], "training_days": 3},
        [
            build_component_result("run_1km", value=360, value_unit="seconds", rpe_0_10=7),
            build_component_result("station_circuit", value=3, value_unit="rounds", rpe_0_10=6),
        ],
        session_date="2026-08-22",
    )

    assert session["schema"] == "sportrx.benchmark_session"
    assert session["completion"]["completed_components"] == 2
    assert session["component_results"][0]["value"] == 360
    assert "validated score" in session["claim_boundary"]
    assert "percentile" in session["claim_boundary"]
    assert session["session_quality"]["save_allowed"] is True
    assert session["import_compatibility"]["raw_only_count"] == 1


def test_benchmark_log_entry_contract_defines_component_specific_fields_and_boundaries():
    contract = build_benchmark_log_entry_contract(["row", "kettlebell"])

    assert contract["schema"] == "sportrx.benchmark_log_entry_contract"
    assert contract["benchmark_path"] == "standard"
    station = next(item for item in contract["components"] if item["component_id"] == "station_circuit")
    row_ski = next(item for item in contract["components"] if item["component_id"] == "row_or_ski_1km")

    assert station["primary_value_field"] == "rounds_completed"
    assert "score" in station["allowed_value_units"]
    assert "time_seconds" in station["companion_fields"]
    assert "loads_used" in station["companion_fields"]
    assert station["import_policy"] == "raw_rounds_only_unless_protocol_score"
    assert "0-100 score" in station["not_allowed"][0]
    assert row_ski["import_policy"] == "needs_row_or_ski_modality"

    markdown = benchmark_log_entry_contract_markdown(contract)
    assert "# SportRx Benchmark Log Entry Contract" in markdown
    assert "1 km row or 1 km ski" in markdown
    assert "Do not infer HYROX race readiness" in markdown


def test_component_result_preserves_structured_result_fields():
    result = build_component_result(
        "station_circuit",
        value=3,
        value_unit="rounds",
        rpe_0_10=6,
        result_fields={"rounds_completed": 3, "time_seconds": 420, "loads_used": "2 x 16 kg kettlebells"},
    )

    assert result["result_fields"]["time_seconds"] == 420
    session = create_benchmark_session({"equipment_access": ["kettlebell"]}, [result], session_date="2026-08-22")
    assert session["component_results"][0]["result_fields"]["loads_used"] == "2 x 16 kg kettlebells"
    exported_csv = export_sessions_csv([session])
    assert "result_fields" in exported_csv
    assert "loads_used" in exported_csv


def test_session_quality_flags_units_outside_entry_contract():
    quality = evaluate_benchmark_session_quality(
        [build_component_result("run_1km", value=360, value_unit="meters", rpe_0_10=7)],
        equipment_access=["row", "kettlebell"],
    )

    assert quality["save_allowed"] is False
    assert any("outside the component entry contract" in issue for issue in quality["issues"])


def test_benchmark_import_compatibility_marks_direct_hyrox_fields():
    compatibility = build_benchmark_import_compatibility(
        [
            build_component_result("run_1km", value=355, value_unit="seconds", rpe_0_10=7),
            build_component_result(
                "row_or_ski_1km",
                value=250,
                value_unit="seconds",
                rpe_0_10=8,
                equipment=["row"],
            ),
        ]
    )

    assert compatibility["status"] == "ready_for_hyrox_import"
    assert compatibility["hyrox_import_ready"] is True
    assert compatibility["importable_fields"] == ["one_km_row_seconds", "one_km_run_seconds"]
    assert compatibility["raw_only_count"] == 0


def test_benchmark_import_compatibility_keeps_rounds_raw_only():
    compatibility = build_benchmark_import_compatibility(
        [build_component_result("station_circuit", value=3, value_unit="rounds", rpe_0_10=6)]
    )

    assert compatibility["status"] == "raw_log_only"
    assert compatibility["hyrox_import_ready"] is False
    assert compatibility["raw_only"][0]["component_id"] == "station_circuit"
    assert compatibility["importable_fields"] == []


def test_benchmark_import_compatibility_requires_row_or_ski_modality():
    compatibility = build_benchmark_import_compatibility(
        [build_component_result("row_or_ski_1km", value=390, value_unit="seconds", rpe_0_10=8)]
    )

    assert compatibility["status"] == "needs_modality_detail"
    assert compatibility["needs_detail_count"] == 1
    assert "RowErg or SkiErg" in compatibility["needs_detail"][0]["reason"]


def test_benchmark_log_summary_requires_retest_for_comparison():
    first = create_benchmark_session(
        {"equipment_access": []},
        [build_component_result("run_1km_or_6min", value=1000, value_unit="meters", rpe_0_10=5)],
        session_date="2026-08-01",
    )
    second = create_benchmark_session(
        {"equipment_access": []},
        [build_component_result("run_1km_or_6min", value=1060, value_unit="meters", rpe_0_10=5)],
        session_date="2026-08-29",
    )

    assert summarize_benchmark_sessions([first])["retest_ready"] is False
    summary = summarize_benchmark_sessions([first, second])
    assert summary["retest_ready"] is True
    assert summary["session_count"] == 2
    assert "run_1km_or_6min" in summary["measured_components"]


def test_benchmark_log_exports_json_and_csv():
    session = create_benchmark_session(
        {"equipment_access": ["ski"]},
        [build_component_result("row_or_ski_1km", value=390, value_unit="seconds", rpe_0_10=8, equipment=["ski"])],
        session_date="2026-08-22",
    )

    exported_json = json.loads(export_sessions_json([session]))
    exported_csv = export_sessions_csv([session])

    assert exported_json["schema"] == "sportrx.benchmark_log_export"
    assert exported_json["sessions"][0]["component_results"][0]["component_id"] == "row_or_ski_1km"
    assert "component_id" in exported_csv
    assert "row_or_ski_1km" in exported_csv


def test_benchmark_profile_patch_imports_only_direct_compatible_measurements():
    session = create_benchmark_session(
        {"equipment_access": ["row", "kettlebell"]},
        [
            build_component_result("run_1km", value=355, value_unit="seconds", rpe_0_10=7),
            build_component_result("row_or_ski_1km", value=250, value_unit="seconds", rpe_0_10=8, equipment=["row"]),
            build_component_result("station_circuit", value=3, value_unit="rounds", rpe_0_10=6),
        ],
        session_date="2026-08-22",
    )

    result = benchmark_profile_patch([session])

    assert result["profile_patch"]["one_km_run_seconds"] == 355
    assert result["profile_patch"]["one_km_row_seconds"] == 250
    assert "station_test_score" not in result["profile_patch"]
    assert any("station_circuit" in item for item in result["skipped"])


def test_benchmark_profile_patch_carries_protocol_source_for_protocol_scores():
    session = create_benchmark_session(
        {"equipment_access": ["kettlebell"]},
        [build_component_result("station_circuit", value=72, value_unit="score", rpe_0_10=7)],
        session_date="2026-08-22",
        benchmark_path="standard",
        protocol_version="0.1",
    )

    result = benchmark_profile_patch([session])

    assert result["profile_patch"]["station_test_score"] == 72
    assert result["profile_patch"]["station_test_protocol"] == (
        "SportRx Hybrid Benchmark v1 0.1 / standard / Benchmark Log 2026-08-22"
    )
    assert "station_test_protocol" in str(result["applied"])


def test_benchmark_imported_protocol_source_makes_lab_record_review_ready():
    profile = {
        "age": 35,
        "training_days": 4,
        "weekly_training_minutes": 180,
        "running_minutes_per_week": 90,
        "available_days_per_week": 4,
        "max_minutes_per_session": 45,
        "symptoms": [],
        "known_conditions": [],
    }
    session = create_benchmark_session(
        {**profile, "equipment_access": ["row", "kettlebell"]},
        [
            build_component_result("run_1km", value=300, value_unit="seconds", rpe_0_10=7),
            build_component_result("station_circuit", value=72, value_unit="score", rpe_0_10=7),
        ],
        session_date="2026-08-22",
        benchmark_path="standard",
        protocol_version="0.1",
    )
    patch = benchmark_profile_patch([session])["profile_patch"]

    result = assess_hybrid_performance({**profile, **patch})

    assert result["lab_test_quality"]["status"] == "review_ready_measurement_record"
    assert result["lab_test_quality"]["missing_protocol_sources"] == []


def test_retest_comparison_uses_raw_direction_not_prediction():
    first = create_benchmark_session(
        {"equipment_access": ["row"]},
        [build_component_result("run_1km", value=370, value_unit="seconds", rpe_0_10=7)],
        session_date="2026-08-01",
    )
    second = create_benchmark_session(
        {"equipment_access": ["row"]},
        [build_component_result("run_1km", value=355, value_unit="seconds", rpe_0_10=7)],
        session_date="2026-08-29",
    )

    comparisons = compare_retest_sessions([first, second])

    assert comparisons[0]["component_id"] == "run_1km"
    assert comparisons[0]["delta"] == -15
    assert comparisons[0]["direction"] == "improved"
    assert "not a prediction" in comparisons[0]["claim_boundary"]


def test_retest_comparison_marks_changed_test_context_as_not_directly_comparable():
    first = create_benchmark_session(
        {"equipment_access": []},
        [
            build_component_result(
                "run_1km_or_6min",
                value=1000,
                value_unit="meters",
                rpe_0_10=6,
                protocol_context={"test_variant": "6min_run", "surface": "track"},
            )
        ],
        session_date="2026-08-01",
    )
    second = create_benchmark_session(
        {"equipment_access": []},
        [
            build_component_result(
                "run_1km_or_6min",
                value=1000,
                value_unit="meters",
                rpe_0_10=6,
                protocol_context={"test_variant": "1km_run", "surface": "track"},
            )
        ],
        session_date="2026-08-29",
    )

    comparison = compare_retest_sessions([first, second])[0]

    assert comparison["direction"] == "context_changed"
    assert "test_variant" in comparison["context_changes"]
    assert "not directly comparable" in comparison["claim_boundary"]


def test_session_quality_blocks_empty_measurement_log():
    quality = evaluate_benchmark_session_quality(
        [
            build_component_result("run_1km", completed=False, value=None, value_unit="seconds"),
            build_component_result("station_circuit", completed=False, value=None, value_unit="rounds"),
        ]
    )

    assert quality["save_allowed"] is False
    assert quality["status"] == "needs_review"
    assert quality["completed_components"] == 0
    assert quality["issues"]


def test_session_quality_warns_until_two_measured_areas_exist():
    quality = evaluate_benchmark_session_quality(
        [
            {**build_component_result("run_1km", value=360, value_unit="seconds", rpe_0_10=7), "area": "running"},
            build_component_result("station_circuit", completed=False, value=None, value_unit="rounds"),
        ]
    )

    assert quality["save_allowed"] is True
    assert quality["interpretation_ready"] is False
    assert quality["measured_area_count"] == 1
    assert any("two measured areas" in warning for warning in quality["warnings"])


def test_session_quality_marks_two_measured_areas_interpretation_ready():
    quality = evaluate_benchmark_session_quality(
        [
            {**build_component_result("run_1km", value=360, value_unit="seconds", rpe_0_10=7), "area": "running"},
            {
                **build_component_result("station_circuit", value=3, value_unit="rounds", rpe_0_10=6),
                "area": "strength_endurance",
            },
        ]
    )

    assert quality["save_allowed"] is True
    assert quality["interpretation_ready"] is True
    assert quality["measured_area_count"] == 2
