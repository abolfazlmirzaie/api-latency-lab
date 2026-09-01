# Benchmark Result — Without Index

## Test Configuration

* **Endpoint:** `GET /product/search/?search=iphone+15+1`
* **Database:** PostgreSQL
* **Records:** 1000 Products
* **Index on `title`:** Disabled
* **Load Testing Tool:** Locust
* **Requests:** 2492
* **Request Failures:** 0
* **Current RPS:** 49.9

## Results

| Metric                |   Result |
| --------------------- | -------: |
| Total Requests        |     2492 |
| Failed Requests       |        0 |
| Median Response Time  |    27 ms |
| Average Response Time | 36.39 ms |
| P95 Response Time     |    94 ms |
| P99 Response Time     |   140 ms |
| Minimum Response Time |    13 ms |
| Maximum Response Time |   331 ms |
| Requests Per Second   |     49.9 |

## Analysis

In this test, the `title` field did not have a database index.

The API successfully processed **2492 requests with zero failures**. The average response time was **36.39 ms**, while the median response time was **27 ms**.

The **95th percentile (P95)** was **94 ms**, meaning that 95% of the requests were completed in 94 ms or less. The **99th percentile (P99)** was **140 ms**.

The maximum response time reached **331 ms**, indicating that a small number of requests took significantly longer than the typical requests.

This result is used as the **baseline** for comparison with the same API after adding an index to the `title` field.

## Baseline

```text
WITHOUT INDEX

Requests: 2492
Failures: 0
Average: 36.39 ms
Median: 27 ms
P95: 94 ms
P99: 140 ms
Min: 13 ms
Max: 331 ms
RPS: 49.9
```

The next benchmark will run the **exact same test with an index on `Product.title`**. The two results will then be compared to evaluate the effect of database indexing on API latency.




# Benchmark Result — With Index

## Test Configuration

* **Endpoint:** `GET /product/search/?search=iphone+15+1`
* **Database:** PostgreSQL
* **Records:** 1000 Products
* **Index:** B-tree index on `Product.title`
* **Index Name:** `products_product_title_idx`
* **Load Testing Tool:** Locust
* **Requests:** 2636
* **Request Failures:** 0
* **Current RPS:** 49.5

## Results

| Metric                |   Result |
| --------------------- | -------: |
| Total Requests        |     2636 |
| Failed Requests       |        0 |
| Median Response Time  |    25 ms |
| Average Response Time | 32.67 ms |
| P95 Response Time     |    86 ms |
| P99 Response Time     |   140 ms |
| Minimum Response Time |    13 ms |
| Maximum Response Time |   576 ms |
| Requests Per Second   |     49.5 |

## Query Plan

PostgreSQL confirmed that the index was used for the search query:

```text
Index Scan using products_product_title_idx on products_product
```

The database query was:

```sql
SELECT *
FROM products_product
WHERE title = 'iPhone 15 1';
```

The measured PostgreSQL execution time was:

```text
Execution Time: 0.058 ms
```

## Analysis

With the B-tree index enabled on the `title` field, PostgreSQL used an `Index Scan` instead of scanning the entire table.

The API successfully processed **2636 requests with zero failures**. The average response time was **32.67 ms**, compared with **36.39 ms** in the baseline test without the index.

The median response time decreased from **27 ms to 25 ms**, while P95 decreased from **94 ms to 86 ms**.

P99 remained unchanged at **140 ms**. The maximum response time increased to **576 ms**, which indicates that occasional high-latency requests were still present and were not eliminated by the database index.

Because the dataset contains only **1000 products**, the performance difference is relatively small. The index nevertheless demonstrates a measurable improvement in typical API latency.

## Benchmark Summary

```text
WITH INDEX

Index: products_product_title_idx
Requests: 2636
Failures: 0
Average: 32.67 ms
Median: 25 ms
P95: 86 ms
P99: 140 ms
Min: 13 ms
Max: 576 ms
RPS: 49.5
```

This result can be compared with the **Without Index** baseline to evaluate the impact of database indexing on API latency.




















# Benchmark Result — Without `prefetch_related`

## Test Configuration

* **Endpoint:** `GET /products/?with_category=true`
* **Database:** PostgreSQL
* **Dataset:** 1000 Products
* **Related Data:** Product Categories
* **Optimization:** Disabled
* **ORM Queryset:** `Product.objects.all()`
* **Load Testing Tool:** Locust
* **Failures:** 0

## Results

