---
title: "Custom Data Models"
slug: "custom-models"
---

## Overview

Custom Data Models allow you to define fully structured, typed data models with relationships and constraints. Built on Django's ORM, Custom Models provide the most powerful and flexible approach to storing custom data in Canvas plugins.

**Best for:**
- Complex domain models
- Data requiring validation and constraints
- Relational data with foreign keys
- Performance-critical queries
- Data requiring indexes

**Example use cases:**
- Provider specialties and certifications
- Custom workflows and forms
- Integration-specific data structures
- Practice-specific business entities

---

## Basic Custom Model

Create a custom model by extending `CustomModel`:

```python
from canvas_sdk.v1.data.custom import CustomModel
from canvas_sdk.v1.data.fields import TextField, IntegerField, BooleanField


class ProviderSpecialty(CustomModel):
    """Track provider specialties and certifications."""

    name = TextField(max_length=200)
    board_certified = BooleanField(default=False)
    years_experience = IntegerField(default=0)

    class Meta:
        db_table = "provider_specialty"
```

Custom Models automatically include:
- `id`: Primary key (UUID)
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last modification

---

## Schema Rules and Constraints

### Field Types

Canvas SDK provides Django-based field types for defining your models:

| Field Type | Description | Common Parameters |
|------------|-------------|-------------------|
| `TextField` | Variable-length text | `max_length`, `blank`, `null`, `default` |
| `CharField` | Fixed-length text | `max_length` (required), `blank`, `null`, `default` |
| `IntegerField` | Integer values | `blank`, `null`, `default` |
| `DecimalField` | Decimal numbers | `max_digits`, `decimal_places`, `blank`, `null`, `default` |
| `BooleanField` | True/False values | `default` |
| `DateField` | Date values | `auto_now`, `auto_now_add`, `blank`, `null`, `default` |
| `DateTimeField` | Date and time values | `auto_now`, `auto_now_add`, `blank`, `null`, `default` |
| `JSONField` | JSON-serializable data | `blank`, `null`, `default` |
| `ForeignKey` | Many-to-one relationship | `on_delete`, `related_name`, `blank`, `null` |
| `OneToOneField` | One-to-one relationship | `on_delete`, `related_name`, `blank`, `null` |
| `ManyToManyField` | Many-to-many relationship | `related_name`, `blank` |

```python
from canvas_sdk.v1.data.custom import CustomModel
from canvas_sdk.v1.data.fields import (
    TextField, IntegerField, DecimalField, BooleanField,
    DateField, DateTimeField, JSONField
)


class ProviderProfile(CustomModel):
    bio = TextField(blank=True, null=True)
    license_number = CharField(max_length=50)
    patient_capacity = IntegerField(default=100)
    hourly_rate = DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    accepting_patients = BooleanField(default=True)
    license_expiry = DateField(blank=True, null=True)
    last_credentialing_check = DateTimeField(auto_now=True)
    specialties = JSONField(default=list)

    class Meta:
        db_table = "provider_profile"
```

### Column Constraints

Apply constraints using field parameters:

```python
from canvas_sdk.v1.data.custom import CustomModel
from canvas_sdk.v1.data.fields import TextField, IntegerField


class Certification(CustomModel):
    # Required field (cannot be null or blank)
    name = TextField(max_length=200)

    # Optional field (can be null or blank)
    description = TextField(blank=True, null=True)

    # Field with default value
    status = TextField(max_length=20, default="active")

    # Positive integer only
    validity_years = IntegerField(default=1)

    # Unique constraint
    certification_number = TextField(max_length=50, unique=True)

    class Meta:
        db_table = "certification"
```

**Common Parameters:**
- `null=True`: Allows NULL in database
- `blank=True`: Allows empty value in forms
- `default`: Default value for new records
- `unique=True`: Enforces uniqueness constraint
- `max_length`: Maximum character length

### Database Constraints

Define table-level constraints using the `Meta` class:

