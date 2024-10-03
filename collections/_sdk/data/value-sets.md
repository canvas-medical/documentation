---
title: "Value Sets"
slug: "data-value-sets"
excerpt: "Canvas SDK Value Sets"
hidden: false
---

#### Introduction

The Canvas SDK includes a library of built-in Value Sets that can be used within plugins to assist with finding conditions or medications related to Electronic Clinical Quality Measures. Plugin developers can also create their own Value Sets and use them in the same manner as the Canvas built-in `ValueSet` classes.

Built-in Value Sets that can be imported into plugins can be found in the Canvas SDK open source repo [here](https://github.com/canvas-medical/canvas-plugins/tree/main/canvas_sdk/value_set/).

#### Usage

**Filtering Conditions by Value Set**

Value Set classes can be used directly in the data module to query for conditions that are included within them. For example, to find if a patient has been diagnosed with a condition whose coding falls under a particular Value Set, the `find` method can be used as follows:

```python
from logger import log

from canvas_sdk.v1.data.patient import Patient
from canvas_sdk.value_set.v2022.condition import EssentialHypertension

patient = Patient.objects.get(id="6cbc40b408294a5f9b41f57ba1b2b487")
patient_essential_hypertension_conditions = patient.conditions.find(EssentialHypertension)

# The patient has been diagnosed with one or more conditions that match a coding within the EssentialHypertension value set
if patient_essential_hypertension_conditions:
    for condition in patient_essential_hypertension_conditions:
        log.info(condition.codings.all().values())
```

**Filtering Medications by Value Set**

Similar to the `Condition` example above, the `find` method can also utilize Value Set classes to filter `Medication` records that fall under a value set:

```python
from canvas_sdk.v1.data.patient import Patient
from canvas_sdk.value_set.v2022.medication import DementiaMedications

patient = Patient.objects.get(id="6cbc40b408294a5f9b41f57ba1b2b487")
patient_dementia_medications = patient.medications.find(DementiaMedications)

if patient_dementia_medications:
    for medication in patient_dementia_medications:
        log.info(medication.codings.all().values())
```


**Filtering with more than one Value Set**

Sometimes it may be desirable to filter using more than one Value Set. For example, finding all of a patient's conditions that belong within `EssentialHypertension` *or* `DiagnosisOfHypertension`. In this case, the `find` supports the pipe (`|`) operator to filter conditions that match the codings in either Value Set:

```python
from canvas_sdk.v1.data.patient import Patient
from canvas_sdk.value_set.v2022.condition import EssentialHypertension, DiagnosisOfHypertension

patient = Patient.objects.get(id="6cbc40b408294a5f9b41f57ba1b2b487")
patient_hypertension_conditions = patient.conditions.find(EssentialHypertension | DiagnosisOfHypertension)

if patient_hypertension_conditions:
    for condition in patient_hypertension_conditions:
        log.info(condition.codings.all().values())
```

#### Creating Custom Value Sets

The Canvas SDK allows plugin developers to create their own ValueSet classes that can be used in the same manner as the examples above. To do so, one can import and inherit the base `ValueSet` class:

```python
from canvas_sdk.value_set.value_set import ValueSet
```

A new class containing Python sets of coding values can be defined like so:

```python
class MyCustomValueSet(ValueSet):
    VALUE_SET_NAME = "My Custom Value Set"

    ICD10CM = {
        "T2601XA",  # Burn of right eyelid and periocular area, initial encounter
    }

    SNOMEDCT = {
        "284537006",  # Eyelid burn (disorder)
    }
```

The valid code system constants that can be used to define sets of codes in Value Sets are:

| Name           | URL     |
| :------------- | :------- |
|`CPT`| `http://www.ama-assn.org/go/cpt`|
| `HCPCSLEVELII` | `https://coder.aapc.com/hcpcs-codes` |
| `CVX` | `http://hl7.org/fhir/sid/cvx` |
| `LOINC` | `http://loinc.org` |
| `SNOMEDCT` | `http://snomed.info/sct` |
| `FDB` | `http://www.fdbhealth.com/` |
| `RXNORM` | `http://www.nlm.nih.gov/research/umls/rxnorm` |
| `ICD10` | `ICD-10` |
| `NUCC` | `http://www.nucc.org/` |
| `CANVAS` | `CANVAS` |
| `INTERNAL` | `INTERNAL` |
| `NDC` | `http://hl7.org/fhir/sid/ndc` |

The following code is an example of a custom `ValueSet` in use within a plugin:

```python
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from logger import log

from canvas_sdk.v1.data.patient import Patient
from canvas_sdk.value_set.value_set import ValueSet

class MyCustomValueSet(ValueSet):
    VALUE_SET_NAME = "My Custom Value Set"

    ICD10CM = {
        "T2601XA",  # Burn of right eyelid and periocular area, initial encounter
    }

    SNOMEDCT = {
        "284537006",  # Eyelid burn (disorder)
    }


class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_UPDATED)

    def compute(self):
        patient = Patient.objects.get(id="6cbc40b408294a5f9b41f57ba1b2b487")
        custom_value_set_conditions = patient.conditions.find(MyCustomValueSet)
        for vs in custom_value_set_conditions:
            log.info(vs)
        return []
```
