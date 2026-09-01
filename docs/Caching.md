# API Caching with Redis

## What is Caching?

**Caching** is a technique where we add a fast storage layer in front of the database.

Instead of sending every request directly to the database, the application first checks the **cache** to see if the requested data is already available.

A common choice for API caching is **Redis** because it stores data primarily in memory (RAM), making read operations significantly faster than accessing a traditional database such as PostgreSQL.

---

## Example: API Returning 1,000 Products

Imagine we have an API endpoint that returns **1,000 products**.

Without caching, every request might follow this flow:

```text
Client
   ↓
API
   ↓
PostgreSQL
   ↓
Fetch 1,000 products
   ↓
API Response
   ↓
Client
```

If many users repeatedly request the same data, the application has to query PostgreSQL and retrieve the same 1,000 products again and again.

This can increase:

* Database load
* Query time
* CPU and memory usage
* API response latency

---

## Using Redis as a Cache

To reduce unnecessary database queries, we can place **Redis** between the API and the database.

The request flow becomes:

```text
Client
   ↓
API
   ↓
Redis
   ↓
Cache Hit?
  /    \
Yes     No
 ↓       ↓
Return  PostgreSQL
data      ↓
 ↓      Get data
Client     ↓
         Store in Redis
            ↓
         Return data
            ↓
          Client
```

### Step 1: Check Redis

When a request arrives, the application first checks Redis.

For example, we can use a cache key such as:

```text
products:all
```

The application asks Redis:

> "Do you already have the response for this request?"

---

### Step 2: Cache Hit

If the data exists in Redis, we have a **cache hit**.

The application can immediately return the cached response to the client without querying PostgreSQL.

```text
Client
   ↓
API
   ↓
Redis
   ↓
Cache Hit ✅
   ↓
Cached Response
   ↓
Client
```

Because Redis is an in-memory data store, reading cached data is generally much faster than performing the same operation against PostgreSQL.

---

### Step 3: Cache Miss

But what happens if the response does **not** exist in Redis?

This is called a **cache miss**.

In this case, the application continues to the database:

```text
Client
   ↓
API
   ↓
Redis
   ↓
Cache Miss ❌
   ↓
PostgreSQL
   ↓
Get 1,000 products
   ↓
Store response in Redis
   ↓
Return response
   ↓
Client
```

The application retrieves the data from PostgreSQL and then stores the result in Redis.

This means that the next request for the same data can be served directly from Redis.

---

## The Complete Caching Flow

The complete process can be summarized as follows:

1. The client sends a request to the API.
2. The API checks Redis for the requested data.
3. If the data exists, Redis returns it immediately (**Cache Hit**).
4. If the data does not exist, we have a **Cache Miss**.
5. The API queries PostgreSQL.
6. The database returns the requested data.
7. The API stores the result in Redis.
8. The API returns the response to the client.
9. Future requests can retrieve the same data directly from Redis.

### First Request

```text
Client
  ↓
API
  ↓
Redis → Cache Miss
  ↓
PostgreSQL
  ↓
1000 Products
  ↓
Redis ← Store Data
  ↓
Client
```

### Subsequent Requests

```text
Client
  ↓
API
  ↓
Redis → Cache Hit
  ↓
1000 Products
  ↓
Client
```

---

## Why Does This Improve API Performance?

Without caching, repeated requests for the same data continuously hit the database.

With caching, frequently requested data can be served from Redis instead.

For example:

```text
Without Cache:

Request → API → PostgreSQL → Response
Request → API → PostgreSQL → Response
Request → API → PostgreSQL → Response
Request → API → PostgreSQL → Response
```

With Redis:

```text
First Request:

Request → API → Redis ❌ → PostgreSQL → Redis → Response

Next Requests:

Request → API → Redis ✅ → Response
Request → API → Redis ✅ → Response
Request → API → Redis ✅ → Response
```

This reduces the number of database queries and can significantly reduce **API latency**, especially when the same data is requested frequently.

> **Important:** Caching does not make PostgreSQL faster. Instead, it prevents PostgreSQL from being queried when the requested data is already available in the cache.

---

## Cache Hit vs. Cache Miss

| Term           | Meaning                                                                                         |
| -------------- | ----------------------------------------------------------------------------------------------- |
| **Cache Hit**  | The requested data exists in Redis and can be returned directly.                                |
| **Cache Miss** | The requested data does not exist in Redis, so the application must fetch it from the database. |

The goal of caching is generally to achieve a high **cache hit rate**, because more cache hits mean fewer database queries.
