import pytest
from pathlib import Path
from zai_coder.core.safety import SafetyPolicy
from zai_coder.github_ready_core.repo_policy import is_safe_stage_path, find_forbidden_command_text
from zai_coder.core.policy_loader import PolicyLoader

def test_safety_policy_block_patterns():
    policy = SafetyPolicy()
    
    # 1. Dangerous git additions
    res1 = policy.check_command("git add .")
    assert not res1.allowed
    assert "exact-path staging" in res1.reason
    
    res2 = policy.check_command("git add -A")
    assert not res2.allowed
    assert "exact-path staging" in res2.reason
    
    # 2. No-verify flags
    res3 = policy.check_command("git commit -m 'update' --no-verify")
    assert not res3.allowed
    assert "bypasses checks" in res3.reason
    
    # 3. Force pushing
    res4 = policy.check_command("git push origin main --force")
    assert not res4.allowed
    assert "force push is disabled" in res4.reason

    res4_lease = policy.check_command("git push origin HEAD --force-with-lease")
    assert not res4_lease.allowed
    assert "force push is disabled" in res4_lease.reason
    
    # 4. Dangerous rm -rf statements
    res5 = policy.check_command("rm -rf /")
    assert not res5.allowed
    assert "rm -rf is dangerous" in res5.reason
    
    res6 = policy.check_command("sudo rm -rf zai_coder")
    assert not res6.allowed
    assert "requires manual review" in res6.reason

    # 5. Environment variable checks
    res7 = policy.check_command("cat .env")
    assert not res7.allowed
    assert "reading .env" in res7.reason

def test_safety_policy_safe_commands():
    policy = SafetyPolicy()
    
    assert policy.check_command("git status --short").allowed
    assert policy.check_command("git diff --stat").allowed
    assert policy.check_command("python3 -m pytest -q").allowed
    assert policy.check_command("make repo-check").allowed

def test_safety_policy_path_checks():
    policy = SafetyPolicy()
    
    # Blocked paths (secrets, generated files, apps/zlms/ protected region)
    assert not policy.check_path("dist/zai_coder-0.1.2.tar.gz").allowed
    assert not policy.check_path("node_modules/lodash/index.js").allowed
    assert not policy.check_path(".env").allowed
    assert not policy.check_path("config/secrets.json").allowed
    assert not policy.check_path("apps/zlms/api.py").allowed

    # Allowed paths
    assert policy.check_path("zai_coder/cli.py").allowed
    assert policy.check_path("tests/test_policy.py").allowed

def test_github_ready_repo_policy_staging():
    # Dangerous stage patterns should fail
    assert not is_safe_stage_path("dist/release-0.1.2.zip")
    assert not is_safe_stage_path("data/database.db")
    assert not is_safe_stage_path(".env")
    assert not is_safe_stage_path("apps/zlms/secret.ts")
    assert not is_safe_stage_path("zai_coder/__pycache__/cli.cpython-312.pyc")
    assert not is_safe_stage_path("tests/.pytest_cache/v/cache/lastfailed")
    assert not is_safe_stage_path("../outside.py")
    assert not is_safe_stage_path("/absolute/path.py")

    # Safe stage patterns should pass
    assert is_safe_stage_path("zai_coder/cli.py")
    assert is_safe_stage_path("docs/release/V0.1.3_CLI_POLISH.md")

def test_find_forbidden_command_text():
    forbidden = find_forbidden_command_text("make release && git add .")
    assert "git add ." in forbidden
    
    forbidden_empty = find_forbidden_command_text("git status")
    assert len(forbidden_empty) == 0

def test_policy_loader_non_existent():
    loader = PolicyLoader(assets_dir="non_existent_dir")
    with pytest.raises(ValueError) as excinfo:
        loader.load("unknown_policy_profile_fail_closed")
    assert "not found" in str(excinfo.value)
