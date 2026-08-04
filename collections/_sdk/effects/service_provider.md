---
title: "ServiceProvider Effect"
slug: "effect-service-provider"
excerpt: "Effects for creating, updating, and deactivating providers in a customer-managed provider directory"
hidden: false
---

The `ServiceProvider` effect creates, updates, and soft-deactivates records in a customer-managed provider directory. The SDK previously exposed `ServiceProvider` only as a read-only data model.

## Overview

`ServiceProvider` exposes `.create()` to add a new provider, `.update()` to modify an existing one, and `.deactivate()` to soft-deactivate one. Each method returns an `Effect`.

## Attributes

All attributes are optional on the class itself; per-operation requirements are described in [Methods](#methods).

| Attribute            | Type   | Description                                             | Required |
|----------------------|--------|---------------------------------------------------------|----------|
| `id`                 | `str`  | Identifier of an existing provider to update or deactivate | Yes (update/deactivate) |
| `first_name`         | `str`  | The provider's first name                               | Yes (create) |
| `last_name`          | `str`  | The provider's last name                                | No       |
| `specialty`          | `str`  | The provider's specialty                                | Yes (create) |
| `business_address`   | `str`  | The provider's business address                         | Yes (create) |
| `business_phone`     | `str`  | The provider's business phone                           | No       |
| `business_fax`       | `str`  | The provider's business fax                             | No       |
| `practice_name`      | `str`  | The provider's practice name                            | No       |
| `notes`              | `str`  | Free-text notes about the provider                      | No       |
| `is_active`          | `bool` | Whether the provider is active                          | No       |
| `npi`                | `str`  | The provider's NPI                                      | No       |
| `direct_address`     | `str`  | Direct (secure messaging) address                       | No       |
| `science_contact_id` | `int`  | Used only as a hint to deduplicate against a shared-directory contact at create time; ignored on update | No       |

`science_contact_id` is only considered when creating a provider and is never written on update — for the field's read semantics, see the [ServiceProvider data model](/sdk/data-serviceprovider/).

## Methods

### create() → Effect

Create a new ServiceProvider.

#### Behavior

- Requires `first_name`, `specialty`, and `business_address`.
- Do not pass `id`.
- `last_name` is intentionally optional so organizations, which have no last name, can still be represented.

### update() → Effect

Update an existing ServiceProvider, sending only the fields that were set.

#### Behavior

- Requires an `id` referencing an existing record.
- `first_name` and `specialty` cannot be set to null on update.
- Only fields you explicitly set are sent, so update never clears fields you didn't set.
- Reactivate a deactivated provider by calling update with `is_active=True`.

### deactivate() → Effect

Soft-deactivate an existing ServiceProvider (sets `is_active=False`).

#### Behavior

- Requires an `id`.

## Validation

The effect validates before execution and raises a descriptive error when validation fails:

- **NPI**: `npi` must be exactly 10 numeric digits when provided, with no formatting characters such as dashes or spaces.
- **Direct address**: `direct_address` must be 512 characters or fewer when provided.
- **Existing record**: `update()` and `deactivate()` require an `id` that references an existing record.

## Examples

Create a new provider:

```python
from canvas_sdk.effects.service_provider import ServiceProvider

effect = ServiceProvider(first_name="Jane", last_name="Doe", specialty="Cardiology", business_address="123 Main St", npi="1234567890").create()
```

Update an existing provider, sending only the fields you set:

```python
from canvas_sdk.effects.service_provider import ServiceProvider

effect = ServiceProvider(id="existing-provider-uuid", notes="Prefers fax").update()
```

Reactivate a deactivated provider — reactivation is always explicit:

```python
from canvas_sdk.effects.service_provider import ServiceProvider

effect = ServiceProvider(id="existing-provider-uuid", is_active=True).update()
```

Soft-deactivate a provider:

```python
from canvas_sdk.effects.service_provider import ServiceProvider

effect = ServiceProvider(id="existing-provider-uuid").deactivate()
```

## Distinguishing ServiceProvider types

This write effect, `canvas_sdk.effects.service_provider.ServiceProvider`, creates, updates, and deactivates directory records. It is distinct from the read-only data model of the same name at `canvas_sdk.v1.data.service_provider.ServiceProvider`, which is the read-only query interface (see [ServiceProvider data model](/sdk/data-serviceprovider/)), and from the `canvas_sdk.commands.constants.ServiceProvider` value object used to set a provider on the Refer command (see [ServiceProvider](/sdk/commands/#serviceprovider)).

<br/>
<br/>
<br/>
