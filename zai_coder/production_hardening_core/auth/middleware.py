"""Session authorization helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SessionDecision:
    allowed: bool
    reason: str
    actor: str = ""

    def to_dict(self) -> dict:
        return {"allowed": self.allowed, "reason": self.reason, "actor": self.actor}


def require_session_header(session_store, session_token: str | None, required_scope: str = "operator") -> SessionDecision:
    session = session_store.verify_session(session_token)
    if session is None:
        return SessionDecision(False, "missing-or-invalid-session")
    if required_scope not in session.scopes and "admin" not in session.scopes:
        return SessionDecision(False, "missing-required-scope", session.actor)
    return SessionDecision(True, "allowed", session.actor)
