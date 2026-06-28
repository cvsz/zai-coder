from __future__ import annotations

FALSE_STRINGS = {"", "0", "false", "f", "no", "n", "off"}
TRUE_STRINGS = {"1", "true", "t", "yes", "y", "on"}


def coerce_bool(value: object, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in TRUE_STRINGS:
            return True
        if normalized in FALSE_STRINGS:
            return False
    return bool(value)
