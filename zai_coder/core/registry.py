from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class RegistryItem:
    name: str
    description: str
    tags: list[str]
    raw: dict[str, Any]


class JsonRegistry:
    def __init__(self, directory: str | Path):
        self.directory = Path(directory)

    def list(self) -> list[RegistryItem]:
        items: list[RegistryItem] = []
        if not self.directory.exists():
            return items
        for path in sorted(self.directory.glob("*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            items.append(RegistryItem(
                name=data.get("name", path.stem),
                description=data.get("description", ""),
                tags=data.get("tags", []),
                raw=data,
            ))
        return items
