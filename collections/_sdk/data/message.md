---
title: "Message"
slug: "data-message"
excerpt: "Data models for messaging functionality in the Canvas SDK"
hidden: false
---

# Message Models

The Canvas SDK defines messaging-related data models for sending, receiving, and tracking messages.

## TransmissionChannel

A `TextChoices` enum representing the available channels for transmitting messages.

| Member         | Value    | Description    |
|----------------|----------|----------------|
| `MANUAL`       | `manual` | Manual         |
| `TEXT_MESSAGE` | `sms`    | Text Message   |
| `EMAIL`        | `email`  | Email          |
| `NOOP`         | `noop`   | No-op          |

## Message

Represents an individual message record.

### Fields

| Name        | Type                     | Description                                                   |
|-------------|--------------------------|---------------------------------------------------------------|
| `id`        | `UUIDField`              | Unique identifier for the message.                           |
| `dbid`      | `BigIntegerField`        | Database primary key.                                         |
| `created`   | `DateTimeField`          | Timestamp when the message was created.                       |
| `modified`  | `DateTimeField`          | Timestamp when the message was last modified.                 |
| `content`   | `TextField`              | The body text of the message.                                |
| `sender`    | `ForeignKey(CanvasUser)` | The user who sent the message. May be null.                   |
| `recipient` | `ForeignKey(CanvasUser)` | The user who received the message. May be null.               |
| `note`      | `ForeignKey(Note)`       | Associated note (if any) for contextual linkage. May be null. |
| `read`      | `BooleanField`           | Indicates whether the recipient has read the message.         |

## MessageAttachment

Represents a file attachment linked to a message.

### Fields

| Name           | Type                        | Description                                |
|----------------|-----------------------------|--------------------------------------------|
| `id`           | `UUIDField`                 | Unique identifier for the attachment.      |
| `dbid`         | `BigIntegerField`           | Database primary key.                      |
| `file`         | `TextField`                 | Storage path or identifier for the file.   |
| `content_type` | `CharField(max_length=255)` | MIME type of the attachment.               |
| `message`      | `ForeignKey(Message)`       | The parent message to which this belongs.  |

## MessageTransmission

Tracks delivery attempts and status for a message.

### Fields

| Name                  | Type                                     | Description                                                    |
|-----------------------|------------------------------------------|----------------------------------------------------------------|
| `id`                  | `UUIDField`                              | Unique identifier for the transmission record.                 |
| `dbid`                | `BigIntegerField`                        | Database primary key.                                          |
| `created`             | `DateTimeField`                          | Timestamp when the transmission was created.                   |
| `modified`            | `DateTimeField`                          | Timestamp when the transmission was last modified.             |
| `message`             | `ForeignKey(Message)`                    | The message associated with this transmission.                 |
| `delivered`           | `BooleanField`                           | Whether delivery was successful.                               |
| `failed`              | `BooleanField`                           | Whether delivery failed.                                       |
| `contact_point_system`| `CharField(choices=TransmissionChannel)` | The channel used for delivery.                       |
| `contact_point_value` | `CharField(max_length=255)`              | The destination address or identifier (e.g., phone, email).    |
| `comment`             | `TextField`                              | Optional comments or error details.                            |
| `delivered_by`        | `ForeignKey(Staff)`                      | The staff member who processed the delivery. May be null.      |
