---
title: "Handlers"
---

The handlers module lets you define reactions to events.

Handlers respond to [Events](/sdk/events/) and return zero, one, or many [Effects](/sdk/effects/).

There are some special types of handlers, like [Protocols](/sdk/protocols/)
and [CronTasks](/sdk/handlers-crontask/). These offer a differentiated
interface for their particular use-cases. For example, CronTasks only ever
respond to the `CRON` event, require a schedule to be specified, and expect
the `execute` method to be implemented rather than `compute`.
