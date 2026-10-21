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

## Methods

### create() → Effect

Creates a message without sending it.

- `content`, `sender_id`, and `recipient_id` are required, and `content` cannot be empty.
- `message_id` must not be set.

### create_and_send() → Effect

Creates the message and sends it in one operation.

- `content`, `sender_id`, and `recipient_id` are required, and `content` cannot be empty.
- `message_id` must not be set.
- When the recipient is a patient, the patient needs an eligible contact point. See [Sending to a patient](#sending-to-a-patient).

### edit() → Effect

Changes an existing message.

- `message_id` is required, and must be the id of an existing message.
- Only the attributes you set on the effect are changed. Attributes you leave unset keep their current values.
- `attachment_upload_keys` adds files to the message, and can be the only attribute you set. A locked message can't take new files. See [Attaching files](#attaching-files).

### send() → Effect

Sends a message that was already created, if you separated creating it from sending it.

- Set `message_id` to the message to send.
- `attachment_upload_keys` must not be set. Attach files with `create()`, `create_and_send()`, or `edit()` before sending.
- When the recipient is a patient, the patient needs an eligible contact point. See [Sending to a patient](#sending-to-a-patient).

## Attaching files

To attach files to a message, set `attachment_upload_keys` to a list of upload keys. Each key is the `key` of a `StoredFilePart` that a user uploaded to your plugin through a SimpleAPI route declared with `file_uploads="stored"`. See [Storing uploaded files](/sdk/handlers-simple-api-http/#storing-uploaded-files).

Attachments can be PNG, JPEG, or PDF files. When the effect is applied, Canvas checks that each key is a file your plugin uploaded and that the file is one of these types. It adds the files in the same transaction as the message, before the message is sent. Canvas then deletes the uploads, so each key works only once.

This SimpleAPI route sends the files in a `multipart/form-data` request to a patient, from the logged-in staff member:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.note.message import Message
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import SessionCredentials, SimpleAPI, api


class SendFilesAPI(SimpleAPI):
    def authenticate(self, credentials: SessionCredentials) -> bool:
        return credentials.logged_in_user["type"] == "Staff"

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

## Validation & Errors

Before any effect is emitted, the model runs these checks:

- **Sender and Recipient Exist**
  Verifies that both `sender_id` and `recipient_id` belong to either a `Patient` or a `Staff` record.
- **Create vs. Edit Constraints**
  - **Create** and **Create-and-Send** must **not** include `message_id`.
  - **Create** and **Create-and-Send** must include non-empty `content` (content cannot be blank or whitespace-only).
  - **Edit** operations **must** include a valid `message_id` that already exists in the database.

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

<br/>
<br/>
<br/>