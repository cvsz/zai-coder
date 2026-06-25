"""Executive KPI snapshots."""

from __future__ import annotations

from .models import KPI


DEFAULT_KPIS = [
    KPI("ops-tests", "Automated tests passing", 246, "tests", "up", 240, "quality"),
    KPI("ops-modules", "Control-plane modules", 31, "modules", "up", 30, "platform"),
    KPI("security-gates", "Safety gates enabled", 12, "gates", "up", 10, "security"),
    KPI("compliance-controls", "Compliance controls tracked", 5, "controls", "flat", 10, "compliance"),
    KPI("connector-count", "Connector stubs available", 4, "connectors", "flat", 6, "integrations"),
    KPI("release-readiness", "Release readiness score", 85, "percent", "up", 90, "release"),
]


def kpi_snapshot() -> list[dict]:
    return [kpi.to_dict() for kpi in DEFAULT_KPIS]


def kpi_validation_report() -> dict:
    reports = [{"id": kpi.id, "issues": kpi.validate()} for kpi in DEFAULT_KPIS]
    return {"ok": all(not item["issues"] for item in reports), "reports": reports}


def kpi_scorecard(kpis: list[dict] | None = None) -> dict:
    rows = kpis or kpi_snapshot()
    scored = []
    for row in rows:
        target = row.get("target")
        if target in (None, 0):
            attainment = None
            status = "unscored"
        else:
            attainment = min(float(row["value"]) / float(target), 2.0)
            status = "green" if attainment >= 1 else "yellow" if attainment >= 0.75 else "red"
        scored.append({**row, "attainment": attainment, "status": status})
    return {
        "scorecard": scored,
        "counts": {
            "green": sum(1 for row in scored if row["status"] == "green"),
            "yellow": sum(1 for row in scored if row["status"] == "yellow"),
            "red": sum(1 for row in scored if row["status"] == "red"),
            "unscored": sum(1 for row in scored if row["status"] == "unscored"),
        },
    }
