---
title: "Automating Note and Billing Workflows"
guide_for:
- /sdk/events/
- /sdk/effects/
- /sdk/handlers/
- /sdk/data-claim/
---

<!-- sources: discussions #1354, #1250, #1101, #1009 -->

Plugins can react to clinical and administrative events on notes and automate steps that staff would otherwise do by hand: carrying commands forward to a new note, reassigning a note based on the payer, attaching billing line items to a diagnosis, and notifying an external system when a note is locked. This guide collects several event-driven patterns that share the same shape — listen for an event, read the relevant data, return an effect.

## Carrying commands forward to a new note

When a command is created or deleted, the event context already carries the data you need — you usually do not have to query the database. For example, to restore a Diagnose command after it is deleted (and re-apply the same code the user had selected), listen for `DIAGNOSE_COMMAND__POST_DELETE` and read the code straight from the context.

On a Diagnose delete, `self.context['fields']` looks like this:

```python
{
    'diagnose': {
        'text': 'Malignant neoplasm of abdomen',
        'extra': {
            'coding': [
                {'code': 'C762', 'system': 'ICD-10', 'display': 'Malignant neoplasm of abdomen'},
                {'code': 188366002, 'system': 'http://snomed.info/sct', 'display': 'Malignant neoplasm of abdomen'},
            ],
        },
        'value': 'C762',
        'disabled': False,
        'annotations': ['C76.2', 'HCC'],
        'description': None,
    },
    'background': '',
    'today_assessment': '',
    'approximate_date_of_onset': None,
}
```

The selected ICD-10 code is at `self.context['fields']['diagnose']['value']`. That makes the handler simple:

```python
from canvas_sdk.commands.commands.diagnose import DiagnoseCommand
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from logger import log


class HandleDiagnoseCommandDelete(BaseProtocol):
    """Adds a Diagnose command back if it is deleted."""

    RESPONDS_TO = [
        EventType.Name(EventType.DIAGNOSE_COMMAND__POST_DELETE),
    ]

    def compute(self) -> list[Effect]:
        note_id = self.context.get("note", {}).get("uuid")
        patient_id = self.context.get("patient", {}).get("id")

        diagnose_command = DiagnoseCommand(note_uuid=note_id)

        try:
            icd10_code = self.context.get("fields", {}).get("diagnose", {}).get("value")
            if icd10_code:
                log.info(f"restoring diagnose command with code: {icd10_code}")
                diagnose_command.icd10_code = icd10_code
            else:
                log.info(f"no code found for patient: {patient_id}, restoring command without code")
        except Exception as e:
            log.info(f"Failed to find icd10 code for patient: {patient_id}, error: {e}")

        return [diagnose_command.originate()]
```

The general pattern for a "carry forward" plugin is to read a `Command.data` attribute (or, as above, the context fields) and originate a duplicate command with the same data. You do not always want to carry every command forward verbatim — sometimes you want to advance it to the next stage instead (for example, carrying a prior Diagnose forward as an Assess of that condition rather than duplicating the diagnosis). For a fuller worked example, see the Medical Software Foundation [carry-forward extension](https://github.com/Medical-Software-Foundation/canvas/tree/action-button-examples-for-developer-support/extensions/carry-forward).

## Reassigning a note based on the payer

You can detect the payer associated with a note and reassign the note to a different provider (for example, a supervisor). When a billable note type is created, Canvas automatically creates a [Claim](/sdk/data-claim/) for the appointment/note, and that claim carries the payer information.

Listen for both `APPOINTMENT_CREATED` and `NOTE_STATE_CHANGE_EVENT_CREATED`, find the associated claim, check the payer against your rules, and return a [Note](/sdk/effect-notes/) or [Appointment](/sdk/effect-appointments/) effect that updates the provider.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.note import Appointment as AppointmentEffect, Note as NoteEffect
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.v1.data import (
    Appointment as AppointmentModel,
    Claim,
    Note as NoteModel,
    Staff,
)


class Protocol(BaseProtocol):
    """Detect the payer for a new note and re-assign the provider."""

    RESPONDS_TO = [
        EventType.Name(EventType.NOTE_STATE_CHANGE_EVENT_CREATED),
        EventType.Name(EventType.APPOINTMENT_CREATED),
    ]

    def handle_note_create(self) -> list[Effect]:
        if self.event.context["state"] != "NEW":
            return []
        note_model = NoteModel.objects.get(id=self.event.context["note_id"])
        claim = note_model.get_claim()
        if not claim:
            return []
        return self.update_provider(claim)

    def handle_appointment_create(self) -> list[Effect]:
        appointment_model = AppointmentModel.objects.get(id=self.event.target.id)
        note_model = appointment_model.note
        if not note_model or not (claim := note_model.get_claim()):
            return []
        return self.update_provider(claim)

    def update_provider(self, claim: Claim) -> list[Effect]:
        if claim.current_coverage.payer_id == "J4054":
            # Replace with whatever payer logic you need. You can also look up
            # more about the payer from the Transactor model.
            new_provider = Staff.objects.filter(first_name="Andrew").first()
            Effect = AppointmentEffect if self.is_appointment else NoteEffect
            effect = Effect(instance_id=self.event.target.id, provider_id=new_provider.id)
            return [effect.update()]
        return []

    def compute(self) -> list[Effect]:
        if self.event.type == EventType.NOTE_STATE_CHANGE_EVENT_CREATED:
            self.is_appointment = False
            return self.handle_note_create()

        if self.event.type == EventType.APPOINTMENT_CREATED:
            self.is_appointment = True
            return self.handle_appointment_create()

        return []
```

The payer information lives on the claim's [`current_coverage`](/sdk/data-claim/#claimcoverage); for additional payer detail you can read the [`Transactor`](/sdk/data-coverage/#transactor) model.

## Attaching a billing line item to a diagnosis

<!-- REVIEW: clinical-accuracy sign-off required -->

You can automate billing for specific note types — for instance, adding a diagnosis and an associated billing line item when an intake note is created. The key detail is that a billing line item is linked to a diagnosis through its **Assessment**, and the Assessment ID only exists once the Diagnose command has been **committed**. Passing the command UUID as the assessment ID will not work; the assessment must come from the committed diagnosis.

Split the work into two handlers. First, originate and commit the diagnosis when the note is created:

```python
from uuid import uuid4

from canvas_sdk.commands import DiagnoseCommand
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.v1.data import Encounter


class IntakeCreatedProtocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.ENCOUNTER_CREATED)

    def compute(self) -> list[Effect]:
        encounter = Encounter.objects.get(id=self.event.target.id)
        note = encounter.note

        # Verify the note type is approved for this workflow before proceeding.

        diagnose_command = DiagnoseCommand(note_uuid=str(note.id), icd10_code="Z13.41")
        diagnose_command.command_uuid = str(uuid4())

        return [diagnose_command.originate(), diagnose_command.commit()]
