---
title: "LabPartner, LabPartnerTest & AOE Questions"
slug: "data-lab-partner-and-test"
excerpt: "Canvas SDK LabPartner, LabPartnerTest, LabPartnerTestQuestion, and LabPartnerTestQuestionChoice models"
hidden: false
---

## Introduction

The **LabPartner**, **LabPartnerTest**, **LabPartnerTestQuestion**, and **LabPartnerTestQuestionChoice** models represent external lab partners, the tests they offer, and the ask-at-order-entry (AOE) questions associated with each test within Canvas.

---

## LabPartner

The `LabPartner` model stores information about a lab partner

### Basic Usage

To retrieve a lab partner by its unique identifier:

```python
from canvas_sdk.v1.data.lab import LabPartner

lab_partner = LabPartner.objects.get(id="your-uuid-here")
```

You can also filter lab partners by attributes. For example, to list all active lab partners:

```python
from canvas_sdk.v1.data.lab import LabPartner

active_lab_partners = LabPartner.objects.filter(active=True)
```

## LabPartnerTest

The `LabPartnerTest` model represents a test offered by a lab partner. Each test is linked to a lab partner via a
foreign key.

### Basic Usage

To retrieve tests for a given lab partner, you can access the related tests using the reverse relationship:

```python
from canvas_sdk.v1.data.lab import LabPartner

lab_partner = LabPartner.objects.get(id="your-uuid-here")
tests = lab_partner.available_tests.all()
```

Alternatively, you can directly filter tests by attributes:

```python
from canvas_sdk.v1.data.lab import LabPartnerTest

tests_with_code = LabPartnerTest.objects.filter(order_code="XYZ123")
```

## Attributes

### LabPartner

| Field Name                  | Type    | Description                                                         |
| --------------------------- | ------- | ------------------------------------------------------------------- |
| id                          | UUID    | The universally unique identifier for the lab partner.              |
| dbid                        | Integer | The internal database identifier (primary key) for the lab partner. |
| name                        | String  | The name of the lab partner.                                        |
| active                      | Boolean | Indicates whether the lab partner is currently active.              |
| electronic_ordering_enabled | Boolean | Indicates if electronic ordering is enabled for this lab partner.   |
| keywords                    | Text    | Keywords associated with the lab partner.                           |
| default_lab_account_number  | String  | The default lab account number used for orders.                     |

### LabPartnerTest Attributes

| Field Name  | Type                                                | Description                                                                                  |
| ----------- | --------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| id          | UUID                                                | The universally unique identifier for the test record.                                       |
| dbid        | Integer                                             | The internal database identifier (primary key) for the test record.                          |
| lab_partner | [LabPartner](#labpartner)                           | A reference to the related `LabPartner` (accessible via the related name `available_tests`). |
| order_code  | String                                              | A code used to identify the test order. May be blank.                                        |
| order_name  | Text                                                | The name of the test order.                                                                  |
| keywords    | Text                                                | Keywords associated with the test. May be blank.                                             |
| cpt_code    | String                                              | The CPT code for the test, if available. Can be blank or null.                               |
| questions   | [LabPartnerTestQuestion](#labpartnertestquestion)[] | AOE questions associated with this test.                                                     |

---

## LabPartnerTestQuestion

The `LabPartnerTestQuestion` model represents an ask-at-order-entry (AOE) question associated with a lab partner test. AOE questions are prompts that must be answered when ordering a specific lab test (e.g., "Is the patient fasting?", "Source of specimen").

### Basic Usage

To retrieve questions for a given lab partner test:

```python
from canvas_sdk.v1.data.lab import LabPartnerTest

test = LabPartnerTest.objects.get(id="your-uuid-here")
questions = test.questions.all()
```

To filter for required questions only:

```python?partial=true
required_questions = test.questions.filter(required=True)
```

To directly query questions by code:

```python
from canvas_sdk.v1.data.lab import LabPartnerTestQuestion

questions = LabPartnerTestQuestion.objects.filter(code="FAST")
```

---

## LabPartnerTestQuestionChoice

The `LabPartnerTestQuestionChoice` model represents a selectable answer option for an AOE question. Not all questions have predefined choices (e.g., free-text questions may have none).

### Basic Usage

To retrieve choices for a given question:

```python?partial=true
question = test.questions.first()
choices = question.choices.all()
```

### Example: Building AOE prompts for a lab test

```python
from canvas_sdk.v1.data.lab import LabPartnerTest
from logger import log

test = LabPartnerTest.objects.get(id="your-uuid-here")

for question in test.questions.all():
    log.info(f"Question: {question.body} (required={question.required})")
    for choice in question.choices.all():
        log.info(f"  - {choice.label}: {choice.value}")
```

## Attributes

### LabPartnerTestQuestion Attributes

| Field Name       | Type                                                            | Description                                                                                         |
| ---------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| dbid             | Integer                                                         | The internal database identifier (primary key) for the question.                                    |
| lab_partner_test | [LabPartnerTest](#labpartnertest)                               | A reference to the related `LabPartnerTest` (accessible via the related name `questions`).          |
| required         | Boolean                                                         | Whether this question must be answered when ordering the test.                                      |
| code             | String                                                          | A code identifying the question (e.g., "FAST" for fasting status).                                 |
| body             | Text                                                            | The full text of the question displayed to the user.                                                |
| type             | String                                                          | The question type (e.g., "text", "select", "date", "numeric").                                     |
| created          | DateTime                                                        | When the record was created.                                                                        |
| modified         | DateTime                                                        | When the record was last modified.                                                                  |
| choices          | [LabPartnerTestQuestionChoice](#labpartnertestquestionchoice)[] | Selectable answer options for this question.                                                        |

### LabPartnerTestQuestionChoice Attributes

| Field Name                 | Type                                              | Description                                                                                        |
| -------------------------- | ------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| dbid                       | Integer                                           | The internal database identifier (primary key) for the choice.                                     |
| lab_partner_test_question  | [LabPartnerTestQuestion](#labpartnertestquestion) | A reference to the related `LabPartnerTestQuestion` (accessible via the related name `choices`).   |
| label                      | String     | The display label for this choice (shown to the user).                                             |
| value                      | String     | The value submitted when this choice is selected.                                                  |
| created                    | DateTime   | When the record was created.                                                                       |
| modified                   | DateTime   | When the record was last modified.                                                                 |

<br/>
<br/>
<br/>
