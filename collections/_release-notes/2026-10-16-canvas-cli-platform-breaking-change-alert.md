---
slug: canvas-cli-platform-2026-10-16
title: "Breaking change: the Canvas CLI moves to Canvas Platform on December 14, 2026"
date: 2026-10-16
layout: productupdates
tags: breaking-change sdk
feed_summary: |
  • Starting December 14, 2026, the Canvas CLI signs in through Canvas Platform. credentials.ini and canvas install stop working that day.
  • Before then: sign in with canvas login, deploy with canvas deploy, and switch CI pipelines to a service account. Plugins keep their names, and Canvas handles the rest.
---

Starting December 14, 2026, the Canvas CLI signs in through [Canvas Platform](https://platform.canvasmedical.com). After this date, `credentials.ini` and `canvas install` will stop working.

_Updated October 28, 2026: the upgrade is simpler than this note first described. Plugins are not renamed or moved, and Canvas handles the upgrade of your plugins._

**What your developers need to do before December 14:**

- Upgrade the Canvas CLI and sign in once with [`canvas login`](/sdk/canvas_cli/#signing-in-to-canvas-platform). _(requires Canvas CLI 0.244.0 or newer)_
- Once Canvas notifies you that your organization's plugins are upgraded, ship them with [`canvas deploy`](/sdk/canvas_cli/#canvas-deploy) where you used `canvas install`. The upgrade does not interrupt your running plugins, and they keep their names, variables, SimpleAPI URLs and custom data.
- If you deploy from a CI pipeline, create a [service account](/sdk/canvas_cli/#service-accounts-for-cicd) on the Credentials page in Canvas Platform and use its token in place of your instance credentials.

**Documentation:**

- [Upgrading to Canvas Platform](/guides/upgrading-to-canvas-platform/) covers the timeline, the workflow changes and common questions.
- The [Canvas CLI reference](/sdk/canvas_cli/) covers every command.

Questions? Submit the Canvas Platform Support Form.
