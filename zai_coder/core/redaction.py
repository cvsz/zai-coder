import re

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_\-]{20,}"),  # OpenAI
    re.compile(r"sk-or-v1-[A-Za-z0-9_\-]{20,}"),  # OpenRouter
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),  # GitHub
    re.compile(r"AIza[A-Za-z0-9_\-]{20,}"),  # Google
    re.compile(r"AKIA[0-9A-Z]{16}"),  # AWS
    re.compile(r"-----BEGIN (RSA |EC |OPENSSH |)PRIVATE KEY-----.*?-----END \1PRIVATE KEY-----", re.DOTALL),
    re.compile(r"Bearer\s+[A-Za-z0-9_\-\.]+"),
    re.compile(r"(?i)(?:password|secret|token|api_key|apikey|access_token|auth_token)\s*[:=]\s*[\"']?[A-Za-z0-9_\-\.\+]{8,}[\"']?"),
]

def redact_text(text: str) -> str:
    out = text
    for pattern in SECRET_PATTERNS:
        out = pattern.sub("[REDACTED_SECRET]", out)
    return out
