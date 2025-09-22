---
title: "Protocols"
---

The protocols module lets you define workflows and workflow automations.

Protocols respond to [Events](/sdk/events/) and return zero, one, or many [Effects](/sdk/effects/).

## Contents

- [BaseProtocol](#baseprotocol)
- [ClinicalQualityMeasure](#clinicalqualitymeasure)

## BaseProtocol

`BaseProtocol` is the abstract base class all protocol implementations inherit from. It extends the handler contract (`BaseHandler`) and provides the lifecycle and surface area plugin authors implement for event-driven protocols.

### Purpose & lifecycle

- A protocol is instantiated with an incoming `Event` and optional `secrets` and `environment` dictionaries.
- The framework will call `compute()` on the protocol instance when an event should be handled. `compute()` must
  return a list of `Effect` objects that the runtime will apply.
- Protocols must override the `compute()` method.

### Constructor and attributes

- Your protocol should inherit from `BaseProtocol` and define the following:

  - `RESPONDS_TO` — The `Event(s)` that trigger the protocol.
  - `compute` — The method that handles the Event and returns a list of Effects.

- Instance attributes available to protocol authors:
  - `self.event` — The `Event` instance.
  - `self.secrets` — Secrets provided to the protocol (defaults to {}).
  - `self.environment` — Environment values (defaults to {}).

### Example

```python
from canvas_sdk.protocols.base import BaseProtocol
from canvas_sdk.events import EventType
from canvas_sdk.effects.task import AddTask

class SimpleFollowUpProtocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.IMAGING_REPORT_CREATED)

    def compute(self):
        # Use self.event, self.secrets, and self.environment
        patient_id = self.event.context["patient"]["id"]
        imaging_report_id = self.event.target["id"]

        # Create a follow-up task effect
        return [AddTask(patient_id=patient_id, title="Follow-up", linked_object_type=AddTask.LinkableObjectType.IMAGING, linked_object_id=imaging_report_id).apply()]
```

## ClinicalQualityMeasure

`ClinicalQualityMeasure` is the base class for clinical quality measure (CQM) protocols. CQMs are patient-centric protocols used to evaluate, detect, or surface clinical conditions, gaps in care, and population-level metrics. Plugin authors create concrete subclasses that implement the clinical logic and return Effects in response to incoming Events.

### Meta properties

Subclasses should populate the `Meta` inner class. Common meta fields include:

- `title` (str): Human-readable title for the protocol.
- `identifiers` (list[str]): One or more external identifiers for the measure (for example, CMS/QDM ids).
- `description` (str): A short description of what the measure evaluates.
- `information` (str): Longer contextual information or rationale.
- `references` (list[str]): Links or identifiers for authoritative references.
- `source_attributes` (dict[str, str]): Map of attribute names used by the protocol to source fields on data models.
- `types` (list[str]): Tags or classification strings for the measure.
- `authors` (list[str]): Authors or maintainers of the protocol.
- `show_in_chart`, `show_in_population`, `can_be_snoozed` (bool): UI/behavior flags.
- `is_abstract`, `is_predictive` (bool): Behavioral flags for the framework.

The `ClinicalQualityMeasure._meta()` classmethod merges the base `Meta` and subclass `Meta` into a single dictionary that is used by the framework for display and routing.

### Key methods

- `timeframe` (property) -> `Timeframe`

  - Provides the default timeframe used by the protocol when searching for relevant events or records. The default implementation returns a timeframe with a start one year before now and an end at the current time. Subclasses can override this property to adjust the window of interest.

- `relative_float(value: str) -> float`

  - Parses comparison-style numeric strings that may include relational prefixes like `<`, `<=`, `>` or `>=`. Returns a float adjusted slightly (±1e-6) for strict `<` or `>` operators so comparisons can be expressed without ambiguity. If parsing fails, returns `0`.

- `patient_id_from_target()` -> str
  - Extracts and caches the patient id from a protocol event target for supported event types. The method supports a variety of patient-centric event targets (Conditions, LabOrders, LabReports, Medications, Patient create/update events, and ProtocolOverride events). The first call will fetch and cache the patient id to avoid repeated DB lookups. If an unsupported event type is provided a `ValueError` is raised.

### Example — react to a lab report

This example shows a protocol that reacts to `LAB_REPORT_CREATED` events, uses `patient_id_from_target` to determine which patient the report belongs to, and emits an Effect when a particular lab value is out of range. Note the example avoids heavy synchronous DB work and emits an Effect for the platform to handle asynchronously.

```python
from canvas_sdk.events import EventType
from canvas_sdk.effects.task import AddTask
from datetime import datetime

class AbnormalPotassiumMeasure(ClinicalQualityMeasure):
    class Meta:
        title = "Abnormal Potassium Alert"
        identifiers = ["CQM-K-001"]
        description = "Creates a task when a potassium lab report shows hypokalemia or hyperkalemia."
        information = "Detects clinically significant potassium abnormalities and surfaces follow-up tasks."
        references = ["https://example.org/guideline/potassium"]
        source_attributes = {"reported_at": "https://example.org/guideline/potassium"}
        types = ["electrolyte", "urgent"]
        authors = ["Clinical Team"]
        show_in_chart = True
        show_in_population = True
        can_be_snoozed = False
        is_abstract = False
        is_predictive = False

    RESPONDS_TO = EventType.Name(EventType.LAB_REPORT_CREATED)

    def compute(self):
        # Resolve patient id (cached on first call)
        patient_id = self.patient_id_from_target()

        # Read the lab report values from the event target (avoid extra DB queries here)
        report = self.event.target
        potassium_value = report.get_value('potassium')  # simplified accessor

        # Use relative_float to safely parse any comparator-style values
        k = self.relative_float(str(potassium_value))

        if k < 3.5 or k > 5.5:
            # Emit an effect — e.g., send an alert or create a task. Keep heavy work to platform handlers.
            return [AddTask(patient_id=patient_id, title=f"Abnormal potassium: {k}", due=datetime.now()).apply()]

        return []

```

### Caveats & notes

- Timeframe: by default the protocol looks at the 1-year window prior to now. Override `timeframe` if your measure requires a broader or narrower lookback.
- patient id resolution: `patient_id_from_target()` supports only the event types enumerated by the implementation; verify the event you plan to subscribe to maps to a supported model. When used heavily, this method avoids extra DB queries by caching the patient id on the instance.
- Event-driven protocols should avoid expensive synchronous DB operations inside their event handler. When possible, emit Effects that are handled asynchronously by the platform.
