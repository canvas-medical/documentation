---
title: 'Group Items in Patient Chart'
slug: 'example-patient_summary_chart_groups'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/patient_summary_chart_groups' target='_blank'>View the source</a> for this plugin on GitHub." %}

A plugin that groups Psychiatry conditions and medications in the patient summary chart.

## SDK Features
* Responds to `PATIENT_CHART__CONDITIONS` and `PATIENT_CHART__MEDICATIONS` [events](/sdk/events/#patient-chart-configuration)
* Loads the patient conditions and medications using event context
* Iterates through conditions to retrieve the ICD10 CodeSystem and assigns to a [Group effect](/sdk/patient-chart-group-effect/#group) list of items
* Iterates through medications to find an RxNorm match on a list of plugin-defined medication codes and assigns to a [Group effect](/sdk/patient-chart-group-effect/#group) list of items
* Returns the [`PatientChartGroup` effect](/sdk/patient-chart-group-effect/) with `.apply()` called

## CANVAS_MANIFEST.json

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1",
    "name": "patient_summary_chart_groups",
    "description": "A plugin that groups Psychiatry conditions and medications in the patient summary chart.",
    "components": {
        "handlers": [
            {
                "class": "patient_summary_chart_groups.handlers.my_handler:Conditions",
                "description": "A handler that groups Psychiatry conditions"
            },
            {
                "class": "patient_summary_chart_groups.handlers.my_handler:Medications",
                "description": "A handler that groups Psychiatry medications"
            }
        ],
        "commands": [],
        "content": [],
        "effects": [],
        "views": []
    },
    "secrets": [],
    "tags": {},
    "references": [],
    "license": "",
    "diagram": false,
    "readme": "./README.md"
}
```

## handlers/

### my_handler.py

This file defines two custom handlers, `Conditions` and `Medications`, using the Canvas SDK. These handlers listen for specific events related to a patient's medical chart and group relevant diagnoses or medications into a "Psychiatry" category, returning these as effects for further processing or display in the Canvas UI.

**Section: `Conditions` Handler**

- Inherits from `BaseHandler`.
- Listens to the `EventType.PATIENT_CHART__CONDITIONS` event (triggered when a patient's chart conditions are accessed).
- For each condition in the event context, it looks at the `codings` list:
  - If the coding system is ICD-10 (`CodeSystems.ICD10`) and the code falls within the ICD-10 psychiatry range ("F01" to "F99") or starts with "R45." (indicating certain psychiatric symptoms), the condition is added to a group named "Psychiatry".
- The resulting group is returned using a `PatientChartGroup` effect, applied to be consumed by other parts of the platform (such as UI rendering).

**Section: `Medications` Handler**

- Inherits from `BaseHandler`.
- Listens to the `EventType.PATIENT_CHART__MEDICATIONS` event (triggered when a patient's medication list is accessed).
- Maintains an explicit list of RxNorm codes (`medication_codes`) representing psychiatric or relevant medications.
- For each medication in the event context, it looks at the `codings` list:
  - If the coding system is RxNorm (`CodeSystems.RXNORM`) and the code (converted to integer) is in the handler's medication list, the medication is added to the "Psychiatry" group.
- The resulting group is returned using a `PatientChartGroup` effect, again allowing psychiatric medications to be grouped in the UI.

**Section: Canvas SDK Constructs Used**

- **Events:** Listens for specific event types (patient chart conditions or medications).
- **Effects:** Returns grouping instructions as `PatientChartGroup` effects, making downstream processing or UI changes possible.
- **Grouping:** Uses the `Group` object to label and prioritize (with `priority=100`) psychiatric items, and the `PatientChartGroup` to wrap effect logic for patient chart groupings.

**Section: Implementation Details**

- The handlers use dictionary storage for groups but always construct only a single "Psychiatry" group.
- ICD-10 and RxNorm code checks strictly conform to predefined domain ranges or explicit code lists.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.group import Group
from canvas_sdk.effects.patient_chart_group import PatientChartGroup
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.commands.constants import CodeSystems

class Conditions(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_CHART__CONDITIONS)

    def compute(self) -> list[Effect]:
        groups: dict[str, Group] = {}
        groups.setdefault("Psychiatry", Group(priority=100, items=[], name="Psychiatry"))

        for condition in self.event.context:
           for coding in condition["codings"]:
               if coding["system"] == CodeSystems.ICD10 and ("F01" <= coding["code"] <= "F99" or coding["code"].startswith("R45.")):
                   groups["Psychiatry"].items.append(condition)
                   break

        return [PatientChartGroup(items=groups).apply()]


class Medications(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_CHART__MEDICATIONS)

    medication_codes = [
        70223, 725, 17941, 1359, 89781, 314517, 1422, 42347, 1841, 3007, 2591497, 62174, 22656, 352372, 3288, 1598,
        3389, 3415, 3416, 3417, 3554, 10402, 11636, 1653781, 4024, 14584, 4328, 325526, 4850, 6130, 6373, 700810, 6664,
        6694, 6782, 6816, 6901, 7243, 326374, 31994, 7781, 2387302, 7966, 33272, 8133, 8150, 8152, 8702, 8704, 9260,
        36514, 1547099, 10689, 11289, 68503, 3920, 4457, 237005, 6378, 6754, 7814, 8001, 9601, 3264, 7242, 7895, 237099,
        203223, 3554, 2626143, 6711, 7407, 314875, 11256, 82819, 161203, 16735, 272, 2557217, 237099, 596, 704, 719,
        722, 725, 17381, 89013, 1673265, 641465, 784649, 38400, 1291301, 1292, 1373, 2690627, 2176312, 2121777, 1658314,
        1749, 19759, 19777, 1819, 42347, 1827, 477631, 19874, 2002, 1667655, 2296, 2356, 2372, 2373, 2403, 2406, 2556,
        2597, 2598, 2599, 2603, 2353, 2622, 2626, 3013, 2591497, 62174, 3247, 3251, 734064, 352372, 3288, 3322, 3332,
        91235, 3403, 3407, 203223, 3498, 3554, 2687966, 135447, 3634, 3637, 3638, 3642, 3648, 72625, 3755, 4024, 321988,
        2119365, 4077, 461016, 4118, 24474, 4328, 1665509, 4457, 4460, 4493, 4495, 4496, 4501, 4507, 42355, 25480, 4637,
        2672253, 325526, 4903, 40114, 26412, 5093, 2267703, 5553, 73178, 5691, 5975, 262150, 6011, 6026, 285228, 28439,
        2626143, 2272403, 237005, 1433212, 700810, 6448, 746070, 42351, 52105, 1546376, 28863, 6470, 28894, 6475,
        2275602, 1040028, 52356, 6646, 6673, 6680, 6711, 6719, 6760, 6779, 6813, 6816, 6823, 6852, 6901, 6904, 6910,
        6960, 588250, 15996, 30125, 7019, 31479, 7242, 7243, 31565, 7407, 7440, 7486, 3155, 7531, 61381, 26225, 1370971,
        7781, 2387302, 679314, 7895, 7909, 32937, 7966, 7974, 8042, 8047, 8766, 8076, 8123, 8156, 8331, 33739, 8338,
        8348, 2197878, 34345, 746741, 3143, 8627, 8701, 8704, 8742, 8770, 8782, 8787, 8825, 8826, 8886, 35185, 51272,
        9100, 596205, 60842, 9260, 35636, 183379, 616739, 2559612, 9624, 9639, 2562176, 41996, 36437, 36676, 1547099,
        10318, 1490468, 10355, 10390, 37985, 10437, 10454, 10464, 38077, 10502, 10510, 31914, 38260, 314875, 38365,
        38404, 10734, 10737, 10767, 1314420, 10800, 10804, 10805, 10834, 10898, 21406, 11017, 1665222, 253206, 40254,
        39786, 1086769, 11256, 1455099, 2694828, 220982, 74667, 115698, 39993, 2669905
    ]

    def compute(self) -> list[Effect]:
        groups: dict[str, Group] = {}
        groups.setdefault("Psychiatry", Group(priority=100, items=[], name="Psychiatry"))

        for medication in self.event.context:
            for coding in medication["codings"]:
                if coding["system"] == CodeSystems.RXNORM and int(coding["code"]) in self.medication_codes:
                    groups["Psychiatry"].items.append(medication)
                    break

        return [PatientChartGroup(items=groups).apply()]
```

## Customize

- The handler is extensible: additional groups or more refined code logic could be added in the future.
<br/>
<br/>
<br/>
