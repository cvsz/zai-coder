import pytest
import yaml
from pathlib import Path
from zai_coder.production_api_gateway.deploy import production_gateway_profile
from zai_coder.cloudflare_go_live.preflight import cloudflare_preflight_gate
from zai_coder.github_ready_core.external_action import require_manual_external_action

def test_production_gateway_profile():
    profile = production_gateway_profile()
    assert profile["tls_termination"] == "expected_from_cloudflare"
    assert profile["upstream_health_failover"] is True
    assert profile["request_size_limit_mb"] == 10
    assert "global" in profile["rate_limits"]
    assert profile["structured_audit_logging"] is True
    assert profile["strict_security_headers"] is True

def test_cloudflare_preflight_gate():
    gate = cloudflare_preflight_gate()
    assert gate["ok"] is True
    assert gate["dns_verified"] is True
    assert gate["access_policy_active"] is True
    assert len(gate["checks"]) == 4

def test_require_manual_external_action():
    for action in ["publishing", "pushing", "paid_jobs", "third_party_mutations"]:
        result = require_manual_external_action(action)
        assert result["ok"] is False
        assert result["blocked"] is True

    result = require_manual_external_action("local_test")
    assert result["ok"] is True
    assert result["blocked"] is False

def test_docker_compose_prod_profile():
    compose_file = Path("docker-compose.prod.yml")
    assert compose_file.exists()
    
    with open(compose_file) as f:
        compose_data = yaml.safe_load(f)
        
    assert "services" in compose_data
    assert "gateway" in compose_data["services"]
    gateway = compose_data["services"]["gateway"]
    assert gateway["image"] == "zai-coder-gateway:latest"
    assert "healthcheck" in gateway
