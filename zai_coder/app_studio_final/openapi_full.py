"""Full OpenAPI schema for final shell."""

from __future__ import annotations

import json

from zai_coder.integration_core.openapi import build_openapi_schema


def build_full_openapi_schema() -> dict:
    schema = build_openapi_schema()
    paths = schema.setdefault("paths", {})
    paths.update({
        "/api/final/status": {"get": {"summary": "Final App Studio status", "responses": {"200": {"description": "OK"}}}},
        "/studio": {"get": {"summary": "Render final home page", "responses": {"200": {"description": "OK"}}}},
        "/studio/plugins": {"get": {"summary": "Render plugin marketplace", "responses": {"200": {"description": "OK"}}}},
        "/studio/workflows": {"get": {"summary": "Render workflow builder", "responses": {"200": {"description": "OK"}}}},
        "/studio/models": {"get": {"summary": "Render model router UI", "responses": {"200": {"description": "OK"}}}},
        "/studio/deployments": {"get": {"summary": "Render deployment control center", "responses": {"200": {"description": "OK"}}}},
        "/api/final/app-generator": {"post": {"summary": "Generate app plan", "responses": {"200": {"description": "OK"}}}},
        "/api/final/audit-search": {"post": {"summary": "Search audit events", "responses": {"200": {"description": "OK"}}}},
    })
    schema["info"]["version"] = "0.12.0"
    schema["info"]["title"] = "ZAI Coder App Studio Final API"
    return schema


def export_full_openapi_json() -> str:
    return json.dumps(build_full_openapi_schema(), indent=2) + "\n"
