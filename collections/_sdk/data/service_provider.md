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

| Name             | Type    |
| ---------------- | ------- |
| id               | UUID    |
| dbid             | Integer |
| first_name       | String  |
| last_name        | String  |
| business_fax     | String  |
| business_phone   | String  |
| business_address | String  |
| specialty        | String  |
| practice_name    | String  |
| notes            | String  |
