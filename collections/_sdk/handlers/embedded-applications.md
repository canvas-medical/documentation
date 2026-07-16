---
title: "Embedded Applications"
slug: "handlers-embedded-applications"
excerpt: "Handler-based applications that render inside a note or replace the scheduling modal."
hidden: false
---

Embedded applications render **inside a specific Canvas surface** — a tab within
a note, or the scheduling modal — rather than as an icon in the app drawer. They
are ordinary [handlers](/sdk/handlers-basehandler/): you subclass a base class,
register it under `handlers` in your `CANVAS_MANIFEST.json`, and Canvas renders
it in the appropriate surface.

There are two kinds:

| Base class            | Surface                                                  |
|-----------------------|----------------------------------------------------------|
| `NoteApplication`     | A tab within a patient's note                            |
| `SchedulingApplication` | Replaces the built-in scheduling modal at every entry point |

## How embedded applications work

Embedded applications are [handlers](/sdk/handlers-basehandler/). You build one
by subclassing `NoteApplication` or `SchedulingApplication` and registering it
under `handlers` in your `CANVAS_MANIFEST.json` — everything else is inherited
from that parent class.

Because the parent class defines the behavior, there's very little to configure:

- The **surface** comes from the class you inherit — `NoteApplication` renders as
  a tab in a note, and `SchedulingApplication` replaces the scheduling modal. You
  don't set a `scope` or an `icon`.
- Canvas **renders them on demand**: when a note opens or a scheduling action is
  triggered, Canvas asks which embedded application is installed for that surface
  and renders the one your handler returns. They aren't persisted as drawer
  applications, so they don't appear in the app drawer or under
  Plugins_IO > Applications.
- If no embedded application is installed for a surface, Canvas falls back to its
  built-in behavior — an unmodified note, or the built-in scheduling modal.

Since the surface and scope are inherited from the parent class, register these
under `handlers` rather than `applications`.

## Note Applications

Note Applications appear as tabs within a patient's note, allowing you to embed custom interfaces directly in the clinical documentation workflow.

### Implementing a Note Application

To create a Note Application, your handler class should inherit from `NoteApplication` and define the following class attributes:

| Attribute    | Description                                                                    |
|--------------|--------------------------------------------------------------------------------|
| `NAME`       | (Required) The display title shown on the tab (supports emojis)                |
| `IDENTIFIER` | (Required) A unique key for the application (recommended format: `plugin_name__app_name`) |
| `PRIORITY`   | (Optional) Controls tab order — lower values appear first. Defaults to `0`      |

> **Tip:** If your Note Application is named "Note", it may cause confusion with the built-in Note tab. Users can rename the built-in tab by updating the Constance Config setting `NOTE_BODY_TAB_LABEL` in your instance Settings, to avoid duplication.

Your class must implement the `on_open()` method, which is called when the user clicks on the tab. This method should return an `Effect` or list of `Effect`s, typically a `LaunchModalEffect` with `target` set to `LaunchModalEffect.TargetType.NOTE`

> **⚠️  Important** If you have an existing plugin that overrides `handle()`, it will continue to work. However, `handle()` is deprecated — migrate to `on_open()` at your earliest convenience.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from canvas_sdk.handlers.application import NoteApplication


class PatientIntakeApp(NoteApplication):
    """Note application for patient intake workflow."""

    NAME = "📋 Patient Intake"
    IDENTIFIER = "my_plugin__patient_intake"

    def on_open(self) -> Effect | list[Effect]:
        """Launch the intake form when the tab is clicked."""
        note_id = self.event.context.get("note_id")
        patient_id = self.event.context.get("patient", {}).get("id")

        return LaunchModalEffect(
            target=LaunchModalEffect.TargetType.NOTE,
            content="<html>Your form HTML here</html>",
            title="Patient Intake Form"
        ).apply()
```

<div style="max-width: 100%"><img style="max-width: 100%" src="/assets/images/note-application-tabs.png" alt="note applications" /></div>

### Manifest Configuration

Register your Note Application under the `handlers` section of your
`CANVAS_MANIFEST.json`. There is no `scope` or `icon` — the note tab is driven by
the `NoteApplication` base class and the `NAME`/`IDENTIFIER` class attributes.

```json
{
  "components": {
    "handlers": [
      {
        "class": "my_plugin.apps.intake:PatientIntakeApp",
        "description": "In-note patient intake tab."
      }
    ]
  }
}
```

### Context and Event Data

Both `on_open()` and `handle()` have access to context data through `self.event.context`:

| Key       | Description                                       |
|-----------|---------------------------------------------------|
| `note_id` | The database ID of the current note               |
| `note`    | A dict containing the note's external `id` (UUID) |
| `patient` | A dict containing the patient's `id` (key)        |
| `user`    | Information about the current user                |

#### `on_open()` — recommended

When using `on_open()`, the patient is available through `self.event.context`:

```python
from canvas_sdk.effects import Effect