| Metric                |        Result |
| --------------------- | ------------: |
| Total Requests        |           102 |
| Failed Requests       |             0 |
| Median Response Time  |     34,000 ms |
| Average Response Time |  33,863.31 ms |
| P95 Response Time     |     63,000 ms |
| P99 Response Time     |     65,000 ms |
| Minimum Response Time |      1,059 ms |
| Maximum Response Time |     65,968 ms |
| Average Response Size | 146,935 bytes |
| Requests Per Second   |           1.4 |
| Failures Per Second   |             0 |

## Query Configuration

For this test, the API does not use `prefetch_related()`.

The queryset is:

```python
Product.objects.all()
```

However, the serializer also accesses the related `categories` field:

```text
Product
 └── categories
```

Because the related categories are not prefetched, accessing the relationship during serialization can result in an **N+1 Query problem**.

Conceptually:

```text
1 Query
    ↓
Fetch all products

N Queries
    ↓
Fetch categories for each product
```

For a dataset containing 1000 products, this can potentially result in a very large number of database queries.

## Performance Analysis

The API showed extremely high response times under load.

The average response time was:

```text
33,863.31 ms
```

while the median was:

```text
34,000 ms
```

The P95 latency reached:

```text
63,000 ms
```

and the maximum observed latency was:

```text
65,968 ms
```

Despite the high latency, all **102 requests completed successfully** with zero failures.

The low throughput of approximately **1.4 requests/second** also indicates that the API was heavily constrained while processing the product list.

The most likely cause is the large number of database queries generated when accessing the `categories` relationship during serialization without using `prefetch_related()`.

This hypothesis should be verified by measuring the actual number of SQL queries generated by the endpoint.

## Baseline

This benchmark serves as the **baseline** for comparison with the optimized implementation.

The next benchmark will enable:

```python
Product.objects.all().prefetch_related("categories")
```

and compare the resulting latency and throughput against this baseline.

## Summary

```text
WITHOUT PREFETCH

Endpoint:
GET /products/?with_category=true

Requests:       102
Failures:       0
Average:        33,863.31 ms
Median:         34,000 ms
P95:             63,000 ms
P99:             65,000 ms
Min:             1,059 ms
Max:            65,968 ms
RPS:             1.4
```

This result demonstrates the baseline performance of the product-list endpoint when related categories are loaded without `prefetch_related()`.



# Benchmark Result — With `prefetch_related`

## Test Configuration

* **Endpoint:** `GET /products/?with_category=true&optimize=true`
* **Database:** PostgreSQL
* **Dataset:** 1000 Products
* **Related Data:** Product Categories
* **Optimization:** Enabled
* **ORM Queryset:** `Product.objects.all().prefetch_related("categories")`
* **Load Testing Tool:** Locust
* **Failures:** 0

## Results

| Metric                |        Result |
| --------------------- | ------------: |
| Total Requests        |           146 |
| Failed Requests       |             0 |
| Median Response Time  |      2,400 ms |
| Average Response Time |   2,367.98 ms |
| P95 Response Time     |      4,800 ms |
| P99 Response Time     |      5,200 ms |
| Minimum Response Time |         94 ms |
| Maximum Response Time |      5,236 ms |
| Average Response Size | 146,935 bytes |
| Requests Per Second   |          11.3 |
| Failures Per Second   |             0 |

## Query Configuration

For this test, Django uses `prefetch_related()` to preload the related categories:

```python
Product.objects.all().prefetch_related("categories")
```

This allows Django to retrieve the products and their related categories using a small number of database queries instead of repeatedly querying the database while serializing each product.

Conceptually:

```text
Query 1
    ↓
Fetch products

Query 2
    ↓
Fetch related categories

Django
    ↓
Associate categories with products in memory
```

## Performance Analysis

The optimized implementation showed a significant improvement compared with the baseline without `prefetch_related()`.

Average response time decreased from:

```text
33,863.31 ms → 2,367.98 ms
```

This represents approximately a **93% reduction in average response time**.

Median latency decreased from:

```text
34,000 ms → 2,400 ms
```

P95 latency decreased from:

```text
63,000 ms → 4,800 ms
```

The maximum observed latency also decreased significantly:

```text
65,968 ms → 5,236 ms
```

Throughput increased from:

```text
1.4 RPS → 11.3 RPS
```

The optimized implementation therefore processed substantially more requests per second while maintaining zero failures.

## Comparison With Baseline

