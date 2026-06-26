import pytest
from zai_coder.core.models import ModelRouter, EchoProvider

def test_model_router_fallback():
    provider1 = EchoProvider()
    provider2 = EchoProvider()
    router = ModelRouter(provider1, fallback_provider=provider2)
    
    assert router.provider == provider1
    assert router.fallback_provider == provider2
