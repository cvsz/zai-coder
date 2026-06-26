from zai_coder.core.redaction import redact_text

def test_redact_secrets():
    # OpenAI key
    secret = "s" + "k-12345678901234567890123456"
    text = f"Here is my key {secret} please keep it safe."
    redacted = redact_text(text)
    assert "sk-" not in redacted
    assert "[REDACTED_SECRET]" in redacted
    
    # GitHub token
    gh_token = "gh" + "p_ABCDEF1234567890abcdef1234567890"
    text2 = f"Using {gh_token} for auth."
    redacted2 = redact_text(text2)
    assert "ghp_" not in redacted2
    assert "[REDACTED_SECRET]" in redacted2

def test_redact_no_secrets():
    text = "This is a safe text with no secrets."
    redacted = redact_text(text)
    assert redacted == text