def on_open(self) -> Effect | list[Effect]:
    note_id = self.event.context.get("note_id")
    patient_id = self.event.context.get("patient", {}).get("id")
    ...
```

`self.event.target.id` contains the application identifier used internally for routing, not the patient.

#### `handle()` — deprecated

When using the deprecated `handle()`, `self.event.target.id` is automatically set to the patient UUID before `handle()` is called, preserving the original behavior that old plugins relied on:

```python
from canvas_sdk.effects import Effect

def handle(self) -> list[Effect]:
    patient_id = self.event.target.id  # backfilled from patient context
    ...
```

> **Note:** This backfilling only happens when `handle()` is called. Plugins that override `on_open()` directly should read the patient from `self.event.context` as shown above.

| Property                              | `on_open()`                          | `handle()` (deprecated)   |
|---------------------------------------|--------------------------------------|---------------------------|
| `self.event.target.id`                | Application identifier (for routing) | Patient UUID (backfilled) |
| `self.event.context["patient"]["id"]` | Patient UUID                         | Patient UUID              |
| `self.event.actor`                    | Authenticated user                   | Authenticated user        |

### Controlling Visibility

You can control when your Note Application tab is visible by overriding the `visible()` method. This method has access to the same context and event data as `on_open()`:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from canvas_sdk.handlers.application import NoteApplication


class ConditionalIntakeApp(NoteApplication):
    NAME = "📋 Intake"
    IDENTIFIER = "my_plugin__conditional_intake"

    def visible(self) -> bool:
        """Only show for specific conditions."""
        # Add your visibility logic here
        return True

    def on_open(self) -> Effect | list[Effect]:
        return LaunchModalEffect(
            target=LaunchModalEffect.TargetType.NOTE,
            content="<html>Form content</html>",
            title="Intake"
        ).apply()
```

### Opening by Default

You can make a Note Application tab open automatically when a note is first viewed by overriding `open_by_default()`. If multiple applications return `True`, the first one (by priority order) will be opened.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from canvas_sdk.handlers.application import NoteApplication


class AutoOpenApp(NoteApplication):
    NAME = "📋 Intake"
    IDENTIFIER = "my_plugin__auto_open_intake"

    def open_by_default(self) -> bool:
        """Open automatically when the note is viewed."""
        return True

    def on_open(self) -> Effect | list[Effect]:
        return LaunchModalEffect(
            target=LaunchModalEffect.TargetType.NOTE,
            content="<html>Form content</html>",
            title="Intake"
        ).apply()
```

### Tab Ordering

You can control the order in which Note Application tabs appear by setting the `PRIORITY` class attribute. Tabs are sorted in ascending order, so lower values appear first. The default is `0`.

```python
from canvas_sdk.handlers.application import NoteApplication

class HighPriorityApp(NoteApplication):
    NAME = "First Tab"
    IDENTIFIER = "my_plugin__first"
    PRIORITY = 1

class LowPriorityApp(NoteApplication):
    NAME = "Second Tab"
    IDENTIFIER = "my_plugin__second"
    PRIORITY = 10
