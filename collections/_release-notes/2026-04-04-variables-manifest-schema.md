---
title: 04.04.2026
layout: productupdates
tags: sdk
date: 2026-04-04
---

Today's release includes the following updates:

<span class="tag-sdk">sdk</span>

- Plugin manifest configuration now uses a [`variables`](/sdk/secrets/) array format instead of the flat `secrets` string array. Each variable is an object with a `name` field and optional `sensitive` boolean. Variables marked as `sensitive: true` behave like the previous secrets (write-only). The legacy `secrets` format is deprecated and displays a warning during `canvas validate-manifest`.
