---
title: "Surescripts Effects"
slug: "effect-surescripts"
excerpt: "Effects for sending Surescripts eligibility, medication history, and benefits requests."
hidden: false
---

{% include alert.html type="warning" content="<b>This feature must be enabled by Canvas.</b> To use the Surescripts effects, <a href='https://portal.usepylon.com/canvas-medical/forms/standard'>contact Canvas Support</a> to have these Surescripts effects enabled for your instance. Until it is enabled, these effects will not send requests." %}

Surescripts effects let plugins query insurance eligibility, benefits, and medication history through Surescripts. Eligibility and benefits requests receive responses asynchronously as corresponding events; medication history is handled by Canvas without a plugin-facing response.

## Eligibility

Check a patient's insurance coverage and plan details. Send a request with `SendSurescriptsEligibilityRequestEffect`, then handle the `SURESCRIPTS_ELIGIBILITY_RESPONSE` event when the response arrives.

### SendSurescriptsEligibilityRequestEffect

Sends an eligibility request to Surescripts to check a patient's insurance coverage. The response arrives as a `SURESCRIPTS_ELIGIBILITY_RESPONSE` event.

#### Attributes

| Name             | Type   | Description                                                                                                                                                     |
|------------------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `patient_id`     | `str`  | The Canvas [Patient](/sdk/data-patient/#patient) ID for whom to check eligibility.                                                                                                            |
| `staff_id`       | `str`  | The Canvas [Staff](/sdk/data-staff/#staff) ID initiating the request.                                                                                                                     |
| `correlation_id` | `str`  | A unique identifier for matching the response to this request. Auto-generated if not provided. Read this value after instantiation and store it for later use. |

#### Correlation ID

Each eligibility request includes a `correlation_id` that echoes back in the corresponding `SURESCRIPTS_ELIGIBILITY_RESPONSE` event. Use this to match responses to their originating requests when handling multiple concurrent eligibility checks.

By default, the effect auto-generates a unique `correlation_id` (a UUID hex string). You can pass your own value if you need to thread external state through the request-response cycle.

> **Note:** The `correlation_id` is required for receiving response events. The platform only delivers `SURESCRIPTS_ELIGIBILITY_RESPONSE` events to plugins that sent a request with a valid `correlation_id`.

#### Example Usage

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

#### Attributes

| Name                     | Type   | Description                                                                                                                                                     |
|--------------------------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `patient_id`             | `str`  | The Canvas [Patient](/sdk/data-patient/#patient) ID for whom to check benefits.                                                                                                              |
| `staff_id`               | `str`  | The Canvas [Staff](/sdk/data-staff/#staff) ID initiating the request.                                                                                                                     |
| `medication_description` | `str`  | A human-readable description of the medication (e.g., "Lipitor 10 mg tablet").                                                                                  |
| `medication_ndc`         | `str`  | The NDC of the medication to check.                                                                                                                            |
| `plan`                   | `str`  | The plan or PBM to check benefits against.                                                                                                                      |
| `correlation_id`         | `str`  | A unique identifier for matching the response to this request. Auto-generated if not provided. Read this value after instantiation and store it for later use. |

#### Correlation ID

As with eligibility requests, each benefits request includes a `correlation_id` that echoes back in the corresponding `SURESCRIPTS_BENEFITS_RESPONSE` event. Use this to match responses to their originating requests when handling multiple concurrent benefits checks.

By default, the effect auto-generates a unique `correlation_id` (a UUID hex string). You can pass your own value if you need to thread external state through the request-response cycle.

> **Note:** The `correlation_id` is required for receiving response events. The platform only delivers `SURESCRIPTS_BENEFITS_RESPONSE` events to plugins that sent a request with a valid `correlation_id`.

#### Example Usage

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

#### Attributes

| Name         | Type  | Description                                                              |
|--------------|-------|--------------------------------------------------------------------------|
| `patient_id` | `str` | The Canvas [Patient](/sdk/data-patient/#patient) ID whose medication history to request. |
| `staff_id`   | `str` | The Canvas [Staff](/sdk/data-staff/#staff) ID initiating the request.    |

#### Example Usage

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

## Imports

```python
# Effects for sending requests
from canvas_sdk.effects.surescripts.surescripts_messages import (
    SendSurescriptsBenefitsRequestEffect,
    SendSurescriptsEligibilityRequestEffect,
    SendSurescriptsMedicationHistoryRequestEffect,
)

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
