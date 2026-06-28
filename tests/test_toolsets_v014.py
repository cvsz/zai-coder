from zai_coder.core.toolsets import get_default_toolset_registry

def test_default_toolsets():
    reg = get_default_toolset_registry()
    read_only = reg.get("read_only")
    assert read_only is not None
    assert read_only.risk_level == "low"
    assert read_only.enabled_by_default is True
    
    operator = reg.get("operator")
    assert operator is not None
    assert operator.risk_level == "high"
    assert operator.enabled_by_default is False
    
    assert len(reg.get_all()) >= 9
