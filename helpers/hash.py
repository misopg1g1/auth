from config.default import AppConfigValues

import hashlib
import json
import typing

from cryptography.fernet import Fernet


def get_hash(payload):
    return hashlib.md5(json.dumps(payload, separators=(",", ":"),
                                  sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def encrypt_hash(hash_sum: typing.Union[str, bytes]) -> str:
    fernet = Fernet(AppConfigValues.ENCRYPTION_KEY_SECRET.encode())
    return fernet.encrypt(hash_sum.encode() if isinstance(hash_sum, str) else hash_sum).decode()


def refresh_object_hash(obj: dict):
    obj["hash"] = encrypt_hash(get_hash(obj))


__all__ = ["get_hash", "encrypt_hash", "refresh_object_hash"]
