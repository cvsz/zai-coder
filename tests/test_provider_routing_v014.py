import pytest
from zai_coder.core.provider_routing import ProviderRoute, ProviderRouter

def test_provider_router_registration():
    router = ProviderRouter()
    r1 = ProviderRoute(provider_id="openai-main", provider_type="openai")
    router.register_route(r1)
    
    assert router.get_route("openai-main").provider_type == "openai"
    assert router.get_route("missing") is None

def test_provider_router_selection():
    router = ProviderRouter()
    r1 = ProviderRoute("p1", "type1", priority=10, supports_vision=False)
    r2 = ProviderRoute("p2", "type2", priority=20, supports_vision=True)
    r3 = ProviderRoute("p3", "type3", priority=5, enabled=False, supports_vision=True)
    
    router.register_route(r1)
    router.register_route(r2)
    router.register_route(r3)
    
    # Best overall (lowest priority that is enabled)
    best = router.select_best_route()
    assert best.provider_id == "p1"
    
    # Best with vision
    best_vision = router.select_best_route(require_vision=True)
    assert best_vision.provider_id == "p2"
