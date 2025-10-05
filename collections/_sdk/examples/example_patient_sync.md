---
title: 'Patient Creation Platform Sync'
slug: 'example-patient_creation_platform_sync'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/example_patient_sync' target='_blank'>View the source</a> for this plugin on GitHub." %}


## Description

An example of bidirectional patient creation between Canvas and a 3rd party system.

At a high level, this plugin:
1. Adds an API endpoint to which the external system can POST a new patient object with a given system_id, which creates a patient in Canvas with an external_identifier.
2. Configures a webhook for the PATIENT_CREATED event to automatically synchronize patient data. When a patient is created in Canvas, the webhook triggers an update (or creation) in the external system via its patient GET/POST/PATCH API, ensuring the Canvas ID is always included.

## Sample CURL request

Once the API endpoint POST action is created, test it is working with the following CURL command (or use a popular GUI like Postman or Bruno). Replace "training" with your Canvas instance name:

```
curl --request POST \
  --url https://training.canvasmedical.com/plugin-io/api/example_patient_sync/patients \
  --header 'content-type: application/json' \
  --header 'authorization: 97f2a0f033666d29ff09ee42b3afd7e4'
  --data '{
  "firstName": "Alice",
  "lastName": "Example",
  "sexAtBirth": "F",
  "dateOfBirth": "1980-02-22",
  "partnerId": "pat_12345678"
}'
```

## Defining and Setting Secrets

This example plugin defines four "secrets" in the manifest file:

