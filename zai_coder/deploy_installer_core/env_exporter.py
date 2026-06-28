"""Environment file exporter and importer with password-based encryption."""

from __future__ import annotations

import base64
import hmac
import hashlib
import os
from pathlib import Path


def _derive_key(password: str, salt: bytes) -> bytes:
    # Derives a cryptographically strong 256-bit key from a password and salt using PBKDF2-HMAC-SHA256
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)


def encrypt_data(data: bytes, password: str) -> bytes:
    # Encrypts binary data using a custom PBKDF2-HMAC-SHA256 CTR stream cipher
    salt = os.urandom(16)
    key = _derive_key(password, salt)
    iv = os.urandom(16)

    keystream = b""
    counter = 0
    while len(keystream) < len(data):
        counter_bytes = counter.to_bytes(8, "big")
        # Generate block keystream by hashing IV and counter
        block_hmac = hmac.new(key, iv + counter_bytes, hashlib.sha256)
        keystream += block_hmac.digest()
        counter += 1

    ciphertext = bytes(a ^ b for a, b in zip(data, keystream))
    # Return salt + IV + ciphertext
    return salt + iv + ciphertext


def decrypt_data(payload: bytes, password: str) -> bytes:
    # Decrypts binary data encrypted by encrypt_data using PBKDF2-HMAC-SHA256 CTR
    if len(payload) < 32:
        raise ValueError("Invalid encrypted payload length")
    salt = payload[:16]
    iv = payload[16:32]
    ciphertext = payload[32:]

    key = _derive_key(password, salt)

    keystream = b""
    counter = 0
    while len(keystream) < len(ciphertext):
        counter_bytes = counter.to_bytes(8, "big")
        block_hmac = hmac.new(key, iv + counter_bytes, hashlib.sha256)
        keystream += block_hmac.digest()
        counter += 1

    return bytes(a ^ b for a, b in zip(ciphertext, keystream))


def export_env(env_path: str | Path, password: str, output_path: str | Path) -> None:
    # Encrypts the .env file contents and writes the encrypted base64 payload to output_path
    env_file = Path(env_path)
    if not env_file.exists():
        raise FileNotFoundError(f"Environment file not found: {env_path}")
    
    data = env_file.read_bytes()
    encrypted = encrypt_data(data, password)
    encoded = base64.b64encode(encrypted)
    
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_bytes(encoded)


def import_env(enc_path: str | Path, password: str, output_path: str | Path) -> None:
    # Decrypts the encrypted env file and writes the plaintext env file to output_path
    enc_file = Path(enc_path)
    if not enc_file.exists():
        raise FileNotFoundError(f"Encrypted environment file not found: {enc_path}")
    
    encoded = enc_file.read_bytes()
    encrypted = base64.b64decode(encoded)
    decrypted = decrypt_data(encrypted, password)
    
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_bytes(decrypted)
