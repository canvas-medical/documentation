---
title: "Lab Report Template"
slug: "data-lab-report-template"
excerpt: "Canvas SDK Lab Report Template"
hidden: false
---

## Introduction

The `LabReportTemplate`, `LabReportTemplateField`, and `LabReportTemplateFieldOption` models represent the templates used for point-of-care (POC) labs and custom lab reports. Templates define the structure of a lab report, including what fields need to be filled in and what options are available for each field.

## Basic Usage

To retrieve a `LabReportTemplate` by identifier, use the `get` method on the model manager:

```python
from canvas_sdk.v1.data.lab import LabReportTemplate

template = LabReportTemplate.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")
```

To access the fields defined in a template:

```python
from canvas_sdk.v1.data.lab import LabReportTemplate

template = LabReportTemplate.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")
fields = template.fields.all()
```

## Filtering

Templates can be filtered by any attribute on the models.

### By active status

```python
from canvas_sdk.v1.data.lab import LabReportTemplate

# Get all active templates
active_templates = LabReportTemplate.objects.active()

# Get inactive templates
inactive_templates = LabReportTemplate.objects.inactive()
```

### By type

```python
from canvas_sdk.v1.data.lab import LabReportTemplate

# Get custom (user-created) templates
custom = LabReportTemplate.objects.custom()

# Get built-in (system) templates
builtin = LabReportTemplate.objects.builtin()

# Get point-of-care test templates
poc = LabReportTemplate.objects.point_of_care()
```

### By search

```python
from canvas_sdk.v1.data.lab import LabReportTemplate

results = LabReportTemplate.objects.search("glucose")
```

## Attributes

### LabReportTemplate

| Field Name      | Type                                                   |
|-----------------|--------------------------------------------------------|
| id              | UUID                                                   |
| dbid            | Integer                                                |
| name            | String                                                 |
| code            | String                                                 |
| code_system     | String                                                 |
| search_keywords | String                                                 |
| active          | Boolean                                                |
| custom          | Boolean                                                |
| poc             | Boolean                                                |
| fields          | [LabReportTemplateField](#labreporttemplatefield)[]     |

### LabReportTemplateField

| Field Name      | Type                                                                 |
|-----------------|----------------------------------------------------------------------|
| dbid            | Integer                                                              |
| report_template | [LabReportTemplate](#labreporttemplate)                              |
| sequence        | Integer                                                              |
| code            | String                                                               |
| code_system     | String                                                               |
| label           | String                                                               |
| units           | String                                                               |
| type            | [FieldType](#fieldtype)                                              |
| required        | Boolean                                                              |
| options         | [LabReportTemplateFieldOption](#labreporttemplatefieldoption)[]       |

### LabReportTemplateFieldOption

| Field Name | Type                                                    |
|------------|---------------------------------------------------------|
| dbid       | Integer                                                 |
| field      | [LabReportTemplateField](#labreporttemplatefield)       |
| label      | String                                                  |
| key        | String                                                  |

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
