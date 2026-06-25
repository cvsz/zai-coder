"""Version planning."""

from __future__ import annotations

import re

from .models import ReleaseVersion


VERSION_RE = re.compile(r"^v(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?:-(?P<label>[a-z]+)\.(?P<num>\d+))?$")


def parse_version(version: str) -> dict:
    match = VERSION_RE.match(version)
    if not match:
        raise ValueError(f"invalid semantic version: {version}")
    data = match.groupdict()
    return {
        "major": int(data["major"]),
        "minor": int(data["minor"]),
        "patch": int(data["patch"]),
        "label": data.get("label") or "",
        "num": int(data["num"] or 0),
    }


def next_version(current: str, bump: str = "minor", channel: str = "stable") -> ReleaseVersion:
    parsed = parse_version(current)
    if bump == "major":
        parsed["major"] += 1
        parsed["minor"] = 0
        parsed["patch"] = 0
    elif bump == "minor":
        parsed["minor"] += 1
        parsed["patch"] = 0
    elif bump == "patch":
        parsed["patch"] += 1
    else:
        raise ValueError("bump must be major, minor, or patch")
    version = f"v{parsed['major']}.{parsed['minor']}.{parsed['patch']}"
    if channel in {"alpha", "beta", "rc"}:
        version += f"-{channel}.1"
    return ReleaseVersion(version=version, channel=channel, previous_version=current)


def version_plan(current: str = "v1.0.0", bump: str = "minor", channel: str = "stable") -> dict:
    release = next_version(current, bump, channel)
    return {"dry_run": True, "current": current, "bump": bump, "release": release.to_dict(), "issues": release.validate()}
