---
title: Canvas FHIR
slug: clients-canvas-fhir
hidden: false
---

The Canvas SDK FHIR client provides a simple interface for interacting with the Canvas FHIR API, supporting CRUD operations on FHIR resources such as Coverages, DocumentReferences, AllergyIntolerances, and more. It handles OAuth client credentials authentication and token caching automatically.

## Requirements

- **Canvas FHIR Client ID**: An OAuth client ID for your Canvas environment
- **Canvas FHIR Client Secret**: The corresponding OAuth client secret

These credentials should be stored as [plugin secrets](/sdk/secrets/) and grant access to the Canvas FHIR API for your environment.

## Imports

The Canvas FHIR client is included in the Canvas SDK. Import the client:

```python
from canvas_sdk.clients.canvas_fhir import CanvasFhir
```

## Initialize the Client

```python?partial=true
client = CanvasFhir(
    client_id="your_client_id",
    client_secret="your_client_secret",
)
```

On initialization, the client will:
1. Authenticate using the OAuth client credentials flow against your Canvas environment's token endpoint.
2. Cache the access token using the plugin cache system, keyed by `client_id`, with automatic expiration.
3. Determine the FHIR API base URL from the `CUSTOMER_IDENTIFIER` setting (e.g., `https://fumage-{CUSTOMER_IDENTIFIER}.canvasmedical.com`).

## Search for Resources

```python
from canvas_sdk.clients.canvas_fhir import CanvasFhir

client = CanvasFhir(
    client_id="your_client_id",
    client_secret="your_client_secret",
)

# Search for a patient's allergy intolerances
results = client.search("AllergyIntolerance", {"patient": "Patient/abc123"})

for entry in results.get("entry", []):
    resource = entry["resource"]
    print(f"Allergy: {resource['code']['coding'][0]['display']}")
```

## Read a Specific Resource

```python?partial=true
# Read a specific resource by ID
allergy = client.read("AllergyIntolerance", "allergy-id-123")
print(f"Status: {allergy['clinicalStatus']['coding'][0]['code']}")
```

## Create a Resource

```python?partial=true
# Create a new Coverage resource
coverage = client.create("Coverage", {
    "resourceType": "Coverage",
    "status": "active",
    "beneficiary": {"reference": "Patient/abc123"},
    "payor": [{"reference": "Organization/org-456"}],
})
print(f"Created Coverage: {coverage['id']}")
```

## Update a Resource

```python?partial=true
# Update an existing resource
updated = client.update("Coverage", "coverage-id-789", {
    "resourceType": "Coverage",
    "id": "coverage-id-789",
    "status": "cancelled",
    "beneficiary": {"reference": "Patient/abc123"},
    "payor": [{"reference": "Organization/org-456"}],
})
print(f"Updated Coverage status: {updated['status']}")
```

## CanvasFhir

The main class for interacting with the Canvas FHIR API.

### Constructor

```python?partial=true
CanvasFhir(client_id: str, client_secret: str)
```

| Parameter       | Type  | Description                         |
|-----------------|-------|-------------------------------------|
| `client_id`     | `str` | OAuth client ID for the Canvas API  |
| `client_secret` | `str` | OAuth client secret                 |

### Methods

#### `search(resource_type: str, parameters: dict) -> dict`

Search for FHIR resources matching the given parameters.

```python?partial=true
results = client.search("Patient", {"name": "Smith", "birthdate": "1990-01-01"})
```

| Parameter       | Type   | Description                                      |
|-----------------|--------|--------------------------------------------------|
| `resource_type` | `str`  | FHIR resource type (e.g., `Patient`, `Coverage`) |
| `parameters`    | `dict` | Search parameters as key-value pairs             |

**Returns:** FHIR Bundle `dict` containing matching resources.

**Raises:** `requests.HTTPError` if the API returns an error status code.

#### `read(resource_type: str, resource_id: str) -> dict`

Read a single FHIR resource by its ID.

```python?partial=true
patient = client.read("Patient", "patient-id-123")
```

| Parameter       | Type  | Description                          |
|-----------------|-------|--------------------------------------|
| `resource_type` | `str` | FHIR resource type                   |
| `resource_id`   | `str` | ID of the resource to read           |

