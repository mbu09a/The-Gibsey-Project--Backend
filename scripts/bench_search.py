#!/usr/bin/env python3
"""
Benchmark script for GET /search endpoint.
Sends 50 requests and reports min, max, and average latency.
"""
import time
import statistics
import requests

def main():
    url = "http://127.0.0.1:8000/search"
    params = {"q": "author", "k": 5, "engine": "native"}
    latencies = []
    for i in range(50):
        start = time.perf_counter()
        try:
            response = requests.get(url, params=params)
        except Exception as e:
            print(f"Request {i+1} failed: {e}")
            continue
        elapsed = time.perf_counter() - start
        latencies.append(elapsed)
        if response.status_code != 200:
            print(f"Request {i+1} returned status {response.status_code}")
    if not latencies:
        print("No successful requests to measure.")
        return
    print(f"Min latency: {min(latencies):.4f}s")
    print(f"Max latency: {max(latencies):.4f}s")
    print(f"Avg latency: {statistics.mean(latencies):.4f}s")

if __name__ == "__main__":
    main()