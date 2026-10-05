from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import os
from typing import Any, Optional, Union

import jwt

from app.core.config import settings

ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY


def get_password_hash(password: str) -> str:
    salt = os.urandom(16)
    iterations = 310_000

    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations,
    )

    return f"pbkdf2_sha256${iterations}${salt.hex()}${digest.hex()}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        scheme, iterations, salt_hex, digest_hex = hashed_password.split("$")

        if scheme != "pbkdf2_sha256":
            return False

        expected = hashlib.pbkdf2_hmac(
            "sha256",
            plain_password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            int(iterations),
        )

        return hmac.compare_digest(expected.hex(), digest_hex)

    except (ValueError, TypeError):
        return False


def create_access_token(
    subject: Union[str, Any] = None,
    data: Optional[dict] = None,
    expires_delta: Optional[timedelta] = None,
) -> str:
    payload = dict(data or {})

    if subject is not None:
        payload["sub"] = str(subject)

    expire = datetime.now(timezone.utc) + (
        expires_delta
        or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload["exp"] = expire

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )