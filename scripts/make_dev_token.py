#!/usr/bin/env python3
"""
Dev token generator for HS256/RS256 tokens with custom scopes and expiry.
Usage:
  python -m scripts.make_dev_token --scopes "gibsey.vault.read gibsey.chat" --exp 8h --alg HS256
Writes JWT to stdout; for RS256 also writes keypair.pem (private key) for test use.
"""
import argparse
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

from jose import jwt, jwk
from jose.utils import base64url_decode, base64url_encode
try:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
except ImportError:
    rsa = None

# Read config
DEV_SECRET = os.getenv("DEV_JWT_SECRET", "dev-only-secret")
AUD = os.getenv("SUPABASE_PROJECT", "gibsey-project")

DURATION_UNITS = {
    's': 1,
    'm': 60,
    'h': 3600,
    'd': 86400,
}


def parse_duration(s: str) -> int:
    """Parse human duration like '30m', '2h', '1d' into seconds."""
    try:
        num = int(s[:-1])
        unit = s[-1]
        return num * DURATION_UNITS.get(unit, 0)
    except Exception:
        raise ValueError(f"Invalid duration: {s}")


def make_token(scopes: str, exp: str, alg: str = 'HS256'):
    iat = int(time.time())
    secs = parse_duration(exp)
    exp_ts = iat + secs
    payload = {
        'sub': 'dev-user',
        'iat': iat,
        'exp': exp_ts,
        'aud': AUD,
        'scope': scopes,
    }
    if alg.upper() == 'HS256':
        token = jwt.encode(payload, DEV_SECRET, algorithm='HS256')
        return token, None
    elif alg.upper() == 'RS256':
        if rsa is None:
            print("Error: cryptography library required for RS256", file=sys.stderr)
            sys.exit(1)
        # generate RSA keypair
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        pem = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        # write private key to file
        path = Path('keypair.pem')
        path.write_bytes(pem)
        token = jwt.encode(payload, pem, algorithm='RS256')
        # construct public JWK for verification
        public = key.public_key()
        jwk_dict = jwk.construct(public, algorithm='RS256').to_dict()
        return token, jwk_dict
    else:
        raise ValueError(f"Unsupported alg: {alg}")


def main():
    parser = argparse.ArgumentParser(description='Generate a dev JWT')
    parser.add_argument('--scopes', type=str, default='gibsey.vault.read', help='Space-separated scopes')
    parser.add_argument('--exp', type=str, default='12h', help='Expiry duration, e.g. 30m, 2h, 1d')
    parser.add_argument('--alg', type=str, default='HS256', help='HS256 or RS256')
    args = parser.parse_args()
    token, jwk_dict = make_token(args.scopes, args.exp, args.alg)
    print(token)
    sys.exit(0)

if __name__ == '__main__':
    main() 