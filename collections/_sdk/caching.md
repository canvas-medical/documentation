---
title: "Caching API"
---

The Canvas SDK provides a caching API for plugin developers to store and retrieve temporary data efficiently.

For persistent storage of plugin data, use instead the [Custom Data](/sdk/custom-data/) features.

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

<!-- source: discussion #1205 -->
### Caching an external access token

When a plugin calls an external API that issues OAuth access tokens, cache the token rather than requesting a new one on every call. Set `timeout_seconds` to the token's lifetime so the plugin fetches a fresh one only after the old one expires. Keep the client credentials in [secrets](/sdk/secrets/).

```python?partial=true
from canvas_sdk.caching.plugins import get_cache
from canvas_sdk.utils import Http


def get_access_token(secrets: dict) -> str:
    cache = get_cache()
    token = cache.get("partner_access_token")
    if token is None:
        response = Http().post(
            "https://auth.example.com/oauth/token",
            data={
                "grant_type": "client_credentials",
                "client_id": secrets["PARTNER_CLIENT_ID"],
                "client_secret": secrets["PARTNER_CLIENT_SECRET"],
            },
        )
        body = response.json()
        token = body["access_token"]
        # Expire a minute early so a token never runs out mid-request.
        cache.set("partner_access_token", token, timeout_seconds=body["expires_in"] - 60)
    return token
```

Call it from a handler as `get_access_token(self.secrets)`.

---

## Supported Methods

### `get(key: str, default: Any | None = None) -> Any`

Retrieve a value from the cache:

```python?partial=true
user = cache.get("key")
```

You can specify a fallback if the key doesn't exist:

```python?partial=true
user = cache.get("key", default="default_value")
```

---

### `set(key: str, value: Any, timeout_seconds: int | None = None) -> None`

Store a value in the cache:

```python?partial=true
cache.set("key", {"name": "Alice"}, timeout_seconds=600)
```

---

### `get_or_set(key: str, default: Any | Callable, timeout_seconds: int | None = None) -> Any`

Fetch a value or set it if not present:

```python?partial=true
value = cache.get_or_set("key", default=lambda: compute_value(), timeout_seconds=300)
```

---

### `set_many(data: dict[str, Any], timeout_seconds: int | None = None) -> list[str]`

Set multiple values at once:

```python?partial=true
cache.set_many({
    "key1": {"name": "Alice"},
    "key2": {"name": "Bob"}
}, timeout_seconds=900)
```

---

### `get_many(keys: Iterable[str]) -> dict[str, Any]`

Fetch multiple values in one operation:

```python?partial=true
users = cache.get_many(["key1", "key2"])
```

---

### `delete(key: str) -> None`

Remove a key from the cache:

```python?partial=true
cache.delete("key")
```

---

### `__contains__(key: str) -> bool`

Check if a key exists in cache:

```python?partial=true
if "key" in cache:
    ...
```
