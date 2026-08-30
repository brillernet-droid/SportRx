from __future__ import annotations

from html import escape
import json
import os
import sys
from pathlib import Path
from typing import Any

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sportrx import (
    PROTOCOL_SOURCE_HELP,
    PROTOCOL_SOURCE_OPTIONS,
    alpha_dataset_csv_templates,
    alpha_dataset_dictionary_markdown,
    build_artifact_catalog,
    build_automation_guard,
    build_alpha_dataset_template,
    build_benchmark_import_compatibility,
    build_benchmark_log_entry_contract,
    build_readiness_passport,
    build_readiness_passport_card,
    build_benchmark_worksheet,
    build_sport_match_card,
    build_feedback_dashboard,
    build_launch_command_center,
    build_launch_readiness,
    build_language_edition_contract,
    build_measurement_timeline,
    build_measurement_schema_registry,
    build_demo_runbook,
    build_demo_experience_console,
    build_demo_scenario_matrix,
    build_demo_scenario_state,
    build_demo_scenarios,
    build_demo_state,
    build_evidence_coverage,
    build_evidence_library,
    build_export_bundle,
    build_first_run_guide,
    build_guided_review_console,
    build_input_ledger,
    build_intake_precision_audit,
    build_lab_readiness_console,
    knowledge_corpus_summary,
    build_open_source_integration_console,
    build_output_prerequisites,
    build_page_health_matrix,
    build_pilot_feedback_prompt,
    build_pilot_review_console,
    build_protocol_deviation_review,
    build_protocol_source_guide,
    build_public_beta_readiness,
    build_quick_match_intake_contract,
    build_quick_match_intake_quality,
    build_quick_match_lab_intake_sheet,
    build_release_candidate_summary,
    build_release_qa,
    build_release_package_manifest,
    build_review_pack_manifest,
    build_review_pack_zip,
    build_review_pack_integrity,
    build_retest_interpretation_guard,
    build_runtime_doctor,
    build_self_use_protocol,
    build_session_snapshot,
    build_session_quality_review,
    build_reviewer_session_plan,
    build_test_day_brief,
    build_test_session_operator,
    build_terminology_guide,
    build_training_profile_report,
    build_training_block,
    build_validation_readiness_matrix,
    build_venue_entry_assessment,
    build_walkthrough,
    build_test_day_command_board,
    benchmark_profile_patch,
    benchmark_log_entry_contract_markdown,
    benchmark_worksheet_markdown,
    compare_retest_sessions,
    create_benchmark_session,
    create_pilot_feedback_entry,
    evaluate_benchmark_session_quality,
    export_sessions_csv,
    export_sessions_json,
    export_pilot_feedback_json,
    feedback_dashboard_markdown,
    first_run_guide_markdown,
    guided_review_markdown,
    input_ledger_markdown,
    intake_precision_markdown,
    lab_readiness_markdown,
    language_edition_label,
    language_edition_markdown,
    language_edition_options,
    load_screening_providers,
    generate_prescription,
    get_benchmark_protocol,
    get_hybrid_benchmark,
    pilot_feedback_markdown,
    pilot_feedback_prompt_markdown,
    protocol_markdown,
    protocol_deviation_markdown,
    protocol_source_guide_markdown,
    public_beta_readiness_markdown,
    quick_match_intake_contract_markdown,
    quick_match_lab_intake_sheet_markdown,
    quick_match,
    search_knowledge,
    synthesize_knowledge,
    launch_readiness_markdown,
    measurement_timeline_markdown,
    measurement_schema_registry_markdown,
    demo_runbook_markdown,
    demo_experience_markdown,
    demo_scenario_matrix_markdown,
    evidence_coverage_markdown,
    evidence_library_markdown,
    open_source_integration_markdown,
    page_health_matrix_markdown,
    page_label,
    release_candidate_summary_markdown,
    release_qa_markdown,
    restore_session_snapshot,
    resolve_protocol_source_choice,
    resolve_protocol_source_value,
    report_markdown,
    reviewer_session_plan_markdown,
    review_pack_integrity_markdown,
    retest_interpretation_markdown,
    runtime_doctor_markdown,
    self_use_protocol_markdown,
    session_snapshot_json,
    session_snapshot_markdown,
    session_quality_review_markdown,
    test_day_brief_markdown,
    test_day_command_board_markdown,
    test_session_operator_markdown,
    terminology_markdown,
    summarize_benchmark_sessions,
    summarize_pilot_feedback,
    training_block_markdown,
    ui_text,
    validation_readiness_markdown,
    validate_knowledge_records,
)
from sportrx.benchmark_log import build_component_result
from sportrx.performance_lab import assess_hybrid_performance, measurement_intake_matrix_csv, measurement_intake_matrix_markdown
from sportrx.release_qa import REQUIRED_EVIDENCE_FILES


DEFAULT_PROFILE = {
    "age": 35,
    "sex": "female",
    "height_cm": 165,
    "weight_kg": 68,
    "training_days": 3,
    "weekly_training_minutes": 120,
    "exercise_days_last_4w": 3,
    "mvpa_minutes_per_week": 120,
    "available_days_per_week": 3,
    "max_minutes_per_session": 45,
    "running_minutes_per_week": 60,
    "longest_continuous_run_minutes": 20,
    "strength_days_per_week": 1,
    "high_intensity_sessions_last_4w": 2,
    "loaded_movement_sessions_last_4w": 2,
    "preferred_activity": "brisk walking",
    "primary_goal": "first finish",
    "goal": "Improve aerobic fitness / general health",
    "symptoms": [],
    "known_conditions": [],
}


V01_DEFAULT_PROFILE = {
    "age": 30,
    "resting_hr": 0,
    "exercise_days_last_4w": 0,
    "mvpa_minutes_per_week": 0,
    "available_days_per_week": 3,
    "max_minutes_per_session": 30,
    "preferred_activity": "brisk walking",
    "goal": "Improve aerobic fitness / general health",
    "symptoms": [],
    "known_conditions": [],
}

V01_ACTIVITY_LABELS = {
    "brisk walking": "快走",
    "easy jogging": "轻松慢跑",
    "cycling": "骑行",
    "elliptical": "椭圆机",
}

V01_INTENSITY_LABELS = {
    "light": "轻松",
    "light_to_moderate": "轻松到中等",
    "moderate": "中等",
}

V01_FITNESS_LABELS = {
    "inactive": "目前运动不足",
    "low_active": "已有一些运动基础",
    "active": "已较规律运动",
}

V01_TALK_TESTS = {
    "light": "可以轻松完整对话。",
    "light_to_moderate": "可以较舒适地说话；接近上限时唱歌会变得困难。",
    "moderate": "可以说话，但唱歌会比较困难。",
}

SYMPTOM_LABELS = {
    "chest_pain": "运动时胸痛、胸闷或压迫感",
    "unexplained_shortness_of_breath": "不明原因气短",
    "dizziness_or_syncope": "头晕、晕厥或眼前发黑",
    "palpitations": "异常心悸",
    "pain_with_walking": "走路时出现异常疼痛",
}

CONDITION_LABELS = {
    "cardiovascular_disease": "心血管疾病",
    "metabolic_disease": "代谢性疾病",
    "renal_disease": "肾脏疾病",
    "pulmonary_disease": "肺部疾病",
}

ZH_VALUE_MAP = {
    "Hybrid Race": "HYROX / Hybrid Race",
    "5K/10K Running": "5K/10K 跑步",
    "measure_first": "Measure First",
    "benchmark_underway": "Benchmark Underway",
    "complete_loop": "Complete Loop",
    "enabled": "已开放",
    "registry_ready": "候补",
    "Strong current fit": "当前很适合",
    "Good current fit": "当前比较适合",
    "Some preparation needed": "需要一些准备",
    "More preparation needed": "还需要更多准备",
    "first finish": "先完成一次",
    "improve performance": "提升表现",
    "understand profile": "了解当前状态",
    "build health": "改善健康",
    "general hybrid starter": "综合基础型",
    "first-challenge builder": "First-race builder",
    "performance-oriented recreational athlete": "表现提升型",
    "strength-leaning hybrid starter": "力量基础偏强",
    "endurance-leaning hybrid starter": "耐力基础偏强",
    "Balanced": "比较均衡",
    "Still being mapped": "还需要测试",
    "Running-dominant": "跑步基础偏强",
    "Strength-dominant": "力量耐力偏强",
    "Work-capacity dominant": "Work capacity 偏强",
    "Not enough measured data": "实测数据不足",
    "Training handoff blocked": "暂不生成训练",
    "Benchmark needed before tailored training": "需要先完成 Benchmark",
    "Starter Path available": "Starter Path 可用",
    "Strong current profile": "当前准备较充分",
    "Well prepared": "准备情况较好",
    "Building": "正在建立基础",
    "Early stage": "早期阶段",
    "Running": "跑步",
    "Aerobic fitness": "有氧基础",
    "Strength endurance": "力量耐力",
    "Station experience": "Station experience",
    "Work capacity": "Work capacity",
    "Strong current area": "当前较强",
    "Good base": "基础较好",
    "Developing": "正在发展",
    "Needs more work": "需要加强",
    "Not tested": "未测试",
    "No single dominant gap identified": "暂未发现单一主要短板",
    "Not enough information": "信息不足",
    "No single main gap from quick check": "快速匹配暂未发现单一短板",
    "Balanced from quick check": "快速匹配显示较均衡",
    "training consistency": "训练规律性",
    "weekly training volume": "每周训练量",
    "running volume": "每周跑/快走量",
    "longest continuous run": "最长连续跑/快走",
    "strength frequency": "力量训练频率",
    "high-intensity exposure": "高强度训练次数",
    "loaded movement exposure": "负重动作次数",
    "measured": "实测",
    "self_reported": "自报",
    "reported_training": "自报训练",
    "estimated": "估算",
    "not_tested": "未测试",
    "missing": "未测试",
    "safety_screen": "安全筛查",
    "unsupported": "未使用",
    "Measured": "实测",
    "Self-reported": "自报",
    "Estimated": "估算",
    "Derived from SportRx rules": "SportRx 规则推导",
    "Not tested": "未测试",
    "Safety screen": "安全筛查",
    "Protocol provenance": "Protocol 来源",
    "Not used": "未使用",
    "ADVERSE_EVENT_REPORTED": "记录到不良事件",
    "HIGH_COMPLETION_LOW_RPE": "完成率高，RPE 偏低",
    "HIGH_COMPLETION_TARGET_RPE": "完成率高，RPE 在目标区间",
    "LOW_COMPLETION_HIGH_RPE": "完成率低，RPE 偏高",
    "FEEDBACK_INCOMPLETE": "反馈未完整填写",
    "FELT_TOO_HARD": "本周主观感觉偏难",
    "COMPLETION_BELOW_TARGET": "完成率低于目标",
    "RPE_ABOVE_TARGET": "RPE 高于目标区间",
    "RPE_BELOW_TARGET": "RPE 低于目标区间",
    "HOLD_FOR_STABILITY": "先维持以观察稳定性",
    "PROVISIONAL_NO_FEEDBACK": "未填写反馈的预览进阶",
    "active": "可用",
    "ready": "已就绪",
    "complete": "已完成",
    "recommended": "建议查看",
    "needs_setup": "待设置",
    "needs_measurement": "待测试",
    "not_started": "未开始",
    "waiting": "等待中",
    "blocked": "被阻断",
    "no_log_yet": "等待记录",
    "limited_report": "报告受限",
    "blocked_by_measurement_gate": "测量门控",
    "awaiting_feedback_or_retest": "等待反馈/复测",
    "nothing_to_export_yet": "暂无可导出材料",
    "qa_needs_demo_loop": "等待完整 demo",
    "blocked_by_measurement": "等待测量",
    "provisional": "预览状态",
    "waiting_for_retest": "等待复测",
    "usable_behavior_snapshot": "可用于行为粗筛",
    "needs_more_behavior_context": "需要更多训练行为信息",
    "ready_for_quick_match_routing": "可用于 Quick Match 路线粗筛",
    "low_behavior_signal": "行为信号较少",
    "waiting_for_measured_tests": "等待实测测试",
    "needs_protocol_source": "需要 protocol 来源",
    "needs_more_measured_areas": "需要更多实测区域",
    "needs_more_measured_dimensions": "需要更多实测维度",
    "measurement_matrix_ready": "测量矩阵可用于交接",
    "review_ready_measurement_record": "测量记录可复查",
    "Resolve Safety Gate before Quick Match routing or training handoff.": "先处理 Safety Gate，再进行 Quick Match 路线粗筛或训练交接。",
    "Complete the missing recent-behavior fields before using Quick Match.": "先补齐缺失的近期训练行为字段，再使用 Quick Match。",
    "Use Quick Match only as a sparse intake record and route to SportRx Hybrid Benchmark v1.": "仅把 Quick Match 当作稀疏 intake 记录，先进入 SportRx Hybrid Benchmark v1。",
    "Use this intake for rough routing, then continue to HYROX Check or Benchmark Protocol for measured data.": "这份 intake 可用于路线粗筛；随后进入 HYROX Check 或 Benchmark Protocol 获取实测数据。",
    "Resolve Safety Gate before interpreting lab test quality.": "先处理 Safety Gate，再解释 Lab test quality。",
    "Complete at least one SportRx Hybrid Benchmark component before interpreting lab quality.": "至少完成一个 SportRx Hybrid Benchmark 组件后，再解释 lab quality。",
    "Add protocol source for station or work-capacity score fields before treating them as review-ready.": "Station 或 Work capacity 分数字段需要补 protocol 来源，之后才可视为 review-ready。",
    "Record at least two measured performance areas before strongest-area and main-gap comparison.": "至少记录两个实测表现区域后，再比较 strongest area 和 main gap。",
    "Keep units, protocol source, and test order stable for retest comparison.": "保持单位、protocol 来源和测试顺序稳定，方便复测比较。",
    "Resolve Safety Gate before training handoff; measured values remain unchanged.": "先处理 Safety Gate；已记录的实测值保持不变。",
    "Add protocol source for Station circuit or Work capacity before review handoff.": "交接前补充 Station circuit 或 Work capacity 的 protocol 来源。",
    "Measure at least two performance dimensions before comparing strongest area and main gap.": "至少测量两个表现维度后，再比较 strongest area 和 main gap。",
    "Use the matrix for Training Profile handoff and keep the same protocol for retest.": "可以用该矩阵交接到 Training Profile；复测时保持同一 protocol。",
    "Safety Gate": "Safety Gate",
    "Behavior Snapshot": "行为快照",
    "Active Signals": "有效行为信号",
    "Time Constraints": "时间约束",
    "Legacy Ignored": "旧字段已忽略",
    "Measurement Route": "测量路径",
    "Benchmark required": "需要 Benchmark",
    "Measure-first status": "Measure-first status",
    "Next best action": "下一步",
    "Measured picture": "当前实测图像",
    "Benchmark log": "Benchmark Log",
    "Training handoff": "训练交接",
    "Gated": "门控中",
    "Separate from performance scoring.": "与表现评分分离。",
    "Missing tests stay Not tested.": "缺失测试保持 Not tested。",
    "Generated only after safety and measurement gates allow it.": "只有安全门和测量门允许后才生成。",
    "Safety Gate can block training handoff, but it never changes measured performance.": "Safety Gate 可以阻断训练交接，但不会改变实测表现。",
    "Measure at least two performance dimensions before comparing strongest area and main gap.": "至少测量两个表现维度后，再比较 strongest area 和 main gap。",
    "Save raw component results, units, RPE, equipment, substitutions, and notes.": "保存原始 component 结果、单位、RPE、器械、替代动作和备注。",
    "Training handoff remains gated until Safety and measurement prerequisites are satisfied.": "Safety 和测量前置条件满足前，训练交接保持门控。",
    "Use the current measured picture for a conservative block, then retest with the same protocol.": "用当前 measured picture 生成保守训练 block，然后按同一 protocol 复测。",
    "ready_for_self_report_routing": "自报路线粗筛可用",
    "Use this self-reported intake for rough routing, then test in Benchmark.": "这份自报 intake 可用于路线粗筛；之后进入 Benchmark 做实测。",
    "Self-report routing ready": "自报路线粗筛可用",
    "Direct-number intake": "直接数字 intake",
    "Measured performance": "实测表现",
    "Missing-data rule": "缺失数据规则",
    "Next step": "下一步",
    "0 used": "0 个被使用",
    "No imputation": "不补值",
    "Age, recent behavior, and time constraints are entered as numbers instead of vague background labels.": "年龄、近期行为和时间约束都用数字记录，不用模糊 background 标签。",
    "1 km, 5 km, RowErg, SkiErg, station, and work-capacity tests are excluded from Quick Match.": "1 km、5 km、RowErg、SkiErg、station 和 work-capacity 测试不进入 Quick Match。",
    "Missing or untested performance data stays Not tested; SportRx does not fill midpoint or average values.": "缺失或未测试的表现数据保持 Not tested；SportRx 不填中点或平均值。",
    "ready_for_operator": "现场测试可执行",
    "Preflight": "测试前检查",
    "Component sequence": "组件顺序",
    "Record now": "立即记录",
    "Benchmark Log handoff": "Benchmark Log 交接",
    "Test-Day Command Board": "Test-Day Command Board",
    "7 fields": "7 个字段",
    "Safety Gate, protocol lock, and warm-up must be checked before component testing.": "组件测试前必须完成 Safety Gate、protocol 锁定和热身检查。",
    "Every completed component needs raw value, unit, RPE, equipment context, substitutions, and notes.": "每个已完成组件都需要原始值、单位、RPE、器械语境、替代动作和备注。",
    "Save the raw session before importing compatible fields or interpreting retest change.": "先保存 raw session，再导入兼容字段或解释复测变化。",
    "Test-Day Command Board turns the benchmark protocol into a local operator workflow: preflight, component tests, raw recording, log handoff, and retest anchor.": "Test-Day Command Board 把 benchmark protocol 变成现场执行流程：测试前检查、组件测试、原始记录、log 交接和复测锚点。",
    "Confirm Safety Gate, lock protocol, and complete warm-up.": "确认 Safety Gate，锁定 protocol，并完成热身。",
    "Safety Gate status, protocol version, equipment path, route/machine/load notes.": "记录 Safety Gate 状态、protocol 版本、器械路径、路线 / 机器 / 负重备注。",
    "Run recommended components in order; optional components can remain Not tested.": "按顺序完成 recommended components；optional components 可以保持 Not tested。",
    "Raw result, unit, RPE, equipment, substitutions, and notes after each component.": "每个组件结束后记录原始结果、单位、RPE、器械、替代动作和备注。",
    "Save Benchmark Log before using results elsewhere.": "在其它页面使用结果前，先保存 Benchmark Log。",
    "Session-level notes, protocol deviations, and component rows.": "记录 session 级备注、protocol 偏离和 component rows。",
    "Retest with the same route, equipment, loads, and order before comparing change.": "比较变化前，使用相同路线、器械、负重和顺序复测。",
    "Retest setup notes and comparable component IDs.": "记录复测设置说明和可比较 component IDs。",
    "First-screen operator summary for preflight, component tests, raw recording, log handoff, and retest anchor.": "测试前检查、组件测试、原始记录、log 交接和复测锚点的一屏式 operator 摘要。",
    "Required": "必须",
    "Timed Tests": "计时测试",
    "Protocol Scores": "Protocol 分数",
    "Protocol Sources": "Protocol 来源",
    "Comparison Gate": "比较门控",
    "Open": "已打开",
    "Complete": "已完整",
    "Waiting": "等待中",
    "Safety can block routing, but never changes performance scores.": "Safety Gate 可以阻断路线和训练交接，但不会改变表现分。",
    "Recent days, minutes, run/walk exposure, strength, high-intensity, and loaded movement fields.": "近期训练天数、分钟数、跑走暴露、力量、高强度和负重动作字段。",
    "Zero is valid, but many zeros mean Quick Match is low-signal and should route to Benchmark first.": "0 是有效输入；但多个 0 表示 Quick Match 信号较少，应先进入 Benchmark。",
    "Future days and session length constrain training blocks; they are not performance advantages.": "未来可训练天数和单次时长只约束训练 block，不是表现优势。",
    "Subjective background / comfort fields are preserved only as ignored legacy compatibility data.": "主观 background / comfort 字段只作为已忽略的旧版兼容数据保留。",
    "Quick Match never replaces HYROX Check or SportRx Hybrid Benchmark v1 measured results.": "Quick Match 不替代 HYROX Check 或 SportRx Hybrid Benchmark v1 的实测结果。",
    "Run, RowErg, and SkiErg entries are raw timed fields.": "Run、RowErg 和 SkiErg 是原始计时字段。",
    "Station and work-capacity scores must come from a named protocol or Benchmark Log.": "Station 和 Work capacity 分数必须来自具名 protocol 或 Benchmark Log。",
    "Protocol provenance is required before protocol scores affect measured performance.": "Protocol 来源是 protocol 分数进入 measured performance 的前置条件。",
    "At least two measured performance areas are required before comparing strongest area and main gap.": "至少两个实测表现区域后，才比较 strongest area 和 main gap。",
    "Safety can block interpretation, but never raises or lowers measured performance.": "Safety Gate 可以阻断解释，但不会提高或降低实测表现。",
    "standard timed field": "标准计时字段",
    "ready_to_log": "可以记录测试",
    "ready_for_training_handoff": "可以进入训练交接",
    "ready_for_retest_review": "可以查看复测",
    "ready_for_test_day": "可以开始测试",
    "blocked_by_safety_gate": "Safety Gate 阻断",
    "low_equipment": "Low-equipment path",
    "standard": "Standard path",
    "recommended": "建议完成",
    "optional": "可选",
    "required": "必须完成",
    "preflight": "测试前",
    "component": "测试组件",
    "handoff": "交接",
    "strength_endurance": "力量耐力",
    "work_capacity": "Work capacity",
    "Ready": "就绪",
    "Blocked": "被阻断",
    "Run the steps in order, then save results in Benchmark Log.": "按顺序完成测试，然后保存到 Benchmark Log。",
    "Resolve Safety Gate before running the operator.": "先处理 Safety Gate，再开始现场测试。",
    "Complete at least one Benchmark component before checking HYROX import compatibility.": "至少完成一个 Benchmark component 后，再检查 HYROX 导入兼容性。",
    "Import the compatible fields and keep the rest as raw Benchmark Log data.": "导入兼容字段，其余保留为 raw Benchmark Log。",
    "These measured fields can be imported into HYROX Check after saving.": "保存后，这些实测字段可以导入 HYROX Check。",
    "Add RowErg/SkiErg modality or substitution detail before importing.": "导入前补充 RowErg / SkiErg modality 或替代说明。",
    "Save as raw Benchmark Log first; do not create artificial HYROX Check fields.": "先保存为 raw Benchmark Log，不创建人工 HYROX Check 字段。",
    "At least one completed component with a raw value is required before saving a Benchmark Log.": "保存 Benchmark Log 前，至少需要一个已完成组件和原始结果。",
    "At least two measured areas are recommended before interpreting strongest area vs main gap.": "建议至少两个实测 area 后，再解释 strongest area 和 main gap。",
    "Session quality checks review data completeness only. They are not performance scores or validation claims.": "Session quality checks 只检查数据完整性，不是表现分或验证结论。",
    "Build 4-week Starter Path": "生成 4-week Starter Path",
    "Complete SportRx Hybrid Benchmark v1": "完成 SportRx Hybrid Benchmark v1",
    "Complete the SportRx Hybrid Benchmark.": "完成 SportRx Hybrid Benchmark。",
    "Keep training consistent for the next 4 weeks.": "未来 4 周保持训练稳定。",
    "Retest the same benchmark before changing the focus.": "调整重点前先按同一 Benchmark 复测。",
    "Compromised running or mixed-work test": "Compromised run 或 mixed-work 测试",
    "No recent 1 km or 5 km run test": "暂无近期 1 km 或 5 km 跑步测试",
    "No station or strength-endurance test": "暂无 station 或 strength-endurance 测试",
    "No RowErg, SkiErg, or station-specific test": "暂无 RowErg、SkiErg 或 station-specific 测试",
    "No compromised running or mixed-work test": "暂无 compromised run 或 mixed-work 测试",
    "1 km or 5 km run benchmark": "1 km 或 5 km 跑步 Benchmark",
    "Station strength-endurance circuit": "Station strength-endurance circuit",
    "Row/Ski or low-equipment station substitute": "Row/Ski 或低器械 station 替代测试",
    "Retest anchor": "复测锚点",
    "Station practice": "Station practice",
    "Aerobic base": "有氧基础",
    "Controlled mixed work": "受控 mixed work",
    "Build consistency": "建立训练稳定性",
    "Practice repeatability": "练习可重复执行",
    "Prepare for retest": "准备复测",
    "brisk walking": "快走",
    "running": "跑步",
    "jogging": "慢跑",
    "cycling": "骑行",
    "Monday": "周一",
    "Tuesday": "周二",
    "Wednesday": "周三",
    "Thursday": "周四",
    "Friday": "周五",
    "Saturday": "周六",
    "Sunday": "周日",
    "Keep a balanced week": "保持均衡训练周",
    "Add one benchmark you have not tested yet": "补测一个尚未完成的 Benchmark",
    "Repeat the same training rhythm": "保持相同训练节奏",
    "Retest the weakest measured area": "复测当前最需要关注的区域",
    "Keep the session repeatable.": "保持每次训练可重复。",
    "Do not add intensity and volume at the same time.": "不要同时增加强度和训练量。",
    "Use RPE to keep the work controlled.": "用 RPE 控制训练负荷。",
    "Retest one area with the same setup.": "用同一设置复测一个区域。",
    "Record completed sessions, average RPE, and whether the week felt too hard.": "记录完成次数、平均 RPE，以及本周是否明显偏难。",
    "Keep this repeatable; record completion and session RPE after training.": "保持可重复；训练后记录完成情况和 session RPE。",
    "measurement_in_progress": "测量进行中",
    "needs_equipment_path": "请选择器械路径",
    "blocked_by_safety_gate": "Safety Gate 阻断",
    "standard": "Standard path",
    "low_equipment": "Low-equipment path",
    "ready_to_save": "可以保存",
    "needs_review": "需要补齐",
    "not_reviewed": "未检查",
    "ready_for_hyrox_import": "可导入 HYROX Check",
    "partial_import_ready": "部分可导入",
    "needs_modality_detail": "需要 Row/Ski 细节",
    "raw_log_only": "仅保留 raw log",
    "no_completed_results": "暂无完成结果",
    "importable": "可导入",
    "needs_detail": "需要补充细节",
    "raw_only": "仅原始记录",
    "not_measured": "未测量",
    "Save allowed": "允许保存",
    "Needs review": "需要检查",
    "Wait": "等待解释",
    "Available": "可生成",
    "Blocked": "暂不生成",
    "Required": "需要记录",
    "No weekly feedback recorded": "尚未记录周反馈",
    "On track": "按计划进行",
    "Needs review": "需要复查",
    "Pause and review": "暂停并复查",
    "Measurement gate": "测量门控",
    "No active training plan is available.": "当前没有可执行训练计划。",
    "No feedback yet": "尚未反馈",
    "No retest yet": "尚未复测",
    "Retest ready": "已有复测",
    "Rule-coded": "规则编码",
    "Increase dose": "增加训练量",
    "Small increase": "小幅进阶",
    "Decrease dose": "降低训练量",
    "Hold current dose": "维持当前剂量",
    "Pause automated progression": "暂停自动进阶",
    "Not entered": "未填写",
    "Enter Hybrid Race Performance Lab": "进入 HYROX Check",
    "Join the 5K/10K registry waitlist": "暂存为 5K/10K registry 候选",
    "Recent running/walking exposure is close to this challenge": "近期跑步/快走暴露接近这个挑战",
    "More weekly running/walking volume": "需要更多每周跑步/快走量",
    "Longer continuous run/walk exposure": "需要更长连续跑步/快走暴露",
    "More weekly strength training exposure": "需要更多每周力量训练暴露",
    "More recent high-intensity exposure": "需要更多近期高强度训练暴露",
    "More recent loaded movement exposure": "需要更多近期负重动作暴露",
    "More running-specific practice": "需要更多跑步专项练习",
    "increase": "增加",
    "small_increase": "小幅进阶",
    "decrease": "降低",
    "hold": "维持",
    "pause": "暂停",
    "not_entered": "未填写",
    "Completion was high and RPE was below the target range.": "完成率较高且 RPE 低于目标区间，因此可以增加训练量。",
    "Completion was high and RPE stayed in an appropriate range.": "完成率较高且 RPE 处在适宜区间，因此可以小幅进阶。",
    "Completion was low and perceived difficulty was high.": "完成率较低且主观难度偏高，因此应降低训练量。",
    "Feedback suggests holding the current dose before progressing.": "反馈提示先维持当前训练剂量，等它更稳定后再进阶。",
    "An adverse symptom/event was reported, so automatic adjustment is paused.": "记录到警示症状或不良事件，因此暂停自动调整。",
    "Plan-actual reason codes explain rule-based weekly adjustment only. They are not recovery scores, risk predictions, or medical advice.": "Plan-actual reason codes 只解释基于规则的周调整，不是恢复评分、风险预测或医疗建议。",
    "needs_more_feedback": "需要更多反馈",
    "ready_for_pattern_review": "可以查看反馈模式",
    "needs_release_fix": "发布门控未通过",
    "limited_review_ready_collect_pilot_feedback": "可小范围试用，继续收集反馈",
    "pilot_feedback_needs_review": "Pilot Feedback 需要复查",
    "public_beta_candidate": "Public Beta 候选",
    "Fix release, runtime, package, runbook, or evidence gates before inviting outside reviewers.": "先修复 Release、Runtime、Package、Runbook 或 Evidence 门控，再邀请外部 reviewer。",
    "Run limited reviewer sessions and collect at least five local pilot feedback entries before public beta messaging.": "先进行小范围 reviewer 试用，并收集至少 5 条本地 Pilot Feedback，再对外称为 Public Beta。",
    "Review low-scoring pilot feedback fields before calling this a public beta candidate.": "先复查低评分 Pilot Feedback 字段，再称为 Public Beta candidate。",
    "Export the review pack and public package, then run the planned public beta review.": "导出 Review Pack 和 Public Package，然后按计划进行 Public Beta review。",
    "Runtime is ready for local reviewers": "Runtime 可供本地 reviewer 使用",
    "Release QA is complete": "Release QA 已完成",
    "Launch readiness is complete": "Launch Readiness 已完成",
    "Public package is clean": "Public Package 干净",
    "Demo runbook is ready": "Demo Runbook 已就绪",
    "Evidence context is present": "Evidence Context 已就绪",
    "Pilot feedback has enough entries for pattern review": "Pilot Feedback 条目足够进行模式复查",
    "Pilot feedback has no low-rating flags": "Pilot Feedback 没有低评分警报",
    "Runtime": "Runtime",
    "Release QA": "Release QA",
    "Launch": "Launch",
    "Public Package": "Public Package",
    "Evidence": "Evidence",
    "Pilot Feedback": "Pilot Feedback",
    "Pilot Flags": "Pilot Flags",
    "Claim Boundary": "Claim Boundary",
    "Product gate only": "仅产品发布门控",
    "No low-rating fields flagged.": "没有低评分字段被标记。",
    "Collect at least five local entries before reviewing pilot feedback flags.": "至少收集 5 条本地反馈后，再复查 Pilot Feedback flags。",
    "Not enough data": "数据不足",
    "First setup clarity": "首次设置清晰度",
    "Measurement realism": "测量真实感",
    "Trust in the explanation": "解释可信度",
    "Next-action clarity": "下一步清晰度",
    "Visual polish": "视觉完成度",
    "Collect the first local product-review entry after a guided demo.": "完成一次 guided demo 后，先收集第一条本地产品反馈。",
    "Collect at least five entries before looking for product-review patterns.": "至少收集 5 条反馈后，再看产品模式。",
    "Review low-scoring fields before public beta messaging.": "公开 beta 前先检查低评分维度。",
    "Review comments and export the local pilot feedback bundle.": "查看评论并导出本地 pilot feedback bundle。",
    "Local product-review entries only.": "仅表示本地产品试用反馈条目。",
    "Average across current rating fields.": "当前评分字段的平均值。",
    "Use this to prioritize product fixes, not validation claims.": "用于排序产品修正，不用于验证声明。",
    "Fields below 3.5 should be inspected before broader sharing.": "低于 3.5 的字段应在更大范围分享前检查。",
    "Qualitative comments explain rating patterns.": "开放评论用于解释评分模式。",
    "Contact information is stored only when consent is checked.": "只有勾选同意后才保存联系方式。",
    "Only generated after Safety Gate and measurement gates allow it.": "只有 Safety Gate 和测量门控都允许后才生成。",
    "Training focus comes from measured main gap, not a chat prompt.": "训练重点来自实测 main gap，不来自聊天式建议。",
    "SportRx keeps this as a short starter block before retest.": "SportRx 先保持短周期 starter block，再复测。",
    "Each session keeps duration, RPE, talk test, and execution notes.": "每次训练保留时长、RPE、talk test 和执行说明。",
    "Volume is constrained by current profile and stated time capacity.": "训练量受当前状态和可用时间约束。",
    "Weekly completion and RPE decide hold/progress/reduce.": "每周完成率和 RPE 决定维持、进阶或降低。",
    "可以执行，但每周必须记录 RPE 和完成率。": "可以执行，但每周必须记录 RPE 和完成率。",
    "A raw Benchmark Log needs at least one completed component with a raw value.": "Raw Benchmark Log 至少需要一个已完成组件和原始结果。",
    "Completed components with a usable raw value.": "已完成且有可用原始结果的组件。",
    "At least two measured areas are recommended before interpreting gap direction.": "建议至少两个实测 area 后再解释短板方向。",
    "Interpretation readiness is not validation or prediction.": "可解释不等于科学验证或预测。",
    "Issues block saving; warnings preserve uncertainty.": "Issues 会阻止保存；warnings 用来保留不确定性。",
    "eligible_for_gap_comparison": "可用于短板比较",
    "context_or_not_tested": "背景信息或未测试",
    "not_collected": "未填写",
    "not_tested": "未测试",
    "not_applicable": "不适用",
    "collected": "已填写",
    "self_reported": "自报",
    "measured": "实测",
    "measured_review_ready": "实测，可复查",
    "measured_needs_protocol": "实测，缺 protocol",
    "protocol_score": "Protocol 分数字段",
    "accepted_preset": "可用 preset",
    "accepted_with_note": "需记录说明",
    "protocol_sources_ready": "Protocol 来源已就绪",
    "waiting_for_protocol_scores": "等待 protocol 分数",
    "source_recorded": "来源已记录",
    "source_required": "需要来源",
    "not_required": "暂不需要",
    "raw_timed_field": "原始计时字段",
    "protocol_recorded": "已记录 protocol",
    "missing_protocol_source": "缺 protocol 来源",
    "Tests with actual values saved in the current profile.": "当前 profile 中已有实测数值的测试。",
    "Missing components stay explicit; they are not replaced by defaults.": "缺失组件保持明确未测，不用默认值替代。",
    "Measured fields with raw timed values or recorded protocol provenance.": "已有原始计时值或已记录 protocol 来源的实测字段。",
    "Station and Work capacity scores need a named protocol source.": "Station 和 Work capacity 分数需要命名 protocol 来源。",
    "Run this component through SportRx Hybrid Benchmark v1 or save it in Benchmark Log.": "通过 SportRx Hybrid Benchmark v1 测这个组件，或先保存到 Benchmark Log。",
    "Add the protocol source before treating this record as review-ready.": "补充 protocol 来源后，才把这条记录视为 review-ready。",
    "Keep the same unit, setup, and protocol for retest.": "复测时保持同一单位、设置和 protocol。",
    "Measured Tests": "已完成测试",
    "Measured Areas": "实测表现区域",
    "Not Tested": "未测试项目",
    "Self-reported Context": "自报训练背景",
    "Safety Boundary": "安全边界",
    "1 km run": "1 km run",
    "5 km run": "5 km run",
    "1 km RowErg": "1 km RowErg",
    "1 km SkiErg": "1 km SkiErg",
    "Station circuit": "Station circuit",
    "Work capacity": "Work capacity",
    "Training days": "每周训练天数",
    "Weekly training volume": "每周训练量",
    "Running volume": "跑步训练量",
    "Safety can block handoff, but never raises or lowers measured performance.": "Safety Gate 可以阻断训练交接，但不会提高或降低实测表现。",
    "Only completed tests are counted; blanks remain Not tested.": "只统计已完成测试；空白项目保持 Not tested。",
    "At least two measured performance areas are needed for strongest/gap comparison.": "至少两个实测表现区域后，才比较 strongest area 和 main gap。",
    "Missing tests are not replaced by average, midpoint, or fake benchmark values.": "缺失测试不会用平均值、中点或虚构 benchmark 数值补齐。",
    "Context can shape feasibility and aerobic-base context; it is not measured performance.": "训练背景会影响可行性和有氧基础语境，但不是实测表现。",
    "Resolve Safety Gate before automated training handoff.": "先处理 Safety Gate，再进行自动训练交接。",
    "Complete at least two measured performance dimensions before comparing strongest area and main gap.": "至少完成两个实测表现维度，再比较 strongest area 和 main gap。",
    "Comparison gate is open; keep protocol and units repeatable for retest.": "比较门已打开；后续复测要保持 protocol 和单位一致。",
    "Measured running capacity input.": "跑步能力实测输入。",
    "Measured station-specific erg input.": "Station-specific erg 实测输入。",
    "Measured station or strength-endurance input.": "Station 或 strength endurance 实测输入。",
    "Measured compromised or mixed-work capacity input.": "Compromised / mixed-work capacity 实测输入。",
    "Not reported": "未填写",
    "0 sessions in last 4 weeks": "过去 4 周 0 次",
    "1 session(s) in last 4 weeks": "过去 4 周 1 次",
    "2 session(s) in last 4 weeks": "过去 4 周 2 次",
    "3 session(s) in last 4 weeks": "过去 4 周 3 次",
    "4 sessions in last 4 weeks": "过去 4 周 4 次",
    "5 sessions in last 4 weeks": "过去 4 周 5 次",
    "6 sessions in last 4 weeks": "过去 4 周 6 次",
    "7 sessions in last 4 weeks": "过去 4 周 7 次",
    "8 sessions in last 4 weeks": "过去 4 周 8 次",
    "Training context; not used for measured strongest-area versus main-gap comparison.": "训练背景；不用于实测 strongest-area / main-gap 比较。",
    "Training context and aerobic-base estimate; not treated as a performance test.": "训练背景和有氧基础估计；不作为表现测试。",
    "Training context; not treated as a measured strength-endurance result.": "训练背景；不作为实测 strength-endurance 结果。",
    "Prescription constraint; not a performance advantage.": "处方约束；不是表现优势。",
    "endurance base": "耐力基础",
    "strength background": "力量训练背景",
    "running comfort": "跑步适应度",
    "high-intensity comfort": "高强度训练熟悉度",
    "loaded movement comfort": "负重/功能性动作熟悉度",
    "Enter Hybrid Race Performance Lab": "进入 HYROX Check",
    "Join the 5K/10K registry waitlist": "加入 5K/10K 候补列表",
    "Complete the SportRx Hybrid Benchmark before building a tailored starter path.": "先完成 SportRx Hybrid Benchmark v1，再生成针对性的 4 周训练。",
    "More weekly running/walking volume": "增加每周跑步/快走量",
    "Longer continuous run/walk exposure": "增加连续跑/快走时间",
    "More weekly strength training exposure": "增加每周力量训练",
    "More recent high-intensity exposure": "增加近期高强度训练接触",
    "More recent loaded movement exposure": "增加近期负重动作接触",
    "More running-specific practice": "增加跑步专项练习",
    "Recent running/walking exposure is close to this challenge": "近期跑步/快走接触接近这个项目要求",
    "Age": "年龄",
    "Recent training days": "近期每周训练天数",
    "Recent training volume": "近期每周训练量",
    "Running or brisk-walking volume": "跑步/快走训练量",
    "Longest continuous run/walk": "最长连续跑/快走",
    "Strength training frequency": "力量训练频率",
    "High-intensity sessions": "高强度训练次数",
    "Loaded movement sessions": "负重动作训练次数",
    "Available training days": "未来可训练天数",
    "Maximum session length": "每次最多训练时长",
    "Primary goal": "主要目标",
    "years": "年",
    "days/week": "天/周",
    "minutes/week": "分钟/周",
    "minutes": "分钟",
    "sessions/4 weeks": "次/4 周",
    "minutes/session": "分钟/次",
    "category": "类别",
    "Safety Gate / adult-scope check": "Safety Gate / 成年人范围检查",
    "Quick Match": "Quick Match",
    "Quick Match / Training Profile": "Quick Match / Training Profile",
    "Quick Match / HYROX Check": "Quick Match / HYROX Check",
    "Training Block / Prescription": "Training Block / Prescription",
    "Routing / explanation language": "路线 / 解释语言",
    "Safety and scope only; it does not raise or lower Quick Match fit.": "只用于安全边界和适用范围，不提高或降低 Quick Match 匹配。",
    "Estimates recent training consistency from behavior, not confidence or identity.": "用近期行为描述训练规律性，不评价自信、身份或天赋。",
    "Describes recent volume; it is not a measured performance test.": "描述近期训练量，不是实测表现测试。",
    "Describes run exposure for hybrid-race context.": "描述 HYROX / Hybrid Race 相关跑走暴露。",
    "Describes recent continuous locomotion exposure.": "描述近期连续跑走能力暴露。",
    "Describes strength-training context; not a measured strength score.": "描述力量训练背景，不是实测力量分数。",
    "Describes recent exposure to harder efforts.": "描述近期高强度努力接触。",
    "Describes recent exposure to loaded carries, sled-like work, or similar station demands.": "描述近期负重搬运、sled-like 或类似 station 需求的接触。",
    "Constrains future frequency; not used as a performance advantage.": "约束未来训练频率，不作为表现优势。",
    "Constrains session duration in rule-based starter plans.": "约束规则生成训练计划中的单次时长。",
    "Changes how SportRx frames next steps; it is not a performance metric.": "影响下一步语言和路线，不是表现指标。",
}


def _language_id() -> str:
    try:
        return str(st.session_state.get("language_edition", "zh_user"))
    except Exception:
        return "zh_user"


def _is_english_edition() -> bool:
    return _language_id() == "en_user"


def _t(key: str) -> str:
    return ui_text(key, _language_id())


def _is_internal_edition() -> bool:
    return _internal_review_enabled() and _language_id() == "internal_mixed"


def _internal_review_enabled() -> bool:
    """Keep review-only controls off public hosts unless explicitly enabled."""

    return os.getenv("SPORT_RX_ENABLE_INTERNAL_REVIEW", "1") == "1"


def _public_preview_enabled() -> bool:
    """Identify the hosted sample-only experience."""

    return os.getenv("SPORT_RX_PUBLIC_PREVIEW", "0") == "1"


def _page_display_label(page_id: str) -> str:
    return page_label(page_id, _language_id())


def zh(value: object) -> str:
    if _is_english_edition():
        if value is None:
            return "Not entered"
        if isinstance(value, list):
            return ", ".join(str(item) for item in value) if value else "None"
        return str(value)
    if value is None:
        return "未填写"
    if isinstance(value, list):
        return "、".join(zh(item) for item in value) if value else "无"
    text = str(value)
    if text.endswith(" min/week reported training"):
        return f"自报每周训练 {text.split()[0]} 分钟"
    if text.endswith(" training days/week"):
        return f"每周训练 {text.split()[0]} 天"
    if text.endswith(" running min/week"):
        return f"每周跑步 {text.split()[0]} 分钟"
    if text.startswith("Training availability: ") and text.endswith(" days/week"):
        return f"可训练时间：每周 {text.split(': ')[1].split()[0]} 天"
    if text.endswith(" sessions in last 4 weeks"):
        return f"过去 4 周 {text.split()[0]} 次"
    if text.endswith(" session(s) in last 4 weeks"):
        return f"过去 4 周 {text.split()[0]} 次"
    if text.startswith("Start with "):
        return f"从 {text.removeprefix('Start with ').removesuffix('.')} 开始。"
    if " recommended + " in text and text.endswith(" optional"):
        recommended, optional = text.split(" recommended + ")
        return f"{recommended} 个 recommended + {optional.removesuffix(' optional')} 个 optional"
    return ZH_VALUE_MAP.get(text, text)


def zh_reason(text: str) -> str:
    if text.endswith(" training days/week reported"):
        return f"每周训练 {text.split()[0]} 天"
    if text.endswith(" total training min/week reported"):
        return f"每周训练总量 {text.split()[0]} 分钟"
    if text.endswith(" running/walking min/week reported"):
        return f"每周跑步/快走 {text.split()[0]} 分钟"
    if text.endswith(" min longest continuous run/walk reported"):
        return f"最长连续跑/快走 {text.split()[0]} 分钟"
    if text.endswith(" strength days/week reported"):
        return f"每周力量训练 {text.split()[0]} 天"
    if " high-intensity and " in text and text.endswith(" loaded sessions in last 4 weeks"):
        parts = text.split()
        return f"过去 4 周高强度 {parts[0]} 次，负重动作 {parts[3]} 次"
    if text.startswith("Training days below "):
        return f"训练天数少于 {text.removeprefix('Training days below ')}"
    if text.startswith("Weekly volume below about "):
        return f"每周训练总量少于约 {text.removeprefix('Weekly volume below about ')}"
    return zh(text)


def zh_join(items: list[str], empty: str) -> str:
    return "；".join(zh_reason(item) for item in items) if items else empty


def _protocol_source_choice(current_value: object) -> str:
    return resolve_protocol_source_choice(current_value)


def _protocol_source_value(choice: str, note: object = "") -> str:
    return resolve_protocol_source_value(choice, note)


def _state_defaults() -> None:
    st.session_state.setdefault("language_edition", "zh_user")
    st.session_state.setdefault("page", "Workbench")
    st.session_state.setdefault("profile", DEFAULT_PROFILE.copy())
    st.session_state.setdefault("quick_match_result", quick_match(st.session_state.profile))
    st.session_state.setdefault("lab_result", assess_hybrid_performance(st.session_state.profile))
    st.session_state.setdefault("passport", build_readiness_passport(st.session_state.profile))
    st.session_state.setdefault("feedback_by_week", {})
    st.session_state.setdefault("benchmark_sessions", [])
    st.session_state.setdefault("pilot_feedback_entries", [])
    st.session_state.setdefault("demo_scenario_id", "custom")
    st.session_state.setdefault("demo_claim_boundary", "")
    st.session_state.setdefault("public_demo_mode", False)
    st.session_state.setdefault("plan", generate_prescription(_prescription_profile(st.session_state.profile)))


def _product_mode() -> str:
    """Return the active product surface without removing the Labs prototype."""

    return os.environ.get("SPORT_RX_PRODUCT_MODE", "aerobic_v01").strip().lower()


def _v01_state_defaults() -> None:
    st.session_state.setdefault("v01_page", "今天")
    st.session_state.setdefault("v01_profile", V01_DEFAULT_PROFILE.copy())
    st.session_state.setdefault("v01_draft", V01_DEFAULT_PROFILE.copy())
    st.session_state.setdefault("v01_setup_step", 1)
    st.session_state.setdefault("v01_feedback_by_week", {})
    st.session_state.setdefault("v01_plan", None)


def _v01_refresh_plan() -> None:
    st.session_state.v01_plan = generate_prescription(
        st.session_state.v01_profile,
        feedback_by_week=st.session_state.v01_feedback_by_week,
    )


def _v01_set_page(page: str) -> None:
    st.session_state.v01_page = page


def _v01_set_setup_step(step: int) -> None:
    st.session_state.v01_setup_step = max(1, min(3, int(step)))


def _v01_activity(activity: object) -> str:
    return V01_ACTIVITY_LABELS.get(str(activity), str(activity))


def _v01_intensity(level: object) -> str:
    return V01_INTENSITY_LABELS.get(str(level), str(level))


def _v01_fitness_class(value: object) -> str:
    return V01_FITNESS_LABELS.get(str(value), str(value))


def _v01_talk_test(level: object) -> str:
    return V01_TALK_TESTS.get(str(level), "以能够完成整段训练为优先。")


def _refresh_outputs() -> None:
    profile = st.session_state.profile
    st.session_state.quick_match_result = quick_match(profile)
    st.session_state.lab_result = assess_hybrid_performance(profile)
    st.session_state.passport = build_readiness_passport(profile)
    st.session_state.plan = generate_prescription(
        _prescription_profile(profile),
        feedback_by_week=st.session_state.feedback_by_week,
    )


def _load_demo_state() -> None:
    _load_demo_scenario("complete_loop")


def _load_public_sample() -> None:
    """Load synthetic data for the public preview without collecting member data."""

    demo = build_demo_scenario_state("complete_loop")
    st.session_state.profile = demo["profile"]
    st.session_state.benchmark_sessions = demo["benchmark_sessions"]
    st.session_state.feedback_by_week = demo["feedback_by_week"]
    st.session_state.pilot_feedback_entries = []
    st.session_state.demo_scenario_id = "public_sample"
    st.session_state.public_demo_mode = True
    st.session_state.demo_claim_boundary = "Public preview uses synthetic sample data only. Do not enter personal, health, or performance data."
    st.session_state.page = "Benchmark Protocol"
    _refresh_outputs()


def _load_demo_scenario(scenario_id: str) -> None:
    demo = build_demo_scenario_state(scenario_id)
    st.session_state.profile = demo["profile"]
    st.session_state.benchmark_sessions = demo["benchmark_sessions"]
    st.session_state.feedback_by_week = demo["feedback_by_week"]
    st.session_state.pilot_feedback_entries = []
    st.session_state.demo_scenario_id = scenario_id
    st.session_state.public_demo_mode = False
    st.session_state.demo_claim_boundary = demo["claim_boundary"]
    st.session_state.page = "Workbench"
    _refresh_outputs()


def _reset_prototype_state() -> None:
    st.session_state.profile = DEFAULT_PROFILE.copy()
    st.session_state.benchmark_sessions = []
    st.session_state.pilot_feedback_entries = []
    st.session_state.feedback_by_week = {}
    st.session_state.demo_scenario_id = "custom"
    st.session_state.demo_claim_boundary = ""
    st.session_state.public_demo_mode = False
    st.session_state.page = "Workbench"
    _refresh_outputs()


def _prescription_profile(profile: dict) -> dict:
    running_minutes = int(profile.get("running_minutes_per_week", 0) or 0)
    longest_run = int(profile.get("longest_continuous_run_minutes", 0) or 0)
    preferred_activity = "running" if running_minutes >= 60 or longest_run >= 20 else "brisk walking"
    return {
        **profile,
        "exercise_days_last_4w": int(profile.get("training_days", profile.get("exercise_days_last_4w", 0)) or 0),
        "mvpa_minutes_per_week": int(profile.get("weekly_training_minutes", profile.get("mvpa_minutes_per_week", 0)) or 0),
        "common_activity": preferred_activity,
        "preferred_activity": preferred_activity,
        "intended_intensity": "moderate",
    }


def _apply_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --rx-ink: #17201b;
            --rx-muted: #5d6b63;
            --rx-line: #dce3de;
            --rx-surface: #f7faf8;
            --rx-panel: #ffffff;
            --rx-green: #1f7a4d;
            --rx-blue: #215a8e;
            --rx-amber: #9a6518;
        }
        .block-container {
            padding: 0.7rem 0.72rem 5.5rem;
            width: min(100%, 414px) !important;
            max-width: 414px !important;
            box-sizing: border-box;
            margin-left: auto !important;
            margin-right: auto !important;
        }
        [data-testid="stAppViewContainer"] {
            background: #edf3ef;
        }
        [data-testid="stHeader"] {
            background: rgba(237, 243, 239, 0.86);
            backdrop-filter: blur(10px);
        }
        [data-testid="stToolbar"] {
            right: 0.35rem;
        }
        div[data-testid="stMainBlockContainer"] {
            padding-left: 0;
            padding-right: 0;
        }
        section[data-testid="stSidebar"] {
            background: #f2f6f3;
            border-right: 1px solid var(--rx-line);
        }
        h1, h2, h3 {
            letter-spacing: 0;
        }
        div[data-testid="stMetric"] {
            background: var(--rx-panel);
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            padding: 12px 13px;
            min-height: 94px;
        }
        div[data-testid="stButton"] > button,
        div[data-testid="stDownloadButton"] > button {
            min-height: 42px;
            border-radius: 8px;
            font-weight: 760;
        }
        div[data-testid="stExpander"] {
            border-radius: 8px;
            overflow: hidden;
        }
        div[data-testid="stDataFrame"],
        div[data-testid="stTable"] {
            font-size: 0.78rem;
        }
        .rx-header {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            padding: 15px 15px 16px;
            background: #ffffff;
            margin-bottom: 12px;
            box-shadow: 0 10px 26px rgba(23, 32, 27, 0.055);
        }
        .rx-kicker {
            color: var(--rx-green);
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-title {
            color: var(--rx-ink);
            font-size: 1.34rem;
            font-weight: 750;
            line-height: 1.2;
            margin: 0;
        }
        .rx-subtitle {
            color: var(--rx-muted);
            font-size: 0.86rem;
            line-height: 1.48;
            margin-top: 8px;
            max-width: 100%;
        }
        .rx-mobile-nav {
            position: sticky;
            top: 0.45rem;
            z-index: 30;
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.94);
            box-shadow: 0 10px 26px rgba(23, 32, 27, 0.08);
            padding: 9px 9px 10px;
            margin: 0 0 12px;
            backdrop-filter: blur(10px);
        }
        .rx-mobile-nav-title {
            color: var(--rx-muted);
            font-size: 0.66rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 7px;
        }
        .rx-mobile-nav-copy {
            color: var(--rx-muted);
            font-size: 0.72rem;
            line-height: 1.35;
            margin-top: 5px;
        }
        .rx-public-home {
            display: grid;
            gap: 12px;
            margin-bottom: 14px;
        }
        .rx-public-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 14px 14px;
            box-shadow: 0 8px 22px rgba(23, 32, 27, 0.052);
        }
        .rx-public-card-ready {
            border-color: #c8e5d4;
            background: #f8fcfa;
        }
        .rx-public-card-waiting {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-public-kicker {
            color: var(--rx-green);
            font-size: 0.68rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 7px;
        }
        .rx-public-title {
            color: var(--rx-ink);
            font-size: 1.04rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 6px;
        }
        .rx-public-copy {
            color: var(--rx-muted);
            font-size: 0.82rem;
            line-height: 1.45;
        }
        .rx-public-value {
            color: var(--rx-ink);
            font-size: 1.18rem;
            font-weight: 880;
            line-height: 1.2;
            margin: 4px 0 5px;
        }
        .rx-public-list {
            display: grid;
            gap: 8px;
            margin: 10px 0 2px;
        }
        .rx-public-list-item {
            border-left: 3px solid #c8e5d4;
            background: rgba(255, 255, 255, 0.72);
            color: var(--rx-ink);
            font-size: 0.8rem;
            line-height: 1.38;
            padding: 8px 10px;
        }
        .rx-strip {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 10px;
            margin: 8px 0 18px;
        }
        .rx-strip-item {
            background: var(--rx-panel);
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            padding: 12px 14px;
        }
        .rx-strip-label {
            color: var(--rx-muted);
            font-size: 0.74rem;
            margin-bottom: 4px;
        }
        .rx-strip-value {
            color: var(--rx-ink);
            font-weight: 700;
            font-size: 0.96rem;
        }
        .rx-callout {
            border-left: 4px solid var(--rx-green);
            background: #f4f8f5;
            padding: 12px 14px;
            margin: 8px 0 16px;
            color: var(--rx-ink);
        }
        .rx-lab-status {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 14px 16px;
            margin: 0 0 16px;
            box-shadow: 0 10px 26px rgba(23, 32, 27, 0.055);
        }
        .rx-lab-status-head {
            display: grid;
            grid-template-columns: minmax(0, 1.2fr) minmax(260px, 0.8fr);
            gap: 16px;
            align-items: start;
            margin-bottom: 12px;
        }
        .rx-lab-status-kicker {
            color: var(--rx-green);
            font-size: 0.72rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        .rx-lab-status-title {
            color: var(--rx-ink);
            font-size: 1.08rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 5px;
        }
        .rx-lab-status-copy {
            color: var(--rx-muted);
            font-size: 0.84rem;
            line-height: 1.45;
        }
        .rx-lab-status-next {
            border-left: 4px solid var(--rx-blue);
            background: #f7fbf9;
            padding: 10px 12px;
            min-height: 78px;
        }
        .rx-lab-status-next-label {
            color: var(--rx-muted);
            font-size: 0.68rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        .rx-lab-status-next-value {
            color: var(--rx-ink);
            font-size: 0.92rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 4px;
        }
        .rx-lab-status-next-detail {
            color: var(--rx-muted);
            font-size: 0.76rem;
            line-height: 1.35;
        }
        .rx-lab-status-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 9px;
        }
        .rx-lab-status-tile {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #fbfdfb;
            padding: 10px 12px;
            min-height: 96px;
        }
        .rx-lab-status-ready {
            border-color: #c8e5d4;
            background: #f7fcf9;
        }
        .rx-lab-status-waiting {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-lab-status-blocked {
            border-color: #efb6a8;
            background: #fff7f4;
        }
        .rx-lab-status-label {
            color: var(--rx-muted);
            font-size: 0.66rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-lab-status-value {
            color: var(--rx-ink);
            font-size: 0.95rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 5px;
            overflow-wrap: anywhere;
        }
        .rx-lab-status-detail {
            color: var(--rx-muted);
            font-size: 0.74rem;
            line-height: 1.3;
        }
        .rx-hero-console {
            background: #ffffff;
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            padding: 18px 20px;
            margin: 2px 0 18px;
            box-shadow: 0 10px 28px rgba(23, 32, 27, 0.06);
        }
        .rx-hero-top {
            display: grid;
            grid-template-columns: minmax(0, 1.25fr) minmax(260px, 0.75fr);
            gap: 18px;
            align-items: end;
            margin-bottom: 16px;
        }
        .rx-hero-label {
            color: var(--rx-green);
            font-size: 0.76rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 7px;
        }
        .rx-hero-title {
            color: var(--rx-ink);
            font-size: 1.38rem;
            font-weight: 850;
            line-height: 1.2;
            margin-bottom: 8px;
        }
        .rx-hero-copy {
            color: var(--rx-muted);
            font-size: 0.92rem;
            line-height: 1.5;
            max-width: 760px;
        }
        .rx-hero-action {
            border-left: 4px solid var(--rx-blue);
            background: #f6fbf8;
            padding: 12px 13px;
            min-height: 96px;
        }
        .rx-hero-action-label {
            color: var(--rx-muted);
            font-size: 0.72rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        .rx-hero-action-value {
            color: var(--rx-ink);
            font-size: 1rem;
            font-weight: 800;
            line-height: 1.3;
            margin-bottom: 5px;
        }
        .rx-hero-action-detail {
            color: var(--rx-muted);
            font-size: 0.82rem;
            line-height: 1.4;
        }
        .rx-hero-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 10px;
        }
        .rx-hero-tile {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #fbfdfb;
            padding: 12px 13px;
            min-height: 112px;
        }
        .rx-hero-tile-ready {
            border-color: #c8e5d4;
            background: #f6fbf8;
        }
        .rx-hero-tile-waiting {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-hero-tile-blocked {
            border-color: #efb6a8;
            background: #fff7f4;
        }
        .rx-hero-tile-label {
            color: var(--rx-muted);
            font-size: 0.72rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 7px;
        }
        .rx-hero-tile-value {
            color: var(--rx-ink);
            font-size: 1.02rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 6px;
            overflow-wrap: anywhere;
        }
        .rx-hero-tile-detail {
            color: var(--rx-muted);
            font-size: 0.78rem;
            line-height: 1.35;
        }
        .rx-experience-console {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: linear-gradient(180deg, #ffffff 0%, #f7fbf9 100%);
            padding: 18px 20px;
            margin: 0 0 18px;
            box-shadow: 0 12px 30px rgba(23, 32, 27, 0.055);
        }
        .rx-experience-head {
            display: grid;
            grid-template-columns: minmax(0, 1.2fr) minmax(240px, 0.8fr);
            gap: 16px;
            align-items: start;
            margin-bottom: 14px;
        }
        .rx-experience-kicker {
            color: var(--rx-green);
            font-size: 0.74rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-experience-title {
            color: var(--rx-ink);
            font-size: 1.12rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 7px;
        }
        .rx-experience-copy {
            color: var(--rx-muted);
            font-size: 0.88rem;
            line-height: 1.48;
        }
        .rx-experience-status {
            border-left: 4px solid var(--rx-green);
            background: #f6fbf8;
            padding: 11px 12px;
        }
        .rx-experience-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 10px;
        }
        .rx-experience-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 12px 13px;
            min-height: 118px;
        }
        .rx-experience-card-ready {
            border-color: #c8e5d4;
            background: #f7fcf9;
        }
        .rx-experience-card-waiting {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-experience-label {
            color: var(--rx-muted);
            font-size: 0.72rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-experience-value {
            color: var(--rx-ink);
            font-size: 0.98rem;
            font-weight: 850;
            line-height: 1.26;
            margin-bottom: 6px;
            overflow-wrap: anywhere;
        }
        .rx-experience-detail {
            color: var(--rx-muted);
            font-size: 0.78rem;
            line-height: 1.38;
        }
        .rx-guided-console {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 18px 20px;
            margin: 0 0 18px;
            box-shadow: 0 10px 26px rgba(23, 32, 27, 0.052);
        }
        .rx-guided-head {
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(230px, 0.45fr);
            gap: 16px;
            align-items: start;
            margin-bottom: 12px;
        }
        .rx-guided-kicker {
            color: var(--rx-green);
            font-size: 0.74rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-guided-title {
            color: var(--rx-ink);
            font-size: 1.12rem;
            font-weight: 850;
            line-height: 1.24;
            margin-bottom: 7px;
        }
        .rx-guided-copy {
            color: var(--rx-muted);
            font-size: 0.88rem;
            line-height: 1.48;
        }
        .rx-guided-meter {
            border-left: 4px solid var(--rx-blue);
            background: #f6fbf8;
            padding: 11px 12px;
        }
        .rx-guided-grid {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 10px;
            margin-top: 12px;
        }
        .rx-guided-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #fbfdfb;
            padding: 11px 12px;
            min-height: 126px;
        }
        .rx-guided-card-ready {
            border-color: #c8e5d4;
            background: #f7fcf9;
        }
        .rx-guided-card-waiting {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-guided-label {
            color: var(--rx-muted);
            font-size: 0.68rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-guided-value {
            color: var(--rx-ink);
            font-size: 0.9rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 6px;
            overflow-wrap: anywhere;
        }
        .rx-guided-detail {
            color: var(--rx-muted);
            font-size: 0.74rem;
            line-height: 1.35;
        }
        .rx-action-rail {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 10px;
            margin: -6px 0 18px;
        }
        .rx-action-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 12px 12px 10px;
            min-height: 112px;
            box-shadow: 0 6px 18px rgba(23, 32, 27, 0.045);
        }
        .rx-action-card-primary {
            border-color: #8cc7a6;
            background: #f6fbf8;
        }
        .rx-action-label {
            color: var(--rx-green);
            font-size: 0.68rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-action-target {
            color: var(--rx-ink);
            font-size: 0.92rem;
            font-weight: 850;
            line-height: 1.24;
            margin-bottom: 7px;
            overflow-wrap: anywhere;
        }
        .rx-action-purpose {
            color: var(--rx-muted);
            font-size: 0.74rem;
            line-height: 1.35;
        }
        .rx-contract-console {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 16px 18px;
            margin: 0 0 18px;
            box-shadow: 0 8px 22px rgba(23, 32, 27, 0.05);
        }
        .rx-contract-head {
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(220px, 0.42fr);
            gap: 14px;
            align-items: start;
            margin-bottom: 12px;
        }
        .rx-contract-kicker {
            color: var(--rx-green);
            font-size: 0.72rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-contract-title {
            color: var(--rx-ink);
            font-size: 1.08rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 7px;
        }
        .rx-contract-copy {
            color: var(--rx-muted);
            font-size: 0.86rem;
            line-height: 1.46;
        }
        .rx-contract-status {
            border-left: 4px solid var(--rx-green);
            background: #f6fbf8;
            padding: 10px 12px;
        }
        .rx-contract-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 10px;
        }
        .rx-contract-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #fbfdfb;
            padding: 11px 12px;
            min-height: 126px;
        }
        .rx-contract-card-ready {
            border-color: #c8e5d4;
            background: #f7fcf9;
        }
        .rx-contract-card-waiting {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-contract-label {
            color: var(--rx-muted);
            font-size: 0.68rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-contract-value {
            color: var(--rx-ink);
            font-size: 0.9rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 6px;
            overflow-wrap: anywhere;
        }
        .rx-contract-detail {
            color: var(--rx-muted);
            font-size: 0.74rem;
            line-height: 1.35;
        }
        .rx-report-dashboard {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 16px 18px;
            margin: 2px 0 18px;
        }
        .rx-report-head {
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(240px, 0.55fr);
            gap: 14px;
            align-items: start;
            margin-bottom: 14px;
        }
        .rx-report-kicker {
            color: var(--rx-green);
            font-size: 0.74rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-report-title {
            color: var(--rx-ink);
            font-size: 1.16rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 7px;
        }
        .rx-report-copy {
            color: var(--rx-muted);
            font-size: 0.88rem;
            line-height: 1.48;
        }
        .rx-report-next {
            border-left: 4px solid var(--rx-green);
            background: #f6fbf8;
            padding: 11px 12px;
        }
        .rx-report-next-label {
            color: var(--rx-muted);
            font-size: 0.72rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        .rx-report-next-value {
            color: var(--rx-ink);
            font-size: 0.96rem;
            font-weight: 800;
            line-height: 1.32;
        }
        .rx-report-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 10px;
        }
        .rx-report-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #fbfdfb;
            padding: 12px 13px;
            min-height: 112px;
        }
        .rx-report-card-ready {
            border-color: #c8e5d4;
            background: #f6fbf8;
        }
        .rx-report-card-waiting {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-report-card-blocked {
            border-color: #efb6a8;
            background: #fff7f4;
        }
        .rx-report-card-label {
            color: var(--rx-muted);
            font-size: 0.7rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-report-card-value {
            color: var(--rx-ink);
            font-size: 0.98rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 6px;
            overflow-wrap: anywhere;
        }
        .rx-report-card-detail {
            color: var(--rx-muted);
            font-size: 0.78rem;
            line-height: 1.35;
        }
        .rx-profile-summary {
            display: grid;
            grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr);
            gap: 12px;
            margin: 10px 0 18px;
        }
        .rx-profile-panel {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 14px 15px;
            box-shadow: 0 8px 22px rgba(23, 32, 27, 0.045);
        }
        .rx-profile-panel-ready {
            border-color: #c8e5d4;
            background: #fbfdfb;
        }
        .rx-profile-panel-waiting {
            border-color: #ead4aa;
            background: #fffdf7;
        }
        .rx-profile-kicker {
            color: var(--rx-green);
            font-size: 0.68rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        .rx-profile-title {
            color: var(--rx-ink);
            font-size: 1rem;
            line-height: 1.25;
            font-weight: 850;
            margin-bottom: 8px;
            overflow-wrap: anywhere;
        }
        .rx-profile-copy {
            color: var(--rx-muted);
            font-size: 0.78rem;
            line-height: 1.42;
            margin-bottom: 10px;
        }
        .rx-profile-list {
            display: grid;
            gap: 7px;
        }
        .rx-profile-list-item {
            border-left: 3px solid #c8e5d4;
            background: #f6fbf8;
            padding: 7px 9px;
            color: var(--rx-ink);
            font-size: 0.76rem;
            line-height: 1.35;
        }
        .rx-profile-list-item-waiting {
            border-left-color: #d6aa52;
            background: #fffaf0;
            color: var(--rx-muted);
        }
        .rx-profile-handoff {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 8px;
            margin-top: 10px;
        }
        .rx-profile-chip {
            border: 1px solid #d6e4dc;
            background: #f6fbf8;
            border-radius: 8px;
            padding: 8px 9px;
        }
        .rx-profile-chip-label {
            color: var(--rx-muted);
            font-size: 0.64rem;
            line-height: 1.15;
            text-transform: uppercase;
            font-weight: 850;
            margin-bottom: 4px;
        }
        .rx-profile-chip-value {
            color: var(--rx-ink);
            font-size: 0.8rem;
            line-height: 1.2;
            font-weight: 850;
            overflow-wrap: anywhere;
        }
        .rx-profile-decision {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 16px 18px;
            margin: 0 0 18px;
            box-shadow: 0 10px 26px rgba(23, 32, 27, 0.05);
        }
        .rx-profile-decision-head {
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(230px, 0.46fr);
            gap: 14px;
            align-items: start;
            margin-bottom: 12px;
        }
        .rx-profile-decision-kicker {
            color: var(--rx-green);
            font-size: 0.72rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-profile-decision-title {
            color: var(--rx-ink);
            font-size: 1.08rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 7px;
        }
        .rx-profile-decision-copy {
            color: var(--rx-muted);
            font-size: 0.86rem;
            line-height: 1.46;
        }
        .rx-profile-decision-status {
            border-left: 4px solid var(--rx-green);
            background: #f6fbf8;
            padding: 10px 12px;
        }
        .rx-profile-decision-status-waiting {
            border-left-color: #d6aa52;
            background: #fffaf0;
        }
        .rx-profile-decision-status-blocked {
            border-left-color: #d86a50;
            background: #fff7f4;
        }
        .rx-profile-decision-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 10px;
        }
        .rx-profile-decision-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #fbfdfb;
            padding: 12px 13px;
            min-height: 126px;
        }
        .rx-profile-decision-card-ready {
            border-color: #c8e5d4;
            background: #f7fcf9;
        }
        .rx-profile-decision-card-waiting {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-profile-decision-card-blocked {
            border-color: #efb6a8;
            background: #fff7f4;
        }
        .rx-profile-decision-label {
            color: var(--rx-muted);
            font-size: 0.68rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-profile-decision-value {
            color: var(--rx-ink);
            font-size: 0.9rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 6px;
            overflow-wrap: anywhere;
        }
        .rx-profile-decision-detail {
            color: var(--rx-muted);
            font-size: 0.74rem;
            line-height: 1.35;
        }
        .rx-profile-dimensions {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 10px;
            margin: 0 0 16px;
        }
        .rx-profile-dimension {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 12px 13px;
            min-height: 132px;
        }
        .rx-profile-dimension-measured {
            border-color: #c8e5d4;
            background: #f7fcf9;
        }
        .rx-profile-dimension-missing {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-profile-dimension-label {
            color: var(--rx-muted);
            font-size: 0.68rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-profile-dimension-title {
            color: var(--rx-ink);
            font-size: 0.94rem;
            line-height: 1.25;
            font-weight: 850;
            margin-bottom: 7px;
            overflow-wrap: anywhere;
        }
        .rx-profile-dimension-value {
            color: var(--rx-green);
            font-size: 0.84rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 7px;
            overflow-wrap: anywhere;
        }
        .rx-profile-dimension-detail {
            color: var(--rx-muted);
            font-size: 0.74rem;
            line-height: 1.36;
        }
        .rx-evidence-console {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 16px 18px;
            margin: 2px 0 18px;
            box-shadow: 0 10px 26px rgba(23, 32, 27, 0.05);
        }
        .rx-evidence-head {
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(240px, 0.52fr);
            gap: 14px;
            align-items: start;
            margin-bottom: 14px;
        }
        .rx-evidence-kicker {
            color: var(--rx-green);
            font-size: 0.72rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-evidence-title {
            color: var(--rx-ink);
            font-size: 1.12rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 7px;
        }
        .rx-evidence-copy {
            color: var(--rx-muted);
            font-size: 0.86rem;
            line-height: 1.46;
        }
        .rx-evidence-status {
            border-left: 4px solid var(--rx-green);
            background: #f6fbf8;
            padding: 10px 12px;
        }
        .rx-evidence-status-waiting {
            border-left-color: #d6aa52;
            background: #fffaf0;
        }
        .rx-evidence-grid {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 10px;
        }
        .rx-evidence-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #fbfdfb;
            padding: 12px 13px;
            min-height: 118px;
        }
        .rx-evidence-card-ready {
            border-color: #c8e5d4;
            background: #f7fcf9;
        }
        .rx-evidence-card-waiting {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-evidence-label {
            color: var(--rx-muted);
            font-size: 0.68rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-evidence-value {
            color: var(--rx-ink);
            font-size: 0.92rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 6px;
            overflow-wrap: anywhere;
        }
        .rx-evidence-detail {
            color: var(--rx-muted);
            font-size: 0.74rem;
            line-height: 1.35;
        }
        .rx-evidence-topic-grid,
        .rx-evidence-source-grid,
        .rx-evidence-claim-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 10px;
            margin: 0 0 16px;
        }
        .rx-evidence-topic,
        .rx-evidence-source,
        .rx-evidence-claim {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 12px 13px;
            min-height: 138px;
        }
        .rx-evidence-topic-ready,
        .rx-evidence-source-ready,
        .rx-evidence-claim-ready {
            border-color: #c8e5d4;
            background: #f7fcf9;
        }
        .rx-evidence-topic-waiting,
        .rx-evidence-source-waiting,
        .rx-evidence-claim-waiting {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-evidence-source-limits {
            border-top: 1px solid #e1e9e4;
            margin-top: 9px;
            padding-top: 8px;
            color: var(--rx-muted);
            font-size: 0.72rem;
            line-height: 1.34;
        }
        .rx-log-dashboard {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 16px 18px;
            margin: 4px 0 18px;
        }
        .rx-log-head {
            display: flex;
            justify-content: space-between;
            gap: 16px;
            align-items: flex-start;
            margin-bottom: 14px;
        }
        .rx-log-kicker {
            color: var(--rx-green);
            font-size: 0.74rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-log-title {
            color: var(--rx-ink);
            font-size: 1.16rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 7px;
        }
        .rx-log-copy {
            color: var(--rx-muted);
            font-size: 0.88rem;
            line-height: 1.48;
            max-width: 760px;
        }
        .rx-log-path {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #f6fbf8;
            padding: 10px 11px;
            min-width: 210px;
        }
        .rx-log-grid {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 10px;
        }
        .rx-log-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #fbfdfb;
            padding: 12px 13px;
            min-height: 112px;
        }
        .rx-log-card-ready {
            border-color: #c8e5d4;
            background: #f6fbf8;
        }
        .rx-log-card-waiting {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-log-card-blocked {
            border-color: #efb6a8;
            background: #fff7f4;
        }
        .rx-log-label {
            color: var(--rx-muted);
            font-size: 0.7rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-log-value {
            color: var(--rx-ink);
            font-size: 0.98rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 6px;
            overflow-wrap: anywhere;
        }
        .rx-log-detail {
            color: var(--rx-muted);
            font-size: 0.78rem;
            line-height: 1.35;
        }
        .rx-session-gallery {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 12px;
            margin: 10px 0 14px;
        }
        .rx-session-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 14px 15px;
            box-shadow: 0 8px 22px rgba(23, 32, 27, 0.045);
        }
        .rx-session-head {
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(150px, 0.42fr);
            gap: 10px;
            align-items: start;
            margin-bottom: 10px;
        }
        .rx-session-kicker {
            color: var(--rx-green);
            font-size: 0.68rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        .rx-session-title {
            color: var(--rx-ink);
            font-size: 1rem;
            line-height: 1.25;
            font-weight: 850;
            overflow-wrap: anywhere;
        }
        .rx-session-meta {
            color: var(--rx-muted);
            font-size: 0.74rem;
            line-height: 1.35;
            margin-top: 5px;
        }
        .rx-session-status {
            border-left: 3px solid var(--rx-blue);
            background: #f6fbf8;
            padding: 9px 10px;
        }
        .rx-session-status-waiting {
            border-left-color: #d6aa52;
            background: #fffaf0;
        }
        .rx-session-status-blocked {
            border-left-color: #d97b64;
            background: #fff7f4;
        }
        .rx-session-status-label {
            color: var(--rx-muted);
            font-size: 0.66rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 4px;
        }
        .rx-session-status-value {
            color: var(--rx-ink);
            font-size: 0.86rem;
            line-height: 1.2;
            font-weight: 850;
        }
        .rx-session-components {
            display: flex;
            flex-wrap: wrap;
            gap: 7px;
            margin: 10px 0;
        }
        .rx-session-pill {
            border: 1px solid #d6e4dc;
            background: #f6fbf8;
            border-radius: 999px;
            padding: 5px 8px;
            color: var(--rx-ink);
            font-size: 0.7rem;
            line-height: 1.15;
            font-weight: 750;
            max-width: 100%;
            overflow-wrap: anywhere;
        }
        .rx-session-pill-missing {
            border-color: #ead4aa;
            background: #fffaf0;
            color: var(--rx-muted);
        }
        .rx-session-notes {
            color: var(--rx-muted);
            font-size: 0.74rem;
            line-height: 1.38;
            border-top: 1px solid var(--rx-line);
            padding-top: 9px;
        }
        .rx-draft-board {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 16px 18px;
            margin: 8px 0 18px;
            box-shadow: 0 8px 22px rgba(23, 32, 27, 0.05);
        }
        .rx-draft-head {
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(220px, 0.36fr);
            gap: 14px;
            align-items: start;
            margin-bottom: 14px;
        }
        .rx-draft-kicker {
            color: var(--rx-green);
            font-size: 0.72rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-draft-title {
            color: var(--rx-ink);
            font-size: 1.12rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 7px;
        }
        .rx-draft-copy {
            color: var(--rx-muted);
            font-size: 0.84rem;
            line-height: 1.45;
        }
        .rx-draft-status {
            border-left: 4px solid var(--rx-blue);
            background: #f6fbf8;
            padding: 10px 11px;
        }
        .rx-draft-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 10px;
            margin-bottom: 12px;
        }
        .rx-draft-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #fbfdfb;
            padding: 11px 12px;
            min-height: 112px;
        }
        .rx-draft-card-ready {
            border-color: #c8e5d4;
            background: #f6fbf8;
        }
        .rx-draft-card-waiting {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-draft-card-blocked {
            border-color: #efb6a8;
            background: #fff7f4;
        }
        .rx-draft-label {
            color: var(--rx-muted);
            font-size: 0.68rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-draft-value {
            color: var(--rx-ink);
            font-size: 0.94rem;
            font-weight: 850;
            line-height: 1.24;
            margin-bottom: 6px;
            overflow-wrap: anywhere;
        }
        .rx-draft-detail {
            color: var(--rx-muted);
            font-size: 0.74rem;
            line-height: 1.35;
        }
        .rx-draft-components {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 10px;
        }
        .rx-draft-component {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 11px 12px;
            min-height: 128px;
        }
        .rx-draft-component-measured {
            border-color: #c8e5d4;
            background: #f6fbf8;
        }
        .rx-draft-component-missing {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-quality-console {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 16px 18px;
            margin: 6px 0 16px;
            box-shadow: 0 8px 22px rgba(23, 32, 27, 0.05);
        }
        .rx-quality-head {
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(230px, 0.42fr);
            gap: 14px;
            align-items: start;
            margin-bottom: 14px;
        }
        .rx-quality-kicker {
            color: var(--rx-green);
            font-size: 0.74rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-quality-title {
            color: var(--rx-ink);
            font-size: 1.16rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 7px;
        }
        .rx-quality-copy {
            color: var(--rx-muted);
            font-size: 0.88rem;
            line-height: 1.48;
            max-width: 780px;
        }
        .rx-quality-status {
            border-left: 4px solid var(--rx-blue);
            background: #f6fbf8;
            padding: 11px 12px;
        }
        .rx-quality-grid {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 10px;
        }
        .rx-quality-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #fbfdfb;
            padding: 12px 13px;
            min-height: 116px;
        }
        .rx-quality-card-ready {
            border-color: #c8e5d4;
            background: #f6fbf8;
        }
        .rx-quality-card-waiting {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-quality-card-blocked {
            border-color: #efb6a8;
            background: #fff7f4;
        }
        .rx-quality-label {
            color: var(--rx-muted);
            font-size: 0.7rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-quality-value {
            color: var(--rx-ink);
            font-size: 0.94rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 6px;
            overflow-wrap: anywhere;
        }
        .rx-quality-detail {
            color: var(--rx-muted);
            font-size: 0.76rem;
            line-height: 1.35;
        }
        .rx-entry-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 12px;
            margin: 12px 0 2px;
        }
        .rx-entry-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #fbfdfb;
            padding: 13px 14px;
            min-height: 230px;
            display: flex;
            flex-direction: column;
            gap: 9px;
        }
        .rx-entry-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 10px;
        }
        .rx-entry-title {
            color: var(--rx-ink);
            font-size: 0.96rem;
            line-height: 1.25;
            font-weight: 850;
            overflow-wrap: anywhere;
        }
        .rx-entry-area {
            color: var(--rx-green);
            font-size: 0.68rem;
            line-height: 1.2;
            font-weight: 850;
            text-transform: uppercase;
            white-space: nowrap;
        }
        .rx-entry-row {
            color: var(--rx-muted);
            font-size: 0.76rem;
            line-height: 1.38;
        }
        .rx-entry-row strong {
            color: var(--rx-ink);
            font-weight: 850;
        }
        .rx-entry-chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }
        .rx-entry-chip {
            border: 1px solid #d6e4dc;
            background: #f6fbf8;
            color: var(--rx-ink);
            border-radius: 999px;
            padding: 4px 8px;
            font-size: 0.68rem;
            line-height: 1.1;
            font-weight: 750;
        }
        .rx-entry-chip-waiting {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-entry-blocked {
            border-left: 3px solid #efb6a8;
            background: #fff7f4;
            padding: 8px 9px;
            color: var(--rx-muted);
            font-size: 0.72rem;
            line-height: 1.35;
            margin-top: auto;
        }
        .rx-training-console {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 16px 18px;
            margin: 6px 0 18px;
            box-shadow: 0 8px 22px rgba(23, 32, 27, 0.05);
        }
        .rx-training-head {
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(230px, 0.42fr);
            gap: 14px;
            align-items: start;
            margin-bottom: 14px;
        }
        .rx-training-kicker {
            color: var(--rx-green);
            font-size: 0.74rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-training-title {
            color: var(--rx-ink);
            font-size: 1.16rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 7px;
        }
        .rx-training-copy {
            color: var(--rx-muted);
            font-size: 0.88rem;
            line-height: 1.48;
            max-width: 780px;
        }
        .rx-training-status {
            border-left: 4px solid var(--rx-blue);
            background: #f6fbf8;
            padding: 11px 12px;
        }
        .rx-training-grid {
            display: grid;
            grid-template-columns: repeat(6, minmax(0, 1fr));
            gap: 10px;
        }
        .rx-training-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #fbfdfb;
            padding: 12px 13px;
            min-height: 118px;
        }
        .rx-training-card-ready {
            border-color: #c8e5d4;
            background: #f6fbf8;
        }
        .rx-training-card-waiting {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-training-card-blocked {
            border-color: #efb6a8;
            background: #fff7f4;
        }
        .rx-training-label {
            color: var(--rx-muted);
            font-size: 0.7rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-training-value {
            color: var(--rx-ink);
            font-size: 0.94rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 6px;
            overflow-wrap: anywhere;
        }
        .rx-training-detail {
            color: var(--rx-muted);
            font-size: 0.76rem;
            line-height: 1.35;
        }
        .rx-week-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 12px;
            margin: 10px 0 18px;
        }
        .rx-week-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 14px 15px;
            box-shadow: 0 8px 22px rgba(23, 32, 27, 0.045);
        }
        .rx-week-card-retest {
            border-color: #c8d7ec;
            background: #f7fbff;
        }
        .rx-week-head {
            display: flex;
            justify-content: space-between;
            gap: 10px;
            align-items: flex-start;
            margin-bottom: 10px;
        }
        .rx-week-kicker {
            color: var(--rx-green);
            font-size: 0.68rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        .rx-week-title {
            color: var(--rx-ink);
            font-size: 1rem;
            line-height: 1.25;
            font-weight: 850;
            overflow-wrap: anywhere;
        }
        .rx-week-volume {
            border-left: 3px solid var(--rx-blue);
            background: #f6fbf8;
            padding: 8px 9px;
            min-width: 112px;
        }
        .rx-week-volume-label {
            color: var(--rx-muted);
            font-size: 0.64rem;
            line-height: 1.1;
            text-transform: uppercase;
            font-weight: 850;
            margin-bottom: 4px;
        }
        .rx-week-volume-value {
            color: var(--rx-ink);
            font-size: 0.86rem;
            line-height: 1.2;
            font-weight: 850;
        }
        .rx-week-copy {
            color: var(--rx-muted);
            font-size: 0.76rem;
            line-height: 1.42;
            margin-bottom: 10px;
        }
        .rx-week-session-list {
            display: grid;
            gap: 7px;
        }
        .rx-week-session {
            border: 1px solid #d6e4dc;
            background: #fbfdfb;
            border-radius: 8px;
            padding: 8px 9px;
        }
        .rx-week-session-title {
            color: var(--rx-ink);
            font-size: 0.76rem;
            line-height: 1.25;
            font-weight: 850;
            margin-bottom: 4px;
        }
        .rx-week-session-detail {
            color: var(--rx-muted);
            font-size: 0.7rem;
            line-height: 1.32;
        }
        .rx-week-review {
            border-top: 1px solid var(--rx-line);
            color: var(--rx-muted);
            font-size: 0.72rem;
            line-height: 1.35;
            margin-top: 10px;
            padding-top: 8px;
        }
        .rx-feedback-console {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 16px 18px;
            margin: 6px 0 18px;
            box-shadow: 0 8px 22px rgba(23, 32, 27, 0.05);
        }
        .rx-feedback-head {
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(230px, 0.42fr);
            gap: 14px;
            align-items: start;
            margin-bottom: 14px;
        }
        .rx-feedback-kicker {
            color: var(--rx-green);
            font-size: 0.74rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-feedback-title {
            color: var(--rx-ink);
            font-size: 1.16rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 7px;
        }
        .rx-feedback-copy {
            color: var(--rx-muted);
            font-size: 0.88rem;
            line-height: 1.48;
            max-width: 780px;
        }
        .rx-feedback-status {
            border-left: 4px solid var(--rx-blue);
            background: #f6fbf8;
            padding: 11px 12px;
        }
        .rx-feedback-grid {
            display: grid;
            grid-template-columns: repeat(6, minmax(0, 1fr));
            gap: 10px;
        }
        .rx-feedback-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #fbfdfb;
            padding: 12px 13px;
            min-height: 118px;
        }
        .rx-feedback-card-ready {
            border-color: #c8e5d4;
            background: #f6fbf8;
        }
        .rx-feedback-card-waiting {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-feedback-card-blocked {
            border-color: #efb6a8;
            background: #fff7f4;
        }
        .rx-feedback-label {
            color: var(--rx-muted);
            font-size: 0.7rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-feedback-value {
            color: var(--rx-ink);
            font-size: 0.94rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 6px;
            overflow-wrap: anywhere;
        }
        .rx-feedback-detail {
            color: var(--rx-muted);
            font-size: 0.76rem;
            line-height: 1.35;
        }
        .rx-loop-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 12px;
            margin: 8px 0 18px;
        }
        .rx-loop-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 13px 14px;
            min-height: 126px;
            box-shadow: 0 8px 22px rgba(23, 32, 27, 0.045);
        }
        .rx-loop-card-ready {
            border-color: #c8e5d4;
            background: #f6fbf8;
        }
        .rx-loop-card-waiting {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-loop-card-blocked {
            border-color: #efb6a8;
            background: #fff7f4;
        }
        .rx-loop-label {
            color: var(--rx-muted);
            font-size: 0.68rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-loop-value {
            color: var(--rx-ink);
            font-size: 1rem;
            font-weight: 850;
            line-height: 1.24;
            margin-bottom: 7px;
            overflow-wrap: anywhere;
        }
        .rx-loop-detail {
            color: var(--rx-muted);
            font-size: 0.75rem;
            line-height: 1.38;
        }
        .rx-decision-panel {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 15px 16px;
            margin: 8px 0 18px;
            box-shadow: 0 8px 22px rgba(23, 32, 27, 0.045);
        }
        .rx-decision-head {
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(190px, 0.34fr);
            gap: 14px;
            align-items: start;
            margin-bottom: 12px;
        }
        .rx-decision-kicker {
            color: var(--rx-green);
            font-size: 0.68rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        .rx-decision-title {
            color: var(--rx-ink);
            font-size: 1.02rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 6px;
        }
        .rx-decision-copy {
            color: var(--rx-muted);
            font-size: 0.8rem;
            line-height: 1.45;
        }
        .rx-decision-dose {
            border-left: 3px solid var(--rx-blue);
            background: #f6fbf8;
            padding: 9px 10px;
        }
        .rx-decision-reasons {
            display: flex;
            flex-wrap: wrap;
            gap: 7px;
        }
        .rx-decision-chip {
            border: 1px solid #d6e4dc;
            border-radius: 999px;
            background: #fbfdfb;
            color: var(--rx-ink);
            font-size: 0.7rem;
            line-height: 1.15;
            font-weight: 800;
            padding: 5px 8px;
        }
        .rx-pilot-console {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 16px 18px;
            margin: 6px 0 18px;
            box-shadow: 0 8px 22px rgba(23, 32, 27, 0.05);
        }
        .rx-pilot-head {
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(230px, 0.42fr);
            gap: 14px;
            align-items: start;
            margin-bottom: 14px;
        }
        .rx-pilot-kicker {
            color: var(--rx-green);
            font-size: 0.74rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-pilot-title {
            color: var(--rx-ink);
            font-size: 1.16rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 7px;
        }
        .rx-pilot-copy {
            color: var(--rx-muted);
            font-size: 0.88rem;
            line-height: 1.48;
            max-width: 780px;
        }
        .rx-pilot-status {
            border-left: 4px solid var(--rx-blue);
            background: #f6fbf8;
            padding: 11px 12px;
        }
        .rx-pilot-grid {
            display: grid;
            grid-template-columns: repeat(6, minmax(0, 1fr));
            gap: 10px;
        }
        .rx-pilot-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #fbfdfb;
            padding: 12px 13px;
            min-height: 118px;
        }
        .rx-pilot-card-ready {
            border-color: #c8e5d4;
            background: #f6fbf8;
        }
        .rx-pilot-card-waiting {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-pilot-label {
            color: var(--rx-muted);
            font-size: 0.7rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-pilot-value {
            color: var(--rx-ink);
            font-size: 0.94rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 6px;
            overflow-wrap: anywhere;
        }
        .rx-pilot-detail {
            color: var(--rx-muted);
            font-size: 0.76rem;
            line-height: 1.35;
        }
        .rx-release-console {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 16px 18px;
            margin: 4px 0 18px;
            box-shadow: 0 8px 22px rgba(23, 32, 27, 0.05);
        }
        .rx-release-head {
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(230px, 0.45fr);
            gap: 14px;
            align-items: start;
            margin-bottom: 14px;
        }
        .rx-release-kicker {
            color: var(--rx-green);
            font-size: 0.74rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-release-title {
            color: var(--rx-ink);
            font-size: 1.16rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 7px;
        }
        .rx-release-copy {
            color: var(--rx-muted);
            font-size: 0.88rem;
            line-height: 1.48;
            max-width: 780px;
        }
        .rx-release-status {
            border-left: 4px solid var(--rx-blue);
            background: #f6fbf8;
            padding: 11px 12px;
        }
        .rx-release-grid {
            display: grid;
            grid-template-columns: repeat(6, minmax(0, 1fr));
            gap: 10px;
        }
        .rx-release-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #fbfdfb;
            padding: 12px 13px;
            min-height: 118px;
        }
        .rx-release-card-ready {
            border-color: #c8e5d4;
            background: #f6fbf8;
        }
        .rx-release-card-waiting {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-release-card-blocked {
            border-color: #efb6a8;
            background: #fff7f4;
        }
        .rx-release-label {
            color: var(--rx-muted);
            font-size: 0.7rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-release-value {
            color: var(--rx-ink);
            font-size: 0.94rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 6px;
            overflow-wrap: anywhere;
        }
        .rx-release-detail {
            color: var(--rx-muted);
            font-size: 0.76rem;
            line-height: 1.35;
        }
        .rx-beta-console {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 16px 18px;
            margin: 4px 0 18px;
            box-shadow: 0 8px 22px rgba(23, 32, 27, 0.05);
        }
        .rx-beta-head {
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(250px, 0.46fr);
            gap: 14px;
            align-items: start;
            margin-bottom: 14px;
        }
        .rx-beta-kicker {
            color: var(--rx-green);
            font-size: 0.74rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-beta-title {
            color: var(--rx-ink);
            font-size: 1.16rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 7px;
        }
        .rx-beta-copy {
            color: var(--rx-muted);
            font-size: 0.88rem;
            line-height: 1.48;
            max-width: 780px;
        }
        .rx-beta-status {
            border-left: 4px solid var(--rx-blue);
            background: #f6fbf8;
            padding: 11px 12px;
        }
        .rx-beta-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 10px;
        }
        .rx-beta-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #fbfdfb;
            padding: 12px 13px;
            min-height: 118px;
        }
        .rx-beta-card-ready {
            border-color: #c8e5d4;
            background: #f6fbf8;
        }
        .rx-beta-card-waiting {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-beta-label {
            color: var(--rx-muted);
            font-size: 0.7rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-beta-value {
            color: var(--rx-ink);
            font-size: 0.94rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 6px;
            overflow-wrap: anywhere;
        }
        .rx-beta-detail {
            color: var(--rx-muted);
            font-size: 0.76rem;
            line-height: 1.35;
        }
        .rx-export-console {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 16px 18px;
            margin: 4px 0 18px;
            box-shadow: 0 8px 22px rgba(23, 32, 27, 0.05);
        }
        .rx-export-head {
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(230px, 0.45fr);
            gap: 14px;
            align-items: start;
            margin-bottom: 14px;
        }
        .rx-export-kicker {
            color: var(--rx-green);
            font-size: 0.74rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-export-title {
            color: var(--rx-ink);
            font-size: 1.16rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 7px;
        }
        .rx-export-copy {
            color: var(--rx-muted);
            font-size: 0.88rem;
            line-height: 1.48;
            max-width: 780px;
        }
        .rx-export-status {
            border-left: 4px solid var(--rx-blue);
            background: #f6fbf8;
            padding: 11px 12px;
        }
        .rx-export-grid {
            display: grid;
            grid-template-columns: repeat(6, minmax(0, 1fr));
            gap: 10px;
        }
        .rx-export-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #fbfdfb;
            padding: 12px 13px;
            min-height: 118px;
        }
        .rx-export-card-ready {
            border-color: #c8e5d4;
            background: #f6fbf8;
        }
        .rx-export-card-waiting {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-export-label {
            color: var(--rx-muted);
            font-size: 0.7rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-export-value {
            color: var(--rx-ink);
            font-size: 0.94rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 6px;
            overflow-wrap: anywhere;
        }
        .rx-export-detail {
            color: var(--rx-muted);
            font-size: 0.76rem;
            line-height: 1.35;
        }
        .rx-qm-input-console {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 15px 17px;
            margin: 4px 0 16px;
        }
        .rx-qm-input-head {
            display: flex;
            justify-content: space-between;
            gap: 16px;
            align-items: flex-start;
            margin-bottom: 13px;
        }
        .rx-qm-input-kicker {
            color: var(--rx-green);
            font-size: 0.72rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-qm-input-title {
            color: var(--rx-ink);
            font-size: 1.08rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 6px;
        }
        .rx-qm-input-copy {
            color: var(--rx-muted);
            font-size: 0.86rem;
            line-height: 1.46;
            max-width: 760px;
        }
        .rx-qm-input-status {
            border-left: 4px solid var(--rx-blue);
            background: #f6fbf8;
            padding: 10px 11px;
            min-width: 205px;
        }
        .rx-qm-input-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 10px;
        }
        .rx-qm-input-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #fbfdfb;
            padding: 11px 12px;
            min-height: 104px;
        }
        .rx-qm-input-label {
            color: var(--rx-muted);
            font-size: 0.68rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-qm-input-value {
            color: var(--rx-ink);
            font-size: 0.94rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 6px;
            overflow-wrap: anywhere;
        }
        .rx-qm-input-detail {
            color: var(--rx-muted);
            font-size: 0.76rem;
            line-height: 1.35;
        }
        .rx-qm-match-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 12px;
            margin: 12px 0 18px;
        }
        .rx-qm-match-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 15px 16px;
            box-shadow: 0 8px 22px rgba(23, 32, 27, 0.045);
        }
        .rx-qm-match-card-ready {
            border-color: #c8e5d4;
            background: #f6fbf8;
        }
        .rx-qm-match-card-waiting {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-qm-match-card-blocked {
            border-color: #efb6a8;
            background: #fff7f4;
        }
        .rx-qm-match-head {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            align-items: flex-start;
            margin-bottom: 11px;
        }
        .rx-qm-match-kicker {
            color: var(--rx-green);
            font-size: 0.68rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        .rx-qm-match-title {
            color: var(--rx-ink);
            font-size: 1.08rem;
            line-height: 1.22;
            font-weight: 850;
            overflow-wrap: anywhere;
        }
        .rx-qm-match-status {
            border-left: 3px solid var(--rx-blue);
            background: rgba(255, 255, 255, 0.66);
            padding: 8px 9px;
            min-width: 126px;
        }
        .rx-qm-match-label {
            color: var(--rx-muted);
            font-size: 0.66rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 4px;
        }
        .rx-qm-match-value {
            color: var(--rx-ink);
            font-size: 0.86rem;
            line-height: 1.22;
            font-weight: 850;
            overflow-wrap: anywhere;
        }
        .rx-qm-match-section {
            border-top: 1px solid var(--rx-line);
            padding-top: 9px;
            margin-top: 9px;
        }
        .rx-qm-match-list {
            display: grid;
            gap: 6px;
            margin-top: 6px;
        }
        .rx-qm-match-list-item {
            border-left: 3px solid #c8e5d4;
            background: rgba(255, 255, 255, 0.68);
            color: var(--rx-ink);
            font-size: 0.74rem;
            line-height: 1.35;
            padding: 6px 8px;
        }
        .rx-qm-match-list-item-missing {
            border-left-color: #d6aa52;
            color: var(--rx-muted);
        }
        .rx-qm-boundary {
            border: 1px solid #d6e4dc;
            border-radius: 8px;
            background: #fbfdfb;
            color: var(--rx-muted);
            font-size: 0.78rem;
            line-height: 1.45;
            padding: 10px 12px;
            margin: 8px 0 14px;
        }
        .rx-workbench {
            display: grid;
            grid-template-columns: minmax(0, 1.25fr) minmax(320px, 0.75fr);
            gap: 16px;
            align-items: start;
            margin-bottom: 18px;
        }
        .rx-lab-board {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 16px 18px;
            margin: 4px 0 18px;
            box-shadow: 0 10px 26px rgba(23, 32, 27, 0.05);
        }
        .rx-lab-board-head {
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(240px, 0.42fr);
            gap: 14px;
            align-items: start;
            margin-bottom: 14px;
        }
        .rx-lab-board-kicker {
            color: var(--rx-green);
            font-size: 0.74rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-lab-board-title {
            color: var(--rx-ink);
            font-size: 1.18rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 7px;
        }
        .rx-lab-board-copy {
            color: var(--rx-muted);
            font-size: 0.88rem;
            line-height: 1.48;
            max-width: 820px;
        }
        .rx-lab-board-action {
            border-left: 4px solid var(--rx-amber);
            background: #fffaf0;
            padding: 11px 12px;
        }
        .rx-lab-board-action-label {
            color: var(--rx-muted);
            font-size: 0.7rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        .rx-lab-board-action-value {
            color: var(--rx-ink);
            font-size: 0.96rem;
            font-weight: 850;
            line-height: 1.28;
            margin-bottom: 5px;
        }
        .rx-lab-board-action-detail {
            color: var(--rx-muted);
            font-size: 0.78rem;
            line-height: 1.34;
        }
        .rx-lab-lanes {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 12px;
        }
        .rx-lab-lane {
            border: 1px solid var(--rx-line);
            border-top: 4px solid var(--rx-blue);
            border-radius: 8px;
            background: #fbfdfb;
            padding: 13px 14px;
            min-height: 170px;
        }
        .rx-lab-lane-ready {
            border-top-color: var(--rx-green);
            background: #f6fbf8;
        }
        .rx-lab-lane-waiting {
            border-top-color: var(--rx-amber);
            background: #fffaf0;
        }
        .rx-lab-lane-blocked {
            border-top-color: #b64f3c;
            background: #fff7f4;
        }
        .rx-lab-lane-label {
            color: var(--rx-muted);
            font-size: 0.7rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-lab-lane-title {
            color: var(--rx-ink);
            font-size: 1rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 8px;
        }
        .rx-lab-lane-row {
            color: var(--rx-muted);
            font-size: 0.8rem;
            line-height: 1.42;
            margin-top: 7px;
        }
        .rx-lab-lane-row strong {
            color: var(--rx-ink);
            font-weight: 800;
        }
        .rx-section {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: var(--rx-panel);
            padding: 16px 18px;
            margin-bottom: 14px;
        }
        .rx-section-title {
            color: var(--rx-ink);
            font-size: 1.05rem;
            font-weight: 750;
            margin-bottom: 8px;
        }
        .rx-section-copy {
            color: var(--rx-muted);
            font-size: 0.94rem;
            line-height: 1.55;
        }
        .rx-module-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 12px;
            margin: 6px 0 16px;
        }
        .rx-module {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: var(--rx-panel);
            padding: 14px 15px;
            min-height: 132px;
        }
        .rx-module-kicker {
            color: var(--rx-green);
            font-size: 0.72rem;
            font-weight: 750;
            text-transform: uppercase;
            margin-bottom: 8px;
        }
        .rx-module-title {
            color: var(--rx-ink);
            font-weight: 750;
            margin-bottom: 6px;
        }
        .rx-module-copy {
            color: var(--rx-muted);
            font-size: 0.88rem;
            line-height: 1.45;
        }
        .rx-pipeline {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 8px;
        }
        .rx-pipeline-step {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            padding: 10px 11px;
            background: #fbfdfb;
        }
        .rx-pipeline-label {
            color: var(--rx-muted);
            font-size: 0.72rem;
            margin-bottom: 4px;
        }
        .rx-pipeline-value {
            color: var(--rx-ink);
            font-size: 0.9rem;
            font-weight: 700;
        }
        .rx-command-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 10px;
            margin: 4px 0 18px;
        }
        .rx-command-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 14px 14px 13px;
            min-height: 156px;
        }
        .rx-command-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
            margin-bottom: 10px;
        }
        .rx-command-label {
            color: var(--rx-muted);
            font-size: 0.76rem;
            font-weight: 700;
            text-transform: uppercase;
        }
        .rx-pill {
            border-radius: 999px;
            padding: 3px 8px;
            font-size: 0.72rem;
            font-weight: 750;
            border: 1px solid var(--rx-line);
            white-space: nowrap;
        }
        .rx-pill-ready {
            background: #eaf6ef;
            color: var(--rx-green);
            border-color: #c8e5d4;
        }
        .rx-pill-needs-review {
            background: #fff6e8;
            color: var(--rx-amber);
            border-color: #ead4aa;
        }
        .rx-command-value {
            color: var(--rx-ink);
            font-size: 1.05rem;
            font-weight: 800;
            line-height: 1.25;
            margin-bottom: 7px;
        }
        .rx-command-detail {
            color: var(--rx-muted);
            font-size: 0.86rem;
            line-height: 1.45;
        }
        .rx-start-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 12px;
            margin: 4px 0 18px;
        }
        .rx-start-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 15px 16px;
            min-height: 188px;
            box-shadow: 0 1px 0 rgba(23, 32, 27, 0.04);
        }
        .rx-start-card-active {
            border-color: #8cc7a6;
            background: #f6fbf8;
        }
        .rx-start-label {
            color: var(--rx-green);
            font-size: 0.76rem;
            font-weight: 750;
            text-transform: uppercase;
            margin-bottom: 7px;
        }
        .rx-start-title {
            color: var(--rx-ink);
            font-weight: 800;
            font-size: 1.05rem;
            margin-bottom: 8px;
        }
        .rx-start-copy {
            color: var(--rx-muted);
            font-size: 0.88rem;
            line-height: 1.45;
            margin-bottom: 8px;
        }
        .rx-start-foot {
            color: var(--rx-ink);
            font-size: 0.86rem;
            font-weight: 700;
        }
        .rx-scenario-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 12px;
            margin: 6px 0 10px;
        }
        .rx-scenario-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 14px 15px;
            min-height: 218px;
            box-shadow: 0 8px 20px rgba(23, 32, 27, 0.045);
        }
        .rx-scenario-card-active {
            border-color: #8cc7a6;
            background: #f6fbf8;
            box-shadow: 0 10px 24px rgba(31, 122, 77, 0.10);
        }
        .rx-scenario-top {
            display: flex;
            justify-content: space-between;
            gap: 8px;
            align-items: flex-start;
            margin-bottom: 8px;
        }
        .rx-scenario-stage {
            color: var(--rx-green);
            font-size: 0.7rem;
            font-weight: 850;
            text-transform: uppercase;
            line-height: 1.25;
        }
        .rx-scenario-pill {
            border: 1px solid var(--rx-line);
            border-radius: 999px;
            padding: 3px 8px;
            color: var(--rx-muted);
            background: #fbfdfb;
            font-size: 0.68rem;
            font-weight: 750;
            white-space: nowrap;
        }
        .rx-scenario-title {
            color: var(--rx-ink);
            font-size: 1.04rem;
            font-weight: 850;
            line-height: 1.24;
            margin-bottom: 8px;
        }
        .rx-scenario-copy {
            color: var(--rx-muted);
            font-size: 0.82rem;
            line-height: 1.42;
            margin-bottom: 10px;
        }
        .rx-scenario-metrics {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 8px;
            margin-bottom: 10px;
        }
        .rx-scenario-metric {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #fbfdfb;
            padding: 8px 9px;
            min-height: 58px;
        }
        .rx-scenario-metric-label {
            color: var(--rx-muted);
            font-size: 0.66rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 3px;
        }
        .rx-scenario-metric-value {
            color: var(--rx-ink);
            font-size: 0.85rem;
            font-weight: 850;
            line-height: 1.25;
        }
        .rx-scenario-pages {
            color: var(--rx-ink);
            font-size: 0.78rem;
            line-height: 1.38;
            font-weight: 650;
            overflow-wrap: anywhere;
        }
        .rx-artifact-group {
            border-top: 1px solid var(--rx-line);
            padding-top: 12px;
            margin: 14px 0 18px;
        }
        .rx-artifact-heading {
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 10px;
        }
        .rx-artifact-title {
            color: var(--rx-ink);
            font-size: 1rem;
            font-weight: 800;
        }
        .rx-artifact-count {
            color: var(--rx-muted);
            font-size: 0.78rem;
            font-weight: 700;
        }
        .rx-artifact-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 10px;
        }
        .rx-artifact-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 12px 13px;
            min-height: 126px;
        }
        .rx-artifact-top {
            display: flex;
            justify-content: space-between;
            gap: 10px;
            margin-bottom: 7px;
        }
        .rx-artifact-file {
            color: var(--rx-ink);
            font-size: 0.86rem;
            font-weight: 800;
            overflow-wrap: anywhere;
        }
        .rx-artifact-use {
            color: var(--rx-blue);
            font-size: 0.72rem;
            font-weight: 800;
            white-space: nowrap;
        }
        .rx-artifact-purpose {
            color: var(--rx-muted);
            font-size: 0.82rem;
            line-height: 1.4;
            margin-bottom: 8px;
        }
        .rx-artifact-mime {
            color: var(--rx-muted);
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
        }
        .rx-lab-console {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 10px;
            margin: 8px 0 18px;
        }
        .rx-lab-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 12px 13px;
            min-height: 148px;
        }
        .rx-lab-card-ready {
            border-color: #c8e5d4;
            background: #f6fbf8;
        }
        .rx-lab-card-blocked {
            border-color: #efb6a8;
            background: #fff7f4;
        }
        .rx-lab-card-waiting,
        .rx-lab-card-needs-setup,
        .rx-lab-card-needs-measurement,
        .rx-lab-card-not-started {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-lab-top {
            display: flex;
            justify-content: space-between;
            gap: 8px;
            align-items: center;
            margin-bottom: 8px;
        }
        .rx-lab-label {
            color: var(--rx-muted);
            font-size: 0.72rem;
            font-weight: 750;
            text-transform: uppercase;
        }
        .rx-lab-status {
            color: var(--rx-ink);
            font-size: 0.68rem;
            font-weight: 750;
            white-space: nowrap;
        }
        .rx-lab-detail {
            color: var(--rx-ink);
            font-size: 0.85rem;
            line-height: 1.38;
            margin-bottom: 7px;
        }
        .rx-lab-action {
            color: var(--rx-muted);
            font-size: 0.78rem;
            line-height: 1.35;
        }
        .rx-lab-measure-panel {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 16px 18px;
            margin: 6px 0 18px;
            box-shadow: 0 8px 22px rgba(23, 32, 27, 0.05);
        }
        .rx-lab-measure-head {
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(230px, 0.42fr);
            gap: 14px;
            align-items: start;
            margin-bottom: 14px;
        }
        .rx-lab-measure-kicker {
            color: var(--rx-green);
            font-size: 0.74rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-lab-measure-title {
            color: var(--rx-ink);
            font-size: 1.16rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 7px;
        }
        .rx-lab-measure-copy {
            color: var(--rx-muted);
            font-size: 0.88rem;
            line-height: 1.48;
            max-width: 780px;
        }
        .rx-lab-measure-status {
            border-left: 4px solid var(--rx-blue);
            background: #f6fbf8;
            padding: 11px 12px;
        }
        .rx-lab-measure-grid {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 10px;
        }
        .rx-lab-measure-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #fbfdfb;
            padding: 12px 13px;
            min-height: 118px;
        }
        .rx-lab-measure-card-ready {
            border-color: #c8e5d4;
            background: #f6fbf8;
        }
        .rx-lab-measure-card-waiting {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-lab-measure-card-blocked {
            border-color: #efb6a8;
            background: #fff7f4;
        }
        .rx-lab-measure-label {
            color: var(--rx-muted);
            font-size: 0.7rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-lab-measure-value {
            color: var(--rx-ink);
            font-size: 0.94rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 6px;
            overflow-wrap: anywhere;
        }
        .rx-lab-measure-detail {
            color: var(--rx-muted);
            font-size: 0.76rem;
            line-height: 1.35;
        }
        .rx-lab-component-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 12px;
            margin: 10px 0 18px;
        }
        .rx-lab-component-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 14px 15px;
            min-height: 178px;
            box-shadow: 0 8px 22px rgba(23, 32, 27, 0.045);
        }
        .rx-lab-component-ready {
            border-color: #c8e5d4;
            background: #f6fbf8;
        }
        .rx-lab-component-waiting {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-lab-component-blocked {
            border-color: #efb6a8;
            background: #fff7f4;
        }
        .rx-lab-component-top {
            display: flex;
            justify-content: space-between;
            gap: 10px;
            align-items: flex-start;
            margin-bottom: 10px;
        }
        .rx-lab-component-kicker {
            color: var(--rx-green);
            font-size: 0.68rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        .rx-lab-component-title {
            color: var(--rx-ink);
            font-size: 1rem;
            line-height: 1.25;
            font-weight: 850;
            overflow-wrap: anywhere;
        }
        .rx-lab-component-status {
            border-left: 3px solid var(--rx-blue);
            background: rgba(255, 255, 255, 0.68);
            padding: 8px 9px;
            min-width: 112px;
        }
        .rx-lab-component-label {
            color: var(--rx-muted);
            font-size: 0.66rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 4px;
        }
        .rx-lab-component-value {
            color: var(--rx-ink);
            font-size: 0.84rem;
            line-height: 1.22;
            font-weight: 850;
            overflow-wrap: anywhere;
        }
        .rx-lab-component-detail {
            border-top: 1px solid var(--rx-line);
            color: var(--rx-muted);
            font-size: 0.74rem;
            line-height: 1.38;
            padding-top: 8px;
            margin-top: 8px;
        }
        .rx-lab-picture-grid {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 10px;
            margin: 10px 0 18px;
        }
        .rx-lab-picture-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 13px 14px;
            min-height: 166px;
            box-shadow: 0 8px 22px rgba(23, 32, 27, 0.04);
        }
        .rx-lab-picture-measured {
            border-color: #c8e5d4;
            background: #f6fbf8;
        }
        .rx-lab-picture-missing {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-lab-picture-label {
            color: var(--rx-muted);
            font-size: 0.68rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-lab-picture-title {
            color: var(--rx-ink);
            font-size: 0.94rem;
            line-height: 1.22;
            font-weight: 850;
            margin-bottom: 7px;
            overflow-wrap: anywhere;
        }
        .rx-lab-picture-value {
            color: var(--rx-ink);
            font-size: 0.82rem;
            line-height: 1.28;
            font-weight: 800;
            margin-bottom: 7px;
        }
        .rx-lab-picture-detail {
            color: var(--rx-muted);
            font-size: 0.72rem;
            line-height: 1.36;
        }
        .rx-protocol-console {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 16px 18px;
            margin: 6px 0 18px;
            box-shadow: 0 8px 22px rgba(23, 32, 27, 0.05);
        }
        .rx-protocol-head {
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(240px, 0.42fr);
            gap: 14px;
            align-items: start;
            margin-bottom: 14px;
        }
        .rx-protocol-kicker {
            color: var(--rx-green);
            font-size: 0.74rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-protocol-title {
            color: var(--rx-ink);
            font-size: 1.16rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 7px;
        }
        .rx-protocol-copy {
            color: var(--rx-muted);
            font-size: 0.88rem;
            line-height: 1.48;
            max-width: 780px;
        }
        .rx-protocol-status {
            border-left: 4px solid var(--rx-blue);
            background: #f6fbf8;
            padding: 11px 12px;
        }
        .rx-protocol-grid {
            display: grid;
            grid-template-columns: repeat(6, minmax(0, 1fr));
            gap: 10px;
        }
        .rx-protocol-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #fbfdfb;
            padding: 12px 13px;
            min-height: 118px;
        }
        .rx-protocol-card-ready {
            border-color: #c8e5d4;
            background: #f6fbf8;
        }
        .rx-protocol-card-waiting {
            border-color: #ead4aa;
            background: #fffaf0;
        }
        .rx-protocol-card-blocked {
            border-color: #efb6a8;
            background: #fff7f4;
        }
        .rx-protocol-label {
            color: var(--rx-muted);
            font-size: 0.7rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .rx-protocol-value {
            color: var(--rx-ink);
            font-size: 0.94rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 6px;
            overflow-wrap: anywhere;
        }
        .rx-protocol-detail {
            color: var(--rx-muted);
            font-size: 0.76rem;
            line-height: 1.35;
        }
        .rx-protocol-components {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 10px;
            margin: 8px 0 16px;
        }
        .rx-protocol-component {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 13px 14px;
            min-height: 176px;
        }
        .rx-protocol-component-optional {
            border-color: #d7dfda;
            background: #fbfdfb;
        }
        .rx-protocol-component-required {
            border-color: #c8e5d4;
            background: #f6fbf8;
        }
        .rx-protocol-component-title {
            color: var(--rx-ink);
            font-size: 0.98rem;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 7px;
        }
        .rx-protocol-component-meta {
            color: var(--rx-green);
            font-size: 0.72rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 8px;
        }
        .rx-protocol-component-copy {
            color: var(--rx-muted);
            font-size: 0.8rem;
            line-height: 1.38;
            margin-bottom: 8px;
        }
        .rx-protocol-component-foot {
            color: var(--rx-ink);
            font-size: 0.76rem;
            line-height: 1.35;
        }
        .rx-operator-flow {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 10px;
            margin: 10px 0 18px;
        }
        .rx-operator-step {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 12px 13px;
            min-height: 150px;
            box-shadow: 0 8px 22px rgba(23, 32, 27, 0.04);
            position: relative;
        }
        .rx-operator-step::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            right: 0;
            height: 4px;
            border-radius: 8px 8px 0 0;
            background: var(--rx-blue);
        }
        .rx-operator-step-ready {
            border-color: #c8e5d4;
            background: #f6fbf8;
        }
        .rx-operator-step-blocked {
            border-color: #efb6a8;
            background: #fff7f4;
        }
        .rx-operator-step-required {
            border-color: #c8d7ec;
            background: #f7fbff;
        }
        .rx-operator-kicker {
            color: var(--rx-muted);
            font-size: 0.68rem;
            font-weight: 850;
            text-transform: uppercase;
            margin: 4px 0 7px;
        }
        .rx-operator-title {
            color: var(--rx-ink);
            font-size: 0.96rem;
            line-height: 1.24;
            font-weight: 850;
            margin-bottom: 7px;
            overflow-wrap: anywhere;
        }
        .rx-operator-copy {
            color: var(--rx-muted);
            font-size: 0.74rem;
            line-height: 1.36;
        }
        .rx-operator-components {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 12px;
            margin: 10px 0 18px;
        }
        .rx-operator-component {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 14px 15px;
            min-height: 240px;
            box-shadow: 0 8px 22px rgba(23, 32, 27, 0.045);
        }
        .rx-operator-component-recommended {
            border-color: #c8e5d4;
            background: #f6fbf8;
        }
        .rx-operator-component-optional {
            border-color: #d7dfda;
            background: #fbfdfb;
        }
        .rx-operator-head {
            display: flex;
            justify-content: space-between;
            gap: 10px;
            align-items: flex-start;
            margin-bottom: 10px;
        }
        .rx-operator-pill {
            border: 1px solid #d6e4dc;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.72);
            color: var(--rx-ink);
            font-size: 0.66rem;
            line-height: 1.1;
            font-weight: 850;
            padding: 5px 8px;
            white-space: nowrap;
        }
        .rx-operator-list {
            display: grid;
            gap: 6px;
            margin-top: 7px;
        }
        .rx-operator-list-item {
            border-left: 3px solid #c8e5d4;
            background: rgba(255, 255, 255, 0.7);
            color: var(--rx-ink);
            font-size: 0.72rem;
            line-height: 1.34;
            padding: 6px 8px;
        }
        .rx-operator-list-item-stop {
            border-left-color: #d97b64;
            color: var(--rx-muted);
        }
        .rx-timeline {
            display: grid;
            grid-template-columns: repeat(9, minmax(118px, 1fr));
            gap: 8px;
            overflow-x: auto;
            padding-bottom: 8px;
            margin: 8px 0 16px;
        }
        .rx-timeline-card {
            border: 1px solid var(--rx-line);
            border-radius: 8px;
            background: #ffffff;
            padding: 11px 11px 12px;
            min-height: 150px;
            position: relative;
        }
        .rx-timeline-card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            border-radius: 8px 8px 0 0;
            background: #c8d3cc;
        }
        .rx-timeline-done::before {
            background: var(--rx-green);
        }
        .rx-timeline-current::before {
            background: var(--rx-blue);
        }
        .rx-timeline-blocked::before {
            background: #b64f3c;
        }
        .rx-timeline-waiting::before {
            background: var(--rx-amber);
        }
        .rx-timeline-step {
            color: var(--rx-muted);
            font-size: 0.7rem;
            font-weight: 750;
            text-transform: uppercase;
            margin-bottom: 7px;
        }
        .rx-timeline-title {
            color: var(--rx-ink);
            font-size: 0.9rem;
            font-weight: 800;
            line-height: 1.25;
            margin-bottom: 7px;
        }
        .rx-timeline-status {
            display: inline-block;
            border: 1px solid var(--rx-line);
            border-radius: 999px;
            padding: 2px 7px;
            color: var(--rx-muted);
            font-size: 0.7rem;
            font-weight: 750;
            margin-bottom: 8px;
        }
        .rx-timeline-why {
            color: var(--rx-muted);
            font-size: 0.78rem;
            line-height: 1.35;
        }
        .rx-progress-shell {
            border: 1px solid var(--rx-line);
            border-radius: 999px;
            background: #eef3ef;
            height: 10px;
            overflow: hidden;
            margin: 4px 0 12px;
        }
        .rx-progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--rx-green), var(--rx-blue));
        }
        .rx-workbench,
        .rx-module-grid,
        .rx-pipeline,
        .rx-command-grid,
        .rx-hero-top,
        .rx-hero-grid,
        .rx-lab-status-head,
        .rx-experience-head,
        .rx-experience-grid,
        .rx-guided-head,
        .rx-guided-grid,
        .rx-contract-head,
        .rx-contract-grid,
        .rx-report-head,
        .rx-report-grid,
        .rx-profile-summary,
        .rx-profile-handoff,
        .rx-profile-decision-head,
        .rx-profile-decision-grid,
        .rx-profile-dimensions,
        .rx-evidence-head,
        .rx-evidence-grid,
        .rx-evidence-topic-grid,
        .rx-evidence-source-grid,
        .rx-evidence-claim-grid,
        .rx-log-grid,
        .rx-session-gallery,
        .rx-session-head,
        .rx-draft-head,
        .rx-draft-grid,
        .rx-draft-components,
        .rx-quality-head,
        .rx-quality-grid,
        .rx-entry-grid,
        .rx-training-head,
        .rx-training-grid,
        .rx-week-grid,
        .rx-feedback-head,
        .rx-feedback-grid,
        .rx-loop-grid,
        .rx-decision-head,
        .rx-qm-match-grid,
        .rx-pilot-head,
        .rx-pilot-grid,
        .rx-release-head,
        .rx-release-grid,
        .rx-beta-head,
        .rx-beta-grid,
        .rx-export-head,
        .rx-export-grid,
        .rx-qm-input-grid,
        .rx-lab-board-head,
        .rx-lab-lanes,
        .rx-start-grid,
        .rx-scenario-grid,
        .rx-artifact-grid,
        .rx-lab-console,
        .rx-lab-measure-head,
        .rx-lab-measure-grid,
        .rx-lab-component-grid,
        .rx-lab-picture-grid,
        .rx-protocol-head,
        .rx-protocol-grid,
        .rx-protocol-components,
        .rx-operator-flow,
        .rx-operator-components {
            grid-template-columns: 1fr !important;
        }
        .rx-strip,
        .rx-lab-status-grid,
        .rx-action-rail {
            grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        }
        .rx-lab-status,
        .rx-hero-console,
        .rx-experience-console,
        .rx-guided-console,
        .rx-contract-console,
        .rx-report-dashboard,
        .rx-profile-panel,
        .rx-profile-decision,
        .rx-quality-console,
        .rx-release-console,
        .rx-export-console {
            padding: 14px 14px !important;
            margin-bottom: 12px !important;
            box-shadow: 0 8px 22px rgba(23, 32, 27, 0.055);
        }
        .rx-hero-tile,
        .rx-lab-status-tile,
        .rx-experience-card,
        .rx-guided-card,
        .rx-action-card,
        .rx-contract-card,
        .rx-report-card,
        .rx-profile-decision-card,
        .rx-quality-card,
        .rx-entry-card {
            min-height: auto !important;
            padding: 11px 12px !important;
        }
        @media (min-width: 901px) {
            .block-container {
                border-left: 1px solid rgba(220, 227, 222, 0.8);
                border-right: 1px solid rgba(220, 227, 222, 0.8);
                background: #f8fbf8;
                min-height: 100vh;
            }
        }
        @media (max-width: 900px) {
            .block-container {
                max-width: 100%;
                padding-left: 0.7rem;
                padding-right: 0.7rem;
            }
            .rx-strip {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
            .rx-workbench {
                grid-template-columns: 1fr;
            }
            .rx-module-grid {
                grid-template-columns: 1fr;
            }
            .rx-pipeline {
                grid-template-columns: 1fr;
            }
            .rx-command-grid {
                grid-template-columns: 1fr;
            }
            .rx-hero-top,
            .rx-hero-grid,
            .rx-lab-status-head,
            .rx-lab-status-grid,
            .rx-experience-head,
            .rx-experience-grid,
            .rx-guided-head,
            .rx-guided-grid,
            .rx-action-rail,
            .rx-contract-head,
            .rx-contract-grid,
            .rx-report-head,
            .rx-report-grid,
            .rx-profile-summary,
            .rx-profile-handoff,
            .rx-profile-decision-head,
            .rx-profile-decision-grid,
            .rx-profile-dimensions,
            .rx-evidence-head,
            .rx-evidence-grid,
            .rx-evidence-topic-grid,
            .rx-evidence-source-grid,
            .rx-evidence-claim-grid,
            .rx-log-grid,
            .rx-session-gallery,
            .rx-session-head,
            .rx-draft-head,
            .rx-draft-grid,
            .rx-draft-components,
            .rx-quality-head,
            .rx-quality-grid,
            .rx-entry-grid,
            .rx-training-head,
            .rx-training-grid,
            .rx-week-grid,
            .rx-feedback-head,
            .rx-feedback-grid,
            .rx-loop-grid,
            .rx-decision-head,
            .rx-qm-match-grid,
            .rx-pilot-head,
            .rx-pilot-grid,
            .rx-release-head,
            .rx-release-grid,
            .rx-beta-head,
            .rx-beta-grid,
            .rx-export-head,
            .rx-export-grid,
            .rx-qm-input-grid {
                grid-template-columns: 1fr;
            }
            .rx-lab-board-head,
            .rx-lab-lanes {
                grid-template-columns: 1fr;
            }
            .rx-log-head {
                display: block;
            }
            .rx-qm-input-head {
                display: block;
            }
            .rx-qm-input-status {
                margin-top: 10px;
            }
            .rx-log-path {
                margin-top: 10px;
            }
            .rx-start-grid {
                grid-template-columns: 1fr;
            }
            .rx-scenario-grid {
                grid-template-columns: 1fr;
            }
            .rx-artifact-grid {
                grid-template-columns: 1fr;
            }
            .rx-lab-console,
            .rx-lab-measure-head,
            .rx-lab-measure-grid,
            .rx-lab-component-grid,
            .rx-lab-picture-grid,
            .rx-protocol-head,
            .rx-protocol-grid,
            .rx-protocol-components,
            .rx-operator-flow,
            .rx-operator-components {
                grid-template-columns: 1fr;
            }
            .rx-timeline {
                grid-template-columns: repeat(9, 170px);
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _page_header(kicker: str, title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="rx-header">
            <div class="rx-kicker">{kicker}</div>
            <div class="rx-title">{title}</div>
            <div class="rx-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _workbench_strip() -> None:
    passport = st.session_state.passport
    summary = summarize_benchmark_sessions(st.session_state.benchmark_sessions)
    safety_status = passport["safety_gate"]["status"]
    measured_label = passport["areas_assessed"]["label"]
    session_count = int(summary["session_count"])
    handoff_allowed = bool(passport.get("starter_path", {}).get("available"))
    if safety_status == "RED":
        next_label = "Resolve Safety Gate"
        next_detail = "Safety Gate can block training handoff, but it never changes measured performance."
    elif passport["areas_assessed"]["assessed"] < 2:
        next_label = "Benchmark Protocol"
        next_detail = "Measure at least two performance dimensions before comparing strongest area and main gap."
    elif session_count == 0:
        next_label = "Benchmark Log"
        next_detail = "Save raw component results, units, RPE, equipment, substitutions, and notes."
    elif not handoff_allowed:
        next_label = zh(passport.get("next_action", "Review measurement gate"))
        next_detail = "Training handoff remains gated until Safety and measurement prerequisites are satisfied."
    else:
        next_label = "Starter Path / Retest"
        next_detail = "Use the current measured picture for a conservative block, then retest with the same protocol."

    tiles = [
        {
            "label": "Safety Gate",
            "value": safety_status,
            "detail": "Separate from performance scoring.",
            "status": "blocked" if safety_status == "RED" else "ready",
        },
        {
            "label": "Measured picture",
            "value": measured_label,
            "detail": "Missing tests stay Not tested.",
            "status": "ready" if passport["areas_assessed"]["assessed"] >= 2 else "waiting",
        },
        {
            "label": "Benchmark log",
            "value": f"{session_count} sessions",
            "detail": summary["message"],
            "status": "ready" if session_count > 0 else "waiting",
        },
        {
            "label": "Training handoff",
            "value": "Available" if handoff_allowed else "Gated",
            "detail": "Generated only after safety and measurement gates allow it.",
            "status": "ready" if handoff_allowed else "waiting",
        },
    ]
    html = [
        '<div class="rx-lab-status">',
        '<div class="rx-lab-status-head">',
        "<div>",
        '<div class="rx-lab-status-kicker">Measure-first status</div>',
        '<div class="rx-lab-status-title">当前测试状态，而不是 AI 猜测状态</div>',
        '<div class="rx-lab-status-copy">Safety Gate、自报 intake、measured performance、Benchmark Log 和训练交接保持分离；没有实测的数据继续显示为 Not tested。</div>',
        "</div>",
        '<div class="rx-lab-status-next">',
        '<div class="rx-lab-status-next-label">Next best action</div>',
        f'<div class="rx-lab-status-next-value">{escape(zh(next_label))}</div>',
        f'<div class="rx-lab-status-next-detail">{escape(zh(next_detail))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-lab-status-grid">',
    ]
    for tile in tiles:
        class_name = {
            "ready": "rx-lab-status-ready",
            "blocked": "rx-lab-status-blocked",
        }.get(tile["status"], "rx-lab-status-waiting")
        html.append(
            (
                f'<div class="rx-lab-status-tile {class_name}">'
                f'<div class="rx-lab-status-label">{escape(zh(tile["label"]))}</div>'
                f'<div class="rx-lab-status-value">{escape(zh(tile["value"]))}</div>'
                f'<div class="rx-lab-status-detail">{escape(zh(tile["detail"]))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _status_badge(status: str) -> None:
    if status == "GREEN":
        st.success("安全门：GREEN")
    elif status == "YELLOW":
        st.warning("安全门：YELLOW")
    else:
        st.error("安全门：RED")


def _metric_row(items: list[tuple[str, str | int | None]]) -> None:
    columns = st.columns(len(items))
    for column, (label, value) in zip(columns, items):
        column.metric(label, "需要进一步确认" if value is None else zh(value))


def _test_status(profile: dict, field_id: str) -> str:
    return "measured" if profile.get(field_id) is not None else "not_tested"


def _measured_number_input(
    container,
    profile: dict,
    field_id: str,
    label: str,
    min_value: int,
    max_value: int,
    fallback: int,
    unit: str,
    step: int = 1,
) -> tuple[bool, int | None]:
    status_options = ["not_tested", "measured"]
    status = container.selectbox(
        f"{label} 状态",
        status_options,
        index=status_options.index(_test_status(profile, field_id)),
        format_func=lambda value: "Measured / 已实测" if value == "measured" else "Not tested / 未测试",
        key=f"{field_id}_status",
    )
    if status != "measured":
        container.caption(f"Not tested：暂不填写 {label}，提交后保存为空值。")
        return False, None

    value = container.number_input(
        f"{label} ({unit})",
        min_value,
        max_value,
        int(profile.get(field_id) or fallback),
        step=step,
        key=f"{field_id}_value",
    )
    return True, int(value)


def _hero_status_console(passport: dict, summary: dict, first_run: dict) -> None:
    safety_status = passport["safety_gate"]["status"]
    measured_count = int(passport.get("measured_performance_areas", {}).get("count", 0) or 0)
    starter_available = bool(passport.get("starter_path", {}).get("available"))
    if safety_status == "RED":
        action_detail = "Safety Gate 阻断自动训练交接，先处理安全边界。"
    elif measured_count < 2:
        action_detail = "至少完成两个 measured performance dimensions 后，再比较 strongest area 和 main gap。"
    elif starter_available:
        action_detail = "可以查看保守的 4-week Starter Path，并在每周记录 RPE 与完成率。"
    else:
        action_detail = first_run["next_action"]

    tile_class = {
        "GREEN": "rx-hero-tile-ready",
        "YELLOW": "rx-hero-tile-waiting",
        "RED": "rx-hero-tile-blocked",
    }.get(safety_status, "rx-hero-tile-waiting")
    starter_class = "rx-hero-tile-ready" if starter_available else "rx-hero-tile-waiting"
    benchmark_class = "rx-hero-tile-ready" if int(summary.get("session_count", 0) or 0) else "rx-hero-tile-waiting"
    measured_class = "rx-hero-tile-ready" if measured_count >= 2 else "rx-hero-tile-waiting"

    tiles = [
        (
            "Safety Gate",
            safety_status,
            "阻断训练交接，但不参与表现评分。",
            tile_class,
        ),
        (
            "Measured Picture",
            passport["current_measured_picture"],
            passport["measured_performance_areas"]["label"],
            measured_class,
        ),
        (
            "Benchmark Log",
            f"{summary['session_count']} sessions",
            summary["message"],
            benchmark_class,
        ),
        (
            "Starter Path",
            "Available" if starter_available else "Gated",
            "只在安全门和实测数据条件满足后生成。",
            starter_class,
        ),
    ]

    html = [
        '<div class="rx-hero-console">',
        '<div class="rx-hero-top">',
        '<div>',
        '<div class="rx-hero-label">Measurement-first console</div>',
        '<div class="rx-hero-title">SportRx 当前测试状态</div>',
        '<div class="rx-hero-copy">先确认安全边界，再完成 SportRx Hybrid Benchmark v1。缺失表现测试保持 Not tested；Safety Gate 不会改变 measured performance。</div>',
        "</div>",
        '<div class="rx-hero-action">',
        '<div class="rx-hero-action-label">Next Action</div>',
        f'<div class="rx-hero-action-value">{escape(str(first_run["next_page"]))}</div>',
        f'<div class="rx-hero-action-detail">{escape(str(action_detail))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-hero-grid">',
    ]
    for label, value, detail, class_name in tiles:
        html.append(
            (
                f'<div class="rx-hero-tile {class_name}">'
                f'<div class="rx-hero-tile-label">{escape(label)}</div>'
                f'<div class="rx-hero-tile-value">{escape(zh(value))}</div>'
                f'<div class="rx-hero-tile-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _demo_experience_console(console: dict) -> None:
    html = [
        '<div class="rx-experience-console">',
        '<div class="rx-experience-head">',
        '<div>',
        '<div class="rx-experience-kicker">Demo experience</div>',
        '<div class="rx-experience-title">让第一次打开像 sport performance lab</div>',
        f'<div class="rx-experience-copy">{escape(console["primary_message"])}</div>',
        "</div>",
        '<div class="rx-experience-status">',
        '<div class="rx-experience-label">Status</div>',
        f'<div class="rx-experience-value">{escape(zh(console["status"]))}</div>',
        f'<div class="rx-experience-detail">{escape(str(console["ready_cards"]))} / {escape(str(console["total_cards"]))} first-screen cards ready.</div>',
        "</div>",
        "</div>",
        '<div class="rx-experience-grid">',
    ]
    for card in console["cards"]:
        class_name = "rx-experience-card-ready" if card["status"] == "ready" else "rx-experience-card-waiting"
        html.append(
            (
                f'<div class="rx-experience-card {class_name}">'
                f'<div class="rx-experience-label">{escape(card["label"])}</div>'
                f'<div class="rx-experience-value">{escape(zh(card["value"]))}</div>'
                f'<div class="rx-experience-detail">{escape(zh(card["detail"]))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _guided_review_console(console: dict) -> None:
    html = [
        '<div class="rx-guided-console">',
        '<div class="rx-guided-head">',
        '<div>',
        '<div class="rx-guided-kicker">Guided review</div>',
        '<div class="rx-guided-title">下一步应该点哪里</div>',
        f'<div class="rx-guided-copy">{escape(console["primary_message"])}</div>',
        "</div>",
        '<div class="rx-guided-meter">',
        '<div class="rx-guided-label">Progress</div>',
        f'<div class="rx-guided-value">{escape(str(console["progress_percent"]))}%</div>',
        f'<div class="rx-guided-detail">{escape(str(console["ready_cards"]))} / {escape(str(console["total_cards"]))} navigation cards ready.</div>',
        "</div>",
        "</div>",
        '<div class="rx-progress-shell">',
        f'<div class="rx-progress-fill" style="width: {int(console["progress_percent"])}%"></div>',
        "</div>",
        '<div class="rx-guided-grid">',
    ]
    for card in console["cards"]:
        class_name = "rx-guided-card-ready" if card["status"] == "ready" else "rx-guided-card-waiting"
        html.append(
            (
                f'<div class="rx-guided-card {class_name}">'
                f'<div class="rx-guided-label">{escape(card["label"])}</div>'
                f'<div class="rx-guided-value">{escape(zh(card["value"]))}</div>'
                f'<div class="rx-guided-detail">{escape(zh(card["detail"]))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _guided_action_rail(console: dict) -> None:
    html = ['<div class="rx-action-rail">']
    for index, action in enumerate(console["quick_actions"]):
        primary_class = " rx-action-card-primary" if index == 0 else ""
        html.append(
            (
                f'<div class="rx-action-card{primary_class}">'
                f'<div class="rx-action-label">{escape(action["label"])}</div>'
                f'<div class="rx-action-target">{escape(action["target"])}</div>'
                f'<div class="rx-action-purpose">{escape(action["purpose"])}</div>'
                "</div>"
            )
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)

    action_cols = st.columns(len(console["quick_actions"]))
    for col, action in zip(action_cols, console["quick_actions"]):
        with col:
            if action["id"] == "load_complete_loop":
                st.button(
                    action["label"],
                    width="stretch",
                    type="primary",
                    on_click=_load_demo_state,
                    key=f"action_rail_{action['id']}",
                )
            else:
                st.button(
                    action["label"],
                    width="stretch",
                    on_click=_set_page,
                    args=(action["target"],),
                    key=f"action_rail_{action['id']}",
                )


def _lab_workflow_board(passport: dict, summary: dict, feedback_dashboard: dict, first_run: dict) -> None:
    measured_count = int(passport.get("measured_performance_areas", {}).get("count", 0) or 0)
    benchmark_count = int(summary.get("session_count", 0) or 0)
    feedback_weeks = int(feedback_dashboard.get("adherence", {}).get("weeks_recorded", 0) or 0)
    retest_count = len(feedback_dashboard.get("retest_comparisons", []))
    safety_status = passport.get("safety_gate", {}).get("status", "UNKNOWN")
    starter_available = bool(passport.get("starter_path", {}).get("available"))
    safety_blocked = safety_status == "RED"
    lanes = [
        {
            "label": "Lane 01",
            "title": "Intake contract",
            "status": "blocked" if safety_blocked else "ready",
            "method": "Quick Match + Intake Precision Audit",
            "proof": f"Safety Gate {safety_status}; self-report is kept separate from measured tests.",
            "output": "粗筛路线、时间约束和安全边界。",
        },
        {
            "label": "Lane 02",
            "title": "Measurement layer",
            "status": "ready" if measured_count >= 2 and benchmark_count else "waiting",
            "method": "SportRx Hybrid Benchmark v1",
            "proof": f"{measured_count} measured areas; {benchmark_count} Benchmark Log session(s).",
            "output": "Current measured picture；缺失项目保持 Not tested。",
        },
        {
            "label": "Lane 03",
            "title": "Training handoff",
            "status": "ready" if starter_available and feedback_weeks else "waiting",
            "method": "Starter Path + weekly RPE + retest",
            "proof": f"Starter Path {'available' if starter_available else 'waiting'}; {feedback_weeks} feedback week(s); {retest_count} retest comparison(s).",
            "output": "保守训练建议、完成率/RPE 反馈和复测解释边界。",
        },
    ]
    html = [
        '<div class="rx-lab-board">',
        '<div class="rx-lab-board-head">',
        '<div>',
        '<div class="rx-lab-board-kicker">Lab workflow board</div>',
        '<div class="rx-lab-board-title">从输入到实测，再到训练交接</div>',
        '<div class="rx-lab-board-copy">SportRx 的首屏按实验室工作流组织：先说明输入能不能量化，再要求至少两个实测维度，最后才允许 Training Handoff。这个面板只展示状态，不改变任何规则。</div>',
        "</div>",
        '<div class="rx-lab-board-action">',
        '<div class="rx-lab-board-action-label">Recommended next page</div>',
        f'<div class="rx-lab-board-action-value">{escape(str(first_run["next_page"]))}</div>',
        f'<div class="rx-lab-board-action-detail">{escape(str(first_run["next_action"]))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-lab-lanes">',
    ]
    for lane in lanes:
        html.append(
            (
                f'<div class="rx-lab-lane rx-lab-lane-{escape(lane["status"])}">'
                f'<div class="rx-lab-lane-label">{escape(lane["label"])} · {escape(zh(lane["status"]))}</div>'
                f'<div class="rx-lab-lane-title">{escape(lane["title"])}</div>'
                f'<div class="rx-lab-lane-row"><strong>Method</strong><br>{escape(lane["method"])}</div>'
                f'<div class="rx-lab-lane-row"><strong>Proof</strong><br>{escape(lane["proof"])}</div>'
                f'<div class="rx-lab-lane-row"><strong>Output</strong><br>{escape(lane["output"])}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _report_dashboard(report: dict) -> None:
    safety_status = report["safety_gate"]["status"]
    measured = report["measurement"]["measured_performance_areas"]
    benchmark = report["measurement"]["benchmark_sessions"]
    lab_quality = report["measurement"].get("lab_test_quality", {})
    starter_available = bool(report["starter_path_status"]["available"])
    safety_class = {
        "GREEN": "rx-report-card-ready",
        "YELLOW": "rx-report-card-waiting",
        "RED": "rx-report-card-blocked",
    }.get(safety_status, "rx-report-card-waiting")
    measured_class = "rx-report-card-ready" if int(measured.get("count", 0) or 0) >= 2 else "rx-report-card-waiting"
    benchmark_class = "rx-report-card-ready" if int(benchmark.get("session_count", 0) or 0) else "rx-report-card-waiting"
    lab_quality_class = "rx-report-card-ready" if lab_quality.get("status") == "review_ready_measurement_record" else "rx-report-card-waiting"
    starter_class = "rx-report-card-ready" if starter_available else "rx-report-card-waiting"
    cards = [
        ("Report Status", report["status_label"], "报告只总结当前已知信息。", "rx-report-card-ready" if starter_available else "rx-report-card-waiting"),
        ("Safety Gate", safety_status, "可阻断训练交接，不参与表现评分。", safety_class),
        ("Measured Areas", measured["label"], "至少两个实测表现区域后才比较短板。", measured_class),
        ("Benchmark Logs", f"{benchmark['session_count']} sessions", benchmark["message"], benchmark_class),
        ("Lab Test Quality", lab_quality.get("status", "not_reviewed"), lab_quality.get("next_action", "Protocol provenance has not been reviewed."), lab_quality_class),
        ("Training Profile", report["training_profile"], "当前训练画像，不代表天赋或长期上限。", "rx-report-card-ready"),
        ("Strongest Area", report["strongest_area"], "只基于可用实测维度。", measured_class),
        ("Main Gap", report["main_gap"], "数据不足时保持 Not enough measured data。", measured_class),
        ("Starter Path", "Available" if starter_available else "Gated", zh(report["starter_path_status"].get("reason") or report["starter_path_status"].get("based_on_gap")), starter_class),
    ]

    html = [
        '<div class="rx-report-dashboard">',
        '<div class="rx-report-head">',
        '<div>',
        '<div class="rx-report-kicker">Training profile dashboard</div>',
        f'<div class="rx-report-title">{escape(report["title"])}</div>',
        f'<div class="rx-report-copy">{escape(report["claim_boundary"])}</div>',
        "</div>",
        '<div class="rx-report-next">',
        '<div class="rx-report-next-label">Next Action</div>',
        f'<div class="rx-report-next-value">{escape(zh(report["next_action"]))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-report-grid">',
    ]
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-report-card {class_name}">'
                f'<div class="rx-report-card-label">{escape(label)}</div>'
                f'<div class="rx-report-card-value">{escape(zh(value))}</div>'
                f'<div class="rx-report-card-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _benchmark_log_dashboard(summary: dict, benchmark: dict, import_result: dict, comparisons: list[dict]) -> None:
    session_count = int(summary.get("session_count", 0) or 0)
    measured_components = len(summary.get("measured_components", []) or [])
    import_count = len(import_result.get("profile_patch", {}) or {})
    retest_count = len(comparisons)
    path = benchmark["path"]
    interpretation_ready = measured_components >= 2
    cards = [
        (
            "Sessions",
            f"{session_count} logged",
            summary.get("latest_date") or "No benchmark session recorded yet.",
            "rx-log-card-ready" if session_count else "rx-log-card-waiting",
        ),
        (
            "Measured Components",
            str(measured_components),
            "Raw components saved locally; missing tests stay Not tested.",
            "rx-log-card-ready" if measured_components >= 2 else "rx-log-card-waiting",
        ),
        (
            "Interpretation",
            "Ready" if interpretation_ready else "Wait",
            "At least two measured components are recommended before interpreting gap direction.",
            "rx-log-card-ready" if interpretation_ready else "rx-log-card-waiting",
        ),
        (
            "HYROX Import",
            f"{import_count} fields",
            "Only unit-compatible raw results can update HYROX Check.",
            "rx-log-card-ready" if import_count else "rx-log-card-waiting",
        ),
        (
            "Retest",
            f"{retest_count} comparisons" if retest_count else "Waiting",
            summary.get("message", "Record another session using the same protocol."),
            "rx-log-card-ready" if retest_count else "rx-log-card-waiting",
        ),
    ]
    html = [
        '<div class="rx-log-dashboard">',
        '<div class="rx-log-head">',
        '<div>',
        '<div class="rx-log-kicker">Benchmark log console</div>',
        '<div class="rx-log-title">原始测试台账状态</div>',
        '<div class="rx-log-copy">这里先保存 raw results、RPE、器械、替代动作和 protocol 偏离。SportRx 不把这些记录转换成 percentile、预测或医学结论。</div>',
        "</div>",
        '<div class="rx-log-path">',
        '<div class="rx-log-label">Benchmark Path</div>',
        f'<div class="rx-log-value">{escape(zh(path))}</div>',
        f'<div class="rx-log-detail">{escape(benchmark["spec"]["version"])}</div>',
        "</div>",
        "</div>",
        '<div class="rx-log-grid">',
    ]
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-log-card {class_name}">'
                f'<div class="rx-log-label">{escape(label)}</div>'
                f'<div class="rx-log-value">{escape(zh(value))}</div>'
                f'<div class="rx-log-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _benchmark_session_gallery(sessions: list[dict]) -> None:
    html = ['<div class="rx-session-gallery">']
    for index, session in enumerate(reversed(sessions), start=1):
        quality = session.get("session_quality", {})
        compatibility = session.get("import_compatibility", {})
        quality_status = quality.get("status", "not_reviewed")
        compatibility_status = compatibility.get("status", "not_reviewed")
        completed = [
            result
            for result in session.get("component_results", [])
            if result.get("completed") and result.get("value") is not None
        ]
        missing = [
            result
            for result in session.get("component_results", [])
            if not (result.get("completed") and result.get("value") is not None)
        ]
        status_class = "rx-session-status"
        if quality_status != "ready_to_save":
            status_class += " rx-session-status-waiting"
        if quality.get("issues"):
            status_class = "rx-session-status rx-session-status-blocked"

        component_pills = []
        for result in completed:
            value = result.get("value")
            unit = result.get("value_unit") or ""
            rpe = result.get("rpe_0_10")
            rpe_label = "RPE n/a" if rpe is None else f"RPE {rpe:g}"
            component_pills.append(
                (
                    '<span class="rx-session-pill">'
                    f'{escape(result.get("test", result.get("component_id", "component")))}: '
                    f'{escape(str(value))} {escape(unit)} · {escape(rpe_label)}'
                    "</span>"
                )
            )
        for result in missing[:3]:
            component_pills.append(
                (
                    '<span class="rx-session-pill rx-session-pill-missing">'
                    f'{escape(result.get("test", result.get("component_id", "component")))}: Not tested'
                    "</span>"
                )
            )
        if len(missing) > 3:
            component_pills.append(
                f'<span class="rx-session-pill rx-session-pill-missing">+{len(missing) - 3} Not tested</span>'
            )

        notes = session.get("notes") or "No session notes recorded."
        html.append(
            (
                '<div class="rx-session-card">'
                '<div class="rx-session-head">'
                "<div>"
                f'<div class="rx-session-kicker">Benchmark session {len(sessions) - index + 1}</div>'
                f'<div class="rx-session-title">{escape(session.get("date", "unknown date"))} · {escape(zh(session.get("benchmark_path", "unknown path")))}</div>'
                f'<div class="rx-session-meta">{escape(session.get("benchmark_name", "SportRx Hybrid Benchmark"))} · Protocol {escape(session.get("protocol_version", "unknown"))}</div>'
                "</div>"
                f'<div class="{status_class}">'
                '<div class="rx-session-status-label">Quality / Import</div>'
                f'<div class="rx-session-status-value">{escape(zh(quality_status))}<br>{escape(zh(compatibility_status))}</div>'
                "</div>"
                "</div>"
                f'<div class="rx-session-meta">{len(completed)} measured components · {quality.get("measured_area_count", 0)} measured areas · {len(compatibility.get("importable_fields", []))} HYROX import fields</div>'
                f'<div class="rx-session-components">{"".join(component_pills)}</div>'
                f'<div class="rx-session-notes">{escape(notes)}</div>'
                "</div>"
            )
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _benchmark_draft_session_board(session: dict) -> None:
    quality = session.get("session_quality", {})
    compatibility = session.get("import_compatibility", {})
    results = session.get("component_results", [])
    completed = [item for item in results if item.get("completed") and item.get("value") is not None]
    not_tested = [item for item in results if not (item.get("completed") and item.get("value") is not None)]
    missing_rpe = [item for item in completed if item.get("rpe_0_10") is None]
    save_allowed = bool(quality.get("save_allowed"))
    cards = [
        (
            "Save Gate",
            "允许保存" if save_allowed else "需要补齐",
            "至少需要一个 completed component 和 raw result。",
            "rx-draft-card-ready" if save_allowed else "rx-draft-card-blocked",
        ),
        (
            "Measured",
            f"{len(completed)} / {len(results)}",
            "只有完成且有原始结果的组件会进入 measured log。",
            "rx-draft-card-ready" if completed else "rx-draft-card-waiting",
        ),
        (
            "RPE",
            "等待测量" if not completed else "完整" if not missing_rpe else f"{len(missing_rpe)} missing",
            "RPE 是执行负荷记录，不是表现分。",
            "rx-draft-card-ready" if completed and not missing_rpe else "rx-draft-card-waiting",
        ),
        (
            "HYROX Import",
            zh(compatibility.get("status", "not_reviewed")),
            zh(compatibility.get("next_action", "保存为 raw Benchmark Log。")),
            "rx-draft-card-ready" if compatibility.get("hyrox_import_ready") else "rx-draft-card-waiting",
        ),
    ]
    html = [
        '<div class="rx-draft-board">',
        '<div class="rx-draft-head">',
        "<div>",
        '<div class="rx-draft-kicker">Draft session review</div>',
        '<div class="rx-draft-title">保存前先看这次记录够不够干净</div>',
        '<div class="rx-draft-copy">这里检查 raw result、unit、RPE、器械和导入兼容性。它只做数据质量检查，不做表现评分、percentile 或完赛预测。</div>',
        "</div>",
        '<div class="rx-draft-status">',
        '<div class="rx-draft-label">Session status</div>',
        f'<div class="rx-draft-value">{escape(zh(quality.get("status", "not_reviewed")))}</div>',
        f'<div class="rx-draft-detail">{escape(zh(quality.get("claim_boundary", "")))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-draft-grid">',
    ]
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-draft-card {class_name}">'
                f'<div class="rx-draft-label">{escape(label)}</div>'
                f'<div class="rx-draft-value">{escape(zh(value))}</div>'
                f'<div class="rx-draft-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append('</div><div class="rx-draft-components">')
    for result in results:
        measured = result.get("completed") and result.get("value") is not None
        class_name = "rx-draft-component-measured" if measured else "rx-draft-component-missing"
        value = "Not tested" if not measured else f"{result.get('value')} {result.get('value_unit')}"
        rpe = "RPE 未记录" if result.get("rpe_0_10") is None else f"RPE {result.get('rpe_0_10'):g}"
        import_status = next(
            (
                item["status"]
                for item in compatibility.get("items", [])
                if item.get("component_id") == result.get("component_id")
            ),
            "not_measured",
        )
        html.append(
            (
                f'<div class="rx-draft-component {class_name}">'
                f'<div class="rx-draft-label">{escape(zh(result.get("area", "")))}</div>'
                f'<div class="rx-draft-value">{escape(result.get("test", result.get("component_id", "component")))}</div>'
                f'<div class="rx-draft-detail">{escape(zh(value))}<br>{escape(rpe)}<br>{escape(zh(import_status))}</div>'
                "</div>"
            )
        )
    html.append("</div>")
    if quality.get("issues") or quality.get("warnings"):
        html.append('<div class="rx-draft-detail" style="margin-top: 12px;">')
        for item in quality.get("issues", []):
            html.append(f'<strong>Issue:</strong> {escape(zh(item))}<br>')
        for item in quality.get("warnings", []):
            html.append(f'<strong>Warning:</strong> {escape(zh(item))}<br>')
        html.append("</div>")
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _profile_list_html(items: list[str], empty: str, *, waiting: bool = False, limit: int = 4) -> str:
    class_name = "rx-profile-list-item rx-profile-list-item-waiting" if waiting else "rx-profile-list-item"
    visible = items[:limit] if items else [empty]
    html = ['<div class="rx-profile-list">']
    for item in visible:
        html.append(f'<div class="{class_name}">{escape(zh(item))}</div>')
    if len(items) > limit:
        html.append(f'<div class="{class_name}">还有 {len(items) - limit} 条在详细报告中</div>')
    html.append("</div>")
    return "".join(html)


def _profile_basis_text(row: dict) -> str:
    if row.get("evidence"):
        return "；".join(zh(item) for item in row["evidence"][:2])
    if row.get("missing"):
        return "缺少：" + "；".join(zh(item) for item in row["missing"][:2])
    return "暂无可展示依据"


def _training_profile_handoff_board(report: dict) -> None:
    safety_status = report["safety_gate"]["status"]
    measured = report["measurement"]["measured_performance_areas"]
    measured_count = int(measured.get("count", 0) or 0)
    benchmark_count = int(report["measurement"]["benchmark_sessions"].get("session_count", 0) or 0)
    starter_available = bool(report["starter_path_status"]["available"])
    comparison_ready = measured_count >= 2
    safety_blocked = safety_status == "RED"
    status_class = "rx-profile-decision-status"
    if safety_blocked:
        status_class += " rx-profile-decision-status-blocked"
    elif not starter_available:
        status_class += " rx-profile-decision-status-waiting"
    handoff_label = "Training handoff blocked" if safety_blocked else "Starter Path available" if starter_available else "Benchmark first"
    cards = [
        (
            "Safety Gate",
            safety_status,
            "Safety 只决定能否继续训练交接，不会抬高或压低表现结果。",
            "rx-profile-decision-card-blocked" if safety_blocked else "rx-profile-decision-card-ready",
        ),
        (
            "Measured Coverage",
            measured.get("label", f"{measured_count} measured areas"),
            f"当前有 {benchmark_count} 次 Benchmark Log；缺失测试继续显示 Not tested。",
            "rx-profile-decision-card-ready" if comparison_ready else "rx-profile-decision-card-waiting",
        ),
        (
            "Compare Areas",
            "可以比较" if comparison_ready else "暂不比较",
            "至少两个实测表现维度后，才显示 strongest area 和 main gap。",
            "rx-profile-decision-card-ready" if comparison_ready else "rx-profile-decision-card-waiting",
        ),
        (
            "Starter Path",
            "Available" if starter_available else "Gated",
            zh(report["starter_path_status"].get("based_on_gap") or report["starter_path_status"].get("reason") or "Measurement gate"),
            "rx-profile-decision-card-ready" if starter_available else "rx-profile-decision-card-waiting",
        ),
    ]
    html = [
        '<div class="rx-profile-decision">',
        '<div class="rx-profile-decision-head">',
        "<div>",
        '<div class="rx-profile-decision-kicker">Measurement handoff</div>',
        '<div class="rx-profile-decision-title">这份 Training Profile 目前能交接到哪里？</div>',
        '<div class="rx-profile-decision-copy">SportRx 先交代测量证据，再决定是否进入 Starter Path。这里不展示内部 0-100 aggregate，不用缺失项目补平均值，也不把 Safety Gate 混进表现评分。</div>',
        "</div>",
        f'<div class="{status_class}">',
        '<div class="rx-profile-decision-label">Current handoff state</div>',
        f'<div class="rx-profile-decision-value">{escape(zh(handoff_label))}</div>',
        f'<div class="rx-profile-decision-detail">{escape(zh(report["next_action"]))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-profile-decision-grid">',
    ]
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-profile-decision-card {class_name}">'
                f'<div class="rx-profile-decision-label">{escape(label)}</div>'
                f'<div class="rx-profile-decision-value">{escape(zh(value))}</div>'
                f'<div class="rx-profile-decision-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _profile_dimension_cards(report: dict) -> None:
    html = ['<div class="rx-profile-dimensions">']
    for row in report["performance_rows"]:
        source_id = row.get("source")
        measured = row.get("score") is not None and source_id not in {"reported_training", "missing"}
        reported_context = source_id == "reported_training"
        class_name = "rx-profile-dimension-measured" if measured else "rx-profile-dimension-missing"
        status_label = "Measured" if measured else "Reported context" if reported_context else "Not tested"
        value = zh(row.get("status", "Recorded")) if measured or reported_context else "Not tested"
        source = zh(row.get("source", "unknown source"))
        basis = _profile_basis_text(row)
        if reported_context:
            basis = f"{basis}；自报训练只作为训练背景，不算实测表现维度。"
        html.append(
            (
                f'<div class="rx-profile-dimension {class_name}">'
                f'<div class="rx-profile-dimension-label">{escape(status_label)}</div>'
                f'<div class="rx-profile-dimension-title">{escape(zh(row["label"]))}</div>'
                f'<div class="rx-profile-dimension-value">{escape(value)}</div>'
                f'<div class="rx-profile-dimension-detail">Source: {escape(source)}<br>{escape(basis)}</div>'
                "</div>"
            )
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _measured_profile_summary(report: dict) -> None:
    starter_available = bool(report["starter_path_status"]["available"])
    starter_reason = report["starter_path_status"].get("based_on_gap") or report["starter_path_status"].get("reason") or "Measurement gate"
    measured = report["measurement"]["measured_performance_areas"]
    benchmark = report["measurement"]["benchmark_sessions"]
    lab_quality = report["measurement"].get("lab_test_quality", {})
    panel_class = "rx-profile-panel-ready" if starter_available else "rx-profile-panel-waiting"
    html = [
        '<div class="rx-profile-summary">',
        f'<div class="rx-profile-panel {panel_class}">',
        '<div class="rx-profile-kicker">Current measured picture</div>',
        f'<div class="rx-profile-title">{escape(zh(report["current_measured_picture"]))}</div>',
        f'<div class="rx-profile-copy">Training Profile：{escape(zh(report["training_profile"]))}。这是当前测量摘要，不是 readiness score，也不是给运动员贴标签。</div>',
        '<div class="rx-profile-handoff">',
        '<div class="rx-profile-chip"><div class="rx-profile-chip-label">Measured areas</div>',
        f'<div class="rx-profile-chip-value">{escape(measured.get("label", str(measured.get("count", 0))))}</div></div>',
        '<div class="rx-profile-chip"><div class="rx-profile-chip-label">Benchmark logs</div>',
        f'<div class="rx-profile-chip-value">{escape(str(benchmark.get("session_count", 0)))} sessions</div></div>',
        '<div class="rx-profile-chip"><div class="rx-profile-chip-label">Lab quality</div>',
        f'<div class="rx-profile-chip-value">{escape(zh(lab_quality.get("status", "not_reviewed")))}</div></div>',
        '<div class="rx-profile-chip"><div class="rx-profile-chip-label">Handoff gate</div>',
        f'<div class="rx-profile-chip-value">{escape("可交接" if starter_available else "等待测量")}</div></div>',
        "</div>",
        f'<div class="rx-profile-copy">Starter Path 边界：{escape(zh(starter_reason))}</div>',
        "</div>",
        '<div class="rx-profile-panel">',
        '<div class="rx-profile-kicker">Known / unknown</div>',
        '<div class="rx-profile-title">哪些已经知道，哪些还不能说</div>',
        '<div class="rx-profile-copy">SportRx 会保留缺失测试，而不是用平均值或主观印象补齐。</div>',
        _profile_list_html(report["known"], "暂无已测信息"),
        '<div style="height: 9px"></div>',
        _profile_list_html(report["unknown"], "暂无主要未知项", waiting=True),
        "</div>",
        '<div class="rx-profile-panel">',
        '<div class="rx-profile-kicker">Performance focus</div>',
        '<div class="rx-profile-title">Strongest area / main gap</div>',
        f'<div class="rx-profile-copy">Strongest area: {escape(zh(report["strongest_area"]))}<br>Main gap: {escape(zh(report["main_gap"]))}</div>',
        _profile_list_html(report["priorities"], "暂无优先事项", waiting=not starter_available),
        "</div>",
        '<div class="rx-profile-panel">',
        '<div class="rx-profile-kicker">Measure next</div>',
        '<div class="rx-profile-title">下一步先补测什么</div>',
        f'<div class="rx-profile-copy">{escape(zh(report["next_action"]))}</div>',
        _profile_list_html(report["measure_next"], "按同一 protocol 完成复测", waiting=True),
        "</div>",
        "</div>",
    ]
    st.markdown("".join(html), unsafe_allow_html=True)


def _release_candidate_console(qa: dict, launch: dict, runtime: dict, package_manifest: dict, runbook: dict, evidence_status: dict) -> None:
    evidence_ready = bool(evidence_status) and all(evidence_status.values())
    review_pack_check = next((item for item in qa["checks"] if item["id"] == "qa_review_pack_zip"), {})
    qa_ready = qa["status"] == "ready_for_demo_review"
    launch_ready = launch["status"] == "ready_for_public_demo"
    runtime_ready = runtime["status"] == "ready_to_run_locally"
    package_ready = package_manifest["status"] == "ready_for_public_package"
    runbook_ready = runbook["status"] == "ready"
    cards = [
        (
            "Release QA",
            qa["status"],
            f"{qa['passed_checks']} / {qa['total_checks']} checks.",
            "rx-release-card-ready" if qa_ready else "rx-release-card-waiting",
        ),
        (
            "Launch",
            launch["status"],
            f"{launch['passed_checks']} / {launch['total_checks']} checks.",
            "rx-release-card-ready" if launch_ready else "rx-release-card-waiting",
        ),
        (
            "Runtime",
            runtime["status"],
            "Smoke, tests, and local run commands are listed below.",
            "rx-release-card-ready" if runtime_ready else "rx-release-card-blocked",
        ),
        (
            "Public Package",
            package_manifest["status"],
            f"{package_manifest['included_file_count']} public files; internal docs excluded.",
            "rx-release-card-ready" if package_ready else "rx-release-card-waiting",
        ),
        (
            "Review Pack",
            review_pack_check.get("status", "needs_review"),
            review_pack_check.get("detail", "Review Pack ZIP has not been checked."),
            "rx-release-card-ready" if review_pack_check.get("passed") else "rx-release-card-waiting",
        ),
        (
            "Evidence Files",
            f"{sum(evidence_status.values())} / {len(evidence_status)}",
            "Required evidence context is present." if evidence_ready else "Evidence context is incomplete.",
            "rx-release-card-ready" if evidence_ready else "rx-release-card-waiting",
        ),
    ]
    overall_ready = all([qa_ready, launch_ready, runtime_ready, package_ready, runbook_ready, evidence_ready])
    html = [
        '<div class="rx-release-console">',
        '<div class="rx-release-head">',
        '<div>',
        '<div class="rx-release-kicker">Release candidate console</div>',
        '<div class="rx-release-title">SportRx 发布前状态</div>',
        f'<div class="rx-release-copy">{escape(qa["claim_boundary"])}</div>',
        "</div>",
        '<div class="rx-release-status">',
        '<div class="rx-release-label">Overall</div>',
        f'<div class="rx-release-value">{escape("Ready for review" if overall_ready else "Needs review")}</div>',
        f'<div class="rx-release-detail">{escape(runbook.get("claim_boundary", "Product-readiness only."))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-release-grid">',
    ]
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-release-card {class_name}">'
                f'<div class="rx-release-label">{escape(label)}</div>'
                f'<div class="rx-release-value">{escape(zh(value))}</div>'
                f'<div class="rx-release-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _release_reviewer_brief(release_candidate: dict, public_beta: dict, validation_matrix: dict) -> None:
    beta_ready = public_beta["status"] == "public_beta_candidate"
    limited_ready = release_candidate["status"] == "limited_review_candidate"
    launch_label = "Public beta candidate" if beta_ready else "Limited reviewer handoff" if limited_ready else "Needs release work"
    open_first = release_candidate.get("open_first", [])[:3]
    run_commands = release_candidate.get("run_commands", [])[:2]
    cards = [
        (
            "Release Candidate",
            release_candidate["status"],
            f"{release_candidate['passed_checks']} / {release_candidate['total_checks']} product gates passed.",
            "rx-release-card-ready" if limited_ready or beta_ready else "rx-release-card-waiting",
        ),
        (
            "Public Beta Gate",
            public_beta["status"],
            public_beta["next_action"],
            "rx-release-card-ready" if beta_ready else "rx-release-card-waiting",
        ),
        (
            "Validation Claim",
            validation_matrix["current_validation_claim"],
            validation_matrix["claim_boundary"],
            "rx-release-card-waiting",
        ),
        (
            "Open First",
            " / ".join(open_first),
            "Reviewer should start from these artifacts before interpreting details.",
            "rx-release-card-ready" if open_first else "rx-release-card-waiting",
        ),
        (
            "Run Locally",
            "Ready" if run_commands else "Missing",
            "；".join(run_commands) if run_commands else "Run commands are not listed.",
            "rx-release-card-ready" if run_commands else "rx-release-card-waiting",
        ),
        (
            "Blocked Claims",
            str(len(release_candidate.get("blocked_claims", []))),
            "Validated score, medical clearance, injury-risk percentage, finish prediction, percentiles and guaranteed outcomes remain blocked.",
            "rx-release-card-ready",
        ),
    ]
    html = [
        '<div class="rx-release-console">',
        '<div class="rx-release-head">',
        '<div>',
        '<div class="rx-release-kicker">Reviewer launch brief</div>',
        '<div class="rx-release-title">外部 reviewer 现在该怎么看 SportRx？</div>',
        f'<div class="rx-release-copy">{escape(release_candidate["claim_boundary"])}</div>',
        "</div>",
        '<div class="rx-release-status">',
        '<div class="rx-release-label">Launch posture</div>',
        f'<div class="rx-release-value">{escape(launch_label)}</div>',
        f'<div class="rx-release-detail">{escape(zh(release_candidate["next_action"]))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-release-grid">',
    ]
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-release-card {class_name}">'
                f'<div class="rx-release-label">{escape(label)}</div>'
                f'<div class="rx-release-value">{escape(zh(value))}</div>'
                f'<div class="rx-release-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _public_beta_console(readiness: dict) -> None:
    html = [
        '<div class="rx-beta-console">',
        '<div class="rx-beta-head">',
        '<div>',
        '<div class="rx-beta-kicker">Public Beta gate</div>',
        '<div class="rx-beta-title">能不能给外部 reviewer 试用</div>',
        f'<div class="rx-beta-copy">{escape(readiness["claim_boundary"])}</div>',
        "</div>",
        '<div class="rx-beta-status">',
        '<div class="rx-beta-label">Next Action</div>',
        f'<div class="rx-beta-value">{escape(zh(readiness["status"]))}</div>',
        f'<div class="rx-beta-detail">{escape(zh(readiness["next_action"]))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-beta-grid">',
    ]
    for card in readiness["cards"]:
        class_status = "ready" if card["status"] == "ready" else "waiting"
        html.append(
            (
                f'<div class="rx-beta-card rx-beta-card-{class_status}">'
                f'<div class="rx-beta-label">{escape(zh(card["label"]))}</div>'
                f'<div class="rx-beta-value">{escape(zh(card["value"]))}</div>'
                f'<div class="rx-beta-detail">{escape(zh(card["detail"]))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _evidence_coverage_console(coverage: dict) -> None:
    ready = coverage["status"] == "ready_for_release_review"
    cards = [
        (
            "Evidence Files",
            f"{coverage['required_files_present']} / {coverage['required_file_count']}",
            "Required local evidence files for release review.",
            "rx-release-card-ready" if ready else "rx-release-card-waiting",
        ),
        (
            "Rules Mapped",
            str(coverage["rule_count"]),
            "Rows parsed from rule_evidence_map.md.",
            "rx-release-card-ready" if coverage["rule_count"] else "rx-release-card-waiting",
        ),
        (
            "Explain Only",
            str(coverage["status_counts"].get("explain_only", 0)),
            "Can be shown only with caveats.",
            "rx-release-card-waiting" if coverage["status_counts"].get("explain_only", 0) else "rx-release-card-ready",
        ),
        (
            "Blocked",
            str(coverage["status_counts"].get("blocked", 0)),
            "Must not enter normal UX until validation changes.",
            "rx-release-card-waiting" if coverage["status_counts"].get("blocked", 0) else "rx-release-card-ready",
        ),
        (
            "Sources",
            str(coverage["source_count"]),
            "Distinct source IDs referenced by current rules.",
            "rx-release-card-ready" if coverage["source_count"] else "rx-release-card-waiting",
        ),
        (
            "Forbidden Claims",
            str(len(coverage["forbidden_claims_present"])),
            "Claim policy explicitly blocks overreach.",
            "rx-release-card-ready",
        ),
    ]
    html = [
        '<div class="rx-release-console">',
        '<div class="rx-release-head">',
        '<div>',
        '<div class="rx-release-kicker">Evidence coverage</div>',
        '<div class="rx-release-title">循证覆盖与声明边界</div>',
        f'<div class="rx-release-copy">{escape(coverage["primary_message"])}</div>',
        "</div>",
        '<div class="rx-release-status">',
        '<div class="rx-release-label">Status</div>',
        f'<div class="rx-release-value">{escape(zh(coverage["status"]))}</div>',
        f'<div class="rx-release-detail">{escape(coverage["claim_boundary"])}</div>',
        "</div>",
        "</div>",
        '<div class="rx-release-grid">',
    ]
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-release-card {class_name}">'
                f'<div class="rx-release-label">{escape(label)}</div>'
                f'<div class="rx-release-value">{escape(value)}</div>'
                f'<div class="rx-release-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _evidence_library_console(library: dict) -> None:
    ready = library["status"] == "ready_for_review"
    tier_summary = ", ".join(f"{tier}: {count}" for tier, count in sorted(library["tier_counts"].items())) or "none"
    quality = library.get("quality_summary", {})
    cards = [
        (
            "Sources",
            str(library["source_count"]),
            f"{library['topic_count']} evidence topics.",
            "rx-evidence-card-ready" if library["source_count"] else "rx-evidence-card-waiting",
        ),
        (
            "Required Files",
            f"{library['required_files_present']} / {library['required_file_count']}",
            "Local evidence library files are present.",
            "rx-evidence-card-ready" if ready else "rx-evidence-card-waiting",
        ),
        (
            "Appraised",
            f"{quality.get('appraised_sources', 0)} / {library['source_count']}",
            "Sources with an evidence tier in literature_matrix.md.",
            "rx-evidence-card-ready" if not quality.get("not_appraised_sources", 0) else "rx-evidence-card-waiting",
        ),
        (
            "Tier Mix",
            str(len(library["tier_counts"])),
            tier_summary,
            "rx-evidence-card-ready" if library["tier_counts"] else "rx-evidence-card-waiting",
        ),
        (
            "Measurement Layer",
            str(quality.get("measurement_sources", 0)),
            "Sources about field testing, RPE, monitoring, and repeatability.",
            "rx-evidence-card-ready" if quality.get("measurement_sources", 0) else "rx-evidence-card-waiting",
        ),
    ]
    html = [
        '<div class="rx-evidence-console">',
        '<div class="rx-evidence-head">',
        '<div>',
        '<div class="rx-evidence-kicker">Evidence library</div>',
        '<div class="rx-evidence-title">SportRx 循证资料库</div>',
        '<div class="rx-evidence-copy">这里展示本地保存的 source index、evidence tier、产品用途和限制。它不是系统综述、RAG、自动引用生成器，也不证明 SportRx 已经验证。</div>',
        "</div>",
        f'<div class="rx-evidence-status{" rx-evidence-status-waiting" if not ready else ""}">',
        '<div class="rx-evidence-label">Status</div>',
        f'<div class="rx-evidence-value">{escape(zh(library["status"]))}</div>',
        f'<div class="rx-evidence-detail">{escape(library["claim_boundary"])}</div>',
        "</div>",
        "</div>",
        '<div class="rx-evidence-grid">',
    ]
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-evidence-card {class_name}">'
                f'<div class="rx-evidence-label">{escape(label)}</div>'
                f'<div class="rx-evidence-value">{escape(value)}</div>'
                f'<div class="rx-evidence-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _evidence_topic_cards(library: dict) -> None:
    html = ['<div class="rx-evidence-topic-grid">']
    for topic in library.get("topic_cards", []):
        tier_summary = ", ".join(f"{tier}: {count}" for tier, count in topic.get("tier_counts", {}).items()) or "not appraised"
        class_name = "rx-evidence-topic-waiting" if topic.get("needs_appraisal") else "rx-evidence-topic-ready"
        html.append(
            (
                f'<div class="rx-evidence-topic {class_name}">'
                f'<div class="rx-evidence-label">Tier {escape(str(topic.get("strongest_tier", "n/a")))}</div>'
                f'<div class="rx-evidence-value">{escape(zh(topic["topic"]))}</div>'
                f'<div class="rx-evidence-detail">{escape(str(topic["source_count"]))} sources · {escape(tier_summary)}<br>'
                f'IDs: {escape(", ".join(topic["source_ids"][:4]))}</div>'
                f'<div class="rx-evidence-source-limits">{escape(zh(topic.get("example_limit", "No limits recorded.")))}</div>'
                "</div>"
            )
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _evidence_source_cards(sources: list[dict], *, limit: int = 9) -> None:
    html = ['<div class="rx-evidence-source-grid">']
    visible = sources[:limit]
    for source in visible:
        appraised = source["evidence_tier"] != "not_appraised"
        class_name = "rx-evidence-source-ready" if appraised else "rx-evidence-source-waiting"
        html.append(
            (
                f'<div class="rx-evidence-source {class_name}">'
                f'<div class="rx-evidence-label">Tier {escape(source["evidence_tier"])}</div>'
                f'<div class="rx-evidence-value">{escape(source["id"])}</div>'
                f'<div class="rx-evidence-detail">{escape(zh(source["product_use"]))}<br>{escape(source["saved_in"])}</div>'
                f'<div class="rx-evidence-source-limits">{escape(zh(source["limits"]))}</div>'
                "</div>"
            )
        )
    if len(sources) > limit:
        html.append(
            (
                '<div class="rx-evidence-source rx-evidence-source-waiting">'
                '<div class="rx-evidence-label">More sources</div>'
                f'<div class="rx-evidence-value">+{len(sources) - limit}</div>'
                '<div class="rx-evidence-detail">完整列表在下方 Source Index 表格和导出的 Markdown 中。</div>'
                "</div>"
            )
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _evidence_claim_boundary_board(validation_matrix: dict, coverage: dict) -> None:
    cards = [
        (
            "Allowed Claim",
            validation_matrix["current_validation_claim"],
            "当前只允许说产品原型和流程证据，不说正式验证。",
            "rx-evidence-claim-ready",
        ),
        (
            "Blocked Claims",
            str(len(validation_matrix["blocked_claims"])),
            "这些声明必须等真实试用、复测和验证数据后再开放。",
            "rx-evidence-claim-waiting" if validation_matrix["blocked_claims"] else "rx-evidence-claim-ready",
        ),
        (
            "Mapped Rules",
            str(coverage["rule_count"]),
            "规则证据映射用于 release review，不是科学验证结果。",
            "rx-evidence-claim-ready" if coverage["rule_count"] else "rx-evidence-claim-waiting",
        ),
        (
            "Capture Ready",
            f"{validation_matrix.get('passed_checks', 0)} / {validation_matrix.get('total_checks', 0)}",
            "用于判断下一阶段能不能收集真实使用数据。",
            "rx-evidence-claim-ready" if validation_matrix.get("capture_ready") else "rx-evidence-claim-waiting",
        ),
        (
            "Forbidden Claims",
            str(len(coverage["forbidden_claims_present"])),
            "医学清除、伤病风险百分比、完赛概率和 fake percentile 都被显式阻断。",
            "rx-evidence-claim-ready",
        ),
        (
            "Validation Status",
            validation_matrix["status"],
            "验证状态和发布状态分开；现在仍是 pre-validation。",
            "rx-evidence-claim-waiting",
        ),
    ]
    html = ['<div class="rx-evidence-claim-grid">']
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-evidence-claim {class_name}">'
                f'<div class="rx-evidence-label">{escape(label)}</div>'
                f'<div class="rx-evidence-value">{escape(zh(value))}</div>'
                f'<div class="rx-evidence-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _validation_readiness_console(matrix: dict) -> None:
    summary = matrix["summary"]
    cards = [
        (
            "Current Claim",
            matrix["current_validation_claim"],
            "This is the only validation claim allowed now.",
            "rx-release-card-ready",
        ),
        (
            "Capture Checks",
            f"{matrix['passed_checks']} / {matrix['total_checks']}",
            "Data-capture gates required before self-use validation.",
            "rx-release-card-ready" if matrix["capture_ready"] else "rx-release-card-waiting",
        ),
        (
            "Retest Data",
            str(summary["retest_comparisons"]),
            "Comparable raw retest items available in the current local session.",
            "rx-release-card-ready" if summary["retest_comparisons"] else "rx-release-card-waiting",
        ),
        (
            "Pilot Feedback",
            str(summary["pilot_feedback_entries"]),
            "Product feedback entries are not validation data.",
            "rx-release-card-waiting",
        ),
    ]
    html = [
        '<div class="rx-release-console">',
        '<div class="rx-release-head">',
        '<div>',
        '<div class="rx-release-kicker">Validation readiness</div>',
        '<div class="rx-release-title">验证状态与下一步数据采集</div>',
        f'<div class="rx-release-copy">{escape(matrix["claim_boundary"])}</div>',
        "</div>",
        '<div class="rx-release-status">',
        '<div class="rx-release-label">Status</div>',
        f'<div class="rx-release-value">{escape(zh(matrix["status"]))}</div>',
        f'<div class="rx-release-detail">{escape(zh(matrix["next_action"]))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-release-grid">',
    ]
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-release-card {class_name}">'
                f'<div class="rx-release-label">{escape(label)}</div>'
                f'<div class="rx-release-value">{escape(zh(value))}</div>'
                f'<div class="rx-release-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _self_use_protocol_console(protocol: dict) -> None:
    cards = [
        (
            "Duration",
            f"{protocol['duration_weeks']} weeks",
            "Baseline, weekly feedback, and Week 4 retest.",
            "rx-release-card-ready",
        ),
        (
            "Participant",
            protocol["participant_scope"],
            "Phase 0 uses builder-owned data only.",
            "rx-release-card-waiting",
        ),
        (
            "Data Fields",
            str(len(protocol["minimum_data_fields"])),
            "Minimum fields required before self-use can be interpreted.",
            "rx-release-card-ready",
        ),
        (
            "Blocked Claims",
            str(len(protocol["blocked_claims"])),
            "Claims that remain blocked after this protocol unless real validation follows.",
            "rx-release-card-waiting",
        ),
    ]
    html = [
        '<div class="rx-release-console">',
        '<div class="rx-release-head">',
        '<div>',
        '<div class="rx-release-kicker">Phase 0 protocol</div>',
        '<div class="rx-release-title">自用测试流程，不是验证结论</div>',
        f'<div class="rx-release-copy">{escape(protocol["claim_boundary"])}</div>',
        "</div>",
        '<div class="rx-release-status">',
        '<div class="rx-release-label">Status</div>',
        f'<div class="rx-release-value">{escape(zh(protocol["status"]))}</div>',
        f'<div class="rx-release-detail">{escape(zh(protocol["next_action"]))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-release-grid">',
    ]
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-release-card {class_name}">'
                f'<div class="rx-release-label">{escape(label)}</div>'
                f'<div class="rx-release-value">{escape(zh(value))}</div>'
                f'<div class="rx-release-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _export_center_console(
    bundle: dict,
    catalog: dict,
    integrity: dict,
    benchmark_sessions: list[dict],
    feedback_by_week: dict,
    pilot_feedback_entries: list[dict],
) -> None:
    file_ids = {item["id"] for item in bundle["files"]}
    artifact_count = int(bundle.get("manifest", {}).get("artifact_count", len(bundle["files"])))
    review_pack_ready = bool(bundle["files"]) and "manifest_json" in file_ids
    handoff_ready = "reviewer_handoff_markdown" in file_ids
    snapshot_ready = {"session_snapshot_json", "session_snapshot_markdown"}.issubset(file_ids)
    raw_data_ready = {"benchmark_log_json", "benchmark_log_csv"}.issubset(file_ids)
    catalog_ready = bool(catalog.get("categories"))
    schema_ready = "measurement_schema_registry_markdown" in file_ids
    command_board_ready = "test_day_command_board_markdown" in file_ids
    feedback_ready = "pilot_feedback_markdown" in file_ids and "pilot_feedback_json" in file_ids
    integrity_ready = integrity.get("status") == "ready_for_review_handoff"
    ready_count = sum(
        [
            review_pack_ready,
            integrity_ready,
            catalog_ready,
            schema_ready,
            command_board_ready,
            handoff_ready,
            snapshot_ready,
            raw_data_ready,
            feedback_ready,
        ]
    )
    cards = [
        (
            "Review Pack",
            f"{artifact_count} files",
            "ZIP includes local review artifacts plus manifest.",
            "rx-export-card-ready" if review_pack_ready else "rx-export-card-waiting",
        ),
        (
            "Integrity",
            f"{integrity.get('passed_checks', 0)} / {integrity.get('total_checks', 0)}",
            f"{integrity.get('payload_file_count', 0)} payload files have SHA-256 checksums.",
            "rx-export-card-ready" if integrity_ready else "rx-export-card-waiting",
        ),
        (
            "Artifact Catalog",
            f"{len(catalog.get('categories', []))} groups",
            "Shows what to open first and when each file is useful.",
            "rx-export-card-ready" if catalog_ready else "rx-export-card-waiting",
        ),
        (
            "Schema Registry",
            "Included" if schema_ready else "Missing",
            "Documents local data objects, required fields, and export coverage.",
            "rx-export-card-ready" if schema_ready else "rx-export-card-waiting",
        ),
        (
            "Test-Day Command Board",
            "Included" if command_board_ready else "Missing",
            "First-screen operator summary for preflight, component tests, raw recording, log handoff, and retest anchor.",
            "rx-export-card-ready" if command_board_ready else "rx-export-card-waiting",
        ),
        (
            "Reviewer Handoff",
            "Included" if handoff_ready else "Missing",
            "One-page guide for opening, demoing, and reviewing SportRx.",
            "rx-export-card-ready" if handoff_ready else "rx-export-card-waiting",
        ),
        (
            "Session Snapshot",
            "Restore-ready" if snapshot_ready else "Missing",
            "Captures local app state for reviewer handoff.",
            "rx-export-card-ready" if snapshot_ready else "rx-export-card-waiting",
        ),
        (
            "Benchmark Raw Data",
            f"{len(benchmark_sessions)} sessions",
            "JSON and CSV preserve raw results; missing tests stay Not tested.",
            "rx-export-card-ready" if raw_data_ready else "rx-export-card-waiting",
        ),
        (
            "Pilot Feedback",
            f"{len(pilot_feedback_entries)} entries",
            f"{len(feedback_by_week)} training feedback weeks saved locally.",
            "rx-export-card-ready" if feedback_ready else "rx-export-card-waiting",
        ),
    ]
    overall_ready = ready_count == len(cards)
    html = [
        '<div class="rx-export-console">',
        '<div class="rx-export-head">',
        '<div>',
        '<div class="rx-export-kicker">Handoff center</div>',
        '<div class="rx-export-title">SportRx 交付物状态</div>',
        f'<div class="rx-export-copy">{escape(bundle["claim_boundary"])}</div>',
        "</div>",
        '<div class="rx-export-status">',
        '<div class="rx-export-label">Overall</div>',
        f'<div class="rx-export-value">{escape("Ready for handoff" if overall_ready else "Needs review")}</div>',
        f'<div class="rx-export-detail">{ready_count} / {len(cards)} handoff groups ready.</div>',
        "</div>",
        "</div>",
        '<div class="rx-export-grid">',
    ]
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-export-card {class_name}">'
                f'<div class="rx-export-label">{escape(label)}</div>'
                f'<div class="rx-export-value">{escape(zh(value))}</div>'
                f'<div class="rx-export-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _export_release_package_board(
    bundle: dict,
    catalog: dict,
    review_pack_manifest: dict,
    review_pack_integrity: dict,
    package_manifest: dict,
    benchmark_sessions: list[dict],
    feedback_by_week: dict[int, dict],
    pilot_feedback_entries: list[dict],
) -> None:
    package_ready = package_manifest["status"] == "ready_for_public_package"
    integrity_ready = review_pack_integrity["status"] == "ready_for_review_handoff"
    evidence_exports = [
        item
        for item in bundle["files"]
        if "evidence" in item["id"] or "validation" in item["id"] or "self_use" in item["id"]
    ]
    local_data_count = len(benchmark_sessions) + len(feedback_by_week) + len(pilot_feedback_entries)
    gitignore_included = ".gitignore" in package_manifest.get("included_files", [])
    cache_check = next((item for item in package_manifest["checks"] if item["id"] == "pkg_cache_files"), {})
    cards = [
        (
            "Review Pack",
            f"{review_pack_manifest['archive_entry_count']} entries",
            f"{review_pack_integrity['passed_checks']} / {review_pack_integrity['total_checks']} integrity checks passed.",
            "rx-export-card-ready" if integrity_ready else "rx-export-card-waiting",
        ),
        (
            "Public Package",
            f"{package_manifest['included_file_count']} files",
            f"{package_manifest['passed_checks']} / {package_manifest['total_checks']} package checks passed.",
            "rx-export-card-ready" if package_ready else "rx-export-card-waiting",
        ),
        (
            "Repository Hygiene",
            ".gitignore included" if gitignore_included else ".gitignore missing",
            zh(cache_check.get("detail", "Cache exclusion not checked.")),
            "rx-export-card-ready" if gitignore_included and cache_check.get("passed") else "rx-export-card-waiting",
        ),
        (
            "Evidence Exports",
            str(len(evidence_exports)),
            "Evidence Library, Evidence Coverage, Validation Readiness and self-use protocol are exportable.",
            "rx-export-card-ready" if evidence_exports else "rx-export-card-waiting",
        ),
        (
            "Local Data",
            str(local_data_count),
            "Benchmark logs, weekly feedback and pilot feedback stay local and user-owned.",
            "rx-export-card-ready" if local_data_count else "rx-export-card-waiting",
        ),
        (
            "Artifact Catalog",
            f"{catalog['artifact_count']} files",
            "Artifacts are grouped by reviewer use case, not dumped as an unlabeled folder.",
            "rx-export-card-ready" if catalog["artifact_count"] else "rx-export-card-waiting",
        ),
    ]
    overall_ready = package_ready and integrity_ready and bool(evidence_exports) and gitignore_included
    html = [
        '<div class="rx-export-console">',
        '<div class="rx-export-head">',
        '<div>',
        '<div class="rx-export-kicker">Release package board</div>',
        '<div class="rx-export-title">发布交付台</div>',
        '<div class="rx-export-copy">这里把 reviewer 下载包、公开代码包、证据导出和本地数据边界放在同一处。它只检查交付完整性，不验证运动处方效果。</div>',
        "</div>",
        '<div class="rx-export-status">',
        '<div class="rx-export-label">Handoff state</div>',
        f'<div class="rx-export-value">{escape("Ready for reviewer handoff" if overall_ready else "Needs release review")}</div>',
        f'<div class="rx-export-detail">{escape(package_manifest["claim_boundary"])}</div>',
        "</div>",
        "</div>",
        '<div class="rx-export-grid">',
    ]
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-export-card {class_name}">'
                f'<div class="rx-export-label">{escape(label)}</div>'
                f'<div class="rx-export-value">{escape(zh(value))}</div>'
                f'<div class="rx-export-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _schema_registry_console(registry: dict) -> None:
    complete = registry["status"] == "complete"
    cards = [
        (
            "Data Objects",
            str(registry["object_count"]),
            f"{registry['owner_count']} owner modules.",
            "rx-export-card-ready",
        ),
        (
            "Export Coverage",
            f"{registry['exported_object_count']} / {registry['object_count']}",
            "Every listed data object points to a local export artifact.",
            "rx-export-card-ready" if complete else "rx-export-card-waiting",
        ),
        (
            "Missing Coverage",
            str(registry["missing_export_count"]),
            "Missing coverage means a data object is not represented in the current bundle.",
            "rx-export-card-ready" if complete else "rx-export-card-waiting",
        ),
        (
            "Claim Boundary",
            "Local contract",
            "Schema documentation is not measurement validation.",
            "rx-export-card-ready",
        ),
    ]
    html = [
        '<div class="rx-export-console">',
        '<div class="rx-export-head">',
        '<div>',
        '<div class="rx-export-kicker">Measurement schema registry</div>',
        '<div class="rx-export-title">本地数据对象契约</div>',
        f'<div class="rx-export-copy">{escape(registry["primary_message"])}</div>',
        "</div>",
        '<div class="rx-export-status">',
        '<div class="rx-export-label">Status</div>',
        f'<div class="rx-export-value">{escape(zh(registry["status"]))}</div>',
        f'<div class="rx-export-detail">{escape(registry["claim_boundary"])}</div>',
        "</div>",
        "</div>",
        '<div class="rx-export-grid">',
    ]
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-export-card {class_name}">'
                f'<div class="rx-export-label">{escape(label)}</div>'
                f'<div class="rx-export-value">{escape(zh(value))}</div>'
                f'<div class="rx-export-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _demo_scenario_matrix_console(matrix: dict) -> None:
    cards = [
        (
            "Scenarios",
            str(matrix["scenario_count"]),
            "Synthetic product-review states available.",
            "rx-release-card-ready",
        ),
        (
            "Complete Loop",
            str(matrix["complete_loop_count"]),
            "Full release demo scenario with feedback and retest.",
            "rx-release-card-ready" if matrix["complete_loop_count"] else "rx-release-card-waiting",
        ),
        (
            "Measurement Gated",
            str(matrix["measurement_gated_count"]),
            "Shows honest Not tested and blocked Starter Path states.",
            "rx-release-card-ready",
        ),
        (
            "First Pick",
            matrix["recommended_first_scenario"],
            "Recommended starting scenario for external reviewers.",
            "rx-release-card-ready",
        ),
    ]
    html = [
        '<div class="rx-release-console">',
        '<div class="rx-release-head">',
        '<div>',
        '<div class="rx-release-kicker">Demo scenario matrix</div>',
        '<div class="rx-release-title">试用场景怎么选</div>',
        f'<div class="rx-release-copy">{escape(matrix["primary_message"])}</div>',
        "</div>",
        '<div class="rx-release-status">',
        '<div class="rx-release-label">Status</div>',
        f'<div class="rx-release-value">{escape(zh(matrix["status"]))}</div>',
        f'<div class="rx-release-detail">{escape(matrix["claim_boundary"])}</div>',
        "</div>",
        "</div>",
        '<div class="rx-release-grid">',
    ]
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-release-card {class_name}">'
                f'<div class="rx-release-label">{escape(label)}</div>'
                f'<div class="rx-release-value">{escape(zh(value))}</div>'
                f'<div class="rx-release-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _reviewer_session_plan_console(plan: dict) -> None:
    cards = [
        (
            track["label"],
            f"{track['duration_min']} min",
            f"{track['scenario_id']} · {track['scenario_state']}",
            "rx-release-card-ready",
        )
        for track in plan["tracks"]
    ]
    html = [
        '<div class="rx-release-console">',
        '<div class="rx-release-head">',
        '<div>',
        '<div class="rx-release-kicker">Reviewer session plan</div>',
        '<div class="rx-release-title">给 reviewer 的试用路线</div>',
        f'<div class="rx-release-copy">{escape(plan["primary_message"])}</div>',
        "</div>",
        '<div class="rx-release-status">',
        '<div class="rx-release-label">Next track</div>',
        f'<div class="rx-release-value">{escape(zh(plan["next_track"]))}</div>',
        f'<div class="rx-release-detail">{escape(plan["claim_boundary"])}</div>',
        "</div>",
        "</div>",
        '<div class="rx-release-grid">',
    ]
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-release-card {class_name}">'
                f'<div class="rx-release-label">{escape(label)}</div>'
                f'<div class="rx-release-value">{escape(value)}</div>'
                f'<div class="rx-release-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _quick_match_input_console(input_review: dict) -> None:
    missing = input_review.get("missing_fields", [])
    cards = [
        (
            "Behavior Inputs",
            f"{input_review['behavior_fields_collected']} / {input_review['behavior_fields_total']}",
            "训练天数、训练量、跑走、力量、高强度和负重动作暴露。",
        ),
        (
            "Context Inputs",
            f"{input_review['context_fields_collected']} / {input_review['context_fields_total']}",
            "年龄、目标和可用时间只约束路线与处方，不冒充表现测试。",
        ),
        (
            "Missing",
            "None" if not missing else str(len(missing)),
            "缺失字段不会被平均值或中点分数替代。",
        ),
        (
            "Measurement Status",
            "Self-reported",
            "Quick Match 是粗筛；真正表现判断进入 Benchmark Log。",
        ),
    ]
    html = [
        '<div class="rx-qm-input-console">',
        '<div class="rx-qm-input-head">',
        '<div>',
        '<div class="rx-qm-input-kicker">Input review</div>',
        '<div class="rx-qm-input-title">这些输入会影响什么？</div>',
        f'<div class="rx-qm-input-copy">{escape(input_review["claim_boundary"])}</div>',
        "</div>",
        '<div class="rx-qm-input-status">',
        '<div class="rx-qm-input-label">Quality Status</div>',
        f'<div class="rx-qm-input-value">{escape(zh(input_review["quality_status"]))}</div>',
        '<div class="rx-qm-input-detail">够做产品路线粗筛，不够做 validated performance conclusion。</div>',
        "</div>",
        "</div>",
        '<div class="rx-qm-input-grid">',
    ]
    for label, value, detail in cards:
        html.append(
            (
                '<div class="rx-qm-input-card">'
                f'<div class="rx-qm-input-label">{escape(label)}</div>'
                f'<div class="rx-qm-input-value">{escape(zh(value))}</div>'
                f'<div class="rx-qm-input-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _quick_match_contract_console(contract: dict) -> None:
    html = [
        '<div class="rx-contract-console">',
        '<div class="rx-contract-head">',
        '<div>',
        '<div class="rx-contract-kicker">Quick Match intake contract</div>',
        '<div class="rx-contract-title">这些问题为什么存在</div>',
        f'<div class="rx-contract-copy">{escape(zh(contract["primary_message"]))}</div>',
        "</div>",
        '<div class="rx-contract-status">',
        '<div class="rx-contract-label">Status</div>',
        f'<div class="rx-contract-value">{escape(zh(contract["status"]))}</div>',
        f'<div class="rx-contract-detail">{escape(zh(contract["next_action"]))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-contract-grid">',
    ]
    for group in contract["groups"]:
        class_name = "rx-contract-card-ready" if group["status"] == "ready" else "rx-contract-card-waiting"
        html.append(
            (
                f'<div class="rx-contract-card {class_name}">'
                f'<div class="rx-contract-label">{escape(group["label"])}</div>'
                f'<div class="rx-contract-value">{escape(str(group["collected"]))} / {escape(str(group["total"]))}</div>'
                f'<div class="rx-contract-detail">{escape(zh(group["purpose"]))}<br>{escape(zh(group["expected_output"]))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)
    st.caption(zh(contract["excluded_measurement_policy"]))


def _quick_match_lab_intake_sheet_console(sheet: dict) -> None:
    html = [
        '<div class="rx-quality-console">',
        '<div class="rx-quality-head">',
        '<div>',
        '<div class="rx-quality-kicker">Quick Match Lab Intake Sheet</div>',
        '<div class="rx-quality-title">先记录可量化输入，再决定要不要进入 Benchmark</div>',
        f'<div class="rx-quality-copy">{escape(zh(sheet["primary_message"]))}</div>',
        "</div>",
        '<div class="rx-quality-status">',
        '<div class="rx-quality-label">Next Action</div>',
        f'<div class="rx-quality-value">{escape(zh(sheet["status"]))}</div>',
        f'<div class="rx-quality-detail">{escape(zh(sheet["next_action"]))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-quality-grid">',
    ]
    for card in sheet["cards"]:
        status = card.get("status", "waiting")
        class_name = "rx-quality-card-ready" if status == "ready" else "rx-quality-card-waiting"
        html.append(
            (
                f'<div class="rx-quality-card {class_name}">'
                f'<div class="rx-quality-label">{escape(zh(card["label"]))}</div>'
                f'<div class="rx-quality-value">{escape(zh(card["value"]))}</div>'
                f'<div class="rx-quality-detail">{escape(zh(card["detail"]))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)
    st.caption(zh(sheet["not_tested_policy"]))


def _quick_match_lab_intake_rows(sheet: dict) -> list[dict]:
    rows = []
    for section in sheet["sections"]:
        for field in section["fields"]:
            rows.append(
                {
                    "Section": zh(section["label"]),
                    "Field": zh(field["label"]),
                    "Value": zh(field["value"]),
                    "Unit": zh(field["unit"]),
                    "Source": zh(field["source_type"]),
                    "Output role": zh(field["output_role"]),
                    "Boundary": zh(field["boundary"]),
                }
            )
    return rows


def _intake_precision_console(audit: dict) -> None:
    summary = audit["summary"]
    cards = [
        (
            "Direct Numeric",
            f"{summary['direct_numeric_collected']} / {summary['direct_numeric_fields']}",
            "年龄、训练天数、分钟数和次数都是直接数字，不再用模糊等级。",
        ),
        (
            "Measured Tests",
            f"{summary['measured_tests_recorded']} / {summary['measured_test_fields']}",
            "只有真正测试过的项目才进入 measured performance。",
        ),
        (
            "Not Tested",
            str(summary["not_tested"]),
            "缺失测试保持 Not tested，不用平均值补齐。",
        ),
        (
            "Legacy / Unsupported",
            str(summary["ignored_or_legacy_fields"]),
            "旧版 alias、主观旧字段和 unsupported 字段都不会伪装成测量结果。",
        ),
    ]
    html = [
        '<div class="rx-qm-input-console">',
        '<div class="rx-qm-input-head">',
        '<div>',
        '<div class="rx-qm-input-kicker">Intake precision audit</div>',
        '<div class="rx-qm-input-title">这些问题是否真的可量化？</div>',
        f'<div class="rx-qm-input-copy">{escape(audit["claim_boundary"])}</div>',
        "</div>",
        '<div class="rx-qm-input-status">',
        '<div class="rx-qm-input-label">Next Action</div>',
        f'<div class="rx-qm-input-value">{escape(zh(audit["status"]))}</div>',
        f'<div class="rx-qm-input-detail">{escape(zh(audit["next_action"]))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-qm-input-grid">',
    ]
    for label, value, detail in cards:
        html.append(
            (
                '<div class="rx-qm-input-card">'
                f'<div class="rx-qm-input-label">{escape(label)}</div>'
                f'<div class="rx-qm-input-value">{escape(zh(value))}</div>'
                f'<div class="rx-qm-input-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _intake_precision_rows(audit: dict) -> list[dict]:
    return [
        {
            "字段": zh(row["label"]),
            "当前值": zh(row["value"]),
            "类型": zh(row["precision_class"]),
            "状态": zh(row["status"]),
            "是否影响输出": "是" if row["affects_output"] else "否",
            "用途": ", ".join(row["used_by"]) if row["used_by"] else "Not used",
            "边界": zh(row["user_boundary"]),
        }
        for row in audit["rows"]
    ]


def _quick_match_intake_console(intake_quality: dict) -> None:
    html = [
        '<div class="rx-quality-console">',
        '<div class="rx-quality-head">',
        '<div>',
        '<div class="rx-quality-kicker">Intake quality</div>',
        '<div class="rx-quality-title">这份 Quick Match 记录够不够用？</div>',
        f'<div class="rx-quality-copy">{escape(intake_quality["claim_boundary"])}</div>',
        "</div>",
        '<div class="rx-quality-status">',
        '<div class="rx-quality-label">Next Action</div>',
        f'<div class="rx-quality-value">{escape(zh(intake_quality["status"]))}</div>',
        f'<div class="rx-quality-detail">{escape(zh(intake_quality["next_action"]))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-quality-grid">',
    ]
    for card in intake_quality["cards"]:
        status = card.get("status", "waiting")
        if status == "blocked":
            class_name = "rx-quality-card-blocked"
        elif status == "ready":
            class_name = "rx-quality-card-ready"
        else:
            class_name = "rx-quality-card-waiting"
        html.append(
            (
                f'<div class="rx-quality-card {class_name}">'
                f'<div class="rx-quality-label">{escape(zh(card["label"]))}</div>'
                f'<div class="rx-quality-value">{escape(zh(card["value"]))}</div>'
                f'<div class="rx-quality-detail">{escape(zh(card["detail"]))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _quick_match_reason_label(value: str) -> str:
    text = str(value)
    if " training days/week reported" in text:
        return text.replace(" training days/week reported", " 天/周训练（自报）")
    if " total training min/week reported" in text:
        return text.replace(" total training min/week reported", " 分钟/周训练总量（自报）")
    if " running/walking min/week reported" in text:
        return text.replace(" running/walking min/week reported", " 分钟/周跑步/快走（自报）")
    if " min longest continuous run/walk reported" in text:
        return text.replace(" min longest continuous run/walk reported", " 分钟最长连续跑/快走（自报）")
    if " strength days/week reported" in text:
        return text.replace(" strength days/week reported", " 天/周力量训练（自报）")
    if " high-intensity and " in text and " loaded sessions in last 4 weeks" in text:
        return (
            text.replace(" high-intensity and ", " 次高强度训练，")
            .replace(" loaded sessions in last 4 weeks", " 次负重动作训练（过去 4 周，自报）")
        )
    if text.startswith("Training days below "):
        return text.replace("Training days below ", "每周训练天数低于 ")
    if text.startswith("Weekly volume below about "):
        return text.replace("Weekly volume below about ", "每周训练总量低于约 ")
    return zh(text)


def _quick_match_match_cards(result: dict) -> None:
    safety_blocked = result.get("safety_gate", {}).get("auto_prescription") is False
    html = [
        '<div class="rx-qm-boundary">',
        "Quick Match 是 self-reported behavior routing。它不会使用 1 km / 5 km 成绩，不显示 0-100 分，也不会替代 HYROX Check 或 SportRx Hybrid Benchmark v1。",
        "</div>",
        '<div class="rx-qm-match-grid">',
    ]
    for item in result["top_matches"]:
        if safety_blocked:
            class_name = "rx-qm-match-card-blocked"
        elif item["pack_status"] == "enabled":
            class_name = "rx-qm-match-card-ready"
        else:
            class_name = "rx-qm-match-card-waiting"
        why = item["why_it_fits"] or ["还需要更多近期训练行为数据"]
        missing = item["what_is_missing"] or ["快速匹配没有发现明显缺口；下一步仍需实测。"]
        why_html = "".join(
            f'<div class="rx-qm-match-list-item">{escape(_quick_match_reason_label(reason))}</div>'
            for reason in why
        )
        missing_html = "".join(
            f'<div class="rx-qm-match-list-item rx-qm-match-list-item-missing">{escape(_quick_match_reason_label(reason))}</div>'
            for reason in missing
        )
        html.append(
            (
                f'<div class="rx-qm-match-card {class_name}">'
                '<div class="rx-qm-match-head">'
                "<div>"
                f'<div class="rx-qm-match-kicker">{escape(zh(item["pack_status"]))}</div>'
                f'<div class="rx-qm-match-title">{escape(zh(item["event_profile"]))}</div>'
                "</div>"
                '<div class="rx-qm-match-status">'
                '<div class="rx-qm-match-label">Current fit</div>'
                f'<div class="rx-qm-match-value">{escape(zh(item["fit_category"]))}</div>'
                "</div>"
                "</div>"
                '<div class="rx-qm-match-section">'
                '<div class="rx-qm-match-label">Why this route appears</div>'
                f'<div class="rx-qm-match-list">{why_html}</div>'
                "</div>"
                '<div class="rx-qm-match-section">'
                '<div class="rx-qm-match-label">What needs measurement</div>'
                f'<div class="rx-qm-match-list">{missing_html}</div>'
                "</div>"
                '<div class="rx-qm-match-section">'
                '<div class="rx-qm-match-label">Next route</div>'
                f'<div class="rx-qm-match-value">{escape(zh(item["cta"]))}</div>'
                "</div>"
                "</div>"
            )
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _command_center(command_center: dict) -> None:
    html = ['<div class="rx-command-grid">']
    for card in command_center["cards"]:
        status = str(card["status"])
        pill_class = "rx-pill-ready" if status == "ready" else "rx-pill-needs-review"
        html.append(
            (
                '<div class="rx-command-card">'
                '<div class="rx-command-top">'
                f'<div class="rx-command-label">{escape(str(card["label"]))}</div>'
                f'<div class="rx-pill {pill_class}">{escape(zh(status))}</div>'
                "</div>"
                f'<div class="rx-command-value">{escape(str(card["value"]))}</div>'
                f'<div class="rx-command-detail">{escape(str(card["detail"]))}</div>'
                "</div>"
            )
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _first_run_cards(guide: dict) -> None:
    html = ['<div class="rx-start-grid">']
    recommended = guide["recommended_path"]
    for path in guide["paths"]:
        active_class = " rx-start-card-active" if path["id"] == recommended else ""
        label = "Recommended" if path["id"] == recommended else f"{path['expected_time_min']} min"
        html.append(
            (
                f'<div class="rx-start-card{active_class}">'
                f'<div class="rx-start-label">{escape(str(label))}</div>'
                f'<div class="rx-start-title">{escape(path["label"])}</div>'
                f'<div class="rx-start-copy">{escape(path["best_for"])}</div>'
                f'<div class="rx-start-copy">{escape(path["primary_action"])}</div>'
                f'<div class="rx-start-foot">{escape(path["outcome"])}</div>'
                "</div>"
            )
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _workbench_launch_selector(guide: dict) -> None:
    html = [
        '<div class="rx-guided-console">',
        '<div class="rx-guided-head">',
        '<div>',
        '<div class="rx-guided-kicker">Launch selector</div>',
        '<div class="rx-guided-title">你现在想怎么试 SportRx？</div>',
        '<div class="rx-guided-copy">先选试用路线，再进入具体页面。这里只做导航和 demo state 切换，不生成分数，也不改变任何运动处方规则。</div>',
        "</div>",
        '<div class="rx-guided-meter">',
        '<div class="rx-guided-label">Recommended</div>',
        f'<div class="rx-guided-value">{escape(zh(guide["next_page"]))}</div>',
        f'<div class="rx-guided-detail">{escape(zh(guide["next_action"]))}</div>',
        "</div>",
        "</div>",
    ]
    st.markdown("".join(html), unsafe_allow_html=True)
    _first_run_cards(guide)

    columns = st.columns(len(guide["paths"]))
    for column, path in zip(columns, guide["paths"]):
        with column:
            if path["action_type"] == "load_demo":
                st.button(
                    path["button_label"],
                    width="stretch",
                    type="primary",
                    on_click=_load_demo_state,
                    key=f"launch_selector_{path['id']}",
                )
            else:
                st.button(
                    path["button_label"],
                    width="stretch",
                    on_click=_set_page,
                    args=(path["start_page"],),
                    key=f"launch_selector_{path['id']}",
                )


def _trial_mode_launcher(guide: dict) -> None:
    """Render first-use action buttons without changing product logic."""

    launch_ids = ["complete_demo", "quick_self_intake", "measure_first"]
    paths = [path for path in guide["paths"] if path["id"] in launch_ids]
    columns = st.columns(len(paths))
    for column, path in zip(columns, paths):
        with column:
            st.caption(f"{path['expected_time_min']} min · {path['start_page']}")
            st.write(f"**{path['label']}**")
            st.write(path["success_check"])
            if path["action_type"] == "load_demo":
                st.button(
                    path["button_label"],
                    width="stretch",
                    type="primary",
                    on_click=_load_demo_state,
                    key=f"trial_mode_{path['id']}",
                )
            else:
                st.button(
                    path["button_label"],
                    width="stretch",
                    on_click=_set_page,
                    args=(path["start_page"],),
                    key=f"trial_mode_{path['id']}",
                )


def _scenario_rows(scenarios: list[dict]) -> list[dict]:
    return [
        {
            "Scenario": item["label"],
            "Stage": item["stage"],
            "适合": item["best_for"],
            "预期状态": item["expected_state"],
        }
        for item in scenarios
    ]


def _scenario_cards(scenarios: list[dict]) -> None:
    html = ['<div class="rx-start-grid">']
    for item in scenarios:
        html.append(
            (
                '<div class="rx-start-card">'
                f'<div class="rx-start-label">{escape(item["stage"])}</div>'
                f'<div class="rx-start-title">{escape(item["label"])}</div>'
                f'<div class="rx-start-copy">{escape(item["best_for"])}</div>'
                f'<div class="rx-start-foot">{escape(item["expected_state"])}</div>'
                "</div>"
            )
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _scenario_switcher(matrix: dict, active_scenario_id: str) -> None:
    rows = matrix["rows"]
    html = ['<div class="rx-scenario-grid">']
    for row in rows:
        active_class = " rx-scenario-card-active" if row["id"] == active_scenario_id else ""
        pill = "Current" if row["id"] == active_scenario_id else zh(row["product_state"])
        html.append(
            (
                f'<div class="rx-scenario-card{active_class}">'
                '<div class="rx-scenario-top">'
                f'<div class="rx-scenario-stage">{escape(row["stage"])}</div>'
                f'<div class="rx-scenario-pill">{escape(pill)}</div>'
                "</div>"
                f'<div class="rx-scenario-title">{escape(row["label"])}</div>'
                f'<div class="rx-scenario-copy">{escape(row["best_for"])}</div>'
                '<div class="rx-scenario-metrics">'
                '<div class="rx-scenario-metric">'
                '<div class="rx-scenario-metric-label">Measured</div>'
                f'<div class="rx-scenario-metric-value">{escape(str(row["measured_area_count"]))} areas</div>'
                "</div>"
                '<div class="rx-scenario-metric">'
                '<div class="rx-scenario-metric-label">Benchmark</div>'
                f'<div class="rx-scenario-metric-value">{escape(str(row["benchmark_sessions"]))} logs</div>'
                "</div>"
                '<div class="rx-scenario-metric">'
                '<div class="rx-scenario-metric-label">Starter Path</div>'
                f'<div class="rx-scenario-metric-value">{escape("Open" if row["starter_path_available"] else "Gated")}</div>'
                "</div>"
                '<div class="rx-scenario-metric">'
                '<div class="rx-scenario-metric-label">Retest</div>'
                f'<div class="rx-scenario-metric-value">{escape("Ready" if row["retest_ready"] else "Waiting")}</div>'
                "</div>"
                "</div>"
                f'<div class="rx-scenario-pages">{escape(" -> ".join(row["recommended_pages"]))}</div>'
                "</div>"
            )
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)

    columns = st.columns(len(rows))
    for column, row in zip(columns, rows):
        with column:
            is_active = row["id"] == active_scenario_id
            button_type = "primary" if row["id"] == matrix["recommended_first_scenario"] else "secondary"
            st.button(
                "当前场景" if is_active else f"加载 {row['label']}",
                width="stretch",
                type=button_type,
                disabled=is_active,
                on_click=_load_demo_scenario,
                args=(row["id"],),
                key=f"scenario_card_load_{row['id']}",
            )


def _lab_console(console: dict) -> None:
    html = ['<div class="rx-lab-console">']
    for card in console["cards"]:
        class_status = str(card["status"]).replace("_", "-")
        html.append(
            (
                f'<div class="rx-lab-card rx-lab-card-{escape(class_status)}">'
                '<div class="rx-lab-top">'
                f'<div class="rx-lab-label">{escape(card["label"])}</div>'
                f'<div class="rx-lab-status">{escape(zh(card["status"]))}</div>'
                "</div>"
                f'<div class="rx-lab-detail">{escape(card["detail"])}</div>'
                f'<div class="rx-lab-action">{escape(card["action"])}</div>'
                "</div>"
            )
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _session_quality_console(review: dict) -> None:
    cards = [
        (
            "Safety",
            review["summary"]["safety_gate"],
            "Safety can block handoff, but does not change measured performance.",
            "rx-quality-card-blocked" if review["summary"]["safety_gate"] == "RED" else "rx-quality-card-ready",
        ),
        (
            "Measured Areas",
            str(review["summary"]["measured_performance_areas"]),
            "At least two measured dimensions are needed for strongest/gap interpretation.",
            "rx-quality-card-ready" if review["summary"]["measured_performance_areas"] >= 2 else "rx-quality-card-waiting",
        ),
        (
            "Benchmark Logs",
            str(review["summary"]["benchmark_sessions"]),
            "Raw protocol-anchored logs make the session reviewable.",
            "rx-quality-card-ready" if review["summary"]["benchmark_sessions"] else "rx-quality-card-waiting",
        ),
        (
            "Feedback",
            str(review["summary"]["feedback_weeks"]),
            "Weekly completion and RPE turn a plan into an adaptive loop.",
            "rx-quality-card-ready" if review["summary"]["feedback_weeks"] else "rx-quality-card-waiting",
        ),
        (
            "Retest",
            "Ready" if review["summary"]["retest_ready"] else "Waiting",
            "Retest comparison stays personal and raw, not predictive.",
            "rx-quality-card-ready" if review["summary"]["retest_ready"] else "rx-quality-card-waiting",
        ),
        (
            "Evidence",
            str(review["summary"]["evidence_sources"]),
            "Saved sources support claim boundaries, not validation claims.",
            "rx-quality-card-ready" if review["summary"]["evidence_sources"] else "rx-quality-card-waiting",
        ),
    ]
    html = [
        '<div class="rx-quality-console">',
        '<div class="rx-quality-head">',
        '<div>',
        '<div class="rx-quality-kicker">Session quality review</div>',
        '<div class="rx-quality-title">这次 SportRx session 够不够解释？</div>',
        f'<div class="rx-quality-copy">{escape(review["claim_boundary"])}</div>',
        "</div>",
        '<div class="rx-quality-status">',
        '<div class="rx-quality-label">Next action</div>',
        f'<div class="rx-quality-value">{escape(zh(review["status"]))}</div>',
        f'<div class="rx-quality-detail">{escape(zh(review["next_action"]))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-quality-grid">',
    ]
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-quality-card {class_name}">'
                f'<div class="rx-quality-label">{escape(label)}</div>'
                f'<div class="rx-quality-value">{escape(zh(value))}</div>'
                f'<div class="rx-quality-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _protocol_deviation_console(review: dict) -> None:
    flag_total = sum(review["flag_counts"].values())
    cards = [
        (
            "Sessions",
            str(review["session_count"]),
            "Saved Benchmark Log sessions reviewed.",
            "rx-quality-card-ready" if review["session_count"] else "rx-quality-card-waiting",
        ),
        (
            "Completed Components",
            str(review["completed_component_count"]),
            "Only completed components with raw values are reviewed.",
            "rx-quality-card-ready" if review["completed_component_count"] else "rx-quality-card-waiting",
        ),
        (
            "Context Flags",
            str(flag_total),
            ", ".join(f"{key}: {value}" for key, value in sorted(review["flag_counts"].items())) or "none",
            "rx-quality-card-waiting" if flag_total else "rx-quality-card-ready",
        ),
        (
            "Retest Context",
            str(review["context_changed_count"]),
            "Counts repeated components where protocol, unit, equipment, or substitution changed.",
            "rx-quality-card-waiting" if review["context_changed_count"] else "rx-quality-card-ready",
        ),
    ]
    html = [
        '<div class="rx-quality-console">',
        '<div class="rx-quality-head">',
        '<div>',
        '<div class="rx-quality-kicker">Protocol deviation review</div>',
        '<div class="rx-quality-title">这次 Benchmark 记录可不可以复测比较？</div>',
        f'<div class="rx-quality-copy">{escape(review["claim_boundary"])}</div>',
        "</div>",
        '<div class="rx-quality-status">',
        '<div class="rx-quality-label">Next action</div>',
        f'<div class="rx-quality-value">{escape(zh(review["status"]))}</div>',
        f'<div class="rx-quality-detail">{escape(zh(review["next_action"]))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-quality-grid">',
    ]
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-quality-card {class_name}">'
                f'<div class="rx-quality-label">{escape(label)}</div>'
                f'<div class="rx-quality-value">{escape(zh(value))}</div>'
                f'<div class="rx-quality-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _retest_interpretation_console(guard: dict) -> None:
    cards = [
        (
            "Comparisons",
            str(guard["comparison_count"]),
            "Repeated benchmark components with raw delta.",
            "rx-quality-card-ready" if guard["comparison_count"] else "rx-quality-card-waiting",
        ),
        (
            "Comparable",
            str(guard["comparable_count"]),
            "Raw changes with matching protocol context.",
            "rx-quality-card-ready" if guard["comparable_count"] else "rx-quality-card-waiting",
        ),
        (
            "Context Changed",
            str(guard["context_changed_count"]),
            "Protocol, unit, equipment, or substitution changed.",
            "rx-quality-card-waiting" if guard["context_changed_count"] else "rx-quality-card-ready",
        ),
        (
            "Protocol Review",
            guard["protocol_deviation_status"],
            "Comes from Protocol Deviation Review.",
            "rx-quality-card-ready" if guard["protocol_deviation_status"] == "repeatable_protocol_record" else "rx-quality-card-waiting",
        ),
    ]
    html = [
        '<div class="rx-quality-console">',
        '<div class="rx-quality-head">',
        '<div>',
        '<div class="rx-quality-kicker">Retest interpretation guard</div>',
        '<div class="rx-quality-title">复测变化能不能解释？</div>',
        f'<div class="rx-quality-copy">{escape(guard["claim_boundary"])}</div>',
        "</div>",
        '<div class="rx-quality-status">',
        '<div class="rx-quality-label">Next action</div>',
        f'<div class="rx-quality-value">{escape(zh(guard["status"]))}</div>',
        f'<div class="rx-quality-detail">{escape(zh(guard["next_action"]))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-quality-grid">',
    ]
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-quality-card {class_name}">'
                f'<div class="rx-quality-label">{escape(label)}</div>'
                f'<div class="rx-quality-value">{escape(zh(value))}</div>'
                f'<div class="rx-quality-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _lab_measurement_review(review: dict) -> None:
    html = [
        '<div class="rx-lab-measure-panel">',
        '<div class="rx-lab-measure-head">',
        '<div>',
        '<div class="rx-lab-measure-kicker">Measurement review</div>',
        '<div class="rx-lab-measure-title">HYROX Check 测量状态</div>',
        f'<div class="rx-lab-measure-copy">{escape(review["claim_boundary"])}</div>',
        "</div>",
        '<div class="rx-lab-measure-status">',
        '<div class="rx-lab-measure-label">Next Action</div>',
        f'<div class="rx-lab-measure-value">{escape(zh(review["status"]))}</div>',
        f'<div class="rx-lab-measure-detail">{escape(zh(review["next_action"]))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-lab-measure-grid">',
    ]
    for card in review["cards"]:
        class_status = str(card["status"]).replace("_", "-")
        html.append(
            (
                f'<div class="rx-lab-measure-card rx-lab-measure-card-{escape(class_status)}">'
                f'<div class="rx-lab-measure-label">{escape(zh(card["label"]))}</div>'
                f'<div class="rx-lab-measure-value">{escape(zh(card["value"]))}</div>'
                f'<div class="rx-lab-measure-detail">{escape(zh(card["detail"]))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _measurement_intake_matrix_console(matrix: dict) -> None:
    summary = matrix["summary"]
    cards = [
        (
            "Measured",
            f"{summary['measured']} / {summary['total']}",
            "Tests with actual values saved in the current profile.",
            "rx-lab-measure-card-ready" if summary["measured"] else "rx-lab-measure-card-waiting",
        ),
        (
            "Not Tested",
            str(summary["not_tested"]),
            "Missing components stay explicit; they are not replaced by defaults.",
            "rx-lab-measure-card-ready" if summary["not_tested"] == 0 else "rx-lab-measure-card-waiting",
        ),
        (
            "Review Ready",
            str(summary["review_ready"]),
            "Measured fields with raw timed values or recorded protocol provenance.",
            "rx-lab-measure-card-ready" if summary["review_ready"] else "rx-lab-measure-card-waiting",
        ),
        (
            "Protocol Source",
            "Missing" if summary["missing_protocol_source"] else "Complete",
            "Station and Work capacity scores need a named protocol source.",
            "rx-lab-measure-card-waiting" if summary["missing_protocol_source"] else "rx-lab-measure-card-ready",
        ),
    ]
    html = [
        '<div class="rx-lab-measure-panel">',
        '<div class="rx-lab-measure-head">',
        '<div>',
        '<div class="rx-lab-measure-kicker">Measurement intake matrix</div>',
        '<div class="rx-lab-measure-title">哪些项目是真测，哪些还没测？</div>',
        f'<div class="rx-lab-measure-copy">{escape(matrix["claim_boundary"])}</div>',
        "</div>",
        '<div class="rx-lab-measure-status">',
        '<div class="rx-lab-measure-label">Next Action</div>',
        f'<div class="rx-lab-measure-value">{escape(zh(matrix["status"]))}</div>',
        f'<div class="rx-lab-measure-detail">{escape(zh(matrix["next_action"]))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-lab-measure-grid">',
    ]
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-lab-measure-card {class_name}">'
                f'<div class="rx-lab-measure-label">{escape(label)}</div>'
                f'<div class="rx-lab-measure-value">{escape(zh(value))}</div>'
                f'<div class="rx-lab-measure-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _lab_component_board(matrix: dict) -> None:
    status_class = {
        "measured_review_ready": "rx-lab-component-ready",
        "measured_needs_protocol": "rx-lab-component-blocked",
        "not_tested": "rx-lab-component-waiting",
    }
    html = ['<div class="rx-lab-component-grid">']
    for row in matrix["rows"]:
        class_name = status_class.get(row["status"], "rx-lab-component-waiting")
        value = "Not tested" if row["status"] == "not_tested" else f"{row['value']} {row['unit']}"
        source = row.get("protocol_source") or "No protocol source"
        counts = "参与 gap 比较" if row["counts_for_gap_comparison"] else "不参与 gap 比较"
        html.append(
            (
                f'<div class="rx-lab-component-card {class_name}">'
                '<div class="rx-lab-component-top">'
                "<div>"
                f'<div class="rx-lab-component-kicker">{escape(zh(row["dimension"]))}</div>'
                f'<div class="rx-lab-component-title">{escape(zh(row["test"]))}</div>'
                "</div>"
                '<div class="rx-lab-component-status">'
                '<div class="rx-lab-component-label">Status</div>'
                f'<div class="rx-lab-component-value">{escape(zh(row["status"]))}</div>'
                "</div>"
                "</div>"
                '<div class="rx-lab-component-label">Recorded value</div>'
                f'<div class="rx-lab-component-value">{escape(zh(value))}</div>'
                '<div class="rx-lab-component-detail">'
                f'{escape(zh(source))}<br>{escape(counts)}<br>{escape(zh(row["next_step"]))}'
                "</div>"
                "</div>"
            )
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _lab_measured_picture_cards(result: dict) -> None:
    html = ['<div class="rx-lab-picture-grid">']
    for item in result["performance_profile"].values():
        measured = item["score"] is not None
        class_name = "rx-lab-picture-measured" if measured else "rx-lab-picture-missing"
        value = "Not tested" if item["score"] is None else f"{item['score']} · {zh(item['status'])}"
        if item.get("evidence"):
            detail = "；".join(zh(part) for part in item["evidence"][:2])
        elif item.get("missing"):
            detail = "缺少：" + "；".join(zh(part) for part in item["missing"][:2])
        else:
            detail = "等待 SportRx Hybrid Benchmark v1。"
        html.append(
            (
                f'<div class="rx-lab-picture-card {class_name}">'
                f'<div class="rx-lab-picture-label">{escape(zh(item["source"]))}</div>'
                f'<div class="rx-lab-picture-title">{escape(zh(item["label"]))}</div>'
                f'<div class="rx-lab-picture-value">{escape(zh(value))}</div>'
                f'<div class="rx-lab-picture-detail">{escape(detail)}</div>'
                "</div>"
            )
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _lab_test_quality_console(quality: dict) -> None:
    html = [
        '<div class="rx-quality-console">',
        '<div class="rx-quality-head">',
        '<div>',
        '<div class="rx-quality-kicker">Lab test quality</div>',
        '<div class="rx-quality-title">实测记录是否有足够 protocol 来源？</div>',
        f'<div class="rx-quality-copy">{escape(quality["claim_boundary"])}</div>',
        "</div>",
        '<div class="rx-quality-status">',
        '<div class="rx-quality-label">Next Action</div>',
        f'<div class="rx-quality-value">{escape(zh(quality["status"]))}</div>',
        f'<div class="rx-quality-detail">{escape(zh(quality["next_action"]))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-quality-grid">',
    ]
    for card in quality["cards"]:
        status = card.get("status", "waiting")
        if status == "blocked":
            class_name = "rx-quality-card-blocked"
        elif status == "ready":
            class_name = "rx-quality-card-ready"
        else:
            class_name = "rx-quality-card-waiting"
        html.append(
            (
                f'<div class="rx-quality-card {class_name}">'
                f'<div class="rx-quality-label">{escape(zh(card["label"]))}</div>'
                f'<div class="rx-quality-value">{escape(zh(card["value"]))}</div>'
                f'<div class="rx-quality-detail">{escape(zh(card["detail"]))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _protocol_source_guide_console(guide: dict) -> None:
    html = [
        '<div class="rx-quality-console">',
        '<div class="rx-quality-head">',
        '<div>',
        '<div class="rx-quality-kicker">Protocol source guide</div>',
        '<div class="rx-quality-title">Protocol 分数从哪里来？</div>',
        f'<div class="rx-quality-copy">{escape(guide["primary_message"])}</div>',
        "</div>",
        '<div class="rx-quality-status">',
        '<div class="rx-quality-label">Status</div>',
        f'<div class="rx-quality-value">{escape(zh(guide["status"]))}</div>',
        f'<div class="rx-quality-detail">{escape(zh(guide["next_action"]))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-quality-grid">',
    ]
    for source in guide["sources"]:
        class_name = "rx-quality-card-ready" if source["status"].startswith("accepted") else "rx-quality-card-waiting"
        html.append(
            (
                f'<div class="rx-quality-card {class_name}">'
                f'<div class="rx-quality-label">{escape(source["source"])}</div>'
                f'<div class="rx-quality-value">{escape(zh(source["status"]))}</div>'
                f'<div class="rx-quality-detail">{escape(source["use_when"])}<br>Blocked: {escape(source["not_allowed_for"])}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _protocol_source_rows(guide: dict) -> list[dict]:
    return [
        {
            "Source": item["source"],
            "Status": zh(item["status"]),
            "Use when": item["use_when"],
            "Requires note": "yes" if item["requires_note"] else "no",
            "Not allowed for": item["not_allowed_for"],
        }
        for item in guide["sources"]
    ]


def _benchmark_protocol_console(protocol: dict, worksheet: dict, brief: dict, readiness: dict) -> None:
    required_components = sum(1 for component in protocol["component_protocols"] if not component.get("optional"))
    optional_components = len(protocol["component_protocols"]) - required_components
    safety_status = readiness.get("summary", {}).get("safety_gate", "UNKNOWN")
    equipment_count = int(readiness.get("summary", {}).get("equipment_count", 0) or 0)
    cards = [
        (
            "Protocol Path",
            protocol["path"],
            f"{protocol['version']} / {protocol['evidence_status']}",
            "rx-protocol-card-ready",
        ),
        (
            "Components",
            f"{required_components}+{optional_components}",
            "Recommended plus optional components for this path.",
            "rx-protocol-card-ready",
        ),
        (
            "Stop Rules",
            str(len(protocol["global_stop_rules"])),
            "Safety rules must be checked before test execution.",
            "rx-protocol-card-blocked" if safety_status == "RED" else "rx-protocol-card-ready",
        ),
        (
            "Worksheet",
            f"{len(worksheet['component_rows'])} rows",
            "Paper-friendly raw data capture before app entry.",
            "rx-protocol-card-ready",
        ),
        (
            "Test-Day Brief",
            f"{len(brief['components'])} tests",
            "Operator checklist for setup, execution, and after-test notes.",
            "rx-protocol-card-ready",
        ),
        (
            "Equipment",
            f"{equipment_count} selected",
            "No equipment selected routes to the low-equipment path.",
            "rx-protocol-card-ready" if equipment_count else "rx-protocol-card-waiting",
        ),
    ]
    html = [
        '<div class="rx-protocol-console">',
        '<div class="rx-protocol-head">',
        '<div>',
        '<div class="rx-protocol-kicker">Protocol command console</div>',
        '<div class="rx-protocol-title">测试当天按这个顺序执行</div>',
        f'<div class="rx-protocol-copy">{escape(protocol["claim_boundary"])}</div>',
        "</div>",
        '<div class="rx-protocol-status">',
        '<div class="rx-protocol-label">Next Action</div>',
        f'<div class="rx-protocol-value">{escape(zh(readiness["status"]))}</div>',
        f'<div class="rx-protocol-detail">{escape(zh(readiness["next_action"]))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-protocol-grid">',
    ]
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-protocol-card {class_name}">'
                f'<div class="rx-protocol-label">{escape(label)}</div>'
                f'<div class="rx-protocol-value">{escape(zh(value))}</div>'
                f'<div class="rx-protocol-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _benchmark_protocol_components(protocol: dict) -> None:
    html = ['<div class="rx-protocol-components">']
    for component in protocol["component_protocols"]:
        optional = bool(component.get("optional"))
        class_name = "rx-protocol-component-optional" if optional else "rx-protocol-component-required"
        required = "Optional" if optional else "Recommended"
        equipment = ", ".join(component.get("required_equipment", [])) or "none"
        fields = ", ".join(component.get("fields", [])) or "raw result, RPE, notes"
        html.append(
            (
                f'<div class="rx-protocol-component {class_name}">'
                f'<div class="rx-protocol-component-meta">{escape(zh(component["area"]))} · {escape(required)}</div>'
                f'<div class="rx-protocol-component-title">{escape(component["test"])}</div>'
                f'<div class="rx-protocol-component-copy">{escape(zh(component["purpose"]))}</div>'
                f'<div class="rx-protocol-component-foot"><strong>Equipment</strong><br>{escape(zh(equipment))}</div>'
                f'<div class="rx-protocol-component-foot"><strong>Record</strong><br>{escape(zh(fields))}</div>'
                "</div>"
            )
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _training_block_console(block: dict) -> None:
    available = bool(block.get("available"))
    weeks = block.get("weeks", [])
    total_sessions = sum(len(week.get("sessions", [])) for week in weeks)
    weekly_minutes = [int(week.get("weekly_minutes") or 0) for week in weeks]
    minute_range = (
        f"{min(weekly_minutes)}-{max(weekly_minutes)} min/week"
        if weekly_minutes
        else "Not generated"
    )
    safety_status = block.get("safety_gate_status", "blocked" if not available else "UNKNOWN")
    based_on = block.get("based_on_gap") or block.get("reason", "Measurement gate")
    cards = [
        (
            "Handoff",
            "Available" if available else "Blocked",
            "Only generated after Safety Gate and measurement gates allow it.",
            "rx-training-card-ready" if available else "rx-training-card-blocked",
        ),
        (
            "Based On",
            based_on,
            "Training focus comes from measured main gap, not a chat prompt.",
            "rx-training-card-ready" if available else "rx-training-card-waiting",
        ),
        (
            "Block Length",
            f"{len(weeks)} weeks" if weeks else "0 weeks",
            "SportRx keeps this as a short starter block before retest.",
            "rx-training-card-ready" if weeks else "rx-training-card-waiting",
        ),
        (
            "Sessions",
            str(total_sessions),
            "Each session keeps duration, RPE, talk test, and execution notes.",
            "rx-training-card-ready" if total_sessions else "rx-training-card-waiting",
        ),
        (
            "Weekly Volume",
            minute_range,
            "Volume is constrained by current profile and stated time capacity.",
            "rx-training-card-ready" if weekly_minutes else "rx-training-card-waiting",
        ),
        (
            "Feedback Loop",
            "Required" if available else "Waiting",
            "Weekly completion and RPE decide hold/progress/reduce.",
            "rx-training-card-ready" if available else "rx-training-card-waiting",
        ),
    ]
    html = [
        '<div class="rx-training-console">',
        '<div class="rx-training-head">',
        '<div>',
        '<div class="rx-training-kicker">Training handoff console</div>',
        '<div class="rx-training-title">从测量交接到 4-week Starter Path</div>',
        f'<div class="rx-training-copy">{escape(block["claim_boundary"])}</div>',
        "</div>",
        '<div class="rx-training-status">',
        '<div class="rx-training-label">Safety Gate</div>',
        f'<div class="rx-training-value">{escape(zh(safety_status))}</div>',
        f'<div class="rx-training-detail">{escape(zh("可以执行，但每周必须记录 RPE 和完成率。" if available else block.get("next_action", "Complete benchmark first.")))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-training-grid">',
    ]
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-training-card {class_name}">'
                f'<div class="rx-training-label">{escape(label)}</div>'
                f'<div class="rx-training-value">{escape(zh(value))}</div>'
                f'<div class="rx-training-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _feedback_loop_console(dashboard: dict) -> None:
    adherence = dashboard["adherence"]
    latest_row = _latest_recorded_feedback_row(dashboard)
    retest_count = len(dashboard.get("retest_comparisons", []))
    plan_actual_count = len(dashboard.get("plan_actual_reasons", []))
    next_action = dashboard.get("next_actions", ["No active training plan is available."])[0]
    available = bool(dashboard.get("available"))
    if latest_row is not None:
        latest_action = latest_row["plan_actual"]["action_label"]
        change_by_action = {
            "increase": "+15%",
            "small_increase": "+10%",
            "decrease": "-10%",
            "hold": "0%",
            "pause": "0%",
            "not_entered": "等待反馈",
        }
        latest_change_label = change_by_action.get(latest_row["plan_actual"]["action"], "按规则")
        latest_card_class = "rx-feedback-card-ready"
    else:
        latest_action = "No feedback yet"
        latest_change_label = "等待反馈"
        latest_card_class = "rx-feedback-card-waiting"
    completion = adherence.get("average_completion_rate")
    completion_value = "Not recorded" if completion is None else f"{round(float(completion) * 100)}%"
    cards = [
        (
            "Adherence",
            adherence["status"],
            f"{adherence['completed_sessions']} / {adherence['planned_sessions']} planned sessions recorded.",
            "rx-feedback-card-blocked" if adherence["status"] == "Pause and review" else "rx-feedback-card-ready" if adherence["weeks_recorded"] else "rx-feedback-card-waiting",
        ),
        (
            "Weeks Recorded",
            str(adherence["weeks_recorded"]),
            "Weekly completion and RPE are required before adaptive progression is meaningful.",
            "rx-feedback-card-ready" if adherence["weeks_recorded"] else "rx-feedback-card-waiting",
        ),
        (
            "Completion",
            completion_value,
            f"Average RPE: {adherence.get('average_rpe') if adherence.get('average_rpe') is not None else 'not recorded'}.",
            "rx-feedback-card-ready" if completion is not None and completion >= 0.8 else "rx-feedback-card-waiting",
        ),
        (
            "Latest Decision",
            latest_action,
            "最近一条已填写周反馈触发的规则动作；未填写周保持 preview。",
            latest_card_class,
        ),
        (
            "Dose Change",
            latest_change_label,
            "Dose changes remain conservative and inspectable.",
            latest_card_class,
        ),
        (
            "Retest",
            "Retest ready" if retest_count else "No retest yet",
            f"{retest_count} raw comparison(s); {plan_actual_count} plan-actual reason objects.",
            "rx-feedback-card-ready" if retest_count else "rx-feedback-card-waiting",
        ),
    ]
    html = [
        '<div class="rx-feedback-console">',
        '<div class="rx-feedback-head">',
        '<div>',
        '<div class="rx-feedback-kicker">Adaptive loop console</div>',
        '<div class="rx-feedback-title">训练反馈如何影响下一周</div>',
        f'<div class="rx-feedback-copy">{escape(dashboard["claim_boundary"])}</div>',
        "</div>",
        '<div class="rx-feedback-status">',
        '<div class="rx-feedback-label">Next Action</div>',
        f'<div class="rx-feedback-value">{escape("Rule-coded" if available else "Blocked")}</div>',
        f'<div class="rx-feedback-detail">{escape(zh(next_action))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-feedback-grid">',
    ]
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-feedback-card {class_name}">'
                f'<div class="rx-feedback-label">{escape(label)}</div>'
                f'<div class="rx-feedback-value">{escape(zh(value))}</div>'
                f'<div class="rx-feedback-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _feedback_percent_label(value: float | None) -> str:
    if value is None:
        return "未填写"
    return f"{round(float(value) * 100)}%"


def _feedback_loop_snapshot(dashboard: dict, retest_guard: dict) -> None:
    adherence = dashboard["adherence"]
    weekly_rows = dashboard.get("weekly_feedback", [])
    recorded_rows = [row for row in weekly_rows if row.get("completed_sessions") is not None]
    adverse_count = sum(1 for row in recorded_rows if row.get("adverse_event"))
    hard_count = sum(1 for row in recorded_rows if row.get("felt_too_hard"))
    retest_items = retest_guard.get("items", [])
    cards = [
        (
            "周反馈记录",
            f"{adherence['weeks_recorded']} / {len(weekly_rows)} 周",
            "只有填写完成次数和 RPE 后，进阶才从 preview 变成 feedback-based。",
            "rx-loop-card-ready" if adherence["weeks_recorded"] else "rx-loop-card-waiting",
        ),
        (
            "完成率",
            _feedback_percent_label(adherence.get("average_completion_rate")),
            f"{adherence['completed_sessions']} / {adherence['planned_sessions']} planned sessions。",
            "rx-loop-card-ready" if adherence.get("average_completion_rate") is not None else "rx-loop-card-waiting",
        ),
        (
            "平均 RPE",
            "未填写" if adherence.get("average_rpe") is None else str(adherence["average_rpe"]),
            f"明显偏难 {hard_count} 周；不良事件 {adverse_count} 次。",
            "rx-loop-card-blocked" if adverse_count else "rx-loop-card-ready" if adherence.get("average_rpe") is not None else "rx-loop-card-waiting",
        ),
        (
            "复测解释",
            f"{len(retest_items)} 项",
            "只有重复完成同一 Benchmark component，才比较原始变化。",
            "rx-loop-card-ready" if retest_items else "rx-loop-card-waiting",
        ),
    ]
    html = ['<div class="rx-loop-grid">']
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-loop-card {class_name}">'
                f'<div class="rx-loop-label">{escape(label)}</div>'
                f'<div class="rx-loop-value">{escape(zh(value))}</div>'
                f'<div class="rx-loop-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _latest_recorded_feedback_row(dashboard: dict) -> dict | None:
    rows = [row for row in dashboard.get("weekly_feedback", []) if row.get("completed_sessions") is not None]
    if not rows:
        return None
    return sorted(rows, key=lambda row: int(row["week"]))[-1]


def _feedback_decision_panel(dashboard: dict) -> None:
    row = _latest_recorded_feedback_row(dashboard)
    if row is None:
        title = "等待第一条周反馈"
        value = "Preview only"
        copy = "当前后续周仍是没有周反馈时的 provisional preview；SportRx 还不能声称它已经根据你的执行情况调整。"
        chips = ["PROVISIONAL_NO_FEEDBACK", "FEEDBACK_INCOMPLETE"]
        class_name = "rx-loop-card-waiting"
    else:
        plan_actual = row["plan_actual"]
        title = f"Week {row['week']} 后的规则动作"
        value = zh(plan_actual["action_label"])
        completion = _feedback_percent_label(plan_actual.get("completion_rate"))
        rpe = "未填写" if plan_actual.get("average_rpe") is None else str(plan_actual["average_rpe"])
        copy = f"完成率 {completion}，平均 RPE {rpe}。这只是 plan-actual 规则解释，不是恢复评分或风险预测。"
        chips = list(plan_actual.get("reason_codes", [])) + list(plan_actual.get("flags", []))
        class_name = "rx-loop-card-blocked" if plan_actual["action"] == "pause" else "rx-loop-card-ready"

    html = [
        f'<div class="rx-decision-panel {class_name}">',
        '<div class="rx-decision-head">',
        "<div>",
        '<div class="rx-decision-kicker">Plan-actual decision</div>',
        f'<div class="rx-decision-title">{escape(title)}</div>',
        f'<div class="rx-decision-copy">{escape(zh(copy))}</div>',
        "</div>",
        '<div class="rx-decision-dose">',
        '<div class="rx-loop-label">Action</div>',
        f'<div class="rx-loop-value">{escape(zh(value))}</div>',
        '<div class="rx-loop-detail">由完成率、RPE、偏难标记和不良事件标记触发。</div>',
        "</div>",
        "</div>",
        '<div class="rx-decision-reasons">',
    ]
    for chip in chips or ["HOLD_FOR_STABILITY"]:
        html.append(f'<div class="rx-decision-chip">{escape(zh(chip))}</div>')
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _weekly_feedback_cards(dashboard: dict) -> None:
    rows = dashboard.get("weekly_feedback", [])
    if not rows:
        st.info("当前没有可记录的训练周。")
        return

    html = ['<div class="rx-loop-grid">']
    for row in rows:
        plan_actual = row["plan_actual"]
        completed = row.get("completed_sessions")
        if completed is None:
            value = "未填写"
            detail = "等待完成次数、平均 RPE 和是否偏难。"
            class_name = "rx-loop-card-waiting"
        else:
            value = f"{completed} / {row['planned_sessions']} sessions"
            rpe = "未填写" if row.get("average_rpe") is None else row["average_rpe"]
            detail = f"完成率 {_feedback_percent_label(row.get('completion_rate'))}；RPE {rpe}；动作：{zh(plan_actual['action_label'])}。"
            class_name = "rx-loop-card-blocked" if row.get("adverse_event") else "rx-loop-card-ready"
        html.append(
            (
                f'<div class="rx-loop-card {class_name}">'
                f'<div class="rx-loop-label">Week {escape(str(row["week"]))}</div>'
                f'<div class="rx-loop-value">{escape(zh(value))}</div>'
                f'<div class="rx-loop-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _retest_loop_cards(dashboard: dict, retest_guard: dict) -> None:
    summary = dashboard["benchmark_summary"]
    items = retest_guard.get("items", [])
    comparable = sum(1 for item in items if item.get("interpretation_status") == "comparable_raw_change")
    context_review = sum(1 for item in items if item.get("context_changes"))
    cards = [
        (
            "Benchmark Sessions",
            str(summary["session_count"]),
            f"Latest date: {summary['latest_date'] or '未记录'}",
            "rx-loop-card-ready" if summary["session_count"] else "rx-loop-card-waiting",
        ),
        (
            "Measured Components",
            str(len(summary["measured_components"])),
            "复测比较只看重复完成的同一 component。",
            "rx-loop-card-ready" if summary["measured_components"] else "rx-loop-card-waiting",
        ),
        (
            "Comparable Retest",
            str(comparable),
            "Context 改变会保留为解释边界，不会被抹平。",
            "rx-loop-card-ready" if comparable else "rx-loop-card-waiting",
        ),
        (
            "Context Flags",
            str(context_review),
            "路线、器械、负重、替代动作变化会影响解释信心。",
            "rx-loop-card-waiting" if context_review else "rx-loop-card-ready",
        ),
    ]
    html = ['<div class="rx-loop-grid">']
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-loop-card {class_name}">'
                f'<div class="rx-loop-label">{escape(label)}</div>'
                f'<div class="rx-loop-value">{escape(zh(value))}</div>'
                f'<div class="rx-loop-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _pilot_review_console(console: dict) -> None:
    html = [
        '<div class="rx-pilot-console">',
        '<div class="rx-pilot-head">',
        '<div>',
        '<div class="rx-pilot-kicker">Pilot review console</div>',
        '<div class="rx-pilot-title">Alpha 试用反馈状态</div>',
        f'<div class="rx-pilot-copy">{escape(console["claim_boundary"])}</div>',
        "</div>",
        '<div class="rx-pilot-status">',
        '<div class="rx-pilot-label">Next Action</div>',
        f'<div class="rx-pilot-value">{escape(zh(console["status"]))}</div>',
        f'<div class="rx-pilot-detail">{escape(zh(console["next_action"]))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-pilot-grid">',
    ]
    for card in console["cards"]:
        class_status = str(card["status"]).replace("_", "-")
        html.append(
            (
                f'<div class="rx-pilot-card rx-pilot-card-{escape(class_status)}">'
                f'<div class="rx-pilot-label">{escape(card["label"])}</div>'
                f'<div class="rx-pilot-value">{escape(zh(card["value"]))}</div>'
                f'<div class="rx-pilot-detail">{escape(zh(card["detail"]))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _alpha_dataset_template_console(template: dict) -> None:
    html = [
        '<div class="rx-pilot-console">',
        '<div class="rx-pilot-head">',
        '<div>',
        '<div class="rx-pilot-kicker">Alpha dataset template</div>',
        '<div class="rx-pilot-title">5-10 人试用的数据采集包</div>',
        f'<div class="rx-pilot-copy">{escape(template["claim_boundary"])}</div>',
        "</div>",
        '<div class="rx-pilot-status">',
        '<div class="rx-pilot-label">Status</div>',
        f'<div class="rx-pilot-value">{escape(zh(template["status"]))}</div>',
        f'<div class="rx-pilot-detail">{escape(template["participant_scope"])}</div>',
        "</div>",
        "</div>",
        '<div class="rx-pilot-grid">',
    ]
    for table in template["tables"]:
        html.append(
            (
                '<div class="rx-pilot-card rx-pilot-card-ready">'
                f'<div class="rx-pilot-label">{escape(table["id"])}</div>'
                f'<div class="rx-pilot-value">{len(table["fields"])} fields</div>'
                f'<div class="rx-pilot-detail">{escape(table["purpose"])}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _alpha_dataset_table_rows(template: dict) -> list[dict]:
    return [
        {
            "表": table["id"],
            "文件": table["filename"],
            "字段数": len(table["fields"]),
            "用途": table["purpose"],
            "关键字段": ", ".join(table["fields"][:5]),
        }
        for table in template["tables"]
    ]


def _measurement_timeline(timeline: dict) -> None:
    completion = timeline["completion"]
    percent = int(float(completion.get("percent", 0)) * 100)
    st.markdown(
        (
            '<div class="rx-progress-shell">'
            f'<div class="rx-progress-fill" style="width: {percent}%"></div>'
            "</div>"
        ),
        unsafe_allow_html=True,
    )
    html = ['<div class="rx-timeline">']
    for item in timeline["items"]:
        stage = str(item["stage"])
        html.append(
            (
                f'<div class="rx-timeline-card rx-timeline-{escape(stage)}">'
                f'<div class="rx-timeline-step">Step {item["step"]:02d} · {escape(stage)}</div>'
                f'<div class="rx-timeline-title">{escape(item["page"])}</div>'
                f'<div class="rx-timeline-status">{escape(zh(item["status"]))}</div>'
                f'<div class="rx-timeline-why">{escape(item["why"])}</div>'
                "</div>"
            )
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _card_table(card: dict) -> None:
    rows = [{"字段": key.replace("_", " ").title(), "内容": zh(value)} for key, value in card.items()]
    st.dataframe(rows, hide_index=True, width="stretch")


def _performance_rows(profile: dict) -> list[dict]:
    return [
        {
            "能力区域": zh(item["label"]),
            "结果": zh(item["status"]),
            "来源": zh(item["source"]),
            "依据": "；".join(item["evidence"]) if item["evidence"] else "未测试",
        }
        for item in profile.values()
    ]


def _measurement_intake_rows(matrix: dict) -> list[dict]:
    return [
        {
            "测试": zh(row["test"]),
            "维度": zh(row["dimension"]),
            "状态": zh(row["status"]),
            "当前值": zh(row["value"]),
            "单位": zh(row["unit"]),
            "数据类型": zh(row["data_kind"]),
            "来源状态": zh(row["source_status"]),
            "Protocol": zh(row["protocol_source"]),
            "参与 gap 比较": "是" if row["counts_for_gap_comparison"] else "否",
            "下一步": zh(row["next_step"]),
        }
        for row in matrix["rows"]
    ]


def _metric_source_rows(register: dict, section: str = "all_metrics") -> list[dict]:
    rows = []
    for item in register.get(section, []):
        value = item.get("value")
        if isinstance(value, list):
            value = "、".join(str(v) for v in value) if value else "未填写"
        elif value in (None, ""):
            value = "未填写"
        rows.append(
            {
                "指标": zh(item["label"]),
                "来源": zh(item["source_label"]),
                "当前值": zh(value),
                "影响输出": "是" if item["affects_output"] else "否",
                "作用": zh(item["output_role"]),
                "输入字段": ", ".join(item["inputs"]),
            }
        )
    return rows


def _output_prerequisite_rows(register: dict) -> list[dict]:
    rows = []
    for item in register.get("outputs", []):
        rows.append(
            {
                "输出": item["label"],
                "状态": zh(item["status"]),
                "已满足": "；".join(item["met"]) if item["met"] else "无",
                "还缺": "；".join(item["missing"]) if item["missing"] else "无",
                "影响": item["affects_user"],
            }
        )
    return rows


def _context_rows(context: dict) -> list[dict]:
    labels = {
        "days_available_per_week": "每周可训练天数",
        "minutes_available_per_session": "每次可训练时间",
        "equipment_access": "可用器械",
        "recent_training_consistency": "近期训练规律性",
        "weekly_training_volume": "每周训练量",
        "resistance_training_history": "力量训练频率",
        "high_intensity_exposure": "高强度训练接触",
        "loaded_movement_exposure": "负重动作接触",
    }
    rows = []
    for key, label in labels.items():
        value = context.get(key)
        if isinstance(value, list):
            value = "、".join(value) if value else "未填写"
        rows.append({"项目": label, "当前填写": zh(value) if value else "未填写"})
    return rows


def _report_performance_rows(report: dict) -> list[dict]:
    rows = []
    for row in report["performance_rows"]:
        score = "Not tested" if row["score"] is None else row["score"]
        source_id = row.get("source")
        if row["score"] is None:
            output_role = "否"
        elif source_id == "reported_training":
            output_role = "作为训练背景"
        else:
            output_role = "实测表现维度"
        if row["evidence"]:
            basis = "；".join(row["evidence"])
        elif row["missing"]:
            basis = "缺少：" + "；".join(row["missing"])
        else:
            basis = "未记录"
        rows.append(
            {
                "能力区域": zh(row["label"]),
                "当前状态": zh(row["status"]),
                "结果": str(score),
                "来源": zh(row["source"]),
                "影响输出": output_role,
                "依据": basis,
            }
        )
    return rows


def _report_summary_rows(report: dict) -> list[dict]:
    return [
        {"项目": "Event Profile", "当前": zh(report["event_profile"])},
        {"项目": "Status", "当前": zh(report["status_label"])},
        {"项目": "Training Profile", "当前": zh(report["training_profile"])},
        {"项目": "Measured Areas", "当前": report["measurement"]["areas_assessed"]["label"]},
        {
            "项目": "Benchmark Sessions",
            "当前": str(report["measurement"]["benchmark_sessions"]["session_count"]),
        },
        {
            "项目": "Lab Test Quality",
            "当前": zh(report["measurement"].get("lab_test_quality", {}).get("status", "not_reviewed")),
        },
        {"项目": "Next Action", "当前": report["next_action"]},
    ]


def _training_week_rows(block: dict) -> list[dict]:
    return [
        {
            "周次": week["week"],
            "重点": week["focus"],
            "频率": f"{week['frequency_per_week']} sessions/week",
            "每次": f"{week['duration_min']} min",
            "周总量": f"{week['weekly_minutes']} min",
            "执行提示": week["starter_instruction"],
        }
        for week in block.get("weeks", [])
    ]


def _training_range_label(value: object, suffix: str = "") -> str:
    if isinstance(value, (list, tuple)) and len(value) == 2:
        return f"{value[0]}-{value[1]}{suffix}"
    if value is None:
        return f"未记录{suffix}" if suffix else "未记录"
    return f"{value}{suffix}"


def _training_week_cards(block: dict) -> None:
    html = ['<div class="rx-week-grid">']
    for week in block.get("weeks", []):
        focus = str(week.get("focus", "Training focus"))
        is_retest = "retest" in focus.lower() or int(week.get("week", 0)) == 4
        sessions = []
        for session in week.get("sessions", []):
            hr_zone = session.get("target_hr_zone_bpm")
            hr_label = ""
            if isinstance(hr_zone, (list, tuple)) and len(hr_zone) == 2:
                hr_label = f" · HR {hr_zone[0]}-{hr_zone[1]} bpm"
            rpe_label = _training_range_label(session.get("rpe_0_10"))
            sessions.append(
                (
                    '<div class="rx-week-session">'
                    f'<div class="rx-week-session-title">{escape(zh(session.get("day")))} · {escape(zh(session.get("purpose")))}</div>'
                    f'<div class="rx-week-session-detail">{escape(zh(session.get("activity")))} · {escape(str(session.get("duration_min")))} min · RPE {escape(rpe_label)}{escape(hr_label)}</div>'
                    "</div>"
                )
            )
        html.append(
            (
                f'<div class="rx-week-card {"rx-week-card-retest" if is_retest else ""}">'
                '<div class="rx-week-head">'
                "<div>"
                f'<div class="rx-week-kicker">Week {escape(str(week.get("week")))}</div>'
                f'<div class="rx-week-title">{escape(zh(focus))}</div>'
                "</div>"
                '<div class="rx-week-volume">'
                '<div class="rx-week-volume-label">Dose</div>'
                f'<div class="rx-week-volume-value">{escape(str(week.get("weekly_minutes")))} min<br>{escape(str(week.get("frequency_per_week")))} sessions</div>'
                "</div>"
                "</div>"
                f'<div class="rx-week-copy">{escape(zh(week.get("starter_instruction")))}</div>'
                f'<div class="rx-week-session-list">{"".join(sessions)}</div>'
                f'<div class="rx-week-review">{escape(zh(week.get("review_prompt")))}</div>'
                "</div>"
            )
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _training_session_rows(block: dict) -> list[dict]:
    rows = []
    for week in block.get("weeks", []):
        for session in week.get("sessions", []):
            rows.append(
                {
                    "周次": week["week"],
                    "日期": session["day"],
                    "目的": session["purpose"],
                    "内容": session["activity"],
                    "时间": f"{session['duration_min']} min",
                    "强度": session["intensity"],
                    "RPE": session["rpe_0_10"],
                    "状态": session["status"],
                }
            )
    return rows


def _feedback_rows(dashboard: dict) -> list[dict]:
    return [
        {
            "周次": str(row["week"]),
            "计划训练": str(row["planned_sessions"]),
            "完成训练": "未填写" if row["completed_sessions"] is None else str(row["completed_sessions"]),
            "完成率": "未填写" if row["completion_rate"] is None else str(row["completion_rate"]),
            "平均 RPE": "未填写" if row["average_rpe"] is None else str(row["average_rpe"]),
            "明显偏难": row["felt_too_hard"],
            "不良事件": row["adverse_event"],
            "调整动作": row["decision_action"],
            "Reason Codes": "、".join(row.get("reason_codes", [])),
            "Flags": "、".join(row.get("flags", [])) if row.get("flags") else "无",
            "依据": row["decision_rationale"],
        }
        for row in dashboard.get("weekly_feedback", [])
    ]


def _plan_actual_rows(items: list[dict]) -> list[dict]:
    rows = []
    for item in items:
        rows.append(
            {
                "动作": item["action_label"],
                "Reason Codes": "、".join(item["reason_codes"]),
                "触发因素": "；".join(zh(code) for code in item["reason_codes"]),
                "Flags": "、".join(item["flags"]) if item["flags"] else "无",
                "完成率": str(item["completion_rate"]) if item["completion_rate"] is not None else "未填写",
                "平均 RPE": str(item["average_rpe"]) if item["average_rpe"] is not None else "未填写",
            }
        )
    return rows


def _walkthrough_rows(walkthrough: dict) -> list[dict]:
    return [
        {
            "Step": item["step"],
            "页面": item["page"],
            "任务": item["title"],
            "状态": item["status"],
            "为什么": item["why"],
        }
        for item in walkthrough["steps"]
    ]


def _runbook_rows(runbook: dict) -> list[dict]:
    return [
        {
            "页面": item["page"],
            "看点": item["talking_point"],
            "状态": item["status"],
        }
        for item in runbook.get("must_show", [])
    ]


def _release_qa_rows(qa: dict) -> list[dict]:
    return [
        {
            "检查": item["label"],
            "状态": item["status"],
            "说明": item["detail"],
        }
        for item in qa["checks"]
    ]


def _runtime_doctor_rows(report: dict) -> list[dict]:
    return [
        {
            "检查": item["label"],
            "状态": item["status"],
            "说明": item["detail"],
        }
        for item in report["checks"]
    ]


def _input_ledger_rows(ledger: dict) -> list[dict]:
    return [
        {
            "输入": item["label"],
            "字段": item["field_id"],
            "状态": item["status"],
            "值": item["value"],
            "来源": item["source_type"],
            "影响输出": "是" if item["affects_output"] else "否",
            "用于": "、".join(item["used_by"]) if item["used_by"] else "不使用",
        }
        for item in ledger["rows"]
    ]


def _terminology_rows(guide: dict) -> list[dict]:
    return [
        {
            "术语": item["display"],
            "中文解释": item["zh_explanation"],
            "用于": item["use_in_ui"],
            "不能说": item["do_not_say"],
        }
        for item in guide["terms"]
    ]


def _terminology_rule_rows(guide: dict) -> list[dict]:
    return [
        {
            "规则": index,
            "说明": rule,
        }
        for index, rule in enumerate(guide["preferred_language_rules"], start=1)
    ]


def _terminology_blocked_rows(guide: dict) -> list[dict]:
    return [
        {
            "Blocked phrase": item["phrase"],
            "原因": item["reason"],
        }
        for item in guide["blocked_language"]
    ]


def _demo_experience_sequence_rows(console: dict) -> list[dict]:
    return [
        {
            "Step": item["step"],
            "动作": item["label"],
            "页面": item["page"],
            "目的": item["purpose"],
        }
        for item in console["guided_sequence"]
    ]


def _guided_review_step_rows(console: dict) -> list[dict]:
    return [
        {
            "Step": item["step"],
            "页面": item["page"],
            "任务": item["title"],
            "状态": zh(item["status"]),
            "为什么": item["why"],
        }
        for item in console["review_steps"]
    ]


def _artifact_catalog_rows(catalog: dict) -> list[dict]:
    return [
        {
            "Category": item["category"],
            "File": item["filename"],
            "Use": item["when_to_use"],
            "Purpose": item["purpose"],
        }
        for item in catalog["items"]
    ]


def _page_health_rows(matrix: dict) -> list[dict]:
    return [
        {
            "页面": row["page"],
            "Lane": row["lane"],
            "状态": zh(row["status"]),
            "核心问题": row["primary_question"],
            "成功信号": row["success_signal"],
            "证据": row["primary_evidence"],
            "不能声称": row["blocked_claim"],
        }
        for row in matrix["rows"]
    ]


def _review_pack_integrity_rows(integrity: dict) -> list[dict]:
    return [
        {
            "文件": item["filename"],
            "内容": item["label"],
            "大小": item["byte_size"],
            "SHA-256": item["sha256"],
        }
        for item in integrity["files"]
    ]


def _evidence_library_rows(sources: list[dict]) -> list[dict]:
    return [
        {
            "Evidence ID": item["id"],
            "Topic": item["topic"],
            "Tier": item["evidence_tier"],
            "Source": item["source"],
            "Product use": item["product_use"],
            "Limits": item["limits"],
            "Saved in": item["saved_in"],
        }
        for item in sources
    ]


def _session_quality_rows(review: dict) -> list[dict]:
    return [
        {
            "Gate": item["label"],
            "Status": zh(item["status"]),
            "Detail": zh(item["detail"]),
            "Action": zh(item["action"]),
        }
        for item in review["gates"]
    ]


def _protocol_deviation_component_rows(review: dict) -> list[dict]:
    return [
        {
            "日期": item["session_date"],
            "测试": item["test"],
            "状态": zh(item["status"]),
            "Flags": ", ".join(item["flags"]) if item["flags"] else "none",
            "单位": item["value_unit"],
            "RPE": "未记录" if item["rpe_0_10"] is None else str(item["rpe_0_10"]),
            "器械": ", ".join(item["equipment"]),
            "替代": item["substitution"] or "",
        }
        for item in review["component_reviews"]
    ]


def _protocol_deviation_retest_rows(review: dict) -> list[dict]:
    return [
        {
            "测试": item["test"],
            "状态": zh(item["status"]),
            "第一次": item["baseline_date"],
            "最近": item["latest_date"],
            "变化": ", ".join(item["changes"]) if item["changes"] else "none",
            "第一次器械": ", ".join(item["baseline_equipment"]),
            "最近器械": ", ".join(item["latest_equipment"]),
        }
        for item in review["retest_reviews"]
    ]


def _retest_interpretation_rows(guard: dict) -> list[dict]:
    return [
        {
            "测试": item["test"],
            "解释状态": zh(item["interpretation_status"]),
            "第一次": item["first_date"],
            "最近": item["latest_date"],
            "变化": item["delta"],
            "单位": item["value_unit"],
            "方向": "有改善" if item["direction"] == "improved" else "未改善/不明确",
            "Protocol context": zh(item["context_status"]),
            "Context changes": ", ".join(item["context_changes"]) if item["context_changes"] else "none",
        }
        for item in guard["items"]
    ]


def _validation_phase_rows(matrix: dict) -> list[dict]:
    return [
        {
            "Phase": phase["label"],
            "Status": zh(phase["status"]),
            "Target": phase["target_sample"],
            "Allowed claim after completion": phase["allowed_claim"],
            "Evidence gap": phase["evidence_gap"],
        }
        for phase in matrix["phases"]
    ]


def _validation_capture_rows(matrix: dict) -> list[dict]:
    return [
        {
            "Check": item["label"],
            "Status": "pass" if item["passed"] else "needs_review",
            "Detail": item["detail"],
        }
        for item in matrix["capture_checks"]
    ]


def _self_use_week_rows(protocol: dict) -> list[dict]:
    return [
        {
            "Week": item["week"],
            "Focus": item["label"],
            "Goal": item["goal"],
            "Required actions": "；".join(item["required_actions"]),
            "Outputs": "、".join(item["outputs"]),
        }
        for item in protocol["weekly_schedule"]
    ]


def _self_use_field_rows(protocol: dict) -> list[dict]:
    return [
        {
            "Field": item["field"],
            "Required": "yes" if item["required"] else "no",
            "Why": item["why"],
        }
        for item in protocol["minimum_data_fields"]
    ]


def _artifact_catalog_cards(catalog: dict) -> None:
    html = []
    for group in catalog["categories"]:
        html.append(
            (
                '<div class="rx-artifact-group">'
                '<div class="rx-artifact-heading">'
                f'<div class="rx-artifact-title">{escape(group["category"])}</div>'
                f'<div class="rx-artifact-count">{group["artifact_count"]} files</div>'
                "</div>"
                '<div class="rx-artifact-grid">'
            )
        )
        for item in group["items"]:
            html.append(
                (
                    '<div class="rx-artifact-card">'
                    '<div class="rx-artifact-top">'
                    f'<div class="rx-artifact-file">{escape(item["filename"])}</div>'
                    f'<div class="rx-artifact-use">{escape(item["when_to_use"])}</div>'
                    "</div>"
                    f'<div class="rx-artifact-purpose">{escape(item["purpose"])}</div>'
                    f'<div class="rx-artifact-mime">{escape(item["mime"])}</div>'
                    "</div>"
                )
            )
        html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _evidence_file_status() -> dict[str, bool]:
    return {path: (ROOT / path).exists() for path in REQUIRED_EVIDENCE_FILES}


def _retest_rows(dashboard: dict) -> list[dict]:
    return [
        {
            "测试": item["test"],
            "第一次日期": item["first_date"],
            "最近日期": item["latest_date"],
            "第一次": item["first_value"],
            "最近一次": item["latest_value"],
            "单位": item["value_unit"],
            "变化": item["delta"],
            "方向": "有改善" if item["direction"] == "improved" else "未改善/不明确",
        }
        for item in dashboard.get("retest_comparisons", [])
    ]


def _set_page(page: str) -> None:
    st.session_state.page = page


def _dashboard_section(title: str, copy: str) -> None:
    st.markdown(
        (
            '<div class="rx-section">'
            f'<div class="rx-section-title">{title}</div>'
            f'<div class="rx-section-copy">{copy}</div>'
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def _language_edition_sidebar() -> None:
    contract = build_language_edition_contract(_language_id())
    current = contract["current_edition"]
    st.sidebar.caption(_t("language_policy_caption"))
    with st.sidebar.expander(_t("language_policy_title"), expanded=False):
        st.caption(contract["claim_boundary"])
        st.write(f"**{current['label']}**")
        st.write(current["description"])
        st.write(current["copy_rule"])
        st.caption(" / ".join(contract["allowed_shared_terms"]))
        st.download_button(
            "下载语言版本契约" if _language_id() != "en_user" else "Download Language Contract",
            language_edition_markdown(contract),
            file_name="sportrx_language_edition_contract.md",
            mime="text/markdown",
            width="stretch",
        )


def _mobile_nav() -> None:
    is_en = _is_english_edition()
    nav_items = [
        ("Workbench", "Home" if is_en else "首页"),
        ("Benchmark Protocol", "Test" if is_en else "测试"),
        ("Training Profile", "Profile" if is_en else "画像"),
        ("训练", "Plan" if is_en else "训练"),
        ("复测", "Retest" if is_en else "复测"),
    ]
    if not _public_preview_enabled():
        nav_items.insert(1, ("Venue Entry", "Entry" if is_en else "确认"))
    flow_copy = (
        "查看示例 Benchmark、训练画像与复测。"
        if _public_preview_enabled()
        else "先完成测试前确认，再测试，再看训练画像。"
    )
    st.markdown(
        (
            '<div class="rx-mobile-nav">'
            f'<div class="rx-mobile-nav-title">{"Mobile trial flow" if is_en else "手机试用入口"}</div>'
            f'<div class="rx-mobile-nav-copy">{flow_copy}'
            "</div></div>"
        ),
        unsafe_allow_html=True,
    )
    cols = st.columns(len(nav_items), gap="small")
    for col, (target, label) in zip(cols, nav_items):
        with col:
            active = st.session_state.page == target
            st.button(
                label,
                type="primary" if active else "secondary",
                width="stretch",
                on_click=_set_page,
                args=(target,),
                key=f"mobile_nav_{target}",
            )


def _public_status_strip() -> None:
    passport = st.session_state.passport
    summary = summarize_benchmark_sessions(st.session_state.benchmark_sessions)
    venue_eligible = _public_venue_entry_eligible()
    safety = passport["safety_gate"]["status"] if venue_eligible else "待完成测试前确认"
    measured_count = int(passport["areas_assessed"]["assessed"])
    next_action = "先完成测试前确认" if not venue_eligible else ("先完成测试" if measured_count < 2 else "查看训练画像")
    html = [
        '<div class="rx-public-home">',
        '<div class="rx-public-card">',
        '<div class="rx-public-kicker">当前状态</div>',
        f'<div class="rx-public-value">{escape(next_action)}</div>',
        '<div class="rx-public-copy">SportRx 只根据已经填写或已经测试的数据给出下一步。没有测试的数据不会被系统猜出来。</div>',
        "</div>",
        '<div class="rx-strip">',
        '<div class="rx-strip-item"><div class="rx-strip-label">Safety Gate</div>'
        f'<div class="rx-strip-value">{escape(safety)}</div></div>',
        '<div class="rx-strip-item"><div class="rx-strip-label">已测维度</div>'
        f'<div class="rx-strip-value">{measured_count} / 5</div></div>',
        '<div class="rx-strip-item"><div class="rx-strip-label">Benchmark 记录</div>'
        f'<div class="rx-strip-value">{int(summary["session_count"])} 次</div></div>',
        '<div class="rx-strip-item"><div class="rx-strip-label">训练计划</div>'
        f'<div class="rx-strip-value">{escape("可生成" if passport["starter_path"]["available"] else "等待测试")}</div></div>',
        "</div>",
        "</div>",
    ]
    st.markdown("".join(html), unsafe_allow_html=True)


def public_home_page() -> None:
    passport = st.session_state.passport
    summary = summarize_benchmark_sessions(st.session_state.benchmark_sessions)
    measured_count = int(passport["areas_assessed"]["assessed"])
    starter_available = bool(passport["starter_path"]["available"])

    _page_header(
        "SportRx",
        "运动测试与训练画像",
        "先记录真实情况，再完成基础测试。SportRx 不猜测缺失数据，也不把安全筛查混进表现判断。",
    )
    if _public_preview_enabled():
        st.info(
            "这是公开示例站，只使用合成数据演示测量、训练画像与复测逻辑。请勿输入姓名、联系方式、健康信息或真实测试成绩。"
        )
        st.button("用合成示例数据体验完整流程", type="primary", width="stretch", on_click=_load_public_sample)
        if not st.session_state.get("public_demo_mode"):
            st.markdown(
                """
                <div class="rx-public-card rx-public-card-ready">
                  <div class="rx-public-kicker">你会看到什么</div>
                  <div class="rx-public-title">Benchmark → 训练画像 → 复测</div>
                  <div class="rx-public-copy">从一组虚拟测试记录开始，查看系统如何保留 Not tested、识别已测表现，并在复测时只比较一致条件下的记录。</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            return
    if not (_public_preview_enabled() and not st.session_state.get("public_demo_mode")):
        _public_status_strip()

    venue_screening = st.session_state.profile.get("venue_screening")
    venue_eligible = bool(st.session_state.get("public_demo_mode")) or (
        isinstance(venue_screening, dict)
        and passport["safety_gate"].get("route") == "eligible_for_benchmark"
    )
    if not venue_eligible:
        next_title = "下一步：完成测试前确认"
        next_copy = "先通过已配置的外部筛查路径确认能否进入 Benchmark。SportRX 不收集筛查题目或健康细节。"
        button_target = "Venue Entry"
        button_label = "开始测试前确认"
    elif measured_count < 2:
        next_title = "下一步：完成基础测试"
        next_copy = "至少完成两个测试维度后，SportRx 才会比较相对优势和主要短板。"
        button_target = "Benchmark Protocol"
        button_label = "开始测试"
    elif not starter_available:
        next_title = "下一步：查看训练画像"
        next_copy = "已经有一些测试信息，但训练交接还需要确认测量门控。"
        button_target = "Training Profile"
        button_label = "查看画像"
    else:
        next_title = "下一步：查看训练安排"
        next_copy = "训练安排只作为保守起步方案，后续需要用 RPE 和复测继续调整。"
        button_target = "训练"
        button_label = "查看训练"

    st.markdown(
        (
            '<div class="rx-public-card rx-public-card-ready">'
            '<div class="rx-public-kicker">下一步</div>'
            f'<div class="rx-public-title">{escape(next_title)}</div>'
            f'<div class="rx-public-copy">{escape(next_copy)}</div>'
            "</div>"
        ),
        unsafe_allow_html=True,
    )
    st.button(button_label, type="primary", width="stretch", on_click=_set_page, args=(button_target,))

    cards = [
        (
            "测试前确认",
            "只确认你是否可以开始 Benchmark，不保存筛查题目或健康细节。",
            "Venue Entry",
        ),
        (
            "测试",
            "按 SportRx Hybrid Benchmark v1 完成标准或低器械路径，记录原始结果。",
            "Benchmark Protocol",
        ),
        (
            "训练画像",
            "查看已经知道什么、还不知道什么，以及是否可以进入保守训练安排。",
            "Training Profile",
        ),
    ]
    html = ['<div class="rx-public-home">']
    for title, copy, _target in cards:
        html.append(
            (
                '<div class="rx-public-card">'
                f'<div class="rx-public-title">{escape(title)}</div>'
                f'<div class="rx-public-copy">{escape(copy)}</div>'
                "</div>"
            )
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)

    if summary["session_count"] == 0:
        st.caption("还没有 Benchmark 记录。没有记录的测试会显示为 Not tested。")
    else:
        st.caption(f"已经保存 {summary['session_count']} 次 Benchmark 记录。")


def _public_venue_entry_eligible() -> bool:
    profile = st.session_state.profile
    safety = st.session_state.passport.get("safety_gate", {})
    return bool(st.session_state.get("public_demo_mode")) or (
        isinstance(profile.get("venue_screening"), dict)
        and safety.get("route") == "eligible_for_benchmark"
    )


def venue_entry_page() -> None:
    """Render a member-owned external-screening handoff without health details."""

    is_en = _is_english_edition()
    copy = (
        {
            "title": "Venue Entry",
            "subtitle": "Complete the approved external screening path first. SportRX records only the routing result, then decides whether Benchmark can begin.",
            "age": "Age",
            "consent": "I understand this local result is not medical clearance and I agree to use this routing step.",
            "provider": "External screening pathway",
            "outcome": "My reported outcome from the external pathway",
            "changed": "Since completing that pathway, has there been a relevant health-status change?",
            "submit": "Check my route",
            "saved": "Local routing result updated.",
            "demo": "This pathway is not approved for venue deployment. The page is an internal/demo workflow only; it cannot open Benchmark.",
            "continue": "Continue to Benchmark",
            "export": "Download local routing result",
            "boundary": "SportRX does not copy, translate, score, or store answers from the external screening tool. It does not provide medical clearance, diagnosis, or exercise advice here.",
        }
        if is_en
        else {
            "title": "测试前确认",
            "subtitle": "先完成已配置的外部筛查路径。SportRX 只记录是否可开始测试的结果，再判断能否进入 Benchmark。",
            "age": "年龄",
            "consent": "我理解本地结果不构成医疗许可，并同意使用此测试前确认步骤。",
            "provider": "外部筛查路径",
            "outcome": "我在外部筛查路径中的自报结果",
            "changed": "完成该路径后，是否出现需要重新确认的健康状态变化？",
            "submit": "查看我是否可开始测试",
            "saved": "已更新本地测试前确认结果。",
            "demo": "该路径尚未获准用于场馆部署。当前仅为内部 / 演示流程，不能开启 Benchmark。",
            "continue": "进入 Benchmark",
            "export": "下载本地确认结果",
            "boundary": "SportRX 不复制、翻译、评分或保存外部筛查工具的答案。本页不提供医疗许可、诊断或运动建议。",
        }
    )
    _page_header("SportRX", copy["title"], copy["subtitle"])
    profile = st.session_state.profile
    current = profile.get("venue_screening") if isinstance(profile.get("venue_screening"), dict) else {}
    providers = load_screening_providers(ROOT)
    provider_by_id = {item["id"]: item for item in providers}
    provider_ids = list(provider_by_id)
    if not provider_ids:
        st.error("No screening-provider registry is available." if is_en else "未找到筛查路径登记表。")
        return

    outcome_labels = (
        {
            "not_completed": "Not completed",
            "completed_continue": "Completed: continue permitted by the external pathway",
            "follow_up_needed": "Follow-up requested by the external pathway",
        }
        if is_en
        else {
            "not_completed": "尚未完成外部筛查",
            "completed_continue": "外部路径提示可继续参加",
            "follow_up_needed": "外部路径提示需要进一步跟进",
        }
    )
    default_provider = current.get("provider_id") if current.get("provider_id") in provider_by_id else provider_ids[0]
    with st.form("venue_entry_form"):
        age = st.number_input(copy["age"], 16, 100, int(profile.get("age", 30)))
        provider_id = st.selectbox(
            copy["provider"],
            provider_ids,
            index=provider_ids.index(default_provider),
            format_func=lambda item: (
                "Chinese venue screening pathway (pending local review)"
                if is_en and item == "CN-VENUE-SCREENING-PENDING"
                else provider_by_id[item]["label"]
            ),
        )
        consent = st.checkbox(copy["consent"], value=current.get("consent") is True)
        outcome = st.selectbox(
            copy["outcome"],
            list(outcome_labels),
            index=list(outcome_labels).index(current.get("member_reported_outcome", "not_completed")),
            format_func=lambda item: outcome_labels[item],
        )
        changed = st.checkbox(copy["changed"], value=current.get("health_changed_since_screening") is True)
        submitted = st.form_submit_button(copy["submit"], type="primary", width="stretch")

    if submitted:
        selected = provider_by_id[provider_id]
        st.session_state.profile.update(
            {
                "age": int(age),
                "venue_screening": {
                    "provider_id": provider_id,
                    "provider_version": selected["version"],
                    "consent": bool(consent),
                    "member_reported_outcome": outcome,
                    "health_changed_since_screening": bool(changed),
                },
            }
        )
        _refresh_outputs()
        profile = st.session_state.profile
        st.success(copy["saved"])

    assessment = build_venue_entry_assessment(profile, root=ROOT) if isinstance(profile.get("venue_screening"), dict) else None
    if assessment is None:
        st.info("Complete the form to see the local route." if is_en else "完成表单后可查看本地确认结果。")
        return

    if assessment["deployment_status"] != "venue_ready":
        st.warning(copy["demo"])
    titles = {
        "eligible_for_benchmark": "Benchmark entry available" if is_en else "可继续进入 Benchmark",
        "screening_follow_up_needed": "Screening completion or follow-up needed" if is_en else "需要完成筛查或进一步确认",
        "stop_automation": "Stop the SportRX automated flow" if is_en else "停止 SportRX 自动流程",
    }
    next_actions = {
        "eligible_for_benchmark": "Enter SportRX Hybrid Benchmark and complete at least two measured dimensions." if is_en else "进入 SportRX Hybrid Benchmark，先完成至少两个测试维度。",
        "screening_follow_up_needed": "Do not enter Benchmark or training. Complete the next step required by the external pathway." if is_en else "暂不进入 Benchmark 或训练路径；请按外部筛查路径的建议完成下一步。",
        "stop_automation": "Do not continue with SportRX Benchmark or training. Seek appropriate professional support." if is_en else "不要继续使用 SportRX 的 Benchmark 或训练功能；请寻求适当的专业支持。",
    }
    st.markdown(
        (
            '<div class="rx-public-card rx-public-card-waiting">'
            f'<div class="rx-public-kicker">{"Current route" if is_en else "当前分流"}</div>'
            f'<div class="rx-public-title">{escape(titles[assessment["route"]])}</div>'
            f'<div class="rx-public-copy">{escape(next_actions[assessment["route"]])}</div>'
            "</div>"
        ),
        unsafe_allow_html=True,
    )
    st.caption(copy["boundary"])
    if assessment.get("provider_member_message") and not is_en:
        st.caption(assessment["provider_member_message"])
    st.download_button(
        copy["export"],
        json.dumps(assessment["member_export"], ensure_ascii=False, indent=2),
        file_name="sportrx_venue_entry_result.json",
        mime="application/json",
        width="stretch",
    )
    if assessment["benchmark_allowed"]:
        st.button(copy["continue"], type="primary", width="stretch", on_click=_set_page, args=("Benchmark Protocol",))


def public_quick_match_page() -> None:
    _page_header(
        "SportRx",
        "快速了解当前训练情况",
        "这里先记录过去 4 周的训练行为。它不是体能测试，也不会生成能力分。",
    )
    profile = st.session_state.profile
    with st.form("public_quick_match_form"):
        age = st.number_input("年龄", 18, 100, int(profile.get("age", 35)))
        training_days = st.number_input("过去 4 周：平均每周训练几天", 0, 7, int(profile.get("training_days", 3)))
        weekly_minutes = st.number_input("过去 4 周：平均每周训练总分钟", 0, 900, int(profile.get("weekly_training_minutes", 120)), step=10)
        running_minutes = st.number_input("过去 4 周：每周跑步或快走分钟", 0, 600, int(profile.get("running_minutes_per_week", 60)), step=10)
        longest_run = st.number_input("最长一次连续跑步或快走分钟", 0, 180, int(profile.get("longest_continuous_run_minutes", 20)), step=5)
        strength_days = st.number_input("平均每周力量训练天数", 0, 7, int(profile.get("strength_days_per_week", 1)))
        available_days = st.number_input("接下来每周能训练几天", 1, 7, int(profile.get("available_days_per_week", 3)))
        max_minutes = st.number_input("每次最多训练多少分钟", 10, 180, int(profile.get("max_minutes_per_session", 45)), step=5)
        submitted = st.form_submit_button("保存并查看结果", type="primary", width="stretch")

    if submitted:
        st.session_state.profile.update(
            {
                "age": int(age),
                "training_days": int(training_days),
                "exercise_days_last_4w": int(training_days),
                "weekly_training_minutes": int(weekly_minutes),
                "mvpa_minutes_per_week": int(weekly_minutes),
                "running_minutes_per_week": int(running_minutes),
                "longest_continuous_run_minutes": int(longest_run),
                "strength_days_per_week": int(strength_days),
                "available_days_per_week": int(available_days),
                "max_minutes_per_session": int(max_minutes),
            }
        )
        _refresh_outputs()
        st.success("已保存。")

    result = quick_match(st.session_state.profile)
    match = result["top_matches"][0] if result["top_matches"] else None
    if match:
        st.markdown(
            (
                '<div class="rx-public-card rx-public-card-ready">'
                '<div class="rx-public-kicker">当前粗筛结果</div>'
                f'<div class="rx-public-title">{escape(zh(match["event_profile"]))}</div>'
                f'<div class="rx-public-value">{escape(zh(match["fit_category"]))}</div>'
                '<div class="rx-public-copy">这个结果只来自自报训练行为。真正表现判断需要完成 Benchmark 测试。</div>'
                "</div>"
            ),
            unsafe_allow_html=True,
        )
        html = ['<div class="rx-public-list">']
        for item in match["why_it_fits"][:4]:
            html.append(f'<div class="rx-public-list-item">{escape(zh_reason(item))}</div>')
        html.append("</div>")
        st.markdown("".join(html), unsafe_allow_html=True)
    st.button("下一步：开始测试", type="primary", width="stretch", on_click=_set_page, args=("Benchmark Protocol",))
    st.caption("缺失测试保持 Not tested；SportRx 不用平均值或默认值补齐。")


def public_benchmark_page() -> None:
    _page_header(
        "SportRx",
        "Benchmark 流程预览" if _public_preview_enabled() else "完成基础测试",
        "公开示例站只展示合成测试记录，不引导你进行实际测试。" if _public_preview_enabled() else "选择你能使用的器械，然后按同一套流程记录结果。至少完成两个维度后，再查看训练画像。",
    )
    if not _public_venue_entry_eligible():
        st.warning("请先完成测试前确认。未确认可进入 Benchmark 时，SportRX 不会开启测试。" if not _is_english_edition() else "Complete Venue Entry first. SportRX does not open Benchmark until eligibility is explicitly confirmed.")
        st.button("去测试前确认" if not _is_english_edition() else "Open Venue Entry", type="primary", width="stretch", on_click=_set_page, args=("Venue Entry",))
        return
    profile = st.session_state.profile
    equipment_access = list(profile.get("equipment_access", []))
    if _public_preview_enabled():
        st.warning("当前为合成示例数据。请勿把本页作为现场测试指引，也不要输入真实测试成绩。")
    else:
        equipment_access = st.multiselect(
            "今天能使用的器械",
            ["row", "ski", "sled", "kettlebell", "dumbbell", "track"],
            default=equipment_access,
        )
        if equipment_access != profile.get("equipment_access", []):
            st.session_state.profile["equipment_access"] = equipment_access
            _refresh_outputs()
    protocol = get_benchmark_protocol(equipment_access)
    st.markdown(
        (
            '<div class="rx-public-card">'
            '<div class="rx-public-kicker">测试路径</div>'
            f'<div class="rx-public-title">{escape(protocol["label"])}</div>'
            f'<div class="rx-public-copy">版本：{escape(protocol["version"])}。复测时尽量保持同一路线、器械、负重和顺序。</div>'
            "</div>"
        ),
        unsafe_allow_html=True,
    )
    with st.expander("测试前安全说明", expanded=not _public_preview_enabled()):
        st.write("在真实测试前，需要完成外部筛查路径并确认 Benchmark 资格。")
        st.write("测试前先进行 8-12 分钟轻松活动和短促练习；测试中任何异常都应停止。")
        for rule in protocol["global_stop_rules"]:
            st.write(f"- {zh(rule)}")
    html = ['<div class="rx-public-home">']
    for component in protocol["component_protocols"][:5]:
        required = "可选" if component["optional"] else "建议完成"
        html.append(
            (
                '<div class="rx-public-card">'
                f'<div class="rx-public-kicker">{escape(zh(component["area"]))} · {required}</div>'
                f'<div class="rx-public-title">{escape(component["test"])}</div>'
                f'<div class="rx-public-copy">{escape(zh(component["purpose"]))}</div>'
                "</div>"
            )
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)
    st.button("查看合成训练画像" if _public_preview_enabled() else "测完后查看训练画像", type="primary", width="stretch", on_click=_set_page, args=("Training Profile",))
    st.caption(_t("public_measurement_scope_caption"))


def public_profile_page() -> None:
    passport = st.session_state.passport
    _page_header(
        "SportRx",
        "当前训练画像",
        "这里只总结已经知道的信息和还缺的测试。它不是综合评分，也不是运动能力标签。",
    )
    if not _public_venue_entry_eligible():
        st.warning("当前只能查看测试前确认结果，不能进入训练画像或 Starter Path。" if not _is_english_edition() else "This route is assessment-only. Training Profile and Starter Path are unavailable.")
        st.button("返回测试前确认" if not _is_english_edition() else "Return to Venue Entry", type="primary", width="stretch", on_click=_set_page, args=("Venue Entry",))
        return
    _public_status_strip()
    st.markdown(
        (
            '<div class="rx-public-card">'
            '<div class="rx-public-kicker">我们现在知道</div>'
            f'<div class="rx-public-title">{escape(zh(passport["current_measured_picture"]))}</div>'
            '<div class="rx-public-list">'
            + "".join(f'<div class="rx-public-list-item">{escape(zh(item))}</div>' for item in passport["what_we_know"][:5])
            + "</div></div>"
        ),
        unsafe_allow_html=True,
    )
    st.markdown(
        (
            '<div class="rx-public-card rx-public-card-waiting">'
            '<div class="rx-public-kicker">还不知道</div>'
            '<div class="rx-public-list">'
            + "".join(f'<div class="rx-public-list-item">{escape(zh(item))}</div>' for item in passport["what_we_do_not_know"][:5])
            + "</div></div>"
        ),
        unsafe_allow_html=True,
    )
    if passport["starter_path"]["available"]:
        st.button("查看训练安排", type="primary", width="stretch", on_click=_set_page, args=("训练",))
    else:
        st.button("返回测试", type="primary", width="stretch", on_click=_set_page, args=("Benchmark Protocol",))


def _module_grid(modules: list[tuple[str, str, str]]) -> None:
    html = ['<div class="rx-module-grid">']
    for kicker, title, copy in modules:
        html.append(
            (
                '<div class="rx-module">'
                f'<div class="rx-module-kicker">{kicker}</div>'
                f'<div class="rx-module-title">{title}</div>'
                f'<div class="rx-module-copy">{copy}</div>'
                "</div>"
            )
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _pipeline_status() -> None:
    passport = st.session_state.passport
    summary = summarize_benchmark_sessions(st.session_state.benchmark_sessions)
    path = passport["starter_path"]
    steps = [
        ("Step 01", "Quick Match", "已建立训练行为粗筛"),
        ("Step 02", "HYROX Check", passport["areas_assessed"]["label"]),
        ("Step 03", "Protocol", "standard / low-equipment"),
        ("Step 04", "Benchmark Log", f"{summary['session_count']} sessions"),
        ("Step 05", "Starter Path", "可生成" if path["available"] else "等待实测"),
    ]
    html = ['<div class="rx-pipeline">']
    for kicker, label, value in steps:
        html.append(
            (
                '<div class="rx-pipeline-step">'
                f'<div class="rx-pipeline-label">{kicker} · {label}</div>'
                f'<div class="rx-pipeline-value">{value}</div>'
                "</div>"
            )
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def workbench_page() -> None:
    _page_header(
        "SportRx Labs",
        "运动表现测试工作台",
        "先建立当前 measured picture，再用同一 protocol 记录 Benchmark，最后才生成保守的 Starter Path。",
    )

    passport = st.session_state.passport
    summary = summarize_benchmark_sessions(st.session_state.benchmark_sessions)
    feedback_dashboard = build_feedback_dashboard(
        st.session_state.plan,
        st.session_state.feedback_by_week,
        st.session_state.benchmark_sessions,
    )
    walkthrough = build_walkthrough(passport, summary, feedback_dashboard)
    output_prerequisites = build_output_prerequisites(passport, summary, feedback_dashboard)
    open_source_console = build_open_source_integration_console()
    launch = build_launch_readiness(
        st.session_state.profile,
        passport,
        st.session_state.plan,
        st.session_state.benchmark_sessions,
        st.session_state.feedback_by_week,
        _evidence_file_status(),
        str(ROOT),
    )
    runbook = build_demo_runbook(launch)
    command_center = build_launch_command_center(launch, runbook)
    timeline = build_measurement_timeline(walkthrough)
    demo_scenarios = build_demo_scenarios()
    scenario_matrix = build_demo_scenario_matrix()
    first_run = build_first_run_guide(
        passport,
        st.session_state.benchmark_sessions,
        st.session_state.feedback_by_week,
        st.session_state.pilot_feedback_entries,
    )
    terminology = build_terminology_guide()
    session_quality = build_session_quality_review(
        st.session_state.profile,
        passport,
        st.session_state.plan,
        st.session_state.benchmark_sessions,
        st.session_state.feedback_by_week,
        _evidence_file_status(),
        ROOT,
    )
    reviewer_session_plan = build_reviewer_session_plan(first_run, scenario_matrix, runbook)
    page_health = build_page_health_matrix(walkthrough)
    demo_experience = build_demo_experience_console(
        first_run,
        launch,
        session_quality,
        terminology,
        open_source_console,
    )
    guided_review = build_guided_review_console(walkthrough, first_run, launch, scenario_matrix)
    _hero_status_console(passport, summary, first_run)
    _workbench_launch_selector(first_run)
    _demo_experience_console(demo_experience)
    with st.expander("Demo Experience：前 5 分钟应该怎么体验？", expanded=False):
        st.caption(demo_experience["claim_boundary"])
        st.dataframe(_demo_experience_sequence_rows(demo_experience), hide_index=True, width="stretch")
        col_a, col_b = st.columns(2)
        with col_a:
            st.write("Trust anchors")
            for item in demo_experience["trust_anchors"]:
                st.write(f"- {item}")
        with col_b:
            st.write("Blocked impressions")
            for item in demo_experience["blocked_impressions"]:
                st.write(f"- {item}")
        st.download_button(
            "下载 Demo Experience Console",
            demo_experience_markdown(demo_experience),
            file_name="sportrx_demo_experience_console.md",
            mime="text/markdown",
            width="stretch",
        )
    _guided_review_console(guided_review)
    _guided_action_rail(guided_review)
    with st.expander("Guided Review：按什么顺序试？", expanded=False):
        st.caption(guided_review["claim_boundary"])
        st.dataframe(_guided_review_step_rows(guided_review), hide_index=True, width="stretch")
        action_cols = st.columns(len(guided_review["quick_actions"]))
        for col, action in zip(action_cols, guided_review["quick_actions"]):
            with col:
                if action["id"] == "load_complete_loop":
                    st.button(
                        action["label"],
                        width="stretch",
                        type="primary",
                        on_click=_load_demo_state,
                        key=f"guided_action_{action['id']}",
                    )
                else:
                    st.button(
                        action["label"],
                        width="stretch",
                        on_click=_set_page,
                        args=(action["target"],),
                        key=f"guided_action_{action['id']}",
                    )
        st.download_button(
            "下载 Guided Review Console",
            guided_review_markdown(guided_review),
            file_name="sportrx_guided_review_console.md",
            mime="text/markdown",
            width="stretch",
        )
    _lab_workflow_board(passport, summary, feedback_dashboard, first_run)
    with st.expander("Page Health Matrix：每个页面应该证明什么？", expanded=False):
        st.caption(page_health["claim_boundary"])
        _metric_row(
            [
                ("Pages", page_health["page_count"]),
                ("Complete", page_health["complete_pages"]),
                ("Waiting", page_health["waiting_pages"]),
                ("Release Pages", page_health["release_page_count"]),
            ]
        )
        st.dataframe(_page_health_rows(page_health), hide_index=True, width="stretch")
        st.download_button(
            "下载 Page Health Matrix",
            page_health_matrix_markdown(page_health),
            file_name="sportrx_page_health_matrix.md",
            mime="text/markdown",
            width="stretch",
        )
    with st.expander("First Run Guide：查看路线细节", expanded=False):
        st.caption(first_run["claim_boundary"])
        _trial_mode_launcher(first_run)
        st.download_button(
            "下载 First Run Guide",
            first_run_guide_markdown(first_run),
            file_name="sportrx_first_run_guide.md",
            mime="text/markdown",
            width="stretch",
        )
    with st.expander("Terminology Guide：哪些英文术语保留？", expanded=False):
        st.caption(terminology["claim_boundary"])
        _metric_row(
            [
                ("Terms", terminology["term_count"]),
                ("Rules", terminology["rule_count"]),
                ("Blocked", terminology["blocked_phrase_count"]),
                ("Status", zh(terminology["status"])),
            ]
        )
        st.dataframe(_terminology_rows(terminology), hide_index=True, width="stretch")
        st.write("Preferred language rules")
        st.dataframe(_terminology_rule_rows(terminology), hide_index=True, width="stretch")
        st.write("Blocked language")
        st.dataframe(_terminology_blocked_rows(terminology), hide_index=True, width="stretch")
        st.download_button(
            "下载 Terminology Guide",
            terminology_markdown(terminology),
            file_name="sportrx_terminology_guide.md",
            mime="text/markdown",
            width="stretch",
        )
    st.subheader("Session Quality Review")
    _session_quality_console(session_quality)
    with st.expander("查看全局质量门控", expanded=False):
        st.dataframe(_session_quality_rows(session_quality), hide_index=True, width="stretch")
    st.download_button(
        "下载 Session Quality Review",
        session_quality_review_markdown(session_quality),
        file_name="sportrx_session_quality_review.md",
        mime="text/markdown",
        width="stretch",
    )
    st.subheader("Reviewer Session Plan")
    _reviewer_session_plan_console(reviewer_session_plan)
    st.dataframe(
        [
            {
                "路线": track["label"],
                "时长": f"{track['duration_min']} min",
                "场景": track["scenario_id"],
                "适合": track["best_for"],
                "页面顺序": " -> ".join(track["page_sequence"]),
                "交付物": ", ".join(track["artifacts"][:3]),
            }
            for track in reviewer_session_plan["tracks"]
        ],
        hide_index=True,
        width="stretch",
    )
    st.download_button(
        "下载 Reviewer Session Plan",
        reviewer_session_plan_markdown(reviewer_session_plan),
        file_name="sportrx_reviewer_session_plan.md",
        mime="text/markdown",
        width="stretch",
    )
    st.subheader("Launch Command Center")
    st.caption(command_center["claim_boundary"])
    _command_center(command_center)
    st.subheader("Open-Source Integration Console")
    _open_source_integration_console(open_source_console)
    st.download_button(
        "下载 Open-Source Integration Notes",
        open_source_integration_markdown(open_source_console),
        file_name="sportrx_open_source_integration.md",
        mime="text/markdown",
        width="stretch",
    )
    input_ledger = build_input_ledger(st.session_state.profile)
    with st.expander("Input Ledger：SportRx 为什么要问这些？", expanded=False):
        st.caption(input_ledger["claim_boundary"])
        _metric_row(
            [
                ("Active Inputs", input_ledger["summary"]["active_inputs"]),
                ("Measured Tests", input_ledger["summary"]["measured_tests_recorded"]),
                ("Not Tested", input_ledger["summary"]["not_tested"]),
                ("Legacy/Ignored", input_ledger["summary"]["legacy_or_ignored"]),
            ]
        )
        st.dataframe(_input_ledger_rows(input_ledger), hide_index=True, width="stretch")
        st.download_button(
            "下载 Input Ledger",
            input_ledger_markdown(input_ledger),
            file_name="sportrx_input_ledger.md",
            mime="text/markdown",
            width="stretch",
        )

    left, right = st.columns([1.25, 0.75])
    with left:
        st.subheader("Measurement Loop Timeline")
        st.caption(timeline["claim_boundary"])
        _measurement_timeline(timeline)
        st.download_button(
            "下载 Measurement Timeline",
            measurement_timeline_markdown(timeline),
            file_name="sportrx_measurement_timeline.md",
            mime="text/markdown",
        )
        st.subheader("Product Tour")
        st.table(_walkthrough_rows(walkthrough))
        _module_grid(
            [
                (
                    "Screen",
                    "Quick Match",
                    "用过去 4 周真实训练行为做粗筛，不用主观“适应度”滑杆。",
                ),
                (
                    "Lab",
                    "HYROX Check",
                    "只接收已测或确定知道的数据；缺失项目保持 Not tested。",
                ),
                (
                    "Protocol",
                    "Hybrid Benchmark v1",
                    "固定测试路径、器械、顺序、stop rules 和记录字段。",
                ),
            ]
        )

        st.subheader("当前判断边界")
        st.table(
            [
                {"项目": "Safety Gate", "当前": passport["safety_gate"]["status"], "边界": "可以阻断训练交接，不参与表现评分"},
                {"项目": "Strongest Area", "当前": zh(passport["strongest_area"]), "边界": "至少两个实测维度后才比较"},
                {"项目": "Main Gap", "当前": zh(passport["main_gap"]), "边界": "数据不足时不生成针对性 Starter Path"},
                {"项目": "Retest", "当前": summary["message"], "边界": "只比较个人前后变化，不做预测"},
            ]
        )
        st.subheader("Output Prerequisites")
        st.caption(output_prerequisites["claim_boundary"])
        st.table(_output_prerequisite_rows(output_prerequisites))

    with right:
        st.subheader("Demo Scenario Library")
        st.caption(demo_scenarios[0]["claim_boundary"])
        _demo_scenario_matrix_console(scenario_matrix)
        st.dataframe(
            [
                {
                    "场景": row["label"],
                    "状态": zh(row["product_state"]),
                    "实测维度": row["measured_area_count"],
                    "Benchmark Logs": row["benchmark_sessions"],
                    "Feedback Weeks": row["feedback_weeks"],
                    "Starter Path": "可用" if row["starter_path_available"] else "等待",
                    "Retest": "已就绪" if row["retest_ready"] else "等待",
                    "推荐页面": " -> ".join(row["recommended_pages"]),
                }
                for row in scenario_matrix["rows"]
            ],
            hide_index=True,
            width="stretch",
        )
        st.download_button(
            "下载 Demo Scenario Matrix",
            demo_scenario_matrix_markdown(scenario_matrix),
            file_name="sportrx_demo_scenario_matrix.md",
            mime="text/markdown",
            width="stretch",
        )
        _scenario_switcher(scenario_matrix, st.session_state.demo_scenario_id)
        if st.session_state.demo_scenario_id != "custom":
            st.caption(f"当前场景：{zh(st.session_state.demo_scenario_id)}")

        _dashboard_section(
            "下一步建议",
            "如果你只是想先体验，先做 Quick Match；如果你想让结果更真实，直接进入 Benchmark Protocol，按 protocol 完成至少两个组件后再记录。",
        )
        col1, col2 = st.columns(2)
        col1.button("加载完整示例", width="stretch", type="primary", on_click=_load_demo_state)
        col2.button("重置原型", width="stretch", on_click=_reset_prototype_state)
        if st.session_state.demo_claim_boundary:
            st.caption(st.session_state.demo_claim_boundary)

        st.subheader("Reviewer Runbook")
        st.caption(runbook["opening_line"])
        st.table(_runbook_rows(runbook))

        st.subheader("Tour Shortcut")
        next_step = walkthrough["next_step"]
        st.write(f"下一步：{next_step['title']}")
        st.button(f"进入 {next_step['page']}", width="stretch", on_click=_set_page, args=(next_step["page"],))

        col1, col2 = st.columns(2)
        col1.button("Quick Match", width="stretch", on_click=_set_page, args=("Quick Match",))
        col2.button("Benchmark Protocol", width="stretch", on_click=_set_page, args=("Benchmark Protocol",))
        col1, col2 = st.columns(2)
        col1.button("HYROX Check", width="stretch", on_click=_set_page, args=("HYROX Check",))
        col2.button("Benchmark Log", width="stretch", on_click=_set_page, args=("Benchmark Log",))

        st.subheader("What SportRx will not claim")
        st.write("- 不显示 fake percentile。")
        st.write("- 不做完赛时间预测。")
        st.write("- 不给 injury-risk 百分比。")
        st.write("- 不把 Safety Gate 混进表现分。")

def discover_page() -> None:
    _page_header(
        "Quick Match",
        "过去 4 周训练行为粗筛",
        "只记录近期训练天数、分钟数、连续跑/快走时间和最近 4 周训练次数。真正的表现判断要进 HYROX Check 和 Benchmark Log。",
    )

    profile = st.session_state.profile
    with st.form("quick_match_form"):
        st.markdown("**Participant scope**")
        st.caption("年龄用于成人范围和 Safety Gate 语境，不会让 Quick Match 匹配度变高或变低。")
        col1, col2, col3 = st.columns(3)
        age = col1.number_input("年龄", 18, 100, int(profile.get("age", 35)), help="直接填写年龄；只用于成人范围和 Safety Gate 语境。")
        goals = ["first finish", "improve performance", "understand profile", "build health"]
        primary_goal = col2.selectbox(
            "主要目标",
            goals,
            format_func=zh,
            index=goals.index(profile.get("primary_goal", "first finish")),
            help="目标只影响路线解释，不是表现分。",
        )
        available_days = col3.number_input(
            "未来每周可训练天数",
            1,
            7,
            int(profile.get("available_days_per_week", 3)),
            help="用于后续训练安排约束，不代表能力更强。",
        )

        st.markdown("**Past 4 weeks: self-reported behavior**")
        st.caption("这里全部是过去 4 周的直接数字。没有 1 km / 5 km 成绩；实测表现请去 HYROX Check 或 Benchmark Log。")
        col1, col2, col3 = st.columns(3)
        training_days = col1.number_input(
            "过去 4 周平均每周训练天数",
            0,
            7,
            int(profile.get("training_days", 3)),
            help="自报行为字段，用于粗略路线匹配。",
        )
        weekly_minutes = col2.number_input(
            "过去 4 周平均每周训练总分钟",
            0,
            600,
            int(profile.get("weekly_training_minutes", 120)),
            step=15,
            help="自报训练量，不是实测表现。",
        )
        running_minutes = col1.number_input(
            "每周跑步/快走分钟",
            0,
            600,
            int(profile.get("running_minutes_per_week", 60)),
            step=10,
            help="自报跑走暴露；不是 1 km 或 5 km 测试。",
        )
        longest_run = col2.number_input(
            "最长一次连续跑/快走分钟",
            0,
            180,
            int(profile.get("longest_continuous_run_minutes", 20)),
            step=5,
            help="自报最长连续时间，用于判断是否需要先做 Benchmark。",
        )
        strength_days = col3.number_input(
            "每周力量训练天数",
            0,
            7,
            int(profile.get("strength_days_per_week", 1)),
            help="自报力量训练频率，不是力量测试。",
        )

        col1, col2, col3 = st.columns(3)
        hiit_sessions = col1.number_input(
            "过去 4 周高强度训练次数",
            0,
            40,
            int(profile.get("high_intensity_sessions_last_4w", 2)),
            help="自报暴露次数，不做风险预测。",
        )
        loaded_sessions = col2.number_input(
            "过去 4 周负重动作训练次数",
            0,
            40,
            int(profile.get("loaded_movement_sessions_last_4w", 2)),
            help="例如 carry、sled-like work 或相似 station demand。",
        )
        max_minutes = col3.number_input(
            "每次最多训练分钟",
            10,
            150,
            int(profile.get("max_minutes_per_session", 45)),
            step=5,
            help="后续处方上限，不是适应度评分。",
        )
        submitted = st.form_submit_button("查看当前匹配", type="primary")

    if submitted:
        st.session_state.profile.update(
            {
                "age": int(age),
                "training_days": int(training_days),
                "weekly_training_minutes": int(weekly_minutes),
                "exercise_days_last_4w": int(training_days),
                "mvpa_minutes_per_week": int(weekly_minutes),
                "running_minutes_per_week": int(running_minutes),
                "longest_continuous_run_minutes": int(longest_run),
                "strength_days_per_week": int(strength_days),
                "high_intensity_sessions_last_4w": int(hiit_sessions),
                "loaded_movement_sessions_last_4w": int(loaded_sessions),
                "available_days_per_week": int(available_days),
                "max_minutes_per_session": int(max_minutes),
                "primary_goal": primary_goal,
            }
        )
        for legacy_key in [
            "endurance_background",
            "resistance_background",
            "running_comfort",
            "hiit_comfort",
            "loaded_movement_comfort",
        ]:
            st.session_state.profile.pop(legacy_key, None)
        _refresh_outputs()
        st.success("当前匹配已更新。")

    result = st.session_state.quick_match_result
    if (
        "input_review" not in result
        or "intake_quality" not in result
        or "intake_contract" not in result
        or "lab_intake_sheet" not in result
    ):
        _refresh_outputs()
        result = st.session_state.quick_match_result
    _status_badge(result["safety_gate"]["status"])
    precision_audit = build_intake_precision_audit(st.session_state.profile)
    _metric_row(
        [
            ("Training Profile", result["athlete_profile_label"]),
            ("Strongest Area", result["strongest_capability"]),
            ("Main Gap", result["obvious_limiter"]),
        ]
    )
    _quick_match_lab_intake_sheet_console(result["lab_intake_sheet"])
    with st.expander("Quick Match Lab Intake Sheet", expanded=True):
        st.caption(result["lab_intake_sheet"]["claim_boundary"])
        st.dataframe(_quick_match_lab_intake_rows(result["lab_intake_sheet"]), hide_index=True, width="stretch")
        st.download_button(
            "下载 Quick Match Lab Intake Sheet",
            quick_match_lab_intake_sheet_markdown(result["lab_intake_sheet"]),
            file_name="sportrx_quick_match_lab_intake_sheet.md",
            mime="text/markdown",
            width="stretch",
        )
    _quick_match_contract_console(result["intake_contract"])
    _quick_match_intake_console(result["intake_quality"])
    _intake_precision_console(precision_audit)
    _quick_match_input_console(result["input_review"])
    with st.expander("Quick Match Intake Contract", expanded=False):
        st.caption(result["intake_contract"]["claim_boundary"])
        st.dataframe(
            [
                {
                    "分组": group["label"],
                    "收集": f"{group['collected']} / {group['total']}",
                    "用途": zh(group["purpose"]),
                    "输出边界": zh(group["expected_output"]),
                    "状态": zh(group["status"]),
                }
                for group in result["intake_contract"]["groups"]
            ],
            hide_index=True,
            width="stretch",
        )
        st.download_button(
            "下载 Quick Match Intake Contract",
            quick_match_intake_contract_markdown(result["intake_contract"]),
            file_name="sportrx_quick_match_intake_contract.md",
            mime="text/markdown",
            width="stretch",
        )
    with st.expander("Intake Precision Audit", expanded=True):
        st.dataframe(_intake_precision_rows(precision_audit), hide_index=True, width="stretch")
        st.download_button(
            "下载 Intake Precision Audit",
            intake_precision_markdown(precision_audit),
            file_name="sportrx_intake_precision_audit.md",
            mime="text/markdown",
            width="stretch",
        )
    with st.expander("Quick Match Input Ledger", expanded=False):
        st.dataframe(
            [
                {
                    "字段": zh(field["label"]),
                    "当前值": zh(field["value"]),
                    "单位": zh(field["unit"]),
                    "状态": zh(field["status"]),
                    "影响输出": zh(field["affects"]),
                    "边界": zh(field["role"]),
                }
                for field in result["input_review"]["fields"]
            ],
            hide_index=True,
            width="stretch",
        )

    st.subheader("Current Route Matches")
    _quick_match_match_cards(result)
    rows = [
        {
            "项目": zh(item["event_profile"]),
            "状态": zh(item["pack_status"]),
            "当前匹配": zh(item["fit_category"]),
            "为什么": "；".join(_quick_match_reason_label(reason) for reason in item["why_it_fits"]) or "还需要更多信息",
            "缺什么": "；".join(_quick_match_reason_label(reason) for reason in item["what_is_missing"]) or "快速匹配未发现明显缺口",
            "下一步": zh(item["cta"]),
        }
        for item in result["top_matches"]
    ]
    with st.expander("查看结构化路线粗筛表", expanded=False):
        st.dataframe(rows, hide_index=True, width="stretch")

    with st.expander("分享卡片"):
        _card_table(build_sport_match_card(result))


def lab_page() -> None:
    _page_header(
        "Performance Lab",
        "HYROX Check",
        "只填你测过或确定知道的数据。没有做过的测试就留空，SportRx 不会用平均值补齐。",
    )

    profile = st.session_state.profile
    benchmark_summary = summarize_benchmark_sessions(st.session_state.benchmark_sessions)
    lab_console = build_lab_readiness_console(profile, st.session_state.passport, benchmark_summary)
    protocol_source_guide = build_protocol_source_guide(profile)
    st.subheader("Lab Readiness Console")
    st.caption(lab_console["claim_boundary"])
    _lab_console(lab_console)
    st.info(lab_console["next_action"])
    _protocol_source_guide_console(protocol_source_guide)
    with st.expander("Protocol Source Guide：哪些来源可以用？", expanded=False):
        st.caption(protocol_source_guide["claim_boundary"])
        st.dataframe(_protocol_source_rows(protocol_source_guide), hide_index=True, width="stretch")
        st.download_button(
            "下载 Protocol Source Guide",
            protocol_source_guide_markdown(protocol_source_guide),
            file_name="sportrx_protocol_source_guide.md",
            mime="text/markdown",
            width="stretch",
        )
    if st.session_state.benchmark_sessions:
        import_result = benchmark_profile_patch(st.session_state.benchmark_sessions)
        with st.expander("从 Benchmark Log 导入实测数据", expanded=bool(import_result["profile_patch"])):
            if import_result["profile_patch"]:
                st.caption(import_result["claim_boundary"])
                st.write("可导入字段：")
                st.json(import_result["profile_patch"])
                if import_result["applied"]:
                    st.write("导入映射：")
                    for item in import_result["applied"]:
                        st.caption(f"- {item}")
                if st.button("应用到 HYROX Check", type="primary"):
                    st.session_state.profile.update(import_result["profile_patch"])
                    _refresh_outputs()
                    st.success("已从 Benchmark Log 更新 HYROX Check。")
            else:
                st.info("当前 Benchmark Log 还没有能直接导入 HYROX Check 的单位兼容数据。")
            if import_result["skipped"]:
                st.caption("保留为原始记录，暂不转换：")
                for item in import_result["skipped"]:
                    st.caption(f"- {item}")

    with st.form("hybrid_lab_form"):
        col1, col2 = st.columns(2)
        age = col1.number_input("年龄", 18, 100, int(profile.get("age", 35)))
        max_minutes = col2.number_input("每次可训练分钟", 10, 150, int(profile.get("max_minutes_per_session", 45)), step=5)

        col1, col2, col3 = st.columns(3)
        training_days = col1.number_input("每周训练天数", 0, 7, int(profile.get("training_days", 3)))
        weekly_minutes = col2.number_input("每周训练分钟", 0, 600, int(profile.get("weekly_training_minutes", 120)), step=15)
        running_minutes = col3.number_input("每周跑步分钟", 0, 600, int(profile.get("running_minutes_per_week", 60)), step=10)

        col1, col2, col3 = st.columns(3)
        strength_days = col1.number_input("每周力量训练天数", 0, 7, int(profile.get("strength_days_per_week", 1)))
        available_days = col2.number_input("每周可训练天数", 1, 7, int(profile.get("available_days_per_week", 3)))
        goals = ["first finish", "improve performance", "understand profile"]
        selected_goal = profile.get("primary_goal", "first finish")
        goal = col3.selectbox(
            "目标",
            goals,
            format_func=zh,
            index=goals.index(selected_goal) if selected_goal in goals else 0,
        )

        st.subheader("Measured Tests")
        st.caption("先选择每个项目的测试状态。只有 Measured / 已实测 才会要求填写数值；Not tested 会保存为空值。")
        col1, col2, col3 = st.columns(3)
        one_km_run_tested, one_km_run = _measured_number_input(
            col1,
            profile,
            "one_km_run_seconds",
            "1 km run",
            60,
            1200,
            330,
            "seconds",
        )
        five_km_run_tested, five_km_run = _measured_number_input(
            col2,
            profile,
            "five_km_run_seconds",
            "5 km run",
            600,
            7200,
            1800,
            "seconds",
            step=10,
        )
        row_tested, one_km_row = _measured_number_input(
            col3,
            profile,
            "one_km_row_seconds",
            "1 km RowErg",
            60,
            1200,
            300,
            "seconds",
        )

        col1, col2, col3 = st.columns(3)
        ski_tested, one_km_ski = _measured_number_input(
            col1,
            profile,
            "one_km_ski_seconds",
            "1 km SkiErg",
            60,
            1200,
            330,
            "seconds",
        )
        station_tested, station_score = _measured_number_input(
            col2,
            profile,
            "station_test_score",
            "Station circuit protocol score",
            1,
            100,
            60,
            "protocol-derived score",
        )
        work_capacity_tested, work_capacity_score = _measured_number_input(
            col3,
            profile,
            "work_capacity_test_score",
            "Work capacity protocol score",
            1,
            100,
            60,
            "protocol-derived score",
        )
        col1, col2 = st.columns(2)
        station_current_protocol = str(profile.get("station_test_protocol", "") or "").strip()
        station_protocol_choice = col1.selectbox(
            "Station circuit protocol source",
            PROTOCOL_SOURCE_OPTIONS,
            index=PROTOCOL_SOURCE_OPTIONS.index(_protocol_source_choice(station_current_protocol)),
            format_func=lambda item: "请选择 protocol source" if item == "" else item,
            disabled=not station_tested,
            help=PROTOCOL_SOURCE_HELP[_protocol_source_choice(station_current_protocol)],
        )
        station_protocol_note = col1.text_input(
            "Station source note",
            value=station_current_protocol if station_protocol_choice == "Other documented protocol" else "",
            disabled=not station_tested or station_protocol_choice != "Other documented protocol",
            placeholder="写明 protocol 名称、版本、负重、轮次或 Benchmark Log 日期",
        )
        work_current_protocol = str(profile.get("work_capacity_test_protocol", "") or "").strip()
        work_capacity_protocol_choice = col2.selectbox(
            "Work capacity protocol source",
            PROTOCOL_SOURCE_OPTIONS,
            index=PROTOCOL_SOURCE_OPTIONS.index(_protocol_source_choice(work_current_protocol)),
            format_func=lambda item: "请选择 protocol source" if item == "" else item,
            disabled=not work_capacity_tested,
            help=PROTOCOL_SOURCE_HELP[_protocol_source_choice(work_current_protocol)],
        )
        work_capacity_protocol_note = col2.text_input(
            "Work capacity source note",
            value=work_current_protocol if work_capacity_protocol_choice == "Other documented protocol" else "",
            disabled=not work_capacity_tested or work_capacity_protocol_choice != "Other documented protocol",
            placeholder="写明 protocol 名称、版本、顺序、负荷或 Benchmark Log 日期",
        )
        station_protocol = _protocol_source_value(station_protocol_choice, station_protocol_note)
        work_capacity_protocol = _protocol_source_value(work_capacity_protocol_choice, work_capacity_protocol_note)
        if station_tested and not station_protocol.strip():
            st.warning("Station circuit protocol score 需要 protocol source；否则会记录为 measured_needs_protocol，但不会进入 measured performance。")
        if work_capacity_tested and not work_capacity_protocol.strip():
            st.warning("Work capacity protocol score 需要 protocol source；否则会记录为 measured_needs_protocol，但不会进入 measured performance。")
        equipment_access = st.multiselect(
            "可用器械",
            ["row", "ski", "sled", "kettlebell", "dumbbell", "track"],
            default=profile.get("equipment_access", []),
        )

        st.subheader("安全筛查")
        symptoms = st.multiselect(
            "相关症状",
            list(SYMPTOM_LABELS.keys()),
            default=profile.get("symptoms", []),
            format_func=lambda key: SYMPTOM_LABELS[key],
        )
        conditions = st.multiselect(
            "已知健康情况",
            list(CONDITION_LABELS.keys()),
            default=profile.get("known_conditions", []),
            format_func=lambda key: CONDITION_LABELS[key],
        )
        recent_major_injury = st.checkbox("近期较严重伤病", value=bool(profile.get("recent_major_injury", False)))
        submitted = st.form_submit_button("更新 HYROX Check", type="primary")

    if submitted:
        st.session_state.profile.update(
            {
                "age": int(age),
                "training_days": int(training_days),
                "exercise_days_last_4w": int(training_days),
                "weekly_training_minutes": int(weekly_minutes),
                "mvpa_minutes_per_week": int(weekly_minutes),
                "running_minutes_per_week": int(running_minutes),
                "strength_days_per_week": int(strength_days),
                "available_days_per_week": int(available_days),
                "max_minutes_per_session": int(max_minutes),
                "primary_goal": goal,
                "one_km_run_seconds": int(one_km_run) if one_km_run_tested else None,
                "five_km_run_seconds": int(five_km_run) if five_km_run_tested else None,
                "one_km_row_seconds": int(one_km_row) if row_tested else None,
                "one_km_ski_seconds": int(one_km_ski) if ski_tested else None,
                "station_test_score": int(station_score) if station_tested else None,
                "work_capacity_test_score": int(work_capacity_score) if work_capacity_tested else None,
                "station_test_protocol": station_protocol.strip() if station_tested else "",
                "work_capacity_test_protocol": work_capacity_protocol.strip() if work_capacity_tested else "",
                "equipment_access": equipment_access,
                "symptoms": symptoms,
                "known_conditions": conditions,
                "recent_major_injury": bool(recent_major_injury),
            }
        )
        _refresh_outputs()
        st.success("HYROX Check 已更新。")

    result = st.session_state.lab_result
    if "measurement_review" not in result or "lab_test_quality" not in result:
        _refresh_outputs()
        result = st.session_state.lab_result
    _status_badge(result["safety_gate"]["status"])
    _metric_row(
        [
            ("已测试区域", result["areas_assessed"]["label"]),
            ("Measured Picture", result["current_measured_picture"]),
            ("Training Profile", result["training_profile"]),
        ]
    )
    _measurement_intake_matrix_console(result["measurement_intake_matrix"])
    st.subheader("Lab Component Board")
    _lab_component_board(result["measurement_intake_matrix"])
    with st.expander("查看 Measurement Intake Matrix 表格", expanded=False):
        st.dataframe(_measurement_intake_rows(result["measurement_intake_matrix"]), hide_index=True, width="stretch")
    col1, col2 = st.columns(2)
    col1.download_button(
        "下载 Measurement Intake Matrix Markdown",
        measurement_intake_matrix_markdown(result["measurement_intake_matrix"]),
        file_name="sportrx_measurement_intake_matrix.md",
        mime="text/markdown",
        width="stretch",
    )
    col2.download_button(
        "下载 Measurement Intake Matrix CSV",
        measurement_intake_matrix_csv(result["measurement_intake_matrix"]),
        file_name="sportrx_measurement_intake_matrix.csv",
        mime="text/csv",
        width="stretch",
    )
    _lab_measurement_review(result["measurement_review"])
    _lab_test_quality_console(result["lab_test_quality"])
    with st.expander("HYROX Check Measurement Ledger", expanded=False):
        st.dataframe(
            [
                {
                    "测试": zh(item["label"]),
                    "当前值": zh(item["value"]),
                    "单位": zh(item["unit"]),
                    "维度": zh(item["dimension"]),
                    "状态": zh(item["status"]),
                    "Protocol 来源": zh(item.get("protocol_source", "")),
                    "是否参与短板比较": "是" if item["affects_gap_comparison"] else "否",
                    "边界": zh(item["protocol_role"]),
                }
                for item in result["measurement_review"]["test_fields"]
            ],
            hide_index=True,
            width="stretch",
        )
        st.dataframe(
            [
                {
                    "背景字段": zh(item["label"]),
                    "当前值": zh(item["value"]),
                    "单位": zh(item["unit"]),
                    "状态": zh(item["status"]),
                    "边界": zh(item["role"]),
                }
                for item in result["measurement_review"]["context_fields"]
            ],
            hide_index=True,
            width="stretch",
        )

    st.subheader("你现在的情况")
    _lab_measured_picture_cards(result)
    with st.expander("查看 Performance Matrix 表格", expanded=False):
        st.dataframe(_performance_rows(result["performance_profile"]), hide_index=True, width="stretch")

    with st.expander("Metric Sources：这些结果从哪里来？", expanded=False):
        st.caption(result["metric_sources"]["claim_boundary"])
        st.table(
            _metric_source_rows(result["metric_sources"], "performance_metrics"),
        )

    st.subheader("目前看起来不错的地方")
    if result["strongest_area"] in {"Not enough data", "Not enough measured data"}:
        st.info("目前实测表现维度不足，SportRx 暂不识别 strongest area。先完成至少两个 measured components。")
    else:
        st.write(f"{zh(result['strongest_area'])} 是目前测到的信息里相对发展较好的部分。")

    st.subheader("接下来最需要补的地方")
    if result["main_gap"] == "Not enough data" or result["main_gap"] == "Not enough measured data":
        st.write("目前实测数据还不够，不能可靠地判断主要短板。")
    else:
        st.write(f"{zh(result['main_gap'])} 可能是下一步最值得发展的部分。")

    st.subheader("你的训练条件")
    st.dataframe(_context_rows(result["training_context"]), hide_index=True, width="stretch")

    st.subheader("下一步")
    for item in result["top_3_priorities"]:
        st.write(f"- {item}")

    with st.expander("为什么是这个结果？"):
        st.write("我们知道什么")
        for item in result["what_we_know"]:
            st.write(f"- {item}")
        st.write("我们还不知道什么")
        for item in result["what_we_do_not_know"]:
            st.write(f"- {item}")
        st.write("下一步测什么")
        for item in result["what_to_measure_next"]:
            st.write(f"- {item}")
        st.write("证据状态")
        st.write(result["evidence_status"])


def passport_page() -> None:
    _page_header(
        "Training Profile",
        "SportRx Training Profile Report",
        "一份面向自用、教练沟通和复测准备的当前训练画像报告。这里总结已测信息、未知信息、下一步测试和训练交接边界。",
    )
    passport = st.session_state.passport
    benchmark_summary = summarize_benchmark_sessions(st.session_state.benchmark_sessions)
    feedback_dashboard = build_feedback_dashboard(
        st.session_state.plan,
        st.session_state.feedback_by_week,
        st.session_state.benchmark_sessions,
    )
    report = build_training_profile_report(passport, benchmark_summary, feedback_dashboard)

    _report_dashboard(report)
    _training_profile_handoff_board(report)
    _measured_profile_summary(report)

    overview_tab, performance_tab, sources_tab, gates_tab, evidence_tab, handoff_tab = st.tabs(
        ["Report Overview", "Performance Matrix", "Metric Sources", "Output Gates", "Known / Unknown", "Handoff"]
    )

    with overview_tab:
        left, right = st.columns([1.1, 0.9])
        with left:
            st.subheader("Report Summary")
            with st.expander("查看报告摘要表", expanded=False):
                st.dataframe(_report_summary_rows(report), hide_index=True, width="stretch")
            st.subheader("Interpretation Boundary")
            with st.expander("查看解释边界表", expanded=False):
                st.dataframe(
                    [
                        {"项目": "Strongest Area", "当前": zh(report["strongest_area"]), "边界": "至少两个实测表现维度后才比较"},
                        {"项目": "Main Gap", "当前": zh(report["main_gap"]), "边界": "数据不足时保持 Not enough measured data"},
                        {
                            "项目": "Starter Path",
                            "当前": "available" if report["starter_path_status"]["available"] else "blocked",
                            "边界": zh(report["starter_path_status"].get("reason") or report["starter_path_status"].get("based_on_gap")),
                        },
                    ],
                    hide_index=True,
                    width="stretch",
                )
        with right:
            st.subheader("Next Best Actions")
            for item in report["priorities"]:
                st.write(f"- {item}")
            st.subheader("Retest Anchor")
            st.write(benchmark_summary["message"])
            st.download_button(
                "下载 Training Profile Markdown",
                report_markdown(report),
                file_name="sportrx_training_profile_report.md",
                mime="text/markdown",
            )

    with performance_tab:
        st.subheader("Performance Matrix")
        _profile_dimension_cards(report)
        with st.expander("查看详细 Performance Matrix", expanded=False):
            st.dataframe(_report_performance_rows(report), hide_index=True, width="stretch")
        st.subheader("Training Context")
        with st.expander("查看训练条件记录", expanded=False):
            st.dataframe(_context_rows(passport["training_context"]), hide_index=True, width="stretch")

    with sources_tab:
        sources = report["metric_sources"]
        st.subheader("Metric Source Register")
        st.caption(sources.get("claim_boundary", "Metric source labels document provenance only."))
        summary = sources.get("summary", {})
        _metric_row(
            [
                ("Total Metrics", summary.get("total_metrics", 0)),
                ("Measured Performance", summary.get("measured_performance_metrics", 0)),
                ("Not Tested", summary.get("not_tested_metrics", 0)),
                ("Ignored Inputs", summary.get("unsupported_inputs", 0)),
            ]
        )
        st.table(_metric_source_rows(sources))
        if sources.get("unsupported_inputs"):
            st.warning("这些输入目前不会影响任何 SportRx 输出，正式界面应避免主动收集。")

    with gates_tab:
        gates = report["output_prerequisites"]
        st.subheader("Output Prerequisites")
        st.caption(gates.get("claim_boundary", "Output prerequisites explain product gates only."))
        summary = gates.get("summary", {})
        _metric_row(
            [
                ("Outputs", summary.get("total_outputs", 0)),
                ("Active", summary.get("active_outputs", 0)),
                ("Blocked", summary.get("blocked_outputs", 0)),
                ("Provisional", summary.get("provisional_outputs", 0)),
            ]
        )
        st.table(_output_prerequisite_rows(gates))

    with evidence_tab:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("What We Know")
            for item in report["known"] or ["暂无已测信息"]:
                st.write(f"- {item}")
        with col2:
            st.subheader("What We Do Not Know")
            for item in report["unknown"] or ["暂无主要未知项"]:
                st.write(f"- {item}")
        with col3:
            st.subheader("Measure Next")
            for item in report["measure_next"] or ["按同一 protocol 完成复测"]:
                st.write(f"- {item}")

    with handoff_tab:
        _status_badge(report["safety_gate"]["status"])
        st.write(passport["rule_evidence_explanation"])
        if report["safety_gate"]["reasons"]:
            st.subheader("Safety Gate Reasons")
            for reason in report["safety_gate"]["reasons"]:
                st.write(f"- {reason}")

        st.subheader("Starter Path Handoff")
        if report["starter_path_status"]["available"]:
            st.success(f"可生成 Starter Path，当前依据：{zh(report['starter_path_status']['based_on_gap'])}")
        else:
            st.warning(zh(report["starter_path_status"]["reason"]))
            benchmark = get_hybrid_benchmark(passport["training_context"].get("equipment_access", []))
            st.write("建议先完成 SportRx Hybrid Benchmark v1：")
            for component in benchmark["spec"]["components"]:
                st.write(f"- {component['test']}")

        st.subheader("External Route")
        st.write(passport["community_route"]["label"])
        st.write(passport["retest_cta"])

        with st.expander("分享卡片"):
            _card_table(build_readiness_passport_card(passport))


def training_page() -> None:
    _page_header(
        "Starter Path",
        "4 周 Training Block",
        "把已测短板、FITT-VP 有氧处方和每周 RPE 反馈合成一个可执行的起步训练 block。",
    )
    if not _is_internal_edition() and not _public_venue_entry_eligible():
        st.warning("当前分流不能进入自动训练内容。请先完成外部筛查路径的下一步。" if not _is_english_edition() else "This route cannot enter automated training content. Complete the required external screening follow-up first.")
        st.button("返回测试前确认" if not _is_english_edition() else "Return to Venue Entry", type="primary", width="stretch", on_click=_set_page, args=("Venue Entry",))
        return
    passport = st.session_state.passport
    block = build_training_block(passport, st.session_state.plan, st.session_state.feedback_by_week)

    if not block["available"]:
        _training_block_console(block)
        st.error(zh(block["reason"]))
        st.caption(block["claim_boundary"])
        st.subheader("为什么暂不生成 Training Block")
        st.write("SportRx 需要至少两个实测表现维度，才会把 Training Profile 交接到针对性 Starter Path。")
        benchmark = get_hybrid_benchmark(passport["training_context"].get("equipment_access", []))
        st.subheader("SportRx Hybrid Benchmark v1")
        st.write(benchmark["spec"]["label"])
        st.write("建议先完成下面至少两个组件，再回到 Training Profile / Starter Path：")
        for component in benchmark["spec"]["components"]:
            st.write(f"- {component['test']}")
        st.download_button(
            "下载 blocked handoff 说明",
            training_block_markdown(block),
            file_name="sportrx_training_block_blocked.md",
            mime="text/markdown",
        )
        return

    _training_block_console(block)
    _training_week_cards(block)
    _metric_row(
        [
            ("Based On Gap", block["based_on_gap"]),
            ("Training Profile", block["training_profile"]),
            ("Safety Gate", block["safety_gate_status"]),
            ("Weeks", len(block["weeks"])),
        ]
    )
    st.caption(block["claim_boundary"])

    overview_tab, weekly_tab, sessions_tab, export_tab = st.tabs(
        ["Block Overview", "Weekly Plan", "Session Detail", "Progression / Export"]
    )

    with overview_tab:
        left, right = st.columns([1.1, 0.9])
        with left:
            st.subheader("4-Week Block")
            st.dataframe(_training_week_rows(block), hide_index=True, width="stretch")
        with right:
            st.subheader("Progression Policy")
            for item in block["progression_policy"]:
                st.write(f"- {item}")
            st.subheader("How To Use")
            st.write("- 每次训练后记录完成情况和 session RPE。")
            st.write("- 每周结束后在 `复测` 页面输入反馈。")
            st.write("- 第 4 周使用同一 Benchmark Protocol 复测一个关键组件。")

    with weekly_tab:
        for week in block["weeks"]:
            with st.expander(f"Week {week['week']} · {week['focus']}", expanded=week["week"] == 1):
                _metric_row(
                    [
                        ("Frequency", week["frequency_per_week"]),
                        ("Duration", f"{week['duration_min']} min"),
                        ("Weekly Volume", f"{week['weekly_minutes']} min"),
                    ]
                )
                st.write(week["starter_instruction"])
                if week["fitt_vp"]:
                    st.dataframe(
                        [
                            {"FITT-VP": key.replace("_", " ").title(), "内容": value}
                            for key, value in week["fitt_vp"].items()
                        ],
                        hide_index=True,
                        width="stretch",
                    )

    with sessions_tab:
        st.subheader("Session Detail")
        st.dataframe(_training_session_rows(block), hide_index=True, width="stretch")
        st.caption("这些 session 来自 SportRx Core FITT-VP，有氧剂量按完成率和 RPE 周度调整。")

    with export_tab:
        st.subheader("Download")
        st.download_button(
            "下载 4 周 Training Block Markdown",
            training_block_markdown(block),
            file_name="sportrx_4_week_training_block.md",
            mime="text/markdown",
        )
        st.subheader("Feedback Loop")
        st.write("完成 Week 1-3 后，到 `复测` 页面填写完成次数、平均 RPE、是否明显偏难或出现不良事件。")
        if st.button("去填写周反馈", type="primary"):
            _set_page("复测")


def _component_unit(component: dict) -> str:
    component_id = component["id"]
    if component_id in {"run_1km", "row_or_ski_1km", "compromised_run"}:
        return "seconds"
    if component_id == "run_1km_or_6min":
        return "meters"
    if "circuit" in component_id or component_id == "transition_practice":
        return "rounds"
    return "raw"


def _quality_review_panel(quality: dict) -> None:
    save_allowed = bool(quality["save_allowed"])
    interpretation_ready = bool(quality["interpretation_ready"])
    cards = [
        (
            "Save Gate",
            "Save allowed" if save_allowed else "Needs review",
            "A raw Benchmark Log needs at least one completed component with a raw value.",
            "rx-quality-card-ready" if save_allowed else "rx-quality-card-blocked",
        ),
        (
            "Completed",
            str(quality["completed_components"]),
            "Completed components with a usable raw value.",
            "rx-quality-card-ready" if quality["completed_components"] else "rx-quality-card-waiting",
        ),
        (
            "Measured Areas",
            str(quality["measured_area_count"]),
            "At least two measured areas are recommended before interpreting gap direction.",
            "rx-quality-card-ready" if quality["measured_area_count"] >= 2 else "rx-quality-card-waiting",
        ),
        (
            "Interpretation",
            "Ready" if interpretation_ready else "Wait",
            "Interpretation readiness is not validation or prediction.",
            "rx-quality-card-ready" if interpretation_ready else "rx-quality-card-waiting",
        ),
        (
            "Review Items",
            f"{len(quality['issues'])} issues / {len(quality['warnings'])} warnings",
            "Issues block saving; warnings preserve uncertainty.",
            "rx-quality-card-ready" if not quality["issues"] else "rx-quality-card-blocked",
        ),
    ]
    html = [
        '<div class="rx-quality-console">',
        '<div class="rx-quality-head">',
        '<div>',
        '<div class="rx-quality-kicker">Session quality review</div>',
        '<div class="rx-quality-title">保存前数据质量检查</div>',
        f'<div class="rx-quality-copy">{escape(quality["claim_boundary"])}</div>',
        "</div>",
        '<div class="rx-quality-status">',
        '<div class="rx-quality-label">Status</div>',
        f'<div class="rx-quality-value">{escape(zh(quality["status"]))}</div>',
        f'<div class="rx-quality-detail">{escape("可以保存为 raw log。" if save_allowed else "至少补齐一个完成组件和原始结果。")}</div>',
        "</div>",
        "</div>",
        '<div class="rx-quality-grid">',
    ]
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-quality-card {class_name}">'
                f'<div class="rx-quality-label">{escape(label)}</div>'
                f'<div class="rx-quality-value">{escape(zh(value))}</div>'
                f'<div class="rx-quality-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)
    if quality["issues"]:
        st.write("需要处理")
        for item in quality["issues"]:
            st.write(f"- {item}")
    if quality["warnings"]:
        st.write("保存后仍需注意")
        for item in quality["warnings"]:
            st.write(f"- {item}")
    st.caption(quality["claim_boundary"])


def _open_source_integration_console(console: dict) -> None:
    html = [
        '<div class="rx-release-console">',
        '<div class="rx-release-head">',
        '<div>',
        '<div class="rx-release-kicker">Open-source integration</div>',
        '<div class="rx-release-title">参考同类项目，但不变成同类产品</div>',
        f'<div class="rx-release-copy">{escape(console["primary_message"])}</div>',
        "</div>",
        '<div class="rx-release-status">',
        '<div class="rx-release-label">Status</div>',
        f'<div class="rx-release-value">{escape(zh(console["status"]))}</div>',
        f'<div class="rx-release-detail">{escape(console["claim_boundary"])}</div>',
        "</div>",
        "</div>",
        '<div class="rx-release-grid">',
    ]
    for card in console["cards"]:
        class_name = "rx-release-card-ready" if card["status"] == "ready" else "rx-release-card-waiting"
        html.append(
            (
                f'<div class="rx-release-card {class_name}">'
                f'<div class="rx-release-label">{escape(card["label"])}</div>'
                f'<div class="rx-release-value">{escape(zh(card["value"]))}</div>'
                f'<div class="rx-release-detail">{escape(zh(card["detail"]))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)

    st.markdown(
        "已吸收的方向："
        + " · ".join(escape(item["lane"]) for item in console["integration_lanes"] if item["status"] == "adopted")
        + "。新增实践参考：REGmon、AthleteLoadMonitor；报告合同参考：Athlete Report Generator。",
        unsafe_allow_html=True,
    )

    adopted = [item for item in console["projects"] if item["status"] == "adopted"]
    later = [item for item in console["projects"] if item["status"] == "later"]
    tab1, tab2, tab3, tab4 = st.tabs(["Integration Map", "Adopted", "Later", "Rejected"])
    with tab1:
        st.dataframe(
            [
                {
                    "整合方向": item["lane"],
                    "参考来源": item["borrow_from"],
                    "SportRx 动作": item["sport_rx_action"],
                    "状态": zh(item["status"]),
                }
                for item in console["integration_lanes"]
            ],
            hide_index=True,
            width="stretch",
        )
    with tab2:
        st.dataframe(
            [
                {
                    "项目": item["project"],
                    "类型": item["category"],
                    "吸收点": item["lesson"],
                    "SportRx 决策": item["decision"],
                    "边界": item["boundary"],
                }
                for item in adopted
            ],
            hide_index=True,
            width="stretch",
        )
    with tab3:
        st.dataframe(
            [
                {
                    "项目": item["project"],
                    "类型": item["category"],
                    "以后再看": item["lesson"],
                    "暂缓原因": item["boundary"],
                }
                for item in later
            ],
            hide_index=True,
            width="stretch",
        )
    with tab4:
        for item in console["rejected_boundaries"]:
            st.write(f"- {item}")
    st.caption(console["next_action"])


def _benchmark_log_entry_contract_panel(contract: dict) -> None:
    cards = [
        (
            "Benchmark path",
            contract["benchmark_path"],
            f"Protocol {contract['protocol_version']}",
            "rx-quality-card-ready",
        ),
        (
            "Components",
            str(len(contract["components"])),
            "Each component has its own raw-result fields and allowed units.",
            "rx-quality-card-ready",
        ),
        (
            "Boundary",
            "Capture only",
            "No score, percentile, race prediction, or medical clearance.",
            "rx-quality-card-waiting",
        ),
    ]
    html = [
        '<div class="rx-quality-console">',
        '<div class="rx-quality-head">',
        '<div>',
        '<div class="rx-quality-kicker">Benchmark Log entry contract</div>',
        '<div class="rx-quality-title">按测试项目记录，不用一个数字假装知道全部</div>',
        f'<div class="rx-quality-copy">{escape(contract["primary_message"])}</div>',
        "</div>",
        '<div class="rx-quality-status">',
        '<div class="rx-quality-label">Claim boundary</div>',
        '<div class="rx-quality-value">Data capture only</div>',
        f'<div class="rx-quality-detail">{escape(contract["claim_boundary"])}</div>',
        "</div>",
        "</div>",
        '<div class="rx-quality-grid">',
    ]
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-quality-card {class_name}">'
                f'<div class="rx-quality-label">{escape(label)}</div>'
                f'<div class="rx-quality-value">{escape(zh(value))}</div>'
                f'<div class="rx-quality-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)
    component_html = ['<div class="rx-entry-grid">']
    for item in contract["components"]:
        units = "".join(
            f'<span class="rx-entry-chip">{escape(unit)}</span>'
            for unit in item["allowed_value_units"]
        )
        companion_fields = item["companion_fields"] or ["None"]
        companions = "".join(
            f'<span class="rx-entry-chip rx-entry-chip-waiting">{escape(field)}</span>'
            for field in companion_fields
        )
        blocked = "<br>".join(escape(rule) for rule in item["not_allowed"])
        component_html.append(
            (
                '<div class="rx-entry-card">'
                '<div class="rx-entry-top">'
                f'<div class="rx-entry-title">{escape(item["test"])}</div>'
                f'<div class="rx-entry-area">{escape(zh(item["area"]))}</div>'
                "</div>"
                f'<div class="rx-entry-row"><strong>Primary result</strong><br>{escape(item["primary_value_field"])} · {escape(item["primary_value_label"])}</div>'
                f'<div class="rx-entry-row"><strong>Allowed units</strong></div><div class="rx-entry-chip-row">{units}</div>'
                f'<div class="rx-entry-row"><strong>Companion fields</strong></div><div class="rx-entry-chip-row">{companions}</div>'
                f'<div class="rx-entry-row"><strong>Import policy</strong><br>{escape(item["import_policy"])}</div>'
                f'<div class="rx-entry-row"><strong>UI hint</strong><br>{escape(item["ui_hint"])}</div>'
                f'<div class="rx-entry-blocked"><strong>Not allowed</strong><br>{blocked}</div>'
                "</div>"
            )
        )
    component_html.append("</div>")
    st.markdown("".join(component_html), unsafe_allow_html=True)


def _benchmark_log_extra_field_input(field: str, component_id: str, completed: bool) -> Any:
    key = f"log_field_{component_id}_{field}"
    if field == "modality":
        value = st.selectbox("Modality", ["", "row", "ski"], key=key)
        return value or None
    if field in {"time_seconds", "distance_meters", "rounds_completed"}:
        label = {
            "time_seconds": "补充时间（秒）",
            "distance_meters": "补充距离（米）",
            "rounds_completed": "补充轮数",
        }[field]
        value = st.number_input(label, min_value=0.0, value=0.0, step=1.0, key=key)
        return float(value) if completed and value > 0 else None
    if field == "loads_used":
        return st.text_input("负重 / loads used", key=key).strip()
    if field == "notes":
        return st.text_input("结构化补充说明", key=key).strip()
    return st.text_input(field, key=key).strip()


def _benchmark_protocol_context_input(field: str, component_id: str) -> Any:
    """Collect only the context needed to keep a later retest honest."""

    key = f"log_context_{component_id}_{field}"
    labels = {
        "test_variant": "测试类型",
        "route_or_treadmill": "路线 / 跑台",
        "surface": "表面",
        "gradient_or_incline": "坡度 / 坡度设置",
        "timing_method": "计时方式",
        "erg_type": "Erg 类型",
        "erg_model": "设备型号",
        "drag_factor": "阻尼 / drag factor",
        "movement_standard": "动作标准",
        "loads_used": "负重",
        "rest_rule": "休息规则",
        "preceding_station_circuit": "前置 station circuit",
    }
    if field == "test_variant":
        return st.selectbox(labels[field], ["", "1km_run", "6min_run", "6min_run_walk"], key=key)
    if field == "surface":
        return st.selectbox(labels[field], ["", "track", "road", "treadmill", "indoor_court", "other"], key=key)
    if field == "timing_method":
        return st.selectbox(labels[field], ["", "manual_timer", "treadmill_console", "erg_monitor"], key=key)
    if field == "erg_type":
        return st.selectbox(labels[field], ["", "row", "ski"], key=key)
    if field == "drag_factor":
        value = st.number_input(labels[field], min_value=0.0, value=0.0, step=1.0, key=key)
        return float(value) if value > 0 else None
    return st.text_input(labels.get(field, field), key=key).strip()


def _benchmark_import_compatibility_panel(compatibility: dict) -> None:
    ready = bool(compatibility["hyrox_import_ready"])
    cards = [
        (
            "HYROX handoff",
            "Ready" if ready else "Not ready",
            compatibility["next_action"],
            "rx-quality-card-ready" if ready else "rx-quality-card-waiting",
        ),
        (
            "Direct imports",
            str(compatibility["direct_import_count"]),
            "Measured fields that match existing HYROX Check inputs.",
            "rx-quality-card-ready" if compatibility["direct_import_count"] else "rx-quality-card-waiting",
        ),
        (
            "Needs detail",
            str(compatibility["needs_detail_count"]),
            "Usually RowErg/SkiErg modality or substitution detail.",
            "rx-quality-card-blocked" if compatibility["needs_detail_count"] else "rx-quality-card-ready",
        ),
        (
            "Raw only",
            str(compatibility["raw_only_count"]),
            "Kept as Benchmark Log data without synthetic conversion.",
            "rx-quality-card-waiting" if compatibility["raw_only_count"] else "rx-quality-card-ready",
        ),
    ]
    html = [
        '<div class="rx-quality-console">',
        '<div class="rx-quality-head">',
        '<div>',
        '<div class="rx-quality-kicker">HYROX import compatibility</div>',
        '<div class="rx-quality-title">保存前导入兼容性检查</div>',
        f'<div class="rx-quality-copy">{escape(compatibility["claim_boundary"])}</div>',
        "</div>",
        '<div class="rx-quality-status">',
        '<div class="rx-quality-label">Status</div>',
        f'<div class="rx-quality-value">{escape(zh(compatibility["status"]))}</div>',
        f'<div class="rx-quality-detail">{escape(zh(compatibility["next_action"]))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-quality-grid">',
    ]
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-quality-card {class_name}">'
                f'<div class="rx-quality-label">{escape(label)}</div>'
                f'<div class="rx-quality-value">{escape(zh(value))}</div>'
                f'<div class="rx-quality-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)

    if compatibility["importable_fields"]:
        st.write("可导入字段")
        for field in compatibility["importable_fields"]:
            st.caption(f"- {field}")
    if compatibility["needs_detail"]:
        st.write("需要补充信息")
        for item in compatibility["needs_detail"]:
            st.caption(f"- {item['component_id']}: {item['reason']}")
    if compatibility["raw_only"]:
        st.write("保留为 raw log")
        for item in compatibility["raw_only"]:
            st.caption(f"- {item['component_id']}: {item['reason']}")
    st.caption(compatibility["claim_boundary"])


def _test_session_operator_console(operator: dict) -> None:
    ready = operator["status"] == "ready_for_test_day"
    cards = [
        (
            "Operator",
            "Ready" if ready else "Blocked",
            operator["next_action"],
            "rx-quality-card-ready" if ready else "rx-quality-card-blocked",
        ),
        (
            "Protocol",
            operator["protocol_version"],
            zh(operator["path"]),
            "rx-quality-card-ready",
        ),
        (
            "Steps",
            str(operator["total_steps"]),
            f"{operator['component_count']} component steps",
            "rx-quality-card-ready",
        ),
        (
            "Components",
            f"{operator['recommended_components']} + {operator['optional_components']}",
            "Recommended + optional measured components.",
            "rx-quality-card-ready",
        ),
    ]
    html = [
        '<div class="rx-quality-console">',
        '<div class="rx-quality-head">',
        '<div>',
        '<div class="rx-quality-kicker">Test session operator</div>',
        '<div class="rx-quality-title">现场测试执行台</div>',
        f'<div class="rx-quality-copy">{escape(operator["claim_boundary"])}</div>',
        "</div>",
        '<div class="rx-quality-status">',
        '<div class="rx-quality-label">Next action</div>',
        f'<div class="rx-quality-value">{escape(zh(operator["status"]))}</div>',
        f'<div class="rx-quality-detail">{escape(zh(operator["next_action"]))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-quality-grid">',
    ]
    for label, value, detail, class_name in cards:
        html.append(
            (
                f'<div class="rx-quality-card {class_name}">'
                f'<div class="rx-quality-label">{escape(label)}</div>'
                f'<div class="rx-quality-value">{escape(zh(value))}</div>'
                f'<div class="rx-quality-detail">{escape(zh(detail))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _test_day_command_board(board: dict) -> None:
    html = [
        '<div class="rx-protocol-console">',
        '<div class="rx-protocol-head">',
        '<div>',
        '<div class="rx-protocol-kicker">Test-Day Command Board</div>',
        '<div class="rx-protocol-title">把 protocol 变成现场测试指挥板</div>',
        f'<div class="rx-protocol-copy">{escape(zh(board["primary_message"]))}</div>',
        "</div>",
        '<div class="rx-protocol-status">',
        '<div class="rx-protocol-label">Next Action</div>',
        f'<div class="rx-protocol-value">{escape(zh(board["status"]))}</div>',
        f'<div class="rx-protocol-detail">{escape(zh(board["next_action"]))}</div>',
        "</div>",
        "</div>",
        '<div class="rx-protocol-grid">',
    ]
    for card in board["cards"]:
        status = card.get("status", "waiting")
        if status == "blocked":
            class_name = "rx-protocol-card-blocked"
        elif status == "ready":
            class_name = "rx-protocol-card-ready"
        else:
            class_name = "rx-protocol-card-waiting"
        html.append(
            (
                f'<div class="rx-protocol-card {class_name}">'
                f'<div class="rx-protocol-label">{escape(zh(card["label"]))}</div>'
                f'<div class="rx-protocol-value">{escape(zh(card["value"]))}</div>'
                f'<div class="rx-protocol-detail">{escape(zh(card["detail"]))}</div>'
                "</div>"
            )
        )
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)
    phase_rows = [
        {
            "阶段": zh(phase["phase"]),
            "动作": zh(phase["action"]),
            "记录": zh(phase["record"]),
        }
        for phase in board["phases"]
    ]
    st.dataframe(phase_rows, hide_index=True, width="stretch")
    st.download_button(
        "下载 Test-Day Command Board",
        test_day_command_board_markdown(board),
        file_name="sportrx_test_day_command_board.md",
        mime="text/markdown",
        width="stretch",
    )


def _operator_flow_board(operator: dict) -> None:
    steps = operator["preflight_steps"] + [
        {
            "order": 4,
            "label": "Component Tests",
            "status": "required",
            "instruction": f"Complete {operator['recommended_components']} recommended component(s); optional components stay Not tested if skipped.",
            "record": "Raw result, unit, RPE, equipment, substitution, notes.",
        },
    ] + operator["after_steps"]
    html = ['<div class="rx-operator-flow">']
    for display_order, step in enumerate(steps[:6], start=1):
        status = str(step.get("status", "ready"))
        if status == "blocked":
            class_name = "rx-operator-step-blocked"
        elif status == "required":
            class_name = "rx-operator-step-required"
        else:
            class_name = "rx-operator-step-ready"
        html.append(
            (
                f'<div class="rx-operator-step {class_name}">'
                f'<div class="rx-operator-kicker">Step {escape(str(display_order))} · {escape(zh(status))}</div>'
                f'<div class="rx-operator-title">{escape(zh(step["label"]))}</div>'
                f'<div class="rx-operator-copy">{escape(zh(step["instruction"]))}</div>'
                f'<div class="rx-operator-copy"><strong>Record</strong><br>{escape(zh(step["record"]))}</div>'
                "</div>"
            )
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def _operator_component_cards(operator: dict) -> None:
    html = ['<div class="rx-operator-components">']
    for step in operator["component_steps"]:
        status_class = "rx-operator-component-optional" if step["optional"] else "rx-operator-component-recommended"
        record_items = "".join(
            f'<div class="rx-operator-list-item">{escape(zh(item))}</div>'
            for item in step["record_now"]
        )
        stop_items = "".join(
            f'<div class="rx-operator-list-item rx-operator-list-item-stop">{escape(zh(item))}</div>'
            for item in step["stop_if"][:2]
        )
        html.append(
            (
                f'<div class="rx-operator-component {status_class}">'
                '<div class="rx-operator-head">'
                "<div>"
                f'<div class="rx-operator-kicker">{escape(zh(step["area"]))}</div>'
                f'<div class="rx-operator-title">{escape(step["label"])}</div>'
                "</div>"
                f'<div class="rx-operator-pill">{escape(zh(step["status"]))}</div>'
                "</div>"
                f'<div class="rx-operator-copy">{escape(zh(step["purpose"]))}</div>'
                f'<div class="rx-operator-copy"><strong>Unit</strong><br>{escape(zh(step["unit_hint"]))}</div>'
                '<div class="rx-operator-kicker">Record now</div>'
                f'<div class="rx-operator-list">{record_items}</div>'
                '<div class="rx-operator-kicker">Stop if</div>'
                f'<div class="rx-operator-list">{stop_items}</div>'
                f'<div class="rx-operator-copy">{escape(zh(step["benchmark_log_handoff"]))}</div>'
                "</div>"
            )
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def benchmark_protocol_page() -> None:
    _page_header(
        "Benchmark Protocol",
        "SportRx Hybrid Benchmark v1",
        "先确定怎么测，再记录结果。只有测试路径、器械、顺序和记录口径稳定，复测才有意义。",
    )

    profile = st.session_state.profile
    equipment_access = st.multiselect(
        "这次测试能使用的器械",
        ["row", "ski", "sled", "kettlebell", "dumbbell", "track"],
        default=profile.get("equipment_access", []),
    )
    protocol = get_benchmark_protocol(equipment_access)
    worksheet = build_benchmark_worksheet(equipment_access)
    brief = build_test_day_brief(equipment_access)
    operator = build_test_session_operator(
        equipment_access,
        safety_gate=st.session_state.passport.get("safety_gate", {}),
    )
    command_board = build_test_day_command_board(operator)
    protocol_profile = {**profile, "equipment_access": equipment_access}
    protocol_console = build_lab_readiness_console(
        protocol_profile,
        st.session_state.passport,
        summarize_benchmark_sessions(st.session_state.benchmark_sessions),
    )

    _metric_row(
        [
            ("测试路径", protocol["path"]),
            ("Protocol", protocol["version"]),
            ("证据状态", protocol["evidence_status"]),
            ("组件数", len(protocol["component_protocols"])),
        ]
    )
    st.markdown(
        '<div class="rx-callout">SportRx 现在先做 repeatable measurement。没有测过的项目保持 Not tested，不用平均值或主观感觉补齐。</div>',
        unsafe_allow_html=True,
    )
    _benchmark_protocol_console(protocol, worksheet, brief, protocol_console)
    _test_day_command_board(command_board)
    st.subheader("Lab Readiness Console")
    st.caption(protocol_console["claim_boundary"])
    _lab_console(protocol_console)
    st.info(protocol_console["next_action"])

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["测试前", "Operator", "标准流程", "组件说明", "Worksheet", "Test-Day Brief", "记录口径"])

    with tab1:
        st.subheader("Safety Gate")
        for rule in protocol["global_stop_rules"]:
            st.write(f"- {rule}")
        st.caption(protocol["claim_boundary"])

        if st.button("用这些器械进入 Benchmark Log", type="primary"):
            st.session_state.profile["equipment_access"] = equipment_access
            _refresh_outputs()
            st.success("器械设置已保存。现在可以切到 Benchmark Log 记录测试。")

    with tab2:
        _test_session_operator_console(operator)
        st.subheader("Test-Day Flow Board")
        _operator_flow_board(operator)
        st.subheader("Component Operator Cards")
        _operator_component_cards(operator)
        with st.expander("查看结构化 Operator Steps", expanded=False):
            st.dataframe(
                [
                    {
                        "顺序": step["order"],
                        "步骤": step["label"],
                        "类型": zh(step["type"]),
                        "状态": zh(step["status"]),
                        "区域": zh(step.get("area", "")),
                        "记录": ", ".join(step.get("required_fields", [])) if step["type"] == "component" else step.get("record", ""),
                        "单位提示": step.get("unit_hint", ""),
                    }
                    for step in operator["steps"]
                ],
                hide_index=True,
                width="stretch",
            )
        for step in operator["component_steps"]:
            with st.expander(f"{step['order']}. {step['label']} · {zh(step['area'])}", expanded=not step["optional"]):
                st.write(f"**Purpose:** {step['purpose']}")
                st.write(f"**Unit hint:** {step['unit_hint']}")
                st.write("**Record now**")
                for item in step["record_now"]:
                    st.write(f"- {item}")
                st.write("**Stop if**")
                for item in step["stop_if"]:
                    st.write(f"- {item}")
                st.caption(step["benchmark_log_handoff"])
        st.download_button(
            "下载 Test Session Operator",
            test_session_operator_markdown(operator),
            file_name="sportrx_test_session_operator.md",
            mime="text/markdown",
            width="stretch",
        )

    with tab3:
        st.subheader("Test-Day Flow")
        for item in protocol["test_day_flow"]:
            st.write(f"**{item['step']}**")
            st.write(item["instruction"])

    with tab4:
        _benchmark_protocol_components(protocol)
        for component in protocol["component_protocols"]:
            with st.expander(component["test"], expanded=not component["optional"]):
                st.write(f"**Area:** {zh(component['area'])}")
                st.write(f"**Purpose:** {component['purpose']}")
                st.write("**Setup**")
                for item in component["setup"]:
                    st.write(f"- {item}")
                st.write("**Execution**")
                for item in component["execution"]:
                    st.write(f"- {item}")
                st.write("**Record**")
                for item in component["record"]:
                    st.write(f"- {item}")
                st.write("**Retest**")
                for item in component["retest_notes"]:
                    st.write(f"- {item}")

    with tab5:
        st.subheader("Benchmark Session Worksheet")
        st.caption(worksheet["claim_boundary"])
        setup_rows = [{"项目": item["label"], "提示": item["hint"], "记录": "________________"} for item in worksheet["session_setup"]]
        st.dataframe(setup_rows, hide_index=True, width="stretch")
        st.write("**Component Recording Sheet**")
        st.dataframe(
            [
                {
                    "顺序": item["order"],
                    "测试": item["test"],
                    "区域": zh(item["area"]),
                    "必填": "可选" if item["optional"] else "建议完成",
                    "记录字段": ", ".join(item["record_fields"]),
                    "Retest Anchor": item["retest_anchor"],
                }
                for item in worksheet["component_rows"]
            ],
            hide_index=True,
            width="stretch",
        )
        st.download_button(
            "下载 Benchmark Worksheet",
            benchmark_worksheet_markdown(worksheet),
            file_name="sportrx_benchmark_worksheet.md",
            mime="text/markdown",
            width="stretch",
        )

    with tab6:
        st.subheader("Test-Day Brief")
        st.caption(brief["claim_boundary"])
        left, right = st.columns([1.05, 0.95])
        with left:
            st.write("**Pre-Test Checks**")
            for item in brief["pre_test_checks"]:
                st.write(f"- {item}")
            st.write("**After Test**")
            for item in brief["after_test"]:
                st.write(f"- {item}")
        with right:
            st.write("**Component Order**")
            st.dataframe(
                [
                    {
                        "顺序": component["order"],
                        "测试": component["test"],
                        "区域": zh(component["area"]),
                        "必填": "可选" if component["optional"] else "建议完成",
                        "记录字段": ", ".join(component["record_fields"]),
                    }
                    for component in brief["components"]
                ],
                hide_index=True,
                width="stretch",
            )
        st.download_button(
            "下载 Test-Day Brief",
            test_day_brief_markdown(brief),
            file_name="sportrx_test_day_brief.md",
            mime="text/markdown",
        )

    with tab7:
        st.subheader("Recording Principles")
        for item in protocol["recording_principles"]:
            st.write(f"- {item}")
        st.download_button(
            "下载 Protocol Markdown",
            protocol_markdown(protocol),
            file_name="sportrx_hybrid_benchmark_protocol.md",
            mime="text/markdown",
        )


def benchmark_log_page() -> None:
    _page_header(
        "Benchmark Log",
        "SportRx Hybrid Benchmark v1",
        "记录原始测试结果、RPE、器械和替代动作。这里保存的是测量记录，不是 percentile、完赛预测或医疗结论。",
    )

    profile = st.session_state.profile
    summary = summarize_benchmark_sessions(st.session_state.benchmark_sessions)

    st.markdown(
        '<div class="rx-callout">建议你先完成至少两个测试组件。下一次复测时尽量使用相同路线、器械、负重和测试顺序。</div>',
        unsafe_allow_html=True,
    )

    equipment_access = st.multiselect(
        "本次可用器械",
        ["row", "ski", "sled", "kettlebell", "dumbbell", "track"],
        default=profile.get("equipment_access", []),
    )
    log_profile = {**profile, "equipment_access": equipment_access}
    log_console = build_lab_readiness_console(log_profile, st.session_state.passport, summary)
    st.subheader("Lab Readiness Console")
    st.caption(log_console["claim_boundary"])
    _lab_console(log_console)
    st.info(log_console["next_action"])
    st.download_button(
        "下载 Lab Readiness Console",
        lab_readiness_markdown(log_console),
        file_name="sportrx_lab_readiness_console.md",
        mime="text/markdown",
    )
    benchmark = get_hybrid_benchmark(equipment_access)
    spec = benchmark["spec"]
    protocol = get_benchmark_protocol(equipment_access)
    worksheet = build_benchmark_worksheet(equipment_access)
    entry_contract = build_benchmark_log_entry_contract(equipment_access)
    import_result = benchmark_profile_patch(st.session_state.benchmark_sessions)
    comparisons = compare_retest_sessions(st.session_state.benchmark_sessions)
    deviation_review = build_protocol_deviation_review(st.session_state.benchmark_sessions)
    _benchmark_log_dashboard(summary, benchmark, import_result, comparisons)
    protocol_lookup = {component["component_id"]: component for component in protocol["component_protocols"]}
    contract_lookup = {component["component_id"]: component for component in entry_contract["components"]}

    st.subheader(f"{spec['name']} / {spec['version']}")
    st.caption(benchmark["scoring"]["note"])
    setup_col, protocol_col = st.columns([1.1, 0.9])
    with setup_col:
        st.write("**Session Setup Snapshot**")
        st.dataframe(
            [
                {"字段": "Benchmark path", "当前": benchmark["path"]},
                {"字段": "Protocol version", "当前": spec["version"]},
                {"字段": "Equipment", "当前": zh(equipment_access)},
                {"字段": "Evidence status", "当前": spec["evidence_status"]},
            ],
            hide_index=True,
            width="stretch",
        )
    with protocol_col:
        st.write("**Protocol Guardrails**")
        for item in protocol["recording_principles"]:
            st.write(f"- {item}")
        st.download_button(
            "下载本次 Benchmark Worksheet",
            benchmark_worksheet_markdown(worksheet),
            file_name="sportrx_benchmark_worksheet.md",
            mime="text/markdown",
            width="stretch",
        )
    st.subheader("Benchmark Log Entry Contract")
    _benchmark_log_entry_contract_panel(entry_contract)
    st.download_button(
        "下载 Benchmark Log Entry Contract",
        benchmark_log_entry_contract_markdown(entry_contract),
        file_name="sportrx_benchmark_log_entry_contract.md",
        mime="text/markdown",
        width="stretch",
    )

    with st.form("benchmark_log_form"):
        setup_tab, component_tab, review_tab = st.tabs(["Session Setup", "Component Results", "Review & Save"])
        with setup_tab:
            col1, col2 = st.columns(2)
            session_date = col1.date_input("测试日期")
            followed_protocol = col2.checkbox("我已按当前 Protocol 完成或记录偏离原因", value=True)
            global_notes = st.text_area("本次测试备注", placeholder="例如：跑道、天气、器械型号、身体状态、是否中断、是否偏离 protocol。")
            context_col1, context_col2, context_col3 = st.columns(3)
            warmup_minutes = context_col1.number_input("热身时长（分钟）", min_value=0.0, value=0.0, step=1.0)
            familiarization_level = context_col2.selectbox("动作 / 器械熟悉度", ["", "first_use", "limited", "familiar"])
            session_timing_method = context_col3.selectbox("主要计时方式", ["", "manual_timer", "treadmill_console", "erg_monitor"])
            st.caption("建议写清楚路线、器械型号、负重、替代动作和身体状态。未来复测时这些信息比一个总分更有价值。")

        component_results = []

        with component_tab:
            for component in spec["components"]:
                component_protocol = protocol_lookup.get(component["id"], {})
                component_contract = contract_lookup.get(component["id"], {})
                st.markdown(f"#### {component['test']}")
                if component_protocol:
                    st.caption(component_protocol["purpose"])
                col1, col2, col3, col4 = st.columns([1.1, 1.0, 1.0, 1.4])
                completed = col1.checkbox("完成", value=False, key=f"log_completed_{component['id']}")
                allowed_units = component_contract.get("allowed_value_units", [_component_unit(component)])
                default_unit = allowed_units[0]
                if len(allowed_units) > 1:
                    unit = col2.selectbox(
                        "单位",
                        allowed_units,
                        index=0,
                        key=f"log_unit_{component['id']}",
                    )
                else:
                    unit = default_unit
                    col2.caption(f"单位：{unit}")
                value_label = component_contract.get("primary_value_label", "结果")
                value = col2.number_input(value_label, min_value=0.0, value=0.0, step=1.0, key=f"log_value_{component['id']}")
                rpe = col3.slider("RPE", 0.0, 10.0, 0.0, 0.5, key=f"log_rpe_{component['id']}")
                substitution = col4.text_input("替代动作/器械", key=f"log_sub_{component['id']}")
                notes = st.text_input("组件备注", key=f"log_notes_{component['id']}")
                result_fields = {}
                primary_field = component_contract.get("primary_value_field", "raw_result")
                if completed and value > 0:
                    result_fields[primary_field] = float(value)
                companion_fields = component_contract.get("companion_fields", [])
                if companion_fields:
                    with st.expander("结构化补充字段", expanded=completed):
                        for field in companion_fields:
                            result_fields[field] = _benchmark_log_extra_field_input(field, component["id"], completed)
                if component_contract:
                    st.caption(component_contract["ui_hint"])
                    status_label = {
                        "supported": "已有直接依据",
                        "partial_evidence": "部分依据",
                        "experimental": "实验性协议",
                    }.get(component_contract["protocol_evidence_status"], "实验性协议")
                    st.caption(f"协议证据状态：{status_label}。{component_contract['protocol_evidence_id']}")
                protocol_context = {}
                context_fields = [
                    field
                    for field in component_contract.get("protocol_context_fields", [])
                    if field not in {"warmup_minutes", "familiarization_level", "test_order", "loads_used"}
                ]
                if context_fields:
                    with st.expander("复测所需的测试条件", expanded=completed):
                        for field in context_fields:
                            protocol_context[field] = _benchmark_protocol_context_input(field, component["id"])
                if component["id"] == "station_circuit":
                    protocol_context["loads_used"] = result_fields.get("loads_used", "")
                if component_protocol:
                    with st.expander("Protocol notes", expanded=False):
                        st.write("Setup")
                        for item in component_protocol["setup"]:
                            st.write(f"- {item}")
                        st.write("Record")
                        for item in component_protocol["record"]:
                            st.write(f"- {item}")
                component_results.append(
                    build_component_result(
                        component["id"],
                        value=value if completed else None,
                        value_unit=unit,
                        rpe_0_10=rpe if completed and rpe > 0 else None,
                        equipment=sorted(set(equipment_access + ([result_fields["modality"]] if result_fields.get("modality") else []))),
                        substitution=substitution,
                        result_fields=result_fields,
                        protocol_context=protocol_context,
                        completed=completed,
                        notes=notes,
                    )
                )

        preview_session = create_benchmark_session(
            {**st.session_state.profile, "equipment_access": equipment_access},
            component_results,
            session_date=session_date.isoformat(),
            global_notes=global_notes,
            session_context={
                "warmup_minutes": float(warmup_minutes) if warmup_minutes > 0 else None,
                "familiarization_level": familiarization_level,
                "timing_method": session_timing_method,
            },
        )
        if not followed_protocol:
            preview_session["session_quality"]["warnings"].append("Protocol was not fully followed; keep this as a contextual raw record.")
        preview_session["import_compatibility"] = build_benchmark_import_compatibility(preview_session["component_results"])
        with review_tab:
            _benchmark_draft_session_board(preview_session)
            _quality_review_panel(preview_session["session_quality"])
            _benchmark_import_compatibility_panel(preview_session["import_compatibility"])
            with st.expander("Raw Payload Preview", expanded=False):
                st.dataframe(
                    [
                        {
                            "测试": result["test"],
                            "完成": "是" if result["completed"] else "否",
                            "结果": "Not tested" if result["value"] is None else str(result["value"]),
                            "单位": result["value_unit"],
                            "RPE": "未记录" if result["rpe_0_10"] is None else str(result["rpe_0_10"]),
                            "Area": zh(result["area"]),
                            "保存状态": zh(preview_session["session_quality"]["status"]),
                            "导入状态": zh(
                                next(
                                    (
                                        item["status"]
                                        for item in preview_session["import_compatibility"]["items"]
                                        if item["component_id"] == result["component_id"]
                                    ),
                                    "not_measured",
                                )
                            ),
                        }
                        for result in preview_session["component_results"]
                    ],
                    hide_index=True,
                    width="stretch",
                )

        submitted = st.form_submit_button("保存 Benchmark Log", type="primary")

    if submitted:
        if not preview_session["session_quality"]["save_allowed"]:
            st.error("这次记录还不能保存：至少需要一个完成组件和一个原始结果值。")
        else:
            st.session_state.profile["equipment_access"] = equipment_access
            st.session_state.benchmark_sessions.append(preview_session)
            st.success("Benchmark Log 已保存。")

    if st.session_state.benchmark_sessions:
        deviation_review = build_protocol_deviation_review(st.session_state.benchmark_sessions)
        st.subheader("Benchmark Session Records")
        _benchmark_session_gallery(st.session_state.benchmark_sessions)
        st.subheader("Protocol Deviation Review")
        _protocol_deviation_console(deviation_review)
        deviation_tab, retest_context_tab, deviation_export_tab = st.tabs(["Component Context", "Retest Context", "Export"])
        with deviation_tab:
            st.dataframe(_protocol_deviation_component_rows(deviation_review), hide_index=True, width="stretch")
        with retest_context_tab:
            if deviation_review["retest_reviews"]:
                st.dataframe(_protocol_deviation_retest_rows(deviation_review), hide_index=True, width="stretch")
            else:
                st.info("还没有重复完成同一 Benchmark component，暂时无法检查复测 context 是否一致。")
        with deviation_export_tab:
            st.download_button(
                "下载 Protocol Deviation Review",
                protocol_deviation_markdown(deviation_review),
                file_name="sportrx_protocol_deviation_review.md",
                mime="text/markdown",
                width="stretch",
            )

        st.subheader("本地记录")
        rows = []
        for session in st.session_state.benchmark_sessions:
            for result in session["component_results"]:
                rows.append(
                    {
                        "日期": session["date"],
                        "路径": session["benchmark_path"],
                        "测试": result["test"],
                        "完成": "是" if result["completed"] else "否",
                        "结果": "Not tested" if result["value"] is None else str(result["value"]),
                        "单位": result["value_unit"],
                        "RPE": "未记录" if result["rpe_0_10"] is None else str(result["rpe_0_10"]),
                        "替代": result["substitution"] or "",
                        "质量": zh(session.get("session_quality", {}).get("status", "not_reviewed")),
                        "导入": zh(session.get("import_compatibility", {}).get("status", "not_reviewed")),
                    }
                )
        st.dataframe(rows, hide_index=True, width="stretch")

        with st.expander("HYROX Check 导入预览", expanded=True):
            st.caption(import_result["claim_boundary"])
            if import_result["profile_patch"]:
                st.json(import_result["profile_patch"])
                if import_result["applied"]:
                    st.write("导入映射：")
                    for item in import_result["applied"]:
                        st.caption(f"- {item}")
                if import_result["skipped"]:
                    st.write("保留为原始记录：")
                    for item in import_result["skipped"]:
                        st.caption(f"- {item}")
                if st.button("把兼容数据应用到 HYROX Check", type="primary"):
                    st.session_state.profile.update(import_result["profile_patch"])
                    _refresh_outputs()
                    st.success("HYROX Check 已更新。可以切到 Training Profile 查看变化。")
            else:
                st.info("还没有可直接导入 HYROX Check 的结果。1 km run 秒数、RowErg/SkiErg 秒数可以导入。")

        if comparisons:
            st.subheader("复测变化")
            comparison_rows = [
                {
                    "测试": item["test"],
                    "第一次": str(item["first_value"]),
                    "最近一次": str(item["latest_value"]),
                    "单位": item["value_unit"],
                    "变化": str(item["delta"]),
                    "方向": "有改善" if item["direction"] == "improved" else "未改善/不明确",
                }
                for item in comparisons
            ]
            st.dataframe(comparison_rows, hide_index=True, width="stretch")
            st.caption("这是原始复测比较，不是预测，也不是已验证的最小有意义变化。")

        col1, col2 = st.columns(2)
        col1.download_button(
            "下载 JSON",
            export_sessions_json(st.session_state.benchmark_sessions),
            file_name="sportrx_benchmark_log.json",
            mime="application/json",
        )
        col2.download_button(
            "下载 CSV",
            export_sessions_csv(st.session_state.benchmark_sessions),
            file_name="sportrx_benchmark_log.csv",
            mime="text/csv",
        )


def progress_page() -> None:
    _page_header(
        "Feedback Loop",
        "复测与周反馈 Dashboard",
        "把每周完成率、平均 RPE、自动进阶决策和 Benchmark 复测变化放在同一个闭环里。SportRx 只总结已经记录的数据，不做预测。",
    )
    if not _is_internal_edition() and not _public_venue_entry_eligible():
        st.warning("当前分流仅提供评估结果，不能进入周反馈、自动进阶或复测解释。" if not _is_english_edition() else "This assessment-only route cannot enter weekly feedback, automated progression, or retest interpretation.")
        st.button("返回测试前确认" if not _is_english_edition() else "Return to Venue Entry", type="primary", width="stretch", on_click=_set_page, args=("Venue Entry",))
        return
    automation_guard = build_automation_guard(st.session_state.feedback_by_week)
    if not automation_guard["automated_outputs_allowed"]:
        st.error(zh(automation_guard["reason"]))
        st.caption(automation_guard["claim_boundary"])
        return
    plan = st.session_state.plan
    dashboard = build_feedback_dashboard(plan, st.session_state.feedback_by_week, st.session_state.benchmark_sessions)
    retest_guard = build_retest_interpretation_guard(st.session_state.benchmark_sessions)
    _feedback_loop_console(dashboard)
    _feedback_loop_snapshot(dashboard, retest_guard)

    if not dashboard["available"]:
        st.error("安全门阻断了自动训练交接，暂不生成训练。")
        st.caption(dashboard["claim_boundary"])
        return

    adherence = dashboard["adherence"]
    _metric_row(
        [
            ("Adherence", adherence["status"]),
            ("Weeks Recorded", adherence["weeks_recorded"]),
            ("Completion Rate", adherence["average_completion_rate"]),
            ("Benchmark Retests", len(dashboard["retest_comparisons"])),
        ]
    )
    st.caption(dashboard["claim_boundary"])

    feedback_tab, decision_tab, retest_tab, export_tab = st.tabs(
        ["Weekly Feedback", "Progression Decision", "Benchmark Retest", "Export"]
    )

    with feedback_tab:
        feedback_week = st.selectbox("反馈周次", [week["week"] for week in plan["weeks"][:-1]])
        planned_sessions = plan["weeks"][feedback_week - 1]["frequency_per_week"]
        existing = st.session_state.feedback_by_week.get(int(feedback_week), {})

        with st.form("feedback_form"):
            completed_sessions = st.number_input(
                "完成训练次数",
                0,
                planned_sessions,
                int(existing.get("completed_sessions", planned_sessions)),
            )
            average_rpe = st.slider("平均 RPE", 0.0, 10.0, float(existing.get("average_rpe", 5.0)), 0.5)
            felt_too_hard = st.checkbox("这一周明显偏难", value=bool(existing.get("felt_too_hard", False)))
            adverse_event = st.checkbox("出现警示症状或不良事件", value=bool(existing.get("adverse_event", False)))
            submitted = st.form_submit_button("保存周反馈并更新下一周", type="primary")

        if submitted:
            st.session_state.feedback_by_week[int(feedback_week)] = {
                "completed_sessions": int(completed_sessions),
                "average_rpe": float(average_rpe),
                "felt_too_hard": bool(felt_too_hard),
                "adverse_event": bool(adverse_event),
            }
            _refresh_outputs()
            st.success("周反馈已保存，进阶建议已更新。")
            dashboard = build_feedback_dashboard(st.session_state.plan, st.session_state.feedback_by_week, st.session_state.benchmark_sessions)

        st.subheader("Weekly Feedback Log")
        _weekly_feedback_cards(dashboard)
        with st.expander("查看结构化周反馈表"):
            st.dataframe(_feedback_rows(dashboard), hide_index=True, width="stretch")

    with decision_tab:
        st.subheader("Current Progression Decision")
        _feedback_decision_panel(dashboard)
        latest_feedback = _latest_recorded_feedback_row(dashboard)
        if latest_feedback:
            plan_actual = latest_feedback["plan_actual"]
            st.write(zh(latest_feedback["decision_rationale"]))
            st.dataframe(
                [
                    {"字段": "After week", "内容": str(latest_feedback["week"])},
                    {"字段": "Action", "内容": zh(plan_actual["action_label"])},
                    {"字段": "Completion", "内容": _feedback_percent_label(plan_actual["completion_rate"])},
                    {"字段": "Average RPE", "内容": str(plan_actual["average_rpe"])},
                    {"字段": "Reason Codes", "内容": "、".join(zh(code) for code in plan_actual.get("reason_codes", []))},
                    {"字段": "Flags", "内容": "、".join(zh(flag) for flag in plan_actual.get("flags", [])) or "无"},
                    {"字段": "Boundary", "内容": zh(plan_actual["claim_boundary"])},
                ],
                hide_index=True,
                width="stretch",
            )
        else:
            st.info("还没有周反馈。保存 Week 1 反馈后，这里会显示下一周进阶决策。")

        st.subheader("Plan-Actual Reason Codes")
        st.caption("这些 reason codes 只解释规则引擎为什么调整，不是恢复评分、风险预测或医疗建议。")
        st.table(_plan_actual_rows(dashboard["plan_actual_reasons"]))

        st.subheader("Next Actions")
        for action in dashboard["next_actions"]:
            st.write(f"- {action}")

    with retest_tab:
        summary = dashboard["benchmark_summary"]
        _retest_interpretation_console(retest_guard)
        _retest_loop_cards(dashboard, retest_guard)
        _metric_row(
            [
                ("Benchmark Sessions", summary["session_count"]),
                ("Latest Date", summary["latest_date"] or "未记录"),
                ("Measured Components", len(summary["measured_components"])),
                ("Retest Ready", "yes" if summary["retest_ready"] else "no"),
            ]
        )
        if retest_guard["items"]:
            st.dataframe(_retest_interpretation_rows(retest_guard), hide_index=True, width="stretch")
            st.caption("这是原始复测比较加 protocol-context guard，不是预测，也不是已验证的最小有意义变化。")
        else:
            st.info("还没有重复测试同一 Benchmark component。先在 Benchmark Log 记录至少两次同一组件。")
            if st.button("去 Benchmark Log", type="primary"):
                _set_page("Benchmark Log")

    with export_tab:
        st.subheader("Download")
        st.download_button(
            "下载 Feedback Dashboard Markdown",
            feedback_dashboard_markdown(dashboard),
            file_name="sportrx_feedback_dashboard.md",
            mime="text/markdown",
        )
        st.download_button(
            "下载 Retest Interpretation Guard",
            retest_interpretation_markdown(retest_guard),
            file_name="sportrx_retest_interpretation_guard.md",
            mime="text/markdown",
        )
        st.subheader("Retest Guidance")
        st.write("建议在 4 周训练 block 后，或完成一次有意义的 benchmark session 后复测。")


def export_center_page() -> None:
    _page_header(
        "Export Center",
        "SportRx 本地导出中心",
        "集中下载 Protocol、Benchmark Log、Training Profile、Training Block 和 Feedback Dashboard。所有导出都保留为用户本地文件。",
    )
    bundle = build_export_bundle(
        st.session_state.profile,
        st.session_state.passport,
        st.session_state.plan,
        st.session_state.benchmark_sessions,
        st.session_state.feedback_by_week,
        _evidence_file_status(),
        str(ROOT),
        st.session_state.pilot_feedback_entries,
    )
    _metric_row(
        [
            ("Downloads", len(bundle["files"])),
            ("Benchmark Logs", len(st.session_state.benchmark_sessions)),
            ("Feedback Weeks", len(st.session_state.feedback_by_week)),
            ("Pilot Feedback", len(st.session_state.pilot_feedback_entries)),
            ("Format", "Markdown / JSON / CSV"),
        ]
    )
    st.caption(bundle["claim_boundary"])
    catalog = build_artifact_catalog([item for item in bundle["files"] if item["id"] != "artifact_catalog_markdown"])
    schema_registry = build_measurement_schema_registry({item["id"] for item in bundle["files"]})
    review_pack_manifest = build_review_pack_manifest(bundle)
    review_pack_integrity = build_review_pack_integrity(bundle["files"])
    package_manifest = build_release_package_manifest(ROOT)
    _export_center_console(
        bundle,
        catalog,
        review_pack_integrity,
        st.session_state.benchmark_sessions,
        st.session_state.feedback_by_week,
        st.session_state.pilot_feedback_entries,
    )
    _export_release_package_board(
        bundle,
        catalog,
        review_pack_manifest,
        review_pack_integrity,
        package_manifest,
        st.session_state.benchmark_sessions,
        st.session_state.feedback_by_week,
        st.session_state.pilot_feedback_entries,
    )

    handoff_file = next(item for item in bundle["files"] if item["id"] == "reviewer_handoff_markdown")
    input_ledger_file = next(item for item in bundle["files"] if item["id"] == "input_ledger_markdown")
    schema_file = next(item for item in bundle["files"] if item["id"] == "measurement_schema_registry_markdown")
    st.subheader("Reviewer Handoff")
    st.write("给第一次试用 SportRx 的 reviewer：先怎么打开、看哪些 demo、下载哪些文件，以及哪些声明不能越界。")
    col1, col2, col3 = st.columns(3)
    col1.download_button(
        "下载 Reviewer Handoff",
        handoff_file["content"],
        file_name=handoff_file["filename"],
        mime=handoff_file["mime"],
        width="stretch",
    )
    col2.download_button(
        "下载 Input Ledger",
        input_ledger_file["content"],
        file_name=input_ledger_file["filename"],
        mime=input_ledger_file["mime"],
        width="stretch",
    )
    col3.download_button(
        "下载 Schema Registry",
        schema_file["content"],
        file_name=schema_file["filename"],
        mime=schema_file["mime"],
        width="stretch",
    )

    st.subheader("Measurement Schema Registry")
    _schema_registry_console(schema_registry)
    st.dataframe(
        [
            {
                "对象": item["label"],
                "Owner": item["owner"],
                "字段数": item["field_count"],
                "导出": item["export_artifact_id"],
                "覆盖": zh(item["export_status"]),
                "Not tested policy": item["not_tested_policy"],
            }
            for item in schema_registry["objects"]
        ],
        hide_index=True,
        width="stretch",
    )

    st.subheader("Review Pack")
    st.write("一键下载当前所有本地 review artifacts。ZIP 只包含 Export Center 生成的本地文件，不包含内部审阅文档或缓存。")
    _metric_row(
        [
            ("Integrity", review_pack_integrity["status"]),
            ("Payload Files", review_pack_integrity["payload_file_count"]),
            ("Archive Entries", review_pack_manifest["archive_entry_count"]),
            ("Checks", f"{review_pack_integrity['passed_checks']} / {review_pack_integrity['total_checks']}"),
        ]
    )
    st.caption(review_pack_integrity["claim_boundary"])
    st.download_button(
        "下载 SportRx Review Pack ZIP",
        build_review_pack_zip(bundle),
        file_name="sportrx_review_pack.zip",
        mime="application/zip",
        width="stretch",
    )
    st.download_button(
        "下载 Review Pack Integrity Markdown",
        review_pack_integrity_markdown(review_pack_integrity),
        file_name="sportrx_review_pack_integrity.md",
        mime="text/markdown",
        width="stretch",
    )
    st.download_button(
        "下载 Public Package Manifest JSON",
        json.dumps(package_manifest, ensure_ascii=False, indent=2),
        file_name="sportrx_public_package_manifest.json",
        mime="application/json",
        width="stretch",
    )

    with st.expander("查看 Review Pack checksums", expanded=False):
        st.dataframe(_review_pack_integrity_rows(review_pack_integrity), hide_index=True, width="stretch")
    with st.expander("查看 Public Package 文件清单", expanded=False):
        st.caption(package_manifest["claim_boundary"])
        _metric_row(
            [
                ("Package Status", package_manifest["status"]),
                ("Included Files", package_manifest["included_file_count"]),
                ("Checks", f"{package_manifest['passed_checks']} / {package_manifest['total_checks']}"),
                ("Internal Docs", "excluded"),
            ]
        )
        st.dataframe(
            [
                {
                    "检查": item["label"],
                    "状态": zh(item["status"]),
                    "说明": zh(item["detail"]),
                }
                for item in package_manifest["checks"]
            ],
            hide_index=True,
            width="stretch",
        )

    st.subheader("Artifact Catalog")
    st.caption(catalog["claim_boundary"])
    _artifact_catalog_cards(catalog)

    rows = [
        {
            "文件": str(item["filename"]),
            "内容": str(item["label"]),
            "格式": str(item["mime"]),
        }
        for item in bundle["files"]
    ]
    st.table(rows)

    st.subheader("Downloads")
    columns = st.columns(2)
    for index, item in enumerate(bundle["files"]):
        with columns[index % 2]:
            st.download_button(
                item["label"],
                item["content"],
                file_name=item["filename"],
                mime=item["mime"],
                width="stretch",
            )


def evidence_library_page() -> None:
    _page_header(
        "Evidence Library",
        "SportRx 循证资料库",
        "浏览当前本地保存的 source index、evidence tier、产品用途和限制。这里帮助 reviewer 判断依据边界，不生成新结论。",
    )
    library = build_evidence_library(ROOT)
    validation_matrix = build_validation_readiness_matrix(
        st.session_state.profile,
        st.session_state.passport,
        st.session_state.plan,
        st.session_state.benchmark_sessions,
        st.session_state.feedback_by_week,
        st.session_state.pilot_feedback_entries,
        ROOT,
    )
    evidence_coverage = build_evidence_coverage(ROOT)
    self_use_protocol = build_self_use_protocol(validation_matrix, st.session_state.profile)
    _evidence_library_console(library)
    st.subheader("Evidence Topic Map")
    _evidence_topic_cards(library)
    st.subheader("Claim Boundary Board")
    _evidence_claim_boundary_board(validation_matrix, evidence_coverage)
    st.subheader("Validation Readiness")
    _validation_readiness_console(validation_matrix)
    validation_tab, capture_tab, claims_tab = st.tabs(["Validation Phases", "Capture Checks", "Blocked Claims"])
    with validation_tab:
        st.dataframe(_validation_phase_rows(validation_matrix), hide_index=True, width="stretch")
    with capture_tab:
        st.dataframe(_validation_capture_rows(validation_matrix), hide_index=True, width="stretch")
    with claims_tab:
        st.write("当前仍然阻断这些声明：")
        for claim in validation_matrix["blocked_claims"]:
            st.write(f"- {claim}")
    st.download_button(
        "下载 Validation Readiness Matrix",
        validation_readiness_markdown(validation_matrix),
        file_name="sportrx_validation_readiness_matrix.md",
        mime="text/markdown",
    )
    st.subheader("Phase 0 Self-Use Protocol")
    _self_use_protocol_console(self_use_protocol)
    schedule_tab, fields_tab, stop_tab = st.tabs(["4-Week Schedule", "Data Fields", "Stop / Review"])
    with schedule_tab:
        st.dataframe(_self_use_week_rows(self_use_protocol), hide_index=True, width="stretch")
    with fields_tab:
        st.dataframe(_self_use_field_rows(self_use_protocol), hide_index=True, width="stretch")
    with stop_tab:
        st.write("出现以下情况时，不继续自动解释：")
        for rule in self_use_protocol["stop_or_review_rules"]:
            st.write(f"- {rule}")
    st.download_button(
        "下载 Phase 0 Self-Use Protocol",
        self_use_protocol_markdown(self_use_protocol),
        file_name="sportrx_phase_0_self_use_protocol.md",
        mime="text/markdown",
    )

    topic_options = ["All"] + [topic["topic"] for topic in library["topics"]]
    selected_topic = st.selectbox("Evidence topic", topic_options)
    filtered_sources = (
        library["sources"]
        if selected_topic == "All"
        else [item for item in library["sources"] if item["topic"] == selected_topic]
    )

    st.subheader("Source Cards")
    _evidence_source_cards(filtered_sources)

    with st.expander("查看 Topic Map 表格", expanded=False):
        st.dataframe(
            [
                {
                    "Topic": item["topic"],
                    "Sources": item["source_count"],
                    "Evidence IDs": ", ".join(item["source_ids"]),
                }
                for item in library["topics"]
            ],
            hide_index=True,
            width="stretch",
        )

    with st.expander("查看 Source Index 表格", expanded=False):
        st.dataframe(_evidence_library_rows(filtered_sources), hide_index=True, width="stretch")
    with st.expander("查看 Evidence Coverage 规则映射", expanded=False):
        _evidence_coverage_console(evidence_coverage)
        st.dataframe(
            [
                {
                    "Rule": item["rule_id"],
                    "Status": zh(item["status"]),
                    "Tier": item["evidence_tier"],
                    "Sources": ", ".join(item["sources"]),
                    "Notes": zh(item["notes"]),
                }
                for item in evidence_coverage["rules"]
            ],
            hide_index=True,
            width="stretch",
        )
    st.download_button(
        "下载 Evidence Library Markdown",
        evidence_library_markdown(library),
        file_name="sportrx_evidence_library.md",
        mime="text/markdown",
    )

    with st.expander("Required evidence files", expanded=False):
        st.table(
            [
                {
                    "文件": item["path"],
                    "状态": "present" if item["present"] else "missing",
                }
                for item in library["required_files"]
            ]
        )


def knowledge_lab_page() -> None:
    _page_header(
        "Knowledge Lab",
        "SportRX Knowledge Lab",
        "内部循证知识检索与中文综合。它解释研究，不改变 Safety Gate、测试解释或训练剂量。",
    )
    summary = knowledge_corpus_summary(ROOT)
    validation = validate_knowledge_records(ROOT)
    _metric_row(
        [
            ("已审核卡片", f"{summary['reviewed_card_count']} / {summary['target_card_count']}"),
            ("可综合门槛", str(summary["minimum_synthesis_card_count"])),
            ("已覆盖主题", len(validation["covered_topics"])),
            ("状态", summary["status"]),
        ]
    )
    st.caption(summary["claim_boundary"])
    if not summary["synthesis_enabled"]:
        st.warning("知识检索可用；中文模型综合在达到 60 张审核卡并完成评测前保持关闭。")
    if validation["warnings"]:
        for warning in validation["warnings"]:
            st.caption(f"- {warning}")

    search_tab, corpus_tab, discovery_tab = st.tabs(["检索", "语料库状态", "发现与审核"])
    with search_tab:
        topics = ["全部"] + list(summary["topic_counts"])
        query = st.text_input("研究问题", placeholder="例如：为什么六分钟跑和跑走不能直接换算？")
        selected_topic = st.selectbox("主题筛选", topics)
        if query.strip():
            filters = {} if selected_topic == "全部" else {"topic": selected_topic}
            result = search_knowledge(query, filters, ROOT)
            st.caption(result["retrieval_mode"])
            if not result["results"]:
                st.info("没有找到足够的已审核知识卡。请加入发现队列，而不是让模型补写答案。")
            else:
                selected_ids = []
                for item in result["results"]:
                    with st.expander(f"{item['title_zh']} · {item['evidence_tier']}", expanded=True):
                        st.write(item["summary_zh"])
                        st.caption(f"英文题名：{item['title_en']}")
                        st.caption(f"来源：{', '.join(item['source_ids'])}")
                        st.caption(f"限制：{item['limitations']}")
                        selected_ids.append(item["id"])
                if st.button("用已检索证据生成中文综合", disabled=not summary["synthesis_enabled"], type="primary"):
                    synthesis = synthesize_knowledge(query, selected_ids, ROOT)
                    st.write(synthesis.get("answer_zh", ""))
                    st.caption(synthesis.get("boundary", synthesis["claim_boundary"]))
                    st.caption("引用卡：" + ", ".join(synthesis.get("cited_card_ids", [])))
    with corpus_tab:
        st.dataframe(
            [{"主题": topic, "已审核卡片": count} for topic, count in summary["topic_counts"].items()],
            hide_index=True,
            width="stretch",
        )
        st.write("当前基础卡仅来自已审核的 SportRX 证据记录；它们不等于 300-card v1 已完成。")
        st.json({"errors": validation["errors"], "warnings": validation["warnings"]})
    with discovery_tab:
        discovery_path = ROOT / "evidence/knowledge/discovery_queries.json"
        discovery = json.loads(discovery_path.read_text(encoding="utf-8"))["records"]
        st.write("自动发现只生成候选来源；候选不会进入检索或模型上下文。")
        st.dataframe(discovery, hide_index=True, width="stretch")


def release_qa_page() -> None:
    _page_header(
        "Release QA",
        "发布前自检",
        "检查 demo loop、导出物、claim boundary、安全边界和证据文件是否齐全。这里是产品自检，不是科学验证。",
    )
    qa = build_release_qa(
        st.session_state.profile,
        st.session_state.passport,
        st.session_state.plan,
        st.session_state.benchmark_sessions,
        st.session_state.feedback_by_week,
        _evidence_file_status(),
    )
    package_manifest = build_release_package_manifest(ROOT)
    launch = build_launch_readiness(
        st.session_state.profile,
        st.session_state.passport,
        st.session_state.plan,
        st.session_state.benchmark_sessions,
        st.session_state.feedback_by_week,
        _evidence_file_status(),
        str(ROOT),
    )
    runbook = build_demo_runbook(launch)
    runtime = build_runtime_doctor(ROOT)
    evidence_status = _evidence_file_status()
    evidence_library = build_evidence_library(ROOT)
    evidence_coverage = build_evidence_coverage(ROOT, evidence_status)
    protocol_deviation = build_protocol_deviation_review(st.session_state.benchmark_sessions)
    retest_guard = build_retest_interpretation_guard(st.session_state.benchmark_sessions)
    validation_matrix = build_validation_readiness_matrix(
        st.session_state.profile,
        st.session_state.passport,
        st.session_state.plan,
        st.session_state.benchmark_sessions,
        st.session_state.feedback_by_week,
        st.session_state.pilot_feedback_entries,
        ROOT,
    )
    self_use_protocol = build_self_use_protocol(validation_matrix, st.session_state.profile)
    session_quality = build_session_quality_review(
        st.session_state.profile,
        st.session_state.passport,
        st.session_state.plan,
        st.session_state.benchmark_sessions,
        st.session_state.feedback_by_week,
        evidence_status,
        ROOT,
    )
    pilot_review = build_pilot_review_console(st.session_state.pilot_feedback_entries)
    public_beta = build_public_beta_readiness(
        qa,
        launch,
        runtime,
        package_manifest,
        runbook,
        evidence_status,
        pilot_review,
    )
    release_bundle = build_export_bundle(
        st.session_state.profile,
        st.session_state.passport,
        st.session_state.plan,
        st.session_state.benchmark_sessions,
        st.session_state.feedback_by_week,
        evidence_status,
        str(ROOT),
        st.session_state.pilot_feedback_entries,
    )
    release_candidate = build_release_candidate_summary(
        qa=qa,
        launch=launch,
        runtime=runtime,
        package_manifest=package_manifest,
        public_beta=public_beta,
        export_file_count=len(release_bundle["files"]),
        review_pack_file_count=len(release_bundle["files"]),
    )
    _release_candidate_console(qa, launch, runtime, package_manifest, runbook, evidence_status)
    _release_reviewer_brief(release_candidate, public_beta, validation_matrix)
    if release_candidate["status"] == "needs_release_work":
        st.warning("当前 session 还没有形成完整 demo loop。可以先加载完整示例，再复查 Release QA。")
        action_col1, action_col2 = st.columns(2)
        action_col1.button(
            "加载完整示例并复查",
            type="primary",
            width="stretch",
            on_click=_load_demo_state,
            key="release_qa_load_demo",
        )
        action_col2.button(
            "打开 Export Center",
            width="stretch",
            on_click=_set_page,
            args=("Export Center",),
            key="release_qa_open_export_center",
        )
    st.download_button(
        "下载 Release Candidate Summary",
        release_candidate_summary_markdown(release_candidate),
        file_name="sportrx_release_candidate_summary.md",
        mime="text/markdown",
        width="stretch",
    )
    _public_beta_console(public_beta)
    st.subheader("Protocol Deviation Review")
    _protocol_deviation_console(protocol_deviation)
    with st.expander("查看 Protocol Deviation component 表格", expanded=False):
        st.dataframe(_protocol_deviation_component_rows(protocol_deviation), hide_index=True, width="stretch")
    st.download_button(
        "下载 Protocol Deviation Review Markdown",
        protocol_deviation_markdown(protocol_deviation),
        file_name="sportrx_protocol_deviation_review.md",
        mime="text/markdown",
    )
    st.subheader("Retest Interpretation Guard")
    _retest_interpretation_console(retest_guard)
    with st.expander("查看 Retest Interpretation 明细", expanded=False):
        st.dataframe(_retest_interpretation_rows(retest_guard), hide_index=True, width="stretch")
    st.download_button(
        "下载 Retest Interpretation Guard Markdown",
        retest_interpretation_markdown(retest_guard),
        file_name="sportrx_retest_interpretation_guard.md",
        mime="text/markdown",
    )
    st.subheader("Validation Readiness")
    _validation_readiness_console(validation_matrix)
    with st.expander("查看 Validation Phase 明细", expanded=False):
        st.dataframe(_validation_phase_rows(validation_matrix), hide_index=True, width="stretch")
    st.download_button(
        "下载 Validation Readiness Matrix Markdown",
        validation_readiness_markdown(validation_matrix),
        file_name="sportrx_validation_readiness_matrix.md",
        mime="text/markdown",
    )
    st.subheader("Phase 0 Self-Use Protocol")
    _self_use_protocol_console(self_use_protocol)
    with st.expander("查看 Phase 0 周计划", expanded=False):
        st.dataframe(_self_use_week_rows(self_use_protocol), hide_index=True, width="stretch")
    st.download_button(
        "下载 Phase 0 Self-Use Protocol Markdown",
        self_use_protocol_markdown(self_use_protocol),
        file_name="sportrx_phase_0_self_use_protocol.md",
        mime="text/markdown",
    )
    st.subheader("Session Quality Review")
    _session_quality_console(session_quality)
    with st.expander("查看 Session Quality Gates", expanded=False):
        st.dataframe(_session_quality_rows(session_quality), hide_index=True, width="stretch")
    st.download_button(
        "下载 Session Quality Review Markdown",
        session_quality_review_markdown(session_quality),
        file_name="sportrx_session_quality_review.md",
        mime="text/markdown",
    )
    st.subheader("Evidence Library")
    _evidence_library_console(evidence_library)
    with st.expander("查看 Evidence Library Source Index", expanded=False):
        st.dataframe(_evidence_library_rows(evidence_library["sources"]), hide_index=True, width="stretch")
    st.download_button(
        "下载 Evidence Library Markdown",
        evidence_library_markdown(evidence_library),
        file_name="sportrx_evidence_library.md",
        mime="text/markdown",
    )
    st.subheader("Evidence Coverage")
    _evidence_coverage_console(evidence_coverage)
    with st.expander("查看 Evidence Coverage 规则明细", expanded=False):
        st.dataframe(
            [
                {
                    "Rule": item["rule_id"],
                    "Status": zh(item["status"]),
                    "Tier": item["evidence_tier"],
                    "Sources": ", ".join(item["sources"]),
                    "Notes": item["notes"],
                }
                for item in evidence_coverage["rules"]
            ],
            hide_index=True,
            width="stretch",
        )
    st.download_button(
        "下载 Evidence Coverage Markdown",
        evidence_coverage_markdown(evidence_coverage),
        file_name="sportrx_evidence_coverage.md",
        mime="text/markdown",
    )
    st.subheader("Public Beta Readiness")
    st.caption(public_beta["claim_boundary"])
    _metric_row(
        [
            ("Beta Status", public_beta["status"]),
            ("Beta Checks", f"{public_beta['passed_checks']} / {public_beta['total_checks']}"),
            ("Pilot Feedback", f"{pilot_review['entry_count']} entries"),
            ("Pilot Status", pilot_review["status"]),
        ]
    )
    st.info(zh(public_beta["next_action"]))
    with st.expander("查看 Public Beta checks", expanded=False):
        st.table(
            [
                {
                    "检查": zh(item["label"]),
                    "状态": zh(item["status"]),
                    "说明": zh(item["detail"]),
                }
                for item in public_beta["checks"]
            ]
        )
    st.download_button(
        "下载 Public Beta Readiness Markdown",
        public_beta_readiness_markdown(public_beta),
        file_name="sportrx_public_beta_readiness.md",
        mime="text/markdown",
    )

    st.caption(qa["claim_boundary"])
    with st.expander("查看 Release QA checks", expanded=False):
        st.table(_release_qa_rows(qa))
    st.download_button(
        "下载 Release QA Markdown",
        release_qa_markdown(qa),
        file_name="sportrx_release_qa.md",
        mime="text/markdown",
    )

    st.subheader("Launch Readiness")
    st.caption(launch["claim_boundary"])
    _metric_row(
        [
            ("Launch Status", launch["status"]),
            ("Launch Checks", f"{launch['passed_checks']} / {launch['total_checks']}"),
            ("QA Status", launch["qa_status"]),
            ("Package", launch["package_status"]),
        ]
    )
    with st.expander("查看 Launch checks", expanded=False):
        st.table(
            [
                {
                    "检查": item["label"],
                    "状态": item["status"],
                    "说明": item["detail"],
                }
                for item in launch["checks"]
            ]
        )
    st.download_button(
        "下载 Launch Readiness Markdown",
        launch_readiness_markdown(launch),
        file_name="sportrx_launch_readiness.md",
        mime="text/markdown",
    )

    st.subheader("Runtime Doctor")
    st.caption(runtime["claim_boundary"])
    _metric_row(
        [
            ("Runtime", runtime["status"]),
            ("Python", runtime["python_version"]),
            ("Streamlit", runtime.get("streamlit_version") or "not installed"),
            ("Checks", f"{runtime['passed_checks']} / {runtime['total_checks']}"),
        ]
    )
    st.table(_runtime_doctor_rows(runtime))
    st.write("**Run Commands**")
    st.table(
        [
            {"Step": index, "Command": command}
            for index, command in enumerate(runtime["commands"], start=1)
        ]
    )
    st.download_button(
        "下载 Runtime Doctor Markdown",
        runtime_doctor_markdown(runtime),
        file_name="sportrx_runtime_doctor.md",
        mime="text/markdown",
    )

    st.subheader("Demo Runbook")
    st.caption(runbook["claim_boundary"])
    _metric_row(
        [
            ("Runbook Status", runbook["status"]),
            ("Must-show Pages", len(runbook["must_show"])),
            ("Estimated Time", f"{runbook['estimated_minutes']} min"),
            ("Guardrails", len(runbook["guardrails"])),
        ]
    )
    st.table(_runbook_rows(runbook))
    st.download_button(
        "下载 Demo Runbook Markdown",
        demo_runbook_markdown(runbook),
        file_name="sportrx_demo_runbook.md",
        mime="text/markdown",
    )

    st.subheader("Public Package Check")
    st.caption(package_manifest["claim_boundary"])
    _metric_row(
        [
            ("Package Status", package_manifest["status"]),
            ("Files", package_manifest["included_file_count"]),
            ("Checks", f"{package_manifest['passed_checks']} / {package_manifest['total_checks']}"),
            ("Internal Docs", "excluded"),
        ]
    )
    st.table(
        [
            {
                "检查": item["label"],
                "状态": item["status"],
                "说明": item["detail"],
            }
            for item in package_manifest["checks"]
        ]
    )
    st.download_button(
        "下载 Public Package Manifest JSON",
        json.dumps(package_manifest, ensure_ascii=False, indent=2),
        file_name="sportrx_public_package_manifest.json",
        mime="application/json",
    )


def pilot_feedback_page() -> None:
    _page_header(
        "Pilot Feedback",
        "本地试用反馈",
        "给 alpha reviewer 或试用者记录结构化反馈。所有内容保存在本地 session，可导出，不上传。",
    )
    prompt = build_pilot_feedback_prompt()
    summary = summarize_pilot_feedback(st.session_state.pilot_feedback_entries)
    review_console = build_pilot_review_console(st.session_state.pilot_feedback_entries)
    _pilot_review_console(review_console)
    _metric_row(
        [
            ("Entries", summary["entry_count"]),
            ("Status", summary["status"]),
            ("Flags", len(summary["review_flags"])),
            ("Scope", "product review"),
        ]
    )
    st.caption(prompt["claim_boundary"])

    prompt_tab, entry_tab, export_tab = st.tabs(["Prompt", "Record Feedback", "Export"])
    with prompt_tab:
        st.subheader("Reviewer Questions")
        for section in prompt["sections"]:
            st.write(f"**{section['section']}**")
            for question in section["questions"]:
                st.write(f"- {question}")
        st.download_button(
            "下载 Pilot Feedback Prompt",
            pilot_feedback_prompt_markdown(prompt),
            file_name="sportrx_pilot_feedback_prompt.md",
            mime="text/markdown",
        )

    with entry_tab:
        with st.form("pilot_feedback_form"):
            reviewer_role = st.selectbox("Reviewer role", ["athlete", "coach", "researcher", "gym operator", "other"])
            col1, col2, col3, col4, col5 = st.columns(5)
            ratings = {
                "setup_clarity": col1.slider("Setup", 1, 5, 4),
                "measurement_realism": col2.slider("Measure", 1, 5, 4),
                "trust": col3.slider("Trust", 1, 5, 4),
                "actionability": col4.slider("Action", 1, 5, 4),
                "visual_polish": col5.slider("Visual", 1, 5, 4),
            }
            comments = {
                "first_impression": st.text_area("第一印象：它像不像一个 testing product？"),
                "measurement_confusion": st.text_area("哪些输入、术语或测试不够清楚？"),
                "trust_boundary": st.text_area("哪些地方让你觉得可信或不可信？"),
                "next_improvement": st.text_area("下一步最该改什么？"),
            }
            consent_to_contact = st.checkbox("允许后续联系我追问反馈", value=False)
            contact = st.text_input("联系方式（可选）") if consent_to_contact else ""
            submitted = st.form_submit_button("保存本地反馈", type="primary")

        if submitted:
            entry = create_pilot_feedback_entry(
                reviewer_role=reviewer_role,
                ratings=ratings,
                comments=comments,
                consent_to_contact=consent_to_contact,
                contact=contact,
            )
            st.session_state.pilot_feedback_entries.append(entry)
            st.success("反馈已保存在本地 session，可在 Export 下载。")

        if st.session_state.pilot_feedback_entries:
            st.subheader("Local Entries")
            st.table(
                [
                    {
                        "日期": item["review_date"],
                        "角色": item["reviewer_role"],
                        "Setup": item["ratings"]["setup_clarity"],
                        "Measure": item["ratings"]["measurement_realism"],
                        "Trust": item["ratings"]["trust"],
                        "Action": item["ratings"]["actionability"],
                        "Visual": item["ratings"]["visual_polish"],
                    }
                    for item in st.session_state.pilot_feedback_entries
                ]
            )

    with export_tab:
        st.subheader("Export")
        alpha_template = build_alpha_dataset_template()
        alpha_csv_templates = alpha_dataset_csv_templates(alpha_template)
        _alpha_dataset_template_console(alpha_template)
        st.dataframe(_alpha_dataset_table_rows(alpha_template), hide_index=True, width="stretch")
        st.download_button(
            "下载 Alpha Dataset Dictionary",
            alpha_dataset_dictionary_markdown(alpha_template),
            file_name="sportrx_alpha_dataset_dictionary.md",
            mime="text/markdown",
        )
        alpha_cols = st.columns(2)
        for index, table in enumerate(alpha_template["tables"]):
            with alpha_cols[index % 2]:
                st.download_button(
                    f"下载 {table['id']} CSV",
                    alpha_csv_templates[table["id"]],
                    file_name=table["filename"],
                    mime="text/csv",
                    key=f"alpha_dataset_{table['id']}",
                )
        st.divider()
        st.download_button(
            "下载 Pilot Feedback JSON",
            export_pilot_feedback_json(st.session_state.pilot_feedback_entries),
            file_name="sportrx_pilot_feedback.json",
            mime="application/json",
        )
        st.download_button(
            "下载 Pilot Feedback Markdown",
            pilot_feedback_markdown(st.session_state.pilot_feedback_entries),
            file_name="sportrx_pilot_feedback.md",
            mime="text/markdown",
        )


def _apply_v01_theme() -> None:
    """Override legacy Labs styles for the focused mobile prescription product."""

    st.markdown(
        """
        <style>
        :root {
            --v01-ink: #14261f;
            --v01-muted: #617169;
            --v01-line: #d5ddd7;
            --v01-canvas: #f4f6f2;
            --v01-panel: #ffffff;
            --v01-green: #0c5a40;
            --v01-lime: #b9e639;
            --v01-blue: #2a6b9f;
            --v01-alert: #b54c2e;
        }
        [data-testid="stAppViewContainer"] { background: var(--v01-canvas) !important; color: var(--v01-ink) !important; }
        [data-testid="stHeader"] { background: rgba(244, 246, 242, 0.92) !important; }
        .block-container { width: min(100%, 430px) !important; max-width: 430px !important; padding: 1.15rem 1rem 2.4rem !important; }
        [data-testid="stMainBlockContainer"] { padding-left: 0 !important; padding-right: 0 !important; }
        h1, h2, h3, p, li, label, [data-testid="stCaptionContainer"], [data-testid="stMarkdownContainer"] { color: var(--v01-ink) !important; }
        h1 { font-size: 1.86rem !important; line-height: 1.08 !important; font-weight: 820 !important; margin: 0.28rem 0 0.35rem !important; }
        h2 { font-size: 1.22rem !important; margin-top: 1.55rem !important; }
        h3 { font-size: 1rem !important; margin-top: 1.35rem !important; }
        [data-testid="stCaptionContainer"] p { color: var(--v01-muted) !important; font-size: 0.82rem !important; line-height: 1.45 !important; }
        [data-testid="stNumberInput"] label, [data-testid="stSelectbox"] label, [data-testid="stRadio"] label, [data-testid="stSlider"] label, [data-testid="stCheckbox"] label { color: var(--v01-ink) !important; font-size: 0.88rem !important; font-weight: 720 !important; }
        [data-testid="stNumberInput"] input, [data-testid="stSelectbox"] input { color: var(--v01-ink) !important; background: var(--v01-panel) !important; border: 1px solid var(--v01-line) !important; border-radius: 8px !important; min-height: 48px !important; font-size: 1rem !important; }
        [data-testid="stNumberInput"] button { color: var(--v01-green) !important; background: #edf5ef !important; border-color: var(--v01-line) !important; }
        [data-testid="stRadio"] [role="radiogroup"] { gap: 0.6rem !important; }
        [data-testid="stRadio"] label { background: var(--v01-panel) !important; border: 1px solid var(--v01-line) !important; border-radius: 8px !important; padding: 0.68rem 0.72rem !important; min-height: 46px !important; align-items: center !important; }
        [data-testid="stRadio"] label:has(input:checked) { border-color: var(--v01-green) !important; background: #eef7f1 !important; }
        [data-testid="stCheckbox"] label { font-weight: 600 !important; }
        [data-testid="stSlider"] [data-baseweb="slider"] { padding: 0.75rem 0.25rem 0.35rem !important; }
        [data-testid="stButton"] > button, [data-testid="stFormSubmitButton"] > button { min-height: 48px !important; border-radius: 8px !important; font-size: 0.94rem !important; font-weight: 780 !important; letter-spacing: 0 !important; border: 1px solid var(--v01-line) !important; color: var(--v01-ink) !important; background: var(--v01-panel) !important; box-shadow: none !important; }
        [data-testid="stButton"] > button[kind="primary"], [data-testid="stFormSubmitButton"] > button[kind="primary"] { color: #ffffff !important; background: var(--v01-green) !important; border-color: var(--v01-green) !important; }
        [data-testid="stButton"] > button[kind="primary"] p, [data-testid="stFormSubmitButton"] > button[kind="primary"] p { color: #ffffff !important; }
        [data-testid="stExpander"] { border: 1px solid var(--v01-line) !important; border-radius: 8px !important; background: var(--v01-panel) !important; box-shadow: none !important; }
        [data-testid="stExpander"] details, [data-testid="stExpander"] summary { background: var(--v01-panel) !important; color: var(--v01-ink) !important; }
        [data-testid="stExpander"] summary { min-height: 48px !important; padding: 0.76rem 0.88rem !important; }
        [data-testid="stExpander"] summary *, [data-testid="stExpander"] summary [data-testid="stMarkdownContainer"] p { color: var(--v01-ink) !important; font-weight: 760 !important; }
        [data-testid="stExpanderDetails"] { background: var(--v01-panel) !important; padding: 0 0.9rem 0.35rem !important; }
        [data-testid="stAlert"] { border-radius: 8px !important; }
        [data-testid="stRadioGroup"][aria-label="页面导航"] { display: grid !important; grid-template-columns: repeat(4, minmax(0, 1fr)) !important; gap: 0.45rem !important; width: 100% !important; }
        [data-testid="stRadioGroup"][aria-label="页面导航"] [data-testid="stRadioOption"] { display: flex !important; justify-content: center !important; min-width: 0 !important; margin: 0 !important; padding: 0.66rem 0.35rem !important; background: var(--v01-panel) !important; border: 1px solid var(--v01-line) !important; border-radius: 8px !important; }
        [data-testid="stRadioGroup"][aria-label="页面导航"] [data-testid="stRadioOption"][data-selected="true"] { background: #eef7f1 !important; border-color: var(--v01-green) !important; }
        [data-testid="stRadioGroup"][aria-label="页面导航"] [data-testid="stRadioOption"] > div > div > div:first-child { display: none !important; }
        [data-testid="stRadioGroup"][aria-label="页面导航"] [data-testid="stMarkdownContainer"] p { color: var(--v01-ink) !important; font-size: 0.8rem !important; font-weight: 760 !important; white-space: nowrap !important; }
        .v01-brand { color: var(--v01-green); font-size: 0.76rem; font-weight: 850; letter-spacing: 0.1em; text-transform: uppercase; margin-top: 0.75rem; }
        .v01-page-head { background: var(--v01-ink); color: #ffffff; padding: 1.3rem 1.2rem 1.25rem; border-radius: 8px; margin: 1rem 0 1.15rem; border: 1px solid #14261f; }
        .v01-page-head .v01-eyebrow { color: var(--v01-lime); font-size: 0.68rem; font-weight: 830; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.55rem; }
        .v01-page-head .v01-title { color: #ffffff; font-size: 1.38rem; font-weight: 800; line-height: 1.2; }
        .v01-page-head .v01-copy { color: #dce7e0; font-size: 0.84rem; line-height: 1.48; margin-top: 0.55rem; }
        .v01-nav-label { color: var(--v01-muted); font-size: 0.72rem; font-weight: 700; margin: 0.8rem 0 0.42rem; }
        .v01-stepper { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.4rem; margin: 0.65rem 0 1.2rem; }
        .v01-step { border-top: 3px solid #d7e0da; color: var(--v01-muted); font-size: 0.72rem; padding-top: 0.42rem; }
        .v01-step-active { border-top-color: var(--v01-green); color: var(--v01-green); font-weight: 800; }
        .v01-section-note { color: var(--v01-muted); font-size: 0.8rem; line-height: 1.45; margin: -0.25rem 0 0.82rem; }
        .v01-stat-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.65rem; margin: 0.9rem 0 1.1rem; }
        .v01-stat { background: var(--v01-panel); border-top: 3px solid var(--v01-green); padding: 0.9rem; }
        .v01-stat-label { color: var(--v01-muted); font-size: 0.72rem; }
        .v01-stat-value { color: var(--v01-ink); font-size: 1.05rem; font-weight: 820; line-height: 1.22; margin-top: 0.3rem; }
        .v01-stat-copy { color: var(--v01-muted); font-size: 0.76rem; line-height: 1.35; margin-top: 0.38rem; }
        .v01-week { background: var(--v01-panel); border: 1px solid var(--v01-line); border-left: 4px solid var(--v01-green); padding: 0.9rem 0.92rem 0.25rem; margin: 0.78rem 0 0; }
        .v01-week-title { color: var(--v01-ink); font-size: 1rem; font-weight: 830; }
        .v01-week-meta { color: var(--v01-muted); font-size: 0.76rem; line-height: 1.4; margin-top: 0.28rem; }
        .v01-today-session { border: 1px solid #aac8b7; border-left: 6px solid var(--v01-green); background: #ffffff; padding: 1.05rem 1rem; margin: 0.95rem 0; }
        .v01-session-kicker { color: var(--v01-green); font-size: 0.72rem; font-weight: 820; letter-spacing: 0.04em; }
        .v01-session-title { color: var(--v01-ink); font-size: 1.36rem; font-weight: 830; line-height: 1.18; margin-top: 0.32rem; }
        .v01-session-detail { color: var(--v01-muted); font-size: 0.86rem; line-height: 1.5; margin-top: 0.45rem; }
        .v01-rule-list { border-top: 1px solid var(--v01-line); margin: 1rem 0; }
        .v01-rule { display: grid; grid-template-columns: 70px minmax(0, 1fr); gap: 0.55rem; padding: 0.75rem 0; border-bottom: 1px solid var(--v01-line); }
        .v01-rule-label { color: var(--v01-green); font-size: 0.76rem; font-weight: 800; }
        .v01-rule-copy { color: var(--v01-muted); font-size: 0.82rem; line-height: 1.42; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _v01_page_header(title: str, subtitle: str) -> None:
    st.markdown(
        (
            '<section class="v01-page-head">'
            '<div class="v01-eyebrow">SportRX / 有氧 v0.1</div>'
            f'<div class="v01-title">{escape(title)}</div>'
            f'<div class="v01-copy">{escape(subtitle)}</div>'
            '</section>'
        ),
        unsafe_allow_html=True,
    )


def _v01_nav() -> None:
    pages = [("设置", "设置"), ("计划", "计划"), ("今天", "今天"), ("进度", "进度")]
    st.markdown('<div class="v01-nav-label">你的训练</div>', unsafe_allow_html=True)
    page_ids = [page_id for page_id, _label in pages]
    selected = st.radio(
        "页面导航",
        page_ids,
        index=page_ids.index(st.session_state.v01_page),
        format_func=lambda page_id: dict(pages)[page_id],
        horizontal=True,
        label_visibility="collapsed",
        key=f"v01_nav_{st.session_state.v01_page}",
    )
    if selected != st.session_state.v01_page:
        st.session_state.v01_page = selected
        st.rerun()


def _v01_setup_page() -> None:
    step = int(st.session_state.v01_setup_step)
    draft = st.session_state.v01_draft
    headers = {
        1: ("你的运动起点", "先从最近 4 周开始。我们不会用模糊的“基础好不好”来猜。"),
        2: ("把计划装进你的日程", "训练必须先适合你的真实时间，才有可能坚持。"),
        3: ("最后做一次开始前确认", "这一步只决定能否继续自动生成计划，不提供医疗判断。"),
    }
    _v01_page_header(*headers[step])
    step_names = ["运动近况", "时间与偏好", "开始前确认"]
    st.markdown(
        '<div class="v01-stepper">'
        + "".join(
            f'<div class="v01-step {"v01-step-active" if index == step else ""}">{index}. {escape(name)}</div>'
            for index, name in enumerate(step_names, start=1)
        )
        + '</div>',
        unsafe_allow_html=True,
    )

    if step == 1:
        st.markdown('<div class="v01-section-note">这些数字决定第 1 周从多大总量开始。</div>', unsafe_allow_html=True)
        with st.form("v01_profile_step_one"):
            age = st.number_input("年龄", min_value=18, max_value=64, value=int(draft.get("age", 30)), step=1)
            activity_days = st.number_input(
                "最近 4 周，平均每周运动几天",
                min_value=0,
                max_value=7,
                value=int(draft.get("exercise_days_last_4w", 0)),
                step=1,
                help="包含快走、慢跑、骑行等中等或更高强度活动。",
            )
            mvpa_minutes = st.number_input(
                "最近 4 周，平均每周中高强度运动分钟数",
                min_value=0,
                max_value=600,
                value=int(draft.get("mvpa_minutes_per_week", 0)),
                step=5,
            )
            next_step = st.form_submit_button("下一步：安排时间", type="primary", width="stretch")
        if next_step:
            draft.update({"age": int(age), "exercise_days_last_4w": int(activity_days), "mvpa_minutes_per_week": int(mvpa_minutes)})
            _v01_set_setup_step(2)
            st.rerun()
        return

    if step == 2:
        st.markdown('<div class="v01-section-note">这些限制会决定每周练几次、每次多长。</div>', unsafe_allow_html=True)
        with st.form("v01_profile_step_two"):
            available_days = st.number_input(
                "未来每周能安排几天",
                min_value=1,
                max_value=7,
                value=int(draft.get("available_days_per_week", 3)),
                step=1,
            )
            max_minutes = st.number_input(
                "每次最多能安排多少分钟",
                min_value=10,
                max_value=120,
                value=int(draft.get("max_minutes_per_session", 30)),
                step=5,
            )
            activity_options = list(V01_ACTIVITY_LABELS)
            current_activity = str(draft.get("preferred_activity", "brisk walking"))
            preferred_activity = st.selectbox(
                "你更愿意用哪种方式完成有氧训练",
                activity_options,
                index=activity_options.index(current_activity) if current_activity in activity_options else 0,
                format_func=_v01_activity,
            )
            resting_hr = st.number_input(
                "静息心率（可选，知道时再填）",
                min_value=0,
                max_value=120,
                value=int(draft.get("resting_hr", 0) or 0),
                step=1,
                help="留空时，计划只使用 RPE 和说话测试。",
            )
            back, next_step = st.columns(2)
            with back:
                previous = st.form_submit_button("上一步", width="stretch")
            with next_step:
                continue_to_safety = st.form_submit_button("下一步：开始前确认", type="primary", width="stretch")
        if previous:
            _v01_set_setup_step(1)
            st.rerun()
        if continue_to_safety:
            draft.update({"available_days_per_week": int(available_days), "max_minutes_per_session": int(max_minutes), "preferred_activity": preferred_activity, "resting_hr": int(resting_hr)})
            _v01_set_setup_step(3)
            st.rerun()
        return

    st.markdown('<div class="v01-section-note">遇到需要进一步确认的情况，SportRX 会停在这里，不会猜测或继续加量。</div>', unsafe_allow_html=True)
    with st.form("v01_profile_step_three"):
        has_warning_symptoms = st.radio(
            "运动时是否出现过胸痛、异常气短、头晕或晕厥等警示情况？",
            ["没有", "有或不确定"],
            horizontal=True,
        )
        has_relevant_condition = st.radio(
            "目前是否有心血管、代谢、肾脏或肺部疾病需要专业人员管理？",
            ["没有", "有或不确定"],
            horizontal=True,
        )
        back, generate = st.columns(2)
        with back:
            previous = st.form_submit_button("上一步", width="stretch")
        with generate:
            submitted = st.form_submit_button("生成 4 周计划", type="primary", width="stretch")
    if previous:
        _v01_set_setup_step(2)
        st.rerun()
    if submitted:
        st.session_state.v01_profile = {
            **draft,
            "goal": "Improve aerobic fitness / general health",
            "symptoms": ["reported_warning_symptom"] if has_warning_symptoms != "没有" else [],
            "known_conditions": ["reported_relevant_condition"] if has_relevant_condition != "没有" else [],
        }
        st.session_state.v01_feedback_by_week = {}
        _v01_refresh_plan()
        _v01_set_page("计划")
        _v01_set_setup_step(1)
        st.rerun()

    st.caption("v0.1 只面向 18-64 岁、表观健康成年人，只生成有氧训练起点。它不提供疾病诊断、医疗许可或紧急建议。")


def _v01_plan_page() -> None:
    plan = st.session_state.v01_plan
    if not isinstance(plan, dict):
        _v01_page_header("你的 4 周计划", "先完成基础设置，SportRX 才能计算可执行的起点。")
        st.button("去填写基本信息", type="primary", width="stretch", on_click=_v01_set_page, args=("设置",))
        return

    safety = plan["safety"]
    if not safety.get("auto_prescription"):
        _v01_page_header("暂不自动生成计划", "当前信息不适合继续自动处方。")
        for reason in safety.get("reasons", []):
            st.warning(zh(reason))
        st.info("SportRX 不判断原因，也不替代专业评估。确认适合开始或调整运动后，再回来重新设置。")
        st.button("返回设置", type="primary", width="stretch", on_click=_v01_set_page, args=("设置",))
        return

    assessment = plan["assessment"]
    intensity = plan["intensity"]
    _v01_page_header(
        "你的 4 周有氧计划",
        "从现在可做到的训练量开始，再根据完成情况和 RPE 调整下一周。",
    )
    st.markdown(
        (
            '<div class="v01-stat-grid">'
            f'<section class="v01-stat"><div class="v01-stat-label">当前运动状态</div><div class="v01-stat-value">{escape(_v01_fitness_class(assessment["fitness_class"]))}</div><div class="v01-stat-copy">基于最近 4 周的运动天数和分钟数。</div></section>'
            f'<section class="v01-stat"><div class="v01-stat-label">本周强度</div><div class="v01-stat-value">{escape(_v01_intensity(intensity["level"]))}</div><div class="v01-stat-copy">RPE {intensity["rpe_0_10"][0]}–{intensity["rpe_0_10"][1]}；{escape(_v01_talk_test(intensity["level"]))}</div></section>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )
    if intensity.get("hrr_target_zone_bpm"):
        zone = intensity["hrr_target_zone_bpm"]
        st.caption(f"若静息心率记录可靠，可参考目标心率：{zone[0]}–{zone[1]} 次/分。RPE 仍是主要执行依据。")

    for week in plan["weeks"]:
        weekly_status = (
            "起始计划"
            if week["week"] == 1
            else ("等待第 %s 周反馈" % (week["week"] - 1) if week["week"] - 1 not in st.session_state.v01_feedback_by_week else "已按反馈更新")
        )
        st.markdown(
            (
                '<section class="v01-week">'
                f'<div class="v01-week-title">第 {week["week"]} 周 · {week["weekly_minutes"]} 分钟</div>'
                f'<div class="v01-week-meta">{escape(weekly_status)}</div>'
                '</section>'
            ),
            unsafe_allow_html=True,
        )
        st.markdown(
            (
                '<div class="v01-rule-list">'
                f'<div class="v01-rule"><div class="v01-rule-label">训练量</div><div class="v01-rule-copy">每周 {week["frequency_per_week"]} 次，每次约 {week["duration_min"]} 分钟，总计 {week["weekly_minutes"]} 分钟。</div></div>'
                f'<div class="v01-rule"><div class="v01-rule-label">执行方式</div><div class="v01-rule-copy">{escape(_v01_activity(week["fitt_vp"]["type"]))} · {escape(_v01_intensity(week["fitt_vp"]["intensity"]))}</div></div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )
        for session in week["sessions"]:
            st.write(
                f"{zh(session['day'])}：{_v01_activity(session['activity'])} {session['duration_min']} 分钟，"
                f"RPE {session['rpe_0_10'][0]}–{session['rpe_0_10'][1]}。"
            )

    st.subheader("为什么是这个计划？")
    st.markdown(
        (
            '<div class="v01-rule-list">'
            f'<div class="v01-rule"><div class="v01-rule-label">起点</div><div class="v01-rule-copy">你的近期运动状态：{escape(zh(assessment["summary"]))}</div></div>'
            f'<div class="v01-rule"><div class="v01-rule-label">限制</div><div class="v01-rule-copy">第 1 周总量为 {plan["weeks"][0]["weekly_minutes"]} 分钟，受你的可训练天数与单次时间限制。</div></div>'
            '<div class="v01-rule"><div class="v01-rule-label">调整</div><div class="v01-rule-copy">第 2–4 周不是固定处方；填写完成率和 RPE 后，系统才会更新相应周次。</div></div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )
    st.button("查看今天练什么", type="primary", width="stretch", on_click=_v01_set_page, args=("今天",))


def _v01_today_page() -> None:
    plan = st.session_state.v01_plan
    if not isinstance(plan, dict) or not plan.get("weeks") or not plan.get("safety", {}).get("auto_prescription"):
        _v01_page_header("今天，先把起点找准", "用最近 4 周的活动和你真正拥有的时间，生成第一份有氧训练安排。")
        st.markdown(
            """
            <div class="v01-rule-list">
              <div class="v01-rule"><div class="v01-rule-label">第 1 步</div><div class="v01-rule-copy">填写近期运动量。SportRX 不会猜测你的体能基础。</div></div>
              <div class="v01-rule"><div class="v01-rule-label">第 2 步</div><div class="v01-rule-copy">计划会匹配你的可训练天数和每次时间。</div></div>
              <div class="v01-rule"><div class="v01-rule-label">第 3 步</div><div class="v01-rule-copy">训练后记录 RPE 与完成情况，下一周才会调整。</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button("开始创建我的计划", type="primary", width="stretch", on_click=_v01_set_page, args=("设置",))
        return
    _v01_page_header("今天的训练", "从第 1 周开始；完成后在「进度」记录本周完成情况和平均 RPE。")
    week_numbers = [week["week"] for week in plan["weeks"] if week.get("sessions")]
    selected_week = st.selectbox("选择训练周", week_numbers, format_func=lambda value: f"第 {value} 周")
    week = next(item for item in plan["weeks"] if item["week"] == selected_week)
    session = week["sessions"][0]
    st.markdown(
        (
            '<section class="v01-today-session">'
            f'<div class="v01-session-kicker">第 {selected_week} 周 · {escape(zh(session["day"]))}</div>'
            f'<div class="v01-session-title">{escape(_v01_activity(session["activity"]))} · {session["duration_min"]} 分钟</div>'
            f'<div class="v01-session-detail">目标强度：{escape(_v01_intensity(session["intensity"]))}<br>RPE {session["rpe_0_10"][0]}–{session["rpe_0_10"][1]} · {escape(_v01_talk_test(session["intensity"]))}</div>'
            '</section>'
        ),
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="v01-rule-list">
          <div class="v01-rule"><div class="v01-rule-label">开始前</div><div class="v01-rule-copy">用轻松走或轻松骑行热身 5–10 分钟。</div></div>
          <div class="v01-rule"><div class="v01-rule-label">过程中</div><div class="v01-rule-copy">以完成整段训练为优先；任何异常不适都应停止。</div></div>
          <div class="v01-rule"><div class="v01-rule-label">结束后</div><div class="v01-rule-copy">周末记录实际完成次数和平均 RPE，决定下一周如何调整。</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.button("记录本周反馈", type="primary", width="stretch", on_click=_v01_set_page, args=("进度",))


def _v01_progress_page() -> None:
    plan = st.session_state.v01_plan
    if not isinstance(plan, dict) or not plan.get("weeks") or not plan.get("safety", {}).get("auto_prescription"):
        _v01_page_header("本周反馈", "先生成一份 4 周计划。")
        st.button("去设置", type="primary", width="stretch", on_click=_v01_set_page, args=("设置",))
        return
    _v01_page_header("根据反馈调整下一周", "每周只记录四项：完成次数、平均 RPE、是否明显偏难、是否出现异常。")
    feedback_weeks = [week["week"] for week in plan["weeks"] if week["week"] < 4 and week["frequency_per_week"] > 0]
    if not feedback_weeks:
        st.info("当前没有可继续调整的周次。")
        return
    feedback_week = st.selectbox("本周", feedback_weeks, format_func=lambda value: f"第 {value} 周")
    planned_sessions = next(item for item in plan["weeks"] if item["week"] == feedback_week)["frequency_per_week"]
    existing = st.session_state.v01_feedback_by_week.get(int(feedback_week), {})
    with st.form("v01_weekly_feedback"):
        completed_sessions = st.number_input(
            "实际完成了几次训练",
            min_value=0,
            max_value=int(planned_sessions),
            value=int(existing.get("completed_sessions", planned_sessions)),
            step=1,
        )
        average_rpe = st.slider(
            "这一周的平均 RPE",
            min_value=0.0,
            max_value=10.0,
            value=float(existing.get("average_rpe", 5.0)),
            step=0.5,
        )
        felt_too_hard = st.checkbox("这一周明显偏难", value=bool(existing.get("felt_too_hard", False)))
        adverse_event = st.checkbox("训练中出现异常不适或不良事件", value=bool(existing.get("adverse_event", False)))
        submitted = st.form_submit_button("保存并更新下一周", type="primary", width="stretch")
    if submitted:
        st.session_state.v01_feedback_by_week[int(feedback_week)] = {
            "completed_sessions": int(completed_sessions),
            "average_rpe": float(average_rpe),
            "felt_too_hard": bool(felt_too_hard),
            "adverse_event": bool(adverse_event),
        }
        _v01_refresh_plan()
        if adverse_event:
            st.error("已暂停自动调整。SportRX 不判断原因，也不提供继续训练建议。")
        else:
            st.success("周反馈已保存，下一周已按规则重新计算。")
        plan = st.session_state.v01_plan

    decisions = {item["after_week"]: item["decision"] for item in plan.get("progression_log", [])}
    decision = decisions.get(int(feedback_week))
    if decision and decision.get("completion_rate") is not None and decision.get("average_rpe") is not None:
        action_labels = {"increase": "增加训练量", "small_increase": "小幅进阶", "hold": "维持", "decrease": "降低训练量", "pause": "暂停自动调整"}
        st.markdown(
            (
                '<section class="v01-today-session">'
                '<div class="v01-session-kicker">下一周建议</div>'
                f'<div class="v01-session-title">{escape(action_labels.get(decision["action"], decision["action"]))}</div>'
                f'<div class="v01-session-detail">完成率 {round(float(decision["completion_rate"]) * 100)}%；平均 RPE {decision["average_rpe"]}。<br>{escape(zh(decision["rationale"]))}</div>'
                '</section>'
            ),
            unsafe_allow_html=True,
        )
    else:
        st.info("保存这一周反馈后，这里会显示下一周的规则解释。")

    if st.session_state.v01_feedback_by_week:
        st.subheader("已记录的周反馈")
        rows = []
        for week, feedback in sorted(st.session_state.v01_feedback_by_week.items()):
            rows.append(
                {
                    "周次": f"第 {week} 周",
                    "完成次数": feedback["completed_sessions"],
                    "平均 RPE": feedback["average_rpe"],
                    "明显偏难": "是" if feedback["felt_too_hard"] else "否",
                }
            )
        st.dataframe(rows, hide_index=True, width="stretch")


def aerobic_v01_app() -> None:
    """Render the original, aerobic-prescription-first SportRX product flow."""

    _v01_state_defaults()
    _apply_theme()
    _apply_v01_theme()
    st.markdown('<div class="v01-brand">SportRX</div>', unsafe_allow_html=True)
    st.title("4 周有氧运动处方")
    st.caption("循证、可解释、可调整。只面向表观健康成年人，只做有氧。")
    _v01_nav()
    page = st.session_state.v01_page
    if page == "设置":
        _v01_setup_page()
    elif page == "计划":
        _v01_plan_page()
    elif page == "今天":
        _v01_today_page()
    else:
        _v01_progress_page()


def main() -> None:
    st.set_page_config(page_title="SportRX", layout="wide")
    if _product_mode() == "aerobic_v01":
        aerobic_v01_app()
        return
    _state_defaults()
    _apply_theme()

    st.sidebar.title("SportRX Labs")
    language_options = language_edition_options(include_internal=_internal_review_enabled())
    if _public_preview_enabled():
        language_options = ["zh_user"]
    current_language = _language_id()
    if current_language not in language_options:
        current_language = "zh_user"
        st.session_state.language_edition = current_language
    st.sidebar.selectbox(
        ui_text("language_selector", current_language),
        language_options,
        index=language_options.index(current_language),
        format_func=language_edition_label,
        key="language_edition",
    )
    st.sidebar.caption(_t("sidebar_caption"))
    if _is_internal_edition():
        _language_edition_sidebar()
        with st.sidebar.expander(_t("demo_controls"), expanded=False):
            st.button(_t("load_complete_demo"), width="stretch", type="primary", on_click=_load_demo_state)
            sidebar_scenarios = build_demo_scenarios()
            sidebar_ids = [item["id"] for item in sidebar_scenarios]
            sidebar_scenario = st.selectbox(
                _t("demo_scenario"),
                sidebar_ids,
                format_func=lambda scenario_id: next(item["label"] for item in sidebar_scenarios if item["id"] == scenario_id),
                key="sidebar_demo_scenario_select",
            )
            st.button(
                _t("load_selected_scenario"),
                width="stretch",
                on_click=_load_demo_scenario,
                args=(sidebar_scenario,),
                key="sidebar_load_demo_scenario",
            )
            st.button(_t("reset_prototype"), width="stretch", on_click=_reset_prototype_state)
            if st.session_state.demo_claim_boundary:
                st.caption(st.session_state.demo_claim_boundary)
        with st.sidebar.expander(_t("session_snapshot"), expanded=False):
            snapshot = build_session_snapshot(
                st.session_state.profile,
                st.session_state.benchmark_sessions,
                st.session_state.feedback_by_week,
                st.session_state.pilot_feedback_entries,
            )
            st.caption(snapshot["claim_boundary"])
            st.download_button(
                _t("download_snapshot_json"),
                session_snapshot_json(snapshot),
                file_name="sportrx_session_snapshot.json",
                mime="application/json",
                width="stretch",
            )
            st.download_button(
                _t("download_snapshot_summary"),
                session_snapshot_markdown(snapshot),
                file_name="sportrx_session_snapshot.md",
                mime="text/markdown",
                width="stretch",
            )
            uploaded_snapshot = st.file_uploader(_t("import_snapshot"), type=["json"], key="session_snapshot_upload")
            if uploaded_snapshot is not None and st.button(_t("restore_snapshot"), width="stretch"):
                try:
                    payload = json.loads(uploaded_snapshot.getvalue().decode("utf-8"))
                    restored = restore_session_snapshot(payload)
                    st.session_state.profile = restored["profile"]
                    st.session_state.benchmark_sessions = restored["benchmark_sessions"]
                    st.session_state.feedback_by_week = restored["feedback_by_week"]
                    st.session_state.pilot_feedback_entries = restored["pilot_feedback_entries"]
                    st.session_state.demo_claim_boundary = "Session snapshot restored locally. Outputs are recalculated from saved inputs."
                    st.session_state.page = "Workbench"
                    _refresh_outputs()
                    st.success(_t("snapshot_restored"))
                except (json.JSONDecodeError, UnicodeDecodeError, ValueError, TypeError) as exc:
                    st.error(f"{_t('snapshot_import_failed')}: {exc}")
    internal_page_options = [
        "Workbench",
        "Quick Match",
        "HYROX Check",
        "Benchmark Protocol",
        "Benchmark Log",
        "Training Profile",
        "训练",
        "复测",
        "Pilot Feedback",
        "Evidence Library",
        "Knowledge Lab",
        "Export Center",
        "Release QA",
    ]
    public_page_options = [
        "Workbench",
        "Venue Entry",
        "Benchmark Protocol",
        "Training Profile",
        "训练",
        "复测",
    ]
    if _public_preview_enabled():
        public_page_options = ["Workbench", "Benchmark Protocol", "Training Profile", "训练", "复测"]
    page_options = internal_page_options if _is_internal_edition() else public_page_options
    if st.session_state.page not in page_options:
        st.session_state.page = "Workbench"
    page = st.sidebar.radio(
        _t("navigation"),
        page_options,
        format_func=_page_display_label,
        key="page",
    )
    if _is_internal_edition():
        _workbench_strip()
    _mobile_nav()

    if page == "Workbench":
        if _is_internal_edition():
            workbench_page()
        else:
            public_home_page()
    elif page == "Venue Entry":
        venue_entry_page()
    elif page == "Quick Match":
        if _is_internal_edition():
            discover_page()
        else:
            public_quick_match_page()
    elif page == "HYROX Check":
        lab_page()
    elif page == "Benchmark Protocol":
        if _is_internal_edition():
            benchmark_protocol_page()
        else:
            public_benchmark_page()
    elif page == "Benchmark Log":
        benchmark_log_page()
    elif page == "Training Profile":
        if _is_internal_edition():
            passport_page()
        else:
            public_profile_page()
    elif page == "训练":
        training_page()
    elif page == "复测":
        progress_page()
    elif page == "Pilot Feedback":
        pilot_feedback_page()
    elif page == "Evidence Library":
        evidence_library_page()
    elif page == "Knowledge Lab":
        knowledge_lab_page()
    elif page == "Export Center":
        export_center_page()
    else:
        release_qa_page()


if __name__ == "__main__":
    main()
