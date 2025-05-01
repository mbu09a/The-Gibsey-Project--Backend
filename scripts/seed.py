#!/usr/bin/env python3
"""Seed Cassandra with the 710‑page corpus and build a local HNSW index.

Usage::

    python -m scripts.seed [--force] [--dry-run]

The script is *idempotent* – if the pages table already contains 710
rows **and** the HNSW index exists it exits early unless `--force`
flag is supplied.

Steps
-----
1. Load ``data/cleaned_normalised.txt`` (marker ``###Page <n>###``)
   into a list of pages.
2. Embed each page via OpenAI `text-embedding-3-small`.
   • Results are cached in ``data/vectors.npy`` to avoid re‑billing.
3. Insert missing rows into Cassandra keyspace ``gibsey`` table
   ``pages``, storing the embedding in the native 1536‑d vector column.
4. Build a cosine HNSW index with *hnswlib* and write to
   ``data/hnsw.idx``.
5. Drop a SHA‑256 manifest ``data/corpus.manifest.json`` with
   counts + file hashes so subsequent runs can validate quickly.

Environment
-----------
Needs ``OPENAI_API_KEY`` and Cassandra reachable at ``$CASS_HOST``
(default *localhost*).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Optional

from tqdm import tqdm

# Lazy / optional deps guarded for unit‑test environments
try:
    import numpy as np  # type: ignore
except ImportError:  # pragma: no cover
    np = None  # type: ignore
try:
    import openai  # type: ignore
except ImportError:  # pragma: no cover
    openai = None  # type: ignore
try:
    import hnswlib  # type: ignore
except ImportError:  # pragma: no cover
    hnswlib = None  # type: ignore
try:
    from cassandra.cluster import Cluster  # type: ignore
except Exception as exc:  # catch DependencyException or ImportError
    Cluster = None  # type: ignore
    IMPORT_ERROR = exc
try:
    from cassandra.query import BatchStatement  # type: ignore
except Exception:
    BatchStatement = None  # type: ignore

# ---------------------------------------------------------------------------
# Constants & Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
CORPUS_TXT = DATA_DIR / "cleaned_normalised.txt"
VEC_NPY = DATA_DIR / "vectors.npy"
HNSW_IDX = DATA_DIR / "hnsw.idx"
MANIFEST = DATA_DIR / "corpus.manifest.json"
EXPECTED_COUNT = 710
EMBED_MODEL = "text-embedding-3-small"
DIM = 1536
BATCH = 20  # embed batch size – tweak to stay under rate limits

STORY_ID = "entrance"  # single story – can extend later

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def split_pages(text: str) -> List[str]:
    """Split the corpus by the ###Page n### markers."""
    pages: List[str] = []
    buf: List[str] = []
    for line in text.splitlines():
        if line.startswith("###Page "):
            # flush previous page
            if buf:
                pages.append("\n".join(buf).strip())
                buf.clear()
            continue  # do not include marker line itself
        buf.append(line)
    if buf:
        pages.append("\n".join(buf).strip())
    return pages


# ---------------------------------------------------------------------------
# Cassandra helpers – skip when dry‑run or driver not installed
# ---------------------------------------------------------------------------


def connect_cassandra() -> "Cluster":  # type: ignore[name-defined]
    if Cluster is None:
        raise RuntimeError("cassandra-driver not installed")
    host = os.getenv("CASS_HOST", "localhost")
    keyspace = os.getenv("CASS_KEYSPACE", "gibsey")
    cluster = Cluster([host])
    sess = cluster.connect()
    # ensure keyspace exists (simple strategy for dev)
    sess.execute(
        f"""
        CREATE KEYSPACE IF NOT EXISTS {keyspace}
        WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}};
        """
    )
    sess.set_keyspace(keyspace)
    # ensure table exists
    sess.execute(
        """
        CREATE TABLE IF NOT EXISTS pages (
            story_id text,
            page_num int,
            html text,
            embedding vector<float, 1536>,
            PRIMARY KEY (story_id, page_num)
        );
        """
    )
    return sess


def count_pages(sess) -> int:  # type: ignore[valid-type]
    res = sess.execute("SELECT COUNT(*) FROM pages WHERE story_id=%s", (STORY_ID,))
    return res.one()[0]


# ---------------------------------------------------------------------------
# Embedding + caching
# ---------------------------------------------------------------------------


def embed_batch(texts: List[str]) -> List[List[float]]:
    if openai is None:
        raise RuntimeError("openai package not installed")
    tries = 0
    while True:
        try:
            resp = openai.Embedding.create(model=EMBED_MODEL, input=texts)
            data = resp["data"]
            return [d["embedding"] for d in data]
        except openai.error.RateLimitError:  # type: ignore[attr-defined]
            tries += 1
            delay = 2**min(tries, 5)
            print(f"Rate‑limited, backing off {delay}s …", file=sys.stderr)
            time.sleep(delay)
        except Exception as e:  # pragma: no cover
            print(f"Embed error: {e}", file=sys.stderr)
            raise


# ---------------------------------------------------------------------------
# HNSW build
# ---------------------------------------------------------------------------


