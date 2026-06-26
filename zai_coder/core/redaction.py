import re

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_\-]{20,}"),
    re.compile(r"sk-or-v1-[A-Za-z0-9_\-]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
    re.compile(r"AIza[A-Za-z0-9_\-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (RSA |EC |OPENSSH |)PRIVATE KEY-----"),
]

def redact_text(text: str) -> str:
    out = text
    for pattern in SECRET_PATTERNS:
        out = pattern.sub("[REDACTED_SECRET]", out)
    return out
