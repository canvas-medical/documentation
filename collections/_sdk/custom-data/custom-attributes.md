---
title: "CustomAttributes on Proxy Models"
slug: "custom-attributes"
---

## Overview

CustomAttributes allow you to extend existing SDK models (like Patient or Staff) with flexible key-value attributes without defining a formal schema. This approach is ideal for storing variable configuration data, rapid prototyping, or simple key-value associations with core models.

**Best for:**
- Storing variable or configuration data on existing models
- Rapid prototyping
- Data that doesn't require strict typing
- Simple key-value associations with core models

**Example use cases:**
- Adding practice-specific flags to patients
- Storing provider preferences
- Temporary or experimental data fields

---

## Creating a Proxy Model

Extend existing SDK models by creating a proxy class that adds CustomAttribute support.

```python
from canvas_sdk.v1.data import Staff, Patient, CustomAttributeMixin, CustomAttributeAwareManager


class StaffProxy(Staff, CustomAttributeMixin):
    """A proxy for Staff with CustomAttribute capabilities"""
    class Meta:
        proxy = True

    # This model manager is necessary efficient retrieval of attributes
    objects = CustomAttributeAwareManager()


class PatientProxy(Patient):
    """A proxy for Patient without custom attributes, for use in associating Patients to CustomModels"""
    class Meta:
        proxy = True
```

You can name your proxy class as you wish, but it **must** subclass a core model,
and declare `proxy = True`.

---

## Setting Attributes

Set individual or multiple custom attributes on a model instance:

```python
from canvas_sdk.v1.data import Staff, Patient
from canvas_sdk.v1.data import CustomAttributeMixin, CustomAttributeAwareManager


# Define proxy models (typically in your plugin's models.py)
class StaffProxy(Staff, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


class PatientProxy(Patient, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


# Get model instances
staff = StaffProxy.objects.get(id="staff-uuid")
patient = PatientProxy.objects.get(id="patient-uuid")

# Set a single attribute
staff.set_attribute("specialty", "Cardiology")
patient.set_attribute("preferred_language", "Spanish")

# Set multiple attributes at once
staff.set_attributes({
    "board_certified": True,
    "years_experience": 15,
    "accepting_new_patients": False
})
```

---

## Getting Attributes

Retrieve custom attribute values by name:

```python
from canvas_sdk.v1.data import Staff, CustomAttributeMixin, CustomAttributeAwareManager


class StaffProxy(Staff, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


staff = StaffProxy.objects.get(id="staff-uuid")

# Get a single attribute
specialty = staff.get_attribute("specialty")  # Returns "Cardiology"

# Returns None if attribute doesn't exist
unknown = staff.get_attribute("nonexistent")  # Returns None
```

---

## Supported Value Types

CustomAttributes automatically handle multiple data types:

```python
from datetime import datetime
from canvas_sdk.v1.data import Staff, CustomAttributeMixin, CustomAttributeAwareManager


class StaffProxy(Staff, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


staff = StaffProxy.objects.get(id="staff-uuid")

# String values
staff.set_attribute("bio", "Board-certified cardiologist")

# Integer values
staff.set_attribute("patient_capacity", 100)

# Boolean values
staff.set_attribute("accepting_patients", True)

# Decimal values
staff.set_attribute("rating", 4.8)

# Datetime values
staff.set_attribute("last_updated", datetime.now())

# JSON/Complex objects
staff.set_attribute("preferences", {
    "notification_email": True,
    "notification_sms": False
})
```

---

## Querying by CustomAttributes

Filter models by their custom attributes:

```python
from django.db.models import Q
from canvas_sdk.v1.data import Staff, CustomAttributeMixin, CustomAttributeAwareManager


class StaffProxy(Staff, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


# Find staff with specific specialty
cardiologists = (
    StaffProxy.objects
    .filter(
        custom_attributes__name="specialty",
        custom_attributes__text_value="Cardiology"
    )
    .all()
)

# Find staff with multiple specialties using OR conditions
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

---

## Optimizing Queries with Prefetch

Reduce database queries by prefetching custom attributes:

```python
from canvas_sdk.v1.data import Staff, CustomAttributeMixin, CustomAttributeAwareManager


class StaffProxy(Staff, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


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

---

## Deleting Attributes

Remove custom attributes when no longer needed:

```python
from canvas_sdk.v1.data import Staff, CustomAttributeMixin, CustomAttributeAwareManager


class StaffProxy(Staff, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


staff = StaffProxy.objects.get(id="staff-uuid")

# Delete a single attribute
deleted = staff.delete_attribute("old_field")  # Returns True if deleted

# Check if deletion was successful
if deleted:
    print("Attribute removed")
```

---

## Best Practices

### Model Design

1. **Use proxy models** for adding CustomAttributes to existing SDK models
2. **Include CustomAttributeAwareManager** - Always use `CustomAttributeAwareManager()` as the objects manager for efficient attribute retrieval
3. **Use related_name** for clear reverse relation access when using CustomAttributes with foreign keys

### Data Privacy and Isolation

1. **Understand plugin data scoping** - All custom data is isolated to your plugin by default
2. **Use APIs for data sharing** - Never attempt to access another plugin's data directly
3. **Implement proper authorization** - Secure all APIs that expose plugin data
4. **Follow PHI guidelines** - Treat all patient-related custom data with appropriate security measures

### Performance

1. **Prefetch related data** to avoid N+1 query problems
2. **Use select_related** for foreign key lookups
3. **Filter at the database level** rather than in Python
4. **Use with_only()** to prefetch only specific attributes when you don't need all custom attributes

### Data Integrity

1. **Validate data** before saving custom attributes
2. **Handle None values** when accessing attributes that may not exist
3. **Use get_or_create** to avoid duplicate records

### Testing

1. **Use factories** to create test data consistently
2. **Test relationship queries** in both directions
3. **Test with and without prefetching** to ensure correct behavior

---

## See Also

- [Custom Data Overview](/sdk/custom-data/) - Overview of all custom data techniques
- [AttributeHubs](/sdk/custom-data/attribute-hub/) - Standalone key-value storage
- [Custom Data Models](/sdk/custom-data/custom-models/) - Structured models with relationships
- [Testing Custom Data](/sdk/custom-data/testing/) - Testing utilities and examples
- [Data Models](/sdk/data/) - Core SDK data models
- [Canvas CLI](/sdk/canvas_cli/#simple-api-endpoints) - Simple API for sharing data between plugins
- [Secrets](/sdk/secrets/) - Managing API keys and sensitive configuration
