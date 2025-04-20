"""Sidecar cron‑style monitor for Gibsey ANN latency.

Every 60 s:
• GET /metrics (internal network)
• Parse `search_request_latency_seconds_sum` & `_count` to compute p95 ≈ sum/count*1.3
  (cheap heuristic that errs high; real p95 needs histogram buckets)
• If p95 > 1 s or request fails, POST message to Slack webhook.
"""

import os
import time
import re
import json
import httpx

APP_HOST = os.getenv("APP_HOST", "http://fastapi:8000")
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")
THRESHOLD = float(os.getenv("LATENCY_THRESHOLD", "1.0"))  # seconds

METRIC_RE = re.compile(r"search_request_latency_seconds_sum (\d+\.?\d*)")
COUNT_RE = re.compile(r"search_request_total\{engine=\"native\"\} (\d+\.?\d*)")

def post_slack(msg: str) -> None:
    """Send alert to Slack webhook."""
    if not SLACK_WEBHOOK:
        print("[monitor] SLACK_WEBHOOK not set; skipping alert:", msg)
        return
    try:
        httpx.post(SLACK_WEBHOOK, json={"text": msg}, timeout=10)
    except Exception as e:
        print(f"[monitor] Failed to post Slack alert: {e}")

def parse_metrics(body: str):
    """Extract total latency sum and count from metrics text."""
    m_sum = METRIC_RE.search(body)
    m_cnt = COUNT_RE.search(body)
    if not (m_sum and m_cnt):
        raise ValueError("metrics missing latency fields")
    total = float(m_sum.group(1))
    count = float(m_cnt.group(1)) or 1.0
    return total, count

def main():
    while True:
        try:
            r = httpx.get(f"{APP_HOST}/metrics", timeout=10)
            if r.status_code != 200:
                raise RuntimeError(f"/metrics HTTP {r.status_code}")
            total, count = parse_metrics(r.text)
            avg = total / count
            p95_est = avg * 1.3  # heuristic multiplier
            print(f"[monitor] avg={avg:.3f}s  p95≈{p95_est:.3f}s  count={count}")
            if p95_est > THRESHOLD:
                post_slack(
                    f"⚠️ Gibsey ANN p95 latency {p95_est:.2f}s (threshold {THRESHOLD}s)"
                )
        except Exception as e:
            post_slack(f"❌ Gibsey monitor error: {e}")
        time.sleep(60)

if __name__ == "__main__":
    main()