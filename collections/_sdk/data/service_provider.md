---
title: "ServiceProvider"
slug: "data-serviceprovider"
excerpt: "Data model for a ServiceProvider in Canvas SDK"
hidden: false
---

## Introduction

A `ServiceProvider` is an external provider or organization — someone outside your practice that a
patient's care touches. The same record backs every surface in Canvas where an outside provider gets
picked:

- The contact selected as the recipient of a [Refer](/sdk/commands/#refer) command.
- The imaging center selected on an [Imaging Order](/sdk/commands/#imagingorder) command.
- An external care team member added to a patient's profile.
- The recipient of an outbound fax, and the matched sender of an inbound one — Data Integration
  looks up the sending fax number in the contact directory and links the resulting provider to the
  incoming document, which is what the `integration_tasks` relation below exposes.

Service providers come from two places. Most are drawn from the shared external contact directory,
which is what those surfaces search by default and which you can query yourself with
[`GET /contacts/`](/sdk/utils/#searching-for-contacts-and-service-providers). You can also build your
own directory: providers created through the
[ServiceProvider effect](/sdk/effect-service-provider/) belong to your instance and are flagged with
`is_customer_managed`.

Your own providers are not searched automatically. To offer them in one of the surfaces above, handle
that surface's search event and return them yourself — see the helpers under
[Search results](#search-results) below, and
[Offering your own providers alongside the directory](/guides/customize-search-results/#offering-your-own-providers-alongside-the-directory)
for a worked handler covering all four surfaces.

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

## Service Provider

### Fields

| Name                 | Type    | Description                                                                 |
| -------------------- | ------- | --------------------------------------------------------------------------- |
| id                   | UUID    | Unique identifier                                                           |
| dbid                 | Integer | Internal database identifier                                                |
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
| science_contact_id   | Integer | The shared directory contact this provider came from, or `None` if it came from none. Not a reliable provenance signal on its own — providers that predate this tracking have no value — so use `is_customer_managed` to identify a customer's own providers. |
| imaging_orders       | QuerySet[[ImagingOrder](/sdk/data-imaging/#imagingorder)] | Imaging orders sent to this provider |
| referrals            | QuerySet[[Referral](/sdk/data-referral/#referral)] | Referrals sent to this provider |
| integration_tasks    | QuerySet[[IntegrationTask](/sdk/data-integration-task/#integrationtask)] | Integration tasks associated with this provider |

## Customer-managed providers

`is_customer_managed` is `True` for providers created with the
[Service Provider effects](/sdk/effect-service-provider/), and `False` for everything else. 

```python
from canvas_sdk.v1.data.service_provider import ServiceProvider

ServiceProvider.objects.filter(is_customer_managed=True, is_active=True)
```

This is also how you find an existing customer-managed provider — to get its `id` — before updating
or deactivating it with the [Service Provider effects](/sdk/effect-service-provider/).

## Search results

Two helpers shape a provider for the provider-search surfaces, so you do not have to build the
payloads yourself. Both take an optional list of annotations, shown next to the result.

| Method | Use it for |
| --- | --- |
| `as_search_result(annotations=None)` | A command's provider search — `Refer to` on Refer, `Imaging center` on Imaging Order |
| `as_search_contact(annotations=None)` | The fax recipient and external care team dropdowns |

Both identify the provider, so selecting one attaches to that exact record.

The two helpers return different shapes, and the key casing below matches the serialized payload
exactly:

- `as_search_result(annotations=None)` returns `text`, `value`, `description`, and `annotations` at
  the top level, plus an `extra.contact` object containing `service_provider_id`,
  `science_contact_id`, `firstName`, `lastName`, `businessFax`, `businessPhone`, `businessAddress`,
  `specialty`, `practiceName`, and `notes`.
- `as_search_contact(annotations=None)` returns a flat object: `id`, `serviceProviderId`,
  `firstName`, `lastName`, `practiceName`, `specialty`, `businessAddress`, `businessPhone`,
  `businessFax`, and `annotations`.

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
