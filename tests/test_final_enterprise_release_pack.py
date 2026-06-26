import json
from zai_coder.final_enterprise_release_pack.routes import route_final_release_status

def test_route_final_release_status():
    result = route_final_release_status()
    assert isinstance(result, str)
    # should be json parseable
    data = json.loads(result)
    assert "ok" in data
    assert "checks" in data
    assert "import_health" in data["checks"]
