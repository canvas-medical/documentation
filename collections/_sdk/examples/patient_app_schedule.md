---
title: 'patient_app_schedule'
slug: 'example-patient_app_schedule'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/patient_app_schedule' target='_blank'>View the source</a> for this plugin on GitHub." %}

patient_app_schedule
===========================

## Description

Filters the provider and location options shown to patients when booking appointments through the patient portal.

Providers: Only shows providers who are active members of the patient's care team
Locations: Only shows locations where the patient has previously had appointments

### Important Note!

The CANVAS_MANIFEST.json is used when installing your plugin. Please ensure it
gets updated if you add, remove, or rename protocols.

## CANVAS_MANIFEST.json

```json
{
  "sdk_version": "0.1.4",
  "plugin_version": "0.0.1",
  "name": "patient_app_schedule",
  "description": "protocols for filtering providers based on care team membership and locations based on appointment history",
  "components": {
    "protocols": [
      {
        "class": "patient_app_schedule.protocols.filters:Providers",
        "description": "filter providers based on care team membership",
        "data_access": {
          "event": "",
          "read": [],
          "write": []
        }
      },
      {
        "class": "patient_app_schedule.protocols.filters:Locations",
        "description": "filter locations based on appointment history",
        "data_access": {
          "event": "",
          "read": [],
          "write": []
        }
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

## protocols/

### __init__.py

This file is empty.
### filters.py

**Purpose**

This file defines two filter classes for use with a Canvas plugin, each designed to process search results for either providers or locations in the context of scheduling appointments via a patient portal. The filters use the Canvas SDK and are triggered by specific events during appointment workflows.

**Providers Class**

- Listens to the event: `PATIENT_PORTAL__APPOINTMENTS__FORM_PROVIDERS__POST_SEARCH`.
- Filters a list of appointment form "providers" to show only those that are members of the current patient's care team.
- Steps:
    - Extracts the list of available providers from the event context.
    - Retrieves the patient ID from the event's target.
    - Fetches the IDs of all providers that are actively in the patient's care team using the `CareTeamMembership` model.
    - Filters the original provider list to just those in the patient’s care team.
    - Returns a single effect with the filtered list, or all providers if an error occurs.
- Logging is used throughout to record the filtering process and any errors.

**Locations Class**

- Listens to the event: `PATIENT_PORTAL__APPOINTMENTS__FORM_LOCATIONS__POST_SEARCH`.
- Filters a list of appointment form "locations" to show only those where the patient has previously had appointments.
- Steps:
    - Extracts the list of available locations from the event context.
    - Gets the patient ID from the event's target.
    - Retrieves all location IDs where the patient has previously had appointments (filters out any without a valid/active location) using the `Appointment` model.
    - Filters the available locations to those IDs.
    - Returns a single effect with the filtered list, or all locations in case of errors.
- Logging records filtering details and errors.

**Common Implementation Aspects**

- Both classes inherit from `BaseHandler`.
- Each overrides the `compute()` method, which is called in response to the relevant event and returns a list of effect objects.
- Each uses a helper function to query the relevant data (`_get_care_team_provider_ids` for providers, `_get_patient_location_ids` for locations).
- Each wraps the outgoing data in an effect with an appropriately typed effect event.
- The handlers are built for robust operation, falling back to returning the unfiltered list in case of failure, with detailed logging for diagnosis.

```python
import json
from typing import Any

from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data import CareTeamMembership, Appointment, Patient
from canvas_sdk.v1.data.care_team import CareTeamMembershipStatus
from logger import log


