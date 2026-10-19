---
slug: canvas-cli-platform-2026-10-16
title: "Breaking change: the Canvas CLI moves to Canvas Platform on December 14, 2026"
date: 2026-10-16
layout: productupdates
tags: breaking-change sdk
feed_summary: |
  • Starting December 14, 2026, the Canvas CLI signs in through Canvas Platform. credentials.ini and canvas install stop working that day.
  • Before then: upgrade the CLI, sign in with canvas login, move each live plugin over, and switch CI pipelines to a service account.
---

Starting December 14, 2026, the Canvas CLI signs in through [Canvas Platform](https://platform.canvasmedical.com). After this date, `credentials.ini` and `canvas install` will stop working.

**What your developers need to do before December 14:**

- Upgrade the Canvas CLI and sign in once with [`canvas login`](/sdk/canvas_cli/#signing-in-to-canvas-platform). _(requires Canvas CLI 0.244.0 or newer)_
- Move each live plugin over. Each one is renamed with your organization's prefix, gets its own repository, and is redeployed on every instance it runs on with [`canvas deploy`](/sdk/canvas_cli/#canvas-deploy).
- If you deploy from a CI pipeline, create a [service account](/sdk/canvas_cli/#service-accounts-for-cicd) on the Credentials page in Canvas Platform and use its token in place of your instance credentials.

**Documentation:**

- [Moving to Canvas Platform](/guides/moving-to-canvas-platform/) walks through moving a plugin step by step.
- The [Canvas CLI reference](/sdk/canvas_cli/) covers every command.

Questions? Submit the Canvas Platform Support Form.
