"""Safe notification render engine."""

from __future__ import annotations

import re
import uuid

from .models import NotificationDraft
from .templates import notification_template_by_id
from .preferences import preference_decision

VARIABLE_RE = re.compile(r"{{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*}}")
FORBIDDEN_VALUE_TERMS = ("password", "token", "secret", "api key", "credit card")


def extract_notification_variables(text: str) -> list[str]:
    return sorted(set(VARIABLE_RE.findall(text)))


def validate_notification_variables(template: dict, variables: dict) -> dict:
    required = set(template.get("variables", []))
    supplied = set(variables.keys())
    missing = sorted(required - supplied)
    sensitive = []
    for key, value in variables.items():
        if any(term in f"{key} {value}".lower() for term in FORBIDDEN_VALUE_TERMS):
            sensitive.append(key)
    return {"ok": not missing and not sensitive, "missing": missing, "extra": sorted(supplied - required), "sensitive": sensitive}


def render_text(text: str, variables: dict) -> str:
    return VARIABLE_RE.sub(lambda match: str(variables.get(match.group(1), "")), text)


def render_notification_draft(template_id: str, recipient_ref: str, customer_id: str, topic: str, variables: dict) -> NotificationDraft:
    template = notification_template_by_id(template_id)
    template_payload = template.to_dict()
    validation = validate_notification_variables(template_payload, variables)
    if not validation["ok"]:
        raise ValueError(f"invalid notification variables: {validation}")
    pref = preference_decision(customer_id, template.channel, topic)
    if not pref["allowed"]:
        raise ValueError(f"notification preference blocked: {pref}")
    draft = NotificationDraft(
        id=f"nd_{uuid.uuid4().hex[:12]}",
        template_id=template.id,
        channel=template.channel,
        subject=render_text(template.subject, variables),
        body=render_text(template.body, variables),
        recipient_ref=recipient_ref,
        topic=topic,
    )
    issues = draft.validate()
    if issues:
        raise ValueError("; ".join(issues))
    return draft


def render_demo_notification() -> dict:
    draft = render_notification_draft(
        "ntpl-welcome",
        "cust_demo",
        "cust_demo",
        "product",
        {"customer_name": "Demo Customer", "product_name": "ZAI Coder Control Plane", "next_step": "review the local-first onboarding checklist"},
    )
    return {"draft": draft.to_dict(), "variables": extract_notification_variables(notification_template_by_id("ntpl-welcome").body)}
