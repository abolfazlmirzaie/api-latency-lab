# Database Connection Pooling Benchmark

## Objective

The purpose of this benchmark is to measure the performance impact of **database connection pooling** on the Django API when communicating with PostgreSQL.

The test compares two configurations:

1. **Without Connection Pooling**
2. **With Connection Pooling**

The goal is to determine whether reusing existing database connections can reduce API latency and improve throughput under concurrent load.

---

## Test Scenario

The API returns a list of products together with their related categories.

Endpoint:

```text
GET /products/?with_category=true
```

The endpoint will be tested under load using Locust.

---

## Test Variables

### Test A — Without Connection Pooling

Django connects to PostgreSQL without an explicitly configured connection pool.

```text
Locust
   ↓
Django
   ↓
PostgreSQL
```

This configuration serves as the baseline.

### Test B — With Connection Pooling

Django uses a database connection pool when communicating with PostgreSQL.

```text
Locust
   ↓
Django
   ↓
Connection Pool
   ↓
PostgreSQL
```

---

## Metrics

For both configurations, the following metrics will be collected:

* Average response time
* Median response time
* P95 latency
* P99 latency
* Minimum response time
* Maximum response time
* Requests per second (RPS)
* Failure rate
* Total number of requests

---

## Controlled Conditions

To make the comparison meaningful, both tests should use the same:

* API endpoint
* Dataset
* Database
* Serializer
* Query optimization configuration
* Number of Locust users
* Spawn rate
* Test duration
* Hardware and Docker environment

The only intended difference between the two tests is whether **database connection pooling is enabled**.

---

## Expected Outcome

The benchmark is designed to determine whether connection pooling provides measurable improvements in API performance, particularly under concurrent load.

The results of both tests will be recorded separately and compared to determine the impact of database connection pooling.
