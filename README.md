# API Latency Lab

**API Latency Lab** is an R&D project focused on understanding, measuring, and improving API performance through controlled and reproducible experiments.

The main goal is to investigate how different factors affect API latency, such as:

* Database performance
* Dataset size
* Response size
* Pagination
* Serialization
* Caching
* Redis
* Synchronous vs asynchronous execution
* External API calls
* Database connection pooling
* Django vs FastAPI
* Concurrent users and system load

The project follows a simple principle:

> **Research → Implement → Benchmark → Measure → Analyze → Document**

We do not assume that an optimization is better. We measure its actual impact under a defined workload.

---

# Current Status

* The Django API (`api/django/`) is implemented and fully dockerized (`docker-compose.yaml`), running behind Postgres.
* Redis and Celery containers are already provisioned in `docker-compose.yaml`, but **they are not yet wired into the application**. No endpoint currently uses Redis for caching, and no task currently runs through Celery. They exist as infrastructure only, waiting for the Caching and Async benchmarks (see milestones) to activate and measure them.
* FastAPI (`api/fastapi/`) has not been implemented yet; it is planned for the Framework benchmark.

---

# Project Structure

```text
api-latency-lab/
│
├── README.md
│
├── docs/
│   ├── latency.md
│   ├── benchmarking.md
│   ├── database.md
│   ├── caching.md
│   └── async.md
│
├── api/
│   ├── django/
│   │   └── ...
│   │
│   └── fastapi/
│       └── ...
│
├── benchmarks/
│   ├── async/
│   │   └── Async-vs-Sync.md
│   │
│   ├── baseline/
│   │   ├── Dataset-Size.md
│   │   └── Endpoint-Latency.md
│   │
│   ├── caching/
│   │   └── Redis-vs-NoRedis.md
│   │
│   ├── database/
│   │   ├── Connection-poling.md
│   │   ├── Indexes.md
│   │   ├── N-plus-one.md
│   │   └── Query-optimization.md
│   │
│   └── framework/
│       └── FastAPI-vs-Django.md
│
├── load-tests/
│   ├── k6/
│   └── locust/
│
├── results/
│   ├── Async.md
│   ├── Baseline.md
│   ├── Cache.md
│   ├── Database.md
│   ├── Framework.md
│   └── Response-size.md
│
└── docker-compose.yml
```

---

# Directory Responsibilities

## `docs/`

Contains the **theoretical research** behind the project.

For example:

```text
docs/latency.md
```

should explain concepts such as:

* What is API latency?
* What is response time?
* What are p50, p90, p95, and p99?
* What is RPS?
* What is throughput?

The `docs/` directory answers:

> **What do we need to know before performing an experiment?**

---

## `api/`

Contains the actual API implementations used for experiments.

Initially, the project uses:

```text
api/django/
```

with Django and PostgreSQL.

The API should provide controlled endpoints that can be used consistently across different experiments.

For example:

```http
GET /api/products/
GET /api/products/{id}/
```

The API should initially remain simple so that we can establish a reliable baseline.

---

## `benchmarks/`

Contains the **definition of experiments**.

A benchmark describes:

* What question are we trying to answer?
* What scenario are we testing?
* What data are we using?
* What conditions should remain constant?
* What metrics should be measured?
* What are we comparing?

The `benchmarks/` directory answers:

> **What are we going to test?**

A benchmark should **not contain the final measured results**.

---

## `load-tests/`

Contains the tools and scripts used to **generate requests against the API**.

For example:

```text
load-tests/k6/
```

may contain k6 scripts that send:

```text
10 concurrent users
50 concurrent users
100 concurrent users
500 concurrent users
```

to an API endpoint.

The important distinction is:

```text
benchmarks/
    Defines WHAT we want to test.

load-tests/
    Defines HOW we generate traffic for the test.

results/
    Contains WHAT we observed.
```

A load-testing tool such as k6 is therefore an **instrument for running a benchmark**, not the benchmark itself.

---

## `results/`

Contains the actual results and analysis of completed benchmarks.

The `results/` directory answers:

> **What did we discover?**

Each result should contain:

* Benchmark reference
* Test environment
* Dataset
* Test configuration
* Metrics
* Raw/observed measurements
* Comparison
* Analysis
* Conclusion

---

# Benchmark Workflow

Every experiment should follow this workflow:

```text
                 ┌──────────────┐
                 │   Research   │
                 │    docs/     │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │   Define     │
                 │  Benchmark   │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │ Implement /  │
                 │ Prepare API  │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │  Load Test   │
                 │   k6/Locust  │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │   Measure    │
                 │ p50/p95/p99  │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │   Analyze    │
                 │   Results    │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │  Document    │
                 │   results/   │
                 └──────────────┘
```

---

# Example: Testing Pagination

Suppose we want to answer:

> **Does pagination reduce API latency when returning 1,000 products?**

## Step 1 — Define the Benchmark

Go to:

```text
benchmarks/response-size/Pagination.md
```

The benchmark defines the experiment.

For example:

```text
Dataset:
1,000 products

Scenario A:
Return all 1,000 products

Scenario B:
Return 20 products per page

Metrics:
p50
p95
p99
RPS
```

At this point, we have **not recorded any results**.

We have only defined what we want to test.

---

# Step 2 — Prepare the API

The API is located in:

```text
api/django/
```

For this experiment, the endpoint might be:

```http
GET /api/products/
```

The database contains:

```text
1,000 products
```

The API should be configured so that the two scenarios can be tested under comparable conditions.

