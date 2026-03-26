---
title: "Extending SDK Models"
slug: "custom-data-extending-sdk-models"
---

## Overview

SDK models like `Patient`, `Staff`, and `Note` are shared across all plugins. To attach custom data
or create relationships to these models from your [CustomModels](/sdk/custom-data-custom-models/),
extend them with `ModelExtension` to create a plugin-private proxy model.

---

## Creating a Model Extension

Subclass the SDK model together with `ModelExtension`:

```python
from canvas_sdk.v1.data import Staff, ModelExtension


class CustomStaff(Staff, ModelExtension):
    pass
```

What happens automatically:
- **`proxy = True`** is set by the `ModelExtensionMetaClass`. No new database table is created —
  the proxy shares the parent model's table.
- **`app_label`** is set to your plugin name (derived from the module path).
- `CustomStaff` behaves identically to `Staff` for queries — `CustomStaff.objects.all()` returns
  the same rows as `Staff.objects.all()`.

You can name the class anything, but it **must** subclass both a concrete SDK model and
`ModelExtension`.

Extended SDK models may be defined anywhere in your plugin since they do not require database
modifications. However, placing them in the `models` directory alongside your CustomModels is
recommended for clarity.

---

## Why Proxy Models?

SDK models are shared across every plugin in the system. If two plugins each added a bare
`related_name="biography"` on a `ForeignKey` pointing at `Staff`, Django would raise a clash
error — both reverse relations would compete for the same attribute on the shared `Staff` class.

Proxy models solve this by giving each plugin its own private subclass of the SDK model. Because
`CustomStaff` is a distinct model (even though it shares the same table), reverse relations
registered on `CustomStaff` are scoped to the plugin that defined it. The shared SDK model stays
clean and unaffected.

---

## Referencing SDK Models from CustomModels

When a CustomModel needs a `ForeignKey` or `OneToOneField` pointing at an SDK model, you have
two approaches.

### Approach 1: Via Proxy (Recommended)

Create a `ModelExtension` proxy and point your relationship field at it. Because the target is
plugin-private, `related_name` can be any simple name — no namespacing required.

```python
from canvas_sdk.v1.data import Staff, ModelExtension
from canvas_sdk.v1.data.base import CustomModel
from django.db.models import DO_NOTHING, OneToOneField, TextField


class CustomStaff(Staff, ModelExtension):
    pass


class Biography(CustomModel):
    staff = OneToOneField(
        CustomStaff, to_field="dbid", on_delete=DO_NOTHING,
        related_name="biography"
    )
    text = TextField()
```

Reverse lookup works through the proxy:

```python?partial=true
staff = CustomStaff.objects.get(id="some-uuid")
bio = staff.biography  # accesses the Biography via related_name
```

### Approach 2: Direct SDK Model with Namespaced `related_name`

Point directly at the SDK model, but you **must** namespace the `related_name` to prevent
collisions across plugins. Two formats are accepted:

| Format | Example | Notes |
|--------|---------|-------|
| `%(app_label)s_` prefix (recommended) | `related_name="%(app_label)s_biography"` | Django substitutes your plugin's `app_label` at class creation time |
| Hardcoded plugin prefix | `related_name="my_plugin_biography"` | Works, but breaks if you rename the plugin |
| `"+"` | `related_name="+"` | Disables the reverse relation entirely |

```python
from canvas_sdk.v1.data import Staff
from canvas_sdk.v1.data.base import CustomModel
from django.db.models import DO_NOTHING, OneToOneField, TextField


class Biography(CustomModel):
    staff = OneToOneField(
        Staff, to_field="dbid", on_delete=DO_NOTHING,
        related_name="%(app_label)s_biography"
    )
    text = TextField()
```

### Comparison

| | Via Proxy | Direct SDK Model |
|---|---|---|
| `related_name` namespacing required? | No | Yes |
| Reverse lookup available? | Yes, via the proxy class | Yes, via the SDK model |
| Reverse attribute name | Simple (e.g., `staff.biography`) | Prefixed (e.g., `staff.my_plugin_biography`) |
| Extra class needed? | Yes (`ModelExtension` proxy) | No |

In most cases, Approach 1 is preferred — it keeps `related_name` values short and readable,
and the proxy class is reusable across multiple CustomModels in the same plugin.

---

## Proxying Related Objects with `proxy_field`

