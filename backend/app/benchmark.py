import time
import math
import numpy as np
import random

# Create a mock dataset
def generate_mock_data(num_rows=1000, dim=1536):
    data = []
    for i in range(num_rows):
        embedding = [random.random() for _ in range(dim)]
        data.append({
            "story_id": f"story_{i}",
            "page_num": i,
            "embedding": embedding
        })
    return data

# Generate a mock query vector
def generate_query_vector(dim=1536):
    return [random.random() for _ in range(dim)]

# Pure Python implementation
def pure_python_search(rows, q_vec, k=5):
    norm_q = math.sqrt(sum(x*x for x in q_vec))
    results = []
    for r in rows:
        vec = r["embedding"]
        dot = sum(a*b for a,b in zip(q_vec, vec))
        norm_r = math.sqrt(sum(x*x for x in vec))
        score = (dot/(norm_q*norm_r)) if norm_q and norm_r else 0.0
        results.append({
            "story_id": r["story_id"],
            "page_num": r["page_num"],
            "score": score
        })
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:k]

# NumPy implementation
def numpy_search(rows, q_vec, k=5):
    q_np = np.asarray(q_vec, dtype=np.float32)
    q_np /= np.linalg.norm(q_np) + 1e-9
    scored = []
    for r in rows:
        v = np.asarray(r["embedding"], dtype=np.float32)
        score = float(np.dot(q_np, v) / (np.linalg.norm(v) + 1e-9))
        scored.append((score, r["story_id"], r["page_num"]))
    top = sorted(scored, key=lambda x: x[0], reverse=True)[:k]
    return [{"story_id": sid, "page_num": pn, "score": s} for s, sid, pn in top]

def run_benchmark(num_rows=100, dim=1536, k=5, iterations=5):
    data = generate_mock_data(num_rows, dim)
    q_vec = generate_query_vector(dim)
    
    # Warm-up
    pure_python_search(data, q_vec, k)
    numpy_search(data, q_vec, k)
    
    # Benchmark pure Python
    start = time.time()
    for _ in range(iterations):
        pure_python_search(data, q_vec, k)
    python_time = (time.time() - start) / iterations
    
    # Benchmark NumPy
    start = time.time()
    for _ in range(iterations):
        numpy_search(data, q_vec, k)
    numpy_time = (time.time() - start) / iterations
    
    return {
        "python_time": python_time,
        "numpy_time": numpy_time,
        "speedup": python_time / numpy_time if numpy_time > 0 else float('inf')
    }

if __name__ == "__main__":
    print("Running benchmark...")
    small_result = run_benchmark(num_rows=100, iterations=10)
    print(f"Small dataset (100 rows):")
    print(f"  Pure Python: {small_result['python_time']:.6f} seconds")
    print(f"  NumPy:       {small_result['numpy_time']:.6f} seconds")
    print(f"  Speedup:     {small_result['speedup']:.2f}x\n")
    
    medium_result = run_benchmark(num_rows=1000, iterations=5)
    print(f"Medium dataset (1000 rows):")
    print(f"  Pure Python: {medium_result['python_time']:.6f} seconds")
    print(f"  NumPy:       {medium_result['numpy_time']:.6f} seconds")
    print(f"  Speedup:     {medium_result['speedup']:.2f}x\n")
    
    large_result = run_benchmark(num_rows=5000, iterations=2)
    print(f"Large dataset (5000 rows):")
    print(f"  Pure Python: {large_result['python_time']:.6f} seconds")
    print(f"  NumPy:       {large_result['numpy_time']:.6f} seconds")
    print(f"  Speedup:     {large_result['speedup']:.2f}x") 