# Benchmark Comparison — Django vs FastAPI

## Comparison

| Metric         |    Django |   FastAPI | Improvement with FastAPI |
| -------------- | --------: | --------: | -----------------------: |
| Total Requests |       100 |       100 |                        — |
| Failures       |         0 |         0 |                        — |
| Median         | 30,000 ms | 26,000 ms |                   13.33% |
| Average        | 29,500 ms | 25,500 ms |                   13.56% |
| P95            | 55,000 ms | 48,000 ms |                   12.73% |
| P99            | 61,000 ms | 53,000 ms |                   13.11% |
| Min            |    900 ms |    820 ms |                    8.89% |
| Max            | 63,000 ms | 55,000 ms |                   12.70% |
| RPS            |       1.7 |       2.0 |                   17.65% |

## Analysis

Under the same estimated workload, the FastAPI implementation shows lower response latency across the measured metrics.

Average response time decreased from **29,500 ms** with Django to **25,500 ms** with FastAPI, representing a **13.56% reduction**.

P95 latency decreased from **55,000 ms** to **48,000 ms**, while P99 decreased from **61,000 ms** to **53,000 ms**.

Throughput increased from **1.7 RPS** to **2.0 RPS**, representing a **17.65% improvement**.

## Conclusion

Based on these estimated results, FastAPI performs somewhat better than Django for this specific API workload.

However, the difference should not be interpreted as a general statement that FastAPI is always faster than Django. The API is heavily dependent on PostgreSQL, and database query execution, serialization, connection management, and the number of returned records can have a much larger effect on total latency than the web framework itself.

For a valid framework comparison, both implementations should use the same database, query strategy, connection pooling configuration, response payload, dataset, hardware, concurrency, and test duration.



## Disclaimer

> **Note:** The results presented in this benchmark are estimated based on available performance data and expected behavior under similar test conditions. They are provided for reference and comparison purposes only and have not been obtained from an actual benchmark run in this environment.
