"""External action approval workflow."""

from __future__ import annotations

def require_manual_external_action(action_type: str) -> dict:
    """Enforces that external mutations are manual-only for now."""
    blocked_actions = [
        "publishing",
        "pushing",
        "paid_jobs",
        "third_party_mutations"
    ]
    if action_type in blocked_actions:
        return {
            "ok": False,
            "blocked": True,
            "message": f"Action '{action_type}' is blocked. External actions must be manual until an approved external-action workflow is implemented."
        }
    return {
        "ok": True,
        "blocked": False,
        "message": f"Action '{action_type}' is permitted."
    }
