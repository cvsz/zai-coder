"""Simple schedule registry and fire plan."""

from __future__ import annotations

import uuid

from .models import WorkerSchedule


DEFAULT_SCHEDULES = [
    WorkerSchedule("sched_health", "Health trend snapshot", "maintenance", "health_snapshot", "*/5 * * * *"),
    WorkerSchedule("sched_backup", "Backup plan reminder", "maintenance", "backup_plan", "0 2 * * *"),
    WorkerSchedule("sched_billing", "Usage aggregation", "billing", "usage_aggregate", "0 * * * *"),
]


def schedule_manifest() -> list[dict]:
    return [schedule.to_dict() for schedule in DEFAULT_SCHEDULES]


def schedule_fire_plan(schedule_id: str) -> dict:
    match = next((schedule for schedule in DEFAULT_SCHEDULES if schedule.id == schedule_id), None)
    if not match:
        raise ValueError(f"unknown schedule: {schedule_id}")
    return {
        "dry_run": True,
        "schedule": match.to_dict(),
        "job": {
            "id": f"planned_{uuid.uuid4().hex[:12]}",
            "queue": match.queue,
            "job_type": match.job_type,
            "payload": match.payload,
        },
    }
