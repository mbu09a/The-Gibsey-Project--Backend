"""Headless load test for /search (native engine). Generates a dev token on start."""

import json, time
from locust import HttpUser, task, between, events


class SearchUser(HttpUser):
    wait_time = between(0.01, 0.02)  # ~50 RPS per user when u=3

    def on_start(self):
        # one dev token per user session
        import jwt, time
        payload = {
            "sub": "locust",
            "iat": int(time.time()),
            "exp": int(time.time()) + 3600,
        }
        # IMPORTANT: replace with your dev secret if different
        self.token = jwt.encode(payload, "your-secret-key", algorithm="HS256")

    @task
    def vector_search(self):
        payload = json.dumps({"q": "door", "k": 5})
        self.client.post(
            "/search",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}",
            },
            name="/search"
        )


# Custom summary at test end
@events.quitting.add_listener
def _(environment, **kwargs):
    if not environment.stats.total.num_requests:
        return
    # p95 in ms→s conversion
    p95 = environment.stats.total.get_response_time_percentile(0.95) / 1000
    print(
        f"\n⚡︎ p95 latency: {p95:.3f}s across {environment.stats.total.num_requests} requests"
    )