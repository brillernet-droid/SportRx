"""Member-owned venue entry assessment for the SportRX prototype."""

from __future__ import annotations

from typing import Any

from .safety_gate import evaluate_safety_gate
from .screening_provider_registry import get_screening_provider, validate_screening_provider_registry


CLAIM_BOUNDARY = (
    "SportRX Venue Entry is a non-diagnostic routing step. It does not reproduce "
    "or score an external screening instrument, provide medical clearance, diagnose "
    "conditions, estimate risk, or prescribe exercise."
)


def build_venue_entry_assessment(profile: dict[str, Any], *, root: str = ".") -> dict[str, Any]:
    """Return the local-only member result without exposing health answers."""

    safety = evaluate_safety_gate(profile, root=root)
    provider_id = safety.get("screening_provider_id")
    provider = get_screening_provider(provider_id, root=root)
    route = safety["route"]
    if route == "eligible_for_benchmark":
        title = "可继续进入 Benchmark"
        next_action = "进入 SportRX Hybrid Benchmark，先完成至少两个测试维度。"
    elif route == "screening_follow_up_needed":
        title = "需要完成筛查或进一步确认"
        next_action = "暂不进入 Benchmark 或训练路径；请按外部筛查路径的建议完成下一步。"
    else:
        title = "停止 SportRX 自动流程"
        next_action = "不要继续使用 SportRX 的 Benchmark 或训练功能；请寻求适当的专业支持。"

    return {
        "schema": "sportrx.venue_entry_assessment",
        "schema_version": "0.1",
        "title": title,
        "route": route,
        "safety_status": safety["status"],
        "benchmark_allowed": safety["benchmark_allowed"],
        "automated_handoff_allowed": safety["automated_handoff_allowed"],
        "next_action": next_action,
        "deployment_status": safety["deployment_status"],
        "screening_provider": (
            {
                "id": provider["id"],
                "label": provider["label"],
                "version": provider["version"],
                "source_url": provider["source_url"],
                "language": provider["language"],
                "permitted_use": provider["permitted_use"],
                "limitations": provider["limitations"],
            }
            if provider
            else None
        ),
        "provider_member_message": provider.get("member_message") if provider else None,
        "registry": validate_screening_provider_registry(root),
        "member_export": {
            "route": route,
            "safety_status": safety["status"],
            "benchmark_allowed": safety["benchmark_allowed"],
            "deployment_status": safety["deployment_status"],
            "screening_provider_id": provider_id,
            "screening_provider_version": safety.get("screening_provider_version"),
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }
