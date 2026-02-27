---
title: "Custom Data Models"
slug: "custom-data-custom-models"
---

## Overview

Custom Data Models allow you to define fully structured, typed data models with relationships among entities and normalized data. 
Built on Django's ORM, Custom Models provide the most powerful and flexible approach to storing custom data in Canvas plugins.

The functionality expressed is a subset of the total ORM. The SDK omits some features in order to simplify the lifecycle 
of plugin installation and maintenance.

**Best for:**
- Complex domain models
- Data requiring validation and normalization
- Relational data with foreign keys
- Performance-critical queries

**Example use cases:**
- Provider specialties and certifications
- Custom workflows and forms
- Integration-specific data structures
- Practice-specific business entities

Custom models may be associated to core SDK data models via proxy classes, or may be entirely standalone.

Custom models must be defined within a `models` directory under the plugin top-level directory. E.g., `/my_plugin/models/custom_model_a.py`. 
If not, then database migrations will not be applied. (Proxy models may be defined anywhere since they do not require any database modifications.)

---

## Basic Custom Model

Create a custom model by extending `CustomModel`:

```python
from canvas_sdk.v1.data.base import CustomModel
from django.db.models import BooleanField, DateField, DateTimeField, DecimalField, IntegerField, JSONField, TextField 


class HealthCoach(CustomModel):

    name = TextField()
    practicing_since = IntegerField()
    version = DecimalField(default=1.0, decimal_places=1, max_digits=3)
    is_accepting_patients = BooleanField()
    created_date = DateField(auto_now_add=True)
    last_modified_at = DateTimeField(auto_now_add=True)
    extended_attributes = JSONField()    
 ```

This above definition will result in a PostgreSQL table named `healthcoach`. It will have a primary key
column named `dbid` of type `serial`, an auto-incrementing integer. It will have six additional columns
of `text`, `integer`, `numeric(3,8)`, `boolean`, `jsonb`,`date`, and `timestamp with time zone`, respectively.

---

## Schema Rules and Constraints

To maintain safety on potentially large datasets, constraints on CustomModels are not enforced within the database. 
They must be enforced within plugin code.

Unsupported contraints
* `not null`
* `unique`
* `max_length`
* `references`

If applied to an existing dataset, some constraints could result in a full table rewrite operation, or prevent
plugin installation.

### Field Types

The Canvas SDK provides Django-based field types for defining your models:

| Field Type        | Description               | Supported Parameters                     |
|-------------------|---------------------------|------------------------------------------|
| `TextField`       | Variable-length text      | `default`                                |
| `IntegerField`    | Integer values            | `default`                                |
| `DecimalField`    | Decimal numbers           | `default`, `max_digits`,`decimal_places` |
| `BooleanField`    | True/False values         | `default`                                |
| `DateField`       | Date values               | `auto_now`, `auto_now_add`, `default`    |
| `DateTimeField`   | Date and time values      | `auto_now`, `auto_now_add`, `default`    |
| `JSONField`       | JSON-serializable data    | `default`                                |
| `ForeignKey`      | Many-to-one relationship  | `related_name`, `on_delete=DO_NOTHING`   |
| `OneToOneField`   | One-to-one relationship   | `related_name`, `on_delete=DO_NOTHING`   |

If `default` is supplied it will be applied by the Django ORM, and will not be a PostgreSQL default. 
As a result, only new records will receive the value, and it will not cause a mass edit of existing records.

Note: `on_delete=CASCADE` is unsupported because it relies upon database-level foreign key constraints
which are not implemented at this time. Plugins are responsible for maintaining data integrity and
preventing orphaned records during delete operations.

### Indexes

Add indexes for frequently queried fields:

