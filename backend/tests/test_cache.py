"""
Tests for the caching module.
"""
import os
import time
import pytest
from app.cache import cache_get, cache_set, cache_clear

@pytest.fixture(autouse=True)
def clear_cache():
    """Clear cache before and after each test."""
    cache_clear()
    yield
    cache_clear()

def test_cache_set_get():
    """Test basic cache set and get functionality."""
    # Set values in different namespaces
    cache_set("test", "key1", "value1")
    cache_set("test", "key2", {"a": 1, "b": 2})
    cache_set("other", "key1", [1, 2, 3])
    
    # Get values
    assert cache_get("test", "key1") == "value1"
    assert cache_get("test", "key2") == {"a": 1, "b": 2}
    assert cache_get("other", "key1") == [1, 2, 3]
    
    # Non-existent values
    assert cache_get("test", "key3") is None
    assert cache_get("nonexistent", "key1") is None

def test_cache_expiry():
    """Test cache expiry."""
    # Set value with short expiry
    cache_set("test", "short", "expires_soon", expires=1)
    assert cache_get("test", "short") == "expires_soon"
    
    # Wait for expiry
    time.sleep(1.1)
    assert cache_get("test", "short") is None
    
    # Set value with longer expiry
    cache_set("test", "long", "expires_later", expires=10)
    assert cache_get("test", "long") == "expires_later"

def test_cache_clear():
    """Test cache clearing."""
    # Set values
    cache_set("ns1", "key1", "value1")
    cache_set("ns1", "key2", "value2")
    cache_set("ns2", "key1", "value3")
    
    # Clear specific key
    cache_clear("ns1", "key1")
    assert cache_get("ns1", "key1") is None
    assert cache_get("ns1", "key2") == "value2"
    assert cache_get("ns2", "key1") == "value3"
    
    # Clear namespace
    cache_clear("ns1")
    assert cache_get("ns1", "key2") is None
    assert cache_get("ns2", "key1") == "value3"
    
    # Clear all
    cache_clear()
    assert cache_get("ns2", "key1") is None