from zai_coder.deploy.planner import DeployPlanner

def test_deploy_planner_systemd():
    planner = DeployPlanner()
    plan = planner.get_plan("systemd")
    
    assert plan["target"] == "systemd"
    assert "zai-coder.service" in plan["files"]
    assert len(plan["checklist"]) > 0
    assert len(plan["rollback"]) > 0

def test_deploy_planner_docker():
    planner = DeployPlanner()
    plan = planner.get_plan("docker")
    
    assert plan["target"] == "docker"
    assert "Dockerfile" in plan["files"]
    assert "docker-compose.yml" in plan["files"]

def test_deploy_planner_nginx():
    planner = DeployPlanner()
    plan = planner.get_plan("nginx")
    
    assert plan["target"] == "nginx"
    assert "nginx.conf" in plan["files"]
