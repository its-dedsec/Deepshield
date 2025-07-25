import os
from deepshield import encryptor


def test_encrypt_and_decrypt(tmp_path):
    log_file = tmp_path / "log.enc"
    key_file = tmp_path / "key.key"
    encryptor.encrypt_and_log("hello", log_path=str(log_file), key_path=str(key_file))
    lines = encryptor.decrypt_lines(str(log_file), key_path=str(key_file))
    assert lines == ["hello"]