```python
from canvas_sdk.v1.data.custom import CustomModel
from canvas_sdk.v1.data.fields import TextField, ForeignKey
from django.db.models import UniqueConstraint


class ProviderLicense(CustomModel):
    provider_id = TextField(max_length=200)
    state = TextField(max_length=2)
    license_number = TextField(max_length=50)

    class Meta:
        db_table = "provider_license"
        # Ensure unique combination of provider and state
        constraints = [
            UniqueConstraint(
                fields=["provider_id", "state"],
                name="unique_provider_state"
            )
        ]
```

### Indexes

Add indexes for frequently queried fields:

```python
from canvas_sdk.v1.data.custom import CustomModel
from canvas_sdk.v1.data.fields import TextField, DateField
from django.db.models import Index


class Appointment(CustomModel):
    provider_id = TextField(max_length=200)
    patient_id = TextField(max_length=200)
    appointment_date = DateField()
    status = TextField(max_length=20)

    class Meta:
        db_table = "appointment"
        indexes = [
            # Single-column index
            Index(fields=["provider_id"]),
            Index(fields=["patient_id"]),
            # Composite index for common query pattern
            Index(fields=["provider_id", "appointment_date"]),
            # Named index
            Index(fields=["status"], name="appointment_status_idx")
        ]
```

**Index Best Practices:**
- Index foreign key fields
- Index fields used in `filter()` and `order_by()`
- Create composite indexes for common multi-field queries
- Avoid over-indexing (indexes slow down writes)

### Migration Best Practices

When modifying Custom Models:

1. **Additive Changes** (safe to deploy):
   - Adding new fields with `null=True` or `default`
   - Adding new models
   - Adding indexes

```python
# Safe: Adding optional field
class ProviderProfile(CustomModel):
    bio = TextField(blank=True, null=True)
    # New field added
    languages = JSONField(default=list)
```

2. **Destructive Changes** (require careful migration):
   - Removing fields
   - Renaming fields
   - Changing field types
   - Adding `null=False` to existing fields

```python
# Requires migration: Adding required field to existing model
class ProviderProfile(CustomModel):
    bio = TextField(blank=True, null=True)
    # This requires a migration with default or data population
    license_number = CharField(max_length=50)  # null=False by default
```

3. **Migration Strategy for Required Fields**:

```python
# Step 1: Add field as optional
class ProviderProfile(CustomModel):
    bio = TextField(blank=True, null=True)
    license_number = CharField(max_length=50, null=True, blank=True)

# Step 2: Populate data for existing records
# (In a data migration or script)

# Step 3: Make field required
class ProviderProfile(CustomModel):
    bio = TextField(blank=True, null=True)
    license_number = CharField(max_length=50)  # Now required
```

---

## Creating and Querying

### Creating Records

```python
from plugins.my_plugin.models import ProviderSpecialty


# Create and save
specialty = ProviderSpecialty(
    name="Cardiology",
    board_certified=True,
    years_experience=15
)
specialty.save()

# Create in one step
specialty = ProviderSpecialty.objects.create(
    name="Neurology",
    board_certified=True,
    years_experience=10
)

# Get or create (avoids duplicates)
specialty, created = ProviderSpecialty.objects.get_or_create(
    name="Internal Medicine",
    defaults={
        "board_certified": False,
        "years_experience": 5
    }
)
```

### Querying Records

```python
from plugins.my_plugin.models import ProviderSpecialty


# Get all records
all_specialties = ProviderSpecialty.objects.all()

# Filter records
board_certified = ProviderSpecialty.objects.filter(board_certified=True)
experienced = ProviderSpecialty.objects.filter(years_experience__gte=10)

# Get single record
try:
    cardiology = ProviderSpecialty.objects.get(name="Cardiology")
except ProviderSpecialty.DoesNotExist:
    cardiology = None

# Chain filters
senior_certified = ProviderSpecialty.objects.filter(
    board_certified=True,
    years_experience__gte=10
)

# Order results
by_experience = ProviderSpecialty.objects.order_by("-years_experience")

# Limit results
top_five = ProviderSpecialty.objects.order_by("-years_experience")[:5]
```

