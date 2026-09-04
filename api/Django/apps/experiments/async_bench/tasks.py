import logging
import time

import httpx
from celery import shared_task

logger = logging.getLogger(__name__)

SIMULATED_EXTERNAL_API_URL = "https://httpbin.org/delay/{seconds}"


@shared_task(name="experiments.async_bench.process_order_notification")
def process_order_notification(order_id: int, delay_seconds: float = 1.0):
    """
    Simulates an I/O-bound side effect that a request might otherwise have
    to wait on inline — e.g. calling a third-party notification/email API.

    Used by BENCH-010 (Async vs Sync) as the "offloaded" scenario: the
    view enqueues this task and returns immediately, instead of blocking
    (sync) or awaiting (async) the same simulated call inline.
    """
    started_at = time.monotonic()

    try:
        response = httpx.get(
            SIMULATED_EXTERNAL_API_URL.format(seconds=delay_seconds),
            timeout=delay_seconds + 5,
        )
        response.raise_for_status()

    except httpx.HTTPError:
        logger.exception(
            "Simulated external API call failed for order #%s", order_id
        )
        raise

    duration = time.monotonic() - started_at

    logger.info(
        "process_order_notification: order=%s requested_delay=%.2fs actual=%.2fs",
        order_id,
        delay_seconds,
        duration,
    )

    return {
        "order_id": order_id,
        "requested_delay_seconds": delay_seconds,
        "actual_duration_seconds": duration,
    }