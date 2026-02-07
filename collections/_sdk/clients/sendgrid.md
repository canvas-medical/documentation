---
title: SendGrid
slug: clients-sendgrid
hidden: false
---

The Canvas SDK SendGrid client provides a simple interface for sending emails, managing webhooks, and querying email logs using the SendGrid API.

## Requirements

- **SendGrid API Key**: Create one at https://app.sendgrid.com/settings/api_keys
- **Authenticated Domain**: Configure at https://app.sendgrid.com/settings/sender_auth

## Imports

The SendGrid client is included in the Canvas SDK. Import the necessary components:

```python
from canvas_sdk.clients.sendgrid.libraries import EmailClient
from canvas_sdk.clients.sendgrid.constants import RecipientType
from canvas_sdk.clients.sendgrid.structures import (
    Address,
    BodyContent,
    Email,
    Recipient,
    RequestFailed,
    Settings,
)
```

## Initialize the Client

```python
client = EmailClient(Settings(key="your_sendgrid_api_key"))
```

## Send a Simple Text Email

```python
from canvas_sdk.clients.sendgrid.libraries import EmailClient
from canvas_sdk.clients.sendgrid.constants import RecipientType
from canvas_sdk.clients.sendgrid.structures import (
    Address, BodyContent, Email, Recipient, RequestFailed, Settings
)

client = EmailClient(Settings(key="your_api_key"))

email = Email(
    sender=Address(email="sender@example.com", name="Sender Name"),
    reply_tos=[Address(email="reply@example.com", name="Reply To")],
    recipients=[
        Recipient(address=Address(email="recipient@example.com", name="Recipient"), type=RecipientType.TO)
    ],
    subject="Hello from Canvas SDK",
    bodies=[BodyContent(type="text/plain", value="This is a test email.")],
    attachments=[],
    send_at=Email.now(),
)

try:
    client.simple_send(email)
    print("Email sent successfully!")
except RequestFailed as e:
    print(f"Failed to send email: {e.message} (HTTP {e.status_code})")
```

## Send an HTML Email with CC

```python
email = Email(
    sender=Address(email="sender@example.com", name="Sender"),
    reply_tos=[Address(email="reply@example.com", name="Reply To")],
    recipients=[
        Recipient(address=Address(email="to@example.com", name="To"), type=RecipientType.TO),
        Recipient(address=Address(email="cc@example.com", name="CC"), type=RecipientType.CC),
    ],
    subject="HTML Email Example",
    bodies=[
        BodyContent(type="text/plain", value="Plain text fallback"),
        BodyContent(type="text/html", value="<html><body><h1>Hello!</h1><p>This is HTML content.</p></body></html>"),
    ],
    attachments=[],
    send_at=Email.now(),
)

client.simple_send(email)
```

## Send an Email with Attachment

```python
from canvas_sdk.clients.sendgrid.structures import Attachment

# Create attachment from URL
attachment = Attachment.from_url(
    url="https://example.com/document.pdf",
    headers={},
    filename="document.pdf"
)

email = Email(
    sender=Address(email="sender@example.com", name="Sender"),
    reply_tos=[Address(email="reply@example.com", name="Reply To")],
    recipients=[
        Recipient(address=Address(email="to@example.com", name="To"), type=RecipientType.TO)
    ],
    subject="Email with Attachment",
    bodies=[BodyContent(type="text/plain", value="Please find attached document.")],
    attachments=[attachment],
    send_at=Email.now(),
)

client.simple_send(email)
```

## Send an Email with Inline Image

```python
# Create inline image attachment
inline_image = Attachment.from_url_inline(
    url="https://example.com/logo.png",
    headers={},
    filename="logo.png",
    content_id="logo123"
)

email = Email(
    sender=Address(email="sender@example.com", name="Sender"),
    reply_tos=[Address(email="reply@example.com", name="Reply To")],
    recipients=[
        Recipient(address=Address(email="to@example.com", name="To"), type=RecipientType.TO)
    ],
    subject="Email with Inline Image",
    bodies=[
        BodyContent(type="text/plain", value="See image in HTML version"),
        BodyContent(type="text/html", value='<html><body><img src="cid:logo123" width="200"/></body></html>'),
    ],
    attachments=[inline_image],
    send_at=Email.now(),
)

client.simple_send(email)
```

