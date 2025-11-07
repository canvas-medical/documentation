---
title: "Patient Chart Group"
slug: "patient-chart-group-effect"
excerpt: "Effect for grouping items on a patient chart section"
hidden: false
---

## Overview

This effect allows developers to group items in a patient chart section. You can define multiple groups with a name, priority, and the items that belong to each group.

Currently, this is supported for the Conditions, Medications, and Detected Issues sections.

```python
from canvas_sdk.effects.patient_chart_group import PatientChartGroup
from canvas_sdk.effects.group import Group

conditions = [{
    "id": 1,
    "codings": {
      "code": "111",
      "system": "ICD-10",
      "display": "Ophiasis",
    }
  }, {
    "id": 2,
    "codings": {
      "code": "112",
      "system": "ICD-10",
      "display": "Acute angle-closure glaucoma",
    }
}]

PatientChartGroup(items=[
  {
    "Psychiatry": Group(priority=100, items=conditions, name="Psychiatry")
  },
  {
    "General": Group(priority=200, items=conditions, name="General")
  }
])
```

## Structure

### **Group**

A Group consists of the following properties:

#### Attributes

| Attribute  | Type   | Description                              |
|------------|--------|------------------------------------------|
| `items`    | `list` | list of items for each group, ex: [Condition] or [Medication]            |
| `priority` | `int`  | the group’s priority within the section. |
| `name`     | `str`  | the group label.                         |

### **PatientChartGroup**

A PatientChartGroup consists of the following properties:

#### Attributes

| Attribute  | Type               | Description    |
|------------|--------------------|----------------|
| `items`    | `dict[str, Group]` | list of Groups |
