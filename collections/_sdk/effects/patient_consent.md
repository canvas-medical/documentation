---
title: "Record Patient Consent"
slug: "effect-record-patient-consent"
excerpt: "Record a patient's decision on a consent and file the signed document."
hidden: false
---

Use the `RecordPatientConsent` effect to record a patient's consent decision on their chart. For example, a plugin can record the decision after the patient completes an intake form. The effect sets the consent's state and effective date, and it can file the signed document with the consent. It runs inside the plugin, so it needs no FHIR API credentials.

Each patient has one [PatientConsent](/sdk/data-patient-consent/) record per consent coding. The first decision for a coding creates the record, and each later decision updates it.

Build a `RecordPatientConsent` with the [attributes](#attributes) you want to set, then return its `apply()` from your handler.

## Methods

### apply() → Effect

Records the patient's decision on one consent.

- `patient_id`, `consent`, `state`, and `effective_date` are required.
- `patient_id` must be the id of an existing patient.
- `consent` must match exactly one [PatientConsentCoding](/sdk/data-patient-consent/#patientconsentcoding).
- `rejection_reason` can be set only when `state` is `REJECTED` or `REJECTED_VIA_PORTAL`, and it must match exactly one [PatientConsentRejectionCoding](/sdk/data-patient-consent/#patientconsentrejectioncoding).
- `document.content` must be valid base64. Line breaks in the encoded content are allowed.

## Attributes

### RecordPatientConsent

| Attribute          | Type                                                                | Description                                                                                         | Required |
|--------------------|---------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|----------|
| `patient_id`       | `str`                                                               | The id of the [patient](/sdk/data-patient/).                                                        | Yes      |
| `consent`          | [ConsentCodingReference](#consentcodingreference)                   | The consent coding the decision applies to.                                                         | Yes      |
| `state`            | [PatientConsentStatus](/sdk/data-patient-consent/#patientconsentstatus) | The patient's decision.                                                                         | Yes      |
| `effective_date`   | `datetime.date`                                                     | The date the decision takes effect. It is also the date of the attached document.                   | Yes      |
| `rejection_reason` | [ConsentCodingReference](#consentcodingreference)                   | The reason the patient rejected the consent. Set it only with a rejected state.                     | No       |
| `document`         | [ConsentDocument](#consentdocument)                                 | The signed consent document to file with the consent.                                               | No       |

The attributes are strictly typed. `state` takes a `PatientConsentStatus` member, not a string, and `effective_date` takes a `datetime.date`, not a `datetime.datetime`.

### ConsentCodingReference

Identifies a consent coding or a rejection coding.

| Attribute | Type  | Description                                                        | Required |
|-----------|-------|--------------------------------------------------------------------|----------|
| `system`  | `str` | The coding system, such as `LOINC` or `INTERNAL`.                  | Yes      |
| `code`    | `str` | The coding's code.                                                 | If `display` is empty |
| `display` | `str` | The coding's display text. Used to find the coding only when `code` is empty. | If `code` is empty |

When `code` is set, the effect finds the coding by `system` and `code`. Otherwise it finds the coding by `system` and `display`. If the reference matches no coding, or more than one, the effect fails validation. Add a `code` to a reference that matches more than one coding.

### ConsentDocument

The signed copy of the consent.

| Attribute  | Type  | Description                                                                         | Required |
|------------|-------|-------------------------------------------------------------------------------------|----------|
| `filename` | `str` | The file name to store the document under, such as `telehealth.pdf`. It can be at most 255 characters and must not contain a path. | Yes |
| `content`  | `str` | The file's bytes, base64 encoded.                                                   | Yes      |

## How Canvas records the decision

- **Expiration date:** Canvas computes the consent's expiration date from `effective_date` and the coding's [expiration rule](/sdk/data-patient-consent/#patientconsentexpirationrule).
- **Rejection reason:** Each decision replaces the consent's rejection reason. A decision without `rejection_reason`, including any accepted decision, clears the earlier reason.
- **Signed documents:** Each document you attach is added to the consent's [signed documents](/sdk/data-patient-consent/#signed-consent-documents) with `effective_date` as its date. The document with the latest date becomes the consent's `active_document`, and earlier signed copies stay on the chart.
- **Other consents:** The effect changes only the consent you name. A consent the patient did not answer keeps its current state.

## Example

This handler records an accepted telehealth consent and attaches the signed PDF:

```python
import base64
import datetime

from canvas_sdk.effects import Effect
from canvas_sdk.effects.patient_consent import (
    ConsentCodingReference,
    ConsentDocument,
    RecordPatientConsent,
)
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.v1.data import PatientConsentStatus


class RecordTelehealthConsent(BaseHandler):
    def compute(self) -> list[Effect]:
        # Replace with the bytes of the PDF the patient signed.
        signed_pdf = b"%PDF-1.7 ..."

        effect = RecordPatientConsent(
            # The handler responds to an event whose target is the patient.
            patient_id=self.event.target.id,
            consent=ConsentCodingReference(system="INTERNAL", code="TELEHEALTH"),
            state=PatientConsentStatus.ACCEPTED_VIA_PORTAL,
            effective_date=datetime.date.today(),
            document=ConsentDocument(
                filename="telehealth.pdf",
                content=base64.b64encode(signed_pdf).decode(),
            ),
        )
        return [effect.apply()]
```

To record a rejection, pass a rejected state and, optionally, the reason:

```python
import datetime

from canvas_sdk.effects.patient_consent import ConsentCodingReference, RecordPatientConsent
from canvas_sdk.v1.data import PatientConsentStatus

effect = RecordPatientConsent(
    patient_id="1eed3ea2a8d546a1b681a2a45de1d790",
    consent=ConsentCodingReference(system="LOINC", code="59284-0"),
    state=PatientConsentStatus.REJECTED,
    effective_date=datetime.date.today(),
    rejection_reason=ConsentCodingReference(system="INTERNAL", display="Patient declined"),
)
effect.apply()
```

<br/>
<br/>
<br/>
