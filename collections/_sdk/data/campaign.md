---
title: "Campaign"
slug: "data-campaign"
excerpt: "Canvas SDK Campaign, Intervention, and InterventionPatient"
hidden: false
---

## Introduction

The `Campaign` model is an outreach campaign built on a protocol. Each `Intervention` is one outreach step in a campaign: a letter template sent to a set of patients from a start date. Use these models to report on outreach, or to find which campaigns a patient is part of.

A campaign is open until it's closed. When a campaign closes, `closed_at` is set, and `total_patients_on_closure` and `satisfied_patients_on_closure` record how many patients the campaign's first intervention targeted and how many of them had satisfied the protocol.

`Campaign.protocol_id` is the database identifier of the protocol the campaign is built on. It's an integer, not a related object, because the protocol record isn't in the data module.

## Basic usage

Campaigns and interventions have no `id` attribute. To get one by its database identifier, use the `get` method on the model manager:

```python
from canvas_sdk.v1.data import Campaign

campaign = Campaign.objects.get(dbid=1234)
```

The interventions in a campaign can be accessed with the `interventions` attribute on a `Campaign` object. Each intervention has its letter `template` and its `author`:

```python
from canvas_sdk.v1.data import Campaign

campaign = Campaign.objects.get(dbid=1234)

for intervention in campaign.interventions.order_by("start_delivery"):
    print(intervention.start_delivery, intervention.template.name, intervention.author.full_name)
```

The interventions that use a letter template can be accessed with the `interventions` attribute on a [LetterTemplate](/sdk/data-letter/#lettertemplate) object. The interventions a staff member authored can be accessed with the `interventions` attribute on a [Staff](/sdk/data-staff/) object:

```python
from canvas_sdk.v1.data import LetterTemplate, Staff

template = LetterTemplate.objects.get(id="b9a4bd6a-5f4b-4c55-9a39-3ad5aef3e3a6")
template_interventions = template.interventions.all()

staff = Staff.objects.get(id="4150cd20de8a470aa570a852859ac87e")
authored_interventions = staff.interventions.all()
```

## Patients in an intervention

The patients an intervention targets can be accessed with the `patients` attribute on an `Intervention` object. From the other side, the interventions that target a patient can be accessed with the `intervention_set` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data import Intervention, Patient

intervention = Intervention.objects.get(dbid=5678)
patients = intervention.patients.all()

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
patient_interventions = patient.intervention_set.all()
```

Each patient in an intervention is an `InterventionPatient` row. Query it directly when you need the pairs themselves, for example to count the patients in each intervention.

## Filtering

Filter on `closed_at` to find open campaigns, and filter interventions through `patients` to find the campaigns a patient is in:

```python
from canvas_sdk.v1.data import Campaign, Intervention

open_campaigns = Campaign.objects.filter(closed_at__isnull=True)

patient_campaigns = Campaign.objects.filter(
    interventions__patients__id="1eed3ea2a8d546a1b681a2a45de1d790"
).distinct()

upcoming_interventions = Intervention.objects.filter(
    campaign__closed_at__isnull=True,
    start_delivery__gte="2026-12-01",
)
```

## Attributes

### Campaign

| Field Name                    | Type                              | Description |
| ----------------------------- | --------------------------------- | ----------- |
| dbid                          | Integer                           | |
| title                         | String                            | |
| description                   | String                            | Up to 512 characters. Can be `None`. |
| closed_at                     | DateTime                          | When the campaign was closed. `None` while the campaign is open. |
| protocol_id                   | Integer                           | The database identifier of the protocol the campaign is built on. |
| work_list                     | Boolean                           | Whether the campaign is a work list. |
| total_patients_on_closure     | Integer                           | The number of patients the campaign's first intervention targeted when the campaign closed. `0` while the campaign is open. |
| satisfied_patients_on_closure | Integer                           | The number of those patients who had satisfied the protocol when the campaign closed. `0` while the campaign is open. |
| interventions                 | [Intervention](#intervention)[]   | |

### Intervention

| Field Name     | Type                                  | Description |
| -------------- | ------------------------------------- | ----------- |
| dbid           | Integer                               | |
| created        | DateTime                              | |
| modified       | DateTime                              | |
| campaign       | [Campaign](#campaign)                 | |
| template       | [LetterTemplate](/sdk/data-letter/#lettertemplate) | The letter template the intervention sends. |
| start_delivery | DateTime                              | When delivery of the intervention starts. |
| author         | [Staff](/sdk/data-staff/#staff)       | |
| patients       | [Patient](/sdk/data-patient/#patient)[] | The patients the intervention targets. |

### InterventionPatient

| Field Name   | Type                                  | Description |
| ------------ | ------------------------------------- | ----------- |
| dbid         | Integer                               | |
| intervention | [Intervention](#intervention)         | |
| patient      | [Patient](/sdk/data-patient/#patient) | |

<br/>
<br/>
<br/>