```python
from canvas_sdk.v1.data.base import CustomModel
from django.contrib.postgres.indexes import GinIndex
from django.db.models import BooleanField, DateTimeField, Index, IntegerField, JSONField, TextField 


class ProviderQualification(CustomModel):

    first_name = TextField()
    last_name = TextField()
    board_certified = BooleanField()
    practicing_since_year = IntegerField()
    degrees = JSONField()
    created_at = DateTimeField()
    
    class Meta:
        indexes = [
            # Single-column index
            Index(fields=["practicing_since_year"]),
            # Composite index for common search combinations
            Index(fields=["first_name", "last_name"]),
            # Descending index for ordering records
            Index(fields=["-created_at"]),
            # Gin index for efficient JSON queries
            GinIndex(fields=["extended_attributes"])
        ]
```

**Index Best Practices:**
- Index fields used in `filter()` and `order_by()`
- Create composite indexes for common multi-field queries
- Foreign key fields are indexed automatically

---

## Creating and Querying

### Creating Records

```python
from my_plugin.models import ProviderQualification


# Create and save
qualification = ProviderQualification(
    first_name="Jessica",
    last_name="Smith",
    board_certified=True,
    practicing_since_year=2005,
    extended_attribtes={ "biography": "Lives in Fresno with her..." }
)
qualification.save()

# Create in one step
qualification = ProviderQualification.objects.create(
    first_name="Jessica",
    last_name="Smith",
    board_certified=True,
    practicing_since_year=2005,
    extended_attribtes={ "biography": "Lives in Fresno with her..." }
)

# Get or create (avoids duplicates)
qualification = ProviderQualification.objects.get_or_create(
    first_name="Jessica",
    last_name="Smith",
    defaults={
        "board_certified": True,
        "practicing_since_year": 2005,
        "extended_attributes": { "biography": "Lives in Fresno with her..." }
    }
)
```

### Querying Records

```python
from my_plugin.models import ProviderQualification
from datetime import date

# Get all records
all_qualifications = ProviderQualification.objects.all()

# Filter records
board_certified = ProviderQualification.objects.filter(board_certified=True)

# Get providers with 10+ years experience 
experienced = ProviderQualification.objects.filter(
    practicing_since_year__lte=date.today().year - 10
)

# Get single record by database primary key
try:
    jessica = ProviderQualification.objects.get(dbid=123)
except ProviderQualification.DoesNotExist:
    jessica = None

# Get single record by fields
try:
    jessica = ProviderQualification.objects.get(first_name="Jessica", last_name="Smith")
except ProviderQualification.DoesNotExist:
    jessica = None

# Apply multiple filters
senior_certified = ProviderQualification.objects.filter(
    board_certified=True,
    practicing_since_year__lte=2010  # Practicing since 2010 or earlier
)

# Order results
by_experience = ProviderQualification.objects.order_by("practicing_since_year")

# Limit results - get 5 most experienced (earliest practicing_since_year)
top_five = ProviderQualification.objects.order_by("practicing_since_year")[:5]
```

### Updating Records

```python
from my_plugin.models import ProviderQualification


# Update single record
qualification = ProviderQualification.objects.get(first_name="Jessica", last_name="Smith")
qualification.practicing_since_year = 2004
qualification.save()

# Update multiple records
ProviderQualification.objects.filter(
    board_certified=False
).update(board_certified=True)

# Update or create
qualification, created = ProviderQualification.objects.update_or_create(
    first_name="Michael",
    last_name="Johnson",
    defaults={
        "board_certified": True,
        "practicing_since_year": 2015,
        "extended_attributes": { "specialties": ["Cardiology", "Internal Medicine"] }
    }
)
```

### Deleting Records

```python
from my_plugin.models import ProviderQualification


# Delete single record
qualification = ProviderQualification.objects.get(first_name="Jessica", last_name="Smith")
qualification.delete()

# Delete multiple records - remove providers who started this year
from datetime import date
ProviderQualification.objects.filter(
    practicing_since_year=date.today().year
).delete()

# Delete all records (use with caution!)
ProviderQualification.objects.all().delete()
```

## Extend Canvas Data Model using Proxy Models

