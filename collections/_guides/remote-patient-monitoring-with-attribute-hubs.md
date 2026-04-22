---
title: "Remote Patient Monitoring with AttributeHubs"
guide_for:
- /sdk/custom-data-attribute-hubs/
- /sdk/handlers-simple-api-http/
- /sdk/custom-data/
---

Remote Patient Monitoring (RPM) programs collect readings from devices patients
use at home — blood pressure cuffs, glucometers, pulse oximeters, weight scales,
and more. Each device type reports a different set of measurements, and RPM
vendors regularly add new devices to their catalog.

In this guide, you'll build a plugin that receives device readings from an
external RPM platform via a webhook and stores them using
[AttributeHubs](/sdk/custom-data-attribute-hubs/). Because each device type
reports different measurements — and new device types can appear at any time —
AttributeHubs' schemaless storage is a natural fit. The plugin will store
whatever fields a device sends without needing to know about them in advance.

{% include alert.html type="info" content="This guide assumes you have the
Canvas CLI installed and configured, and that you're familiar with plugin
basics. If you're starting from scratch, work through
<a href='/guides/your-first-plugin/'>Your First Plugin</a> first." %}

## Why AttributeHubs for this use case?

A blood pressure cuff sends systolic, diastolic, and pulse. A glucometer sends
glucose level, meal context, and measurement site. A pulse oximeter sends SpO2
and perfusion index. These schemas are defined by the devices, not by your
plugin.

A [CustomModel](/sdk/custom-data-custom-models/) would require either a separate
table per device type or a single wide table full of nullable columns — and
either way, supporting a new device means changing the schema.
AttributeHubs sidestep this entirely: each reading is stored as a hub with
whatever key-value pairs the device reports. When the RPM vendor adds a
new device, the plugin handles it with zero code changes.

For a deeper comparison of when to use each approach, see
[Design Considerations](/sdk/custom-data-design-considerations/).

## Initialize the plugin

Scaffold a new plugin with the Canvas CLI:

```sh
$ canvas init
  [1/1] project_name (My Cool Plugin): RPM Device Readings
Project created in /Users/you/rpm-device-readings
```

Then navigate into the project:

```sh
cd rpm-device-readings
```

The generated structure looks like this:

```
rpm-device-readings/
├── rpm_device_readings/
│   ├── CANVAS_MANIFEST.json
│   ├── README.md
│   └── handlers/
│       ├── __init__.py
│       └── my_protocol.py
├── pyproject.toml
└── tests/
    ├── __init__.py
    └── test_models.py
```

We'll be using a [SimpleAPI](/sdk/handlers-simple-api-http/) route instead of an
event handler, so you can remove the placeholder handler:

```sh
rm rpm_device_readings/handlers/my_protocol.py
```

## Configure the manifest

Replace the contents of `rpm_device_readings/CANVAS_MANIFEST.json` with:

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1",
    "name": "rpm_device_readings",
    "description": "Stores device readings from an external RPM platform using AttributeHubs",
    "components": {
        "handlers": [
            {
                "class": "rpm_device_readings.routes.device_readings_api:DeviceReadingsAPI",
                "description": "Webhook endpoint for receiving and retrieving RPM device readings"
            }
        ]
    },
    "secrets": ["RPM_VENDOR_API_KEY"],
    "custom_data": {
        "namespace": "my_org__rpm_readings",
        "access": "read_write"
    },
    "tags": {},
    "license": "",
    "readme": "./README.md"
}
```

A few things to note:

- **`secrets`** declares `RPM_VENDOR_API_KEY`, which you'll share with your RPM
  vendor so they can authenticate their webhook requests.
- **`custom_data`** declares a namespace for AttributeHub storage. Replace
  `my_org` with your organization's name. See
  [Namespace Lifecycle](/sdk/custom-data-namespace-lifecycle/) for details.
- The **handler class** points to a `routes/` module that we'll create next.
  SimpleAPI routes are registered as handlers in the manifest — they just live
  in a different directory by convention.

## Create the API route

Create the `routes/` directory:

```sh
mkdir -p rpm_device_readings/routes
touch rpm_device_readings/routes/__init__.py
```

Then create `rpm_device_readings/routes/device_readings_api.py` with the
following code:

```python
from datetime import datetime
from hmac import compare_digest
from http import HTTPStatus

from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyCredentials, SimpleAPI, api
from canvas_sdk.v1.data import AttributeHub
from logger import log


def normalize_timestamp(value: str) -> str:
    """Parse an ISO 8601 timestamp and truncate to second precision."""
    dt = datetime.fromisoformat(value)
    return dt.replace(microsecond=0).isoformat()