### Updating Records

```python
from plugins.my_plugin.models import ProviderSpecialty


# Update single record
specialty = ProviderSpecialty.objects.get(name="Cardiology")
specialty.years_experience = 16
specialty.save()

# Update multiple records
ProviderSpecialty.objects.filter(
    board_certified=False
).update(board_certified=True)

# Update or create
specialty, created = ProviderSpecialty.objects.update_or_create(
    name="Pediatrics",
    defaults={
        "board_certified": True,
        "years_experience": 8
    }
)
```

### Deleting Records

```python
from plugins.my_plugin.models import ProviderSpecialty


# Delete single record
specialty = ProviderSpecialty.objects.get(name="Cardiology")
specialty.delete()

# Delete multiple records
ProviderSpecialty.objects.filter(years_experience=0).delete()

# Delete all records (use with caution!)
ProviderSpecialty.objects.all().delete()
```

---

## One-to-One Relationships

A one-to-one relationship links one record in a model to exactly one record in another model. Use `OneToOneField` to define this relationship.

### Basic One-to-One

```python
from canvas_sdk.v1.data.custom import CustomModel
from canvas_sdk.v1.data.fields import TextField, OneToOneField, DateField
from canvas_sdk.v1.data import Staff


class StaffProxy(Staff):
    """Proxy for Staff to use with custom models."""
    class Meta:
        proxy = True


class ProviderCredentials(CustomModel):
    """One-to-one relationship: Each staff member has one credentials record."""

    staff = OneToOneField(
        StaffProxy,
        on_delete=models.CASCADE,
        related_name="credentials"
    )
    dea_number = TextField(max_length=50, blank=True, null=True)
    npi_number = TextField(max_length=10)
    license_number = TextField(max_length=50)
    license_state = TextField(max_length=2)
    license_expiry = DateField()

    class Meta:
        db_table = "provider_credentials"
```

### Creating One-to-One Records

```python
from plugins.my_plugin.models import StaffProxy, ProviderCredentials
from datetime import date


# Get staff member
staff = StaffProxy.objects.get(id="staff-uuid")

# Create credentials
credentials = ProviderCredentials.objects.create(
    staff=staff,
    dea_number="AB1234563",
    npi_number="1234567890",
    license_number="MD12345",
    license_state="CA",
    license_expiry=date(2025, 12, 31)
)
```

### Querying One-to-One Relationships

```python
from plugins.my_plugin.models import StaffProxy, ProviderCredentials


# Access from credentials to staff
credentials = ProviderCredentials.objects.get(npi_number="1234567890")
staff_member = credentials.staff
print(f"Provider: {staff_member.first_name} {staff_member.last_name}")

# Access from staff to credentials (using related_name)
staff = StaffProxy.objects.get(id="staff-uuid")
try:
    credentials = staff.credentials
    print(f"DEA: {credentials.dea_number}")
except ProviderCredentials.DoesNotExist:
    print("No credentials found")

# Query across relationship
# Find all staff with expiring licenses
from datetime import date, timedelta

expiring_soon = StaffProxy.objects.filter(
    credentials__license_expiry__lte=date.today() + timedelta(days=90)
)
```

### One-to-One with Optional Relationship

```python
from canvas_sdk.v1.data.custom import CustomModel
from canvas_sdk.v1.data.fields import TextField, OneToOneField


class ProviderBio(CustomModel):
    """Optional one-to-one: Not all staff may have a bio."""

    staff = OneToOneField(
        StaffProxy,
        on_delete=models.CASCADE,
        related_name="bio",
        null=True,
        blank=True
    )
    biography = TextField()
    education = TextField()
    research_interests = TextField(blank=True, null=True)

    class Meta:
        db_table = "provider_bio"
```

---

## One-to-Many Relationships

A one-to-many (or many-to-one) relationship allows one record to be associated with multiple records in another model. Use `ForeignKey` to define this relationship.

