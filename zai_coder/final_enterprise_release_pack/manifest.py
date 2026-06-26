def get_manifest():
    return {
        "package": "zai-coder-control-plane-v50-final-enterprise-release-pack",
        "install_modes": ["local", "docker-plan", "ssh-plan"],
        "safe_defaults": {"dry_run": True, "apply_requires": "APPLY=1", "production_launch": False},
        "entrypoints": ["install.sh", "run.sh", "Makefile"],
        "post_install_checks": ["make final-release-status", "make final-validation-report", "make final-go-live-checklist"],
    }
