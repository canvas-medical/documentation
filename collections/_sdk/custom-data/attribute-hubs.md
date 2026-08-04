---
title: "AttributeHubs"
slug: "custom-data-attribute-hubs"
---

## Overview

`AttributeHubs` provide a simple mechanism for storing arbitrary data that doesn't belong to existing models,
or does not conform to a traditional database schema. An AttributeHub is merely a collection of named attributes with values.
This approach is ideal for cross-cutting concerns that span multiple models, temporary data storage, external system state tracking, 
data model prototyping, or plugin-specific configuration.

**Best for:**
- Cross-cutting state that spans multiple models (sync cursors, external IDs)
- One-off or small-collection configuration and state
- Data with no natural schema (varying fields per record)
- External system state tracking

**Example use cases:**
- API synchronization state
- External system identifiers
- Plugin configuration and feature flags

**Not ideal for** entities with relationships, large collections you need to search or paginate, or data
requiring aggregation or reporting. See [Design Considerations](/sdk/custom-data-design-considerations/) for
detailed guidance.

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

## Supported Value Types

Attributes are automatically stored in appropriately typed database columns. The column is
selected based on the Python type of the value you pass to `set_attribute()`:

```python
from datetime import date, datetime
from canvas_sdk.v1.data import AttributeHub

hub = AttributeHub.objects.get(type="staff_profile", id="staff_id:abc123")

# String values
hub.set_attribute("bio", "Board-certified cardiologist")

# Integer values
hub.set_attribute("patient_capacity", 100)

# Boolean values
hub.set_attribute("accepting_patients", True)

# Decimal values
hub.set_attribute("rating", 4.8)

# Date values
hub.set_attribute("creation_date", date.today())

# Datetime values
hub.set_attribute("last_updated", datetime.now())

# JSON/Complex objects (dicts, lists)
hub.set_attribute("preferences", {
    "notification_email": True,
    "notification_sms": False
})
```

| Field Name        | Python Type                  | Django Field Type | PostgreSQL Data Type       |
|-------------------|------------------------------|-------------------|----------------------------|
| `text_value`      | `str`                        | `TextField`       | `text`                     |
| `int_value`       | `int`                        | `IntegerField`    | `integer`                  |
| `bool_value`      | `bool`                       | `BooleanField`    | `boolean`                  |
| `decimal_value`   | `float`, `Decimal`           | `DecimalField`    | `decimal(20,10)`           |
| `date_value`      | `date`                       | `DateField`       | `date`                     |
| `timestamp_value` | `datetime`                   | `DateTimeField`   | `timestamp with time zone` |
| `json_value`      | `dict`, `list`               | `JSONField`       | `jsonb`                    |

