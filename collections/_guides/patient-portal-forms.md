---
title: "Implementing Patient Portal Forms in Canvas SDK"
guide_for:
  - /sdk/effects-form-result/
---

The Canvas SDK enables custom patient engagement workflows by dynamically displaying forms (questionnaires) within the
Patient Portal. This guide walks through implementing a plugin that automatically assigns forms based on a patient's
appointment type and previously completed forms.
The patient’s responses are stored as Interviews, and the developer can choose to generate a Questionnaire Command
within a Note.

## **In this guide you will learn how to:**

- Use the [`FormResult`](/sdk/effects-form-result) effect to display questionnaires dynamically.
- Fetch patient [appointments](/sdk/data-appointment/) and [interviews](/sdk/data-interview/).
- Control when forms should be shown or hidden.
- Optionally create a Questionnaire Command inside a Note.

## **How It Works**

1. **On each Patient Portal page load**, the plugin evaluates which forms to show.
2. Forms are automatically assigned based on:
  - **Upcoming Appointments**
  - **Previously completed forms**
3. If applicable, the response can create a Questionnaire Command inside a Note.
4. The developer is responsible for ensuring that forms do not persist unnecessarily.

## **Adding Form Logic in a Protocol Handler**

We define a **Protocol** that listens for `PATIENT_PORTAL__GET_FORMS` events and determines which forms need to be
displayed.

```python
from canvas_sdk.effects.patient_portal.form_result import FormResult
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data import Patient, Appointment, Interview, Note, Questionnaire
from canvas_sdk.v1.data.appointment import AppointmentProgressStatus
import arrow

INTAKE_QUESTIONNAIRES = [
  "Insurance Details",
  "Preferred Pharmacy Details",
  "Social History",
]


class Protocol(BaseHandler):
  """Protocol for processing Patient Portal form requests and generating form effects."""

  RESPONDS_TO = EventType.Name(EventType.PATIENT_PORTAL__GET_FORMS)

  def _get_upcoming_appointment_note_id(self, appointments, codes):
    """Retrieve the note_id for the first confirmed future appointment matching given codes."""
    now = arrow.now().date()
    return appointments.filter(
      status=AppointmentProgressStatus.CONFIRMED,
      start_time__gt=now,
      note_type__code__in=codes
    ).values_list("note__id", flat=True).first()

  def compute(self):
    """Compute and return a list of FormResult effects based on upcoming appointments."""

    patient = Patient.objects.get(id=self.target)
    patient_appointments = patient.appointments

    completed_forms = set(
      Interview.objects.filter(
        patient=patient,
        questionnaires__name__in=INTAKE_QUESTIONNAIRES
      ).values_list("questionnaires__name", flat=True)
    )

    forms = []

    # Assign Intake Forms for new patients
    if note_id := self._get_upcoming_appointment_note_id(patient_appointments, ["telehealth", "office"]):
      missing_intake_forms = [qname for qname in INTAKE_QUESTIONNAIRES if qname not in completed_forms]
      missing_intake_questionnaire_ids = Questionnaire.objects.filter(name__in=missing_intake_forms).values_list("id",
                                                                                                                 flat=True)

      forms = [
        FormResult(questionnaire_id=qid, create_command=True, note_id=note_id).apply()
        for qid in missing_intake_questionnaire_ids
      ]

    return forms
```

## **Best Practices**

- **Prevent Duplicate Forms:** Since this logic runs on every page load, check **existing responses** before assigning
  new forms.

## **Summary**

- This plugin **automatically assigns Patient Portal forms** based on upcoming appointments.
- Forms are created as **Questionnaires**, and responses are stored as **Interviews**.
- The developer can **optionally** create a **Questionnaire Command** inside a **Note**.
- **Forms are re-evaluated on each page load**, so plugin developers must ensure they don’t persist unnecessarily.
