#!/usr/bin/env python
"""
Test script for the FastAPI service with authentication.
"""
import os
import json
import time
import requests
try:
    import jwt
except ImportError:
    # Stub for type checking
    class JWTStub:
        @staticmethod
        def encode(*args, **kwargs): return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    jwt = JWTStub()

try:
    import pytest
except ImportError:
    # Stub for type checking
    class PytestStub:
        @staticmethod
        def fixture(*args, **kwargs): return lambda x: x
    pytest = PytestStub()

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set base URL for API
BASE_URL = "http://localhost:8000"

def generate_token():
    """Generate a JWT token with a user_id and name."""
    # Get the JWT secret from environment
    secret = os.getenv("JWT_SECRET", "your-secret-key")
    
    # Create a payload with some claims
    payload = {
        "sub": "test-user-123",
        "name": "Test User",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600  # Token valid for 1 hour
    }
    
    # Generate the token
    token = jwt.encode(payload, secret, algorithm="HS256")
    
    return token

def test_authentication():
    """Test authentication for restricted endpoints."""
    print("Testing authentication...")
    
    # Test without token
    try:
        resp = requests.get(f"{BASE_URL}/pages/story1/1")
        print(f"Request without token: {resp.status_code} - {resp.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test with token
    token = generate_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        resp = requests.get(f"{BASE_URL}/pages/story1/1", headers=headers)
        if resp.status_code == 404:
            print("Authenticated request successful (page not found, but authentication worked)!")
        else:
            print(f"Authenticated request: {resp.status_code} - {resp.json()}")
    except Exception as e:
        print(f"Error: {e}")

def test_search():
    """Test search endpoint with native engine."""
    print("\nTesting search functionality...")
    
    # Generate token
    token = generate_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test search
    search_data = {
        "q": "test query",
        "k": 3
    }
    
    try:
        resp = requests.post(f"{BASE_URL}/search", headers=headers, json=search_data)
        print(f"Search response: {resp.status_code}")
        if resp.status_code == 200:
            print("Search successful!")
        else:
            print(f"Search error: {resp.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Testing FastAPI service with authentication...")
    print("=============================================")
    
    test_authentication()
    test_search()
    
    print("\nTests completed!") 