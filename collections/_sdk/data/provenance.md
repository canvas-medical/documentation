---
title: "Provenance"
slug: "data-provenance"
excerpt: "Who created or updated a clinical record, and when."
hidden: false
---

## Introduction

The `Provenance` model records who created or updated a patient's clinical record, and when. Canvas writes a provenance record each time it saves a record of one of these types:

- AllergyIntolerance
- CarePlan
- CareTeamMembership
- Condition
- ConsolidatedImmunization
- Coverage
- Device
- DiagnosticReport
- DocumentReference
- Encounter
- Goal
- Observation
- Patient
- Prescription
- Procedure
- ServiceRequest
- UpdateGoal

These are the same records the [FHIR Provenance API](/api/provenance/) returns. Read them from a plugin to build an audit trail for a patient's chart, or to find who last changed a record.

## Basic usage

To get a provenance record by identifier, use the `get` method on the `Provenance` model manager:

```python
from canvas_sdk.v1.data import Provenance

provenance = Provenance.objects.get(id="5b6f2c1e-8d3a-4f7b-9e21-0c4d8a6b3f10")
```

If you have a patient object, the patient's provenance records are available through the `provenance_set` attribute:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
provenance_records = patient.provenance_set.order_by("-occurred_date_time")
```

## Targets, agents, and on-behalf-of

A provenance record points at three other records, each as a [content type](/sdk/data-content-type/) and a database id rather than as a related object:

- **Target**: the record that was created or updated, in `target_object_type` and `target_object_id`.
- **Agent**: who made the change, in `agent_object_type` and `agent_object_id`. The agent is the [Staff](/sdk/data-staff/), [Patient](/sdk/data-patient/), or [PatientContactPerson](/sdk/data-patient/#patientcontactperson) record of the user who committed the target record, or of the user who created it when it has no committer. Its `agent_participation_type` is `author`. When that user has no such record on the patient's chart, the agent is the Canvas [OrganizationalEntity](/sdk/data-organizational-entity/) and `agent_participation_type` is `composer`.
- **On behalf of**: the organization the change was made for, in `on_behalf_of_object_type` and `on_behalf_of_object_id`. Canvas sets this to the Canvas organizational entity.

The ids are the `dbid` of the linked record. To find a record's history, look up its content type by `app_label` and `model`, then filter on the target:

```python
from canvas_sdk.v1.data import ContentType, Provenance, Staff
from canvas_sdk.v1.data.condition import Condition
from logger import log

condition = Condition.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
condition_type = ContentType.objects.get(app_label="api", model="condition")

history = Provenance.objects.filter(
    target_object_type=condition_type,
    target_object_id=condition.dbid,
).select_related("agent_object_type").order_by("occurred_date_time")

for provenance in history:
    who = "Canvas"
    if provenance.agent_object_type and provenance.agent_object_type.model == "staff":
        staff = Staff.objects.filter(dbid=provenance.agent_object_id).first()
        who = staff.full_name if staff else "unknown staff member"
    log.info(f"{provenance.occurred_date_time}: {provenance.action} by {who}")
```

## Filtering

Provenance records can be filtered by any attribute that exists on the model, with the `filter` method on the `Provenance` model manager:

```python
from canvas_sdk.v1.data import Provenance

updates = Provenance.objects.filter(
    patient__id="1eed3ea2a8d546a1b681a2a45de1d790",
    action="update",
)
```

## Attributes

### Provenance

| Field Name               | Type                                                    | Description |
|--------------------------|---------------------------------------------------------|-------------|
| id                       | UUID                                                    |             |
| dbid                     | Integer                                                 |             |
| created                  | DateTime                                                |             |
| modified                 | DateTime                                                |             |
| patient                  | [Patient](/sdk/data-patient/#patient)                   |             |
| action                   | String                                                  | `create` or `update` |
| occurred_date_time       | DateTime                                                | When the target record was saved |
| target_object_type       | [ContentType](/sdk/data-content-type/)                  | The content type of the record that changed |
| target_object_id         | Integer                                                 | The `dbid` of the record that changed |
| agent_object_type        | [ContentType](/sdk/data-content-type/)                  | The content type of the agent |
| agent_object_id          | Integer                                                 | The `dbid` of the agent |
| agent_participation_type | [ProvenanceParticipantType](#provenanceparticipanttype) | How the agent took part |
| on_behalf_of_object_type | [ContentType](/sdk/data-content-type/)                  | The content type of the organization the change was made for |
| on_behalf_of_object_id   | Integer                                                 | The `dbid` of the organization the change was made for |

## Enumeration types

### ProvenanceParticipantType

| Value         | Label               |
|---------------|---------------------|
| `enterer`     | Enterer             |
| `performer`   | Performer           |
| `author`      | Author              |
| `verifier`    | Verifier            |
| `legal`       | Legal Authenticator |
| `attester`    | Attester            |
| `informant`   | Informant           |
| `custodian`   | Custodian           |
| `assembler`   | Assembler           |
| `composer`    | Composer            |
| `transmitter` | Transmitter         |

<br/>
<br/>
<br/>
