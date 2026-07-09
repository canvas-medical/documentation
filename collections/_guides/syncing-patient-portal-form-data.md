---
title: "Syncing Patient Portal Form Data to the Chart"
guide_for:
- /sdk/data-questionnaire/
- /sdk/events/
- /sdk/effect-patient/
- /sdk/form-result-effect/
---

<!-- sources: discussions #785, #696 -->

This guide builds on [Implementing Patient Portal Forms](/guides/patient-portal-forms/). Once a patient fills out a form in the portal, you often want that data to flow back into the chart — updating demographics, recording insurance coverage, and so on. This guide explains how questionnaires and patients are linked, and how a clinic-side handler can act on a submitted form.

## How questionnaires link to patients: the Interview

A [`Questionnaire`](/sdk/data-questionnaire/) is the form definition. A patient's *responses* to a questionnaire are stored as an [`Interview`](/sdk/data-questionnaire/#interview) — the Interview is the link between a `Patient` and a `Questionnaire`. A patient who has never completed a given form has no Interview for it.

This matters when you decide which forms to present in the portal. To find which intake forms a patient has already completed, filter Interviews for that patient:

```python
from canvas_sdk.v1.data import Interview

INTAKE_QUESTIONNAIRES = ["Tobacco", "Stress"]

completed_forms = set(
    Interview.objects.filter(
        patient=patient,
        entered_in_error_id__isnull=True,
        questionnaires__name__in=INTAKE_QUESTIONNAIRES,
    ).values_list("questionnaires__name", flat=True)
)
```

`completed_forms` returns an **empty set** when the patient has no completed questionnaires (no matching Interviews). If you are seeing every intake questionnaire appear as "completed," confirm that you are filtering Interviews (the patient's responses), not the `Questionnaire` definitions themselves — the questionnaires always exist, but Interviews only exist after a patient submits.

You then present the forms the patient is still missing:

```python
missing_intake_forms = [qname for qname in INTAKE_QUESTIONNAIRES if qname not in completed_forms]
```

For the full portal-side flow — listening for `PATIENT_PORTAL__GET_FORMS` and returning `FormResult` effects — see [Implementing Patient Portal Forms](/guides/patient-portal-forms/).

## Acting on a submitted form from the clinic side

To sync the responses into the chart, set up a handler that listens for the [questionnaire created event](/sdk/events/#questionnaire-command). When it fires, read the responses from the resulting [Interview](/sdk/data-questionnaire/#interview) and return whatever [effects](/sdk/effects/) you need:

- To update demographics (name, contact details, and so on), use the [patient effects](/sdk/effect-patient/).
- To record insurance coverage, use the [FHIR API coverage endpoints](/api/coverage/), since coverage is not currently writable through a dedicated SDK effect.

The high-level flow for a "collect demographics and coverage in the portal, write them to the chart" workflow is:

```
Patient submits the portal form
  → Responses are stored as an Interview linking the Patient and Questionnaire
  → A questionnaire created event fires
  → Clinic-side handler reads the Interview responses
  → Returns a patient effect to update demographics
  → Calls the FHIR Coverage endpoint to record insurance coverage
```

Because the responses live on the Interview, your handler can map each answer to the corresponding patient field or coverage attribute and apply the appropriate effect or API call.
