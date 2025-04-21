import numpy as np
from pathlib import Path
import subprocess, sys

def test_seed_dry_run(tmp_path, monkeypatch):
    """Dry‑run should create manifest and vectors without touching DB."""
    proj_root = Path(__file__).resolve().parents[2]
    data_dir = proj_root / "data"
    # isolate vector/manifest paths in tmp to avoid clobbering
    monkeypatch.setattr("scripts.seed.VEC_NPY", tmp_path / "vectors.npy", raising=False)
    monkeypatch.setattr("scripts.seed.HNSW_IDX", tmp_path / "hnsw.idx", raising=False)
    monkeypatch.setattr("scripts.seed.MANIFEST", tmp_path / "corpus.manifest.json", raising=False)

    # run as module
    cmd = [sys.executable, "-m", "scripts.seed", "--dry-run", "--force"]
    subprocess.check_call(cmd, cwd=str(proj_root))

    vec = np.load(tmp_path / "vectors.npy")
    assert vec.shape == (710, 1536)
    assert (tmp_path / "corpus.manifest.json").exists() 