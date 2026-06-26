from .systemd import get_systemd_template
from .docker import get_dockerfile_template, get_docker_compose_template
from .reverse_proxy import get_nginx_template

class DeployPlanner:
    def get_plan(self, target: str) -> dict:
        files = {}
        checklist = []
        
        if target == "systemd":
            files["zai-coder.service"] = get_systemd_template()
            checklist = [
                "Copy zai-coder.service to /etc/systemd/system/",
                "Run 'systemctl daemon-reload'",
                "Run 'systemctl enable zai-coder.service'",
                "Run 'systemctl start zai-coder.service'"
            ]
        elif target == "docker":
            files["Dockerfile"] = get_dockerfile_template()
            files["docker-compose.yml"] = get_docker_compose_template()
            checklist = [
                "Run 'docker-compose up -d --build'",
                "Check logs with 'docker-compose logs -f'"
            ]
        elif target == "nginx":
            files["nginx.conf"] = get_nginx_template()
            checklist = [
                "Copy nginx.conf to /etc/nginx/sites-available/zai-coder",
                "Symlink to /etc/nginx/sites-enabled/",
                "Run 'nginx -t' to verify",
                "Run 'systemctl reload nginx'"
            ]
            
        rollback = [
            "Stop service/container",
            "Restore previous release directory or container image",
            "Restart service/container"
        ]
            
        return {
            "target": target,
            "files": files,
            "checklist": checklist,
            "rollback": rollback
        }
