---
title: "Specialty Report Template"
slug: "data-specialty-report-template"
excerpt: "Canvas SDK Specialty Report Template"
hidden: false
---

## Introduction

The `SpecialtyReportTemplate`, `SpecialtyReportTemplateField`, and `SpecialtyReportTemplateFieldOption` models represent the templates used for specialty and referral reports. Templates define the structure of a specialty report, including what fields need to be filled in and what options are available for each field. Each template can be associated with a medical specialty via taxonomy codes.

## Basic Usage

To retrieve a `SpecialtyReportTemplate` by identifier, use the `get` method on the model manager:

```python
from canvas_sdk.v1.data.specialty_report_template import SpecialtyReportTemplate

template = SpecialtyReportTemplate.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")
```

To access the fields defined in a template:

```python
from canvas_sdk.v1.data.specialty_report_template import SpecialtyReportTemplate

template = SpecialtyReportTemplate.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")
fields = template.fields.all()
```

## Filtering

Templates can be filtered by any attribute on the models.

### By active status

```python
from canvas_sdk.v1.data.specialty_report_template import SpecialtyReportTemplate

active_templates = SpecialtyReportTemplate.objects.active()
```

### By type

```python
from canvas_sdk.v1.data.specialty_report_template import SpecialtyReportTemplate

# Get custom (user-created) templates
custom = SpecialtyReportTemplate.objects.custom()

# Get built-in (system) templates
builtin = SpecialtyReportTemplate.objects.builtin()
```

### By specialty

```python
from canvas_sdk.v1.data.specialty_report_template import SpecialtyReportTemplate

# Filter by specialty taxonomy code
cardiology = SpecialtyReportTemplate.objects.by_specialty("207RC0000X")
```

### By search

```python
from canvas_sdk.v1.data.specialty_report_template import SpecialtyReportTemplate

results = SpecialtyReportTemplate.objects.search("cardiology")
```

## Attributes

### SpecialtyReportTemplate

| Field Name            | Type                                                                     |
|-----------------------|--------------------------------------------------------------------------|
| id                    | UUID                                                                     |
| dbid                  | Integer                                                                  |
| name                  | String                                                                   |
| code                  | String                                                                   |
| code_system           | String                                                                   |
| search_keywords       | String                                                                   |
| active                | Boolean                                                                  |
| custom                | Boolean                                                                  |
| search_as             | String                                                                   |
| specialty_name        | String                                                                   |
| specialty_code        | String                                                                   |
| specialty_code_system | String                                                                   |
| fields                | [SpecialtyReportTemplateField](#specialtyreporttemplatefield)[]           |

### SpecialtyReportTemplateField

| Field Name      | Type                                                                                 |
|-----------------|--------------------------------------------------------------------------------------|
| dbid            | Integer                                                                              |
| report_template | [SpecialtyReportTemplate](#specialtyreporttemplate)                                  |
| sequence        | Integer                                                                              |
| code            | String                                                                               |
| code_system     | String                                                                               |
| label           | String                                                                               |
| units           | String                                                                               |
| type            | String                                                                               |
| required        | Boolean                                                                              |
| options         | [SpecialtyReportTemplateFieldOption](#specialtyreporttemplatefieldoption)[]           |

### SpecialtyReportTemplateFieldOption

| Field Name | Type                                                                    |
|------------|-------------------------------------------------------------------------|
| dbid       | Integer                                                                 |
| field      | [SpecialtyReportTemplateField](#specialtyreporttemplatefield)           |
| label      | String                                                                  |
| key        | String                                                                  |

<br/>
<br/>
<br/>
