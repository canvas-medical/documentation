---
title: "Custom Data"
---

## Overview

The Canvas SDK provides three techniques for storing custom data in your plugins, allowing you to extend existing models, create flexible key-value stores, or define fully structured data models with relationships:

1. **CustomAttributes on Proxy Models** - Extend existing SDK data models (like Patient or Staff) with flexible key-value attributes
2. **AttributeHubs** - Store arbitrary key-value data that doesn't belong to existing models
3. **Custom Data Models** - Define fully structured models with typed fields and relationships

Each technique serves different use cases and provides different levels of structure and type safety. 
All three techniques may be used together.

---

## Data Privacy and Plugin Isolation

All custom data created by a plugin—whether using CustomAttributes, AttributeHubs, or Custom Data Models—is **scoped to that plugin**. This isolation ensures that plugins cannot directly access or modify another plugin's data, maintaining security and data integrity across the system.

### Data Isolation

**CustomAttributes** attached to SDK models (like Patient or Staff) are scoped by plugin. Each plugin maintains its own separate namespace for custom attributes, even when attached to the same core model instance.

```python
# In plugin-a
staff.set_attribute("specialty", "Cardiology")  # Only accessible within plugin-a

# In plugin-b
staff.get_attribute("specialty")  # Returns None - cannot see plugin-a's data
staff.set_attribute("specialty", "Neurology")  # Creates separate attribute in plugin-b
```

**Custom Data Models** created by a plugin exist in a plugin-specific database schema. Tables and data are completely isolated from other plugins.

```python
# In plugin-a: Creates table in plugin-a schema
class Specialty(CustomModel):
    name = TextField()

# In plugin-b: Cannot access plugin-a's Specialty model or data
# Would need to define its own Specialty model if needed
```

**AttributeHubs** store data within the plugin's namespace and are not accessible to other plugins.

### Sharing Data Between Plugins

