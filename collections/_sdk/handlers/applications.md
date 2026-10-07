---
title: "Applications"
slug: "handlers-applications"
excerpt: "Launch external content within the EHR from the app drawer."
hidden: false
---

Applications put your own tools inside Canvas, so staff and patients can use them without leaving the workflow they're in. An application can be a dashboard, a form, a third-party tool loaded in an iframe, or a full page you build in your plugin.

Applications can show up wherever they fit the work:

- In the app drawer, on a patient's chart or across Canvas
- As a tab in the patient chart, next to Chart and Profile
- In the provider menu
- In the patient portal menu, for patients
- In the [Provider Companion](/sdk/companion/)

An application opens your content when a user selects it, and it can show a [notification badge](#notification-badges) to flag what's waiting. Its [scope](#application-scopes) decides where it appears.

## Implementing an Application

To add an application, create a handler class that inherits from `Application`, then register it in your manifest.

### Methods

- **`on_open()`** (required) runs when a user opens the application. It usually returns a [`LaunchModalEffect`](/sdk/layout-effect/#modals) with a `url` to load in an iframe or `content` to render directly. Set a `title` so users can recognize the application when it's minimized. Return one `Effect` or a list of them.
- **`on_context_change()`** (optional) runs when the user moves to another page while the application is open. Return an `Effect`, a list of them, or `None` to do nothing. See [Context Change Events](#context-change-events) for when it fires and what it receives.

### Opening for the current patient

<!-- source: discussion #307 -->
When an application opens on a patient chart, `on_open()` can read the current patient from `self.context`, which looks like `{'patient': {'id': '24cfe22ecf74420fb82dc40e44ca6166'}}`. Use it to open your application for that patient:

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

### Registering the application

Your [`CANVAS_MANIFEST.json`](/sdk/canvas_manifest/#applications) must also describe the application. Reference your class in the "applications"
section of the components so your application is registered in the app drawer
on plugin installation.

This is also where you can define the title and icon that displays your
app in the app drawer. The icon will be rendered at 48px by 48px, so should be
square and simple enough to not lose detail at that size.

### Example

This application opens in the right chart pane and reloads with claim or queue details as the user moves through revenue pages:

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

Note Applications (tabs inside a note), Scheduling Applications (which replace the built-in scheduling modal), and Docked Applications (a persistent pane pinned to a window edge) are **embedded applications** — handler-based applications that render inside a specific Canvas surface rather than appearing in the app drawer. They are declared under `handlers` (not `applications`), take no `scope` or `icon`, and create no application record.

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

## Installing and updating applications

When you install or upgrade a plugin, Canvas reconciles its applications to match
`CANVAS_MANIFEST.json`. Canvas creates each application declared under
`components.applications` that is new and updates each one that already exists.
Canvas removes any registered application that the manifest no longer declares.
The removed application's entry disappears from the app drawer and from any menu
it appeared in, such as the provider menu, and its stored icon is deleted.

Reconciliation affects only the plugin being installed. Applications that belong
to other plugins are left unchanged.

An application's identity is its `class` value, the `module:ClassName` string,
and Canvas matches applications by `class` during reconciliation:

- Editing only display fields (`name`, `description`, `icon`, `scope`, and so on)
  while keeping the same `class` updates the existing application in place.
- Changing the `class` value, by editing either the module path or the class
  name, removes the old application and adds a new one rather than updating the
  existing application in place.

> **Note:** Per-application instance settings such as
> [Open on load](#opening-an-application-on-load) attach to a specific
> application. Because changing an application's `class` creates a new
> application, those settings do not carry over to the new application.

Application changes apply together with the plugin's other install or upgrade
changes, such as commands and questionnaires, as a single all-or-nothing
operation, so if an install fails, the plugin's applications are left unchanged.

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

You can display a notification badge — a small count — on an application in
these scopes:

- `global` and `patient_specific`: on the icon in the app drawer, or on the panel
  when a `patient_specific` application sets `show_in_panel`.
- `provider_menu_item`: next to the label in the provider menu.
- `portal_menu_item`: next to the label in the patient portal menu.

A badge is useful for surfacing how many items are waiting
for attention, such as unread messages or open tasks. Applications in other scopes
(`full_chart` and the Provider Companion scopes) do not display badges.

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

For a `portal_menu_item` application, the count is computed for the patient
logged in to the portal. The event context carries that patient and no staff
member:

```python
from canvas_sdk.v1.data.task import Task, TaskStatus

def compute_notification_badge(self) -> int | None:
    patient_id = self.event.context.get("patient", {}).get("id")
    if not patient_id:
        return None
    return Task.objects.filter(patient__id=patient_id, status=TaskStatus.OPEN).count()
```

The badge event context contains:

| Key       | Description                                                          |
| --------- | -------------------------------------------------------------------- |
| `staff`   | A dict with the staff `id` and `type` (present for staff-facing apps). |
| `patient` | A dict with the patient `id` and `type` (present on a patient chart, and in the patient portal for the logged-in patient). |

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
### Application iframes and cookies

An application iframe can use cookies for its own domain only when its URL's entry
in [`url_permissions`](/sdk/canvas_manifest/#url-permissions) includes
`ALLOW_SAME_ORIGIN`. Without it, each launch behaves like an incognito session, so a
user may have to sign in to your application every time it opens.

<!-- source: discussion #571 -->
### Custom task views

To present tasks with locked fields, predefined dropdowns, or custom labels beyond what the built-in Task command offers, build an application, for example one that opens on the right side of a note. Read tasks with the [Task](/sdk/data-task/) data model, and create or update them with the [task effects](/sdk/effect-tasks/) from a [SimpleAPI](/sdk/handlers-simple-api-http/) endpoint in the same plugin. Give these tasks a label of their own so your application can find them and staff can filter them out of the general Tasks list.

<br/>
<br/>
<br/>
