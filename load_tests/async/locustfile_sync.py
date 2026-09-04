"""
Locust load test — Scenario A: Sync (WSGI)

Targets a single endpoint in isolation. Per the project's experimental
rules (change one variable at a time), this file is intentionally kept
separate from the async and offloaded scenarios rather than combined
into one Locust file with multiple tasks — Locust would pick tasks at
random, mixing scenarios together and making results impossible to
attribute cleanly.

Usage:
    locust -f load-tests/locust/async/locustfile_sync.py --host=http://localhost:8000
"""

from locust import HttpUser, task, constant


class SyncNotifyUser(HttpUser):
    # No think time between requests — we want sustained load, not a
    # simulation of natural human pacing.
    wait_time = constant(0)

    @task
    def notify_sync(self):
        self.client.get("/lab/async/notify-sync/", name="notify-sync")