from zai_coder.core.booleans import coerce_bool
from zai_coder.enterprise_governance.policy_engine import governance_gate
from zai_coder.execution_runner.routes import route_enqueue
from zai_coder.multi_tenant_control.routes import route_provider_permission
from zai_coder.real_provider_adapters.routes import route_provider_env_check, route_github_create_repo_plan


def test_coerce_bool_handles_form_style_false_values():
    for value in (False, None, "", "0", "false", "False", "no", "off"):
        assert coerce_bool(value) is False
    for value in (True, "1", "true", "TRUE", "yes", "on"):
        assert coerce_bool(value) is True


def test_apply_routes_do_not_treat_false_string_as_apply(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    assert route_provider_env_check({"provider": "github", "apply": "false"})["ok"] is True
    plan = route_github_create_repo_plan({"repo_name": "demo", "apply": "false"})
    assert plan["ok"] is True
    assert plan["dry_run"] is True

    queued = route_enqueue({"command": ["echo", "hello"], "apply": "false"})
    assert queued["command"]["apply"] is False

    permission = route_provider_permission({"provider": "docker", "roles": ["operator"], "apply": "false"})
    assert permission["allowed"] is True


def test_governance_gate_parses_boolean_payload_strings():
    allowed = governance_gate(
        {
            "mutating": "false",
            "apply": "false",
            "public_exposure": "false",
            "cloudflare_access_enabled": "false",
        }
    )
    assert allowed["allowed"] is True

    blocked = governance_gate({"mutating": "true", "apply": "true", "dry_run_completed": "false"})
    assert blocked["allowed"] is False

    secret_blocked = governance_gate({"secret_scan_ok": "false"})
    assert secret_blocked["allowed"] is False
