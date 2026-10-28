---
title: "BusinessLine"
slug: "data-business-line"
excerpt: "Canvas SDK BusinessLine"
hidden: false
---

## Introduction

The `BusinessLine` model represents a group of [Patients](/sdk/data-patient/#patient) that share a common brand under an [Organization](/sdk/data-organization).

## Usage

The `BusinessLine` model can be used to find all of the patients for a given Business Line:

```python
>>> from canvas_sdk.v1.data import BusinessLine
>>> business_line = BusinessLine.objects.get(id="ff844d60Od18466698dc645PtYZ3019Tt")
>>> business_line_patients = business_line.patients.all()
>>> print([patient.first_name for patient in business_line_patients])
['George', 'Louise', 'Julia']
```

You can also access a patient's Business Line from the `Patient` model:

```python
>>> from canvas_sdk.v1.data import Patient
>>> patient_1 = Patient.objects.get(id="aebe4d3f5d18410388dc69c4b5169fc3")
>>> patient_business_line = patient_1.business_line
>>> print(patient_business_line.name)
'New Patients that love cheese'
```

And you can also access all of the Business Lines under a given Organization:

```python
>>> from canvas_sdk.v1.data import Organization
>>> organization = Organization.objects.first()
>>> organization_business_lines = organization.business_lines.all()
>>> print([business_line.name for business_line in organization_business_lines])
['New Patients that love cheese', 'Spanish Speaking Patients', 'One Medical']
```

## Accessing the logo

The `logo_url` property returns a presigned S3 URL for the business line's logo image, or `None` when no logo is set. Use it to brand plugin output, such as a patient portal page or a generated document, with the logo configured in Canvas. The URL is valid for one hour, so generate it when you need it rather than storing it.

```python
from canvas_sdk.v1.data import Patient

patient = Patient.objects.get(id="aebe4d3f5d18410388dc69c4b5169fc3")

# Presigned S3 URL to the logo image, or None if no logo is set
logo_url = patient.business_line.logo_url if patient.business_line else None
```

## Filtering

The `filter` method can be used to filter by desired attributes. The following examples show commonly used operations to filter Business Line data:

**Show an Organization's Business Lines that are active and in the 732 area code**

```python
>>> from canvas_sdk.v1.data import BusinessLine, Organization
>>> org = Organization.objects.first()
>>> active_732_business_lines = BusinessLine.objects.filter(organization=org, active=True, area_code="732")
>>> print([business_line.name for business_line in active_732_business_lines])
['Foo', 'Bar']
```

## Attributes

### BusinessLine

| Field Name   | Type                                    |
| ------------ | --------------------------------------- |
| id           | UUID                                    |
| dbid         | Integer                                 |
| created      | DateTime                                |
| modified     | DateTime                                |
| name         | String                                  |
| description  | String                                  |
| area_code    | String                                  |
| subdomain    | String                                  |
| active       | Boolean                                 |
| state        | [BusinessLineState](#businesslinestate) |
| organization | [Organization](/sdk/data-organization)  |
| logo         | File (S3 key)                           |
| logo_url     | String (computed)                       |
| patients     | QuerySet[[Patient](/sdk/data-patient/#patient)] |

## Enumeration types

### BusinessLineState

| Value   | Label   |
| ------- | ------- |
| success | Success |
| pending | Pending |
| error   | Deleted |
