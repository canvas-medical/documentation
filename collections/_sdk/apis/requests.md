---
title: Requests
---

# Requests

The Requests API is responsible for handling HTTP requests. It provides
a simple interface for completing HTTP calls with metrics tracking.

## Basic Usage

The requests interface is simple, and should be used as a drop-in
substitute for the python `requests` library\'s `Session` object.

For convenience, all you need to get started is the `get_session`
function, which returns an instance of the `Session` class.

``` python
from canvas_core import get_session

session = get_session()

get_resp = session.get("http://...")
post_resp = session.post("http://...", data=...)
```

## API Reference

::: {.automodule members=""}
canvas_core.requests
:::
