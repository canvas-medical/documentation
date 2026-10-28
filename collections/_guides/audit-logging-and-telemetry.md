---
title: "Audit Logging and Telemetry"
---

Canvas records an attributed audit trail of activity in your instance and makes it
available to you through several export paths. This page describes what is captured, how
long it is retained, and how to get it out — whether for an internal investigation, a
compliance review, or ingestion into your own SIEM.

## What is captured

Canvas maintains a per-record audit trail. Each entry identifies the record type acted
on, the action taken, the acting user, the patient context where applicable, and a UTC
timestamp.

| Action | Captured | Granularity |
| --- | --- | --- |
| Create | Yes | Per record, per model, attributed to the acting user |
| Edit or change | Yes | Per record, with full authorship history |
| Delete, void, or enter-in-error | Yes | Per record, covering hard deletion, soft deletion, and marking entered-in-error |
| Print | Yes | Every printed document, attributed to the user who printed it |
| Chart access | Yes | Chart-open events, attributed to the user opening the chart |

Individual record reads within an already-opened chart are not enumerated separately;
chart access is recorded at the point the chart is opened.

### Print events

Printing discloses patient information, so Canvas records every print. Recorded
documents include notes, After Visit Summaries, letters, appointment lists, claim forms,
and superbills. Patient receipts and ledgers, insurance cards, and cash reconciliation
reports are recorded too. So are full chart exports that a plugin requests on a staff
member's behalf. When a patient downloads the After Visit Summary of their own visit from
the patient portal, Canvas records a download attributed to that patient.

Each print event records the document printed, its identifier, the acting user, the
patient in context, and a UTC timestamp. Some documents, such as appointment lists and
cash reconciliation reports, are not about a single patient, so their events have no
patient. If Canvas cannot record the event, the print fails and the document is not
delivered.

Opening a fax preview is recorded as a fax preview rather than a print. Sending the fax
does not record a separate print event.

Alongside the record audit trail, Canvas captures:

- **Authentication events** — sign-in successes and failures, account lockouts, and Canvas
  administrators starting and ending a session as another user.
- **Refused requests** — requests and GraphQL operations refused for lack of permission,
  attributed to the user who was refused.
- **Administrative activity** — configuration and permission changes, surfaced in the
  admin console and protected there against edit and deletion.
- **Staff activity reports** — generated nightly.

### Change history through FHIR Provenance

Authorship and change history are also exposed as FHIR `Provenance` resources across
supported resource types, giving you a queryable record of who created or revised a
resource and when. See the [Provenance API](/api/provenance/) reference for supported
resource types and query parameters.

Clinical notes additionally carry in-application revision history, visible to users
directly in the chart.

## Retention

Audit records are retained in the live, queryable index for **90 days**. Older indices
are archived to durable object storage and remain recoverable well beyond that window.
If you require retrieval of archived records, contact Canvas support with the date range
you need.

Retention requirements that exceed the live window are best served by exporting on a
schedule into your own retention tier — see the export paths below.

## Viewing the audit trail in the application

Authorized users can browse the audit trail in a filterable, searchable, read-only view
built into the application. It surfaces recorded events without allowing any change to
them.

The view is enabled per instance by Canvas; contact Canvas to turn it on for your
instance. Once enabled, access still requires an explicit permission that no default role
carries, so a customer administrator must grant it intentionally.

This view reviews audit data in place; it does not extract or export anything. To get
audit data out of Canvas, see the paths below.

## Getting audit data out

Five supported paths exist today. Which one fits depends on whether you need a
point-in-time extract, an ongoing feed, or ad-hoc investigation.

| Path | Best for | Interface |
| --- | --- | --- |
| Audit Report export | Point-in-time extract of administrative and record-level audit events | Admin console |
| [FHIR Provenance API](/api/provenance/) | Authorship and change history for specific resources | FHIR API |
| FHIR Bulk Data export | Large-scale structured extraction | FHIR API — see [Electronic Health Information (EHI) Export](/documentation/ehi-export/) |
| Read-only replica database | Ad-hoc investigation, custom reporting, scheduled ingestion | SQL |
| Streaming to a SIEM | Continuous security monitoring in your own SIEM | HTTPS push |

### Audit Report export

The Audit Report is generated from the admin console and exports the audit trail for a
selected date range. This is the most direct route to the record-level events described
above, including chart access and print events.

For print events, the report shows the document type as the data accessed and `print` or
`faxpreview` as the action. When an event has no patient in context, the patient columns
read `N/A`.

