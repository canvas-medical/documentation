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

| Name        | Type                                      | Description                                                    |
|-------------|-------------------------------------------|----------------------------------------------------------------|
| `id`        | `UUID`                                    | Unique identifier for the message.                             |
| `dbid`      | `Integer`                                 | Database primary key.                                          |
| `created`   | `DateTime`                                | Timestamp when the message was created.                        |
| `modified`  | `DateTime`                                | Timestamp when the message was last modified.                  |
| `content`   | `Text`                                    | The body text of the message.                                  |
| `sender`    | [CanvasUser](/sdk/data-canvasuser)        | The user who sent the message. May be null.                    |
| `recipient` | [CanvasUser](/sdk/data-canvasuser)        | The user who received the message. May be null.                |
| `note`      | [Note](/sdk/data-note)                    | Associated note (if any) for contextual linkage. May be null.  |
| `read`      | `DateTime`                                | Timestamp when the recipient read the message. Null if unread. |

## MessageAttachment

Represents a file attachment linked to a message.

### Fields

| Name           | Type                       | Description                                |
|----------------|----------------------------|--------------------------------------------|
| `id`           | `UUID`                     | Unique identifier for the attachment.      |
| `dbid`         | `Integer`                  | Database primary key.                      |
| `file`         | `Text`                     | Storage path or identifier for the file.   |
| `content_type` | `String`                   | MIME type of the attachment.               |
| `message`      | [Message](#message)        | The parent message to which this belongs.  |

## MessageTransmission

Tracks delivery attempts and status for a message.

### Fields

| Name                   | Type                                        | Description                                                 |
|------------------------|---------------------------------------------|-------------------------------------------------------------|
| `id`                   | `UUID`                                      | Unique identifier for the transmission record.              |
| `dbid`                 | `Integer`                                   | Database primary key.                                       |
| `created`              | `DateTime`                                  | Timestamp when the transmission was created.                |
| `modified`             | `DateTime`                                  | Timestamp when the transmission was last modified.          |
| `message`              | [Message](#message)                         | The message associated with this transmission.              |
| `delivered`            | `Boolean`                                   | Whether delivery was successful.                            |
| `failed`               | `Boolean`                                   | Whether delivery failed.                                    |
| `contact_point_system` | [TransmissionChannel](#transmissionchannel) | The channel used for delivery.                              |
| `contact_point_value`  | `String`                                    | The destination address or identifier (e.g., phone, email). |
| `comment`              | `Text`                                      | Optional comments or error details.                         |
| `delivered_by`         | [Staff](/sdk/data-staff/#staff)             | The staff member who processed the delivery. May be null.   |