CustomModels may attach to a "proxy" of a core SDK model. A proxy is a Django ORM model that extends another model 
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

The mixin automatically configures the class as a Django proxy model.

---

## One-to-One Relationships

A one-to-one relationship links one record in a model to exactly one record in another model. 
Use `OneToOneField` to define this relationship.

### Basic One-to-One

```python
from canvas_sdk.v1.data import Staff, ModelExtension
from canvas_sdk.v1.data.base import CustomModel
from django.db.models import DateTimeField, DecimalField, DO_NOTHING, OneToOneField, TextField


class StaffProxy(Staff, ModelExtension):
    """Proxy for Staff to use with custom models."""
    pass

class Biography(CustomModel):

    biography = TextField()
    language = TextField()
    version = DecimalField(default=1.0, decimal_places=1, max_digits=3)
    last_modified_at = DateTimeField(auto_now_add=True)

    staff = OneToOneField(
        StaffProxy, to_field="dbid", on_delete=DO_NOTHING, related_name="biography"
    )
```

The above will create a table with a `serial` primary key, two `text` columns, a `numeric(1,3)` column, a `timestamptz` column, 
and an `integer` column named `staff_id` that contains a foreign key into the SDK `Staff` model. The `StaffProxy` class 
defined in this plugin will contain the reverse mapping via `related_name`.

### Creating One-to-One Records

```python
from my_plugin.models import StaffProxy, Biography

# Get the staff member
staff = StaffProxy.objects.get(id="staff-uuid")

# Create biography
biography = Biography.objects.create(
    staff=staff,
    biography="Dr. Smith is a board-certified cardiologist with over 20 years of experience...",
    language="English",
    version=1.0
)
```

### Querying One-to-One Relationships

```python
from my_plugin.models import StaffProxy, Biography


# Access from biography to staff
biography = Biography.objects.get(dbid=1)
staff_member = biography.staff

# Access from staff to biography (using related_name)
staff = StaffProxy.objects.get(id="staff-uuid")
try:
    bio = staff.biography
except Biography.DoesNotExist:
    print("No biography found")

# Find all staff with biographies in Spanish
spanish_providers = StaffProxy.objects.filter(
    biography__language="Spanish"
)

# Find staff whose biography was last updated before a certain date
from datetime import datetime, timedelta

outdated_bios = StaffProxy.objects.filter(
    biography__last_modified_at__lte=datetime.now() - timedelta(days=365)
)
```

---

## One-to-Many Relationships

A one-to-many (or many-to-one) relationship allows one record to be associated with multiple records in another model. 
Use `ForeignKey` to define this relationship.

### Basic One-to-Many

```python
from canvas_sdk.v1.data import Staff, ModelExtension
from canvas_sdk.v1.data.base import CustomModel
from django.db.models import DateTimeField, DecimalField, DO_NOTHING, ForeignKey, TextField


class StaffProxy(Staff, ModelExtension):
  """Proxy for Staff to use with custom models."""
  pass

class Biography(CustomModel):
  biography = TextField()
  language = TextField()
  version = DecimalField(default=1.0, decimal_places=1, max_digits=3)
  last_modified_at = DateTimeField(auto_now_add=True)

  # Same as one-to-one, but a Foreign key with a plural 'related_name'. Now, each staff may have multiple biographies,
  # perhaps in different languages.
  staff = ForeignKey(
    StaffProxy, to_field="dbid", on_delete=DO_NOTHING, related_name="biographies"
  )
```

### Creating One-to-Many Records

```python
from plugins.my_plugin.models import StaffProxy, Biography


# Get staff member
staff = StaffProxy.objects.get(id="staff-uuid")

# Create multiple biographies for one provider (e.g., in different languages)
english_bio = Biography.objects.create(
    staff=staff,
    biography="Dr. Smith is a board-certified cardiologist with over 20 years of experience in interventional cardiology.",
    language="English",
    version=1.0
)

spanish_bio = Biography.objects.create(
    staff=staff,
    biography="La Dra. Smith es una cardióloga certificada con más de 20 años de experiencia en cardiología intervencionista.",
    language="Spanish",
    version=1.0
)
```