---

# Step 3 — Create the Load Test

Now we need to generate traffic.

We use:

```text
load-tests/k6/
```

For example:

```text
load-tests/k6/products.js
```

The script can send requests to:

```http
GET /api/products/
```

with a defined workload such as:

```text
10 concurrent users
1,000 requests
```

The important point is that the load test should remain consistent between Scenario A and Scenario B.

---

# Step 4 — Run the Benchmark

We first test:

```text
Scenario A
Without Pagination
```

Then:

```text
Scenario B
With Pagination
```

The same major conditions should be maintained:

```text
Same API
Same database
Same dataset
Same machine
Same number of requests
Same concurrency
Same load-test configuration
```

Only the variable being investigated should change whenever possible.

---

# Step 5 — Collect the Metrics

The load-testing tool provides measurements such as:

```text
Average latency
p50
p90
p95
p99
RPS
Error rate
```

For example:

```text
Without Pagination

p50 = 180ms
p95 = 250ms
p99 = 400ms
RPS = 45
```

and:

```text
With Pagination

p50 = 35ms
p95 = 60ms
p99 = 90ms
RPS = 180
```

These numbers are the actual experimental results.

---

# Step 6 — Document the Result

The results for response-size experiments are stored in:

```text
results/Response-size.md
```

Create a section for the benchmark:

```md
## Pagination

### Benchmark

[Pagination Benchmark](../benchmarks/response-size/Pagination.md)

### Results

| Scenario | p50 | p95 | p99 | RPS |
|---|---:|---:|---:|---:|
| Without Pagination | 180ms | 250ms | 400ms | 45 |
| With Pagination | 35ms | 60ms | 90ms | 180 |

### Conclusion

Pagination significantly reduced response latency
under this workload.
```

This creates a direct connection:

```text
benchmarks/response-size/Pagination.md
                  │
                  │ defines
                  ↓
             Experiment
                  │
                  │ executed by
                  ↓
          load-tests/k6/
                  │
                  │ produces
                  ↓
        results/Response-size.md
```

---

# How to Find the Result of a Benchmark

Every benchmark file should contain a **Result** section at the bottom.

For example:

```md
## Result

See the corresponding result in
[Response-size Results](../../results/Response-size.md#pagination).
```

The result file should also link back to the benchmark:

```md
## Pagination

**Benchmark:** [Pagination](../benchmarks/response-size/Pagination.md)
```

Therefore, navigation works in both directions:

```text
Benchmark
    ↓
Result

Result
    ↓
Benchmark
```

---

# Do Not Use Line Numbers for Results

Do not document results like:

```text
results/Response-size.md — line 42
```

Line numbers can change whenever someone edits the file.

Instead, use Markdown headings and GitHub's generated anchors:

```md
## Pagination
```

Then link directly to that section:

```text
results/Response-size.md#pagination
```

This remains much more stable.

---

# Benchmark IDs

For larger experiments, each benchmark should have a unique ID.

For example:

```text
BENCH-001 — Endpoint Latency
BENCH-002 — Dataset Size
BENCH-003 — Pagination
BENCH-004 — Serialization
```

The corresponding result can reference the benchmark:

```text
RES-003 — BENCH-003: Pagination
```

Example:

```md
## RES-003 — BENCH-003: Pagination
```

This makes it immediately clear which result belongs to which benchmark.

---

# What Goes Where?

| Question                     | Location          |
| ---------------------------- | ----------------- |
| What is API latency?         | `docs/`           |
| What is p95?                 | `docs/latency.md` |
| What are we testing?         | `benchmarks/`     |
| What API are we testing?     | `api/`            |
| How do we generate requests? | `load-tests/`     |
| What were the measurements?  | `results/`        |
| What did we learn?           | `results/`        |

The core relationship is:

```text
docs/
  ↓
Understand the concept

benchmarks/
  ↓
Define the experiment

api/
  ↓
Provide the system under test

load-tests/
  ↓
Generate controlled traffic

results/
  ↓
Record and analyze the findings
```

---

# Experimental Rules

To keep results meaningful and reproducible:

1. Establish a baseline before optimization.
2. Change one major variable at a time whenever possible.
3. Keep the test environment consistent.
4. Record dataset size.
5. Record concurrency.
6. Record the number of requests.
7. Record p50, p90, p95, and p99.
8. Record RPS and error rate where applicable.
9. Repeat important experiments.
10. Document unexpected results.
11. Never claim an optimization is better without measurement.
12. Always link a benchmark to its corresponding result.

---

# Initial Project Flow

The project will be developed in the following order:

```text
1. Project Setup
        ↓
2. Django + PostgreSQL
        ↓
3. Research docs
        ↓
4. Build the baseline API
        ↓
5. Seed benchmark data
        ↓
6. Run baseline benchmarks
        ↓
7. Run individual experiments
        ↓
8. Collect measurements
        ↓
9. Document results
        ↓
10. Analyze and compare findings
```

Redis, Celery, and other components may exist in the infrastructure from the beginning, but they should only be introduced into an experiment when that experiment specifically requires them.

---

# Final Goal

The final goal of this repository is to build a collection of **reproducible performance experiments** and use measured data to understand how different techniques affect API performance.

The project should answer questions with evidence rather than assumptions.

Instead of:

> "Redis is faster."

We want conclusions such as:

> "Under a workload of 100 concurrent users and 1,000 products, Redis reduced p95 latency from X ms to Y ms."

This approach makes the repository useful as both an R&D project and a practical reference for future backend engineering decisions.
