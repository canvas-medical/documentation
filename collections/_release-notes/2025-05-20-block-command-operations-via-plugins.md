---
title: Block Command Deletions and Commits via Plugin Validation
date: 2025-05-20
layout: productupdates
tags: plugins sdk enhancement
---

Plugins can now return a `CommandValidationErrorEffect` from `PRE_DELETE` and `PRE_COMMIT` event handlers to block command operations with custom error messages.

When a handler returns this effect, the operation is aborted and validation errors appear in the Canvas UI. This is useful for scenarios like preventing prescription deletions while an order is being processed by an external pharmacy.

See the [Command Validation](/sdk/effect-command-validation/) documentation for details and examples.
