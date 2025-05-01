import os
import time
import httpx
import jwt
import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# Settings
ENV = os.getenv("ENV", "dev")
# HS256 secret for dev and CI (fallback)
DEV_JWT_SECRET = os.getenv("DEV_JWT_SECRET", "dev-only-secret")
# JWKS URL for RS256
JWKS_URL = os.getenv("SUPABASE_JWKS_URL", f"https://{os.getenv('SUPABASE_PROJECT')}.supabase.co/auth/v1/keys")
# Required scopes for Gibsey API
REQUIRED_SCOPES = {"gibsey.vault.read", "gibsey.chat", "gibsey.search"}
# Logger
logger = logging.getLogger("auth")

# testing helper (HS256)
TEST_SECRET = os.getenv("JWT_SECRET", "dev_secret")
def _issue_dev_token():
    """Return a short‑lived HS256 token for pytest."""
    payload = {
        "sub": "pytest",
        "iat": int(time.time()),
        "exp": int(time.time()) + 300,
        "aud": os.getenv("SUPABASE_PROJECT", "gibsey-project"),
    }
    return jwt.encode(payload, TEST_SECRET, algorithm="HS256")

security = HTTPBearer()

_jwks_cache = None

async def _get_jwks():
    global _jwks_cache
    if _jwks_cache is None:
        try:
            _jwks_cache = (await httpx.AsyncClient(timeout=5).get(JWKS_URL)).json()["keys"]
        except Exception:
            # offline env (pytest) – return empty list so HS256 path is used
            _jwks_cache = []
    return _jwks_cache

async def verify_token(auth: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verify a JWT token from Supabase (RS256) or HS256 fallback in dev/ci."""
    token = auth.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    forbidden_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Missing required scope",
    )
    now = int(time.time())
    # Dev/CI HS256 fallback
    if ENV in ("dev", "ci"):
        try:
            payload = jwt.decode(token, DEV_JWT_SECRET, algorithms=["HS256"])
            logger.warning("Using HS256 dev/ci fallback verification")
        except jwt.PyJWTError:
            raise credentials_exception
    else:
        # Production RS256 via Supabase JWKS
        try:
            jwks = await _get_jwks()
            payload = jwt.decode(
                token,
                jwks,
                algorithms=["RS256"],
                audience=os.getenv("SUPABASE_PROJECT"),
            )
        except jwt.PyJWTError:
            raise credentials_exception
    # Expiry check with small leeway
    exp = payload.get("exp")
    if not exp or exp < now - 30:
        raise credentials_exception
    # Scope enforcement
    scopes = set(payload.get("scope", "").split())
    if not REQUIRED_SCOPES.intersection(scopes):
        raise forbidden_exception
    return payload 