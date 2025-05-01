#!/usr/bin/env python3
"""
Benchmark script for GET /search endpoint with dynamic HNSW params.
"""
import argparse
import time
import statistics
import requests
import json
from datetime import datetime
from pathlib import Path

# Default server URL
URL = "http://127.0.0.1:8000/search"


def parse_args():
    parser = argparse.ArgumentParser(description="Benchmark search endpoint latency")
    parser.add_argument("--runs", type=int, default=100, help="Number of queries to send")
    parser.add_argument("--ef", type=int, default=64, help="HNSW ef (search) parameter")
    parser.add_argument("--M", type=int, default=8, help="HNSW M (construction) parameter placeholder")
    parser.add_argument("--k", type=int, default=5, help="Number of results per query")
    parser.add_argument("--q", type=str, default="author", help="Base query term")
    return parser.parse_args()


def main():
    args = parse_args()
    latencies = []
    for i in range(args.runs):
        params = {
            "q": args.q,
            "k": args.k,
            "engine": "native",
            "ef": args.ef,
            "M": args.M,
        }
        start = time.perf_counter()
        try:
            response = requests.get(URL, params=params)
            response.raise_for_status()
        except Exception as e:
            print(f"Request {i+1} failed: {e}")
            continue
        elapsed = (time.perf_counter() - start) * 1000
        latencies.append(elapsed)
    if not latencies:
        print("No successful requests.")
        return
    stats = {
        "runs": len(latencies),
        "mean_ms": statistics.mean(latencies),
        "p50_ms": statistics.quantiles(latencies, n=100)[49],
        "p90_ms": statistics.quantiles(latencies, n=100)[89],
        "p95_ms": statistics.quantiles(latencies, n=100)[94],
        "max_ms": max(latencies),
    }
    # Print summary
    print(f"Mean: {stats['mean_ms']:.1f}ms | p50: {stats['p50_ms']:.1f}ms | p90: {stats['p90_ms']:.1f}ms | p95: {stats['p95_ms']:.1f}ms | max: {stats['max_ms']:.1f}ms")
    # Write JSON
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    out_dir = Path("benchmarks")
    out_dir.mkdir(exist_ok=True)
    fname = out_dir / f"search_{ts}.json"
    with open(fname, "w") as f:
        json.dump({**stats, "ef": args.ef, "M": args.M, "latencies_ms": latencies}, f, indent=2)
    print(f"Saved benchmark → {fname}")


if __name__ == "__main__":
    main()