### Querying One-to-Many Relationships

```python
from plugins.my_plugin.models import StaffProxy, Biography


# Access from biography to staff (forward)
biography = Biography.objects.get(language="Spanish")
provider = biography.staff
print(f"Provider: {provider.first_name} {provider.last_name}")

# Access from staff to biographies (reverse, using related_name)
staff = StaffProxy.objects.get(id="staff-uuid")
biographies = staff.biographies.all()
for bio in biographies:
    print(f"- {bio.language}: {bio.biography[:50]}... (v{bio.version})")

# Filter reverse relationship
english_bios = staff.biographies.filter(language="English")

# Query across relationship
# Find all staff who have biographies in Spanish
spanish_speaking_providers = StaffProxy.objects.filter(
    biographies__language="Spanish"
)

# Find staff with multiple biography versions
from django.db.models import Count

providers_with_multiple_bios = StaffProxy.objects.annotate(
    bio_count=Count('biographies')
).filter(bio_count__gt=1)

# Count related records
biography_count = staff.biographies.count()

# Check existence
has_spanish_bio = staff.biographies.filter(language="Spanish").exists()
```


---

## Many-to-Many Relationships

A many-to-many relationship allows multiple records in one model to be associated with multiple records in another model.

### Many-to-Many with Through Model

Many-to-many relationships are implemented using an explicit through model (also called a join table or junction table).
The through model contains ForeignKey fields to both sides of the relationship.

In the example above, `StaffSpecialty` is the through model that creates the many-to-many relationship 
between `StaffProxy` and `Specialty`.

`StaffSpecialty` may include additional fields to describe the nature of the association between `Staff` and `Specialty`.

The Canvas SDK does **not** support the Django `ManyToManyField` at this time.

```python
from django.db.models import ForeignKey, Index, TextField, DO_NOTHING
from canvas_sdk.v1.data.base import CustomModel
from canvas_sdk.v1.data import Staff, ModelExtension


class StaffProxy(Staff, ModelExtension):
  """Proxy for Staff to use with custom models."""
  pass

class Specialty(CustomModel):
  """Medical specialty (e.g., Cardiology, Neurology)."""

  name = TextField()

  class Meta:
    indexes = [
      Index(fields=["name"]),
    ]


# Declaring this class will result in a join table called `staffspecialty`
class StaffSpecialty(CustomModel):
  """Many-to-many relationship: Staff can have many specialties, specialties can have many staff."""

  staff = ForeignKey(
    StaffProxy,
    to_field="dbid",
    on_delete=DO_NOTHING,
    related_name="staff_specialties"
  )
  specialty = ForeignKey(
    Specialty,
    to_field="dbid",
    on_delete=DO_NOTHING,
    related_name="staff_specialties"
  )
```

This creates a many-to-many relationship where:
- One staff member can have multiple specialties
- One specialty can be assigned to multiple staff members
- `StaffSpecialty` is the through model that connects them

### Creating Many-to-Many Records

```python
from my_plugin.models import StaffProxy, Specialty, StaffSpecialty


# Create specialties
cardiology = Specialty.objects.create(name="Cardiology")
internal_medicine = Specialty.objects.create(name="Internal Medicine")
emergency_medicine = Specialty.objects.create(name="Emergency Medicine")

# Get staff member
staff = StaffProxy.objects.get(id="staff-uuid")

# Create associations between staff and specialties
StaffSpecialty.objects.create(staff=staff, specialty=cardiology)
StaffSpecialty.objects.create(staff=staff, specialty=internal_medicine)

# Bulk create multiple associations at once
specialties_to_add = [emergency_medicine, cardiology]
staff_specialties = [
    StaffSpecialty(staff=staff, specialty=specialty) for specialty in specialties_to_add
]
StaffSpecialty.objects.bulk_create(staff_specialties)

# Replace all specialties for a staff member
# First, remove existing associations
StaffSpecialty.objects.filter(staff=staff).delete()

# Then create new associations
new_specialties = [cardiology, emergency_medicine]
new_staff_specialties = [
    StaffSpecialty(staff=staff, specialty=specialty) for specialty in new_specialties
]
StaffSpecialty.objects.bulk_create(new_staff_specialties)
```

