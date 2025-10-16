---
title: "Message Effect"
slug: "effect-messages"
excerpt: "Effect for creating, editing, and sending messages."
hidden: false
---

# Message Effect

The `Message` effect provides a unified way to create, edit, and transmit messages between users (patients or staff)
within the Canvas platform.
It supports standalone creation, immediate send after creating, edits, and dedicated send operations.

## Attributes

| Name           | Type                      | Description                                                                                                 |
|----------------|---------------------------|-------------------------------------------------------------------------------------------------------------|
| `message_id`   | `str` or `UUID` or `None` | Unique identifier of an existing message. Must be unset when creating a new message; required when editing. |
| `content`      | `str` or `None`           | The text body of the message. Required when creating; cannot be empty.                                      |
| `sender_id`    | `str` or `UUID`           | ID of the user (Patient or Staff) who is sending the message.                                               |
| `recipient_id` | `str` or `UUID`           | ID of the user (Patient or Staff) who will receive the message.                                             |
| `read`         | `datetime` or `None`      | Timestamp indicating when the message was read by the recipient. Defaults to `None` (unread).               |

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
- **No Attachments Supported:** The Message effect does not yet support attachments.
- **Immediate Post for Patient-to-Staff:** Messages created from a Patient to Staff cannot be drafted and will immediately appear in the timeline. This means that `CREATE_AND_SEND` and `SEND` effects will fail in these scenarios. You should only use the `CREATE` method for Patient-to-Staff messaging.


## Effect Methods

### `create()`

Originate a new message record without sending.

- **Effect Type:** `CREATE_MESSAGE`
- **Payload:** `{ "data": { content, sender_id, recipient_id } }`

### `create_and_send()`

Create the message and immediately send it in one operation.

- **Effect Type:** `CREATE_AND_SEND_MESSAGE`
- **Payload:** `{ "data": { content, sender_id, recipient_id } }`

### `edit()`

Modify an existing message’s content.

- **Effect Type:** `EDIT_MESSAGE`
- **Payload:** `{ "data": { message_id, content?, sender_id?, recipient_id? } }`
- Only fields marked dirty (modified on the model) are included; unchanged fields remain intact in the system.

### `send()`

Send an already-created message. Useful if you separated creation from transmission.

- **Effect Type:** `SEND_MESSAGE`
- **Payload:** `{ "data": { message_id } }`

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
