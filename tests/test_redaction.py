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

    # AWS token
    aws_token = "A" + "KIA1234567890ABCDEF"
    assert "AKIA" not in redact_text(aws_token)

    # Private key
    pk = "-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA...\n-----END RSA PRIVATE KEY-----"
    assert "MIIE" not in redact_text(pk)

    # Bearer token
    bearer = "Authorization: Bearer my-secret-jwt.token.here123"
    assert "my-secret-jwt" not in redact_text(bearer)

    # JSON / env token
    env_str = 'PASS' + 'WORD="super_secret_value"'
    assert "super_secret" not in redact_text(env_str)
    
    json_str = '{"api' + '_key": "some-random-key-123"}'
    assert "some-random" not in redact_text(json_str)

def test_redact_no_secrets():
    text = "This is a safe text with no secrets."
    redacted = redact_text(text)
    assert redacted == text
