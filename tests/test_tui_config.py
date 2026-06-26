import json
import pytest

from zai_coder.tui.config import DEFAULT_TUI_CONFIG, TuiConfig, load_tui_config, resolve_tui_config


def test_default_config_loads(tmp_path):
    config = load_tui_config(root=tmp_path)
    assert isinstance(config, TuiConfig)
    assert config["template"] == DEFAULT_TUI_CONFIG["template"]
    assert config.template == DEFAULT_TUI_CONFIG["template"]
    assert config["dry_run_first"] is True
    assert config["state_path"] == ".zai-coder/tui-state.json"


def test_config_override_works(tmp_path):
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "zai-coder.config.json").write_text(
        json.dumps({"tui": {"template": "tui-template-06", "refresh_interval_seconds": 5}}),
        encoding="utf-8",
    )

    config = load_tui_config(root=tmp_path)

    assert config["template"] == "operation-gate"
    assert config["refresh_interval_seconds"] == 5
    assert config["dry_run_first"] is True


def test_invalid_config_template_fails_clearly(tmp_path):
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "zai-coder.config.json").write_text(
        json.dumps({"tui": {"template": "missing"}}),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Invalid TUI template"):
        load_tui_config(root=tmp_path)


def test_resolve_tui_config_applies_overrides():
    config = resolve_tui_config(path=None, overrides={"template": "06", "persist_state": False})
    assert config.template == "operation-gate"
    assert config.persist_state is False
