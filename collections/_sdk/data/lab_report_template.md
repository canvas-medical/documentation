---
title: "LabReportTemplate"
slug: "data-lab-report-template"
excerpt: "Canvas SDK LabReportTemplate"
hidden: false
---

## Introduction

The `LabReportTemplate`, `LabReportTemplateField`, and `LabReportTemplateFieldOption` models represent templates for Point of Care (POC) labs and custom lab reports.

## Basic Usage

To retrieve a `LabReportTemplate` by identifier:

```python
from canvas_sdk.v1.data.lab_report_template import LabReportTemplate

template = LabReportTemplate.objects.get(id="a1b2c3d4-e5f6-7890-abcd-ef1234567890")
```

To access a template's fields and field options:

```python
from canvas_sdk.v1.data.lab_report_template import LabReportTemplate

template = LabReportTemplate.objects.get(id="a1b2c3d4-e5f6-7890-abcd-ef1234567890")

for field in template.fields.all().order_by('sequence'):
    print(f"Field: {field.label}, Type: {field.field_type}, Required: {field.required}")

    for option in field.options.all():
        print(f"  Option: {option.label} ({option.key})")
```

## Filtering

Lab report templates can be filtered by any attribute that exists on the model. The model also provides convenient filter methods for common use cases.

```python
from canvas_sdk.v1.data.lab_report_template import LabReportTemplate

active_templates = LabReportTemplate.objects.active()
inactive_templates = LabReportTemplate.objects.inactive()
matching_templates = LabReportTemplate.objects.search("glucose")
poc_templates = LabReportTemplate.objects.point_of_care()
custom_templates = LabReportTemplate.objects.custom()
builtin_templates = LabReportTemplate.objects.builtin()
results = LabReportTemplate.objects.active().point_of_care().search("a1c")
```

## Attributes

### LabReportTemplate

| Field Name      | Type                                                  |
|-----------------|-------------------------------------------------------|
| id              | UUID                                                  |
| dbid            | Integer                                               |
| name            | String                                                |
| code            | String                                                |
| code_system     | String                                                |
| search_keywords | String                                                |
| active          | Boolean                                               |
| custom          | Boolean                                               |
| poc             | Boolean                                               |
| fields          | [LabReportTemplateField](#labreporttemplatefield)[]   |

### LabReportTemplateField

| Field Name      | Type                                                              |
|-----------------|-------------------------------------------------------------------|
| id              | UUID                                                              |
| dbid            | Integer                                                           |
| report_template | [LabReportTemplate](#labreporttemplate)                           |
| sequence        | Integer                                                           |
| code            | String                                                            |
| code_system     | String                                                            |
| label           | String                                                            |
| units           | String                                                            |
| field_type      | [FieldType](#fieldtype)                                           |
| required        | Boolean                                                           |
| options         | [LabReportTemplateFieldOption](#labreporttemplatefieldoption)[]   |

### LabReportTemplateFieldOption

| Field Name | Type                                                  |
|------------|-------------------------------------------------------|
| id         | UUID                                                  |
| dbid       | Integer                                               |
| field      | [LabReportTemplateField](#labreporttemplatefield)     |
| label      | String                                                |
| key        | String                                                |

## Enumeration types

### FieldType

| Value        | Label         |
|--------------|---------------|
| float        | Float         |
| select       | Select        |
| text         | Text          |
| checkbox     | Checkbox      |
| radio        | Radio         |
| array        | Array         |
| labReport    | Lab Report    |
| remoteFields | Remote Fields |
| autocomplete | Autocomplete  |
| date         | Date          |

<br/>
<br/>
<br/>
