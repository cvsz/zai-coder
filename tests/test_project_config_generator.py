import json
from pathlib import Path
from zai_coder.deploy_installer_core.project_config_generator import ProjectConfigGenerator
from zai_coder.cli import main


def test_generator_presets(tmp_path):
    out_file = tmp_path / "config.json"
    generator = ProjectConfigGenerator(out_file)

    # Test OpenAI preset
    cfg = generator.generate_from_preset("openai")
    assert cfg.provider == "openai"
    assert cfg.model == "gpt-4o-mini"
    assert out_file.exists()

    # Verify written JSON matches
    data = json.loads(out_file.read_text(encoding="utf-8"))
    assert data["provider"] == "openai"
    assert data["model"] == "gpt-4o-mini"


def test_generator_preset_overrides(tmp_path):
    out_file = tmp_path / "config.json"
    generator = ProjectConfigGenerator(out_file)

    # Test OpenAI preset with model override
    cfg = generator.generate_from_preset("openai", {"model": "gpt-4-custom"})
    assert cfg.provider == "openai"
    assert cfg.model == "gpt-4-custom"
    
    data = json.loads(out_file.read_text(encoding="utf-8"))
    assert data["model"] == "gpt-4-custom"


def test_generator_custom(tmp_path):
    out_file = tmp_path / "config.json"
    generator = ProjectConfigGenerator(out_file)

    cfg = generator.generate_custom(
        provider="custom-llm",
        base_url="https://custom.api/v1",
        model="custom-v1",
        fallback_models=["fallback-1", "fallback-2"],
        workspace="/tmp/workspace",
        max_tokens=1000,
        temperature=0.5,
        safe_mode=False,
        allow_apps_zlms=True,
        tool_timeout_seconds=60,
    )

    assert cfg.provider == "custom-llm"
    assert cfg.max_tokens == 1000
    assert cfg.safe_mode is False
    assert cfg.allow_apps_zlms is True
    assert cfg.tool_timeout_seconds == 60


def test_generator_cli_preset(tmp_path):
    out_file = tmp_path / "config.json"

    # Test preset via CLI
    args = [
        "config-generator",
        "--preset", "openrouter",
        "--out", str(out_file)
    ]
    exit_code = main(args)
    assert exit_code == 0
    assert out_file.exists()

    data = json.loads(out_file.read_text(encoding="utf-8"))
    assert data["provider"] == "openrouter"
    assert data["model"] == "google/gemini-2.5-flash"


def test_generator_cli_custom(tmp_path):
    out_file = tmp_path / "config.json"

    # Test custom via CLI
    args = [
        "config-generator",
        "--provider", "test-provider",
        "--base-url", "http://test-url",
        "--model", "test-model",
        "--fallback-models", "fall1,fall2",
        "--workspace", str(tmp_path),
        "--max-tokens", "500",
        "--temperature", "0.8",
        "--unsafe",
        "--allow-apps-zlms",
        "--tool-timeout", "90",
        "--out", str(out_file)
    ]
    exit_code = main(args)
    assert exit_code == 0
    assert out_file.exists()

    data = json.loads(out_file.read_text(encoding="utf-8"))
    assert data["provider"] == "test-provider"
    assert data["base_url"] == "http://test-url"
    assert data["model"] == "test-model"
    assert data["fallback_models"] == ["fall1", "fall2"]
    assert data["workspace"] == str(tmp_path)
    assert data["max_tokens"] == 500
    assert data["temperature"] == 0.8
    assert data["safe_mode"] is False
    assert data["allow_apps_zlms"] is True
    assert data["tool_timeout_seconds"] == 90