### Basic One-to-Many

```python
from canvas_sdk.v1.data.custom import CustomModel
from canvas_sdk.v1.data.fields import TextField, ForeignKey, DateField


class ProviderSpecialty(CustomModel):
    """One provider can have many specialties."""

    staff = ForeignKey(
        StaffProxy,
        on_delete=models.CASCADE,
        related_name="specialties"
    )
    name = TextField(max_length=200)
    board_certified = BooleanField(default=False)
    certification_date = DateField(blank=True, null=True)

    class Meta:
        db_table = "provider_specialty"
```

### Creating One-to-Many Records

```python
from plugins.my_plugin.models import StaffProxy, ProviderSpecialty
from datetime import date


# Get staff member
staff = StaffProxy.objects.get(id="staff-uuid")

# Create multiple specialties for one provider
cardiology = ProviderSpecialty.objects.create(
    staff=staff,
    name="Cardiology",
    board_certified=True,
    certification_date=date(2015, 6, 1)
)

internal_medicine = ProviderSpecialty.objects.create(
    staff=staff,
    name="Internal Medicine",
    board_certified=True,
    certification_date=date(2010, 5, 15)
)
```

### Querying One-to-Many Relationships

```python
from plugins.my_plugin.models import StaffProxy, ProviderSpecialty


# Access from specialty to staff (forward)
specialty = ProviderSpecialty.objects.get(name="Cardiology")
provider = specialty.staff
print(f"Provider: {provider.first_name} {provider.last_name}")

# Access from staff to specialties (reverse, using related_name)
staff = StaffProxy.objects.get(id="staff-uuid")
specialties = staff.specialties.all()
for specialty in specialties:
    print(f"- {specialty.name} (Certified: {specialty.board_certified})")

# Filter reverse relationship
board_certified_specialties = staff.specialties.filter(board_certified=True)

# Query across relationship
# Find all staff who are board certified in Cardiology
cardiologists = StaffProxy.objects.filter(
    specialties__name="Cardiology",
    specialties__board_certified=True
)

# Count related records
specialty_count = staff.specialties.count()

# Check existence
has_cardiology = staff.specialties.filter(name="Cardiology").exists()
```

### One-to-Many with Patient Relationships

```python
from canvas_sdk.v1.data.custom import CustomModel
from canvas_sdk.v1.data.fields import TextField, ForeignKey, DateTimeField
from canvas_sdk.v1.data import Patient


class PatientProxy(Patient):
    """Proxy for Patient to use with custom models."""
    class Meta:
        proxy = True


class PatientNote(CustomModel):
    """One patient can have many custom notes."""

    patient = ForeignKey(
        PatientProxy,
        on_delete=models.CASCADE,
        related_name="custom_notes"
    )
    note_type = TextField(max_length=50)
    content = TextField()
    created_by = TextField(max_length=200)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "patient_note"
        indexes = [
            Index(fields=["patient", "created_at"]),
        ]


# Usage
patient = PatientProxy.objects.get(id="patient-uuid")

# Create notes
PatientNote.objects.create(
    patient=patient,
    note_type="care_plan",
    content="Patient prefers morning appointments",
    created_by="staff-uuid"
)

# Query patient's notes
recent_notes = patient.custom_notes.order_by("-created_at")[:5]
care_plan_notes = patient.custom_notes.filter(note_type="care_plan")
```

### Cascading Deletes

Control what happens when the related object is deleted using `on_delete`:

```python
from canvas_sdk.v1.data.fields import ForeignKey
from django.db.models import CASCADE, PROTECT, SET_NULL


class ProviderSpecialty(CustomModel):
    # CASCADE: Delete specialties when staff is deleted
    staff = ForeignKey(
        StaffProxy,
        on_delete=CASCADE,
        related_name="specialties"
    )


class ProviderAssignment(CustomModel):
    # PROTECT: Prevent staff deletion if assignments exist
    staff = ForeignKey(
        StaffProxy,
        on_delete=PROTECT,
        related_name="assignments"
    )


class ProviderReview(CustomModel):
    # SET_NULL: Set to null when staff is deleted
    staff = ForeignKey(
        StaffProxy,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="reviews"
    )
```

