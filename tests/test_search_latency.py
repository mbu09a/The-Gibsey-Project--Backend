import statistics
import random
import time
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

TEST_COUNT = 100
P95_THRESHOLD_MS = 250


def load_queries() -> list[str]:
    text = Path("data/cleaned_normalised.txt").read_text(encoding="utf-8")
    pages = []
    buf = []
    for line in text.splitlines():
        if line.startswith("###Page "):
            if buf:
                snippet = " ".join(" ".join(buf).split()[:8])
                pages.append(snippet)
                buf = []
            continue
        buf.append(line)
    if buf:
        pages.append(" ".join(" ".join(buf).split()[:8]))
    return pages

client = TestClient(app)

@pytest.mark.skipif(not Path("data/hnsw.idx").exists(), reason="Run `make seed` before running latency tests")
def test_search_latency_p95():
    queries = load_queries()
    latencies = []
    for _ in range(TEST_COUNT):
        q = random.choice(queries)
        start = time.perf_counter()
        response = client.get("/search", params={"q": q, "k": 5})
        elapsed_ms = (time.perf_counter() - start) * 1000
        latencies.append(elapsed_ms)
        assert response.status_code == 200
    latencies.sort()
    p95 = statistics.quantiles(latencies, n=100)[94]
    assert p95 <= P95_THRESHOLD_MS, f"Search p95 latency {p95:.1f}ms exceeds {P95_THRESHOLD_MS}ms" 