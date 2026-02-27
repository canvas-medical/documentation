---
title: "CustomAttributes for SDK Models"
slug: "custom-data-custom-attributes"
---

## Overview

CustomAttributes allow you to extend existing SDK models (like Patient or Staff) with flexible key-value attributes 
without defining a formal schema. This approach is ideal for storing variable configuration data, rapid prototyping, 
or simple key-value associations with core models.

**Best for:**
- Storing variable or configuration data on existing models
- Rapid prototyping
- Data that doesn't require strict typing
- Simple key-value associations with core models

**Example use cases:**
- Adding practice-specific flags or identifiers to patients
- Storing provider preferences
- Temporary or experimental data fields

## Creating a Proxy for the SDK Model

CustomAttributes attach to a "proxy" of a core SDK model. A proxy is a Django ORM model that extends another model 
and allows customizations without changing the base model. It cannot define new database fields, but inherits all
of those from its base model.

Extend existing SDK models by subclassing the SDK model and `ModelExtension`. The latter adds CustomAttribute support
and sets up the proxy relationship.

```python
from canvas_sdk.v1.data import Staff, ModelExtension


class StaffProxy(Staff, ModelExtension):
    """A proxy for Staff with CustomAttribute capabilities"""
    pass
```

You can name your proxy class as you wish, but it **must**:
1. subclass a core model,
1. include `ModelExtension`.

The mixin automatically configures the class as a Django proxy model and assigns a `CustomAttributeAwareManager`
as the `objects` manager for efficient attribute retrieval. No `Meta` class or explicit manager assignment is needed.

## Setting Attributes

Set individual or multiple custom attributes on a model instance:

```python
from canvas_sdk.v1.data import Staff, Patient, ModelExtension


# Define proxy models (typically in your plugin's models.py)
class StaffProxy(Staff, ModelExtension):
    pass


class PatientProxy(Patient, ModelExtension):
    pass


# Get model instances
staff = StaffProxy.objects.get(id="staff-uuid")
patient = PatientProxy.objects.get(id="patient-uuid")

# Set a single attribute
staff.set_attribute("specialty", "Cardiology")
patient.set_attribute("preferred_language", "Spanish")

# Set multiple attributes at once
staff.set_attributes({
    "practicing_since": 2005,
    "accepting_new_patients": False,
    "languages": ["English", "Spanish"]
})
```

Setting attributes in bulk via `set_attributes` will be more performant with larger numbers of individual attributes.

## Getting Attributes

Retrieve custom attribute values by name:

```python
from canvas_sdk.v1.data import Staff, ModelExtension


class StaffProxy(Staff, ModelExtension):
    pass


staff = StaffProxy.objects.get(id="staff-uuid")

# Get a single attribute
specialty = staff.get_attribute("specialty")  # Returns "Cardiology"

# Returns None if attribute doesn't exist
unknown = staff.get_attribute("nonexistent")  # Returns None
```

## Supported Value Types

CustomAttributes automatically handle multiple data types:

```python
from datetime import date, datetime
from canvas_sdk.v1.data import Staff, ModelExtension


class StaffProxy(Staff, ModelExtension):
    pass


staff = StaffProxy.objects.get(id="staff-uuid")

# String values
staff.set_attribute("bio", "Board-certified cardiologist")

# Integer values
staff.set_attribute("patient_capacity", 100)

# Boolean values
staff.set_attribute("accepting_patients", True)

# Decimal values
staff.set_attribute("rating", 4.8)

# Date values
staff.set_attribute("creation_date", date.today())

# Datetime values
staff.set_attribute("last_updated", datetime.now())

# JSON/Complex objects
staff.set_attribute("preferences", {
    "notification_email": True,
    "notification_sms": False
})
```

Values are stored in appropriately typed columns for the value, and these columns may be referenced in queries.

