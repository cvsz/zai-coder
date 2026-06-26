import pytest
from zai_coder.core.policy_loader import PolicyLoader
from zai_coder.core.policy import PolicyProfile

def test_policy_loader_fallback():
    loader = PolicyLoader(assets_dir="non_existent_dir")
    policies = loader.list_policies()
    assert "read_only" in policies
    
    p = loader.load("read_only")
    assert isinstance(p, PolicyProfile)
    assert p.name == "read_only"
    assert "ls" in p.allowed_commands

def test_policy_loader_assets(tmp_path):
    loader = PolicyLoader(assets_dir="assets/policies")
    policies = loader.list_policies()
    assert "developer" in policies
    
    p = loader.load("developer")
    assert p.name == "developer"
    assert p.allow_network is True
    
def test_policy_decisions():
    loader = PolicyLoader(assets_dir="assets/policies")
    dev = loader.load("developer")
    
    # check command OK
    ok, _ = dev.check_command("git status")
    assert ok
    
    # check command BLOCKED
    ok, reason = dev.check_command("rm -rf /")
    assert not ok
    assert "matches denied pattern" in reason
    
    # check path OK
    ok, _ = dev.check_path("zai_coder/core/tools.py")
    assert ok
    
    # check path BLOCKED
    ok, reason = dev.check_path("apps/zlms/secret.ts")
    assert not ok
    assert "protected" in reason
    
    ok, reason = dev.check_path("node_modules/index.js")
    assert not ok
    assert "generated" in reason
