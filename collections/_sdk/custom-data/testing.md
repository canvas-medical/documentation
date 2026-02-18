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

---

## Creating Factories for Proxy Models

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

## Testing CustomAttributes

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

## Testing AttributeHub

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

## Testing Custom Models

Test custom model creation, relationships, and queries:

```python
import factory
from datetime import datetime
from django.db.models import (
    ForeignKey, OneToOneField, TextField, IntegerField, DateTimeField,
    Index, DO_NOTHING
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

## Testing with Factories

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

## Testing Queries and Prefetching

Test that prefetching and query optimization work correctly:

```python
import factory
from django.db.models import (
    ForeignKey, OneToOneField, TextField, IntegerField,
    Index, DO_NOTHING, Count
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

## Testing Data Integrity

Test data validation, constraints, and cascade behavior:

```python
import factory
from django.db.models import ForeignKey, TextField, Index, DO_NOTHING
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

    staff = factory.SubFactory(StaffProxyFactory)
    specialty = factory.SubFactory(SpecialtyFactory)


def test_manual_cleanup_on_delete():
    """Test manual cleanup since DO_NOTHING doesn't cascade."""
    staff = StaffProxyFactory.create()
    specialty = SpecialtyFactory.create()
    ss = StaffSpecialtyFactory.create(staff=staff, specialty=specialty)

    # With DO_NOTHING, you must clean up related records manually
    specialty_id = specialty.dbid
    StaffSpecialty.objects.filter(specialty_id=specialty_id).delete()
    specialty.delete()

    # Verify both are gone
    assert not StaffSpecialty.objects.filter(specialty_id=specialty_id).exists()
    assert not Specialty.objects.filter(dbid=specialty_id).exists()


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

## Testing Best Practices

1. **Use factories** for consistent test data generation
2. **Test isolation** - Each test should be independent and not rely on data from other tests
3. **Test both directions** of relationships (forward and reverse)
4. **Verify persistence** by reloading objects from the database
5. **Test edge cases** like None values, empty lists, and missing relationships
6. **Use descriptive test names** that explain what is being tested
7. **Test query optimization** to ensure prefetching works as expected
8. **Verify constraints** like uniqueness behavior
9. **Clean up manually** - Custom models use `DO_NOTHING` for foreign keys, so related records must be deleted manually before deleting the parent

---

## See Also

- [Custom Data Overview](/sdk/custom-data/) - Introduction to custom data storage
- [CustomAttributes](/sdk/custom-data-custom-attributes/) - Flexible key-value storage
- [AttributeHubs](/sdk/custom-data-attribute-hubs/) - Standalone key-value storage
- [Custom Models](/sdk/custom-data-custom-models/) - Django models for structured data
- [Sharing Data](/sdk/custom-data-sharing-data/) - Sharing data among plugins
- [Caching API](/sdk/caching) - Auto-expiring transient data
