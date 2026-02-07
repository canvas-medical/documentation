---
title: Twilio
slug: clients-twilio
hidden: false
---

The Canvas SDK Twilio client provides a simple interface for sending SMS and MMS messages, managing phone numbers, and handling webhooks using the Twilio API.

## Requirements

- **Twilio Account SID**: Found in your [Twilio Console](https://console.twilio.com/)
- **Twilio API Key and Secret**: Create at [API Keys](https://console.twilio.com/us1/account/keys-credentials/api-keys)
- **Twilio Phone Number**: Purchase at [Phone Numbers](https://console.twilio.com/us1/develop/phone-numbers/manage/incoming)

## Imports

The Twilio client is included in the Canvas SDK. Import the necessary components:

```python
from canvas_sdk.clients.twilio.libraries import SmsClient
from canvas_sdk.clients.twilio.structures import Settings, SmsMms, RequestFailed
```

## Initialize the Client

```python
settings = Settings(
    account_sid="your_account_sid",
    key="your_api_key",
    secret="your_api_secret",
)
client = SmsClient(settings)
```

## Send a Simple SMS

```python
from canvas_sdk.clients.twilio.libraries import SmsClient
from canvas_sdk.clients.twilio.structures import Settings, SmsMms, RequestFailed

# Initialize the client
settings = Settings(
    account_sid="ACxxxxxxxxxxxxxxxxx",
    key="SKxxxxxxxxxxxxxxxxx",
    secret="your_api_secret",
)
client = SmsClient(settings)

# First, get your phone number SID
phones = list(client.account_phone_numbers())
phone = phones[0]  # Use the first phone number
print(f"Using phone: {phone.phone_number} (SID: {phone.sid})")

# Create and send the SMS
sms = SmsMms(
    number_from=phone.phone_number,
    number_from_sid=phone.sid,
    number_to="+1234567890",
    message="Hello from Canvas SDK!",
    media_url="",
    status_callback_url="",
)

try:
    message = client.send_sms_mms(sms)
    print(f"Message sent! SID: {message.sid}, Status: {message.status.value}")
except RequestFailed as e:
    print(f"Failed to send: {e.message} (HTTP {e.status_code})")
```

## Send an MMS with Image

```python
# Create an MMS with an image attachment
mms = SmsMms(
    number_from=phone.phone_number,
    number_from_sid=phone.sid,
    number_to="+1234567890",
    message="Check out this image!",
    media_url="https://example.com/image.jpg",
    status_callback_url="",
)

try:
    message = client.send_sms_mms(mms)
    print(f"MMS sent! SID: {message.sid}")
except RequestFailed as e:
    print(f"Failed to send: {e.message}")
```

## Send SMS with Status Callback

```python
# Send SMS with a callback URL to track delivery status
sms = SmsMms(
    number_from=phone.phone_number,
    number_from_sid=phone.sid,
    number_to="+1234567890",
    message="Message with tracking",
    media_url="",
    status_callback_url="https://your-app.com/api/sms-status",
)

message = client.send_sms_mms(sms)
print(f"Message queued with callback. SID: {message.sid}")
```

## Retrieve Message History

```python
from canvas_sdk.clients.twilio.constants import DateOperation

# Get all messages (no filters)
for message in client.retrieve_all_sms("", "", "", DateOperation.ON_EXACTLY):
    print(f"{message.date_sent}: {message.number_from} -> {message.number_to}: {message.body}")

# Get messages sent to a specific number
for message in client.retrieve_all_sms("+1234567890", "", "", DateOperation.ON_EXACTLY):
    print(f"To {message.number_to}: {message.body}")

# Get messages from a specific date onwards
for message in client.retrieve_all_sms("", "", "2024-01-01", DateOperation.ON_AND_AFTER):
    print(f"{message.date_sent}: {message.body}")
```

## Handle Inbound Messages (Webhook)

When Twilio receives an SMS to your number, it can call your webhook. Parse the callback data:

```python
from canvas_sdk.clients.twilio.structures import StatusInbound, TwiMlMessage

def handle_inbound_sms(raw_body: str) -> str:
    """Process incoming SMS and return TwiML response."""
    # Parse the incoming message
    inbound = StatusInbound.callback_inbound(raw_body)

    print(f"Received from {inbound.number_from}: {inbound.body}")

    # Create a reply using TwiML
    if "hello" in inbound.body.lower():
        reply = TwiMlMessage.instance("Hello! Nice to hear from you!")
    else:
        reply = TwiMlMessage.instance("Thanks for your message!")

    return reply.to_xml()
```

## Reply with MMS (TwiML)

```python
from canvas_sdk.clients.twilio.structures import TwiMlMessage

# Create a TwiML response with text and image
reply = TwiMlMessage.instance_with_media(
    message_text="Here's a picture for you!",
    media_url="https://example.com/image.jpg"
)

xml_response = reply.to_xml()
# Returns TwiML like:
# <?xml version="1.0" encoding="UTF-8"?>
# <Response><Message><Body>Here's a picture for you!</Body><Media>https://example.com/image.jpg</Media></Message></Response>
```

## SmsClient

The main class for interacting with the Twilio SMS/MMS API.

### Constructor

```python
SmsClient(settings: Settings)
```

| Parameter  | Type       | Description                                      |
|------------|------------|--------------------------------------------------|
| `settings` | `Settings` | Configuration object with Twilio credentials    |

### Phone Number Management

#### `account_phone_numbers() -> Iterator[Phone]`

Retrieve all phone numbers associated with the Twilio account.

```python
for phone in client.account_phone_numbers():
    print(f"{phone.friendly_name}: {phone.phone_number}")
    print(f"  SMS: {phone.capabilities.sms}, MMS: {phone.capabilities.mms}")
```

**Returns:** Iterator of `Phone` objects

**Raises:** `RequestFailed` on error

#### `account_phone_number(phone_sid: str) -> Phone`

Retrieve details for a specific phone number by its SID.

```python
phone = client.account_phone_number("PNxxxxxxxxxxxxxxxxx")
print(f"Phone: {phone.phone_number}, Status: {phone.status}")
```

| Parameter   | Type  | Description                    |
|-------------|-------|--------------------------------|
| `phone_sid` | `str` | The Twilio SID of the phone    |

**Returns:** `Phone` object

**Raises:** `RequestFailed` on error

#### `set_inbound_webhook(phone_sid: str, webhook_url: str, method: HttpMethod) -> bool`

Configure the webhook URL for receiving inbound messages on a phone number.

```python
from canvas_sdk.clients.twilio.constants import HttpMethod

success = client.set_inbound_webhook(
    phone_sid="PNxxxxxxxxxxxxxxxxx",
    webhook_url="https://your-app.com/api/inbound-sms",
    method=HttpMethod.POST
)
```

| Parameter     | Type         | Description                        |
|---------------|--------------|-----------------------------------|
| `phone_sid`   | `str`        | The Twilio SID of the phone       |
| `webhook_url` | `str`        | URL to receive inbound messages   |
| `method`      | `HttpMethod` | HTTP method (GET or POST)         |

**Returns:** `True` on success

**Raises:** `RequestFailed` on error

### Sending Messages

#### `send_sms_mms(sms_mms: SmsMms) -> Message`

Send an SMS or MMS message. The method automatically validates phone capabilities.

```python
sms = SmsMms(
    number_from="+15551234567",
    number_from_sid="PNxxxxxxxxxxxxxxxxx",
    number_to="+15559876543",
    message="Hello!",
    media_url="",  # Empty for SMS, URL for MMS
    status_callback_url="https://your-app.com/status",
)

message = client.send_sms_mms(sms)
print(f"Sent! SID: {message.sid}, Status: {message.status.value}")
```

| Parameter | Type     | Description              |
|-----------|----------|--------------------------|
| `sms_mms` | `SmsMms` | Message details to send  |

**Returns:** `Message` object with sent message details

**Raises:** `RequestFailed` if the phone lacks required capabilities or API fails

### Retrieving Messages

#### `retrieve_sms(message_id: str) -> Message`

Get details for a specific message by its SID.

```python
message = client.retrieve_sms("SMxxxxxxxxxxxxxxxxx")
print(f"Status: {message.status.value}")
print(f"Body: {message.body}")
print(f"Sent: {message.date_sent}")
```

| Parameter    | Type  | Description            |
|--------------|-------|------------------------|
| `message_id` | `str` | The Twilio message SID |

**Returns:** `Message` object

**Raises:** `RequestFailed` on error

#### `retrieve_all_sms(number_to, number_from, date_sent, date_operation) -> Iterator[Message]`

Retrieve messages with optional filtering.

```python
from canvas_sdk.clients.twilio.constants import DateOperation

# All messages
for msg in client.retrieve_all_sms("", "", "", DateOperation.ON_EXACTLY):
    print(msg.body)

# Messages to a specific number
for msg in client.retrieve_all_sms("+15551234567", "", "", DateOperation.ON_EXACTLY):
    print(msg.body)

# Messages from a specific date
for msg in client.retrieve_all_sms("", "", "2024-06-01", DateOperation.ON_AND_AFTER):
    print(f"{msg.date_sent}: {msg.body}")
```

| Parameter        | Type            | Description                                |
|------------------|-----------------|-------------------------------------------|
| `number_to`      | `str`           | Filter by recipient (empty = no filter)   |
| `number_from`    | `str`           | Filter by sender (empty = no filter)      |
| `date_sent`      | `str`           | Date to filter by (YYYY-MM-DD format)     |
| `date_operation` | `DateOperation` | How to compare the date                   |

**Returns:** Iterator of `Message` objects

**Raises:** `RequestFailed` on error

#### `delete_sms(message_id: str) -> bool`

Delete a message from Twilio.

```python
deleted = client.delete_sms("SMxxxxxxxxxxxxxxxxx")
print(f"Deleted: {deleted}")
```

| Parameter    | Type  | Description            |
|--------------|-------|------------------------|
| `message_id` | `str` | The Twilio message SID |

**Returns:** `True` on success

**Raises:** `RequestFailed` on error

### Media Handling

#### `retrieve_media_list(message_id: str) -> Iterator[Media]`

Get all media attachments for a message.

```python
for media in client.retrieve_media_list("SMxxxxxxxxxxxxxxxxx"):
    print(f"Media SID: {media.sid}")
    print(f"Content Type: {media.content_type}")
```

| Parameter    | Type  | Description            |
|--------------|-------|------------------------|
| `message_id` | `str` | The Twilio message SID |

**Returns:** Iterator of `Media` objects

**Raises:** `RequestFailed` on error

#### `retrieve_raw_media(message_id: str, media_sid: str) -> bytes`

Download the raw binary content of a media attachment.

```python
for media in client.retrieve_media_list(message_sid):
    content = client.retrieve_raw_media(message_sid, media.sid)

    # Save to file
    with open(f"media_{media.sid}.jpg", "wb") as f:
        f.write(content)
```

| Parameter    | Type  | Description            |
|--------------|-------|------------------------|
| `message_id` | `str` | The Twilio message SID |
| `media_sid`  | `str` | The Twilio media SID   |

**Returns:** Raw binary content (`bytes`)

**Raises:** `RequestFailed` on error

---

## Data Structures

### Settings

Configuration for the SmsClient.

| Field         | Type  | Description                    |
|---------------|-------|--------------------------------|
| `account_sid` | `str` | Twilio Account SID             |
| `key`         | `str` | Twilio API Key SID             |
| `secret`      | `str` | Twilio API Key Secret          |

### SmsMms

Represents an SMS or MMS message to send.

| Field                 | Type  | Description                                |
|-----------------------|-------|--------------------------------------------|
| `number_from`         | `str` | Sender phone number (E.164 format)         |
| `number_from_sid`     | `str` | Twilio SID of the sender phone number      |
| `number_to`           | `str` | Recipient phone number (E.164 format)      |
| `message`             | `str` | Text content of the message                |
| `media_url`           | `str` | URL of media to attach (empty for SMS)     |
| `status_callback_url` | `str` | URL to receive delivery status updates     |

### Message

Represents a Twilio message with full metadata.

| Field              | Type                     | Description                          |
|--------------------|--------------------------|--------------------------------------|
| `sid`              | `str`                    | Unique message identifier            |
| `body`             | `str`                    | Message text content                 |
| `date_created`     | `datetime`               | When the message was created         |
| `date_sent`        | `datetime \| None`       | When the message was sent            |
| `date_updated`     | `datetime`               | When the message was last updated    |
| `direction`        | `MessageDirection`       | Message direction                    |
| `number_from`      | `str`                    | Sender phone number                  |
| `number_to`        | `str`                    | Recipient phone number               |
| `price`            | `str \| None`            | Cost of the message                  |
| `price_unit`       | `str`                    | Currency of the price                |
| `error_code`       | `int \| None`            | Error code if failed                 |
| `error_message`    | `str \| None`            | Error description if failed          |
| `uri`              | `str`                    | API URI for this resource            |
| `count_media`      | `int \| None`            | Number of media attachments          |
| `count_segments`   | `int`                    | Number of SMS segments               |
| `status`           | `MessageStatus`          | Current message status               |
| `sub_resource_uris`| `dict[str, str] \| None` | URIs to related resources            |

### Phone

Represents a Twilio phone number with configuration.

| Field                    | Type           | Description                            |
|--------------------------|----------------|----------------------------------------|
| `account_sid`            | `str`          | Twilio Account SID                     |
| `capabilities`           | `Capabilities` | Phone capabilities (SMS, MMS, etc.)    |
| `date_created`           | `datetime`     | When added to account                  |
| `date_updated`           | `datetime`     | Last configuration update              |
| `friendly_name`          | `str`          | User-defined name                      |
| `phone_number`           | `str`          | Phone number in E.164 format           |
| `sid`                    | `str`          | Unique phone number identifier         |
| `sms_fallback_method`    | `HttpMethod`   | HTTP method for fallback URL           |
| `sms_fallback_url`       | `str`          | Fallback URL if primary fails          |
| `sms_method`             | `HttpMethod`   | HTTP method for SMS webhook            |
| `sms_url`                | `str`          | Webhook URL for inbound SMS            |
| `status_callback_method` | `HttpMethod`   | HTTP method for status callbacks       |
| `status_callback`        | `str`          | URL for status updates                 |
| `status`                 | `str`          | Current phone number status            |

### Capabilities

Phone number communication capabilities.

| Field   | Type   | Description                    |
|---------|--------|--------------------------------|
| `fax`   | `bool` | Supports fax                   |
| `mms`   | `bool` | Supports MMS (multimedia)      |
| `sms`   | `bool` | Supports SMS (text)            |
| `voice` | `bool` | Supports voice calls           |

### Media

Represents media attached to a message.

| Field          | Type       | Description                        |
|----------------|------------|------------------------------------|
| `sid`          | `str`      | Unique media identifier            |
| `content_type` | `str`      | MIME type (e.g., `image/jpeg`)     |
| `date_created` | `datetime` | When the media was created         |
| `date_updated` | `datetime` | When the media was last updated    |
| `parent_sid`   | `str`      | Message SID this media belongs to  |
| `uri`          | `str`      | API URI for this resource          |

### StatusInbound

Parsed data from an inbound message webhook callback.

| Field                  | Type            | Description                         |
|------------------------|-----------------|-------------------------------------|
| `account_sid`          | `str`           | Twilio Account SID                  |
| `message_sid`          | `str`           | Message SID                         |
| `messaging_service_sid`| `str`           | Messaging Service SID               |
| `sms_message_sid`      | `str`           | SMS Message SID                     |
| `sms_sid`              | `str`           | SMS SID                             |
| `sms_status`           | `MessageStatus` | Message status                      |
| `to_country`           | `str`           | Recipient country                   |
| `to_zip`               | `str`           | Recipient ZIP code                  |
| `to_state`             | `str`           | Recipient state                     |
| `to_city`              | `str`           | Recipient city                      |
| `from_country`         | `str`           | Sender country                      |
| `from_zip`             | `str`           | Sender ZIP code                     |
| `from_state`           | `str`           | Sender state                        |
| `from_city`            | `str`           | Sender city                         |
| `number_to`            | `str`           | Recipient phone number              |
| `number_from`          | `str`           | Sender phone number                 |
| `body`                 | `str`           | Message text                        |
| `count_media`          | `int`           | Number of media attachments         |
| `count_segments`       | `int`           | Number of SMS segments              |
| `media_content_type`   | `list[str]`     | MIME types of attached media        |
| `media_url`            | `list[str]`     | URLs of attached media              |

**Class Methods:**

| Method                                     | Description                              |
|--------------------------------------------|------------------------------------------|
| `StatusInbound.callback_inbound(raw_body)` | Parse URL-encoded webhook body           |

### StatusOutboundApi

Parsed data from an outbound message status callback.

| Field            | Type            | Description                |
|------------------|-----------------|----------------------------|
| `account_sid`    | `str`           | Twilio Account SID         |
| `message_sid`    | `str`           | Message SID                |
| `sms_sid`        | `str`           | SMS SID                    |
| `sms_status`     | `MessageStatus` | SMS status                 |
| `message_status` | `MessageStatus` | Message status             |
| `number_to`      | `str`           | Recipient phone number     |
| `number_from`    | `str`           | Sender phone number        |

**Class Methods:**

| Method                                              | Description                    |
|-----------------------------------------------------|--------------------------------|
| `StatusOutboundApi.callback_outbound_api(raw_body)` | Parse URL-encoded webhook body |

### TwiMlMessage

Generates TwiML XML for responding to inbound messages.

| Field                 | Type               | Description                          |
|-----------------------|--------------------|--------------------------------------|
| `number_to`           | `str`              | Recipient (optional in response)     |
| `number_from`         | `str`              | Sender (optional in response)        |
| `status_callback_url` | `str`              | Status callback URL                  |
| `message_text`        | `str`              | Message text content                 |
| `media_url`           | `str`              | Media URL to attach                  |
| `method`              | `HttpMethod\|None` | HTTP method for callbacks            |

**Class Methods:**

| Method                                                                         | Description                    |
|--------------------------------------------------------------------------------|--------------------------------|
| `TwiMlMessage.instance(message_text) -> TwiMlMessage`                          | Create text-only TwiML message |
| `TwiMlMessage.instance_with_media(message_text, media_url) -> TwiMlMessage`    | Create TwiML with media        |

**Instance Methods:**

| Method            | Description                |
|-------------------|----------------------------|
| `to_xml() -> str` | Generate TwiML XML string  |

**Example:**

```python
# Simple text reply
reply = TwiMlMessage.instance("Thanks for your message!")
xml = reply.to_xml()

# Reply with media
reply = TwiMlMessage.instance_with_media("Check this out!", "https://example.com/image.jpg")
xml = reply.to_xml()
```

---

## Constants (Enums)

### MessageStatus

Message lifecycle status values.

| Value                 | Description                              |
|-----------------------|------------------------------------------|
| `ACCEPTED`            | Message accepted by Twilio               |
| `SCHEDULED`           | Message scheduled for future delivery    |
| `CANCELED`            | Scheduled message was canceled           |
| `QUEUED`              | Message queued for sending               |
| `SENDING`             | Message is being sent                    |
| `SENT`                | Message sent to carrier                  |
| `FAILED`              | Message failed to send                   |
| `DELIVERED`           | Message delivered to recipient           |
| `UNDELIVERED`         | Message could not be delivered           |
| `PARTIALLY_DELIVERED` | Some recipients received the message     |
| `RECEIVING`           | Inbound message being received           |
| `RECEIVED`            | Inbound message received                 |
| `READ`                | Message was read (WhatsApp only)         |

### MessageDirection

Message direction types.

| Value            | Description                              |
|------------------|------------------------------------------|
| `INBOUND`        | Message received from external number    |
| `OUTBOUND_API`   | Message sent via API                     |
| `OUTBOUND_CALL`  | Message sent during a call               |
| `OUTBOUND_REPLY` | Message sent as webhook reply            |

### DateOperation

Date filtering operations for message queries.

| Value           | Description                              |
|-----------------|------------------------------------------|
| `ON_EXACTLY`    | Messages on exactly this date            |
| `ON_AND_BEFORE` | Messages on or before this date          |
| `ON_AND_AFTER`  | Messages on or after this date           |

### HttpMethod

HTTP methods for webhook configuration.

| Value  | Description      |
|--------|------------------|
| `GET`  | HTTP GET method  |
| `POST` | HTTP POST method |

---

## Error Handling

### RequestFailed

Exception raised when a Twilio API request fails (extends `RuntimeError`).

| Attribute     | Type  | Description                 |
|---------------|-------|-----------------------------|
| `status_code` | `int` | HTTP status code            |
| `message`     | `str` | Error message from Twilio   |

**Example:**

```python
try:
    message = client.send_sms_mms(sms)
except RequestFailed as e:
    if e.status_code == 0:
        # Client-side validation error (e.g., phone lacks MMS capability)
        print(f"Validation error: {e.message}")
    else:
        # Twilio API error
        print(f"API error {e.status_code}: {e.message}")
```

---

## Complete Webhook Example

Here's a complete example of handling inbound SMS and sending replies:

```python
from canvas_sdk.clients.twilio.structures import StatusInbound, TwiMlMessage

def handle_webhook(raw_body: str) -> str:
    """
    Handle incoming SMS webhook from Twilio.

    Args:
        raw_body: URL-encoded form data from Twilio POST request

    Returns:
        TwiML XML response string
    """
    # Parse the inbound message
    inbound = StatusInbound.callback_inbound(raw_body)

    # Log the message
    print(f"From: {inbound.number_from}")
    print(f"To: {inbound.number_to}")
    print(f"Body: {inbound.body}")
    print(f"Media count: {inbound.count_media}")

    # Check for media attachments
    if inbound.count_media > 0:
        for i, url in enumerate(inbound.media_url):
            print(f"Media {i}: {inbound.media_content_type[i]} - {url}")

    # Generate appropriate response
    body_lower = inbound.body.lower()

    if "help" in body_lower:
        reply = TwiMlMessage.instance("Commands: HELP, STATUS, HELLO")
    elif "hello" in body_lower:
        reply = TwiMlMessage.instance_with_media(
            "Hello! Here's a welcome image!",
            "https://example.com/welcome.jpg"
        )
    elif "status" in body_lower:
        reply = TwiMlMessage.instance("System is operational.")
    else:
        reply = TwiMlMessage.instance("Unknown command. Text HELP for options.")

    return reply.to_xml()
```

---

## Additional Resources

- [Twilio SMS API Documentation](https://www.twilio.com/docs/sms)
- [Twilio Webhooks Guide](https://www.twilio.com/docs/messaging/guides/webhook-request)
- [TwiML Reference](https://www.twilio.com/docs/messaging/twiml)
- [Example Plugin](/sdk/example-twilio_sms_mms/) - Documentation for the example plugin
- [Source Code](https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/twilio_sms_mms) - View the source on GitHub
