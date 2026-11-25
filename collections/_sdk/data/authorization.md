---
title: "Authorization"
slug: "data-authorization"
excerpt: "Canvas SDK Authorization and AuthorizationDiagnosisCode"
hidden: false
---

## Introduction

An `Authorization` is a payer's prior authorization for a patient. It records the authorization number, the [Coverage](/sdk/data-coverage/#coverage) it applies to, the dates it's valid for, and the visits it approves. Its `charges` are the [ChargeDescriptionMaster](/sdk/data-charge-description-master/) charges it covers, and its `codings` are the diagnosis codes it covers. A [Claim](/sdk/data-claim/#claim) billed under the authorization points to it through `authorization`.

## Basic usage

### Find a patient's authorizations

```python
from canvas_sdk.v1.data import Patient

patient = Patient.objects.get(id="b80b1cdc2e6a4aca90ccebc02e683f35")

authorizations = patient.authorizations.filter(deleted=False)
```

A coverage's authorizations are on `coverage.authorizations`.

### Read what an authorization covers

```python
from canvas_sdk.v1.data import Authorization

authorization = Authorization.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")

cpt_codes = list(authorization.charges.values_list("cpt_code", flat=True))
diagnosis_codes = list(authorization.codings.values_list("code", flat=True))
```

## Visits

When `unlimited_visits` is `True`, the authorization doesn't limit the number of visits, and `visits_approved` doesn't apply. Otherwise, Canvas counts each claim linked to the authorization as one visit used. To work out the visits left:

```python
from canvas_sdk.v1.data import Authorization

authorization = Authorization.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")

if authorization.unlimited_visits:
    visits_left = None
else:
    visits_left = max(authorization.visits_approved - authorization.claims.count(), 0)
```

## Filtering

### Authorizations that haven't expired

`expiration_date` is null when the authorization has no end date:

```python
import datetime

from django.db.models import Q

from canvas_sdk.v1.data import Authorization

today = datetime.date.today()

current = Authorization.objects.filter(
    patient__id="b80b1cdc2e6a4aca90ccebc02e683f35", deleted=False
).filter(Q(expiration_date__isnull=True) | Q(expiration_date__gt=today))
```

### By charge

```python
from canvas_sdk.v1.data import Authorization

authorizations = Authorization.objects.filter(charges__cpt_code="97110", deleted=False)
```

## Attributes

### Authorization

| Field Name                    | Type                                                                       | Notes |
|-------------------------------|----------------------------------------------------------------------------|-------|
| id                            | UUID                                                                       |       |
| dbid                          | Integer                                                                    |       |
| created                       | DateTime                                                                   |       |
| modified                      | DateTime                                                                   |       |
| originator                    | [CanvasUser](/sdk/data-canvasuser)                                         |       |
| committer                     | [CanvasUser](/sdk/data-canvasuser)                                         |       |
| entered_in_error              | [CanvasUser](/sdk/data-canvasuser)                                         |       |
| deleted                       | Boolean                                                                    |       |
| patient                       | [Patient](/sdk/data-patient/#patient)                                      |       |
| coverage                      | [Coverage](/sdk/data-coverage/#coverage)                                   | Null when no coverage was selected |
| authorization_number          | String                                                                     |       |
| start_date                    | Date                                                                       |       |
| expiration_date               | Date                                                                       | Null when the authorization has no end date |
| charges                       | QuerySet[[ChargeDescriptionMaster](/sdk/data-charge-description-master/)]  | The charges the authorization covers |
| codings                       | QuerySet[[AuthorizationDiagnosisCode](#authorizationdiagnosiscode)]        | The diagnosis codes the authorization covers |
| referring_provider_first_name | String                                                                     |       |
| referring_provider_last_name  | String                                                                     |       |
| referring_provider_npi        | String                                                                     |       |
| notes                         | String                                                                     |       |
| visits_approved               | Integer                                                                    | Doesn't apply when `unlimited_visits` is `True` |
| unlimited_visits              | Boolean                                                                    |       |
| claims                        | QuerySet[[Claim](/sdk/data-claim/#claim)]                                  | Claims billed under the authorization. Each one counts as a visit used. |

### AuthorizationDiagnosisCode

| Field Name    | Type                            |
|---------------|---------------------------------|
| dbid          | Integer                         |
| authorization | [Authorization](#authorization) |
| code          | String                          |
| display       | String                          |
