"""OpenAPI schema export for integration routes."""

from __future__ import annotations

import json


def build_openapi_schema() -> dict:
    return {
        "openapi": "3.1.0",
        "info": {
            "title": "ZAI Coder Integration Core API",
            "version": "0.10.0",
        },
        "paths": {
            "/api/integrations": {"get": {"summary": "List integration providers", "responses": {"200": {"description": "OK"}}}},
            "/api/integrations/github/status-plan": {"get": {"summary": "Generate GitHub status plan", "responses": {"200": {"description": "OK"}}}},
            "/api/integrations/cloudflare/tunnel-plan": {"get": {"summary": "Generate Cloudflare tunnel validation plan", "responses": {"200": {"description": "OK"}}}},
            "/api/integrations/docker/status-plan": {"get": {"summary": "Generate Docker status plan", "responses": {"200": {"description": "OK"}}}},
            "/api/integrations/social/drafts": {"post": {"summary": "Generate social media drafts", "responses": {"200": {"description": "OK"}}}},
            "/api/saas/status": {"get": {"summary": "Get SaaS system status", "responses": {"200": {"description": "OK"}}}},
            "/api/saas/billing": {"get": {"summary": "Render billing dashboard", "responses": {"200": {"description": "OK"}}}},
            "/api/saas/first-run-plan": {"post": {"summary": "Generate first-run setup plan", "responses": {"200": {"description": "OK"}}}},
        },
    }


def export_openapi_json() -> str:
    return json.dumps(build_openapi_schema(), indent=2) + "\n"