```

> **Note:** Note Applications do not support [notification badges](/sdk/handlers-applications/#notification-badges).

## Scheduling Applications

Scheduling Applications replace the built-in scheduling modal throughout Canvas. When you install a plugin with a scheduling application, it takes over all scheduling entry points: the schedule page, patient chart, calendar drag-and-drop, calendar reschedule, and note reschedule flows.

### Implementing a Scheduling Application

To create a Scheduling Application, your handler class should inherit from `SchedulingApplication` and define two required class attributes:

| Attribute    | Description                                                                    |
|--------------|--------------------------------------------------------------------------------|
| `NAME`       | The display title shown in the modal                                           |
| `IDENTIFIER` | A unique key for the application (recommended format: `plugin_name__app_name`) |

Your class must implement the `on_open()` method, which is called when a scheduling action is triggered. This method should return an `Effect` or list of `Effect`s, typically a `LaunchModalEffect`.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from canvas_sdk.handlers.application import SchedulingApplication


class CustomScheduler(SchedulingApplication):
    """Scheduling application for custom appointment booking."""

    NAME = "Schedule Appointment"
    IDENTIFIER = "my_plugin__scheduler"

    def on_open(self) -> Effect | list[Effect]:
        """Launch the scheduling form when triggered."""
        patient = self.event.context.get("patient", {})
        provider = self.event.context.get("provider", {})
        start = self.event.context.get("start", "")
        mode = self.event.context.get("mode", "schedule")

        return LaunchModalEffect(
            url=f"https://scheduler.example.com/book?patient={patient.get('id', '')}&provider={provider.get('id', '')}&start={start}&mode={mode}",
            title="Schedule Appointment"
        ).apply()
```

### Context Data

When `on_open()` is called, scheduling context is available through `self.event.context`. The available keys depend on which entry point triggered the scheduling action.

#### Entity Objects

Entities are delivered as `{"id": <external id>}` objects, resolvable with the conventional `.objects.get(id=...)`:

| Field         | Resolves To                                                      | Value                            | Available From                  |
|---------------|------------------------------------------------------------------|----------------------------------|---------------------------------|
| `patient`     | [Patient](/sdk/data-patient/#patient)                            | `{"id": <patient id>}`           | Patient chart, reschedule flows |
| `provider`    | [Staff](/sdk/data-staff/#staff)                                  | `{"id": <staff id>}`             | Calendar, patient chart         |
| `location`    | [PracticeLocation](/sdk/data-practicelocation/#practicelocation) | `{"id": <practice location id>}` | Current location context        |
| `appointment` | [Appointment](/sdk/data-appointment/#appointment)                | `{"id": <appointment id>}`       | Reschedule flows                |
| `note`        | [Note](/sdk/data-note/#note)                                     | `{"id": <note id>}`              | Note reschedule flow            |

#### Scalar Values

| Key        | Description                                                                                                 |
|------------|-------------------------------------------------------------------------------------------------------------|
| `start`    | ISO-8601 datetime of the selected slot (all entry points)                                                   |
| `end`      | ISO-8601 datetime for the slot end (calendar drag-and-drop only)                                            |
| `duration` | Slot length in minutes (reschedule flows only). Either `end` or `duration` is present, never both           |
| `mode`     | One of `schedule`, `reschedule`, or `followup`                                                              |
| `origin`   | The launching surface: `schedule_page`, `patient_chart`, `calendar`, `calendar_reschedule`, or `note_reschedule` |

When `end` is not provided, derive it from `start + duration`.

#### Origins

`origin` tells you which surface launched the scheduling action, which in turn determines the `mode` and whether the slot length arrives as `end` or `duration`:

| `origin`              | Launching surface                                               | `mode`                   | Slot length            |
|-----------------------|-----------------------------------------------------------------|--------------------------|------------------------|
| `schedule_page`       | **New appointment** from the schedule page (no patient context) | `schedule` or `followup` | neither (`start` only) |
| `patient_chart`       | **New appointment** from a patient's chart                      | `schedule` or `followup` | neither (`start` only) |
| `calendar`            | Drag-and-drop on the calendar to create a slot                  | `schedule`               | `end`                  |
| `calendar_reschedule` | Rescheduling an existing appointment from the calendar          | `reschedule`             | `duration`             |
| `note_reschedule`     | Rescheduling an appointment from within a note                  | `reschedule`             | `duration`             |

Which entities accompany each origin is shown in the [Entity Objects](#entity-objects) table's "Available From" column above — for example, `patient_chart` and the reschedule flows include a `patient`, while `schedule_page` and `calendar` do not.

### Manifest Configuration

Register your Scheduling Application under the `handlers` section of your
`CANVAS_MANIFEST.json`. There is **no** `scope` or `icon` — inheriting from
`SchedulingApplication` is what tells Canvas to use it as the scheduling-modal
override.

```json
{
  "components": {
    "handlers": [
      {
        "class": "my_plugin.apps.scheduler:CustomScheduler",
        "description": "Custom appointment scheduling that overrides the built-in modal."
      }
    ]
  }
}
```

When installed, this application replaces the built-in scheduling modal. If no scheduling application is installed, the existing built-in modal continues to work unchanged.
