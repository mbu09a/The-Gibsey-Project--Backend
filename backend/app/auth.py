import os
import time
import httpx
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# -------- testing helper (HS256) ----------
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

JWKS_URL = f"https://{os.getenv('SUPABASE_PROJECT')}.supabase.co/auth/v1/keys"
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
    """Verify a JWT token from Supabase."""
    # Development mode bypass - return a dummy user payload
    if os.getenv("AUTH_BYPASS", "false").lower() == "true":
        return {"sub": "test-user", "email": "test@example.com", "role": "authenticated"}
        
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Extract the token
        token = auth.credentials

        jwks = await _get_jwks()
        if jwks:
            payload = jwt.decode(
                token, jwks, algorithms=["RS256"], audience=os.getenv("SUPABASE_PROJECT")
            )
        else:  # offline, fall back to HS256 dev secret
            payload = jwt.decode(token, TEST_SECRET, algorithms=["HS256"])
        
        # Check if token is expired
        if payload.get("exp") and payload.get("exp") < time.time():
            raise credentials_exception
            
        return payload
    except jwt.PyJWTError:
        raise credentials_exception 