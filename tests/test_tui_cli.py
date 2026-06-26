import os
import subprocess

from zai_coder.cli import main


def test_cli_print_config_exits_zero(capsys):
    assert main(["tui", "--print-config"]) == 0
    assert '"template": "command-center"' in capsys.readouterr().out


def test_cli_list_templates_exits_zero(capsys):
    assert main(["tui", "--list-templates"]) == 0
    output = capsys.readouterr().out
    assert "tui-template-01 command-center" in output
    assert "tui-template-06 operation-gate" in output


def test_cli_no_textual_exits_zero(capsys):
    assert main(["tui", "--template", "command-center", "--no-textual"]) == 0
    assert "Command Center" in capsys.readouterr().out


def test_cli_dry_run_exits_zero_for_all_templates(capsys):
    for template in (
        "command-center",
        "agent-hub",
        "flow-stream",
        "architect-tree",
        "creative-canvas",
        "operation-gate",
    ):
        assert main(["tui", "--template", template, "--dry-run"]) == 0
    output = capsys.readouterr().out
    assert '"mode": "dry-run"' in output
    assert '"name": "operation-gate"' in output


def test_cli_invalid_template_exits_nonzero(capsys):
    assert main(["tui", "--template", "missing", "--dry-run"]) == 2
    assert "Unknown TUI template" in capsys.readouterr().err


def test_cli_textual_missing_path_fails_gracefully(capsys):
    code = main(["tui", "--template", "command-center"])
    if code != 0:
        assert code == 1
        assert "Textual is not installed" in capsys.readouterr().out


def test_installed_launcher_supports_tui_dry_run_after_install(tmp_path):
    env = os.environ.copy()
    env["HOME"] = str(tmp_path)
    env["PREFIX"] = str(tmp_path / "share" / "zai-coder")
    env["APPLY"] = "1"
    subprocess.run(["make", "install", "APPLY=1"], check=True, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    launcher = tmp_path / ".local" / "bin" / "zai-coder"
    result = subprocess.run(
        [str(launcher), "tui", "--template", "operation-gate", "--dry-run"],
        check=False,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    assert result.returncode == 0
    assert '"name": "operation-gate"' in result.stdout
