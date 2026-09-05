import asyncio
import time

from django.http import JsonResponse
from django.views import View

from apps.experiments.async_bench.tasks import process_order_notification

# Simulated I/O wait time. Using a local sleep instead of a real external
# HTTP call (e.g. httpbin.org) removes any dependency on network/DNS
# conditions inside the container, so the only variable under test is the
# execution model (sync vs async vs offloaded) — not network flakiness.
# See benchmarks/async/Async-vs-Sync.md for the full benchmark definition.
SIMULATED_DELAY_SECONDS = 1.0


class NotifySyncView(View):
    """
    Scenario A — Sync (WSGI).
    Blocks the request thread for the duration of the simulated I/O wait.
    """

    def get(self, request):
        time.sleep(SIMULATED_DELAY_SECONDS)

        return JsonResponse({"status": "done", "mode": "sync"})


async def notify_async_view(request):
    """
    Scenario B — Async (ASGI).
    Awaits the same simulated wait without blocking the thread.

    Registered as a plain async function view rather than a class-based
    view, since Django's class-based View does not dispatch to async
    handlers the same way — this keeps it simple and explicit. Only
    behaves non-blockingly when served over ASGI (e.g. Daphne), not
    plain WSGI.
    """
    await asyncio.sleep(SIMULATED_DELAY_SECONDS)

    return JsonResponse({"status": "done", "mode": "async"})


class NotifyOffloadedView(View):
    """
    Scenario C — Offloaded (Celery).
    Enqueues the work and returns immediately without waiting on it.
    """

    def get(self, request):
        process_order_notification.delay(
            order_id=0,  # placeholder id, no real order needed for this benchmark
            delay_seconds=SIMULATED_DELAY_SECONDS,
        )

        return JsonResponse({"status": "queued", "mode": "offloaded"})