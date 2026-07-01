---
title: "Applications"
slug: "handlers-applications"
excerpt: "Launch external content within the EHR from the app drawer."
hidden: false
---

Applications are accessible in the app drawer and launch your content when
clicked. Applications can be patient specific, or global.

## Implementing an Application

To add an application, your handler class should inherit from the
`Application` class.

Your class must implement the `on_open()` method. In most cases, you will
return a `LaunchModalEffect`, with either a URL you wish to iframe into the
Canvas UI or HTML to be rendered in that iframe directly, make sure to set a `title` so users can easily recognize the application when it's minimized. You can return a single `Effect` or a list of `Effect`s from the `on_open()` method.

You can also optionally implement the `on_context_change()` method to handle
context changes within the application. This method is automatically triggered when
users navigate to different URLs within Canvas, allowing your application to react
to contextual changes with rich information about the current page.

Context change events are currently supported for revenue workflows and include:

- **URL information**: The current page URL that triggered the context change
- **Patient data**: Patient information when applicable
- **Resource-specific context**: Additional context based on the specific page:
  - `/revenue/claims/<id>` - Includes claim data with externally exposable ID
  - `/revenue/queues/<id>` - Includes queue data with database ID
  - `/revenue` - Base revenue page with no additional context

This method can return an `Effect` or list of `Effect`s to perform actions when the application's context
changes, or `None` if no action is needed. When `None` is returned, no effect will
be added to the execution queue.

Here is an example of an implemented application class:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from canvas_sdk.handlers.application import Application


class IFrameApp(Application):
    def on_open(self) -> Effect | list[Effect]:
        return LaunchModalEffect(url=f"https://www.your-iframe-app.com",
            target=LaunchModalEffect.TargetType.RIGHT_CHART_PANE, title="Your Iframe App").apply()

    def on_context_change(self) -> Effect | list[Effect] | None:
        # Access the current URL that triggered the context change
        current_url = self.event.context.get("url", "")

        # Handle claim-specific context
        if claim := self.event.context.get("claim"):
            claim_id = claim["id"]
            return LaunchModalEffect(
                url=f"https://www.your-iframe-app.com?claim_id={claim_id}&source_url={current_url}",
                target=LaunchModalEffect.TargetType.RIGHT_CHART_PANE,
                title=f"Your Iframe App - Claim {claim_id}"
            ).apply()

        # Handle queue-specific context
        if queue := self.event.context.get("claim_queue"):
            queue_id = queue["dbid"]
            return LaunchModalEffect(
                url=f"https://www.your-iframe-app.com?queue_id={queue_id}&source_url={current_url}",
                target=LaunchModalEffect.TargetType.RIGHT_CHART_PANE,
                title=f"Your Iframe App - Queue {queue_id}"
            ).apply()

        # Handle general revenue page context
        if current_url.startswith("/revenue"):
            return LaunchModalEffect(
                url=f"https://www.your-iframe-app.com?page=revenue&source_url={current_url}",
                target=LaunchModalEffect.TargetType.RIGHT_CHART_PANE,
                title="Your Iframe App - Revenue"
            ).apply()

        # Return None when no relevant context - this will result in an empty effect list
        return None
