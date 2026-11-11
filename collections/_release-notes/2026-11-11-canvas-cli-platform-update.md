---
slug: canvas-cli-platform-2026-11-11
title: "Canvas CLI updates ahead of the Canvas Platform upgrade"
date: 2026-11-11 12:00:00
layout: productupdates
tags: sdk
feed_summary: |
  • Canvas CLI 1.0: list, enable, disable, config, uninstall, logs, and namespace commands work through Canvas Platform once you sign in.
  • canvas deploy runs canvas validate first, and canvas deploy --branch deploys a branch to your test instances.
  • Keep using credentials.ini until Canvas says your plugins are upgraded, then run canvas login before December 14, 2026.
---

The Canvas CLI has new releases to get you ready for the [Canvas Platform upgrade](/guides/upgrading-to-canvas-platform/). Upgrade to the latest Canvas CLI with `pip install --upgrade canvas`, or `uv tool upgrade canvas` if you installed it with `uv`.

<span class="tag-sdk">sdk</span>

### What's new

- **More commands through Canvas Platform.** Once you sign in with `canvas login`, these commands go through Canvas Platform for the plugins and instances it manages, with no `credentials.ini` client needed. See [which commands go through Canvas Platform](/sdk/canvas_cli/#which-plugins-go-through-canvas-platform).
  - `enable`, `disable`, `config list`, `config set`, `config unset`, and `uninstall` _(requires Canvas CLI 1.0.0 or newer)_
  - `list` and the `namespace` commands _(requires Canvas CLI 1.0.0 or newer)_
  - `logs` _(requires Canvas CLI 0.268.0 or newer)_

- **Validation before every deploy.** `canvas deploy` runs `canvas validate` before it pushes, so a plugin that wouldn't load is caught on your machine. See [canvas deploy](/sdk/canvas_cli/#canvas-deploy). _(requires Canvas CLI 0.268.0 or newer)_

- **Branch deployments.** `canvas deploy --branch` deploys a branch other than `main` to your organization's test instances, so you can try work that hasn't merged. _(requires Canvas CLI 0.268.0 or newer)_

{% include alert.html type="info" content="<strong>Keep using <code>credentials.ini</code> until Canvas tells you your plugins are upgraded.</strong> Signing in sooner sends these commands through Canvas Platform, which refuses plugins and instances it doesn't manage yet. Once you hear from us, sign in with <code>canvas login</code> before December 14, 2026. See <a href='/guides/upgrading-to-canvas-platform/'>Upgrading to Canvas Platform</a>." %}
