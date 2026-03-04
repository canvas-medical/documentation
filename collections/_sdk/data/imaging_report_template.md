---
title: "Imaging Report Template"
slug: "data-imaging-report-template"
excerpt: "Canvas SDK Imaging Report Template"
hidden: false
---

## Introduction

The `ImagingReportTemplate`, `ImagingReportTemplateField`, and `ImagingReportTemplateFieldOption` models represent the templates used for imaging reports. Templates define the structure of an imaging report, including what fields need to be filled in and what options are available for each field.

## Basic Usage

To retrieve an `ImagingReportTemplate` by identifier, use the `get` method on the model manager:

```python
from canvas_sdk.v1.data.imaging import ImagingReportTemplate

template = ImagingReportTemplate.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")
```

To access the fields defined in a template:

```python
from canvas_sdk.v1.data.imaging import ImagingReportTemplate

template = ImagingReportTemplate.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")
fields = template.fields.all()
```

## Filtering

Templates can be filtered by any attribute on the models.

### By active status

```python
from canvas_sdk.v1.data.imaging import ImagingReportTemplate

active_templates = ImagingReportTemplate.objects.active()
```

### By type

```python
from canvas_sdk.v1.data.imaging import ImagingReportTemplate

# Get custom (user-created) templates
custom = ImagingReportTemplate.objects.custom()

# Get built-in (system) templates
builtin = ImagingReportTemplate.objects.builtin()
```

### By search

```python
from canvas_sdk.v1.data.imaging import ImagingReportTemplate

results = ImagingReportTemplate.objects.search("chest x-ray")
```

## Attributes

### ImagingReportTemplate

| Field Name      | Type                                                             |
|-----------------|------------------------------------------------------------------|
| id              | UUID                                                             |
| dbid            | Integer                                                          |
| name            | String                                                           |
| long_name       | String                                                           |
| code            | String                                                           |
| code_system     | String                                                           |
| search_keywords | String                                                           |
| active          | Boolean                                                          |
| custom          | Boolean                                                          |
| rank            | Integer                                                          |
| fields          | [ImagingReportTemplateField](#imagingreporttemplatefield)[]       |

### ImagingReportTemplateField

| Field Name      | Type                                                                           |
|-----------------|--------------------------------------------------------------------------------|
| dbid            | Integer                                                                        |
| report_template | [ImagingReportTemplate](#imagingreporttemplate)                                |
| sequence        | Integer                                                                        |
| code            | String                                                                         |
| code_system     | String                                                                         |
| label           | String                                                                         |
| units           | String                                                                         |
| type            | String                                                                         |
| required        | Boolean                                                                        |
| options         | [ImagingReportTemplateFieldOption](#imagingreporttemplatefieldoption)[]         |

### ImagingReportTemplateFieldOption

| Field Name | Type                                                              |
|------------|-------------------------------------------------------------------|
| dbid       | Integer                                                           |
| field      | [ImagingReportTemplateField](#imagingreporttemplatefield)         |
| label      | String                                                            |
| key        | String                                                            |

<br/>
<br/>
<br/>
