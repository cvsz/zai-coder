import pytest
from zai_coder.core.registry import JsonRegistry

def test_json_registry_malformed(tmp_path):
    reg_dir = tmp_path / "agents"
    reg_dir.mkdir()
    
    reg_file = reg_dir / "agents.json"
    reg_file.write_text("{ malformed json")
    
    registry = JsonRegistry(str(reg_dir))
    items = registry.list()
    assert isinstance(items, list)
    assert len(items) == 0
    
    # Valid json
    reg_file.write_text('{"name": "test"}')
    items2 = registry.list()
    assert len(items2) == 1
    assert items2[0].name == "test"
