# BENCH-010 — Async vs Sync

## Question

Does converting an I/O-bound endpoint from a synchronous (WSGI) view to an
asynchronous (ASGI) view reduce latency — particularly p95/p99 — and
increase sustainable throughput under concurrent load, without changing
what the endpoint actually does?

As a secondary question: how does offloading the same I/O-bound work to a
Celery task (returning immediately instead of waiting on it at all)
compare to both of the above?

## Hypothesis

Under low concurrency, sync and async should perform similarly, since
there's no contention for threads. As concurrent users increase, the sync
version is expected to degrade faster (rising p95/p99, dropping RPS) once
the number of concurrent requests approaches the size of the WSGI thread
pool, while the async version should continue to scale until CPU or other
resources become the bottleneck. The Celery-offload version is expected to
show the lowest and flattest latency of the three, since the request
thread/coroutine never waits on the I/O at all — at the cost of the work
no longer being complete by the time the response is returned.

## Scenarios

All three scenarios perform the *same* simulated I/O-bound operation: an
HTTP call to `https://httpbin.org/delay/{n}` (a fixed, configurable delay),
representing a slow external API/notification call.

- **Scenario A — Sync (WSGI):** A standard Django `def` view makes the
  delayed HTTP call directly and blocks until it returns, then responds.
- **Scenario B — Async (ASGI):** An `async def` view awaits the same
  delayed HTTP call via `httpx.AsyncClient` without blocking the thread,
  then responds.
- **Scenario C — Offloaded (Celery):** A standard Django view enqueues a
  Celery task (`benchmarks.process_order_notification`) that performs the
  delayed HTTP call out-of-band, and responds immediately without waiting.

## Dataset

No database records are required for this benchmark — the variable under
test is I/O wait time, not data volume. A fixed artificial delay of
**1 second per request** is used across all three scenarios (via the
`httpbin.org/delay/1` endpoint).

## Conditions Held Constant

- Same Django project, same deployment (containers, CPU/memory limits).
- Same simulated external delay (1s) across all three scenarios.
- Same k6 load-test script and configuration, varied only by target
  endpoint and concurrency level.
- Same Postgres/Redis services running, even though this particular
  benchmark doesn't query them, to keep environment conditions identical
  to other benchmarks in this repo.
- Only the execution model changes between scenarios: sync vs async vs
  offloaded.

## Load Levels

Each scenario is tested at the same set of concurrency levels:

```
10 concurrent users
50 concurrent users
100 concurrent users
500 concurrent users
```

## Metrics

- p50, p90, p95, p99 latency
- RPS (requests per second)
- Error rate
- For Scenario C only: task queue lag (time between enqueue and task
  execution start), to confirm the Celery worker pool isn't itself
  becoming a bottleneck at high concurrency.

## What This Benchmark Does NOT Cover

- CPU-bound workloads (a separate benchmark would be needed to test the
  claim that async provides no benefit for CPU-bound work).
- Database-bound I/O (covered separately under the database benchmarks).
- Correctness/eventual-consistency trade-offs of offloading work to
  Celery (e.g. the caller not knowing the result immediately) — this
  benchmark only measures latency/throughput, not architectural
  trade-offs.

## Result

See the corresponding result in
[Async Results](../../results/Async.md#bench-010-async-vs-sync).