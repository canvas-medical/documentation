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
| `patient` | A dict containing the patient's `id`             |
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

Reach for a docked pane when a surface needs to follow the user instead of being opened and re-opened: a telephony or messaging bar that has to survive navigation mid-call, a live worklist the user works through while moving between charts, or an ambient scribe that keeps recording as the clinician moves around a note. Because the pane stays mounted, whatever state it holds survives that navigation, whether that's a scroll position, a half-filled form, or an open connection. A modal or an overlay cannot do this, since both are torn down when the page changes.

### Implementing a Docked Application

A Docked Application is a handler that inherits from `DockedApplication`, declares the pane's
placement as class attributes, and implements `on_open()` to mount the pane's content:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from canvas_sdk.handlers.application import DockedApplication, DockEdge
from canvas_sdk.templates import render_to_string
from canvas_sdk.v1.data.task import Task, TaskStatus


class TaskDock(DockedApplication):
    """Docked application that keeps the signed-in user's open tasks on screen."""

    NAME = "My Tasks"
    IDENTIFIER = "my_plugin__task_dock"
    DOCK_EDGE = DockEdge.RIGHT
    DOCK_SIZE = "320px"

    def on_open(self) -> Effect | list[Effect]:
        """Mount the docked pane's content."""
        user_id = self.event.context.get("user", {}).get("id")
        tasks = Task.objects.filter(assignee__id=user_id, status=TaskStatus.OPEN).order_by("due")

        return LaunchModalEffect(
            target=LaunchModalEffect.TargetType.DOCKED_PANE,
            content=render_to_string("templates/task_dock.html", {"tasks": tasks}),
            title="My Tasks",
        ).apply()
```

The pane's markup lives in a Django template in your plugin rather than in a Python string, rendered by [`render_to_string`](/sdk/layout-effect/#custom-html-and-django-templates). Here that template is `templates/task_dock.html`:
{% raw %}

```html
<!DOCTYPE html>
<html>
  <head>
    <title>My Tasks</title>
  </head>
  <body>
    <h1>My Tasks</h1>
    <ul>
      {% for task in tasks %}
        <li>{{ task.title }} (due {{ task.due }})</li>
      {% endfor %}
    </ul>
  </body>
</html>
```

{% endraw %}

`on_open()` returns a [`LaunchModalEffect`](/sdk/layout-effect/#modals) with `target` set to `LaunchModalEffect.TargetType.DOCKED_PANE`. That target is what mounts the effect's rendered `content` (or a `url`) in the pane rather than in a modal. Canvas draws no chrome around a docked pane, so `title` is never displayed: it becomes the pane's accessible name for screen readers.

There is no app drawer entry that opens a docked pane and no Canvas-provided control that closes or minimizes it. For the staff who get one, the pane is simply on screen for the whole session, and which staff those are is the plugin's decision: see [Controlling who gets a pane](#controlling-who-gets-a-pane). The pane's own content can remove itself at runtime, which is how a plugin offers its own collapse or close control. See [Sizing, Resizing, and Collapsing](#sizing-resizing-and-collapsing).

#### Class attributes

| Attribute    | Required | Description                                                         |
|--------------|----------|---------------------------------------------------------------------|
| `NAME`       | Required | The display title for the pane                                      |
| `IDENTIFIER` | Optional | A unique key for the application. When omitted, the identifier defaults to one derived automatically from the class's module and name. Set it explicitly in the recommended `plugin_name__app_name` format to give the application a stable, readable identifier. |
| `DOCK_EDGE`  | Required | Which window edge to pin the pane to, given as a [`DockEdge`](#dockedge) value |
| `DOCK_SIZE`  | Required | The pane's initial size and the initial ceiling for the plugin's own resize requests, as a CSS length string (for example, `320px`). See [Sizing, Resizing, and Collapsing](#sizing-resizing-and-collapsing). |
| `PRIORITY`   | Optional | An integer controlling stacking order when multiple panes share an edge — lower values sit nearer the window edge. Defaults to `0`. See [Multiple Docked Panes](#multiple-docked-panes). |

#### DockEdge

`DockEdge` is an enum of the four window edges a pane can be pinned to.

| Name     | Value    | Edge to pin to            |
|----------|----------|---------------------------|
| `LEFT`   | `left`   | Left edge of the window   |
| `RIGHT`  | `right`  | Right edge of the window  |
| `TOP`    | `top`    | Top edge of the window    |
| `BOTTOM` | `bottom` | Bottom edge of the window |

#### Controlling who gets a pane

A docked pane is not all-or-nothing across an instance. Override `visible()` to decide,
per staff member, whether the pane exists for them at all:

```python?partial=true
def visible(self) -> bool:
    """Only dock the pane for the care coordination team."""
    staff_id = self.event.context.get("user", {}).get("id")

    return Staff.objects.filter(id=staff_id, teams__name="Care Coordination").exists()