class DeviceReadingsAPI(SimpleAPI):
    PREFIX = "/routes"

    def authenticate(self, credentials: APIKeyCredentials) -> bool:
        expected_key = self.secrets.get("RPM_VENDOR_API_KEY", "")
        return compare_digest(credentials.key.encode(), expected_key.encode())

    @api.post("/readings")
    def receive_reading(self) -> list[Response | Effect]:
        """Accept a device reading from the RPM platform."""
        body = self.request.json()

        patient_id = body.get("patient_id")
        device_type = body.get("device_type")
        recorded_at = body.get("recorded_at")
        measurements = body.get("measurements")

        if not all([patient_id, device_type, recorded_at, measurements]):
            return [
                JSONResponse(
                    {"error": "patient_id, device_type, recorded_at, and measurements are required"},
                    status_code=HTTPStatus.BAD_REQUEST,
                )
            ]

        try:
            recorded_at = normalize_timestamp(recorded_at)
        except (ValueError, TypeError):
            return [
                JSONResponse(
                    {"error": "recorded_at must be a valid ISO 8601 timestamp"},
                    status_code=HTTPStatus.BAD_REQUEST,
                )
            ]

        hub, created = AttributeHub.objects.get_or_create(
            type="rpm_reading",
            id=f"patient:{patient_id}:device:{device_type}:{recorded_at}",
        )

        hub.set_attributes({
            "patient_id": patient_id,
            "device_type": device_type,
            "recorded_at": recorded_at,
            **measurements,
        })

        log.info(
            f"Stored {device_type} reading for patient {patient_id}: "
            f"{len(measurements)} measurements"
        )

        return [JSONResponse({"status": "stored"}, status_code=HTTPStatus.CREATED)]

    @api.get("/readings/<patient_id>")
    def get_readings(self) -> list[Response | Effect]:
        """Retrieve all readings for a patient, grouped by device type."""
        patient_id = self.request.path_params["patient_id"]

        hubs = AttributeHub.objects.filter(
            type="rpm_reading",
            custom_attributes__name="patient_id",
            custom_attributes__value=patient_id,
        )

        readings_by_device: dict[str, list[dict]] = {}
        for hub in hubs:
            device_type = hub.get_attribute("device_type")
            recorded_at = hub.get_attribute("recorded_at")

            metadata_keys = {"patient_id", "device_type", "recorded_at"}
            measurements = {
                attr.name: attr.value
                for attr in hub.custom_attributes.all()
                if attr.name not in metadata_keys
            }

            readings_by_device.setdefault(device_type, []).append({
                "recorded_at": recorded_at,
                "measurements": measurements,
            })

        return [JSONResponse({"patient_id": patient_id, "readings": readings_by_device})]
```

That's the entire plugin. Let's walk through the important parts.

## Anatomy of the plugin

### Authentication

The `authenticate` method uses API key authentication. The RPM vendor includes
the key in the `Authorization` header of each request. The plugin compares it
against the `RPM_VENDOR_API_KEY` secret using constant-time comparison to
prevent timing attacks.

### Receiving a reading

The `receive_reading` endpoint accepts a POST with a JSON body. The body has
four required fields — `patient_id`, `device_type`, `recorded_at`, and
`measurements` — but the contents of `measurements` are completely open-ended.

A blood pressure reading might look like:

```json
{
    "patient_id": "abc-123",
    "device_type": "blood_pressure",
    "recorded_at": "2026-04-21T14:30:00Z",
    "measurements": {
        "systolic": 128,
        "diastolic": 82,
        "pulse": 72,
        "irregular_heartbeat_detected": false
    }
}
```

A glucometer reading has an entirely different set of measurements:

```json
{
    "patient_id": "abc-123",
    "device_type": "glucometer",
    "recorded_at": "2026-04-21T08:15:00Z",
    "measurements": {
        "glucose_mg_dl": 142,
        "meal_context": "fasting",
        "measurement_site": "fingertip"
    }
}
```

The plugin doesn't distinguish between these. It stores whatever fields appear
in `measurements` as AttributeHub attributes. When the RPM vendor starts
supporting a new device — say, a continuous temperature monitor — the plugin
stores its readings without any code or schema changes.

### Storing the reading

Each reading becomes an AttributeHub with:

- **`type`**: `"rpm_reading"` — groups all RPM readings together for querying.
- **`id`**: A compound key combining patient, device type, and timestamp. The
  `type` and `id` pair must be unique, so this ensures one hub per reading.

The `normalize_timestamp` helper truncates the incoming timestamp to second
precision before it's used in the hub ID. This prevents the same reading from
creating duplicate hubs when the vendor sends varying precision — for example,
`"2026-04-21T14:30:00Z"` and `"2026-04-21T14:30:00.000Z"` both normalize to
the same value.

```python?partial=true
hub, created = AttributeHub.objects.get_or_create(
    type="rpm_reading",
    id=f"patient:{patient_id}:device:{device_type}:{recorded_at}",
)

