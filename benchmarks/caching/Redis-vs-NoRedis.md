# BENCH-009 — Redis Cache vs No Cache

## Question

Does enabling Redis caching on a read-heavy Django API endpoint reduce
response latency (p50/p95/p99) and increase sustainable throughput under
concurrent load, compared to the same endpoint with no caching?

## Independent Variable

- Scenario A (baseline): Endpoint served directly from the database
  on every request. No caching layer.
- Scenario B: Same endpoint, same data, with django-redis caching
  enabled (cache-aside pattern, TTL = 5 minutes).

Only this variable changes between the two scenarios.

## Fixed Conditions

| Condition | Value |
|---|---|
| API endpoint | GET /api/products/ |
| Database | PostgreSQL (same instance, same dataset) |
| Dataset | Same fixed dataset, no writes during test |
| Machine | Same host, no other load running |
| Concurrency (k6) | 50 virtual users |
| Duration | 60 seconds per scenario |
| Test tool | k6 |

## Hypothesis

Scenario B (Redis enabled) will show materially lower p95/p99 latency and
higher achievable throughput than Scenario A, since repeated identical
reads will be served from memory instead of re-querying and
re-serializing from PostgreSQL on every request.

## Metrics Collected

- Average latency
- p50, p90, p95
- Requests per second (RPS)
- Error rate

## Result

See the corresponding result in [BENCH-009 Results](../results/BENCH-009-results.md).

## Related

- Benchmark: BENCH-009 (this file)
- Load test: load-tests/bench-009-redis-cache.js
- Result: results/BENCH-009-results.md
- Concept background: docs/Latency.md