```

Returning `False` means that user gets no pane: Canvas never calls `on_open()` for them
and sends them no context changes. `visible()` defaults to `True`, so a Docked
Application that does not override it docks for everyone.

Two things to know about when this runs. Canvas asks for docked applications once as the
EHR shell loads, so `visible()` is evaluated then and not again as the user navigates
inside the shell. A change in the answer therefore takes effect on that user's next full
page load. And the context `visible()` receives holds only `scope` and `user`, with no
`patient` or `note`, because the question being asked is which panes this session gets
rather than what is on screen. Gate on the staff member, or on anything you can look up
from them, rather than on what they are currently viewing.

Do not use `on_open()` for this. Returning no docked-pane effect from `on_open()` also
leaves the pane unmounted, but panes are mounted once per session and never retried, so
the pane stays gone for the rest of the session with no way back.

### Pane Context and Navigation

Like other embedded applications, a Docked Application reads request context from
`self.event.context`. It receives that context twice over: once when the pane first
mounts, through [`on_open()`](#on_open), and again on each navigation, through
[`on_context_change()`](#on_context_change). Both entry points get the same three keys:

| Key       | Value                       | Description                                                                                                                                                                    |
|-----------|-----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `url`     | `str`                       | The path of the Canvas page the user is on. Always one of the [pages a pane sees](#pages-a-pane-sees).                                                                          |
| `user`    | `{"id": str, "type": str}`  | The signed-in user, always present. `id` is the [Staff](/sdk/data-staff/#staff) id; `type` is the name of the person record behind the login, which is `Staff` in the EHR.     |
| `patient` | `{"id": str}`               | The patient whose chart is open. Present only on a `/patient/<patient id>` path and absent entirely elsewhere, so read it as `self.event.context.get("patient", {})`.          |

On a patient chart the whole context looks like this:

```python?partial=true
{
    "url": "/patient/b80b1cdc2e6a4aca90ccebc02e683f35",
    "user": {"id": "5eede137ecfe4124b8b773040e33be14", "type": "Staff"},
    "patient": {"id": "b80b1cdc2e6a4aca90ccebc02e683f35"},
}
```

On the schedule, where no patient is in the path, the `patient` key is simply not there:

```python?partial=true
{
    "url": "/schedule",
    "user": {"id": "5eede137ecfe4124b8b773040e33be14", "type": "Staff"},
}
```

#### `on_open()`

Fires once, when the pane mounts, and returns the effect that gives the pane its content:

```python?partial=true
def on_open(self) -> Effect | list[Effect]:
    url = self.event.context.get("url")
    user_id = self.event.context.get("user", {}).get("id")
    patient_id = self.event.context.get("patient", {}).get("id")
    ...
