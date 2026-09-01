# Benchmark — Query Optimization with `prefetch_related`

## Objective

The purpose of this benchmark is to measure the performance impact of Django ORM query optimization using `prefetch_related()` when returning a list of products along with their related categories.

The benchmark compares two implementations:

1. **Without Query Optimization**
2. **With `prefetch_related()`**

---

## Test Scenario

The API returns a list of products and their related categories.

### Without Optimization

The queryset is:

```python
Product.objects.all()
```

No `prefetch_related()` is used.

### With Optimization

The queryset is:

```python
Product.objects.all().prefetch_related("categories")
```

Django preloads the related categories to avoid unnecessary database queries while serializing the products.

---

## Endpoint

### Without Optimization

```http
GET /products/
```

### With Optimization

```http
GET /products/?optimize=true
```

---

## Locust Configuration

| Configuration     |              Value |
| ----------------- | -----------------: |
| Load Testing Tool |             Locust |
| Users             |                 50 |
| Spawn Rate        |        5 users/sec |
| Test Duration     |         60 seconds |
| Dataset           |      1000 Products |
| Related Data      | Product Categories |

Both tests must use the same load configuration to ensure a fair comparison.

---

# Test 1 — Without `prefetch_related`

### Locust File

```text
loadtest/locust_without_prefetch.py
```

### Request

```http
GET /products/
```

### Results

| Metric          | Result |
| --------------- | -----: |
| Total Requests  |    TBD |
| Failed Requests |    TBD |
| Median          |    TBD |
| Average         |    TBD |
| P95             |    TBD |
| P99             |    TBD |
| Minimum         |    TBD |
| Maximum         |    TBD |
| RPS             |    TBD |

---

# Test 2 — With `prefetch_related`

### Locust File

```text
loadtest/locust_with_prefetch.py
```

### Request

```http
GET /products/?optimize=true
```

### Results

| Metric          | Result |
| --------------- | -----: |
| Total Requests  |    TBD |
| Failed Requests |    TBD |
| Median          |    TBD |
| Average         |    TBD |
| P95             |    TBD |
| P99             |    TBD |
| Minimum         |    TBD |
| Maximum         |    TBD |
| RPS             |    TBD |

---

# Query Behavior

## Without `prefetch_related`

When related categories are accessed during serialization, Django may execute additional queries for each product.

Conceptually:

```text
1 query → Fetch products

N queries → Fetch categories for each product
```

This can result in an **N+1 query problem**.

For example, with 100 products:

```text
1 + 100 = 101 queries
```

---

## With `prefetch_related`

Using:

```python
Product.objects.all().prefetch_related("categories")
```

Django fetches the products and their related categories in a small number of queries and associates the related objects in memory.

Conceptually:

```text
1 query → Fetch products

1 additional query → Fetch related categories
```

Instead of performing one category query per product.

---

# Comparison

| Metric   | Without Prefetch | With Prefetch | Improvement |
| -------- | ---------------: | ------------: | ----------: |
| Requests |              TBD |           TBD |         TBD |
| Failures |              TBD |           TBD |         TBD |
| Median   |              TBD |           TBD |         TBD |
| Average  |              TBD |           TBD |         TBD |
| P95      |              TBD |           TBD |         TBD |
| P99      |              TBD |           TBD |         TBD |
| RPS      |              TBD |           TBD |         TBD |

---

# Expected Result

The optimized implementation is expected to reduce the number of database queries required to serialize the product list.

As the number of products increases, the performance difference between the two implementations should become more significant.

The main goal of this benchmark is to demonstrate how `prefetch_related()` can reduce unnecessary database queries and improve API latency when working with related objects.

---

# Conclusion

This benchmark evaluates the effect of Django ORM query optimization using `prefetch_related()`.

The final conclusion should be based on the Locust results and should compare:

* Average response time
* P95 latency
* P99 latency
* Requests per second
* Number of failed requests

The benchmark results will be updated after running both test scenarios under identical load conditions.