To share data across plugins, a plugin must **explicitly expose an API** with appropriate authorization and access controls. This is done using the [Simple API](/sdk/canvas_cli/#simple-api-endpoints) feature.

#### Example: Exposing Provider Profile Data

```python
from canvas_sdk.handlers.simple_api import SimpleAPI, APIKeyCredentials, api
from canvas_sdk.effects.simple_api import JSONResponse
from canvas_sdk.v1.data import Staff, CustomAttributeMixin, CustomAttributeAwareManager


class StaffProxy(Staff, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


class ProfileAPI(SimpleAPI):
    """API to share staff profile data with authorized plugins."""

    PREFIX = "/staff-profiles"

    def authenticate(self, credentials: APIKeyCredentials) -> bool:
        """Validate API key from requesting plugin."""
        from hmac import compare_digest

        provided_key = credentials.key
        expected_key = self.secrets["profile_api_key"]

        return compare_digest(provided_key.encode(), expected_key.encode())

    @api.get("/<staff_id>")
    def get_profile(self):
        """Return staff profile data."""
        staff_id = self.request.path_params["staff_id"]
        staff = StaffProxy.objects.get(id=staff_id)

        # Explicitly choose what data to expose
        profile = {
            "staff_id": staff.id,
            "first_name": staff.first_name,
            "last_name": staff.last_name,
            "specialty": staff.get_attribute("specialty"),
            "accepting_patients": staff.get_attribute("accepting_patients")
        }

        return [JSONResponse(profile)]
```

#### Consuming Shared Data from Another Plugin

```python
import requests
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.events import EventType


class ConsumerHandler(BaseHandler):
    """Handler that consumes profile data from another plugin."""

    RESPONDS_TO = EventType.Name(EventType.APPOINTMENT__APPOINTMENT__POST_SEARCH)

    def compute(self):
        staff_id = self.target.staff_id

        # Call the other plugin's API
        api_key = self.secrets["profile_api_key"]
        response = requests.get(
            f"http://<canvas-host>/plugin-io/api/staff-profiles/profile/{staff_id}",
            headers={"Authorization": f"Bearer {api_key}"}
        )

        if response.status_code == 200:
            profile = response.json()
            specialty = profile.get("specialty")
            # Use the shared data...

        return []
```

### Data Sharing Best Practices

1. **Explicit Authorization** - Always require authentication for APIs that expose plugin data
2. **Minimal Exposure** - Only expose the specific data fields that are necessary
3. **Validate Requests** - Check permissions and validate that the requester should have access
4. **Document APIs** - Provide clear documentation for plugins that will consume your API
5. **Version APIs** - Use versioning (e.g., `/v1/profiles`) to allow API evolution
6. **Audit Access** - Log API access for security and debugging purposes
7. **Rate Limiting** - Consider implementing rate limits to prevent abuse

### Security Considerations

- **Never bypass plugin isolation** by attempting to access another plugin's database schema directly
- **Use API keys or tokens** stored in secrets, never hardcoded in plugin code
- **Implement proper error handling** that doesn't leak sensitive information
- **Consider PHI implications** when exposing patient-related data via APIs
- **Follow least privilege** principle - grant minimum necessary access

---

## When to Use Each Technique

### CustomAttributes on Proxy Models

Use this when you need to add flexible data to existing SDK models without defining a schema.

**Best for:**
- Storing variable or configuration data on existing models
- Rapid prototyping
- Data that doesn't require strict typing
- Simple key-value associations with core models

**Example use cases:**
- Adding practice-specific flags to patients
- Storing provider preferences
- Temporary or experimental data fields

### AttributeHubs

Use this when you need to store data that doesn't naturally belong to any existing model.

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

### Custom Data Models

Use this when you need structured, typed data with relationships and constraints.

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

## CustomAttributes on Proxy Models

Extend existing SDK models by creating a proxy class that adds CustomAttribute support.

### Creating a Proxy Model

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

### Setting Attributes

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

### Getting Attributes

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

### Supported Value Types

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

### Querying by CustomAttributes

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

### Optimizing Queries with Prefetch

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

### Deleting Attributes

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

## AttributeHub

AttributeHub provides a simple model for storing arbitrary key-value data that doesn't belong to existing models.

### Creating an AttributeHub

```python
from canvas_sdk.v1.data import AttributeHub

# Create a hub for a specific purpose
hub = AttributeHub.objects.create(
    type="staff_profile",
    externally_exposable_id="staff_id:abc123"
)
```

### Storing Data in AttributeHub

```python
from datetime import datetime
from canvas_sdk.v1.data import AttributeHub

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
```

### Retrieving Data from AttributeHub

```python
from canvas_sdk.v1.data import AttributeHub

# Get or create pattern
hub, created = AttributeHub.objects.get_or_create(
    type="staff_profile",
    externally_exposable_id="staff_id:abc123"
)

# Retrieve attributes
profile = hub.get_attribute("profile")
last_sync = hub.get_attribute("last_sync")
```

### Use Case Example: External API State

```python
from datetime import datetime
from canvas_sdk.handlers.simple_api import SimpleAPI, api
from canvas_sdk.effects.simple_api import JSONResponse
from canvas_sdk.v1.data import AttributeHub, Staff


class ExternalSyncAPI(SimpleAPI):
    @api.post("/sync/<staff_id>")
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

---

## Custom Data Models

Create fully structured data models with typed fields and relationships using Django's ORM.

### Basic Custom Model

Define a custom model by inheriting from `CustomModel`:

```python
from django.db.models import TextField, IntegerField, Index
from canvas_sdk.v1.data.base import CustomModel


class Specialty(CustomModel):
    class Meta:
        # Add indexes for fields used in filter queries
        indexes = [
            Index(fields=["name"]),
        ]

    name = TextField()
    description = TextField()
    years_required = IntegerField()

    def __str__(self):
        return f"{self.name}"
```

**Note on Indexing:** Foreign key and one-to-one fields are automatically indexed by the SDK. You only need to manually add indexes for other fields that you use in `.filter()` queries.

---

## Schema Rules and Constraints

Custom data models have specific rules for schema evolution to ensure database stability and prevent data loss.

### Schema Evolution Rules

**Tables:**
- Tables may be **declared** in your plugin code within a **models** directory
- Tables **cannot be renamed** once created
- Table definitions persist across plugin updates

**Columns:**
- Columns may be **added** to existing tables
- Columns **cannot be removed** from tables
- Columns **cannot be renamed** once created

```python
from django.db.models import TextField, IntegerField, BooleanField, Index
from canvas_sdk.v1.data.base import CustomModel


class Provider(CustomModel):
    class Meta:
        indexes = [
            Index(fields=["specialty"]),
        ]

    # Original fields
    name = TextField()
    specialty = TextField()

    # New field added in v2 - must allow null or have default
    board_certified = BooleanField()

    # Another new field with default value
    years_experience = IntegerField(default=0)

    # ❌ CANNOT rename 'specialty' to 'medical_specialty'
    # ❌ CANNOT remove 'name' field
```

### Database Constraints

**No database-level constraints allowed:**
- Do not use `unique=True` on fields
- Do not use `null=False` on fields
- Do not use `UniqueConstraint` in Meta
- Do not use `CheckConstraint` in Meta
- Foreign keys are supported but not backed by database constraints

Any declared constraints will be ignored during database schema initialization.

**Your plugin is responsible for:**
- Data validation before saving
- Ensuring uniqueness if needed
- Maintaining data quality and integrity
- Handling constraint violations in application logic

```python
from django.db.models import TextField, Index
from canvas_sdk.v1.data.base import CustomModel


class Specialty(CustomModel):
    class Meta:
        indexes = [
            Index(fields=["name"]),
        ]

        # ❌ NOT ALLOWED - no database constraints
        # constraints = [
        #     UniqueConstraint(fields=["name"], name="unique_specialty_name")
        # ]

    name = TextField()  # ✓ Correct - no unique=True


# ✓ Correct - validate uniqueness in application code
def create_specialty(name: str) -> Specialty:
    """Create specialty, ensuring name uniqueness at application level."""
    # Check for existing specialty
    existing = Specialty.objects.filter(name=name).first()
    if existing:
        raise ValueError(f"Specialty with name '{name}' already exists")

    return Specialty.objects.create(name=name)
```

### Indexes

**Allowed:**
- Indexes may be declared on **one or more non-key columns**
- Use `Index(fields=[...])` in the Meta class
- Multi-column indexes are supported
- Foreign key fields are automatically indexed (no need to declare)

```python
from django.db.models import TextField, ForeignKey, DateTimeField, Index, DO_NOTHING
from datetime import datetime
from canvas_sdk.v1.data import Staff, CustomAttributeMixin, CustomAttributeAwareManager
from canvas_sdk.v1.data.base import CustomModel


class StaffProxy(Staff, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


class Appointment(CustomModel):
    class Meta:
        indexes = [
            # ✓ Single column index
            Index(fields=["status"]),

            # ✓ Multi-column index for common query pattern
            Index(fields=["staff", "appointment_date"]),

            # ✓ Index with descending order
            Index(fields=["-created_at"]),
        ]

    staff = ForeignKey(
        StaffProxy,
        to_field="dbid",
        on_delete=DO_NOTHING,
        related_name="custom_appointments"
    )  # Automatically indexed - don't add to Meta.indexes

    status = TextField()  # Indexed in Meta
    appointment_date = DateTimeField()  # Indexed as part of composite
    created_at = DateTimeField(default=datetime.now)
    notes = TextField()  # Not indexed - not used in filters
```

### Migration Best Practices

1. **Additive changes only** - Only add new fields, never remove or rename
5. **Handle missing data** - Code should gracefully handle null values in new fields

```python
from django.db.models import TextField, IntegerField, BooleanField, Index
from canvas_sdk.v1.data.base import CustomModel


class ProviderProfile(CustomModel):
    """Provider profile data.

    Schema versions:
    - v1.0: Initial fields (name, specialty, years_experience)
    - v1.1: Added board_certified field
    - v1.2: Added accepting_patients field
    """

    class Meta:
        indexes = [
            Index(fields=["specialty"]),
        ]

    # v1.0 fields
    name = TextField()
    specialty = TextField()
    years_experience = IntegerField(default=0)

    # v1.1 fields - nullable for backward compatibility
    board_certified = BooleanField(null=True, blank=True)

    # v1.2 fields - with sensible default
    accepting_patients = BooleanField(default=True)


# ✓ Code handles null values gracefully
def get_board_certification_status(profile: ProviderProfile) -> str:
    if profile.board_certified is None:
        return "Unknown"
    return "Board Certified" if profile.board_certified else "Not Board Certified"
```

---

### Creating and Querying

Use standard Django ORM methods for CRUD operations:

```python
from django.db.models import TextField, IntegerField, Index
from canvas_sdk.v1.data.base import CustomModel


class Specialty(CustomModel):
    class Meta:
        indexes = [
            Index(fields=["name"]),
        ]

    name = TextField()
    description = TextField()
    years_required = IntegerField()


# Create
specialty = Specialty.objects.create(
    name="Cardiology",
    description="Heart and cardiovascular system",
    years_required=3
)

# Read
specialty = Specialty.objects.get(dbid=specialty.dbid)
all_specialties = Specialty.objects.all()

# Update
specialty.description = "Diseases of the heart and blood vessels"
specialty.save()

# Delete
specialty.delete()

# Filter
cardio_specialties = Specialty.objects.filter(name__icontains="cardio")
```

---

## One-to-One Relationships

Use `OneToOneField` to create a one-to-one relationship between models.

### Defining the Model

```python
from django.db.models import OneToOneField, TextField, IntegerField, DO_NOTHING
from canvas_sdk.v1.data.base import CustomModel
from staff_plus.models.proxy import StaffProxy


class Biography(CustomModel):
    """Extended profile information for a staff member"""

    staff = OneToOneField(
        StaffProxy,
        to_field="dbid",
        on_delete=DO_NOTHING,
        related_name="biography"
    )
    biography = TextField()
    language = TextField()
    practicing_since = IntegerField()
```

**Note:** The `staff` foreign key field is automatically indexed by the SDK.

### Creating and Accessing

```python
from datetime import datetime
from django.db.models import OneToOneField, TextField, IntegerField, DO_NOTHING
from canvas_sdk.v1.data import Staff, CustomAttributeMixin, CustomAttributeAwareManager
from canvas_sdk.v1.data.base import CustomModel


class StaffProxy(Staff, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


class Biography(CustomModel):
    staff = OneToOneField(
        StaffProxy,
        to_field="dbid",
        on_delete=DO_NOTHING,
        related_name="biography"
    )
    biography = TextField()
    language = TextField()
    practicing_since = IntegerField()


# Create a biography for a staff member
staff = StaffProxy.objects.get(id="staff-uuid")
biography = Biography.objects.create(
    staff=staff,
    biography="Board-certified cardiologist with 15 years experience",
    language="English",
    practicing_since=2008
)

# Access from staff (forward relation)
bio = Biography.objects.get(staff=staff)

# Access from staff (reverse relation)
staff = StaffProxy.objects.get(id="staff-uuid")
bio_text = staff.biography.biography  # Access via related_name
years_experience = datetime.today().year - staff.biography.practicing_since
```

### Updating One-to-One Relations

```python
from django.db.models import OneToOneField, TextField, IntegerField, DO_NOTHING
from canvas_sdk.v1.data import Staff, CustomAttributeMixin, CustomAttributeAwareManager
from canvas_sdk.v1.data.base import CustomModel


class StaffProxy(Staff, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


class Biography(CustomModel):
    staff = OneToOneField(
        StaffProxy,
        to_field="dbid",
        on_delete=DO_NOTHING,
        related_name="biography"
    )
    biography = TextField()
    language = TextField()
    practicing_since = IntegerField()


# Get or create pattern
staff = StaffProxy.objects.get(id="staff-uuid")

if not hasattr(staff, 'biography') or staff.biography is None:
    # Create new biography
    Biography.objects.create(
        staff=staff,
        biography="New biography text",
        language="English",
        practicing_since=2010
    )
else:
    # Update existing biography
    staff.biography.biography = "Updated biography text"
    staff.biography.practicing_since = 2010
    staff.biography.save()
```

---

## One-to-Many Relationships

Use `ForeignKey` to create a one-to-many relationship.

### Defining the Model

```python
from django.db.models import ForeignKey, TextField, DateTimeField, DO_NOTHING, Index
from datetime import datetime
from canvas_sdk.v1.data.base import CustomModel
from staff_plus.models.proxy import StaffProxy


class Language(CustomModel):
    """Languages spoken by a staff member"""

    class Meta:
        # Add indexes for non-foreign-key fields used in queries
        indexes = [
            Index(fields=["code"]),  # If you filter by language code
        ]

    staff = ForeignKey(
        StaffProxy,
        to_field="dbid",
        on_delete=DO_NOTHING,
        related_name="languages"
    )
    name = TextField()
    code = TextField()
    created = DateTimeField(default=datetime.now)
    updated = DateTimeField(default=datetime.now)
```

**Note:** The `staff` foreign key field is automatically indexed. Add indexes for other fields like `code` if you frequently filter by them.

### Creating and Accessing

```python
from datetime import datetime
from django.db.models import ForeignKey, TextField, DateTimeField, DO_NOTHING, Index
from canvas_sdk.v1.data import Staff, CustomAttributeMixin, CustomAttributeAwareManager
from canvas_sdk.v1.data.base import CustomModel


class StaffProxy(Staff, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


class Language(CustomModel):
    class Meta:
        indexes = [
            Index(fields=["code"]),
        ]

    staff = ForeignKey(
        StaffProxy,
        to_field="dbid",
        on_delete=DO_NOTHING,
        related_name="languages"
    )
    name = TextField()
    code = TextField()
    created = DateTimeField(default=datetime.now)
    updated = DateTimeField(default=datetime.now)


# Create multiple languages for a staff member
staff = StaffProxy.objects.get(id="staff-uuid")

Language.objects.create(staff=staff, name="English", code="en")
Language.objects.create(staff=staff, name="Spanish", code="es")
Language.objects.create(staff=staff, name="Mandarin", code="zh")

# Access all languages for a staff member (reverse relation)
languages = staff.languages.all()
language_names = [lang.name for lang in languages]  # ["English", "Spanish", "Mandarin"]

# Filter languages
english_speakers = StaffProxy.objects.filter(languages__code="en").distinct()
```

### Querying Across Relationships

```python
from django.db.models import Count, ForeignKey, TextField, DateTimeField, DO_NOTHING, Index
from datetime import datetime
from canvas_sdk.v1.data import Staff, CustomAttributeMixin, CustomAttributeAwareManager
from canvas_sdk.v1.data.base import CustomModel


class StaffProxy(Staff, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


class Language(CustomModel):
    class Meta:
        indexes = [
            Index(fields=["code"]),
        ]

    staff = ForeignKey(
        StaffProxy,
        to_field="dbid",
        on_delete=DO_NOTHING,
        related_name="languages"
    )
    name = TextField()
    code = TextField()
    created = DateTimeField(default=datetime.now)
    updated = DateTimeField(default=datetime.now)


# Find all staff who speak Spanish
spanish_speakers = StaffProxy.objects.filter(
    languages__name="Spanish"
).distinct()

# Find staff who speak multiple specific languages
bilingual_staff = StaffProxy.objects.filter(
    languages__code__in=["en", "es"]
).distinct()

# Count languages per staff member
staff_with_counts = (
    StaffProxy.objects
    .annotate(language_count=Count('languages'))
    .filter(language_count__gte=2)
)
```

### Bulk Creation

```python
from datetime import datetime
from django.db.models import ForeignKey, TextField, DateTimeField, DO_NOTHING, Index
from canvas_sdk.v1.data import Staff, CustomAttributeMixin, CustomAttributeAwareManager
from canvas_sdk.v1.data.base import CustomModel


class StaffProxy(Staff, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


class Language(CustomModel):
    class Meta:
        indexes = [
            Index(fields=["code"]),
        ]

    staff = ForeignKey(
        StaffProxy,
        to_field="dbid",
        on_delete=DO_NOTHING,
        related_name="languages"
    )
    name = TextField()
    code = TextField()
    created = DateTimeField(default=datetime.now)
    updated = DateTimeField(default=datetime.now)


# Create multiple related objects efficiently
staff = StaffProxy.objects.get(id="staff-uuid")

languages_to_create = [
    Language(staff=staff, name="English", code="en"),
    Language(staff=staff, name="French", code="fr"),
    Language(staff=staff, name="German", code="de")
]

Language.objects.bulk_create(languages_to_create)
```

---

## Many-to-Many Relationships

Implement many-to-many relationships using an explicit junction table with `ForeignKey` fields.

### Defining the Models

```python
from django.db.models import ForeignKey, TextField, Index, CASCADE
from canvas_sdk.v1.data.base import CustomModel
from staff_plus.models.proxy import StaffProxy


class Specialty(CustomModel):
    """A medical specialty"""

    class Meta:
        # Index the name field since we filter by it
        indexes = [
            Index(fields=["name"]),
        ]

    name = TextField()

    def __str__(self):
        return f"{self.name}"


class StaffSpecialty(CustomModel):
    """Junction table for staff-to-specialty many-to-many relationship"""

    staff = ForeignKey(
        StaffProxy,
        to_field="dbid",
        on_delete=CASCADE,
        related_name="staff_specialties"
    )
    specialty = ForeignKey(
        Specialty,
        to_field="dbid",
        on_delete=CASCADE,
        related_name="staff_specialties"
    )
```

**Note:** Both `staff` and `specialty` foreign key fields are automatically indexed by the SDK. You don't need to manually add indexes for foreign keys.

### Creating Associations

```python
from django.db.models import ForeignKey, TextField, Index, CASCADE
from canvas_sdk.v1.data import Staff, CustomAttributeMixin, CustomAttributeAwareManager
from canvas_sdk.v1.data.base import CustomModel


class StaffProxy(Staff, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


class Specialty(CustomModel):
    class Meta:
        indexes = [
            Index(fields=["name"]),
        ]

    name = TextField()


class StaffSpecialty(CustomModel):
    staff = ForeignKey(
        StaffProxy,
        to_field="dbid",
        on_delete=CASCADE,
        related_name="staff_specialties"
    )
    specialty = ForeignKey(
        Specialty,
        to_field="dbid",
        on_delete=CASCADE,
        related_name="staff_specialties"
    )


# Get or create specialties
cardiology, _ = Specialty.objects.get_or_create(name="Cardiology")
internal_med, _ = Specialty.objects.get_or_create(name="Internal Medicine")

# Associate staff with specialties
staff = StaffProxy.objects.get(id="staff-uuid")
StaffSpecialty.objects.create(staff=staff, specialty=cardiology)
StaffSpecialty.objects.create(staff=staff, specialty=internal_med)

# Bulk create associations
specialties = [cardiology, internal_med]
associations = [
    StaffSpecialty(staff=staff, specialty=specialty)
    for specialty in specialties
]
StaffSpecialty.objects.bulk_create(associations)
```

### Querying Many-to-Many

```python
from django.db.models import ForeignKey, TextField, Index, CASCADE
from canvas_sdk.v1.data import Staff, CustomAttributeMixin, CustomAttributeAwareManager
from canvas_sdk.v1.data.base import CustomModel


class StaffProxy(Staff, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


class Specialty(CustomModel):
    class Meta:
        indexes = [
            Index(fields=["name"]),
        ]

    name = TextField()


class StaffSpecialty(CustomModel):
    staff = ForeignKey(
        StaffProxy,
        to_field="dbid",
        on_delete=CASCADE,
        related_name="staff_specialties"
    )
    specialty = ForeignKey(
        Specialty,
        to_field="dbid",
        on_delete=CASCADE,
        related_name="staff_specialties"
    )


# Get all specialties for a staff member
staff = StaffProxy.objects.get(id="staff-uuid")
staff_specialty_links = staff.staff_specialties.all()
specialties = [link.specialty for link in staff_specialty_links]
specialty_names = [link.specialty.name for link in staff_specialty_links]

# Get all staff with a specific specialty
cardiology = Specialty.objects.get(name="Cardiology")
staff_with_cardiology = StaffSpecialty.objects.filter(
    specialty=cardiology
).select_related("staff")

for link in staff_with_cardiology:
    print(f"{link.staff.first_name} {link.staff.last_name}")

# Find staff by multiple specialties
specialty_names = ["Cardiology", "Internal Medicine"]
staff_ids = (
    StaffSpecialty.objects
    .filter(specialty__name__in=specialty_names)
    .values_list("staff_id", flat=True)
    .distinct()
)

matching_staff = StaffProxy.objects.filter(dbid__in=staff_ids)
```

### Optimizing Many-to-Many Queries

```python
from django.db.models import ForeignKey, TextField, Index, CASCADE
from canvas_sdk.v1.data import Staff, CustomAttributeMixin, CustomAttributeAwareManager
from canvas_sdk.v1.data.base import CustomModel


class StaffProxy(Staff, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


class Specialty(CustomModel):
    class Meta:
        indexes = [
            Index(fields=["name"]),
        ]

    name = TextField()


class StaffSpecialty(CustomModel):
    staff = ForeignKey(
        StaffProxy,
        to_field="dbid",
        on_delete=CASCADE,
        related_name="staff_specialties"
    )
    specialty = ForeignKey(
        Specialty,
        to_field="dbid",
        on_delete=CASCADE,
        related_name="staff_specialties"
    )


# Prefetch related data to avoid N+1 queries
staff_members = (
    StaffProxy.objects
    .prefetch_related("staff_specialties__specialty")
    .all()
)

for staff in staff_members:
    specialties = [
        link.specialty.name
        for link in staff.staff_specialties.all()
    ]
    print(f"{staff.first_name}: {', '.join(specialties)}")
```

### Updating Associations

```python
from django.db.models import ForeignKey, TextField, Index, CASCADE
from canvas_sdk.v1.data import Staff, CustomAttributeMixin, CustomAttributeAwareManager
from canvas_sdk.v1.data.base import CustomModel


class StaffProxy(Staff, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


class Specialty(CustomModel):
    class Meta:
        indexes = [
            Index(fields=["name"]),
        ]

    name = TextField()


class StaffSpecialty(CustomModel):
    staff = ForeignKey(
        StaffProxy,
        to_field="dbid",
        on_delete=CASCADE,
        related_name="staff_specialties"
    )
    specialty = ForeignKey(
        Specialty,
        to_field="dbid",
        on_delete=CASCADE,
        related_name="staff_specialties"
    )


# Replace all specialties for a staff member
staff = StaffProxy.objects.get(id="staff-uuid")
new_specialties = ["Cardiology", "Pulmonology"]

# Clear existing associations
StaffSpecialty.objects.filter(staff=staff).delete()

# Create new associations
for specialty_name in new_specialties:
    specialty, _ = Specialty.objects.get_or_create(name=specialty_name)
    StaffSpecialty.objects.create(staff=staff, specialty=specialty)
```

---

## Advanced Patterns

### Combining techniques

Use multiple techniques together for maximum flexibility:

```python
from datetime import datetime
from django.db.models import (
    ForeignKey, OneToOneField, TextField, IntegerField,
    Index, CASCADE, DO_NOTHING
)
from canvas_sdk.v1.data import Staff, CustomAttributeMixin, CustomAttributeAwareManager
from canvas_sdk.v1.data.base import CustomModel


class StaffProxy(Staff, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


class Biography(CustomModel):
    staff = OneToOneField(
        StaffProxy,
        to_field="dbid",
        on_delete=DO_NOTHING,
        related_name="biography"
    )
    biography = TextField()
    language = TextField()
    practicing_since = IntegerField()


class Specialty(CustomModel):
    class Meta:
        indexes = [
            Index(fields=["name"]),
        ]

    name = TextField()


class StaffSpecialty(CustomModel):
    staff = ForeignKey(
        StaffProxy,
        to_field="dbid",
        on_delete=CASCADE,
        related_name="staff_specialties"
    )
    specialty = ForeignKey(
        Specialty,
        to_field="dbid",
        on_delete=CASCADE,
        related_name="staff_specialties"
    )


# Get staff with all data types
staff = StaffProxy.objects.get(id="staff-uuid")

# Custom data model (structured, one-to-one)
biography_text = staff.biography.biography
practicing_since = staff.biography.practicing_since

# Custom data model (structured, many-to-many)
specialties = [
    link.specialty.name
    for link in staff.staff_specialties.all()
]

# CustomAttribute (flexible, key-value)
accepting_patients = staff.get_attribute("accepting_patients")
years_experience = datetime.today().year - practicing_since

profile = {
    "first_name": staff.first_name,
    "last_name": staff.last_name,
    "biography": biography_text,
    "specialties": specialties,
    "years_experience": years_experience,
    "accepting_patients": accepting_patients
}
```

### Query Optimization

Combine prefetching strategies for optimal performance:

```python
from datetime import datetime
from django.db.models import (
    ForeignKey, OneToOneField, TextField, IntegerField, DateTimeField,
    Index, CASCADE, DO_NOTHING
)
from canvas_sdk.v1.data import Staff, CustomAttributeMixin, CustomAttributeAwareManager
from canvas_sdk.v1.data.base import CustomModel


class StaffProxy(Staff, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


class Biography(CustomModel):
    staff = OneToOneField(
        StaffProxy,
        to_field="dbid",
        on_delete=DO_NOTHING,
        related_name="biography"
    )
    biography = TextField()
    practicing_since = IntegerField()


class Specialty(CustomModel):
    class Meta:
        indexes = [
            Index(fields=["name"]),
        ]

    name = TextField()


class StaffSpecialty(CustomModel):
    staff = ForeignKey(
        StaffProxy,
        to_field="dbid",
        on_delete=CASCADE,
        related_name="staff_specialties"
    )
    specialty = ForeignKey(
        Specialty,
        to_field="dbid",
        on_delete=CASCADE,
        related_name="staff_specialties"
    )


class Language(CustomModel):
    staff = ForeignKey(
        StaffProxy,
        to_field="dbid",
        on_delete=DO_NOTHING,
        related_name="languages"
    )
    name = TextField()
    code = TextField()


# Fetch staff with all related data in one query
staff_members = (
    StaffProxy.objects
    .with_only(["accepting_patients", "last_updated"])  # CustomAttributes
    .prefetch_related("biography")  # One-to-one
    .prefetch_related("staff_specialties__specialty")  # Many-to-many
    .prefetch_related("languages")  # One-to-many
    .all()
)

# Access all data without additional queries
for staff in staff_members:
    bio = staff.biography.biography if staff.biography else None
    specialties = [link.specialty.name for link in staff.staff_specialties.all()]
    languages = [lang.name for lang in staff.languages.all()]
    accepting = staff.get_attribute("accepting_patients")
```

---

## Testing Custom Data

The Canvas SDK provides comprehensive testing utilities for custom data. Tests run within database transactions that automatically roll back, ensuring isolation between test cases.

### Test Setup

Install the test utilities extra to enable pytest-based testing:

```bash
uv add "canvas[test-utils]"
```

Run your tests with:

```bash
uv run pytest
```

Each test runs inside a transaction and automatically rolls back at the end, providing clean isolation without manual cleanup.

See [Testing Utilities](/sdk/testing-utils/) for complete setup instructions.

---

### Creating Factories for Proxy Models

Define factories for proxy models by extending the base SDK factories:

```python
import factory
from canvas_sdk.test_utils.factories import StaffFactory, PatientFactory
from staff_plus.models.proxy import StaffProxy, PatientProxy


class StaffProxyFactory(StaffFactory, factory.django.DjangoModelFactory[StaffProxy]):
    """Factory for creating StaffProxy instances."""
    class Meta:
        model = StaffProxy


class PatientProxyFactory(PatientFactory, factory.django.DjangoModelFactory[PatientProxy]):
    """Factory for creating PatientProxy instances."""
    class Meta:
        model = PatientProxy
```

---

### Creating Factories for Custom Models

Define factories for your custom models with appropriate field values:

```python
import factory
from staff_plus.models.specialty import Specialty, StaffSpecialty
from staff_plus.models.biography import Biography


class SpecialtyFactory(factory.django.DjangoModelFactory):
    """Factory for creating Specialty instances."""
    class Meta:
        model = Specialty
        django_get_or_create = ("name",)  # Avoid duplicate specialties

    name = factory.Faker("random_element", elements=[
        "Cardiology", "Dermatology", "Neurology", "Orthopedics",
        "Pediatrics", "Psychiatry", "Radiology", "Surgery"
    ])


class BiographyFactory(factory.django.DjangoModelFactory):
    """Factory for creating Biography instances."""
    class Meta:
        model = Biography

    staff = factory.SubFactory(StaffProxyFactory)
    biography = factory.Faker("paragraph", nb_sentences=5)
    language = factory.Faker("language_name")
    practicing_since = factory.Faker("year")


class StaffSpecialtyFactory(factory.django.DjangoModelFactory):
    """Factory for many-to-many relationship."""
    class Meta:
        model = StaffSpecialty

    staff = factory.SubFactory(StaffProxyFactory)
    specialty = factory.SubFactory(SpecialtyFactory)
```

---

### Testing CustomAttributes

Test that CustomAttributes persist correctly and maintain isolation between objects:

```python
from datetime import datetime
import factory
from canvas_sdk.test_utils.factories import StaffFactory, PatientFactory
from canvas_sdk.v1.data import Staff, Patient, CustomAttributeMixin, CustomAttributeAwareManager


class StaffProxy(Staff, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


class PatientProxy(Patient, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


class StaffProxyFactory(StaffFactory, factory.django.DjangoModelFactory[StaffProxy]):
    class Meta:
        model = StaffProxy


class PatientProxyFactory(PatientFactory, factory.django.DjangoModelFactory[PatientProxy]):
    class Meta:
        model = PatientProxy


def test_custom_attributes_on_proxy():
    """Test CustomAttributes on proxy models."""
    # Create test instances
    staff = StaffProxyFactory.create()
    patient = PatientProxyFactory.create()

    # Set attributes
    staff.set_attribute("specialty", "Cardiology")
    staff.set_attribute("years_experience", 15)
    patient.set_attribute("preferred_language", "Spanish")

    # Verify attributes persist to database
    staff_from_db = StaffProxy.objects.get(id=staff.id)
    assert staff_from_db.get_attribute("specialty") == "Cardiology"
    assert staff_from_db.get_attribute("years_experience") == 15

    # Verify attributes are isolated between objects
    assert staff_from_db.get_attribute("preferred_language") is None
    patient_from_db = PatientProxy.objects.get(id=patient.id)
    assert patient_from_db.get_attribute("specialty") is None


def test_custom_attributes_multiple_types():
    """Test CustomAttributes with different value types."""
    from datetime import datetime

    staff = StaffProxyFactory.create()

    # Set different types
    staff.set_attribute("text_field", "some text")
    staff.set_attribute("int_field", 42)
    staff.set_attribute("bool_field", True)
    staff.set_attribute("float_field", 3.14)
    staff.set_attribute("datetime_field", datetime.now())
    staff.set_attribute("json_field", {"key": "value", "list": [1, 2, 3]})

    # Verify retrieval
    staff_from_db = StaffProxy.objects.get(id=staff.id)
    assert staff_from_db.get_attribute("text_field") == "some text"
    assert staff_from_db.get_attribute("int_field") == 42
    assert staff_from_db.get_attribute("bool_field") is True
    assert staff_from_db.get_attribute("json_field") == {"key": "value", "list": [1, 2, 3]}


def test_set_attributes_bulk():
    """Test setting multiple attributes at once."""
    staff = StaffProxyFactory.create()

    attributes = {
        "accepting_patients": True,
        "board_certified": True,
        "languages_spoken": ["English", "Spanish"],
        "years_experience": 10
    }

    staff.set_attributes(attributes)

    staff_from_db = StaffProxy.objects.get(id=staff.id)
    assert staff_from_db.get_attribute("accepting_patients") is True
    assert staff_from_db.get_attribute("board_certified") is True
    assert staff_from_db.get_attribute("years_experience") == 10


def test_delete_attribute():
    """Test deleting CustomAttributes."""
    staff = StaffProxyFactory.create()
    staff.set_attribute("temporary_field", "value")

    # Verify it exists
    assert staff.get_attribute("temporary_field") == "value"

    # Delete and verify
    deleted = staff.delete_attribute("temporary_field")
    assert deleted is True
    assert staff.get_attribute("temporary_field") is None

    # Deleting non-existent attribute returns False
    deleted_again = staff.delete_attribute("temporary_field")
    assert deleted_again is False
```

---

### Testing AttributeHub

Test that AttributeHub stores and retrieves data correctly:

```python
from datetime import datetime
import factory
from canvas_sdk.test_utils.factories import StaffFactory
from canvas_sdk.v1.data import AttributeHub, Staff, CustomAttributeMixin, CustomAttributeAwareManager


class StaffProxy(Staff, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


class StaffProxyFactory(StaffFactory, factory.django.DjangoModelFactory[StaffProxy]):
    class Meta:
        model = StaffProxy


def test_attribute_hub_creation():
    """Test creating and using AttributeHub."""
    # Create hub
    hub = AttributeHub.objects.create(
        type="staff_profile",
        externally_exposable_id="staff_123"
    )

    # Set attributes
    hub.set_attribute("last_sync", datetime.now())
    hub.set_attribute("external_id", "ext_456")

    # Verify persistence
    hub_from_db = AttributeHub.objects.get(dbid=hub.dbid)
    assert hub_from_db.get_attribute("external_id") == "ext_456"


def test_attribute_hub_get_or_create():
    """Test get_or_create pattern with AttributeHub."""
    staff = StaffProxyFactory.create()

    # First call creates
    hub1, created1 = AttributeHub.objects.get_or_create(
        type="staff_sync",
        externally_exposable_id=f"staff:{staff.id}"
    )
    assert created1 is True

    hub1.set_attribute("data", {"key": "value"})

    # Second call retrieves existing
    hub2, created2 = AttributeHub.objects.get_or_create(
        type="staff_sync",
        externally_exposable_id=f"staff:{staff.id}"
    )
    assert created2 is False
    assert hub1.dbid == hub2.dbid
    assert hub2.get_attribute("data") == {"key": "value"}


def test_attribute_hub_json_storage():
    """Test storing complex JSON in AttributeHub."""
    hub = AttributeHub.objects.create(
        type="profile",
        externally_exposable_id="test_123"
    )

    profile_data = {
        "biography": "Experienced physician",
        "specialties": ["Cardiology", "Internal Medicine"],
        "languages": ["English", "Spanish"],
        "practicing_since": 2005,
        "accepting_patients": False
    }

    hub.set_attribute("profile", profile_data)

    hub_from_db = AttributeHub.objects.get(dbid=hub.dbid)
    retrieved = hub_from_db.get_attribute("profile")

    assert retrieved == profile_data
    assert retrieved["biography"] == "Experienced physician"
    assert len(retrieved["specialties"]) == 2
```

---

### Testing Custom Models

Test custom model creation, relationships, and queries:

```python
import factory
from datetime import datetime
from django.db.models import (
    ForeignKey, OneToOneField, TextField, IntegerField, DateTimeField,
    Index, CASCADE, DO_NOTHING
)
from canvas_sdk.test_utils.factories import StaffFactory
from canvas_sdk.v1.data import Staff, CustomAttributeMixin, CustomAttributeAwareManager
from canvas_sdk.v1.data.base import CustomModel


class StaffProxy(Staff, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


class StaffProxyFactory(StaffFactory, factory.django.DjangoModelFactory[StaffProxy]):
    class Meta:
        model = StaffProxy


class Specialty(CustomModel):
    class Meta:
        indexes = [
            Index(fields=["name"]),
        ]

    name = TextField()


class Biography(CustomModel):
    staff = OneToOneField(
        StaffProxy,
        to_field="dbid",
        on_delete=DO_NOTHING,
        related_name="biography"
    )
    biography = TextField()
    language = TextField()
    practicing_since = IntegerField()


class Language(CustomModel):
    staff = ForeignKey(
        StaffProxy,
        to_field="dbid",
        on_delete=DO_NOTHING,
        related_name="languages"
    )
    name = TextField()
    code = TextField()
    created = DateTimeField(default=datetime.now)


class StaffSpecialty(CustomModel):
    staff = ForeignKey(
        StaffProxy,
        to_field="dbid",
        on_delete=CASCADE,
        related_name="staff_specialties"
    )
    specialty = ForeignKey(
        Specialty,
        to_field="dbid",
        on_delete=CASCADE,
        related_name="staff_specialties"
    )


def test_custom_model_creation():
    """Test creating custom models."""
    specialty = Specialty.objects.create(name="Cardiology")
    assert specialty.dbid is not None
    assert specialty.name == "Cardiology"

    # Verify persistence
    specialty_from_db = Specialty.objects.get(dbid=specialty.dbid)
    assert specialty_from_db.name == "Cardiology"


def test_one_to_one_relationship():
    """Test one-to-one relationships."""
    staff = StaffProxyFactory.create()

    # Create related biography
    biography = Biography.objects.create(
        staff=staff,
        biography="Experienced cardiologist",
        language="English",
        practicing_since=2005
    )

    # Access from biography to staff
    assert biography.staff.id == staff.id

    # Access from staff to biography (reverse relation)
    staff_from_db = StaffProxy.objects.get(id=staff.id)
    assert staff_from_db.biography.biography == "Experienced cardiologist"
    assert staff_from_db.biography.practicing_since == 2005


def test_one_to_many_relationship():
    """Test one-to-many relationships."""
    staff = StaffProxyFactory.create()

    # Create multiple related languages
    Language.objects.create(staff=staff, name="English", code="en")
    Language.objects.create(staff=staff, name="Spanish", code="es")
    Language.objects.create(staff=staff, name="French", code="fr")

    # Access all languages via reverse relation
    languages = staff.languages.all()
    assert languages.count() == 3

    language_names = [lang.name for lang in languages]
    assert "English" in language_names
    assert "Spanish" in language_names
    assert "French" in language_names


def test_many_to_many_relationship():
    """Test many-to-many relationships via junction table."""
    staff = StaffProxyFactory.create()
    cardiology = Specialty.objects.create(name="Cardiology")
    internal_med = Specialty.objects.create(name="Internal Medicine")

    # Create associations
    StaffSpecialty.objects.create(staff=staff, specialty=cardiology)
    StaffSpecialty.objects.create(staff=staff, specialty=internal_med)

    # Query specialties for staff
    staff_specialties = staff.staff_specialties.all()
    assert staff_specialties.count() == 2

    specialty_names = [ss.specialty.name for ss in staff_specialties]
    assert "Cardiology" in specialty_names
    assert "Internal Medicine" in specialty_names

    # Query staff by specialty
    staff_ids = (
        StaffSpecialty.objects
        .filter(specialty__name="Cardiology")
        .values_list("staff_id", flat=True)
    )
    assert staff.dbid in staff_ids


def test_many_to_many_query_filtering():
    """Test querying across many-to-many relationships."""
    staff1 = StaffProxyFactory.create()
    staff2 = StaffProxyFactory.create()

    cardiology = Specialty.objects.create(name="Cardiology")
    neurology = Specialty.objects.create(name="Neurology")

    StaffSpecialty.objects.create(staff=staff1, specialty=cardiology)
    StaffSpecialty.objects.create(staff=staff2, specialty=neurology)
    StaffSpecialty.objects.create(staff=staff2, specialty=cardiology)

    # Find all staff with cardiology
    cardiology_staff_ids = (
        StaffSpecialty.objects
        .filter(specialty__name="Cardiology")
        .values_list("staff_id", flat=True)
    )

    assert staff1.dbid in cardiology_staff_ids
    assert staff2.dbid in cardiology_staff_ids

    # Find staff with multiple specialties
    multi_specialty_ids = (
        StaffSpecialty.objects
        .filter(specialty__name__in=["Cardiology", "Neurology"])
        .values_list("staff_id", flat=True)
        .distinct()
    )

    assert len(multi_specialty_ids) == 2
```

---

### Testing with Factories

Use factories to simplify test data creation:

```python
import factory
from django.db.models import OneToOneField, TextField, IntegerField, DO_NOTHING
from canvas_sdk.test_utils.factories import StaffFactory
from canvas_sdk.v1.data import Staff, CustomAttributeMixin, CustomAttributeAwareManager
from canvas_sdk.v1.data.base import CustomModel


class StaffProxy(Staff, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


class StaffProxyFactory(StaffFactory, factory.django.DjangoModelFactory[StaffProxy]):
    class Meta:
        model = StaffProxy


class Biography(CustomModel):
    staff = OneToOneField(
        StaffProxy,
        to_field="dbid",
        on_delete=DO_NOTHING,
        related_name="biography"
    )
    biography = TextField()
    language = TextField()
    practicing_since = IntegerField()


class BiographyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Biography

    staff = factory.SubFactory(StaffProxyFactory)
    biography = factory.Faker("paragraph", nb_sentences=5)
    language = factory.Faker("language_name")
    practicing_since = factory.Faker("year")


def test_with_factories():
    """Test using factories for quick data setup."""
    # Create staff with biography using factories
    biography = BiographyFactory.create()

    assert biography.staff is not None
    assert biography.biography is not None
    assert biography.practicing_since is not None

    # Factory automatically created the related staff
    staff = biography.staff
    assert staff.first_name is not None


class StaffSpecialty(CustomModel):
    staff = ForeignKey(
        StaffProxy,
        to_field="dbid",
        on_delete=CASCADE,
        related_name="staff_specialties"
    )
    specialty = ForeignKey(
        Specialty,
        to_field="dbid",
        on_delete=CASCADE,
        related_name="staff_specialties"
    )


class StaffSpecialtyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StaffSpecialty

    staff = factory.SubFactory(StaffProxyFactory)
    specialty = factory.SubFactory(SpecialtyFactory)


def test_many_to_many_with_factories():
    """Test many-to-many relationships with factories."""
    # Create staff-specialty associations
    ss1 = StaffSpecialtyFactory.create()
    ss2 = StaffSpecialtyFactory.create(staff=ss1.staff)  # Same staff, different specialty

    # Verify relationships
    assert ss1.staff.staff_specialties.count() == 2


def test_factory_with_custom_attributes():
    """Combine factories with CustomAttributes."""
    staff = StaffProxyFactory.create()

    # Add custom attributes to factory-created object
    staff.set_attributes({
        "board_certified": True,
        "accepting_patients": True,
        "patient_capacity": 100
    })

    # Verify both factory fields and custom attributes
    assert staff.first_name is not None  # From factory
    assert staff.get_attribute("board_certified") is True  # Custom attribute
```

---

### Testing Queries and Prefetching

Test that prefetching and query optimization work correctly:

```python
import factory
from django.db.models import (
    ForeignKey, OneToOneField, TextField, IntegerField,
    Index, CASCADE, DO_NOTHING, Count
)
from canvas_sdk.test_utils.factories import StaffFactory
from canvas_sdk.v1.data import Staff, CustomAttributeMixin, CustomAttributeAwareManager
from canvas_sdk.v1.data.base import CustomModel


class StaffProxy(Staff, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


class StaffProxyFactory(StaffFactory, factory.django.DjangoModelFactory[StaffProxy]):
    class Meta:
        model = StaffProxy


class Biography(CustomModel):
    staff = OneToOneField(
        StaffProxy,
        to_field="dbid",
        on_delete=DO_NOTHING,
        related_name="biography"
    )
    biography = TextField()
    practicing_since = IntegerField()


class Specialty(CustomModel):
    class Meta:
        indexes = [
            Index(fields=["name"]),
        ]

    name = TextField()


class StaffSpecialty(CustomModel):
    staff = ForeignKey(
        StaffProxy,
        to_field="dbid",
        on_delete=CASCADE,
        related_name="staff_specialties"
    )
    specialty = ForeignKey(
        Specialty,
        to_field="dbid",
        on_delete=CASCADE,
        related_name="staff_specialties"
    )


class BiographyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Biography

    staff = factory.SubFactory(StaffProxyFactory)
    biography = factory.Faker("paragraph")
    practicing_since = factory.Faker("year")


class SpecialtyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Specialty

    name = factory.Faker("word")


class StaffSpecialtyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StaffSpecialty

    staff = factory.SubFactory(StaffProxyFactory)
    specialty = factory.SubFactory(SpecialtyFactory)


def test_custom_attributes_prefetch():
    """Test prefetching CustomAttributes."""
    staff1 = StaffProxyFactory.create()
    staff2 = StaffProxyFactory.create()

    staff1.set_attribute("specialty", "Cardiology")
    staff2.set_attribute("specialty", "Neurology")

    # Query with automatic prefetch
    all_staff = StaffProxy.objects.all()

    # Access attributes without additional queries
    for staff in all_staff:
        specialty = staff.get_attribute("specialty")
        assert specialty in [None, "Cardiology", "Neurology"]


def test_custom_attributes_with_only():
    """Test selective attribute prefetching."""
    staff = StaffProxyFactory.create()
    staff.set_attributes({
        "specialty": "Cardiology",
        "years_experience": 15,
        "accepting_patients": True
    })

    # Prefetch only specific attributes
    staff_from_db = (
        StaffProxy.objects
        .with_only(["specialty", "accepting_patients"])
        .get(id=staff.id)
    )

    # Prefetched attributes accessible
    assert staff_from_db.get_attribute("specialty") == "Cardiology"
    assert staff_from_db.get_attribute("accepting_patients") is True


def test_relationship_prefetch():
    """Test prefetching related models."""
    staff1 = StaffProxyFactory.create()
    staff2 = StaffProxyFactory.create()

    BiographyFactory.create(staff=staff1)
    BiographyFactory.create(staff=staff2)

    cardiology = SpecialtyFactory.create(name="Cardiology")
    StaffSpecialtyFactory.create(staff=staff1, specialty=cardiology)
    StaffSpecialtyFactory.create(staff=staff2, specialty=cardiology)

    # Prefetch all relationships
    all_staff = (
        StaffProxy.objects
        .prefetch_related("biography")
        .prefetch_related("staff_specialties__specialty")
        .all()
    )

    # Access without additional queries
    for staff in all_staff:
        bio = staff.biography.biography
        specialties = [ss.specialty.name for ss in staff.staff_specialties.all()]
        assert bio is not None
        assert len(specialties) > 0
```

---

### Testing Data Integrity

Test data validation, constraints, and cascade behavior:

```python
import factory
from django.db.models import ForeignKey, TextField, Index, CASCADE
from canvas_sdk.test_utils.factories import StaffFactory
from canvas_sdk.v1.data import Staff, CustomAttributeMixin, CustomAttributeAwareManager
from canvas_sdk.v1.data.base import CustomModel
from canvas_sdk.v1.data.custom_attribute import CustomAttribute


class StaffProxy(Staff, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


class StaffProxyFactory(StaffFactory, factory.django.DjangoModelFactory[StaffProxy]):
    class Meta:
        model = StaffProxy


class Specialty(CustomModel):
    class Meta:
        indexes = [
            Index(fields=["name"]),
        ]

    name = TextField()


class SpecialtyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Specialty

    name = factory.Faker("word")


class StaffSpecialty(CustomModel):
    staff = ForeignKey(
        StaffProxy,
        to_field="dbid",
        on_delete=CASCADE,
        related_name="staff_specialties"
    )
    specialty = ForeignKey(
        Specialty,
        to_field="dbid",
        on_delete=CASCADE,
        related_name="staff_specialties"
    )


class StaffSpecialtyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StaffSpecialty

    staff = factory.SubFactory(StaffProxyFactory)
    specialty = factory.SubFactory(SpecialtyFactory)


def test_cascade_delete():
    """Test CASCADE delete behavior."""
    staff = StaffProxyFactory.create()
    specialty = SpecialtyFactory.create()
    ss = StaffSpecialtyFactory.create(staff=staff, specialty=specialty)

    # Delete specialty should cascade to junction table
    specialty_id = specialty.dbid
    specialty.delete()

    # Junction table record should be deleted
    assert not StaffSpecialty.objects.filter(specialty_id=specialty_id).exists()


def test_unique_constraint():
    """Test unique constraints on CustomAttributes."""
    staff = StaffProxyFactory.create()

    # Set attribute
    staff.set_attribute("unique_field", "value1")

    # Setting same attribute name should update, not create duplicate
    staff.set_attribute("unique_field", "value2")

    # Verify only one attribute exists
    staff_from_db = StaffProxy.objects.get(id=staff.id)
    assert staff_from_db.get_attribute("unique_field") == "value2"

    # Verify no duplicates in database
    count = CustomAttribute.objects.filter(
        object_id=staff.dbid,
        name="unique_field"
    ).count()
    assert count == 1


def test_transaction_rollback():
    """Verify that tests automatically roll back."""
    # This test demonstrates automatic rollback
    # Data created here won't exist in subsequent tests

    staff = StaffProxyFactory.create()
    staff_id = staff.id

    specialty = SpecialtyFactory.create(name="Test Specialty")

    # After this test, these objects won't exist in other tests
    # due to automatic transaction rollback
    assert staff_id is not None
    assert specialty.name == "Test Specialty"
```

---

### Testing Best Practices

1. **Use factories** for consistent test data generation
2. **Test isolation** - Each test should be independent and not rely on data from other tests
3. **Test both directions** of relationships (forward and reverse)
4. **Verify persistence** by reloading objects from the database
5. **Test edge cases** like None values, empty lists, and missing relationships
6. **Use descriptive test names** that explain what is being tested
7. **Test query optimization** to ensure prefetching works as expected
8. **Verify constraints** like uniqueness and cascade behavior

---

## Best Practices

### Data Privacy and Isolation

1. **Understand plugin data scoping** - All custom data is isolated to your plugin by default
2. **Use APIs for data sharing** - Never attempt to access another plugin's data directly
3. **Implement proper authorization** - Secure all APIs that expose plugin data
4. **Follow PHI guidelines** - Treat all patient-related custom data with appropriate security measures

### Model Design

1. **Use proxy models** for adding CustomAttributes to existing SDK models
2. **Define Meta classes** with appropriate indexes for custom models
3. **Foreign keys are automatically indexed** - Only manually index fields you use in `.filter()` queries
4. **Index fields used in queries** - Add indexes to the Meta class for fields frequently used in lookups
5. **Use related_name** for clear reverse relation access
6. **Choose CASCADE or DO_NOTHING** carefully based on your data retention needs

### Schema Management

1. **Additive changes only** - Only add new fields; never remove or rename tables or columns
2. **No database constraints** - Validate data in application code, not at the database level
3. **Nullable new fields** - New columns must allow null or provide default values
4. **Document schema versions** - Track changes in code comments for maintainability
5. **Test schema changes** - Thoroughly test additions in development before deploying

### Performance

1. **Prefetch related data** to avoid N+1 query problems
2. **Use bulk_create** for creating multiple objects
3. **Use select_related** for foreign key lookups
4. **Filter at the database level** rather than in Python

### Data Integrity

1. **Validate data** before saving to custom models
2. **Use transactions** for operations that modify multiple related objects
3. **Handle None values** when accessing one-to-one relations
4. **Use get_or_create** to avoid duplicate records

### Testing

1. **Use factories** to create test data consistently
2. **Test relationship queries** in both directions
3. **Verify cascade deletion** behavior
4. **Test with and without prefetching** to ensure correct behavior

---

## See Also

- [Data Models](/sdk/data/) - Core SDK data models
- [Testing Utils](/sdk/testing-utils/) - Factories for testing custom data
- [Effects](/sdk/effects/) - Effects for manipulating data
- [Canvas CLI](/sdk/canvas_cli/#simple-api-endpoints) - Simple API for sharing data between plugins
- [Secrets](/sdk/secrets/) - Managing API keys and sensitive configuration
