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
| Print | Yes | Note-print events |
| Chart access | Yes | Chart-open events, attributed to the user opening the chart |

Individual record reads within an already-opened chart are not enumerated separately;
chart access is recorded at the point the chart is opened.

Alongside the record audit trail, Canvas captures:

- **Authentication events** — sign-in successes and failures, and account lockouts.
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
above.

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
