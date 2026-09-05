# Async

## BENCH-010 — Async vs Sync

### Benchmark

[BENCH-010 — Async vs Sync](../benchmarks/async/Async-vs-Sync.md)

### Test Environment

- Django 5.2.15, Python 3.13
- Sync (WSGI): Gunicorn, `core.wsgi:application`, 4 workers
- Async (ASGI): Gunicorn + `uvicorn.workers.UvicornWorker`, `core.asgi:application`, 4 workers, served on a separate port/service from the WSGI service
- Offloaded: same WSGI service as Sync, work enqueued to a Celery worker (Redis broker)
- All services run via Docker Compose on the same machine
- Load generated with Locust (single master, one worker process)

### Dataset

No database records used. Simulated I/O wait implemented locally
(`time.sleep` for sync, `asyncio.sleep` for async) rather than a real
external HTTP call, to remove network dependency and keep the delay
constant. Fixed delay: **1 second** per request across all three
scenarios.

### Test Configuration

- Concurrency levels: 10, 50, 100, 500 simulated users
- No wait time between requests (sustained load)
- Each scenario run in isolation (not mixed in the same Locust run)

### Metrics

| Concurrency | Scenario  | Median (ms) | p95 (ms) | p99 (ms) | Average (ms) | RPS    |
|---:|---|---:|---:|---:|---:|---:|
| 10  | Sync       | 2100  | 3000  | 3000  | 2434.80  | 4      |
| 10  | Async      | 1008  | 1000  | 1100  | 1022.88  | 10     |
| 10  | Offloaded  | 24    | 30    | 38    | 22.76    | 379.6  |
| 50  | Sync       | 8000  | 13000 | 13000 | 7777.60  | 4      |
| 50  | Async      | 1005  | 1100  | 1100  | 1046.02  | 64     |
| 50  | Offloaded  | 53    | 130   | 180   | 58.93    | 407.88 |
| 100 | Sync       | 10000 | 17000 | 18000 | 10074.41 | 4      |
| 100 | Async      | 1005  | 1100  | 1200  | 1044.08  | 92.2   |
| 100 | Offloaded  | 88    | 200   | 260   | 91.55    | 467.14 |
| 500 | Sync       | 23000 | 29000 | 29000 | 23224.61 | 4      |
| 500 | Async      | 1100  | 1400  | 1600  | 1183.40  | 362.3  |
| 500 | Offloaded  | 910   | 1000  | 1100  | 717.08   | 461.9  |

### Comparison

- **Sync** RPS stayed flat at ~4 across every concurrency level tested
  (10 → 500), while p95/p99 grew roughly linearly with concurrency,
  reaching ~29s at 500 users. This matches a fixed pool of 4 WSGI
  workers: only 4 requests can be in flight at once, so additional
  concurrent users simply queue.
- **Async** latency stayed close to the fixed 1s simulated delay across
  all tested concurrency levels (median 1005–1100ms from 10 to 500
  users), while RPS scaled from 10 to 362. Some growth in p95/p99 is
  visible at 500 users (up to 1600ms), suggesting the event loop is
  starting to feel pressure at that level, but nowhere near the
  degradation seen under Sync.
- **Offloaded** was the fastest option at low-to-moderate concurrency
  (24–88ms median through 100 users), since the request only waits on
  enqueueing, not on the actual I/O-bound work. At 500 users, median
  jumped sharply to 910ms — the Celery worker/queue itself became the
  new bottleneck at that load level.

### Analysis

The results align with the hypothesis in BENCH-010: async scales far
better than sync under concurrent I/O-bound load because it doesn't
block a thread waiting on I/O, while sync is hard-capped by its worker
pool size. Offloading to Celery avoids blocking the request entirely,
giving the best low-concurrency latency, but shifts the bottleneck
downstream to the worker/queue rather than eliminating it — at high
enough concurrency (500 users here), that downstream bottleneck becomes
visible.

An earlier version of this benchmark used real HTTP calls to
`httpbin.org` to simulate the I/O delay, which introduced network
flakiness and inflated/unstable latency unrelated to the execution
model being tested. Switching to a local `time.sleep` / `asyncio.sleep`
delay removed that noise and is reflected in the numbers above.

### Conclusion

Under a workload of up to 500 concurrent users with a 1-second
I/O-bound operation, converting a Django endpoint from sync (WSGI) to
async (ASGI) reduced p95 latency from ~29s to ~1.4s and increased
sustainable throughput roughly 90x (4 RPS → 362 RPS). Offloading the
same work to Celery produced the lowest latency at low-to-moderate
concurrency, but is bounded by the capacity of the Celery worker pool
rather than by the web server's execution model.