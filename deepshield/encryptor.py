import os
import base64

try:
    from cryptography.fernet import Fernet
except Exception:  # pragma: no cover
    Fernet = None


def load_key(path: str = "secret.key") -> bytes:
    """Load an AES key or generate a new one."""
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f.read()
    if Fernet is not None:
        key = Fernet.generate_key()
    else:
        key = os.urandom(16)
    with open(path, "wb") as f:
        f.write(key)
    return key


def _encrypt(data: bytes, key: bytes) -> bytes:
    if Fernet is not None:
        return Fernet(key).encrypt(data)
    return base64.b64encode(bytes(b ^ key[i % len(key)] for i, b in enumerate(data)))


def _decrypt(token: bytes, key: bytes) -> bytes:
    if Fernet is not None:
        return Fernet(key).decrypt(token)
    data = base64.b64decode(token)
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def encrypt_and_log(text: str, log_path: str = "results.log", key_path: str = "secret.key") -> str:
    """Encrypt ``text`` and append to ``log_path``."""
    key = load_key(key_path)
    token = _encrypt(text.encode(), key)
    with open(log_path, "ab") as f:
        f.write(token + b"\n")
    return log_path


def decrypt_lines(log_path: str, key_path: str = "secret.key") -> list[str]:
    """Decrypt lines in ``log_path`` using the key."""
    key = load_key(key_path)
    lines: list[str] = []
    with open(log_path, "rb") as f:
        for line in f:
            line = line.strip()
            if line:
                lines.append(_decrypt(line, key).decode())
    return lines

