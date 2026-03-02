---
title: "AttributeHubs"
slug: "custom-data-attribute-hubs"
---

## Overview

`AttributeHubs` provide a simple mechanism for storing arbitrary key-value data that doesn't belong to existing models. 
This approach is ideal for cross-cutting concerns that span multiple models, temporary data storage, external system state tracking, 
or plugin-specific configuration.

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

## Creating an AttributeHub

Create a hub for a specific purpose using the `type` and `id` fields, which together form a unique key.
There is a database constraint on these two fields to ensure uniqueness, and creating a duplicate will raise a `UniqueViolation` 
exception.

```python
from canvas_sdk.v1.data import AttributeHub

# Create a hub for a specific purpose
hub = AttributeHub.objects.create(
    type="staff_profile",
    id="staff_id:abc123"
)
```

## Storing Data in AttributeHub

Store individual attributes or complex data as JSON. Here's an example of a meal tracker that records patient meals and calories:

```python
from datetime import datetime
from canvas_sdk.v1.data import AttributeHub, Patient

patient = Patient.objects.get(id="patient-uuid-here")

# Create a hub to track a specific meal
hub = AttributeHub.objects.create(
    type="meal_entry",
    id=f"patient:{patient.id}:meal:{datetime.now().isoformat()}"
)

# Store individual attributes
hub.set_attribute("meal_type", "lunch")
hub.set_attribute("calories", 650)
hub.set_attribute("recorded_at", datetime.now())

# Store complex data as JSON
meal_details = {
    "foods": [
        {"name": "Grilled chicken salad", "calories": 350, "protein_g": 35},
        {"name": "Whole grain roll", "calories": 150, "protein_g": 5},
        {"name": "Apple", "calories": 95, "protein_g": 0},
        {"name": "Water", "calories": 0, "protein_g": 0}
    ],
    "notes": "Patient reported feeling satisfied after meal"
}
hub.set_attribute("meal_details", meal_details)

# Store multiple attributes at once
hub.set_attributes({
    "total_protein_g": 40,
    "meal_location": "home",
    "logged_by": "patient_self_report"
})
```

## Retrieving Data from AttributeHub

Use the get-or-create pattern to retrieve existing hubs or create new ones:

```python
from canvas_sdk.v1.data import AttributeHub, Patient

patient = Patient.objects.get(id="patient-uuid-here")

# Get or create a hub for tracking daily calorie totals
hub, created = AttributeHub.objects.get_or_create(
    type="daily_calorie_summary",
    id=f"patient:{patient.id}:date:2024-01-15"
)

if created:
    # Initialize a new day's tracking
    hub.set_attributes({
        "total_calories": 0,
        "meal_count": 0,
        "calorie_goal": 2000
    })

# Retrieve attributes
total_calories = hub.get_attribute("total_calories")
meal_count = hub.get_attribute("meal_count")
calorie_goal = hub.get_attribute("calorie_goal")

# Handle missing attributes gracefully
notes = hub.get_attribute("daily_notes")  # Returns None if not set
```

## Querying AttributeHubs by Attribute Values

Find AttributeHubs based on the values stored in their attributes using `custom_attributes__value`.
The SDK automatically routes the filter to the correct typed column based on the Python type of the
value you pass in:

```python
from canvas_sdk.v1.data import AttributeHub

# Find hubs with a specific string attribute
lunch_hubs = AttributeHub.objects.filter(
    type="meal_entry",
    custom_attributes__name="meal_type",
    custom_attributes__value="lunch",
)

# Find hubs with a calorie count above a threshold
high_calorie = AttributeHub.objects.filter(
    type="meal_entry",
    custom_attributes__name="calories",
    custom_attributes__value__gte=500,
)

# Find hubs with a boolean flag
active_flags = AttributeHub.objects.filter(
    type="feature_flags",
    custom_attributes__name="enabled",
    custom_attributes__value=True,
)
```

You can also filter CustomAttribute objects directly, for example when working with a hub's
related attributes:

```python
hub = AttributeHub.objects.get(type="meal_entry", id="patient:abc:meal:2024-01-15T12:00")

# Filter the hub's own attributes
high_cal_attrs = hub.custom_attributes.filter(value__gte=500)
```

### When to Use Explicit Field Names

In most cases `custom_attributes__value` (or `value` on a hub's related attributes) is sufficient.
However, you must reference the typed column directly for:

- **JSON containment queries** (`json_value__contains`) — `value__contains` with a string targets
  `text_value`, not `json_value`. Use `json_value__contains` for PostgreSQL `@>` JSON containment.
- **Custom JSON lookups** like `json_value__has_key` or key-path access (`json_value__foods__0__name`).
- **Ambiguous types** — when the Python type of your filter value doesn't match the intended storage
  column (e.g., passing a string but querying `json_value`).
- **Null checks across relations** — `custom_attributes__value=None` and
  `custom_attributes__value__isnull` are not supported on `AttributeHub.objects.filter(...)` and
  will raise `TypeError`. Use the explicit column name instead (e.g.,
  `custom_attributes__text_value__isnull=True`). Direct queries on a hub's own attributes
  (`hub.custom_attributes.filter(value__isnull=True)`) are unaffected.

See [CustomAttributes — When to Use Explicit Field Names](/sdk/custom-data-custom-attributes/#when-to-use-explicit-field-names)
for a full discussion and examples.

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
            id=f"patient:{patient.id}:campaign:{campaign_id}"
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
            id=f"patient:{patient_id}:campaign:{campaign_id}"
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

## Best Practices

### Data Organization

1. **Use descriptive type values** - Choose meaningful type names that describe the purpose of the hub (e.g., "external_sync", "api_cache", "feature_flags")
2. **Use consistent ID patterns** - Use a consistent pattern for `id` (e.g., "entity_type:entity_id")
3. **Namespace by purpose** - Group related data under a single hub rather than creating multiple hubs for the same entity type

### Data Privacy and Isolation

1. **Understand plugin data scoping** - All AttributeHub data is isolated to your plugin's namespace
3. **Implement proper authorization** - Secure all APIs that expose AttributeHub data
4. **Follow PHI guidelines** - Treat all patient-related data with appropriate security measures

### Performance

2. **Batch attribute updates** - Use `set_attributes()` to set multiple values at once
3. **Cache hub lookups** - If accessing the same hub multiple times, store the reference

### Data Integrity

1. **Use get_or_create** - Use `get_or_create()` to avoid duplicate hubs
1. **Handle None values** - Always check if an attribute exists before using it
2. **Validate data** - Validate data before storing in AttributeHub
3. **Clean up unused data** - Remove AttributeHub instances that are no longer needed

### Testing

1. **Use get_or_create in tests** - This pattern works well for test isolation
3. **Isolate test data** - Create all data required by the test, within the test

## See Also

- [Custom Data Overview](/sdk/custom-data/) - Overview of all custom data techniques
- [CustomAttributes](/sdk/custom-data-custom-attributes/) - Flexible key-value attributes on existing models
- [CustomModels](/sdk/custom-data-custom-models/) - Structured models with relationships
- [Sharing Data](/sdk/custom-data-sharing-data/) - Sharing data among plugins
- [Testing Custom Data](/sdk/custom-data-testing/) - Testing utilities and examples
- [Data Models](/sdk/data/) - Core SDK data models
- [Caching API](/sdk/caching) - Auto-expiring transient data
- [Secrets](/sdk/secrets/) - Managing API keys and sensitive configuration

<br/>
<br/>
<br/>
