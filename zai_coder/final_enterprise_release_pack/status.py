from zai_coder.final_enterprise_release_pack.checks import (
    check_import_health,
    check_cli_parser,
    check_required_files,
    check_safety_rules,
    check_tests_directory,
    check_makefile_targets,
    check_scripts_executable,
    check_package_metadata
)

def build_status_report():
    checks = {
        "import_health": check_import_health(),
        "cli_parser": check_cli_parser(),
        "required_files": check_required_files(),
        "safety_rules": check_safety_rules(),
        "tests_directory": check_tests_directory(),
        "makefile_targets": check_makefile_targets(),
        "scripts_executable": check_scripts_executable(),
        "package_metadata": check_package_metadata(),
    }
    ok = all(result["ok"] for result in checks.values())
    return {
        "ok": ok,
        "checks": checks,
    }
