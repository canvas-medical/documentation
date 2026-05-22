---
title: "Constance: Config (runtime configuration)"
layout: documentation
---

Several Canvas features are toggled per-instance via **Constance: Config**, a section of the Django admin interface that exposes runtime-tweakable settings. Release notes will sometimes reference one of these settings directly &mdash; for example, [`ENABLE_CANVAS_CHAT`](/release-notes/config-canvas-chat/), `COVERAGE_DEFAULT_QR_SCAN_MODAL`, `NOTE_BODY_TAB_LABEL`, or `ALLOW_PATIENT_ADDRESS_ZIP4_INTERNATIONAL` &mdash; without explaining where the setting lives or who can change it. This page covers both.

## Where to find Constance: Config

In your Canvas admin, **Settings &rarr; Constance &rarr; Config**. The Constance section appears in the left sidebar of the admin index above similarly-grouped admin apps. Inside, find the setting by name (settings are listed alphabetically) and edit the **Value** column. Boolean settings show a checkbox; string and numeric settings show a text input. Click `SAVE` at the bottom to apply.

Changes take effect immediately for the instance you're editing &mdash; no restart, no deploy. The setting is per-instance, so changing it on a dev instance does not affect production.

## Who can access it

**Constance: Config is restricted to Django superusers.** Standard staff accounts &mdash; even with every per-model permission granted and full membership in admin groups &mdash; will not see the **Constance** section in the admin sidebar. This is a global gate inside the underlying `django-constance` library: the admin view defers to a superuser-only check rather than a granular per-setting permission, so there is no group or role short of superuser that exposes it.

If you need a user to be able to change Constance settings:

1. An **existing superuser at your instance** can promote another staff member: **Settings &rarr; Users &rarr; (select user) &rarr; "Superuser status"** checkbox, then save.
2. If **no one on your team is currently a superuser**, contact [Canvas support](https://portal.usepylon.com/canvas-medical/forms/standard){:target="_blank"} and they can make the change on your behalf.

{% include alert.html type="warning" content="<b>Superuser is broad.</b> A superuser can access every model in the admin, run actions you have not enabled for regular staff, and edit configuration that affects the whole instance. Grant it deliberately and only to the people who need to administer instance-wide settings." %}

## Why a setting may not appear

If a release note mentions a Constance setting that you do not see in **Constance: Config**, the most common reasons are:

- **Your account is not a superuser.** Confirm this first &mdash; the entire Constance section is hidden, not just the missing setting.
- **The setting hasn't shipped to your instance yet.** Constance settings are added in code; an instance that's behind on releases will not show settings added in a newer version. Check the [Release Notes](/release-notes/) for the version that introduced the setting and confirm your instance is on or past it.
- **You're looking at the wrong instance.** Settings are per-instance; a setting flipped on production will not show as changed on a dev instance and vice versa.
