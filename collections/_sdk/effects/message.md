---
title: "Message Effect"
slug: "effect-messages"
excerpt: "Effect for creating, editing, and sending messages."
hidden: false
---

The `Message` effect provides a unified way to create, edit, and transmit messages between users (patients or staff)
within the Canvas platform.
It supports standalone creation, immediate send after creating, edits, and dedicated send operations.

Build a `Message` with the [attributes](#attributes) you want to set, then return one of its methods from your handler: `create()`, `create_and_send()`, `edit()`, or `send()`.

To route a message to a group of staff rather than one person, assign it to a team. See [Assigning a message to a team](#assigning-a-message-to-a-team).

## Methods

### create() → Effect

Creates a message without sending it.

- `content`, `sender_id`, and `recipient_id` are required, and `content` cannot be empty.
- `message_id` must not be set.
- `team_id` is optional. Set it to create the message already assigned to a team.

### create_and_send() → Effect

Creates the message and sends it in one operation.

- `content`, `sender_id`, and `recipient_id` are required, and `content` cannot be empty.
- `message_id` must not be set.
- `team_id` is optional. Set it to create the message already assigned to a team.
- When the recipient is a patient, the patient needs an eligible contact point. See [Sending to a patient](#sending-to-a-patient).

### edit() → Effect

Changes an existing message.

- `message_id` is required, and must be the id of an existing message.
- Only the attributes you set on the effect are changed. Attributes you leave unset keep their current values.
- `attachment_upload_keys` adds files to the message, and can be the only attribute you set. A locked message can't take new files. See [Attaching files](#attaching-files).
- `team_id` must not be set. Editing a message keeps its team. To change the team, use [`AssignMessageTeam`](#assigning-a-message-to-a-team).
- For a message a family member sent through [family portal access](/sdk/patient-portal/#family-portal-access), set `sender_id` to the patient whose chart the message is filed on. The family member stays the message's sender.

### send() → Effect

Sends a message that was already created, if you separated creating it from sending it.

- Set `message_id` to the message to send.
- `attachment_upload_keys` must not be set. Attach files with `create()`, `create_and_send()`, or `edit()` before sending.
- `team_id` must not be set. Use [`AssignMessageTeam`](#assigning-a-message-to-a-team) to change the team.
- When the recipient is a patient, the patient needs an eligible contact point. See [Sending to a patient](#sending-to-a-patient).

## Attaching files

To attach files to a message, set `attachment_upload_keys` to a list of upload keys. Each key is the `key` of a `StoredFilePart` that a user uploaded to your plugin through a SimpleAPI route declared with `file_uploads="stored"`. See [Storing uploaded files](/sdk/handlers-simple-api-http/#storing-uploaded-files).

Attachments can be PNG, JPEG, or PDF files, and each key must come from a file your plugin uploaded. When the effect is applied, Canvas adds the files in the same transaction as the message, before the message is sent. Canvas then deletes the uploads, so each key works only once.

This SimpleAPI route sends the files in a `multipart/form-data` request to a patient, from the logged-in staff member:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.note.message import Message
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import SimpleAPI, StaffSessionAuthMixin, api


class SendFilesAPI(StaffSessionAuthMixin, SimpleAPI):
    @api.post("/send-files", file_uploads="stored")
    def send_files(self) -> list[Response | Effect]:
        form = self.request.form_data()
        message = Message(
            content="Here is the form we discussed.",
            sender_id=self.request.headers["canvas-logged-in-user-id"],
            recipient_id=form["patient_id"].value,
            attachment_upload_keys=[part.key for part in form.get_list("files") if not part.error],
        )
        return [message.create_and_send(), JSONResponse({})]
```

To read a message's attachments, see [MessageAttachment](/sdk/data-message/#messageattachment).

## Sending to a patient

When `create_and_send()` or `send()` sends a message to a patient, Canvas notifies the patient the same way it does for a message sent from the chart: a text message or email to each of the patient's phone numbers and email addresses that is eligible. A contact point is eligible when all three of these are true:

- `has_consent` is `True`
- `last_verified` is set
- `state` is `"active"`

If the patient has no eligible contact point, Canvas cannot deliver the message. The message is saved but not sent, it appears as a draft in the patient's chart, and the effect fails.

To avoid this, check the patient's [contact points](/sdk/data-patient/#patientcontactpoint) before sending, and use `create()` instead when none is eligible:

```python?partial=true
has_eligible_contact = patient.telecom.filter(
    has_consent=True,
    last_verified__isnull=False,
    state="active",
).exists()

message = Message(content=content, sender_id=staff.id, recipient_id=patient.id)
effect = message.create_and_send() if has_eligible_contact else message.create()
```

Instances set up to deliver patient messages through a plugin, rather than through Canvas, do not send these notifications.

`create()` on its own never notifies the patient.

## Attributes

| Attribute      | Type                      | Description                                                                                   | Required |
|----------------|---------------------------|-----------------------------------------------------------------------------------------------|----------|
| `message_id`   | `str` or `UUID` or `None` | Unique identifier of an existing message. Must be unset when creating a new message.          | For `edit()` and `send()` |
| `content`      | `str` or `None`           | The text body of the message. Cannot be empty.                                                | For `create()` and `create_and_send()` |
| `sender_id`    | `str` or `UUID`           | ID of the user (Patient or Staff) who is sending the message.                                 | Yes      |
| `recipient_id` | `str` or `UUID`           | ID of the user (Patient or Staff) who will receive the message.                               | Yes      |
| `read`         | `datetime` or `None`      | Timestamp indicating when the message was read by the recipient. Defaults to `None` (unread). | No       |
| `attachment_upload_keys` | `list[str]` or `None` | Upload keys of PNG, JPEG, or PDF files to attach. Not allowed with `send()`. See [Attaching files](#attaching-files). | No |
| `team_id`      | `str` or `UUID` or `None` | ID of the [team](/sdk/data-team/) to assign the new message to. Not allowed with `edit()` or `send()`. See [Assigning a message to a team](#assigning-a-message-to-a-team). | No |

## Validation & Errors

Before any effect is emitted, the model runs these checks:

- **Sender and Recipient Exist**
  Verifies that both `sender_id` and `recipient_id` belong to either a `Patient` or a `Staff` record.
- **Create vs. Edit Constraints**
  - **Create** and **Create-and-Send** must **not** include `message_id`.
  - **Create** and **Create-and-Send** must include non-empty `content` (content cannot be blank or whitespace-only).
  - **Edit** operations **must** include a valid `message_id` that already exists in the database.
- **Team Exists**
  When `create()` or `create_and_send()` sets `team_id`, it must be the id of an existing team. `edit()` and `send()` reject `team_id`.

## Caveats

- **Role Constraints:** Sender and Recipient must always be one of Patient or Staff. Patient-to-Patient messaging is not allowed.
- **UI Refresh Required:** Due to system constraints, editing a message requires a manual UI refresh for updated content to display.
- **Immediate Post for Patient-to-Staff:** Messages created from a Patient to Staff cannot be drafted and will immediately appear in the timeline. This means that `CREATE_AND_SEND` and `SEND` effects will fail in these scenarios. You should only use the `CREATE` method for Patient-to-Staff messaging.


## Example Usage

```python
from canvas_sdk.v1.data.message import Message as MessageModel
from canvas_sdk.v1.data.patient import Patient
from canvas_sdk.v1.data.staff import Staff

from canvas_sdk.effects.note.message import Message

staff = Staff.objects.first()
patient = Patient.objects.first()
```

### Create (originate) only

```python?partial=True
m1 = Message(
    content="Your lab results are available.",
    sender_id=staff.id,
    recipient_id=patient.id
)
effect_create = m1.create()
```

### Create and send in one step

```python?partial=True
m2 = Message(
    content="Your appointment is confirmed.",
    sender_id=staff.id,
    recipient_id=patient.id
)
effect_create_and_send = m2.create_and_send()

m = MessageModel.objects.get(message_id="msg-1234")
```

### Edit an existing message

```python?partial=True
m3 = Message(
    message_id=m.id,
    content="Updated: Your appointment has moved to 3pm."
)
effect_edit = m3.edit()
```

### Send an existing message

```python?partial=True
m4 = Message(message_id=m.id)
effect_send = m4.send()
```

## Assigning a message to a team

A message always has one staff or patient `recipient`. It can also be assigned to a [team](/sdk/data-team/), so a group such as a front desk or a care team can work messages together. Assigning a team does not change the `recipient`. In the global Messages panel, the assignee filter defaults to **Me or my teams**, so staff see messages addressed to them and messages assigned to any of their teams, and the unread badge counts both. A message has a single read timestamp, so when one team member reads a team message, it is read for the whole team.

There are two ways to assign a team:

- Set `team_id` when you create the message with `create()` or `create_and_send()`.
- Return an `AssignMessageTeam` effect to set, change, or clear the team of an existing message.

### AssignMessageTeam

Build an `AssignMessageTeam` and return its `apply()` from your handler.

#### Methods

##### apply() → Effect

Sets, changes, or clears the team of an existing message.

- `message_id` is required, and must be the id of an existing message.
- `team_id` is required. Set it to `None` to unassign the message.
- The effect fails validation, and the message keeps its current team, when either id is not a valid UUID or does not match an existing message or team.
- Each assignment, reassignment, and unassignment emits the [`MESSAGE_TEAM_ASSIGNED`](/sdk/events/#messaging) event. Creating a message with a team emits it too.

#### Attributes

| Attribute    | Type                      | Description                                                         | Required |
|--------------|---------------------------|---------------------------------------------------------------------|----------|
| `message_id` | `str` or `UUID`           | ID of the [message](/sdk/data-message/#message) to assign.          | Yes      |
| `team_id`    | `str` or `UUID` or `None` | ID of the [team](/sdk/data-team/) to assign the message to, or `None` to unassign it. | Yes      |

#### Example

This handler assigns each message a patient sends to the team named "Front Desk":

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.note.message import AssignMessageTeam
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.v1.data import Message, Team


class RoutePatientMessages(BaseHandler):
    """Assign messages that patients send to the Front Desk team."""

    RESPONDS_TO = EventType.Name(EventType.MESSAGE_CREATED)

    def compute(self) -> list[Effect]:
        message = Message.objects.select_related("sender").filter(id=self.target).first()

        # Only route messages a patient sent, not messages staff sent to a patient.
        if message is None or message.sender is None or message.sender.is_staff:
            return []

        team = Team.objects.filter(name="Front Desk").first()
        if team is None:
            return []

        return [AssignMessageTeam(message_id=message.id, team_id=team.id).apply()]
```

<br/>
<br/>
<br/>