---
title: 'Twilio SMS/MMS'
slug: 'example-twilio_sms_mms'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/twilio_sms_mms' target='_blank'>View the source</a> for this plugin on GitHub." %}


## Description

Plugin that provides a SimpleAPI for sending and receiving SMS/MMS messages using the Canvas SDK's Twilio client. It supports listing phone numbers, sending messages, retrieving message history and media, managing inbound webhooks, handling delivery status callbacks, and auto-replying to inbound messages. Includes a chart application that renders a form interface for SMS management directly from the chart.

## Configuration

This example plugin defines the following "secrets" in the manifest file:

```
    "secrets": [
        "TwilioAccountSID",
        "TwilioAPIKey",
        "TwilioAPISecret"
    ],
```
Once defined in the `MANIFEST.json`, set the secrets for your plugin in the Admin UI of your Canvas EMR. [Read more](https://docs.canvasmedical.com/sdk/secrets/)

### TwilioAccountSID
Your [Twilio Account SID](https://www.twilio.com/docs/iam/api/account).

### TwilioAPIKey
Your [Twilio API Key SID](https://www.twilio.com/docs/iam/api-keys).

### TwilioAPISecret
Your [Twilio API Key Secret](https://www.twilio.com/docs/iam/api-keys).

## CANVAS_MANIFEST.json

```json
{
  "sdk_version": "0.85.0",
  "plugin_version": "0.0.1",
  "name": "twilio_sms_mms",
  "description": "use Twillio to send and receive SMS/MMS",
  "components": {
    "handlers": [
      {
        "class": "twilio_sms_mms.handlers.sms_manip:SmsManip",
        "description": "SMS/MMS with Twilio"
      }
    ],
    "applications": [
      {
        "class": "twilio_sms_mms.handlers.sms_form_app:SmsFormApp",
        "name": "SMS Twilio",
        "description": "SMS/MMS with Twilio",
        "icon": "static/twilio_sms_mms.png",
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
    "TwilioAccountSID",
    "TwilioAPIKey",
    "TwilioAPISecret"
  ],
  "tags": {},
  "references": [],
  "license": "",
  "diagram": false,
  "readme": "./README.md"
}
```

## handlers/

### sms_manip.py

**Purpose**

This code defines a SimpleAPI handler that exposes REST endpoints for managing SMS/MMS operations via the Canvas SDK's Twilio client.

**Class Overview**

- The main class, `SmsManip`, extends `StaffSessionAuthMixin` and `SimpleAPI`.
- It creates a Twilio `SmsClient` using credentials stored in plugin secrets (Account SID, API Key, API Secret).

**Main Workflow**

- `GET /phone_list` — Retrieves all phone numbers associated with the Twilio account, including capabilities and webhook configuration.
- `GET /message_list/<number>/<direction>` — Lists messages for a specific phone number filtered by direction (from/to).
- `GET /message/<message_sid>` — Retrieves details of a specific message.
- `GET /medias/<message_sid>` — Retrieves all media attachments for a specific message.
- `DELETE /message_delete/<message_sid>` — Deletes a specific message.
- `POST /sms_send` — Sends an SMS message with optional status callback URL.
- `POST /inbound_webhook/<phone_sid>` — Configures the inbound webhook URL for a Twilio phone number.
- `POST /outbound_api_status` — Handles status callbacks for outbound SMS messages.
- `POST /inbound_treatment` — Processes incoming messages and sends automatic replies with optional media.

**Twilio Client Integration**

- The `_twillio_client` method creates an `SmsClient` instance from `canvas_sdk.clients.twilio.libraries`.
- Error handling uses the `RequestFailed` exception from the Twilio client structures.
- Inbound message handling generates TwiML responses for automatic replies.

```python
from http import HTTPStatus

from canvas_sdk.clients.twilio.constants import DateOperation, HttpMethod
from canvas_sdk.clients.twilio.libraries import SmsClient
from canvas_sdk.clients.twilio.structures import (
    RequestFailed,
    Settings,
    SmsMms,
    StatusInbound,
    StatusOutboundApi,
)
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import HTMLResponse, JSONResponse, Response
from canvas_sdk.handlers.simple_api import SimpleAPI, StaffSessionAuthMixin, api
from logger import log

from ..constants.constants import Constants


class SmsManip(StaffSessionAuthMixin, SimpleAPI):
    """API handler for Twilio SMS/MMS operations."""

    PREFIX = None

    def _twillio_client(self) -> SmsClient:
        """Create and configure a Twilio SMS client."""
        settings = Settings(
            account_sid=self.secrets[Constants.twillio_account_sid],
            key=self.secrets[Constants.twillio_api_key],
            secret=self.secrets[Constants.twillio_api_secret],
        )
        return SmsClient(settings)

    @api.get("/phone_list")
    def phone_list(self) -> list[Response | Effect]:
        """Retrieve the list of phone numbers associated with the Twilio account."""
        client = self._twillio_client()
        try:
            result = [
                JSONResponse(
                    [
                        {
                            "sid": p.sid,
                            "phoneNumber": p.phone_number,
                            "label": p.friendly_name,
                            "capabilities": p.capabilities.to_dict(),
                            "statusCallback": p.status_callback,
                            "status": p.status,
                            "inboundWebhook": {
                                "url": p.sms_url,
                                "method": p.sms_method.value,
                            },
                        }
                        for p in client.account_phone_numbers()
                    ],
                    status_code=HTTPStatus(HTTPStatus.OK),
                ),
            ]
        except RequestFailed as e:
            result = [
                JSONResponse({"information": e.message}, status_code=HTTPStatus(e.status_code))
            ]
        return result

    @api.get("/message_list/<number>/<direction>")
    def message_list(self) -> list[Response | Effect]:
        """Retrieve a list of messages for a specific phone number."""
        number = self.request.path_params["number"]
        direction = self.request.path_params["direction"]
        number_from = number if direction == "from" else ""
        number_to = number if direction == "to" else ""

        client = self._twillio_client()
        try:
            result = [
                JSONResponse(
                    [
                        {
                            "sid": p.sid,
                            "sent": p.date_sent.isoformat(),
                            "status": p.status.value,
                            "mediaCount": p.count_media,
                        }
                        for p in client.retrieve_all_sms(
                            number_to, number_from, "", DateOperation.ON_EXACTLY
                        )
                    ],
                    status_code=HTTPStatus(HTTPStatus.OK),
                ),
            ]
        except RequestFailed as e:
            result = [
                JSONResponse({"information": e.message}, status_code=HTTPStatus(e.status_code))
            ]
        return result

    @api.get("/message/<message_sid>")
    def message(self) -> list[Response | Effect]:
        """Retrieve details of a specific message."""
        message_sid = self.request.path_params["message_sid"]
        client = self._twillio_client()
        try:
            result = [
                JSONResponse(
                    client.retrieve_sms(message_sid).to_dict(),
                    status_code=HTTPStatus(HTTPStatus.OK),
                ),
            ]
        except RequestFailed as e:
            result = [
                JSONResponse({"information": e.message}, status_code=HTTPStatus(e.status_code))
            ]
        return result

    @api.get("/medias/<message_sid>")
    def media_list(self) -> list[Response | Effect]:
        """Retrieve all media attachments for a specific message."""
        message_sid = self.request.path_params["message_sid"]
        client = self._twillio_client()
        try:
            result = [
                Response(
                    content_type=p.content_type,
                    content=client.retrieve_raw_media(message_sid, p.sid),
                )
                for p in client.retrieve_media_list(message_sid)
            ]
        except RequestFailed as e:
            result = [
                JSONResponse({"information": e.message}, status_code=HTTPStatus(e.status_code))
            ]
        return result

    @api.delete("/message_delete/<message_sid>")
    def message_delete(self) -> list[Response | Effect]:
        """Delete a specific message from Twilio."""
        message_sid = self.request.path_params["message_sid"]
        client = self._twillio_client()
        try:
            result = [
                JSONResponse(
                    {
                        "sid": message_sid,
                        "deleted": client.delete_sms(message_sid),
                    },
                    status_code=HTTPStatus(HTTPStatus.OK),
                )
            ]
        except RequestFailed as e:
            result = [
                JSONResponse({"information": e.message}, status_code=HTTPStatus(e.status_code))
            ]
        return result

    @api.post("/inbound_webhook/<phone_sid>")
    def inbound_webhook(self) -> list[Response | Effect]:
        """Configure the inbound webhook URL for a Twilio phone number."""
        phone_sid = self.request.path_params["phone_sid"]
        content = self.request.json()
        webhook_url = content["url"]
        method = HttpMethod(content["method"])

        client = self._twillio_client()
        try:
            response = client.set_inbound_webhook(phone_sid, webhook_url, method)
            result = [JSONResponse({"result": response}, status_code=HTTPStatus(HTTPStatus.OK))]
        except RequestFailed as e:
            result = [
                JSONResponse({"information": e.message}, status_code=HTTPStatus(e.status_code))
            ]
        return result

    @api.post("/sms_send")
    def sms_send(self) -> list[Response | Effect]:
        """Send an SMS message via Twilio."""
        content = self.request.json()
        number_from = content.get("numberFrom")
        number_from_id = content.get("numberFromSid")
        number_to = content.get("numberTo")
        callback_url = content.get("callbackUrl")
        text = content.get("text")

        client = self._twillio_client()
        try:
            sms_mms = SmsMms(
                number_from=number_from,
                number_from_sid=number_from_id,
                number_to=number_to,
                message=text,
                media_url="",
                status_callback_url=callback_url,
            )
            response = client.send_sms_mms(sms_mms)
            result = [JSONResponse(response.to_dict(), status_code=HTTPStatus(HTTPStatus.OK))]
        except RequestFailed as e:
            result = [
                JSONResponse({"information": e.message}, status_code=HTTPStatus(e.status_code))
            ]
        return result

    @api.post("/outbound_api_status")
    def outbound_api_status(self) -> list[Response | Effect]:
        """Handle status callbacks for outbound SMS messages."""
        status = StatusOutboundApi.callback_outbound_api(self.request.text())
        log.info(f"sms_extern: sid/status: {status.sms_sid}/{status.sms_status}")
        return [Response(status_code=HTTPStatus(HTTPStatus.OK))]

    @api.post("/inbound_treatment")
    def inbound_treatment(self) -> list[Response | Effect]:
        """Handle inbound SMS messages with automatic replies."""
        inbound = StatusInbound.callback_inbound(self.request.text())
        if "hello" in inbound.body.lower():
            reply = "Hello!"
            image = "<Media>https://img.freepik.com/free-psd/hand-drawn-summer-frame-illustration_23-2151631028.jpg</Media>"
        else:
            reply = "Say hello!"
            image = ""

        response = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            "<Response>"
            f"<Message><Body>{reply}</Body>{image}</Message>"
            "</Response>"
        )
        return [
            HTMLResponse(
                content=response,
                status_code=HTTPStatus(HTTPStatus.OK),
            )
        ]
```

### sms_form_app.py

**Purpose**

This code defines an Application handler that launches a modal form in the right chart pane for interacting with the Twilio SMS/MMS API endpoints.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from canvas_sdk.handlers.application import Application
from canvas_sdk.templates import render_to_string

from ..constants.constants import Constants


class SmsFormApp(Application):
    """Application handler for the SMS/MMS form interface."""

    def on_open(self) -> Effect:
        """Render and launch the SMS form modal in the right chart pane."""
        host = f"https://{self.environment[Constants.customer_identifier]}.canvasmedical.com"
        content = render_to_string(
            "templates/sms_form.html",
            {
                "smsSendURL": f"{Constants.plugin_api_base_route}/sms_send",
                "phoneListURL": f"{Constants.plugin_api_base_route}/phone_list",
                "setInboundWebhookURL": f"{Constants.plugin_api_base_route}/inbound_webhook",
                "messageListURL": f"{Constants.plugin_api_base_route}/message_list",
                "messageURL": f"{Constants.plugin_api_base_route}/message",
                "mediaURL": f"{Constants.plugin_api_base_route}/medias",
                "deleteMessageURL": f"{Constants.plugin_api_base_route}/message_delete",
                "defaultCallbackURL": f"{host}{Constants.plugin_api_base_route}/outbound_api_status",
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