class Providers(BaseHandler):
    """
    Filters form providers to only show those in the patient's care team.

    This plugin listens to the PATIENT_PORTAL__APPOINTMENTS__FORM_PROVIDERS__POST_SEARCH
    event and returns a filtered list containing only providers who are members of the
    patient's care team.
    """

    # Name the event type you wish to run in response to
    RESPONDS_TO = EventType.Name(EventType.PATIENT_PORTAL__APPOINTMENTS__FORM_PROVIDERS__POST_SEARCH)

    def compute(self) -> list[Effect]:
        """Filters providers based on patient's care team membership.

        Returns:
            List[Effect]: A single effect containing the filtered provider list
        """

        # Extract providers from context
        context = self.event.context
        providers = context.get("providers", [])

        try:
            if not providers:
                log.info("No providers to filter")
                return []

            # Get patient ID
            patient_id = self.target

            if not patient_id:
                log.warning("No patient ID found, returning all providers")
                return self._create_effect(providers)

            # Get care team provider IDs for this patient
            care_team_provider_ids = self._get_care_team_provider_ids(patient_id)

            log.info(f"Patient {patient_id} care team provider IDs: {care_team_provider_ids}")
            log.info(f"Available providers: {[provider.get('id') for provider in providers]}")

            # Filter providers
            filtered_providers = [
                provider for provider in providers
                if provider.get("id") in care_team_provider_ids
            ]

            log.info(
                f"Filtered {len(providers)} providers to {len(filtered_providers)} "
                f"care team members for patient {patient_id}"
            )

            return self._create_effect(filtered_providers)

        except Exception as e:
            log.error(f"Error filtering providers by care team: {str(e)}")
            # Fail gracefully - return all providers on error
            return self._create_effect(providers)

    def _get_care_team_provider_ids(self, patient_id: str) -> set:
        """Retrieves all provider IDs in the patient's care team.

        Args:
            patient_id: The patient's identifier

        Returns:
            Set of provider IDs that are part of the patient's care team
        """
        try:
            care_team_members = CareTeamMembership.objects.filter(
                patient__id=patient_id,
                status=CareTeamMembershipStatus.ACTIVE
            ).values_list('staff__id', flat=True)

            return set(care_team_members)

        except Exception as e:
            log.error(f"Error fetching care team members: {str(e)}")
            return set()

    def _create_effect(self, providers: list[dict[str, Any]]) -> list[Effect]:
        """Creates the effect with the filtered provider list.

        Args:
            providers: List of provider dictionaries

        Returns:
            List containing a single effect with the provider data
        """
        payload = {
            "providers": providers
        }

        effect_type = EffectType.PATIENT_PORTAL__APPOINTMENTS__FORM_PROVIDERS__POST_SEARCH_RESULTS

        return [Effect(
            type=effect_type,
            payload=json.dumps(payload))]


class Locations(BaseHandler):
    """
    Filters form locations to only show those where the patient has had appointments.

    This plugin listens to the PATIENT_PORTAL__APPOINTMENTS__FORM_LOCATIONS__POST_SEARCH
    event and returns a filtered list containing only locations where the patient
    has previously had appointments.
    """

    # Name the event type you wish to run in response to
    RESPONDS_TO = EventType.Name(EventType.PATIENT_PORTAL__APPOINTMENTS__FORM_LOCATIONS__POST_SEARCH)

    def compute(self) -> list[Effect]:
        """Filters locations based on patient's appointment history.

        Returns:
            List[Effect]: A single effect containing the filtered location list
        """

        # Extract locations from context
        context = self.event.context
        locations = context.get("locations", [])

        try:
            if not locations:
                log.info("No locations to filter")
                return []

            # Get patient ID
            patient_id = self.target

            if not patient_id:
                log.warning("No patient ID found, returning all locations")
                return self._create_effect(locations)

            # Get location IDs where patient has had appointments
            patient_location_ids = self._get_patient_location_ids(patient_id)

            log.info(f"Patient {patient_id} has appointments at locations: {patient_location_ids}")
            log.info(f"Available locations: {[location.get('id') for location in locations]}")

            # Filter locations
            filtered_locations = [
                location for location in locations
                if location.get("id") in patient_location_ids
            ]

            log.info(
                f"Filtered {len(locations)} locations to {len(filtered_locations)} "
                f"locations with appointments for patient {patient_id}"
            )

            return self._create_effect(filtered_locations)

        except Exception as e:
            log.error(f"Error filtering locations by appointment history: {str(e)}")
            # Fail gracefully - return all locations on error
            return self._create_effect(locations)

    def _get_patient_location_ids(self, patient_id: str) -> set:
        """Retrieves all location IDs where the patient has had appointments.

        Args:
            patient_id: The patient's identifier

        Returns:
            Set of location IDs where the patient has had appointments
        """
        try:
            # Query distinct location IDs from patient's appointments
            # Using exclude to filter out appointments without locations
            location_ids = (
                Appointment.objects.filter(patient__id=patient_id)
                .exclude(location__isnull=True, location__active=False)
                .values_list('location__id', flat=True)
                .distinct()
            )

            return set(str(location_id) for location_id in location_ids)

        except Exception as e:
            log.error(f"Error fetching patient appointment locations: {str(e)}")
            return set()

    def _create_effect(self, locations: list[dict[str, Any]]) -> list[Effect]:
        """Creates the effect with the filtered location list.

        Args:
            locations: List of location dictionaries

        Returns:
            List containing a single effect with the location data
        """
        payload = {
            "locations": locations
        }

        effect_type = EffectType.PATIENT_PORTAL__APPOINTMENTS__FORM_LOCATIONS__POST_SEARCH_RESULTS

        return [Effect(
            type=effect_type,
            payload=json.dumps(payload)
        )]
```

<br/>
<br/>
<br/>
