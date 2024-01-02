---
title: "Banner Alerts"
---
The workflow kit allows the user to place Banners on the canvas UI. 

You can customize two things with banners: Placement and Intent

## AlertPlacement

`from canvas_workflow_kit.constants import AlertPlacement`

The placement of an alert on the Canvas Interface.

| Alert Placement                                | Description                                                                                       |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| AlertPlacement.ALERT_PLACEMENT_CHART           | This will place the banner under the patient's name on their chart                                 |
| AlertPlacement.ALERT_PLACEMENT_TIMELINE        | This will place the banner on the top of the patient's timeline of notes in their chart           |
| AlertPlacement.ALERT_PLACEMENT_APPOINTMENT_CARD | This will appear when you click an appointment on the calendar view                                 |
| AlertPlacement.ALERT_PLACEMENT_SCHEDULING_CARD  | This will appear when you select a patient during the scheduling of an appointment on the calendar view |
| AlertPlacement.ALERT_PLACEMENT_PROFILE         | This will place the banner under the patient's name on their patient registration page           |


## AlertIntent

`from canvas_workflow_kit.constants import AlertIntent`

The type or severity of an alert. This will change how the Banner alert looks 



| ALERT_INTENT_INFO          | <img src="https://files.readme.io/db97162-Screen_Shot_2022-08-23_at_1.30.15_PM.png" width="400">      |
| ALERT_INTENT_WARNING       | <img src="https://files.readme.io/ddecd4c-Screen_Shot_2022-08-23_at_1.30.20_PM.png" width="400">      |
| ALERT_INTENT_ALERT         | <img src="https://files.readme.io/ccd8805-Screen_Shot_2022-08-23_at_1.30.54_PM.png" width="400">      |


