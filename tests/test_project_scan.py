from zai_coder.core.project import scan_project


def test_scan_project(tmp_path):
    (tmp_path / "README.md").write_text("# x", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("print(1)", encoding="utf-8")
    scan = scan_project(tmp_path)
    assert scan.files >= 2
    assert ".py" in scan.languages
    assert "README.md" in scan.notable_files
