import pytest
from zai_coder.core.tools import ToolRuntime

def test_tool_runtime_allowlist(tmp_path):
    runtime = ToolRuntime(workspace=str(tmp_path), profile="read_only")
    
    # ls is allowed in read_only
    res = runtime.run("ls -la")
    assert res.ok
    
    # mkdir is not allowed in read_only
    res = runtime.run("mkdir test_dir")
    assert not res.ok
    assert "not in allowlist" in res.blocked_reason

def test_tool_runtime_operator(tmp_path):
    runtime = ToolRuntime(workspace=str(tmp_path), profile="operator")
    
    # mkdir is allowed in operator
    res = runtime.run("mkdir test_dir")
    assert res.ok
    
    # unknown command is blocked
    res = runtime.run("some_random_command")
    assert not res.ok
    assert "not in allowlist" in res.blocked_reason

def test_tool_runtime_redaction(tmp_path):
    runtime = ToolRuntime(workspace=str(tmp_path), profile="operator")
    # Using python to echo a string that should be redacted
    # Assuming redaction redacts 'sk-...' strings
    res = runtime.run("python -c \"print('sk-' + '12345678901234567890123456')\"")
    assert res.ok
    assert "REDACTED" in res.stdout
    assert "sk-" not in res.stdout

def test_tool_runtime_shell_bypass(tmp_path):
    runtime = ToolRuntime(workspace=str(tmp_path), profile="operator")
    res = runtime.run("echo hello ; ls")
    assert not res.ok
    assert "Parse error" in res.blocked_reason
