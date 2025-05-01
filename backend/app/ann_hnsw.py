"""Lightweight ANN wrapper (cosine) stored at /data/hnsw.idx."""

import hnswlib, numpy as np, os
from typing import Dict, Tuple

DIM = 1536
PATH = "/data/hnsw.idx"

idx = hnswlib.Index(space="cosine", dim=DIM)
if os.path.exists(PATH):
    idx.load_index(PATH)
else:
    idx.init_index(max_elements=20000, ef_construction=200, M=16)

def add(vec: list[float], id_: int):
    idx.add_items(np.asarray([vec], dtype=np.float32), [id_])

# id map for reverse lookup of HNSW integer IDs
_id_map: Dict[int, Tuple[str, int]] = {}

def pack_id(story_id: str, page_num: int) -> int:
    """Pack a (story_id, page_num) into an integer and store mapping."""
    i = abs(hash(f"{story_id}|{page_num}")) % (2**31)
    _id_map[i] = (story_id, page_num)
    return i

def unpack_id(i: int) -> Tuple[str, int]:
    """Unpack an integer ID back into (story_id, page_num)."""
    return _id_map.get(i, ("unknown", 0))

def query(vec: np.ndarray, k: int):
    lbls, dists = idx.knn_query(vec.reshape(1, -1), k=k)
    return list(zip(lbls[0].tolist(), dists[0].tolist()))

def save():
    idx.save_index(PATH) 