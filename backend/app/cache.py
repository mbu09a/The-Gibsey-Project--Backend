"""
Caching module for FastAPI server.
Provides Redis caching with a memory fallback for development.
"""
import os
import json
import time
from typing import Any, Dict, Optional, Union

# Try to import Redis, use in-memory cache if not available
try:
    import redis
    _redis = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", "6379")),
        db=int(os.getenv("REDIS_DB", "0")),
        password=os.getenv("REDIS_PASSWORD", None),
        decode_responses=True
    )
    # Test connection
    try:
        _redis.ping()
        _HAVE_REDIS = True
    except redis.exceptions.ConnectionError:
        _HAVE_REDIS = False
except (ImportError, redis.exceptions.ConnectionError):
    _HAVE_REDIS = False

# In-memory cache for development/testing
_mem_cache: Dict[str, Dict[str, Dict[str, Any]]] = {}
_mem_expiry: Dict[str, Dict[str, float]] = {}

def cache_get(namespace: str, key: str) -> Optional[Any]:
    """
    Get a value from the cache.
    
    Args:
        namespace: The namespace for the key (e.g., "search", "page")
        key: The cache key
        
    Returns:
        The cached value if found, None otherwise
    """
    if _HAVE_REDIS:
        try:
            redis_key = f"{namespace}:{key}"
            value = _redis.get(redis_key)
            if value:
                return json.loads(value)
        except Exception:
            # Fall back to memory cache on Redis error
            pass
    
    # Use memory cache
    if namespace in _mem_cache and key in _mem_cache[namespace]:
        # Check expiry
        if namespace in _mem_expiry and key in _mem_expiry[namespace]:
            if _mem_expiry[namespace][key] > time.time():
                return _mem_cache[namespace][key]
            # Expired
            del _mem_cache[namespace][key]
            del _mem_expiry[namespace][key]
    
    return None

def cache_set(namespace: str, key: str, value: Any, expires: int = 3600) -> bool:
    """
    Set a value in the cache.
    
    Args:
        namespace: The namespace for the key (e.g., "search", "page")
        key: The cache key
        value: The value to store (must be JSON serializable)
        expires: Expiry time in seconds (default: 1 hour)
        
    Returns:
        True if successful, False otherwise
    """
    if _HAVE_REDIS:
        try:
            redis_key = f"{namespace}:{key}"
            _redis.setex(redis_key, expires, json.dumps(value))
            return True
        except Exception:
            # Fall back to memory cache on Redis error
            pass
    
    # Use memory cache
    if namespace not in _mem_cache:
        _mem_cache[namespace] = {}
    if namespace not in _mem_expiry:
        _mem_expiry[namespace] = {}
    
    _mem_cache[namespace][key] = value
    _mem_expiry[namespace][key] = time.time() + expires
    return True

def cache_clear(namespace: Optional[str] = None, key: Optional[str] = None) -> bool:
    """
    Clear cache entries.
    
    Args:
        namespace: If provided, only clear this namespace
        key: If provided with namespace, only clear this specific key
        
    Returns:
        True if successful, False otherwise
    """
    if namespace is None:
        # Clear all
        if _HAVE_REDIS:
            try:
                _redis.flushdb()
            except Exception:
                pass
        
        _mem_cache.clear()
        _mem_expiry.clear()
        return True
    
    if key is None:
        # Clear namespace
        if _HAVE_REDIS:
            try:
                for k in _redis.scan_iter(f"{namespace}:*"):
                    _redis.delete(k)
            except Exception:
                pass
        
        if namespace in _mem_cache:
            _mem_cache[namespace].clear()
        if namespace in _mem_expiry:
            _mem_expiry[namespace].clear()
        return True
    
    # Clear specific key
    if _HAVE_REDIS:
        try:
            redis_key = f"{namespace}:{key}"
            _redis.delete(redis_key)
        except Exception:
            pass
    
    if namespace in _mem_cache and key in _mem_cache[namespace]:
        del _mem_cache[namespace][key]
    if namespace in _mem_expiry and key in _mem_expiry[namespace]:
        del _mem_expiry[namespace][key]
    return True