| Field Name        | Django Field Type | PostgreSQL Data Type       |
|-------------------|-------------------|----------------------------|
| `text_value`      | `TextField`       | `text`                     |
| `date_value`      | `DateField`       | `date`                     |
| `timestamp_value` | `DateTimeField`   | `timestamp with time zone` |
| `int_value`       | `IntegerField`    | `integer`                  |
| `decimal_value`   | `DecimalField`    | `decimal(20,10)`           |
| `json_value`      | `JSONField`       | `jsonb`                    |
| `bool_value`      | `BooleanField`    | `boolean`                  |


## Querying by CustomAttributes

Filter models by their custom attributes:

```python
from django.db.models import Q
from canvas_sdk.v1.data import Staff, ModelExtension


class StaffProxy(Staff, ModelExtension):
    pass


# Find staff with a specific specialty assigned as a text value
cardiologists = (
    StaffProxy.objects
    .filter(
        custom_attributes__name="specialty",
        custom_attributes__text_value="Cardiology"
    )
    .all()
)

# Find staff with multiple specialties assigned using a JSON array using OR conditions
specialties = ["Cardiology", "Internal Medicine"]
specialty_filters = Q()
for specialty in specialties:
    specialty_filters |= Q(custom_attributes__json_value__contains=specialty)

matching_staff = (
    StaffProxy.objects
    .filter(Q(custom_attributes__name="specialties") & specialty_filters)
    .all()
)
```

## Optimizing Queries with Prefetch

Reduce database queries by prefetching custom attributes with the `CustomAttributeAwareManager` model manager. By default,
this manager will prefetch all attributes associated to the record.

```python
from canvas_sdk.v1.data import Staff, ModelExtension


class StaffProxy(Staff, ModelExtension):
    pass


# Prefetch all custom attributes
staff_list = StaffProxy.objects.all()  # Automatically prefetches

# Prefetch only specific attributes
staff = StaffProxy.objects.with_only("accepting_patients").get(id="staff-uuid")

# Prefetch multiple specific attributes
staff = StaffProxy.objects.with_only([
    "accepting_patients",
    "specialty",
    "years_experience"
]).get(id="staff-uuid")
```

## Deleting Attributes

Remove custom attributes when no longer needed:

```python
from canvas_sdk.v1.data import Staff, ModelExtension


class StaffProxy(Staff, ModelExtension):
    pass


staff = StaffProxy.objects.get(id="staff-uuid")

# Delete a single attribute
deleted = staff.delete_attribute("old_field")  # Returns True if deleted

# Check if deletion was successful
if deleted:
    print("Attribute removed")
```

## Best Practices

### Data Privacy and Isolation

1. **Understand plugin data scoping** - All custom data is isolated to your plugin's namespace by default
2. **Implement proper authorization** - Secure all APIs that expose plugin data
3. **Follow PHI guidelines** - Treat all patient-related custom data with appropriate security measures

### Performance

1. **CustomAttributeAwareManager is auto-assigned** - The mixin automatically assigns `CustomAttributeAwareManager()` as the `objects` manager for efficient attribute retrieval
2. **Filter at the database level** rather than in Python
3. **Use with_only()** to prefetch only specific attributes when you don't need all custom attributes

### Data Integrity

1. **Validate data** before saving custom attributes
2. **Handle None values** when accessing attributes that may not exist

### Testing

1. **Use factories** to create test data consistently
2. **Isolate test data** - Create all data required by the test, within the test

## See Also

- [Custom Data Overview](/sdk/custom-data/) - Overview of all custom data techniques
- [AttributeHubs](/sdk/custom-data-attribute-hubs/) - Standalone key-value storage
- [Custom Data Models](/sdk/custom-data-custom-models/) - Structured models with relationships
- [Sharing Data](/sdk/custom-data-sharing-data/) - Sharing data among plugins
- [Testing Custom Data](/sdk/custom-data-testing/) - Testing utilities and examples
- [Caching API](/sdk/caching) - Auto-expiring transient data
- [Data Models](/sdk/data/) - Core SDK data models

<br/>
<br/>
<br/>
