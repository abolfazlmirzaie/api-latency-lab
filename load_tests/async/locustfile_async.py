"""
Locust load test — Scenario B: Async (ASGI)

Must be run against a server actually served over ASGI (e.g. Daphne or
Uvicorn) — running this against a plain WSGI dev server will not exercise
the non-blocking behavior being measured.

Usage:
    locust -f load-tests/locust/async/locustfile_async.py --host=http://localhost:8000
"""

from locust import HttpUser, task, constant


class AsyncNotifyUser(HttpUser):
    wait_time = constant(0)

    @task
    def notify_async(self):
        self.client.get("/lab/async/notify-async/", name="notify-async")