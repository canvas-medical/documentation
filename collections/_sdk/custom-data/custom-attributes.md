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

## Extending an SDK Model

Extend an existing SDK model by subclassing it along with `ModelExtension`. This enables CustomAttribute support
on model instances, allowing you to attach flexible key-value data without changing the base model.

```python
from canvas_sdk.v1.data import Staff, ModelExtension


class CustomStaff(Staff, ModelExtension):
    """Extends Staff with custom attribute support."""
    pass
```

You can name your class as you wish, but it **must**:
1. subclass a core model,
1. include `ModelExtension`.

The mixin automatically configures the class and assigns a manager for efficient attribute retrieval.
No `Meta` class or explicit manager assignment is needed.

## Setting Attributes

Set individual or multiple custom attributes on a model instance:

```python
from canvas_sdk.v1.data import Staff, Patient, ModelExtension


# Define extended models (typically in your plugin's models/__init__.py)
class CustomStaff(Staff, ModelExtension):
    pass


class CustomPatient(Patient, ModelExtension):
    pass


# Get model instances
staff = CustomStaff.objects.get(id="staff-uuid")
patient = CustomPatient.objects.get(id="patient-uuid")

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


class CustomStaff(Staff, ModelExtension):
    pass


staff = CustomStaff.objects.get(id="staff-uuid")

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


class CustomStaff(Staff, ModelExtension):
    pass


staff = CustomStaff.objects.get(id="staff-uuid")

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

Filter models by their custom attribute values using `custom_attributes__value`. The SDK automatically
routes the filter to the correct typed column based on the Python type of the value you pass in:

```python
from canvas_sdk.v1.data import Staff, ModelExtension


class CustomStaff(Staff, ModelExtension):
    pass


# String → text_value
cardiologists = CustomStaff.objects.filter(
    custom_attributes__name="specialty",
    custom_attributes__value="Cardiology",
)

# Integer → int_value
senior_staff = CustomStaff.objects.filter(
    custom_attributes__name="practicing_since",
    custom_attributes__value__lte=2010,
)

# Boolean → bool_value (not confused with int 0/1)
available = CustomStaff.objects.filter(
    custom_attributes__name="accepting_patients",
    custom_attributes__value=True,
)
```

Standard Django lookups (`__gte`, `__lte`, `__contains`, `__in`, `__isnull`, etc.) work with `value`:

```python
# Find staff whose bio mentions "cardiology"
CustomStaff.objects.filter(
    custom_attributes__name="bio",
    custom_attributes__value__contains="cardiology",
)

# Find staff with practicing since 2010 or earlier
CustomStaff.objects.filter(
    custom_attributes__name="practicing_since",
    custom_attributes__value__lte=2010,
)
```

### When to Use Explicit Field Names

In most cases `custom_attributes__value` is sufficient. However, there are situations where you must
reference the typed column (`text_value`, `json_value`, etc.) directly:

- **JSON containment queries.** PostgreSQL's `@>` containment operator on `jsonb` has different
  semantics from the `LIKE '%...%'` that `__contains` produces on a text column. Since `value__contains`
  with a string argument targets `text_value`, you must use `json_value__contains` to perform JSON
  containment checks:

  ```python
  from django.db.models import Q

  # Find staff whose "specialties" JSON array contains "Cardiology"
  CustomStaff.objects.filter(
      custom_attributes__name="specialties",
      custom_attributes__json_value__contains="Cardiology",
  )

  # OR across multiple JSON values
  specialty_filters = Q()
  for specialty in ["Cardiology", "Internal Medicine"]:
      specialty_filters |= Q(custom_attributes__json_value__contains=specialty)

  CustomStaff.objects.filter(
      Q(custom_attributes__name="specialties") & specialty_filters
  )
  ```

- **Ambiguous Python types.** The `value` rewriter uses `type()` (not `isinstance()`) to select
  the column. If you pass a string but intend to query `json_value` (or vice versa), the rewriter
  will target the wrong column. Use the explicit field name when the Python type of your filter
  value doesn't match the storage column.

- **Custom JSON lookups.** Django's `JSONField` supports lookups like `__has_key`, `__contained_by`,
  and key-path access (`json_value__key__nested`). These are only available on the `json_value`
  column directly.

- **Null checks across relations.** `custom_attributes__value=None` and
  `custom_attributes__value__isnull` are not supported on parent-model queries (e.g.,
  `CustomStaff.objects.filter(...)`) and will raise `TypeError`. Null checks require testing every
  typed column, which produces unreliable results when combined with Django's cross-relation JOIN
  machinery. Use explicit column names instead:

  ```python
  # Check whether a specific column is null across the relation
  CustomStaff.objects.filter(
      custom_attributes__name="specialty",
      custom_attributes__text_value__isnull=True,
  )
  ```

  Note that `value=None` and `value__isnull` *are* supported for direct CustomAttribute queries
  (e.g., `hub.custom_attributes.filter(value__isnull=True)`), where no cross-relation join is involved.

Refer to the [Supported Value Types](#supported-value-types) table above for the mapping between
Python types and database columns.

## Optimizing Queries with Prefetch

Reduce database queries by prefetching custom attributes. By default, the manager will prefetch all attributes
associated to the record.

```python
from canvas_sdk.v1.data import Staff, ModelExtension


class CustomStaff(Staff, ModelExtension):
    pass


# Prefetch all custom attributes
staff_list = CustomStaff.objects.all()  # Automatically prefetches

# Prefetch only specific attributes
staff = CustomStaff.objects.with_only("accepting_patients").get(id="staff-uuid")

# Prefetch multiple specific attributes
staff = CustomStaff.objects.with_only([
    "accepting_patients",
    "specialty",
    "years_experience"
]).get(id="staff-uuid")
```

## Deleting Attributes

Remove custom attributes when no longer needed:

```python
from canvas_sdk.v1.data import Staff, ModelExtension


class CustomStaff(Staff, ModelExtension):
    pass


staff = CustomStaff.objects.get(id="staff-uuid")

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

1. **Efficient manager is auto-assigned** - `ModelExtension` automatically configures the `objects` manager for efficient attribute retrieval
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
- [CustomModels](/sdk/custom-data-custom-models/) - Structured models with relationships
- [Sharing Data](/sdk/custom-data-sharing-data/) - Sharing data among plugins
- [Testing Custom Data](/sdk/custom-data-testing/) - Testing utilities and examples
- [Caching API](/sdk/caching) - Auto-expiring transient data
- [Data Models](/sdk/data/) - Core SDK data models

<br/>
<br/>
<br/>
