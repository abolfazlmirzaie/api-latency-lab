# Async

## What is Async I/O?

Synchronous code executes one operation at a time: when a request handler
calls the database, makes an HTTP request, or reads a file, the entire
thread blocks — doing nothing — until that operation completes. Asynchronous
(async) I/O lets a single thread hold many in-flight operations at once:
while one request is waiting on the database, the thread can start working
on another request instead of sitting idle.

Async doesn't make any individual operation faster. What it improves is
**throughput under concurrency** — how many simultaneous requests a server
can handle before latency and error rates start to climb — because the
server stops wasting time blocked on I/O.

## Sync vs Async in Django

Django has supported async views since Django 3.1, and the async story
matured significantly with ASGI support:

- **WSGI (traditional):** one thread per request. If a view blocks on I/O,
  that thread is unavailable for anything else until the response is
  returned.
- **ASGI (async):** a single event loop can juggle many concurrent
  requests. A view defined with `async def` can `await` I/O-bound work
  (database calls via async ORM methods, external API calls via
  `httpx.AsyncClient`, etc.) without blocking the whole process.

```python
# Synchronous view
def get_products(request):
    products = Product.objects.all()  # blocks the thread
    return JsonResponse(list(products.values()), safe=False)

# Asynchronous view
async def get_products(request):
    products = [p async for p in Product.objects.all()]  # non-blocking
    return JsonResponse(products, safe=False)
```

## When Async Helps — and When It Doesn't

Async provides the most benefit when:

- The workload is **I/O-bound** (waiting on network calls, database
  queries, external APIs) rather than CPU-bound.
- **Concurrency is high** — many simultaneous requests competing for
  the same limited resources.
- Requests spend a meaningful fraction of their time waiting, not
  computing.

Async provides little or no benefit — and can even add overhead — when:

- The workload is **CPU-bound** (heavy computation), since async doesn't
  parallelize CPU work; it only avoids blocking on I/O waits.
- Traffic is low and concurrency is minimal, since the server is never
  contending for threads in the first place.
- The database driver or third-party library in use isn't async-native,
  which can force blocking calls inside an async view anyway.

## Why This Matters for This Project

This lab tests the hypothesis that converting specific endpoints from sync
to async reduces latency (particularly p95/p99) and increases sustainable
throughput under concurrent load — without changing what the endpoint
actually does. As with all benchmarks in this repository, the comparison
isolates a single variable:

- Same endpoint, same dataset, same infrastructure.
- Only the execution model changes: sync (WSGI) vs async (ASGI).
- k6 load tests measure p50/p95/p99 latency and error rate under matched
  concurrent user counts for both versions.

## Related

- See `benchmarks/BENCH-010.md` for the specific async vs sync benchmark
  definition.
- See `results/` for the measured outcomes.