```

Then, in a second handler, listen for `DIAGNOSE_COMMAND__POST_COMMIT`, retrieve the diagnosis (the command's `anchor_object`), confirm it is the diagnosis you care about, and attach the billing line item using the latest assessment's ID:

```python
from canvas_sdk.commands.constants import CodeSystems
from canvas_sdk.effects import Effect
from canvas_sdk.effects.billing_line_item import AddBillingLineItem
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.v1.data.command import Command


class AddBillingLineItemToAutismDiagnoses(BaseHandler):

    RESPONDS_TO = EventType.Name(EventType.DIAGNOSE_COMMAND__POST_COMMIT)

    def compute(self) -> list[Effect]:
        command = Command.objects.get(id=self.event.target.id)

        diagnosis = command.anchor_object
        icd_10_coding = diagnosis.codings.filter(system=CodeSystems.ICD10).first()
        if icd_10_coding.code.replace(".", "") != "Z1341":
            return []
        note = command.note

        latest_assessment = diagnosis.assessments.last()

        b = AddBillingLineItem(
            note_id=str(note.id),
            cpt="AUTISM_DX",
            assessment_ids=[str(latest_assessment.id)],
        )
        return [b.apply()]
```

In this example the ICD-10 code `Z13.41` and CPT `AUTISM_DX` are placeholders from the originating discussion — substitute the codes and fee schedule entries your workflow requires, and confirm code selection with your clinical and billing teams.

## Triggering an external transfer when a note is locked

To push data to an external system when a provider locks a note, build a [webhook plugin](/guides/creating-webhooks-with-the-canvas-sdk/) that listens for `NOTE_STATE_CHANGE_EVENT_CREATED` and checks for the lock state. A note lock is the state `'LKD'`; ignore other states (see the full list of [note states](/sdk/data-note/#notestates)).

Read `note_id` and `patient_id` from the context, fetch the data you want to send from the FHIR API (which returns FHIR-shaped JSON), and forward it to your endpoint. Use the [`Http`](/sdk/utils/) util for the requests and store credentials in [secrets](/sdk/secrets/) rather than in plaintext.

```python
from urllib.parse import urlencode

from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.utils import Http
from logger import log


class Protocol(BaseProtocol):
    """When a note is locked, fetch FHIR data and notify an external endpoint."""

    RESPONDS_TO = EventType.Name(EventType.NOTE_STATE_CHANGE_EVENT_CREATED)

    def compute(self):
        # Ignore any note state change that is not a lock.
        if self.event.context["state"] != "LKD":
            return []

        note_id = str(self.event.context["note_id"])
        patient_id = str(self.event.context["patient_id"])

        http = Http()

        # Get a bearer token using your OAuth client credentials.
        payload = urlencode(
            {
                "grant_type": "client_credentials",
                "client_id": self.secrets["CLIENT_ID"],
                "client_secret": self.secrets["CLIENT_SECRET"],
            }
        )
        bearer_token = http.post(
            "your-canvas-ehr-instance/auth/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=payload,
        )
        headers = {"Authorization": f"Bearer {bearer_token}"}

        # Read the FHIR Patient and Encounter resources.
        patient_fhir_data = http.get(
            f"https://fumage-example.canvasmedical.com/Patient/{patient_id}", headers=headers
        )
        encounter_fhir_data = http.get(
            f"https://fumage-example.canvasmedical.com/Encounter/{note_id}", headers=headers
        )

        # Forward the payload to your secure endpoint.
        response = http.post(
            "your-secure-api-gateway-address",
            json={"patient": patient_fhir_data, "encounter": encounter_fhir_data},
            headers={"Authorization": f"Bearer {self.secrets['AUTH_TOKEN']}"},
        )

        if response.ok:
            log.info("Successfully notified API of note lock!")
        else:
            log.info("Notification unsuccessful.")

        return []
```

This pattern runs entirely inside the Canvas environment — there is no need to host a separate EC2 service to react to the lock. See the [Patient read](/api/patient/#read) and [Encounter read](/api/encounter/#read) API references for the resources you can pull. Note that the `note_id` in the plugin context is not necessarily the identifier the Encounter endpoint expects; confirm the right Encounter identifier for your instance before relying on it.
