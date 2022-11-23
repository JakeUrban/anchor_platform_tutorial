from os import environ
from logging import getLogger

import jwt


logger = getLogger(__name__)


def verify_jwt(token: str) -> dict:
    if not token:
        raise ValueError("token is required")
    contents = jwt.decode(
        token, key=environ.get("SECRET_SEP10_JWT_SECRET"), algorithms=["HS256"]
    )
    if not contents.get("jti"):
        raise ValueError("missing 'jti'")
    return contents
