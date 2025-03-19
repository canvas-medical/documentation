---
title: "Banner Alert"
slug: "data-banner-alert"
excerpt: "Canvas SDK Banner Alert"
hidden: false
---

## Introduction

The `BannerAlert` model represents alerts associated with [Patient](/sdk/data-patient/#patient) records. This page deals with data retrieval. To create or remove `BannerAlert` records, see [Banner Alert Effects](/sdk/effect-banner-alerts/).

## Usage

The `BannerAlert` model can be used to find all of the banner alert records linked to a patient. For example, to find all of the banner alerts for a patient, the `Patiient.banner_alerts` method can be used:

```python
>>> from canvas_sdk.v1.data.patient import Patient
>>> patient_1 = Patient.objects.get(id="aebe4d3f5d18410388dc69c4b5169fc3")
>>> patient_banner_alerts = patient_1.banner_alerts.all()
>>> print([item.narrative for item in patient_banner_alerts])
['Patient spits when angry', 'Confirm contact info']
```

## Filtering

The `filter` method can be used to filter by desired attributes. The following examples show commonly used operations to filter banner alert data:

**Show a Patient's active BannerAlert records from the 'foo' plugin in order of descending creation date**

```python
>>> from canvas_sdk.v1.data.patient import Patient
>>> patient_1 = Patient.objects.get(id="aebe4d3f5d18410388dc69c4b5169fc3")
>>> banner_alerts = patient_1.banner_alerts.filter(status='active', plugin_name='foo').order_by("created")
>>> print([item.narrative for item in banner_alerts])
['foo', 'bar']
```

## Attributes

### BannerAlert

| Field Name   | Type                                             |
| ------------ | ------------------------------------------------ |
| dbid         | Integer                                          |
| created      | DateTime                                         |
| modified     | DateTime                                         |
| patient      | [Patient](/sdk/data-patient/#patient)            |
| plugin_name  | String                                           |
| key          | String                                           |
| narrative    | String                                           |
| placement    | [BannerAlertPlacement](#banneralertplacement)[]  |
| intent       | [BannerAlertIntent](#banneralertintent)          |
| href         | String                                           |
| status       | [BannerAlertStatus](#banneralertstatus)          |

## Enumeration types

### BannerAlertStatus

| Value    | Label    |
| -------  | -------  |
| active   | Active   |
| inactive | Inactive |

### BannerAlertIntent

| Value    | Label    |
| -------  | -------  |
| info     | Info     |
| warning  | Warning  |
| alert    | Alert    |

### BannerAlertPlacement

| Value            | Label            |
| -------          | -------          |
| chart            | Chart            |
| timeline         | Timeline         |
| appointment_card | Appointment Card |
| scheduling_card  | Scheduling Card  |
| profile          | Profile          |
