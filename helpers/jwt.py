from common import ResponseMessagesValues, error_handling

import os
import datetime
import jwt
from config import AppConfigValues

JWT_SECRET = os.getenv('JWT_SECRET', AppConfigValues.JWT_SECRET)


def generate_token(payload: dict):
    payload["exp"] = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=1)
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token


def decode_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        del payload["exp"]
        return payload
    except jwt.ExpiredSignatureError:
        raise error_handling.NotAllowed(ResponseMessagesValues.TOKEN_EXPIRED.value)
    except (jwt.InvalidTokenError, jwt.PyJWTError):
        raise error_handling.NotAllowed(ResponseMessagesValues.INVALID_TOKEN.value)


__all__ = ['decode_token', 'generate_token']
