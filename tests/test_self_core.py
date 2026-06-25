from pathlib import Path

from zai_coder.cli import build_parser
from zai_coder.core.self_core import (
    SELF_FEATURES,
    feature_summary,
    next_requirements_markdown,
    run_self_doctor,
    runbook,
    self_features_markdown,
)


def test_self_feature_count_and_names():
    names = {feature.name for feature in SELF_FEATURES}
    assert len(names) >= 30
    for required in {
        "self-doctor",
        "self-test",
        "self-heal",
        "self-monitor",
        "self-document",
        "self-host",
        "self-package",
        "self-rollback",
    }:
        assert required in names


def test_self_summary_counts():
    summary = feature_summary()
    assert summary["total"] == len(SELF_FEATURES)
    assert summary["ready"] >= 10
    assert summary["next"] >= 10
    assert summary["read_only"] > 0
    assert summary["mutating"] > 0


def test_self_docs_include_safety_rules():
    md = next_requirements_markdown()
    assert "git add ." in md
    assert "--no-verify" in md
    assert "apps/zlms/**" in md
    assert "self-heal" in md
    assert "self-monitor" in md


def test_self_matrix_markdown():
    md = self_features_markdown()
    assert "Total features" in md
    assert "self-doctor" in md
    assert "self-package" in md


def test_runbook_known_feature():
    md = runbook("self-heal")
    assert "Runbook: self-heal" in md
    assert "dry-run" in md


def test_self_doctor_report_ok():
    report = run_self_doctor(Path(__file__).resolve().parents[1])
    assert report["ok"] is True
    assert report["features"]["total"] >= 30


def test_cli_has_self_commands():
    parser = build_parser()
    for args in (["self", "list"], ["self", "doctor"], ["self", "plan"], ["self", "requirement-next"], ["self", "runbook", "self-doctor"]):
        ns = parser.parse_args(args)
        assert hasattr(ns, "func")