def build_hnsw(vectors: "np.ndarray") -> None:  # type: ignore[name-defined]
    if hnswlib is None:
        raise RuntimeError("hnswlib not installed – cannot build index")
    idx = hnswlib.Index(space="cosine", dim=DIM)
    idx.init_index(max_elements=len(vectors), ef_construction=200, M=16)
    idx.add_items(vectors, list(range(len(vectors))))
    idx.save_index(str(HNSW_IDX))


# ---------------------------------------------------------------------------
# Manifest logic
# ---------------------------------------------------------------------------


def write_manifest(page_ct: int) -> None:
    manifest = {
        "pages": page_ct,
        "vectors": str(VEC_NPY),
        "index": str(HNSW_IDX),
        "txt_sha": sha256(CORPUS_TXT) if CORPUS_TXT.exists() else None,
        "vec_sha": sha256(VEC_NPY) if VEC_NPY.exists() else None,
        "idx_mtime": HNSW_IDX.stat().st_mtime if HNSW_IDX.exists() else None,
        "generated": datetime.utcnow().isoformat() + "Z",
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2))


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Seed corpus & build ANN index")
    parser.add_argument("--force", action="store_true", help="Rebuild even if already seeded")
    parser.add_argument("--dry-run", action="store_true", help="Parse & embed only, no DB / index writes")
    args = parser.parse_args()

    # Ensure Cassandra driver is available when not in dry-run
    if Cluster is None and not args.dry_run:
        print(
            "Cassandra driver unavailable (import error: %s)\n" \
            % (getattr(globals(), 'IMPORT_ERROR', 'Unknown import error')),
            file=sys.stderr,
        )
        sys.exit(1)

    start = time.time()
    if not CORPUS_TXT.exists():
        print(f"Corpus file {CORPUS_TXT} not found", file=sys.stderr)
        sys.exit(1)

    # Fast‑path idempotence check
    up_to_date = VEC_NPY.exists() and HNSW_IDX.exists()
    if not args.force and up_to_date:
        try:
            vecs = np.load(VEC_NPY) if np is not None else None  # type: ignore[arg-type]
            if vecs is not None and vecs.shape[0] == EXPECTED_COUNT:
                if Cluster is not None and not args.dry_run:
                    sess = connect_cassandra()
                    if count_pages(sess) == EXPECTED_COUNT:
                        print("Corpus + index already present – use --force to rebuild")
                        return
        except Exception:
            pass  # treat as not up‑to‑date

    text = CORPUS_TXT.read_text(encoding="utf-8")
    pages = split_pages(text)
    if len(pages) != EXPECTED_COUNT:
        print(f"Expected {EXPECTED_COUNT} pages, got {len(pages)}", file=sys.stderr)
        if not args.force:
            sys.exit(1)

    # Step 2: embeddings with caching
    if np is None:
        raise RuntimeError("numpy required for embedding cache")

    vectors: "np.ndarray"
    if VEC_NPY.exists() and not args.force:
        vectors = np.load(VEC_NPY)
        if vectors.shape[0] != EXPECTED_COUNT:
            print("Vector cache shape mismatch – regenerating", file=sys.stderr)
            vectors = np.empty((0, DIM), dtype=np.float32)  # trigger embed
    else:
        vectors = np.empty((0, DIM), dtype=np.float32)

    missing = EXPECTED_COUNT - vectors.shape[0]
    if missing > 0:
        if openai is None:
            raise RuntimeError("openai required to generate embeddings")
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            print("OPENAI_API_KEY env var missing", file=sys.stderr)
            sys.exit(1)

        print(f"Embedding {missing} new pages …")
        new_vecs: List[List[float]] = []
        for i in tqdm(range(0, EXPECTED_COUNT, BATCH)):
            batch_pages = pages[i : i + BATCH]
            batch_vecs = embed_batch(batch_pages)
            new_vecs.extend(batch_vecs)
        vectors = np.asarray(new_vecs, dtype=np.float32)
        np.save(VEC_NPY, vectors)
        print(f"Saved vectors → {VEC_NPY}")

    # Dry‑run stops here
    if args.dry_run:
        write_manifest(len(pages))
        print("Dry‑run complete – no DB or index writes")
        return

    # Cassandra insert
    sess = connect_cassandra()
    if args.force:
        sess.execute("TRUNCATE TABLE pages")
    existing = count_pages(sess)
    if existing < EXPECTED_COUNT:
        insert_stmt = sess.prepare(
            "INSERT INTO pages (story_id, page_num, html, embedding) VALUES (?, ?, ?, ?)"
        )
        print(f"Inserting {EXPECTED_COUNT - existing} rows into Cassandra …")
        batch = BatchStatement()
        for idx, page in tqdm(list(enumerate(pages, start=1))):
            if idx <= existing:
                continue  # already present
            batch.add(insert_stmt, (STORY_ID, idx, page, vectors[idx - 1].tolist()))
            # Flush every 50 to avoid huge batch
            if idx % 50 == 0:
                sess.execute(batch)
                batch.clear()
        if batch:
            sess.execute(batch)
        print("Cassandra load complete")
    else:
        print("Cassandra already has full corpus")

    # Build HNSW
    print("Building HNSW index …")
    build_hnsw(vectors)
    print(f"Index written → {HNSW_IDX}")

    write_manifest(len(pages))
    print("✔ seed complete in %.1fs" % (time.time() - start))


if __name__ == "__main__":
    main() 