"""
Pytest configuration file for test fixtures.
"""
import pytest

@pytest.fixture
def base_url():
    """Return the base URL for the FastAPI service."""
    return "http://localhost:8000" 