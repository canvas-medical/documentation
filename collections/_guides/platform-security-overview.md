---
title: "Platform Security Overview"
---

This page describes how Canvas is deployed, where its trust boundaries sit, and which
security controls are in force before any plugin, integration, or custom code is
introduced. It is intended for security and compliance teams evaluating Canvas, and for
implementers who need to know which controls they inherit and which they own.

Canvas holds HITRUST CSF r2 certification. The certification report, SOC-equivalent
artifacts, and the most recent independent penetration test are available under NDA
through your Canvas contact.

## Deployment and tenancy model

Every Canvas customer runs on a **dedicated instance**: its own set of immutable
application containers and its own database. Customer data is separated at the database
level rather than by a row- or column-scoped partition inside a shared store, so there is
no query path from one customer's application to another customer's data.

Instances are hosted on Aptible, which runs on AWS in `us-east-1`, inside a segregated
virtual private cloud. Application containers are rebuilt from a pinned image on each
deploy rather than mutated in place.

## Trust boundaries

Requests cross five boundaries, each of which enforces its own controls:

| Boundary | Responsibility |
| --- | --- |
| Edge | TLS termination, IP allow-listing, rate limiting, WAF and DDoS protection |
| Core application | Authentication, session handling, role- and object-level authorization |
| Plugin runner | Isolated execution of customer plugin code — see [Plugin Security Model](/guides/plugin-security-model/) |
| FHIR API | Scoped, token-based access with patient-context enforcement |
| Per-customer database | Tenant-isolated persistence, encrypted at rest |

## Platform controls

These apply to every instance and are not customer-configurable.

### Encryption

Traffic to and between Canvas services is encrypted with TLS. Databases and disk volumes
are encrypted at rest with AES-256. Patient documents stored in object storage are
encrypted at rest with AES-256 server-side encryption.

### Identity and authentication

Canvas supports SSO via SAML, with multi-factor authentication enforced by your identity
provider. Failed-login lockout is applied to interactive sessions. Where an instance uses
Canvas-managed credentials rather than SSO, password policy — including minimum length,
complexity, and screening against known-breached and commonly-used passwords — is
enforced centrally.

### Authorization

Access is governed by role-based access control. Permissions are evaluated at two levels:

- **Model permissions** determine which record types a user may read or modify.
- **Object permissions** narrow that further to specific records, scoped by patient group.

Both are administered through roles and groups rather than granted to individuals
directly.

### Network

Each instance's externally reachable endpoints carry IP allow-lists backed by cloud
security groups. Internal services are not exposed to the public internet. Administrative
access to Canvas infrastructure requires authentication through the corporate identity
provider and traverses a VPN.

### Privileged access

Access to production containers is restricted by role. Sessions are recorded end to end,
and the resulting logs are retained and reviewable.

## Shared responsibility

Canvas operates the platform and its controls. The following remain with the customer:

| Area | Customer responsibility |
| --- | --- |
| Identity | Enforcing MFA, provisioning and deprovisioning users, periodic access review |
| Authorization | Assigning roles and groups according to least privilege |
| Plugins and extensions | Reviewing and approving code deployed to your instance — see [Plugin Security Model](/guides/plugin-security-model/) |
| Credentials | Custody of API keys, OAuth client secrets, and plugin secrets |
| Exported data | Protecting data once it leaves Canvas through an API, export, or replica |

{% include alert.html type="info" content="Canvas can configure your instance so that plugins reach production only through a release pipeline you control. See Deployment governance in the Plugin Security Model guide." %}

## Related

- [Plugin Security Model](/guides/plugin-security-model/)
- [Roles and Permissions](/guides/roles-and-permissions/)
- [Audit Logging and Telemetry](/guides/audit-logging-and-telemetry/)
- [Customer Authentication](/api/customer-authentication/)
- [Authentication Best Practices](/api/authentication-best-practices/)
