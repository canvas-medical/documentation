---
title: "SpecialtyReportTemplate"
slug: "data-specialty-report-template"
excerpt: "Canvas SDK SpecialtyReportTemplate"
hidden: false
---

## Introduction

The `SpecialtyReportTemplate`, `SpecialtyReportTemplateField`, and `SpecialtyReportTemplateFieldOption` models represent templates for capturing structured data from specialty and referral consultation reports.

## Basic Usage

To retrieve a `SpecialtyReportTemplate` by identifier:

```python
from canvas_sdk.v1.data.specialty_report_template import SpecialtyReportTemplate

template = SpecialtyReportTemplate.objects.get(id="a1b2c3d4-e5f6-7890-abcd-ef1234567890")

print(f"Template: {template.name}")
print(f"Specialty: {template.specialty_name} ({template.specialty_code})")
print(f"Active: {template.active}")
```

To access a template's fields and field options:

```python
from canvas_sdk.v1.data.specialty_report_template import SpecialtyReportTemplate

template = SpecialtyReportTemplate.objects.get(id="a1b2c3d4-e5f6-7890-abcd-ef1234567890")

for field in template.fields.all().order_by('sequence'):
    print(f"Field: {field.label}, Type: {field.type}, Required: {field.required}")

    for option in field.options.all():
        print(f"  Option: {option.label} ({option.key})")
```

## Filtering

Specialty report templates can be filtered by any attribute that exists on the model. The model also provides convenient filter methods for common use cases.

```python
from canvas_sdk.v1.data.specialty_report_template import SpecialtyReportTemplate

active_templates = SpecialtyReportTemplate.objects.active()
matching_templates = SpecialtyReportTemplate.objects.search("cardiology")
custom_templates = SpecialtyReportTemplate.objects.custom()
builtin_templates = SpecialtyReportTemplate.objects.builtin()
cardiology_templates = SpecialtyReportTemplate.objects.by_specialty("207RC0000X")
results = SpecialtyReportTemplate.objects.active().custom().by_specialty("207RC0000X")
```

## Attributes

### SpecialtyReportTemplate

| Field Name           | Type                                                              |
|----------------------|-------------------------------------------------------------------|
| id                   | UUID                                                              |
| dbid                 | Integer                                                           |
| name                 | String                                                            |
| code                 | String                                                            |
| code_system          | String                                                            |
| search_keywords      | String                                                            |
| active               | Boolean                                                           |
| custom               | Boolean                                                           |
| search_as            | String                                                            |
| specialty_name       | String                                                            |
| specialty_code       | String                                                            |
| specialty_code_system| String                                                            |
| fields               | [SpecialtyReportTemplateField](#specialtyreporttemplatefield)[]   |

### SpecialtyReportTemplateField

| Field Name      | Type                                                                          |
|-----------------|-------------------------------------------------------------------------------|
| dbid            | Integer                                                                       |
| report_template | [SpecialtyReportTemplate](#specialtyreporttemplate)                           |
| sequence        | Integer                                                                       |
| code            | String                                                                        |
| code_system     | String                                                                        |
| label           | String                                                                        |
| units           | String                                                                        |
| type            | String                                                                        |
| required        | Boolean                                                                       |
| options         | [SpecialtyReportTemplateFieldOption](#specialtyreporttemplatefieldoption)[]   |

### SpecialtyReportTemplateFieldOption

| Field Name | Type                                                          |
|------------|---------------------------------------------------------------|
| dbid       | Integer                                                       |
| field      | [SpecialtyReportTemplateField](#specialtyreporttemplatefield) |
| label      | String                                                        |
| key        | String                                                        |

<br/>
<br/>
<br/>
