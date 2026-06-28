"""Health dashboard data and HTML rendering."""

from __future__ import annotations

from html import escape

from .models import HealthSignal


def default_health_signals(execute: bool = False) -> list[HealthSignal]:
    signals = [
        HealthSignal("healthz", True, "localhost endpoint planned"),
        HealthSignal("readyz", True, "readiness planned"),
        HealthSignal("auth", True, "session-protected API foundation"),
        HealthSignal("backup-policy", True, "daily encrypted backup policy"),
        HealthSignal("cloudflare-access", False, "must be enabled before public exposure", "warning"),
    ]
    if execute:
        import urllib.request
        live_signals = []
        for s in signals:
            if s.name in {"healthz", "readyz"}:
                try:
                    urllib.request.urlopen(f"http://127.0.0.1:8765/{s.name}", timeout=1)
                    live_signals.append(HealthSignal(s.name, True, "live check passed", "info"))
                except Exception as e:
                    live_signals.append(HealthSignal(s.name, False, f"live check failed: {e}", "error"))
            else:
                live_signals.append(s)
        return live_signals
    return signals


def health_summary(signals: list[HealthSignal] | None = None) -> dict:
    signals = signals or default_health_signals()
    data = [signal.to_dict() for signal in signals]
    return {
        "ok": all(signal.ok or signal.severity == "warning" for signal in signals),
        "signals": data,
        "warnings": [signal.to_dict() for signal in signals if not signal.ok],
    }


def render_health_dashboard(signals: list[HealthSignal] | None = None) -> str:
    signals = signals or default_health_signals()
    rows = "\n".join(
        f"<tr><td>{escape(s.name)}</td><td>{'OK' if s.ok else 'WARN'}</td><td>{escape(s.severity)}</td><td>{escape(s.value)}</td></tr>"
        for s in signals
    )
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>Health Dashboard</title></head><body>
<h1>Health Dashboard</h1>
<table><thead><tr><th>Name</th><th>Status</th><th>Severity</th><th>Value</th></tr></thead><tbody>{rows}</tbody></table>
</body></html>
"""
