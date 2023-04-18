import hashlib
import json


def get_hash(payload):
    return hashlib.md5(json.dumps(payload, separators=(",", ":"),
                                  sort_keys=True, ensure_ascii=False).encode()).hexdigest()


__all__ = ["get_hash"]
