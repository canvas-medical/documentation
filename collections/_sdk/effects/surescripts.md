---
title: "Surescripts Effects"
slug: "effect-surescripts"
excerpt: "Effects for sending Surescripts eligibility, medication history, and benefits requests."
hidden: false
---

Surescripts effects let plugins query insurance eligibility, medication history, and benefits information through Surescripts. These effects send requests to Surescripts, and responses arrive asynchronously as corresponding events.

## SendSurescriptsEligibilityRequestEffect

Sends an eligibility request to Surescripts to check a patient's insurance coverage. The response arrives as a `SURESCRIPTS_ELIGIBILITY_RESPONSE` event.

### Attributes

| Name             | Type   | Description                                                                                                                                                     |
|------------------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `patient_id`     | `str`  | The Canvas patient ID for whom to check eligibility.                                                                                                            |
| `staff_id`       | `str`  | The Canvas staff ID initiating the request.                                                                                                                     |
| `correlation_id` | `str`  | A unique identifier for matching the response to this request. Auto-generated if not provided. Read this value after instantiation and store it for later use. |

### Correlation ID

Each eligibility request includes a `correlation_id` that echoes back in the corresponding `SURESCRIPTS_ELIGIBILITY_RESPONSE` event. Use this to match responses to their originating requests when handling multiple concurrent eligibility checks.

By default, the effect auto-generates a unique `correlation_id` (a UUID hex string). You can pass your own value if you need to thread external state through the request-response cycle.

> **Note:** The `correlation_id` is required for receiving response events. The platform only delivers `SURESCRIPTS_ELIGIBILITY_RESPONSE` events to plugins that sent a request with a valid `correlation_id`.

### Example Usage

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

## Handling Eligibility Responses

When Surescripts returns an eligibility response, the platform fires a `SURESCRIPTS_ELIGIBILITY_RESPONSE` event. Use the typed data classes from `canvas_sdk.events.surescripts` to parse the response.

> **Important:** To prevent infinite loops, you cannot return a `SendSurescriptsEligibilityRequestEffect` from a handler that responds to `SURESCRIPTS_ELIGIBILITY_RESPONSE` events.

### Response Data Classes

#### SurescriptsEligibilityResponse

The top-level response object containing eligibility results.

| Name             | Type                   | Description                                                           |
|------------------|------------------------|-----------------------------------------------------------------------|
| `correlation_id` | `str`                  | The correlation ID from the originating request.                      |
| `patient_id`     | `str`                  | The Canvas patient ID for this eligibility check.                     |
| `plans`          | `list[EligibilityPlan]`| List of insurance plans returned in the response.                     |
| `error`          | `str` or `None`        | Error message if the request failed, otherwise `None`.                |

#### EligibilityPlan

Represents a single insurance plan from the eligibility response.

| Name                    | Type            | Description                                                                 |
|-------------------------|-----------------|-----------------------------------------------------------------------------|
| `pbm_name`              | `str`           | Name of the Pharmacy Benefit Manager.                                       |
| `payer_id`              | `str`           | Identifier for the insurance payer.                                         |
| `member_id`             | `str`           | The patient's member ID for this plan.                                      |
| `plan_network_id`       | `str` or `None` | Network identifier for the plan.                                            |
| `group_number`          | `str` or `None` | Group number for the plan.                                                  |
| `drug_formulary_number` | `str` or `None` | Drug formulary identifier.                                                  |
| `coverage_id`           | `str` or `None` | Coverage identifier.                                                        |
| `description`           | `str` or `None` | Human-readable description of the plan.                                     |
| `rejected`              | `bool`          | `True` if the eligibility check was rejected for this plan.                 |
| `reject_reason`         | `str` or `None` | Reason for rejection, if applicable.                                        |
| `service_types`         | `list[str]`     | List of service types covered (e.g., "MEDICAL", "RX").                      |

### Response Handler Example

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

### Imports

```python
# Effect for sending requests
from canvas_sdk.effects.surescripts.surescripts_messages import SendSurescriptsEligibilityRequestEffect

# Data classes for parsing responses
from canvas_sdk.events.surescripts import EligibilityPlan, SurescriptsEligibilityResponse
```

## Other Surescripts Effects

The following Surescripts effects are also available:

| Effect                                     | Description                                      |
|--------------------------------------------|--------------------------------------------------|
| `SEND_SURESCRIPTS_ELIGIBILITY_REQUEST`     | Send an eligibility request (documented above).  |
| `SEND_SURESCRIPTS_MEDICATION_HISTORY_REQUEST` | Send a medication history request.            |
| `SEND_SURESCRIPTS_BENEFITS_REQUEST`        | Send a benefits request.                         |

<br/>
<br/>
<br/>