---

## Many-to-Many Relationships

A many-to-many relationship allows multiple records in one model to be associated with multiple records in another model. Use `ManyToManyField` to define this relationship.

### Basic Many-to-Many

```python
from canvas_sdk.v1.data.custom import CustomModel
from canvas_sdk.v1.data.fields import TextField, ManyToManyField


class Certification(CustomModel):
    """Certification that providers can have."""

    name = TextField(max_length=200)
    issuing_body = TextField(max_length=200)
    description = TextField(blank=True, null=True)

    class Meta:
        db_table = "certification"


class ProviderProfile(CustomModel):
    """Provider can have many certifications, certification can belong to many providers."""

    staff = OneToOneField(
        StaffProxy,
        on_delete=models.CASCADE,
        related_name="provider_profile"
    )
    certifications = ManyToManyField(
        Certification,
        related_name="providers",
        blank=True
    )

    class Meta:
        db_table = "provider_profile"
```

### Creating Many-to-Many Records

```python
from plugins.my_plugin.models import StaffProxy, ProviderProfile, Certification


# Create certifications
acls = Certification.objects.create(
    name="ACLS",
    issuing_body="American Heart Association",
    description="Advanced Cardiovascular Life Support"
)

bls = Certification.objects.create(
    name="BLS",
    issuing_body="American Heart Association",
    description="Basic Life Support"
)

pals = Certification.objects.create(
    name="PALS",
    issuing_body="American Heart Association",
    description="Pediatric Advanced Life Support"
)

# Create provider profile
staff = StaffProxy.objects.get(id="staff-uuid")
profile = ProviderProfile.objects.create(staff=staff)

# Add certifications
profile.certifications.add(acls)
profile.certifications.add(bls, pals)  # Add multiple at once

# Set certifications (replaces existing)
profile.certifications.set([acls, pals])

# Remove certifications
profile.certifications.remove(bls)

# Clear all certifications
profile.certifications.clear()
```

### Querying Many-to-Many Relationships

```python
from plugins.my_plugin.models import ProviderProfile, Certification


# Access from profile to certifications (forward)
profile = ProviderProfile.objects.get(staff__id="staff-uuid")
certifications = profile.certifications.all()
for cert in certifications:
    print(f"- {cert.name} ({cert.issuing_body})")

# Access from certification to providers (reverse)
acls = Certification.objects.get(name="ACLS")
acls_providers = acls.providers.all()

# Filter
profile_certs = profile.certifications.filter(issuing_body="American Heart Association")

# Check existence
has_acls = profile.certifications.filter(name="ACLS").exists()

# Count
cert_count = profile.certifications.count()

# Query across relationship
# Find all profiles with ACLS certification
acls_certified = ProviderProfile.objects.filter(
    certifications__name="ACLS"
)

# Find providers with multiple specific certifications
from django.db.models import Q

critical_care = ProviderProfile.objects.filter(
    Q(certifications__name="ACLS") & Q(certifications__name="PALS")
).distinct()
```

### Many-to-Many with Through Model

Use a through model when you need to store additional data about the relationship:

```python
from canvas_sdk.v1.data.custom import CustomModel
from canvas_sdk.v1.data.fields import (
    TextField, ForeignKey, ManyToManyField, DateField, BooleanField
)


class Certification(CustomModel):
    name = TextField(max_length=200)
    issuing_body = TextField(max_length=200)

    class Meta:
        db_table = "certification"


class ProviderProfile(CustomModel):
    staff = OneToOneField(
        StaffProxy,
        on_delete=models.CASCADE,
        related_name="provider_profile"
    )
    certifications = ManyToManyField(
        Certification,
        through="ProviderCertification",
        related_name="providers"
    )

    class Meta:
        db_table = "provider_profile"


class ProviderCertification(CustomModel):
    """Through model storing additional certification data."""

    provider_profile = ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE
    )
    certification = ForeignKey(
        Certification,
        on_delete=models.CASCADE
    )
    obtained_date = DateField()
    expiry_date = DateField(blank=True, null=True)
    is_active = BooleanField(default=True)
    certificate_number = TextField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "provider_certification"
        unique_together = ["provider_profile", "certification"]
```

