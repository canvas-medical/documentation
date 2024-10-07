---
title: "Questionnaire"
slug: "data-questionnaire"
excerpt: "Canvas SDK Questionnaire"
hidden: false
---

# Introduction

The `Questionnaire` model represents a structured set of questions intended to guide the collection of answers from end-users.

# Basic usage

To get a questionnaire by identifier, use the `get` method on the `Questionnaire` model manager:

```python
from canvas_sdk.v1.data.questionnaire import Questionnaire

questionnaire = Questionnaire.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

# Questions

The questions for a questionnaire can be accessed with the `questions` attribute on an `Questionnaire` object:

```python
from canvas_sdk.v1.data.questionnaire import Questionnaire
from logger import log

questionnaire = Questionnaire.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

for question in questionnaire.questions:
    log.info(f"system: {question.code_system}")
    log.info(f"system: {question.code}")
    log.info(f"system: {question.name}")
```

# Filtering

Questionnaires can be filtered by any attribute that exists on the model.

Filtering for questionnaires is done with the `filter` method on the `Questionnaire` model manager.

## By attribute

Specify an attribute calling `filter` to filter by that attribute.

```python
from canvas_sdk.v1.data.questionnaire import Questionnaire

questionnaire = Questionnaire.objects.filter(name="Tobacco")
```

## By ValueSet

Filtering by ValueSet works a little differently. The `find` method on the model manager is used to perform `ValueSet` filtering.

```python
from canvas_sdk.v1.data.questionnaire import Questionnaire
from canvas_sdk.value_set.v2022.assessment import TobaccoUseScreening

questionnaires = Questionnaire.objects.find(TobaccoUseScreening)
```
