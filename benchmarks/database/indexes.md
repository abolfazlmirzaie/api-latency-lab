# BENCH-001 — Database Index Impact

## Research Question

How does adding a database index to the `Product.title` field affect the latency of API requests that search for a product by title?

## Objective

Compare the performance of the same API endpoint in two scenarios:

1. Without an index on `Product.title`
2. With an index on `Product.title`

The goal is to determine whether the index reduces database query time and overall API latency.

## Hypothesis

We expect the indexed query to be faster than the non-indexed query, especially as the number of records increases.

## Test Endpoint

```http
GET /api/products/?search=iPhone