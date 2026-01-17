---
title: "AttributeHubs"
slug: "custom-data-attribute-hub"
---

## Overview

AttributeHub provides a simple model for storing arbitrary key-value data that doesn't belong to existing models. This approach is ideal for cross-cutting concerns that span multiple models, temporary data storage, external system state tracking, or plugin-specific configuration.

**Best for:**
- Cross-cutting concerns that span multiple models
- Temporary data storage
- External system state tracking
- Plugin-specific configuration

**Example use cases:**
- API synchronization state
- External system identifiers
- Plugin session data
- Feature flags

---

## Creating an AttributeHub

Create a hub for a specific purpose using the `type` and `externally_exposable_id` fields:

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
from canvas_sdk.v1.data import AttributeHub

# Get or create pattern
hub, created = AttributeHub.objects.get_or_create(
    type="staff_profile",
    externally_exposable_id=f"staff_id:{staff_id}"
)

# Retrieve attributes
profile = hub.get_attribute("profile")
last_sync = hub.get_attribute("last_sync")
external_id = hub.get_attribute("external_id")

# Handle missing attributes
status = hub.get_attribute("sync_status")  # Returns None if not set
```

---

## Use Case Example: External API State

Store synchronization state and external system data using AttributeHub:

```python
from canvas_sdk.handlers.simple_api import SimpleAPI, api
from canvas_sdk.effects.simple_api import JSONResponse
from canvas_sdk.v1.data import AttributeHub, Staff
from datetime import datetime


class ExternalSyncAPI(SimpleAPI):
    """API endpoint for syncing external profile data."""

    PREFIX = "/sync"

    @api.post("/profile/<staff_id>")
    def sync_profile(self):
        staff_id = self.request.path_params["staff_id"]
        staff = Staff.objects.get(id=staff_id)
        json_body = self.request.json()

        # Store data in AttributeHub
        hub, created = AttributeHub.objects.get_or_create(
            type="external_sync",
            externally_exposable_id=f"staff:{staff_id}"
        )

        hub.set_attributes({
            "profile_data": json_body,
            "last_synced": str(datetime.now()),
            "sync_status": "completed"
        })

        return [JSONResponse({"status": "success"})]
```

Later, retrieve the sync state:

```python
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.events import EventType
from canvas_sdk.v1.data import AttributeHub


class ProfileHandler(BaseHandler):
    """Handler that checks external sync state."""

    RESPONDS_TO = EventType.Name(EventType.STAFF__STAFF__READ)

    def compute(self):
        staff_id = self.target.id

        # Retrieve sync state from AttributeHub
        hub, created = AttributeHub.objects.get_or_create(
            type="external_sync",
            externally_exposable_id=f"staff:{staff_id}"
        )

        if not created:
            last_synced = hub.get_attribute("last_synced")
            profile_data = hub.get_attribute("profile_data")
            sync_status = hub.get_attribute("sync_status")

            # Use the sync data...
            if sync_status == "completed":
                # Process profile data
                pass

        return []
```

---

## Best Practices

### Data Organization

1. **Use descriptive type values** - Choose meaningful type names that describe the purpose of the hub (e.g., "external_sync", "api_cache", "feature_flags")
2. **Use consistent ID patterns** - Use a consistent pattern for `externally_exposable_id` (e.g., "entity_type:entity_id")
3. **Namespace by purpose** - Group related data under a single hub rather than creating multiple hubs for the same entity

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
- [CustomAttributes on Proxy Models](/sdk/custom-data/custom-attributes/) - Flexible key-value attributes on existing models
- [Custom Data Models](/sdk/custom-data/custom-models/) - Structured models with relationships
- [Testing Custom Data](/sdk/custom-data/testing/) - Testing utilities and examples
- [Data Models](/sdk/data/) - Core SDK data models
- [Canvas CLI](/sdk/canvas_cli/#simple-api-endpoints) - Simple API for sharing data between plugins
- [Secrets](/sdk/secrets/) - Managing API keys and sensitive configuration
