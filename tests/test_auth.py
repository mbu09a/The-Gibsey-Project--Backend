import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import time

testapp = TestClient(__import__('backend.app.main').app)

from scripts.make_dev_token import make_token
import backend.app.auth as auth_mod

# Stub database for /pages endpoint
@pytest.fixture(autouse=True)
def stub_db(monkeypatch):
    class DummyRow:
        def __init__(self):
            self._data = {'story_id': 'entrance', 'page_num': 1, 'html': 'dummy', 'embedding': [0]*1536}
        def _asdict(self): return self._data
    class DummySession:
        def prepare(self, q): return q
        def execute(self, *args, **kwargs): return [DummyRow()]
    monkeypatch.setattr('backend.app.main.get_cassandra_session', lambda: DummySession())

@pytest.fixture(autouse=True)
def set_env_ci(monkeypatch):
    # Ensure HS256 fallback active
    monkeypatch.setenv('ENV', 'dev')
    monkeypatch.setenv('DEV_JWT_SECRET', auth_mod.DEV_JWT_SECRET)

@pytest.fixture()
def override_jwks(monkeypatch):
    # For RS256: override JWKS fetch to return our jwk
    def fake_get_jwks():
        return [override_jwks.jwk]
    monkeypatch.setattr(auth_mod, '_get_jwks', fake_get_jwks)
    return fake_get_jwks

@pytest.mark.parametrize("scopes,exp,alg,status_code,reason", [
    ("gibsey.vault.read gibsey.chat gibsey.search", '1h', 'HS256', 200, None),
    ("other.scope", '1h', 'HS256', 403, 'Missing required scope'),
    ("gibsey.vault.read", '0s', 'HS256', 401, 'Could not validate credentials'),
])
def test_hs256_cases(scopes, exp, alg, status_code, reason):
    token, _ = make_token(scopes, exp, alg)
    headers = {'Authorization': f'Bearer {token}'}
    resp = testapp.get('/pages/entrance/1', headers=headers)
    assert resp.status_code == status_code
    if reason:
        assert reason in resp.json().get('detail', '')

def test_rs256_valid(override_jwks):
    # Generate RS256 token and capture jwk for verify
    token, jwk_dict = make_token("gibsey.vault.read", '1h', 'RS256')
    override_jwks.jwk = jwk_dict
    headers = {'Authorization': f'Bearer {token}'}
    resp = testapp.get('/pages/entrance/1', headers=headers)
    assert resp.status_code == 200 