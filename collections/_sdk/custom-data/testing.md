---
title: "Testing Custom Data"
slug: "custom-data-testing"
---

The Canvas SDK provides comprehensive testing utilities for custom data. Tests run within database transactions that automatically roll back, ensuring isolation between test cases.

## Test Setup

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

## Creating Factories for Extended Models

Define factories for extended models by extending the base SDK factories:

```python
import factory
from canvas_sdk.test_utils.factories import StaffFactory, PatientFactory
from staff_plus.models import CustomStaff, CustomPatient


class CustomStaffFactory(StaffFactory, factory.django.DjangoModelFactory[CustomStaff]):
    """Factory for creating CustomStaff instances."""
    class Meta:
        model = CustomStaff


class CustomPatientFactory(PatientFactory, factory.django.DjangoModelFactory[CustomPatient]):
    """Factory for creating CustomPatient instances."""
    class Meta:
        model = CustomPatient
```

## Creating Factories for Custom Models

Define factories for your custom models with appropriate field values:

```python
import factory
from my_plugin.models import Specialty, StaffSpecialty
from my_plugin.models import Biography


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

    staff = factory.SubFactory(CustomStaffFactory)
    biography = factory.Faker("paragraph", nb_sentences=5)
    language = factory.Faker("language_name")
    practicing_since = factory.Faker("year")


class StaffSpecialtyFactory(factory.django.DjangoModelFactory):
    """Factory for many-to-many relationship."""
    class Meta:
        model = StaffSpecialty

    staff = factory.SubFactory(CustomStaffFactory)
    specialty = factory.SubFactory(SpecialtyFactory)
```

## Testing AttributeHub

Test that AttributeHub stores and retrieves data correctly:

```python
from datetime import datetime
import factory
from canvas_sdk.test_utils.factories import StaffFactory
from canvas_sdk.v1.data import AttributeHub, Staff, ModelExtension


class CustomStaff(Staff, ModelExtension):
    pass


class CustomStaffFactory(StaffFactory, factory.django.DjangoModelFactory[CustomStaff]):
    class Meta:
        model = CustomStaff


def test_attribute_hub_creation():
    """Test creating and using AttributeHub."""
    # Create hub
    hub = AttributeHub.objects.create(
        type="staff_profile",
        id="staff_123"
    )

    # Set attributes
    hub.set_attribute("last_sync", datetime.now())
    hub.set_attribute("external_id", "ext_456")

    # Verify persistence
    hub_from_db = AttributeHub.objects.get(dbid=hub.dbid)
    assert hub_from_db.get_attribute("external_id") == "ext_456"


def test_attribute_hub_get_or_create():
    """Test get_or_create pattern with AttributeHub."""
    staff = CustomStaffFactory.create()

    # First call creates
    hub1, created1 = AttributeHub.objects.get_or_create(
        type="staff_sync",
        id=f"staff:{staff.id}"
    )
    assert created1 is True

    hub1.set_attribute("data", {"key": "value"})

    # Second call retrieves existing
    hub2, created2 = AttributeHub.objects.get_or_create(
        type="staff_sync",
        id=f"staff:{staff.id}"
    )
    assert created2 is False
    assert hub1.dbid == hub2.dbid
    assert hub2.get_attribute("data") == {"key": "value"}


def test_attribute_hub_json_storage():
    """Test storing complex JSON in AttributeHub."""
    hub = AttributeHub.objects.create(
        type="profile",
        id="test_123"
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

## Testing Custom Models

Test custom model creation, relationships, and queries:

```python
import factory
from datetime import datetime
from django.db.models import (
    ForeignKey, ManyToManyField, OneToOneField, TextField, IntegerField,
    DateTimeField, Index, DO_NOTHING
)
from canvas_sdk.test_utils.factories import StaffFactory
from canvas_sdk.v1.data import Staff, ModelExtension
from canvas_sdk.v1.data.base import CustomModel


class CustomStaff(Staff, ModelExtension):
    pass


class CustomStaffFactory(StaffFactory, factory.django.DjangoModelFactory[CustomStaff]):
    class Meta:
        model = CustomStaff


class Specialty(CustomModel):
    class Meta:
        indexes = [
            Index(fields=["name"]),
        ]

    name = TextField()
    staff_members = ManyToManyField(
        "CustomStaff",
        through="StaffSpecialty",
        related_name="specialties",
    )


class Biography(CustomModel):
    staff = OneToOneField(
        CustomStaff,
        to_field="dbid",
        on_delete=DO_NOTHING,
        related_name="biography"
    )
    biography = TextField()
    language = TextField()
    practicing_since = IntegerField()


