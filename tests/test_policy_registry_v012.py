import pytest
from zai_coder.github_ready_core.repo_policy import is_safe_stage_path, find_forbidden_command_text

def test_repo_policy_is_safe_stage_path():
    # Safe paths
    assert is_safe_stage_path("README.md") is True
    assert is_safe_stage_path("zai_coder/server.py") is True
    assert is_safe_stage_path("tests/test_server_routes_v012.py") is True
    
    # Unsafe / blocked path prefixes
    assert is_safe_stage_path("apps/zlms/conf.py") is False
    assert is_safe_stage_path("node_modules/textual/app.py") is False
    assert is_safe_stage_path("dist/zai-coder-standalone-0.1.1.zip") is False
    assert is_safe_stage_path("data/enterprise-admin-console.db") is False
    
    # Unsafe / blocked filenames
    assert is_safe_stage_path("credentials.json") is False
    assert is_safe_stage_path(".env") is False
    assert is_safe_stage_path(".env.production") is False
    
    # Unsafe extensions
    assert is_safe_stage_path("keys/key.pem") is False
    assert is_safe_stage_path("archive.tar.gz") is False
    assert is_safe_stage_path("db.sqlite3") is False
    assert is_safe_stage_path("module.pyc") is False

def test_find_forbidden_commands():
    # Clean text
    assert find_forbidden_command_text("git status") == []
    assert find_forbidden_command_text("git commit -m 'test'") == []
    
    # Text with forbidden commands
    assert find_forbidden_command_text("git add .") == ["git add ."]
    assert find_forbidden_command_text("git add -A") == ["git add -A"]
    assert find_forbidden_command_text("git push --force") == ["push --force"]
    assert find_forbidden_command_text("git commit --no-verify") == ["--no-verify"]