hub.set_attributes({
    "patient_id": patient_id,
    "device_type": device_type,
    "recorded_at": recorded_at,
    **measurements,
})
```

We use `get_or_create` rather than `create` so that retried webhook deliveries
are idempotent — if the RPM vendor resends a reading, we update the existing
hub rather than failing with a duplicate key error.

The `set_attributes` call stores all measurements as typed attributes.
AttributeHub automatically maps Python types to the appropriate database
columns: integers to `int_value`, booleans to `bool_value`, strings to
`text_value`, floats to `decimal_value`, and so on.

### Retrieving readings

The `get_readings` endpoint filters hubs by type and patient ID, then groups
results by device type:

```python?partial=true
hubs = AttributeHub.objects.filter(
    type="rpm_reading",
    custom_attributes__name="patient_id",
    custom_attributes__value=patient_id,
)
```

This query finds all `rpm_reading` hubs that have a `patient_id` attribute
matching the requested patient. AttributeHub automatically prefetches all
attributes when you iterate over a queryset, so the loop that extracts
measurements from each hub does not cause additional queries.

## Install and test

Install the plugin on your Canvas instance, setting the API key secret at
install time:

```sh
canvas install rpm-device-readings \
    --host YOUR_INSTANCE \
    --secret RPM_VENDOR_API_KEY=your-secret-key-here
```

{% include alert.html type="info" content="Generate a secure API key with:
<code>python -c \"import secrets; print(secrets.token_hex(32))\"</code>. Share
this key with your RPM vendor so they can authenticate their webhook requests." %}

Send a blood pressure reading:

```sh
curl -X POST \
    https://YOUR_INSTANCE.canvasmedical.com/plugin-io/api/rpm_device_readings/routes/readings \
    -H "Authorization: your-secret-key-here" \
    -H "Content-Type: application/json" \
    -d '{
        "patient_id": "abc-123",
        "device_type": "blood_pressure",
        "recorded_at": "2026-04-21T14:30:00Z",
        "measurements": {
            "systolic": 128,
            "diastolic": 82,
            "pulse": 72,
            "irregular_heartbeat_detected": false
        }
    }'
```

Send a pulse oximeter reading for the same patient:

```sh
curl -X POST \
    https://YOUR_INSTANCE.canvasmedical.com/plugin-io/api/rpm_device_readings/routes/readings \
    -H "Authorization: your-secret-key-here" \
    -H "Content-Type: application/json" \
    -d '{
        "patient_id": "abc-123",
        "device_type": "pulse_oximeter",
        "recorded_at": "2026-04-21T14:32:00Z",
        "measurements": {
            "spo2": 97,
            "pulse_rate": 74,
            "perfusion_index": 3.2
        }
    }'
```

Now retrieve the patient's readings:

```sh
curl https://YOUR_INSTANCE.canvasmedical.com/plugin-io/api/rpm_device_readings/routes/readings/abc-123 \
    -H "Authorization: your-secret-key-here"
```

The response groups readings by device type:

```json
{
    "patient_id": "abc-123",
    "readings": {
        "blood_pressure": [
            {
                "recorded_at": "2026-04-21T14:30:00Z",
                "measurements": {
                    "systolic": 128,
                    "diastolic": 82,
                    "pulse": 72,
                    "irregular_heartbeat_detected": false
                }
            }
        ],
        "pulse_oximeter": [
            {
                "recorded_at": "2026-04-21T14:32:00Z",
                "measurements": {
                    "spo2": 97,
                    "pulse_rate": 74,
                    "perfusion_index": 3.2
                }
            }
        ]
    }
}
```

## Adding new device types

When the RPM vendor starts supporting a new device, no plugin changes are
needed. The vendor simply sends readings with the new device type and its
measurements:

```json
{
    "patient_id": "abc-123",
    "device_type": "weight_scale",
    "recorded_at": "2026-04-22T07:00:00Z",
    "measurements": {
        "weight_kg": 81.2,
        "bmi": 25.4,
        "body_fat_pct": 22.1
    }
}
```

The plugin stores and retrieves it exactly like any other reading. This is the
core advantage of AttributeHubs for this use case — the schema is defined by the
devices, not by the plugin.

## When to reach for CustomModels instead

AttributeHubs are the right fit here because the measurements vary per device
and the primary access pattern is retrieving readings for a specific patient.
If your requirements shift, consider
[CustomModels](/sdk/custom-data-custom-models/) instead when:

- You need to **query across patients by measurement value** — for example,
  "find all patients with systolic > 140." AttributeHub filtering requires a
  JOIN to the attribute table per condition, which gets expensive at scale.
- You need to **aggregate readings** — for example, "average glucose over the
  past 30 days." Django ORM aggregation functions work naturally on typed
  CustomModel columns but are awkward with AttributeHub's EAV structure.
- Your **device types are stable and known** at development time. If you'll only
  ever support three device types, three small CustomModels with typed columns
  will give you better query performance and a self-documenting schema.

<br/>
<br/>
<br/>
