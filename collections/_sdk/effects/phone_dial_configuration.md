---
title: "Phone Dial Configuration Effect"
slug: "effect-phone-dial-configuration"
excerpt: "Make the phone numbers in a patient chart clickable so a plugin can dial them through the device or handle the click itself."
hidden: false
---

The `PhoneDialConfiguration` effect turns the phone numbers in a patient chart into clickable links — the click-to-dial affordance. It lets a user click to dial a number, or hand it to a softphone, directly from the chart. Return it in response to the `PHONE_DIAL__GET_CONFIGURATION` event, which Canvas fires as a chart loads its phone numbers.

Import the effect and its enums from the submodule — they are not re-exported from `canvas_sdk.effects`:

```python?partial=True
from canvas_sdk.effects.phone_dial_configuration import (
    PhoneDialClickHandling,
    PhoneDialConfiguration,
    PhoneDialSection,
)
```

---

## How it works

As a patient chart loads phone numbers, Canvas fires `PHONE_DIAL__GET_CONFIGURATION`. A handler subscribed to the event returns one or more `PhoneDialConfiguration` effects, each naming the chart sections it makes clickable and how a click on those sections is handled. If no plugin returns a configuration, every number renders as plain text.

A single effect carries one `click_handling` mode that applies to every section it lists. To handle sections differently — some dialed by the device, some by your plugin — return one effect per handling mode.

The two handling modes differ in what a click does:

- `DEVICE` — the click opens a `tel:` link that the device's phone app handles. Your plugin does nothing beyond declaring the section.
- `PLUGIN` — nothing opens locally. The click fires `PHONE_NUMBER_CLICKED`, and your handler decides what to do with it.

`PHONE_NUMBER_CLICKED` fires under either handling mode, so a plugin can observe clicks even on device-dialed sections.

Two categories of numbers are never affected by this configuration: sections you do not list render as plain text, and fax numbers are always plain text regardless of configuration.

When more than one plugin responds, Canvas merges their configurations:

- A section is clickable if any plugin lists it.
- A section is plugin-driven if any plugin asks for `PLUGIN` on it.
- Among the remaining configurations, the first one that names a `dial_label` supplies the label.

### Event payload

| Property          | Value        | Description                                                             |
|-------------------|--------------|-------------------------------------------------------------------------|
| `event.target.id` | `str` (UUID) | The id of the patient whose chart is loading phone numbers.             |
| `event.actor`     | user         | The logged-in user viewing the chart, when available.                   |
| `event.context`   | `{}`         | Empty — no additional context is provided.                              |

### Attributes

| Field                | Type                     | Default  | Description                                                                                                                                                              |
|----------------------|--------------------------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `clickable_sections` | `list[PhoneDialSection]` | Required | The chart sections whose numbers become clickable. Provide at least one — an empty list is rejected.                                                                     |
| `click_handling`     | `PhoneDialClickHandling` | `DEVICE` | How a click on the listed sections is handled.                                                                                                                           |
| `dial_label`         | `str \| None`            | `None`   | A display affordance only. When `dial_label` is set, the section shows the number plus a "Dial number with `<label>`" button. When it isn't, the number itself is the link. Where the call actually goes is still the click handler's decision, not the configuration's. |

`PhoneDialSection` — the chart sections you can make clickable:

| Member                                | Value                  |
|---------------------------------------|------------------------|
| `PhoneDialSection.PATIENT`            | `"patient"`            |
| `PhoneDialSection.CONTACT`            | `"contact"`            |
| `PhoneDialSection.EXTERNAL_CARE_TEAM` | `"external_care_team"` |

`PhoneDialClickHandling` — how a click is handled:

| Member                          | Value      |
|---------------------------------|------------|
| `PhoneDialClickHandling.DEVICE` | `"device"` |
| `PhoneDialClickHandling.PLUGIN` | `"plugin"` |

### Example

This handler makes three sections clickable with different handling: contact numbers go to your plugin behind a "Dial number with Zoom" button, patient numbers go to your plugin as a plain link, and external-care-team numbers are dialed by the device.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.phone_dial_configuration import (
    PhoneDialClickHandling,
    PhoneDialConfiguration,
    PhoneDialSection,
)
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler


