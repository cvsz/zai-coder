"""Support-deflection helpers."""

from __future__ import annotations

from .search import help_search


def support_deflection_suggestions(ticket_subject: str, ticket_body: str = "") -> dict:
    query = f"{ticket_subject} {ticket_body}".strip()
    search = help_search(query, "customer", 5)
    confidence = "high" if search["results"] and search["results"][0]["score"] >= 3 else "medium" if search["results"] else "low"
    return {
        "query": query,
        "confidence": confidence,
        "suggestions": search["results"],
        "auto_reply": False,
        "send_external_message": False,
    }


def deflection_policy() -> dict:
    return {
        "local_search_only": True,
        "no_auto_reply": True,
        "no_external_email": True,
        "customer_private_filter": True,
        "human_review_required": True,
    }
