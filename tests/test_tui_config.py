import json

from zai_coder.tui.config import DEFAULT_TUI_CONFIG, load_tui_config


def test_default_config_loads(tmp_path):
    config = load_tui_config(root=tmp_path)
    assert config["template"] == DEFAULT_TUI_CONFIG["template"]
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
