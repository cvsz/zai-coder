"""Production FastAPI/Starlette app factory.

The app factory imports FastAPI lazily so the source tree can still run tests in
minimal Python environments. Install `requirements-production.txt` for runtime.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from zai_coder.production_hardening_core.server.health import health_payload, readiness_payload
from zai_coder.production_hardening_core.auth.session_store import SessionStore
from zai_coder.production_hardening_core.auth.middleware import require_session_header
from zai_coder.production_hardening_core.ops.logging_config import configure_logging


@dataclass(frozen=True)
class AppSettings:
    app_name: str = "ZAI Coder Control Plane"
    environment: str = "production"
    db_url: str = "sqlite:///data/zai-prod.db"
    session_db_path: str = "data/zai-sessions.db"
    require_session: bool = True

    def to_dict(self) -> dict:
        return {
            "app_name": self.app_name,
            "environment": self.environment,
            "db_url": self.db_url,
            "session_db_path": self.session_db_path,
            "require_session": self.require_session,
        }


def build_route_manifest() -> list[dict]:
    return [
        {"method": "GET", "path": "/healthz", "auth": False},
        {"method": "GET", "path": "/readyz", "auth": False},
        {"method": "GET", "path": "/api/status", "auth": True},
        {"method": "POST", "path": "/api/session/create", "auth": False},
        {"method": "POST", "path": "/api/session/revoke", "auth": True},
    ]


def create_app(settings: AppSettings | None = None) -> Any:
    settings = settings or AppSettings()
    configure_logging()
    try:
        from fastapi import FastAPI, Header, HTTPException
    except ImportError as exc:
        raise RuntimeError("FastAPI runtime missing. Install requirements-production.txt before serving.") from exc

    app = FastAPI(
        title=settings.app_name,
        version="0.13.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )
    sessions = SessionStore(settings.session_db_path)

    @app.get("/healthz")
    def healthz():
        return health_payload(settings.to_dict())

    @app.get("/readyz")
    def readyz():
        return readiness_payload(settings.to_dict())

    @app.get("/api/status")
    def status(x_zai_session: str | None = Header(default=None)):
        if settings.require_session:
            decision = require_session_header(sessions, x_zai_session)
            if not decision.allowed:
                raise HTTPException(status_code=401, detail=decision.reason)
        return {"ok": True, "service": "zai-coder-production", "routes": build_route_manifest()}

    @app.post("/api/session/create")
    def create_session(actor: str = "local-admin"):
        session = sessions.create_session(actor=actor, scopes=("admin", "operator"))
        return {"session_id": session.id, "session_token": session.token, "actor": session.actor}

    @app.post("/api/session/revoke")
    def revoke_session(x_zai_session: str | None = Header(default=None)):
        decision = require_session_header(sessions, x_zai_session)
        if not decision.allowed:
            raise HTTPException(status_code=401, detail=decision.reason)
        sessions.revoke_session(x_zai_session or "")
        return {"ok": True}

    return app
