---
title: Jobs
---

# Jobs

The Jobs API provides a seamless way of running any function
asynchronously, either ad-hoc, on a fixed interval, or on a cron
schedule.

## Basic Usage

The interface for this module consists of a few decorators you can use
in any method, depending on the use-case you\'re trying to achieve:

### `@jobs.background_task`

Decorating a function with `@background_task` will allow the function to
be executed asynchronously in a background worker.

Background tasks can be invoked by calling their
`.delay(*args, **kwargs)` method:

``` python
import time
from canvas_core import jobs

@jobs.background_task
def print_message(message: str, wait: int = 0) -> None:
    time.sleep(wait)
    print(message)

# This job will be enqueued for immediate execution, and the function will
# wait 10 seconds before printing "Hello world!"
print_message.delay("Hello world!", wait=10)
```

### `@jobs.periodic_task`

This decorator takes an `interval` argument, which will cause the
function to be executed periodically on the configured time interval.

The following example will print the current timestamp every minute.

``` python
from datetime import datetime, timedelta

from canvas_core import jobs

@jobs.periodic_task(interval=timedelta(seconds=60))
def print_time() -> None:
    print(datetime.now().isoformat())
```

### `@jobs.scheduled_task`

This decorator takes a `schedule` argument, which will execute the
function on a specific time-based schedule (i.e., cron).

The following example will print the current timestamp every day at
midnight.

``` python
from datetime import datetime

from canvas_core import jobs

@jobs.periodic_task(schedule=jobs.crontab(minute=0, hour=0))
def print_time() -> None:
    print(datetime.now().isoformat())
```

## API Reference

::: {.automodule members=""}
canvas_core.jobs
:::
