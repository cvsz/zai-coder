"""Board pack builder and exporters."""

from __future__ import annotations

import json
import uuid
from pathlib import Path

from .models import BoardPack
from .sections import board_sections
from .kpis import kpi_snapshot
from .decisions import decision_register, risk_register


def build_board_pack(period: str = "Q1", title: str = "ZAI Coder Enterprise Board Pack") -> BoardPack:
    pack = BoardPack(
        id=f"board_{uuid.uuid4().hex[:12]}",
        period=period,
        title=title,
        sections=tuple(board_sections(period)),
        kpis=tuple(kpi_snapshot()),
        decisions=tuple(decision_register()),
        risks=tuple(risk_register()),
    )
    issues = pack.validate()
    if issues:
        raise ValueError("; ".join(issues))
    return pack


def board_pack_markdown(pack: BoardPack | dict) -> str:
    payload = pack.to_dict() if hasattr(pack, "to_dict") else pack
    sections = "\n\n".join(f"## {section['title']}\n\n{section['body']}" for section in payload["sections"])
    kpis = "\n".join(f"- {k['name']}: {k['value']} {k['unit']} ({k['trend']})" for k in payload["kpis"])
    decisions = "\n".join(f"- {d['title']} — {d['status']} ({d['owner']})" for d in payload["decisions"])
    risks = "\n".join(f"- {r['title']} — {r['severity']} / {r['status']} — mitigation: {r['mitigation']}" for r in payload["risks"])
    return f"""# {payload['title']}

Period: {payload['period']}

{sections}

## KPI Appendix

{kpis}

## Decision Register

{decisions}

## Risk Register

{risks}

## Safety Notice

This board pack is generated from local scaffold data. Review before external use.
"""


def export_board_pack(pack: BoardPack, root: str | Path = ".", out_dir: str = "reports/board-pack") -> dict:
    root = Path(root)
    out = root / out_dir
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / f"{pack.id}.json"
    md_path = out / f"{pack.id}.md"
    json_path.write_text(json.dumps(pack.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(board_pack_markdown(pack), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}


def export_bundle_manifest(pack: BoardPack, exports: dict) -> dict:
    return {
        "kind": "zai-board-pack-bundle",
        "version": "1.0",
        "pack_id": pack.id,
        "period": pack.period,
        "exports": exports,
        "external_publish": False,
        "requires_review": True,
    }
