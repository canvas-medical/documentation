---
title: "Lab Partner & Lab Partner Test"
slug: "data-lab-partner-and-test"
excerpt: "Canvas SDK Lab Partner and Lab Partner Test models"
hidden: false
---

## Introduction

The **LabPartner** and **LabPartnerTest** models represent external lab partners and the tests they offer within Canvas.

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
|-----------------------------|---------|---------------------------------------------------------------------|
| id                          | UUID    | The universally unique identifier for the lab partner.              |
| dbid                        | Integer | The internal database identifier (primary key) for the lab partner. |
| name                        | String  | The name of the lab partner.                                        |
| active                      | Boolean | Indicates whether the lab partner is currently active.              |
| electronic_ordering_enabled | Boolean | Indicates if electronic ordering is enabled for this lab partner.   |
| keywords                    | Text    | Keywords associated with the lab partner.                           |
| default_lab_account_number  | String  | The default lab account number used for orders.                     |

### LabPartnerTest Attributes

| Field Name  | Type       | Description                                                                                  |
|-------------|------------|----------------------------------------------------------------------------------------------|
| id          | UUID       | The universally unique identifier for the test record.                                       |
| dbid        | Integer    | The internal database identifier (primary key) for the test record.                          |
| lab_partner | ForeignKey | A reference to the related `LabPartner` (accessible via the related name `available_tests`). |
| order_code  | String     | A code used to identify the test order. May be blank.                                        |
| order_name  | Text       | The name of the test order.                                                                  |
| keywords    | Text       | Keywords associated with the test. May be blank.                                             |
| cpt_code    | String     | The CPT code for the test, if available. Can be blank or null.                               |

<br/>
<br/>
<br/>
