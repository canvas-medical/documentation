---
title: "Intake Forms"
slug: "effect-intake-forms"
excerpt: "Effects for intake forms"
hidden: false
---

# Intake Forms

The **Canvas SDK** supports dynamically creating intake forms in the **patient portal** using existing questionnaires.
This feature is currently **in development** and subject to change.

---

## Overview

Plugins can generate patient intake forms by responding to the `PATIENT_PORTAL__GET_INTAKE_FORMS`event and returning an
`IntakeFormResults` effect.
When Canvas encounters this effect, it will build and display a sequence of forms in the patient portal, based on the
`Questionnaire` objects you specify.

1. **Event Trigger**

- Occurs when the patient portal requests intake forms (currently only when loading the application).

2. **Create `IntakeFormResults`**

- Bundle the questionnaire IDs into an `IntakeFormResults` effect and return it from `compute()`.

3. **Patient Portal Displays Forms**

- Canvas automatically generates and displays the questionnaires as forms in the patient portal. Patients can fill
  these out, and Interviews will be created from their responses.

---

### Example

Below is a simple example of how to provide a list of `Questionnaire` objects as intake forms. It checks whether the
patient has already completed a form (by looking for an existing `Interview` object) and filters out any previously
completed forms.

```python
import json

from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.effects.patient_portal.intake_form_results import IntakeFormResults
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.v1.data import Patient, Interview, Questionnaire


class Protocol(BaseProtocol):
  RESPONDS_TO = EventType.Name(EventType.PATIENT_PORTAL__GET_INTAKE_FORMS)

  def compute(self) -> list[Effect]:
    # Get the patient from the target
    patient = Patient.objects.get(id=self.target)

    # Get required intake forms:
    intake_1 = Questionnaire.objects.first()
    intake_2 = Questionnaire.objects.last()

    intake_forms = [intake_1, intake_2]

    # Check if the patient already has an interview for the intake form and remove it from the list
    final_intake_forms = []
    for questionnaire in intake_forms:
      if not Interview.objects.filter(patient=patient,
                                      questionnaires__id=questionnaire.id).exists():
        final_intake_forms.append(questionnaire)

    effect = IntakeFormResults(questionnaire_ids=[q.id for q in final_intake_forms])
    return [effect.apply()]
```
