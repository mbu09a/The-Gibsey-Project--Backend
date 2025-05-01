#!/usr/bin/env python
"""
Generate a JWT token for testing authenticated API routes.
"""
import jwt
import time
import os
from dotenv import load_dotenv

load_dotenv()

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

if __name__ == "__main__":
    token = generate_token()
    print(f"Bearer {token}") 