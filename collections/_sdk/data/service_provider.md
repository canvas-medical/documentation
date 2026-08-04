---
title: "ServiceProvider"
slug: "data-serviceprovider"
excerpt: "Data model for a ServiceProvider in Canvas SDK"
hidden: false
---

## Introduction

This module defines the read-only data model used to query service providers in the Canvas SDK. Two other same-named symbols serve different purposes: the write effect `canvas_sdk.effects.service_provider.ServiceProvider` creates, updates, or deactivates providers (see the [ServiceProvider effect](/sdk/effect-service-provider/)), and the Refer command's provider value object lives in `canvas_sdk.commands.constants`.

## Basic usage

To retrieve a `ServiceProvider` by identifier, use the `get` method on the model manager:

```python
from canvas_sdk.v1.data.service_provider import ServiceProvider

service_provider = ServiceProvider.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")
```

To retrieve a service provider from an `ImagingOrder` or a `Referral`

```python
from canvas_sdk.v1.data.imaging import ImagingOrder
from canvas_sdk.v1.data.referral import Referral

imaging_order = ImagingOrder.objects.get(id="9d2e0f58-338b-11ec-8d3d-0242ac130003")
imaging_order_service_provider = imaging_order.imaging_center

referral = Referral.objects.get(id="9d2e0f58-338b-11ec-8d3d-0242ac130004")
referral_service_provider = referral.service_provider
```

To show a `ServiceProvider` full name or full name with specialty use the properties `full_name` or `full_name_and_specialty`

```python
from canvas_sdk.v1.data.service_provider import ServiceProvider

service_provider = ServiceProvider.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")
full_name = service_provider.full_name
full_name_and_specialty = service_provider.full_name_and_specialty

```

## Filtering

Customer-managed providers — those created through the SDK — can be found by filtering on `is_customer_managed`, which distinguishes them from Science-derived providers.

```python
from canvas_sdk.v1.data.service_provider import ServiceProvider

customer_managed_providers = ServiceProvider.objects.filter(is_customer_managed=True)
```

This is the recommended way to look up an existing customer-managed provider (for example, to get its `id`) before updating or deactivating it via the [ServiceProvider effect](/sdk/effect-service-provider/).

## Service Provider

### Fields

| Name                 | Type    | Description |
| -------------------- | ------- | ----------- |
| `id`                 | UUID    | Unique identifier (UUID). |
| `dbid`               | Integer | Internal database identifier. |
| `first_name`         | String  | The provider's first name. |
| `last_name`          | String  | The provider's last name. |
| `business_fax`       | String  | The provider's business fax number. |
| `business_phone`     | String  | The provider's business phone number. |
| `business_address`   | String  | The provider's business address. |
| `specialty`          | String  | The provider's specialty. |
| `practice_name`      | String  | The provider's practice name. |
| `notes`              | String  | Free-text notes about the provider. |
| `is_active`          | Boolean | Whether the provider is active. |
| `npi`                | String  | The provider's NPI. |
| `direct_address`     | String  | Direct (secure messaging) address. |
| `is_customer_managed` | Boolean | True only for providers a customer created through the SDK. Filter on it to search a customer's own directory; everything else, including Science-derived providers, is False. |
| `science_contact_id`  | Integer | The shared directory contact this provider came from, null when it came from none. Read-only, and not a provenance signal: legacy providers predate this tracking, so use `is_customer_managed` to tell a customer's own providers apart. |
| `imaging_orders`     | QuerySet[[ImagingOrder](/sdk/data-imaging/#imagingorder)] | Imaging orders sent to this provider. |
| `referrals`          | QuerySet[[Referral](/sdk/data-referral/#referral)] | Referrals sent to this provider. |
| `integration_tasks`  | QuerySet[[IntegrationTask](/sdk/data-integration-task/#integrationtask)] | Integration tasks associated with this provider. |

### Methods

To shape a `ServiceProvider` as a search result or a contact record, use `as_search_result` or `as_search_contact`.

`as_search_result(annotations=None)` shapes this provider as an autocomplete result for a command's search. It returns a dict with the following keys:

- Top level: `text`, `value`, `description`, `annotations`
- `extra.contact`: `service_provider_id`, `science_contact_id`, `firstName`, `lastName`, `businessFax`, `businessPhone`, `businessAddress`, `specialty`, `practiceName`, `notes`

The key casing shown matches the serialized search payload exactly.

`as_search_contact(annotations=None)` shapes this provider as a contact record for a contact directory search. It returns a dict with the following keys:

- `id`, `serviceProviderId`, `firstName`, `lastName`, `practiceName`, `specialty`, `businessAddress`, `businessPhone`, `businessFax`, `annotations`

These serialized shapes are intended to be returned from a search handler that customizes autocomplete results; see [Customize search results](/guides/customize-search-results/).

```python
from canvas_sdk.v1.data.service_provider import ServiceProvider

service_provider = ServiceProvider.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")
search_result = service_provider.as_search_result()
search_contact = service_provider.as_search_contact()
```
