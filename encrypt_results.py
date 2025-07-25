import json
import sys
import os
import datetime

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


def encrypt_data(data: bytes, key: bytes) -> bytes:
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted


def main():
    if len(sys.argv) != 2:
        print("Usage: python encrypt_results.py <results_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    with open(input_file, "r") as f:
        contents = f.read()

    log_entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "filename": input_file,
        "content": contents,
    }

    data = json.dumps(log_entry).encode("utf-8")

    key = os.urandom(32)  # AES-256
    encrypted = encrypt_data(data, key)

    with open("results.enc", "wb") as f:
        f.write(encrypted)
    with open("results.key", "wb") as f:
        f.write(key)

    print("Encrypted log written to results.enc")
    print("Encryption key saved to results.key")


if __name__ == "__main__":
    main()