### Querying Many-to-Many Relationships

```python
from plugins.my_plugin.models import StaffProxy, Specialty, StaffSpecialty


# Access staff member's specialties through the join table
staff = StaffProxy.objects.get(id="staff-uuid")
staff_specialty_records = staff.staff_specialties.all()
for staff_specialty in staff_specialty_records:
    print(f"- {staff_specialty.specialty.name}")

# Get just the specialty names
specialty_names = [ss.specialty.name for ss in staff.staff_specialties.all()]

# Access all staff members with a specific specialty (reverse)
cardiology = Specialty.objects.get(name="Cardiology")
cardiology_staff_records = cardiology.staff_specialties.all()
for staff_specialty in cardiology_staff_records:
    staff_member = staff_specialty.staff
    print(f"- {staff_member.first_name} {staff_member.last_name}")

# Find staff IDs with specific specialties
staff_ids = StaffSpecialty.objects.filter(
    specialty__name__in=["Cardiology", "Internal Medicine"]
).values_list("staff_id", flat=True)

# Find staff members with a specific specialty
cardiologists = StaffProxy.objects.filter(
    staff_specialties__specialty__name="Cardiology"
).distinct()

# Check if a staff member has a specific specialty
has_cardiology = staff.staff_specialties.filter(specialty__name="Cardiology").exists()

# Count specialties for a staff member
specialty_count = staff.staff_specialties.count()

# Efficient querying with prefetch_related
staff_with_specialties = (
    StaffProxy.objects
    .prefetch_related("staff_specialties__specialty")
    .all()
)
for staff in staff_with_specialties:
    specialties = [ss.specialty.name for ss in staff.staff_specialties.all()]
    print(f"{staff.first_name} {staff.last_name}: {', '.join(specialties)}")
```

**Key points about through models:**

- Both sides of the relationship can access the through model using `related_name`
- `staff.staff_specialties.all()` returns `StaffSpecialty` objects (not `Specialty` objects)
- To get the actual specialties, access through the join table: `[ss.specialty for ss in staff.staff_specialties.all()]`
- You can add additional fields to the through model to store metadata about the relationship (e.g., date assigned, certification level, etc.)
- Query across the relationship using double underscores: `StaffProxy.objects.filter(staff_specialties__specialty__name="Cardiology")`

## No Cascaded Operations

At this time the SDK does **not** support `CASCADE`, `PROTECT`, or `SET_NULL` for the required `on_delete` attribute 
to `ForeignKey` and `OneToOneField`. Only `DO_NOTHING` is allowed. It is the responsibility of the plugin to 
delete associated records correctly.

## The CustomModel Lifecycle

Managing database schemas necessarily introduces complexity, because there is state to maintain over time as the software evolves. 
Common pitfalls include expensive table rewrite operations, migrations that fail in some environments due to manual changes,
database system-specific nuances, unsatisfied foreign key constraints due to data corruption or improper order of operations, etc.

The Canvas SDK Custom Data feature aims to simplify maintenance, while sacrificing some rigor found in a full migration system like Django's.