### Creating and Querying Through Models

```python
from plugins.my_plugin.models import (
    ProviderProfile, Certification, ProviderCertification
)
from datetime import date


# Create provider profile
staff = StaffProxy.objects.get(id="staff-uuid")
profile = ProviderProfile.objects.create(staff=staff)

# Create certification
acls = Certification.objects.get(name="ACLS")

# Create through model explicitly
provider_cert = ProviderCertification.objects.create(
    provider_profile=profile,
    certification=acls,
    obtained_date=date(2020, 1, 15),
    expiry_date=date(2025, 1, 15),
    is_active=True,
    certificate_number="ACLS-12345"
)

# Query through model
# Get all active certifications for a provider
active_certs = ProviderCertification.objects.filter(
    provider_profile=profile,
    is_active=True
)

# Get certifications expiring soon
from datetime import timedelta

expiring_soon = ProviderCertification.objects.filter(
    provider_profile=profile,
    expiry_date__lte=date.today() + timedelta(days=90),
    is_active=True
)

# Access through data from queryset
profile_certs = profile.certifications.all()
for cert in profile_certs:
    # Access through model
    through = ProviderCertification.objects.get(
        provider_profile=profile,
        certification=cert
    )
    print(f"{cert.name}: Expires {through.expiry_date}")
```

---

## Advanced Patterns

### Combining Approaches

You can combine Custom Models with CustomAttributes for maximum flexibility:

```python
from canvas_sdk.v1.data.custom import CustomModel
from canvas_sdk.v1.data.fields import TextField, ForeignKey
from canvas_sdk.v1.data import Staff, CustomAttributeMixin, CustomAttributeAwareManager


class StaffProxy(Staff, CustomAttributeMixin):
    """Staff proxy with CustomAttribute support."""
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


class Department(CustomModel):
    """Structured department model."""

    name = TextField(max_length=200)
    code = TextField(max_length=10, unique=True)

    class Meta:
        db_table = "department"


class StaffDepartment(CustomModel):
    """Staff can belong to multiple departments."""

    staff = ForeignKey(
        StaffProxy,
        on_delete=models.CASCADE,
        related_name="department_assignments"
    )
    department = ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="staff_members"
    )
    role = TextField(max_length=100)

    class Meta:
        db_table = "staff_department"
        unique_together = ["staff", "department"]


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
from plugins.my_plugin.models import ProviderSpecialty, ProviderProfile, StaffProxy


# Use select_related for ForeignKey and OneToOneField (SQL JOIN)
specialties = ProviderSpecialty.objects.select_related("staff").all()
for specialty in specialties:
    # No additional query - staff is already loaded
    print(f"{specialty.name}: {specialty.staff.first_name}")

# Use prefetch_related for reverse ForeignKey and ManyToManyField
staff_list = StaffProxy.objects.prefetch_related("specialties").all()
for staff in staff_list:
    # No additional queries - specialties are already loaded
    for specialty in staff.specialties.all():
        print(f"{staff.first_name}: {specialty.name}")

# Combine both for complex queries
profiles = ProviderProfile.objects.select_related(
    "staff"
).prefetch_related(
    "certifications",
    "staff__department_assignments__department"
).all()

# Use Prefetch for custom filtering
from django.db.models import Prefetch

profiles = ProviderProfile.objects.prefetch_related(
    Prefetch(
        "certifications",
        queryset=Certification.objects.filter(issuing_body="American Heart Association")
    )
).all()
```

### Complex Queries

