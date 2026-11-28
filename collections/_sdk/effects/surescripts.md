---
title: "Surescripts Effects"
slug: "effect-surescripts"
excerpt: "Effects for sending Surescripts eligibility, medication history, and benefits requests, and for overriding pharmacy benefit identifiers on outbound prescriptions."
hidden: false
---

{% include alert.html type="warning" content="<b>This feature must be enabled by Canvas.</b> To use the Surescripts effects, <a href='https://portal.usepylon.com/canvas-medical/forms/standard'>contact Canvas Support</a> to have these Surescripts effects enabled for your instance. Until it is enabled, these effects will not send requests." %}

Surescripts effects let plugins query insurance eligibility, benefits, and medication history through Surescripts. Eligibility and benefits requests receive responses asynchronously as corresponding events; medication history is handled by Canvas without a plugin-facing response.

A separate effect, [`SurescriptsBenefitsCoordinationOverride`](#benefits-coordination-override), sets the pharmacy benefit identifiers (BIN, PCN, group ID, and member ID) that Canvas sends with a new prescription.

## Eligibility

Check a patient's insurance coverage and plan details. Send a request with `SendSurescriptsEligibilityRequestEffect`, then handle the `SURESCRIPTS_ELIGIBILITY_RESPONSE` event when the response arrives.

### SendSurescriptsEligibilityRequestEffect

Sends an eligibility request to Surescripts to check a patient's insurance coverage. The response arrives as a `SURESCRIPTS_ELIGIBILITY_RESPONSE` event.

Build a `SendSurescriptsEligibilityRequestEffect` and return its `apply()` from your handler.

#### Methods

##### apply() → Effect

Sends the eligibility request.

- `patient_id` and `staff_id` are required.

#### Attributes

| Attribute        | Type  | Description                                                                                                                                                    | Required |
|------------------|-------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| `patient_id`     | `str` | The Canvas [Patient](/sdk/data-patient/#patient) ID for whom to check eligibility.                                                                             | Yes      |
| `staff_id`       | `str` | The Canvas [Staff](/sdk/data-staff/#staff) ID initiating the request.                                                                                          | Yes      |
| `correlation_id` | `str` | A unique identifier for matching the response to this request. Auto-generated if not provided. Read this value after instantiation and store it for later use. | No       |

#### Correlation ID

Each eligibility request includes a `correlation_id` that echoes back in the corresponding `SURESCRIPTS_ELIGIBILITY_RESPONSE` event. Use this to match responses to their originating requests when handling multiple concurrent eligibility checks.

By default, the effect auto-generates a unique `correlation_id` (a UUID hex string). You can pass your own value if you need to thread external state through the request-response cycle.

> **Note:** The `correlation_id` is required for receiving response events. The platform only delivers `SURESCRIPTS_ELIGIBILITY_RESPONSE` events to plugins that sent a request with a valid `correlation_id`.

#### Example

```python
from canvas_sdk.effects.surescripts.surescripts_messages import SendSurescriptsEligibilityRequestEffect
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler


class CheckEligibilityOnAppointment(BaseHandler):
    RESPONDS_TO = [EventType.Name(EventType.APPOINTMENT_CREATED)]

    def compute(self):
        patient_id = self.event.target.get("id")
        staff_id = self.event.context.get("created_by", {}).get("id")

        effect = SendSurescriptsEligibilityRequestEffect(
            patient_id=patient_id,
            staff_id=staff_id,
        )

        # Store the correlation_id to match the response later
        # For example, save it to custom data or cache
        correlation_id = effect.correlation_id

        return [effect.apply()]
```

### Handling Eligibility Responses

When Surescripts returns an eligibility response, the platform fires a `SURESCRIPTS_ELIGIBILITY_RESPONSE` event. Use the typed data classes from `canvas_sdk.events.surescripts` to parse the response.

> **Important:** To prevent infinite loops, you cannot return a `SendSurescriptsEligibilityRequestEffect` from a handler that responds to `SURESCRIPTS_ELIGIBILITY_RESPONSE` events.

#### Response Data Classes

##### SurescriptsEligibilityResponse

The top-level response object containing eligibility results.

| Name             | Type                   | Description                                                           |
|------------------|------------------------|-----------------------------------------------------------------------|
| `correlation_id` | `str`                  | The correlation ID from the originating request.                      |
| `patient_id`     | `str`                  | The Canvas [Patient](/sdk/data-patient/#patient) ID for this eligibility check.                     |
| `plans`          | [EligibilityPlan](#eligibilityplan)[] | List of insurance plans returned in the response.      |
| `error`          | `str` or `None`        | Error message if the request failed, otherwise `None`.                |

##### EligibilityPlan

Represents a single insurance plan from the eligibility response.

| Name                    | Type            | Description                                                                 |
|-------------------------|-----------------|-----------------------------------------------------------------------------|
| `pbm_name`              | `str`           | Name of the Pharmacy Benefit Manager.                                       |
| `payer_id`              | `str`           | Identifier for the insurance payer ([Transactor](/sdk/data-coverage/#transactor)).                                         |
| `member_id`             | `str`           | The patient's member ID for this plan.                                      |
| `plan_network_id`       | `str` or `None` | Network identifier for the plan.                                            |
| `group_number`          | `str` or `None` | Group number for the plan.                                                  |
| `drug_formulary_number` | `str` or `None` | Drug formulary identifier.                                                  |
| `coverage_id`           | `str` or `None` | [Coverage](/sdk/data-coverage/#coverage) identifier.                        |
| `description`           | `str` or `None` | Human-readable description of the plan.                                     |
| `rejected`              | `bool`          | `True` if the eligibility check was rejected for this plan.                 |
| `reject_reason`         | `str` or `None` | Reason for rejection, if applicable.                                        |
| `service_types`         | `list[str]`     | List of service types covered (e.g., "MEDICAL", "RX").                      |

#### Response Handler Example

```python
from canvas_sdk.events import EventType
from canvas_sdk.events.surescripts import EligibilityPlan, SurescriptsEligibilityResponse
from canvas_sdk.handlers.base import BaseHandler
from logger import log


class HandleEligibilityResponse(BaseHandler):
    RESPONDS_TO = [EventType.Name(EventType.SURESCRIPTS_ELIGIBILITY_RESPONSE)]

    def compute(self):
        # Parse the event context into a typed response object
        response = SurescriptsEligibilityResponse.from_context(self.event.context)

        log.info(f"Received eligibility response for correlation_id: {response.correlation_id}")
        log.info(f"Patient ID: {response.patient_id}")

        if response.error:
            log.error(f"Eligibility check failed: {response.error}")
            return []

        for plan in response.plans:
            if plan.rejected:
                log.warning(f"Plan rejected: {plan.pbm_name} - {plan.reject_reason}")
            else:
                log.info(f"Active plan: {plan.pbm_name}, Member ID: {plan.member_id}")
                if plan.service_types:
                    log.info(f"  Service types: {', '.join(plan.service_types)}")

        return []
```

## Benefits

Retrieve formulary and coverage details for a specific medication. Send a request with `SendSurescriptsBenefitsRequestEffect`, then handle the `SURESCRIPTS_BENEFITS_RESPONSE` event when the response arrives.

### SendSurescriptsBenefitsRequestEffect

Sends a benefits request to Surescripts to retrieve formulary and coverage details for a specific medication. The response arrives as a `SURESCRIPTS_BENEFITS_RESPONSE` event.

Build a `SendSurescriptsBenefitsRequestEffect` and return its `apply()` from your handler.

#### Methods

##### apply() → Effect

Sends the benefits request.

- `patient_id`, `staff_id`, `medication_description`, `medication_ndc`, and `plan` are required.

#### Attributes

| Attribute                | Type  | Description                                                                                                                                                    | Required |
|--------------------------|-------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| `patient_id`             | `str` | The Canvas [Patient](/sdk/data-patient/#patient) ID for whom to check benefits.                                                                                | Yes      |
| `staff_id`               | `str` | The Canvas [Staff](/sdk/data-staff/#staff) ID initiating the request.                                                                                          | Yes      |
| `medication_description` | `str` | A human-readable description of the medication (e.g., "Lipitor 10 mg tablet").                                                                                 | Yes      |
| `medication_ndc`         | `str` | The NDC of the medication to check.                                                                                                                            | Yes      |
| `plan`                   | `str` | The plan or PBM to check benefits against.                                                                                                                     | Yes      |
| `correlation_id`         | `str` | A unique identifier for matching the response to this request. Auto-generated if not provided. Read this value after instantiation and store it for later use. | No       |

#### Correlation ID

As with eligibility requests, each benefits request includes a `correlation_id` that echoes back in the corresponding `SURESCRIPTS_BENEFITS_RESPONSE` event. Use this to match responses to their originating requests when handling multiple concurrent benefits checks.

By default, the effect auto-generates a unique `correlation_id` (a UUID hex string). You can pass your own value if you need to thread external state through the request-response cycle.

> **Note:** The `correlation_id` is required for receiving response events. The platform only delivers `SURESCRIPTS_BENEFITS_RESPONSE` events to plugins that sent a request with a valid `correlation_id`.

#### Example

```python
from canvas_sdk.effects.surescripts.surescripts_messages import SendSurescriptsBenefitsRequestEffect
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler


class CheckBenefitsOnPrescription(BaseHandler):
    RESPONDS_TO = [EventType.Name(EventType.PRESCRIBE_COMMAND__POST_ORIGINATE)]

    def compute(self):
        patient_id = self.event.target.get("id")
        staff_id = self.event.context.get("created_by", {}).get("id")

        effect = SendSurescriptsBenefitsRequestEffect(
            patient_id=patient_id,
            staff_id=staff_id,
            medication_description="Lipitor 10 mg tablet",
            medication_ndc="00071015523",
            plan="Acme PBM",
        )

        # Store the correlation_id to match the response later
        correlation_id = effect.correlation_id

        return [effect.apply()]
```

### Handling Benefits Responses

When Surescripts returns a benefits response, the platform fires a `SURESCRIPTS_BENEFITS_RESPONSE` event. Use the typed data classes from `canvas_sdk.events.surescripts` to parse the response.

> **Important:** To prevent infinite loops, you cannot return a `SendSurescriptsBenefitsRequestEffect` from a handler that responds to `SURESCRIPTS_BENEFITS_RESPONSE` events.

#### Response Data Classes

##### SurescriptsBenefitsResponse

The top-level response object containing benefits results.

| Name             | Type                    | Description                                                           |
|------------------|-------------------------|-----------------------------------------------------------------------|
| `correlation_id` | `str`                   | The correlation ID from the originating request.                      |
| `patient_id`     | `str`                   | The Canvas [Patient](/sdk/data-patient/#patient) ID for this benefits check.                        |
| `medication_ndc` | `str`                   | The NDC of the medication that was checked.                           |
| `coverages`      | [BenefitCoverage](#benefitcoverage)[] | List of coverage results returned in the response.    |
| `error`          | `str` or `None`         | Error message if the request failed, otherwise `None`.                |

##### BenefitCoverage

Represents a single coverage result from the benefits response.

| Name                           | Type                            | Description                                                       |
|--------------------------------|---------------------------------|-------------------------------------------------------------------|
| `pbm_name`                     | `str`                           | Name of the Pharmacy Benefit Manager.                             |
| `payer_id`                     | `str`                           | Identifier for the insurance payer ([Transactor](/sdk/data-coverage/#transactor)).                               |
| `formulary_status`             | `str` or `None`                 | Formulary status of the medication (e.g., "On Formulary").        |
| `prior_authorization_required` | `bool`                          | `True` if prior authorization is required.                        |
| `step_therapy_required`        | `bool`                          | `True` if step therapy is required.                               |
| `quantity_limits`              | `list[str]`                     | Human-readable quantity limits (e.g., "30 fills per 1 calendar year"). |
| `copays`                       | `list[str]`                     | Human-readable copay descriptions (e.g., "Tier 2: $25.00").       |
| `alternatives`                 | [TherapeuticAlternative](#therapeuticalternative)[]  | Therapeutic alternatives for the requested medication.            |
| `rejected`                     | `bool`                          | `True` if the benefits check was rejected for this coverage.      |
| `reject_reason`                | `str` or `None`                 | Reason for rejection, if applicable.                              |

##### TherapeuticAlternative

Represents a therapeutic alternative suggested for the requested medication.

| Name                           | Type            | Description                                                |
|--------------------------------|-----------------|------------------------------------------------------------|
| `ndc`                          | `str`           | The NDC of the alternative medication.                     |
| `description`                  | `str` or `None` | Human-readable description of the alternative.             |
| `brand_or_generic`             | `str` or `None` | Whether the alternative is "Brand" or "Generic".           |
| `rx_or_otc`                    | `str` or `None` | Whether the alternative is "Rx" or "OTC".                  |
| `formulary_status`             | `str` or `None` | Formulary status of the alternative.                       |
| `prior_authorization_required` | `bool`          | `True` if prior authorization is required.                 |
| `step_therapy_required`        | `bool`          | `True` if step therapy is required.                        |
| `quantity_limits`              | `list[str]`     | Human-readable quantity limits.                            |
| `copays`                       | `list[str]`     | Human-readable copay descriptions.                         |

#### Response Handler Example

```python
from canvas_sdk.events import EventType
from canvas_sdk.events.surescripts import (
    BenefitCoverage,
    SurescriptsBenefitsResponse,
    TherapeuticAlternative,
)
from canvas_sdk.handlers.base import BaseHandler
from logger import log


class HandleBenefitsResponse(BaseHandler):
    RESPONDS_TO = [EventType.Name(EventType.SURESCRIPTS_BENEFITS_RESPONSE)]

    def compute(self):
        # Parse the event context into a typed response object
        response = SurescriptsBenefitsResponse.from_context(self.event.context)

        log.info(f"Received benefits response for correlation_id: {response.correlation_id}")
        log.info(f"Medication NDC: {response.medication_ndc}")

        if response.error:
            log.error(f"Benefits check failed: {response.error}")
            return []

        for coverage in response.coverages:
            if coverage.rejected:
                log.warning(f"Coverage rejected: {coverage.pbm_name} - {coverage.reject_reason}")
                continue

            log.info(f"{coverage.pbm_name} formulary status: {coverage.formulary_status}")
            if coverage.prior_authorization_required:
                log.info("  Prior authorization required")
            for copay in coverage.copays:
                log.info(f"  Copay: {copay}")
            for alternative in coverage.alternatives:
                log.info(f"  Alternative: {alternative.description} ({alternative.ndc})")

        return []
```

## Medication History

Request a patient's medication history from Surescripts.

Unlike eligibility and benefits, this effect has **no paired response event** — Canvas retrieves the medication history and processes it on the platform side; the results are not delivered back to your plugin. There is no `correlation_id` and no `SURESCRIPTS_MEDICATION_HISTORY_RESPONSE` event to handle.

### SendSurescriptsMedicationHistoryRequestEffect

Sends a medication history request to Surescripts for the patient. Canvas requests the patient's recent fill history (currently the trailing 12 months).

Build a `SendSurescriptsMedicationHistoryRequestEffect` and return its `apply()` from your handler.

#### Methods

##### apply() → Effect

Sends the medication history request.

- `patient_id` and `staff_id` are required.

#### Attributes

| Attribute    | Type  | Description                                                                              | Required |
|--------------|-------|------------------------------------------------------------------------------------------|----------|
| `patient_id` | `str` | The Canvas [Patient](/sdk/data-patient/#patient) ID whose medication history to request. | Yes      |
| `staff_id`   | `str` | The Canvas [Staff](/sdk/data-staff/#staff) ID initiating the request.                    | Yes      |

#### Example

```python
from canvas_sdk.effects.surescripts.surescripts_messages import SendSurescriptsMedicationHistoryRequestEffect
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler


class RequestMedicationHistoryOnAppointment(BaseHandler):
    RESPONDS_TO = [EventType.Name(EventType.APPOINTMENT_CREATED)]

    def compute(self):
        patient_id = self.event.target.get("id")
        staff_id = self.event.context.get("created_by", {}).get("id")

        return [
            SendSurescriptsMedicationHistoryRequestEffect(
                patient_id=patient_id,
                staff_id=staff_id,
            ).apply()
        ]
```

## Benefits coordination override

Set the pharmacy benefit identifiers that Canvas sends to the pharmacy with a new electronic prescription. Use it when your plugin has the correct BIN, PCN, group ID, or member ID for a patient. For example, a program or benefit manager might supply these values. Canvas then sends those values even when they differ from the Surescripts eligibility response, or when no eligibility check was run.

By default, Canvas fills the `BenefitsCoordination` segment of the outbound Surescripts NewRx message from the patient's Surescripts eligibility response. Right before it sends the NewRx, Canvas fires the [`PRESCRIBE_COMMAND__PRE_SEND`](/sdk/events/#prescribe-command) event. A handler for that event can return a `SurescriptsBenefitsCoordinationOverride` effect to replace any of those values.

### SurescriptsBenefitsCoordinationOverride

Overrides fields in the `BenefitsCoordination` segment of the outbound NewRx message. Return it from a handler that responds to `PRESCRIBE_COMMAND__PRE_SEND`.

#### Methods

##### apply() → Effect

Overrides each benefits coordination field you set. No attribute is required.

#### Behavior

- Each attribute is optional and independent. An attribute you set replaces the value Canvas derived from eligibility for that field. An attribute you leave unset, or set to an empty string, keeps the eligibility-derived value.
- When you set at least one attribute, Canvas includes the `BenefitsCoordination` segment in the NewRx even if no eligibility check was run for the patient.
- When more than one effect sets the same attribute for a prescription, the last one wins.

#### Attributes

| Attribute                         | Type  | Description                                                                              | Required |
|-----------------------------------|-------|------------------------------------------------------------------------------------------|----------|
| `iin_number`                      | `str` | The BIN (issuer identification number), sent as `PayerIdentification/IINNumber`.        | No       |
| `processor_identification_number` | `str` | The PCN (processor control number), sent as `PayerIdentification/ProcessorIdentificationNumber`. | No       |
| `group_id`                        | `str` | The pharmacy benefit group ID, sent as `GroupID`.                                        | No       |
| `pbm_member_id`                   | `str` | The patient's member ID with the pharmacy benefit manager, sent as `PBMMemberID`.        | No       |

#### Event data

The `PRESCRIBE_COMMAND__PRE_SEND` event carries the following identifiers:

| Location                                   | Value                                                         |
|--------------------------------------------|---------------------------------------------------------------|
| `self.event.target.id`                     | The ID of the [Prescription](/sdk/data-prescription/) being sent. |
| `self.event.context["prescription"]["id"]` | The same prescription ID.                                     |
| `self.event.context["patient"]["id"]`      | The ID of the patient the prescription is for.                |

#### Example

This handler sends a program's BIN, PCN, and group ID, stored as [plugin secrets](/sdk/secrets/), on every new prescription. Fields it doesn't set, such as the member ID, keep their eligibility-derived values.

```python
from canvas_sdk.effects.surescripts import SurescriptsBenefitsCoordinationOverride
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler


class OverridePharmacyBenefits(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PRESCRIBE_COMMAND__PRE_SEND)

    def compute(self):
        return [
            SurescriptsBenefitsCoordinationOverride(
                iin_number=self.secrets["RX_BIN"],
                processor_identification_number=self.secrets["RX_PCN"],
                group_id=self.secrets["RX_GROUP_ID"],
            ).apply()
        ]
```

## Imports

```python
# Effects for sending requests
from canvas_sdk.effects.surescripts.surescripts_messages import (
    SendSurescriptsBenefitsRequestEffect,
    SendSurescriptsEligibilityRequestEffect,
    SendSurescriptsMedicationHistoryRequestEffect,
)

# Effect for overriding benefits coordination on outbound prescriptions
from canvas_sdk.effects.surescripts import SurescriptsBenefitsCoordinationOverride

# Data classes for parsing responses
from canvas_sdk.events.surescripts import (
    BenefitCoverage,
    EligibilityPlan,
    SurescriptsBenefitsResponse,
    SurescriptsEligibilityResponse,
    TherapeuticAlternative,
)
```

<br/>
<br/>
<br/>
