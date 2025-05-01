import os

import logging
from fastapi import FastAPI, HTTPException, Depends, Request, Query
import os

# Optional dependencies: dotenv, cassandra, numpy, openai
try:
    from dotenv import load_dotenv
except ImportError:
    # no-op stub if python-dotenv not installed
    def load_dotenv():
        return None
try:
    from cassandra.cluster import Cluster
except ImportError:
    Cluster = None
try:
    import heapq, numpy as np
except ImportError:
    # fallback stubs if numpy not installed; minimal stubs for import only
    heapq = None
    np = None
try:
    from cassandra import util as cass_util  # provides Vector in driver ≥ 3.29
    HAS_NATIVE = True
except ImportError:
    HAS_NATIVE = False
try:
    import openai
except ImportError:
    # stub openai module if not installed
    import types
    openai = types.SimpleNamespace()
    # stub Embedding API
    class _EmbeddingStub:
        @staticmethod
        def create(*args, **kwargs):
            raise NotImplementedError("openai.Embedding.create not available")
    openai.Embedding = _EmbeddingStub
    # stub error classes
    openai.error = types.SimpleNamespace(RateLimitError=Exception)
    # allow setting api_key attribute
    openai.api_key = None
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from datetime import datetime
import openai
import math
import time
from fastapi.responses import StreamingResponse
from auth import verify_token

load_dotenv()
if hasattr(openai, 'api_key'):
    openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()
# Initialize logger for API
logger = logging.getLogger("api")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Log entry and exit of each route
    try:
        logger.info(f"ENTER {request.url.path}")
    except Exception:
        pass
    response = await call_next(request)
    try:
        logger.debug(f"EXIT {request.url.path}")
    except Exception:
        pass
    return response

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/search-native-test")
async def search_native_test(q: str = Query("door"), k: int = Query(5)):
    """Test endpoint for ANN search without authentication"""
    if os.getenv("SEARCH_ENABLED", "false").lower() != "true":
        raise HTTPException(status_code=404, detail="Search disabled")
    
    start_time = time.time()
    
    # Generate embedding
    resp = openai.Embedding.create(
        model="text-embedding-3-small",
        input=q
    )
    q_vec = resp["data"][0]["embedding"]
    
    # Using Native ANN with HNSW
    import numpy as np
    import ann_hnsw
    q_np = np.asarray(q_vec, dtype=np.float32)
    
    try:
        hits = ann_hnsw.query(q_np, k)
        results = []
        for int_id, dist in hits:
            story_id, page_num = ann_hnsw.unpack_id(int_id)
            results.append({"story_id": story_id, "page_num": page_num, "score": 1 - dist})
    except Exception as e:
        # Fallback: return error information if HNSW index not available
        return {
            "error": f"HNSW index query failed: {str(e)}",
            "status": "The index may not be populated yet. Run the embed_load.py script to populate the index."
        }
    
    latency = time.time() - start_time
    return {"query": q, "results": results, "latency_seconds": latency}

def get_cassandra_session():
    cass_host = os.getenv("CASS_HOST", "localhost")
    cass_keyspace = os.getenv("CASS_KEYSPACE", "gibsey")
    cluster = Cluster([cass_host])
    return cluster.connect(cass_keyspace)

@app.get("/pages/{story_id}/{page_num}", dependencies=[Depends(verify_token)])
async def read_page(story_id: str, page_num: int):
    session = get_cassandra_session()
    query = "SELECT * FROM pages WHERE story_id = ? AND page_num = ?"
    prepared = session.prepare(query)
    result = session.execute(prepared, (story_id, page_num))
    row = result.one()
    if not row:
        raise HTTPException(status_code=404, detail="Page not found")
    return dict(row._asdict())

@app.get("/stories/{story_id}")
async def read_story(story_id: str):
    session = get_cassandra_session()
    query = "SELECT * FROM stories WHERE story_id = ?"
    prepared = session.prepare(query)
    result = session.execute(prepared, (story_id,))
    row = result.one()
    if not row:
        raise HTTPException(status_code=404, detail="Story not found")
    return dict(row._asdict())

@app.get("/bots/{bot_id}")
async def read_bot(bot_id: str):
    session = get_cassandra_session()
    query = "SELECT * FROM bots WHERE bot_id = ?"
    prepared = session.prepare(query)
    result = session.execute(prepared, (bot_id,))
    row = result.one()
    if not row:
        raise HTTPException(status_code=404, detail="Bot not found")
    return dict(row._asdict())

@app.get("/vault/{user_id}")
async def read_vault(user_id: str):
    session = get_cassandra_session()
    query = "SELECT * FROM vault WHERE user_id = ?"
    prepared = session.prepare(query)
    results = session.execute(prepared, (user_id,))
    return [dict(row._asdict()) for row in results]

class PageIn(BaseModel):
    story_id: str
    page_num: int
    embedding: List[float]

@app.post("/pages")
async def create_page(page: PageIn):
    session = get_cassandra_session()
    query = "INSERT INTO pages (story_id, page_num, embedding) VALUES (?, ?, ?)"
    prepared = session.prepare(query)
    session.execute(prepared, (page.story_id, page.page_num, page.embedding))
    return {"status": "created", "resource": "page", "id": {"story_id": page.story_id, "page_num": page.page_num}}

class StoryIn(BaseModel):
    story_id: str