class Language(CustomModel):
    staff = ForeignKey(
        CustomStaff,
        to_field="dbid",
        on_delete=DO_NOTHING,
        related_name="languages"
    )
    name = TextField()
    code = TextField()
    created = DateTimeField(default=datetime.now)


class StaffSpecialty(CustomModel):
    staff = ForeignKey(
        CustomStaff,
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
    staff = CustomStaffFactory.create()

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
    staff_from_db = CustomStaff.objects.get(id=staff.id)
    assert staff_from_db.biography.biography == "Experienced cardiologist"
    assert staff_from_db.biography.practicing_since == 2005


def test_one_to_many_relationship():
    """Test one-to-many relationships."""
    staff = CustomStaffFactory.create()

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
    staff = CustomStaffFactory.create()
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
    staff1 = CustomStaffFactory.create()
    staff2 = CustomStaffFactory.create()

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


def test_many_to_many_through_field():
    """Test direct M2M traversal via ManyToManyField(through=...)."""
    staff = CustomStaffFactory.create()
    cardiology = Specialty.objects.create(name="Cardiology")
    internal_med = Specialty.objects.create(name="Internal Medicine")

    StaffSpecialty.objects.create(staff=staff, specialty=cardiology)
    StaffSpecialty.objects.create(staff=staff, specialty=internal_med)

    # Direct M2M traversal — Specialty → staff
    assert staff in cardiology.staff_members.all()

    # Reverse M2M traversal — staff → specialties
    specialty_names = [s.name for s in staff.specialties.all()]
    assert "Cardiology" in specialty_names
    assert "Internal Medicine" in specialty_names
```

## Testing with Factories

Use factories to simplify test data creation:

```python
import factory
from django.db.models import OneToOneField, TextField, IntegerField, DO_NOTHING
from canvas_sdk.test_utils.factories import StaffFactory
from canvas_sdk.v1.data import Staff, ModelExtension
from canvas_sdk.v1.data.base import CustomModel


class CustomStaff(Staff, ModelExtension):
    pass


class CustomStaffFactory(StaffFactory, factory.django.DjangoModelFactory[CustomStaff]):
    class Meta:
        model = CustomStaff


class Biography(CustomModel):
    staff = OneToOneField(
        CustomStaff,
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

    staff = factory.SubFactory(CustomStaffFactory)
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
        CustomStaff,
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


class StaffSpecialtyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StaffSpecialty

    staff = factory.SubFactory(CustomStaffFactory)
    specialty = factory.SubFactory(SpecialtyFactory)


def test_many_to_many_with_factories():
    """Test many-to-many relationships with factories."""
    # Create staff-specialty associations
    ss1 = StaffSpecialtyFactory.create()
    ss2 = StaffSpecialtyFactory.create(staff=ss1.staff)  # Same staff, different specialty

    # Verify relationships
    assert ss1.staff.staff_specialties.count() == 2
```

## Testing Queries and Prefetching

Test that prefetching and query optimization work correctly:

```python
import factory
from django.db.models import (
    ForeignKey, OneToOneField, TextField, IntegerField,
    Index, DO_NOTHING, Count
)
from canvas_sdk.test_utils.factories import StaffFactory
from canvas_sdk.v1.data import AttributeHub, Staff, ModelExtension
from canvas_sdk.v1.data.base import CustomModel


class CustomStaff(Staff, ModelExtension):
    pass


class CustomStaffFactory(StaffFactory, factory.django.DjangoModelFactory[CustomStaff]):
    class Meta:
        model = CustomStaff


class Biography(CustomModel):
    staff = OneToOneField(
        CustomStaff,
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
        CustomStaff,
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


class BiographyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Biography

    staff = factory.SubFactory(CustomStaffFactory)
    biography = factory.Faker("paragraph")
    practicing_since = factory.Faker("year")


class SpecialtyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Specialty

    name = factory.Faker("word")


class StaffSpecialtyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StaffSpecialty

    staff = factory.SubFactory(CustomStaffFactory)
    specialty = factory.SubFactory(SpecialtyFactory)


def test_attribute_hub_prefetch():
    """Test prefetching AttributeHub attributes."""
    hub1 = AttributeHub.objects.create(type="profile", id="staff_1")
    hub2 = AttributeHub.objects.create(type="profile", id="staff_2")

    hub1.set_attribute("specialty", "Cardiology")
    hub2.set_attribute("specialty", "Neurology")

    # Query with automatic prefetch (default behavior)
    hubs = AttributeHub.objects.filter(type="profile")

    # Access attributes without additional queries
    for hub in hubs:
        specialty = hub.get_attribute("specialty")
        assert specialty in ["Cardiology", "Neurology"]


def test_attribute_hub_with_only():
    """Test selective attribute prefetching on AttributeHub."""
    hub = AttributeHub.objects.create(type="profile", id="staff_1")
    hub.set_attributes({
        "specialty": "Cardiology",
        "years_experience": 15,
        "accepting_patients": True
    })

    # Prefetch only specific attributes
    hub_from_db = (
        AttributeHub.objects
        .with_only(["specialty", "accepting_patients"])
        .get(dbid=hub.dbid)
    )

    # Prefetched attributes accessible
    assert hub_from_db.get_attribute("specialty") == "Cardiology"
    assert hub_from_db.get_attribute("accepting_patients") is True


def test_relationship_prefetch():
    """Test prefetching related models."""
    staff1 = CustomStaffFactory.create()
    staff2 = CustomStaffFactory.create()

    BiographyFactory.create(staff=staff1)
    BiographyFactory.create(staff=staff2)

    cardiology = SpecialtyFactory.create(name="Cardiology")
    StaffSpecialtyFactory.create(staff=staff1, specialty=cardiology)
    StaffSpecialtyFactory.create(staff=staff2, specialty=cardiology)

    # Prefetch all relationships
    all_staff = (
        CustomStaff.objects
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


def test_select_related():
    """Test select_related for FK and OneToOne joins."""
    staff = CustomStaffFactory.create()
    BiographyFactory.create(staff=staff)
    StaffSpecialtyFactory.create(staff=staff)

    # select_related eagerly loads FK/O2O relations in a single query
    specialty_assoc = (
        StaffSpecialty.objects
        .select_related("staff", "specialty")
        .filter(staff=staff)
        .first()
    )

    assert specialty_assoc.staff.first_name is not None
    assert specialty_assoc.specialty.name is not None
```

## Testing Data Integrity

Test data validation, constraints, and cascade behavior:

```python
from datetime import datetime

import factory
import pytest
from django.db import IntegrityError
from django.db.models import (
    CASCADE, DateTimeField, ForeignKey, TextField, Index,
    UniqueConstraint, DO_NOTHING
)
from canvas_sdk.test_utils.factories import StaffFactory
from canvas_sdk.v1.data import AttributeHub, Staff, ModelExtension
from canvas_sdk.v1.data.base import CustomModel


class CustomStaff(Staff, ModelExtension):
    pass


class CustomStaffFactory(StaffFactory, factory.django.DjangoModelFactory[CustomStaff]):
    class Meta:
        model = CustomStaff


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
        CustomStaff,
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


class StaffSpecialtyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StaffSpecialty

    staff = factory.SubFactory(CustomStaffFactory)
    specialty = factory.SubFactory(SpecialtyFactory)


class Team(CustomModel):
    class Meta:
        constraints = [
            UniqueConstraint(fields=["name"], name="unique_team_name"),
        ]

    name = TextField()


class TeamMember(CustomModel):
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["team", "staff"],
                name="unique_team_staff",
            ),
        ]

    team = ForeignKey(Team, to_field="dbid", on_delete=CASCADE, related_name="members")
    staff = ForeignKey(
        CustomStaff, to_field="dbid", on_delete=DO_NOTHING, related_name="team_memberships"
    )
    joined_at = DateTimeField()


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team

    name = factory.Sequence(lambda n: f"Team {n + 1}")


class TeamMemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TeamMember

    team = factory.SubFactory(TeamFactory)
    staff = factory.SubFactory(CustomStaffFactory)
    joined_at = factory.LazyFunction(datetime.now)


def test_manual_cleanup_on_delete():
    """Test manual cleanup for DO_NOTHING foreign keys.

    ForeignKeys to SDK models (Staff, Patient, etc.) must use DO_NOTHING
    because those tables are managed externally. Related records must be
    deleted manually before deleting the parent.
    """
    staff = CustomStaffFactory.create()
    specialty = SpecialtyFactory.create()
    ss = StaffSpecialtyFactory.create(staff=staff, specialty=specialty)

    # With DO_NOTHING, you must clean up related records manually
    specialty_id = specialty.dbid
    StaffSpecialty.objects.filter(specialty_id=specialty_id).delete()
    specialty.delete()

    # Verify both are gone
    assert not StaffSpecialty.objects.filter(specialty_id=specialty_id).exists()
    assert not Specialty.objects.filter(dbid=specialty_id).exists()


def test_cascade_delete():
    """Test CASCADE deletion between custom models.

    ForeignKeys between your own CustomModels can use CASCADE to
    automatically delete related records.
    """
    team = TeamFactory.create()
    TeamMemberFactory.create(team=team)
    TeamMemberFactory.create(team=team)

    assert TeamMember.objects.filter(team=team).count() == 2

    # Deleting the team cascades to members
    team.delete()
    assert not TeamMember.objects.filter(team=team).exists()


def test_unique_constraint_violation():
    """Test that UniqueConstraint prevents duplicate records."""
    team = TeamFactory.create()
    staff = CustomStaffFactory.create()

    TeamMember.objects.create(team=team, staff=staff, joined_at=datetime.now())

    # Same team + staff violates the UniqueConstraint
    with pytest.raises(IntegrityError):
        TeamMember.objects.create(team=team, staff=staff, joined_at=datetime.now())


def test_attribute_hub_upsert():
    """Test that set_attribute updates existing values rather than creating duplicates."""
    hub = AttributeHub.objects.create(type="test", id="upsert_test")

    # Set attribute
    hub.set_attribute("field", "value1")

    # Setting same attribute name should update, not create duplicate
    hub.set_attribute("field", "value2")

    # Verify only the updated value exists
    hub_from_db = AttributeHub.objects.get(dbid=hub.dbid)
    assert hub_from_db.get_attribute("field") == "value2"


def test_transaction_rollback():
    """Verify that tests automatically roll back."""
    # This test demonstrates automatic rollback
    # Data created here won't exist in subsequent tests

    staff = CustomStaffFactory.create()
    staff_id = staff.id

    specialty = SpecialtyFactory.create(name="Test Specialty")

    # After this test, these objects won't exist in other tests
    # due to automatic transaction rollback
    assert staff_id is not None
    assert specialty.name == "Test Specialty"
```

## Testing proxy_field

The `proxy_field` descriptor lets a `ModelExtension` proxy transparently return another proxy class from a ForeignKey lookup, so you can access custom methods on related objects:

```python
from canvas_sdk.v1.data import Note, Patient, Staff, ModelExtension
from canvas_sdk.v1.data.base import proxy_field
from canvas_sdk.test_utils.factories import NoteFactory


class CustomPatient(Patient, ModelExtension):
    @property
    def display_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class CustomNote(Note, ModelExtension):
    # Without proxy_field, accessing note.patient returns a plain Patient.
    # With proxy_field, it returns a CustomPatient instead.
    patient = proxy_field(CustomPatient)


def test_proxy_field_returns_proxy_class():
    """proxy_field swaps __class__ so the returned object is CustomPatient."""
    note = NoteFactory.create()
    custom_note = CustomNote.objects.select_related("patient").get(dbid=note.dbid)

    # The patient is a CustomPatient, not a plain Patient
    assert type(custom_note.patient) is CustomPatient
    assert custom_note.patient.display_name == (
        f"{note.patient.first_name} {note.patient.last_name}"
    )


def test_proxy_field_handles_null():
    """proxy_field returns None when the FK is null."""
    note = NoteFactory.create(patient=None)
    custom_note = CustomNote.objects.get(dbid=note.dbid)
    assert custom_note.patient is None
```

## Testing Best Practices

1. **Use factories** for consistent test data generation
2. **Test isolation** - Each test should be independent and not rely on data from other tests
3. **Test both directions** of relationships (forward and reverse)
4. **Verify persistence** by reloading objects from the database
5. **Test edge cases** like None values, empty lists, and missing relationships
6. **Use descriptive test names** that explain what is being tested
7. **Test query optimization** to ensure prefetching works as expected
8. **Verify constraints** like uniqueness behavior
9. **Choose the right `on_delete`** - ForeignKeys to SDK models (Staff, Patient, etc.) must use `DO_NOTHING` and related records must be deleted manually. ForeignKeys between your own CustomModels can use `CASCADE` for automatic cleanup

## See Also

- [Custom Data Overview](/sdk/custom-data/) - Introduction to custom data storage
- [CustomModels](/sdk/custom-data-custom-models/) - Django models for structured data
- [AttributeHubs](/sdk/custom-data-attribute-hubs/) - Standalone key-value storage
- [Sharing Data](/sdk/custom-data-sharing-data/) - Sharing data among plugins
- [Caching API](/sdk/caching) - Auto-expiring transient data

<br/>
<br/>
<br/>
