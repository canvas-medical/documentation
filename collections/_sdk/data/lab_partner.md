---
title: "LabPartner, LabPartnerTest & AOE Questions"
slug: "data-lab-partner-and-test"
excerpt: "Canvas SDK LabPartner, LabPartnerTest, LabPartnerTestQuestion, LabPartnerTestQuestionChoice, and lab account number models"
hidden: false
---

## Introduction

The **LabPartner**, **LabPartnerTest**, **LabPartnerTestQuestion**, and **LabPartnerTestQuestionChoice** models represent external lab partners, the tests they offer, and the ask-at-order-entry (AOE) questions associated with each test within Canvas. The [lab account number](#lab-account-numbers) models hold the Health Gorilla account numbers configured for each practice location and staff member.

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
| created                     | DateTime | When the record was created.                                        |
| modified                    | DateTime | When the record was last modified.                                  |
| name                        | String  | The name of the lab partner.                                        |
| active                      | Boolean | Indicates whether the lab partner is currently active.              |
| electronic_ordering_enabled | Boolean | Indicates if electronic ordering is enabled for this lab partner.   |
| keywords                    | Text    | Keywords associated with the lab partner.                           |
| default_lab_account_number  | String  | The default lab account number used for orders.                     |
| available_tests             | [LabPartnerTest](#labpartnertest)[] | The tests offered by this lab partner (reverse relation, accessible via `available_tests`). |
| location_account_numbers    | [PracticeLocationLabAccountNumber](#practicelocationlabaccountnumber)[] | The practice location account numbers configured for this lab partner. |

### LabPartnerTest Attributes

| Field Name  | Type                                                | Description                                                                                  |
| ----------- | --------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| id          | UUID                                                | The universally unique identifier for the test record.                                       |
| dbid        | Integer                                             | The internal database identifier (primary key) for the test record.                          |
| created     | DateTime                                            | When the record was created.                                                                 |
| modified    | DateTime                                            | When the record was last modified.                                                           |
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

---

## Lab account numbers

Each practice location can have its own account number with a lab partner, and staff at that location can have their own account numbers under it. When Canvas sends an electronic lab order to Health Gorilla, it fills in two account numbers from these records:

- **Organization account number:** the account number for the lab partner and the note's practice location. If the location has none, Canvas uses the lab partner's `default_lab_account_number`.
- **Practitioner account number:** a staff account number under that location account that applies to all staff at the location or to the ordering provider. If none applies, Canvas uses the organization account number.

A plugin can read these records to choose the account numbers it returns in a [`HealthGorillaLabOrderOverride`](/sdk/effect-health-gorilla-lab-order-override/) effect, which takes precedence over these defaults.

Three models hold these account numbers:

- `PracticeLocationLabAccountNumber`: a practice location's account number with a lab partner. A location has at most one per lab partner.
- `StaffLabAccountNumber`: a staff account number under a practice location's account. It applies to every staff member at the location when `use_for_all_staff_at_location` is `True`, and otherwise to the staff members linked to it.
- `StaffLabAccountNumberStaff`: the link between a `StaffLabAccountNumber` and each staff member it's assigned to.

### Basic usage

To list a practice location's account numbers, with the lab partner each one is for:

```python
from canvas_sdk.v1.data.practicelocation import PracticeLocation
from logger import log

practice_location = PracticeLocation.objects.get(id="your-uuid-here")

for location_account in practice_location.lab_account_numbers.select_related("lab_partner"):
    log.info(f"{location_account.lab_partner.name}: {location_account.account_number}")
```

To find the account number a practice location uses with a lab partner, and the staff account numbers under it:

```python
from canvas_sdk.v1.data.lab import PracticeLocationLabAccountNumber
from logger import log

location_account = PracticeLocationLabAccountNumber.objects.filter(
    lab_partner__name="Quest Diagnostics",
    practice_location__id="your-uuid-here",
).first()

if location_account:
    for staff_account in location_account.staff_account_numbers.all():
        if staff_account.use_for_all_staff_at_location:
            log.info(f"{staff_account.account_number}: all staff at the location")
        else:
            names = [staff.full_name for staff in staff_account.staff.all()]
            log.info(f"{staff_account.account_number}: {', '.join(names)}")
```

`staff.lab_account_numbers` returns only the staff account numbers linked to that staff member. A staff account number with `use_for_all_staff_at_location` set to `True` also applies to staff members it isn't linked to. To find every staff account number that applies to a staff member at a practice location:

```python
from django.db.models import Q

from canvas_sdk.v1.data.lab import StaffLabAccountNumber
from canvas_sdk.v1.data.staff import Staff

staff = Staff.objects.get(id="your-staff-key-here")

staff_accounts = StaffLabAccountNumber.objects.filter(
    Q(use_for_all_staff_at_location=True) | Q(staff=staff),
    practice_location_lab_account__practice_location__id="your-uuid-here",
).distinct()
```

### PracticeLocationLabAccountNumber

| Field Name            | Type                                                    | Description                                                                         |
| --------------------- | ------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| id                    | UUID                                                    | The universally unique identifier for the account number record.                    |
| dbid                  | Integer                                                 | The internal database identifier (primary key) for the account number record.      |
| lab_partner           | [LabPartner](#labpartner)                               | The lab partner the account is with (related name `location_account_numbers`).     |
| practice_location     | [PracticeLocation](/sdk/data-practicelocation/#practicelocation) | The practice location the account number belongs to (related name `lab_account_numbers`). |
| account_number        | String                                                  | The practice location's account number with the lab partner.                        |
| staff_account_numbers | [StaffLabAccountNumber](#stafflabaccountnumber)[]       | The staff account numbers under this account.                                       |

### StaffLabAccountNumber

| Field Name                    | Type                                                                    | Description                                                                                       |
| ----------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| id                            | UUID                                                                    | The universally unique identifier for the staff account number record.                            |
| dbid                          | Integer                                                                 | The internal database identifier (primary key) for the staff account number record.              |
| practice_location_lab_account | [PracticeLocationLabAccountNumber](#practicelocationlabaccountnumber)   | The practice location account this staff account number belongs to (related name `staff_account_numbers`). |
| account_number                | String                                                                  | The staff account number.                                                                         |
| use_for_all_staff_at_location | Boolean                                                                 | `True` when the account number applies to every staff member at the practice location.            |
| staff                         | [Staff](/sdk/data-staff/#staff)[]                                       | The staff members linked to this account number (related name `lab_account_numbers`).            |

### StaffLabAccountNumberStaff

| Field Name               | Type                                            | Description                                                          |
| ------------------------ | ----------------------------------------------- | -------------------------------------------------------------------- |
| dbid                     | Integer                                         | The internal database identifier (primary key) for the link record. |
| staff_lab_account_number | [StaffLabAccountNumber](#stafflabaccountnumber) | The staff account number.                                            |
| staff                    | [Staff](/sdk/data-staff/#staff)                 | The staff member the account number is linked to.                    |

<br/>
<br/>
<br/>
