"""Retry and dead-letter policy."""

from __future__ import annotations

from .models import WorkerJob


def retry_decision(job: WorkerJob, error_type: str = "transient") -> dict:
    if job.status == "cancelled":
        return {"action": "none", "reason": "job cancelled", "retry": False}
    if error_type in {"validation", "permission", "tenant_denied"}:
        return {"action": "dead_letter", "reason": f"non-retryable: {error_type}", "retry": False}
    if job.attempts >= job.max_attempts:
        return {"action": "dead_letter", "reason": "max attempts reached", "retry": False}
    return {"action": "retry", "reason": "transient retry allowed", "retry": True, "next_attempt": job.attempts + 1}


def dead_letter_payload(job: WorkerJob, reason: str) -> dict:
    return {"job": job.to_dict(), "reason": reason, "status": "dead_letter"}
