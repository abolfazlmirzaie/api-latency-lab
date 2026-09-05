# Latency

## What is Latency?

Latency is the time it takes for a system to respond to a request — measured
from the moment a client sends a request until it receives the first byte
(or the full response) back. In the context of this lab, latency is the
primary metric we use to evaluate the effect of different optimization
techniques (caching, async I/O, background task offloading) on a Django API.

Latency is not a single number. A single average can hide serious problems,
so this project reports latency using **percentiles**:

- **p50 (median):** half of all requests are faster than this. Represents
  the "typical" experience.
- **p95:** 95% of requests are faster than this. Represents the experience
  of most users, including some slower ones.
- **p99:** 99% of requests are faster than this. Captures tail latency —
  the worst-case experience for a small but significant fraction of users.

## Why Percentiles Matter More Than Averages

An average can look fine even when a meaningful number of users are having
a bad experience. For example, an endpoint could have an average of 120ms
while its p99 is 900ms — meaning 1% of users wait nearly a full second.
Averages smooth this out; percentiles expose it. Because latency
distributions are rarely symmetric (a few very slow requests pull the tail
out much further than they pull the average), percentiles are the standard
way of reporting API performance.

## Sources of Latency in a Django API

Latency in a typical Django request can come from several places:

1. **Database queries** — slow or unindexed queries, N+1 query problems,
   or queries that don't use `select_related` / `prefetch_related`.
2. **Serialization** — converting querysets into JSON, especially for
   large or deeply nested responses.
3. **Synchronous blocking I/O** — waiting on external services, database
   connections, or file systems while holding up the request thread.
4. **Application logic** — expensive computation performed inline during
   the request/response cycle instead of offloaded elsewhere.
5. **Network and infrastructure** — load balancers, DNS resolution,
   TLS handshakes — generally out of scope for this lab, since the goal
   is to compare *application-level* optimizations under fixed
   infrastructure conditions.

## Why This Matters for This Project

The core hypothesis of this lab is that specific, measurable techniques —
caching with Redis, async request handling, and background task
offloading with Celery — can reduce latency (especially at the p95/p99
tail) under load. To validate or reject that hypothesis, every benchmark
in this repository:

- Defines a single independent variable (e.g., cache on/off).
- Keeps all other conditions fixed (same machine, same dataset, same
  concurrency).
- Measures p50/p95/p99 and error rate using k6.
- Documents raw results in `results/` and links them back to the
  benchmark definition that produced them.

## Related

- See `benchmarks/` for the specific benchmark definitions (e.g., BENCH-009,
  BENCH-010) that apply these concepts.
- See `results/` for the measured outcomes.