```
    "secrets": [
        "PARTNER_URL_BASE",
        "PARTNER_API_BASE_URL",
        "PARTNER_SECRET_API_KEY",
        "simpleapi-api-key"
    ],
```
Once defined in the `MANIFEST.json`, set the secrets for your plugin in the Admin UI of your Canvas EMR. [Read more](https://docs.canvasmedical.com/sdk/secrets/)

### PARTNER_URL_BASE
This string value will be set as the "system" in the patient external identifier that is created. A patient can have many external identifiers, so make sure this is a unique value that is searchable to find their external ID in the future. [Read more](https://docs.canvasmedical.com/sdk/effect-create-patient-external-identifier/)

### PARTNER_API_BASE_URL
This string value will be used when making REST API calls to a partner system (to create or update a patient record, for example). It may or may not be the same as the PARTNER_URL_BASE.

### PARTNER_SECRET_API_KEY
If accessing a partner API requires authorization, this can define the auth secret to enable the API handshake.

### simpleapi-api-key
This is the authorization needed for Canvas when using APIKeyAuthMixin. [Read more](https://docs.canvasmedical.com/sdk/handlers-simple-api-http/#session)


## CANVAS_MANIFEST.json

```json
{
    "sdk_version": "0.40.0",
    "plugin_version": "0.0.1",
    "name": "example_patient_sync",
    "description": "Example bidirectional patient synchronization between Canvas and a 3rd party system",
    "components": {
        "protocols": [
            {
                "class": "example_patient_sync.handlers.patient_sync:PatientSync",
                "description": "Create or update patients in an external system based on Canvas events",
            },
            {
                "class": "example_patient_sync.routes.patient_create_api:PatientCreateApi",
                "description": "Create a patient in Canvas when a user is created in an external system",
            }
        ],

        "commands": [],
        "content": [],
        "effects": [],
        "views": []
    },
    "secrets": [
        "PARTNER_URL_BASE",
        "PARTNER_API_BASE_URL",
        "PARTNER_SECRET_API_KEY",
        "simpleapi-api-key"
    ],
    "tags": {},
    "references": [],
    "license": "",
    "diagram": false,
    "readme": "./README.md"
}
```

## routes/

### patient_create_api.py

**Purpose**

The code defines an HTTP API endpoint for creating new patient records in Canvas from a third-party system. It authenticates requests using an API key and expects data in JSON format.

**Authentication**

The endpoint uses APIKeyAuthMixin, which requires clients to provide a valid API key in the request headers for authorization.

**Endpoint Details**

- **Route:** POST /patients
- **Description:** Accepts and processes patient creation requests sent by external systems.

**Request Handling**

- Expects a JSON body describing the patient. If the JSON body is not a dictionary, returns a "400 Bad Request".
- Extracts and processes the following fields from the request:
  - `firstName`: Patient's first name.
  - `lastName`: Patient's last name.
  - `dateOfBirth`: Patient's date of birth, parsed and converted to a date object.
  - `sexAtBirth`: Patient's sex at birth; attempts to standardize and map to one of the PersonSex enum values (`SEX_FEMALE`, `SEX_MALE`, `SEX_OTHER`, `SEX_UNKNOWN`). Unrecognized values are ignored.
  - `partnerId`: An external identifier for the patient, which is combined with a secret value (`PARTNER_URL_BASE`) to create a unique identifier object.

**Patient Creation**

- Constructs a Patient object with the collected and parsed data.
- Attaches the external identifier from the requesting system.

**Response**

- Issues two actions in its response list:
  - Requests the creation of the Patient record (an Effect for persistence in Canvas).
  - Returns a JSON response (HTTP 202 Accepted) containing the external identifier information (system and value), indicating the request was accepted.

**Error Handling**

- If the request body is not valid JSON or not a dictionary, the endpoint immediately returns a 400 Bad Request with an error message.

**Dependencies**

- Relies on the Canvas SDK for authentication, response creation, effect handling, and data models.
- Uses the arrow library for robust date parsing.

```python
from http import HTTPStatus
from typing import cast

import arrow

from canvas_sdk.effects import Effect
from canvas_sdk.effects.patient import Patient, PatientExternalIdentifier
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyAuthMixin, SimpleAPI, api
from canvas_sdk.v1.data.common import PersonSex


# Authentication is handled by the APIKeyAuthMixin, which checks the API key in the request headers
# https://docs.canvasmedical.com/sdk/handlers-simple-api-http/#api-key-1
class PatientCreateApi(APIKeyAuthMixin, SimpleAPI):
    """API endpoint for use by third-party system to create patients in Canvas when that system is the point of origination for that patient record."""

    # Docs: https://docs.canvasmedical.com/sdk/handlers-simple-api-http/
    # POST https://<instance-name>.canvasmedical.com/plugin-io/api/example_patient_sync/patients
    @api.post("/patients")
    def post(self) -> list[Response | Effect]:
        """Handle POST requests for patient sync."""
        json_body = self.request.json()

        if not isinstance(json_body, dict):
            return [
                JSONResponse(
                    content="Invalid JSON body.", status_code=HTTPStatus.BAD_REQUEST
                ).apply()
            ]
        birthdate = None
        date_of_birth_str = json_body.get("dateOfBirth")
        if isinstance(date_of_birth_str, str) and date_of_birth_str:
            birthdate = arrow.get(date_of_birth_str).date()

        sex_at_birth = None
        sex_at_birth_str = json_body.get("sexAtBirth")
        if sex_at_birth_str:
            s = cast(str, sex_at_birth_str).strip().upper()
            if s in ("F", "FEMALE"):
                sex_at_birth = PersonSex.SEX_FEMALE
            elif s in ("M", "MALE"):
                sex_at_birth = PersonSex.SEX_MALE
            elif s in ("O", "OTHER"):
                sex_at_birth = PersonSex.SEX_OTHER
            elif s in ("U", "UNKNOWN"):
                sex_at_birth = PersonSex.SEX_UNKNOWN
            else:
                sex_at_birth = None

        partner_id = str(json_body.get("partnerId"))

        external_id = PatientExternalIdentifier(
            system=self.secrets['PARTNER_URL_BASE'],
            value=partner_id,
        )

        patient = Patient(
            birthdate=birthdate,
            first_name=str(json_body.get("firstName")),
            last_name=str(json_body.get("lastName")),
            sex_at_birth=sex_at_birth,
            external_identifiers=[external_id],
        )

        response = {"external_identifier": {"system": self.secrets['PARTNER_URL_BASE'], "value": partner_id}}

        return [
            patient.create(),
            JSONResponse(content=response, status_code=HTTPStatus.ACCEPTED).apply(),
        ]
```

## handlers/

### patient_sync.py

**Summary**

This file defines a synchronization handler for patient data between the Canvas Medical platform and an external partner system. It listens for the event when a patient is created on Canvas and then ensures that this patient also exists (and is linked via an external identifier) in the partner system. The handler manages bidirectional lookup and updates of patient IDs between the two systems.

**Details of Operation**

- The core class, `PatientSync`, inherits from `BaseHandler` and is triggered by the `PATIENT_CREATED` event in Canvas.
- It uses configuration secrets and environment variables to determine endpoints, authentication headers, and other partner-specific parameters.
- When a new patient is created in Canvas, the handler:
    1. Checks if the patient already has an external identifier linking them to the partner system.
    2. If not, attempts to look up the patient in the partner system using the Canvas patient ID by issuing a GET request.
    3. If an existing patient ID is found in the partner system, or after determining a new patient needs to be created, it prepares a payload with patient details.
    4. Issues a POST request to the partner API to either create or update the patient there.
    5. If creating, the handler expects the partner system to return the newly created patient’s external ID.
    6. Handles duplicate creation attempts (HTTP 409) by simply returning without making changes.
    7. When a new external identifier is obtained, triggers an Effect to update the Canvas patient record with this identifier.

**Technical Implementation**

- Secrets such as API keys and base URLs are used for secure access and configuration.
- The handler functions as a stateless, event-driven adapter to maintain patient cross-system consistency.
- HTTP request functionality is abstracted via Canvas SDK utilities.
- Effects (a pattern used in Canvas plugins) are queued to perform changes in Canvas asynchronously and safely.
- Logging is imported but not shown in use in the provided code.

**Key Methods**

- `lookup_external_id_by_system_url`: Searches Canvas patient external identifiers for the partner system's record.
- `get_patient_from_system_api`: Fetches patient details from the external partner via GET request.
- `compute`: Main workflow coordinating the above logic, handling deduplication, updates, and creation logic for patients in both systems.

**Error and Edge Cases**

- Handles the situation where the partner system returns a duplicate on creation.
- Deals with missing IDs by attempting lookups and only initiating creation when necessary.
- Only updates Canvas when a new cross-system ID must be set.

**Purpose**

This plugin component ensures that every patient created in Canvas is also represented in a connected partner system, with persistent, synchronized external identifiers to enable cross-platform interoperability and data consistency.

```python
from typing import Any

from canvas_sdk.effects import Effect
from canvas_sdk.effects.patient import CreatePatientExternalIdentifier
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.utils import Http
from canvas_sdk.v1.data.patient import Patient
from logger import log

class PatientSync(BaseHandler):
    """Handler for synchronizing patient data between systems."""

    RESPONDS_TO = [
        EventType.Name(EventType.PATIENT_CREATED),
    ]

    @property

    def partner_url_base(self) -> str:
        """Return the base URL for the external partner platform."""
        return self.secrets["PARTNER_URL_BASE"]

    def partner_api_base_url(self) -> str:
        """Return the base URL for the external partner API."""
        return self.secrets["PARTNER_API_BASE_URL"]

    @property
    def partner_request_headers(self) -> dict[str, str]:
        """Return the request headers for external partner API requests."""
        partner_secret_api_key = self.secrets["PARTNER_SECRET_API_KEY"]
        return {"X-API-Key": partner_secret_api_key}

    @property
    def partner_patient_metadata(self) -> Any:
        """Return metadata for creation of the patient on external partner platform."""
        metadata = {"canvasPatientId": self.target}

        subdomain = self.environment["CUSTOMER_IDENTIFIER"]
        canvas_url = f"https://{subdomain}.canvasmedical.com"

        # This sets the canvas URL for the patient in the partner platform metadata
        # Combined with the canvasPatientId, this allows the partner platform to link back to the patient in Canvas
        metadata["canvasUrl"] = canvas_url

        return metadata

    def lookup_external_id_by_system_url(self, canvas_patient: Patient, system: str) -> str | None:
        """Get the system ID for a given patient and system from Canvas."""
        # If the patient already has a external identifier for the partner platform, identified by a matching system url, use the first one
        return (
            canvas_patient.external_identifiers.filter(system=system)
            .values_list("value", flat=True)
            .first()
        )

    def get_patient_from_system_api(self, canvas_patient_id: str) -> Any:
        """Look up a patient in the external system."""
        http = Http()
        return http.get(
            f"{self.partner_api_base_url}/patients/v2/{canvas_patient_id}",
            headers=self.partner_request_headers,
        )

    def compute(self) -> list[Effect]:
        """Compute the sync actions for the patient."""
        canvas_patient_id = self.target

        http = Http()

        canvas_patient = Patient.objects.get(id=canvas_patient_id)
        # by default assume we don't yet have a system patient ID
        # and that we need to update the patient in Canvas to add one
        system_patient_id = self.lookup_external_id_by_system_url(canvas_patient, self.partner_url_base)
        update_patient_external_identifier = system_patient_id is None

        # Here we check if the patient already has an external ID in Canvas for the partner platform
        if not system_patient_id:

            # Get the system external ID by making a GET request to the partner platform
            system_patient = self.get_patient_from_system_api(canvas_patient_id)

            system_patient_id = (
                system_patient.json()["id"] if system_patient.status_code == 200 else None
            )

        # Great, now we know if the patient is assigned a system external ID with the partner
        # platform, and if we need to update it. At this point the system_patient_id can be 3 possible values:
        # 1. value we already had stored in Canvas in an external identifier,
        # 2. value we just got from our partner GET API lookup, or
        # 3. None
        # And we have a true/false call to action telling us if we need to add
        # an external identifier to our Canvas patient: `update_patient_external_identifier`

        # Generate the payload for creating or updating the patient in partner platform API
        partner_payload = {
            "externalId": canvas_patient.id,
            "firstName": canvas_patient.first_name,
            "lastName": canvas_patient.last_name,
            "dateOfBirth": canvas_patient.birth_date.isoformat(),
        }

        base_request_url = f"{self.partner_api_base_url}/patients/v2"

        # If we have a patient's partner external id, we know this is an update, so we'll append it to the request URL
        request_url = (
            f"{base_request_url}/{system_patient_id}" if system_patient_id else base_request_url
        )
        resp = http.post(request_url, json=partner_payload, headers=self.partner_request_headers)

        # If your system's API returns the ID of the newly created record,
        # grab it from the response so we can add it to the Canvas patient record
        if system_patient_id is None:
            system_patient_id = resp.json().get("id")

        duplicate_patient_attempt = resp.status_code == 409

        if duplicate_patient_attempt:
            # If your system's API can let you know when a duplicate record was attempted to be added,
            # you can use that information to return early here.
            return []
        elif update_patient_external_identifier:
            # Queue up an effect to update the patient in Canvas and add the external identifier
            external_id = CreatePatientExternalIdentifier(
                patient_id=canvas_patient.id,
                system=self.partner_url_base,
                value=str(system_patient_id)
            )
            return [external_id.create()]
        else:
            return [] # Done!
```

<br/>
<br/>
<br/>
