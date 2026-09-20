# BENCH-003 — Pagination

## Objective

Measure the effect of pagination on API response latency and response size.

The benchmark compares returning the complete product dataset with returning a
small page of the same dataset.

The main question is:

> Does pagination reduce response size and API latency when the database contains
> 1,000 products?

---

## Dataset

- Entity: Products
- Dataset size: 1,000 products
- Endpoint: `GET /api/products/`

The same dataset must be used for both scenarios.

---

## Scenarios

### Scenario A — Without Pagination

Request the complete product collection:

```http
GET /api/products/