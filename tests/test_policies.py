import pytest
from zai_coder.core.policies import PolicyManager

def test_policy_manager(tmp_path):
    manager = PolicyManager(workspace=str(tmp_path))
    
    profiles = manager.list_profiles()
    assert "read_only" in profiles
    assert "developer" in profiles
    assert "release" in profiles
    assert "operator" in profiles
    assert "locked_down" in profiles
    
    # Test read_only
    ro = manager.get_profile("read_only")
    ok, _ = ro.check_command("ls -la")
    assert ok
    ok, _ = ro.check_command("git status")
    assert ok
    ok, _ = ro.check_command("mkdir test")
    assert not ok
    
    # Test developer
    dev = manager.get_profile("developer")
    ok, _ = dev.check_command("git status")
    assert ok
    ok, _ = dev.check_command("git add .")
    assert not ok  # blocked by denied pattern
    ok, _ = dev.check_command("mkdir test")
    assert ok
    ok, _ = dev.check_command("sudo rm -rf /")
    assert not ok
    
    # Test operator
    op = manager.get_profile("operator")
    ok, _ = op.check_command("some_random_cmd")
    assert ok  # operator allows * command roots
    ok, _ = op.check_command("git add .")
    assert not ok  # still blocked by denied pattern
    
    # Test path checking
    assert not ro.check_path("dist/bundle.js")[0]
    assert ro.check_path("src/index.js")[0]