These typed columns can be referenced directly in queries. See [When to Use Explicit Field Names](#when-to-use-explicit-field-names)
for cases where you need to target a specific column.

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

You can also filter attribute objects directly, for example when working with a hub's
related attributes:

```python
from canvas_sdk.v1.data import AttributeHub

hub = AttributeHub.objects.get(type="meal_entry", id="patient:abc:meal:2024-01-15T12:00")

# Filter the hub's own attributes
high_cal_attrs = hub.custom_attributes.filter(value__gte=500)
```

### When to Use Explicit Field Names

In most cases `custom_attributes__value` (or `value` on a hub's related attributes) is sufficient.
However, you must reference the typed column directly in the following cases:

- **JSON containment queries.** PostgreSQL's `@>` containment operator on `jsonb` has different
  semantics from the `LIKE '%...%'` that `__contains` produces on a text column. Since `value__contains`
  with a string argument targets `text_value`, you must use `json_value__contains` to perform JSON
  containment checks:

  ```python
  from django.db.models import Q
  from canvas_sdk.v1.data import AttributeHub

  # Find hubs whose "specialties" JSON array contains "Cardiology"
  AttributeHub.objects.filter(
      type="staff_profile",
      custom_attributes__name="specialties",
      custom_attributes__json_value__contains="Cardiology",
  )

  # OR across multiple JSON values
  specialty_filters = Q()
  for specialty in ["Cardiology", "Internal Medicine"]:
      specialty_filters |= Q(custom_attributes__json_value__contains=specialty)

  AttributeHub.objects.filter(
      Q(custom_attributes__name="specialties") & specialty_filters
  )
  ```

- **Custom JSON lookups.** Django's `JSONField` supports lookups like `__has_key`, `__contained_by`,
  and key-path access (`json_value__key__nested`). These are only available on the `json_value`
  column directly.

- **Ambiguous Python types.** The `value` rewriter uses `type()` (not `isinstance()`) to select
  the column. If you pass a string but intend to query `json_value` (or vice versa), the rewriter
  will target the wrong column. Use the explicit field name when the Python type of your filter
  value doesn't match the storage column.

- **Null checks across relations.** `custom_attributes__value=None` and
  `custom_attributes__value__isnull` are not supported on `AttributeHub.objects.filter(...)` and
  will raise `TypeError`. Null checks require testing every typed column, which produces unreliable
  results when combined with Django's cross-relation JOIN machinery. Use explicit column names instead:

  ```python
  from canvas_sdk.v1.data import AttributeHub

  # Check whether a specific column is null across the relation
  AttributeHub.objects.filter(
      type="staff_profile",
      custom_attributes__name="specialty",
      custom_attributes__text_value__isnull=True,
  )
  ```

  Note that `value=None` and `value__isnull` *are* supported for direct queries on a hub's own
  attributes (e.g., `hub.custom_attributes.filter(value__isnull=True)`), where no cross-relation
  join is involved.

Refer to [Supported Value Types](#supported-value-types) for the mapping between Python types and
database columns.

## Optimizing Queries with Prefetch

By default, the AttributeHub manager prefetches all custom attributes when you query hubs. This means
accessing `hub.get_attribute(...)` after a query does not trigger additional database queries:

```python
from canvas_sdk.v1.data import AttributeHub

# All custom attributes are prefetched automatically
hubs = AttributeHub.objects.filter(type="meal_entry")
for hub in hubs:
    # No additional queries — attributes are already loaded
    meal_type = hub.get_attribute("meal_type")
    calories = hub.get_attribute("calories")
```

### Prefetching Specific Attributes

When a hub has many attributes but you only need a few, use `with_only()` to prefetch only the
attributes you need. This reduces the amount of data transferred from the database:

```python
from canvas_sdk.v1.data import AttributeHub

# Prefetch only the "calories" and "meal_type" attributes
hubs = AttributeHub.objects.with_only(["calories", "meal_type"]).filter(type="meal_entry")
for hub in hubs:
    calories = hub.get_attribute("calories")       # Loaded from prefetch cache
    meal_type = hub.get_attribute("meal_type")     # Loaded from prefetch cache
    notes = hub.get_attribute("notes")             # Falls back to a DB query (not prefetched)

# Prefetch a single attribute
hub = AttributeHub.objects.with_only("campaign_status").get(
    type="crm_sync", id="patient:abc123"
)
```

If you access an attribute that was not included in `with_only()`, it will fall back to a database
query. Use `with_only()` as an optimization, not a filter.

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
            "last_synced": datetime.now(),
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
- [Design Considerations](/sdk/custom-data-design-considerations/) - Choosing the right technique and avoiding anti-patterns
- [CustomModels](/sdk/custom-data-custom-models/) - Structured models with relationships
- [Sharing Data](/sdk/custom-data-sharing-data/) - Sharing data among plugins
- [Testing Custom Data](/sdk/custom-data-testing/) - Testing utilities and examples
- [Data Models](/sdk/data/) - Core SDK data models
- [Caching API](/sdk/caching) - Auto-expiring transient data
- [Secrets](/sdk/secrets/) - Managing API keys and sensitive configuration

<br/>
<br/>
<br/>
