---
title: "AttributeHubs"
slug: "custom-data-attribute-hubs"
---

## Overview

`AttributeHub` provides a simple model for storing arbitrary key-value data that doesn't belong to existing models. 
This approach is ideal for cross-cutting concerns that span multiple models, temporary data storage, 
external system state tracking, or plugin-specific configuration.

**Best for:**
- Cross-cutting concerns that span multiple models
- Temporary (but not auto-expiring) data storage
- External system state tracking
- Plugin-specific configuration

**Example use cases:**
- API synchronization state
- External system identifiers
- Plugin session data
- Feature flags

---

## Creating an AttributeHub

Create a hub for a specific purpose using the `type` and `externally_exposable_id` fields, which together form a unique key.

```python
from canvas_sdk.v1.data import AttributeHub

# Create a hub for a specific purpose
hub = AttributeHub.objects.create(
    type="staff_profile",
    externally_exposable_id="staff_id:abc123"
)
```

---

## Storing Data in AttributeHub

Store individual attributes or complex data as JSON:

```python
from datetime import datetime
from canvas_sdk.v1.data import AttributeHub

# Create or get hub
hub = AttributeHub.objects.create(
    type="staff_profile",
    externally_exposable_id="staff_id:abc123"
)

# Store individual attributes
hub.set_attribute("last_sync", datetime.now())
hub.set_attribute("external_id", "ext_12345")

# Store complex data as JSON
profile_data = {
    "biography": "Experienced physician",
    "specialties": ["Cardiology", "Internal Medicine"],
    "languages": ["English", "Spanish"],
    "practicing_since": 2005
}
hub.set_attribute("profile", profile_data)

# Store multiple attributes at once
hub.set_attributes({
    "last_sync": datetime.now(),
    "external_id": "ext_12345",
    "sync_status": "completed"
})
```

---

## Retrieving Data from AttributeHub

Use the get-or-create pattern to retrieve existing hubs or create new ones:

```python
from canvas_sdk.v1.data import AttributeHub, Staff

staff = Staff.objects.get(id=staff.id)

# Get or create pattern
hub, created = AttributeHub.objects.get_or_create(
    type="staff_profile",
    externally_exposable_id=f"staff_id:{staff.id}"
)

# Retrieve attributes
profile = hub.get_attribute("profile")
last_sync = hub.get_attribute("last_sync")
external_id = hub.get_attribute("external_id")

# Handle missing attributes
status = hub.get_attribute("sync_status")  # Returns None if not set
```

---

## Use Case Example: CRM Campaign Sync

Store synchronization state between a custom data model and an external CRM using AttributeHub:

```python
from canvas_sdk.handlers.simple_api import SimpleAPI, api
from canvas_sdk.effects.simple_api import JSONResponse
from canvas_sdk.v1.data import AttributeHub, Patient
from datetime import datetime


class CRMSyncAPI(SimpleAPI):
    """API endpoint for syncing campaign data with external CRM."""

    PREFIX = "/crm"

    @api.post("/campaign/<campaign_id>/patient/<patient_id>")
    def sync_patient_campaign(self):
        campaign_id = self.request.path_params["campaign_id"]
        patient_id = self.request.path_params["patient_id"]
        patient = Patient.objects.get(id=patient_id)
        crm_data = self.request.json()

        # Store CRM sync state in AttributeHub
        hub, created = AttributeHub.objects.get_or_create(
            type="crm_campaign_sync",
            externally_exposable_id=f"patient:{patient.id}:campaign:{campaign_id}"
        )

        hub.set_attributes({
            "crm_contact_id": crm_data.get("contact_id"),
            "campaign_status": crm_data.get("status"),
            "enrollment_date": crm_data.get("enrolled_at"),
            "last_synced": str(datetime.now()),
            "sync_direction": "crm_to_canvas"
        })

        return [JSONResponse({"status": "success", "hub_id": str(hub.id)})]
```

Later, retrieve the sync state when processing patient events:

```python
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.events import EventType
from canvas_sdk.v1.data import AttributeHub


class CampaignEnrollmentHandler(BaseHandler):
    """Handler that checks CRM campaign sync state for patients."""

    RESPONDS_TO = EventType.Name(EventType.PATIENT_UPDATED)

    def compute(self):
        patient_id = self.target.id
        campaign_id = "wellness_2024"  # Your campaign identifier

        # Retrieve CRM sync state from AttributeHub
        hub, created = AttributeHub.objects.get_or_create(
            type="crm_campaign_sync",
            externally_exposable_id=f"patient:{patient_id}:campaign:{campaign_id}"
        )

        if not created:
            crm_contact_id = hub.get_attribute("crm_contact_id")
            campaign_status = hub.get_attribute("campaign_status")
            last_synced = hub.get_attribute("last_synced")

            # Use the CRM data to drive clinical workflows
            if campaign_status == "enrolled":
                # Patient is enrolled in CRM campaign - trigger relevant protocols
                pass

        return []
```

---

## Best Practices

### Data Organization

1. **Use descriptive type values** - Choose meaningful type names that describe the purpose of the hub (e.g., "external_sync", "api_cache", "feature_flags")
2. **Use consistent ID patterns** - Use a consistent pattern for `externally_exposable_id` (e.g., "entity_type:entity_id")
3. **Namespace by purpose** - Group related data under a single hub rather than creating multiple hubs for the same entity type

### Data Privacy and Isolation

1. **Understand plugin data scoping** - All AttributeHub data is isolated to your plugin by default
2. **Use APIs for data sharing** - Never attempt to access another plugin's AttributeHub data directly
3. **Implement proper authorization** - Secure all APIs that expose AttributeHub data
4. **Follow PHI guidelines** - Treat all patient-related data with appropriate security measures

### Performance

1. **Use get_or_create** - Always use `get_or_create()` to avoid duplicate hubs
2. **Batch attribute updates** - Use `set_attributes()` to set multiple values at once
3. **Cache hub lookups** - If accessing the same hub multiple times, store the reference

### Data Integrity

1. **Handle None values** - Always check if an attribute exists before using it
2. **Validate data** - Validate data before storing in AttributeHub
3. **Clean up unused data** - Remove AttributeHub instances that are no longer needed

### Testing

1. **Use get_or_create in tests** - This pattern works well for test isolation
2. **Verify persistence** - Reload hubs from the database to ensure data persists
3. **Test with different data types** - Verify that strings, numbers, booleans, datetimes, and JSON objects all work correctly

---

## See Also

- [Custom Data Overview](/sdk/custom-data/) - Overview of all custom data techniques
- [CustomAttributes on Proxy Models](/sdk/custom-data-custom-attributes/) - Flexible key-value attributes on existing models
- [Custom Data Models](/sdk/custom-data-custom-models/) - Structured models with relationships
- [Testing Custom Data](/sdk/custom-data-testing/) - Testing utilities and examples
- [Data Models](/sdk/data/) - Core SDK data models
- [Canvas CLI](/sdk/canvas_cli/#simple-api-endpoints) - Simple API for sharing data between plugins
- [Secrets](/sdk/secrets/) - Managing API keys and sensitive configuration
