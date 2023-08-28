# Metrics

The Metrics API provides a preconfigured client for the StatsD protocol,
as well as several useful utilities for reporting metrics.

## Basic Usage

``` python
>>> from canvas_core import metrics

# Get a preconfigured StatsD client.
>>> statsd = metrics.get_statsd_client()

# Use any method that the StatsD interface provides.
>>> statsd.incr("my.metric.identifier")
>>> statsd.timing("my.metric.timing", 10)
>>> ...

# Use the mkstat utility to add tags to your metrics.
>>> stat = metrics.mkstat("my.metric.identifier", tags={"my": "tag", "another": "tag"})
>>> statsd.incr(stat)

# Use the measure context manager to automatically measure blocks of code.
#
# The context manager will automatically measure call count, successful
# calls, errored calls, and executing timing.
#
>>> with measure("my.function.call", extra_tags={"my": "tag"}):
...    my_function()

# You can also used the @measured decorator on any function, which applies
# the measure context manager to the function call. It automatically tags
# the metrics with the import path of the decorated function.
>>> @metrics.measured
... def my_function() -> None:
...     pass

# The @measured decorator accepts the same keyword arguments as the measure
# context manager.
>>> @metrics.measured(extra_tags={"my": "tags"})
... def my_function() -> None:
...     pass
```

## Metrics reported by the `measure` context manager

The metrics collected by the `measured` context manager are:

### `metrics.measurements.executions`

The number of times the block within the context manager was executed.

Each execution is tagged with a `status` tag (either `success` for
successful executions, or `error` for executions that resulted in an
exception being raised).

### `metrics.measurements.timings`

The amount of time elapsed during execution of the block (in
milliseconds).

Each timing is tagged with a `status` tag (either `success` for
successful executions, or `error` for executions that resulted in an
exception being raised).

## API Reference

::: {.automodule members=""}
canvas_core.metrics
:::