Use Django's Q objects for complex filtering:

```python
from django.db.models import Q, Count, Avg
from plugins.my_plugin.models import ProviderProfile, ProviderSpecialty


# OR conditions
profiles = ProviderProfile.objects.filter(
    Q(certifications__name="ACLS") | Q(certifications__name="BLS")
).distinct()

# AND with OR
senior_specialists = ProviderSpecialty.objects.filter(
    Q(board_certified=True) &
    (Q(name="Cardiology") | Q(name="Neurology")) &
    Q(years_experience__gte=10)
)

# Negation
non_certified = ProviderProfile.objects.filter(
    ~Q(certifications__name="ACLS")
)

# Aggregation
from django.db.models import Count, Avg

# Count related objects
staff_with_counts = StaffProxy.objects.annotate(
    specialty_count=Count("specialties"),
    avg_experience=Avg("specialties__years_experience")
).filter(specialty_count__gte=2)

# Group by and aggregate
from django.db.models import Count

specialty_counts = ProviderSpecialty.objects.values("name").annotate(
    provider_count=Count("staff")
).order_by("-provider_count")
```

---

## Best Practices

### Model Design

1. **Use appropriate field types** - Choose the most specific field type for your data
2. **Set null and blank appropriately** - Use `null=True` for optional database values, `blank=True` for optional form fields
3. **Define related_name** - Always specify `related_name` for clear reverse relationships
4. **Use Meta options** - Define `db_table`, `indexes`, and `constraints` in the Meta class
5. **Keep models focused** - Each model should represent a single, well-defined concept

### Relationships

1. **Choose the right relationship type** - OneToOne for 1:1, ForeignKey for 1:many, ManyToMany for many:many
2. **Use through models** - Add a through model when you need to store relationship metadata
3. **Set on_delete appropriately** - Use CASCADE, PROTECT, or SET_NULL based on your business logic
4. **Avoid circular dependencies** - Structure models to minimize circular foreign key relationships

### Performance

1. **Add indexes strategically** - Index foreign keys and frequently filtered fields
2. **Use select_related** - For ForeignKey and OneToOneField to reduce queries
3. **Use prefetch_related** - For reverse ForeignKey and ManyToManyField
4. **Avoid N+1 queries** - Always prefetch related data when iterating
5. **Use exists() for checks** - More efficient than count() or len()
6. **Use iterator() for large datasets** - Reduces memory usage for processing many records

### Data Integrity

1. **Use unique constraints** - Prevent duplicate data at the database level
2. **Use unique_together** - For composite uniqueness constraints
3. **Validate in model methods** - Add custom validation in `clean()` method
4. **Use transactions** - Wrap multiple operations in atomic transactions
5. **Handle DoesNotExist** - Always catch exceptions when using `get()`

### Migrations

1. **Add fields as nullable first** - Then populate data, then make required
2. **Use data migrations** - For complex data transformations
3. **Test migrations** - Always test on a copy of production data
4. **Keep migrations small** - Break complex changes into multiple migrations
5. **Document breaking changes** - Add comments for migrations that require special handling

### Testing

1. **Use model factories** - Create test data with factory patterns
2. **Test model methods** - Verify custom model methods and properties
3. **Test relationships** - Ensure relationships work in both directions
4. **Test constraints** - Verify unique constraints and validation
5. **Test edge cases** - Test with null values, empty strings, boundary conditions

---

## See Also

- [Custom Data Overview](/sdk/custom-data/) - Overview of all custom data techniques
- [CustomAttributes on Proxy Models](/sdk/custom-data/custom-attributes/) - Flexible key-value attributes
- [AttributeHubs](/sdk/custom-data/attribute-hub/) - Standalone key-value storage
- [Testing Custom Data](/sdk/custom-data/testing/) - Testing utilities and examples
- [Data Models](/sdk/data/) - Core SDK data models
- [Canvas CLI](/sdk/canvas_cli/#simple-api-endpoints) - Simple API for sharing data between plugins