```

#### `on_context_change()`

Fires on each navigation after that, with the new `url` and the `patient` derived from
the new path. This is how a pane stays context-aware as the user moves around Canvas.

It defaults to a no-op, so a pane that does not override it keeps whatever it last
rendered. Override it to return the plugin's own content or hosted URL, rebuilt from the
new context, such as a hosted URL that carries the new patient id:

```python?partial=true
def on_context_change(self) -> Effect | list[Effect]:
    patient_id = self.event.context.get("patient", {}).get("id", "")
    return LaunchModalEffect(
        target=LaunchModalEffect.TargetType.DOCKED_PANE,
        url=f"https://task-dock.example.com/panel?patient={patient_id}",
    ).apply()
```

The pane's document reloads only when `on_context_change()` returns a different `url` or
`content`. Returning the same `url` or `content` as before leaves the pane's current
document in place, preserving its scroll position and state, and so does returning no
effect at all (`None` or an empty list). Whether to reload is your plugin's choice.

#### Pages a pane sees

`url` is the path of the Canvas page around the pane, never the URL loaded inside the
pane's own iframe. A pane navigating its own document is invisible to Canvas and produces
no context change, and neither does a change to the page URL's hash.

Docked panes mount in the EHR shell, so `url` is always one of the paths that shell
routes. Some of these pages are gated by permission or by a feature flag, so which of
them a given user reaches will vary:

| Path                      | Page                                                                    |
|---------------------------|-------------------------------------------------------------------------|
| `/patient/<patient id>`   | A patient's chart, including its sub-paths. The only path that carries a `patient` in context |
| `/schedule`               | The schedule calendar                                                   |
| `/patients`               | The patient list                                                        |
| `/panel`                  | A patient panel                                                         |
| `/populations`            | Population health                                                       |
| `/campaigns`              | Campaigns                                                               |
| `/revenue`                | Revenue and claims                                                      |
| `/data-integration`       | Data integration                                                        |
| `/questionnaire-builder`  | The questionnaire builder                                               |
| `/application`            | A full-page plugin application                                          |
| `/403`                    | Permission denied                                                       |

Everything else on the domain sits outside that shell, including `/admin`, `/login`,
`/app/...`, `/companion/...` and `/plugin-io/...`. Moving to one of those is a full page
load rather than a navigation: the pane is not on screen while the user is there, and
returning to the EHR mounts it again from scratch, so `on_open()` fires rather than
`on_context_change()`.

The patient portal is outside the shell as well, so a docked pane cannot appear there. A
Docked Application is a staff-facing surface only.

Because the pane stays mounted across every navigation inside the shell, it keeps its
state there instead of being recreated like a modal or overlay that opens and closes.

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

Panes cannot crowd Canvas out of its own window. The left and right panes together
take up at most half the window's width, and the top and bottom panes together at most
half its height. If the panes on one of those pairs would exceed their half, all of
them are scaled down in proportion rather than any one being dropped.

Where two panes share a single edge, that edge is only as thick as the larger of them,
not as thick as both added together.

### Sizing, Resizing, and Collapsing

<p>
  <object alt="A pane docked to the right edge at DOCK_SIZE, and the same pane collapsed by its plugin to a thin rail" type="image/svg+xml" data="/assets/images/sdk/handlers/docked-pane-sizing.svg" style="width: 100%; max-width: 720px;"></object>
</p>

`DOCK_SIZE` sets the pane's initial size — its width on the `LEFT` and `RIGHT` edges,
its height on the `TOP` and `BOTTOM` edges — and the initial ceiling for the plugin's
own resize requests. The user and the plugin resize the pane under different rules.

A user can resize a pane by dragging its edge or with the keyboard arrow keys, using
the standard splitter the pane exposes. A user resize can make the pane larger or
smaller than `DOCK_SIZE`: it stops at 48px, and at the half-the-window limit described
above, but is not otherwise bound by `DOCK_SIZE`. The size a user drags to becomes the
pane's new ceiling, replacing `DOCK_SIZE`, and is stored in the browser
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
        "class": "my_plugin.apps.task_dock:TaskDock",
        "description": "Open task list docked to the right edge."
      }
    ]
  }
}
```