```

## Context Change Events

Context change events are automatically triggered when users navigate between different URLs within Canvas. This feature allows your applications to react dynamically to the user's current context, providing relevant information and functionality based on where they are in the system.

### Event Triggers

Context change events are currently supported for revenue workflows and are triggered when:

- A user navigates to a different URL within Canvas
- The application is already open and running
- The new URL is within the `/revenue` namespace

### Context Data Structure

When a context change event occurs, your `on_context_change()` method receives contextual information through `self.event.context`:

```python
{
    "url": "/revenue/claims/123",           # Current URL that triggered the event
    "patient": {"id": "patient_key"},       # Patient information (when applicable)
    "user": {...},                          # User information
    "claim": {"id": "external_claim_id"},   # Claim context (for /revenue/claims/<id>)
    "claim_queue": {"dbid": "queue_id"}     # Queue context (for /revenue/queues/<id>)
}
```

### Supported URL Patterns

| URL Pattern            | Context Provided                            | Description                    |
| ---------------------- | ------------------------------------------- | ------------------------------ |
| `/revenue`             | Base context only                           | General revenue page           |
| `/revenue/claims/<id>` | `claim` object with externally exposable ID | Specific claim details page    |
| `/revenue/queues/<id>` | `claim_queue` object with database ID       | Specific queue management page |

### Best Practices

1. **Always check for context existence**: Use safe dictionary access patterns to avoid KeyErrors
2. **Handle multiple context types**: Your application may receive different types of context based on the URL
3. **Return None appropriately**: When no relevant action is needed, return None to avoid unnecessary effects

### Advanced Example

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from canvas_sdk.handlers.application import Application


class AdvancedRevenueApp(Application):
    def on_open(self) -> Effect | list[Effect]:
        return LaunchModalEffect(
            url="https://www.your-app.com/dashboard",
            target=LaunchModalEffect.TargetType.RIGHT_CHART_PANE,
            title="Revenue Analytics"
        ).apply()

    def on_context_change(self) -> Effect | list[Effect] | None:
        current_url = self.event.context.get("url", "")
        patient = self.event.context.get("patient", {})
        user = self.event.context.get("user", {})

        # Build base parameters
        params = {
            "source_url": current_url,
            "user_id": user.get("id", ""),
            "patient_id": patient.get("id", "")
        }

        # Handle specific contexts
        if claim := self.event.context.get("claim"):
            params["claim_id"] = claim["id"]
            params["view"] = "claim_details"
            title = f"Revenue Analytics - Claim {claim['id']}"

        elif queue := self.event.context.get("claim_queue"):
            params["queue_id"] = queue["dbid"]
            params["view"] = "queue_management"
            title = f"Revenue Analytics - Queue {queue['dbid']}"

        elif current_url.startswith("/revenue"):
            params["view"] = "revenue_overview"
            title = "Revenue Analytics - Overview"

        else:
            # No relevant context for this application
            return None

        # Build query string
        query_string = "&".join(f"{k}={v}" for k, v in params.items() if v)

        return LaunchModalEffect(
            url=f"https://www.your-app.com/revenue?{query_string}",
            target=LaunchModalEffect.TargetType.RIGHT_CHART_PANE,
            title=title
        ).apply()
```

In addition, your `CANVAS_MANIFEST.json` file must provide some information
about your application. You reference your class in the "applications"
section of the components so your application is registered in the app drawer
on plugin installation.

This is also where you can define the title and icon that displays your
app in the app drawer. The icon will be rendered at 48px by 48px, so should be
square and simple enough to not lose detail at that size.

## Application Scopes

The `scope` attribute determines where your application is visible within Canvas. The following scopes are available:

