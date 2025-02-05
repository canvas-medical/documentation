---
title: "CronTask"
slug: "handlers-crontask"
excerpt: "Canvas SDK CronTasks offer scheduled code execution."
---

You can write a handler that subclasses `CronTask` to execute code on a
schedule. You might use this to automate reporting on task performance (every
hour, send the number of tasks created during the previous hour, and the
number of tasks completed during the previous hour), to send birthday wishes
to your patients (at 7am every morning, find patients born on this day and
send them an email wishing them a happy birthday), or to send customized
appointment reminders (every hour, find appointments that start on this hour
the following day and send the patients of those appointments a message that
says "Dr. X is looking forward to seeing you at (location) at (time)").

## Example

This example `CronTask` shows an extremely basic example that just logs the
time. You can see the critical pieces here:
- Subclass `CronTask`
- Set your `SCHEDULE` with a cron string
- Implement an `execute` method with the code you want to schedule to run,
  returning a list containing any effects you want to return, or an empty list
  if you do not wish to return any effects.

```python
from canvas_sdk.handlers.cron_task import CronTask
from canvas_sdk.effects import Effect

from logger import log


class LogTheTime(CronTask):
    # A cron string.
    #           ┌───────────── minute (0 - 59)
    #           │ ┌───────────── hour (0 - 23)
    #           │ │ ┌───────────── day of the month (1 - 31)
    #           │ │ │ ┌───────────── month (1 - 12)
    #           │ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday)
    #           │ │ │ │ │
    #           │ │ │ │ │
    #           │ │ │ │ │
    SCHEDULE = "* * * * *"  # Run every minute, which is the most frequently something can run.

    def execute(self) -> list[Effect]:
        # The current timestamp can be found as an iso8601 string in
        # `self.target`
        log.info(f"The current time is {self.target}")

        # We don't need to return any effects
        return []
```

### Output
Here's what this scheduled task would output in the logs:

`INFO 2024-07-18 18:47:00,000 The current time is 2024-07-18T18:47:00.000000+00:00`

<br/>
<br/>
<br/>
<br/>
