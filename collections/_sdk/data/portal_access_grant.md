---
title: "PortalAccessGrant"
slug: "data-portal-access-grant"
excerpt: "Read who was given family portal access to a patient's chart and what each grant allows"
hidden: false
---

## Introduction

The `PortalAccessGrant` model represents [family portal access](/sdk/patient-portal/#family-portal-access) to a patient's chart. Staff give a grant to a family member or another representative from one of the patient's contacts. The grant names the portal login it was given to and its access level in each area of the chart: appointments, messaging, clinical, and billing.

Use it to show a patient or staff member who has access to a chart, to show a family member which charts they can use, or to read what a grant allows.

Each area's level is `"none"`, `"view"`, or `"act"`. Follow the level on your portal pages the way the built-in pages do:

| Level  | On a portal page                       |
| ------ | -------------------------------------- |
| `none` | Hide the area                          |
| `view` | Show the area without its actions      |
| `act`  | Show the area and allow its actions    |

To compare levels, wrap one in `PortalAccessLevel` from `canvas_sdk.handlers.simple_api`. Levels compare in order from `NONE` to `ACT`.

A revoked or flagged grant stays as a record. A grant gives its login the chart only while `revoked_at` and `flagged_at` are both empty and the patient is active.

## Basic usage

To list the logins that currently have access to a patient's chart, filter the patient's grants:

```python
from canvas_sdk.v1.data import PortalAccessGrant

grants = PortalAccessGrant.objects.filter(
    patient__id="d7af3e356368446c85b40a5d6ff7288e",
    revoked_at__isnull=True,
    flagged_at__isnull=True,
)
```

The same grants are on the patient as `patient.portal_grants`, and the grants given to a login are on its [CanvasUser](/sdk/data-canvasuser/#user) as `portal_grants`.

## Reading the grant for a portal request

In a [SimpleAPI](/sdk/handlers-simple-api-http/#session) handler or [WebSocket API](/sdk/handlers-simple-api-websocket/#websocket-object), `portal_access.grant` is the grant that gives the acting family member or representative the chart. It's `None` on a patient's own chart.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import PatientSessionAuthMixin, SimpleAPIRoute


class AccessSummary(PatientSessionAuthMixin, SimpleAPIRoute):
    PATH = "/access-summary"
    PORTAL_ACCESS = {}

    def get(self) -> list[Response | Effect]:
        grant = self.request.portal_access.grant
        if grant is None:
            return [JSONResponse({"own_chart": True})]

        return [
            JSONResponse(
                {
                    "own_chart": False,
                    "relationship": grant.contact_relationship,
                    "billing": grant.billing,
                }
            )
        ]
```

## Reading the grant for a portal event

Portal events and `portal_menu_item` [applications](/sdk/handlers-applications/) name the chart's patient and the acting login separately. The event's target, or the `user` in an application's context, is the patient whose chart the portal is open on, and `self.event.actor` is the login. Look up the grant from both:

```python
from canvas_sdk.v1.data import PortalAccessGrant


def current_grant(actor, patient_id):
    return PortalAccessGrant.objects.filter(
        user=actor.instance,
        patient__id=patient_id,
        revoked_at__isnull=True,
    ).first()
```

Call it as `current_grant(self.event.actor, patient_id)` from your handler. It returns `None` when the login is the patient's own.

## Attributes

### PortalAccessGrant

| Field Name           | Type                                                              | Description                                                                         |
| -------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| id                   | UUID                                                              |                                                                                     |
| dbid                 | Integer                                                           |                                                                                     |
| created              | DateTime                                                          |                                                                                     |
| modified             | DateTime                                                          |                                                                                     |
| patient              | [Patient](/sdk/data-patient/#patient)                             | The patient whose chart the grant gives access to                                   |
| user                 | [CanvasUser](/sdk/data-canvasuser/#user)                          | The portal login the grant was given to                                             |
| contact              | [PatientContactPerson](/sdk/data-patient/#patientcontactperson)   | The patient's contact the grant was given from. Empty after the contact is deleted. |
| contact_name         | String                                                            | The contact's name, kept after the contact is deleted                               |
| contact_relationship | String                                                            | The contact's relationship to the patient, kept after the contact is deleted        |
| appointments         | String                                                            | Access level in appointments: `none`, `view`, or `act`                              |
| messaging            | String                                                            | Access level in messaging: `none`, `view`, or `act`                                 |
| clinical             | String                                                            | Access level in clinical records: `none`, `view`, or `act`                          |
| billing              | String                                                            | Access level in billing: `none`, `view`, or `act`                                   |
| dob_verified_at      | DateTime                                                          | When the login confirmed the patient's date of birth                                |
| dob_failed_attempts  | Integer                                                           | How many date of birth entries didn't match                                         |
| flagged_at           | DateTime                                                          | When the login reported that they don't know the patient                            |
| granted_by           | [Staff](/sdk/data-staff/#staff)                                   | The staff member who gave the grant                                                 |
| granted_at           | DateTime                                                          | When the grant was given                                                            |
| notified_at          | DateTime                                                          | When the login was notified of the grant                                            |
| revoked_at           | DateTime                                                          | When the grant was revoked                                                          |
| revoked_by           | [Staff](/sdk/data-staff/#staff)                                   | The staff member who revoked the grant                                              |
| revoke_reason        | String                                                            | The reason given for revoking the grant                                             |

<br/>
<br/>
<br/>
