---
title: "Constance: Config (runtime configuration)"
layout: documentation
---

Several Canvas features are toggled per-instance via **Constance: Config**, a section of the Django admin interface that exposes runtime-tweakable settings. Release notes will sometimes reference one of these settings directly &mdash; for example, [`ENABLE_CANVAS_CHAT`](/release-notes/config-canvas-chat/), `COVERAGE_DEFAULT_QR_SCAN_MODAL`, `NOTE_BODY_TAB_LABEL`, or `ALLOW_PATIENT_ADDRESS_ZIP4_INTERNATIONAL` &mdash; without explaining where the setting lives or who can change it. This page covers both.

## Where to find Constance: Config

In your Canvas admin, **Settings &rarr; Constance &rarr; Config**. The **Constance** section appears in the left sidebar of the admin index above similarly-grouped admin apps. Inside, find the setting by name (settings are listed alphabetically) and edit the **Value** column. Boolean settings show a checkbox; string and numeric settings show a text input. Click `SAVE` at the bottom to apply.

Changes take effect immediately for the instance you're editing &mdash; no restart, no deploy. The setting is per-instance, so changing it on a dev instance does not affect production.

## Who can access it

Constance: Config is admin-level functionality. **Staff who hold the "Administrative Developer" (AD) role on your Canvas instance get access to the Constance section in admin.** Standard staff accounts that have not been granted the AD role will not see the Constance section in the admin sidebar.

A small number of settings within Constance: Config are reserved for Canvas Medical engineering and will not appear even to AD-role staff. These are typically settings that govern infrastructure-level behavior (e.g. service endpoint overrides, integration credentials, internal feature flags Canvas is still validating). If a release note references a setting and you cannot see it in your admin even after confirming you hold the AD role, that's the most likely reason; contact [Canvas support](https://portal.usepylon.com/canvas-medical/forms/standard){:target="_blank"} to request the change on your behalf.

## Granting the Administrative Developer role

If you need a user to be able to change Constance settings:

1. **An existing administrator at your instance** can grant the AD role to another staff member via the usual staff role management flow (Settings &rarr; Staff &rarr; select the staff member &rarr; assign the **Administrative Developer** role).
2. **If no one on your team currently has the AD role**, contact [Canvas support](https://portal.usepylon.com/canvas-medical/forms/standard){:target="_blank"} and they can assign it on your behalf.

{% include alert.html type="warning" content="<b>The Administrative Developer role is broad.</b> It exposes runtime configuration that affects the whole instance, plus other admin surfaces beyond Constance. Grant it deliberately, only to the people who need to administer instance-wide settings." %}

## Why a setting may not appear

If a release note mentions a Constance setting that you do not see in **Constance: Config**, the most common reasons are:

- **Your account does not hold the Administrative Developer role.** Confirm this first &mdash; the entire Constance section is hidden, not just the missing setting.
- **The setting is root-restricted.** A small set of Constance settings is reserved for Canvas Medical engineering and will not appear even to AD-role staff (see above). If you need such a setting changed, open a support ticket.
- **The setting hasn't shipped to your instance yet.** Constance settings are added in code; an instance that's behind on releases will not show settings added in a newer version. Check the [Release Notes](/release-notes/) for the version that introduced the setting and confirm your instance is on or past it.
- **You're looking at the wrong instance.** Settings are per-instance; a setting flipped on production will not show as changed on a dev instance and vice versa.
