---
title: "Transactions"
slug: "custom-data-transactions"
---

## Overview

By default, each ORM operation in a plugin (`.save()`, `.create()`, `.update()`, `.delete()`)
is committed to the database immediately. There is no automatic transaction wrapping your handler
or protocol — if you perform three writes and the third one fails, the first two are already
committed.

When you need multiple operations to succeed or fail together, use `transaction.atomic()`.

---

## Using `transaction.atomic()`

Wrap related operations in an `atomic()` block to ensure all-or-nothing behavior:

```python
from django.db.transaction import atomic


with atomic():
    # All operations inside this block are part of a single transaction.
    # If any operation raises an exception, everything is rolled back.
    specialty, _ = Specialty.objects.get_or_create(name="Cardiology")
    StaffSpecialty.objects.filter(staff=staff).delete()
    StaffSpecialty.objects.bulk_create([
        StaffSpecialty(staff=staff, specialty=specialty)
    ])
    Biography.objects.create(staff=staff, biography="...")
```

If an exception occurs anywhere inside the block, all changes are rolled back — the database
is left as it was before the block started.

---

## When to Use Transactions

Use `transaction.atomic()` when your handler performs **multiple related writes** that should
not be partially applied:

- **Replacing associations** — deleting existing records and creating new ones (e.g., replacing
  a staff member's specialties). Without a transaction, a failure after the delete leaves the
  staff member with no specialties.
- **Creating a parent and its children** — e.g., creating a `Biography` and several `Language`
  records in one request. A partial failure could leave orphaned or incomplete data.
- **Coordinated updates** — updating multiple models that must stay consistent with each other.

You do **not** need a transaction for:
- A single `.create()`, `.save()`, or `.update()` call — these are already atomic on their own.
- Read-only operations — `SELECT` queries don't modify data.

---

## Example: Multi-Model Upsert

This example accepts a JSON payload and upserts a staff profile spanning multiple CustomModels.
The `atomic()` block ensures that either the entire profile is saved or nothing is:

```python
from django.db.transaction import atomic
from canvas_sdk.effects.simple_api import JSONResponse
from canvas_sdk.handlers.simple_api import SimpleAPI, api


class ProfileAPI(SimpleAPI):
    PREFIX = "/profile"

    @api.post("/v2/<staff_id>")
    def post_profile(self):
        with atomic():
            staff_id = self.request.path_params["staff_id"]
            json_body = self.request.json()
            staff = CustomStaff.objects.get(id=staff_id)

            # Upsert languages
            for name in json_body.get("languages", []):
                Language.objects.get_or_create(name=name, staff=staff)

            # Replace specialty associations
            specialties = []
            for name in json_body.get("specialties", []):
                specialty, _ = Specialty.objects.get_or_create(name=name)
                specialties.append(specialty)

            StaffSpecialty.objects.filter(staff=staff).delete()
            StaffSpecialty.objects.bulk_create([
                StaffSpecialty(staff=staff, specialty=s) for s in specialties
            ])

            # Upsert biography
            biography_text = json_body.get("biography")
            Biography.objects.update_or_create(
                staff=staff,
                defaults={
                    "biography": biography_text,
                    "practicing_since": json_body.get("practicing_since"),
                    "is_accepting_patients": json_body.get("accepting_patients"),
                },
            )

        return [JSONResponse({"status": "ok"})]
```

If any operation inside the `atomic()` block raises an exception — a constraint violation, an
unexpected data type, a model validation error — the entire block is rolled back and no partial
data is written.

---

## How It Works

Plugin code runs inside a database context that sets the PostgreSQL `search_path` to the
plugin's namespace. `transaction.atomic()` operates on this same connection automatically —
no `using=` parameter is needed.

Under the hood, `atomic()` issues a `SAVEPOINT` (for nested usage) or manages the transaction
directly. When the block exits cleanly, the transaction is committed. When an exception
propagates out, it is rolled back.

---

## Nesting

`atomic()` blocks can be nested. Inner blocks use PostgreSQL savepoints, so a failure in an
inner block rolls back only that block's changes (not the entire outer transaction), provided
you catch the exception:

```python
from django.db.transaction import atomic


with atomic():
    Specialty.objects.create(name="Cardiology")

    try:
        with atomic():
            Specialty.objects.create(name="Neurology")
            raise ValueError("something went wrong")
    except ValueError:
        pass  # Only the "Neurology" insert is rolled back

    # "Cardiology" is still pending and will be committed
```

If the exception is **not** caught, it propagates to the outer block and rolls back everything.

---

## See Also

- [CustomModels](/sdk/custom-data-custom-models/) - Defining structured models, relationships, and queries
- [AttributeHubs](/sdk/custom-data-attribute-hubs/) - Standalone key-value storage
- [Design Considerations](/sdk/custom-data-design-considerations/) - Choosing the right technique and avoiding anti-patterns
- [Testing Custom Data](/sdk/custom-data-testing/) - Testing utilities and examples

<br/>
<br/>
<br/>
