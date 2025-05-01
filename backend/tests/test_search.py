from fastapi.testclient import TestClient
import pytest
from unittest.mock import patch, MagicMock

# Dev token for authentication
from auth import _issue_dev_token
# Import the FastAPI app and native flag
from main import app, HAS_NATIVE

client = TestClient(app)
# Generate and set auth header for all requests
token = _issue_dev_token()
headers = {"Authorization": f"Bearer {token}"}

@pytest.fixture
def mock_openai_embedding():
    with patch('openai.Embedding.create') as mock:
        # Mock embedding response
        mock.return_value = {
            "data": [
                {
                    "embedding": [0.1] * 1536,  # Simplified mock embedding
                    "index": 0,
                    "object": "embedding"
                }
            ],
            "model": "text-embedding-3-small",
            "object": "list",
            "usage": {"prompt_tokens": 8, "total_tokens": 8}
        }
        yield mock

@pytest.fixture
def mock_cassandra_session():
    # Patch Cassandra session in main module
    with patch('main.get_cassandra_session') as mock:
        session = MagicMock()
        
        # Mock rows without html field
        mock_row1 = MagicMock()
        mock_row1.story_id = "test_story_1"
        mock_row1.page_num = 1
        mock_row1.embedding = [0.1] * 1536
        
        mock_row2 = MagicMock()
        mock_row2.story_id = "test_story_2"
        mock_row2.page_num = 2
        mock_row2.embedding = [0.2] * 1536
        
        mock_row3 = MagicMock()
        mock_row3.story_id = "test_story_3"
        mock_row3.page_num = 3
        mock_row3.embedding = [0.3] * 1536
        
        # Set up the mock session to handle different query patterns
        def mock_execute(query, *args, **kwargs):
            # For ANN queries
            if isinstance(query, MagicMock) and args and len(args) > 0:
                return [mock_row1, mock_row2, mock_row3]
            # For normal SELECT queries
            else:
                return [mock_row1, mock_row2, mock_row3]
        
        session.execute = MagicMock(side_effect=mock_execute)
        
        # Mock the prepare method
        prepared = MagicMock()
        session.prepare.return_value = prepared
        
        mock.return_value = session
        yield mock

def test_search_endpoint(mock_openai_embedding, mock_cassandra_session):
    """Test the GET /search endpoint"""
    response = client.get("/search", params={"q": "an author", "k": 3}, headers=headers)
    
    # Check status code
    assert response.status_code == 200
    
    # Check response structure
    data = response.json()
    assert "query" in data
    assert "results" in data
    
    # Check query value
    assert data["query"] == "an author"
    
    # Check results length
    assert len(data["results"]) == 3
    
    # Check results structure - no HTML
    for result in data["results"]:
        assert "story_id" in result
        assert "page_num" in result
        assert "score" in result
        assert "html" not in result

def test_search_engine_python(mock_openai_embedding, mock_cassandra_session):
    """Test the GET /search endpoint with Python engine"""
    response = client.get("/search", params={"q": "an author", "k": 3, "engine": "python"}, headers=headers)
    
    # Check status code
    assert response.status_code == 200
    
    # Check response structure
    data = response.json()
    assert "query" in data
    assert "results" in data
    
    # Check query value
    assert data["query"] == "an author"
    
    # Check results length
    assert len(data["results"]) == 3
    
    # Check results structure
    for result in data["results"]:
        assert "story_id" in result
        assert "page_num" in result
        assert "score" in result
        assert "html" not in result

@pytest.mark.skipif(not HAS_NATIVE, reason="Native ANN not available")
def test_search_engine_native(mock_openai_embedding, mock_cassandra_session):
    """Test the GET /search endpoint with native engine"""
    response = client.get("/search", params={"q": "an author", "k": 3, "engine": "native"}, headers=headers)
    
    # Check status code
    assert response.status_code == 200
    
    # Check response structure
    data = response.json()
    assert "query" in data
    assert "results" in data
    
    # Check query value
    assert data["query"] == "an author"
    
    # Check results length
    assert len(data["results"]) == 3
    
    # Check results structure - no scores in native mode
    for result in data["results"]:
        assert "story_id" in result
        assert "page_num" in result
        assert "html" not in result

@pytest.mark.parametrize("q,k,status_code,len_results", [
    ("", None, 422, None),
    ("a" * 1024, None, 422, None),
    ("¿Quién es Gibsey?", 3, 200, 3),
    ("an author", 1, 200, 1),
])
def test_search_parameterized(mock_openai_embedding, mock_cassandra_session, q, k, status_code, len_results):
    """Parameterized tests for GET /search edge cases"""
    params = {"q": q}
    if k is not None:
        params["k"] = k
    response = client.get("/search", params=params, headers=headers)
    assert response.status_code == status_code
    if status_code == 200:
        data = response.json()
        assert "results" in data
        assert len(data["results"]) == len_results