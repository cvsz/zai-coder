from pathlib import Path

from zai_coder.github_ready_core.secret_scan import scan_repo


def _assignment(name: str, value: str) -> str:
    return f"{name} = {value!r}\n"


def test_secret_scan_skips_virtualenv_and_site_packages(tmp_path: Path) -> None:
    pip_auth = (
        tmp_path
        / ".venv"
        / "lib"
        / "python3.12"
        / "site-packages"
        / "pip"
        / "_internal"
        / "network"
        / "auth.py"
    )
    pip_auth.parent.mkdir(parents=True)
    pip_auth.write_text(_assignment("pass" + "word", "x" * 32), encoding="utf-8")

    app_file = tmp_path / "zai_coder" / "safe.py"
    app_file.parent.mkdir()
    app_file.write_text("VALUE = 'safe'\n", encoding="utf-8")

    report = scan_repo(tmp_path)

    assert report["ok"] is True
    assert report["findings"] == []


def test_secret_scan_still_flags_project_secret_like_assignment(tmp_path: Path) -> None:
    app_file = tmp_path / "zai_coder" / "unsafe.py"
    app_file.parent.mkdir()
    app_file.write_text(_assignment("api" + "_key", "y" * 32), encoding="utf-8")

    report = scan_repo(tmp_path)

    assert report["ok"] is False
    assert report["findings"][0]["path"] == "zai_coder/unsafe.py"
