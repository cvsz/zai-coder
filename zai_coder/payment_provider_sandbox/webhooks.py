"""Webhook verifier scaffold.

This is a scaffold verifier for sandbox events. It does not validate real
payment-provider signatures unless a sandbox secret is supplied.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import uuid

from .models import WebhookEventDraft


def sign_sandbox_webhook(payload: dict, secret: str = "sandbox_webhook_secret") -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hmac.new(secret.encode("utf-8"), raw, hashlib.sha256).hexdigest()


def verify_sandbox_webhook(payload: dict, signature: str, secret: str = "sandbox_webhook_secret") -> dict:
    expected = sign_sandbox_webhook(payload, secret)
    return {"ok": hmac.compare_digest(expected, signature), "expected_preview": expected[:10] + "...", "signature_preview": (signature or "")[:10] + "..."}


def create_webhook_event_draft(org_id: str, event_type: str = "checkout.session.completed", secret: str = "sandbox_webhook_secret") -> WebhookEventDraft:
    payload = {"org_id": org_id, "event_type": event_type, "mode": "sandbox", "no_real_charge": True}
    return WebhookEventDraft(
        id=f"wh_sandbox_{uuid.uuid4().hex[:12]}",
        provider="sandbox",
        event_type=event_type,
        org_id=org_id,
        payload=payload,
        signature=sign_sandbox_webhook(payload, secret),
    )


def webhook_event_policy() -> dict:
    return {
        "allowed_events": [
            "checkout.session.completed",
            "customer.subscription.created",
            "customer.subscription.updated",
            "customer.subscription.deleted",
            "invoice.payment_failed",
        ],
        "mode": "sandbox-only",
        "real_webhooks_disabled": True,
    }
