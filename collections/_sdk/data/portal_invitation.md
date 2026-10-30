---
title: "PortalInvitation"
slug: "data-portal-invitation"
excerpt: "A patient portal invite or password reset link, with when it was opened, claimed, or refused."
hidden: false
---

The `PortalInvitation` model represents a patient portal invite or password reset link that Canvas created for a user. Canvas creates one each time it sends a portal link, including through [Send Invite](/sdk/patient-portal/#send-invite), and each time a plugin mints a link with [`patient_portal_http.get_login_url()`](/sdk/utils/#getting-a-patient-portal-login-link). The user is usually a patient, or a representative's login when a patient shares portal access. Use it to see whether a patient opened their link, set a password with it, or let it expire, and to find patients who need a new link.

The model records the link's history, not the link: you can't read its URL from it. To react to a link as its state changes, handle the [portal invitation events](/sdk/events/#portal-invitations).

## Basic usage

To get an invitation by identifier, use the `get` method on the `PortalInvitation` model manager:

```python
from canvas_sdk.v1.data import PortalInvitation

invitation = PortalInvitation.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")
```

A user's invitations are available from the [CanvasUser](/sdk/data-canvasuser/) through the `portal_invitations` accessor:

```python
from canvas_sdk.v1.data import Patient

patient = Patient.objects.get(id="b80b1cdc2e6a4aca90ccebc02e683f35")

invitations = patient.user.portal_invitations.order_by("-created")
```

## Filtering

Invitations can be filtered by any attribute that exists on the model.

### By status

Filter on `status` with a [PortalInvitationStatus](#portalinvitationstatus) value. For example, to find links that expired before the patient ever opened them:

```python
from canvas_sdk.v1.data import PortalInvitation, PortalInvitationStatus

expired_unopened = PortalInvitation.objects.filter(
    status=PortalInvitationStatus.EXPIRED, first_opened_at__isnull=True
)
```

### Links a patient can still use

`is_redeemable` is true while a link hasn't been claimed and hasn't expired. Check it before you send a patient another link:

```python
from canvas_sdk.v1.data import Patient

patient = Patient.objects.get(id="b80b1cdc2e6a4aca90ccebc02e683f35")

has_live_link = patient.user.portal_invitations.filter(is_redeemable=True).exists()
```

## Status

Each invitation has one `status`, chosen in this order:

1. `claimed` when the link was used to set a password.
2. `expired` when the link has passed `expires_at` or can no longer be used. A link that expired after the patient opened it stays `expired`; check `first_opened_at` to tell the two apart.
3. `opened` when the patient opened the link at least once.
4. `pending` otherwise.

Links created before Canvas recorded claims have no `claimed_at`, so a link of that age that was used to set a password shows `expired`.

A link that Canvas couldn't use when someone opened it records the time and reason in `last_rejected_at` and `last_rejection_reason`. Those fields don't change `status`, `first_opened_at`, or `is_redeemable`.

## Attributes

### PortalInvitation

| Field Name                 | Type                                                                    | Description                                                                          |
|----------------------------|-------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| id                         | UUID                                                                    | The `target` ID on [portal invitation events](/sdk/events/#portal-invitations)       |
| created                    | DateTime                                                                | When the link was created                                                            |
| modified                   | DateTime                                                                |                                                                                      |
| user                       | [CanvasUser](/sdk/data-canvasuser/)                                     | The user the link signs in                                                           |
| expires\_at                | DateTime                                                                | When the link stops working                                                          |
| first\_opened\_at          | DateTime                                                                | When the link was first opened successfully, or `None` if it never was               |
| first\_opened\_user\_agent | String                                                                  | The browser user agent of that first open, or `None`                                 |
| claimed\_at                | DateTime                                                                | When the link was used to set a password, or `None`                                  |
| last\_rejected\_at         | DateTime                                                                | When Canvas last couldn't use the link after it was opened, or `None`                |
| last\_rejection\_reason    | [PortalInvitationRejectionReason](#portalinvitationrejectionreason)     | Why Canvas last couldn't use the link, or `None`                                     |
| status                     | [PortalInvitationStatus](#portalinvitationstatus)                       | See [Status](#status)                                                                |
| is\_redeemable             | Boolean                                                                 | Whether the link can still be used: not claimed and not expired                      |

## Enumeration types

### PortalInvitationStatus

| Value   | Label   |
|---------|---------|
| pending | Pending |
| opened  | Opened  |
| claimed | Claimed |
| expired | Expired |

### PortalInvitationRejectionReason

| Value              | Label             | Description                                                 |
|--------------------|-------------------|-------------------------------------------------------------|
| expired            | Expired           | The link had expired when it was opened                     |
| different\_account | Different account | Another account was signed in on the browser that opened it |

<br/>
<br/>
<br/>
