---
title: Logging
---

# Logging

The Logging API is responsible for handling structured logging. It
provides a simple interface for all standard log levels.

## Basic Usage

The logging interface is simple, and should be used as a drop-in
substitute for the standard library `logging` module.

For convenience, all you need to get started is the `get_logger`
function, which returns an instance of the `Logger` class.

``` python
>>> from canvas_core import logging
>>> logger = logging.get_logger(__name__)

# Log a message
>>> logger.info("Processing...")
# INFO     canvas_core.logging.tests:base.py:35 2022-12-22T19:58:34.803565Z [info     ] Processing...                  [canvas_core.logging.tests]

# Log a message with custom levels and added context
>>> logger.debug("Processing...", event="Save Patient", patient_name="John Doe")
# INFO     canvas_core.logging.tests:base.py:35 2022-12-22T20:00:59.226831Z [debug    ] Processing...                  [canvas_core.logging.tests] event_id=Save Patient patient=John Doe

# Bind context to all logging messages for a block
>>> with logger.bind_context(request_id="my-request-id"):
...     logger.debug("Processing...")
# INFO     canvas_core.logging.tests:base.py:35 2022-12-22T19:58:34.803565Z [debug    ] Processing...                  [canvas_core.logging.tests] request_id=my-request-id
```

## API Reference

::: {.automodule members=""}
canvas_core.logging
:::
