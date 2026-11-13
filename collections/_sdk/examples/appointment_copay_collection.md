---
title: 'Appointment Copay Collection'
slug: 'example-appointment_copay_collection'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/appointment_copay_collection' target='_blank'>View the source</a> for this plugin on GitHub." %}

This plugin adds an **Appointment Copays** page to the patient portal, where a patient pays the copay for an upcoming appointment with a card saved to their account. The plugin charges the card with the [`ChargeStoredCard`](/sdk/effect-charge-stored-card/) effect and posts the payment to the copay line item on the appointment's claim. Canvas records it the same way as a copay that staff collect in **Collect payment**.

## SDK Features

* Adds a patient portal menu item with a `portal_menu_item` [application](/sdk/handlers-applications/)
* Serves the page and its JSON endpoints from a [SimpleAPI](/sdk/handlers-simple-api-http/) handler authenticated with [`PatientSessionAuthMixin`](/sdk/handlers-simple-api-http/#patient-session)
* Charges a stored [PaymentCard](/sdk/data-payment-card/) as a copay on a [Claim](/sdk/data-claim/) with [`ChargeStoredCard`](/sdk/effect-charge-stored-card/#payment-allocation)
* Handles the [`REVENUE__STORED_CARD__CHARGE_RESPONSE`](/sdk/effect-charge-stored-card/#reconciling-the-charge) event and pushes the result to the open page with the [`Broadcast`](/sdk/handlers-simple-api-websocket/#broadcasting-messages) effect and a [WebSocket](/sdk/handlers-simple-api-websocket/) handler
* Reads per-visit-type copay amounts from a plugin [variable](/sdk/secrets/), with the copay on the patient's primary coverage ([`EligibilitySummary`](/sdk/data-coverage/#eligibilitysummary)) as the fallback

## How it works

1. The patient selects **Appointment Copays** in the portal menu, and the page opens.
2. The page lists the patient's upcoming appointments, leaving out canceled and no-showed ones, with the copay status of each.
3. For an appointment with a copay due, the patient chooses a saved card and pays.
4. The plugin emits `ChargeStoredCard` with the appointment's `claim_id` and `copay=True`.
5. When Canvas finishes processing the charge, the plugin pushes the result to the open page over a WebSocket.

A billable appointment has a claim from the moment it's booked, through its note (appointment → note → claim), so its copay can be paid before the visit.

## Copay amount

The plugin takes the copay amount from the first of these that has one:

1. The amount set for the appointment's note type in the `COPAY_AMOUNTS` plugin variable.
2. The copay on the patient's primary active coverage, from `EligibilitySummary.copay_cents`.

Set `COPAY_AMOUNTS` to a JSON object that maps note type codes to dollar amounts:

```json
{"office-visit": "25.00", "telehealth": "15.00"}
```

## Appointment statuses

The plugin gives each appointment one of these statuses, and the patient can pay only an appointment whose copay is due. A due appointment shows the copay amount with a card picker and a pay button, or a prompt to add a card when the patient has none saved. Every other appointment shows its status label.

| Status | When it applies |
| --- | --- |
| Due | The note type is billable, the claim exists, no copay has been posted to it yet, and the plugin has a copay amount |
| Copay paid | The claim already has a copay payment |
| No payment needed for this visit | The note type isn't billable, so the appointment has no claim |
| Payment isn't available for this visit yet | The note type is billable, but the appointment has no active claim |
| No copay on file for this visit | Neither `COPAY_AMOUNTS` nor the primary coverage has an amount |

## CANVAS_MANIFEST.json

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1",
    "name": "appointment_copay_collection",
    "description": "Patient portal page that collects an upcoming appointment's copay on a stored card and posts it to the appointment claim's COPAY line item.",
    "components": {
        "applications": [
            {
                "class": "appointment_copay_collection.applications.copay_application:CopayApplication",
                "name": "Appointment Copays",
                "description": "Opens the page where a patient pays the copay for an upcoming appointment.",
                "scope": "portal_menu_item",
                "icon": "assets/icon.png"
            }
        ],
        "handlers": [
            {
                "class": "appointment_copay_collection.handlers.copay_api:CopayAPI",
                "description": "Serves the copay page, lists upcoming appointments, and emits ChargeStoredCard effects."
            },
            {
                "class": "appointment_copay_collection.handlers.charge_response:ChargeResponseHandler",
                "description": "Pushes the stored-card charge result to the patient's open copay page."
            },
            {
                "class": "appointment_copay_collection.handlers.copay_websocket:CopayWebSocket",
                "description": "Lets a logged-in patient subscribe to their own charge-result channel."
            }
        ],
        "commands": [],
        "content": [],
        "effects": [],
        "views": []
    },
    "variables": [
        {
            "name": "COPAY_AMOUNTS",
            "default": "{}"
        }
    ],
    "tags": {},
    "references": [],
    "license": "",
    "diagram": false,
    "readme": "./README.md"
}
```

## applications/

### copay_application.py

`CopayApplication` registers the **Appointment Copays** menu item. When the patient opens it, `on_open` returns a `LaunchModalEffect` that shows the copay page as a full portal page.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from canvas_sdk.handlers.application import Application


class CopayApplication(Application):
    """Patient portal menu item that opens the appointment copay page."""

    def on_open(self) -> Effect:
        """Open the copay page as a full portal page."""
        return LaunchModalEffect(
            url="/plugin-io/api/appointment_copay_collection/portal/page",
            target=LaunchModalEffect.TargetType.PAGE,
        ).apply()
```

## handlers/

### copay_api.py

`CopayAPI` is a SimpleAPI handler with the `/portal` prefix. It uses `PatientSessionAuthMixin` and reads the ID of the patient whose chart the request acts on from the `canvas-logged-in-user-id` request header, so every lookup is scoped to that patient.

With [family portal access](/sdk/patient-portal/#family-portal-access), a family member using the portal on the patient's chart can use the page with view access to the chart's appointments and billing, which `PORTAL_ACCESS` declares for every route. The pay endpoint declares its own `portal_access` and also requires act access to billing. See [Family portal access](/sdk/handlers-simple-api-http/#family-portal-access).

**Endpoints**

- `GET /portal/page`: Renders the page, passing in the name of the patient's WebSocket channel.
- `GET /portal/copay.js` and `GET /portal/copay.css`: Serve the page's script and styles.
- `GET /portal/appointments`: Returns the patient's upcoming appointments, each with its status and copay amount, and the patient's saved cards with the default card first.
- `POST /portal/appointments/<appointment_id>/pay`: Takes a `payment_card_id` in the JSON body and charges that card for the appointment's copay.

The page sends only the appointment and the card. The pay endpoint works out the amount and the claim again on the server for every payment, and responds with `202 Accepted` along with the `ChargeStoredCard` effect:

- `claim_id` is the appointment's claim, and `copay` is `True`, so the payment is posted to the claim's copay line item.
- `idempotency_key` is a `uuid5` built from the appointment, card, and amount. A repeated submission of the same payment uses the same key, so the processor treats it as a retry of one charge. See [Idempotency](/sdk/effect-charge-stored-card/#idempotency).
- `description` is `"Appointment copay"`.

The response body carries the `idempotency_key`, which the page uses to match the charge result when it arrives.

```python
from decimal import Decimal
from http import HTTPStatus
from typing import Any

from appointment_copay_collection.handlers.charge_response import channel_for
from appointment_copay_collection.services.copay import (
    COPAY_AMOUNTS_VARIABLE,
    CopayStatus,
    charge_idempotency_key,
    copay_rows,
    parse_copay_amounts,
    stored_cards,
)
from canvas_sdk.effects import Effect
from canvas_sdk.effects.payment import ChargeStoredCard
from canvas_sdk.effects.simple_api import HTMLResponse, JSONResponse, Response
from canvas_sdk.handlers.simple_api import (
    PatientSessionAuthMixin,
    PortalAccessLevel,
    SimpleAPI,
    api,
)
from canvas_sdk.templates import render_to_string


def _appointment_json(row: dict[str, Any]) -> dict[str, Any]:
    """Serialize one copay row for the page."""
    appointment = row["appointment"]
    provider = appointment.provider
    return {
        "id": str(appointment.id),
        "start_time": appointment.start_time.isoformat(),
        "duration_minutes": appointment.duration_minutes,
        "visit_type": appointment.note_type.name if appointment.note_type else None,
        "provider": f"{provider.first_name} {provider.last_name}" if provider else None,
        "location": appointment.location.full_name if appointment.location else None,
        "status": row["status"],
        "amount": str(row["amount"]) if row["amount"] is not None else None,
    }


class CopayAPI(PatientSessionAuthMixin, SimpleAPI):
    """Serve the copay page and charge a stored card for an appointment's copay.

    Every request acts on one patient's chart, and every lookup is scoped to that patient, so a
    patient can only see and pay for their own appointments. A family member acting on the chart
    needs view access to its appointments and billing to use the page, and act access to its
    billing to pay.
    """

    PREFIX = "/portal"
    PORTAL_ACCESS = {"appointments": PortalAccessLevel.VIEW, "billing": PortalAccessLevel.VIEW}

    @property
    def patient_id(self) -> str:
        """The id of the patient whose chart the request acts on."""
        return self.request.headers["canvas-logged-in-user-id"]

    def _configured_amounts(self) -> dict[str, Decimal]:
        return parse_copay_amounts(self.secrets.get(COPAY_AMOUNTS_VARIABLE))

    @api.get("/page")
    def page(self) -> list[Response | Effect]:
        """Serve the copay page."""
        return [
            HTMLResponse(
                render_to_string("templates/copay.html", {"channel": channel_for(self.patient_id)}),
                status_code=HTTPStatus.OK,
            )
        ]

    @api.get("/copay.js")
    def script(self) -> list[Response | Effect]:
        """Serve the page's script."""
        return [
            Response(
                render_to_string("templates/copay.js").encode(),
                status_code=HTTPStatus.OK,
                content_type="text/javascript",
            )
        ]

    @api.get("/copay.css")
    def styles(self) -> list[Response | Effect]:
        """Serve the page's styles."""
        return [
            Response(
                render_to_string("templates/copay.css").encode(),
                status_code=HTTPStatus.OK,
                content_type="text/css",
            )
        ]

    @api.get("/appointments")
    def appointments(self) -> list[Response | Effect]:
        """List the patient's upcoming appointments with their copay, plus their stored cards."""
        rows = copay_rows(self.patient_id, self._configured_amounts())
        return [
            JSONResponse(
                {
                    "appointments": [_appointment_json(row) for row in rows],
                    "cards": stored_cards(self.patient_id),
                },
                status_code=HTTPStatus.OK,
            )
        ]

    @api.post(
        "/appointments/<appointment_id>/pay",
        portal_access={"appointments": PortalAccessLevel.VIEW, "billing": PortalAccessLevel.ACT},
    )
    def pay(self) -> list[Response | Effect]:
        """Charge the chosen stored card for the appointment's copay.

        The amount and the claim are recomputed here rather than taken from the request, so the
        page cannot change what is charged or where it is posted. The charge result arrives
        later as a REVENUE__STORED_CARD__CHARGE_RESPONSE event.
        """
        appointment_id = self.request.path_params["appointment_id"]
        body = self.request.json()
        payment_card_id = body.get("payment_card_id") if isinstance(body, dict) else None

        rows = copay_rows(self.patient_id, self._configured_amounts())
        row = next((r for r in rows if str(r["appointment"].id) == appointment_id), None)
        if row is None:
            return [
                JSONResponse({"error": "Appointment not found."}, status_code=HTTPStatus.NOT_FOUND)
            ]
        if row["status"] != CopayStatus.DUE:
            return [
                JSONResponse(
                    {"error": "This appointment has no copay to pay.", "status": row["status"]},
                    status_code=HTTPStatus.CONFLICT,
                )
            ]
        if not isinstance(payment_card_id, str) or payment_card_id not in {
            card["id"] for card in stored_cards(self.patient_id)
        }:
            return [
                JSONResponse(
                    {"error": "Choose one of your saved cards."},
                    status_code=HTTPStatus.BAD_REQUEST,
                )
            ]

        amount = row["amount"]
        idempotency_key = charge_idempotency_key(appointment_id, payment_card_id, amount)
        return [
            JSONResponse(
                {"idempotency_key": str(idempotency_key), "amount": str(amount)},
                status_code=HTTPStatus.ACCEPTED,
            ),
            ChargeStoredCard(
                patient_id=self.patient_id,
                payment_card_id=payment_card_id,
                amount=amount,
                idempotency_key=idempotency_key,
                claim_id=str(row["claim"].id),
                copay=True,
                description="Appointment copay",
            ).apply(),
        ]
```

### charge_response.py

`ChargeResponseHandler` responds to `REVENUE__STORED_CARD__CHARGE_RESPONSE`. It broadcasts the outcome to the charged patient's channel, `copay-<patient_id>`, so the open page can show whether the payment went through.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import Broadcast
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


def channel_for(patient_id: str) -> str:
    """Return the WebSocket channel a patient's copay page listens on."""
    return f"copay-{patient_id}"


class ChargeResponseHandler(BaseHandler):
    """Push the result of a stored-card charge to the patient's open copay page.

    The page matches the result to its pending payment by idempotency key.
    """

    RESPONDS_TO = EventType.Name(EventType.REVENUE__STORED_CARD__CHARGE_RESPONSE)

    def compute(self) -> list[Effect]:
        """Broadcast the charge result on the patient's channel."""
        context = self.event.context
        patient_id = context.get("patient_id")
        if not patient_id:
            return []

        error = context.get("error") or {}
        return [
            Broadcast(
                channel=channel_for(patient_id),
                message={
                    "event_type": "charge_response",
                    "idempotency_key": context.get("idempotency_key"),
                    "success": bool(context.get("success")),
                    "amount": context.get("amount"),
                    "error_code": error.get("code"),
                },
            ).apply()
        ]
```

### copay_websocket.py

`CopayWebSocket` is a `WebSocketAPI` handler. Its `authenticate` method accepts a patient session connecting to the channel of the chart it acts on, the same `copay-<patient_id>` channel that `ChargeResponseHandler` broadcasts on. Its `PORTAL_ACCESS` lets a family member connect with the same access the page needs.

```python
from appointment_copay_collection.handlers.charge_response import channel_for
from canvas_sdk.handlers.simple_api import PortalAccessLevel
from canvas_sdk.handlers.simple_api.websocket import WebSocketAPI


class CopayWebSocket(WebSocketAPI):
    """Let a session subscribe to the charge results of the chart it acts on, and no other.

    A family member acting on the chart needs the access the copay page needs.
    """

    PORTAL_ACCESS = {"appointments": PortalAccessLevel.VIEW, "billing": PortalAccessLevel.VIEW}

    def authenticate(self) -> bool:
        """Accept only a patient session connecting to the channel of the chart it acts on."""
        user = self.websocket.logged_in_user
        return (
            user is not None
            and user["type"] == "Patient"
            and self.websocket.channel == channel_for(user["id"])
        )
```

## services/

### copay.py

This module holds the logic the API handler uses:

- Parses `COPAY_AMOUNTS`, skipping entries whose amount isn't a positive number.
- Looks up the copay on the patient's primary, active, in-use coverage.
- Lists upcoming appointments, finds the newest active claim on each appointment's note, and checks the claims for an existing copay [`PatientPosting`](/sdk/data-posting/#patientposting) to set each appointment's status.
- Builds the idempotency key for a charge.
- Lists the patient's saved cards.

## templates/

### copay.html, copay.js, and copay.css

The page lists the appointments, offers a card picker and a pay button for each appointment with a copay due, and opens a WebSocket to the patient's channel. When a result arrives with the idempotency key of the pending payment, the page shows whether it succeeded. If no result arrives in time, the page tells the patient the payment is still processing.

<br/>
<br/>
<br/>