## Query Sent Emails

```python
from datetime import datetime
from canvas_sdk.clients.sendgrid.constants import CriterionOperation
from canvas_sdk.clients.sendgrid.structures import CriterionDatetime, LoggedEmailCriteria

criteria = LoggedEmailCriteria(
    message_id="",
    subject="",
    to_email="recipient@example.com",
    reason="",
    status=[],
    message_created_at=[
        CriterionDatetime(
            date_time=datetime(2024, 1, 1),
            operation=CriterionOperation.GREATER_THAN_OR_EQUAL
        )
    ],
)

for email in client.logged_emails(criteria, up_to=10):
    print(f"Subject: {email.subject}, Status: {email.status.value}")
```

## EmailClient

The main class for interacting with the SendGrid API.

### Constructor

```python
EmailClient(settings: Settings)
```

| Parameter  | Type       | Description                                 |
|------------|------------|---------------------------------------------|
| `settings` | `Settings` | Configuration object containing the API key |

### Sending Emails

#### `simple_send(email: Email) -> bool`

Send an email using a structured `Email` object. This is the recommended method for most use cases.

**Returns:** `True` on success

**Raises:** `RequestFailed` on error

#### `prepared_send(data: dict) -> bool`

Send an email using a raw dictionary following SendGrid's API schema. Use this for advanced cases not covered by `simple_send`.

**Parameters:**