| Scope | Description |
| ----- | ----------- |
| `patient_specific` | Visible only within a patient's chart in the app drawer |
| `global` | Visible outside of patient charts in the app drawer |
| `full_chart` | Displayed as a tab in the patient chart navigation menu alongside Chart and Profile |
| `provider_menu_item` | Displayed as a menu item in the provider menu |
| `portal_menu_item` | Displayed as a menu item in the patient portal |
| `provider_companion` | Visible on the [Provider Companion](/sdk/companion/) main page (legacy, use `provider_companion_global` for new apps) |
| `provider_companion_global` | In the app launcher on the [Provider Companion](/sdk/companion/) main page |
| `provider_companion_patient_specific` | As a tab on a patient's page in the [Provider Companion](/sdk/companion/) |
| `provider_companion_note_specific` | As a tab within an opened note in the [Provider Companion](/sdk/companion/) |
| `scheduling` | Replaces the built-in scheduling modal at all entry points. See [Scheduling Applications](#scheduling-applications) |

### Full Chart Scope

Applications with the `full_chart` scope appear as navigation tabs at the top of the patient chart, alongside the default "Chart" and "Profile" tabs. This is ideal for building comprehensive patient-level views or dashboards.

```json
{
  "class": "my_plugin.apps.analytics:PatientAnalytics",
  "name": "Analytics",
  "description": "Patient analytics dashboard",
  "icon": "/assets/analytics-icon.png",
  "scope": "full_chart"
}
```

## Provider Companion Applications

Provider companion applications run in the Canvas provider companion — a mobile-optimized, provider-facing surface. They use the `Application` handler with one of three companion scopes (`provider_companion_global`, `provider_companion_patient_specific`, `provider_companion_note_specific`) declared in the manifest. The legacy `provider_companion` scope continues to work and is treated the same as `provider_companion_global`.

See [Provider Companion](/sdk/companion/) for the full guide — scope-by-scope examples, event context, code sharing across scopes, originating commands from a note, modal dismissal, and mobile UX guidance.

## Note Applications

Note Applications appear as tabs within a patient's note, allowing you to embed custom interfaces directly in the clinical documentation workflow.

### Implementing a Note Application

To create a Note Application, your handler class should inherit from `NoteApplication` and define two required class attributes:

| Attribute    | Description                                                                    |
|--------------|--------------------------------------------------------------------------------|
| `NAME`       | The display title shown on the tab (supports emojis)                           |
| `IDENTIFIER` | A unique key for the application (recommended format: `plugin_name__app_name`) |
| `PRIORITY`   | Controls tab order — lower values appear first. Defaults to `0`                |

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

Register your scheduling application in the `CANVAS_MANIFEST.json`. The application's `scope` **must** be set to `"scheduling"` — this is what tells Canvas to use it as the scheduling-modal override:

```json
{
  "components": {
    "applications": [
      {
        "class": "my_plugin.apps.scheduler:CustomScheduler",
        "name": "Custom Scheduler",
        "description": "Custom appointment scheduling",
        "scope": "scheduling"
      }
    ]
  }
}
```

> **Important:** The `scope` must be exactly `"scheduling"`. With any other value the application will not take over the scheduling flows, and the built-in modal will continue to be used.

When installed, this application replaces the built-in scheduling modal. If no scheduling application is installed, the existing built-in modal continues to work unchanged.

## Panel Display

If you want to increase your application's visibility and display it alongside
other panel buttons (instead of in the applications drawer), you can add
the `show_in_panel` attribute. If you've added more than one application
to that panel, you can set their priorities using the `panel_priority` attribute.

For security reasons you also need to specify the domains that will be loaded within the iframe, or they will not be
rendered. For more info on the format of the `url_permissions` field, check the [Additional Configuration](/sdk/layout-effect/#additional-configuration) for `LaunchModalEffect`.

Here's what your `CANVAS_MANIFEST.json` might look like:

```json
{
  "sdk_version": "0.1.4",
  "plugin_version": "0.0.1",
  "name": "my_application",
  "description": "This is a very nice application",
  "url_permissions": [
    {
      "url": "https://example.com/",
      "permissions": ["ALLOW_SAME_ORIGIN", "MICROPHONE", "SCRIPTS", "CAMERA", "CLIPBOARD_READ", "CLIPBOARD_WRITE"]
    }
  ],
  "components": {
    "handlers": [],
    "applications": [
      {
        "class": "my_application.apps.iframe:IFrameApp",
        "name": "My Application",
        "description": "Test App for patients",
        "icon": "/assets/cappuccino.png",
        "scope": "patient_specific",
        "show_in_panel": true,
        "panel_priority": 100
      }
    ],
    "commands": [],
    "content": [],
    "effects": [],
    "views": []
  },
  "variables": [],
  "tags": {},
  "references": [],
  "license": "",
  "diagram": false,
  "readme": "./README.md"
}
```

## Opening an Application on Load

You can configure an application to open **automatically**, without the user
clicking its icon, by enabling the **Open on load** setting for that application
in your instance settings.

To enable it, go to the Plugins_IO > Applications section of your instance settings
(`/admin/plugin_io/application/`), open the application you want, check
**Open on load**, and save. If you don't have access to this setting, reach out
to Canvas Support.

Behavior depends on the application's [scope](#application-scopes):

| Scope              | When it opens                                    |
|--------------------|--------------------------------------------------|
| `global`           | Automatically when the app shell first loads.    |
| `patient_specific` | Automatically when a patient chart is opened.    |

This is an instance-level setting configured per application in your instance
settings. It is **not** part of `CANVAS_MANIFEST.json`, so the value you set is
preserved when the plugin is reinstalled or updated.

{% include alert.html type="warning" content="<b>Enable Open on load for at most one application per scope.</b> There is no priority or ordering logic for this setting, and no constraint preventing multiple applications in the same scope from being flagged. If more than one application in the same scope (for example, two <code>patient_specific</code> apps) has Open on load enabled, all of them will attempt to open, resulting in unpredictable behavior. Make sure only one application per scope is set to open on load." %}

> **Note:** This is distinct from a Note Application's
> [`open_by_default()`](#opening-by-default), which controls which **tab** is
> active when a note is viewed. **Open on load** controls whether a `global` or
> `patient_specific` application opens automatically on app/chart load.

## Notification Badges

You can display a notification badge — a small count — on the icon of a `global`
or `patient_specific` application: in the app drawer, or on the panel when the
application sets `show_in_panel`. A badge is useful for surfacing how many items
are waiting for attention, such as unread messages or open tasks. Applications in
other scopes (`full_chart`, `provider_menu_item`, `portal_menu_item`, and the
Provider Companion scopes) do not display badges.

### Initial count on load

Override `compute_notification_badge()` on your `Application` handler to provide
the count shown when Canvas loads applications. Return an integer to show a badge,
or `None` (the default) to show no badge. A count of `0` shows no badge.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from canvas_sdk.handlers.application import Application
from canvas_sdk.v1.data.task import Task, TaskStatus


class InboxApp(Application):
    def on_open(self) -> Effect | list[Effect]:
        return LaunchModalEffect(
            url="https://www.your-app.com/inbox",
            title="Inbox",
        ).apply()

    def compute_notification_badge(self) -> int | None:
        """Return the badge count shown on the icon when applications load."""
        staff_id = self.event.context.get("staff", {}).get("id")
        if not staff_id:
            return None
        return Task.objects.filter(assignee__id=staff_id, status=TaskStatus.OPEN).count()
```

When the application is rendered on a patient chart (`patient_specific` scope),
the event context also carries the patient, so you can compute a count specific
to the staff member *and* the patient they are viewing:

```python
from canvas_sdk.v1.data.task import Task, TaskStatus

def compute_notification_badge(self) -> int | None:
    staff_id = self.event.context.get("staff", {}).get("id")
    patient_id = self.event.context.get("patient", {}).get("id")
    if not (staff_id and patient_id):
        return None
    return Task.objects.filter(
        assignee__id=staff_id, patient__id=patient_id, status=TaskStatus.OPEN
    ).count()
```

The badge event context contains:

| Key       | Description                                                          |
| --------- | -------------------------------------------------------------------- |
| `staff`   | A dict with the staff `id` and `type` (present for staff-facing apps). |
| `patient` | A dict with the patient `id` and `type` (present on a patient chart). |

> **Note:** Note Applications (`NoteApplication`) do not
> support notification badges.

### Live updates

To change the count after load — for example, in response to a new task or
message — emit an `ApplicationNotificationBadge` effect from any event handler.
The badge updates in real time without the user reloading the page. See the
[Application Notification Badge](/sdk/effect-application-notification-badge/)
effect for details.


<br/>
<br/>
<br/>
