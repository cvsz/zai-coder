"""Storage backend plans."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from zai_coder.integration_core.models import IntegrationPlan


@dataclass(frozen=True)
class StorageConfig:
    backend: str
    bucket: str = ""
    endpoint_url: str = ""
    region: str = ""

    def validate(self) -> list[str]:
        issues: list[str] = []
        if self.backend not in {"local", "s3", "r2"}:
            issues.append(f"unsupported backend: {self.backend}")
        if self.backend in {"s3", "r2"} and not self.bucket:
            issues.append("bucket is required for s3/r2")
        return issues

    def to_dict(self) -> dict:
        return {"backend": self.backend, "bucket": self.bucket, "endpoint_url": self.endpoint_url, "region": self.region}


def local_storage_plan(path: str = "storage") -> IntegrationPlan:
    p = Path(path)
    warnings = []
    if p.is_absolute() or ".." in p.parts:
        warnings = [f"unsafe local storage path: {path}"]
    return IntegrationPlan(
        provider="storage",
        action="local_storage_plan",
        commands=[f"mkdir -p {path}"],
        payload={"path": path},
        warnings=warnings,
    )


def object_storage_upload_plan(config: StorageConfig, local_path: str, remote_key: str) -> IntegrationPlan:
    warnings = config.validate()
    commands = ["# Configure credentials through environment variables only.", f"aws s3 cp {local_path} s3://{config.bucket}/{remote_key}"]
    if config.backend == "r2" and config.endpoint_url:
        commands[-1] += f" --endpoint-url {config.endpoint_url}"
    return IntegrationPlan(
        provider="storage",
        action="object_upload_plan",
        commands=commands,
        payload={"config": config.to_dict(), "local_path": local_path, "remote_key": remote_key},
        warnings=warnings + ["No credentials are stored in this repository."],
    )
