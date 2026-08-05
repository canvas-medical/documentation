---
title: "Provider Menu Configuration"
slug: "effect-provider-menu-configuration"
excerpt: "Control which native items appear in the provider (hamburger) menu via an allow-list."
hidden: false
---

The `ProviderMenuConfiguration` effect controls which native items render in the provider (hamburger) navigation menu, using an allow-list. A handler returns it in response to the `GET_PROVIDER_MENU_CONFIGURATION` event. The list *replaces* the default set: every item you want visible must be listed, and anything omitted is hidden. An empty list hides all native items.

## Basic usage

```python
from canvas_sdk.effects.provider_menu_configuration import ProviderMenuConfiguration

ProviderMenuConfiguration(
    items=[
        ProviderMenuConfiguration.Items.SCHEDULE,
        ProviderMenuConfiguration.Items.PATIENTS,
    ]
).apply()
```

## Items

The nested `ProviderMenuConfiguration.Items` enum defines the native menu items you can allow:

| Value                         | Menu label                 |
|-------------------------------|----------------------------|
| `SCHEDULE`                    | Schedule                   |
| `PATIENTS`                    | Patients                   |
| `REVENUE`                     | Revenue                    |
| `POPULATIONS`                 | Populations                |
| `CAMPAIGNS`                   | Campaigns                  |
| `DATA_INTEGRATION`            | Data integration           |
| `QUESTIONNAIRE_BUILDER`       | Questionnaire Builder      |
| `SETTINGS`                    | Settings                   |
| `MULTI_FACTOR_AUTHENTICATION` | Multi-Factor Authentication |
| `CHANGELOG`                   | Changelog                  |
| `HELP_CENTER`                 | Help center                |

## Attributes

| Field   | Type          | Description                                                                                            |
|---------|---------------|--------------------------------------------------------------------------------------------------------|
| `items` | `list[Items]` | The allow-list of native menu items to display. |

## Behavior

- The allow-list replaces the default set. Items omitted from the list are hidden, and an empty list hides everything.
- It does not reorder or regroup the menu — the native order and grouping are preserved.
- It does not grant access. A user's permissions still apply: an item the user lacks permission for still appears, disabled, exactly as it would without this effect. The effect cannot bypass permissions.
- The account avatar and Sign out are always rendered and cannot be hidden.
- Plugin-provided menu items (applications with the `provider_menu_item` scope) are independent and unaffected by this effect. See [Applications](/sdk/handlers-applications/).
- Omitting `SETTINGS` hides the link to `/admin`; omitting `MULTI_FACTOR_AUTHENTICATION` hides MFA enrollment.
- Passing a non-enum value raises a `ValidationError` when `ProviderMenuConfiguration` is constructed.
- This is an allow-list, so it does not pick up new items automatically. If Canvas adds a native menu item later, add it to your list — otherwise it stays hidden in your instance.
- If no handler responds to `GET_PROVIDER_MENU_CONFIGURATION`, the full native menu renders as usual.
- Hiding the Schedule item does not stop providers landing on the schedule at login, and does not remove the Appointments panel filter. Fully removing the scheduling experience means coordinating three separate controls — see the note below.

{% include alert.html type="info" content="Hiding the Schedule menu item does not change where a provider lands on login — they still land on <code>/schedule</code>. Fully removing the scheduling experience means coordinating three separate, independent controls: <code>ProviderMenuConfiguration</code> (this effect) for the menu item, <a href='/sdk/layout-effect/#panel-configuration'>PanelConfiguration</a> for the Appointments filter in the side panel, and <a href='/sdk/default-homepage-effect/'>DefaultHomepageEffect</a> for the default landing page." %}

## Example

The handler below shows every native item except Schedule:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.provider_menu_configuration import ProviderMenuConfiguration
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler


class HideScheduleMenuItem(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.GET_PROVIDER_MENU_CONFIGURATION)

    def compute(self) -> list[Effect]:
        items = [
            item
            for item in ProviderMenuConfiguration.Items
            if item != ProviderMenuConfiguration.Items.SCHEDULE
        ]
        return [ProviderMenuConfiguration(items=items).apply()]
```
