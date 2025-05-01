import os
import jwt
import datetime

__all__ = ["issue_hs256"]

def issue_hs256(sub: str, expires_in: int = 900) -> str:
    """
    Issue a JWT signed with HS256.

    :param sub: Subject (e.g., user identifier)
    :param expires_in: Expiration time in seconds (default 900s)
    :return: JWT as a string
    """
    secret = os.getenv("JWT_SECRET")
    if not secret:
        raise RuntimeError("JWT_SECRET must be set for HS256 token issuance")
    now = datetime.datetime.utcnow()
    payload = {
        "sub": sub,
        "iat": now,
        "exp": now + datetime.timedelta(seconds=expires_in),
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    # jwt.encode may return bytes in some versions
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token