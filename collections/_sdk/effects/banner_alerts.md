---
title: "Banner Alerts"
slug: "effect-banner-alerts"
excerpt: "Contextual information in a patient's chart."
hidden: false
---

The Canvas SDK allows you to place Banners on the Canvas UI. 

## Adding a Banner Alert

To add a banner alert, import the `AddBannerAlert` class and create an
instance of it.

| Attribute |   | Type | Description |
| --------- | - | ---- | ----------- |
| patient_id | required | String | The id of the [patient](/sdk/data-patient/) the alert should be associated with. |
| key        | required | String | An identifier that categorizes the alert. | 
| narrative  | required | String | The content of the alert. |
| placement  | required | list[[Placement](#placement)] | List of areas the alert should show. |
| intent     | optional | [Intent](#intent) | Affects the styling of the alert. |
| href       | optional | String | If given, the alert will appear as a link to this URL. |

```python
from canvas_sdk.effects.banner_alert import AddBannerAlert

banner_alert = AddBannerAlert(
    patient_id="d4c933fe8f6948f6a7d2a42a2641b13b",
    key='test-alert',
    narrative='This is only a test.',
    placement=[
        AddBannerAlert.Placement.CHART,
        AddBannerAlert.Placement.APPOINTMENT_CARD,
        AddBannerAlert.Placement.SCHEDULING_CARD,
    ],
    intent=AddBannerAlert.Intent.INFO,
    href="https://docs.canvasmedical.com",
)

banner_alert.apply()
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

Removing a banner alert is done wih the `RemoveBannerAlert` class. Create an
instance of the class, identifying the key of the alert and the patient id.
Return the Effect by calling the `.apply()` method. Both the `key` and
`patient_id` attributes are required.

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
