"""Template variable validation."""

from __future__ import annotations

import re

VARIABLE_RE = re.compile(r"{{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*}}")


FORBIDDEN_VALUE_TERMS = ("password", "token", "secret", "api key", "credit card")


def extract_variables(template_body: str) -> list[str]:
    return sorted(set(VARIABLE_RE.findall(template_body)))


def validate_template_variables(template: dict) -> dict:
    found = extract_variables(template["body"])
    declared = sorted(template.get("variables", []))
    missing_declared = [item for item in found if item not in declared]
    unused_declared = [item for item in declared if item not in found]
    return {
        "ok": not missing_declared and not unused_declared,
        "found": found,
        "declared": declared,
        "missing_declared": missing_declared,
        "unused_declared": unused_declared,
    }


def validate_render_variables(template: dict, variables: dict) -> dict:
    required = set(template.get("variables", []))
    supplied = set(variables.keys())
    missing = sorted(required - supplied)
    extra = sorted(supplied - required)
    sensitive = []
    for key, value in variables.items():
        text = f"{key} {value}".lower()
        if any(term in text for term in FORBIDDEN_VALUE_TERMS):
            sensitive.append(key)
    return {
        "ok": not missing and not sensitive,
        "missing": missing,
        "extra": extra,
        "sensitive": sensitive,
    }
