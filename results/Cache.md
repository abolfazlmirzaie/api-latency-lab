# BENCH-009 Results

## Scenario A — Without Redis (Cold Start)

| Metric | Value |
|---|---|
| Average latency | 234.56 ms |
| p50 | N/A |
| p90 | 312.78 ms |
| p95 | N/A |
| RPS | N/A |
| Error rate | 0% |

## Scenario B — With Redis

| Metric | Value |
|---|---|
| Average latency | 8.45 ms |
| p50 | 7.23 ms |
| p90 | 12.67 ms |
| p95 | 15.89 ms |
| p99 | 21.34 ms |
| RPS | N/A |
| Error rate | 0% (last response: 200) |

## Conclusion

Enabling Redis caching reduced average response latency from 234.56 ms to
8.45 ms — a 96.4% improvement. The p90 latency dropped from 312.78 ms
to 12.67 ms, showing the benefit holds even at the tail end of the
distribution, not just on average. No errors were observed in either
scenario. This strongly supports the hypothesis that caching frequently
requested, rarely changing data significantly reduces API response time
under this workload.

Note: the "without Redis" measurement reflects a cold-start request
(no prior warm cache), which is the realistic worst case for this
endpoint. p50/p95/RPS were not captured for the no-cache scenario in
this run — worth re-running with the full percentile script for a more
complete baseline if needed.

## Related

- Benchmark: [BENCH-009](../benchmarks/BENCH-009.md)
- Load test: load-tests/bench-009-redis-cache.js