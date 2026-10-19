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

Patient-group scope applies however a record is reached. Lists and direct lookups by
ID return only records for patients in the user's groups. An appointment for a
patient outside those groups still appears on the schedule, but without its subject, note,
or patient address.

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
| Revenue access | The revenue module, including claims, payments, coverage and eligibility information, remittances, and authorization management |
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

Turning emergency access on or off requires the Emergency Access role.

Your instance may include additional roles introduced in later releases, or roles created
by your own administrators.

## Patient groups

Patient groups appear alongside roles in the admin console but behave differently: they
carry no model permissions of their own. Their purpose is object scoping — assigning a
user to a patient group determines which patients their permissions apply to.

Every instance is provisioned with an **All Patients** group. Narrower groups are created
per organization to reflect panels, sites, programs, or any other division that should
bound a user's reach.

## Permissions for common workflows

Some workflows need more than one permission. Use this table when you design a role for
billing staff, front-desk staff, or another restricted group. Check that the role includes
every permission in each row it needs. Where a row mentions patient-group access, the
user must also be in a group that includes the patient.

| Workflow | Required permissions |
| --- | --- |
| View coverage and eligibility information | Revenue access, and patient-group access. Coverage and eligibility requests and responses for patients outside the user's groups aren't returned |
| Change, order, expire, or remove a coverage, or remove a coverage card photo | Change permission on coverage, and patient-group access. Copay and coinsurance also require revenue access. Without it, the rest of a new or edited coverage saves, but its copay and coinsurance stay unchanged |
| Update a coverage's eligibility summary | Change permission on coverage, revenue access, and patient-group access |
| Change claims and their coverages, snoozes, labels, comments, activity logs, and manual remits | Revenue access. Batch claim actions apply only to claims for patients the user has patient-group access to |
| Add, update, or delete a prior authorization, or generate a batch of patient statements | Revenue access |
| Collect a payment on a claim | Add permission on payment collections, revenue access, and patient-group access. A saved card can be charged only for the patient it belongs to |
| Create, edit, or delete a payer | Add, change, or delete permission on payers, which the admin console lists as insurers. Any signed-in user can search for and view payers, so staff can enter coverage without these permissions |
| Process ERAs in the admin console | Revenue access and view permission on ERA process jobs |
| Select claims for an installment plan in the admin console | View permission on installment plans to see the selection, and change permission to save it |
| Create, view, or update a campaign, or add an intervention to one | Campaign access, plus membership in the **All Patients** group when that group is enabled, because a campaign reaches every patient |
| Remove a care team member | Change permission on care team memberships, and patient-group access |
| Send, edit, or delete a message | Patient-group access. No model permission is required. A message that has been sent, or that a campaign created, can only be marked read. It can't be sent again, edited, or deleted. If the message's template restricts editing, its content can't be changed |

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
