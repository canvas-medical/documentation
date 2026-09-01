---
title: "Embedded Applications"
slug: "handlers-embedded-applications"
excerpt: "Handler-based applications that render inside a note, replace the scheduling modal, or dock a persistent pane to a window edge."
hidden: false
---

Embedded applications render **inside a specific Canvas surface** (a tab within
a note, the scheduling modal, or a pane pinned to a window edge) rather than as
an icon in the app drawer. They
are ordinary [handlers](/sdk/handlers-basehandler/): you subclass a base class,
register it under `handlers` in your `CANVAS_MANIFEST.json`, and Canvas renders
it in the appropriate surface.

There are three kinds:

| Base class            | Surface                                                  |
|-----------------------|----------------------------------------------------------|
| `NoteApplication`     | A tab within a patient's note                            |
| `SchedulingApplication` | Replaces the built-in scheduling modal at every entry point |
| `DockedApplication` | A persistent pane pinned to a window edge, always visible |

## How embedded applications work

Embedded applications are [handlers](/sdk/handlers-basehandler/). You build one
by subclassing `NoteApplication`, `SchedulingApplication`, or `DockedApplication`
and registering it under `handlers` in your `CANVAS_MANIFEST.json` — everything
else is inherited from that parent class.

Because the parent class defines the behavior, there's very little to configure:

- The **surface** comes from the class you inherit — `NoteApplication` renders as
  a tab in a note, `SchedulingApplication` replaces the scheduling modal, and
  `DockedApplication` pins a persistent pane to a window edge. You don't set a
  `scope` or an `icon`.
- Canvas renders Note and Scheduling Applications **on demand**: when a note opens
  or a scheduling action is triggered, Canvas asks which embedded application is
  installed for that surface, then renders what your handler returns. A Docked
  Application is the exception: it stays mounted at all times instead of rendering
  on demand. None of the three are persisted as drawer applications, so they don't
  appear in the app drawer or under Plugins_IO > Applications.
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

## Docked Applications

A Docked Application mounts as a persistent **docked pane** pinned to a window edge. It stays in place as the user moves between pages, including between a patient chart and global pages, rather than opening fresh each time.

### Implementing a Docked Application

To create a Docked Application, your handler class should inherit from `DockedApplication`, set the required class attributes, and implement `on_open()` returning a `LaunchModalEffect` with `target` set to `LaunchModalEffect.TargetType.DOCKED_PANE`.

