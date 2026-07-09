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

<!-- source: discussion #307 -->
When an application is opened on a patient chart, `on_open()` has access to the
current patient through `self.context`. The structure looks like
`{'patient': {'id': '24cfe22ecf74420fb82dc40e44ca6166'}}`, so you can launch your
application in the current patient context like this:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from canvas_sdk.handlers.application import Application


class MyApplication(Application):
    """An embeddable application that can be registered to Canvas."""

    def on_open(self) -> Effect:
        """Handle the on_open event."""
        patient_id = self.context['patient']['id']
        patient_specific_url = f"https://example.com/patient-specific-application?patient={patient_id}"

        return LaunchModalEffect(
            url=patient_specific_url,
            target=LaunchModalEffect.TargetType.DEFAULT_MODAL,
        ).apply()
```

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

## Embedded Applications

Note Applications (tabs inside a note) and Scheduling Applications (which replace the built-in scheduling modal) are **embedded applications** — handler-based applications that render inside a specific Canvas surface rather than appearing in the app drawer. They are declared under `handlers` (not `applications`), take no `scope` or `icon`, and create no application record.

See [Embedded Applications](/sdk/handlers-embedded-applications/) for the full guide.

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
> [`open_by_default()`](/sdk/handlers-embedded-applications/#opening-by-default), which controls which **tab** is
> active when a note is viewed. **Open on load** controls whether a `global` or
> `patient_specific` application opens automatically on app/chart load.

## Notification Badges

You can display a notification badge — a small count — on a `global`,
`patient_specific`, or `provider_menu_item` application: on the icon in the app
drawer or panel (`global` / `patient_specific`, the latter when the application
sets `show_in_panel`), or next to the label in the provider menu
(`provider_menu_item`). A badge is useful for surfacing how many items are waiting
for attention, such as unread messages or open tasks. Applications in other scopes
(`full_chart`, `portal_menu_item`, and the Provider Companion scopes) do not
display badges.

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


## Limitations and patterns

<!-- source: discussion #595 -->
### Third-party scripts only run inside a plugin iframe

Canvas does not provide a way to inject application-wide JavaScript (for example,
Segment or Sentry snippets) into the Canvas front end. Third-party scripts can
only run inside the iframe of a plugin's own application.

<!-- source: discussion #389 -->
### Application iframes cannot access cookies

Application iframes currently cannot access cookies, so each launch behaves like
an incognito session. This affects auth and session persistence — a user may have
to authenticate every time the iframe is launched, because the session is not
remembered between launches.

<!-- source: discussion #571 -->
### Custom Task views backed by the Task API

To present Tasks with locked fields, predefined dropdowns, or custom labels —
beyond what the built-in Task command offers — build a custom web Application
(for example one that launches on the right-hand side of a note) that reads and
writes Tasks through the [Task API](/api/task/). Give these Tasks a custom label
so you can filter for them in your application and filter them out of the general
Tasks section. This requires building and maintaining the custom web app, but
gives full control over the presentation and behavior of the Task-like objects.

<br/>
<br/>
<br/>
