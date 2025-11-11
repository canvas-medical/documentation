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

Other information you can define about your application is the `scope`
(`"patient_specific"` or `"global"`), which determines if the application is
visible only in a patient chart or outside of charts.

If you want to increase your application’s visibility and display it alongside
other panel buttons (instead of in the applications drawer), you can add
the `show_in_panel` attribute. If you’ve added more than one application
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
      "permissions": ["ALLOW_SAME_ORIGIN", "MICROPHONE", "SCRIPTS", "CAMERA"]
    }
  ],
  "components": {
    "protocols": [],
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
  "secrets": [],
  "tags": {},
  "references": [],
  "license": "",
  "diagram": false,
  "readme": "./README.md"
}
```

<br/>
<br/>
<br/>
