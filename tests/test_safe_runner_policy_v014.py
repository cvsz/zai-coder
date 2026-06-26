from zai_coder.core.safety import SafetyPolicy
import pytest

def test_git_add_dot_blocked():
    policy = SafetyPolicy()
    assert not policy.check_command("git add .").allowed

def test_git_add_a_blocked():
    policy = SafetyPolicy()
    assert not policy.check_command("git add -A").allowed

def test_git_commit_no_verify_blocked():
    policy = SafetyPolicy()
    assert not policy.check_command("git commit --no-verify -m 'skip'").allowed

def test_git_force_push_blocked():
    policy = SafetyPolicy()
    assert not policy.check_command("git push --force").allowed
    assert not policy.check_command("git push -f").allowed

def test_destructive_rm_rf_blocked():
    policy = SafetyPolicy()
    assert not policy.check_command("rm -rf /").allowed
    assert not policy.check_command("rm -rf ~").allowed
    assert not policy.check_command("sudo rm -rf /").allowed

def test_shell_chaining_blocked():
    policy = SafetyPolicy()
    assert not policy.check_command("echo 'bad'; bash").allowed
    assert not policy.check_command("ls | sh").allowed