**Returns:** FHIR resource `dict`.

**Raises:** `requests.HTTPError` if the API returns an error status code.

#### `create(resource_type: str, data: dict) -> dict`

Create a new FHIR resource.

```python?partial=true
new_resource = client.create("DocumentReference", {
    "resourceType": "DocumentReference",
    "status": "current",
    "type": {"coding": [{"system": "http://loinc.org", "code": "34133-9"}]},
    "subject": {"reference": "Patient/abc123"},
})
```

| Parameter       | Type   | Description                          |
|-----------------|--------|--------------------------------------|
| `resource_type` | `str`  | FHIR resource type                   |
| `data`          | `dict` | FHIR resource data to create        |

**Returns:** Created FHIR resource `dict` (including server-assigned `id`).

**Raises:** `requests.HTTPError` if the API returns an error status code.

#### `update(resource_type: str, resource_id: str, data: dict) -> dict`

Update an existing FHIR resource.

```python?partial=true
updated = client.update("Coverage", "coverage-id-789", {
    "resourceType": "Coverage",
    "id": "coverage-id-789",
    "status": "cancelled",
    "beneficiary": {"reference": "Patient/abc123"},
    "payor": [{"reference": "Organization/org-456"}],
})
```

| Parameter       | Type   | Description                          |
|-----------------|--------|--------------------------------------|
| `resource_type` | `str`  | FHIR resource type                   |
| `resource_id`   | `str`  | ID of the resource to update         |
| `data`          | `dict` | Complete FHIR resource data          |

**Returns:** Updated FHIR resource `dict`.

**Raises:** `requests.HTTPError` if the API returns an error status code.

## Authentication

The client uses the OAuth 2.0 client credentials flow to authenticate with the Canvas API. Token management is handled automatically:

- On first use, the client exchanges the `client_id` and `client_secret` for an access token via the Canvas token endpoint.
- The token is cached using the plugin cache system with the key `canvas_fhir_credentials_{client_id}`.
- The cached token expires 60 seconds before the actual token expiration to avoid using stale credentials.
- Subsequent requests reuse the cached token until it expires.

## Error Handling

The Canvas FHIR client uses `raise_for_status()` on all HTTP responses, which raises `requests.HTTPError` for non-successful status codes.

```python?partial=true
from requests import HTTPError

try:
    result = client.read("Patient", "nonexistent-id")
except HTTPError as e:
    print(f"HTTP {e.response.status_code}: {e.response.text}")
```

## Complete Plugin Example

Here's a complete example of using the Canvas FHIR client in an ActionButton handler:

```python
from canvas_sdk.clients.canvas_fhir import CanvasFhir
from canvas_sdk.effects import Effect
from canvas_sdk.handlers.action_button import ActionButton
from logger import log


class FhirRequestHandler(ActionButton):
    """Handler that queries the FHIR API when a button is clicked."""

    BUTTON_TITLE = "Trigger FHIR Request"
    BUTTON_KEY = "TRIGGER_FHIR_REQUEST"
    BUTTON_LOCATION = ActionButton.ButtonLocation.CHART_SUMMARY_ALLERGIES_SECTION

    def handle(self) -> list[Effect]:
        """Handle the button click."""
        client_id = self.secrets["CANVAS_FHIR_CLIENT_ID"]
        client_secret = self.secrets["CANVAS_FHIR_CLIENT_SECRET"]
        patient_id = self.event.target.id

        client = CanvasFhir(client_id, client_secret)

        # Search for the patient's allergy intolerances
        search_response = client.search(
            "AllergyIntolerance",
            {"patient": f"Patient/{patient_id}"},
        )
        log.info(f"Search: {search_response}")

        # Read the first result
        first_entry = search_response["entry"][0]["resource"]
        read_response = client.read("AllergyIntolerance", first_entry["id"])
        log.info(f"Read: {read_response}")

        return []
```

## Additional Resources

- [Canvas FHIR API Documentation](/api/)
- [Example Plugin Source Code](https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/canvas_fhir_client)

<br/>
<br/>
<br/>
