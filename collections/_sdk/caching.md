---
title: "Caching API"
---

The Canvas SDK provides a caching API for plugin developers to store and retrieve temporary data efficiently.

---

## Getting the Cache Client

To use the cache in your plugin, simply import and call:

```python
from canvas_sdk.caching.plugins import get_cache

cache = get_cache()
```

---

## TTL and Expiration

- By default, all cached keys expire after **14 days**.
- You can set a shorter TTL when writing to the cache via the `timeout_seconds` parameter.
- If a longer TTL is provided, a `CachingException` will be raised.

---

## Supported Methods

### `get(key: str, default: Any | None = None) -> Any`

Retrieve a value from the cache:

```python
user = cache.get("key")
```

You can specify a fallback if the key doesn't exist:

```python
user = cache.get("key", default="default_value")
```

---

### `set(key: str, value: Any, timeout_seconds: int | None = None) -> None`

Store a value in the cache:

```python
cache.set("key", {"name": "Alice"}, timeout_seconds=600)
```

---

### `get_or_set(key: str, default: Any | Callable, timeout_seconds: int | None = None) -> Any`

Fetch a value or set it if not present:

```python
value = cache.get_or_set("key", default=lambda: compute_value(), timeout_seconds=300)
```

---

### `set_many(data: dict[str, Any], timeout_seconds: int | None = None) -> list[str]`

Set multiple values at once:

```python
cache.set_many({
    "key1": {"name": "Alice"},
    "key2": {"name": "Bob"}
}, timeout_seconds=900)
```

---

### `get_many(keys: Iterable[str]) -> dict[str, Any]`

Fetch multiple values in one operation:

```python
users = cache.get_many(["key1", "key2"])
```

---

### `delete(key: str) -> None`

Remove a key from the cache:

```python
cache.delete("key")
```

---

### `__contains__(key: str) -> bool`

Check if a key exists in cache:

```python
if "key" in cache:
    ...
```
