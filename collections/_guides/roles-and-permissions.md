---
title: "Roles and Permissions"
---

Access in Canvas is governed by role-based access control. This page explains how
authorization is evaluated, describes the roles every instance is provisioned with, and
outlines how to extend them for your organization.

## How authorization works

Canvas evaluates two independent levels of permission on every request.

**Model permissions** determine which record types a user may act on, and which actions
are allowed on each: view, add, change, or delete. A user who lacks the view permission
on a record type cannot read it anywhere in the application, including through the API.

**Object permissions** narrow that further to specific records. Object scope is expressed
through **patient groups**: a user may hold a permission on a record type in general but
only exercise it for patients within the groups assigned to them. This is how an
organization restricts a clinician to a panel, a site, or a program rather than the whole
patient population.

Both levels are always evaluated together. A user must satisfy the model permission and
the object permission — and be an active user — for access to be granted.

{% include alert.html type="info" content="Permissions are granted to roles, never directly to individuals. Adding or removing a user's access means changing their role assignments, which makes access reviews a question of who holds which role rather than an audit of per-user exceptions." %}

Some capabilities are gated by **named feature permissions** rather than by a record type
— printing, revenue, data integration, campaigns, the questionnaire builder, patient
activation, and prescription cancellation among them. These behave identically in
evaluation; they simply gate a feature rather than a model.

## Default roles

Every Canvas instance is provisioned with the roles below. They are grouped here by what
they are for; in the admin console they appear as a flat list.

### Broad functional roles

| Role | Grants |
| --- | --- |
| Administrative | Organization and practice-location configuration, staff records, note types, letter and questionnaire templates, and revenue configuration |
| Clinical | Clinical configuration and care-team management, lab and imaging report templates, protocol versions, and reporting |

### Record access, split by read and write

These are deliberately separate so that read access can be granted without write access.

| Role | Grants |
| --- | --- |
| Clinical read | View clinical records — notes, patients, lab and imaging reports, prescriptions, referrals, messages, and related clinical documents |
| Clinical write | Create and modify clinical records, including notes, plans, prescriptions, referrals, and reasons for visit |
| Profile read | View patient demographics, contacts, identification cards, and payment methods |
| Profile write | Modify patient demographics, coverage, consents, contacts, authorizations, and payment details |
| Document Read | View patient administrative documents |
| Document Write | Modify patient administrative documents |

### Feature and workflow access

| Role | Grants |
| --- | --- |
| Patient Create | Create new patient records |
| Schedule write | Create and modify appointments |
| Tasking Access | View and update tasks |
| Printing Access | Print from the chart |
| Revenue access | The revenue module and authorization management |
| Data integration Access | The data integration module |
| Patient Data Integration Access | Patient-level data integration tasks |
| Questionnaire Builder Access | The questionnaire builder |

### Security-sensitive roles

Treat these as privileged. They should be assigned narrowly and reviewed on a defined
cadence.

| Role | Grants |
| --- | --- |
| Staff Permissions Access | Manage roles, groups, staff permissions, and patient-group membership — in effect, the ability to grant access to others |
| Emergency Access | Break-glass access, recorded against a dedicated emergency-access record |
| Admin Lockout | View and clear failed-login lockouts |
| Lead | Manage multi-factor authentication devices for users, including TOTP, email, and SMS |

{% include alert.html type="warning" content="Staff Permissions Access is the role that can change other users' access, and Lead can manage their MFA devices. Both warrant the tightest assignment and the most frequent review of any role in the list." %}

Your instance may include additional roles introduced in later releases, or roles created
by your own administrators.

## Patient groups

Patient groups appear alongside roles in the admin console but behave differently: they
carry no model permissions of their own. Their purpose is object scoping — assigning a
user to a patient group determines which patients their permissions apply to.

Every instance is provisioned with an **All Patients** group. Narrower groups are created
per organization to reflect panels, sites, programs, or any other division that should
bound a user's reach.

## Extending the defaults

The default roles are a starting point, not a fixed set. Administrators with Staff
Permissions Access can create additional roles, and adjust the permissions on existing
ones, to match how the organization actually works. Both are done through the admin
console.

When you do, a few practices keep the model reviewable:

- Prefer creating a **new role** over broadening an existing one, so the default set stays
  a recognizable baseline.
- Grant **read and write separately** where the split exists, rather than defaulting to
  both.
- Scope by **patient group** wherever a user does not legitimately need the full
  population.
- Review assignments to the security-sensitive roles above on a defined cadence.

## Reviewing access

Because permissions are held by roles rather than individuals, an access review is a
review of role membership. The admin console lists the staff assigned to each role and the
patient groups scoping them.

Changes to roles, permissions, and staff records are captured in the audit trail — see
[Audit Logging and Telemetry](/guides/audit-logging-and-telemetry/) for what is recorded
and how to export it.

{% include alert.html type="info" content="Canvas can provide a complete role-to-model permission matrix for your instance on request, for use in a security review or access-control audit. Contact your Canvas representative." %}

## Related

- [Platform Security Overview](/guides/platform-security-overview/)
- [Audit Logging and Telemetry](/guides/audit-logging-and-telemetry/)
- [Plugin Security Model](/guides/plugin-security-model/)
