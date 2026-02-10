---
title: 'SendGrid Email'
slug: 'example-sendgrid_email'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/sendgrid_email' target='_blank'>View the source</a> for this plugin on GitHub." %}


## Description

Plugin that provides a SimpleAPI for sending emails, querying sent emails, managing inbound and outbound webhooks, and handling email status callbacks using the Canvas SDK's SendGrid client. It supports inline images, file attachments, inbound email parsing, and outbound event tracking. Includes a chart application that renders a form interface for email management directly from the chart.

## Configuration

This example plugin defines the following "secrets" in the manifest file:

```
    "secrets": [
        "SendgridAPIKey"
    ],
```
Once defined in the `MANIFEST.json`, set the secrets for your plugin in the Admin UI of your Canvas EMR. [Read more](https://docs.canvasmedical.com/sdk/secrets/)

### SendgridAPIKey
Your [SendGrid API key](https://docs.sendgrid.com/ui/account-and-settings/api-keys).

## CANVAS_MANIFEST.json

```json
{
  "sdk_version": "0.85.0",
  "plugin_version": "0.0.1",
  "name": "email_sender",
  "description": "use Sendgrid to send emails, retrieve sent emails, manage inbound and outbound webhooks",
  "components": {
    "protocols": [
      {
        "class": "email_sender.handlers.email_manip:EmailManip",
        "description": "Emails with Sendgrid"
      }
    ],
    "applications": [
      {
        "class": "email_sender.handlers.email_form_app:EmailFormApp",
        "name": "Emails Sendgrid",
        "description": "Emails with Sendgrid",
        "icon": "static/email_sender.png",
        "scope": "patient_specific",
        "show_in_panel": false
      }
    ],
    "commands": [],
    "content": [],
    "effects": [],
    "views": []
  },
  "secrets": [
    "SendgridAPIKey"
  ],
  "tags": {},
  "references": [],
  "license": "",
  "diagram": false,
  "readme": "./README.md"
}
```

## handlers/

### email_manip.py

**Purpose**

This code defines a SimpleAPI handler that exposes REST endpoints for managing email operations via the Canvas SDK's SendGrid client.

**Class Overview**

- The main class, `EmailManip`, extends `SimpleAPI`.
- It creates a SendGrid `EmailClient` using an API key stored in plugin secrets.
- It uses the plugin cache system for storing webhook callback data.

**Main Workflow**

- `POST /send_email` — Sends an email with optional inline images and file attachments.
- `POST /emails_sent` — Queries sent emails with optional filters for recipient and date.
- `GET /email_events/<message_id>` — Retrieves email events for a specific message.
- `POST /inbound_webhook` — Enables/disables the SendGrid inbound parse webhook.
- `GET /inbound_webhook` — Gets the current inbound webhook configuration status.
- `POST /outbound_webhook` — Enables/disables the SendGrid outbound event webhook.
- `GET /outbound_webhook` — Gets the current outbound webhook configuration status.
- `POST /inbound_email` — Receives and caches parsed inbound emails from SendGrid.
- `GET /inbound_email` — Retrieves the most recent inbound email from cache.
- `POST /outbound_email_status` — Receives and caches outbound email status events.
- `GET /outbound_email_status` — Retrieves the most recent outbound status events from cache.

**SendGrid Client Integration**

- The `_sendgrid_client` method creates an `EmailClient` instance from `canvas_sdk.clients.sendgrid.libraries`.
- Email composition uses structured types: `Address`, `Recipient`, `BodyContent`, `Attachment`, and `Email`.
- Error handling uses the `RequestFailed` exception from the SendGrid client structures.

```python
from datetime import UTC, datetime, timedelta
from http import HTTPStatus

from email_sender.constants.constants import Constants

from canvas_sdk.caching.plugins import get_cache
from canvas_sdk.clients.sendgrid.constants import (
    CriterionOperation,
    RecipientType,
)
from canvas_sdk.clients.sendgrid.libraries import EmailClient
from canvas_sdk.clients.sendgrid.structures import (
    Address,
    Attachment,
    BodyContent,
    CriterionDatetime,
    Email,
    EmailEvent,
    EventWebhook,
    LoggedEmailCriteria,
    ParsedEmail,
    ParseSetting,
    Recipient,
    RequestFailed,
    Settings,
)
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import Credentials, SimpleAPI, api
from logger import log


class EmailManip(SimpleAPI):
    """API handler for SendGrid email operations including sending, webhooks, and logging."""

    PREFIX = None

    def authenticate(self, credentials: Credentials) -> bool:
        """Authenticate the API request. Always returns True (no authentication required)."""
        return True

    def _sendgrid_client(self) -> EmailClient:
        """Create and return a configured SendGrid email client."""
        settings = Settings(key=self.secrets[Constants.sendgrid_api_key])
        return EmailClient(settings)

    @api.get("/email_events/<message_id>")
    def email_events(self) -> list[Response | Effect]:
        """Retrieve email events for a specific message ID from SendGrid."""
        message_id = self.request.path_params["message_id"]
        client = self._sendgrid_client()
        try:
            result = [
                JSONResponse(
                    client.logged_email(message_id).to_dict(),
                    status_code=HTTPStatus(HTTPStatus.OK),
                )
            ]
        except RequestFailed as e:
            result = [
                JSONResponse({"information": e.message}, status_code=HTTPStatus(e.status_code))
            ]
        return result

    @api.post("/emails_sent")
    def emails_sent(self) -> list[Response | Effect]:
        """Query sent emails from SendGrid with optional filters for recipient and date."""
        content = self.request.json()
        to_email = content.get("emailTo")
        on_day = content.get("onDay")
        max_logs = content.get("maxLogs")

        client = self._sendgrid_client()
        try:
            message_created_at = []
            if on_day:
                date_time = datetime.strptime(on_day, "%Y-%m-%d")
                message_created_at = [
                    CriterionDatetime(
                        date_time=date_time,
                        operation=CriterionOperation.GREATER_THAN_OR_EQUAL,
                    ),
                ]
                next_date = date_time + timedelta(days=1)
                if next_date < datetime.now():
                    message_created_at.append(
                        CriterionDatetime(
                            date_time=next_date,
                            operation=CriterionOperation.LOWER_THAN_OR_EQUAL,
                        )
                    )

            criteria = LoggedEmailCriteria(
                message_id="",
                subject="",
                to_email=to_email,
                reason="",
                status=[],
                message_created_at=message_created_at,
            )
            result = [
                JSONResponse(
                    [email.to_dict() for email in client.logged_emails(criteria, max_logs)],
                    status_code=HTTPStatus(HTTPStatus.OK),
                )
            ]
        except RequestFailed as e:
            result = [
                JSONResponse({"information": e.message}, status_code=HTTPStatus(e.status_code))
            ]
        return result

    @api.post("/send_email")
    def send_email(self) -> list[Response | Effect]:
        """Send an email via SendGrid with optional inline images and attachments."""
        content = self.request.json()
        email_from = content.get("emailFrom")
        email_to = content.get("emailTo")
        email_cc = content.get("emailCc")
        subject = content.get("subject")
        body = content.get("body")
        inline_url = content.get("inlineUrl")
        attachment_url = content.get("attachmentUrl")

        client = self._sendgrid_client()
        try:
            sender = Address(email=email_from, name="Sender")
            reply_tos = [Address(email=email_from, name="ReplyTo")]
            recipients = [
                Recipient(address=Address(email=email_to, name="RecTo"), type=RecipientType.TO)
            ]
            if email_cc:
                cc = Recipient(address=Address(email=email_cc, name="RecCc"), type=RecipientType.CC)
                recipients.append(cc)
            subject = f"{subject} - {datetime.now(UTC).strftime('%H:%M:%S')}"

            bodies = [BodyContent(type="text/plain", value=body)]
            attachments = []
            if inline_url:
                attached = Attachment.from_url_inline(
                    inline_url, {}, "inline_picture.png", "pictureId"
                )
                attachments.append(attached)
                html_body = BodyContent(
                    type="text/html",
                    value=f"<html><body>{body}<br/>"
                    '<img src="cid:pictureId" width="200px"/><br/>'
                    "Bye!</body></html>",
                )
                bodies.append(html_body)

            if attachment_url:
                attached = Attachment.from_url(attachment_url, {}, "attached_picture.png")
                attachments.append(attached)

            email = Email(
                sender=sender,
                reply_tos=reply_tos,
                recipients=recipients,
                subject=subject,
                bodies=bodies,
                attachments=attachments,
                send_at=Email.now(),
            )

            result = [
                JSONResponse(
                    {"successful": client.simple_send(email)},
                    status_code=HTTPStatus(HTTPStatus.OK),
                )
            ]
        except RequestFailed as e:
            result = [
                JSONResponse({"information": e.message}, status_code=HTTPStatus(e.status_code))
            ]
        return result

    def parser_url(self) -> str:
        """Build the URL for the inbound email parser webhook endpoint."""
        host = f"https://{self.environment[Constants.customer_identifier]}.canvasmedical.com"
        return f"{host}{Constants.plugin_api_base_route}/inbound_email"

    @api.post("/inbound_webhook")
    def inbound_webhook_toggle(self) -> list[Response | Effect]:
        """Enable or disable the SendGrid inbound parse webhook."""
        content = self.request.json()
        enabled = content.get("enabled")
        hostname = content.get("hostname")

        client = self._sendgrid_client()
        try:
            result = [JSONResponse({"enabled": enabled}, status_code=HTTPStatus(HTTPStatus.OK))]
            parser_url = self.parser_url()
            parsers = [
                parser.hostname
                for parser in client.parser_setting_list()
                if parser.url == parser_url
            ]
            if enabled and not parsers:
                setting = ParseSetting(
                    url=self.parser_url(),
                    hostname=hostname,
                    spam_check=True,
                    send_raw=False,
                )
                client.parser_setting_add(setting)
            if not enabled and parsers:
                client.parser_setting_delete(parsers[0])

        except RequestFailed as e:
            result = [
                JSONResponse({"information": e.message}, status_code=HTTPStatus(e.status_code))
            ]
        return result

    @api.get("/inbound_webhook")
    def inbound_webhook_get(self) -> list[Response | Effect]:
        """Get the current status of the inbound parse webhook configuration."""
        client = self._sendgrid_client()
        try:
            parser_url = self.parser_url()
            parsers = [
                parser for parser in client.parser_setting_list() if parser.url == parser_url
            ]
            response = {"enabled": bool(parsers), "hostname": ""}
            if parsers:
                response["hostname"] = parsers[0].hostname
            result = [JSONResponse(response, status_code=HTTPStatus(HTTPStatus.OK))]
        except RequestFailed as e:
            result = [
                JSONResponse({"information": e.message}, status_code=HTTPStatus(e.status_code))
            ]
        return result

    def webhook_url(self) -> str:
        """Build the URL for the outbound email status webhook endpoint."""
        host = f"https://{self.environment[Constants.customer_identifier]}.canvasmedical.com"
        return f"{host}{Constants.plugin_api_base_route}/outbound_email_status"

    @api.post("/outbound_webhook")
    def outbound_webhook_toggle(self) -> list[Response | Effect]:
        """Enable or disable the SendGrid outbound event webhook."""
        content = self.request.json()
        enabled = content.get("enabled")
        client = self._sendgrid_client()
        try:
            result = [JSONResponse({"enabled": enabled}, status_code=HTTPStatus(HTTPStatus.OK))]
            webhook_url = self.webhook_url()
            webhook_ids = [
                webhook.id for webhook in client.event_webhook_list() if webhook.url == webhook_url
            ]

            if enabled and not webhook_ids:
                event = EventWebhook(
                    url=webhook_url,
                    enabled=True,
                    group_resubscribe=False,
                    group_unsubscribe=False,
                    delivered=True,
                    spam_report=True,
                    bounce=True,
                    unsubscribe=False,
                    processed=True,
                    open=True,
                    click=True,
                    dropped=True,
                    friendly_name="Canvas Plugin Webhook",
                )
                client.event_webhook_add(event)
            if not enabled and webhook_ids:
                client.event_webhook_delete(webhook_ids[0])

        except RequestFailed as e:
            result = [
                JSONResponse({"information": e.message}, status_code=HTTPStatus(e.status_code))
            ]
        return result

    @api.get("/outbound_webhook")
    def outbound_webhook_get(self) -> list[Response | Effect]:
        """Get the current status of the outbound event webhook configuration."""
        client = self._sendgrid_client()
        try:
            webhook_url = self.webhook_url()
            enabled = any(
                webhook.id for webhook in client.event_webhook_list() if webhook.url == webhook_url
            )
            result = [JSONResponse({"enabled": enabled}, status_code=HTTPStatus(HTTPStatus.OK))]
        except RequestFailed as e:
            result = [
                JSONResponse({"information": e.message}, status_code=HTTPStatus(e.status_code))
            ]
        return result

    @api.get("/outbound_email_status")
    def last_outbound_status(self) -> list[Response | Effect]:
        """Retrieve the most recent outbound email status events from cache."""
        return [
            JSONResponse(
                self.cache_retrieve("outbound_email_status"), status_code=HTTPStatus(HTTPStatus.OK)
            )
        ]

    @api.post("/outbound_email_status")
    def outbound_status_save(self) -> list[Response | Effect]:
        """Receive and cache outbound email status events from SendGrid webhook."""
        events = [EmailEvent.from_dict(item) for item in self.request.json()]
        self.cache_save("outbound_email_status", [e.to_dict() for e in events])
        log.info(f"outbound status received:{len(events)}")
        return [Response(status_code=HTTPStatus(HTTPStatus.OK))]

    @api.get("/inbound_email")
    def last_inbound_email(self) -> list[Response | Effect]:
        """Retrieve the most recent inbound email from cache."""
        return [
            JSONResponse(
                self.cache_retrieve("inbound_treatment"),
                status_code=HTTPStatus(HTTPStatus.OK),
            )
        ]

    @api.post("/inbound_email")
    def inbound_email_save(self) -> list[Response | Effect]:
        """Receive and cache parsed inbound emails from SendGrid webhook."""
        form = self.request.form_data()
        message = {}
        files = []
        for key, value in form.multi_items():
            if (
                hasattr(value, "file")
                and hasattr(value, "filename")
                and hasattr(value, "content_type")
            ):
                files.append((key, value))
            else:
                if hasattr(value, "value"):
                    message[key] = value.value
                elif isinstance(value, str):
                    message[key] = value
                else:
                    message[key] = str(value)

        parsed = ParsedEmail.from_dict(message)
        self.cache_save("inbound_treatment", [parsed.to_dict()])
        log.info(f"inbound email received from {parsed.email_from} to {parsed.email_to}")
        return [Response(status_code=HTTPStatus(HTTPStatus.OK))]

    @classmethod
    def cache_save(cls, key: str, payload: list) -> None:
        """Store a payload in the plugin cache under the given key."""
        get_cache().set(key, payload)

    @classmethod
    def cache_retrieve(cls, key: str) -> list:
        """Retrieve a cached payload by key, returning an empty list if not found."""
        return get_cache().get(key) or []
```

### email_form_app.py

**Purpose**

This code defines an Application handler that launches a modal form in the right chart pane for interacting with the SendGrid email API endpoints.

```python
from email_sender.constants.constants import Constants

from canvas_sdk.effects import Effect
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from canvas_sdk.handlers.application import Application
from canvas_sdk.templates import render_to_string


class EmailFormApp(Application):
    """Application handler that displays the email sender form in a modal."""

    def on_open(self) -> Effect:
        """Render and launch the email form modal in the right chart pane."""
        content = render_to_string(
            "templates/email_form.html",
            {
                "sendEmailURL": f"{Constants.plugin_api_base_route}/send_email",
                "emailsSentURL": f"{Constants.plugin_api_base_route}/emails_sent",
                "emailEventsURL": f"{Constants.plugin_api_base_route}/email_events",
                "outboundWebhookURL": f"{Constants.plugin_api_base_route}/outbound_webhook",
                "outboundStatusesURL": f"{Constants.plugin_api_base_route}/outbound_email_status",
                "inboundWebhookURL": f"{Constants.plugin_api_base_route}/inbound_webhook",
                "inboundEmailURL": f"{Constants.plugin_api_base_route}/inbound_email",
            },
        )

        return LaunchModalEffect(
            content=content,
            target=LaunchModalEffect.TargetType.RIGHT_CHART_PANE,
        ).apply()
```

<br/>
<br/>
<br/>
