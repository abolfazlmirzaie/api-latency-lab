"""
Locust load test — Scenario C: Offloaded (Celery)

Note: this scenario only measures the latency of *enqueueing* the task,
not the actual I/O-bound work itself (which happens out-of-band on a
Celery worker). Requires a Celery worker to be running and connected to
the same broker so tasks don't just pile up unprocessed in the queue —
per BENCH-010, queue lag should also be checked separately to confirm
the worker pool isn't itself becoming a bottleneck at high concurrency.

Usage:
    locust -f load-tests/locust/async/locustfile_offloaded.py --host=http://localhost:8000
"""

from locust import HttpUser, task, constant


class OffloadedNotifyUser(HttpUser):
    wait_time = constant(0)

    @task
    def notify_offloaded(self):
        self.client.get("/lab/async/notify-offloaded/", name="notify-offloaded")