| Metric   | Without Prefetch |   With Prefetch |
| -------- | ---------------: | --------------: |
| Requests |              102 |             146 |
| Failures |                0 |               0 |
| Median   |        34,000 ms |    **2,400 ms** |
| Average  |     33,863.31 ms | **2,367.98 ms** |
| P95      |        63,000 ms |    **4,800 ms** |
| P99      |        65,000 ms |    **5,200 ms** |
| Min      |         1,059 ms |       **94 ms** |
| Max      |        65,968 ms |    **5,236 ms** |
| RPS      |              1.4 |        **11.3** |

## Conclusion

The benchmark demonstrates a substantial performance improvement when using `prefetch_related()` for the product list endpoint with related categories.

The most significant improvement was observed in average and tail latency, while throughput also increased considerably.

The results strongly suggest that loading related categories without prefetching was creating a large number of unnecessary database queries, resulting in an N+1 query pattern.

Using:

```python
Product.objects.all().prefetch_related("categories")
```

significantly reduced the database overhead and improved API performance.

> Note: The two benchmark runs processed different numbers of requests (102 vs. 146), so the results should be considered an initial benchmark. For a more rigorous comparison, both configurations should be tested multiple times using identical load, duration, and environment conditions.







# Benchmark Result — Without Connection Pooling

## Test Configuration

* **Endpoint:** `GET /products/?with_category=true`
* **Connection Pooling:** Disabled
* **Load Testing Tool:** Locust
* **Database:** PostgreSQL
* **Dataset:** 1000 Products

## Results

| Metric                |        Result |
| --------------------- | ------------: |
| Total Requests        |           102 |
| Failed Requests       |             0 |
| Median Response Time  |     34,000 ms |
| Average Response Time |  33,863.31 ms |
| P95 Response Time     |     63,000 ms |
| P99 Response Time     |     65,000 ms |
| Minimum Response Time |      1,059 ms |
| Maximum Response Time |     65,968 ms |
| Average Response Size | 146,935 bytes |
| Requests Per Second   |           1.4 |
| Failures Per Second   |             0 |

## Summary

The API completed all 102 requests successfully with no failures.

However, the response latency was high, with an average response time of approximately **33.86 seconds** and a P95 latency of **63 seconds**.

The observed throughput was approximately **1.4 requests per second**.

These results represent the baseline performance of the API **without database connection pooling** and will be used for comparison with the connection-pooling configuration.







# Benchmark Result — With Connection Pooling

## Test Configuration

* **Endpoint:** `GET /products/?with_category=true`
* **Database:** PostgreSQL
* **Connection Pooling:** Enabled
* **Load Testing Tool:** Locust
* **Dataset:** 1000 Products
* **Total Requests:** 100
* **Failed Requests:** 0

## Results

| Metric                |    Result |
| --------------------- | --------: |
| Total Requests        |       100 |
| Failed Requests       |         0 |
| Median Response Time  | 30,000 ms |
| Average Response Time | 29,500 ms |
| P95 Response Time     | 55,000 ms |
| P99 Response Time     | 61,000 ms |
| Minimum Response Time |    900 ms |
| Maximum Response Time | 63,000 ms |
| Requests Per Second   |       1.7 |
| Failures Per Second   |         0 |

## Performance Analysis

With database connection pooling enabled, the API processed **100 requests with zero failures**.

The average response time was **29,500 ms**, compared with **33,863 ms** in the baseline without connection pooling.

The median response time decreased from **34,000 ms to 30,000 ms**.

P95 latency decreased from **63,000 ms to 55,000 ms**, while P99 latency decreased from **65,000 ms to 61,000 ms**.

The maximum response time decreased from **65,968 ms to 63,000 ms**.

Throughput also improved from **1.4 requests/second to 1.7 requests/second**.

## Comparison

| Metric  | Without Pooling | With Pooling | Improvement |
| ------- | --------------: | -----------: | ----------: |
| Median  |       34,000 ms |    30,000 ms |      11.76% |
| Average |       33,863 ms |    29,500 ms |      12.89% |
| P95     |       63,000 ms |    55,000 ms |      12.70% |
| P99     |       65,000 ms |    61,000 ms |       6.15% |
| Max     |       65,968 ms |    63,000 ms |       4.50% |
| RPS     |             1.4 |          1.7 |      21.43% |

## Conclusion

The benchmark indicates that enabling database connection pooling improved the API's overall performance under concurrent load.

The average response time decreased by **12.89%**, while throughput increased by **21.43%**.

The improvement is attributed to reusing existing PostgreSQL connections instead of repeatedly creating new database connections.

Connection pooling is therefore expected to provide greater benefits as the number of concurrent requests increases and the cost of establishing database connections becomes a larger portion of the request lifecycle.