| Operation    | Allowed | Explanation                                                                                                                                                                            |
|--------------|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Create Model | Yes     | A table corresponding to your CustomModel will be created if it does not exist. An autoincrementing column named `dbid` will be its sole attribute.                                    |
| Add Field    | Yes     | A column corresponding to a Field declared within your CustomModel will be added to the table if it does not exist. It will be nullable, without defaults to eliminate table rewrites. |
| Alter Field  | No      | This can cause a table rewrite, and requires a full migration metadata system. Create a new Field in your model. Copy data from old to new.                                            |
| Drop Field   | No      | This will cause a table rewrite, and requires a full migration metadata system. Remove the Field from your model and it will be ignored.                                               |
| Alter Model  | No      | Requires a full migration metadata system. Create a new Model in your plugin. Copy data from old to new.                                                                               |
| Drop Model   | No      | Requires a full migration metadata system. Remove the model from your plugin and it will be ignored.                                                                                   |

### Best Practices 
1. Emphasize [local development](#local-db-seeding-via-run-plugin) over use of a development EMR instance.
2. Write [automated tests](/sdk/custom-data-testing/) exercising your business logic.
3. Extract business logic and CRUD operations into "service" classes that can be tested in isolation.

## Advanced Patterns

### Combining Approaches

You can combine Custom Models with CustomAttributes for maximum flexibility:

```python
from canvas_sdk.v1.data.custom import CustomModel
from django.db.models import DO_NOTHING, ForeignKey, TextField 
from canvas_sdk.v1.data import Staff, ModelExtension


class StaffProxy(Staff, ModelExtension):
    """Staff proxy with CustomAttribute support."""
    pass


class Department(CustomModel):
    """Structured department model."""

    name = TextField()
    code = TextField()


class StaffDepartment(CustomModel):
    """Staff can belong to multiple departments."""

    staff = ForeignKey(
        StaffProxy, on_delete=DO_NOTHING, related_name="department_assignments"
    )
    department = ForeignKey(
        Department, on_delete=DO_NOTHING, related_name="staff_members"
    )
    role = TextField()


# Usage: Combine structured relationships with flexible attributes
staff = StaffProxy.objects.get(id="staff-uuid")

# Use Custom Model for structured data
dept = Department.objects.get(code="CARDIO")
StaffDepartment.objects.create(
    staff=staff,
    department=dept,
    role="Lead Physician"
)

# Use CustomAttributes for flexible data
staff.set_attributes({
    "pager_number": "555-1234",
    "preferred_contact": "email",
    "office_hours": {"monday": "9-5", "tuesday": "9-5"}
})
```

### Query Optimization

Optimize database queries using `select_related` and `prefetch_related`:

```python
from my_plugin.models import Specialty, StaffSpecialty, StaffProxy


# Use select_related for ForeignKey (SQL JOIN)
# Load StaffSpecialty with related staff and specialty in one query
staff_specialties = StaffSpecialty.objects.select_related("staff", "specialty").all()
for ss in staff_specialties:
    # No additional queries - both staff and specialty are already loaded
    print(f"{ss.staff.first_name} {ss.staff.last_name}: {ss.specialty.name}")

# Use prefetch_related for reverse ForeignKey relationships
# Load staff with all their specialties efficiently
staff_list = StaffProxy.objects.prefetch_related("staff_specialties__specialty").all()
for staff in staff_list:
    # No additional queries - staff_specialties and specialties are already loaded
    for ss in staff.staff_specialties.all():
        print(f"{staff.first_name}: {ss.specialty.name}")

# Prefetch specialties for multiple staff members
specialties_list = Specialty.objects.prefetch_related("staff_specialties__staff").all()
for specialty in specialties_list:
    staff_members = [ss.staff for ss in specialty.staff_specialties.all()]
    print(f"{specialty.name}: {len(staff_members)} staff members")

# Use Prefetch for custom filtering
from django.db.models import Prefetch

# Only load staff specialties with specific specialty names
staff_with_filtered_specialties = StaffProxy.objects.prefetch_related(
    Prefetch(
        "staff_specialties",
        queryset=StaffSpecialty.objects.filter(
            specialty__name__in=["Cardiology", "Neurology"]
        ).select_related("specialty")
    )
).all()
```

### Complex Queries

Use Django's Q objects for complex filtering and aggregation:

```python
from django.db.models import Q, Count
from plugins.my_plugin.models import StaffProxy, Specialty, StaffSpecialty


# OR conditions - Find staff with Cardiology OR Neurology specialty
staff_with_cardio_or_neuro = StaffProxy.objects.filter(
    Q(staff_specialties__specialty__name="Cardiology") |
    Q(staff_specialties__specialty__name="Neurology")
).distinct()

# AND conditions - Find specialties with "Cardiology" or "Medicine" in the name
cardio_or_medicine = Specialty.objects.filter(
    Q(name__icontains="Cardiology") | Q(name__icontains="Medicine")
)

# Negation - Find staff WITHOUT a specific specialty
staff_without_cardiology = StaffProxy.objects.exclude(
    staff_specialties__specialty__name="Cardiology"
)

# Complex filtering - Staff with multiple specific specialties
# Note: This requires DISTINCT because joins can create duplicate rows
staff_with_multiple = StaffProxy.objects.filter(
    staff_specialties__specialty__name="Cardiology"
).filter(
    staff_specialties__specialty__name="Internal Medicine"
).distinct()

# Count related objects - Staff with specialty counts
staff_with_counts = StaffProxy.objects.annotate(
    specialty_count=Count("staff_specialties")
).filter(specialty_count__gte=2)

# Group by and aggregate - Count how many staff have each specialty
specialty_counts = Specialty.objects.annotate(
    staff_count=Count("staff_specialties")
).order_by("-staff_count")

for specialty in specialty_counts:
    print(f"{specialty.name}: {specialty.staff_count} staff members")
```

## Best Practices

### Model Design

1. **Use appropriate field types** - Choose the most specific field type for your data
3. **Define related_name** - Always specify `related_name` for clear reverse relationships
5. **Keep models focused** - Each model should represent a single, well-defined concept

### Relationships

1. **Choose the right relationship type** - OneToOne for 1:1, ForeignKey for 1:many, join tables and "through" models for many:many
2. **Use through models** - To create a join table bridging two other entities, create a CustomModel representing the relationship
3. **Delete dependencies** - To prevent orphaned records, delete join table entries prior to deleting child records

### Performance

1. **Add indexes strategically** - Index frequently filtered fields - foreign key fields are automatically indexed
2. **Use select_related** - For ForeignKey and OneToOneField to reduce queries
3. **Use prefetch_related** - For reverse ForeignKey fields (including join tables for many-to-many fields)
4. **Avoid N+1 queries** - Always prefetch related data when iterating
5. **Use exists() for checks** - More efficient than count() or len()
6. **Use iterator() for large datasets** - Reduces memory usage for processing many records

### Data Integrity

1. **Ensure uniqueness of records** - Prevent duplicate data by checking for the presence of a record before creating a new one
3. **Validate in model methods** - Add custom validation in `clean()` method
4. **Use transactions** - Wrap multiple operations in atomic transactions
5. **Handle DoesNotExist** - Always catch exceptions when using `get()`

### Testing

1. **Use model factories** - Create test data with factory patterns
2. **Test model methods** - Verify custom model methods and properties
3. **Test relationships** - Ensure relationships work in both directions
4. **Test data quality** - The plugin is responsible for ensuring uniqueness and validity of foreign keys 
5. **Test edge cases** - Test with null values, empty strings, boundary conditions

## See Also

- [Custom Data Overview](/sdk/custom-data/) - Overview of all custom data techniques
- [CustomAttributes on Proxy Models](/sdk/custom-data-custom-attributes/) - Flexible key-value attributes
- [AttributeHubs](/sdk/custom-data-attribute-hubs/) - Standalone key-value storage
- [Sharing Data](/sdk/custom-data-sharing-data/) - Sharing data among plugins
- [Testing Custom Data](/sdk/custom-data-testing/) - Testing utilities and examples
- [Data Models](/sdk/data/) - Core SDK data models
- [Caching API](/sdk/caching) - Auto-expiring transient data

<br/>
<br/>
<br/>
