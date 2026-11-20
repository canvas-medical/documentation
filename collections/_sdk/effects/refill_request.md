---
title: "Refill Request"
slug: "effect-update-refill-request"
excerpt: "Assign a pending refill request to a staff member, ignore it, or both."
hidden: false
---

The `UpdateRefillRequest` effect changes a [refill request](/sdk/data-refill-request/) that is still in the refill queue. Use it to assign the request to a staff member, to ignore it, or to do both in one effect.

Ignoring a request does the same thing as the **Ignore** button in the refill panel: the request leaves the queue, and nothing is sent to the pharmacy. Use it for a request that was already handled some other way. To send the pharmacy an answer, approve or deny the request instead.

Only pending requests can be updated: requests that aren't ignored and have no committed response. These are the requests that [`RefillRequest.objects.pending()`](/sdk/data-refill-request/#pending-requests) returns.

## Methods

### apply() → Effect

Updates the refill request.

- `id` must be the id of a [pending refill request](/sdk/data-refill-request/#pending-requests), one that `RefillRequest.objects.pending()` returns. A request that was already ignored or answered can't be updated, including to reassign it.
- Set `assignee_id`, `ignored`, or both.

Ignoring sets the request's `ignored` attribute and fires the [`REFILL_REQUEST_UPDATED`](/sdk/events/#refill-requests) event. It doesn't write a response to the request.

## Attributes

| Attribute     | Type            | Description                                                                 | Required |
|---------------|-----------------|-----------------------------------------------------------------------------|----------|
| `id`          | `str` or `UUID` | ID of the refill request to update                                          | Yes      |
| `assignee_id` | `str`           | Key of the [staff](/sdk/data-staff/#staff) member to assign the request to. The assignee must be an active prescriber with a Surescripts SPI. | Unless `ignored` is set |
| `ignored`     | `bool`          | Set to `True` to ignore the request. An ignored request can't be returned to the queue, so `True` is the only value this attribute accepts. | Unless `assignee_id` is set |

## Example

This handler runs on a schedule and ignores pending requests that are more than 30 days old:

```python
from datetime import timedelta

from canvas_sdk.effects import Effect
from canvas_sdk.effects.refill_request import UpdateRefillRequest
from canvas_sdk.handlers.cron_task import CronTask
from canvas_sdk.v1.data.refill_request import RefillRequest
from django.utils import timezone


class IgnoreStaleRefillRequests(CronTask):
    SCHEDULE = "0 6 * * *"

    def execute(self) -> list[Effect]:
        cutoff = timezone.now() - timedelta(days=30)
        stale_requests = RefillRequest.objects.pending().filter(created__lt=cutoff)
        return [
            UpdateRefillRequest(id=refill_request.id, ignored=True).apply()
            for refill_request in stale_requests
        ]
```

To reassign a request, set `assignee_id`:

```python
from canvas_sdk.effects.refill_request import UpdateRefillRequest

effect = UpdateRefillRequest(
    id="d2194110-5c9a-4842-8733-ef09ea5ead11",
    assignee_id="4150cd20de8a470aa570a852859ac87e",
).apply()
```

When an assignment changes, Canvas fires the [`REFILL_REQUEST_ASSIGNEE_UPDATED`](/sdk/events/#refill-requests) event.
