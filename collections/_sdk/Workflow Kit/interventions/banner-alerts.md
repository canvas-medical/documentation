---
title: "Banner Alerts"
---
The workflow kit also allows the user to place Banner's on the canvas UI. 

You can customize two things with banners: Placement and Intent

## AlertPlacement

`from canvas_workflow_kit.constants import AlertPlacement`

The placement of an alert on the Canvas Interface.
[block:parameters]
{
  "data": {
    "0-0": "AlertPlacement.ALERT_PLACEMENT_CHART",
    "1-0": "AlertPlacement.ALERT_PLACEMENT_TIMELINE",
    "2-0": "AlertPlacement.ALERT_PLACEMENT_APPOINTMENT_CARD",
    "3-0": "AlertPlacement.ALERT_PLACEMENT_SCHEDULING_CARD",
    "4-0": "AlertPlacement.ALERT_PLACEMENT_PROFILE",
    "0-1": "This will place the banner under the patient's name on their chart",
    "1-1": "This will place the banner on the top of the patient's timeline of notes in their chart",
    "2-1": "This will appear when you click an appointment on the calendar view",
    "4-1": "This will place the banner under the patient's name on their patient registration page",
    "3-1": "This will appear when you select a patient during the scheduling of an appointment on the calendar view."
  },
  "cols": 2,
  "rows": 5
}
[/block]
## AlertIntent

`from canvas_workflow_kit.constants import AlertIntent`

The type or severity of an alert. This will change how the Banner alert looks 


    AlertIntent.ALERT_INTENT_INFO
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/db97162-Screen_Shot_2022-08-23_at_1.30.15_PM.png",
        "Screen Shot 2022-08-23 at 1.30.15 PM.png",
        592,
        78,
        "#f1f2f3"
      ]
    }
  ]
}
[/block]
    AlertIntent.ALERT_INTENT_WARNING
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/ddecd4c-Screen_Shot_2022-08-23_at_1.30.20_PM.png",
        "Screen Shot 2022-08-23 at 1.30.20 PM.png",
        674,
        92,
        "#efeeed"
      ]
    }
  ]
}
[/block]
    AlertIntent.ALERT_INTENT_ALERT
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/ccd8805-Screen_Shot_2022-08-23_at_1.30.54_PM.png",
        "Screen Shot 2022-08-23 at 1.30.54 PM.png",
        676,
        94,
        "#f6e8e6"
      ]
    }
  ]
}
[/block]
## Example protocol walkthrough 
This protocol displays banners in several locations throughout Canvas. So if the patient is over 70 and has a certain number of contacts listed as emergency, authorized for release of information, and power of attorney. The following scenarios will be followed for patients > 70 years old
* exactly 1 contact designated as emergency, authorized for release, or power of attorney: a banner with info styling is displayed above the timeline and on appointment cards with the contact's name. 
* no contact designated as emergency, authorized for release, or power of attorney: a banner with alert styling is displayed in the profile and chart, as well as in appointment and scheduling cards (with links to take the user right to patient registration to update the patient's contacts). 
* more than one contact designated as emergency, authorized for release, or power of attorney: a banner with warning styling is displayed in the profile indicating the number of contacts, and asking the user to reduce to just 1 contact

Here is the code:
**[Banner Alerts for Contacts Code ](https://github.com/canvas-medical/open-source-sdk/blob/main/canvas_workflow_helpers/protocols/banner_alerts_for_contacts.py)**

After uploading, go to any patient that is >= 70 years old, or find any test patient and update their birth date to make them older than 70. If the patient has no contacts you should see the following banners on the chart (using    AlertPlacement.ALERT_PLACEMENT_CHART) :
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/ce302d8-Screen_Shot_2021-12-27_at_2.18.27_PM.png",
        "Screen Shot 2021-12-27 at 2.18.27 PM.png",
        806,
        746,
        "#f6f2f2"
      ]
    }
  ]
}
[/block]
And the same ones in the profile (using AlertPlacement.ALERT_PLACEMENT_PROFILE):
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/e6d0374-Screen_Shot_2021-12-27_at_2.18.53_PM.png",
        "Screen Shot 2021-12-27 at 2.18.53 PM.png",
        1672,
        662,
        "#faf8f8"
      ]
    }
  ]
}
[/block]
If you go to the schedule and book an appointment for this patient, you should see the same alerts in the scheduling card (using AlertPlacement.ALERT_PLACEMENT_SCHEDULING_CARD), but with hover styling. Try clicking on the banner and it should take you to the patient's registration in another tab. 
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/a6d5052-Screen_Shot_2021-12-27_at_2.21.25_PM.png",
        "Screen Shot 2021-12-27 at 2.21.25 PM.png",
        1220,
        720,
        "#d9d6d6"
      ]
    }
  ]
}
[/block]
After booking the appointment, when you click on the appointment slot on the schedule you should see the same alerts, also with clickable links (using AlertPlacement.ALERT_PLACEMENT_APPOINTMENT_CARD). 
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/f49c133-Screen_Shot_2021-12-27_at_2.22.35_PM.png",
        "Screen Shot 2021-12-27 at 2.22.35 PM.png",
        1096,
        1172,
        "#f1efee"
      ]
    }
  ]
}
[/block]
Now if you add contact(s) to the patient's profile and check on `Contact in case of emergency` and `Authorized for release of information` each exactly 1 time throughout the contact list, the alert banners should go away, and there should be just be info banners displayed in the appointment cards on the schedule and above the timeline like so:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/22bffa1-Screen_Shot_2021-12-27_at_2.28.12_PM.png",
        "Screen Shot 2021-12-27 at 2.28.12 PM.png",
        1894,
        484,
        "#e9ecef"
      ]
    }
  ]
}
[/block]
If you check one of those options on for more than 1 contact, you should see a warning banner in the profile related to the number of contacts exceeding 1. 
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/d3caa1e-Screen_Shot_2021-12-27_at_2.30.38_PM.png",
        "Screen Shot 2021-12-27 at 2.30.38 PM.png",
        1664,
        636,
        "#fafafa"
      ]
    }
  ]
}
[/block]
This example is intended to show all the different placements that banners can be displayed, as well as the different intents they can use. Take note of the `placement` and `intent` parameters passed to the recommendation for each scenario to ensure they make sense, and then apply them to your own use case!