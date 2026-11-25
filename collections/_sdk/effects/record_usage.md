---
title: "Record Usage"
slug: "effect-record-usage"
excerpt: "Record units of a plugin's work that its catalog listing prices, such as one visit."
hidden: false
---

The `RecordUsage` effect records units of work that a plugin charges for. A plugin priced per unit in its [manifest `catalog.pricing`](/sdk/canvas_manifest/#catalog), such as $0.50 a visit, returns one `RecordUsage` for each piece of that work, alongside the effects that do it. Canvas keeps each record on the instance, and Canvas Platform reads them a few minutes later to show what the units come to.

Canvas fills in what the plugin does not choose:

* **The plugin.** The record is attributed to the plugin whose handler returned it. A plugin can record usage under its own name only.
* **The version.** The plugin version and package installed on the instance when the record is stored.
* **The time.** When Canvas applied the effect, so a handler never passes a timestamp.

## Counting once

`key` names the piece of work being counted, such as `visit:<note id>`. Canvas records a key once per plugin, so a handler that runs again for the same work (a retried event, a note signed twice) adds nothing. Choose a key that is the same every time the same work is counted and different for different work.

## Failed work is not counted

Canvas applies a plugin's `RecordUsage` effects after the plugin's other effects in the same response. When one of those other effects fails, the usage is kept with a withheld status, naming the effect that failed, and is not charged. A later run that does the work successfully can record the same key and is counted.

An effect run later with [`set_async`](/sdk/effects/#async-execution) has no outcome yet when the usage is stored, so the unit is counted and the record names the deferred effect. A `RecordUsage` effect itself cannot be deferred: one with `set_async` is discarded.

## Units

`unit` must be one of the units the plugin's installed manifest lists in `catalog.pricing`, matched without regard to case or repeated whitespace. A record in any other unit, or in `token`, is discarded and logged, since the inference gateway meters tokens on its own. Units are recorded on every instance; the instance's stage decides what is charged.

## Methods

### apply() → Effect

Records the usage.

## Attributes

| Name | Type | Description | Required |
|---|---|---|---|
| `unit` | `str` | A unit from the plugin's manifest `catalog.pricing`, at most 40 characters. | Yes |
| `key` | `str` | Names the work being counted, so the same work is counted once. 1 to 256 characters. | Yes |
| `quantity` | `int` | How many units the work comes to, from 1 to 10,000. Defaults to 1. | No |

## Example

A plugin listed at a price per `visit` records one visit when a note is locked, keyed on the note so a note locked again is not counted twice:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.usage import RecordUsage
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class CountVisit(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.NOTE_STATE_CHANGE_EVENT_CREATED)

    def compute(self) -> list[Effect]:
        if self.event.context["state"] != "LKD":
            return []
        note_id = self.event.context["note_id"]
        return [RecordUsage(unit="visit", key=f"visit:{note_id}").apply()]
```

A plugin recording several units of one piece of work passes `quantity`, such as `RecordUsage(unit="page", key=f"fax:{fax_id}", quantity=12)`.
