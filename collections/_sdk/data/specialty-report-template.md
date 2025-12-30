---
title: "Specialty Report Template"
slug: "data-specialty-report-template"
excerpt: "Canvas SDK Specialty Report Template"
hidden: false
---

## Introduction

The `SpecialtyReportTemplate`, `SpecialtyReportTemplateField`, and `SpecialtyReportTemplateFieldOption` models represent templates used for LLM-powered specialty/referral report parsing. These templates define the structure for parsing specialty consultation reports, referral responses, and other clinical documents organized by medical specialty.

## Basic Usage

To retrieve a `SpecialtyReportTemplate` by identifier, use the `get` method on the model manager:

```python
from canvas_sdk.v1.data.specialty_report_template import (
    SpecialtyReportTemplate,
    SpecialtyReportTemplateField,
    SpecialtyReportTemplateFieldOption,
)

template = SpecialtyReportTemplate.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")
```

## Filtering

Specialty report templates can be filtered by any attribute that exists on the model.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.specialty_report_template import SpecialtyReportTemplate

templates = SpecialtyReportTemplate.objects.filter(active=True)
templates = SpecialtyReportTemplate.objects.filter(custom=False)
```

### Active templates

Return only active templates:

```python
from canvas_sdk.v1.data.specialty_report_template import SpecialtyReportTemplate

templates = SpecialtyReportTemplate.objects.active()
```

### By specialty

Filter templates by specialty taxonomy code:

```python
from canvas_sdk.v1.data.specialty_report_template import SpecialtyReportTemplate

cardiology = SpecialtyReportTemplate.objects.by_specialty("207RC0000X")
```

### Custom and built-in templates

```python
from canvas_sdk.v1.data.specialty_report_template import SpecialtyReportTemplate

custom_templates = SpecialtyReportTemplate.objects.custom()
builtin_templates = SpecialtyReportTemplate.objects.builtin()
```

### Search

Perform full-text search using the search_keywords field:

```python
from canvas_sdk.v1.data.specialty_report_template import SpecialtyReportTemplate

templates = SpecialtyReportTemplate.objects.search("cardiology")
```

### Chaining methods

QuerySet methods can be chained:

```python
from canvas_sdk.v1.data.specialty_report_template import SpecialtyReportTemplate

templates = SpecialtyReportTemplate.objects.active().by_specialty("207RC0000X")
templates = SpecialtyReportTemplate.objects.active().custom()
```

## Accessing Related Fields

To retrieve a template with its fields and options, use `prefetch_related`:

```python
from canvas_sdk.v1.data.specialty_report_template import SpecialtyReportTemplate

template = SpecialtyReportTemplate.objects.prefetch_related(
    'fields',
    'fields__options'
).get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")

for field in template.fields.all():
    print(f"Field: {field.label}")
    for option in field.options.all():
        print(f"  Option: {option.label}")
```

## Attributes

### SpecialtyReportTemplate

| Field Name            | Type    |
|-----------------------|---------|
| id                    | UUID    |
| dbid                  | Integer |
| name                  | String  |
| code                  | String  |
| code_system           | String  |
| search_keywords       | String  |
| active                | Boolean |
| custom                | Boolean |
| search_as             | String  |
| specialty_name        | String  |
| specialty_code        | String  |
| specialty_code_system | String  |

### SpecialtyReportTemplateField

| Field Name      | Type                                                |
|-----------------|-----------------------------------------------------|
| dbid            | Integer                                             |
| report_template | [SpecialtyReportTemplate](#specialtyreporttemplate) |
| sequence        | Integer                                             |
| code            | String                                              |
| code_system     | String                                              |
| label           | String                                              |
| units           | String                                              |
| type            | String                                              |
| required        | Boolean                                             |

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
