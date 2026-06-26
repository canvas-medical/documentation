---
title: "Configure Command Buttons"
slug: "effect-configure-command-buttons"
excerpt: "Control the visibility of command buttons in patient chart locations."
hidden: false
---

The `ConfigureCommandButtons` effect allows plugins to hide or disable the command buttons that appear in specific areas of the patient chart — such as the conditions section, medications section, or protocol cards.

## Locations

The `Location` enum defines which areas of the chart can be configured:

| Value                 | Area                                              |
|-----------------------|---------------------------------------------------|
| `CONDITIONS`          | Conditions chart summary section                  |
| `MEDICATIONS`         | Medications chart summary section                 |
| `ALLERGIES`           | Allergies chart summary section                   |
| `GOALS`               | Goals chart summary section                       |
| `VITALS`              | Vitals chart summary section                      |
| `IMMUNIZATIONS`       | Immunizations chart summary section               |
| `SURGICAL_HISTORY`    | Surgical history chart summary section            |
| `FAMILY_HISTORY`      | Family history chart summary section              |
| `SOCIAL_DETERMINANTS` | Social determinants chart summary section         |
| `CARE_TEAMS`          | Care teams chart summary section                  |
| `CODING_GAPS`         | Coding gaps chart summary section                 |
| `QUALITY_PROTOCOLS`   | Quality protocol result cards                     |
| `LAB_REVIEWS`         | Lab report review result cards                    |
| `IMAGING_REVIEWS`     | Imaging report review result cards                |
| `REFERRAL_REVIEWS`    | Referral report review result cards               |
| `DOCUMENT_REVIEWS`    | Uncategorized document review result cards        |

## Visibility

Each location can be configured with one of three visibility values:

| Value | Behaviour |
|---|---|
| `VISIBLE` | Buttons are shown and interactive (default when not listed) |
| `HIDDEN` | Buttons are not rendered |
| `DISABLED` | Buttons are rendered but not interactive |

## Attributes

Each entry in `locations` is a `LocationConfig` with the following attributes:

| Attribute    | Required | Type         | Description                        |
|--------------|----------|--------------|------------------------------------|
| `location`   | yes      | `Location`   | The chart area to configure        |
| `visibility` | yes      | `Visibility` | The visibility state for that area |

| Top-level    | Required | Type                   | Description                                                              |
|--------------|----------|------------------------|--------------------------------------------------------------------------|
| `patient_id` | yes      | `str`                  | The patient key                                                          |
| `locations`  | no       | `list[LocationConfig]` | Areas to configure. Areas not listed retain their default visible state. |

## Validation

Duplicate `location` values in the `locations` list will raise a `ValidationError` when `apply()` is called.

## Example: Patient Chart Load

`PATIENT_TIMELINE__GET_CONFIGURATION` fires every time a patient chart is opened, making it a convenient hook for configuring button visibility on chart load. The example below hides all command buttons across every location:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.configure_command_buttons import ConfigureCommandButtons
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol

Location = ConfigureCommandButtons.Location
LocationConfig = ConfigureCommandButtons.LocationConfig
Visibility = ConfigureCommandButtons.Visibility


class HideButtonsOnChartLoad(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_TIMELINE__GET_CONFIGURATION)

    def compute(self) -> list[Effect]:
        return [
            ConfigureCommandButtons(
                patient_id=self.target,
                locations=[
                    LocationConfig(location=loc, visibility=Visibility.HIDDEN)
                    for loc in Location
                ],
            ).apply()
        ]
```

## Example: Note Applications

One use case is toggling chart buttons alongside a `NoteApplication`. When the application tab opens, `on_open` disables chart buttons. When the provider switches back to the note body, Canvas sends a `NOTE_TAB_CHANGE` message to the iframe, which calls a `SimpleAPI` endpoint to restore them.

### Python

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.configure_command_buttons import ConfigureCommandButtons
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.application import NoteApplication
from canvas_sdk.handlers.simple_api import SimpleAPI, StaffSessionAuthMixin, api
from canvas_sdk.templates import render_to_string

Location = ConfigureCommandButtons.Location
LocationConfig = ConfigureCommandButtons.LocationConfig
Visibility = ConfigureCommandButtons.Visibility


class MyChartingApp(NoteApplication):
    NAME = "My Charting App"
    IDENTIFIER = "my-plugin:charting-app"

    def on_open(self) -> list[Effect]:
        patient_id = self.event.context.get("patient", {}).get("id")
        return [
            LaunchModalEffect(
                target=LaunchModalEffect.TargetType.NOTE,
                content=render_to_string(
                    "templates/charting_app.html",
                    context={"identifier": self.IDENTIFIER},
                ),
                title="My Charting App",
            ).apply(),
            ConfigureCommandButtons(
                patient_id=patient_id,
                locations=[
                    LocationConfig(location=loc, visibility=Visibility.DISABLED)
                    for loc in Location
                ],
            ).apply(),
        ]


class CommandButtonsApi(StaffSessionAuthMixin, SimpleAPI):
    @api.post("/configure-buttons/disable")
    def disable(self) -> list[Response | Effect]:
        patient_id = self.request.json().get("patient_id")
        return [
            JSONResponse({"ok": True}),
            ConfigureCommandButtons(
                patient_id=patient_id,
                locations=[
                    LocationConfig(location=loc, visibility=Visibility.DISABLED)
                    for loc in Location
                ],
            ).apply(),
        ]

    @api.post("/configure-buttons/enable")
    def enable(self) -> list[Response | Effect]:
        patient_id = self.request.json().get("patient_id")
        return [
            JSONResponse({"ok": True}),
            ConfigureCommandButtons(
                patient_id=patient_id,
                locations=[
                    LocationConfig(location=loc, visibility=Visibility.VISIBLE)
                    for loc in Location
                ],
            ).apply(),
        ]
```

### Template

The iframe listens for `NOTE_TAB_CHANGE` messages from Canvas and calls the appropriate endpoint. When `tab` is `"note"` the provider has switched back to the note body; when `tab` matches the application's identifier the application tab is active.

```html
<!-- templates/charting_app.html -->
<script>
  var port;
  var myIdentifier = '{{ identifier }}';

  function post(endpoint, patientId) {
    fetch('/plugin-io/api/my_plugin/configure-buttons/' + endpoint, {
      method: 'POST',
      body: JSON.stringify({ patient_id: patientId })
    });
  }

  window.addEventListener('message', function(event) {
    if (event.data?.type === 'INIT_CHANNEL') {
      port = event.ports[0];
      port.onmessage = function(e) {
        if (e.data?.type === 'NOTE_TAB_CHANGE') {
          if (e.data.tab === 'note') post('enable', e.data.patient.id);
          else if (e.data.tab === myIdentifier) post('disable', e.data.patient.id);
        }
      };
    }
  });
</script>
```

Both `MyChartingApp` and `CommandButtonsApi` should be registered as `handlers` in your `CANVAS_MANIFEST.json`.