For a staff account created or a change to staff access, the report names the administrator
who made the change.

{% include alert.html type="warning" content="Audit Report access is permission-based. If you need access, your internal administrators can work with Canvas support to assign it to the appropriate groups." %}

### Read-only replica database

Instances can be provisioned with a read-only replica for direct SQL access. This is the
most flexible path for building custom audit reporting with your own SQL queries, and for
ad-hoc or scheduled extraction into an external system. For continuous security
monitoring, use the SIEM export below instead.

### Streaming to a SIEM

Canvas pushes audit events to an HTTPS endpoint you control. Events use the Open
Cybersecurity Schema Framework (OCSF) schema — an open, vendor-neutral format that SIEMs
understand — and are delivered as batched newline-delimited JSON (NDJSON).

The endpoint must be an `https://` URL whose host resolves only to public internet
addresses, not to private, loopback, or link-local ones. The URL can't contain a
username, password, or backslash; Canvas sends credentials in a request header instead.
If the URL doesn't meet these requirements, Canvas sends nothing and holds events until
the URL is corrected. Canvas doesn't follow redirects, so the endpoint must accept the POST
at the configured URL. A redirect response counts as a failed delivery, and Canvas retries
the batch later.

Delivery is at-least-once, so the receiving system must tolerate occasional duplicate
events. "Delivered" means your endpoint accepted the batch with an HTTP 2xx response; it
is not a guarantee that every event became queryable in your SIEM. Reconcile against the
events you actually receive.