## Example 
This protocol displays banners in several locations throughout Canvas. So if the patient is over 70 and has a certain number of contacts listed as emergency, authorized for release of information, and power of attorney. The following scenarios will be followed for patients > 70 years old
* exactly 1 contact designated as emergency, authorized for release, or power of attorney: a banner with info styling is displayed above the timeline and on appointment cards with the contact's name. 
* no contact designated as emergency, authorized for release, or power of attorney: a banner with alert styling is displayed in the profile and chart, as well as in appointment and scheduling cards (with links to take the user right to patient registration to update the patient's contacts). 
* more than one contact designated as emergency, authorized for release, or power of attorney: a banner with warning styling is displayed in the profile indicating the number of contacts, and asking the user to reduce to just 1 contact

Here is the [code](https://github.com/canvas-medical/open-source-sdk/blob/main/canvas_workflow_helpers/protocols/banner_alerts_for_contacts.py):

```python
import math

from canvas_workflow_kit import events
from canvas_workflow_kit.constants import CHANGE_TYPE
from canvas_workflow_kit.intervention import BannerAlertIntervention
from canvas_workflow_kit.protocol import STATUS_DUE, ClinicalQualityMeasure, ProtocolResult


class BannerAlertContacts(ClinicalQualityMeasure):
    """
    A protocol that displays banner alerts for patients over the age of 70
    without a single emergency contact, a single contact authorized for release of information,
    and a single Power of Attorney contact
    """

    class Meta:

        title = 'Banner Alert Contacts'

        version = 'v1.0.0'

        description = 'Reminders about patients over the age of 70'

        information = 'https://canvasmedical.com/'

        identifiers = ['BannerAlertContacts']

        types = ['Alerts']

        responds_to_event_types = [
            events.HEALTH_MAINTENANCE,
        ]
        compute_on_change_types = [CHANGE_TYPE.PATIENT]

        authors = ['Canvas Medical']

        references = ['Canvas Medical']

        funding_source = ''

    rounded_patient_age = None

    def get_contact_display(self, contact):
        display = contact['name']
        relationship = contact['relationship']
        if relationship and relationship != '':
            display += f' ({relationship})'
        return display

    def in_denominator(self):
        """
        Patients over the age of 70.

        """
        rounded_patient_age = math.floor(self.patient.age)
        self.rounded_patient_age = rounded_patient_age
        return rounded_patient_age >= 70

    def has_contact_category(self, categories, category):
        return next((cat for cat in categories if cat['category'] == category),
                    None) is not None

    def compute_results(self):
        result = ProtocolResult()
        if self.in_denominator():
            result.status = STATUS_DUE
            result.due_in = -1

            emergency_contacts = []
            release_of_info_contacts = []
            poa_contacts = []
            for contact in self.patient.patient.get('contacts', []):
                categories = contact.get('categories', [])
                if self.has_contact_category(categories, 'EMC'):
                    emergency_contacts.append(contact)
                if self.has_contact_category(categories, 'ARI'):
                    release_of_info_contacts.append(contact)
                if self.has_contact_category(categories, 'POA'):
                    poa_contacts.append(contact)

            num_emergency_contacts = len(emergency_contacts)
            num_release_contacts = len(release_of_info_contacts)
            num_poa_contacts = len(poa_contacts)

            if num_emergency_contacts == 1:
                emergency_contact_display = self.get_contact_display(
                    emergency_contacts[0])
                result.recommendations.append(
                    BannerAlertIntervention(
                        narrative=(
                            f'{self.patient.first_name} has 1 '
                            f'emergency contact: {emergency_contact_display}'),
                        placement=['timeline', 'appointment_card'],
                        intent='info'))
            if num_release_contacts == 1:
                release_contact_display = self.get_contact_display(
                    release_of_info_contacts[0])
                result.recommendations.append(
                    BannerAlertIntervention(narrative=(
                        f'{self.patient.first_name} has 1 '
                        f'contact authorized for release of info: {release_contact_display}'
                    ),
                                            placement=[
                                                'timeline', 'appointment_card'
                                            ],
                                            intent='info'))
            if num_poa_contacts == 1:
                poa_contact_display = self.get_contact_display(poa_contacts[0])
                result.recommendations.append(
                    BannerAlertIntervention(narrative=(
                        f'{self.patient.first_name} has 1 '
                        f'contact with Power of Attorney: {poa_contact_display}'
                    ),
                                            placement=[
                                                'timeline', 'appointment_card'
                                            ],
                                            intent='info'))

            if num_emergency_contacts > 1:
                result.recommendations.append(
                    BannerAlertIntervention(narrative=(
                        f'{self.patient.first_name} has {num_emergency_contacts} '
                        'emergency contacts listed. Please reduce to 1.'),
                                            placement=['profile'],
                                            intent='warning'))
            if num_release_contacts > 1:
                result.recommendations.append(
                    BannerAlertIntervention(narrative=(
                        f'{self.patient.first_name} has {num_release_contacts} '
                        'contacts authorized for release of info. Please reduce to 1.'
                    ),
                                            placement=['profile'],
                                            intent='warning'))
            if num_poa_contacts > 1:
                result.recommendations.append(
                    BannerAlertIntervention(narrative=(
                        f'{self.patient.first_name} has {num_poa_contacts} '
                        'contacts with Power of Attorney. Please reduce to 1.'
                    ),
                                            placement=['profile'],
                                            intent='warning'))

            if num_emergency_contacts == 0:
                result.recommendations.append(
                    BannerAlertIntervention(
                        narrative=
                        (f'{self.patient.first_name} is {self.rounded_patient_age} '
                         'and has no emergency contacts listed'),
                        placement=['appointment_card', 'scheduling_card'],
                        intent='alert',
                        href=
                        f'http://{self.settings.INSTANCE_NAME}.canvasmedical.com/patient/{self.patient.patient_key}/edit#'
                    ))
                result.recommendations.append(
                    BannerAlertIntervention(narrative=(
                        f'{self.patient.first_name} is {self.rounded_patient_age} '
                        'and has no emergency contacts listed'),
                                            placement=['profile', 'chart'],
                                            intent='alert'))
            if num_release_contacts == 0:
                result.recommendations.append(
                    BannerAlertIntervention(
                        narrative=
                        (f'{self.patient.first_name} is {self.rounded_patient_age} '
                         'and has no contacts authorized for release of info'),
                        placement=['appointment_card', 'scheduling_card'],
                        intent='alert',
                        href=
                        f'http://{self.settings.INSTANCE_NAME}.canvasmedical.com/patient/{self.patient.patient_key}/edit#'
                    ))
                result.recommendations.append(
                    BannerAlertIntervention(narrative=(
                        f'{self.patient.first_name} is {self.rounded_patient_age} '
                        'and has no contacts authorized for release of info'),
                                            placement=['profile', 'chart'],
                                            intent='alert'))
            if num_poa_contacts == 0:
                result.recommendations.append(
                    BannerAlertIntervention(
                        narrative=
                        (f'{self.patient.first_name} is {self.rounded_patient_age} '
                         'and has no contacts with Power of Attorney'),
                        placement=['appointment_card', 'scheduling_card'],
                        intent='alert',
                        href=
                        f'http://{self.settings.INSTANCE_NAME}.canvasmedical.com/patient/{self.patient.patient_key}/edit#'
                    ))
                result.recommendations.append(
                    BannerAlertIntervention(narrative=(
                        f'{self.patient.first_name} is {self.rounded_patient_age} '
                        'and has no contacts with Power of Attorney'),
                                            placement=['profile', 'chart'],
                                            intent='alert'))
        return result
```
<br>
After uploading, go to any patient that is >= 70 years old, or find any test patient and update their birth date to make them older than 70. If the patient has no contacts you should see the following banners on the chart (using    AlertPlacement.ALERT_PLACEMENT_CHART) :

<img src="https://files.readme.io/ce302d8-Screen_Shot_2021-12-27_at_2.18.27_PM.png" width="60%">

And the same ones in the profile (using AlertPlacement.ALERT_PLACEMENT_PROFILE):

<img src="https://files.readme.io/e6d0374-Screen_Shot_2021-12-27_at_2.18.53_PM.png" width="60%">

If you go to the schedule and book an appointment for this patient, you should see the same alerts in the scheduling card (using AlertPlacement.ALERT_PLACEMENT_SCHEDULING_CARD), but with hover styling. Try clicking on the banner, and it should take you to the patient's registration in another tab.

<img src="https://files.readme.io/a6d5052-Screen_Shot_2021-12-27_at_2.21.25_PM.png" width="60%">

After booking the appointment, when you click on the appointment slot on the schedule, you should see the same alerts, also with clickable links (using AlertPlacement.ALERT_PLACEMENT_APPOINTMENT_CARD).

<img src="https://files.readme.io/f49c133-Screen_Shot_2021-12-27_at_2.22.35_PM.png" width="60%">

Now if you add contact(s) to the patient's profile and check on `Contact in case of emergency` and `Authorized for release of information` each exactly 1 time throughout the contact list, the alert banners should go away, and there should be just be info banners displayed in the appointment cards on the schedule and above the timeline like so:

<img src="https://files.readme.io/22bffa1-Screen_Shot_2021-12-27_at_2.28.12_PM.png" width="60%">

If you check one of those options on for more than 1 contact, you should see a warning banner in the profile related to the number of contacts exceeding 1.

<img src="https://files.readme.io/d3caa1e-Screen_Shot_2021-12-27_at_2.30.38_PM.png" width="60%">

This example is intended to show all the different placements that banners can be displayed, as well as the different intents they can use. Take note of the `placement` and `intent` parameters passed to the recommendation for each scenario to ensure they make sense, and then apply them to your own use case!

