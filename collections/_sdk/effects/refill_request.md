---
title: "Refill Request"
slug: "effect-update-refill-request"
excerpt: "Assign a pending refill request to a staff member, or ignore it."
hidden: false
---

The `UpdateRefillRequest` effect changes a [refill request](/sdk/data-refill-request/) that is still in the refill queue. Use it to assign the request to a staff member, or to ignore it.

Ignoring a request does the same thing as the **Ignore** button in the refill panel: the request leaves the queue, and nothing is sent to the pharmacy. Use it for a request that was already handled some other way. To send the pharmacy an answer, approve or deny the request instead.

Only pending requests can be updated: requests that aren't ignored and have no committed response. These are the requests that [`RefillRequest.objects.pending()`](/sdk/data-refill-request/#pending-requests) returns.

## Methods

### apply() → Effect

Updates the refill request.

- `id` must be the id of a [pending refill request](/sdk/data-refill-request/#pending-requests), one that `RefillRequest.objects.pending()` returns. A request that was already ignored or answered can't be updated, including to reassign it.
- Set `assignee_id` to reassign the request, or `ignored=True` to take it out of the queue. One of them is required.

Ignoring sets the request's `ignored` attribute and fires the [`REFILL_REQUEST_UPDATED`](/sdk/events/#refill-requests) event. It doesn't write a response to the request.

## Attributes

| Attribute     | Type            | Description                                                                 | Required |
|---------------|-----------------|-----------------------------------------------------------------------------|----------|
| `id`          | `str` or `UUID` | ID of the [refill request](/sdk/data-refill-request/#refillrequest) to update                                          | Yes      |
| `assignee_id` | `str`           | ID of the [staff](/sdk/data-staff/#staff) member to assign the request to. The assignee must be an active prescriber with a Surescripts SPI. See [Choosing an assignee](#choosing-an-assignee). | Unless `ignored` is set |
| `ignored`     | `bool`          | Set to `True` to ignore the request. An ignored request can't be returned to the queue, so `True` is the only value this attribute accepts. | Unless `assignee_id` is set |

## Choosing an assignee

A refill request can only be assigned to someone who could prescribe the refill, the same people the refill panel's assignee picker lists. Canvas checks three things on the staff member:

- **Active:** `staff.active` is `True`.
- **Set up for e-prescribing:** `staff.spi_number` is set. This is the staff member's Surescripts prescriber ID.
- **A prescriber role:** the `internal_code` of `staff.top_clinical_role` is one of your instance's prescriber roles. By default those are `MD`, `DO`, `NP`, and `PA`.

If any check fails, the effect is refused with "the assignee must be an active prescriber with a Surescripts SPI", and the request keeps its current assignee.

Reassigning moves the request to the new assignee's queue. It doesn't change the prescriber on the refill: the pharmacy's answer still names the prescriber from the original request.

To pick only staff who pass, filter in your plugin:

```python
from canvas_sdk.v1.data import Staff

PRESCRIBER_ROLES = {"MD", "DO", "NP", "PA"}


def can_be_refill_assignee(staff: Staff) -> bool:
    role = staff.top_clinical_role
    return bool(
        staff.active
        and staff.spi_number
        and role is not None
        and role.internal_code in PRESCRIBER_ROLES
    )


assignees = [
    staff
    for staff in Staff.objects.filter(active=True)
    .exclude(spi_number="")
    .prefetch_related("roles")
    if can_be_refill_assignee(staff)
]
```

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

To reassign requests, set `assignee_id`. This handler runs every 15 minutes and assigns every pending request to an active nurse practitioner who can e-prescribe, skipping requests already assigned to them. Change `REFILL_ROLE` to the role your team routes refills to, and see [Choosing an assignee](#choosing-an-assignee) for who can be assigned:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.refill_request import UpdateRefillRequest
from canvas_sdk.handlers.cron_task import CronTask
from canvas_sdk.v1.data import Staff
from canvas_sdk.v1.data.refill_request import RefillRequest

REFILL_ROLE = "NP"


class AssignPendingRefillRequests(CronTask):
    SCHEDULE = "*/15 * * * *"

    def execute(self) -> list[Effect]:
        candidates = (
            Staff.objects.filter(active=True)
            .exclude(spi_number="")
            .prefetch_related("roles")
        )
        assignee = next(
            (
                staff
                for staff in candidates
                if staff.top_clinical_role
                and staff.top_clinical_role.internal_code == REFILL_ROLE
            ),
            None,
        )
        if assignee is None:
            return []

        pending = RefillRequest.objects.pending().exclude(staff=assignee)
        return [
            UpdateRefillRequest(
                id=refill_request.id, assignee_id=assignee.id
            ).apply()
            for refill_request in pending
        ]
```

When an assignment changes, Canvas fires the [`REFILL_REQUEST_ASSIGNEE_UPDATED`](/sdk/events/#refill-requests) event.
