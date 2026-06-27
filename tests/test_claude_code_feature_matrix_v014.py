from __future__ import annotations

from zai_coder.product.features import (
    CLAUDE_CODE_FEATURES,
    VALID_STATUSES,
    VALID_TIERS,
    feature_matrix_markdown,
    features_by_status,
    validate_feature_claims,
)


def test_claude_code_feature_matrix_has_expected_coverage():
    ids = {feature.id for feature in CLAUDE_CODE_FEATURES}
    for required in {
        "terminal_cli",
        "file_read_write_edit",
        "safe_bash",
        "slash_commands",
        "hooks",
        "subagents",
        "skills",
        "mcp",
        "permissions",
        "ide_integration",
        "artifacts",
    }:
        assert required in ids


def test_claude_code_feature_claims_validate():
    assert validate_feature_claims() == []
    assert {feature.status for feature in CLAUDE_CODE_FEATURES}.issubset(VALID_STATUSES)
    assert {feature.tier_hint for feature in CLAUDE_CODE_FEATURES}.issubset(VALID_TIERS)
    assert features_by_status("available")


def test_claude_code_markdown_exports_claim_control_matrix():
    md = feature_matrix_markdown()
    assert "# Claude Code Feature Coverage" in md
    assert "Terminal CLI" in md
    assert "requires_integration" in md
    assert "Artifacts" in md

