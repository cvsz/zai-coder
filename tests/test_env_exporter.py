from pathlib import Path
import pytest
from zai_coder.deploy_installer_core.env_exporter import export_env, import_env, encrypt_data, decrypt_data
from zai_coder.cli import main


def test_encryption_decryption_roundtrip():
    original = b"ZAI_SESSION_SECRET=my-super-secret-key-value\nDATABASE_URL=postgresql://localhost"
    password = "secpwd123"

    # Encrypt
    encrypted = encrypt_data(original, password)
    assert encrypted != original
    assert len(encrypted) > len(original)

    # Decrypt with correct password
    decrypted = decrypt_data(encrypted, password)
    assert decrypted == original

    # Decrypt with incorrect password should fail or produce garbage (not match original)
    wrong_decrypted = decrypt_data(encrypted, "wrong-password")
    assert wrong_decrypted != original


def test_env_exporter_file_roundtrip(tmp_path):
    env_file = tmp_path / ".env"
    enc_file = tmp_path / ".env.enc"
    dec_file = tmp_path / ".env.dec"

    original_content = "SECRET_TOKEN=xyz123\nPORT=8080"
    env_file.write_text(original_content, encoding="utf-8")

    password = "exportpass"

    # Export
    export_env(env_file, password, enc_file)
    assert enc_file.exists()
    assert enc_file.read_bytes() != original_content.encode("utf-8")

    # Import
    import_env(enc_file, password, dec_file)
    assert dec_file.exists()
    assert dec_file.read_text(encoding="utf-8") == original_content


def test_env_exporter_cli(tmp_path, capsys):
    env_file = tmp_path / ".env"
    enc_file = tmp_path / ".env.enc"
    dec_file = tmp_path / ".env.dec"

    original_content = "KEY=value\nPASSWORD=source_secret"
    env_file.write_text(original_content, encoding="utf-8")

    password = "clipass"

    # Test CLI Export
    args_export = [
        "env-exporter", "export",
        "--env", str(env_file),
        "--password", password,
        "--out", str(enc_file)
    ]
    exit_code_export = main(args_export)
    assert exit_code_export == 0
    assert enc_file.exists()

    # Test CLI Import
    args_import = [
        "env-exporter", "import",
        "--enc", str(enc_file),
        "--password", password,
        "--out", str(dec_file)
    ]
    exit_code_import = main(args_import)
    assert exit_code_import == 0
    assert dec_file.exists()
    assert dec_file.read_text(encoding="utf-8") == original_content