| Attribute    | Description                                                                    |
|--------------|--------------------------------------------------------------------------------|
| `NAME`       | (Required) The display title for the pane                                      |
| `IDENTIFIER` | (Optional) A unique key for the application (recommended format: `plugin_name__app_name`) |
| `DOCK_EDGE`  | (Required) Which window edge to pin the pane to, given as a `DockEdge` value    |
| `DOCK_SIZE`  | (Required) The pane's initial size and the initial ceiling for the plugin's own resize requests, as a CSS length string (for example, `320px`). See [Sizing, Resizing, and Collapsing](#sizing-resizing-and-collapsing). |
| `PRIORITY`   | (Optional) An integer controlling stacking order when multiple panes share an edge — lower values sit nearer the window edge. Defaults to `0`. See [Multiple Docked Panes](#multiple-docked-panes). |

When `IDENTIFIER` is omitted, the application's identifier defaults to one derived automatically from the class's module and name. Set it explicitly in the recommended `plugin_name__app_name` format to give the application a stable, readable identifier.

`DOCK_EDGE` and `DOCK_SIZE` are both mandatory. Omitting either is a programming error that Canvas surfaces when the application runs.

`DOCK_EDGE` takes one of the following `DockEdge` values:

| Value    | Edge to pin to        |
|----------|-----------------------|
| `LEFT`   | Left edge of the window   |
| `RIGHT`  | Right edge of the window  |
| `TOP`    | Top edge of the window    |
| `BOTTOM` | Bottom edge of the window |

An edge Canvas does not recognize is rejected.

The pane has no launcher entry to open it and no host-provided or user-facing control to dismiss it. Installing the plugin makes the pane appear; removing the plugin removes it. The plugin cannot override this: a Docked Application always opens. A plugin can remove its own pane from inside its content — see [Sizing, Resizing, and Collapsing](#sizing-resizing-and-collapsing). Existing Note Applications and Scheduling Applications are unaffected and keep working unchanged.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from canvas_sdk.handlers.application import DockedApplication, DockEdge


class InfoPanel(DockedApplication):
    """Docked application that shows a persistent information pane on the right edge."""

    NAME = "Info Panel"
    IDENTIFIER = "my_plugin__info_panel"
    DOCK_EDGE = DockEdge.RIGHT
    DOCK_SIZE = "320px"

    def on_open(self) -> Effect | list[Effect]:
        """Mount the docked pane's content."""
        return LaunchModalEffect(
            target=LaunchModalEffect.TargetType.DOCKED_PANE,
            content="<html>Your pane HTML here</html>",
            title="Info Panel"
        ).apply()
```

### Pane Context and Navigation

Like other embedded applications, a Docked Application reads request context from
`self.event.context`. The pane receives context when it first mounts and again
each time the user moves to a new page.

| Key       | Description                                                                                             |
|-----------|---------------------------------------------------------------------------------------------------------|
| `url`     | The pathname of the current page                                                                        |
| `user`    | Information about the current user                                                                       |
| `patient` | A dict containing the patient's `id` (key), present only when the current page's URL carries a patient  |

A Docked Application has two entry points for this context. `on_open()` fires once,
when the pane first mounts; `on_context_change()` fires on each subsequent navigation.

`on_open()` mounts the pane's content:

```python
from canvas_sdk.effects import Effect

def on_open(self) -> Effect | list[Effect]:
    url = self.event.context.get("url")
    user = self.event.context.get("user")
    patient_id = self.event.context.get("patient", {}).get("id")
    ...
```

`on_context_change()` is how the pane stays context-aware as the user navigates.
Canvas calls it on each page change with the updated context (the new `url`, and the
`patient` derived from the new path). It defaults to a no-op, so a pane that does not
override it keeps whatever it last rendered as the user moves between pages. Override
it to return the plugin's own content or hosted URL, rebuilt from the new context —
for example, a hosted URL that carries the new patient id:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.launch_modal import LaunchModalEffect

def on_context_change(self) -> Effect | list[Effect]:
    patient_id = self.event.context.get("patient", {}).get("id", "")
    return LaunchModalEffect(
        target=LaunchModalEffect.TargetType.DOCKED_PANE,
        url=f"https://info-panel.example.com/panel?patient={patient_id}",
    ).apply()
```

The pane's document reloads only when `on_context_change()` returns a different `url`
or `content`. Returning the same `url` or `content` as before leaves the pane's current
document in place, preserving its scroll position and state. An override that returns no
effect — `None` or an empty list — leaves the pane untouched too, the same outcome as
not overriding the method. Whether to reload is your plugin's choice.

Because the pane stays mounted, it keeps its state across navigation instead of being
recreated like a modal or overlay that opens and closes.

### Multiple Docked Panes

Docked panes stack rather than being limited to one per edge. Each edge holds up to
two panes. When an edge already holds its two panes, an additional pane for that edge
is not displayed — it is ignored rather than raising an install-time error.

When more than one pane shares an edge, they are ordered by priority: the lower the
priority value, the nearer the pane sits to the window edge. Panes with equal
priority are ordered by their identifier. This mirrors the way the `PRIORITY` class
attribute orders Note Application tabs. To get a predictable order, set an explicit
`PRIORITY` on each pane, and set an explicit `IDENTIFIER` rather than relying on the
auto-derived one.

Docked panes are limited to half the viewport on each axis. The left and right edges
share the horizontal budget, and the top and bottom edges share the vertical budget,
each capped at 50% of the viewport. When the panes on an axis would exceed that
budget, they are scaled down proportionally rather than any pane being dropped.

An edge's thickness is set by its largest pane on that axis, not by the sum of its
panes.

### Sizing, Resizing, and Collapsing

`DOCK_SIZE` sets the pane's initial size — its width on the `LEFT` and `RIGHT` edges,
its height on the `TOP` and `BOTTOM` edges — and the initial ceiling for the plugin's
own resize requests. The user and the plugin resize the pane under different rules.

A user can resize a pane by dragging its edge or with the keyboard arrow keys, using
the standard splitter the pane exposes. A user resize can make the pane larger or
smaller than `DOCK_SIZE`. It is floored at 48px and capped at the axis budget
described above, but is not otherwise bound by `DOCK_SIZE`. The size a user drags to
becomes the pane's new ceiling, replacing `DOCK_SIZE`, and is stored in the browser
(`localStorage`) keyed by the pane's identifier, so it survives page reload and
navigation. Once a user has resized a pane, that persisted size takes precedence on
future loads, so changing `DOCK_SIZE` in a later plugin version does not affect panes a
user has already resized, until the stored size is cleared.

There is no host-provided control to close or minimize the pane. A plugin can,
however, resize or collapse its own pane from inside its iframe (for example, by
collapsing it to a thin rail). A plugin's own resize can shrink the pane freely, down
to a thin rail. It cannot grow the pane past the current ceiling: a request at or above
the ceiling is clamped to the ceiling rather than applied as given, so a plugin restores
the pane to its full (ceiling) size by requesting any value at or above it. A
plugin-driven resize is not bound by the 48px floor that applies to user resizing.

A pane is removed only when the plugin's own content requests it, by posting the same
`CLOSE_MODAL` message that applications use to dismiss modals. See
[Closing Modals from Applications](/sdk/layout-effect/#closing-modals-from-applications)
for the full mechanism. Once removed, nothing re-mounts the pane short of a page reload.

A docked pane cannot navigate the host application directly; navigation is issued
through a redirect effect. It does not reset the session idle-logout timer.

### Manifest Configuration

Register your Docked Application under the `handlers` section of your
`CANVAS_MANIFEST.json`. As with Note and Scheduling Applications, there is **no**
`scope` or `icon` — inheriting from `DockedApplication` is what tells Canvas to
mount it as a docked pane.

```json
{
  "components": {
    "handlers": [
      {
        "class": "my_plugin.apps.info_panel:InfoPanel",
        "description": "Fixed information pane docked to the right edge."
      }
    ]
  }
}
```
