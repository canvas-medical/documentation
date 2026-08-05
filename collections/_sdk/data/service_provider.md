---
title: "ServiceProvider"
slug: "data-serviceprovider"
excerpt: "Data model for a ServiceProvider in Canvas SDK"
hidden: false
---

## Introduction

This module defines the data models used to manage Service Provider in the Canvas SDK.

## Basic usage

To retrieve an `ServiceProvider` by identifier, use the `get` method on the model manager:

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

## Service Provider

### Fields

| Name                 | Type    | Description                                                                 |
| -------------------- | ------- | --------------------------------------------------------------------------- |
| id                   | UUID    |                                                                             |
| dbid                 | Integer |                                                                             |
| first_name           | String  | Provider name, or the organization name                                     |
| last_name            | String  | Empty for organizations                                                     |
| business_fax         | String  |                                                                             |
| business_phone       | String  |                                                                             |
| business_address     | String  |                                                                             |
| specialty            | String  | Free text                                                                   |
| practice_name        | String  |                                                                             |
| notes                | String  |                                                                             |
| is_active            | Boolean | `False` once deactivated; the provider is kept, not deleted                  |
| npi                  | String  | 10 digits                                                                   |
| direct_address       | String  | Direct address                                                              |
| is_customer_managed  | Boolean | `True` for providers created through the SDK — see below                     |
| imaging_orders    | QuerySet[[ImagingOrder](/sdk/data-imaging/#imagingorder)] |
| referrals         | QuerySet[[Referral](/sdk/data-referral/#referral)] |
| integration_tasks | QuerySet[[IntegrationTask](/sdk/data-integration-task/#integrationtask)] |

## Customer-managed providers

`is_customer_managed` is `True` for providers created with the
[Service Provider effects](/sdk/effect-service-provider/), and `False` for everything else. 

```python
from canvas_sdk.v1.data.service_provider import ServiceProvider

ServiceProvider.objects.filter(is_customer_managed=True, is_active=True)
```

## Search results

Two helpers shape a provider for the provider-search surfaces, so you do not have to build the
payloads yourself. Both take an optional list of annotations, shown next to the result.

| Method | Use it for |
| --- | --- |
| `as_search_result(annotations=None)` | A command's provider search — `Refer to` on Refer, `Imaging center` on Imaging Order |
| `as_search_contact(annotations=None)` | The fax recipient and external care team dropdowns |

Both identify the provider, so selecting one attaches to that exact record.

```python
import json

from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.v1.data.service_provider import ServiceProvider


class OwnDirectoryFirst(BaseHandler):
    RESPONDS_TO = [EventType.Name(EventType.FAX__RECIPIENT__PRE_SEARCH), EventType.Name(EventType.PATIENT_PROFILE__EXTERNAL_CARE_TEAM__PRE_SEARCH)]

    def compute(self):
        term = self.event.context.get("search_term", "").strip()
        if not term:
            return []

        providers = ServiceProvider.objects.filter(
            is_customer_managed=True, first_name__icontains=term
        )
        if not providers:
            return []

        return [
            Effect(
                type=EffectType.AUTOCOMPLETE_SEARCH_RESULTS,
                payload=json.dumps(
                    [
                        provider.as_search_contact(
                            [] if provider.is_active else ["Inactive"]
                        )
                        for provider in providers
                    ]
                ),
            )
        ]
```

Both surfaces reply with the same `AUTOCOMPLETE_SEARCH_RESULTS` effect. Only the event you subscribe
to and the helper you call differ.

What you return means different things on each surface:

- **Contact dropdowns, pre-search** — results replace the search; returning nothing runs the normal
  search instead.
- **Command searches, post-search** — an empty list clears the results, so return no effect at all
  when you have nothing to add.
