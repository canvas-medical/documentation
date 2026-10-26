---
title: "LetterTemplate"
slug: "data-letter-template"
excerpt: "Canvas SDK LetterTemplate"
hidden: false
---

## Introduction

The `LetterTemplate` model represents a reusable template for [letters](/sdk/data-letter/), messages, and interventions. Read it to find the templates an instance has configured and where each one can be used.

## Basic usage

**List the active templates that can be used for letters**

```python
from canvas_sdk.v1.data import LetterTemplate
from canvas_sdk.v1.data.letter_template import LetterTemplateType

letter_templates = LetterTemplate.objects.filter(
    active=True, template_type__contains=[LetterTemplateType.LETTER]
)
print([template.name for template in letter_templates])
```

## Attributes

### LetterTemplate

| Field Name       | Type                                              |
| ---------------- | ------------------------------------------------- |
| dbid             | Integer                                           |
| created          | DateTime                                          |
| modified         | DateTime                                          |
| name             | String                                            |
| active           | Boolean                                           |
| restrict_editing | Boolean                                           |
| template_type    | List[[LetterTemplateType](#lettertemplatetype)]   |
| locations        | List[String]                                      |

## Enumeration types

### LetterTemplateType

| Value        | Label        |
| ------------ | ------------ |
| intervention | Intervention |
| letter       | Letter       |
| message      | Message      |
