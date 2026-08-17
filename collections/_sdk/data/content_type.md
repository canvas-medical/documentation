---
title: "ContentType"
slug: "data-content-type"
excerpt: "Canvas SDK ContentType"
hidden: false
---

## Introduction

The `ContentType` model provides read-only access to Django content types. Use it to resolve the content type id for a given model, which is required when working with generic relations (such as [document references](/sdk/data-document-reference)) and when generating permalinks.

A content type is identified by two **stable** values — `app_label` and `model` — that are the same on every Canvas instance. Its `dbid` (the content type id) is a per-database auto-increment that **is not stable across environments**. Always resolve the `dbid` at runtime from the `app_label` and `model`; never hardcode a content type id, or it will point at the wrong model in another environment.

## Basic usage

To get a content type by its database id, use the `get` method on the `ContentType` model manager:

```python
from canvas_sdk.v1.data import ContentType

content_type = ContentType.objects.get(dbid=42)
```

## Resolving a content type at runtime

Because the `dbid` differs per environment, look the content type up by its stable `app_label` and `model`, then read `dbid` from the result:

```python
from canvas_sdk.v1.data import ContentType

content_type = ContentType.objects.filter(app_label="api", model="note").first()
if content_type:
    # Resolved for this environment — safe to use for a generic relation or permalink.
    content_type_id = content_type.dbid
```

## Filtering

Content types can be filtered by any attribute that exists on the model.

Filtering for content types is done with the `filter` method on the `ContentType` model manager.

### By model

To find the content type for a specific model, filter by `app_label` and `model`:

```python
from canvas_sdk.v1.data import ContentType

content_type = ContentType.objects.filter(app_label="api", model="note").first()
if content_type:
    print(f"Content type id: {content_type.dbid}")
```

## app_label and model for data module models

Use these stable values to resolve a content type with `ContentType.objects.filter(app_label=..., model=...)`. The `model` value is the lowercased Django model name, and most data module models live under the `api` app. This list is not exhaustive — any model not shown here can be resolved the same way once you know its `app_label` and `model`.

### `api` app

| SDK data model        | app_label | model                         |
|-----------------------|-----------|-------------------------------|
| [AllergyIntolerance](/sdk/data-allergy-intolerance/) | `api` | `allergyintolerance` |
| [Appointment](/sdk/data-appointment/) | `api` | `appointment` |
| [Assessment](/sdk/data-assessment/) | `api` | `assessment` |
| [BannerAlert](/sdk/data-banner-alert/) | `api` | `banneralert` |
| [ChartSectionReview](/sdk/data-chart-section-review/) | `api` | `chartsectionreview` |
| [Condition](/sdk/data-condition/) | `api` | `condition` |
| [Coverage](/sdk/data-coverage/) | `api` | `coverage` |
| [DetectedIssue](/sdk/data-detected-issue/) | `api` | `detectedissue` |
| [Device](/sdk/data-device/) | `api` | `device` |
| [DiagnosticReport](/sdk/data-labs/#diagnosticreport) | `api` | `diagnosticreport` |
| [DocumentReference](/sdk/data-document-reference/) | `api` | `documentreference` |
| [Encounter](/sdk/data-encounter/) | `api` | `encounter` |
| [Facility](/sdk/data-facility/) | `api` | `facility` |
| [Goal](/sdk/data-goal/) | `api` | `goal` |
| [ImagingOrder](/sdk/data-imaging/) | `api` | `imagingorder` |
| [ImagingReport](/sdk/data-imaging/) | `api` | `imagingreport` |
| [ImagingReview](/sdk/data-imaging/) | `api` | `imagingreview` |
| [Immunization](/sdk/data-immunization/) | `api` | `immunization` |
| [Instruction](/sdk/data-instruction/) | `api` | `instruction` |
| [Interview](/sdk/data-questionnaire/) | `api` | `interview` |
| [LabOrder](/sdk/data-labs/) | `api` | `laborder` |
| [LabReport](/sdk/data-labs/) | `api` | `labreport` |
| [LabValue](/sdk/data-labs/) | `api` | `labvalue` |
| [Letter](/sdk/data-letter/) | `api` | `letter` |
| [Medication](/sdk/data-medication/) | `api` | `medication` |
| [MedicationStatement](/sdk/data-medication-statement/) | `api` | `medicationstatement` |
| [Message](/sdk/data-message/) | `api` | `message` |
| [Note](/sdk/data-note/) | `api` | `note` |
| [Observation](/sdk/data-observation/) | `api` | `observation` |
| [Organization](/sdk/data-organization/) | `api` | `organization` |
| [OrganizationalEntity](/sdk/data-organizational-entity/) | `api` | `organizationalentity` |
| [Patient](/sdk/data-patient/) | `api` | `patient` |
| [PatientConsent](/sdk/data-patient-consent/) | `api` | `patientconsent` |
| [PatientGroup](/sdk/data-patient-group/) | `api` | `patientgroup` |
| [PracticeLocation](/sdk/data-practicelocation/) | `api` | `practicelocation` |
| [Prescription](/sdk/data-prescription/) | `api` | `prescription` |
| [Questionnaire](/sdk/data-questionnaire/) | `api` | `questionnaire` |
| [ReasonForVisit](/sdk/data-reason-for-visit/) | `api` | `reasonforvisit` |
| [Referral](/sdk/data-referral/) | `api` | `referral` |
| [Staff](/sdk/data-staff/) | `api` | `staff` |
| [StopMedicationEvent](/sdk/data-stop-medication-event/) | `api` | `stopmedicationevent` |
| [Task](/sdk/data-task/) | `api` | `task` |
| [Team](/sdk/data-team/) | `api` | `team` |
| [UncategorizedClinicalDocument](/sdk/data-uncategorized-clinical-document/) | `api` | `uncategorizedclinicaldocument` |
| [VisualExamFinding](/sdk/data-visual-exam-finding/) | `api` | `visualexamfinding` |

### Other apps

Some models live in a different Django app, so their `app_label` is not `api`:

| SDK data model         | app_label             | model                    |
|------------------------|-----------------------|--------------------------|
| [Command](/sdk/data-command/) | `commands` | `command` |
| [Application](/sdk/data-application/) | `plugin_io` | `application` |
| [PluginCommand](/sdk/data-plugin-command/) | `plugin_io` | `plugincommand` |
| [Calendar](/sdk/data-calendar/) | `calendars` | `calendar` |
| [ExternalEvent](/sdk/data-external-event/) | `data_integration` | `externalevent` |
| [ServiceProvider](/sdk/data-serviceprovider/) | `data_integration` | `serviceprovider` |
| [ChargeDescriptionMaster](/sdk/data-charge-description-master/) | `quality_and_revenue` | `chargedescriptionmaster` |
| [Claim](/sdk/data-claim/) | `quality_and_revenue` | `claim` |
| [PayorSpecificCharge](/sdk/data-payor-specific-charge/) | `quality_and_revenue` | `payorspecificcharge` |

## Attributes

### ContentType

| Field Name | Type    |
|------------|---------|
| dbid       | Integer |
| app_label  | String  |
| model      | String  |

- **dbid**: The internal database primary key, which is the content type id used for generic relations and permalinks. This value is environment-specific — resolve it at runtime rather than hardcoding it.
- **app_label**: The label of the application the model belongs to (e.g., `api`).
- **model**: The lowercased name of the model (e.g., `note`).

<br/>
<br/>
<br/>
