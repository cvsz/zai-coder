"""Framework-neutral integration route registry."""

from __future__ import annotations

from zai_coder.integration_core.registry import list_integrations
from zai_coder.integration_core.adapters.github_adapter import repo_status_plan, exact_path_publish_plan
from zai_coder.integration_core.adapters.cloudflare_adapter import tunnel_validate_plan
from zai_coder.integration_core.adapters.docker_adapter import docker_status_plan
from zai_coder.integration_core.adapters.huggingface_adapter import model_publish_plan, dataset_upload_plan, space_scaffold_plan
from zai_coder.integration_core.adapters.social_drafts import create_social_drafts
from zai_coder.integration_core.adapters.storage_backends import local_storage_plan, object_storage_upload_plan, StorageConfig
from zai_coder.integration_core.adapters.notifications import email_draft, slack_payload_draft
from zai_coder.integration_core.openapi import build_openapi_schema


def route_integrations() -> dict:
    return {"integrations": list_integrations()}


def route_github_status() -> dict:
    return repo_status_plan().to_dict()


def route_github_publish(payload: dict) -> dict:
    return exact_path_publish_plan(payload.get("paths", []), payload.get("branch", "main")).to_dict()


def route_cloudflare_tunnel() -> dict:
    return tunnel_validate_plan().to_dict()


def route_docker_status() -> dict:
    return docker_status_plan().to_dict()


def route_huggingface_plan(payload: dict) -> dict:
    kind = payload.get("kind", "model")
    repo_id = payload.get("repo_id", "cvsz/zai-coder-demo")
    if kind == "dataset":
        return dataset_upload_plan(repo_id, payload.get("data_dir", "data")).to_dict()
    if kind == "space":
        return space_scaffold_plan(repo_id, payload.get("sdk", "gradio")).to_dict()
    return model_publish_plan(repo_id, payload.get("model_dir", "model")).to_dict()


def route_social_drafts(payload: dict) -> dict:
    return create_social_drafts(payload.get("title", "ZAI Coder"), payload.get("body", "ZAI Coder update")).to_dict()


def route_storage_plan(payload: dict) -> dict:
    backend = payload.get("backend", "local")
    if backend == "local":
        return local_storage_plan(payload.get("path", "storage")).to_dict()
    config = StorageConfig(
        backend=backend,
        bucket=payload.get("bucket", ""),
        endpoint_url=payload.get("endpoint_url", ""),
        region=payload.get("region", ""),
    )
    return object_storage_upload_plan(config, payload.get("local_path", "release/artifact.zip"), payload.get("remote_key", "artifact.zip")).to_dict()


def route_notification(payload: dict) -> dict:
    kind = payload.get("kind", "email")
    if kind == "slack":
        return slack_payload_draft(payload.get("channel", "#general"), payload.get("text", "ZAI update")).to_dict()
    return email_draft(payload.get("to", "admin@example.com"), payload.get("subject", "ZAI update"), payload.get("body", "Done")).to_dict()


def route_openapi() -> dict:
    return build_openapi_schema()