When you use `ModelExtension` proxies and follow related objects through ForeignKey fields, the
returned instance is the base SDK class — not your proxy. For example:

```python?partial=true
from canvas_sdk.v1.data import Note, Patient, ModelExtension

class CustomPatient(Patient, ModelExtension):
    def full_display_name(self):
        # custom method only available on CustomPatient
        return f"{self.first_name} {self.last_name} (DOB: {self.birth_date})"


class CustomNote(Note, ModelExtension):
    pass


note = CustomNote.objects.get(id=note_id)
note.patient                       # returns a Patient, not CustomPatient
note.patient.full_display_name()   # AttributeError!
```

This happens because Django's ForeignKey descriptor resolves the relation to the concrete model
(`Patient`), unaware of your proxy class. You would need an extra query to "re-fetch" the object
as a `CustomPatient`.

### The `proxy_field` descriptor

`proxy_field` solves this by intercepting the ForeignKey access and transparently returning the
proxy class instead:

```python
from canvas_sdk.v1.data import Note, Patient, ModelExtension, proxy_field


class CustomPatient(Patient, ModelExtension):
    def full_display_name(self):
        return f"{self.first_name} {self.last_name} (DOB: {self.birth_date})"


class CustomNote(Note, ModelExtension):
    patient = proxy_field(CustomPatient)


note = CustomNote.objects.get(id=note_id)
note.patient                       # returns a CustomPatient instance
note.patient.full_display_name()   # works!
```

No extra queries are issued — `proxy_field` reuses the already-fetched row and swaps its Python
class to the proxy. Because proxy models share the same database table, this is safe and
efficient.

### How it works

`proxy_field` is a Python [descriptor](https://docs.python.org/3/howto/descriptor.html). When
you declare `patient = proxy_field(CustomPatient)` on a model class:

1. `__set_name__` runs at class creation time and finds the original FK descriptor (`patient`)
   from the parent class in the MRO.
2. `__get__` delegates to that original descriptor to load the related object, then sets
   `__class__` on the result to your proxy class.
3. `__set__` passes assignment through to the original descriptor, so `note.patient = some_patient`
   continues to work normally.
4. Accessing the attribute on the class (e.g., `CustomNote.patient`) returns the descriptor
   itself, not a model instance.

### When to use `proxy_field`

Use `proxy_field` when:

- You have `ModelExtension` proxies for multiple SDK models and need to navigate between them
  while keeping access to your custom methods or `related_name` fields.
- You want to avoid extra database queries to "re-fetch" a related object as the proxy type.

`proxy_field` is not needed when:

- You don't add custom methods, properties or `related_name` fields to your proxy class.
- You access the related object's fields directly (e.g., `note.patient.first_name`) without
  needing proxy-specific behavior.

### Null foreign keys

`proxy_field` handles nullable ForeignKeys safely — if the relation is `None`, it returns `None`
without error:

```python?partial=true
note = CustomNote.objects.get(id=note_id)
note.patient  # returns None if the FK is null, not an error
```

---

## Common Errors

### `ValueError`: non-namespaced `related_name` on SDK model target

If you point a `ForeignKey` or `OneToOneField` directly at an SDK model with a plain
`related_name`, installation will fail with:

```text
ValueError: CustomModel 'Biography' declares related_name='biography' on field 'staff'
targeting SDK model 'Staff'. To prevent collisions across plugins, use a namespaced
related_name like related_name='%(app_label)s_biography', or related_name='+' to
disable the reverse relation.
```

**Fix:** Either switch to a proxy target (Approach 1) or add the `%(app_label)s_` prefix to
your `related_name` (Approach 2).

This validation applies to `ForeignKey` and `OneToOneField`. Fields targeting other CustomModels
or proxy models are exempt because those targets are already plugin-private.

---

## See Also

- [CustomModels](/sdk/custom-data-custom-models/) - Defining structured models, relationships, and queries
- [AttributeHubs](/sdk/custom-data-attribute-hubs/) - Standalone key-value storage
- [Design Considerations](/sdk/custom-data-design-considerations/) - Choosing the right technique and avoiding anti-patterns
- [Transactions](/sdk/custom-data-transactions/) - All-or-nothing writes with `transaction.atomic()`
- [Sharing Data](/sdk/custom-data-sharing-data/) - Sharing data with other plugins and external services
- [Data Models](/sdk/data/) - Core SDK data models

<br/>
<br/>
<br/>
