---
title: "Service Provider Effects"
slug: "effect-service-provider"
excerpt: "Effects for managing a customer's own directory of external providers"
hidden: false
---

The Service Provider effects let a plugin build and maintain its own directory of external
providers. Providers created this way are readable through the SDK and can be offered in the
provider-search surfaces.

## Create Service Provider

Creates a service provider, or updates a matching one.

### Attributes

| Attribute          | Type            | Description                                     | Required |
|--------------------|-----------------|-------------------------------------------------|----------|
| `first_name`       | `str`           | Provider name, or the organization name         | Yes      |
| `specialty`        | `str`           | Free text                                       | Yes      |
| `business_address` | `str`           | Business address                                | Yes      |
| `last_name`        | `str` or `None` | Omit for organizations                          | No       |
| `practice_name`    | `str` or `None` | Practice or organization name                   | No       |
| `business_phone`   | `str` or `None` | Business phone number                           | No       |
| `business_fax`     | `str` or `None` | Business fax number                             | No       |
| `npi`              | `str` or `None` | Exactly 10 digits                               | No       |
| `direct_address`   | `str` or `None` | Up to 512 characters                            | No       |
| `notes`            | `str` or `None` | Free-text notes                                 | No       |
| `is_active`        | `bool`          | Defaults to `True`                              | No       |

The required fields reject empty strings.

### Calling create more than once

A create matches an existing provider on first name, last name, specialty and business address. On
a match it updates that provider instead of adding another, and:

- only the fields you sent are written; the rest keep their values
- a deactivated provider stays deactivated unless you send `is_active=True`

So it is safe to run the same create on a schedule.

### Example Usage

```python
from canvas_sdk.effects.service_provider import ServiceProvider
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler


class ProviderLoader(BaseHandler):
    RESPONDS_TO = [EventType.Name(EventType.PLUGIN_CREATED)]

    def compute(self):
        return [
            ServiceProvider(
                first_name="Jane",
                last_name="Doe",
                specialty="Cardiology",
                business_address="123 Main St",
                business_fax="5555550100",
                npi="1234567890",
                direct_address="jane.doe@direct.example.org",
            ).create(),
            # An organization has no last name.
            ServiceProvider(
                first_name="Acme Imaging Center",
                specialty="Radiology",
                business_address="1 Hospital Way",
            ).create(),
        ]
```

## Update Service Provider

Updates the provider with the given `id`. Only the fields you set are sent, so an update never
clears a field you did not mention. `first_name` and `specialty` cannot be set to `None`.

```python?partial=true
ServiceProvider(id="d2194110-5c9a-4842-8733-ef09ea5ead11", notes="Prefers fax").update()
```

### Reactivating a provider

Set `is_active=True` explicitly. Nothing else reactivates a provider.

```python?partial=true
ServiceProvider(id="d2194110-5c9a-4842-8733-ef09ea5ead11", is_active=True).update()
```

## Deactivate Service Provider

Deactivates a provider without deleting it, so anything referencing it keeps working.

```python?partial=true
ServiceProvider(id="d2194110-5c9a-4842-8733-ef09ea5ead11").deactivate()
```

## Effects

| Effect                      | Description                    |
|-----------------------------|--------------------------------|
| CREATE_SERVICE_PROVIDER     | Create a service provider.     |
| UPDATE_SERVICE_PROVIDER     | Update a service provider.     |
| DEACTIVATE_SERVICE_PROVIDER | Deactivate a service provider. |

## Reading providers back

Use the [ServiceProvider data module](/sdk/data-serviceprovider/), and `is_customer_managed` to read
only the providers your plugin created:

```python
from canvas_sdk.v1.data.service_provider import ServiceProvider

ServiceProvider.objects.filter(is_customer_managed=True, is_active=True)
```

To offer them in a provider search, see
[`as_search_result` and `as_search_contact`](/sdk/data-serviceprovider/#search-results).
