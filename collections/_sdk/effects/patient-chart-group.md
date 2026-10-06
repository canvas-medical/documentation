---
title: "Patient Chart Group"
slug: "patient-chart-group-effect"
excerpt: "Effect for grouping items on a patient chart section"
hidden: false
---

This effect allows developers to group items in a patient chart section. You can define multiple groups with a name, priority, and the items that belong to each group.

This is supported for the Conditions, Medications, and Detected Issues sections.

Build a `PatientChartGroup` with the [groups](#group) to show, then return its `apply()` from your handler.

## Methods

### apply() → Effect

Groups the section's items.

- `items` is required.

## Attributes

| Attribute | Type                                 | Description                               | Required |
|-----------|--------------------------------------|-------------------------------------------|----------|
| `items`   | `dict[str, `[`Group`](#group)`]`     | The groups, keyed by group name.          | Yes      |

## Group

| Attribute  | Type   | Description                                                      |
|------------|--------|------------------------------------------------------------------|
| `items`    | `list` | List of items for each group, for example conditions or medications. |
| `priority` | `int`  | The group's priority within the section.                         |
| `name`     | `str`  | The group label.                                                 |

All three are required.

## Example

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

PatientChartGroup(items={
    "Psychiatry": Group(priority=100, items=conditions, name="Psychiatry"),
    "General": Group(priority=200, items=conditions, name="General"),
}).apply()
```

<br/>
<br/>
<br/>
