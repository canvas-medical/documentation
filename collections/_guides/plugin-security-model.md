---
title: "Plugin Security Model"
guide_for:
- /sdk/
---

Plugins let you extend Canvas with your own logic. Because that logic runs inside a
system holding patient data, the plugin runtime is deliberately constrained. This page
describes those constraints and the deployment controls available to you, so your
security team can evaluate what plugin code can and cannot do.

## Execution model

Plugins do not manipulate Canvas data directly. They **subscribe to events** and **return
declarative effects** that the platform interprets and applies.

That indirection is the core of the model. A plugin describes an intended outcome — add a
banner, create a command, send a notification — and the platform decides whether and how
to carry it out, applying the same validation and permission rules it applies to any
other write. A plugin cannot reach past the effect layer to mutate records itself.

## Runtime isolation

The plugin runner executes customer code under several layers of containment:

- **Process and user isolation.** Plugin code runs in a separate operating-system user
  and process from the core application.
- **Restricted interpreter.** Code executes in a RestrictedPython sandbox with an
  explicit allowlist of importable modules. Modules outside that list are rejected at
  load time, not at run time.
- **No direct system access.** Plugins have no direct database connection, no filesystem
  access, and no operating-system access.
- **Constrained network surface.** Outbound communication is limited to HTTP and HTTPS
  through the SDK's supported clients. Raw sockets and non-HTTP protocol libraries are
  not available in the sandbox.
- **Package integrity.** Plugin packages are checksummed, and the manifest is validated
  before a plugin is installed.

Because the module allowlist is enforced when the plugin is loaded, a plugin that
attempts a disallowed import fails to install rather than failing partway through a
patient-facing workflow.

## Secrets

Plugins declare the secrets they need in their manifest, and values are supplied per
instance. Secret values are **write-only** from the plugin author's perspective: they can
be set and used at runtime, but not read back out through the interface used to configure
them.

Treat plugin secrets like any other production credential — scope them narrowly, and
rotate them on the same cadence as the rest of your estate.

## API access

Where a plugin or external application reaches Canvas through the FHIR API, access is
scoped by OAuth token, and patient-context enforcement applies to patient-scoped launches.
See [Customer Authentication](/api/customer-authentication/) and
[Authentication Best Practices](/api/authentication-best-practices/).

## Deployment governance

### Who can install

Installing or updating a plugin is an authenticated operation: it requires an OAuth token
carrying the plugin scope for your instance. Controlling who holds that credential is the
primary control over what reaches your production environment, and it is a control your
organization owns.

### Installing from your own pipeline

Most organizations keep plugin source in their own repository and install from their own
continuous-integration pipeline rather than from individual workstations. Under that
arrangement the installing credential lives in CI, and your existing review process —
pull-request approval, required checks, protected branches — is what gates production.

Canvas recommends this pattern where your change-management policy requires documented
human review before code runs in production.

{% include alert.html type="info" content="Plugins built through Canvas Studio follow their own staged workflow, with explicit approval steps before a project is published." %}

### Environment separation

Instances are provisioned per environment, and release channels let you promote a plugin
through a lower environment before it reaches production. Deploys are pinned to a
specific commit, so what you reviewed is what runs.

### Change tracking

Plugin deployment activity is tracked, and plugin runtime activity is instrumented per
plugin. Combined with the audit trail described in
[Audit Logging and Telemetry](/guides/audit-logging-and-telemetry/), this gives you a
record of both what changed and what the plugin did.

## Recommended practices

- Hold the installing credential in CI rather than on workstations, so your pull-request
  review is what gates production.
- Scope plugin secrets to the minimum required, and rotate them on your normal cadence.
- Exercise plugins in a lower environment before promoting to production.

## Related

- [Platform Security Overview](/guides/platform-security-overview/)
- [Roles and Permissions](/guides/roles-and-permissions/)
- [Audit Logging and Telemetry](/guides/audit-logging-and-telemetry/)
- [Your First Plugin](/guides/your-first-plugin/)
- [Plugin Logs](/sdk/plugin-logs/)
