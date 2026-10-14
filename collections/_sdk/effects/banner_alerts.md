---
title: "Banner Alerts"
slug: "effect-banner-alerts"
excerpt: "Contextual information in a patient's chart."
hidden: false
---

The Canvas SDK allows you to place Banners on the Canvas UI.

## Adding a Banner Alert

To add a banner alert, build an `AddBannerAlert` and return its `apply()` from your handler.

### Methods

#### apply() → Effect

Adds the banner alert.

- `key`, `narrative`, `placement`, and `intent` are required, along with either `patient_id` or `patient_filter`.
- `narrative` can be at most 90 characters.

### Attributes

| Attribute      | Type                          | Description                                                                                                                                        | Required |
| -------------- | ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| patient_id     | String                        | The id of the [patient](/sdk/data-patient/) the alert should be associated with.                                                                   | If `patient_filter` is not provided |
| patient_filter | dict                          | Patient queryset filters to apply the effect to multiple patients. For example, `{"active": True}` will apply to the effect to all active patients | If `patient_id` is not provided |
| key            | String                        | An identifier that categorizes the alert.                                                                                                          | Yes      |
| narrative      | String                        | The content of the alert. Maximum 90 characters.                                                                                                   | Yes      |
| placement      | list[[Placement](#placement)] | List of areas the alert should show.                                                                                                               | Yes      |
| intent         | [Intent](#intent)             | Affects the styling of the alert.                                                                                                                  | Yes      |
| href           | String                        | If given, the alert will appear as a link to this URL.                                                                                             | No       |

### Example

```python
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler

from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.effects.banner_alert import AddBannerAlert


class MyHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_UPDATED)

    def compute(self):
        banner = AddBannerAlert(
            patient_id=self.target,
            key="test-alert",
            narrative="This is only a test.",
            placement=[
                AddBannerAlert.Placement.CHART,
                AddBannerAlert.Placement.APPOINTMENT_CARD,
                AddBannerAlert.Placement.SCHEDULING_CARD,
            ],
            intent=AddBannerAlert.Intent.INFO,
            href="https://docs.canvasmedical.com",
        )

        return [banner.apply()]

```

To apply the effect to all active patients when a plugin is created or updated, include the `PLUGIN_CREATED` and/or `PLUGIN_UPDATED` events in the `RESPONDS_TO` list. Additionally, `patient_filter` can be used (instead of `patient_id`) on the `AddBannerAlert` class.

```python
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler

from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.effects.banner_alert import AddBannerAlert


class MyHandler(BaseHandler):
    RESPONDS_TO = [
        EventType.Name(EventType.PATIENT_UPDATED),
        EventType.Name(EventType.PLUGIN_CREATED),
        EventType.Name(EventType.PLUGIN_UPDATED),
    ]

    def compute(self):
        banner = AddBannerAlert(
            key="test-alert",
            narrative="This is only a test.",
            placement=[
                AddBannerAlert.Placement.CHART,
                AddBannerAlert.Placement.APPOINTMENT_CARD,
                AddBannerAlert.Placement.SCHEDULING_CARD,
            ],
            intent=AddBannerAlert.Intent.INFO,
            href="https://docs.canvasmedical.com",
        )

        if self.event.type in [EventType.PLUGIN_CREATED, EventType.PLUGIN_UPDATED]:
            banner.patient_filter = {"active": True}
        else:
            banner.patient_id = self.target

        return [banner.apply()]

```

### Placement

This determines where the banner alert appears.

#### `Placement.CHART`

This will place the banner under the patient's name on their chart

<img src="/assets/images/sdk/banner-alerts/banner_alert_placement_chart.png" width="50%">

#### `Placement.TIMELINE`

This will place the banner on the top of the patient's timeline of notes in their chart

<img src="/assets/images/sdk/banner-alerts/banner_alert_placement_timeline.png" width="90%">

#### `Placement.APPOINTMENT_CARD`

This will appear when you click an appointment on the calendar view

<img src="/assets/images/sdk/banner-alerts/banner_alert_placement_appointment_card.png" width="60%">

#### `Placement.SCHEDULING_CARD`

This will appear when you select a patient during the scheduling of an appointment on the calendar view

<img src="/assets/images/sdk/banner-alerts/banner_alert_placement_scheduling_card.png" width="60%">

#### `Placement.PROFILE`

This will place the banner under the patient's name on their patient registration page

<img src="/assets/images/sdk/banner-alerts/banner_alert_placement_profile.png" width="90%">

### Intent

The type or severity of an alert. This will change the appearance of the
banner alert.

#### `Intent.INFO`

<img src="/assets/images/sdk/banner-alerts/banner_alert_intent_info.png" width="400">

#### `Intent.WARNING`

<img src="/assets/images/sdk/banner-alerts/banner_alert_intent_warning.png" width="400">

#### `Intent.ALERT`

<img src="/assets/images/sdk/banner-alerts/banner_alert_intent_alert.png" width="400">

## Removing a Banner Alert

To remove a banner alert, build a `RemoveBannerAlert` identifying the alert's key and patient, and return its `apply()` from your handler.

### Methods

#### apply() → Effect

Removes the banner alert.

- `key` is required, along with either `patient_id` or `patient_filter`.

### Attributes

| Attribute      | Type   | Description                                                                 | Required |
| -------------- | ------ | --------------------------------------------------------------------------- | -------- |
| patient_id     | String | The id of the [patient](/sdk/data-patient/) whose alert should be removed.   | If `patient_filter` is not provided |
| patient_filter | dict   | Patient queryset filters to remove the alert from multiple patients.        | If `patient_id` is not provided |
| key            | String | The key of the alert to remove.                                             | Yes      |

### Example

```python
from canvas_sdk.effects.banner_alert import RemoveBannerAlert

banner_alert = RemoveBannerAlert(
    key='test-alert',
    patient_id="d4c933fe8f6948f6a7d2a42a2641b13b",
)

banner_alert.apply()
```

<br/>
<br/>
<br/>
