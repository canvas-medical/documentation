---
title: Caching
---

# Caching

The Caching API provides a simple interface for caching objects with
multiple storage strategies.

## Basic Usage

``` python
>>> from canvas_core import caching

# Get the Cache client.
>>> cache = caching.get_cache()

# Fetch a given key from the cache.
>>> cache.get("my_cache_key")

# Set a value in the cache.
>>> cache.set("my_cache_key", "my_value")

# Delete a key from the cache.
>>> cache.delete("my_cache_key")

# Check if the key exists in the cache
>>> "my_cache_key" in cache

# Delete the entire cache
>>> cache.clear()

# Delete the contents of all configured caches.
>>> caching.clear_caches()
```

## API Reference

::: {.automodule members=""}
canvas_core.caching
:::