class ConfigurePhoneDialing(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PHONE_DIAL__GET_CONFIGURATION)

    def compute(self) -> list[Effect]:
        return [
            PhoneDialConfiguration(
                clickable_sections=[PhoneDialSection.CONTACT],
                click_handling=PhoneDialClickHandling.PLUGIN,
                dial_label="Zoom",
            ).apply(),
            PhoneDialConfiguration(
                clickable_sections=[PhoneDialSection.PATIENT],
                click_handling=PhoneDialClickHandling.PLUGIN,
            ).apply(),
            PhoneDialConfiguration(
                clickable_sections=[PhoneDialSection.EXTERNAL_CARE_TEAM],
                click_handling=PhoneDialClickHandling.DEVICE,
            ).apply(),
        ]
```

### Dial a plugin-handled section

A `PLUGIN` section does not dial anything on its own — the click only fires `PHONE_NUMBER_CLICKED`. To send the number to a softphone, subscribe to that event and return a [Redirect](/sdk/effect-redirect/) effect that navigates to the softphone's dial URL. `PHONE_NUMBER_CLICKED` carries the clicking user as `event.actor`, so the redirect has a browser to navigate — see [Event Actor](/sdk/events/#event-actor). The click event's context carries the number as `phone_number` and the chart section it came from as `source`.

{% include alert.html type="warning" content="Set <code>target</code> to <code>RedirectEffect.TargetType.SAME_TAB</code> — the only usable target here. The redirect arrives over a subscription rather than inside the click, so a <code>NEW_TAB</code> target would be treated as an unrequested popup and blocked." %}

{% include alert.html type="warning" content="The dial URL must be listed in the plugin's <code>REDIRECT_ALLOWLIST_EXTERNAL</code> secret. An unset allowlist denies everything. An entry needs both a scheme and a host, so authority-style URIs work (<code>zoomus://</code>, <code>msteams://</code>, <code>rcmobile://</code>, <code>https://</code>) but scheme-only URIs are rejected (<code>sip:</code>, <code>callto:</code>, <code>skype:</code>, <code>sms:</code>). A <code>tel:</code> link is unaffected because <code>DEVICE</code> handling opens it natively rather than through a redirect." %}

{% include alert.html type="warning" content="Compose the dial URL with an f-string, not <code>str.format</code>. The RestrictedPython sandbox blocks <code>str.format</code> and <code>format_map</code> at call time, so a <code>str.format</code> version passes <code>canvas validate</code> and unit tests but fails on the first real click." %}

This handler reads the base of your softphone's dial URL from a plugin secret named `ZOOM_DIAL_URL_BASE`, rather than hard-coding it, then composes the dial URL with an f-string. Set that secret to the value from your Zoom Phone account.

```python
from urllib.parse import quote

from canvas_sdk.effects import Effect
from canvas_sdk.effects.redirect import RedirectEffect
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler


class DialClickedNumber(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PHONE_NUMBER_CLICKED)

    def compute(self) -> list[Effect]:
        zoom_dial_url_base = self.secrets["ZOOM_DIAL_URL_BASE"]
        phone_number = self.event.context["phone_number"]
        # source names the chart section the click came from, e.g. "contact".
        source = self.event.context["source"]
        return [
            RedirectEffect(
                url=f"{zoom_dial_url_base}?number={quote(phone_number)}",
                target=RedirectEffect.TargetType.SAME_TAB,
            ).apply()
        ]
```

Declare both keys under `variables` in your plugin's `CANVAS_MANIFEST.json` so an admin can set them — an undeclared variable has nowhere to receive a value, so the secret read and the redirect both fail silently:

```json
{
  "variables": [
    { "name": "REDIRECT_ALLOWLIST_EXTERNAL" },
    { "name": "ZOOM_DIAL_URL_BASE" }
  ]
}
```

Add `zoomus://` (or your softphone's scheme and host) to `REDIRECT_ALLOWLIST_EXTERNAL` so the redirect is permitted. See [Redirect](/sdk/effect-redirect/#security--allowlist) for how the allowlist is declared and set.