Delivery is also durable: Canvas stores each audit event and keeps trying to deliver it,
retrying when your endpoint is temporarily unreachable, so a brief outage at your end does
not immediately drop events from the feed. If you suspect a gap in what your SIEM
received, the same events are retained in Canvas (see [Retention](#retention) above) and
remain available through the other audit paths on this page, so you can reconcile or
recover them there. If a delivery problem persists, contact Canvas.

The export never includes patient names, dates of birth, or clinical values — only opaque
identifiers, booleans, and enumerated values. Identifiers are direct Canvas identifiers by
default, or pseudonymized on request.

{% include alert.html type="info" content="The SIEM export is opt-in and enabled per instance by Canvas — it is not a self-serve toggle. Request it through your Canvas representative, who sets up your destination endpoint and the credentials Canvas presents to it." %}

#### Event format

Each request to your endpoint is a `POST` with `Content-Type: application/x-ndjson`, carrying
up to 500 events by default, one JSON object per line. Every body ends with a newline, so
successive bodies appended to one file read as a single NDJSON stream. Events follow OCSF 1.1.0.

| Field | Meaning |
| --- | --- |
| `metadata.uid` | Unique id for the event. Delivery is at-least-once, so use it to drop duplicates. |
| `metadata.correlation_uid` | Id of the request that produced the event, when there was one. Events from the same request share it. |
| `metadata.version` | OCSF schema version. |
| `metadata.tenant_uid` | The Canvas instance that produced the event, so one SIEM can take events from several instances. |
| `metadata.labels` | `environment:production` for a production instance, `environment:non-production` for a sandbox or test instance. |
| `category_uid`, `class_uid`, `activity_id`, `type_uid` | OCSF classification of the event (see the table below). `type_uid` is `class_uid * 100 + activity_id`. |
| `time` | When the event happened, in milliseconds since the Unix epoch (UTC). |
| `status_id` | Outcome: `1` success, `2` failure. |
| `status_code` | Why an event failed: `invalid_credentials` or `account_locked` on a sign-in, `403` on a refused request, `permission_denied` on a refused GraphQL operation, and the WebSocket close code (`4401` or `4403`) on a refused GraphQL websocket connection. Absent on success. |
| `api.operation` | On a refused request, the operation that was refused: the HTTP method and the URL pattern the request matched (`GET api/Patient/(?P<key>[a-f0-9]{32})$`), or `graphql`, the operation type (`query`, `mutation`, or `subscription`), and the top-level field when the refusal comes from one (`graphql mutation updateNoteBody`), or `WEBSOCKET` and the websocket route. A request refused by the instance's network filter has the HTTP method followed by `network filter` (`GET network filter`), a `null` actor, and the refused client address in `src_endpoint.ip`. Never the actual path or its arguments. |
| `actor.user.uid`, `actor.user.name` | Canvas user id and username of the acting user. On a failed sign-in or lockout, `uid` is `null` and `name` is the username that was tried. Both are `null` when no signed-in user caused the event. While a Canvas administrator is acting as another user, this is the user being acted as, except on staff account and access changes (see below). |
| `actor.invoked_by` | The plugin whose action caused the event. Absent when a user acted directly. |
| `src_endpoint.ip`, `src_endpoint.user_agent` | Client address and browser or client identifier. Both are `null` when the event didn't come from a client request. |
| `resources` | What the event acted on: the patient (`type` `patient`) and the record, typed by its Canvas resource name. The patient `uid` is the patient key, the same id the FHIR API uses for the Patient. A record `uid` is Canvas's internal record id, which differs from the record's FHIR resource id. On an update to a clinical record, the record's `data.changed_fields` lists the names of the fields that changed; values are never included. |
| `enrichments` | Canvas detail. `source` is `authentication`, `activity_log`, `provenance`, or `access_control`; `event_name` names the Canvas action; `impersonated_by` is the username of the administrator behind a session as another user (`id:` followed by the administrator's user id if the username can't be read), on every event that session writes except those whose `actor` is that administrator; `operator` is the email address of the Canvas support person behind a session as `root`, the account Canvas support shares, on every event that session writes, including while it acts as another user; `plugin_handler` names the plugin handler alongside `actor.invoked_by`; `payload` carries extra identifiers; `payload_withheld` lists the names of payload fields left out because they can contain names or free text. |

| `class_uid` | OCSF class | Canvas events |
| --- | --- | --- |
| 3001 | Account Change | Staff account created |
| 3002 | Authentication | Sign-in, sign-out, failed sign-in, account lockout, patient portal sign-in link issued, an administrator starting or ending a session as another user |
| 3005 | User Access Management | Staff access granted or revoked |
| 6001 | Web Resources Access | Chart opened, note printed |
| 6003 | API Activity | Clinical records and the patient record created, updated, or deleted; coverage, address, patient location, facility address, and care team changes; requests refused for lack of permission |

`activity_id` values depend on the class. In Authentication, `1` is a sign-in attempt, including
failed sign-ins, lockouts, issued portal sign-in links, and the start of a session as another
user, and `2` is a sign-out or the end of one. In User Access Management, `1` grants access and
`2` revokes it. In the other classes, `1` is create, `2` is read, including a refused GraphQL
query or subscription, `3` is update, `4` is delete, and `99` is a refused GraphQL mutation or websocket connection.
A refused request whose operation type can't be determined has `0`. Marking a clinical record
entered in error is reported as a delete.

On a staff account created or a change to staff access, `actor` is the administrator who made
the change and `resources` holds the account changed. This holds during a session as another
user too: `actor` is the administrator, not the user being acted as. A change made outside a signed-in
session, such as a directory sync, has a `null` actor. When an administrator starts a session
as another user, `actor` is the administrator and `resources` holds the user taken over, with
`event_name` `impersonation.started` (and `impersonation.ended` when the session returns to
the administrator).

With pseudonymized identifiers, `resources[].uid` values are per-customer HMAC-SHA256
tokens (64 hex characters) in place of Canvas identifiers, and `enrichments.payload` and
`enrichments.payload_withheld` are omitted. `changed_fields` is kept, since it holds only
field names.

#### Example events

The examples below are formatted across several lines for reading; each arrives on a single
line. Identifiers and addresses are illustrative.

A failed sign-in:

```json
{
  "metadata": {
    "version": "1.1.0",
    "uid": "6be79fea-caa8-40e1-a480-9c86e2b243f4",
    "product": {"name": "Canvas", "vendor_name": "Canvas Medical"},
    "tenant_uid": "acme",
    "labels": ["environment:production"],
    "correlation_uid": "7a1c3e5f9b2d4f6a8c0e1b3d5f7a9c2e"
  },
  "category_uid": 3,
  "class_uid": 3002,
  "activity_id": 1,
  "type_uid": 300201,
  "time": 1791999125000,
  "actor": {"user": {"uid": null, "name": "jsmith"}},
  "src_endpoint": {
    "ip": "203.0.113.24",
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15"
  },
  "status_id": 2,
  "status_code": "invalid_credentials",
  "enrichments": {"source": "authentication"}
}
```

A staff member opening a patient's chart:

```json
{
  "metadata": {
    "version": "1.1.0",
    "uid": "b7f9f925-646d-4607-ac71-36f5708565ca",
    "product": {"name": "Canvas", "vendor_name": "Canvas Medical"},
    "tenant_uid": "acme",
    "labels": ["environment:production"],
    "correlation_uid": "f32eec1863c3dda8afea21ba0cb39a9d"
  },
  "category_uid": 6,
  "class_uid": 6001,
  "activity_id": 2,
  "type_uid": 600102,
  "time": 1791999185000,
  "actor": {"user": {"uid": "412", "name": "jsmith"}},
  "src_endpoint": {
    "ip": "203.0.113.24",
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15"
  },
  "status_id": 1,
  "resources": [{"type": "patient", "uid": "381bf94ac3b269eedec9dc3f660a4cf0"}],
  "enrichments": {"source": "activity_log", "event_name": "chart_access"}
}
```

An update to a condition on that patient's chart:

```json
{
  "metadata": {
    "version": "1.1.0",
    "uid": "98e8a792-dd0f-4d4e-909e-94653f2af09c",
    "product": {"name": "Canvas", "vendor_name": "Canvas Medical"},
    "tenant_uid": "acme",
    "labels": ["environment:production"],
    "correlation_uid": "0c5d1f7a9e2b4c6d8f1a3b5c7d9e0f12"
  },
  "category_uid": 6,
  "class_uid": 6003,
  "activity_id": 3,
  "type_uid": 600303,
  "time": 1791999302000,
  "actor": {"user": {"uid": "412", "name": "jsmith"}},
  "src_endpoint": {
    "ip": "203.0.113.24",
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15"
  },
  "status_id": 1,
  "resources": [
    {"type": "patient", "uid": "381bf94ac3b269eedec9dc3f660a4cf0"},
    {
      "type": "Condition",
      "uid": "52817",
      "data": {"changed_fields": ["clinical_status", "committer"]}
    }
  ],
  "enrichments": {"source": "provenance"}
}
```

A request refused for lack of permission:

```json
{
  "metadata": {
    "version": "1.1.0",
    "uid": "3d0b8f4e-2a61-4c7e-9f15-6e8a2c4b7d90",
    "product": {"name": "Canvas", "vendor_name": "Canvas Medical"},
    "tenant_uid": "acme",
    "labels": ["environment:production"],
    "correlation_uid": "5e7a9c1b3d5f7a9c2e4b6d8f0a2c4e6b"
  },
  "category_uid": 6,
  "class_uid": 6003,
  "activity_id": 2,
  "type_uid": 600302,
  "time": 1791999411000,
  "actor": {"user": {"uid": "418", "name": "mlee"}},
  "src_endpoint": {
    "ip": "198.51.100.7",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
  },
  "status_id": 2,
  "status_code": "403",
  "api": {"operation": "GET api/Patient/(?P<key>[a-f0-9]{32})$"},
  "enrichments": {"source": "access_control", "event_name": "access_denied"}
}
```

A Canvas administrator, signed in as `jsmith`, opening a patient's chart:

```json
{
  "metadata": {
    "version": "1.1.0",
    "uid": "c41e7a2d-8b3f-4e19-a6d0-2f5c9b1e7a34",
    "product": {"name": "Canvas", "vendor_name": "Canvas Medical"},
    "tenant_uid": "acme",
    "labels": ["environment:production"],
    "correlation_uid": "9c2e4b6d8f0a2c4e6b8d0f1a3c5e7b9d"
  },
  "category_uid": 6,
  "class_uid": 6001,
  "activity_id": 2,
  "type_uid": 600102,
  "time": 1791999520000,
  "actor": {"user": {"uid": "412", "name": "jsmith"}},
  "src_endpoint": {
    "ip": "192.0.2.15",
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
  },
  "status_id": 1,
  "resources": [{"type": "patient", "uid": "381bf94ac3b269eedec9dc3f660a4cf0"}],
  "enrichments": {
    "source": "activity_log",
    "event_name": "chart_access",
    "impersonated_by": "canvas-support"
  }
}
```

## Plugin activity

Plugins execute in an isolated runner, and their activity is instrumented per plugin,
including outbound HTTP calls made through the SDK. Plugins can also emit their own
application logs — see [Plugin Logs](/sdk/plugin-logs/).

## Related

- [Platform Security Overview](/guides/platform-security-overview/)
- [Roles and Permissions](/guides/roles-and-permissions/)
- [Plugin Security Model](/guides/plugin-security-model/)
- [Provenance API](/api/provenance/)
- [EHI Export](/documentation/ehi-export/)
