"""Webhook ingress scaffold for connectors."""

from __future__ import annotations

import hashlib
import hmac
import json
import uuid

from .models import WebhookIngressDraft
from .catalog import find_connector


def sign_webhook_payload(payload: dict, secret: str = "connector_webhook_secret") -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hmac.new(secret.encode("utf-8"), raw, hashlib.sha256).hexdigest()


def verify_webhook_payload(payload: dict, signature: str, secret: str = "connector_webhook_secret") -> dict:
    expected = sign_webhook_payload(payload, secret)
    return {"ok": hmac.compare_digest(expected, signature), "expected_preview": expected[:10] + "...", "signature_preview": (signature or "")[:10] + "..."}


def webhook_ingress_draft(connector_id: str, event_type: str = "connector.event", org_id: str = "org_local", workspace_id: str = "ws_default") -> WebhookIngressDraft:
    connector = find_connector(connector_id)
    if not connector.webhook_supported:
        raise ValueError(f"connector does not support webhooks: {connector_id}")
    return WebhookIngressDraft(
        id=f"whc_{uuid.uuid4().hex[:12]}",
        connector_id=connector_id,
        event_type=event_type,
        org_id=org_id,
        workspace_id=workspace_id,
        payload_schema={"type": "object", "required": ["event_type", "connector_id"]},
        secret_env=f"{connector.provider.upper()}_WEBHOOK_SECRET",
    )


def webhook_policy() -> dict:
    return {
        "mode": "scaffold-only",
        "requires_signature": True,
        "requires_tenant_context": True,
        "external_delivery_disabled_by_default": True,
    }