- `data`: Dictionary following [SendGrid's mail send schema](https://www.twilio.com/docs/sendgrid/api-reference/mail-send/mail-send#request-body)

**Returns:** `True` on success

**Raises:** `RequestFailed` on error

### Email Logs

#### `logged_emails(criteria: LoggedEmailCriteria, up_to: int) -> Iterator[SentEmail]`

Query sent emails matching the specified criteria.

**Parameters:**

- `criteria`: Filter criteria for the query
- `up_to`: Maximum number of results to return

**Returns:** Iterator of `SentEmail` objects

#### `logged_email(message_id: str) -> SentEmailDetail`

Get detailed information about a specific email including its event history.

**Parameters:**

- `message_id`: The SendGrid message ID

**Returns:** `SentEmailDetail` object with full event history

### Inbound Parse Webhooks

Configure webhooks to receive incoming emails.

| Method                                                      | Description                           |
|-------------------------------------------------------------|---------------------------------------|
| `parser_setting_add(setting: ParseSetting) -> ParseSetting` | Create a new inbound parse webhook    |
| `parser_setting_delete(hostname: str) -> bool`              | Delete a webhook by hostname          |
| `parser_setting_get(hostname: str) -> ParseSetting`         | Get webhook configuration by hostname |
| `parser_setting_list() -> Iterator[ParseSetting]`           | List all inbound parse webhooks       |

Requires MX record setup pointing to `mx.sendgrid.net`, for example:

| host     | type | priority | TTL  | value             |
|----------|------|----------|------|-------------------|
| `canvas` | `MX` | 10       | 1 hr | `mx.sendgrid.net` |


### Event Webhooks

Configure webhooks to receive email delivery status notifications.

| Method                                                            | Description                                               |
|-------------------------------------------------------------------|-----------------------------------------------------------|
| `event_webhook_add(event: EventWebhook) -> EventWebhookRecord`    | Create a new event webhook                                |
| `event_webhook_delete(event_webhook_id: str) -> bool`             | Delete a webhook by ID                                    |
| `event_webhook_get(event_webhook_id: str) -> EventWebhookRecord`  | Get webhook by ID                                         |
| `event_webhook_list() -> Iterator[EventWebhookRecord]`            | List all event webhooks                                   |
| `event_webhook_sign(event_webhook_id: str, enabled: bool) -> str` | Enable/disable signature verification, returns public key |

---

## Data Structures

### Settings

Configuration for the EmailClient.

| Field | Type  | Description        |
|-------|-------|--------------------|
| `key` | `str` | SendGrid API key   |

### Address

Represents an email address with display name.

| Field   | Type  | Description   |
|---------|-------|---------------|
| `email` | `str` | Email address |
| `name`  | `str` | Display name  |

### Recipient

Represents an email recipient with type.

| Field     | Type            | Description           |
|-----------|-----------------|----------------------|
| `address` | `Address`       | Email address object |
| `type`    | `RecipientType` | TO, CC, or BCC       |

### BodyContent

Represents email body content with MIME type.

| Field   | Type  | Description                                    |
|---------|-------|------------------------------------------------|
| `type`  | `str` | MIME type (e.g., `text/plain`, `text/html`)    |
| `value` | `str` | Content                                        |

### Email

Complete email message structure.

| Field         | Type               | Description                    |
|---------------|--------------------|--------------------------------|
| `sender`      | `Address`          | Sender email address           |
| `reply_tos`   | `list[Address]`    | Reply-to addresses             |
| `recipients`  | `list[Recipient]`  | List of recipients (TO/CC/BCC) |
| `subject`     | `str`              | Email subject line             |
| `bodies`      | `list[BodyContent]`| Email body content(s)          |
| `attachments` | `list[Attachment]` | File attachments               |
| `send_at`     | `int`              | Unix timestamp for sending     |

**Class Methods:**

| Method                            | Description                              |
|-----------------------------------|------------------------------------------|
| `Email.now() -> int`              | Get current timestamp for immediate send |
| `Email.timestamp(dt: datetime) -> int` | Convert datetime to Unix timestamp  |

### Attachment

Represents an email attachment.

| Field         | Type                    | Description                  |
|---------------|-------------------------|------------------------------|
| `content_id`  | `str`                   | ID for inline references     |
| `content`     | `str`                   | Base64 encoded content       |
| `type`        | `str`                   | MIME type                    |
| `filename`    | `str`                   | Filename                     |
| `disposition` | `AttachmentDisposition` | ATTACHMENT or INLINE         |

**Class Methods:**

| Method                                                              | Description                        |
|---------------------------------------------------------------------|------------------------------------|
| `Attachment.from_url(url, headers, filename) -> Attachment`         | Create attachment from URL         |
| `Attachment.from_url_inline(url, headers, filename, content_id) -> Attachment` | Create inline attachment from URL |

### LoggedEmailCriteria

Search criteria for querying sent emails.

| Field                | Type                     | Description                     |
|----------------------|--------------------------|---------------------------------|
| `message_id`         | `str`                    | Filter by message ID            |
| `subject`            | `str`                    | Filter by subject               |
| `to_email`           | `str`                    | Filter by recipient email       |
| `reason`             | `str`                    | Filter by reason                |
| `status`             | `list[StatusEmail]`      | Filter by status(es)            |
| `message_created_at` | `list[CriterionDatetime]`| Filter by creation date/time    |

### CriterionDatetime

DateTime comparison for email queries.

| Field       | Type                 | Description              |
|-------------|----------------------|--------------------------|
| `date_time` | `datetime`           | Date/time to compare     |
| `operation` | `CriterionOperation` | Comparison operator      |

### SentEmail

Basic information about a sent email (returned by `logged_emails`).

| Field        | Type          | Description              |
|--------------|---------------|--------------------------|
| `from_email` | `str`         | Sender email address     |
| `message_id` | `str`         | SendGrid message ID      |
| `subject`    | `str`         | Email subject            |
| `to_email`   | `str`         | Recipient email address  |
| `reason`     | `str`         | Delivery failure reason  |
| `status`     | `StatusEmail` | Delivery status          |
| `created_at` | `datetime`    | Creation timestamp       |

### SentEmailDetail

Detailed sent email information with event history (returned by `logged_email`).

| Field        | Type               | Description                |
|--------------|--------------------|----------------------------|
| `from_email` | `str`              | Sender email address       |
| `message_id` | `str`              | SendGrid message ID        |
| `subject`    | `str`              | Email subject              |
| `to_email`   | `str`              | Recipient email address    |
| `status`     | `StatusEmail`      | Current delivery status    |
| `events`     | `list[EmailEvent]` | List of lifecycle events   |

### EmailEvent

Represents an event in an email's lifecycle.

| Field         | Type         | Description                              |
|---------------|--------------|------------------------------------------|
| `event`       | `EventEmail` | Event type                               |
| `email`       | `str`        | Recipient email address                  |
| `message_id`  | `str`        | SendGrid message ID                      |
| `event_id`    | `str`        | Unique event ID                          |
| `on_datetime` | `datetime`   | Event timestamp                          |
| `reason`      | `str`        | Reason (for bounce, dropped events)      |
| `response`    | `str`        | Server response (for delivered events)   |
| `url`         | `str`        | Clicked/opened URL (for click, open)     |
| `attempt`     | `int`        | Delivery attempt number (for deferred)   |

### ParseSetting

Configuration for inbound email parsing.

| Field        | Type   | Description                                  |
|--------------|--------|----------------------------------------------|
| `url`        | `str`  | Webhook URL to receive parsed emails         |
| `hostname`   | `str`  | Domain to receive emails (requires MX record)|
| `spam_check` | `bool` | Enable spam filtering                        |
| `send_raw`   | `bool` | Send raw MIME message instead of parsed      |

### EventWebhook

Configuration for outbound email event notifications.

| Field               | Type   | Description                        |
|---------------------|--------|------------------------------------|
| `enabled`           | `bool` | Whether webhook is active          |
| `url`               | `str`  | Webhook URL                        |
| `friendly_name`     | `str`  | Display name                       |
| `delivered`         | `bool` | Track delivered events             |
| `bounce`            | `bool` | Track bounce events                |
| `dropped`           | `bool` | Track dropped events               |
| `spam_report`       | `bool` | Track spam report events           |
| `processed`         | `bool` | Track processed events             |
| `open`              | `bool` | Track open events                  |
| `click`             | `bool` | Track click events                 |
| `unsubscribe`       | `bool` | Track unsubscribe events           |
| `group_resubscribe` | `bool` | Track group resubscribe events     |
| `group_unsubscribe` | `bool` | Track group unsubscribe events     |

### EventWebhookRecord

Stored event webhook with metadata (extends EventWebhook).

| Field          | Type       | Description                              |
|----------------|------------|------------------------------------------|
| *(all fields from EventWebhook)* | | |
| `id`           | `str`      | Webhook ID                               |
| `public_key`   | `str`      | Public key for signature verification    |
| `created_date` | `datetime` | Creation timestamp                       |
| `updated_date` | `datetime` | Last update timestamp                    |

### ParsedEmail

Represents an inbound email received via the Inbound Parse webhook.

| Field             | Type                          | Description                    |
|-------------------|-------------------------------|--------------------------------|
| `headers`         | `list[ParsedHeader]`          | Email headers                  |
| `charsets`        | `dict[str, str]`              | Character set mappings         |
| `envelope`        | `ParsedEnvelope`              | SMTP envelope information      |
| `email_from`      | `str`                         | Sender address                 |
| `email_to`        | `str`                         | Recipient address              |
| `subject`         | `str`                         | Email subject                  |
| `text`            | `str`                         | Plain text body                |
| `html`            | `str`                         | HTML body                      |
| `attachments`     | `int`                         | Number of attachments          |
| `attachment_info` | `dict[str, ParsedAttachment]` | Attachment metadata            |
| `content_ids`     | `dict[str, str]`              | Content ID mappings            |
| `spf`             | `str`                         | SPF verification result        |
| `dkim`            | `str`                         | DKIM verification result       |
| `spam_report`     | `list[str]`                   | Spam analysis report           |
| `spam_score`      | `float`                       | Spam score                     |

---

## Constants (Enums)

### RecipientType

| Value | Description        |
|-------|--------------------|
| `TO`  | Primary recipient  |
| `CC`  | Carbon copy        |
| `BCC` | Blind carbon copy  |

### AttachmentDisposition

| Value        | Description                  |
|--------------|------------------------------|
| `ATTACHMENT` | Standard file attachment     |
| `INLINE`     | Embedded in email body       |

### StatusEmail

Email delivery status values.

| Value           | Description                |
|-----------------|----------------------------|
| `PROCESSED`     | Email processed by SendGrid|
| `DELIVERED`     | Successfully delivered     |
| `NOT_DELIVERED` | Delivery failed            |
| `DEFERRED`      | Temporarily delayed        |
| `DROPPED`       | Dropped by SendGrid        |
| `BOUNCED`       | Bounced back               |
| `BLOCKED`       | Blocked by recipient       |

### EventEmail

Email event types for webhooks.

| Value               | Description                     |
|---------------------|---------------------------------|
| `BOUNCE`            | Email bounced                   |
| `CLICK`             | Link clicked                    |
| `DEFERRED`          | Delivery deferred               |
| `DELIVERED`         | Email delivered                 |
| `DROPPED`           | Email dropped                   |
| `CANCEL_DROP`       | Drop cancelled                  |
| `OPEN`              | Email opened                    |
| `PROCESSED`         | Email processed                 |
| `RECEIVED`          | Inbound email received          |
| `SPAM_REPORT`       | Reported as spam                |
| `GROUP_UNSUBSCRIBE` | Unsubscribed from group         |
| `GROUP_RESUBSCRIBE` | Resubscribed to group           |
| `UNSUBSCRIBE`       | Unsubscribed                    |

### CriterionOperation

Comparison operators for email log queries.

| Value                    | Symbol | Description              |
|--------------------------|--------|--------------------------|
| `GREATER_THAN`           | `>`    | Greater than             |
| `GREATER_THAN_OR_EQUAL`  | `>=`   | Greater than or equal    |
| `LOWER_THAN`             | `<`    | Less than                |
| `LOWER_THAN_OR_EQUAL`    | `<=`   | Less than or equal       |
| `EQUAL`                  | `=`    | Equal to                 |

---

## Error Handling

### RequestFailed

Exception raised when a SendGrid API request fails (extends `RuntimeError`).

| Attribute     | Type  | Description                   |
|---------------|-------|-------------------------------|
| `status_code` | `int` | HTTP status code              |
| `message`     | `str` | Error message from SendGrid   |

**Example:**

```python
try:
    client.simple_send(email)
except RequestFailed as e:
    print(f"Error {e.status_code}: {e.message}")
```

---

## Webhook Setup Examples

### Inbound Parse Webhook (Receive Incoming Emails)

```python
from canvas_sdk.clients.sendgrid.structures import ParseSetting

# Note: Requires MX record for the hostname pointing to mx.sendgrid.net
setting = ParseSetting(
    url="https://your-app.com/api/incoming-email",
    hostname="mail.yourdomain.com",
    spam_check=True,
    send_raw=False,
)

try:
    created = client.parser_setting_add(setting)
    print(f"Inbound webhook created for {created.hostname}")
except RequestFailed as e:
    print(f"Failed: {e.message}")
```

### Event Webhook (Track Outbound Email Status)

```python
from canvas_sdk.clients.sendgrid.structures import EventWebhook

webhook = EventWebhook(
    url="https://your-app.com/api/email-events",
    enabled=True,
    friendly_name="My Email Tracker",
    delivered=True,
    bounce=True,
    dropped=True,
    spam_report=True,
    processed=True,
    open=True,
    click=True,
    unsubscribe=False,
    group_resubscribe=False,
    group_unsubscribe=False,
)

try:
    created = client.event_webhook_add(webhook)
    print(f"Event webhook created with ID: {created.id}")
except RequestFailed as e:
    print(f"Failed: {e.message}")
```

---

## Additional Resources

- [SendGrid API Documentation](https://www.twilio.com/docs/sendgrid/api-reference)
- [Inbound Parse Webhook Setup](https://www.twilio.com/docs/sendgrid/for-developers/parsing-email/inbound-email)
- [Event Webhook Documentation](https://www.twilio.com/docs/sendgrid/for-developers/tracking-events/event)
- [Example Plugin](/sdk/example-sendgrid_email/) - Documentation for the example plugin
- [Source Code](https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/sendgrid_email) - View the source on GitHub
