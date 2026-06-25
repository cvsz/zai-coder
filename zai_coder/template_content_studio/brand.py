"""Brand and tone rules."""

from __future__ import annotations


DEFAULT_BRAND_RULES = {
    "product_name": "ZAI Coder Control Plane",
    "tone": "professional, precise, helpful",
    "must_include": ["local-first", "review-first"],
    "must_not_claim": ["automatic certification", "audited financial statements", "guaranteed compliance"],
    "external_publish": False,
}


def brand_rules() -> dict:
    return dict(DEFAULT_BRAND_RULES)


def tone_guard(content: str, audience: str = "customer") -> dict:
    lower = content.lower()
    blocked = []
    for claim in DEFAULT_BRAND_RULES["must_not_claim"]:
        if claim in lower:
            blocked.append(f"blocked claim: {claim}")
    if "local-first" not in lower and audience in {"customer", "public"}:
        blocked.append("customer/public content should mention local-first safety")
    return {
        "allowed": not blocked,
        "blocked": blocked,
        "audience": audience,
        "brand_rules": brand_rules(),
    }


def content_safety_gate(rendered_payload: dict, external_publish_requested: bool = False, approval_id: str = "") -> dict:
    blocked = []
    if external_publish_requested:
        blocked.append("external content publishing is disabled")
    if external_publish_requested and not approval_id.startswith("approved_"):
        blocked.append("external publishing would require approval")
    if not rendered_payload.get("dry_run", True):
        blocked.append("rendered content must remain dry-run/export-only")
    tone = tone_guard(rendered_payload.get("content", ""), "customer")
    blocked.extend(tone["blocked"])
    return {"allowed": not blocked, "blocked": blocked, "tone": tone, "content_id": rendered_payload.get("id")}
