import httpx
from django.http import JsonResponse
from django.views import View

from apps.experiments.async_bench.tasks import process_order_notification

SIMULATED_DELAY_SECONDS = 1.0
SIMULATED_EXTERNAL_API_URL = f"https://httpbin.org/delay/{int(SIMULATED_DELAY_SECONDS)}"


class NotifySyncView(View):
    """Scenario A — Sync (WSGI). Blocks the request thread."""

    def get(self, request):
        response = httpx.get(SIMULATED_EXTERNAL_API_URL, timeout=10)
        response.raise_for_status()
        return JsonResponse({"status": "done", "mode": "sync"})


async def notify_async_view(request):
    """Scenario B — Async (ASGI). Awaits without blocking the thread."""
    async with httpx.AsyncClient() as client:
        response = await client.get(SIMULATED_EXTERNAL_API_URL, timeout=10)
        response.raise_for_status()
    return JsonResponse({"status": "done", "mode": "async"})


class NotifyOffloadedView(View):
    """Scenario C — Offloaded (Celery). Returns immediately."""

    def get(self, request):
        process_order_notification.delay(
            order_id=0,
            delay_seconds=SIMULATED_DELAY_SECONDS,
        )
        return JsonResponse({"status": "queued", "mode": "offloaded"})