@app.post("/stories")
async def create_story(item: StoryIn):
    session = get_cassandra_session()
    query = "INSERT INTO stories (story_id) VALUES (?)"
    prepared = session.prepare(query)
    session.execute(prepared, (item.story_id,))
    return {"status": "created", "resource": "story", "story_id": item.story_id}

class BotIn(BaseModel):
    bot_id: str

@app.post("/bots")
async def create_bot(item: BotIn):
    session = get_cassandra_session()
    query = "INSERT INTO bots (bot_id) VALUES (?)"
    prepared = session.prepare(query)
    session.execute(prepared, (item.bot_id,))
    return {"status": "created", "resource": "bot", "bot_id": item.bot_id}

class VaultIn(BaseModel):
    user_id: str
    ts: datetime

@app.post("/vault")
async def create_vault(entry: VaultIn):
    session = get_cassandra_session()
    query = "INSERT INTO vault (user_id, ts) VALUES (?, ?)"
    prepared = session.prepare(query)
    session.execute(prepared, (entry.user_id, entry.ts))
    return {"status": "created", "resource": "vault", "user_id": entry.user_id, "ts": entry.ts.isoformat()}

class SearchRequest(BaseModel):
    q: str
    k: int = 5

@app.post("/search", dependencies=[Depends(verify_token)])
async def search(req: SearchRequest):
    if os.getenv("SEARCH_ENABLED", "false").lower() != "true":
        raise HTTPException(status_code=404, detail="Search disabled")
    # Generate query embedding with retry/backoff
    max_attempts = 3
    delay = 1
    for attempt in range(max_attempts):
        try:
            # Legacy v0.28.1 API
            resp = openai.Embedding.create(
                model='text-embedding-3-small', input=req.q
            )
            break
        except openai.error.RateLimitError:
            if attempt == max_attempts - 1:
                raise HTTPException(status_code=429, detail="Rate limit exceeded")
            time.sleep(delay)
            delay *= 2
    # Extract embedding from legacy response
    q_vec = resp['data'][0]['embedding']
    # Fetch all pages
    session = get_cassandra_session()
    rows = session.execute("SELECT page_num, html, embedding FROM pages")
    norm_q = math.sqrt(sum(x*x for x in q_vec))
    results = []
    for r in rows:
        vec = r.embedding
        dot = sum(a*b for a,b in zip(q_vec, vec))
        norm_r = math.sqrt(sum(x*x for x in vec))
        score = (dot/(norm_q*norm_r)) if norm_q and norm_r else 0.0
        results.append({"page_num": r.page_num, "html": r.html, "score": score})
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:req.k]

@app.get("/search", dependencies=[Depends(verify_token)])
async def search_pages(
    q: str = Query(..., min_length=1, max_length=512),
    k: int = Query(5, ge=1),
    engine: str = Query("native")
):
    """Return k most similar pages. engine=native|python"""
    resp = openai.Embedding.create(
        model="text-embedding-3-small",
        input=q
    )
    q_vec = resp["data"][0]["embedding"]

    # Native ANN with HNSW
    if engine == "native":
        import numpy as np
        import ann_hnsw
        q_np = np.asarray(q_vec, dtype=np.float32)
        try:
            hits = ann_hnsw.query(q_np, k)
            results = []
            for int_id, dist in hits:
                story_id, page_num = ann_hnsw.unpack_id(int_id)
                results.append({"story_id": story_id, "page_num": page_num, "score": 1 - dist})
            return {"query": q, "results": results}
        except Exception as e:
            # Fall back to NumPy cosine search if HNSW fails
            return {"query": q, "results": [], "error": f"HNSW search failed: {str(e)}", "engine": "native_failed"}

    # --- NumPy cosine fallback ---
    session = get_cassandra_session()
    rows = session.execute("SELECT story_id, page_num, embedding FROM pages")
    q_np = np.asarray(q_vec, dtype=np.float32)
    q_np /= np.linalg.norm(q_np) + 1e-9
    scored = []
    for r in rows:
        v = np.asarray(r.embedding, dtype=np.float32)
        score = float(np.dot(q_np, v) / (np.linalg.norm(v) + 1e-9))
        scored.append((score, r.story_id, r.page_num))
    top = heapq.nlargest(k, scored, key=lambda x: x[0])
    return {"query": q, "results": [{"story_id": sid, "page_num": pn, "score": s} for s, sid, pn in top]}

class ChatRequest(BaseModel):
    q: str
    k: int = 5

@app.post("/chat", dependencies=[Depends(verify_token)])
async def chat(req: ChatRequest):
    if os.getenv("SEARCH_ENABLED", "false").lower() != "true":
        raise HTTPException(status_code=404, detail="Chat disabled")
    # Retrieve top context pages
    search_req = SearchRequest(q=req.q, k=req.k)
    context_pages = await search(search_req)
    # Build prompt with context
    docs = "\n".join([f"Page {p['page_num']}: {p['html']}" for p in context_pages])
    prompt = f"Answer question: {req.q}\n\nContext:\n{docs}"
    # Non-streaming chat completion for easy consumption
    resp = openai.ChatCompletion.create(
        model='gpt-4o',
        messages=[
            {'role':'system', 'content':'You are a helpful assistant.'},
            {'role':'user', 'content': prompt}
        ]
    )
    answer = resp.choices[0].message.content
    return {"answer": answer, "source": context_pages} 